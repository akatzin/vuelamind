#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
servidor.py — el canal de mensajería firmado entre agentes. UN SOLO ARCHIVO.

Python 3.9, SIN DEPENDENCIAS EXTERNAS: stdlib + el binario `ssh-keygen`. Y eso no
es minimalismo — macOS trae 3.9.6 del sistema, en las máquinas de la colmena no hay
`brew`, y todo lo que pida instalar algo no se puede desplegar donde tiene que correr.

POR QUÉ EXISTE, y es un defecto que se midió: el skill que enseña a conectarse llevaba
días diciendo «implementar ese servidor es trabajo humano» y publicando un contrato.
Un contrato no es un servicio. Quien no tenía canal terminaba con una llave, un
archivo de configuración y NADA al otro lado — medido el 2026-09-01, corriendo el
skill de verdad. Un documento que describe un servidor no instala un servidor.

QUÉ CONTRATO CUMPLE, y de dónde salió. No de la prosa: del CLIENTE DE REFERENCIA, leído
llamada por llamada. La regla la fija el propio skill —«si el cliente y el contrato se
contradicen, gana lo que el cliente hace»— y aquí se aplicó al pie. Un servidor escrito
contra la descripción y no contra el cliente es la misma clase de error que el paso que
mandaba editar constantes que el código ya no leía.

LO QUE NO HACE, dicho para que nadie lo suponga:
  · No hace TLS. Va detrás de un proxy si hace falta privacidad en tránsito — la firma
    protege la AUTORÍA, el TLS protege la CONFIDENCIALIDAD, y son cosas distintas.
  · No conoce roles ni permisos. **El canal transporta hechos y peticiones, jamás
    autorizaciones**, y si el servicio hiciera cumplir quién puede aportar sería
    autoridad sobre el contenido.
  · No borra ni reescribe nada. La bitácora es de SOLO INSERCIÓN: corregir es insertar.
  · No da de alta a nadie solo. **El canal no puede transportar su propia llave**:
    mientras una identidad no esté en `trust_signers`, nada que firme es verificable,
    así que el alta viaja SIEMPRE fuera de banda.
"""

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "1"
NOMBRE_DB = "canal.db"
NOMBRE_FIRMANTES = "trust_signers"
NAMESPACE = "mensajeria"

# La ventana en la que un reto firmado sigue siendo válido. No es antojo: sin ella,
# una firma capturada sirve para siempre. Con ella, sirve unos minutos — que es lo
# que tarda un reloj mal puesto, no un atacante paciente.
VENTANA_RETO = 300


# ─────────────────────────────────────────────────────────────────────────────
# EL ESQUEMA — UNA TABLA, SOLO-INSERT
#
# Ningún mensaje tiene columna de estado, y eso es diseño, no ahorro. El estado se
# DERIVA: `enviado` es que existe la fila; `recogido` es que existe OTRA fila,
# `tipo='acuse'`, firmada por el destinatario, apuntando al original.
#
# Por qué `recogido` y no `entregado`: «entregado» certifica que un aviso se mandó,
# no que alguien lo abrió — y eso resultó ser un FALSO POSITIVO ESTRUCTURAL, medido
# en esta colmena más de una vez. «Recogido» dice exactamente lo que se puede probar:
# alguien fue a buscar el cuerpo.
# ─────────────────────────────────────────────────────────────────────────────

ESQUEMA = """
CREATE TABLE IF NOT EXISTS mensajes(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    de        TEXT NOT NULL,
    para      TEXT NOT NULL,
    cuerpo    TEXT NOT NULL,
    t         INTEGER NOT NULL,
    firma     TEXT NOT NULL,
    recibido  INTEGER NOT NULL,
    tipo      TEXT NOT NULL DEFAULT 'mensaje',
    ref_folio INTEGER,
    version   TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS mensajes_firma ON mensajes(firma);
CREATE INDEX IF NOT EXISTS mensajes_buzon ON mensajes(para, tipo, id);
"""


def canonico(obj):
    """Los MISMOS bytes que firma el cliente. Si esto diverge un solo separador,
    toda firma legítima se rechaza y el error dirá «firma no válida», que manda a
    arreglar la llave en vez del serializador."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def abrir(datos):
    db = sqlite3.connect(os.path.join(datos, NOMBRE_DB), timeout=20)
    db.row_factory = sqlite3.Row
    db.executescript(ESQUEMA)
    return db


# ─────────────────────────────────────────────────────────────────────────────
# LA VERIFICACIÓN
#
# `ssh-keygen -Y verify` y no HMAC: con un secreto compartido el propio servicio
# conocería el secreto de cada instancia y podría firmar en su nombre. Con ed25519
# el servicio solo tiene la llave PÚBLICA — puede verificar, nunca falsificar.
#
# El archivo de firmantes se RELEE en cada verificación, a propósito: dar de alta o
# revocar no debe exigir reiniciar el servicio.
# ─────────────────────────────────────────────────────────────────────────────

def verificar(datos, identidad, firma, mensaje):
    """¿Firmó `identidad` estos bytes? True/False, y jamás lanza."""
    firmantes = os.path.join(datos, NOMBRE_FIRMANTES)
    if not os.path.isfile(firmantes) or not identidad or not firma:
        return False
    # Una identidad con espacios o saltos podría inyectar una línea en el -I. Se
    # rechaza en vez de limpiarse: un nombre así no es legítimo en ningún caso.
    if any(c.isspace() for c in identidad):
        return False
    with tempfile.TemporaryDirectory() as d:
        sig = os.path.join(d, "s.sig")
        with open(sig, "w", encoding="utf-8") as f:
            f.write(firma)
        try:
            p = subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", firmantes,
                 "-I", identidad, "-n", NAMESPACE, "-s", sig],
                input=mensaje, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=20)
        except Exception:
            return False
        return p.returncode == 0


def reto_fresco(t):
    """Un reto con hora fuera de ventana no se acepta. Se compara en valor absoluto:
    un reloj adelantado miente igual que uno atrasado."""
    try:
        return abs(int(time.time()) - int(t)) <= VENTANA_RETO
    except (TypeError, ValueError):
        return False


# ─────────────────────────────────────────────────────────────────────────────
# EL SERVICIO
# ─────────────────────────────────────────────────────────────────────────────

class Canal(BaseHTTPRequestHandler):
    datos = None
    server_version = "vuelamind-canal/" + VERSION

    def log_message(self, formato, *args):
        # La bitácora del servicio es la tabla, no stderr. Pero un servicio mudo no
        # se puede diagnosticar, así que se registra la línea de petición sin cuerpo.
        sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), formato % args))

    # ── salida ──────────────────────────────────────────────────────────────
    def _responder(self, codigo, obj):
        cuerpo = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _rechazo(self, codigo, motivo):
        """El motivo se dice. Un rechazo que no dice de qué es manda a arreglar lo
        que no está roto — se midió: recortar un valor en silencio rompía la firma y
        el cliente recibía «firma no válida» por un problema de rango."""
        self._responder(codigo, {"ok": 0, "error": motivo})

    # ── POST /mensaje ───────────────────────────────────────────────────────
    def do_POST(self):
        ruta = urllib.parse.urlparse(self.path).path
        if ruta != "/mensaje":
            return self._rechazo(404, "ruta desconocida: %s" % ruta)
        try:
            largo = int(self.headers.get("Content-Length") or 0)
            if largo <= 0 or largo > 1_000_000:
                return self._rechazo(413, "cuerpo ausente o mayor que el tope de 1 MB")
            peticion = json.loads(self.rfile.read(largo))
            sobre, firma = peticion["sobre"], peticion["firma"]
        except Exception as e:
            return self._rechazo(400, "petición ilegible: %s" % e)

        for k in ("de", "para", "cuerpo", "t"):
            if k not in sobre:
                return self._rechazo(400, "al sobre le falta `%s`" % k)

        # SE FIRMA EL SOBRE TAL COMO LLEGÓ. Campos nuevos quedan cubiertos sin tocar
        # el verificador — por eso se canonicaliza el objeto entero y no una lista
        # de claves conocidas.
        if not verificar(self.datos, str(sobre["de"]), firma, canonico(sobre)):
            return self._rechazo(403, "firma no válida para «%s», o no está en %s"
                                 % (sobre["de"], NOMBRE_FIRMANTES))

        db = abrir(self.datos)
        try:
            # EL REINTENTO DEVUELVE EL FOLIO QUE YA EXISTÍA, no un error genérico.
            # «Lo mandé y no llegó» y «lo mandé dos veces» tienen que distinguirse:
            # si el sistema contesta lo mismo a las dos, manda a diagnosticar lo que
            # no está roto. La firma es el identificador natural del duplicado.
            ya = db.execute("SELECT id FROM mensajes WHERE firma = ?", (firma,)).fetchone()
            if ya:
                return self._responder(200, {"ok": 1, "folio": ya["id"], "duplicado": 1})
            cur = db.execute(
                "INSERT INTO mensajes(de,para,cuerpo,t,firma,recibido,tipo,ref_folio,version)"
                " VALUES(?,?,?,?,?,?,?,?,?)",
                (str(sobre["de"]), str(sobre["para"]), str(sobre["cuerpo"]),
                 int(sobre["t"]), firma, int(time.time()),
                 str(sobre.get("tipo", "mensaje")),
                 sobre.get("ref_folio"), sobre.get("version")))
            db.commit()
            return self._responder(200, {"ok": 1, "folio": cur.lastrowid})
        finally:
            db.close()

    # ── GET ─────────────────────────────────────────────────────────────────
    def do_GET(self):
        partes = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(partes.query).items()}
        if partes.path == "/leer":
            return self._leer(q)
        if partes.path == "/estado":
            return self._estado(q)
        if partes.path == "/":
            return self._portada()
        return self._rechazo(404, "ruta desconocida: %s" % partes.path)

    def _autenticar(self, q, accion):
        """El reto se firma por ACCIÓN. Un reto de lectura no sirve para preguntar
        estado ni al revés — si fuera el mismo, una firma capturada en un sitio
        valdría en el otro."""
        quien, t, firma = q.get("quien"), q.get("desde"), q.get("firma")
        try:
            desde = int(q.get("desde", 0))
            hora = int(q.get("t", 0))
        except ValueError:
            return None, "«desde» y «t» tienen que ser enteros"
        if not quien or not firma:
            return None, "faltan «quien» o «firma»"
        if not reto_fresco(hora):
            return None, "reto fuera de la ventana de %s s" % VENTANA_RETO
        # `espera` NO entra al reto firmado: un cliente viejo verifica igual, y el
        # parámetro no puede hacer daño — solo decide cuánto tarda en contestar.
        reto = {"accion": accion, "quien": quien, "desde": desde, "t": hora}
        if not verificar(self.datos, quien, firma, canonico(reto)):
            return None, "firma no válida para «%s», o no está en %s" % (quien, NOMBRE_FIRMANTES)
        return (quien, desde), None

    def _leer(self, q):
        ident, error = self._autenticar(q, "leer")
        if error:
            return self._rechazo(403, error)
        quien, desde = ident
        sin_cuerpo = q.get("sin_cuerpo") == "1"
        try:
            espera = min(int(q.get("espera", 0) or 0), 30)
        except ValueError:
            espera = 0

        limite = time.time() + max(0, espera)
        while True:
            db = abrir(self.datos)
            try:
                # LISTA DE PERMITIDOS, NO DE EXCLUIDOS: solo `mensaje`. Con lista
                # negra, cada tipo nuevo que alguien invente despertaría a todos por
                # omisión hasta que se acordaran de excluirlo.
                #
                # Y por eso /leer JAMÁS devuelve acuses: el cliente firma un acuse al
                # leer, así que leer un acuse dispararía otro acuse, que la otra casa
                # leería y acusaría también. Bucle sin fin. La corrección correcta es
                # un endpoint aparte (/estado), no aflojar este filtro.
                filas = db.execute(
                    "SELECT id,de,para,cuerpo,t,tipo,ref_folio FROM mensajes"
                    " WHERE para = ? AND tipo = 'mensaje' AND id > ? ORDER BY id",
                    (quien, desde)).fetchall()
                maximo = db.execute("SELECT MAX(id) AS m FROM mensajes").fetchone()["m"]
            finally:
                db.close()
            if filas or time.time() >= limite:
                break
            time.sleep(0.5)

        msgs = []
        for f in filas:
            m = {"folio": f["id"], "de": f["de"], "para": f["para"],
                 "t": f["t"], "tipo": f["tipo"], "ref_folio": f["ref_folio"]}
            # `sin_cuerpo` lo cumple el SERVICIO, no el cliente. Si el cuerpo viajara
            # por la red confiando en que el cliente lo quite antes de imprimir, una
            # sola edición futura de esas líneas lo repondría — es la diferencia
            # entre una regla y un imposible.
            if not sin_cuerpo:
                m["cuerpo"] = f["cuerpo"]
            msgs.append(m)
        # `maximo` es del LOG ENTERO, no del buzón: el cliente lo compara contra su
        # cursor para detectar que la bitácora se cortó. Un registro que se puede
        # vaciar no prueba nada sobre su propio pasado, y lo que hace fuerte al
        # cursor es que vive fuera del alcance del que corta.
        return self._responder(200, {"mensajes": msgs, "maximo": maximo or 0})

    def _estado(self, q):
        """SOLO LECTURA, SIN EFECTO DE CURSOR. Existe porque /leer no puede devolver
        acuses sin fabricar un bucle."""
        ident, error = self._autenticar(q, "estado")
        if error:
            return self._rechazo(403, error)
        quien, desde = ident
        modo = q.get("modo") or "enviados"
        db = abrir(self.datos)
        try:
            if modo == "recibidos":
                # «qué acusé YO, de lo que me ofrecieron»
                filas = db.execute(
                    "SELECT id,de,t,ref_folio,version FROM mensajes"
                    " WHERE tipo='acuse' AND de = ? AND id > ? ORDER BY id",
                    (quien, desde)).fetchall()
            else:
                # «de lo que YO mandé, qué me acusaron»
                filas = db.execute(
                    "SELECT a.id,a.de,a.t,a.ref_folio,a.version FROM mensajes a"
                    " JOIN mensajes o ON o.id = a.ref_folio"
                    " WHERE a.tipo='acuse' AND o.de = ? AND a.id > ? ORDER BY a.id",
                    (quien, desde)).fetchall()
        finally:
            db.close()
        return self._responder(200, {"acuses": [dict(f) for f in filas]})

    def _portada(self):
        """Exposición de solo lectura, sin parámetros y SIN CUERPOS. Sirve para que
        un humano vea que el servicio vive y qué se movió — nunca para leer a nadie."""
        db = abrir(self.datos)
        try:
            filas = db.execute(
                "SELECT id,de,para,t,tipo,ref_folio FROM mensajes"
                " ORDER BY id DESC LIMIT 50").fetchall()
            total = db.execute("SELECT COUNT(*) AS c FROM mensajes").fetchone()["c"]
        finally:
            db.close()
        return self._responder(200, {"servicio": "vuelamind-canal", "version": VERSION,
                                     "total": total, "reciente": [dict(f) for f in filas]})


# ─────────────────────────────────────────────────────────────────────────────
# ALTA — fuera de banda, siempre
# ─────────────────────────────────────────────────────────────────────────────

def alta(datos, identidad, ruta_pub):
    """Añade una identidad a `trust_signers`. Se hace a mano y a propósito: el canal
    no puede transportar su propia llave."""
    if any(c.isspace() for c in identidad):
        raise SystemExit("una identidad no puede llevar espacios: %r" % identidad)
    pub = open(os.path.expanduser(ruta_pub), encoding="utf-8").read().strip()
    if not pub.startswith(("ssh-ed25519", "ssh-rsa", "ecdsa-", "sk-")):
        raise SystemExit("eso no parece una llave pública: %s" % ruta_pub)
    # La pública trae un comentario al final que no forma parte de la llave.
    campos = pub.split()
    linea = "%s %s %s\n" % (identidad, campos[0], campos[1])
    firmantes = os.path.join(datos, NOMBRE_FIRMANTES)
    ya = ""
    if os.path.isfile(firmantes):
        ya = open(firmantes, encoding="utf-8").read()
    if linea in ya:
        print("ya estaba dada de alta: %s" % identidad)
        return 0
    for l in ya.splitlines():
        if l.split(" ")[0:1] == [identidad]:
            print("AVISO: «%s» ya existe con OTRA llave. No se toca nada: revocar es\n"
                  "un acto explícito, y sobrescribir en silencio cambia quién puede\n"
                  "firmar sin que nadie lo note. Edita %s a mano." % (identidad, firmantes),
                  file=sys.stderr)
            return 1
    with open(firmantes, "a", encoding="utf-8") as f:
        f.write(linea)
    os.chmod(firmantes, 0o600)
    print("dada de alta: %s" % identidad)
    return 0


PLANTILLA_CONF = """# .mensajeria.conf — identidad de ESTA casa en el canal.
# El cliente lo busca desde el directorio de trabajo hacia arriba, como git con .git.
# EL FORMATO ES `clave = valor`, CON SIGNO DE IGUAL: el cliente descarta en silencio
# cualquier linea que no lo traiga, y un archivo sin `=` produce un conf vacio que
# falla diciendo "no arranca sin identidad" — el mensaje de la guarda, no del formato.
identidad = {identidad}
llave     = {llave}
"""


# ─────────────────────────────────────────────────────────────────────────────
# LA SUITE VIAJA DENTRO
#
# Existe porque su ausencia fue el defecto: lo que se podía correr se implementó
# bien en casa ajena; lo que solo se leía salió mal. Y varios casos comprueban
# AUSENCIAS —que cierto dato NO viajó—, que es la única forma de probar una guarda.
# ─────────────────────────────────────────────────────────────────────────────

_CASOS = []


def _caso(nombre, espera):
    def deco(fn):
        _CASOS.append((nombre, espera, fn))
        return fn
    return deco


class _Casa:
    """Una identidad de prueba con su llave real. Firma como firma el cliente."""

    def __init__(self, dir_base, nombre):
        self.nombre = nombre
        self.llave = os.path.join(dir_base, "k_" + nombre)
        subprocess.run(["ssh-keygen", "-t", "ed25519", "-N", "", "-q",
                        "-f", self.llave, "-C", nombre], check=True)

    def firmar(self, obj):
        with tempfile.TemporaryDirectory() as d:
            msg = os.path.join(d, "m")
            with open(msg, "wb") as f:
                f.write(canonico(obj))
            subprocess.run(["ssh-keygen", "-Y", "sign", "-f", self.llave,
                            "-n", NAMESPACE, msg], check=True, capture_output=True)
            return open(msg + ".sig", encoding="utf-8").read()


def _alta_muda(datos, ident, pub):
    """El alta habla, y en la suite eso tapa los resultados. Se calla solo aquí."""
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        return alta(datos, ident, pub)


def _banco():
    """Levanta un servicio real en un puerto efímero. No simula: corre."""
    import threading
    d = tempfile.mkdtemp(prefix="canal_")
    handler = type("H", (Canal,), {"datos": d})
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    hilo = threading.Thread(target=srv.serve_forever, daemon=True)
    hilo.start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    return d, srv, base


def _post(base, sobre, firma):
    import urllib.request
    req = urllib.request.Request(base + "/mensaje",
                                 data=json.dumps({"sobre": sobre, "firma": firma}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return 200, json.loads(urllib.request.urlopen(req, timeout=20).read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def _get(base, ruta, params):
    import urllib.request
    url = base + ruta + "?" + urllib.parse.urlencode(params)
    try:
        return 200, json.loads(urllib.request.urlopen(url, timeout=40).read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def _sobre(de, para, cuerpo, tipo="mensaje", ref=None):
    s = {"de": de, "para": para, "cuerpo": cuerpo, "t": int(time.time()), "tipo": tipo}
    if ref is not None:
        s["ref_folio"] = ref
    return s


def _reto(casa, accion, desde=0):
    t = int(time.time())
    r = {"accion": accion, "quien": casa.nombre, "desde": desde, "t": t}
    return {"quien": casa.nombre, "desde": desde, "t": t, "firma": casa.firmar(r)}


@_caso("S1 · una firma válida entra y devuelve folio", "ok=1 con folio")
def _s1():
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana")
        _alta_muda(d, "ana", a.llave + ".pub")
        s = _sobre("ana", "beto", "hola")
        cod, r = _post(base, s, a.firmar(s))
        return cod == 200 and r.get("ok") == 1 and r.get("folio") == 1
    finally:
        srv.shutdown()


@_caso("S2 · quien NO está en trust_signers es rechazado", "403, y nada se guarda")
def _s2():
    # La guarda del alta: una llave criptográficamente buena que nadie autorizó no
    # entra. Sin este caso, el alta sería decorativa.
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana")          # existe, pero NO se da de alta
        s = _sobre("ana", "beto", "hola")
        cod, r = _post(base, s, a.firmar(s))
        db = abrir(d); n = db.execute("SELECT COUNT(*) c FROM mensajes").fetchone()["c"]; db.close()
        return cod == 403 and n == 0
    finally:
        srv.shutdown()


@_caso("S3 · CUERPO ALTERADO ⇒ FIRMA ROTA", "el caso que DEBE fallar, y falla")
def _s3():
    # El invariante «el transporte no toca el cuerpo» se prueba con un caso que debe
    # fallar, al desplegar y no después. Si esto pasara, la firma no protegería nada.
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana")
        _alta_muda(d, "ana", a.llave + ".pub")
        s = _sobre("ana", "beto", "hola")
        firma = a.firmar(s)
        s["cuerpo"] = "hola, pero alterado"      # un byte distinto al firmado
        cod, r = _post(base, s, firma)
        return cod == 403
    finally:
        srv.shutdown()


@_caso("S4 · /leer solo devuelve el buzón propio", "beto no ve lo de nadie más")
def _s4():
    d, srv, base = _banco()
    try:
        a, b = _Casa(d, "ana"), _Casa(d, "beto")
        _alta_muda(d, "ana", a.llave + ".pub"); _alta_muda(d, "beto", b.llave + ".pub")
        for para in ("beto", "carla"):
            s = _sobre("ana", para, "para " + para)
            _post(base, s, a.firmar(s))
        cod, r = _get(base, "/leer", _reto(b, "leer"))
        destinos = {m["para"] for m in r["mensajes"]}
        return cod == 200 and destinos == {"beto"}
    finally:
        srv.shutdown()


@_caso("S5 · /leer JAMÁS devuelve acuses", "el bucle de acuses es imposible, no evitado")
def _s5():
    # Si un acuse fuera visible por /leer, y el cliente firma un acuse al leer, leer
    # un acuse dispararía otro acuse — sin fin. Es lista de PERMITIDOS.
    d, srv, base = _banco()
    try:
        a, b = _Casa(d, "ana"), _Casa(d, "beto")
        _alta_muda(d, "ana", a.llave + ".pub"); _alta_muda(d, "beto", b.llave + ".pub")
        s = _sobre("ana", "beto", "hola"); _post(base, s, a.firmar(s))
        ack = _sobre("beto", "ana", "", tipo="acuse", ref=1); _post(base, ack, b.firmar(ack))
        cod, r = _get(base, "/leer", _reto(a, "leer"))
        return all(m["tipo"] != "acuse" for m in r["mensajes"])
    finally:
        srv.shutdown()


@_caso("S6 · sin_cuerpo=1: el cuerpo NO viaja", "lo cumple el servicio, no el cliente")
def _s6():
    d, srv, base = _banco()
    try:
        a, b = _Casa(d, "ana"), _Casa(d, "beto")
        _alta_muda(d, "ana", a.llave + ".pub"); _alta_muda(d, "beto", b.llave + ".pub")
        s = _sobre("ana", "beto", "TEXTO-SECRETO"); _post(base, s, a.firmar(s))
        p = _reto(b, "leer"); p["sin_cuerpo"] = "1"
        cod, r = _get(base, "/leer", p)
        crudo = json.dumps(r)
        return "TEXTO-SECRETO" not in crudo and "cuerpo" not in r["mensajes"][0]
    finally:
        srv.shutdown()


@_caso("S7 · el reintento devuelve el folio ORIGINAL", "«no llegó» ≠ «lo mandé dos veces»")
def _s7():
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana"); _alta_muda(d, "ana", a.llave + ".pub")
        s = _sobre("ana", "beto", "hola"); firma = a.firmar(s)
        c1, r1 = _post(base, s, firma)
        c2, r2 = _post(base, s, firma)
        db = abrir(d); n = db.execute("SELECT COUNT(*) c FROM mensajes").fetchone()["c"]; db.close()
        return r1["folio"] == r2["folio"] and r2.get("duplicado") == 1 and n == 1
    finally:
        srv.shutdown()


@_caso("S8 · `maximo` es del LOG ENTERO, no del buzón", "con eso el cliente caza un corte")
def _s8():
    d, srv, base = _banco()
    try:
        a, b = _Casa(d, "ana"), _Casa(d, "beto")
        _alta_muda(d, "ana", a.llave + ".pub"); _alta_muda(d, "beto", b.llave + ".pub")
        # Cuerpos DISTINTOS a propósito: la primera versión de este caso mandó dos
        # mensajes idénticos a la misma casa en el mismo segundo, y el sobre canónico
        # salió igual — misma firma, y la regla del duplicado (S7) los colapsó. El
        # caso falló y el servidor tenía razón. Queda escrito porque es fácil de
        # repetir: dos envíos «distintos» que solo se diferencian en nada, no lo son.
        for para, cuerpo in (("carla", "uno"), ("carla", "dos"), ("beto", "tres")):
            s = _sobre("ana", para, cuerpo); _post(base, s, a.firmar(s))
        cod, r = _get(base, "/leer", _reto(b, "leer"))
        return len(r["mensajes"]) == 1 and r["maximo"] == 3
    finally:
        srv.shutdown()


@_caso("S9 · un reto de LEER no sirve para /estado", "la firma es por acción")
def _s9():
    # Si el reto fuera el mismo, una firma capturada en un sitio valdría en el otro.
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana"); _alta_muda(d, "ana", a.llave + ".pub")
        cod, r = _get(base, "/estado", _reto(a, "leer"))
        return cod == 403
    finally:
        srv.shutdown()


@_caso("S10 · /estado separa enviados de recibidos", "dos preguntas distintas")
def _s10():
    d, srv, base = _banco()
    try:
        a, b = _Casa(d, "ana"), _Casa(d, "beto")
        _alta_muda(d, "ana", a.llave + ".pub"); _alta_muda(d, "beto", b.llave + ".pub")
        s = _sobre("ana", "beto", "hola"); _post(base, s, a.firmar(s))
        ack = _sobre("beto", "ana", "", tipo="acuse", ref=1); _post(base, ack, b.firmar(ack))
        _, env = _get(base, "/estado", _reto(a, "estado"))          # ana: me acusaron
        p = _reto(b, "estado"); p["modo"] = "recibidos"
        _, rec = _get(base, "/estado", p)                            # beto: yo acusé
        _, nada = _get(base, "/estado", _reto(b, "estado"))          # beto no mandó nada
        return (len(env["acuses"]) == 1 and env["acuses"][0]["ref_folio"] == 1
                and len(rec["acuses"]) == 1 and len(nada["acuses"]) == 0)
    finally:
        srv.shutdown()


@_caso("S11 · un reto viejo no se acepta", "una firma capturada no vale para siempre")
def _s11():
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana"); _alta_muda(d, "ana", a.llave + ".pub")
        viejo = int(time.time()) - (VENTANA_RETO + 60)
        reto = {"accion": "leer", "quien": "ana", "desde": 0, "t": viejo}
        cod, r = _get(base, "/leer", {"quien": "ana", "desde": 0, "t": viejo,
                                      "firma": a.firmar(reto)})
        return cod == 403
    finally:
        srv.shutdown()


@_caso("S12 · el alta no sobrescribe una identidad con otra llave", "revocar es explícito")
def _s12():
    # Sobrescribir en silencio cambia QUIÉN PUEDE FIRMAR sin que nadie lo note.
    d, srv, base = _banco()
    try:
        a1, a2 = _Casa(d, "ana"), _Casa(d, "ana2")
        _alta_muda(d, "ana", a1.llave + ".pub")
        codigo = _alta_muda(d, "ana", a2.llave + ".pub")     # misma identidad, otra llave
        texto = open(os.path.join(d, NOMBRE_FIRMANTES), encoding="utf-8").read()
        return codigo == 1 and texto.count("\n") == 1
    finally:
        srv.shutdown()


@_caso("S13 · la portada no expone cuerpos", "un humano ve el tráfico, no el contenido")
def _s13():
    d, srv, base = _banco()
    try:
        a = _Casa(d, "ana"); _alta_muda(d, "ana", a.llave + ".pub")
        s = _sobre("ana", "beto", "TEXTO-SECRETO"); _post(base, s, a.firmar(s))
        cod, r = _get(base, "/", {})
        return cod == 200 and "TEXTO-SECRETO" not in json.dumps(r) and r["total"] == 1
    finally:
        srv.shutdown()


def suite(silencio=False):
    import shutil
    ancho = max(len(n) for n, _, _ in _CASOS)
    fallos = 0
    if not silencio:
        print("== conformidad del canal — %d casos ==\n" % len(_CASOS))
    for nombre, espera, fn in _CASOS:
        try:
            ok = bool(fn())
        except Exception as e:
            ok, espera = False, espera + "  [excepción: %r]" % e
        if not silencio:
            print("%s  %-*s   %s" % ("PASA " if ok else "FALLA", ancho, nombre, espera))
        fallos += 0 if ok else 1
    if not silencio:
        print("\n%d/%d" % (len(_CASOS) - fallos, len(_CASOS)))
    for p in os.listdir(tempfile.gettempdir()):
        if p.startswith("canal_"):
            shutil.rmtree(os.path.join(tempfile.gettempdir(), p), ignore_errors=True)
    return 1 if fallos else 0


USO = """servidor.py — el canal de mensajería firmado. Un solo archivo, sin dependencias.

  --iniciar [--puerto N] [--datos DIR]   levanta el servicio (por omisión 8090, ./datos)
  --alta IDENTIDAD RUTA.pub              da de alta una llave en trust_signers
  --conf IDENTIDAD RUTA_LLAVE            imprime un .mensajeria.conf listo para esa casa
  --conformidad                          corre sus propios casos; no toca ningún dato real
  --ayuda

El alta viaja SIEMPRE fuera de banda: el canal no puede transportar su propia llave."""


def main(argv):
    if not argv or "--ayuda" in argv or "-h" in argv:
        print(USO)
        return 0
    if "--conformidad" in argv:
        return suite()

    datos = os.path.abspath(argv[argv.index("--datos") + 1] if "--datos" in argv else "datos")
    os.makedirs(datos, exist_ok=True)

    if "--alta" in argv:
        i = argv.index("--alta")
        try:
            return alta(datos, argv[i + 1], argv[i + 2])
        except IndexError:
            raise SystemExit("uso: --alta IDENTIDAD RUTA.pub")
    if "--conf" in argv:
        i = argv.index("--conf")
        try:
            print(PLANTILLA_CONF.format(identidad=argv[i + 1], llave=argv[i + 2]), end="")
            return 0
        except IndexError:
            raise SystemExit("uso: --conf IDENTIDAD RUTA_LLAVE")
    if "--iniciar" in argv:
        puerto = int(argv[argv.index("--puerto") + 1] if "--puerto" in argv else 8090)
        handler = type("H", (Canal,), {"datos": datos})
        # 127.0.0.1 por omisión y a propósito: exponer un servicio a la red es un acto
        # deliberado de quien despliega, nunca el valor por omisión de un programa.
        srv = ThreadingHTTPServer(("127.0.0.1", puerto), handler)
        print("canal en http://127.0.0.1:%d  ·  datos en %s" % (puerto, datos))
        print("firmantes: %s" % os.path.join(datos, NOMBRE_FIRMANTES))
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\ndetenido")
        return 0
    print(USO, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
