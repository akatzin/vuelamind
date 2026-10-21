#!/usr/bin/env python3
"""La cola de pendientes, un archivo por pendiente, y su indice generado.

LO QUE HACE CUMPLIR: un pendiente cerrado sale de la carpeta de abiertos, deja su
parrafo de cierre y nadie lo vuelve a cargar al trabajar. `revisar` sale con 1 si no
se cumple.

    <vault>/Pendientes.md                 el indice: cabecera a mano, lo demas generado
    <vault>/pendientes/<folio>.md         un abierto
    <vault>/pendientes/cerrados/<folio>.md
    <vault>/pendientes/riesgo/<folio>.md  riesgo aceptado

    python3 pendientes.py nuevo   <vault> "<titulo>" [--severidad media]
    python3 pendientes.py cerrar  <vault> <folio>
    python3 pendientes.py indice  <vault>
    python3 pendientes.py revisar <vault> [--max-lineas 80]
    python3 pendientes.py migrar  <vault> [--escribir]      sin --escribir, solo ensaya

    --cola <nombre>     el indice, si no se llama Pendientes.md (clave `notas: cola`)
    --archivo <nombre>  el archivo de cerrados de antes de migrar (clave `notas: archivo`);
                        sus folios cuentan como existentes. Por omision Pendientes_Cerrados.md

Un pendiente se mueve a riesgo aceptado con `mv` y despues `indice`.

Salidas: 0 = bien · 1 = hallazgos o no se pudo · 2 = error de uso
"""
import collections
import datetime
import os
import pathlib
import re
import sys

MARCA = "<!-- pendientes.py: lo de abajo se genera; no se edita a mano -->"
FALTA = "FALTA el parrafo de cierre: que era, que se hizo y como se verifico."
CARPETAS = {"abiertos": "", "cerrados": "cerrados", "riesgo": "riesgo"}
TITULO = re.compile(r"^# #(\d+) · (.+?)\s*$")
VIEJO = re.compile(r"^### - \[( |x|X)\] #(\d+) · (.+?)\s*$")
SECCION = re.compile(r"^## (.+?)\s*$")


def hoy():
    return datetime.date.today().isoformat()


def leer(p):
    return pathlib.Path(p).read_text(encoding="utf-8")


def partir_frontmatter(texto):
    if texto.startswith("---\n"):
        fin = texto.find("\n---\n", 4)
        if fin != -1:
            return texto[4:fin], texto[fin + 5:]
    return None, texto


def carpeta(vault, estado):
    base = pathlib.Path(vault) / "pendientes"
    return base / CARPETAS[estado] if CARPETAS[estado] else base


def inventario(vault):
    """{folio: (estado, ruta)}, y los errores de nombre o de titulo."""
    items, errores = {}, []
    for estado in CARPETAS:
        d = carpeta(vault, estado)
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            if not p.stem.isdigit():
                errores.append(f"{p}: el nombre no es un folio")
                continue
            folio = int(p.stem)
            primera = (leer(p).splitlines() or [""])[0]
            m = TITULO.match(primera)
            if not m or int(m.group(1)) != folio:
                errores.append(f"{p}: la primera linea no es «# #{folio} · <titulo>»")
            if folio in items:
                errores.append(f"#{folio} esta dos veces: {items[folio][1]} y {p}")
                continue
            items[folio] = (estado, p)
    return items, errores


def legado(vault, archivo):
    """Folios que solo viven en el archivo de cerrados de antes de migrar."""
    p = pathlib.Path(vault) / archivo
    if not p.exists():
        return set()
    return {int(m) for m in re.findall(r"(?m)^#{2,3} (?:- \[[xX]\] )?#(\d+) · ", leer(p))}


def titulo_y_severidad(p):
    lineas = leer(p).splitlines()
    m = TITULO.match(lineas[0]) if lineas else None
    titulo = m.group(2) if m else p.stem
    sev = next((l.split("::", 1)[1].strip() for l in lineas
                if re.match(r"^severidad::", l)), "—")
    return titulo, sev


def generado(vault, items):
    cuenta = collections.Counter(e for e, _ in items.values())
    partes = [MARCA, ""]
    for estado, nombre in (("abiertos", "Abiertos"), ("riesgo", "Riesgo aceptado")):
        partes.append(f"## {nombre} — {cuenta[estado]}")
        partes.append("")
        for folio in sorted((f for f, (e, _) in items.items() if e == estado), reverse=True):
            t, s = titulo_y_severidad(items[folio][1])
            ruta = "pendientes/" + (CARPETAS[estado] + "/" if CARPETAS[estado] else "") + str(folio)
            partes.append(f"- [[{ruta}|#{folio}]] · {s} · {t}")
        partes.append("")
    partes.append(f"## Cerrados — {cuenta['cerrados']}")
    partes.append("")
    partes.append("Cada uno en `pendientes/cerrados/<folio>.md`. No se cargan al trabajar.")
    return "\n".join(partes) + "\n", cuenta


def con_contadores(fm, cuenta):
    claves = {"total_abiertos": cuenta["abiertos"], "cerrados": cuenta["cerrados"],
              "riesgo_aceptado": cuenta["riesgo"]}
    lineas, vistas = [], set()
    for l in (fm or "").splitlines():
        k = l.split(":", 1)[0].strip()
        if k in claves:
            lineas.append(f"{k}: {claves[k]}")
            vistas.add(k)
        else:
            lineas.append(l)
    lineas += [f"{k}: {v}" for k, v in claves.items() if k not in vistas]
    return "\n".join(lineas)


def escribir_indice(vault, cola, cabecera=None):
    p = pathlib.Path(vault) / cola
    carpeta(vault, "abiertos").mkdir(parents=True, exist_ok=True)
    items, errores = inventario(vault)
    if errores:
        return errores
    fm, cuerpo = partir_frontmatter(leer(p)) if p.exists() else (None, "")
    if cabecera is None:
        cabecera = cuerpo.split(MARCA)[0].rstrip("\n") + "\n" if MARCA in cuerpo else cuerpo
    gen, cuenta = generado(vault, items)
    texto = "---\n" + con_contadores(fm, cuenta) + "\n---\n" + cabecera.rstrip("\n") + "\n\n" + gen
    tmp = p.with_name(f"{p.name}.{os.getpid()}.parcial")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, p)
    return []


def cierre_ok(texto):
    """None si el cierre es un parrafo escrito; si no, el motivo."""
    if FALTA in texto:
        return "falta el parrafo de cierre"
    m = re.search(r"(?m)^## Cierre\s*$", texto)
    if not m:
        return "no tiene «## Cierre»"
    resto = texto[m.end():]
    siguiente = re.search(r"(?m)^#{1,2} ", resto)
    resto = resto[:siguiente.start()] if siguiente else resto
    bloques = [b for b in re.split(r"\n\s*\n", resto)
               if b.strip() and not re.match(r"^\s*cerrado::", b.strip())]
    if len(bloques) != 1:
        return f"el cierre tiene {len(bloques)} parrafos; va uno"
    return None


# ------------------------------------------------------------------- las ordenes

def revisar(vault, cola, max_lineas, archivo="Pendientes_Cerrados.md"):
    errores, avisos = [], []
    p = pathlib.Path(vault) / cola
    if not p.exists():
        print(f"MAL  no existe el indice {p}")
        return 1
    texto = leer(p)
    if any(VIEJO.match(l) for l in texto.splitlines()):
        print(f"MAL  {cola} tiene pendientes dentro: la cola no esta migrada "
              f"(python3 pendientes.py migrar {vault})")
        return 1
    items, errores = inventario(vault)
    for folio, (estado, ruta) in sorted(items.items()):
        t = leer(ruta)
        if estado != "cerrados" and (re.search(r"(?m)^## Cierre\s*$", t) or re.search(r"(?m)^cerrado::", t)):
            errores.append(f"#{folio}: tiene cierre y sigue en {ruta.parent.name}/ — muevelo con «cerrar»")
        if estado == "cerrados" and not re.search(r"(?m)^migrado::", t):
            motivo = cierre_ok(t)
            if motivo:
                errores.append(f"#{folio}: {motivo} ({ruta})")
        if estado == "abiertos" and t.count("\n") > max_lineas:
            avisos.append(f"#{folio}: {t.count(chr(10))} lineas; un pendiente se reescribe, no se apila")
    fm, cuerpo = partir_frontmatter(texto)
    if MARCA not in cuerpo:
        errores.append(f"{cola}: le falta la marca del indice generado")
    else:
        gen, cuenta = generado(vault, items)
        if MARCA + cuerpo.split(MARCA, 1)[1] != gen:
            errores.append(f"{cola}: el indice no coincide con las carpetas — corre «indice»")
        for k, est in (("total_abiertos", "abiertos"), ("cerrados", "cerrados"), ("riesgo_aceptado", "riesgo")):
            m = re.search(rf"(?m)^{k}:\s*(\d+)", fm or "")
            if not m or int(m.group(1)) != cuenta[est]:
                errores.append(f"{cola}: {k} no dice {cuenta[est]}")
    # Folios citados desde otras notas: «[[<cola>]] #NN» tiene que existir.
    viejos = legado(vault, archivo)
    tallo = pathlib.Path(cola).stem
    cita = re.compile(r"\[\[" + re.escape(tallo) + r"(?:\|[^\]]*)?\]\]\s*#(\d+)")
    for n in pathlib.Path(vault).rglob("*.md"):
        if "pendientes" in n.relative_to(vault).parts[:1]:
            continue
        for num in cita.findall(leer(n)):
            if int(num) not in items and int(num) not in viejos:
                errores.append(f"{n.relative_to(vault)} cita #{num}, que no existe")
    if items:
        huecos = sorted(set(range(1, max(items) + 1)) - set(items) - viejos)
        if huecos:
            avisos.append(f"folios sin archivo: {', '.join('#' + str(h) for h in huecos)}")
    for e in errores:
        print("MAL  ", e)
    for a in avisos:
        print("AVISO", a)
    print(f"{len(items)} pendientes · {len(errores)} mal · {len(avisos)} avisos")
    return 1 if errores else 0


def nuevo(vault, cola, titulo, severidad):
    items, errores = inventario(vault)
    if errores:
        print("\n".join("MAL  " + e for e in errores)); return 1
    d = carpeta(vault, "abiertos")
    d.mkdir(parents=True, exist_ok=True)
    folio = max(items, default=0) + 1
    while True:
        try:
            with open(d / f"{folio}.md", "x", encoding="utf-8") as f:
                f.write(f"# #{folio} · {titulo}\n\nseveridad:: {severidad}\narea::      \n"
                        f"esfuerzo::  \nbloquea::   --\n\n**Encontrado el {hoy()}**, \n\n"
                        "**El problema.** \n\n**Cómo se comprobó.** \n\n**Lo que NO pasa.** \n\n"
                        "**El arreglo propuesto.** \n\n**Cómo verificar que quedó.** \n")
            break
        except FileExistsError:   # otra instancia lo tomo en el mismo instante
            folio += 1
    errores = escribir_indice(vault, cola)
    print(f"#{folio}: {d / f'{folio}.md'}")
    return 1 if errores else 0


def cerrar(vault, cola, folio):
    origen = carpeta(vault, "abiertos") / f"{folio}.md"
    if not origen.exists():
        print(f"MAL  #{folio} no esta en {origen.parent}"); return 1
    destino = carpeta(vault, "cerrados") / f"{folio}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        print(f"MAL  ya existe {destino}"); return 1
    os.replace(origen, destino)
    with open(destino, "a", encoding="utf-8") as f:
        f.write(f"\n## Cierre\n\ncerrado:: {hoy()}\n\n{FALTA}\n")
    errores = escribir_indice(vault, cola)
    print(f"#{folio} cerrado: {destino}\nEscribe su parrafo en «## Cierre»; «revisar» sale con 1 hasta entonces.")
    return 1 if errores else 0


def migrar(vault, cola, escribir, archivo="Pendientes_Cerrados.md"):
    p = pathlib.Path(vault) / cola
    texto = leer(p)
    fm, cuerpo = partir_frontmatter(texto)
    if MARCA in cuerpo:
        print(f"{cola} ya esta migrada."); return 0
    if any(carpeta(vault, e).is_dir() and any(carpeta(vault, e).glob("*.md")) for e in CARPETAS):
        print("MAL  ya hay archivos en pendientes/: no se mezcla"); return 1
    cabecera, notas, items, estado_sec = [], [], [], None
    actual = None
    for linea in cuerpo.splitlines():
        s = SECCION.match(linea)
        v = VIEJO.match(linea)
        if s and not linea.startswith("### "):
            nombre = s.group(1).lower()
            estado_sec = ("abiertos" if "abierto" in nombre else "cerrados" if "cerrado" in nombre
                          else "riesgo" if "riesgo" in nombre else None)
            actual = None
            if estado_sec is None:
                cabecera.append(linea)
            continue
        if v:
            caja, folio, titulo = v.group(1), int(v.group(2)), v.group(3)
            estado = ("riesgo" if estado_sec == "riesgo" else
                      "cerrados" if caja.lower() == "x" or estado_sec == "cerrados" else "abiertos")
            actual = {"folio": folio, "titulo": titulo, "estado": estado, "lineas": []}
            items.append(actual)
            continue
        if actual is not None:
            actual["lineas"].append(linea)
        elif estado_sec is None:
            cabecera.append(linea)
        else:
            notas.append(linea)
    vistos = collections.Counter(i["folio"] for i in items)
    dobles = [f for f, n in vistos.items() if n > 1]
    if dobles:
        print("MAL  folios repetidos: " + ", ".join("#" + str(f) for f in dobles)); return 1
    archivos = {}
    for i in items:
        cuerpo_i = "\n".join(i["lineas"]).strip("\n")
        extra = f"\nmigrado:: {hoy()}\n" if i["estado"] == "cerrados" else ""
        ruta = carpeta(vault, i["estado"]) / f"{i['folio']}.md"
        archivos[ruta] = f"# #{i['folio']} · {i['titulo']}\n{extra}\n{cuerpo_i}\n"
    if any(l.strip() for l in notas):
        cabecera += ["", "## Lo que vivia entre los pendientes", ""] + notas
    cab = "\n".join(cabecera).strip("\n") + "\n"
    # Que no se pierda nada: cada linea con texto del original sigue en algun archivo.
    antes = collections.Counter(l for l in cuerpo.splitlines()
                                if l.strip() and not VIEJO.match(l) and not SECCION.match(l))
    despues = collections.Counter(l for t in list(archivos.values()) + [cab]
                                  for l in t.splitlines() if l.strip())
    perdidas = antes - despues
    if perdidas:
        print("MAL  se perderian lineas:"); [print("     ", l[:100]) for l in perdidas]; return 1
    cuenta = collections.Counter(i["estado"] for i in items)
    print(f"{len(items)} pendientes: {cuenta['abiertos']} abiertos, {cuenta['cerrados']} cerrados, "
          f"{cuenta['riesgo']} en riesgo aceptado · ninguna linea se pierde")
    if any(l.strip() for l in notas):
        print(f"{sum(1 for l in notas if l.strip())} lineas fuera de un pendiente pasan a la cabecera del indice")
    anclas = [str(n.relative_to(vault)) for n in pathlib.Path(vault).rglob("*.md")
              if re.search(r"\[\[" + re.escape(p.stem) + r"#", leer(n))]
    if anclas:
        print("AVISO enlaces a una seccion de la cola, que dejan de resolver: " + ", ".join(anclas))
    if not escribir:
        print("ENSAYO: no se escribio nada. Con --escribir se hace.")
        return 0
    respaldo = p.with_name(p.name + f".antes-migrar-{hoy()}")
    respaldo.write_text(texto, encoding="utf-8")
    for ruta, t in archivos.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "x", encoding="utf-8") as f:
            f.write(t)
    p.write_text(("---\n" + fm + "\n---\n" if fm is not None else "") + cab, encoding="utf-8")
    errores = escribir_indice(vault, cola, cab)
    print(f"migrada · respaldo en {respaldo.name}")
    return 1 if errores else revisar(vault, cola, 10**9, archivo)


def main(argv):
    args = argv[1:]
    def opcion(nombre, defecto):
        if nombre in args:
            i = args.index(nombre); v = args[i + 1]; del args[i:i + 2]; return v
        return defecto
    try:
        cola = opcion("--cola", "Pendientes.md")
        sev = opcion("--severidad", "media")
        maxl = int(opcion("--max-lineas", "80"))
        archivo = opcion("--archivo", "Pendientes_Cerrados.md")
        escribir = "--escribir" in args
        args = [a for a in args if a != "--escribir"]
        orden, vault = args[0], args[1]
    except (IndexError, ValueError):
        print(__doc__); return 2
    if not pathlib.Path(vault).is_dir():
        print(f"no existe el vault {vault}"); return 2
    if orden == "revisar":
        return revisar(vault, cola, maxl, archivo)
    if orden == "indice":
        e = escribir_indice(vault, cola)
        print("\n".join("MAL  " + x for x in e) or "indice al dia"); return 1 if e else 0
    if orden == "nuevo" and len(args) == 3:
        return nuevo(vault, cola, args[2], sev)
    if orden == "cerrar" and len(args) == 3 and args[2].lstrip("#").isdigit():
        return cerrar(vault, cola, int(args[2].lstrip("#")))
    if orden == "migrar":
        return migrar(vault, cola, escribir, archivo)
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
