#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disparador.py — el reloj que despierta a una instancia cuando le llega un mensaje.

UN SOLO ARCHIVO, Python 3.9, SIN DEPENDENCIAS EXTERNAS. Y eso no es minimalismo:
macOS trae 3.9.6 del sistema y en las máquinas de la colmena no hay `brew`, así que
todo lo que pida instalar algo no se puede desplegar donde tiene que correr.

POR QUÉ ES CÓDIGO Y NO UN DOCUMENTO. La versión anterior de este mecanismo viajó
como prosa. En la casa que la implementó salió un disparador que reanudó contra su
propia sesión viva; se salvó por un código de salida que nadie supo explicar. La
lectura: un PROTOCOLO viaja en prosa —bytes, firmas, endpoints: se lee y se
verifica— pero la CONCURRENCIA no, porque quien implementa reconstruye su propia
versión de las carreras. Lo que va aquí dentro es exactamente la concurrencia.

LA COSTURA. Este archivo encapsula lo que es igual en todas partes (candado, sellos,
topes, reloj de invocación, cursor, guardas) y DELEGA en configuración lo único que
es propio de cada herramienta: cómo se enumeran las sesiones vivas y cómo se le
entrega un recado a una viva. Si tu herramienta no puede contestar eso, ése es tu
hueco: se declara, no se sustituye por un proxy.

EL HUECO QUE NINGUNA GUARDA DE ESTE ARCHIVO CIERRA, Y HAY QUE DECIRLO.
Este disparador transporta PETICIONES. Una petición puede ser legítima en la forma
—bien argumentada, de una casa de confianza, con su contexto y su enlace— y aun así
no traer el permiso que hacía falta. Ninguna guarda por identificador ni por estado
distingue una orden autorizada de una que no lo está: eso solo lo sabe el dueño de la
casa que la recibe.

MEDIDO el 2026-09-01, y contra quien escribe esto: esta casa pidió a cuatro casas que
ejecutaran este artefacto cuando su dueño solo había autorizado a una. Ninguna de las
tres de más tenía forma mecánica de saberlo. Lo que lo frenó no fue una comprobación:
fue que una de ellas se negó a descargar y ejecutar código porque se lo pedía una casa
hermana, y fue a preguntarle a su dueño.

Por eso la regla del protocolo —el canal transporta hechos y peticiones, JAMÁS
autorizaciones— no es una restricción del transporte: es la única defensa que hay, y
vive en la conducta de quien recibe, no en el código de quien manda.
(Aportado por la casa que se negó, sin que se le pidiera.)

LA SESIÓN NO SE CONFIGURA: SE RESUELVE. Corrección del 2026-09-01.
La versión anterior pedía el identificador de la sesión a despertar como un valor
de configuración. Era un puntero estático a un blanco móvil: la sesión de una casa
cambia sin emitir señal —un `/clear` basta— y desde ahí el enumerador ya no la
encuentra. El disparador leía esa ausencia como «la casa está cerrada», reanudaba
el transcript ABANDONADO, la invocación salía 0, y CONFIRMABA. El cursor avanzaba
sobre una entrega que nadie recibió: sin error, sin registro, todo verde.

Lo que estaba mal no era la guarda: era LA PREGUNTA. Se preguntaba «¿vive la sesión
X?» cuando lo que hay que saber es «¿CUÁL es la sesión de esta casa, ahora?». Una
casa es un DIRECTORIO —el de su configuración— y eso no se mueve; la sesión sí. Por
eso se resuelve en cada ciclo contra el enumerador, exigiendo EXACTAMENTE UNA: cero
es una casa cerrada, dos es una casa ambigua, y en ninguno de los dos casos se
entrega ni se confirma.

MEDIDO en esta casa, y es el caso que lo destapó: el 2026-09-01 se perdió así el
folio 874 — que era, precisamente, otra casa avisando de este mismo defecto. Lo halló
Sho LEYENDO este archivo, no ejecutándolo: la batería pasaba en verde CON el defecto
dentro, porque certificaba «reanudar y confirmar» como la conducta correcta. Un caso
que consagra el defecto es peor que no tener casos.

Y LA CONSECUENCIA, ENTERA: `cmd_reanudar` SALIÓ DEL CAMINO DE ENTREGA. Sus dos únicos
blancos posibles están medidos como rotos en la herramienta para la que esto se
escribió — contra un transcript abandonado levanta a un lector que no es nadie
(arriba), y contra una sesión ABIERTA levanta un gemelo sin cabeza que contesta en su
lugar y firma el acuse (MEDIDO el 2026-08-23). Sin blanco legítimo no queda rama.

La única entrega es `cmd_entregar` contra una sesión viva resuelta. Y AQUÍ HUBO UNA
AFIRMACIÓN FALSA QUE DURÓ UNAS HORAS, escrita en este mismo sitio: se dijo que esta vía
era segura porque «si el blanco es el equivocado, FALLA». MEDIDO el 2026-09-01: es falso.
Entregar a un nombre que no existe termina en CÓDIGO 0 — el agente explica en prosa que
no envió nada y el proceso sale bien.

O sea que la vía que quedaba tenía el MISMO vicio que la retirada: una invocación que
acierta el código de salida sin que nadie reciba nada. La reanudación mentía por
resucitar un transcript abandonado; ésta miente porque el código de salida mide el
PROCESO, no el recado.

Lo que de verdad cierra el hueco no es elegir mejor vía: es no aceptar la ausencia de
error como prueba. El éxito exige un ACUSE POSITIVO —la plantilla ya pedía «después
responde solo OK», y nadie lo comprobaba jamás—. Sin acuse no se confirma, el folio
espera y el siguiente ciclo reintenta. Un contrato que no se verifica es una decoración.

DESPERTAR UNA CASA CERRADA QUEDA SIN RESOLVER, y se declara como hueco en vez de
fingirse: el folio espera en la cola y la casa lo recoge cuando abre. Un hueco
declarado se puede cerrar; una entrega falsa no se nota.
"""

import json
import os
import subprocess
import sys
import time

VERSION = "1"
NOMBRE_CONF = ".disparador.conf"


# ─────────────────────────────────────────────────────────────────────────────
# Configuración — misma regla de búsqueda que `.mensajeria.conf`: desde el directorio
# de trabajo hacia arriba, como git con `.git`.
#
# ACEPTA `clave = valor` Y `clave valor`. Antes solo lo segundo, mientras decía usar
# "el mismo formato" que la del canal — que parte por `=`. Eran DOS formatos para el
# mismo mecanismo, o sea el defecto de las dos fuentes que este comentario presumía de
# evitar. Se acepta el de la conf del canal, que es el que la gente ya escribe.
# ─────────────────────────────────────────────────────────────────────────────

# `sesion` YA NO EXISTE como clave, y su ausencia es el arreglo: un identificador
# de sesión escrito a mano es un puntero estático a un blanco móvil. Lo que se
# declara ahora es `casa` —un directorio, que no se mueve— y por omisión es el
# directorio de esta misma configuración, así que no hay nada que rellenar.
OBLIGATORIAS = ("cliente", "cmd_vivas", "cmd_entregar")

POR_OMISION = {
    "casa": "",
    "intervalo": "15",
    "tope_invocacion": "90",
    "max_intentos": "3",
    "cache_vivas": "60",
    "rezagados_cada": "600",
    "rezagados_edad": "600",
    "rezagados_max": "3",
    "bitacora": "",
    "acuse_entrega": "OK",
    "sesion_propia": "",
    "env_sesion_propia": "CLAUDE_SESSION_ID",
    "tipos_despiertan": "mensaje",
}


# ─────────────────────────────────────────────────────────────────────────────
# LA PLANTILLA VIAJA DENTRO, Y NO ES COMODIDAD
#
# Los tres comandos de abajo son lo único propio de cada herramienta, y son
# justo lo que quien instala tendría que ADIVINAR. Adivinar en la instalación es
# el defecto que ya pagamos en otro sitio: un documento mandaba editar constantes
# que el código había dejado de usar diez días antes, y nadie lo notó porque
# nadie instaló desde cero. Una plantilla que se envejece sola es lo mismo con
# otra ropa — por eso hay un caso que comprueba que ésta sigue completa.
# ─────────────────────────────────────────────────────────────────────────────

PLANTILLA_CONF = r"""# .disparador.conf — generado por `disparador.py --plantilla`.
# Formato `clave valor`, separado por espacios. Se busca desde el directorio de
# trabajo hacia arriba, como git con `.git` — igual que la del canal.

# ── RELLENA ESTOS DOS ────────────────────────────────────────────────────────
# La LLAVE es la MISMA que declara tu .mensajeria.conf. No la copies de aqui: copiala
# de alli. Fijar una ruta en una plantilla ya costo un defecto —el skill mandaba usar
# ~/.ssh y las casas reales no guardan ahi su llave del canal, asi que quien seguia el
# documento daba de alta una publica que su cliente nunca iba a usar.
cliente           /ruta/absoluta/al/cliente_del_canal.py
llave             /LA-MISMA-RUTA-QUE-PUSISTE-EN-.mensajeria.conf

# NO hay que poner ningun identificador de sesion, y eso es a proposito: la
# sesion de una casa cambia sola —un /clear basta— y un id escrito aqui apunta
# a un blanco que se movio. La casa es su DIRECTORIO, y por omision es el de
# este archivo. Solo se declara si la conf no vive en la casa:
# casa            /ruta/absoluta/a/la/casa

# ── LO DEMAS YA VIENE ESCRITO PARA CLAUDE CODE ───────────────────────────────
# Son los dos comandos propios de la herramienta. En otra herramienta, estos dos
# son tu hueco: se declaran, no se inventan.
#
# CONTRATO DE cmd_vivas: JSON, una lista de sesiones vivas, y cada una con
# `cwd`, `sessionId` y `name`. El `cwd` NO es opcional: es como se sabe cual de
# las sesiones vivas es esta casa. Si tu herramienta no lo reporta, ese es tu
# hueco y se declara — sin el, este disparador no entrega nada.
cmd_vivas         claude agents --json
cmd_entregar      claude -p "Usa la herramienta SendMessage para enviar a \"{nombre}\" exactamente este texto y nada mas: \"{aviso}\" Despues responde solo OK."

# EL ACUSE NO ES ADORNO, y su ausencia costo un defecto: MEDIDO el 2026-09-01, entregar
# a un nombre que NO existe termina en CODIGO 0 — el agente explica en prosa que no
# envio nada y el proceso sale bien. El codigo de salida mide el PROCESO, no el recado.
# Por eso solo cuenta como entregado si la ULTIMA linea es exactamente este acuse.
# Se compara la ultima linea y no "contiene": el texto del fracaso medido trae la
# palabra OK dentro de una frase que dice justo lo contrario.
# Vacio lo desactiva, y entonces vuelves a confiar en el codigo de salida — no lo hagas.
acuse_entrega     OK

# cmd_reanudar NO existe y no se echa de menos: despertar una casa CERRADA es un
# hueco declarado de este artefacto. Contra un transcript abandonado se levanta a
# nadie, y contra una sesion abierta se levanta un gemelo que firma el acuse — las
# dos cosas MEDIDAS. El folio espera en la cola y la casa lo recoge al abrir.

# ── AJUSTES, con valores sanos por omision ───────────────────────────────────
bitacora          ~/Library/Logs/vuelamind-disparador.log
intervalo         15
tope_invocacion   90
tipos_despiertan  mensaje
"""


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


def leer_conf(ruta):
    cfg = dict(POR_OMISION)
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            # ACEPTA LOS DOS FORMATOS, y es una correccion: este archivo declaraba
            # usar "el mismo formato que la del canal" y era FALSO — `.mensajeria.conf`
            # parte por `=` y esta partia por espacios. Dos archivos hermanos con dos
            # formatos, que es exactamente el defecto de las dos fuentes que el
            # comentario de arriba decia evitar. Hallado por Samantha el 2026-09-01
            # midiendo el parser en vez de creerle al texto.
            if "=" in linea.split("#", 1)[0]:
                k, v = linea.split("=", 1)
            else:
                partes = linea.split(None, 1)
                if len(partes) != 2:
                    continue
                k, v = partes
            cfg[k.strip().lower()] = v.strip()
    faltan = [k for k in OBLIGATORIAS if not cfg.get(k)]
    if faltan:
        raise SystemExit("falta(n) en %s: %s" % (ruta, ", ".join(faltan)))
    # La casa es el directorio de su propia configuración salvo que se diga otra
    # cosa. Que el valor por omisión sea una ruta y no un identificador es la
    # corrección entera: un directorio no cambia cuando la sesión cambia.
    if not cfg.get("casa"):
        cfg["casa"] = os.path.dirname(os.path.abspath(ruta))
    cfg["casa"] = os.path.abspath(os.path.expanduser(cfg["casa"]))
    # Una clave retirada que se ignora en silencio es una configuración que
    # miente: quien la escribió cree que sigue mandando. Se nombra.
    obsoletas = [k for k in ("sesion", "cmd_reanudar") if cfg.get(k)]
    if obsoletas:
        sys.stderr.write(
            "AVISO: %s ya no se usa(n) y se ignora(n) en %s — la sesión se resuelve\n"
            "sola por `casa` (%s). Bórralas para que la conf no diga lo que no hace.\n"
            % (", ".join(obsoletas), ruta, cfg["casa"]))
    return cfg


# ─────────────────────────────────────────────────────────────────────────────
# Bitácora propia — salida de PRIMERA CLASE, no `stderr` a un archivo temporal.
# Cuando en una casa ajena falló una reanudación, el único testigo de que había
# salido bien fue un número sin explicación. Lo que no se sabe por qué falló no
# se sabe si volverá a fallar.
# ─────────────────────────────────────────────────────────────────────────────

class Bitacora:
    def __init__(self, ruta, observando):
        self.ruta = ruta or None
        self.observando = observando
        if self.ruta:
            os.makedirs(os.path.dirname(os.path.abspath(self.ruta)), exist_ok=True)

    def __call__(self, evento, **datos):
        campos = " ".join("%s=%s" % (k, v) for k, v in sorted(datos.items()))
        marca = "OBSERVA " if self.observando else ""
        linea = "%s %s%s %s" % (time.strftime("%Y-%m-%dT%H:%M:%S"), marca, evento, campos)
        sys.stderr.write(linea + "\n")
        if self.ruta:
            with open(self.ruta, "a", encoding="utf-8") as f:
                f.write(linea + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Ejecución con reloj. Al vencer se mata al proceso Y A SUS HIJOS: un proceso
# colgado deja descendientes que siguen reteniendo la salida, y entonces el ciclo
# "termina" pero el disparador no suelta. Se descubrió cuando el propio banco de
# pruebas se colgó por un hijo huérfano.
#
# La entrada va a DEVNULL y eso NO es adorno: heredar la tubería de donde salió la
# lista de pendientes hace que el proceso se trague las líneas que faltaban CON SUS
# CUERPOS COMPLETOS — o sea, el cuerpo que el sobre evita a propósito entraba por
# detrás y en la misma posición de instrucción contra la que se diseñó el sobre.
# ─────────────────────────────────────────────────────────────────────────────

def correr(cmd, tope, entrada_nula=True):
    """Devuelve (codigo, salida). Nunca lanza por código distinto de cero."""
    try:
        p = subprocess.Popen(
            cmd, shell=True, stdin=subprocess.DEVNULL if entrada_nula else None,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            start_new_session=True,  # grupo propio: para poder matar a los hijos
        )
    except Exception as e:
        return 127, "no se pudo lanzar: %s" % e
    try:
        salida, _ = p.communicate(timeout=tope)
        return p.returncode, (salida or b"").decode("utf-8", "replace").strip()
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(p.pid), 15)
        except Exception:
            pass
        try:
            salida, _ = p.communicate(timeout=5)
        except Exception:
            salida = b""
        try:
            os.killpg(os.getpgid(p.pid), 9)
        except Exception:
            pass
        return 124, (salida or b"").decode("utf-8", "replace").strip()


# ─────────────────────────────────────────────────────────────────────────────
# LO QUE VIENE DE FUERA NO ENTRA CRUDO A UN SHELL
#
# Hallazgo de Sho (2026-09-01): `nombre` sale del JSON del enumerador y se
# interpola en `cmd_entregar`, que corre con shell=True — un nombre con comillas
# EJECUTA. El vector realista es local, así que la gravedad es baja; la familia no
# lo es: es la misma que el `echo` sin comillas que hacía pasar a C16 por
# accidente, y ese defecto ya mordió una vez aquí dentro.
#
# `de` y el folio vienen de OTRA CASA por el canal. Si el servicio no los restringe
# a identidades registradas, el vector deja de ser local — Sho declaró que eso no lo
# midió, y esta casa tampoco. Por eso se acotan igual, en vez de descansar en una
# restricción que nadie ha comprobado.
#
# Se LIMPIA en vez de entrecomillar, y es a propósito: la plantilla ya trae
# `{nombre}` dentro de comillas, así que añadir las nuestras rompería el texto. Un
# nombre de sesión es una etiqueta para mostrar; quitarle metacaracteres no le
# quita nada que signifique algo.
# ─────────────────────────────────────────────────────────────────────────────

_PELIGROSOS = '"\'`$\\;&|<>\n\r'


def _seguro(valor):
    return "".join(c for c in str(valor) if c not in _PELIGROSOS)


# ─────────────────────────────────────────────────────────────────────────────
# El candado. El cursor se queda atrás a propósito hasta que el trabajo termina,
# así que un ciclo lento garantiza que el siguiente tick vea los mismos pendientes
# y lance una segunda invocación sobre la misma sesión. No es higiene: es parte de
# la corrección.
#
# Directorio y no `flock`: flock(1) es de util-linux y macOS no lo trae. Crear un
# directorio es atómico en POSIX. No bloqueante: un tick que espera acumula ticks
# esperando. En disco LOCAL: la atomicidad se debilita sobre NFS/SMB, y mover el
# candado a un recurso compartido "para que lo vean las dos máquinas" rompe
# exactamente lo que lo hacía candado.
# ─────────────────────────────────────────────────────────────────────────────

def sello_de(pid):
    """Identidad del proceso, no solo su número. LC_ALL=C porque `lstart` cambia
    de formato con el locale, y los programadores del sistema no heredan el
    entorno del shell: sin fijarlo, el MISMO proceso da cadenas distintas según
    quién pregunte, y el dueño vivo se lee como huérfano."""
    env = dict(os.environ, LC_ALL="C")
    try:
        s = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           env=env, timeout=10)
        return " ".join(s.stdout.decode("utf-8", "replace").split())
    except Exception:
        return ""


class Candado:
    def __init__(self, ruta, log):
        self.ruta, self.log, self.mio = ruta, log, False

    def tomar(self):
        try:
            os.mkdir(self.ruta)
        except FileExistsError:
            return self._rescatar()
        except Exception as e:
            self.log("candado_error", detalle=e)
            return False
        self._firmar()
        return True

    def _firmar(self):
        with open(os.path.join(self.ruta, "pid"), "w") as f:
            f.write(str(os.getpid()))
        with open(os.path.join(self.ruta, "sello"), "w") as f:
            f.write(sello_de(os.getpid()))
        self.mio = True

    def _rescatar(self):
        # Huérfano si: no hay pid · el pid ya no existe · o existe pero es OTRO
        # proceso que heredó el número. Preguntar solo si el pid vive no basta:
        # con reutilización de PID la lógica ve "vivo" y se salta turnos PARA
        # SIEMPRE. Por eso se compara también la hora de arranque.
        try:
            with open(os.path.join(self.ruta, "pid")) as f:
                duenio = f.read().strip()
            with open(os.path.join(self.ruta, "sello")) as f:
                guardado = f.read().strip()
        except Exception:
            duenio, guardado = "", ""
        actual = sello_de(duenio) if duenio else ""
        if not duenio or not actual or actual != guardado:
            self.log("candado_huerfano", pid=duenio or "?")
            import shutil
            shutil.rmtree(self.ruta, ignore_errors=True)
            try:
                os.mkdir(self.ruta)
            except Exception:
                return False
            self._firmar()
            return True
        return False   # otro ciclo trabaja: el siguiente tick lo recoge

    def soltar(self):
        if self.mio:
            import shutil
            shutil.rmtree(self.ruta, ignore_errors=True)
            self.mio = False


# ─────────────────────────────────────────────────────────────────────────────
# Cuenta de intentos en disco: si un folio se anuncia y el cursor no avanza, el
# siguiente ciclo lo vuelve a encontrar — sin tope eso es un bucle infinito que
# cuesta una sesión por vuelta.
# ─────────────────────────────────────────────────────────────────────────────

def intentos(ruta, folio, sumar=False):
    n = 0
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            n = sum(1 for l in f if l.strip() == str(folio))
    if sumar:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("%s\n" % folio)
        n += 1
    return n


def olvidar(ruta, folio):
    if not os.path.exists(ruta):
        return
    with open(ruta, encoding="utf-8") as f:
        quedan = [l for l in f if l.strip() != str(folio)]
    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(quedan)


# ─────────────────────────────────────────────────────────────────────────────
# El disparador
# ─────────────────────────────────────────────────────────────────────────────

class Disparador:
    def __init__(self, cfg, log, observando=False):
        self.cfg, self.log, self.observando = cfg, log, observando
        self.tmp = os.environ.get("TMPDIR", "/tmp")
        self.cliente = cfg["cliente"]
        self.casa = cfg["casa"]
        self.desde_cache = False
        self.tope = int(cfg["tope_invocacion"])
        self.ident = self._identidad()
        base = os.path.join(self.tmp, "disparador_%s" % self.ident)
        self.candado = Candado(base + ".lock", log)
        self.cuenta = base + ".intentos"
        self.cache_vivas = base + ".vivas"

    # La identidad se le pregunta AL CLIENTE, que es quien de verdad la sabe, en
    # vez de tomarla de una etiqueta que alguien puede escribir mal. Y el candado
    # es POR IDENTIDAD y no por máquina: varias casas viven en el mismo equipo y
    # con un candado de ruta fija se estorbarían sin compartir nada.
    def _identidad(self):
        cod, sal = correr("python3 %s identidad" % self.cliente, 30)
        if cod != 0 or not sal:
            raise SystemExit("el cliente no da identidad (código %s): %s" % (cod, sal))
        return sal.strip().splitlines()[-1].strip()

    # ── GUARDA DETERMINISTA ──────────────────────────────────────────────────
    # Un disparador JAMÁS se entrega a la sesión desde la que corre, y se comprueba
    # por IDENTIFICADOR, no por estado. No es una costumbre, es un imposible: no
    # depende de que ninguna fuente diga la verdad.
    #
    # Ahora se compara contra la sesión RESUELTA y no contra una escrita en la
    # configuración, así que la guarda dejó de depender de que alguien copiara bien
    # un identificador. Cuesta lo mismo: la resolución ya se hizo.
    def guarda_autoataque(self, sesion):
        propia = self.cfg.get("sesion_propia") or os.environ.get(
            self.cfg.get("env_sesion_propia") or "", "")
        if propia and propia.strip() == str(sesion).strip():
            self.log("ME_NIEGO_autoataque", sesion=sesion)
            return False
        return True

    def pendientes(self):
        # LA COLA PRIMERO, Y NADA DE PROCESOS SI ESTÁ VACÍA. Preguntar por el
        # estado de la sesión levanta un proceso —y en macOS dispara el diálogo
        # de acceso a datos de otras apps. Con cuatro casas cada 15 s eso son
        # ~960 procesos por hora solo para averiguar si alguien está en casa.
        cod, sal = correr("python3 %s pendientes" % self.cliente, 30)
        if cod != 0:
            self.log("cola_error", codigo=cod, salida=sal[:200])
            return []
        out = []
        for l in sal.splitlines():
            l = l.strip()
            if not l:
                continue
            try:
                out.append(json.loads(l))
            except ValueError:
                continue
        return out

    def resolver_casa(self, usar_cache=True):
        """¿CUÁL es la sesión de esta casa, ahora? Devuelve `(sesión, nombre)` si
        hay EXACTAMENTE una viva en este directorio, None si no hay ninguna, y
        False si NO SE PUDO SABER. Tres estados, no dos: 'no pude preguntar' no es
        'está cerrada'.

        Dos vivas en la misma casa tampoco es una respuesta: es una casa ambigua,
        y elegir una de las dos sería adivinar con cara de dato. También devuelve
        None — con su propio motivo en la bitácora, que no es lo mismo."""
        # Se cachea SOLO el resultado POSITIVO, y no es pereza: equivocarse hacia
        # "está viva" cuesta un aviso que el siguiente ciclo repite; equivocarse
        # hacia "cerrada" lanza una reanudación contra una sesión viva y fabrica
        # gemelos sin cabeza. Un fallo cuesta un aviso; el otro cuesta la verdad
        # de la bitácora.
        # La caché guarda EL PAR sesión+nombre, nunca el nombre suelto: un nombre
        # sin su identificador se puede volver a emparejar con la sesión
        # equivocada, que es en pequeño el mismo defecto que este rediseño quita.
        # De DÓNDE salió la respuesta importa tanto como la respuesta: una
        # resolución de caché no está verificada, y un intento gastado contra un
        # blanco sin verificar no puede contar como «nadie lo recoge». Ver el
        # bloque de intentos en `_entregar`.
        self.desde_cache = False
        vida = int(self.cfg["cache_vivas"])
        if usar_cache and os.path.exists(self.cache_vivas):
            if time.time() - os.path.getmtime(self.cache_vivas) < vida:
                with open(self.cache_vivas, encoding="utf-8") as f:
                    guardado = f.read().strip().split("\t")
                if len(guardado) == 2 and guardado[0]:
                    self.desde_cache = True
                    return (guardado[0], guardado[1])
        cod, sal = correr(self.cfg["cmd_vivas"], 60)
        if cod != 0:
            self.log("vivas_incontestable", codigo=cod, salida=sal[:200])
            return False
        try:
            datos = json.loads(sal)
        except ValueError:
            self.log("vivas_ilegible", salida=sal[:200])
            return False
        # realpath en los dos lados: en macOS /tmp es un enlace a /private/tmp, y
        # dos rutas que nombran el mismo directorio no se pueden comparar como
        # texto sin resolverlas antes.
        casa = os.path.realpath(self.casa)
        mias, vistas, con_cwd = [], 0, 0
        for a in datos if isinstance(datos, list) else []:
            vistas += 1
            cwd = a.get("cwd") or ""
            sid = str(a.get("sessionId", ""))
            if not cwd or not sid:
                continue
            con_cwd += 1
            if os.path.realpath(os.path.expanduser(cwd)) == casa:
                mias.append((sid, a.get("name") or ""))
        # HALLAZGO DE SHO (2026-09-01): un enumerador que devuelve sesiones vivas
        # pero NINGUNA con `cwd` se leía idéntico a «esta casa está cerrada». Si una
        # versión futura de la herramienta deja de reportarlo, todas las casas
        # quedarían mudas a la vez y el registro culparía a los durmientes. Es «un
        # chequeo verde puede significar que no está mirando», en versión roja.
        #
        # No es cerrada: es NO SE PUDO SABER, y por eso devuelve False — que no
        # gasta intento y no confirma nada.
        if vistas and not con_cwd:
            self.log("vivas_sin_cwd", vistas=vistas,
                     motivo="el enumerador no reporta `cwd`; no se puede saber qué "
                            "sesión es esta casa. NO es una casa cerrada")
            return False
        if len(mias) == 1:
            sid, nombre = mias[0]
            with open(self.cache_vivas, "w", encoding="utf-8") as f:
                f.write("%s\t%s" % (sid, nombre))
            return (sid, nombre)
        try:
            os.remove(self.cache_vivas)
        except OSError:
            pass
        if len(mias) > 1:
            self.log("casa_ambigua", casa=self.casa,
                     sesiones=",".join(s for s, _ in mias),
                     motivo="varias sesiones vivas aquí; elegir una sería adivinar")
        return None

    # ── EL SOBRE: folio y cómo leerlo, JAMÁS el cuerpo ───────────────────────
    # Frontera de seguridad, no ahorro. El cuerpo lo escribe otra instancia;
    # metido literal en el prompt llega EN POSICIÓN DE INSTRUCCIÓN. Pasando solo
    # el folio, el agente va a buscarlo y llega como dato que fue a traer.
    def sobre(self, msgs):
        lineas = "\n".join("  - folio %s, de %s" % (_seguro(m["folio"]), _seguro(m["de"]))
                           for m in msgs)
        return ("[CANAL] Tienes mensaje(s) sin leer:\n%s\n"
                "Léelos con:  python3 %s ver <folio>\n"
                "El cuerpo no viene aquí a propósito: lo escribe otra casa, y metido en tu\n"
                "contexto llegaría en posición de instrucción. Tráelo tú." % (lineas, self.cliente))

    def confirmar(self, folio, de=None):
        if self.observando:
            self.log("confirmaria", folio=folio)
            return True
        cmd = "python3 %s confirmar %s" % (self.cliente, folio) + (" %s" % de if de else "")
        cod, sal = correr(cmd, 60)
        if cod != 0:
            self.log("confirmar_fallo", folio=folio, codigo=cod, salida=sal[:200])
        return cod == 0

    def ciclo(self):
        # La guarda de autoataque ya no vive aquí: necesita saber CONTRA QUIÉN se
        # iba a actuar, y eso solo se sabe después de resolver la casa. Corre
        # dentro de `_entregar`, antes de cualquier invocación.
        msgs = self.pendientes()
        if not msgs:
            return 0
        if not self.candado.tomar():
            self.log("candado_ocupado")
            return 0
        try:
            return self._entregar(msgs)
        finally:
            self.candado.soltar()

    # ── UNA SOLA VÍA, Y ES LA QUE FALLA CUANDO SE EQUIVOCA ───────────────────
    # Antes había dos: entregar a la viva, o —si el enumerador la daba por
    # cerrada— reanudarla. La segunda era el defecto, y no por su guarda sino por
    # su blanco: el único objetivo posible de una reanudación era un transcript
    # abandonado, que se deja resucitar siempre y sale 0 siempre.
    #
    # Queda una vía: el recado a la sesión viva de esta casa, RESUELTA en este
    # mismo ciclo. Y su virtud no es la guarda, es la forma de fallar — si el
    # blanco ya no existe, la entrega se cae y el cursor no se mueve. La
    # reanudación acertaba el código de salida aunque no hubiera nadie leyendo;
    # ésta no puede.
    #
    # Cuando no hay a quién entregar —casa cerrada, casa ambigua, enumerador
    # mudo— no se hace NADA y no se confirma NADA. El folio se queda en la cola.
    # Equivocarse cuesta un aviso que llega tarde; nunca un folio que se perdió
    # constando como entregado.
    # ── EL TIPO DECIDE SI SE DESPIERTA, Y LO DESCONOCIDO NO SE TRAGA ─────────
    # El canal etiqueta cada sobre con un tipo. Hoy casi todo es `mensaje`, pero
    # el diseño del master ya define otro —`propuesta`— cuyo contrato dice que
    # NO la resuelve un agente: la lee un humano. Despertar una sesión sin cabeza
    # para atender una propuesta contradice el rol que la propuesta tiene.
    #
    # Y la regla de fondo, que vale para cualquier tipo que se invente después:
    # UN TIPO QUE NO SÉ ATENDER NO SE DESPIERTA Y NO SE CONFIRMA. Confirmar
    # avanzaría el cursor y el folio desaparecería de la cola sin que nadie lo
    # hubiera visto — invisible, sin error y sin síntoma. Se reporta y se deja.
    #
    # EL CURSOR ES LO DELICADO: avanza por número, así que confirmar un folio
    # ALTO se traga cualquier folio MÁS BAJO que no se haya atendido. Por eso el
    # cursor no pasa nunca por encima del primer folio que no se atendió.
    def _repartir(self, msgs):
        despiertan = set(t.strip() for t in self.cfg["tipos_despiertan"].split(",") if t.strip())
        atiendo, dejo = [], []
        for m in msgs:
            (atiendo if m.get("tipo", "mensaje") in despiertan else dejo).append(m)
        for m in dejo:
            self.log("tipo_no_despierta", folio=m["folio"], tipo=m.get("tipo", "mensaje"),
                     nota="no se confirma; queda en cola para quien sepa atenderlo")
        if dejo:
            tope = min(m["folio"] for m in dejo)
            retenidos = [m for m in atiendo if m["folio"] > tope]
            if retenidos:
                self.log("cursor_retenido", desde=tope,
                         folios=",".join(str(m["folio"]) for m in retenidos),
                         nota="no se avanza por encima de un folio sin atender")
            atiendo = [m for m in atiendo if m["folio"] < tope]
        return atiendo

    def _entregar(self, msgs):
        msgs = self._repartir(msgs)
        if not msgs:
            return 0
        folios = [m["folio"] for m in msgs]
        ultimo = max(folios)
        for f in folios:
            if intentos(self.cuenta, f) >= int(self.cfg["max_intentos"]):
                # El texto viejo decía «nadie lo recoge», que ATRIBUYE AL RECEPTOR
                # un fallo que puede ser del disparador — y con la caché rancia lo
                # era. Ahora dice qué pasó y dónde se deshace.
                self.log("folio_agotado", folio=f, cuenta=self.cuenta,
                         aviso="se agotaron los intentos de ENTREGA; el folio sigue en "
                               "la cola. Para reintentar, borra su línea de `cuenta`")
                return 1
        aviso = self.sobre(msgs)

        quien = self.resolver_casa()
        if quien is False:
            self.log("no_entrego_incontestable", folios=",".join(map(str, folios)),
                     motivo="no se pudo enumerar; no se entrega ni se confirma a ciegas")
            return 1
        if quien is None:
            self.log("no_entrego_casa_sin_sesion", casa=self.casa,
                     folios=",".join(map(str, folios)),
                     motivo="ninguna sesión viva aquí; el folio espera en la cola, NO se confirma")
            return 1
        sesion, nombre = quien
        if not self.guarda_autoataque(sesion):
            return 2

        if self.observando:
            self.log("entregaria_a_viva", sesion=sesion, nombre=nombre,
                     folios=",".join(map(str, folios)))
            return 0
        cmd = self.cfg["cmd_entregar"].format(
            nombre=_seguro(nombre), aviso=aviso, sesion=_seguro(sesion))
        # ── UN INTENTO CONTRA UN BLANCO SIN VERIFICAR NO CUENTA ──────────────
        # HALLAZGO DE SHO (2026-09-01), MEDIDO aquí con control: con la caché
        # vigente 60 s, tres intentos y un tick de 15 s, un /clear dentro de la
        # ventana dejaba la caché sosteniendo una sesión MUERTA el tiempo justo
        # para quemar los tres intentos contra el blanco rancio. Y el agotamiento
        # es PERMANENTE —`olvidar()` solo corre tras un acierto y la comprobación
        # ocurre antes de resolver—, así que el tick siguiente, con la casa VIVA y
        # la caché ya caducada, no llegaba a intentarlo nunca. Medido: casa sana,
        # caché limpia, entrega buena, y el folio varado para siempre.
        #
        # No era el defecto viejo —el cursor no se movía, no se firmaba nada
        # falso— pero el folio se perdía igual. Se cierra por los dos lados: el
        # intento no se cobra si el blanco salió de la caché, y un fallo INVALIDA
        # la caché para que el siguiente tick resuelva de verdad.
        if not self.desde_cache:
            for f in folios:
                intentos(self.cuenta, f, sumar=True)
        cod, sal = correr(cmd, self.tope)
        # ── EL CÓDIGO DE SALIDA NO ES PRUEBA DE ENTREGA ──────────────────────
        # MEDIDO el 2026-09-01, y tira la premisa con la que se justificó todo el
        # rediseño. Se decía: «si el blanco es el equivocado, la entrega FALLA, y
        # por eso esta vía es segura donde la reanudación no lo era». Es FALSO en
        # esta herramienta: entregar a un nombre que no existe termina en CÓDIGO 0.
        # El agente explica en prosa que no envió nada —«No puedo responder OK: el
        # envío no ocurrió»— y el proceso sale bien.
        #
        # O sea que la vía que quedaba tenía el MISMO vicio que la que se retiró:
        # una invocación que acierta el código de salida sin que nadie reciba nada.
        # La reanudación mentía por resucitar un transcript; ésta miente porque el
        # código de salida mide el proceso, no el recado.
        #
        # Por eso el éxito exige un ACUSE POSITIVO, no la ausencia de error: la
        # plantilla ya pedía «después responde solo OK» y nadie lo comprobaba nunca.
        # Un contrato que no se verifica es una decoración.
        #
        # Se compara la ÚLTIMA LÍNEA no vacía, no «contiene»: el texto del fracaso
        # medido contiene la palabra OK dentro de una frase que dice lo contrario.
        acuse = (self.cfg.get("acuse_entrega") or "").strip()
        lineas = [l.strip() for l in sal.splitlines() if l.strip()]
        acusado = (not acuse) or (bool(lineas) and lineas[-1].lower() == acuse.lower())
        if cod != 0 or not acusado:
            try:
                os.remove(self.cache_vivas)
            except OSError:
                pass
            # Registrar SIEMPRE la salida del intento fallido: cuando esto falló en
            # una casa ajena, el único testigo fue un número sin explicación.
            self.log("entrega_fallo", codigo=cod, salida=sal[:400],
                     motivo="código != 0" if cod != 0 else "salió 0 pero NO acusó recibo",
                     cobrado="no" if self.desde_cache else "sí",
                     nota="cursor quieto; caché invalidada; el siguiente tick resuelve")
            return 1
        # EL ACUSE VIAJA EN EL REGISTRO, y no es adorno: hallazgo de Sho en la
        # primera prueba de campo real (2026-09-01). En el camino de ÉXITO no se
        # registraba QUÉ contestó el agente, así que la prueba de que el acuse se
        # evaluó era INDIRECTA —«se escribió entregado_a_viva, y en esta versión eso
        # exige acuse»—. Correcta, pero deducida de la versión del código.
        #
        # Si algún día el acuse se rompiera de una forma que igual dejara pasar,
        # esta línea no lo delataría. Es «una medición viaja con lo que la produjo,
        # o es inauditable», aplicado al camino que sí funciona — que es donde nadie
        # mira.
        self.log("entregado_a_viva", sesion=sesion, folios=",".join(map(str, folios)),
                 acuse=(lineas[-1][:60] if lineas else "(sin salida)"))
        if self.confirmar(ultimo):
            for f in folios:
                olvidar(self.cuenta, f)
        return 0


# ─────────────────────────────────────────────────────────────────────────────
# INSTALADOR — AGENTE DE USUARIO, NUNCA DEMONIO DE SISTEMA
#
# Una casa ajena instaló esto como LaunchDaemon en /Library/LaunchDaemons/. Un
# demonio corre como root, ANTES del login y SIN sesión de usuario: no puede ver
# las sesiones de nadie y choca de frente con el control de acceso a datos de
# macOS. Por eso aquí se instala como agente del usuario y se REHÚSA si corre
# como root — negativa, no advertencia.
#
# Y JAMÁS genera la llave. Puede comprobarla; generarla es de la casa, en su
# máquina, con la palabra de su dueño. Una llave que generó otra instancia no es
# tuya, y la firma sigue verificando igual: fallo silencioso en la identidad.
# ─────────────────────────────────────────────────────────────────────────────

PLANTILLA_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<!--
  Generado por disparador.py {version}. NO editar a mano: se regenera.
  KeepAlive y no StartInterval a propósito — MEDIDO tras 19 dias sin reinicio:
  launchd seguia vivo y los procesos persistentes corrian bien, pero volver a
  disparar un trabajo periodico estaba roto (ni StartInterval ni cron dispararon
  en mas de dos minutos, probado con un trabajo NUEVO). El bucle vive dentro del
  proceso; a launchd solo se le pide lo que si sabe hacer: mantenerlo vivo.
-->
<plist version="1.0">
<dict>
  <key>Label</key><string>{etiqueta}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{python}</string>
    <string>{script}</string>
  </array>
  <key>WorkingDirectory</key><string>{dir_conf}</string>

  <!--
    PATH EXPLICITO, y no es adorno: launchd NO hereda el entorno del shell, asi que
    `claude` a secas no se encuentra. DATO DE CAMPO de la primera instalacion real
    (Sho, 2026-09-01): la enumeracion dio 127 y el disparador quedo mudo. Fallo del
    lado correcto —vivas_incontestable, sin entregar y sin confirmar— pero una casa
    recien instalada no entrega nada hasta que alguien diagnostica un 127.
    Se graba el PATH de quien instala, que es el unico que se sabe bueno en esta maquina.
  -->
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>{ruta_path}</string>
  </dict>
  <key>KeepAlive</key><true/>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>{salida}</string>
  <key>StandardErrorPath</key><string>{salida}</string>
</dict>
</plist>
"""


def _etiqueta(ident):
    return "ai.vuelamind.disparador.%s" % ident


def _ruta_plist(ident):
    return os.path.expanduser("~/Library/LaunchAgents/%s.plist" % _etiqueta(ident))


def _revisar_llave(cfg, log):
    """No genera nada: comprueba. Y se niega, no advierte."""
    llave = os.path.expanduser(cfg.get("llave", "") or "")
    if not llave:
        log("ME_NIEGO_sin_llave", motivo="declara `llave` en la configuración")
        return False
    if not os.path.isfile(llave):
        log("ME_NIEGO_llave_ausente", ruta=llave,
            motivo="la llave se genera en ESTA máquina; el instalador no la crea")
        return False
    st = os.stat(llave)
    if st.st_uid != os.getuid():
        log("ME_NIEGO_llave_ajena", ruta=llave, motivo="no es de este usuario")
        return False
    if st.st_mode & 0o077:
        log("ME_NIEGO_llave_abierta", ruta=llave, modo=oct(st.st_mode & 0o777))
        return False
    if not os.path.isfile(llave + ".pub"):
        log("ME_NIEGO_sin_publica", ruta=llave + ".pub")
        return False
    return True


def instalar(cfg, ruta_conf, log):
    if os.geteuid() == 0:
        log("ME_NIEGO_como_root",
            motivo="agente de usuario, no demonio: un demonio no ve ninguna sesión")
        return 2
    if sys.platform != "darwin":
        log("ME_NIEGO_plataforma", plataforma=sys.platform,
            motivo="esta versión solo instala LaunchAgent; en otro sistema, declara el hueco")
        return 2
    if not _revisar_llave(cfg, log):
        return 2
    if suite(silencio=True) != 0:
        log("ME_NIEGO_conformidad_en_rojo",
            motivo="no se instala lo que no pasa sus propios casos")
        return 2

    ident = Disparador(cfg, log, True).ident
    destino = _ruta_plist(ident)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    def _xml(v):
        return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = PLANTILLA_PLIST.format(
        version=VERSION, etiqueta=_etiqueta(ident), python=_xml(sys.executable),
        script=_xml(os.path.abspath(__file__)),
        dir_conf=_xml(os.path.dirname(os.path.abspath(ruta_conf))),
        ruta_path=_xml(os.environ.get("PATH") or "/usr/local/bin:/usr/bin:/bin"),
        salida=_xml(os.path.expanduser("~/Library/Logs/%s.log" % _etiqueta(ident))))
    with open(destino, "w", encoding="utf-8") as f:
        f.write(texto)
    correr("launchctl bootout gui/%s/%s" % (os.getuid(), _etiqueta(ident)), 30)
    cod, sal = correr("launchctl bootstrap gui/%s %s" % (os.getuid(), destino), 60)
    if cod != 0:
        log("carga_fallo", codigo=cod, salida=sal[:300])
        return 1
    log("instalado", etiqueta=_etiqueta(ident), plist=destino)
    return 0


def desinstalar(cfg, log):
    ident = Disparador(cfg, log, True).ident
    correr("launchctl bootout gui/%s/%s" % (os.getuid(), _etiqueta(ident)), 30)
    destino = _ruta_plist(ident)
    if os.path.exists(destino):
        os.remove(destino)
    log("desinstalado", etiqueta=_etiqueta(ident))
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# LA SUITE VIAJA DENTRO DEL ARTEFACTO
#
# Existe porque su ausencia fue el defecto: el canal se implementó bien en una
# casa ajena porque se podían correr casos y ver pasa/falla; el disparador salió
# mal porque no había NADA que correr — se leía un documento y se confiaba.
#
# Va DENTRO y no al lado para que sea un solo archivo el que se copia: dos
# archivos son dos cosas que pueden divergir. Y varios casos comprueban
# AUSENCIAS —que cierto comando NO se ejecutó—, que es la única forma de probar
# una guarda: una guarda que no se prueba es una intención.
# ─────────────────────────────────────────────────────────────────────────────

_CLIENTE_FALSO = '''#!/usr/bin/env python3
import os, sys
v = sys.argv[1] if len(sys.argv) > 1 else ""
if v == "identidad":
    print(os.environ.get("FALSA_IDENT", "pruebas")); raise SystemExit(0)
if v == "pendientes":
    sys.stdout.write(os.environ.get("FALSOS_PENDIENTES", "")); raise SystemExit(0)
if v == "confirmar":
    open(os.environ["TESTIGO"], "a").write("confirmar %s\\n" % " ".join(sys.argv[2:]))
    raise SystemExit(0)
raise SystemExit(9)
'''

_M1 = {"folio": 7, "de": "otra"}
_M2 = {"folio": 8, "de": "otra"}
_OTRA_CASA = "/tmp/otra-casa-que-no-es-esta"
_CASOS = []


def _caso(nombre, espera):
    def deco(fn):
        _CASOS.append((nombre, espera, fn))
        return fn
    return deco


def _montar(pendientes=(), omitir=(), vivas=None, **extra):
    import tempfile
    d = tempfile.mkdtemp(prefix="conf_disp_")
    with open(os.path.join(d, "cliente.py"), "w", encoding="utf-8") as f:
        f.write(_CLIENTE_FALSO)
    open(os.path.join(d, "testigo"), "w").close()
    # El enumerador falso contesta desde un ARCHIVO, no desde un `echo` con
    # comillas escapadas: el transporte por comillas es una clase de fallo que
    # esta casa ya pagó, y un banco de pruebas no debe apostar contra el shell.
    # Por omisión reporta UNA sesión viva en esta casa, que es el caso sano.
    if vivas is None:
        vivas = [{"sessionId": "SES-A", "cwd": d, "name": "la-casa"}]
    ruta_vivas = os.path.join(d, "vivas.json")
    with open(ruta_vivas, "w", encoding="utf-8") as f:
        json.dump(vivas, f)
    base = {"casa": d, "cliente": os.path.join(d, "cliente.py"),
            "cmd_vivas": "cat %s" % ruta_vivas, "cmd_entregar": "echo OK",
            "intervalo": "1",
            "tope_invocacion": "8", "cache_vivas": "0",
            "bitacora": os.path.join(d, "bitacora.log")}
    base.update(extra)
    with open(os.path.join(d, NOMBRE_CONF), "w", encoding="utf-8") as f:
        for k, v in base.items():
            if k not in omitir:
                f.write("%s %s\n" % (k, v))
    env = dict(os.environ)
    env["FALSOS_PENDIENTES"] = "".join(json.dumps(p) + "\n" for p in pendientes)
    env["TESTIGO"] = os.path.join(d, "testigo")
    env["TMPDIR"] = d
    env["FALSA_IDENT"] = os.path.basename(d)
    env.pop("CLAUDE_SESSION_ID", None)
    return d, env


def _correr(d, env, *args):
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--una-vez"] + list(args),
                       cwd=d, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=180)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def _testigo(d):
    return open(os.path.join(d, "testigo"), encoding="utf-8").read()


@_caso("C1 · sin configuración: se niega y dice desde dónde buscó", "código != 0, nombra el archivo")
def _c1():
    import tempfile
    d = tempfile.mkdtemp(prefix="conf_disp_")
    env = dict(os.environ); env["TMPDIR"] = d
    cod, sal = _correr(d, env)
    return cod != 0 and NOMBRE_CONF in sal


@_caso("C2 · falta una clave obligatoria: la NOMBRA", "código != 0, nombra cmd_vivas")
def _c2():
    d, env = _montar([_M1], omitir=("cmd_vivas",))
    cod, sal = _correr(d, env)
    return cod != 0 and "cmd_vivas" in sal


@_caso("C3 · GUARDA: no se entrega a la sesión desde la que corre", "ME_NIEGO y CERO entregas")
def _c3():
    # La guarda se comprueba ahora contra la sesión RESUELTA, así que el
    # enumerador sí corre — lo que no puede correr es la entrega.
    d, env = _montar([_M1], sesion_propia="SES-A", cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "ME_NIEGO_autoataque" in sal and "NO_DEBIO" not in sal


@_caso("C4 · la guarda lee la variable de entorno de la herramienta", "ME_NIEGO por entorno")
def _c4():
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO")
    env["CLAUDE_SESSION_ID"] = "SES-A"
    cod, sal = _correr(d, env)
    return "ME_NIEGO_autoataque" in sal and "NO_DEBIO" not in sal


@_caso("C5 · cola vacía: no levanta ni un proceso", "cmd_vivas nunca corre")
def _c5():
    d, env = _montar([], cmd_vivas="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return cod == 0 and "NO_DEBIO" not in sal


@_caso("C6 · casa viva y la entrega entra: confirma una sola vez", "entregado · confirmar 8")
def _c6():
    d, env = _montar([_M1, _M2])
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "confirmar 8" in _testigo(d)


@_caso("C7 · la entrega falla: el cursor NO se mueve", "entrega_fallo, cero confirmaciones")
def _c7():
    d, env = _montar([_M1], cmd_entregar="exit 3")
    cod, sal = _correr(d, env)
    return "entrega_fallo" in sal and "confirmar" not in _testigo(d)


@_caso("C8 · el enumerador no contesta: no se entrega a ciegas", "incontestable, cursor quieto")
def _c8():
    d, env = _montar([_M1], cmd_vivas="exit 4", cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return ("no_entrego_incontestable" in sal and "NO_DEBIO" not in sal
            and "confirmar" not in _testigo(d))


@_caso("C9 · el enumerador devuelve basura: incontestable", "ilegible, cero entregas")
def _c9():
    d, env = _montar([_M1], cmd_vivas="echo no-es-json", cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return ("vivas_ilegible" in sal and "NO_DEBIO" not in sal
            and "confirmar" not in _testigo(d))


@_caso("C10 · una `cmd_reanudar` heredada NO se ejecuta, y se avisa de que se ignora",
       "cero reanudaciones y la conf obsoleta se nombra")
def _c10():
    # ESTE CASO CERTIFICABA EL DEFECTO. Decía «ambas señales en CERRADA: un turno
    # por mensaje» y comprobaba que se reanudaba Y se confirmaba — o sea, exigía
    # como correcta la conducta que perdía folios. Sho lo cazó LEYENDO el archivo,
    # con los 24 casos en verde. Un caso que consagra el defecto es peor que no
    # tenerlo: convierte la revisión en una firma.
    #
    # Ahora comprueba lo contrario, y además que una conf vieja no reviva la vía
    # por la puerta de atrás: la clave se ignora y se dice en voz alta.
    d, env = _montar([_M1, _M2], sesion="SES-VIEJA", cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return ("NO_DEBIO" not in sal and "entregado_a_viva" in sal
            and "cmd_reanudar" in sal and "sesion" in sal)


@_caso("C11 · la salida del intento fallido se registra entera", "razón visible, cursor quieto")
def _c11():
    # Cuando esto falló en una casa ajena, el único testigo fue un número sin
    # explicación: lo que no se sabe por qué falló no se sabe si volverá a fallar.
    d, env = _montar([_M1], cmd_entregar="echo 'razon del fallo'; exit 1")
    cod, sal = _correr(d, env)
    return "entrega_fallo" in sal and "razon del fallo" in sal and "confirmar" not in _testigo(d)


@_caso("C12 · invocación colgada: se corta y se registra", "código 124")
def _c12():
    d, env = _montar([_M1], tope_invocacion="3", cmd_entregar="sleep 60")
    cod, sal = _correr(d, env)
    return "entrega_fallo" in sal and "codigo=124" in sal


@_caso("C13 · candado de otro ciclo vivo: se salta el turno", "ocupado, cero entregas")
def _c13():
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO")
    lock = os.path.join(d, "disparador_%s.lock" % os.path.basename(d))
    os.mkdir(lock); pid = str(os.getpid())
    open(os.path.join(lock, "pid"), "w").write(pid)
    open(os.path.join(lock, "sello"), "w").write(sello_de(pid))
    cod, sal = _correr(d, env)
    return "candado_ocupado" in sal and "NO_DEBIO" not in sal


@_caso("C14 · candado huérfano: lo rescata y sigue", "huerfano y entrega ocurre")
def _c14():
    d, env = _montar([_M1])
    lock = os.path.join(d, "disparador_%s.lock" % os.path.basename(d))
    os.mkdir(lock)
    open(os.path.join(lock, "pid"), "w").write("999999")
    open(os.path.join(lock, "sello"), "w").write("un sello que ya no existe")
    cod, sal = _correr(d, env)
    return "candado_huerfano" in sal and "entregado_a_viva" in sal


@_caso("C15 · tope de repetición: para y grita", "folio_agotado")
def _c15():
    d, env = _montar([_M1], cmd_entregar="exit 1", max_intentos="2")
    for _ in range(3):
        cod, sal = _correr(d, env)
    return "folio_agotado" in sal


@_caso("C16 · el sobre lleva folio, JAMÁS el cuerpo", "el cuerpo no aparece")
def _c16():
    # ESTE CASO PASABA POR ACCIDENTE, y se descubrió al rehacerlo (2026-09-01).
    # Comprobaba el texto contra la SALIDA DEL DISPARADOR, y ahí solo aparecía
    # porque el `echo` sin comillas se partía en el shell y el fragmento acababa
    # dentro de un registro de error. O sea: medía un fallo del shell, y si la
    # invocación hubiera funcionado, el caso no habría comprobado nada.
    #
    # Ahora se mide lo único que importa: QUÉ RECIBIÓ LA INVOCACIÓN. El comando
    # escribe el aviso en un archivo y el caso lo lee de ahí.
    d, env = _montar([{"folio": 7, "de": "otra", "cuerpo": "TEXTO-SECRETO"}],
                     cmd_entregar='printf %s "{aviso}" > "$RECADO"')
    env["RECADO"] = os.path.join(d, "recado.txt")
    cod, sal = _correr(d, env)
    recado = open(env["RECADO"], encoding="utf-8").read()
    return "TEXTO-SECRETO" not in recado and "folio 7" in recado


@_caso("C17 · observación: dice qué haría y no invoca ni confirma", "cero efectos")
def _c17():
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env, "--observar")
    return "entregaria_a_viva" in sal and "NO_DEBIO" not in sal and "confirmar" not in _testigo(d)


@_caso("C20 · la caché SOLO positiva protege y nunca produce un falso-cerrada",
       "caché viva vigente + enumerador que ahora dice cerrada ⇒ sigue entregando, no reanuda")
def _c20():
    # HALLAZGO DE SHO (2026-09-01), y es de los buenos: la caché asimétrica es la
    # guarda que impide el fallo que motivó todo el rediseño —un falso «cerrada»
    # que dispara la reanudación contra una sesión viva— y NINGÚN caso la
    # ejercitaba: los 19 corrían con `cache_vivas=0`. Por la doctrina de esta
    # casa, una guarda que no se prueba es una intención.
    #
    # Se comprueba lo que de verdad importa: con caché positiva vigente, aunque
    # el enumerador conteste «aquí no vive nadie», el disparador SIGUE tratando a
    # la casa como viva y entrega. Equivocarse hacia «viva» cuesta una entrega que
    # se cae sola; equivocarse hacia «cerrada» deja el aviso sin salir.
    #
    # Y la caché guarda EL PAR sesión+nombre desde el 2026-09-01: un nombre suelto
    # se puede reemparejar con la sesión equivocada, que es el mismo defecto del
    # puntero congelado en versión pequeña.
    d, env = _montar([_M1], cache_vivas="600", vivas=[])
    cache = os.path.join(d, "disparador_%s.vivas" % os.path.basename(d))
    with open(cache, "w", encoding="utf-8") as f:
        f.write("SES-A\tla-casa")
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "confirmar 7" in _testigo(d)


@_caso("C21 · un tipo que no sé atender NO despierta y NO se confirma",
       "tipo_no_despierta, cero invocaciones, cursor quieto")
def _c21():
    # Confirmar avanzaría el cursor y el folio desaparecería de la cola sin que
    # nadie lo hubiera visto: invisible, sin error y sin síntoma.
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "propuesta"}],
                     cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return ("tipo_no_despierta" in sal and "NO_DEBIO" not in sal
            and "confirmar" not in _testigo(d))


@_caso("C22 · un tipo sin atender RETIENE el cursor de los folios más altos",
       "el mensaje alto no se confirma porque hay una propuesta por debajo")
def _c22():
    # El cursor avanza por número: confirmar el 8 se tragaría el 7. Por eso el
    # cursor no pasa nunca por encima del primer folio que no se atendió.
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "propuesta"},
                      {"folio": 8, "de": "otra", "tipo": "mensaje"}])
    cod, sal = _correr(d, env)
    return ("cursor_retenido" in sal and "confirmar 8" not in _testigo(d)
            and "confirmar 7" not in _testigo(d))


@_caso("C23 · un tipo por debajo del atendido no lo bloquea al revés",
       "la propuesta alta no impide entregar el mensaje bajo")
def _c23():
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "mensaje"},
                      {"folio": 8, "de": "otra", "tipo": "propuesta"}])
    cod, sal = _correr(d, env)
    return ("tipo_no_despierta" in sal and "entregado_a_viva" in sal
            and "confirmar 7" in _testigo(d) and "confirmar 8" not in _testigo(d))


@_caso("C24 · qué tipos despiertan es configurable, no está cableado",
       "añadir propuesta a tipos_despiertan la hace despertar")
def _c24():
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "propuesta"}],
                     tipos_despiertan="mensaje,propuesta")
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "confirmar 7" in _testigo(d)


@_caso("C26 · la casa sin sesión viva: NO entrega y NO confirma",
       "el folio espera en la cola, el cursor no se mueve")
def _c26():
    # EL CASO QUE FALTABA, y el que habría cazado el defecto. Antes, «ninguna
    # sesión viva» se leía como «está cerrada, la reanudo», la reanudación salía 0
    # contra un transcript abandonado y el cursor avanzaba sobre un folio que
    # nadie leyó. Ahora no hay a quién entregar, así que no se hace nada — y no
    # hacer nada deja el folio en la cola, que es el modo de falla correcto.
    d, env = _montar([_M1], vivas=[], cmd_entregar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return ("no_entrego_casa_sin_sesion" in sal and "NO_DEBIO" not in sal
            and "confirmar" not in _testigo(d))


@_caso("C27 · una sesión viva de OTRA casa no es esta casa",
       "no se entrega al vecino aunque sea el único vivo")
def _c27():
    # LA REGRESIÓN DEL DEFECTO DEL 2026-09-01, dicha con precisión: lo que se
    # resuelve es el DIRECTORIO, no un identificador. Aquí el enumerador contesta
    # con una sesión viva —pero de otra casa— y encima con el identificador que
    # una configuración vieja habría tenido congelado. Las dos trampas a la vez:
    # ni el id manda, ni «hay alguien vivo» basta.
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO",
                     vivas=[{"sessionId": "SES-A", "cwd": _OTRA_CASA, "name": "el-vecino"}])
    cod, sal = _correr(d, env)
    return ("no_entrego_casa_sin_sesion" in sal and "NO_DEBIO" not in sal
            and "el-vecino" not in sal and "confirmar" not in _testigo(d))


@_caso("C28 · dos sesiones vivas en la misma casa: ambigua, no se adivina",
       "casa_ambigua, cero entregas, cursor quieto")
def _c28():
    # Elegir una de las dos sería adivinar con cara de dato. Y es un estado real:
    # dos terminales abiertas en el mismo directorio bastan.
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO", vivas=None)
    ruta = os.path.join(d, "vivas.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump([{"sessionId": "SES-A", "cwd": d, "name": "una"},
                   {"sessionId": "SES-B", "cwd": d, "name": "otra"}], f)
    cod, sal = _correr(d, env)
    return ("casa_ambigua" in sal and "NO_DEBIO" not in sal
            and "confirmar" not in _testigo(d))


@_caso("C29 · una caché rancia NO deja varado un folio para siempre",
       "se sana sola en cuanto la casa vuelve: entrega, no folio_agotado")
def _c29():
    # HALLAZGO DE SHO, y vive en la guarda que él mismo pidió. Antes: la caché
    # sostenía una sesión muerta el tiempo justo para quemar los tres intentos, y
    # el agotamiento era PERMANENTE — con la casa ya sana y la caché ya limpia, el
    # folio no volvía a intentarse jamás. Medido entonces con control; éste es el
    # caso que lo impide desde ahora.
    d, env = _montar([_M1], cache_vivas="600",
                     cmd_entregar='test -f "$ROTO" && exit 1; echo ok')
    env["ROTO"] = os.path.join(d, "roto")
    open(env["ROTO"], "w").close()
    cache = os.path.join(d, "disparador_%s.vivas" % os.path.basename(d))
    with open(cache, "w", encoding="utf-8") as f:
        f.write("SES-MUERTA\tla-casa")
    for _ in range(3):                      # se queman los tres ticks contra el rancio
        _correr(d, env)
    os.remove(env["ROTO"])                  # la casa vuelve en sí
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "folio_agotado" not in sal


@_caso("C30 · un enumerador que dejó de reportar `cwd` NO se lee como casa cerrada",
       "vivas_sin_cwd, distinguible de C26, y sin gastar intento")
def _c30():
    # «Un chequeo verde puede significar que no está mirando», en versión roja: si
    # una versión futura de la herramienta deja de dar `cwd`, TODAS las casas
    # quedarían mudas a la vez y el registro culparía a los durmientes.
    d, env = _montar([_M1], cmd_entregar="echo NO_DEBIO",
                     vivas=[{"sessionId": "SES-A", "name": "sin-cwd"}])
    cod, sal = _correr(d, env)
    return ("vivas_sin_cwd" in sal and "no_entrego_casa_sin_sesion" not in sal
            and "NO_DEBIO" not in sal and "confirmar" not in _testigo(d))


@_caso("C31 · un nombre de sesión con metacaracteres NO ejecuta",
       "el shell no ve el intento de fuga")
def _c31():
    # El nombre sale del JSON del enumerador y se interpola en un shell=True.
    # Misma familia que el `echo` sin comillas: ya mordió una vez aquí dentro.
    d, env = _montar([_M1], cmd_entregar='echo "hola {nombre}" > "$RECADO"',
                     vivas=[{"sessionId": "SES-A", "cwd": None, "name": 'x"; touch $FUGA; #'}])
    # el cwd real hay que ponerlo después, que es cuando se conoce
    ruta = os.path.join(d, "vivas.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump([{"sessionId": "SES-A", "cwd": d, "name": 'x"; touch $FUGA; #'}], f)
    env["RECADO"] = os.path.join(d, "recado.txt")
    env["FUGA"] = os.path.join(d, "fuga")
    _correr(d, env)
    return not os.path.exists(env["FUGA"])


@_caso("C32 · salir 0 NO es haber entregado: sin acuse no se confirma",
       "entrega_fallo aunque el código sea 0, y el cursor no se mueve")
def _c32():
    # EL DEFECTO QUE TIRÓ LA PREMISA DE TODO EL REDISEÑO, medido el 2026-09-01.
    # Se había escrito que esta vía era segura porque «si el blanco es el
    # equivocado, FALLA». Es falso: entregar a un nombre que no existe termina en
    # CÓDIGO 0, y el agente explica en prosa que no envió nada. La vía que quedaba
    # tenía el mismo vicio que la retirada.
    #
    # El texto de abajo es el que se midió de verdad, y trae la trampa dentro: la
    # palabra OK aparece EN UNA FRASE QUE DICE LO CONTRARIO. Por eso se compara la
    # última línea y no «contiene» — un `in` habría dado esto por entregado.
    d, env = _montar([_M1],
                     cmd_entregar='echo "No puedo responder OK: el envio no ocurrio."; '
                                  'echo "Dime a cual de los tres lo mando."')
    cod, sal = _correr(d, env)
    return ("entrega_fallo" in sal and "NO acusó recibo" in sal
            and "entregado_a_viva" not in sal and "confirmar" not in _testigo(d))


@_caso("C33 · el acuse tiene que ser el acuse, no parecerse",
       "una última línea que solo CONTIENE el acuse no cuenta")
def _c33():
    d, env = _montar([_M1], cmd_entregar='echo "casi OK pero no"')
    cod, sal = _correr(d, env)
    return "entrega_fallo" in sal and "confirmar" not in _testigo(d)


@_caso("C34 · el plist que genera el instalador declara PATH",
       "launchd no hereda el entorno; sin esto la casa nace muda")
def _c34():
    # DATO DE CAMPO de la primera instalación real, en casa ajena (Sho, 2026-09-01):
    # `claude` a secas dio 127 bajo launchd. Falló del lado correcto —incontestable,
    # sin entregar ni confirmar— pero una casa recién instalada no entrega nada
    # hasta que alguien sabe leer un 127. La plantilla del plist se puede envejecer
    # igual que la de la conf, así que se comprueba, no se recuerda.
    hueco = "{ruta_path}" in PLANTILLA_PLIST and "EnvironmentVariables" in PLANTILLA_PLIST
    render = PLANTILLA_PLIST.format(version="X", etiqueta="e", python="/p", script="/s",
                                    dir_conf="/d", ruta_path="/usr/bin:/bin", salida="/l")
    return hueco and "<key>PATH</key><string>/usr/bin:/bin</string>" in render


@_caso("C35 · el registro de ÉXITO dice QUÉ contestó el agente",
       "la prueba del acuse es directa, no deducida de la versión del código")
def _c35():
    # Hallazgo de Sho en la primera prueba de campo real: la línea de éxito no
    # traía la respuesta, así que había que deducir que el acuse se evaluó a partir
    # de saber qué versión corría. El camino que funciona es justo donde nadie
    # mira, y por eso es donde una regla puede dejar de aplicarse sin síntoma.
    d, env = _montar([_M1], cmd_entregar='echo "ruido antes"; echo OK')
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "acuse=OK" in sal and "confirmar 7" in _testigo(d)


@_caso("C25 · la plantilla está completa y su comando no revienta el shell",
       "trae todas las claves obligatorias y conserva las comillas escapadas")
def _c25():
    # Una plantilla que envejece es el mismo defecto que un documento que
    # envejece: en otro artefacto de esta familia, el paso de instalación mandó
    # editar constantes que el código había dejado de usar diez días antes, y
    # nadie lo notó porque nadie instaló desde cero. Aquí no puede pasar en
    # silencio: si alguien añade una clave obligatoria y no la pone en la
    # plantilla, este caso se cae.
    #
    # Y comprueba lo segundo que rompió al escribirla: Python se comía los
    # escapes de las comillas y el comando llegaba al shell partido en pedazos.
    import tempfile
    d = tempfile.mkdtemp(prefix="conf_disp_")
    ruta = os.path.join(d, NOMBRE_CONF)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(PLANTILLA_CONF)
    cfg = leer_conf(ruta)          # lanza si falta cualquier obligatoria
    faltan = [k for k in OBLIGATORIAS if not cfg.get(k)]
    escapadas = '\\"' in cfg["cmd_entregar"]
    return not faltan and escapadas


@_caso("C19 · el sello del candado no depende del locale del sistema",
       "mismo proceso, misma cadena bajo cualquier locale")
def _c19():
    # NO es adorno: `lstart` devuelve una fecha legible cuyo formato cambia con el
    # locale, y launchd no hereda el entorno del shell. MEDIDO aquí: el mismo
    # proceso da "Tue Sep  1" con LC_ALL=C y "mar.  1 sep" con es_MX.UTF-8. Sin
    # forzarlo, el dueño VIVO del candado se lee como huérfano y se le arrebata
    # el candado — el duplicado exacto que el candado existe para evitar.
    pid = str(os.getpid())
    bajo_c = sello_de(pid)
    guardado = os.environ.get("LC_ALL")
    os.environ["LC_ALL"] = "es_MX.UTF-8"
    try:
        bajo_otro = sello_de(pid)
    finally:
        if guardado is None:
            os.environ.pop("LC_ALL", None)
        else:
            os.environ["LC_ALL"] = guardado
    suelto = subprocess.run(["ps", "-o", "lstart=", "-p", pid],
                            stdout=subprocess.PIPE,
                            env=dict(os.environ, LC_ALL="es_MX.UTF-8")).stdout
    suelto = " ".join(suelto.decode("utf-8", "replace").split())
    # el sello debe ser estable, Y debe diferir de lo que saldría sin forzarlo
    # (si no difiriera, esta prueba no estaría comprobando nada)
    return bool(bajo_c) and bajo_c == bajo_otro and bajo_c != suelto


@_caso("C18 · el instalador se niega si la llave no existe", "ME_NIEGO_llave_ausente")
def _c18():
    d, env = _montar([], llave=os.path.join(d0(), "no-existe"))
    cod, sal = _correr(d, env, "--instalar")
    return "ME_NIEGO_llave_ausente" in sal and cod != 0


def d0():
    import tempfile
    return tempfile.gettempdir()


def suite(silencio=False):
    import shutil, tempfile
    ancho = max(len(n) for n, _, _ in _CASOS)
    fallos = 0
    if not silencio:
        print("== conformidad del disparador — %d casos ==\n" % len(_CASOS))
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
        if p.startswith("conf_disp_"):
            shutil.rmtree(os.path.join(tempfile.gettempdir(), p), ignore_errors=True)
    return 1 if fallos else 0


USO = """disparador.py — el reloj que despierta a una instancia. Un solo archivo.

  (sin argumentos)   corre el bucle: es lo que lanza el servicio
  --una-vez          un solo ciclo y sale
  --observar         dice qué HARÍA sin despertar ni confirmar a nadie
  --plantilla        imprime un .disparador.conf listo para rellenar\n  --conformidad      corre sus propios casos; no toca el canal real
  --instalar         lo carga como agente de usuario (nunca demonio)
  --desinstalar      lo descarga y borra su plist

La configuración es `%s`, formato `clave valor`, buscada desde el directorio de
trabajo hacia arriba — igual que la del canal.""" % NOMBRE_CONF


def main(argv):
    if "--ayuda" in argv or "-h" in argv:
        print(USO); return 0
    if "--conformidad" in argv:
        return suite()
    if "--plantilla" in argv:
        sys.stdout.write(PLANTILLA_CONF)
        return 0

    ruta = buscar_conf()
    if not ruta:
        raise SystemExit(
            "no encontré %s desde %s hacia arriba.\n"
            "Créalo con:  python3 %s --plantilla > %s   y rellena los tres valores marcados."
            % (NOMBRE_CONF, os.getcwd(), os.path.basename(__file__), NOMBRE_CONF))
    cfg = leer_conf(ruta)
    observando = "--observar" in argv
    log = Bitacora(cfg.get("bitacora"), observando)

    if "--instalar" in argv:
        return instalar(cfg, ruta, log)
    if "--desinstalar" in argv:
        return desinstalar(cfg, log)

    # `casa` se registra en cada arranque a propósito: es el valor del que ahora
    # depende toda la entrega, y un valor por omisión que nadie ve es un supuesto.
    # Si apunta al sitio equivocado, esta línea es donde se nota.
    log("arranca", version=VERSION, conf=ruta, casa=cfg["casa"],
        modo="observa" if observando else "vivo")
    d = Disparador(cfg, log, observando)
    if observando or "--una-vez" in argv:
        return d.ciclo()
    # El bucle vive DENTRO del proceso a propósito: MEDIDO tras 19 días sin
    # reinicio, launchd seguía vivo y los procesos persistentes corrían bien,
    # pero volver a disparar un trabajo periódico estaba roto. El rodeo es
    # pedirle solo lo que sí sabe hacer: mantener un proceso vivo.
    intervalo = int(cfg["intervalo"])
    while True:
        try:
            d.ciclo()
        except Exception as e:
            log("ciclo_excepcion", detalle=repr(e)[:300])
        time.sleep(intervalo)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
