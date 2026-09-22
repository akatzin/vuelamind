#!/bin/bash
# Autentica este contenedor contra Vertex (Model Garden) y lo comprueba EJERCIENDO.
#
# El login por cuenta de Claude (`claude` -> /login) y este son dos caminos
# distintos y excluyentes: si el CLI esta en modo Vertex, la sesion sale por el
# proyecto de GCP y se factura ahi. Aqui solo vive el segundo.
set -u

ADC="${CLOUDSDK_CONFIG:-$HOME/.config/gcloud}/application_default_credentials.json"

command -v gcloud >/dev/null || {
  echo "No hay gcloud en esta imagen."
  echo "Se hornea a peticion, porque son ~1 GB:"
  echo "    docker compose build --build-arg CON_GCLOUD=1"
  echo "  (o CON_GCLOUD: \"1\" en el bloque args: del compose.yml)"
  exit 1
}

falta=""
for k in CLAUDE_CODE_USE_VERTEX ANTHROPIC_VERTEX_PROJECT_ID CLOUD_ML_REGION; do
  [ -n "${!k:-}" ] || falta="$falta $k"
done
if [ -n "$falta" ]; then
  echo "Faltan variables en el entorno del contenedor:$falta"
  echo "Van en el bloque environment: del compose.yml, y el contenedor se recrea"
  echo "para que las tome (docker compose up -d)."
  exit 1
fi

if [ -r "$ADC" ]; then
  echo "Ya hay credencial de aplicacion en $ADC — no vuelvo a pedirla."
  echo "Para rehacerla: rm '$ADC' y corre esto otra vez."
else
  echo "Voy a pedir la credencial de aplicacion. Aqui dentro NO hay navegador,"
  echo "asi que gcloud imprime una URL: la abres en tu maquina, te da un codigo"
  echo "y lo pegas de vuelta."
  echo
  gcloud auth application-default login --no-launch-browser || exit 1
  gcloud auth application-default set-quota-project "$ANTHROPIC_VERTEX_PROJECT_ID" 2>/dev/null \
    || echo "(no pude fijar el quota project; suele no hacer falta)"
fi

# Lo unico que prueba que esto sirve es pedirle un turno al modelo. Que el
# archivo exista, que gcloud diga que hay cuenta activa y que las variables
# esten puestas son tres indicadores, y los tres pueden estar verdes con la
# sesion fallando: ninguno ejerce la funcion.
echo
echo "Comprobando contra el modelo, que es lo unico que lo demuestra..."
salida=$(timeout 120 claude -p "responde solo con la palabra: listo" 2>&1)
codigo=$?
echo "  respuesta: ${salida:-(vacia)}"
if [ $codigo -ne 0 ]; then
  echo
  echo "NO quedo: el CLI salio con codigo $codigo."
  echo "Si se queja de credenciales, revisa que el proyecto tenga aprovisionado"
  echo "el modelo que pide el puente (por omision opus)."
  exit 1
fi
echo
echo "Vertex listo en este contenedor. Proyecto: $ANTHROPIC_VERTEX_PROJECT_ID  region: $CLOUD_ML_REGION"
echo "La credencial vive en el volumen del hogar: sobrevive a apagar y encender."
