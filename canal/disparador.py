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

EL LÍMITE DE CLASE DE LA REGLA DE LAS DOS SEÑALES, dicho por su nombre.
La regla es de verdad independiente SOLO en la rama donde sí se intentó entregar:
ahí las dos señales vienen de instrumentos distintos. En la rama contraria —la
sesión se lee cerrada, así que no hay a quién entregarle— la reanudación descansa
en UN SOLO instrumento: el enumerador. Eso baja la probabilidad de equivocarse y
NO cambia la clase: sigue siendo un proxy.

Y el cierre de clase para «reanudar la sesión viva de OTRO» **no vive en este
archivo**: vive en qué hace `cmd_reanudar` contra una sesión viva. Si la
reanudación SE ADJUNTA a la sesión en vez de duplicarla, la exactitud del
enumerador deja de importar y el problema se disuelve; si duplica, ninguna guarda
de aquí alcanza.

**Por eso `cmd_reanudar` DEBE ser idempotente contra una sesión viva**, y quien
configura este disparador tiene que haberlo medido en su herramienta —no supuesto—.
Mientras no esté medido, es un hueco declarado y no una garantía.
(Hallazgo de la casa que probó el artefacto, 2026-09-01.)
"""

import json
import os
import subprocess
import sys
import time

VERSION = "1"
NOMBRE_CONF = ".disparador.conf"


# ─────────────────────────────────────────────────────────────────────────────
# Configuración — mismo formato y misma regla de búsqueda que `.mensajeria.conf`:
# `clave valor` separado por espacios, buscado desde el directorio de trabajo
# hacia arriba, como git con `.git`. NO se inventa un formato nuevo: dos formatos
# de configuración para el mismo mecanismo es el defecto de las dos fuentes.
# ─────────────────────────────────────────────────────────────────────────────

OBLIGATORIAS = ("sesion", "cliente", "cmd_vivas", "cmd_entregar", "cmd_reanudar")

POR_OMISION = {
    "intervalo": "15",
    "tope_invocacion": "90",
    "max_intentos": "3",
    "cache_vivas": "60",
    "rezagados_cada": "600",
    "rezagados_edad": "600",
    "rezagados_max": "3",
    "bitacora": "",
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

# ── RELLENA ESTOS TRES ───────────────────────────────────────────────────────
sesion            PON-AQUI-EL-ID-DE-LA-SESION-A-DESPERTAR
cliente           /ruta/absoluta/al/cliente_del_canal.py
llave             ~/.ssh/id_mensajeria_TU-IDENTIDAD

# ── LO DEMAS YA VIENE ESCRITO PARA CLAUDE CODE ───────────────────────────────
# Son los tres comandos propios de la herramienta. En otra herramienta, estos
# tres son tu hueco: se declaran, no se inventan.
cmd_vivas         claude agents --json
cmd_entregar      claude -p "Usa la herramienta SendMessage para enviar a \"{nombre}\" exactamente este texto y nada mas: \"{aviso}\" Despues responde solo OK."
cmd_reanudar      claude --resume {sesion} -p "{aviso}"

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
            partes = linea.split(None, 1)
            if len(partes) != 2:
                continue
            cfg[partes[0]] = partes[1].strip()
    faltan = [k for k in OBLIGATORIAS if not cfg.get(k)]
    if faltan:
        raise SystemExit("falta(n) en %s: %s" % (ruta, ", ".join(faltan)))
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
        self.sesion = cfg["sesion"]
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
    # Un disparador JAMÁS reanuda la sesión desde la que corre, y se comprueba por
    # IDENTIFICADOR, no por estado. No es una costumbre, es un imposible: no
    # depende de que ninguna fuente diga la verdad. Cubre el caso en que el
    # disparador se ataca a sí mismo; NO cierra el caso general de reanudar la
    # sesión de otro, que sigue dependiendo del estado.
    def guarda_autoataque(self):
        propia = self.cfg.get("sesion_propia") or os.environ.get(
            self.cfg.get("env_sesion_propia") or "", "")
        if propia and propia.strip() == self.sesion.strip():
            self.log("ME_NIEGO_autoataque", sesion=self.sesion)
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

    def nombre_si_viva(self):
        """Consulta la fuente autoritativa. Devuelve el nombre de la sesión si la
        reporta viva, None si la reporta cerrada, y False si NO SE PUDO SABER.
        Tres estados, no dos: 'no pude preguntar' no es 'está cerrada'."""
        # Se cachea SOLO el resultado POSITIVO, y no es pereza: equivocarse hacia
        # "está viva" cuesta un aviso que el siguiente ciclo repite; equivocarse
        # hacia "cerrada" lanza una reanudación contra una sesión viva y fabrica
        # gemelos sin cabeza. Un fallo cuesta un aviso; el otro cuesta la verdad
        # de la bitácora.
        vida = int(self.cfg["cache_vivas"])
        if os.path.exists(self.cache_vivas):
            if time.time() - os.path.getmtime(self.cache_vivas) < vida:
                with open(self.cache_vivas, encoding="utf-8") as f:
                    n = f.read().strip()
                if n:
                    return n
        cod, sal = correr(self.cfg["cmd_vivas"], 60)
        if cod != 0:
            self.log("vivas_incontestable", codigo=cod, salida=sal[:200])
            return False
        try:
            datos = json.loads(sal)
        except ValueError:
            self.log("vivas_ilegible", salida=sal[:200])
            return False
        for a in datos if isinstance(datos, list) else []:
            if str(a.get("sessionId", "")) == self.sesion:
                nombre = a.get("name") or ""
                if nombre:
                    with open(self.cache_vivas, "w", encoding="utf-8") as f:
                        f.write(nombre)
                return nombre or True
        try:
            os.remove(self.cache_vivas)
        except OSError:
            pass
        return None

    # ── EL SOBRE: folio y cómo leerlo, JAMÁS el cuerpo ───────────────────────
    # Frontera de seguridad, no ahorro. El cuerpo lo escribe otra instancia;
    # metido literal en el prompt llega EN POSICIÓN DE INSTRUCCIÓN. Pasando solo
    # el folio, el agente va a buscarlo y llega como dato que fue a traer.
    def sobre(self, msgs):
        lineas = "\n".join("  - folio %s, de %s" % (m["folio"], m["de"]) for m in msgs)
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
        if not self.guarda_autoataque():
            return 2
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

    # ── EL ORDEN INVERTIDO, Y LA REGLA DE LAS DOS SEÑALES ────────────────────
    # Antes se preguntaba el estado y LUEGO se actuaba, lo cual obliga a que la
    # respuesta sea verdad. Una casa ajena midió que no lo es: el enumerador
    # reportó cerrada una sesión activa durante un solo tick. Y "exigir dos
    # lecturas seguidas" baja la probabilidad sin cambiar la clase — sigue siendo
    # un proxy, la misma especie que la fecha del transcript.
    #
    # Aquí se actúa primero con la vía QUE NO PUEDE HACER DAÑO: se intenta
    # entregar el recado a la sesión viva. Si entra, listo — y nunca hizo falta
    # saber el estado.
    #
    # Y para reanudar se exigen DOS SEÑALES INDEPENDIENTES DE ACUERDO: que la
    # entrega haya fallado Y que el enumerador diga que no está viva. Si
    # discrepan —o si no se pudo preguntar— NO se reanuda: se reintenta al
    # siguiente tick. El modo de falla queda invertido: equivocarse cuesta un
    # aviso que llega tarde, nunca un gemelo firmando acuses.
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
                self.log("folio_agotado", folio=f, aviso="nadie lo recoge; revisar a mano")
                return 1
        aviso = self.sobre(msgs)

        nombre = self.nombre_si_viva()
        if nombre not in (None, False):
            cmd = self.cfg["cmd_entregar"].format(
                nombre="" if nombre is True else nombre, aviso=aviso, sesion=self.sesion)
            if self.observando:
                self.log("entregaria_a_viva", folios=",".join(map(str, folios)))
                return 0
            for f in folios:
                intentos(self.cuenta, f, sumar=True)
            cod, sal = correr(cmd, self.tope)
            if cod == 0:
                self.log("entregado_a_viva", folios=",".join(map(str, folios)))
                if self.confirmar(ultimo):
                    for f in folios:
                        olvidar(self.cuenta, f)
                return 0
            # Registrar SIEMPRE la salida del intento fallido.
            self.log("entrega_fallo", codigo=cod, salida=sal[:400])
        else:
            cod = None

        # Segunda señal antes de reanudar.
        estado = self.nombre_si_viva()
        if estado is not False and estado is not None:
            self.log("no_reanudo_discrepan", motivo="la entrega falló pero sigue viva")
            return 1
        if estado is False:
            self.log("no_reanudo_incontestable",
                     motivo="no se pudo saber el estado; no se reanuda a ciegas")
            return 1

        # Ambas señales de acuerdo: cerrada. Un turno por mensaje.
        for m in msgs:
            f, de = m["folio"], m["de"]
            n = intentos(self.cuenta, f, sumar=True)
            if n > int(self.cfg["max_intentos"]):
                self.log("folio_agotado", folio=f)
                return 1
            uno = ("[CANAL] Tienes un mensaje: folio %s, de %s.\n"
                   "Léelo con:  python3 %s ver %s\n"
                   "Si vas a responder:  python3 %s mandar %s \"...\""
                   % (f, de, self.cliente, f, self.cliente, de))
            if self.observando:
                self.log("reanudaria", folio=f)
                continue
            cmd = self.cfg["cmd_reanudar"].format(sesion=self.sesion, aviso=uno, nombre="")
            cod, sal = correr(cmd, self.tope)
            if cod != 0:
                self.log("reanudar_fallo", folio=f, codigo=cod, salida=sal[:400])
                return 1
            self.log("reanudado", folio=f)
            if self.confirmar(f, de):
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
    texto = PLANTILLA_PLIST.format(
        version=VERSION, etiqueta=_etiqueta(ident), python=sys.executable,
        script=os.path.abspath(__file__), dir_conf=os.path.dirname(os.path.abspath(ruta_conf)),
        salida=os.path.expanduser("~/Library/Logs/%s.log" % _etiqueta(ident)))
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
_VIVA = """python3 -c "print('[{\\"sessionId\\": \\"SES-A\\", \\"name\\": \\"la-casa\\"}]')" """
_CASOS = []


def _caso(nombre, espera):
    def deco(fn):
        _CASOS.append((nombre, espera, fn))
        return fn
    return deco


def _montar(pendientes=(), omitir=(), **extra):
    import tempfile
    d = tempfile.mkdtemp(prefix="conf_disp_")
    with open(os.path.join(d, "cliente.py"), "w", encoding="utf-8") as f:
        f.write(_CLIENTE_FALSO)
    open(os.path.join(d, "testigo"), "w").close()
    base = {"sesion": "SES-A", "cliente": os.path.join(d, "cliente.py"),
            "cmd_vivas": "echo '[]'", "cmd_entregar": "echo entregado",
            "cmd_reanudar": "echo reanudado", "intervalo": "1",
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


@_caso("C3 · GUARDA: no reanuda la sesión desde la que corre", "ME_NIEGO y CERO invocaciones")
def _c3():
    d, env = _montar([_M1], sesion_propia="SES-A", cmd_vivas="echo NO_DEBIO",
                     cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "ME_NIEGO_autoataque" in sal and "NO_DEBIO" not in sal


@_caso("C4 · la guarda lee la variable de entorno de la herramienta", "ME_NIEGO por entorno")
def _c4():
    d, env = _montar([_M1]); env["CLAUDE_SESSION_ID"] = "SES-A"
    return "ME_NIEGO_autoataque" in _correr(d, env)[1]


@_caso("C5 · cola vacía: no levanta ni un proceso", "cmd_vivas nunca corre")
def _c5():
    d, env = _montar([], cmd_vivas="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return cod == 0 and "NO_DEBIO" not in sal


@_caso("C6 · viva y la entrega entra: confirma y NUNCA reanuda", "entregado · confirmar 8")
def _c6():
    d, env = _montar([_M1, _M2], cmd_vivas=_VIVA, cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "NO_DEBIO" not in sal and "confirmar 8" in _testigo(d)


@_caso("C7 · entrega falla pero sigue viva: NO reanuda", "señales discrepan")
def _c7():
    d, env = _montar([_M1], cmd_vivas=_VIVA, cmd_entregar="exit 3", cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "no_reanudo_discrepan" in sal and "NO_DEBIO" not in sal


@_caso("C8 · el enumerador no contesta: NO reanuda a ciegas", "incontestable")
def _c8():
    d, env = _montar([_M1], cmd_vivas="exit 4", cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "no_reanudo_incontestable" in sal and "NO_DEBIO" not in sal


@_caso("C9 · el enumerador devuelve basura: incontestable", "ilegible, cero reanudaciones")
def _c9():
    d, env = _montar([_M1], cmd_vivas="echo no-es-json", cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env)
    return "vivas_ilegible" in sal and "NO_DEBIO" not in sal


@_caso("C10 · ambas señales en CERRADA: un turno por mensaje", "dos turnos, dos confirmaciones")
def _c10():
    d, env = _montar([_M1, _M2])
    cod, sal = _correr(d, env); t = _testigo(d)
    return sal.count("reanudado ") == 2 and "confirmar 7" in t and "confirmar 8" in t


@_caso("C11 · si la reanudación falla NO confirma", "registra la salida, cursor quieto")
def _c11():
    d, env = _montar([_M1], cmd_reanudar="echo 'razon del fallo'; exit 1")
    cod, sal = _correr(d, env)
    return "reanudar_fallo" in sal and "razon del fallo" in sal and "confirmar" not in _testigo(d)


@_caso("C12 · invocación colgada: se corta y se registra", "código 124")
def _c12():
    d, env = _montar([_M1], tope_invocacion="3", cmd_reanudar="sleep 60")
    cod, sal = _correr(d, env)
    return "reanudar_fallo" in sal and "codigo=124" in sal


@_caso("C13 · candado de otro ciclo vivo: se salta el turno", "ocupado, cero reanudaciones")
def _c13():
    d, env = _montar([_M1], cmd_reanudar="echo NO_DEBIO")
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
    return "candado_huerfano" in sal and "reanudado" in sal


@_caso("C15 · tope de repetición: para y grita", "folio_agotado")
def _c15():
    d, env = _montar([_M1], cmd_reanudar="exit 1", max_intentos="2")
    for _ in range(3):
        cod, sal = _correr(d, env)
    return "folio_agotado" in sal


@_caso("C16 · el sobre lleva folio, JAMÁS el cuerpo", "el cuerpo no aparece")
def _c16():
    d, env = _montar([{"folio": 7, "de": "otra", "cuerpo": "TEXTO-SECRETO"}],
                     cmd_reanudar="echo AVISO:{aviso}")
    cod, sal = _correr(d, env)
    return "TEXTO-SECRETO" not in sal and "folio 7" in sal


@_caso("C17 · observación: dice qué haría y no invoca ni confirma", "cero efectos")
def _c17():
    d, env = _montar([_M1], cmd_reanudar="echo NO_DEBIO")
    cod, sal = _correr(d, env, "--observar")
    return "reanudaria" in sal and "NO_DEBIO" not in sal and "confirmar" not in _testigo(d)


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
    # el enumerador conteste «cerrada», el disparador SIGUE tratándola como viva
    # y entrega — nunca reanuda. La caché puede costar un aviso; jamás un gemelo.
    d, env = _montar([_M1], cache_vivas="600", cmd_vivas="echo '[]'",
                     cmd_reanudar="echo NO_DEBIO")
    cache = os.path.join(d, "disparador_%s.vivas" % os.path.basename(d))
    with open(cache, "w", encoding="utf-8") as f:
        f.write("la-casa")
    cod, sal = _correr(d, env)
    return "entregado_a_viva" in sal and "NO_DEBIO" not in sal


@_caso("C21 · un tipo que no sé atender NO despierta y NO se confirma",
       "tipo_no_despierta, cero invocaciones, cursor quieto")
def _c21():
    # Confirmar avanzaría el cursor y el folio desaparecería de la cola sin que
    # nadie lo hubiera visto: invisible, sin error y sin síntoma.
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "propuesta"}],
                     cmd_reanudar="echo NO_DEBIO", cmd_entregar="echo NO_DEBIO")
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
    return ("tipo_no_despierta" in sal and "reanudado" in sal
            and "confirmar 7" in _testigo(d) and "confirmar 8" not in _testigo(d))


@_caso("C24 · qué tipos despiertan es configurable, no está cableado",
       "añadir propuesta a tipos_despiertan la hace despertar")
def _c24():
    d, env = _montar([{"folio": 7, "de": "otra", "tipo": "propuesta"}],
                     tipos_despiertan="mensaje,propuesta")
    cod, sal = _correr(d, env)
    return "reanudado" in sal and "confirmar 7" in _testigo(d)


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

    log("arranca", version=VERSION, conf=ruta, modo="observa" if observando else "vivo")
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
