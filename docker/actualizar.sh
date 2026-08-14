#!/bin/bash
# Trae el canon fresco y DICE que cambio.
#
# Un canon horneado envejece desde el minuto en que se construye la imagen, y
# sin este comando no habria forma de saberlo desde dentro: el archivo se lee
# igual de convincente estando al dia que estando cuatro meses atras.
set -u
C=${VUELAMIND_CANON:-/opt/vuelamind}

[ -d "$C/.git" ] || { echo "El canon en $C no es un repositorio; esta imagen no puede actualizarlo."; exit 1; }
[ -w "$C" ] || { echo "Sin permiso de escritura en $C. Corre este comando como root: docker exec -u root <contenedor> vuelamind-actualizar"; exit 1; }

antes=$(git -C "$C" rev-parse HEAD)
git -C "$C" fetch --depth 1 origin main --quiet || { echo "No se pudo alcanzar el repositorio."; exit 1; }
despues=$(git -C "$C" rev-parse origin/main)

if [ "$antes" = "$despues" ]; then
  echo "El canon ya esta al dia (${antes:0:12})."
  exit 0
fi

echo "Del ${antes:0:12} al ${despues:0:12}:"
echo
git -C "$C" log --oneline --no-decorate "$antes..$despues" | sed 's/^/  /'
echo
echo "Archivos tocados:"
git -C "$C" diff --name-only "$antes" "$despues" | sed 's/^/  /'
echo

git -C "$C" reset --hard "$despues" --quiet
git -C "$C" log -1 --format='%H %cI' > "$C/.horneado"

# Verificar del lado instalado, no confiar en el codigo de salida del reset.
real=$(git -C "$C" rev-parse HEAD)
[ "$real" = "$despues" ] || { echo "El canon quedo en $real, no en $despues."; exit 1; }
echo "Canon actualizado y verificado: ${real:0:12}"

# Un aviso que cuesta caro descubrir de otra forma.
echo
echo "Ojo: los comandos que ya instalaste en un dominio NO se actualizan solos."
echo "Vuelve a instalarlos desde $C/skills y verifica contra su MD5SUM.txt."
