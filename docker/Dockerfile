# Vuelamind horneado: el metodo ya viene dentro.
#
# Lo que este contenedor resuelve es el primer paso del README —crear la
# carpeta y clonar— para quien prefiere no tener nada instalado en su maquina.
# Lo que NO resuelve es la disciplina: eso sigue siendo del que lo usa.
FROM node:22-slim

ARG VUELAMIND_REF=main

RUN apt-get update && apt-get install -y --no-install-recommends \
      git rsync curl ca-certificates less procps ripgrep \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

# El canon, horneado. Vive aparte del trabajo y se lee, no se edita:
# el metodo dice que la copia propia se compara contra el canon, no que
# se confundan. /trabajo es del usuario; /opt/vuelamind es del marco.
RUN git clone --depth 1 --branch "$VUELAMIND_REF" \
      https://github.com/akatzin/vuelamind.git /opt/vuelamind \
    && cd /opt/vuelamind \
    && git log -1 --format='%H %cI' > /opt/vuelamind/.horneado \
    && chmod -R a+rX /opt/vuelamind

# El vault del NAS suele ser 1000:100. La imagen node trae 1000:1000.
RUN usermod -g users node && mkdir -p /home/node/.claude && chown -R node:users /home/node

COPY bienvenida.sh /usr/local/bin/vuelamind-bienvenida
COPY actualizar.sh /usr/local/bin/vuelamind-actualizar
RUN chmod 755 /usr/local/bin/vuelamind-bienvenida /usr/local/bin/vuelamind-actualizar

USER node
WORKDIR /trabajo
ENV HOME=/home/node \
    VUELAMIND_CANON=/opt/vuelamind

# Sin ENTRYPOINT que envuelva: un contenedor que secuestra el comando es un
# contenedor que no se puede depurar. La bienvenida se invoca, no se impone.
CMD ["bash"]
