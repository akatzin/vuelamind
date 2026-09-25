#!/usr/bin/env python3
"""Quién enlaza una nota y a quién enlaza ella, calculado EN VIVO.

EL HUECO QUE CIERRA: el ciclo obliga a barrer el radio de un cambio AL ESCRIBIR —qué
notas vuelve falsas, quién lo cita—. No hay nada equivalente AL RESPONDER, y ahí es
donde se contesta sobre una nota sin mirar las que hablan de lo mismo. Nada lo delata:
la respuesta sale coherente, enlaza bien y no contradice a nadie.

POR QUÉ NO ES UN ARCHIVO DE ÍNDICE: los enlaces YA tienen esa información. Un índice
sería una segunda copia de algo derivable, y deja de nombrar una relación en cuanto
alguien añade un enlace y no lo toca — sin fallar al hacerlo: simplemente calla, que es
el fallo que venía a evitar. Calcularlo en vivo cuesta un segundo sobre un centenar de
notas y no puede mentir.

    python3 vecinas.py <nota> <vault>                 quién la enlaza y a quién enlaza
    python3 vecinas.py --sirvio "<qué cambió>" <vault>   la última corrida SÍ cambió algo
    python3 vecinas.py --nada "<por qué no>" <vault>     la última corrida NO cambió nada
    python3 vecinas.py --informe <vault>              qué ha dado de sí, con números

Salidas: 0 = bien · 1 = no hay ninguna que se le parezca · 2 = error de uso
"""
import collections
import datetime
import pathlib
import re
import sys
import unicodedata

# ---------------------------------------------------------------- el registro de uso
#
# Existe porque la pregunta «¿esto sirve?» no se puede contestar de memoria, y a este
# instrumento se la van a hacer. Cuenta DOS cosas distintas y no las mezcla:
#
#   · cuántas veces se corrió y qué encontró  -> lo anota el propio guion, solo
#   · cuántas veces CAMBIÓ una respuesta      -> eso el guion NO puede saberlo, y no
#     lo finge: lo marca quien la escribió, con --sirvio
#
# Y SE PUEDE MARCAR QUE NO SIRVIÓ, con --nada. Sin esa mitad, el registro solo sabe
# crecer a favor: quien marca cuando acierta y calla cuando no, fabrica una estadística
# que dice que todo funciona. Medido en la primera corrida real de este contador — se
# anotó «no cambió nada» y quedó contado como que sí.
#
# Un contador que dedujera lo segundo de lo primero estaría inventando el dato que más
# importa. Vive junto al vault y no dentro: es telemetría del instrumento, no
# conocimiento del dominio, y no tiene por qué viajar con el vault ni ensuciarlo.


def registro_de(vault: pathlib.Path) -> pathlib.Path:
    """Un registro POR VAULT, con su nombre dentro.

    Decia `.vecinas-uso.tsv` a secas, y eso hacia que **varios vaults que cuelgan del
    mismo padre compartieran un solo registro**. Medido en una maquina con tres:
    el `--informe` de una casa mostraba una corrida marcada «SI» que era de otra.

    El daño no es cosmetico: la cifra que decide si este instrumento se queda es la
    SUMA entre casas, y con registros compartidos las lineas se cuentan dos veces —
    un unico «SI» ajeno puede salvar lo que ninguna casa habria salvado sola.

    La regla, que vale mas que el arreglo: **un archivo de estado colocado «al lado»
    de lo que describe hereda el espacio de nombres del PADRE, no la identidad del
    hijo.** Se nota tarde, porque con un solo hijo funciona perfecto — y con un solo
    hijo se prueba.
    """
    return vault.parent / f".vecinas-uso-{vault.name}.tsv"


def anotar(vault: pathlib.Path, nota: str, entrantes: int, salientes: int) -> None:
    """Una línea por corrida. Si no se puede escribir, se calla: medir el uso nunca
    puede ser motivo de que la herramienta falle."""
    try:
        linea = "\t".join([datetime.datetime.now().isoformat(timespec="seconds"),
                           nota, str(entrantes), str(salientes), ""])
        with registro_de(vault).open("a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass


def marcar(vault: pathlib.Path, razon: str, sirvio: bool) -> int:
    """Marca la ÚLTIMA corrida como útil. Se hace aparte y después a propósito: en el
    momento de correrlo todavía no se sabe si va a cambiar algo — eso se sabe al
    escribir la respuesta, que es más tarde."""
    reg = registro_de(vault)
    if not reg.exists():
        print("no hay ninguna corrida registrada todavía.")
        return 1
    lineas = reg.read_text(encoding="utf-8").splitlines()
    if not lineas:
        print("el registro está vacío.")
        return 1
    campos = lineas[-1].split("\t")
    while len(campos) < 5:
        campos.append("")
    campos[4] = ("SI" if sirvio else "NO") + "\t" + razon.replace("\t", " ").strip()
    lineas[-1] = "\t".join(campos[:5]) + ("\t" + campos[5] if len(campos) > 5 else "")
    reg.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    verbo = "cambió algo" if sirvio else "NO cambió nada"
    print(f"anotado: la corrida sobre «{campos[1]}» {verbo} — {razon.strip()}")
    return 0


def informe(vault: pathlib.Path) -> int:
    reg = registro_de(vault)
    if not reg.exists():
        print("sin corridas registradas. El instrumento existe y nadie lo ha usado:")
        print("eso también es un dato, y es el que más dice.")
        return 0
    filas = [l.split("\t") for l in reg.read_text(encoding="utf-8").splitlines() if l.strip()]
    utiles = [f for f in filas if len(f) > 4 and f[4] == "SI"]
    nada = [f for f in filas if len(f) > 4 and f[4] == "NO"]
    sin_marcar = [f for f in filas if len(f) < 5 or f[4] not in ("SI", "NO")]
    con_vecinas = [f for f in filas if len(f) > 3 and (f[2] != "0" or f[3] != "0")]
    razon = lambda f: f[5] if len(f) > 5 else ""
    print(f"── {len(filas)} corrida(s) desde {filas[0][0][:10]}")
    print(f"   con vecinas que enseñar: {len(con_vecinas)}")
    print(f"   CAMBIARON una respuesta:  {len(utiles)}   <- la cifra que decide si esto sube al canon")
    print(f"   no cambiaron nada:        {len(nada)}")
    print(f"   sin marcar:               {len(sin_marcar)}   <- ni a favor ni en contra: nadie dijo")
    for f in utiles:
        print(f"        SI · {f[0][:10]} · {f[1]} — {razon(f)}")
    for f in nada:
        print(f"        NO · {f[0][:10]} · {f[1]} — {razon(f)}")
    if sin_marcar and not utiles and not nada:
        print("\n   Nadie ha marcado ninguna. O no ha servido, o nadie se acordó de decirlo:")
        print("   las dos cosas se arreglan distinto, y confundirlas es el error a evitar.")
    return 0


# ---------------------------------------------------------------- el cálculo
def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).casefold()
    return s[:-3] if s.endswith(".md") else s


def vecinas(vault: pathlib.Path, consulta: str) -> int:
    notas = {p: p.read_text(encoding="utf-8", errors="replace") for p in vault.rglob("*.md")}
    if not notas:
        print(f"no encontré notas en {vault}", file=sys.stderr)
        return 2

    # El nombre por el que un wikilink se refiere a una nota es su basename sin extensión.
    por_nombre = {norm(p.name): p for p in notas}

    salientes = {}
    for p, t in notas.items():
        # [[Nota]], [[Nota|alias]] y [[Nota#sección]] apuntan todos a la misma nota.
        destinos = set()
        for c in re.findall(r"\[\[([^\]]+)\]\]", t):
            base = norm(c.split("|")[0].split("#")[0].strip())
            if base in por_nombre:
                destinos.add(por_nombre[base])
        salientes[p] = destinos - {p}

    entrantes = collections.defaultdict(set)
    for p, ds in salientes.items():
        for d in ds:
            entrantes[d].add(p)

    q = norm(consulta)
    elegida = por_nombre.get(q)
    if elegida is None:
        # Sin coincidencia exacta se ofrecen las parecidas, en vez de decir "no existe" a
        # secas: quien se equivoca de nombre no sabe cuál es el bueno, que es justo por lo
        # que pregunta.
        cerca = sorted(p.name for n, p in por_nombre.items() if q in n)
        if not cerca:
            print(f"no hay ninguna nota que se parezca a «{consulta}»")
            return 1
        if len(cerca) > 1:
            print(f"«{consulta}» encaja con varias — precisa cuál:")
            for c in cerca[:12]:
                print("   ·", c)
            return 1
        elegida = por_nombre[norm(cerca[0])]

    rel = lambda p: str(p.relative_to(vault))
    ent = sorted(entrantes.get(elegida, ()), key=rel)
    sal = sorted(salientes.get(elegida, ()), key=rel)

    print(f"── {rel(elegida)}")
    print(f"\n   ← LA ENLAZAN ({len(ent)})" + ("" if ent else "   — nadie. Si esta nota "
          "importa, nada la delata: alguien tendrá que citarla desde donde se decide."))
    for p in ent:
        print("        ", rel(p))
    print(f"\n   → ENLAZA A ({len(sal)})" + ("" if sal else "   — a nadie."))
    for p in sal:
        print("        ", rel(p))

    # Las dos direcciones sirven para cosas distintas, y conviene decirlo en vez de suponer
    # que se entiende: hacia adentro está quien puede quedarse desactualizado; hacia afuera,
    # lo que hay que leer antes de afirmar.
    print(f"\n   quién puede quedar desactualizado si cambias ésta: las {len(ent)} de arriba.")
    print(f"   qué conviene leer antes de afirmar sobre ella: las {len(sal)} de abajo.")

    anotar(vault, rel(elegida), len(ent), len(sal))
    if ent or sal:
        print("\n   ¿Cambió lo que ibas a decir? Anótalo, en un sentido o en el otro — es la")
        print("   única forma de saber si esto sirve, y el 'no' cuenta tanto como el 'sí':")
        print(f"        vecinas.py --sirvio \"<qué cambió>\" {vault}")
        print(f"        vecinas.py --nada   \"<por qué no>\" {vault}")
    return 0


def main(argv) -> int:
    if len(argv) >= 2 and argv[1] in ("--sirvio", "--nada"):
        if len(argv) < 4:
            print(f"uso: vecinas.py {argv[1]} \"<razón>\" <vault>", file=sys.stderr)
            return 2
        return marcar(pathlib.Path(argv[3]).expanduser(), argv[2], argv[1] == "--sirvio")
    if len(argv) >= 3 and argv[1] == "--informe":
        return informe(pathlib.Path(argv[2]).expanduser())
    if len(argv) < 3:
        print("uso:\n"
              "    python3 vecinas.py <nota> <vault>\n"
              "    python3 vecinas.py --sirvio \"<qué cambió>\" <vault>\n"
              "    python3 vecinas.py --informe <vault>", file=sys.stderr)
        return 2
    vault = pathlib.Path(argv[2]).expanduser()
    if not vault.is_dir():
        print(f"el vault no existe: {vault}", file=sys.stderr)
        return 2
    return vecinas(vault, argv[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
