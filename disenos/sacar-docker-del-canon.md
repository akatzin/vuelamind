# Sacar `docker/` a su propio proyecto

**Estado: idea, sin decidir. Se abre para no perderla.**

## El hallazgo que la hace viable

`docker/` **ya trata al canon como dependencia externa**. El `Dockerfile` no usa los
archivos de al lado: hace `git clone` desde GitHub, por red.

```
ADD https://api.github.com/repos/akatzin/vuelamind/git/refs/heads/$VUELAMIND_REF
RUN git clone --depth 1 --branch "$VUELAMIND_REF" ...
```

Esa carpeta **vive dentro del repositorio del que se descarga**. Copiada a cualquier otro
sitio funcionaría igual. **El acoplamiento mecánico ya es cero** — que es justo lo que suele
impedir un corte así.

## Qué se gana

**Cadencias distintas dejan de pelearse.** El canon cambia por método; la imagen, por
empaquetado. Hoy cada versión del marco arrastra asuntos de imagen, y al revés.

**Y el canon deja de cargar con lo que no es método**: `Dockerfile`, `compose.yml`, la
evidencia por plataforma. Eso es cómo se despliega, no qué es el marco.

## Qué se arriesga, y esta casa ya lo pagó

**Dos repositorios son dos versiones que se pueden separar.** El precedente está medido: el
`_Marco` del NAS quedó **fuera del linaje** del canon y **declaraba `v3.0` con confianza**.
Compararse contra él fue, durante días, medir dos huérfanas entre sí.

**Y el contenedor es hoy la vía más fácil de adoptar el marco.** Si se va sin que el canon lo
nombre, se vuelve invisible — *un track sin nodo no aparece en ningún censo*.

## Las dos condiciones, si se hace

**Clavar por commit, no por rama.** Hoy `VUELAMIND_REF=main` es un blanco móvil: la imagen
anota `.horneado` *después*, lo cual dice qué hay dentro pero no qué se quiso. Dentro del
mismo repositorio eso se perdona; en dos, es por donde se separan.

**Y que el canon lo nombre**, con su enlace, en el README y en el skill. No por cortesía: es
la única forma de que exista en el censo.

## El disparador

**Cuando la cola de PRs esté vacía.** Mover una carpeta con trabajo en vuelo fabrica
conflictos a cambio de nada — al proponerse esto había catorce PRs abiertos y dos tocaban
`docker/`.

## Qué haría cambiar de opinión

Que alguien necesite construir la imagen **desde el propio repositorio** sin red. Hoy no
puede: el `Dockerfile` clona de GitHub. Si eso cambiara, la carpeta volvería a tener razón
para vivir dentro.
