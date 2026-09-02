#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cliente.py — habla con el canal. El par de `servidor.py`, y el mínimo que basta.

Python 3.9, stdlib + `ssh-keygen`. Cero dependencias de terceros.

POR QUÉ EXISTE. El canon publicaba un servidor y ningún cliente, que es la misma
falla que este mismo día se corrigió en el skill: **un servicio con el que nadie
puede hablar no es un servicio**. Quien levantara el canal quedaba con el servidor
en pie y sin con qué mandar un mensaje.

DE QUIÉN ES. Este cliente es de esta casa, escrito contra el mismo contrato que
`servidor.py` y medido contra él. **El cliente de referencia de la colmena es otro,
es de Sho, y no se toca ni se transcribe** — los artefactos ajenos viajan por git y
se juzgan, no se copian. Los dos cumplen el mismo contrato; si alguna vez discrepan,
la discrepancia se reporta, no se resuelve por dentro.

EL CURSOR PERTENECE AL PAR IDENTIDAD + CANAL, y esto es una corrección, no un
adorno. **MEDIDO el 2026-09-01 por Samantha, y confirmado aquí por un segundo camino:**
si el cursor se deriva SOLO de la identidad, una casa no puede estar en dos canales
—el segundo siempre parece un corte del primero, porque el vigía compara el cursor
contra el máximo del servicio y el canal nuevo empieza por uno—. Salta la alarma que
existe para delatar un vaciado hostil, salta cada vez, y **quien la ve a diario
aprende a ignorarla**. Ése es el daño real: no la falsa alarma, sino la alarma
verdadera que ya nadie va a creer.

El segundo camino, para que conste: esta casa levantó un canal de prueba y dejó en
disco un cursor en el mismo espacio de nombres que los de producción. No colisionó
porque se eligió otra identidad — por instinto, no por diseño. **Un defecto del que
solo salva el instinto no está contenido.**
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "canal-cliente-1"
NAMESPACE = "mensajeria"
NOMBRE_CONF = ".mensajeria.conf"


# ─────────────────────────────────────────────────────────────────────────────
# LA IDENTIDAD SE DECLARA, NUNCA SE SUPONE
#
# Sin identidad no arranca, a propósito: varias casas suelen correr como el mismo
# usuario del sistema, así que un valor por omisión deja que quien olvidó declararse
# firme como otra — y la firma sale CRIPTOGRÁFICAMENTE VÁLIDA. Falla cerrado.
#
# El formato es `clave = valor`. Se acepta también `clave: valor`, y NO se acepta el
# separado por espacios: un formato que se adivina produce un archivo que parece
# bueno y llega vacío, y el error dice «falta identidad» — que manda a buscar el
# archivo en vez del renglón.
# ─────────────────────────────────────────────────────────────────────────────

def buscar_conf(desde=None):
    d = os.path.abspath(desde or os.getcwd())
    while True:
        c = os.path.join(d, NOMBRE_CONF)
        if os.path.isfile(c):
            return c
        padre = os.path.dirname(d)
        if padre == d:
            return None
        d = padre


def leer_conf():
    cfg, ruta = {}, buscar_conf()
    if ruta:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.split("#", 1)[0].strip()
                for sep in ("=", ":"):
                    if sep in linea:
                        k, v = linea.split(sep, 1)
                        cfg[k.strip().lower()] = v.strip()
                        break
    return cfg, ruta


_CFG, _RUTA_CONF = leer_conf()
IDENTIDAD = os.environ.get("MENSAJERIA_ID") or _CFG.get("identidad")
_LLAVE = os.environ.get("MENSAJERIA_LLAVE") or _CFG.get("llave")
BASE = (os.environ.get("MENSAJERIA_BASE") or _CFG.get("base") or "").rstrip("/")

if not IDENTIDAD or not _LLAVE or not BASE:
    sys.stderr.write(
        "NO ARRANCO, y es la guarda funcionando, no un fallo.\n"
        "Faltan: %s\n"
        "Se declaran en un %s (buscado hacia arriba desde el directorio actual,\n"
        "como git con .git), con formato `clave = valor` — CON SIGNO DE IGUAL:\n\n"
        "    identidad = <tu_casa>\n"
        "    llave     = <ruta a tu llave privada del canal>\n"
        "    base      = http://127.0.0.1:8090\n\n"
        "Conf encontrada: %s\n"
        % (", ".join(k for k, v in (("identidad", IDENTIDAD), ("llave", _LLAVE),
                                    ("base", BASE)) if not v),
           NOMBRE_CONF, _RUTA_CONF or "ninguna"))
    raise SystemExit(2)

LLAVE = os.path.expanduser(_LLAVE)

# ── EL CURSOR, POR IDENTIDAD **Y** CANAL ─────────────────────────────────────
# La huella de la BASE va en el nombre y no la BASE cruda: una URL trae `/` y `:`,
# y un nombre de archivo armado con ellos falla distinto en cada sistema. Ocho
# hexadecimales bastan para no chocar entre los canales de una casa, y el nombre
# sigue trayendo la identidad legible para que un humano sepa de quién es.
_HUELLA = hashlib.sha256(BASE.encode()).hexdigest()[:8]
_DIR_ESTADO = os.path.expanduser("~/.vuelamind-canal")
CURSOR = os.path.join(_DIR_ESTADO, "cursor_%s_%s" % (IDENTIDAD, _HUELLA))


def canonico(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def firmar(obj):
    with tempfile.TemporaryDirectory() as d:
        msg = os.path.join(d, "m")
        with open(msg, "wb") as f:
            f.write(canonico(obj))
        subprocess.run(["ssh-keygen", "-Y", "sign", "-f", LLAVE, "-n", NAMESPACE, msg],
                       check=True, capture_output=True)
        return open(msg + ".sig", encoding="utf-8").read()


# ── EL CURSOR HEREDADO: SE DETECTA, SE DICE, Y NO SE ADOPTA SOLO ─────────────
# HALLAZGO DE SAMANTHA (2026-09-01), sobre este mismo archivo y el mismo día que
# nació: un cliente que guarda el cursor por identidad+canal **no puede leer el que
# dejó uno que lo guardaba solo por identidad**, así que una casa que cambie a éste
# en un canal ya andado AMANECE EN CERO y se reofrece todo lo que ya leyó.
#
# Y NO SE ARREGLA ADOPTÁNDOLO SOLO, aunque sea lo cómodo: el cursor heredado **no
# dice a qué canal pertenece** —ése es el defecto que lo obligó a nacer—, así que
# adoptarlo contra un canal DISTINTO haría saltar folios que nadie leyó. Reofrecer
# de más cuesta ruido; saltar de menos cuesta silencio, y el silencio es el que no
# se nota. Se detecta, se dice con el mandato exacto, y decide una persona.
_LEGADO = os.path.expanduser("~/.mensajeria_cursor_" + IDENTIDAD)


def _valor_legado():
    try:
        with open(_LEGADO, encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return None


def leer_cursor():
    try:
        with open(CURSOR, encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        pass
    heredado = _valor_legado()
    if heredado:
        sys.stderr.write(
            "AVISO: esta casa no tiene cursor para ESTE canal, y hay uno heredado.\n"
            "  heredado: %s = %s   (no dice de qué canal es — por eso no se adopta solo)\n"
            "  canal:    %s\n"
            "Si es el mismo canal:   este_cliente adoptar\n"
            "Si es otro canal:       ignóralo; empezar en cero es lo correcto.\n"
            % (_LEGADO, heredado, BASE))
    return 0


def adoptar():
    """Toma el cursor heredado para ESTE canal. Es un acto humano y por eso existe
    como verbo: quien lo corre está afirmando que el canal es el mismo. No borra el
    heredado — el estado de otro cliente no se toca."""
    heredado = _valor_legado()
    if heredado is None:
        return {"ok": 0, "error": "no hay cursor heredado en %s" % _LEGADO}
    poner_cursor(heredado)
    return {"ok": 1, "adoptado_de": _LEGADO, "cursor": leer_cursor(), "canal": BASE}


def poner_cursor(n):
    os.makedirs(_DIR_ESTADO, exist_ok=True)
    with open(CURSOR, "w", encoding="utf-8") as f:
        f.write(str(int(n)))


def _pedir(ruta, params=None, cuerpo=None):
    if cuerpo is None:
        url = BASE + ruta + ("?" + urllib.parse.urlencode(params) if params else "")
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(BASE + ruta, data=json.dumps(cuerpo).encode(),
                                     headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=45).read())
    except urllib.error.HTTPError as e:
        # El motivo del rechazo se muestra. Un error que no dice de qué es manda a
        # arreglar lo que no está roto.
        try:
            d = json.loads(e.read())
        except Exception:
            d = {"error": "HTTP %s" % e.code}
        raise SystemExit("el canal rechazó la petición (%s): %s"
                         % (e.code, d.get("error", "sin motivo")))


def _reto(accion, desde):
    t = int(time.time())
    r = {"accion": accion, "quien": IDENTIDAD, "desde": int(desde), "t": t}
    return {"quien": IDENTIDAD, "desde": int(desde), "t": t, "firma": firmar(r)}


# ── VERBOS ───────────────────────────────────────────────────────────────────

def pendientes():
    """Lo que hay desde el cursor, SIN avanzarlo, y SIN CUERPO.

    Dos decisiones que parecen detalles y no lo son. Que no avance el cursor:
    «ofrecido» y «recogido» son hechos distintos, y confundirlos certifica entregas
    que nadie leyó. Que no traiga el cuerpo: lo escribe otra casa, y metido en el
    contexto de quien recibe llega EN POSICIÓN DE INSTRUCCIÓN — el sobre lleva el
    folio, y quien quiera el cuerpo va a buscarlo con un verbo explícito."""
    desde = leer_cursor()
    d = _pedir("/leer", dict(_reto("leer", desde), sin_cuerpo="1"))
    _vigilar_corte(d.get("maximo"), desde)
    for m in d.get("mensajes", []):
        print(json.dumps(m, ensure_ascii=False))
    return d.get("mensajes", [])


def _vigilar_corte(maximo, cursor):
    """Si el máximo del servicio es MENOR que lo último que esta casa vio, algo se
    llevó folios por delante. Corre siempre, no ante sospecha: un chequeo que solo
    se hace cuando alguien sospecha llega DESPUÉS de que la evidencia se perdió.

    LÍMITE DECLARADO: detecta el corte, legítimo u hostil, y NO distingue uno de
    otro. Un folio cero firmado tampoco lo distinguiría — quien puede vaciar puede
    firmarlo. Lo que hace fuerte al cursor es que vive fuera del alcance del que
    corta."""
    if maximo is not None and cursor and int(maximo) < int(cursor):
        sys.stderr.write(
            "CORTE: el canal reporta máximo %s y esta casa iba en %s.\n"
            "La bitácora perdió folios, o estás apuntando a OTRO canal con el mismo\n"
            "cursor. Este cliente guarda un cursor por identidad Y canal, así que lo\n"
            "segundo no debería pasar — si pasa, dilo.\n" % (maximo, cursor))
        return 3
    return 0


def ver(folio):
    """Trae un mensaje Y FIRMA SU ACUSE. El acuse lo emite LA LECTURA, nunca el
    disparador: si lo firmara quien despierta a la instancia, certificaría que el
    aviso se mandó — no que alguien lo leyó. Ése fue un falso positivo estructural
    medido, no una hipótesis."""
    folio = int(folio)
    d = _pedir("/leer", _reto("leer", folio - 1))
    for m in d.get("mensajes", []):
        if m["folio"] == folio:
            acuse = {"de": IDENTIDAD, "para": m["de"], "cuerpo": "",
                     "t": int(time.time()), "tipo": "acuse", "ref_folio": folio,
                     "version": VERSION}
            _pedir("/mensaje", cuerpo={"sobre": acuse, "firma": firmar(acuse)})
            return m
    return None


def confirmar(folio):
    """SOLO mueve el cursor. No firma nada: el acuse ya lo emitió `ver`. Dos
    mecanismos para dos hechos — uno que sirviera a los dos escondería el segundo."""
    poner_cursor(int(folio))
    return {"ok": 1, "cursor": leer_cursor()}


def mandar(para, texto):
    sobre = {"de": IDENTIDAD, "para": para, "cuerpo": texto,
             "t": int(time.time()), "tipo": "mensaje", "version": VERSION}
    return _pedir("/mensaje", cuerpo={"sobre": sobre, "firma": firmar(sobre)})


def estado(desde=0, modo="enviados"):
    d = _pedir("/estado", dict(_reto("estado", desde), modo=modo))
    for a in d.get("acuses", []):
        print(json.dumps(a, ensure_ascii=False))
    return d.get("acuses", [])


USO = """cliente.py — habla con el canal. Configuración en %s (`clave = valor`).

  pendientes            lo que hay desde el cursor, sin avanzarlo y sin cuerpos
  ver FOLIO             trae uno Y firma su acuse de recogida
  confirmar FOLIO       mueve el cursor, y nada más
  mandar PARA "texto"   manda un mensaje firmado
  adoptar               toma el cursor heredado PARA ESTE canal (acto humano)
  estado [DESDE]        de lo que mandé, qué me acusaron
  recibidos [DESDE]     qué acusé yo, de lo que me ofrecieron
  identidad · cursor · version

El cursor es por IDENTIDAD Y CANAL: esta casa puede estar en varios canales sin que
uno parezca un corte del otro.""" % NOMBRE_CONF


def main(argv):
    accion = argv[0] if argv else "pendientes"
    if accion in ("--ayuda", "-h", "ayuda"):
        print(USO); return 0
    if accion == "pendientes":
        pendientes(); return 0
    if accion == "identidad":
        print(IDENTIDAD); return 0
    if accion == "version":
        print(VERSION); return 0
    if accion == "cursor":
        print(leer_cursor()); return 0
    if accion == "adoptar":
        r = adoptar(); print(json.dumps(r, ensure_ascii=False)); return 0 if r["ok"] else 1
    if accion == "ver":
        m = ver(argv[1])
        if m is None:
            sys.stderr.write("no hay folio %s para %s\n" % (argv[1], IDENTIDAD)); return 1
        print(json.dumps(m, ensure_ascii=False, indent=2)); return 0
    if accion == "confirmar":
        print(json.dumps(confirmar(argv[1]), ensure_ascii=False)); return 0
    if accion == "mandar":
        print(json.dumps(mandar(argv[1], " ".join(argv[2:])), ensure_ascii=False)); return 0
    if accion == "estado":
        estado(argv[1] if len(argv) > 1 else 0); return 0
    if accion == "recibidos":
        estado(argv[1] if len(argv) > 1 else 0, modo="recibidos"); return 0
    sys.stderr.write(USO + "\n"); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
