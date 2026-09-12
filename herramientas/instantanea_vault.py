#!/usr/bin/env python3
"""Instantánea del vault, para que el cierre pueda RELEER lo que se escribió.

EL HUECO QUE CIERRA. El ciclo comprueba el RADIO de un cambio —las vecinas de las notas
tocadas— y el validador comprueba MECÁNICA —conteos, enlaces, huellas—. Nadie relee lo que
se ESCRIBIÓ. Un párrafo nuevo que afirma algo falso pasa los dos: cuadra, enlaza y no
contradice a nadie porque es lo único que habla de ese tema. Es la única parte del cierre
que nada comprueba, y el vault es la memoria del dominio.

CUÁNDO SE TOMA, que es lo único que hay que entender: la copia se RENUEVA AL TERMINAR cada
cierre, no al empezarlo. Tomada al empezar, ya traería dentro todo lo que la sesión escribió
y el diff saldría vacío — y un diff vacío no dice «no pude comparar», dice «no cambió nada».
Renovada al terminar, el diff del cierre siguiente cubre todo lo escrito desde el anterior,
que además es la unidad correcta: lo que NADIE HA RELEÍDO todavía, porque una sesión que no
llegó a cerrar también escribió.

POR QUÉ NO ES GIT. Lo que hace falta es el diff de un tramo, no una historia. Meter un
repositorio sube la barrera para quien no es técnico sin dar nada que este diff no dé, y el
método sirve a casas que no tienen por qué aprender git para poder releerse. Un dominio que
YA viva en git usa el suyo y se salta esto.

    python3 instantanea_vault.py diff    <vault>   al cerrar: qué se escribió desde el anterior
    python3 instantanea_vault.py renovar <vault>   al TERMINAR el cierre, ya releído
    python3 instantanea_vault.py tomar   <vault>   la primera vez, o si se perdió
    python3 instantanea_vault.py tirar   <vault>

En Python y no en shell a propósito: el marco ya exige Python en todas las plataformas, y un
.sh no corre en Windows sin traerse otra cosa. Una herramienta del ciclo que media casa no
puede ejecutar no es una herramienta del ciclo.
"""

import difflib
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

IGNORADOS = {".obsidian", ".git", ".trash", "node_modules"}


def notas(vault: Path):
    """Las notas del vault, en rutas relativas y ordenadas."""
    return sorted(
        p.relative_to(vault)
        for p in vault.rglob("*.md")
        if not IGNORADOS & set(p.relative_to(vault).parts)
    )


def donde(vault: Path) -> Path:
    """Una copia por vault: dos dominios en la misma máquina no se pisan."""
    sello = hashlib.sha256(str(vault).encode()).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"vuelamind-instantanea-{sello}"


def tomar(vault: Path, copia: Path, verbo: str) -> int:
    if copia.exists():
        shutil.rmtree(copia)
    for rel in notas(vault):
        destino = copia / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(vault / rel, destino)
    n = len(notas(vault))
    print(f"instantánea {verbo}: {n} notas")
    print("  el próximo cierre comparará contra esto")
    return 0


def diff(vault: Path, copia: Path) -> int:
    if not copia.exists():
        print("NO HAY INSTANTÁNEA — este cierre NO puede releer lo que se escribió.",
              file=sys.stderr)
        print(f"  Se toma una vez:  python3 {Path(__file__).name} tomar {vault}",
              file=sys.stderr)
        print("  y se renueva al terminar cada cierre, ya releída.", file=sys.stderr)
        return 3

    actuales = notas(vault)
    nuevas = [r for r in actuales if not (copia / r).exists()]
    if nuevas:
        # aparte, porque una nota nueva NO TIENE con qué compararse: mezclarla con las
        # modificadas la colaría como si estuviera revisada
        print("== NOTAS NUEVAS — no tienen con qué compararse, nadie las ha releído ==")
        for r in nuevas:
            print(f"  {r}")
        print()

    borradas = [r for r in notas(copia) if not (vault / r).exists()]
    if borradas:
        print("== NOTAS QUE YA NO ESTÁN ==")
        for r in borradas:
            print(f"  {r}")
        print()

    print("== LO QUE CAMBIÓ EN LAS QUE YA EXISTÍAN ==")
    hubo = False
    for rel in actuales:
        viejo = copia / rel
        if not viejo.exists():
            continue
        a = viejo.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        b = (vault / rel).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        if a == b:
            continue
        hubo = True
        sys.stdout.writelines(difflib.unified_diff(a, b, f"antes/{rel}", f"ahora/{rel}"))
        print()
    if not hubo and not nuevas and not borradas:
        print("  (nada: no se ha escrito nada desde el cierre anterior)")
    return 0


def main(argv) -> int:
    if len(argv) < 3:
        print(f"uso: {Path(__file__).name} diff|renovar|tomar|tirar <ruta-del-vault>",
              file=sys.stderr)
        return 1
    accion, ruta = argv[1], argv[2]
    vault = Path(ruta).expanduser().resolve()
    if not vault.is_dir():
        print(f"no existe el vault: {vault}", file=sys.stderr)
        return 2
    copia = donde(vault)

    if accion in ("tomar", "renovar"):
        return tomar(vault, copia, "renovada" if accion == "renovar" else "tomada")
    if accion == "diff":
        return diff(vault, copia)
    if accion == "tirar":
        if copia.exists():
            shutil.rmtree(copia)
        print("instantánea tirada")
        return 0
    print(f"acción desconocida: {accion}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
