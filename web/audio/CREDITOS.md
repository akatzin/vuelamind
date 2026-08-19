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

`historia.html` sortea una pieza de cada pool al cargar y **solo descarga la sorteada**.
Se sirven **desde archive.org**, no desde este repositorio: son ~30 MB en total y meterlos
aquí los dejaría en el historial de git para siempre. La página trae **respaldo local**
(`a-wish-to-fulfill.ogg`) para el caso en que el CDN falle.

| Pool | Pista | Álbum | Autor | Licencia | Fuente | Dur. |
|---|---|---|---|---|---|---|
| `intro (arcade)` | *Working time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 80s |
| `intro (arcade)` | *Party time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 140s |
| `intro (arcade)` | *Flirting time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 192s |
| `intro (arcade)` | *Psychedelic time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 224s |
| `intro (arcade)` | *Resting time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 210s |
| `intro (arcade)` | *Coffee time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 82s |
| `intro (arcade)` | *Dramatic time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 196s |
| `intro (arcade)` | *Anxious time* | GAME JAM VOL 1 !!! | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1](https://archive.org/details/LoyaltyFreakMusic-GAMEJAMVOL1) | 320s |
| `historia (deep focus)` | *Once more with you* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 183s |
| `historia (deep focus)` | *One Cool Minute* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 193s |
| `historia (deep focus)` | *Old Key* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 157s |
| `historia (deep focus)` | *Static Shoes* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 233s |
| `historia (deep focus)` | *Waiting TTTT* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 175s |
| `historia (deep focus)` | *Lag* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 269s |
| `historia (deep focus)` | *No Cadillac* | MINIMAL AMBIENT BOUNCE | Loyalty Freak Music | **CC0** | [archive.org/details/MINIMALAMBIENTBOUNCE](https://archive.org/details/MINIMALAMBIENTBOUNCE) | 171s |
| `historia (deep focus)` | *Coexistenz* | TO CHILL AND STAY AWAKE | Loyalty Freak Music | **CC0** | [archive.org/details/LoyaltyFreakMusicTOCHILLANDSTAYAWAKE20170923132621469](https://archive.org/details/LoyaltyFreakMusicTOCHILLANDSTAYAWAKE20170923132621469) | 155s |

### Cómo se comprobaron — MEDIDO 2026-08-19

- La licencia se leyó del campo `licenseurl` de la **API de metadatos** de archive.org,
  no del título de un resultado: las 16 devuelven
  `http://creativecommons.org/publicdomain/zero/1.0/`.
- La procedencia importa tanto como la etiqueta: **las tres son subidas del propio
  artista** (Loyalty Freak Music, autor CC0 conocido), no copias de terceros.
- Cada URL se pidió y se verificó con `file` sobre los primeros 2 KB: las 16 son
  `Ogg data, Vorbis audio, stereo, 44100 Hz`. No se confía en la extensión.
- Las cabeceras traen `access-control-allow-origin: *` y `accept-ranges: bytes`, así que
  el `<audio>` puede transmitirlas y buscar dentro sin descargar todo.

> [!warning] El CDN falla de vez en cuando, y está medido
> Dos de las 16 devolvieron una **página HTML de error** en el primer intento y el archivo
> correcto en el segundo. Por eso la página lleva respaldo local: sin él, una visita de
> cada tantas se quedaría muda sin que nadie se entere.

> [!danger] Buscar «CC0» en archive.org NO basta
> La consulta por género devolvió discos comerciales —Neurosis, Current 93— con etiqueta
> CC0 puesta por quien los subió. **La etiqueta la escribe el que sube, no el titular.**
> Regla de esta casa: la licencia se acepta solo cuando el que sube ES el autor, o cuando
> la obra es verificablemente de dominio público por edad.
