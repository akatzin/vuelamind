#!/usr/bin/env python3
"""Banco de la puerta del puente — se corre, no se lee.

    python3 probar_puerta.py <ruta/session_bridge.py> <python3> <registro.json> <env>

Genera pares de claves ES256 DE VERDAD con openssl, sirve un JWKS local y ejerce los
casos contra un puente levantado de verdad. Lo unico simulado es de donde salen las
claves publicas: la firma, la verificacion y los 403 son reales.

LO QUE IMPORTA SON LOS NEGATIVOS. Que la pagina cargue con un token bueno no demuestra
nada -- lo demuestra que NO cargue con uno fabricado. Si el caso de la cabecera firmada
con otra clave pasara, no habria puerta: habria un cartel de puerta.
"""
import base64, json, os, re, signal, socket, subprocess, sys, tempfile, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TMP = Path(tempfile.mkdtemp(prefix="puerta-"))
def sh(*a, **k): return subprocess.run(a, capture_output=True, text=True, **k)
def b64u(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")

def par_de_claves(nombre):
    k = TMP / f"{nombre}.pem"
    sh("openssl", "ecparam", "-genkey", "-name", "prime256v1", "-noout", "-out", str(k))
    txt = sh("openssl", "ec", "-in", str(k), "-pubout", "-text", "-noout").stdout
    hexs = re.search(r"pub:\s*((?:\s*[0-9a-f]{2}:?)+)", txt).group(1)
    raw = bytes.fromhex(re.sub(r"[\s:]", "", hexs))
    assert raw[0] == 0x04 and len(raw) == 65, f"punto raro: {len(raw)}"
    return k, {"kty":"EC","crv":"P-256","alg":"ES256","kid":nombre,
               "x": b64u(raw[1:33]), "y": b64u(raw[33:])}

def der_a_crudo(der):
    i = 2
    if der[1] & 0x80: i += der[1] & 0x7F
    assert der[i] == 0x02; lr = der[i+1]; r = der[i+2:i+2+lr]; i = i+2+lr
    assert der[i] == 0x02; ls = der[i+1]; s = der[i+2:i+2+ls]
    r = r.lstrip(b"\x00").rjust(32, b"\x00"); s = s.lstrip(b"\x00").rjust(32, b"\x00")
    return r + s

def jwt(clave, kid, cuerpo):
    cab = b64u(json.dumps({"alg":"ES256","typ":"JWT","kid":kid}).encode())
    cue = b64u(json.dumps(cuerpo).encode())
    dato = TMP / "d.bin"; dato.write_bytes(f"{cab}.{cue}".encode())
    der = subprocess.run(["openssl","dgst","-sha256","-sign",str(clave),str(dato)],
                         capture_output=True).stdout
    return f"{cab}.{cue}.{b64u(der_a_crudo(der))}"

BUENA, JWK_BUENA = par_de_claves("la-buena")
MALA,  _         = par_de_claves("la-mala")

class JWKS(BaseHTTPRequestHandler):
    def do_GET(self):
        b = json.dumps({"keys":[JWK_BUENA]}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass

srv = ThreadingHTTPServer(("127.0.0.1", 8899), JWKS)
threading.Thread(target=srv.serve_forever, daemon=True).start()

AUD = "/projects/123/global/backendServices/456"
PUENTE = sys.argv[1]; PY3 = sys.argv[2]; REG = sys.argv[3]; ENVV = sys.argv[4]
base = dict(os.environ, BRIDGE_PERMISSION="safe", BRIDGE_REGISTRY=REG,
            VUELAMIND_RC_ENV=ENVV, BRIDGE_IAP_JWKS_URL="http://127.0.0.1:8899/jwks")

def arranca(puerto, extra, espera=3):
    env = dict(base, PORT=str(puerto), **extra)
    p = subprocess.Popen([PY3, PUENTE], env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
    t0 = time.time()
    while time.time() - t0 < espera:
        if p.poll() is not None:
            return p, p.stdout.read()
        try:
            socket.create_connection(("127.0.0.1", puerto), 0.2).close()
            return p, None
        except OSError: time.sleep(0.15)
    return p, None

def pedir(puerto, cabeceras=None, ruta="/sessions"):
    r = urllib.request.Request(f"http://127.0.0.1:{puerto}{ruta}",
                               headers={"Host": "agente.ejemplo.com", **(cabeceras or {})})
    try:
        with urllib.request.urlopen(r, timeout=6) as x: return x.status, x.read().decode()[:120]
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:160]
    except Exception as e: return 0, f"{type(e).__name__}: {e}"

fallos = []
def caso(nombre, real, esperado):
    ok = real == esperado
    print(f"  {'OK ' if ok else 'MAL'}  {nombre}: {real}   (esperado {esperado})")
    if not ok: fallos.append(nombre)

print("=== ARRANQUE: falla cerrado ===")
p, salida = arranca(8891, {"BRIDGE_PUBLIC_ORIGIN": "https://agente.ejemplo.com"})
caso("origen publico sin audiencia -> no arranca", p.poll() is not None, True)
if salida: print("        dice:", salida.strip().split("\n")[0][:90])
p.kill()

p, salida = arranca(8892, {"BRIDGE_PUBLIC_ORIGIN": "http://agente.ejemplo.com",
                           "BRIDGE_IAP_AUDIENCE": AUD})
caso("origen publico sin https -> no arranca", p.poll() is not None, True)
if salida: print("        dice:", salida.strip().split("\n")[0][:90])
p.kill()

print("\n=== CON LA PUERTA PUESTA ===")
p, _ = arranca(8893, {"BRIDGE_PUBLIC_ORIGIN": "https://agente.ejemplo.com",
                      "BRIDGE_IAP_AUDIENCE": AUD}, espera=6)
if p.poll() is not None:
    print("  el puente no levanto:", p.stdout.read()[:400]); sys.exit(1)
try:
    ahora = int(time.time())
    val = lambda **k: dict({"iss":"https://cloud.google.com/iap","aud":AUD,
                            "email":"quien@ejemplo.com","exp":ahora+600,"iat":ahora}, **k)
    caso("/health sin nada (lo sondea el balanceador)", pedir(8893, ruta="/health")[0], 200)
    caso("NEGATIVO 1 · sin cabecera", pedir(8893)[0], 403)
    cod, cuerpo = pedir(8893, {"x-goog-iap-jwt-assertion": jwt(MALA, "la-buena", val())})
    caso("NEGATIVO 2 · cabecera fabricada (firmada con otra clave)", cod, 403)
    print("        dice:", cuerpo[:120])
    caso("firma valida pero para otro servicio (aud)",
         pedir(8893, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val(aud="/otro"))})[0], 403)
    caso("firma valida pero caducada",
         pedir(8893, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val(exp=ahora-10))})[0], 403)
    caso("firma valida pero otro emisor",
         pedir(8893, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val(iss="https://malo"))})[0], 403)
    caso("basura en la cabecera", pedir(8893, {"x-goog-iap-jwt-assertion":"no.soy.jwt"})[0], 403)
    caso("POSITIVO · token bueno", pedir(8893, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val())})[0], 200)
finally:
    p.kill()

print("\n=== LISTA DE CORREOS (defensa en profundidad) ===")
p, _ = arranca(8895, {"BRIDGE_PUBLIC_ORIGIN": "https://agente.ejemplo.com",
                      "BRIDGE_IAP_AUDIENCE": AUD,
                      "BRIDGE_IAP_EMAILS": "duena@ejemplo.com, otra@ejemplo.com"}, espera=6)
try:
    ahora = int(time.time())
    val2 = lambda **k: dict({"iss":"https://cloud.google.com/iap","aud":AUD,
                             "exp":ahora+600,"iat":ahora}, **k)
    caso("correo dado de alta -> entra",
         pedir(8895, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val2(email="duena@ejemplo.com"))})[0], 200)
    caso("mayusculas del correo no importan",
         pedir(8895, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val2(email="Duena@Ejemplo.com"))})[0], 200)
    cod, cuerpo = pedir(8895, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val2(email="ajena@ejemplo.com"))})
    caso("token PERFECTO de otra identidad -> fuera", cod, 403)
    print("        dice:", cuerpo[:130])
    caso("token sin correo -> fuera",
         pedir(8895, {"x-goog-iap-jwt-assertion": jwt(BUENA,"la-buena",val2())})[0], 403)
finally:
    p.kill()

print("\n=== SIN PUERTA (instalacion local, no debe cambiar) ===")
p, _ = arranca(8894, {}, espera=6)
try:
    r = urllib.request.Request("http://127.0.0.1:8894/sessions", headers={"Host":"127.0.0.1:8894"})
    with urllib.request.urlopen(r, timeout=6) as x: cod = x.status
    caso("loopback sigue entrando sin cabecera", cod, 200)
    caso("host ajeno sigue rechazado", pedir(8894)[0], 403)
finally:
    p.kill()

print()
print("RESULTADO:", "VERDE" if not fallos else f"ROJO — {fallos}")
sys.exit(1 if fallos else 0)
