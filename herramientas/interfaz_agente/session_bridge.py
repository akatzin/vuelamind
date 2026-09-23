#!/usr/bin/env python3
"""
session_bridge.py — puente HTTP local a sesiones de Claude Code.

Qué hace: un servicio HTTP en loopback (sin token) que crea y maneja VARIAS
conversaciones de Claude Code en esta máquina, cada una direccionable por nombre.
No se engancha a una sesión interactiva ya abierta (eso no tiene vía soportada);
maneja conversaciones que él mismo crea/continúa por la vía headless soportada:

    claude -p "<msg>" [--resume <sessionId>] --output-format stream-json --verbose --model <m>

que continúa la conversación guardada, corre un turno, y devuelve JSON limpio.

Seguridad (decidido para este dominio):
  - Escucha SOLO en 127.0.0.1. El acceso "desde fuera" es por TÚNEL SSH:
        ssh -N -L 8850:127.0.0.1:8850 <usuario>@<esta-máquina>
    Así nunca se abre nada a 0.0.0.0 (evita el #119).
  - SIN token: el modelo de confianza es "solo esta máquina". Dos candados en su
    lugar, porque loopback NO basta contra el navegador:
      · allowlist de Host  → solo 127.0.0.1 / localhost (mata el DNS-rebinding).
      · chequeo de Origin  → los métodos que cambian estado (POST/DELETE) rechazan
        un Origin ajeno; el navegador siempre lo manda verídico en cross-site, así
        que una página maliciosa no puede disparar una sesión (CSRF/RCE).
    Lo que queda expuesto —y se asume— es otro usuario/proceso LOCAL en la máquina.
  - Nunca usa shell=True; los argumentos van como lista (sin inyección).
  - Modelo por defecto: opus. En este Model Garden haiku NO está aprovisionado,
    así que un subproceso sin --model explícito a un modelo válido falla (404).

Uso:
    python3 session_bridge.py                 # 127.0.0.1:8850
    PORT=9000 python3 session_bridge.py       # otro puerto

Endpoints (JSON):
    GET  /health                         → {"ok": true}                      (sin auth)
    GET  /sessions                       → registro local + 'claude agents --json --all'
    POST /sessions        {name, prompt, cwd?, model?}   → crea; devuelve {name, session_id, text}
    POST /sessions/<name>/messages  {message}            → continúa (bloquea al fin); {session_id, text}
    POST /sessions/<name>/stream    {message}            → continúa con progreso NDJSON en vivo
    POST /sessions/<name>/deliver   {message}            → ENTREGAR Y SOLTAR: arranca el turno,
                                                           responde al 'init' (llegó) y se desengancha
                                                           sin matar el turno; {name, session_id, started}
    DELETE /sessions/<name>                               → olvida del registro (y stop si sigue viva)

El modo "entregar y soltar" (deliver) existe para despertar una casa que opera en
sesiones HEADLESS: quien dispara (un trigger de mensajería, un cron) sólo necesita
saber que el aviso LLEGÓ —que el turno arrancó—, no esperar a que TERMINE, que es
trabajo ajeno de duración no acotada. Desacopla despertar de completar; el turno
corre hasta el final aunque el cliente cierre la conexión.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import threading
import io
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote


# ------------------------------------------------------ config por archivo (portable)
def _load_env_file() -> None:
    """Lee ~/.claude/vuelamind-rc.env (KEY=VALUE por línea) y puebla os.environ
    SIN pisar lo que ya venga del entorno real. Es la vía portable: el autostart
    (launchd / Tarea Programada / systemd) solo lanza python; la config vive aquí."""
    path = Path(os.environ.get("VUELAMIND_RC_ENV",
                               Path.home() / ".claude" / "vuelamind-rc.env"))
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


# Este archivo usa anotaciones de 3.10 (`list | None`). En 3.9 NO es error de sintaxis:
# revienta al EVALUAR el primer `def` que las lleva, ya empezado el import, con un
# TypeError que no explica nada. MEDIDO el 2026-09-11: con el python3 de fábrica de macOS
# (3.9.6) el servicio no arrancaba y el instalador terminaba bien igual. En Windows el
# autostart usa pythonw.exe, que corre SIN ventana: ahí el mismo error no se ve en ningún
# sitio. Por eso el corte va ANTES, en sintaxis que 3.9 entiende, y dice qué hacer.
if sys.version_info < (3, 10):
    sys.exit(
        "vuelamind-rc necesita Python 3.10 o superior; este es %d.%d (%s).\n"
        "  El servicio usa anotaciones `X | None`, que en 3.9 fallan al importar.\n"
        "  Instala uno mas nuevo y reinstala apuntando a el, o invocalo con ese binario."
        % (sys.version_info[0], sys.version_info[1], sys.executable))

_load_env_file()

# Sin consola —`pythonw` bajo el Programador— el servicio se queda MUDO: no hay dónde
# escribir ni un arranque ni un error. Se le da una bitácora para que el silencio no sea
# la única señal.
if sys.stderr is None or sys.stdout is None:
    try:
        _bitacora = open(Path.home() / ".claude" / "vuelamind-rc.log", "a",
                         encoding="utf-8", errors="replace", buffering=1)
        if sys.stdout is None:
            sys.stdout = _bitacora
        if sys.stderr is None:
            sys.stderr = _bitacora
    except Exception:
        pass   # sin bitácora se sigue: la guarda de log_message ya evita el crash

# TODA lectura, escritura y tubería de este archivo declara `encoding="utf-8"`, y no es
# manía: `read_text()` sin codificación usa la del SISTEMA — UTF-8 en Unix, CP1252 en
# Windows. MEDIDO en Windows 11 el 2026-09-11: el servicio arrancaba, el puerto abría, y
# al servir su PROPIA página moría con UnicodeDecodeError en el byte 0x8f. El archivo
# estaba bien; el lector estaba mal. Lo mismo vale para las tuberías con el CLI: por ahí
# viajan los acentos de cada turno.

# ---------------------------------------------------------------- configuración
HOST = "127.0.0.1"                                   # loopback SIEMPRE; salir por túnel SSH
PORT = int(os.environ.get("PORT", "8850"))   # canonico del marco; 8787 colisiona
DEFAULT_MODEL = os.environ.get("BRIDGE_MODEL", "")   # vacio = el default del CLI.
# El canon NO congela un id de modelo: "solo opus" fue un hecho del Model Garden de
# origen, no del marco, y un id fijo revienta donde no este aprovisionado.
DEFAULT_CWD = os.environ.get("BRIDGE_CWD", str(Path(__file__).resolve().parent.parent))
TURN_TIMEOUT = int(os.environ.get("BRIDGE_TIMEOUT", "600"))   # segundos por turno
# entregar-y-soltar: cuánto espera el handler el evento 'init' antes de rendirse.
# El turno YA arranca en segundos; este tope solo evita que el handler cuelgue si
# claude no emite init (p.ej. no arrancó). El turno, si arrancó, sigue en background.
DELIVER_INIT_TIMEOUT = int(os.environ.get("BRIDGE_DELIVER_INIT_TIMEOUT", "120"))
# ventana de contexto del modelo, para pintar el % en vivo. El valor autoritativo
# llega en result.modelUsage.contextWindow; éste es el default mientras el turno
# corre (aún no hay result). 200000 = opus/sonnet en este despliegue.
CONTEXT_WINDOW = int(os.environ.get("BRIDGE_CONTEXT_WINDOW", "200000"))
# Ruta del master del marco, si esta maquina lo tiene a mano (p.ej. dentro del
# contenedor, donde el canon viene horneado). El puente NO la sabe por si mismo y
# no se inventa una ruta por omision: sin esto, la pagina no ofrece nacer un
# dominio, que es mejor que ofrecer un boton que abre un archivo inexistente.
MASTER = os.environ.get("BRIDGE_MASTER", "")


def _dentro_de(hijo: str, padre: str) -> bool:
    """True si `hijo` cuelga de `padre` una vez resueltos los dos. Es lo que impide
    que crear un agente escriba carpetas en cualquier punto del disco: el puente
    crea directorios SOLO bajo el suyo."""
    try:
        h = Path(hijo).resolve()
        pa = Path(padre).resolve()
        return h == pa or pa in h.parents
    except Exception:
        return False


def _identidad(d: Path) -> dict:
    """Lee `asistente:` y `dominio:` del frontmatter del panorama (`0_*.md`), que la
    v3.9 del marco manda escribir. Mira el propio directorio y UN nivel adentro,
    que es donde cae el vault segun la convencion.

    Lo que NO hace, y es deliberado: deducir el nombre leyendo la prosa. Un dominio
    que no lo declara vuelve con los campos vacios y quien lo muestre dira que no
    esta declarado. Un nombre inventado por el puente se veria igual de cierto."""
    for patron in ("0_*.md", "*/0_*.md"):
        for nota in sorted(d.glob(patron)):
            try:
                texto = nota.read_text(encoding="utf-8", errors="replace")[:4000]
            except Exception:
                continue
            if not texto.startswith("---"):
                continue
            fin = texto.find("\n---", 3)
            fm = texto[3:fin] if fin > 0 else ""
            campos = {}
            for linea in fm.splitlines():
                if ":" in linea and not linea.startswith(" "):
                    k, v = linea.split(":", 1)
                    campos[k.strip()] = v.strip()
            if "asistente" in campos or "dominio" in campos:
                return {"asistente": campos.get("asistente", ""),
                        "dominio": campos.get("dominio", ""),
                        "panorama": nota.name}
            return {"asistente": "", "dominio": "", "panorama": nota.name}
    return {"asistente": "", "dominio": "", "panorama": ""}

CLAUDE = os.environ.get("BRIDGE_CLAUDE_BIN") or shutil.which("claude") or \
    str(Path.home() / ".local/bin/claude")


def _invocacion(binario: str) -> list:
    """Cómo hay que LLAMAR al CLI, que no siempre es «ejecútalo».

    En Windows la instalación por npm deja un `claude.cmd`, y un .cmd/.bat NO lo puede
    lanzar `CreateProcess` — que es lo que hace subprocess sin shell: falla con
    «no es una aplicación Win32 válida». Hay que pasar por `cmd /c`.

    INFERIDO (2026-09-11): no medido. La VM donde se probó Windows tenía el CLI como
    `claude.exe` y por eso este camino nunca se ejerció allí; el instalador, en cambio, SÍ
    busca `claude.cmd` — o sea que el caso existe y nadie ha pasado por él. Se escribe
    defensivo en vez de esperar a que alguien lo descubra en su propia máquina.
    """
    if os.name == "nt" and binario.lower().endswith((".cmd", ".bat")):
        return ["cmd", "/c", binario]
    return [binario]


CLAUDE_ARGS = _invocacion(CLAUDE)

HTML_FILE = Path(__file__).resolve().parent / "session_bridge.html"
CONF_DIR = Path.home() / ".claude"
REGISTRY_FILE = Path(os.environ.get("BRIDGE_REGISTRY", CONF_DIR / "vuelamind-bridge-sessions.json"))

# candados que sustituyen al token (ver docstring). Host y Origin permitidos.
_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", "[::1]"}
SAME_ORIGINS = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}

_registry_lock = threading.Lock()
NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")        # nombres seguros para direccionar


# ---------------------------------------------------------------- registro
# Turnos que se estan drenando AHORA, por nombre de sesion. Existe para que el endpoint
# de recuperacion pueda decir "sigue corriendo" en vez de dejar al cliente girando sobre
# un turno que ya murio: sin esto, "todavia no hay respuesta" y "no la va a haber nunca"
# se ven identicos desde fuera.
TURNOS_VIVOS: set = set()
_VIVOS_LOCK = threading.Lock()


def marcar_vivo(nombre: str, vivo: bool) -> None:
    with _VIVOS_LOCK:
        TURNOS_VIVOS.add(nombre) if vivo else TURNOS_VIVOS.discard(nombre)


def esta_en_vuelo(nombre: str) -> bool:
    with _VIVOS_LOCK:
        return nombre in TURNOS_VIVOS


def ultimo_del_transcript(session_id: str) -> dict:
    """Lee la ultima respuesta que el CLI YA escribio en disco para esa sesion.

    EL HUECO QUE CIERRA: si el navegador pierde el stream -pestana recargada, red
    interrumpida, maquina dormida- el turno NO se pierde: el CLI lo sigue y lo escribe en
    su propio transcript. Lo que se pierde es el CAMINO, no el texto. Esto lo va a buscar.

    NO le pide nada al modelo: no cuesta tokens, no puede alucinar, no reescribe nada. Es
    el texto que ya existe, leido del archivo que lo guarda.

    POR QUE SE BUSCA POR NOMBRE DE ARCHIVO Y NO POR RUTA CALCULADA: el CLI nombra cada
    transcript como su session_id, que es unico, y lo guarda bajo una carpeta derivada del
    cwd con una regla de sustitucion que no esta documentada -medido: `/` y `_` pasan a
    `-`, y adivinar el resto seria inventar-. Buscarlo por su nombre no depende de esa
    regla, asi que no se rompe el dia que cambie.
    """
    # Todas las salidas traen LAS MISMAS CLAVES. Una respuesta que a veces incluye
    # `terminado` y a veces no obliga a cada cliente a adivinar la forma, y el que adivine
    # mal no falla: lee `undefined` y sigue. MEDIDO mientras se probaba esto: el propio
    # guion de prueba reventó con KeyError en el primer sondeo, antes de que existiera el
    # transcript.
    raiz = Path.home() / ".claude" / "projects"
    if not raiz.is_dir():
        return {"hay": False, "terminado": False, "texto": "", "por_que": "no existe ~/.claude/projects"}
    archivo = next(raiz.glob(f"*/{session_id}.jsonl"), None)
    if archivo is None:
        return {"hay": False, "terminado": False, "texto": "", "por_que": "esa sesion no tiene transcript todavia"}
    ultimo_asistente = ultimo_usuario = None
    try:
        with archivo.open(encoding="utf-8", errors="replace") as fh:
            for linea in fh:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    d = json.loads(linea)
                except json.JSONDecodeError:
                    continue                  # una linea a medio escribir no invalida el resto
                if d.get("type") == "assistant":
                    ultimo_asistente = d
                elif d.get("type") == "user":
                    ultimo_usuario = d
    except OSError as e:
        return {"hay": False, "terminado": False, "texto": "", "por_que": f"no se pudo leer el transcript: {e}"}
    if ultimo_asistente is None:
        return {"hay": False, "terminado": False, "texto": "", "por_que": "el transcript no tiene ninguna respuesta todavia"}

    bloques = (ultimo_asistente.get("message") or {}).get("content") or []
    texto = "\n\n".join(b.get("text", "") for b in bloques if b.get("type") == "text").strip()
    t_asis = ultimo_asistente.get("timestamp") or ""
    t_usua = (ultimo_usuario or {}).get("timestamp") or ""
    # Si lo ultimo escrito es una pregunta y no una respuesta, el turno SIGUE en vuelo.
    # Decirlo importa: ensenar la respuesta ANTERIOR como si fuera la de ahora seria
    # justo el modo de fallo que este puente lleva semanas persiguiendo.
    terminado = bool(t_asis) and (not t_usua or t_asis >= t_usua)
    return {"hay": bool(texto), "texto": texto, "cuando": t_asis, "terminado": terminado,
            "stop_reason": (ultimo_asistente.get("message") or {}).get("stop_reason"),
            "por_que": "" if texto else "la ultima respuesta no trae texto, solo herramientas"}


def historial_del_transcript(session_id: str, limite: int = 50) -> dict:
    """Reconstruye la conversacion desde el transcript que el CLI ya escribio.

    EL HUECO QUE CIERRA: la pagina guarda la conversacion en el navegador que la escribio.
    Abrir el puente desde otra ventana, otro perfil o -su caso de uso declarado- otra maquina
    por tunel, ensena la sesion viva y el chat EN BLANCO. La conversacion existe: esta en el
    transcript del CLI, que es el mismo archivo del que lee la recuperacion.

    SE RECONSTRUYEN SOLO LOS TEXTOS, no las llamadas a herramientas. La pagina nunca guardo
    los pasos de un turno -viven en el panel de progreso y mueren con el-, asi que incluirlos
    aqui daria a la segunda ventana un historial que la primera nunca tuvo: dos vistas
    distintas de la misma sesion. Se reconstruye lo que habia, no lo que el disco guardo.
    """
    raiz = Path.home() / ".claude" / "projects"
    archivo = next(raiz.glob(f"*/{session_id}.jsonl"), None) if raiz.is_dir() else None
    if archivo is None:
        return {"hay": False, "mensajes": [], "parcial": False,
                "por_que": "esa sesion no tiene transcript todavia"}
    mensajes = []
    try:
        with archivo.open(encoding="utf-8", errors="replace") as fh:
            for linea in fh:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    d = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                tipo = d.get("type")
                if tipo not in ("user", "assistant"):
                    continue
                c = (d.get("message") or {}).get("content")
                if tipo == "user":
                    texto = c if isinstance(c, str) else "\n".join(
                        b.get("text", "") for b in (c or []) if b.get("type") == "text")
                else:
                    texto = "\n\n".join(b.get("text", "") for b in (c or [])
                                         if b.get("type") == "text")
                texto = (texto or "").strip()
                if texto:
                    mensajes.append({"role": "user" if tipo == "user" else "asst",
                                     "text": texto})
    except OSError as e:
        return {"hay": False, "mensajes": [], "parcial": False,
                "por_que": f"no se pudo leer el transcript: {e}"}
    total = len(mensajes)
    parcial = total > limite
    return {"hay": bool(mensajes), "mensajes": mensajes[-limite:], "total": total,
            "parcial": parcial, "por_que": "" if mensajes else "el transcript no trae textos"}


def guardar_ventana(nombre: str, win) -> None:
    """Anota la ventana REAL que ese modelo demostro, para que el turno siguiente no
    empiece midiendo contra una suposicion. Se guarda por sesion porque es propiedad del
    modelo con el que esa sesion corre, no de la maquina."""
    if not win:
        return
    with _registry_lock:
        reg = load_registry()
        meta = reg.get(nombre)
        if meta is not None and meta.get("context_window") != win:
            meta["context_window"] = win
            save_registry(reg)


def load_registry() -> dict:
    if REGISTRY_FILE.exists():
        try:
            return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_registry(reg: dict) -> None:
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2), encoding="utf-8")
    # En Windows esto NO protege el archivo: `chmod` solo toca el bit de solo-lectura
    # y los permisos los hereda del perfil de usuario. No falla, y por eso no se nota.
    # Declarado en 2026-09-11: en Windows la protección real pide ACLs (`icacls`).
    REGISTRY_FILE.chmod(0o600)


# ---------------------------------------------------------------- claude headless
import base64 as _base64

# tipos que sabemos pasar como bloque nativo (MEDIDO en Vertex/opus 2026-09-10)
IMAGE_TYPES = ("image/png", "image/jpeg", "image/gif", "image/webp")
DOC_TYPES = ("application/pdf",)


def build_content(text: str, attachments: list | None) -> list:
    """Arma la lista de bloques de contenido para un mensaje de usuario.

    text        → bloque {"type":"text"} (si no está vacío).
    attachments → lista de {name, media_type, data(base64)}. Imágenes van como
                  bloque 'image'; PDF como 'document'; texto como bloque de texto
                  rotulado. Tipos no soportados se ignoran (el cliente ya avisa).
    """
    blocks: list = []
    if text:
        blocks.append({"type": "text", "text": text})
    for a in attachments or []:
        mt = (a.get("media_type") or "").lower().split(";")[0].strip()
        data = a.get("data") or ""
        name = a.get("name") or "archivo"
        if not data:
            continue
        if mt in IMAGE_TYPES or mt.startswith("image/"):
            blocks.append({"type": "image",
                           "source": {"type": "base64", "media_type": mt, "data": data}})
        elif mt in DOC_TYPES:
            blocks.append({"type": "document",
                           "source": {"type": "base64", "media_type": mt, "data": data}})
        elif mt.startswith("text/"):
            try:
                txt = _base64.b64decode(data).decode("utf-8", "replace")
                blocks.append({"type": "text",
                               "text": f"--- Archivo adjunto: {name} ---\n{txt}"})
            except Exception:
                pass
    if not blocks:                       # nunca mandes contenido vacío
        blocks.append({"type": "text", "text": ""})
    return blocks


# --- niveles de permiso de las sesiones que crea el puente (MEDIDO 2026-09-10)
#   full  → autonomía total: ejecuta python/red/escritura sin preguntar.
#   tools → default + allowlist: corre python y consulta la web, nada más auto.
#   safe  → solo lectura/chat (lo que no pide permiso). Sin banderas extra.
DEFAULT_PERMISSION = os.environ.get("BRIDGE_PERMISSION")   # SIN valor por omision
PERMISSION_ARGS = {
    "full": ["--permission-mode", "bypassPermissions"],
    "tools": ["--allowedTools", "Bash(python3:*)", "Bash(python:*)", "WebFetch"],
    "safe": [],
}


def permission_args(level: str | None) -> list:
    """Falla CERRADO. Un nivel ausente o desconocido no se degrada a `full`: revienta.

    Lo anterior hacia `PERMISSION_ARGS.get(nivel, PERMISSION_ARGS["full"])`, asi que
    una errata en el `.env` o un registro viejo concedian ejecucion arbitraria sin que
    nadie lo pidiera. El resto del marco falla cerrado; esto tambien.
    """
    nivel = level or DEFAULT_PERMISSION
    if nivel not in PERMISSION_ARGS:
        raise ValueError(f"nivel de permiso desconocido o no declarado: {nivel!r}")
    return PERMISSION_ARGS[nivel]


def run_turn(text: str, attachments: list | None, session_id: str | None,
             cwd: str, model: str, permission: str | None = None) -> dict:
    """Corre un turno headless (entrada stream-json) y devuelve
    {session_id, text, is_error, raw_error}. Soporta adjuntos multimedia y
    un nivel de permiso (full|tools|safe)."""
    args = CLAUDE_ARGS + ["-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            ]
    if model:
        args += ["--model", model]
    args += permission_args(permission)
    if session_id:
        args += ["--resume", session_id]
    content = build_content(text, attachments)
    stdin_msg = json.dumps({"type": "user",
                            "message": {"role": "user", "content": content}}) + "\n"
    try:
        proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              input=stdin_msg, timeout=TURN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"session_id": session_id, "text": None, "is_error": True,
                "raw_error": f"timeout tras {TURN_TIMEOUT}s"}

    sid, text, is_error, err = session_id, None, False, None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("session_id"):
            sid = ev["session_id"]
        if ev.get("type") == "result":
            text = ev.get("result")
            is_error = bool(ev.get("is_error")) or ev.get("subtype") != "success"

    if text is None and proc.returncode != 0:
        is_error = True
        err = (proc.stderr or proc.stdout or "").strip()[:2000] or f"exit {proc.returncode}"
    return {"session_id": sid, "text": text, "is_error": is_error, "raw_error": err}


def _tool_brief(name: str, inp: dict | None) -> str:
    """Resumen corto y legible de una llamada a herramienta, para el progreso."""
    inp = inp or {}
    key = {"Bash": "command", "Read": "file_path", "Write": "file_path",
           "Edit": "file_path", "NotebookEdit": "file_path", "WebFetch": "url",
           "WebSearch": "query", "Grep": "pattern", "Glob": "pattern",
           "Task": "description", "Skill": "skill"}.get(name)
    val = inp.get(key) if key else None
    if val is None:
        try:
            val = json.dumps(inp, ensure_ascii=False)
        except Exception:
            val = str(inp)
    return str(val).replace("\n", " ")[:160]


def stream_turn(text: str, attachments: list | None, session_id: str | None,
                cwd: str, model: str, permission: str | None, emit,
                ventana: int | None = None) -> dict:
    """Corre un turno headless y llama emitir(dict) por cada evento de UI, en vivo.
    Emite: init / tool / text / result / error. Devuelve {session_id, text, is_error}.

    EL CLIENTE PUEDE IRSE Y EL TURNO SIGUE. Antes, si `emit` lanzaba -pestana cerrada, red
    caida, maquina dormida- la excepcion subia y el `finally` mataba el proceso: el trabajo
    se perdia entero, no solo su camino. MEDIDO: matando al cliente a los 4 s de un turno
    largo, el transcript quedaba con la pregunta escrita y SIN respuesta, y no habia nada
    que recuperar. Ahora la escritura hacia el navegador puede fallar sin detener la
    lectura: el turno termina, el CLI lo escribe en su transcript, y
    `GET /sessions/<n>/ultimo` puede devolverlo."""
    args = CLAUDE_ARGS + ["-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            ]
    if model:
        args += ["--model", model]
    args += permission_args(permission)
    if session_id:
        args += ["--resume", session_id]
    content = build_content(text, attachments)
    stdin_msg = json.dumps({"type": "user",
                            "message": {"role": "user", "content": content}}) + "\n"

    sid, final_text, is_error = session_id, None, False
    out_total, last_ctx = 0, 0   # tokens generados en el turno · último tamaño de contexto
    # La ventana REAL del modelo solo llega al final, dentro del `result`. Durante el turno se
    # usaba el valor por omision (200k), y en una sesion de 1M eso pinta 56% lo que es 11%:
    # el porcentaje sube cinco veces mas rapido y salta a su sitio al cerrar. Ahora se recibe
    # la ventana que esta sesion ya demostro en su turno anterior; solo el PRIMER turno de una
    # sesion nueva usa el valor por omision, y entonces se marca `provisional` para que la
    # pagina no lo presente como un dato medido.
    ventana_conocida = int(ventana) if ventana else None
    ventana_viva = ventana_conocida or CONTEXT_WINDOW

    # Si el cliente se fue, dejamos de escribirle — pero NO dejamos de leer al CLI.
    ido = {"si": False}

    def emitir(ev):
        if ido["si"]:
            return
        try:
            emit(ev)
        except Exception:
            ido["si"] = True
    try:
        proc = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, bufsize=1,
                                encoding="utf-8", errors="replace")
    except Exception as e:
        emitir({"kind": "error", "error": str(e)})
        return {"session_id": sid, "text": None, "is_error": True}

    stderr_buf: list = []
    drain = threading.Thread(
        target=lambda: stderr_buf.extend(proc.stderr or []), daemon=True)
    drain.start()
    timer = threading.Timer(TURN_TIMEOUT, proc.kill)
    timer.start()
    try:
        proc.stdin.write(stdin_msg)
        proc.stdin.close()
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("session_id"):
                sid = ev["session_id"]
            t = ev.get("type")
            if t == "system" and ev.get("subtype") == "init":
                # slash_commands/skills viajan en el init: la web los usa para el
                # autocomplete. Son del install entero, iguales para toda sesión.
                emitir({"kind": "init", "session_id": sid,
                      "commands": ev.get("slash_commands") or [],
                      "skills": ev.get("skills") or []})
            elif t == "system" and ev.get("subtype") == "compact_boundary":
                # el turno cruzó el umbral y claude compactó el contexto en caliente
                cm = ev.get("compact_metadata") or {}
                emitir({"kind": "compact", "trigger": cm.get("trigger"),
                      "pre_tokens": cm.get("pre_tokens")})
            elif t == "assistant":
                msg = ev.get("message", {})
                for blk in msg.get("content", []):
                    if blk.get("type") == "tool_use":
                        emitir({"kind": "tool", "name": blk.get("name"),
                              "brief": _tool_brief(blk.get("name"), blk.get("input"))})
                    elif blk.get("type") == "text" and blk.get("text", "").strip():
                        emitir({"kind": "text", "text": blk["text"]})
                # uso: el contexto es todo lo que entró (fresco + caché); el gasto
                # del turno es la suma de lo generado en cada paso assistant.
                u = msg.get("usage") or {}
                if u:
                    last_ctx = (u.get("input_tokens", 0)
                                + u.get("cache_creation_input_tokens", 0)
                                + u.get("cache_read_input_tokens", 0))
                    out_total += u.get("output_tokens", 0)
                    emitir({"kind": "usage", "context_tokens": last_ctx,
                          "output_tokens": out_total, "window": ventana_viva,
                          "provisional": ventana_conocida is None})
            elif t == "result":
                final_text = ev.get("result")
                is_error = bool(ev.get("is_error")) or ev.get("subtype") != "success"
                # cierre autoritativo, con cuidado: result.usage SUMA el input de
                # cada llamada del turno (vista de facturación), NO la ocupación de
                # la ventana. La ocupación real es el último input por paso (last_ctx);
                # del result tomamos sólo el contextWindow real y el total generado.
                ru = ev.get("usage") or {}
                mu = ev.get("modelUsage") or {}
                win = next((m.get("contextWindow") for m in mu.values()
                            if isinstance(m, dict) and m.get("contextWindow")), None)
                if win:
                    ventana_viva = win          # la autoritativa, para quien la guarde
                emitir({"kind": "usage", "context_tokens": last_ctx,
                      "output_tokens": ru.get("output_tokens") or out_total,
                      "window": win or ventana_viva, "final": True})
        proc.wait()
    finally:
        timer.cancel()
        if proc.poll() is None:
            proc.kill()

    if final_text is None and proc.returncode not in (0, None):
        is_error = True
        err = ("".join(stderr_buf) or "").strip()[:2000] or f"exit {proc.returncode}"
        emitir({"kind": "error", "error": err})
    emitir({"kind": "result", "text": final_text, "is_error": is_error, "session_id": sid})
    return {"session_id": sid, "text": final_text, "is_error": is_error,
            "window": ventana_viva if ventana_viva != CONTEXT_WINDOW else None}


def deliver_turn(text: str, attachments: list | None, session_id: str | None,
                 cwd: str, model: str, permission: str | None,
                 name: str, on_init, on_error) -> None:
    """Entrega-y-suelta: corre un turno headless DESACOPLADO de la conexión HTTP.

    Llama on_init(sid) EN CUANTO el turno arranca (evento 'init' = el aviso llegó);
    llama on_error(msg) si falla ANTES de arrancar. Pensada para correr en su propio
    hilo: el turno sigue hasta terminar aunque el cliente cierre la conexión — NO se
    mata por desconexión, sólo por TURN_TIMEOUT. Persiste la rotación de session_id
    en el registro (al arrancar y al terminar), para que el registro quede fresco sin
    depender de que el cliente siga escuchando.
    """
    args = CLAUDE_ARGS + ["-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            ]
    if model:
        args += ["--model", model]
    args += permission_args(permission)
    if session_id:
        args += ["--resume", session_id]
    content = build_content(text, attachments)
    stdin_msg = json.dumps({"type": "user",
                            "message": {"role": "user", "content": content}}) + "\n"

    def _persist(new_sid: str | None) -> None:
        if new_sid and new_sid != session_id:
            with _registry_lock:
                reg = load_registry()
                if name in reg:
                    reg[name]["session_id"] = new_sid
                    save_registry(reg)

    try:
        proc = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, bufsize=1,
                                encoding="utf-8", errors="replace")
    except Exception as e:
        on_error(str(e))
        return

    # drenar stderr para que el proceso no se bloquee por buffer lleno
    threading.Thread(target=lambda: list(proc.stderr or []), daemon=True).start()
    timer = threading.Timer(TURN_TIMEOUT, proc.kill)
    timer.start()
    sid, started = session_id, False
    try:
        proc.stdin.write(stdin_msg)
        proc.stdin.close()
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("session_id"):
                sid = ev["session_id"]
            if (ev.get("type") == "system" and ev.get("subtype") == "init"
                    and not started):
                started = True
                _persist(sid)          # registro fresco apenas arranca
                on_init(sid)           # el handler ya puede responder "llegó"
        proc.wait()
    finally:
        timer.cancel()
        if proc.poll() is None:
            proc.kill()
    _persist(sid)                      # por si rotó después del init
    if not started:                    # nunca arrancó: no hubo entrega
        err = (f"exit {proc.returncode}" if proc.returncode not in (0, None)
               else "el turno terminó sin emitir init")
        on_error(err)


def claude_agents() -> list:
    try:
        out = subprocess.run([CLAUDE, "agents", "--json", "--all"],
                             capture_output=True, text=True, timeout=30)
        return json.loads(out.stdout) if out.stdout.strip() else []
    except (subprocess.SubprocessError, json.JSONDecodeError):
        return []


def stop_session(short_id: str) -> None:
    try:
        subprocess.run([CLAUDE, "stop", short_id], capture_output=True, timeout=30)
    except subprocess.SubprocessError:
        pass


# ---------------------------------------------------------------- servidor HTTP
class Handler(BaseHTTPRequestHandler):
    server_version = "VuelamindSessionBridge/1.0"

    # --- utilidades
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _host_ok(self) -> bool:
        """El Host debe apuntar a loopback. Corta el DNS-rebinding: una página en
        attacker.com resuelta a 127.0.0.1 llega con Host=attacker.com y se rechaza."""
        host = self.headers.get("Host", "")
        name = host.rsplit(":", 1)[0] if host else ""
        return name in _LOCAL_HOSTS

    def _origin_ok(self) -> bool:
        """Para métodos que cambian estado. Sin Origin (navegación de nivel superior
        o cliente no-navegador) se permite; con Origin, debe ser el nuestro. El
        navegador manda Origin verídico en cross-site, así que frena el CSRF/RCE."""
        origin = self.headers.get("Origin")
        return origin is None or origin in SAME_ORIGINS

    def _blocked(self, changing: bool = False) -> bool:
        """True (y ya respondió 403) si la petición no pasa los candados locales."""
        if not self._host_ok():
            self._json(403, {"error": "host no permitido (solo loopback)"})
            return True
        if changing and not self._origin_ok():
            self._json(403, {"error": "origen no permitido"})
            return True
        return False

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length", "0") or "0")
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return {}

    def log_message(self, fmt, *args):  # silencio; logging propio abajo
        # `pythonw.exe` lanzado POR EL PROGRAMADOR DE TAREAS no tiene consola:
        # `sys.stderr` es None, y esto corre EN CADA PETICIÓN. MEDIDO en Windows el
        # 2026-09-11 con una tarea de prueba: el puente abría el puerto, quedaba
        # LISTENING, y reventaba en TODA petición antes de responder. El cliente veía
        # «the connection was closed unexpectedly» y no quedaba rastro, porque el único
        # sitio donde se escribiría el error es justo el que no existe.
        #
        # Y lo peor, visto por accidente: el trabajo SÍ se hacía antes de reventar. Un
        # turno creaba la sesión y la registraba, moría al escribir la línea del log, y
        # al reintentar con el mismo nombre contestaba 409 «ya existe». El efecto queda
        # hecho y el acuse se pierde: quien reintenta choca contra su propio trabajo
        # invisible.
        if sys.stderr is None:
            return
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # --- ruteo
    def _html(self, code: int, text: str) -> None:
        body = text.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            if HTML_FILE.exists():
                return self._html(200, HTML_FILE.read_text(encoding="utf-8"))
            return self._html(200, "<h1>puente arriba</h1><p>falta session_bridge.html</p>")
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if self.path == "/health":
            return self._json(200, {"ok": True})
        if self._blocked():
            return
        if self.path == "/sessions":
            reg = load_registry()
            live = {a.get("sessionId"): a for a in claude_agents()}
            merged = []
            for name, meta in reg.items():
                a = live.get(meta.get("session_id"), {})
                merged.append({"name": name, "session_id": meta.get("session_id"),
                               "cwd": meta.get("cwd"), "created": meta.get("created"),
                               "permission": meta.get("permission") or DEFAULT_PERMISSION,
                               "live_state": a.get("state") or a.get("status")})
            # Se comprueba AQUI y no al arrancar: el master puede llegar en un
            # montaje posterior, y un dato cacheado del arranque mentiria sin fallar.
            master = MASTER if (MASTER and Path(MASTER).is_file()) else ""
            # `base` es donde nacen los agentes nuevos. La pagina no la adivina ni la
            # teclea nadie: el que manda es el directorio con el que arrancó el puente.
            return self._json(200, {"sessions": merged, "agents_raw": list(live.values()),
                                    "master": master, "base": str(Path(DEFAULT_CWD))})
        # GET /agentes -> los dominios que viven bajo el directorio del puente.
        # Un agente NO es una sesion: la sesion es efimera y el agente es la carpeta,
        # con su vault y su memoria. Aqui se enumera lo que hay en disco, exista o no
        # una conversacion abierta contra ello.
        if self.path == "/agentes":
            base = Path(DEFAULT_CWD)
            salida = []
            if base.is_dir():
                for d in sorted(base.iterdir()):
                    if not d.is_dir() or d.name.startswith("."):
                        continue
                    ident = _identidad(d)
                    if not ident["panorama"]:
                        continue          # una carpeta cualquiera no es un dominio
                    salida.append({"carpeta": d.name, "cwd": str(d), **ident})
            return self._json(200, {"agentes": salida, "base": str(base)})

        # GET /agentes/<carpeta>/vault.zip -> el dominio entero, empaquetado, para
        # bajarlo a la maquina de quien mira. El vault es suyo: vive fuera del
        # contenedor a proposito, y esto es la otra mitad de esa frase.
        mz = re.match(r"^/agentes/([^/]+)/vault\.zip$", self.path)
        if mz:
            return self._vault_zip(unquote(mz.group(1)))

        # GET /sessions/<name>/historial -> la conversacion, para una ventana que no la tiene
        mh = re.match(r"^/sessions/([^/]+)/historial(?:\?limite=(\d+))?$", self.path)
        if mh:
            nombre, lim = mh.group(1), int(mh.group(2) or 50)
            meta = load_registry().get(nombre)
            if not meta:
                return self._json(404, {"error": f"no hay sesión '{nombre}'"})
            if not meta.get("session_id"):
                return self._json(409, {"error": "esa sesión no tiene session_id todavía"})
            return self._json(200, historial_del_transcript(meta["session_id"],
                                                            max(1, min(lim, 500))))
        # GET /sessions/<name>/ultimo  -> RECUPERAR lo que el stream no alcanzo a traer
        mu = re.match(r"^/sessions/([^/]+)/ultimo$", self.path)
        if mu:
            nombre = mu.group(1)
            meta = load_registry().get(nombre)
            if not meta:
                return self._json(404, {"error": f"no hay sesión '{nombre}'"})
            if not meta.get("session_id"):
                return self._json(409, {"error": "esa sesión no tiene session_id todavía"})
            resp = ultimo_del_transcript(meta["session_id"])
            # Tres estados, no dos: sin esto, "todavía no" y "ya nunca" son la misma cosa
            # vistos desde el navegador, y la página se queda esperando para siempre.
            resp["en_vuelo"] = esta_en_vuelo(nombre)
            return self._json(200, resp)
        return self._json(404, {"error": "ruta desconocida"})

    # Lo que NUNCA entra al zip. No es una lista de comodidad: un paquete se manda
    # por chat, por correo o a un disco ajeno, y lo que cruza ese borde no vuelve.
    # Un `.llaves/` dentro de un zip es una credencial publicada.
    ZIP_FUERA = {".git", ".llaves", ".ssh", ".instantanea-vault",
                 "node_modules", "__pycache__", ".venv"}
    ZIP_FUERA_SUFIJOS = (".conf", ".env", ".pem", ".key", ".p12")

    def _vault_zip(self, carpeta: str) -> None:
        """Empaqueta UN agente. No `/trabajo` entero: el dia que haya dos dominios,
        un zip unico se lleva el de al lado sin que nadie lo pida."""
        base = Path(DEFAULT_CWD)
        # El nombre NO se usa para construir la ruta: se busca en lo ya enumerado,
        # con el mismo filtro que /agentes. Asi el salto de directorio no se
        # sanea — no llega a existir, porque no hay ruta que envenenar.
        destino = None
        if base.is_dir():
            for d in sorted(base.iterdir()):
                if (d.is_dir() and not d.name.startswith(".")
                        and d.name == carpeta and _identidad(d)["panorama"]):
                    destino = d
                    break
        if destino is None:
            return self._json(404, {"error": f"no hay agente '{carpeta}'"})

        # En memoria: un vault son notas, y el de la casa mas grande medida no llega
        # a 2 MB. Si algun dia deja de ser cierto, esto se escribe a disco temporal.
        fuera, dentro, buf = [], 0, io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for ruta in sorted(destino.rglob("*")):
                rel = ruta.relative_to(destino)
                motivo = ""
                if set(rel.parts) & self.ZIP_FUERA:
                    motivo = "carpeta excluida por norma"
                elif ruta.name.endswith(self.ZIP_FUERA_SUFIJOS):
                    motivo = "puede llevar un secreto"
                if not ruta.is_file():
                    continue
                if motivo:
                    fuera.append(f"{rel}  --  {motivo}")
                    continue
                try:
                    z.write(ruta, str(Path(carpeta) / rel))
                    dentro += 1
                except OSError as e:
                    fuera.append(f"{rel}  --  no se pudo leer: {e}")
            # Un paquete que calla lo que dejo fuera se lee como completo, y nadie
            # descubre el hueco hasta que lo necesita. Este lo dice SIEMPRE, tambien
            # cuando no falta nada: "vacio" y "no se miro" tienen que verse distinto.
            acta = [f"vault de '{carpeta}'  ·  {dentro} archivos dentro",
                    "", "Lo que quedo FUERA de este zip:", ""]
            acta += fuera if fuera else ["  (nada: no habia ningun archivo excluido)"]
            acta += ["", "La norma que los excluye vive en session_bridge.py,",
                     "en ZIP_FUERA y ZIP_FUERA_SUFIJOS.", ""]
            z.writestr(str(Path(carpeta) / "_EXCLUIDO.txt"), "\n".join(acta))

        datos = buf.getvalue()
        # El nombre de archivo viaja en una cabecera entre comillas: se limpia lo que
        # podria cerrarla antes de tiempo.
        seguro = re.sub(r'[^A-Za-z0-9._-]', "_", carpeta) or "vault"
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition",
                         f'attachment; filename="{seguro}-vault.zip"')
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        if self._blocked(changing=True):
            return
        # POST /sessions  -> crear
        if self.path == "/sessions":
            b = self._body()
            name, prompt = b.get("name"), b.get("prompt")
            attachments = b.get("attachments") or []
            if not name or not NAME_RE.match(name):
                return self._json(400, {"error": "name inválido (usa [A-Za-z0-9._-], 1-64)"})
            if not prompt and not attachments:
                return self._json(400, {"error": "falta prompt (o al menos un adjunto)"})
            with _registry_lock:
                reg = load_registry()
                if name in reg:
                    return self._json(409, {"error": f"ya existe una sesión '{name}'"})
            cwd = b.get("cwd") or DEFAULT_CWD
            model = b.get("model") or DEFAULT_MODEL
            permission = b.get("permission") or DEFAULT_PERMISSION
            if permission not in PERMISSION_ARGS:
                return self._json(400, {"error": "permission inválido (full|tools|safe)"})
            # El cwd decide QUE agente es esta sesion -su vault, su CLAUDE.md y su memoria
            # automatica salen de ahi-. Si no existe, hoy reventaba dentro del subproceso con
            # un error que no dice que paso; una ruta mal tecleada merece decirse aqui.
            if not Path(cwd).is_dir():
                # Nacer un agente crea su carpeta; teclear mal una ruta, no. La
                # diferencia la marca quien llama pidiendolo, y el limite es duro:
                # solo bajo el directorio del puente, nunca en cualquier sitio.
                if b.get("crear_cwd") and _dentro_de(cwd, DEFAULT_CWD):
                    try:
                        Path(cwd).mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        return self._json(400, {"error": f"no pude crear {cwd}: {e}"})
                else:
                    return self._json(400, {"error": f"el directorio no existe: {cwd}"})
            res = run_turn(prompt or "", attachments, None, cwd, model, permission)
            if res["is_error"] or not res["session_id"]:
                return self._json(502, {"error": "claude falló al crear",
                                        "detail": res.get("raw_error"), "text": res.get("text")})
            with _registry_lock:
                reg = load_registry()
                reg[name] = {"session_id": res["session_id"], "cwd": cwd,
                             "model": model, "permission": permission, "created": _now()}
                save_registry(reg)
            return self._json(201, {"name": name, "session_id": res["session_id"],
                                    "text": res["text"]})
        # POST /sessions/crear  -> CREAR VIENDO. Misma entrada que POST /sessions, pero el
        # primer turno viaja como NDJSON en vez de esperarse entero.
        #
        # POR QUE EXISTE: crear con run_turn bloquea hasta que el turno TERMINA y no emite
        # nada por el camino; con un primer mensaje caro -leer el arranque del dominio,
        # correr el validador- eso son minutos con un boton que dice "Creando..." y ninguna
        # senal de si sigue vivo. Y era ademas el ultimo turno que seguia muriendo con el
        # cliente, porque no pasaba por stream_turn.
        #
        # EL REGISTRO SE ESCRIBE AL LLEGAR EL `init`, no al final: ahi aparece el session_id,
        # y a partir de ese instante la sesion existe aunque el navegador se caiga.
        if self.path == "/sessions/crear":
            b = self._body()
            name, prompt = b.get("name"), b.get("prompt")
            attachments = b.get("attachments") or []
            if not name or not NAME_RE.match(name):
                return self._json(400, {"error": "name inválido (usa [A-Za-z0-9._-], 1-64)"})
            if not prompt and not attachments:
                return self._json(400, {"error": "falta prompt (o al menos un adjunto)"})
            with _registry_lock:
                reg = load_registry()
                if name in reg:
                    return self._json(409, {"error": f"ya existe una sesión '{name}'"})
            cwd = b.get("cwd") or DEFAULT_CWD
            model = b.get("model") or DEFAULT_MODEL
            permission = b.get("permission") or DEFAULT_PERMISSION
            if permission not in PERMISSION_ARGS:
                return self._json(400, {"error": "permission inválido (full|tools|safe)"})
            # El cwd decide QUE agente es esta sesion -su vault, su CLAUDE.md y su memoria
            # automatica salen de ahi-. Si no existe, hoy reventaba dentro del subproceso con
            # un error que no dice que paso; una ruta mal tecleada merece decirse aqui.
            if not Path(cwd).is_dir():
                # Nacer un agente crea su carpeta; teclear mal una ruta, no. La
                # diferencia la marca quien llama pidiendolo, y el limite es duro:
                # solo bajo el directorio del puente, nunca en cualquier sitio.
                if b.get("crear_cwd") and _dentro_de(cwd, DEFAULT_CWD):
                    try:
                        Path(cwd).mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        return self._json(400, {"error": f"no pude crear {cwd}: {e}"})
                else:
                    return self._json(400, {"error": f"el directorio no existe: {cwd}"})

            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            registrada = {"si": False}

            def emit(ev):
                # El init trae el session_id: es el momento exacto en que la sesión pasa a
                # existir, y por eso se anota aquí y no cuando el turno termine.
                if ev.get("kind") == "init" and ev.get("session_id") and not registrada["si"]:
                    with _registry_lock:
                        reg2 = load_registry()
                        reg2[name] = {"session_id": ev["session_id"], "cwd": cwd,
                                      "model": model, "permission": permission,
                                      "created": _now()}
                        save_registry(reg2)
                    registrada["si"] = True
                self.wfile.write((json.dumps(ev) + "\n").encode())
                self.wfile.flush()

            marcar_vivo(name, True)
            try:
                res = stream_turn(prompt or "", attachments, None, cwd, model, permission,
                                  emit)
                guardar_ventana(name, res.get("window"))
            except (BrokenPipeError, ConnectionResetError):
                return   # el cliente se fue; el turno sigue y la sesión ya quedó anotada
            finally:
                marcar_vivo(name, False)
            if not registrada["si"]:
                # Nunca hubo `init`: no hay sesión que anotar. Se dice, en vez de dejar un
                # nombre a medias que el usuario creeria creado.
                try:
                    self.wfile.write((json.dumps(
                        {"kind": "error", "error": "la sesión no llegó a arrancar: sin init"}
                    ) + "\n").encode())
                    self.wfile.flush()
                except Exception:
                    pass
            return
        # POST /sessions/<name>/deliver  -> ENTREGAR Y SOLTAR (arranca, acusa al init, se desengancha)
        md = re.match(r"^/sessions/([^/]+)/deliver$", self.path)
        if md:
            name = md.group(1)
            b = self._body()
            msg = b.get("message") or ""
            attachments = b.get("attachments") or []
            if not msg and not attachments:
                return self._json(400, {"error": "falta message (o al menos un adjunto)"})
            reg = load_registry()
            meta = reg.get(name)
            if not meta:
                return self._json(404, {"error": f"no hay sesión '{name}'"})
            started = threading.Event()
            box = {"session_id": meta["session_id"], "error": None}

            def on_init(sid):
                if sid:
                    box["session_id"] = sid
                started.set()

            def on_error(err):
                box["error"] = err
                started.set()

            # el turno corre en su PROPIO hilo (daemon): sigue aunque respondamos y
            # el cliente cierre. No lo atamos a la vida de esta conexión HTTP.
            threading.Thread(
                target=deliver_turn,
                args=(msg, attachments, meta["session_id"],
                      meta.get("cwd") or DEFAULT_CWD,
                      meta.get("model") or DEFAULT_MODEL,
                      meta.get("permission") or DEFAULT_PERMISSION,
                      name, on_init, on_error),
                daemon=True).start()

            if not started.wait(DELIVER_INIT_TIMEOUT):
                # no arrancó a tiempo; el turno puede seguir en background, pero no
                # afirmamos entrega — que quien dispara reintente
                return self._json(504, {"error": "el turno no arrancó a tiempo",
                                        "name": name, "started": False})
            if box["error"] is not None:
                return self._json(502, {"error": "claude falló al arrancar",
                                        "detail": box["error"], "name": name,
                                        "started": False})
            return self._json(200, {"name": name, "session_id": box["session_id"],
                                    "started": True})
        # POST /sessions/<name>/stream  -> continuar con progreso en vivo (NDJSON)
        ms = re.match(r"^/sessions/([^/]+)/stream$", self.path)
        if ms:
            name = ms.group(1)
            b = self._body()
            msg = b.get("message") or ""
            attachments = b.get("attachments") or []
            if not msg and not attachments:
                return self._json(400, {"error": "falta message (o al menos un adjunto)"})
            reg = load_registry()
            meta = reg.get(name)
            if not meta:
                return self._json(404, {"error": f"no hay sesión '{name}'"})
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()

            def emit(ev):
                self.wfile.write((json.dumps(ev) + "\n").encode())
                self.wfile.flush()

            marcar_vivo(name, True)
            try:
                res = stream_turn(msg, attachments, meta["session_id"],
                                  meta.get("cwd") or DEFAULT_CWD,
                                  meta.get("model") or DEFAULT_MODEL,
                                  meta.get("permission") or DEFAULT_PERMISSION, emit,
                                  ventana=meta.get("context_window"))
            except (BrokenPipeError, ConnectionResetError):
                return   # el cliente se fue; el turno NO: sigue drenándose hasta terminar
            finally:
                marcar_vivo(name, False)
            guardar_ventana(name, res.get("window"))
            if res.get("session_id") and res["session_id"] != meta["session_id"]:
                with _registry_lock:
                    reg = load_registry()
                    if name in reg:
                        reg[name]["session_id"] = res["session_id"]
                        save_registry(reg)
            return
        # POST /sessions/<name>/messages  -> continuar
        m = re.match(r"^/sessions/([^/]+)/messages$", self.path)
        if m:
            name = m.group(1)
            b = self._body()
            msg = b.get("message") or ""
            attachments = b.get("attachments") or []
            if not msg and not attachments:
                return self._json(400, {"error": "falta message (o al menos un adjunto)"})
            reg = load_registry()
            meta = reg.get(name)
            if not meta:
                return self._json(404, {"error": f"no hay sesión '{name}'"})
            res = run_turn(msg, attachments, meta["session_id"],
                          meta.get("cwd") or DEFAULT_CWD,
                          meta.get("model") or DEFAULT_MODEL,
                          meta.get("permission") or DEFAULT_PERMISSION)
            if res["is_error"]:
                return self._json(502, {"error": "claude falló al continuar",
                                        "detail": res.get("raw_error"),
                                        "session_id": res["session_id"], "text": res.get("text")})
            # el sessionId puede rotar al continuar; lo actualizamos
            if res["session_id"] and res["session_id"] != meta["session_id"]:
                with _registry_lock:
                    reg = load_registry()
                    if name in reg:
                        reg[name]["session_id"] = res["session_id"]
                        save_registry(reg)
            return self._json(200, {"name": name, "session_id": res["session_id"],
                                    "text": res["text"]})
        return self._json(404, {"error": "ruta desconocida"})

    def do_DELETE(self):
        if self._blocked(changing=True):
            return
        m = re.match(r"^/sessions/([^/]+)$", self.path)
        if not m:
            return self._json(404, {"error": "ruta desconocida"})
        name = m.group(1)
        with _registry_lock:
            reg = load_registry()
            meta = reg.pop(name, None)
            if meta:
                save_registry(reg)
        if not meta:
            return self._json(404, {"error": f"no hay sesión '{name}'"})
        sid = meta.get("session_id", "")
        short = sid.split("-")[0] if sid else ""
        for a in claude_agents():
            if a.get("sessionId") == sid and a.get("id"):
                stop_session(a["id"])
        return self._json(200, {"deleted": name, "stopped_short_id": short})


def _now() -> str:
    import datetime
    return datetime.datetime.now().isoformat(timespec="seconds")


def main():
    if not Path(CLAUDE).exists() and not shutil.which(CLAUDE):
        sys.exit(f"no encuentro el binario claude en: {CLAUDE}")
    # El `cwd` se comprueba AL ARRANCAR. MEDIDO el 2026-09-11 en Windows: con un
    # `BRIDGE_CWD` inexistente el puente arranca, sirve la página entera y contesta
    # `/health` con `ok: true` — y revienta en el PRIMER TURNO con `NotADirectoryError
    # [WinError 267] The directory name is invalid`, que habla de directorios sin decir
    # cuál. Quien lo reciba va a buscar el defecto en el CLI, que es donde no está.
    # Un fallo diferido cuesta más que uno inmediato: el arranque sano es una promesa.
    if not Path(DEFAULT_CWD).is_dir():
        sys.exit(f"ME NIEGO A ARRANCAR: el directorio de trabajo no existe.\n"
                 f"  BRIDGE_CWD = {DEFAULT_CWD}\n"
                 "  Créalo, o apúntalo a otro con --set BRIDGE_CWD=<ruta> al instalar.\n"
                 "  Si arrancara igual, el fallo saldría en el primer turno y hablaría\n"
                 "  de directorios sin decir cuál.")

    # El nivel de permiso NO tiene valor por omision: sin declararlo, no se arranca.
    # `full` concede ejecucion arbitraria, y nadie debe heredarla por no haber escrito
    # nada. Quien la quiere, la firma en su .env.
    if DEFAULT_PERMISSION is None:
        sys.exit("ME NIEGO A ARRANCAR: BRIDGE_PERMISSION no esta declarado.\n"
                 "  Escribelo en ~/.claude/vuelamind-rc.env con uno de: full | tools | safe\n"
                 "  full = ejecucion arbitraria con tus privilegios. No hay default a proposito.")
    if DEFAULT_PERMISSION not in PERMISSION_ARGS:
        sys.exit(f"ME NIEGO A ARRANCAR: BRIDGE_PERMISSION={DEFAULT_PERMISSION!r} no existe. "
                 "Usa full | tools | safe.")
    # En Windows, `allow_reuse_address` (SO_REUSEADDR) SI permite un bind duplicado, así
    # que un segundo puente levanta EN SILENCIO sobre el mismo puerto. MEDIDO el
    # 2026-09-11 provocándolo: dos procesos LISTENING en 8872, el segundo sin decir nada.
    # Quedan dos puentes con DOS REGISTROS de sesiones distintos y las peticiones caen en
    # cualquiera: el usuario ve sesiones que aparecen y desaparecen, y ningún log lo dice.
    # En Linux y macOS el mismo código da «Address already in use». Es divergencia de
    # plataforma, no del código — y aquí el diseño produce el escenario solo: la tarea
    # levanta uno al iniciar sesión y alguien levanta otro a mano.
    if os.name == "nt":
        ThreadingHTTPServer.allow_reuse_address = False
    try:
        srv = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as e:
        sys.exit(f"NO PUEDO ESCUCHAR EN {HOST}:{PORT} — {e}\n"
                 "  Lo más probable: ya hay un puente corriendo en ese puerto.\n"
                 "  Míralo y mátalo, o arranca éste con otro PORT.")
    # Sin esto, NADA de lo que sigue llega al log cuando la salida no es una terminal:
    # stdout queda en buffer de bloque y el arranque se queda dentro, mientras las
    # peticiones -que van por stderr- sí se ven. Medido el 2026-09-21 corriendo el
    # puente como servicio: el log tenía los GET y ni una línea del arranque, que es
    # justo donde se lee en qué puerto quedó y con qué configuración.
    try: sys.stdout.reconfigure(line_buffering=True)
    except Exception: pass
    print(f"puente escuchando en http://{HOST}:{PORT}  (solo loopback, sin token)")
    print(f"candados: allowlist de Host + chequeo de Origin en POST/DELETE")
    if MASTER:
        print(f"master del marco: {MASTER}" if Path(MASTER).is_file()
              else f"AVISO: BRIDGE_MASTER apunta a {MASTER}, que NO existe — la página no lo ofrecerá")
    print(f"modelo por defecto: {DEFAULT_MODEL or '(el del CLI)'}   ·   cwd por defecto: {DEFAULT_CWD}")
    print(f"permiso por defecto: {DEFAULT_PERMISSION}   (declarado, no heredado)")
    print(f"desde otra máquina:  ssh -N -L {PORT}:127.0.0.1:{PORT} <usuario>@<esta-máquina>")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nadiós")


if __name__ == "__main__":
    main()
