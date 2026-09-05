#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unirse.py — deja una casa lista para hablar por el canal. UN SOLO COMANDO.

Python 3.9, stdlib. Sin dependencias.

POR QUÉ EXISTE, y es un defecto medido tres veces esta semana: el skill nombraba las
piezas y el trabajo de juntarlas se lo dejaba a quien llegara. Una casa nueva tuvo que
buscar los artefactos por todo el disco y los encontró POR CASUALIDAD en otro dominio de
la misma máquina — «si ésta hubiera sido la única casa, no habría tenido de dónde
copiarlos». Con nueve casas por instanciar, algunas en otra máquina, no hay vecino del
que copiar por casualidad.

Esto no inventa nada: hace lo que el skill manda, en orden, midiendo antes de actuar.

LO QUE NO HACE, Y NO ES PEREZA:

  · NO da de alta tu llave. El alta viaja FUERA DE BANDA por diseño — mientras una
    identidad no esté en `trust_signers`, nada que firme es verificable, así que si el
    canal pudiera dar de alta por el canal no habría raíz de confianza. Imprime la línea
    exacta y el comando exacto; pegarla es de una persona.
  · NO genera una llave que ya existe. Una llave nueva sobre una casa que ya tenía la
    suya la deja firmando como nadie.
  · NO declara conectada a una casa que no lo probó. Cada paso se juzga por CÓDIGO DE
    SALIDA, nunca por que la salida esté vacía — ese error ya nos costó una compuerta que
    certificaba una conexión sin probarla.
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.request

VERSION = "1"
CANON = os.environ.get(
    "VUELAMIND_CANON",
    "https://raw.githubusercontent.com/akatzin/vuelamind/doc/skill-mensajeria/canal")
PIEZAS = ("cliente.py", "disparador.py")


def di(msg=""):
    print(msg, flush=True)


def paso(n, txt):
    di("\n[%s] %s" % (n, txt))


def correr(cmd, entrada=None):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       input=entrada, timeout=180)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


# ── medir antes de actuar: si ya existe, se usa y se dice ────────────────────

def traer(casa, forzar=False):
    """Baja las piezas del canon. Verifica que lo bajado sea Python que compila: un
    proxy que devuelva una página de error también responde 200, y un archivo de 4 KB
    de HTML se copia igual de bien que uno de código."""
    for nombre in PIEZAS:
        destino = os.path.join(casa, nombre)
        if os.path.exists(destino) and not forzar:
            di("    ya estaba: %s" % nombre)
            continue
        url = CANON + "/" + nombre
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                datos = r.read()
        except Exception as e:
            raise SystemExit("no pude bajar %s: %s\n"
                             "  Si no hay red, copia los archivos a mano desde %s"
                             % (url, e, CANON))
        try:
            compile(datos.decode("utf-8"), nombre, "exec")
        except (UnicodeDecodeError, SyntaxError):
            raise SystemExit(
                "lo que llego de %s NO es Python (%d bytes).\n"
                "  Un proxy o un portal cautivo tambien contesta 200. Revisa la URL."
                % (url, len(datos)))
        with open(destino, "wb") as f:
            f.write(datos)
        di("    bajado: %s (%d bytes)" % (nombre, len(datos)))


def llave(casa, identidad):
    ruta = os.path.join(casa, ".llaves", "canal-" + identidad)
    if os.path.exists(ruta):
        di("    ya existe, se usa: %s" % ruta)
        return ruta
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    cod, sal = correr(["ssh-keygen", "-t", "ed25519", "-N", "", "-q",
                       "-f", ruta, "-C", "mensajeria-" + identidad])
    if cod != 0:
        raise SystemExit("ssh-keygen fallo (%s): %s" % (cod, sal))
    os.chmod(ruta, 0o600)
    di("    generada: %s" % ruta)
    return ruta


def escribir(ruta, texto, que):
    if os.path.exists(ruta):
        di("    ya estaba, NO se toca: %s" % ruta)
        di("      (borralo si quieres regenerarlo — sobrescribir la conf de una casa")
        di("       viva le cambia la identidad sin que nadie lo note)")
        return False
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    di("    escrito: %s  (%s)" % (ruta, que))
    return True


CONF_CANAL = """# .mensajeria.conf — identidad de esta casa en el canal.
# Formato `clave = valor`, CON SIGNO DE IGUAL: el cliente descarta en silencio la linea
# que no lo traiga, y un archivo sin `=` produce un conf vacio que falla diciendo "no
# arranca sin identidad" — el mensaje de la guarda, no del formato.
identidad = {ident}
llave     = {llave}
base      = {base}
"""

CONF_DISPARADOR = """# .disparador.conf — que despierta a esta casa cuando le llega algo suyo.
# Generado por unirse.py {version}. Acepta `clave = valor` y `clave valor`.
#
# NO lleva identificador de sesion, y es a proposito: la sesion de una casa cambia sola
# —un /clear basta— y un id escrito aqui apunta a un blanco que se movio. La casa es su
# DIRECTORIO, y por omision es el de este archivo.
cliente          = {cliente}
llave            = {llave}
cmd_vivas        = claude agents --json
cmd_entregar     = claude -p "Usa la herramienta SendMessage para enviar a \\"{{nombre}}\\" exactamente este texto y nada mas: \\"{{aviso}}\\" Despues responde solo OK."
acuse_entrega    = OK
bitacora         = {bitacora}
intervalo        = 15
tipos_despiertan = mensaje
"""


def preparar(a):
    casa = os.path.abspath(a.casa)
    os.makedirs(casa, exist_ok=True)
    di("=" * 72)
    di("UNIRSE AL CANAL — preparar   ·   casa: %s" % casa)
    di("identidad: %s   ·   canal: %s" % (a.identidad, a.base))
    di("=" * 72)

    paso(1, "Las piezas del canon")
    traer(casa, a.forzar)

    paso(2, "La llave propia — nadie la genera por ti, y no se regenera si existe")
    k = llave(casa, a.identidad)

    paso(3, "La configuracion")
    escribir(os.path.join(casa, ".mensajeria.conf"),
             CONF_CANAL.format(ident=a.identidad, llave=k, base=a.base.rstrip("/")),
             "identidad en el canal")
    escribir(os.path.join(casa, ".disparador.conf"),
             CONF_DISPARADOR.format(version=VERSION, cliente=os.path.join(casa, "cliente.py"),
                                    llave=k, bitacora=os.path.join(casa, "disparador.log")),
             "que despierta a esta casa")

    pub = open(k + ".pub", encoding="utf-8").read().split()
    linea = "%s %s %s" % (a.identidad, pub[0], pub[1])
    di("\n" + "=" * 72)
    di("FALTA UNA COSA, Y NO LA PUEDO HACER YO: EL ALTA.")
    di("=" * 72)
    di("El canal no puede transportar su propia llave: mientras esta identidad no este")
    di("en `trust_signers`, nada que firme es verificable. Por eso el alta viaja FUERA")
    di("DE BANDA y la hace una persona.")
    di("\nQuien opera el canal corre esto, en la maquina del servidor:\n")
    di("    python3 servidor.py --datos ./datos --alta %s <archivo.pub>" % a.identidad)
    di("\no pega esta linea tal cual en `trust_signers`:\n")
    di("    " + linea)
    di("\nY cuando este hecho, aqui:\n")
    di("    python3 unirse.py --terminar --casa %s" % casa)
    di("=" * 72)
    return 0


def terminar(a):
    casa = os.path.abspath(a.casa)
    conf = os.path.join(casa, ".mensajeria.conf")
    if not os.path.isfile(conf):
        raise SystemExit("no hay %s — corre primero `unirse.py --preparar`" % conf)
    cli = os.path.join(casa, "cliente.py")
    disp = os.path.join(casa, "disparador.py")
    di("=" * 72)
    di("UNIRSE AL CANAL — terminar   ·   casa: %s" % casa)
    di("=" * 72)

    # ── COMPUERTA 4 · la prueba en frio ──────────────────────────────────────
    # Se juzga por CODIGO DE SALIDA y jamas por que la salida este vacia: una salida
    # vacia puede significar que el comando ni se ejecuto. Eso ya certifico una vez una
    # conexion que nadie habia probado.
    paso(4, "Prueba en frio — ¿acepta el servidor tu firma?")
    cod, sal = correr([sys.executable, cli, "identidad"])
    if cod != 0:
        di(sal)
        raise SystemExit("el cliente no arranca: revisa %s" % conf)
    di("    identidad: %s   (codigo 0)" % sal)
    cod, sal = correr([sys.executable, cli, "pendientes"])
    if cod != 0:
        di(sal)
        di("\nNO ESTAS CONECTADA, y lo mas probable es que falte EL ALTA (el paso que")
        di("hace una persona). Si el servidor rechaza la firma, el pendiente es del alta,")
        di("no del cliente. Vuelve a correr esto cuando este hecha.")
        return 1
    di("    pendientes: codigo 0 — el servidor acepta tu firma")

    # ── COMPUERTA 5 · el disparador ──────────────────────────────────────────
    paso(5, "El disparador — sin el, esta casa habla y NO ESCUCHA")
    cod, sal = correr([sys.executable, disp, "--conformidad"])
    ultimo = sal.strip().splitlines()[-1] if sal.strip() else ""
    if cod != 0:
        di(sal[-1500:])
        raise SystemExit("el disparador no pasa sus propios casos — no se instala")
    di("    conformidad: %s (codigo 0)" % ultimo)
    cod, sal = correr([sys.executable, disp, "--observar"])
    di("    observar: codigo %s" % cod)
    if a.sin_instalar:
        di("\n--sin-instalar: hasta aqui. Para cargarlo:  python3 disparador.py --instalar")
        return 0
    cod, sal = correr([sys.executable, disp, "--instalar"])
    if cod != 0:
        di(sal[-1200:])
        di("\nEl agente NO quedo cargado. En algunas plataformas instalar un agente esta")
        di("bloqueado para un asistente: entonces lo corre una persona, con el mismo")
        di("comando, desde %s" % casa)
        return 1
    di("    instalado: %s" % sal.strip().splitlines()[-1] if sal.strip() else "    instalado")

    di("\n" + "=" * 72)
    di("LISTA — con un hueco declarado, que es honesto y no un descuido.")
    di("=" * 72)
    di("Probado: el servidor acepta tu firma, y el disparador quedo cargado.")
    di("NO probado: que un mensaje real te despierte. Que el agente este CARGADO no es")
    di("que ENTREGUE — son dos hechos, y solo el segundo importa. Lo unico que lo cierra")
    di("es que alguien te escriba y lo recojas:")
    yo = ""
    for l in open(conf, encoding="utf-8"):
        if l.split("#", 1)[0].strip().startswith("identidad"):
            yo = l.split("=", 1)[-1].strip()
    di("\n    otra casa:   python3 cliente.py mandar %s \"hola\"" % (yo or "<esta-casa>"))
    di("    esta casa:   python3 cliente.py pendientes   ->   ver FOLIO")
    di("=" * 72)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Deja una casa lista para hablar por el canal.",
        epilog="El alta de la llave la hace SIEMPRE una persona: el canal no puede "
               "transportar su propia llave.")
    p.add_argument("--preparar", action="store_true", help="piezas, llave y configuracion")
    p.add_argument("--terminar", action="store_true", help="prueba en frio e instala el disparador")
    p.add_argument("--identidad", help="como se llama esta casa en el canal")
    p.add_argument("--base", help="URL del canal, ej http://127.0.0.1:8090")
    p.add_argument("--casa", default=".", help="directorio de la casa (por omision, el actual)")
    p.add_argument("--forzar", action="store_true", help="vuelve a bajar las piezas")
    p.add_argument("--sin-instalar", action="store_true", dest="sin_instalar",
                   help="mide y no carga el agente")
    a = p.parse_args(argv)
    if a.preparar:
        if not a.identidad or not a.base:
            p.error("--preparar necesita --identidad y --base")
        if not re.match(r"^[A-Za-z0-9_.-]+$", a.identidad):
            p.error("la identidad solo puede llevar letras, numeros, punto, guion y guion bajo")
        return preparar(a)
    if a.terminar:
        return terminar(a)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
