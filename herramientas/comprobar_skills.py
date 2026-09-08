#!/usr/bin/env python3
"""comprobar_skills.py — ¿tus skills instalados son los del canon?

EXISTE POR UN CASO MEDIDO, no por precaucion. Una casa estuvo DIECINUEVE DIAS
con un skill del canon una revision atrasado: ni un error, ni un aviso, ni un
sintoma. Se descubrio por casualidad discutiendo otra cosa.

LA CAUSA: adherir al canon por referencia actualiza EL CLON, no los skills
instalados. Lo que vive en el nivel personal son COPIAS MUERTAS — nada las
sincroniza y nada las vigila. Y el salto de version verifica la huella del
skill que INSTALA; ningun paso verifica los que YA ESTABAN.

QUE HACE: baja el inventario de huellas del canon, busca cada skill en las dos
formas de instalacion que existen (archivo suelto en commands/, o carpeta con
SKILL.md dentro de skills/) y dice cuales difieren. No escribe nada, no toca
nada y no manda nada a ningun sitio.

SALIDAS: 0 si todo cuadra, 1 si algo difiere. Las dos probadas — un chequeo
probado solo en verde no esta probado.

SI TU DOMINIO NO EJECUTA COSAS BAJADAS DE INTERNET, no lo bajes: el canon YA
publica skills/MD5SUM.txt, que es todo lo que hace falta. La receta cabe en
seis lineas y no ejecuta nada ajeno —

    curl -s https://raw.githubusercontent.com/akatzin/vuelamind/main/skills/MD5SUM.txt > /tmp/inv
    while read h n; do
      [ "$n" = README.md ] && continue
      f=~/.claude/commands/$n; [ -f "$f" ] || f=~/.claude/skills/${n%.md}/SKILL.md
      [ -f "$f" ] || { echo "no instalado: $n"; continue; }
      m=$(md5 -q "$f" 2>/dev/null || md5sum "$f" | cut -d" " -f1)
      [ "$m" = "$h" ] || echo "DESALINEADO: $n  $m -> $h"
    done < /tmp/inv

— y es preferible: no hay que confiar en un script para comprobar que confias
en los otros. Lo unico que la receta NO hace es avisarte de los skills que
tienes instalados y el inventario no lista, que es la mitad ciega del problema.
"""

import hashlib, os, sys, urllib.request

CANON = "https://raw.githubusercontent.com/akatzin/vuelamind/main/skills/MD5SUM.txt"
BASE  = os.path.expanduser("~/.claude")

inv = urllib.request.urlopen(CANON, timeout=20).read().decode()
filas = [l.split(None, 1) for l in inv.splitlines() if l.strip()]

viejos, ok, ausentes = [], 0, []
for h, nombre in filas:
    nombre = nombre.strip()
    if nombre == "README.md":
        continue
    base = nombre[:-3]
    candidatos = [os.path.join(BASE, "commands", nombre),
                  os.path.join(BASE, "skills", base, "SKILL.md"),
                  os.path.join(BASE, "skills", nombre)]
    ruta = next((c for c in candidatos if os.path.exists(c)), None)
    if not ruta:
        ausentes.append(nombre); continue
    mio = hashlib.md5(open(ruta, "rb").read()).hexdigest()
    if mio == h:
        ok += 1
    else:
        viejos.append((nombre, mio[:8], h[:8], ruta))

# Lo que el inventario NO cubre. Sin esto, un skill instalado que el canon no
# lista es INVISIBLE para este comprobador: no tiene huella contra la que medir,
# asi que sale verde sin haberse comprobado nada. Un inventario incompleto y uno
# completo se ven igual desde el lado del que compara — hallazgo de otra casa,
# que tenia dos skills fuera del inventario y este script no los mencionaba.
conocidos = {n.strip() for _, n in filas}
sin_huella = []
for d, patron in ((os.path.join(BASE, "commands"), None),
                  (os.path.join(BASE, "skills"), "SKILL.md")):
    if not os.path.isdir(d):
        continue
    for e in sorted(os.listdir(d)):
        if not e.startswith("vuelamind"):
            continue
        nombre = e if e.endswith(".md") else e + ".md"
        ruta = os.path.join(d, e) if patron is None else os.path.join(d, e, patron)
        if nombre not in conocidos and os.path.exists(ruta):
            sin_huella.append((nombre, ruta))

print("AL DIA:    %d" % ok)
print("NO INSTALADOS: %s" % (", ".join(ausentes) if ausentes else "ninguno"))
if sin_huella:
    print("\nSIN HUELLA EN EL CANON  (instalados que el inventario NO lista):")
    for n, r in sin_huella:
        print("  %-28s %s" % (n, r))
    print("  Sobre estos NO se comprobo nada. Pueden ser locales a proposito —")
    print("  compruebalo tu— pero este script no puede decir si estan al dia.")
if viejos:
    print("\nDESALINEADOS  (el tuyo -> el del canon):")
    for n, m, c, r in viejos:
        print("  %-28s %s -> %s   %s" % (n, m, c, r))
    print("\nCopia esos desde skills/ del canon. Ninguno da error si no lo haces.")
    sys.exit(1)
else:
    print("\nNinguno desalineado.")
