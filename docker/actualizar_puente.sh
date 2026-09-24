#!/bin/bash
# Pone al dia el canon DENTRO del contenedor y reinicia el puente SOLO si hace falta.
#
# EL HUECO QUE CIERRA. `vuelamind-actualizar` refresca el canon horneado, pero el puente
# ya esta corriendo: su `session_bridge.py` lo cargo Python al arrancar y ahi se queda.
# Su `session_bridge.html`, en cambio, se lee del disco EN CADA PETICION.
#
# O sea que actualizar sin reiniciar deja PAGINA NUEVA HABLANDO CON SERVIDOR VIEJO. No
# falla: la pagina carga entera y contesta a todo menos a lo que el servidor viejo no
# sabe, y eso se ve como un 404 raro en una funcion concreta. Peor que romperse.
#
# Es el equivalente en contenedor de `/vuelamind-rc-update`, y comparte su regla:
# reiniciar SOLO si cambio el backend. Un reinicio gratuito tira las sesiones en vuelo.
#
# Uso:  ./actualizar_puente.sh [--seco] [--contenedor <nombre>]
#       --seco        mide y dice que haria, sin tocar nada.
#       --contenedor  cual, si hay varios.
#
# Trabaja con `docker` y no con `docker compose` a proposito: compose se ata al
# DIRECTORIO desde el que se levanto la pila, y esta carpeta viaja con el canon --
# quien la copie a otro sitio no tendria ahi el proyecto. El contenedor, en cambio, se
# encuentra por su imagen desde cualquier parte.
set -u

IMAGEN=vuelamind:horneado
SECO=""; CONT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --seco) SECO=1 ;;
    --contenedor) shift; CONT="${1:-}" ;;
    *) echo "uso: $0 [--seco] [--contenedor <nombre>]" >&2; exit 2 ;;
  esac
  shift
done

command -v docker >/dev/null || { echo "Falta docker."; exit 1; }

if [ -z "$CONT" ]; then
  encontrados=$(docker ps --filter "ancestor=$IMAGEN" --format '{{.Names}}')
  n=$(printf '%s\n' "$encontrados" | grep -c . )
  if [ "$n" -eq 0 ]; then
    echo "No hay ningun contenedor corriendo con la imagen $IMAGEN."
    echo "Levantalo donde viva tu compose.yml:  docker compose up -d"
    exit 1
  fi
  if [ "$n" -gt 1 ]; then
    echo "Hay $n contenedores con esa imagen; di cual con --contenedor:"
    printf '%s\n' "$encontrados" | sed 's/^/  /'
    exit 1
  fi
  CONT="$encontrados"
fi

docker inspect -f '{{.State.Running}}' "$CONT" 2>/dev/null | grep -qx true || {
  echo "El contenedor '$CONT' no esta corriendo."; exit 1; }

# La huella se toma del archivo que el puente USA, no del que el repositorio tiene:
# son el mismo hasta que alguien monta algo encima, y entonces dejan de serlo callando.
DENTRO=/opt/vuelamind/herramientas/interfaz_agente
huella() { docker exec "$CONT" sh -c "md5sum $DENTRO/session_bridge.py 2>/dev/null | cut -d' ' -f1"; }

echo "  contenedor:    $CONT"
antes=$(huella)
[ -n "$antes" ] || { echo "No pude leer el puente dentro del contenedor."; exit 1; }
echo "  puente ahora:  ${antes:0:12}"

if [ -n "$SECO" ]; then
  echo
  echo "  (seco) no se toco nada. Esto es lo que se haria:"
  echo "    1. vuelamind-actualizar dentro de $CONT, como root"
  echo "    2. volver a medir la huella del puente"
  echo "    3. reiniciar el contenedor SOLO si cambio"
  echo "    4. esperar a que /health conteste, ejerciendolo"
  exit 0
fi

echo
# Como root: el canon es de root y el contenedor corre como `node`.
docker exec -u root "$CONT" vuelamind-actualizar || {
  echo "La actualizacion del canon fallo; no se reinicia nada."; exit 1; }

despues=$(huella)
echo
echo "  puente despues: ${despues:0:12}"

if [ "$antes" = "$despues" ]; then
  echo
  echo "El backend NO cambio: no se reinicia, y las sesiones en vuelo siguen vivas."
  echo "La pagina si pudo cambiar -se lee en cada peticion-, asi que recarga el navegador."
  exit 0
fi

echo
echo "El backend cambio. Reiniciando $CONT (las sesiones en vuelo se pierden)..."
docker restart "$CONT" >/dev/null || { echo "El reinicio fallo."; exit 1; }

# Se comprueba EJERCIENDO /health, no leyendo el codigo de salida del restart: un
# contenedor arriba y un puente que no contesta se ven igual desde fuera.
PUERTO=$(docker port "$CONT" 8851 2>/dev/null | head -1 | sed 's/.*://')
PUERTO=${PUERTO:-8850}
for _ in $(seq 1 20); do
  if curl -fsS -m 2 "http://127.0.0.1:$PUERTO/health" >/dev/null 2>&1; then
    echo "Listo: el puente contesta en http://127.0.0.1:$PUERTO/  (${despues:0:12})"
    # `vuelamind-actualizar` avisa de que los comandos ya instalados NO se actualizan
    # solos, y ahi deja el hueco. Aqui se MIDE, que es lo unico que convierte ese aviso
    # en algo accionable: o nombra los que derivaron, o calla.
    echo
    docker exec "$CONT" python3 /opt/vuelamind/herramientas/comprobar_skills.py 2>/dev/null \
      || echo "(no se pudo comprobar la deriva de los comandos instalados)"
    exit 0
  fi
  sleep 1
done
echo "Reinicio hecho pero /health no contesta en 20 s. Mira:  docker logs $CONT"
exit 1
