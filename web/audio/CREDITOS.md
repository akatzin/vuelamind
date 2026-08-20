# Créditos de recursos — `web/`

Assets de terceros usados en el sitio público. Ninguno exige atribución por su
licencia; se cita de todos modos, como práctica de esta casa.

| Archivo | Pista | Autor | Licencia | Fuente | Medido |
|---|---|---|---|---|---|
| `a-wish-to-fulfill.ogg` | *A Wish to Fulfill* | Centurion_of_war | **CC0** (Dominio público) | [opengameart.org/content/a-wish-to-fulfill](https://opengameart.org/content/a-wish-to-fulfill) | 2026-08-19 — licencia leída en la página del recurso; archivo verificado por `file`: Ogg Vorbis genuino, 64s, 3.6 MB |

## Cómo se comprobó

`file` confirmó que la cabecera del `.ogg` descargado coincide con lo que la página de
origen declara (Ogg Vorbis, estéreo, 44100 Hz) — no se confía en la extensión del nombre.
La licencia se leyó del campo `License(s):` de la página del recurso, no del título de un
resultado de búsqueda.

## Regla para sumar la siguiente

Un renglón por archivo, con la licencia leída de la página del recurso (no del buscador),
la fuente citada, y el archivo verificado por `file` antes de commitear. Si la licencia
exige atribución (CC-BY, CC-BY-SA), la fila lo dice explícito y la atribución también va
en la página que lo usa, no solo aquí.

## Los dos fondos sorteados — el motor está, las piezas no todavía

`historia.html` sortea una pieza de cada pool al cargar, **baja las dos enteras** con una
pantalla de progreso, y solo entonces abre el juego. Hoy los dos pools traen una sola
pieza: la que ya vive aquí.

**Las 16 piezas CC0 que llenan los pools viajan en su propio PR.** Son ~15 MB de binarios,
y lo que entra al historial de git no sale: no se suben hasta que estén decididas.

### Lo que se aprendió consiguiéndolas — MEDIDO 2026-08-19

> [!danger] Un asset de terceros se comprueba desde el NAVEGADOR, no desde `curl`
> Parecía correcto servirlas desde archive.org: enlaces directos, cero peso en el repo, y
> un `curl -I` mostraba `access-control-allow-origin: *`. **Esa comprobación era falsa.**
> `curl` sigue la redirección y no aplica CORS; el navegador sí. Medido:
>
> - `archive.org/download/…` **redirige** a un nodo por petición (`dn601301.us.archive.org`).
> - **El nodo final NO manda cabeceras CORS** → `fetch()` se cuelga y la precarga cae al
>   respaldo. Síntoma en la página: «siempre suena la misma canción».
> - Ese nodo devolvió **HTTP 502** en pruebas directas, y la cadena tarda **~7 s**.
>
> Son dos clientes con reglas distintas, y el que importa es el del visitante. Mismo
> origen elimina el problema entero.

> [!danger] Buscar «CC0» en archive.org NO basta
> La consulta por género devolvió discos comerciales —Neurosis, Current 93— con etiqueta
> CC0 puesta por quien los subió. **La etiqueta la escribe el que sube, no el titular.**
> Solo se acepta cuando el que sube ES el autor, o la obra es de dominio público por edad.

## La ilustración del héroe (`historia.html`) — 2026-08-19

La criatura del encabezado es **generada con Gemini a partir de un prompt de
Akatzin**, y vive en la página como **trazo vectorial**, no como imagen.

| Qué | Cómo |
|---|---|
| Origen | Imagen generada por Gemini · prompt de Akatzin · fuente en `borradores/mass2.png` |
| En la página | SVG trazado del PNG: dos capas (`cuerpo`, `pliegues`), **71.6 KB** contra 711 KB del original |
| Herramienta | Trazador propio en Python + PIL — marching squares sobre la reja de píxeles y Douglas-Peucker. No hay `potrace` ni `vtracer` en esta máquina |
| Los ojos | **No están en la ilustración.** Se siembran por código sobre 121 sitios medidos del cuerpo —puntos donde un ojo cabe entero dentro de la masa— y renacen cada 7 s |
| La carita | **Dibujada a mano en SVG**: un círculo, dos elipses y un arco. No es imagen |

### Dos cosas que se decidieron a propósito

**La insignia de procedencia se quitó del trazo, y por eso queda escrita aquí.**
Es distinto de una marca de licencia: la imagen la generó Akatzin con su propio
prompt y puede usarla. Pero que la obra sea generada por IA es un hecho del
recurso, y en esta casa los hechos de un recurso viven en su registro, no en una
esquina de la imagen.

**Un smiley de stock se descartó.** Llegó un PNG de *pngtree* con sus marcas de
agua repetidas: activo con licencia ajena, y quitarle la marca es justo lo que la
marca impide. No hacía falta — la carita ya estaba dibujada en SVG, que además
sale geométricamente perfecta y pesa unos bytes.
