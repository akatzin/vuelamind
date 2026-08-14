#!/bin/bash
# Lo que ve quien abre este contenedor por primera vez.
# Dice lo que hay, lo que falta y lo que NO puede hacer desde aqui.
set -u
C=${VUELAMIND_CANON:-/opt/vuelamind}
c(){ printf '\033[36m%s\033[0m' "$1"; }
d(){ printf '\033[2m%s\033[0m' "$1"; }

echo
c "  vuelamind"; echo " — el metodo viene horneado en esta imagen."
echo

if [ -r "$C/.horneado" ]; then
  read -r sha fecha < "$C/.horneado"
  printf '  canon:   %s  %s\n' "$C" "$(d "(${sha:0:12} · ${fecha})")"
else
  printf '  canon:   %s  %s\n' "$C" "$(d '(sin sello de horneado)')"
fi

n=$(ls "$C/skills"/*.md 2>/dev/null | wc -l)
printf '  metodo:  MARCO_Inicial.md  ·  %s archivos en skills/\n' "$n"

# El vault no se supone: se mide. Una carpeta vacia y una a medio llegar
# mandan cosas distintas, y el marco entero depende de distinguirlas.
if [ -d /trabajo ]; then
  archivos=$(find /trabajo -type f -not -path '*/.git/*' 2>/dev/null | wc -l)
  if [ "$archivos" -eq 0 ]; then
    printf '  trabajo: /trabajo  %s\n' "$(d '(vacio — un dominio nace aqui)')"
  else
    printf '  trabajo: /trabajo  %s\n' "$(d "($archivos archivos — ya hay algo dentro)")"
  fi
fi
echo

echo "  Para empezar:"
echo
printf '    %s\n' "$(c 'claude')"
printf '    %s\n' "$(d "y dile: «Inicializa $C/MARCO_Inicial.md»")"
echo
printf '  %s\n' "$(d 'No hace falta pegar nada: el archivo ya esta en disco.')"
echo
printf '  %s\n' "$(d 'La segunda pregunta decide todo lo que sigue: si el dominio nace')"
printf '  %s\n' "$(d 'aqui, o si esta maquina se suma a uno que ya vive.')"
echo
printf '  %s\n' "$(d 'El canon horneado no se actualiza solo: vuelamind-actualizar lo trae')"
printf '  %s\n' "$(d 'fresco del repositorio y te dice que cambio.')"
echo
