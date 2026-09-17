#!/usr/bin/env python3
"""rc_estado — ¿qué versión del puente corre esta máquina, y cuánto le falta?

EL HUECO QUE CIERRA: el salto de versión actualiza el CANON, no lo que nació de él. Un
servicio instalado vive en su directorio, con su `.env` y su proceso, y **nadie sabía
preguntarle qué versión corre** — porque el puente no tiene ninguna escrita.

CÓMO LO RESUELVE SIN INVENTAR UN CAMPO NUEVO: la historia del canon ES el registro de
versiones. Cada commit que tocó un archivo deja la huella exacta de su contenido en ese
momento, así que una copia instalada se identifica buscando su huella en esa historia. Tres
desenlaces, y el tercero es el que importa:

  · coincide con HEAD            → al día
  · coincide con un commit viejo → atrasado, y se puede decir EXACTAMENTE qué entró desde él
  · no coincide con ninguno      → modificado localmente, o de otra procedencia.
                                   NO se pisa: se dice y decide una persona.

Ese tercer caso es el que un comparador ingenuo se come: «distinto de HEAD» junta «viejo» con
«tuyo», y sobrescribir lo segundo borra trabajo ajeno sin avisar.

Salidas: 0 = al día · 1 = atrasado · 2 = no hay instalación · 3 = desconocido o modificado
         4 = error de uso o de acceso al canon
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ARCHIVOS = ("session_bridge.py", "session_bridge.html")
EN_CANON = "herramientas/interfaz_agente"


def huella(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def git(clon: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", clon, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "").strip()[:300] or f"git {' '.join(args)} falló")
    return r.stdout


def git_bytes(clon: str, *args: str) -> bytes:
    r = subprocess.run(["git", "-C", clon, *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} falló")
    return r.stdout


def identificar(clon: str, ref: str, archivo: str, instalado: bytes) -> dict:
    """Busca la huella del archivo instalado en la historia del canon."""
    ruta = f"{EN_CANON}/{archivo}"
    h_inst = huella(instalado)
    h_head = huella(git_bytes(clon, "show", f"{ref}:{ruta}"))
    if h_inst == h_head:
        return {"estado": "al-dia", "huella": h_inst}
    commits = git(clon, "log", "--format=%H", ref, "--", ruta).split()
    for i, c in enumerate(commits):
        if huella(git_bytes(clon, "show", f"{c}:{ruta}")) == h_inst:
            titulos = [l for l in git(clon, "log", "--format=%s",
                                      f"{c}..{ref}", "--", ruta).splitlines() if l]
            fecha = git(clon, "log", "-1", "--format=%ad", "--date=short", c).strip()
            return {"estado": "atrasado", "huella": h_inst, "commit": c[:12],
                    "fecha": fecha, "detras": len(titulos), "cambios": titulos}
    return {"estado": "desconocido", "huella": h_inst}


def main() -> int:
    args = [a for a in sys.argv[1:]]
    dir_inst = None
    if "--dir" in args:
        i = args.index("--dir")
        dir_inst = Path(args[i + 1]).expanduser()
        del args[i:i + 2]
    ref = "origin/main"
    if "--ref" in args:
        i = args.index("--ref")
        ref = args[i + 1]
        del args[i:i + 2]
    if not args:
        print("uso: rc_estado.py [--dir <instalacion>] [--ref <ref>] <clon-del-canon>",
              file=sys.stderr)
        return 4
    clon = args[0]
    if dir_inst is None:
        dir_inst = Path.home() / ".claude" / "vuelamind-rc"

    if not dir_inst.is_dir():
        print(f"NO HAY INSTALACION en {dir_inst}")
        print("  Esta maquina no tiene el puente instalado. Para instalarlo: /vuelamind-rc.")
        print("  (Este guion NO instala: solo mide lo que ya existe.)")
        return 2
    try:
        git(clon, "rev-parse", "--git-dir")
    except Exception as e:
        print(f"NO PUEDO LEER EL CANON en {clon}: {e}", file=sys.stderr)
        return 4

    faltan = [f for f in ARCHIVOS if not (dir_inst / f).exists()]
    if faltan:
        print(f"INSTALACION INCOMPLETA en {dir_inst}: falta {', '.join(faltan)}")
        return 3

    print(f"instalacion : {dir_inst}")
    print(f"canon       : {clon}  ({ref})")
    res = {}
    for f in ARCHIVOS:
        res[f] = identificar(clon, ref, f, (dir_inst / f).read_bytes())

    peor = 0
    for f, r in res.items():
        if r["estado"] == "al-dia":
            print(f"  {f:22} AL DIA")
        elif r["estado"] == "atrasado":
            peor = max(peor, 1)
            print(f"  {f:22} ATRASADO — es la version del {r['fecha']} ({r['commit']}), "
                  f"{r['detras']} cambio(s) detras:")
            for t in r["cambios"]:
                print(f"      · {t}")
        else:
            peor = max(peor, 3)
            print(f"  {f:22} DESCONOCIDO — su huella no esta en la historia del canon.")
            print( "                         Esta modificado localmente o viene de otra parte.")
            print(f"                         huella: {r['huella'][:16]}...")

    # El .py exige reiniciar el servicio; el .html se recarga solo. Confundirlo hace que un
    # arreglo parezca aplicado sin estarlo, asi que se dice aqui y no en la cabeza de nadie.
    #
    # PERO SOLO SE DICE CUANDO APLICA. Si algo salio DESCONOCIDO, la pregunta no es si hay
    # que reiniciar: es si hay que sobrescribir, y eso lo decide una persona. Dar el consejo
    # operativo ahi seria cierto en una rama y enganoso en la otra —medido: la primera
    # version de este guion decia "basta recargar" sobre un archivo modificado a mano—.
    if any(r["estado"] == "desconocido" for r in res.values()):
        print("\nNO ACTUALICES A CIEGAS: hay al menos un archivo que no viene del canon.")
        print("  Comparalo antes de decidir:")
        print(f"    diff <(git -C {clon} show {ref}:{EN_CANON}/<archivo>) {dir_inst}/<archivo>")
        print("  Si el cambio local vale, sale al canon como propuesta; no se pisa en silencio.")
    elif res["session_bridge.py"]["estado"] != "al-dia":
        print("\nREINICIO NECESARIO si actualizas: cambia el backend (session_bridge.py).")
    elif res["session_bridge.html"]["estado"] != "al-dia":
        print("\nSIN REINICIO: solo cambia la pagina; basta recargar el navegador.")

    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False))
    return peor


if __name__ == "__main__":
    sys.exit(main())
