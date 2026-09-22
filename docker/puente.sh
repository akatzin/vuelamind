#!/bin/bash
# Levanta el puente de sesiones DENTRO del contenedor y lo saca al espacio de red.
#
# El puente del canon escucha en 127.0.0.1 y eso NO se toca: el loopback esta
# escrito a proposito en su codigo y atarlo a 0.0.0.0 es una decision del dominio,
# no un detalle de empaquetado. Pero el loopback DEL CONTENEDOR no lo alcanza
# `docker -p`: el proxy de Docker conecta a la IP del contenedor, no a su loopback.
#
# Por eso hay dos piezas y se ven las dos: el puente en su loopback, y un relevo
# que escucha en el espacio de red del contenedor y le pasa los bytes tal cual.
# Quien pone el limite de verdad es Docker, publicando el puerto SOLO en el
# loopback de la maquina anfitriona (ver compose.yml).
#
# EL PUERTO NO ES LIBRE, Y ESTO MUERDE:
#   el puente valida `Origin` contra http://127.0.0.1:$PORT — la cadena entera,
#   con puerto. Asi que el puerto que ve el NAVEGADOR tiene que ser el mismo $PORT
#   del puente, o todo POST/DELETE sale 403 «origen no permitido» mientras el GET
#   funciona: la pagina carga y no se puede crear ninguna sesion.
#   De ahi el mapeo:  anfitrion 127.0.0.1:$PORT  ->  contenedor $RELEVO  ->  $PORT.
#   (El chequeo de Host si tolera otro puerto: compara solo el nombre.)
set -u

C=${VUELAMIND_CANON:-/opt/vuelamind}
PUENTE="$C/herramientas/interfaz_agente/session_bridge.py"
PORT=${PORT:-8850}
RELEVO=${VUELAMIND_RELEVO:-8851}
export PORT
export BRIDGE_CWD=${BRIDGE_CWD:-/trabajo}

[ -r "$PUENTE" ] || { echo "No encuentro el puente en $PUENTE — ¿canon horneado incompleto?"; exit 1; }
command -v python3 >/dev/null || { echo "Falta python3 en la imagen; el puente lo necesita (3.10+)."; exit 1; }
command -v socat  >/dev/null || { echo "Falta socat en la imagen; es el relevo al espacio de red."; exit 1; }
command -v claude >/dev/null || { echo "Falta el CLI de claude en la imagen."; exit 1; }

# El directorio de trabajo tiene que ser ESCRIBIBLE por quien corre aqui dentro, y
# se comprueba escribiendo: `test -w` mira permisos, y un montaje puede mentirle.
#
# Sin esto el fallo llega tardisimo y acusa a otro: en Linux con Engine, Docker crea
# el ./trabajo que falta como root, dentro se corre como uid 1000, y todo funciona
# -la pagina, el login, la primera pregunta- hasta que el agente intenta escribir su
# vault. Para entonces la persona ya pago el login y media entrevista. En macOS no
# pasa porque el montaje traduce los dueños, que es justo lo que hace que nadie lo
# vea venir.
if ! ( touch "$BRIDGE_CWD/.escritura-de-prueba" && rm -f "$BRIDGE_CWD/.escritura-de-prueba" ) 2>/dev/null; then
  echo "NO PUEDO ESCRIBIR EN $BRIDGE_CWD — y sin eso ningun dominio puede nacer aqui."
  echo
  echo "  soy:      uid $(id -u), gid $(id -g)"
  echo "  el dueño: uid $(stat -c '%u' "$BRIDGE_CWD" 2>/dev/null || echo '?'), gid $(stat -c '%g' "$BRIDGE_CWD" 2>/dev/null || echo '?')"
  echo
  echo "Pasa en Linux SIEMPRE que la carpeta no existe antes: Docker la crea el, y la"
  echo "crea como root. No es un caso raro — es el primer arranque de un clon nuevo."
  echo
  echo "Hay dos salidas, y la primera NO necesita sudo. En la maquina anfitriona,"
  echo "junto al compose.yml:"
  echo
  echo "    mkdir -p trabajo && docker compose up -d"
  echo
  echo "Basta si tu usuario del anfitrion tiene uid $(id -u). Si no, hace falta la otra:"
  echo
  echo "    sudo chown -R $(id -u):$(id -g) trabajo"
  echo
  echo "Prefiero parar aqui que fallar a media entrevista."
  exit 1
fi

python3 "$PUENTE" &
pid_puente=$!

limpiar(){ kill "$pid_puente" ${pid_relevo:-} 2>/dev/null; }
trap limpiar EXIT INT TERM

# El relevo espera a que haya a quien relevar. Si arranca antes, su primer
# cliente se come un "connection refused" que parece del puente y no lo es:
# un error que acusa a la pieza equivocada cuesta mas caro que el segundo
# que se tarda aqui en esperar.
for _ in $(seq 1 40); do
  curl -fsS -m 2 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
  kill -0 "$pid_puente" 2>/dev/null || { echo "El puente murio durante el arranque."; exit 1; }
  sleep 0.5
done

socat "TCP-LISTEN:$RELEVO,fork,reuseaddr" "TCP:127.0.0.1:$PORT" &
pid_relevo=$!

# Comprobar EJERCIENDO, y por donde entra el trafico de verdad: si se mira el
# proceso o el log, un relevo que no pasa nada se ve igual de sano que uno que si.
listo=""
for _ in $(seq 1 20); do
  if curl -fsS -m 2 "http://127.0.0.1:$RELEVO/health" >/dev/null 2>&1; then listo=si; break; fi
  kill -0 "$pid_puente" 2>/dev/null || { echo "El puente murio durante el arranque."; exit 1; }
  sleep 0.5
done
[ -n "$listo" ] || { echo "El puente no contesta por el relevo (0.0.0.0:$RELEVO) tras 10s — el relevo no esta pasando el trafico."; exit 1; }

echo
echo "  puente arriba — comprobado por el relevo, no por el log."
echo "    dentro:     127.0.0.1:$PORT   (loopback del contenedor, sin token)"
echo "    relevo:     0.0.0.0:$RELEVO    (lo que publica Docker)"
echo "    directorio: $BRIDGE_CWD"
echo
echo "  Publicado como manda compose.yml, en tu maquina se abre:"
echo "    http://127.0.0.1:$PORT"
echo
echo "  Para la entrevista, crea una sesion con directorio $BRIDGE_CWD y di:"
echo "    Inicializa $C/MARCO_Inicial.md"
echo

# Un centinela no puede delatar su propia muerte: si cualquiera de los dos cae,
# este proceso cae con el y el contenedor sale con error. Nada de seguir vivo
# a medias, que es la forma en que una vigilancia deja de vigilar sin avisar.
wait -n "$pid_puente" "$pid_relevo"
codigo=$?
if ! kill -0 "$pid_puente" 2>/dev/null; then
  echo "El puente termino (codigo $codigo); tiro el relevo y salgo."
else
  echo "El relevo termino (codigo $codigo); el puente queda inalcanzable, salgo."
fi
exit "${codigo:-1}"
