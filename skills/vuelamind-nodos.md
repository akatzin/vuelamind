---
description: Dibuja la red de pendientes de un dominio —quién bloquea a quién, por área y severidad— creciendo en el tiempo, como una página HTML de un solo archivo. Contesta qué folios son nudos, que es lo que una lista no puede
---

# /vuelamind-nodos — la cola como red, y creciendo

Una cola de pendientes se lee como lista y **se comporta como red**. La lista contesta *qué
falta*; no contesta **qué folios son nudos de los que cuelgan otros**, que es lo que decide
por dónde empezar.

> [!note] De dónde viene, y cómo llegó
> **Aportación de Zero (Liverpool), 2026-09-02**, destilada de una construcción real en su
> dominio y entregada como aportación, no como parche aplicado. Ahí destapó que **un solo
> folio bloqueaba a siete** — y ese folio representaba una cifra que el censo contaba como
> uno. Esta casa lo publicó con la palabra de Akatzin, parametrizando lo que allá eran
> literales y añadiendo lo que midió al comprobarlo contra otro vault.

**Salida:** un HTML de un solo archivo, autocontenido. Solo la animación y su botón de
repetir — sin encabezados, tablas ni pie.

---

## 1 · Los datos se DERIVAN del vault, y nada se inventa

**El manifiesto del dominio dice cómo se llaman sus notas.** No supongas `Pendientes.md`:
léelo de ahí, y usa la cola y el archivo de cerrados que declare.

Un nodo por folio. Cuatro cosas por nodo, y **las cuatro pueden faltar** — lo que falta se
reporta, no se rellena:

| Dato | De dónde | Si falta |
|---|---|---|
| **folio y título** | el encabezado del folio | sin folio no hay nodo |
| **fecha de aparición** | lo que el folio DECLARA **EN PROSA**, dentro del cuerpo: «Abierto el / Encontrado el / Se abrió el AAAA-MM-DD». **No es un campo `::`** — en el dominio de origen `abierto::` no existe, y quien busque un campo declarado encuentra cero | **ver abajo: es el que más falta** |
| **severidad** | campo de severidad del dominio | nodo sin color de estado, y se dice |
| **área** | primer enlace del campo de área; si no hay enlace, el texto antes del primer separador | nodo sin ancla, al centro |

Dos tipos de arista, y **no son la misma cosa**:

- **bloquea** — del campo de bloqueo. Es **DIRIGIDA**.
- **se citan** — folios que se mencionan entre sí en el cuerpo. **No dirigida.**

**Cuenta y cuadra antes de dibujar nada.** Reporta los conteos que salgan.

> [!danger] LA FECHA DEL SISTEMA DE ARCHIVOS MIENTE. No la uses jamás
> Cada guardado atómico reinicia el nacimiento del archivo, así que **la nota que existe
> desde el primer día del dominio figura como creada hoy** — medido por Zero sobre su propia
> cola. La única fecha buena es **la que el folio declara en su texto**.
>
> *Este aviso llegó a decir «falsa en el 75% de las notas». **Ese número no se pudo
> reproducir**: remedido por su propio autor sobre 80 notas dio **58%**, y como cota
> inferior. Se quita en vez de corregirse — el mecanismo es la razón de la prohibición, y
> **un dato preciso y falso hace más daño que uno ausente**.*

> [!warning] Y comprueba cuántos folios la declaran ANTES de prometer una animación
> **MEDIDO en un segundo dominio (vuelamind-watcher, 2026-09-03): 3 de 27.** Con eso **no
> hay línea de tiempo**, y ése es el corazón de la idea. No la inventes ni la deduzcas: si
> faltan fechas, **dilo y dibuja el estado asentado**. Una animación con fechas supuestas es
> una crónica falsa que se ve preciosa.
>
> Lo mismo con el resto de la forma: en ese dominio los campos coinciden pero **el archivo
> de cerrados usa otro formato de encabezado** y el patrón de corte no encuentra nada.
> **Parametriza el patrón; no lo cablees.** Y con pocas dependencias reales —allí 6 de 21
> campos tenían contenido— la red sale casi toda de puntos sueltos: eso es un hallazgo
> **sobre ese dominio**, no un fallo del dibujo, y conviene decirlo en vez de disimularlo.

---

### La compuerta de cobertura — obligatoria, y nació de un defecto real

**Cuenta los fechados contra el TOTAL, y reporta la razón SIEMPRE**, tenga el valor que
tenga. Bajo un umbral razonable —**80%**— no se anima: se dibuja el estado asentado.

**Y todo folio sin fecha sale LISTADO con su número.** Si un folio desaparece del grafo, eso
es un hallazgo, no ruido.

> [!danger] NUNCA un `continue` callado. Esto pasó, y es el motivo de esta sección
> **MEDIDO por Zero en su propia implementación, 2026-09-05**, al correr este skill por
> primera vez: su extractor hacía `if not fecha: continue`. Los folios sin fecha **no se
> degradaban: desaparecían del grafo sin decirlo**. De 131 folios se dibujaron 116 y
> **catorce se cayeron en silencio** — entre ellos el único riesgo aceptado de su dominio y
> un defecto de cobro cerrado *as-is*.
>
> **Nadie lo nota porque un grafo incompleto se ve idéntico a uno completo.** Y el prompt ya
> mandaba «reporta los conteos y cuádralos»: se reportó 116 y **nunca se cuadró contra 131**.
> *Un conteo reportado y uno cuadrado se leen igual.*

### Y la degradación YA ESTÁ CONSTRUIDA: conéctala, no la reinventes

El código que dibuja el estado asentado **ya existe** — es el que atiende
`prefers-reduced-motion`. Lo único que falta es **conectarlo con la falta de fechas**. Sin
ese renglón, quien corra el skill lo escribe otra vez a mano, que es lo que pasó la primera
vez que se ejecutó.

## 2 · La forma

- **Disposición dirigida por fuerzas**: repulsión entre nodos, resortes en las aristas, y
  una **ancla por área**. Reparte las anclas en un anillo **alternando áreas grandes y
  pequeñas** — ordenadas por peso se amontonan todas de un lado. Las de más peso tiran más
  hacia el centro.
- **Tamaño por número de conexiones.** Halo suave a los que bloquean a alguien, proporcional
  a cuántos.
- **Las etiquetas son NOMBRES DE ÁREA**, en el centroide de sus nodos visibles, solo para
  áreas con tres o más, con anti-colisión. **Nunca etiquetes con el número de folio: un
  folio es una dirección, no un nombre.** El folio va en el hover, con título, severidad y
  área.
- **`bloquea` se dibuja con arco curvo Y PUNTA DE FLECHA.** Una raya simétrica **miente**
  sobre una relación dirigida. Las citas van curvas, tenues y al fondo.

## 3 · El color

- **La severidad es ESTADO, no identidad.** Usa la paleta de estado reservada
  (`#d03b3b` crítica · `#ec835a` alta · `#fab219` media · `#0ca30c` baja), **igual en los dos
  temas**. No la trates como paleta categórica.
- Define claro y oscuro **por tokens en `:root`**, con `@media (prefers-color-scheme: dark)`
  guardado como `:root:not([data-theme="light"])` y también `:root[data-theme="dark"]`.
  **Ningún color puede vivir solo dentro de un bloque de tema.**
- **Leyenda con texto siempre visible**: la identidad no puede depender solo del color.

## 4 · La animación

- Los nodos aparecen **en su día real**, con un destello breve. Las aristas, cuando existen
  sus dos extremos.
- **HUD mínimo:** contador de **días operando** (día 1 = el primer folio del vault) grande, y
  debajo la fecha. Nada más.
- Botón de repetir, **R** para repetir, **espacio** para pausar.
- **Respeta `prefers-reduced-motion`:** dibuja el estado final asentado, sin animar.

---

## 5 · Rendimiento — esto ya tumbó una versión

> [!danger] PROHIBIDO `ctx.shadowBlur` por nodo
> Con ~116 nodos obliga a rasterizar un desenfoque a pantalla completa **cada fotograma** y
> mata la página. Usa **sprites de destello pre-renderizados**: un canvas por severidad con
> un gradiente radial, dibujado **una sola vez**, y luego `drawImage` escalado.

- **Tope de `devicePixelRatio` en 1.5.**
- El listener de `resize` **con freno (~220 ms)** y **solo recoloca las anclas** — no
  reinicia la animación.
- **`try/catch` alrededor del bucle:** si algo revienta, dibuja el estado asentado en vez de
  dejar la pantalla en blanco.
- Si cambias de tema en caliente, **reconstruye los sprites** o se quedan del color viejo.

## 6 · Modo render, para exportar video

Acepta `?f=N&fpd=K`: dibuja el fotograma N **de forma determinista** —misma semilla, mismos
pasos de física, sin `requestAnimationFrame`— y marca `window.__listo`. Con eso se capturan
los fotogramas con Chrome headless y se arman con `ffmpeg`.

> [!warning] Al capturar en paralelo, NO le des a cada Chrome su propio `--user-data-dir`
> Crear el perfil **domina el tiempo** y parece un cuelgue. Referencia medida por Zero: 870
> fotogramas a 1920×1080 en unos 8 minutos con ocho Chrome en paralelo, y 5 MB de mp4.

---

## Lo que NO sirve, para que nadie lo vuelva a intentar

**Gource no vale para esto.** Es un visualizador de árboles: las líneas que dibuja son
**contención de carpetas, no relaciones**. Medido por Zero antes de escribir nada.

## Antes de entregar

Comprueba la sintaxis del JS, que los datos carguen, y que existan **todos** los ids que el
código busca. Y **di explícitamente qué no pudiste verificar** — un entregable que calla lo
que no comprobó se lee como si lo hubiera comprobado.
