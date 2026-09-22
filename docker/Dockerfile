# Vuelamind horneado: el metodo ya viene dentro.
#
# Lo que este contenedor resuelve es el primer paso del README —crear la
# carpeta y clonar— para quien prefiere no tener nada instalado en su maquina.
# Lo que NO resuelve es la disciplina: eso sigue siendo del que lo usa.
FROM node:22-slim

ARG VUELAMIND_REF=main

RUN apt-get update && apt-get install -y --no-install-recommends \
      git rsync curl ca-certificates less procps ripgrep \
      python3 socat gnupg \
    && rm -rf /var/lib/apt/lists/*

# gcloud, solo si se pide. Son ~1 GB y nadie que no autentique contra Vertex
# tiene por que cargarlos: el login por cuenta de Claude no lo necesita.
#   docker build --build-arg CON_GCLOUD=1 .
# Hace falta cuando el CLI se autentica por Model Garden: la credencial de
# usuario (ADC) se saca con `gcloud auth application-default login`, y ese
# comando no existe si el SDK no esta dentro.
ARG CON_GCLOUD=0
RUN if [ "$CON_GCLOUD" = "1" ]; then \
      curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
      && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list \
      && apt-get update \
      && apt-get install -y --no-install-recommends google-cloud-cli \
      && rm -rf /var/lib/apt/lists/* \
      && gcloud --version; \
    else \
      echo "sin gcloud (CON_GCLOUD=$CON_GCLOUD)"; \
    fi

RUN npm install -g @anthropic-ai/claude-code

# El canon, horneado. Vive aparte del trabajo y se lee, no se edita:
# el metodo dice que la copia propia se compara contra el canon, no que
# se confundan. /trabajo es del usuario; /opt/vuelamind es del marco.
# ESTO INVALIDA LA CACHE DEL CLON CUANDO EL CANON AVANZA, y sin ello el contenedor
# se queda congelado en el dia que se construyo la primera vez. MEDIDO el 2026-09-22:
# una imagen reconstruida con `--build` seguia trayendo el canon del dia anterior,
# porque la capa del `git clone` no cambia nunca — el Dockerfile no cambia, asi que
# Docker la reusa. El sintoma es el peor de todos: `--build` dice que construyo, la
# imagen es nueva, y el metodo de dentro es viejo.
#
# El truco: descargar la referencia de la rama ANTES de clonar. Si el commit es el
# mismo, este archivo es identico y la capa se reusa; si cambio, se rehace el clone.
ADD https://api.github.com/repos/akatzin/vuelamind/git/refs/heads/$VUELAMIND_REF /tmp/canon-ref.json

RUN git clone --depth 1 --branch "$VUELAMIND_REF" \
      https://github.com/akatzin/vuelamind.git /opt/vuelamind \
    && cd /opt/vuelamind \
    && git log -1 --format='%H %cI' > /opt/vuelamind/.horneado \
    && chmod -R a+rX /opt/vuelamind

# El vault del NAS suele ser 1000:100. La imagen node trae 1000:1000.
RUN usermod -g users node && mkdir -p /home/node/.claude && chown -R node:users /home/node

COPY bienvenida.sh /usr/local/bin/vuelamind-bienvenida
COPY actualizar.sh /usr/local/bin/vuelamind-actualizar
COPY puente.sh /usr/local/bin/vuelamind-puente
COPY vertex.sh /usr/local/bin/vuelamind-vertex
# El `sed` no es paranoia: si estos .sh se descomprimen o se clonan en Windows, viajan
# con CRLF, y un script con CRLF dentro de una imagen Linux falla con «bad interpreter»
# o «no such file or directory» — un error que acusa al archivo que si esta ahi y no
# menciona ni a Windows ni a los saltos de linea. Se normaliza al copiar, una vez.
RUN sed -i 's/\r$//' /usr/local/bin/vuelamind-bienvenida /usr/local/bin/vuelamind-actualizar \
                      /usr/local/bin/vuelamind-puente /usr/local/bin/vuelamind-vertex \
 && chmod 755 /usr/local/bin/vuelamind-bienvenida /usr/local/bin/vuelamind-actualizar \
              /usr/local/bin/vuelamind-puente /usr/local/bin/vuelamind-vertex

USER node
WORKDIR /trabajo
ENV HOME=/home/node \
    VUELAMIND_CANON=/opt/vuelamind

# El puerto del relevo, no el del puente: el puente sigue en su loopback. Es
# documentacion — quien publica decide, y compose.yml lo hace solo al loopback
# de la maquina anfitriona. Publicarlo a secas (-p 8850:8851) lo abre a la red,
# y eso es otra decision (ver session_bridge.README.md).
EXPOSE 8851

# Sin ENTRYPOINT que envuelva: un contenedor que secuestra el comando es un
# contenedor que no se puede depurar. La bienvenida se invoca, no se impone.
CMD ["bash"]
