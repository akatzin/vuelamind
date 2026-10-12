#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# EJEMPLO DECLARADO — NO ES PARTE DEL ARTEFACTO, Y PUEDE QUE NO LO NECESITES.
#
#   aportado por  ZeroPani · 2026-09-02
#   medido contra Claude Code 2.1.248, macOS
#
# CUANDO **NO** USARLO, y va primero a proposito: si tu herramienta descubre las
# sesiones LOCALMENTE —si el nombre que lista `cmd_vivas` es un nombre con el que
# puedes hablar—, el `cmd_entregar` de la plantilla te sirve tal cual y esto te
# sobra. Copiarlo entonces te mete un `--bg` que no hace falta.
#
# Un ejemplo que se copia por si acaso es un ejemplo que empeora las cosas.
#
# ── POR QUE EXISTE ───────────────────────────────────────────────────────────
# Donde el unico descubrimiento es DE CUENTA y no local, hay DOS defectos
# independientes y hacen falta los dos arreglos:
#
#   · `claude -p` NUNCA se engancha a Remote Control. Medido dandole 12 s antes
#     de preguntar: sigue viendo 0 pares. Solo `--bg` conecta, y el propio CLI lo
#     dice al rechazar `--bg -p`: «--print nunca arranca la sesion a la que
#     claude agents se engancha». `--remote-control` solo arranca sesiones
#     interactivas, asi que no hay bandera que salve al `-p`.
#   · El nombre que reporta el enumerador NO es el nombre alcanzable. Eso lo
#     cubre `nombre_entrega` en la conf — pero **`nombre_entrega` arregla el
#     NOMBRE, no el TRANSPORTE**. Rellenar la plantilla al pie de la letra y
#     poner `nombre_entrega` te deja creyendo que hiciste lo que hacia falta.
#
# ── TRES COSAS QUE PARECEN DETALLE Y NO LO SON ───────────────────────────────
#   1. El acuse va por ARCHIVO CENTINELA, no por la salida. `--bg` devuelve su
#      banner al instante y no la respuesta del agente, asi que leer su stdout
#      daria por entregado lo que solo se LANZO. La guarda del acuse del
#      disparador lo rechazaria, con razon.
#   2. El agente se PARA al terminar. Sin eso queda vivo y ocioso, y en la vuelta
#      siguiente el disparador ve dos sesiones en la misma casa y se niega a
#      elegir — `casa_ambigua`, y con razon. Medido: se degrada solo con cada
#      entrega hasta quedar ambiguo para siempre.
#   3. DESTINO no trae valor por omision, a proposito. Un ejemplo con un nombre
#      dentro se copia con ese nombre puesto.
#
# ── USO ──────────────────────────────────────────────────────────────────────
#   DESTINO=<nombre-alcanzable> entregar-claude-code.sh "<aviso>"
#
#   y en el .disparador.conf:
#   cmd_entregar   DESTINO=<nombre> /ruta/a/entregar-claude-code.sh "{aviso}"
# ─────────────────────────────────────────────────────────────────────────────

set -u
DESTINO="${DESTINO:?declara DESTINO con el nombre ALCANZABLE de esta casa}"
AVISO="${1:?falta el aviso}"
TOPE="${TOPE:-70}"

SENAL="$(mktemp -t entrega)"; rm -f "$SENAL"

SALIDA="$(claude --bg -n entrega-canal "Llama a SendMessage con to=\"$DESTINO\" y message=\"$AVISO\". Si el envio fue exitoso, escribe exactamente OK en el archivo $SENAL usando Bash. Si fallo, escribe en ese archivo el error verbatim. No hagas nada mas." 2>&1)"
SID="$(printf '%s\n' "$SALIDA" | grep -oE 'backgrounded · [0-9a-f]+' | awk '{print $3}')"

t=0; while [ $t -lt "$TOPE" ]; do [ -s "$SENAL" ] && break; sleep 1; t=$((t+1)); done

[ -n "${SID:-}" ] && claude stop "$SID" >/dev/null 2>&1

[ -s "$SENAL" ] || { echo "sin confirmacion tras ${TOPE}s — NO se entrego"; exit 1; }
CONT="$(tr -d '[:space:]' < "$SENAL")"; rm -f "$SENAL"
[ "$CONT" = "OK" ] && { echo "OK"; exit 0; }
echo "fallo: $CONT"; exit 1
