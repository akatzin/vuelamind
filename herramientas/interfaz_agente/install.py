#!/usr/bin/env python3
"""
install.py — instalador portable del puente de sesiones (vuelamind-rc).

Deja el servicio instalado, con arranque automático propio del sistema operativo,
y su configuración en un archivo (no depende de cómo cada SO inyecta variables):

    macOS    → LaunchAgent  (~/Library/LaunchAgents/com.vuelamind.rc.plist)
    Windows  → Tarea Programada al iniciar sesión (schtasks, con pythonw)
    Linux    → unidad systemd de usuario (~/.config/systemd/user/)

Config del servicio: ~/.claude/vuelamind-rc.env  (KEY=VALUE por línea).
El servicio la lee al arrancar; el autostart solo tiene que lanzar python.

Uso:
    python3 install.py                 # instala/actualiza y arranca
    python3 install.py --cwd <ruta>    # dir de trabajo por defecto de las sesiones
    python3 install.py --permission safe          # el permiso es OBLIGATORIO
    python3 install.py --port 8850 --permission full --model <id>
    python3 install.py --set CLAUDE_CODE_USE_VERTEX=1 --set ANTHROPIC_VERTEX_PROJECT_ID=...
    python3 install.py --status        # ¿está arriba?
    python3 install.py --uninstall     # quita el autostart
    python3 install.py --no-start      # instala sin arrancar
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

LABEL = "com.vuelamind.rc"
OLD_LABELS = ["ai.vuelamind.session-bridge"]      # etiquetas de versiones previas: se LEEN para migrar, nunca se crean
HOME = Path.home()
CONF_DIR = HOME / ".claude"
ENV_FILE = CONF_DIR / "vuelamind-rc.env"
INSTALL_DIR = CONF_DIR / "vuelamind-rc"
ASSETS = Path(__file__).resolve().parent

# claves que persistimos en el .env (config del dominio/cuenta, no del código)
VERTEX_KEYS = ["CLAUDE_CODE_USE_VERTEX", "ANTHROPIC_VERTEX_PROJECT_ID",
               "CLOUD_ML_REGION", "ANTHROPIC_DEFAULT_OPUS_MODEL"]
BRIDGE_KEYS = ["PORT", "BRIDGE_MODEL", "BRIDGE_PERMISSION", "BRIDGE_CWD",
               "BRIDGE_CLAUDE_BIN"]
# El modelo NO se congela aqui: vacio = el default del CLI. Un id fijo revienta en
# cualquier cuenta donde no este aprovisionado, y eso ya se midio.
# Y BRIDGE_PERMISSION NO tiene default a proposito: se exige declararlo (ver abajo).
DEFAULTS = {"PORT": "8850", "BRIDGE_MODEL": ""}


# --------------------------------------------------------------- utilidades
# La consola de Windows es CP1252 y este archivo imprime flechas, puntos medios y
# tildes. MEDIDO en Windows 11 el 2026-09-11: con 3.9 el instalador CRASHEA con
# UnicodeEncodeError al imprimir `→`; con 3.12 no truena pero el texto sale corrupto.
# Mismo defecto, dos caras, y en macOS no se ve nunca. Se arregla en la SALIDA, una vez,
# y así protege también las líneas que nadie ha escrito todavía.
# NO se fuerza utf-8: se CONSERVA la codificación de la consola y solo se relaja el
# error. MEDIDO el 2026-09-11 comparando las tres estrategias sobre la misma línea, tal
# como la leería una consola cp1252:
#   sin arreglo          → UnicodeEncodeError, el instalador muere
#   utf-8 + replace      → «pÃ¡gina cÃ³digo aÃ±o»  (mojibake: no truena y no se entiende)
#   conservar + replace  → «página código año», con `?` donde va la flecha  ← ésta
# Forzar utf-8 arregla el crash y estropea los acentos, que en español son casi todo el
# texto. Lo que cp1252 sí sabe escribir se escribe bien; lo que no, se marca.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(errors="replace")
    except Exception:
        pass


def say(msg):
    print(msg, flush=True)


MINIMO_PY = (3, 10)


def exigir_python(py):
    """El autostart apunta a UN interprete concreto; si ese no sirve, el servicio no
    arranca y NADA lo dice. MEDIDO el 2026-09-11: instalacion completa y con exito,
    autostart escrito, URL impresa, sobre un python 3.9 que no podia ni importar el
    servicio. En Windows pythonw.exe corre sin ventana y el error no se ve en ningun sitio."""
    try:
        sal = subprocess.run([py, "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
                             capture_output=True, text=True, timeout=20)
        may, men = (int(x) for x in sal.stdout.strip().split("."))
    except Exception as e:
        sys.exit(f"no pude preguntarle la version a {py}: {type(e).__name__}: {e}")
    if (may, men) < MINIMO_PY:
        sys.exit(f"ME NIEGO A INSTALAR: ese interprete es Python {may}.{men} y hace falta "
                 f"{MINIMO_PY[0]}.{MINIMO_PY[1]} o superior.\n"
                 f"  Interprete: {py}\n"
                 "  El servicio usa anotaciones `X | None` y en 3.9 no llega ni a arrancar:\n"
                 "  la instalacion terminaria bien y el puente no levantaria nunca.\n"
                 "  Instala uno mas nuevo y vuelve a correr esto CON ese binario.")
    return f"{may}.{men}"


def resolve_claude():
    for name in ("claude", "claude.cmd", "claude.exe"):
        p = shutil.which(name)
        if p:
            return p
    for c in (HOME / ".local/bin/claude", HOME / "AppData/Roaming/npm/claude.cmd"):
        if c.exists():
            return str(c)
    return ""


def read_env_file(path):
    cfg = {}
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg


def read_old_plist():
    """Rescata la config de una instalación previa a mano (macOS)."""
    cfg = {}
    if platform.system() != "Darwin":
        return cfg
    # Este paso es OPCIONAL por definición: rescata una instalación previa que en una
    # máquina nueva no existe. Antes importaba plistlib fuera de la guarda, así que un
    # plistlib roto —MEDIDO el 2026-09-11: dos pythons de Homebrew con pyexpat enlazado
    # contra un libexpat que ya no exporta su símbolo— tumbaba la instalación ENTERA por
    # no poder hacer algo que no había que hacer. Un paso opcional no derriba al principal.
    plistlib = None
    if any((HOME / "Library/LaunchAgents" / f"{lbl}.plist").exists() for lbl in OLD_LABELS):
        try:
            import plistlib
        except Exception as e:
            say(f"  aviso: no puedo leer instalaciones previas ({type(e).__name__}); sigo sin migrar")
            return cfg
    if plistlib is None:
        return cfg
    for lbl in OLD_LABELS:
        p = HOME / "Library/LaunchAgents" / f"{lbl}.plist"
        if p.exists():
            try:
                d = plistlib.loads(p.read_bytes())
                cfg.update(d.get("EnvironmentVariables", {}) or {})
            except Exception:
                pass
    return cfg


def build_config(args):
    """Fusiona config (baja→alta prioridad): defaults < plist viejo < entorno <
    .env previo < --set/flags."""
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in read_old_plist().items()
                if k in VERTEX_KEYS + BRIDGE_KEYS})
    cfg.update({k: os.environ[k] for k in VERTEX_KEYS + BRIDGE_KEYS
                if k in os.environ})
    cfg.update(read_env_file(ENV_FILE))
    for pair in (args.set or []):
        if "=" in pair:
            k, v = pair.split("=", 1)
            cfg[k.strip()] = v.strip()
    if args.port:
        cfg["PORT"] = str(args.port)
    if args.model:
        cfg["BRIDGE_MODEL"] = args.model
    if args.permission:
        cfg["BRIDGE_PERMISSION"] = args.permission
    if args.cwd:
        cfg["BRIDGE_CWD"] = str(Path(args.cwd).expanduser().resolve())
    cfg.setdefault("BRIDGE_CWD", str(Path.cwd()))
    # El permiso se DECLARA o no se instala. `full` concede ejecucion arbitraria con
    # los privilegios de quien instala, y nadie debe heredarla por omision.
    if not cfg.get("BRIDGE_PERMISSION"):
        sys.exit("FALTA EL PERMISO — y es a proposito que no haya default.\n"
                 "  Vuelve a correr esto con uno de:\n"
                 "    --permission safe    solo lee, busca y conversa\n"
                 "    --permission tools   ademas python y web\n"
                 "    --permission full    TODO: ejecuta, escribe y borra sin preguntar\n"
                 "  Con `full` cualquier proceso local que alcance el puerto ejecuta\n"
                 "  comandos con tus privilegios. Eleges tu, no el instalador.")
    if cfg["BRIDGE_PERMISSION"] not in ("full", "tools", "safe"):
        sys.exit(f"PERMISO DESCONOCIDO: {cfg['BRIDGE_PERMISSION']!r}. Usa full | tools | safe.")
    if not cfg.get("BRIDGE_CLAUDE_BIN"):
        cb = resolve_claude()
        if cb:
            cfg["BRIDGE_CLAUDE_BIN"] = cb
    return cfg


def write_env_file(cfg):
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# vuelamind-rc — config del puente (generado por install.py)",
             "# editable a mano; el servicio la lee al arrancar.", ""]
    for k in VERTEX_KEYS + BRIDGE_KEYS:
        if cfg.get(k):
            lines.append(f"{k}={cfg[k]}")
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # En Windows esto NO protege el archivo: `chmod` solo toca el bit de solo-lectura y
    # los permisos los hereda del perfil de usuario. No falla, y por eso no se nota.
    # Declarado el 2026-09-11: en Windows la protección real pide ACLs (`icacls`).
    try:
        ENV_FILE.chmod(0o600)
    except OSError:
        pass


def copy_assets():
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    for f in ("session_bridge.py", "session_bridge.html"):
        src = ASSETS / f
        if not src.exists():
            sys.exit(f"falta el asset: {src}")
        shutil.copy2(src, INSTALL_DIR / f)
    return INSTALL_DIR / "session_bridge.py"


def warn_missing_vertex(cfg):
    missing = [k for k in ("CLAUDE_CODE_USE_VERTEX", "ANTHROPIC_VERTEX_PROJECT_ID",
                           "CLOUD_ML_REGION") if not cfg.get(k)]
    if missing:
        say("  ⚠️  faltan variables de Vertex/Model Garden: " + ", ".join(missing))
        say("     el servicio arrancará, pero invocar modelos fallará hasta que las")
        say("     pongas:  python install.py --set CLAUDE_CODE_USE_VERTEX=1 "
            "--set ANTHROPIC_VERTEX_PROJECT_ID=<proj> --set CLOUD_ML_REGION=<region>")


def health(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=4) as r:
            return r.status == 200
    except Exception:
        return False


# --------------------------------------------------------------- macOS (launchd)
def install_darwin(python, script, port, start):
    import plistlib
    la = HOME / "Library/LaunchAgents"
    la.mkdir(parents=True, exist_ok=True)
    logs = HOME / "Library/Logs"
    logs.mkdir(parents=True, exist_ok=True)
    uid = os.getuid()
    # baja servicios previos (incluida la versión a mano) para no chocar el puerto
    for lbl in [LABEL] + OLD_LABELS:
        subprocess.run(["launchctl", "bootout", f"gui/{uid}/{lbl}"],
                       capture_output=True)
    # y borra los plist VIEJOS: si no, al próximo login se recargarían y chocarían
    for lbl in OLD_LABELS:
        old = la / f"{lbl}.plist"
        if old.exists():
            old.unlink()
            say(f"  · migrado: removido plist viejo {lbl}")
    plist = la / f"{LABEL}.plist"
    data = {
        "Label": LABEL,
        "ProgramArguments": [python, str(script)],
        "EnvironmentVariables": {"VUELAMIND_RC_ENV": str(ENV_FILE)},
        "RunAtLoad": True, "KeepAlive": True,
        "StandardOutPath": str(logs / "vuelamind-rc.log"),
        "StandardErrorPath": str(logs / "vuelamind-rc.log"),
    }
    plist.write_bytes(plistlib.dumps(data))
    if start:
        subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist)],
                       capture_output=True)
        subprocess.run(["launchctl", "enable", f"gui/{uid}/{LABEL}"],
                       capture_output=True)
    return f"LaunchAgent → {plist}"


def uninstall_darwin():
    uid = os.getuid()
    for lbl in [LABEL] + OLD_LABELS:
        subprocess.run(["launchctl", "bootout", f"gui/{uid}/{lbl}"], capture_output=True)
    p = HOME / "Library/LaunchAgents" / f"{LABEL}.plist"
    if p.exists():
        p.unlink()
    return "LaunchAgent removido"


# --------------------------------------------------------------- Windows (schtasks)
# MEDIDO en Windows 11 el 2026-09-11, con dos reinicios: la tarea se creaba bien —«At
# logon time», usuario correcto— y NO DISPARABA NUNCA. Last Run Time se quedaba en la vez
# que se forzó a mano. El sospechoso, señalado por quien lo midió y NO probado todavía:
# `schtasks /Create` deja por defecto «No Start On Batteries / Stop On Battery Mode», que
# es la causa clásica de tareas que no arrancan en VMs y portátiles.
#
# Por eso la tarea se crea ahora desde XML, que es la única vía por la que `schtasks` deja
# declarar esas condiciones. El camino viejo queda de respaldo: si el XML falla, se hace
# como antes y se DICE, en vez de quedarse sin autostart en silencio.
#
# Nota de formato, y muerde: `schtasks /Create /XML` quiere el archivo en UTF-16.
TAREA_XML = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>vuelamind-rc session bridge</Description></RegistrationInfo>
  <Triggers><LogonTrigger><Enabled>true</Enabled><UserId>{usuario}</UserId></LogonTrigger></Triggers>
  <Principals><Principal id="Author"><UserId>{usuario}</UserId>
    <LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author"><Exec><Command>{exe}</Command><Arguments>"{script}"</Arguments></Exec></Actions>
</Task>"""


def install_windows(python, script, port, start):
    pyw = python
    cand = Path(python).with_name("pythonw.exe")
    if cand.exists():
        pyw = str(cand)                       # sin ventana de consola
    tr = f'"{pyw}" "{script}"'
    subprocess.run(["schtasks", "/Delete", "/TN", "VuelamindRC", "/F"],
                   capture_output=True)
    usuario = os.environ.get("USERDOMAIN", "") + "\\" + os.environ.get("USERNAME", "")
    xml = Path(os.environ.get("TEMP", ".")) / "vuelamind-rc-tarea.xml"
    creada = False
    try:
        xml.write_text(TAREA_XML.format(usuario=usuario.lstrip("\\"), exe=pyw, script=script),
                       encoding="utf-16")
        r = subprocess.run(["schtasks", "/Create", "/TN", "VuelamindRC", "/XML", str(xml), "/F"],
                           capture_output=True, text=True)
        creada = r.returncode == 0
        if not creada:
            say(f"  aviso: no pude crear la tarea desde XML ({r.stderr.strip()[:120]});"
                " uso el modo básico, que puede NO dispararse con la máquina en batería")
    except Exception as e:
        say(f"  aviso: fallo al escribir el XML de la tarea ({type(e).__name__}); uso el modo básico")
    finally:
        try:
            xml.unlink()
        except Exception:
            pass
    if not creada:
        subprocess.run(["schtasks", "/Create", "/SC", "ONLOGON", "/TN", "VuelamindRC",
                        "/TR", tr, "/RL", "LIMITED", "/F"], check=True)
    if start:
        # arranca ya, sin esperar al próximo login
        subprocess.Popen([pyw, str(script)],
                         creationflags=getattr(subprocess, "DETACHED_PROCESS", 0))
    return "Tarea Programada 'VuelamindRC' (al iniciar sesión)"


def uninstall_windows():
    subprocess.run(["schtasks", "/Delete", "/TN", "VuelamindRC", "/F"],
                   capture_output=True)
    return "Tarea Programada removida (el proceso vivo, si lo hay, ciérralo a mano)"


# --------------------------------------------------------------- Linux (systemd --user)
def install_linux(python, script, port, start):
    unit_dir = HOME / ".config/systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    unit = unit_dir / "vuelamind-rc.service"
    unit.write_text(
        "[Unit]\nDescription=vuelamind-rc session bridge\n\n"
        "[Service]\n"
        f"Environment=VUELAMIND_RC_ENV={ENV_FILE}\n"
        f"ExecStart={python} {script}\nRestart=always\n\n"
        "[Install]\nWantedBy=default.target\n", encoding="utf-8")
    if shutil.which("systemctl"):
        subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
        if start:
            subprocess.run(["systemctl", "--user", "enable", "--now",
                            "vuelamind-rc.service"], capture_output=True)
        return f"systemd --user → {unit}"
    if start:                                  # sin systemd: arranque suelto
        subprocess.Popen([python, str(script)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"unidad escrita en {unit} (systemctl no disponible; arranque suelto)"


def uninstall_linux():
    if shutil.which("systemctl"):
        subprocess.run(["systemctl", "--user", "disable", "--now",
                        "vuelamind-rc.service"], capture_output=True)
    u = HOME / ".config/systemd/user/vuelamind-rc.service"
    if u.exists():
        u.unlink()
    return "unidad systemd removida"


# --------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Instalador portable de vuelamind-rc")
    ap.add_argument("--cwd", help="dir de trabajo por defecto de las sesiones")
    ap.add_argument("--port", type=int)
    ap.add_argument("--model")
    ap.add_argument("--permission", choices=["full", "tools", "safe"])
    ap.add_argument("--set", action="append", metavar="KEY=VALUE",
                    help="fija una variable en el .env (repetible)")
    ap.add_argument("--no-start", action="store_true")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)

    osname = platform.system()
    python = sys.executable or shutil.which("python3") or shutil.which("python")

    if args.status:
        port = read_env_file(ENV_FILE).get("PORT", "8850")
        ok = health(port)
        say(f"{'✅ arriba' if ok else '❌ no responde'}  ·  http://127.0.0.1:{port}/")
        return 0 if ok else 1

    if args.uninstall:
        fn = {"Darwin": uninstall_darwin, "Windows": uninstall_windows,
              "Linux": uninstall_linux}.get(osname)
        say(fn() if fn else f"SO no soportado para desinstalar: {osname}")
        return 0

    ver = exigir_python(python)
    say(f"· sistema: {osname}   python: {python}  ({ver})")
    cfg = build_config(args)
    script = copy_assets()
    write_env_file(cfg)
    say(f"· config  → {ENV_FILE}")
    say(f"· código  → {INSTALL_DIR}")
    say(f"· claude  → {cfg.get('BRIDGE_CLAUDE_BIN') or '(no encontrado — ponlo con --set BRIDGE_CLAUDE_BIN=...)'}")
    say(f"· cwd     → {cfg.get('BRIDGE_CWD')}")
    say(f"· permiso → {cfg.get('BRIDGE_PERMISSION')}   modelo: {cfg.get('BRIDGE_MODEL')}")
    warn_missing_vertex(cfg)

    installer = {"Darwin": install_darwin, "Windows": install_windows,
                 "Linux": install_linux}.get(osname)
    if not installer:
        sys.exit(f"SO no soportado: {osname}. Corre a mano: python {script}")
    # Instalar el arranque automático de un servicio que ACABAS DE COMPROBAR que no puede
    # arrancar garantiza un fallo mudo en cada inicio de sesión. MEDIDO en Windows 11 el
    # 2026-09-11: sin el CLI, el instalador lo reportaba y creaba la tarea igual; el
    # servicio salía con código 1 diciendo «no encuentro el binario claude», y como el
    # autostart usa pythonw.exe —sin ventana— ese mensaje no llegaba a ningún sitio.
    if not cfg.get("BRIDGE_CLAUDE_BIN") and not args.no_start:
        sys.exit("NO INSTALO EL ARRANQUE AUTOMATICO: no encuentro el CLI `claude`.\n"
                 "  El servicio no puede levantar sin el, y el autostart correria sin\n"
                 "  ventana: fallaria mudo en cada inicio de sesion.\n"
                 "  Instala el CLI, o dime donde esta:\n"
                 "     --set BRIDGE_CLAUDE_BIN=<ruta al ejecutable>\n"
                 "  (Si solo querias copiar los archivos, usa --no-start.)")

    if args.no_start:
        # `--no-start` significaba «no arranques AHORA» y dejaba el autostart escrito, asi
        # que el servicio aparecia solo en el siguiente inicio de sesion. Instalar el
        # arranque automatico y arrancar son DOS cosas; esta bandera gobierna las dos.
        say("· autostart → NO instalado (--no-start). Para ponerlo, corre esto sin la bandera.")
        say(f"· a mano:  {python} {script}")
    else:
        where = installer(python, script, cfg["PORT"], True)
        say(f"· autostart → {where}")

    if not args.no_start:
        import time
        for _ in range(6):
            time.sleep(1)
            if health(cfg["PORT"]):
                break
        ok = health(cfg["PORT"])
        say(("✅ servicio arriba" if ok else
             "⚠️  instalado, pero /health no responde aún — revisa el log"))
    port = cfg["PORT"]
    say("")
    say(f"Página:  http://127.0.0.1:{port}/   (solo loopback · sin token)")
    say(f"Túnel:   ssh -N -L {port}:127.0.0.1:{port} <usuario>@<esta-máquina>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
