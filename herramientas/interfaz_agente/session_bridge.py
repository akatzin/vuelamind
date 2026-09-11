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
        ssh -N -L 8787:127.0.0.1:8787 <usuario>@<esta-máquina>
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
    python3 session_bridge.py                 # 127.0.0.1:8787
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
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


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


_load_env_file()

# ---------------------------------------------------------------- configuración
HOST = "127.0.0.1"                                   # loopback SIEMPRE; salir por túnel SSH
PORT = int(os.environ.get("PORT", "8787"))
DEFAULT_MODEL = os.environ.get("BRIDGE_MODEL", "opus")   # haiku no existe en este despliegue
DEFAULT_CWD = os.environ.get("BRIDGE_CWD", str(Path(__file__).resolve().parent.parent))
TURN_TIMEOUT = int(os.environ.get("BRIDGE_TIMEOUT", "600"))   # segundos por turno
# entregar-y-soltar: cuánto espera el handler el evento 'init' antes de rendirse.
# El turno YA arranca en segundos; este tope solo evita que el handler cuelgue si
# claude no emite init (p.ej. no arrancó). El turno, si arrancó, sigue en background.
DELIVER_INIT_TIMEOUT = int(os.environ.get("BRIDGE_DELIVER_INIT_TIMEOUT", "120"))

CLAUDE = os.environ.get("BRIDGE_CLAUDE_BIN") or shutil.which("claude") or \
    str(Path.home() / ".local/bin/claude")

HTML_FILE = Path(__file__).resolve().parent / "session_bridge.html"
CONF_DIR = Path.home() / ".claude"
REGISTRY_FILE = Path(os.environ.get("BRIDGE_REGISTRY", CONF_DIR / "liverpool-bridge-sessions.json"))

# candados que sustituyen al token (ver docstring). Host y Origin permitidos.
_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", "[::1]"}
SAME_ORIGINS = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}

_registry_lock = threading.Lock()
NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")        # nombres seguros para direccionar


# ---------------------------------------------------------------- registro
def load_registry() -> dict:
    if REGISTRY_FILE.exists():
        try:
            return json.loads(REGISTRY_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_registry(reg: dict) -> None:
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2))
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
DEFAULT_PERMISSION = os.environ.get("BRIDGE_PERMISSION", "full")
PERMISSION_ARGS = {
    "full": ["--permission-mode", "bypassPermissions"],
    "tools": ["--allowedTools", "Bash(python3:*)", "Bash(python:*)", "WebFetch"],
    "safe": [],
}


def permission_args(level: str | None) -> list:
    return PERMISSION_ARGS.get(level or DEFAULT_PERMISSION, PERMISSION_ARGS["full"])


def run_turn(text: str, attachments: list | None, session_id: str | None,
             cwd: str, model: str, permission: str | None = None) -> dict:
    """Corre un turno headless (entrada stream-json) y devuelve
    {session_id, text, is_error, raw_error}. Soporta adjuntos multimedia y
    un nivel de permiso (full|tools|safe)."""
    args = [CLAUDE, "-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            "--model", model]
    args += permission_args(permission)
    if session_id:
        args += ["--resume", session_id]
    content = build_content(text, attachments)
    stdin_msg = json.dumps({"type": "user",
                            "message": {"role": "user", "content": content}}) + "\n"
    try:
        proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
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
                cwd: str, model: str, permission: str | None, emit) -> dict:
    """Corre un turno headless y llama emit(dict) por cada evento de UI, en vivo.
    Emite: init / tool / text / result / error. Devuelve {session_id, text, is_error}.
    emit puede lanzar (cliente desconectado); en ese caso matamos el proceso."""
    args = [CLAUDE, "-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            "--model", model]
    args += permission_args(permission)
    if session_id:
        args += ["--resume", session_id]
    content = build_content(text, attachments)
    stdin_msg = json.dumps({"type": "user",
                            "message": {"role": "user", "content": content}}) + "\n"

    sid, final_text, is_error = session_id, None, False
    try:
        proc = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, bufsize=1)
    except Exception as e:
        emit({"kind": "error", "error": str(e)})
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
                emit({"kind": "init", "session_id": sid})
            elif t == "assistant":
                for blk in ev.get("message", {}).get("content", []):
                    if blk.get("type") == "tool_use":
                        emit({"kind": "tool", "name": blk.get("name"),
                              "brief": _tool_brief(blk.get("name"), blk.get("input"))})
                    elif blk.get("type") == "text" and blk.get("text", "").strip():
                        emit({"kind": "text", "text": blk["text"]})
            elif t == "result":
                final_text = ev.get("result")
                is_error = bool(ev.get("is_error")) or ev.get("subtype") != "success"
        proc.wait()
    finally:
        timer.cancel()
        if proc.poll() is None:
            proc.kill()

    if final_text is None and proc.returncode not in (0, None):
        is_error = True
        err = ("".join(stderr_buf) or "").strip()[:2000] or f"exit {proc.returncode}"
        emit({"kind": "error", "error": err})
    emit({"kind": "result", "text": final_text, "is_error": is_error, "session_id": sid})
    return {"session_id": sid, "text": final_text, "is_error": is_error}


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
    args = [CLAUDE, "-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
            "--model", model]
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
                                text=True, bufsize=1)
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
    server_version = "LiverpoolSessionBridge/1.0"

    # --- utilidades
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
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
                return self._html(200, HTML_FILE.read_text())
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
            return self._json(200, {"sessions": merged, "agents_raw": list(live.values())})
        return self._json(404, {"error": "ruta desconocida"})

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

            try:
                res = stream_turn(msg, attachments, meta["session_id"],
                                  meta.get("cwd") or DEFAULT_CWD,
                                  meta.get("model") or DEFAULT_MODEL,
                                  meta.get("permission") or DEFAULT_PERMISSION, emit)
            except (BrokenPipeError, ConnectionResetError):
                return   # el cliente se fue; el proceso ya se mató en stream_turn
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
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"puente escuchando en http://{HOST}:{PORT}  (solo loopback, sin token)")
    print(f"candados: allowlist de Host + chequeo de Origin en POST/DELETE")
    print(f"modelo por defecto: {DEFAULT_MODEL}   ·   cwd por defecto: {DEFAULT_CWD}")
    print(f"desde otra máquina:  ssh -N -L {PORT}:127.0.0.1:{PORT} <usuario>@<esta-máquina>")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nadiós")


if __name__ == "__main__":
    main()
