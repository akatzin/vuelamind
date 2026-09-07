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

print("AL DIA:    %d" % ok)
print("NO INSTALADOS: %s" % (", ".join(ausentes) if ausentes else "ninguno"))
if viejos:
    print("\nDESALINEADOS  (el tuyo -> el del canon):")
    for n, m, c, r in viejos:
        print("  %-28s %s -> %s   %s" % (n, m, c, r))
    print("\nCopia esos desde skills/ del canon. Ninguno da error si no lo haces.")
    sys.exit(1)
else:
    print("\nNinguno desalineado.")
