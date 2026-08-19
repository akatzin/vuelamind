# Créditos de audio — `web/audio/`

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

## Los dos fondos sorteados (2026-08-19)

`historia.html` sortea una pieza de cada pool al cargar, **baja las dos enteras** con una
pantalla de progreso, y solo entonces abre el juego. Viven **en este repositorio**
(`web/audio/pistas/`, 15.03 MB en 16 archivos) — ver abajo por qué no se sirven del CDN.

Todas se re-encodearon a **mono, calidad Vorbis 0** (`sox -C 0 -c 1`): a la mitad del peso
y sin pérdida audible en música de fondo.

| Pool | Archivo | Pista | Álbum | Licencia | Fuente | Dur. | Peso |
|---|---|---|---|---|---|---|---|
| intro · arcade | `pistas/working-time.ogg` | *Working time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 80s | 0.38 MB |
| intro · arcade | `pistas/party-time.ogg` | *Party time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 140s | 0.86 MB |
| intro · arcade | `pistas/flirting-time.ogg` | *Flirting time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 192s | 1.07 MB |
| intro · arcade | `pistas/psychedelic-time.ogg` | *Psychedelic time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 224s | 0.79 MB |
| intro · arcade | `pistas/resting-time.ogg` | *Resting time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 210s | 1.11 MB |
| intro · arcade | `pistas/coffee-time.ogg` | *Coffee time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 82s | 0.33 MB |
| intro · arcade | `pistas/dramatic-time.ogg` | *Dramatic time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 196s | 0.96 MB |
| intro · arcade | `pistas/anxious-time.ogg` | *Anxious time* | GAME JAM VOL 1 !!! | **CC0** | [LoyaltyFreakMusic-GAMEJAMV](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 320s | 1.21 MB |
| historia · deep focus | `pistas/once-more-with-you.ogg` | *Once more with you* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 183s | 1.04 MB |
| historia · deep focus | `pistas/one-cool-minute.ogg` | *One Cool Minute* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 193s | 0.99 MB |
| historia · deep focus | `pistas/old-key.ogg` | *Old Key* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 157s | 0.92 MB |
| historia · deep focus | `pistas/static-shoes.ogg` | *Static Shoes* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 233s | 1.25 MB |
| historia · deep focus | `pistas/waiting-tttt.ogg` | *Waiting TTTT* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 175s | 1.02 MB |
| historia · deep focus | `pistas/lag.ogg` | *Lag* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 269s | 1.49 MB |
| historia · deep focus | `pistas/no-cadillac.ogg` | *No Cadillac* | MINIMAL AMBIENT BOUNCE | **CC0** | [MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 171s | 0.73 MB |
| historia · deep focus | `pistas/coexistenz.ogg` | *Coexistenz* | TO CHILL AND STAY AWAKE | **CC0** | [LoyaltyFreakMusicTOCHILLAN](https://archive.org/details/LoyaltyFreakMusicTOCHILLANDSTAYAWAKE20170923132621469) | 155s | 0.89 MB |

### Cómo se comprobaron — MEDIDO 2026-08-19

- La licencia se leyó del campo `licenseurl` de la **API de metadatos** de archive.org: las
  16 devuelven `http://creativecommons.org/publicdomain/zero/1.0/`.
- La procedencia importa tanto como la etiqueta: **las tres son subidas del propio artista**
  (Loyalty Freak Music, autor CC0 conocido), no copias de terceros.
- Cada archivo verificado con `file` tras convertir: las 16 son `Ogg data, Vorbis audio`.

> [!danger] Por qué NO se sirven desde archive.org — se intentó y falló
> Parecía la opción correcta: enlaces directos, sin peso en el repo, y un `curl -I` mostraba
> `access-control-allow-origin: *`. **Esa comprobación era falsa.** `curl` sigue la
> redirección y no aplica CORS; el navegador sí. Medido:
>
> - `archive.org/download/…` **redirige** a un nodo por petición (`dn601301.us.archive.org`).
> - **El nodo final NO manda cabeceras CORS** → `fetch()` se cuelga y la precarga cae al
>   respaldo. Síntoma en la página: «siempre suena la misma canción».
> - Ese nodo devolvió **HTTP 502** en pruebas directas, y la cadena tarda **~7 s**.
> - Bajando las 16 para convertirlas, **una falló 8 intentos seguidos**.
>
> Regla: **un asset de terceros se comprueba desde el navegador, no desde `curl`** — son
> dos clientes con reglas distintas, y el que importa es el del visitante. Mismo origen
> elimina el problema entero.

> [!danger] Buscar «CC0» en archive.org NO basta
> La consulta por género devolvió discos comerciales —Neurosis, Current 93— con etiqueta
> CC0 puesta por quien los subió. **La etiqueta la escribe el que sube, no el titular.**
> Solo se acepta cuando el que sube ES el autor, o la obra es de dominio público por edad.
