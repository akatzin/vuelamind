---
description: Motor genérico de reconciliación — lee el manifiesto del dominio actual y ejecuta el ciclo completo: medir, confirmar, escribir, reportar
---

# /vuelamind-commit — reconciliar el dominio actual con la realidad

Reconciliar el vault con la realidad. **No es escribir documentación nueva: es detectar y corregir lo que envejeció.**

Este comando es el **motor**: trae el método completo y **no nombra ningún dominio**. Lo del dominio —rutas, nombres de nota, validador, acceso— vive en su **manifiesto**, que es datos y no comando.

> [!important] El orden importa: primero medir, luego confirmar, al final escribir
> Toda la escritura en el vault ocurre en el paso 4, y **solo después de que el usuario confirme** la lista del paso 3. Los pasos 0 a 2 son de lectura y verificación: no se toca ninguna nota mientras se está averiguando qué cambió.
>
> **Este orden no es tropicalizable.** Es la barrera que evita escribir sobre estado recordado en vez de medido — el error más caro que puede cometer un dominio con memoria. Lo que el manifiesto puede hacer es **inyectar pasos en dos enganches** (`antes_de_medir`, `despues_de_escribir`); lo que no puede es reordenar.

## Paso previo: localizar y leer el manifiesto

Vive en el proyecto: **`.claude/vuelamind-commit.manifiesto.md`**, junto al directorio de trabajo. No está en `commands/` a propósito — es datos, no un comando invocable.

Declara, como mínimo:

| Clave | Qué es |
|---|---|
| `vault` | dónde vive el conocimiento en esta máquina. **Opcional desde la v3.6**: sin declarar, `<proyecto>/vault/`. Declararla gana sobre la convención |
| `validador` | el script de comprobaciones mecánicas, con su ruta — o `—` si el dominio no tiene, y entonces los chequeos se hacen a mano y se dice |
| `acceso_vivo` | cómo se llega a los sistemas que hay que verificar |
| `notas:` `cola` · `archivo` · `panorama` · `decisiones` · `bitacora` · `arranque` | los nombres reales de las seis notas del ciclo |
| `marco` | dónde vive la copia local del método y sus parches |
| `canon` | **de qué repositorio se jala el método.** Por omisión el oficial; declararlo gana — un espejo, un derivado, o una copia bajo otra cuenta. **Quien declare uno distinto declara también quién lo sincroniza y cada cuánto** |
| `antes_de_medir` | enganche opcional: qué correr antes del paso 0 (desbloquear una llave, montar algo) |
| `despues_de_escribir` | enganche opcional: qué correr tras el paso 4 |
| `avisos_del_dominio` | lista corta de trampas propias que el motor debe respetar al escribir |
| `instancias` | quién trabaja en el dominio: la sección `## instancias`, con una tabla `nombre · acceso · carril · dónde` y una fila por instancia; `acceso` es `escribe` o `lee`. Opcional con una sola instancia |

**Si el manifiesto no existe, detente y dilo.** Ofrece generarlo desde este contrato preguntando las claves una a una — no inventes rutas ni corras un checkpoint "genérico" sin él: reconciliar el vault equivocado es peor que no reconciliar.

**Si existe pero le falta una clave, repórtalo como hueco** y sigue con lo que sí declara. Un manifiesto incompleto que avisa vale más que uno que aparenta completitud.

### Con varias instancias: un cierre a la vez

Si `## instancias` tiene más de una fila con acceso `escribe`, el cierre toma un candado antes de medir y lo suelta al final:

1. **El nombre.** La sesión sabe qué instancia es, o lo pregunta. No se inventa.
2. **Tomarlo:** `mkdir <proyecto>/.cierre.lock`, que es atómico, y dentro el archivo `quien` con una línea: `<nombre> <AAAA-MM-DDTHH:MM:SSZ>`. **Si la carpeta ya existe, no se cierra:** se dice quién la tiene y desde cuándo, y se espera. Un candado huérfano lo decide la persona: puede ser de un cierre que sigue corriendo.
3. **Con el candado puesto** se numeran los folios nuevos. Lo de otra instancia que salga en la relectura se le avisa a quien lo escribió; no se corrige.
4. **Soltarlo** después de renovar la instantánea: borrar `quien` y la carpeta, y comprobar que ya no existe.

El candado vale entre sesiones de una misma máquina: `mkdir` no es atómico entre máquinas que sincronizan una carpeta. Por eso `.cierre.lock/` no se sincroniza ni se versiona, y entre máquinas sigue mandando traer fresco cada archivo antes de editarlo.

Si declara `antes_de_medir`, córrelo ahora.

## 0. Correr el validador del dominio

**Empieza siempre por aquí.** El validador hace las comprobaciones mecánicas de una vez, y no se cansa ni se salta pasos. Corre el que declare el manifiesto; sus banderas y chequeos concretos son del dominio.

**Corre el script antes de revisar nada a mano.** Este método nació de un cierre donde se reportó "sin defectos" habiendo saltado una verificación entera.

Los **avisos** de enlaces colgantes no son errores en un vault que los use a propósito para marcar trabajo pendiente. Lo que hay que confirmar es que cada uno siga siendo deliberado.

**Y la cola, aunque el validador del dominio no la llame:** `python3 herramientas/pendientes.py revisar <vault>`, desde el canon, con `--cola` y `--archivo` si el manifiesto les da otro nombre. Si dice que la cola no está migrada, se reporta y se ofrece `migrar` (`UPGRADE_v3.12.0.md`).

Si el script reporta algo, anótalo para el paso 3 — **no lo arregles todavía**.

> [!warning] Si corriges un chequeo del validador, dos disciplinas, no una
> **Un chequeo que solo se probó en verde no está probado.** Cada arreglo se verifica con **dos casos**: el que antes fallaba (debe pasar ahora) y uno **inventado** que debe seguir saliendo — si ya no sale, el chequeo no se corrigió: se apagó. Después, deshacer el escenario y **comprobar la reversión** con un `diff` contra el estado previo, no con la memoria de haberlo hecho.
>
> **Y comprueba las dos SALIDAS, no solo la lógica.** Un chequeo tiene lo que **imprime** y lo que **devuelve** (el código de salida), y casi nunca se prueban las dos. Dos comprobaciones baratas: una fila de la salida comparada a mano contra la fuente, y `echo $?` en el camino verde y en el rojo. Suele fallar justo la rama que más ocurre.
>
> *(Parches `un-chequeo-arreglado-puede-quedar-ciego` y `el-instrumento-acierta-y-el-informe-miente`.)*

## 1. Revisar lo que el script no puede juzgar

Lo mecánico ya lo cubrió el paso 0. Aquí va el criterio:

- **La evidencia de los items cerrados sirve de verdad.** El script solo comprueba que exista algo; hay que leerla y ver si un lector futuro podría reconstruir qué se hizo y cómo se verificó.
- **Los huecos de numeración siguen siendo intencionales.** El script los reporta sin juzgarlos.
- **Las capacidades afirmadas siguen siendo incondicionales.** Si una nota dice que el sistema *tiene*, *puede* o *soporta* algo, comprobar que no dependa de un estado que hoy no se cumple. Una capacidad condicional escrita sin su condición es indistinguible de una permanente, y se propaga a todos los planes que la citen.
- **Las tablas de prioridad y las cadenas de dependencia siguen vigentes**, si la cola del dominio las tiene: cerrar un item que bloqueaba a otro cambia la cadena.

## 2. Verificar contra el sistema en vivo

Solo lo que haya cambiado desde el último cierre — no revalidar toda la cola cada vez.

Prioridad a **lo que se afirmó sin comprobar** y a lo que depende de estado volátil: servicios encendidos, montajes, tareas programadas, espacio libre. El acceso es el que declara el manifiesto; si falla, revisa su `antes_de_medir`.

> [!warning] Deshacer el escenario de prueba, y comprobar que se deshizo
> Verificar un arreglo exige provocar el fallo. Al terminar, **revertir el escenario y comprobar la reversión** — no darla por hecha porque el comando salió con 0.
>
> - **Detener algo no siempre lo detiene.** Comprobar que los procesos murieron, no solo que el comando de cierre no dio error.
> - **Si lo tocado es la capa de gestión, el servicio seguirá pareciendo sano** — lo roto es la red de seguridad que se estaba instalando, y eso no tiene síntoma.
> - **Si el escenario es documental** —una copia del vault, una fila alterada, un archivo de prueba— el residuo no tiene síntoma, tiene **lector**: la comprobación es un `diff` contra el estado previo, y borrar el respaldo comprobando que se borró. Si tocó el vault real, validador completo al final.
>
> *(Parche `deshacer-el-escenario-de-prueba`, v2.)*

## 3. Listar los cambios y confirmar

**Antes de escribir una sola línea en el vault**, presentar la lista y esperar el visto bueno.

### El radio del cambio — descubre las relaciones ANTES de cerrar la lista

La lista de notas a tocar **no sale solo de lo que la sesión tuvo abierto**: sale del **grafo de enlaces**. Por cada nota candidata, dos barridos:

1. **Hacia afuera**: sus `[[enlaces]]` salientes — ¿alguna vecina habla del mismo tema y quedaría desactualizada, o tiene un *"por confirmar"* que este cambio responde?
2. **Hacia adentro**: quién la enlaza — ¿alguien cita como hecho lo que este cambio vuelve falso?

**Los dos barridos los da un comando**, y conviene usarlo en vez de improvisar un `grep`:

    python3 herramientas/vecinas.py <nota> <vault>

> [!warning] Por qué no basta con `grep` del nombre de la nota
> Es lo que este paso decía antes, y **falla en las tres formas en que se escribe un
> enlace**: no distingue un `[[enlace]]` de una mención suelta en prosa, no resuelve
> `[[Nota|alias]]` ni `[[Nota#sección]]` —que apuntan a la misma nota con otro texto— y no
> normaliza acentos ni mayúsculas. **Sus fallos son silenciosos en la dirección peor**:
> devuelve de menos, y de menos aquí significa una vecina que se quedó desactualizada sin
> que nadie lo viera.
>
> Y el comando **marca si sirvió** (`--sirvio` / `--nada`). Si en semanas de uso real ningún
> barrido cambia una sola decisión, este paso está costando más de lo que devuelve y hay que
> decirlo con la cifra delante, no por intuición.

3. **Hacia la regla** — y este barrido es de otra naturaleza. Si lo que cambió **no es un hecho sino una regla** —una memoria, una convención, un vocabulario, un umbral—, **el radio no es el grafo: es el corpus**. Lo escrito bajo la regla anterior no tiene ningún enlace que lo delate; sigue ahí, coherente consigo mismo y desalineado con la regla nueva.

   **Se busca por el término que cambió, no por el nombre del archivo.** Si el vocabulario pasó de una palabra a otra, se barre la vieja; si cambió un umbral, se barren las cifras que lo citaban; si cambió una convención de escritura, se barre su forma. **Y se busca en las dos direcciones**: lo que usa la forma vieja, y lo que ya usaba la nueva sin que nadie lo hubiera declarado.

   > [!warning] Este es el barrido que más se salta, porque nada se pone en rojo
   > Una regla que cambia **no rompe nada visible**: los conteos cuadran, los enlaces resuelven, el validador sale verde. El desalineamiento vive en el contenido, y el contenido no se valida solo.
   >
   > **Si el barrido devuelve muchos, no es motivo para posponerlo entero:** se corrige lo que la regla vuelve *falso* —que es urgente— y se anota como pendiente lo que solo vuelve *inconsistente*. Lo que no se vale es cambiar la regla y dejar el corpus sin mirar, porque entonces la regla nueva convive con su contradicción y **la siguiente sesión no sabrá cuál de las dos manda**.

Lo que el barrido encuentre **entra a la lista del paso 3 como fila propia**, con su porqué. Mirar la estructura de carpetas no basta — nada en un nombre de archivo dice "esto es relevante"; la relación temática vive en el grafo. Y si el tema no tiene nota de la que salir, eso también es hallazgo: un track sin nodo no aparece en ningún censo.

> *En el dominio de origen: una auditoría de un aparato de red se iba a escribir solo en el panorama, con dos notas vecinas cargando semanas un "por confirmar" que la auditoría acababa de resolver — los wikilinks de la nota ya leída las delataban, y nadie los siguió. Semanas después, un permiso de acceso se concedió sobre una premisa que otra nota marcaba como no verificada: el grafo las conectaba, la sesión no.*

Para cada cambio: **qué nota**, **qué cambia** (el hecho concreto), **por qué** (qué se midió que lo contradice). Y separar:

- **Correcciones** — algo que el vault afirma y es falso. Van primero.
- **Actualizaciones** — algo que era cierto y dejó de serlo.
- **Lo que se deja igual** aunque parezca candidato, con la razón.

> [!note] Qué NO necesita confirmación
> Los conteos y casillas que son **consecuencia mecánica** de cerrar un item. Pedir permiso para eso es ruido que esconde lo que sí importa.

### Antes de preguntarle algo al usuario, busca si ya lo decidió

El registro de decisiones existe para no volver a preguntar. Si la decisión está, **ejecútala**. Si de verdad hay que reabrirla: *"esto ya se decidió el `<fecha>` por `<razón>`; propongo reabrirlo porque `<qué cambió>`"*. Escalar parece siempre la opción segura y por eso no hay resistencia natural contra este error. *(Parche `antes-de-escalar-consulta-las-decisiones-ya-tomadas`.)*

### Antes de decir "encontré", búscalo

En los **tres** sitios: el registro de decisiones, la nota del componente y **el archivo de cerrados**, que es el que nadie abre. Un hallazgo redundante no falla, y con tono de descubrimiento **hace dudar de documentación que estaba bien**. La forma correcta: *"el vault ya lo dice desde `<fecha>`; lo re-medí y sigue siendo cierto"*. *(Parche `antes-de-decir-que-encontraste-algo-buscalo`.)*

### ¿Algo de esto es del MÉTODO y no de este dominio?

**Se hace en TODOS los cierres, sin excepción, y su resultado va al reporte final — también cuando es «nada».**

> [!danger] Esto no es un recordatorio: es un paso con salida obligatoria
> Un paso cuyo resultado **no aparece en el reporte** es un paso opcional, por mucho que el texto diga *siempre*. Si saltárselo produce una salida idéntica a haberlo hecho, **se va a saltar** — no por mala fe, sino porque nada lo distingue.
>
> Por eso el cierre **no está completo** sin la línea del método en el paso 5. La diferencia entre *«no hubo nada del método»* y *«no lo miré»* es toda, y solo se ve si se escribe.

**Se recorren los hallazgos de la sesión uno por uno**, no en bloque ni de memoria: cada corrección, cada error propio, cada regla que se descubrió a medio trabajar. La prueba: reescribe el hallazgo sustituyendo **todos** los nombres propios por genéricos. ¿Sigue siendo cierto y útil? Si sí, es del método → **es un parche**. Ante la duda, se escribe: uno de más cuesta un archivo; uno de menos cuesta que otra instancia repita el error meses después.

**El parche se escribe siempre, en el vault del dominio, y ahí se queda**: no hay camino al canon.

### Cómo se pide la confirmación

Con **`AskUserQuestion`**, no con una pregunta suelta — así el visto bueno es un clic sin ambigüedad. Dos opciones: **"Sí, continúa"** y **"No, tengo comentarios"**. Con la segunda: ajustar, **volver a presentar la lista completa** y preguntar de nuevo. **No se escribe nada hasta el "Sí, continúa".**

## 4. Escribir la documentación

El **único** paso que escribe en el vault. En este orden, porque cada uno depende del anterior — los nombres reales los da el manifiesto:

> [!danger] LA NARRATIVA VA A LA BITÁCORA. En ninguna otra nota.
> No es «poca narrativa fuera de la bitácora»: es **ninguna**. En el resto se escribe **el
> hecho y la regla**; el relato de cómo se llegó a ellos tiene un sitio y ya existe.
>
> **Es presupuesto, no estilo.** Cada línea que cuenta el camino en vez del destino la paga
> **cada sesión que cargue ese texto**, para siempre. Y tiene un segundo coste menos visible:
> **el relato diluye la regla** — quien lee tres párrafos sobre cómo se descubrió algo tiene
> que extraer él la instrucción, y la extrae mal más veces de las que nadie mide.
>
> **El corte, que es mecánico:** una frase se queda si **cambia una decisión futura**.
>
>     se queda:  «se comprueba escribiendo: mirar permisos no basta, un montaje miente»
>     se va:     «lo intenté mirando permisos, no funcionó, y entonces probé a escribir»
>
> El caso medido **sí** se queda cuando es lo que sostiene la regla, comprimido a su hecho
> —*medido en X, falló así*—. Lo que se va es la crónica de la jornada.
>
> **La prueba, al releer:** si un párrafo se puede sustituir por su primera frase sin perder
> ninguna instrucción, era relato. A la bitácora, o fuera.
>
> *La versión blanda no sirve: «menos narrativa» no se puede barrer porque no se puede medir
> —todo autor cree que la suya es la mínima— y el texto vuelve a crecer en el cierre
> siguiente.*

1. **La cola**, con `herramientas/pendientes.py`: `cerrar <folio>` por cada pendiente cerrado y su párrafo en «## Cierre»; un abierto que cambió se reescribe en su archivo, y uno nuevo se abre con `nuevo`. El índice lo regenera el script: debajo de su marca no se edita a mano.
2. **Las notas de componente** — la lección se promueve **antes** de archivar: archivar una lección es perderla. **Y también a la nota que hacía la PREGUNTA**: si el item nació de un *"por confirmar"* escrito en una nota temática, esa nota es destino obligatorio de la respuesta — hacia atrás no va nadie, y una pregunta sin tachar invita a re-medir lo ya medido. *(Parche `la-leccion-va-tambien-a-la-nota-que-preguntaba`.)*
3. **El archivo de cerrados** — el registro completo ya está en `pendientes/cerrados/<folio>.md`; aquí solo se comprueba que su evidencia sirva.
4. **El registro de decisiones** — si hubo elección con alternativa defendible: qué se descartó y qué haría cambiar de opinión.
5. **El panorama** — solo si cambió de verdad, refrescando su fecha. **Es una FOTO, no una crónica**: presente, sin fechas de jornada. La prueba: ¿esta frase seguirá siendo cierta y útil en seis meses? Al convertir crónica en foto, rescatar el hecho y tirar la jornada — y comprobar que ningún hecho vivía solo en la parte narrativa.
6. **La bitácora** — la entrada **del día**, al final; si ya existe la de hoy, se amplía con un `###`, no se abre otra. Solo entradas con fecha — las lecturas de conjunto van al registro de decisiones. Se escribe **en voz alta, para contárselo a un amigo**: si una frase no se entendería en una cocina, se reescribe. **Los errores propios van, y van con nombre** — es lo que separa una bitácora de un boletín de logros.
7. **El parche**, si el paso 3 detectó algo del método.
8. **El documento de arranque** — al final, porque resume todo lo anterior y es lo que más envejece: le habla a una sesión que no tiene el contexto de ésta. Revisar que el conteo cuadre con la cola, que no mande a rehacer trabajo hecho, que los hechos de arquitectura sigan ciertos, y que liste los errores más instructivos con fecha.

   **Y que lleve escrita la regla de la narrativa**, porque este documento es lo único que
   **toda** sesión del dominio lee siempre. Una regla de cómo se escribe que vive en el
   registro de decisiones la cumple quien va a buscarla; escrita aquí, la cumple quien
   empieza. Es también el documento donde más cara sale incumplirla: lo carga cada sesión.

   > **El arranque es el sitio más caro del vault.** Si una sección suya se puede sustituir
   > por su primera frase, sobra — y sobra multiplicada por todas las sesiones que vengan.

Al terminar, **volver a correr el validador y `pendientes.py revisar`**: los cambios pueden romper conteos o dejar un enlace colgante nuevo. Con cualquiera de los dos en rojo, el cierre no está hecho.

**Y releer lo que la sesión escribió** — con `python3 herramientas/instantanea_vault.py diff <vault>`, o con lo que el dominio tenga. **Ni el barrido del radio ni el validador lo hacen**: el radio mira las **vecinas** de lo tocado, el validador mira **mecánica**. Un párrafo nuevo que afirma algo falso **pasa los dos**, porque cuadra, enlaza y no contradice a nadie — es la única parte del cierre que nada comprueba.

> [!important] La instantánea se renueva al TERMINAR el cierre, no al empezarlo
> Si se tomara al empezar, la copia ya traería dentro todo lo que la sesión escribió y **el
> diff saldría vacío** — un verde que miente, y el error fácil de cometer.
>
> Renovándola al terminar, el diff del cierre siguiente cubre **todo lo escrito desde el
> anterior**. Y ésa es además la unidad correcta: no *«lo de esta sesión»* sino **lo que nadie
> ha releído todavía** — porque una sesión que no llegó a cerrar también escribió.

Así que el cierre hace dos cosas con ella: **comparar** aquí, y **renovar** al final, ya
releída. **Si falta la instantánea, se dice** en vez de seguir como si se hubiera releído.

> [!note] Por qué esto no es git
> Lo que hace falta es el diff de **una sesión**, no una historia — y meter un repositorio sube la barrera para quien no es técnico sin dar nada más. Un dominio que ya viva en git puede usar el suyo; el resto no debería tener que aprenderlo para poder releerse.

**Y barrer las remisiones con fecha que se escribieron hoy.** Una frase del tipo *"ver `<nota>`, `<fecha>`"* **promete una sección**, y el chequeo de enlaces no puede verla: comprueba que el archivo destino exista —y existe siempre—, no que la entrada de ese día esté dentro. Una remisión a una sección no escrita **pasa en verde y se lee como respaldo**, que es peor que no citar nada: quien la sigue encuentra el archivo lleno de otras entradas y concluye que buscó mal.

Es un `grep` por fecha, no una lectura: por cada remisión con la fecha de hoy, comprobar que el destino tenga una sección con esa fecha. Lo que **no** debe reportarse es un enlace **sin** fecha — ése no promete nada. Y la regla al escribir: **la entrada primero, aunque sea su título y una línea; el enlace después.** Si no va a escribirse ahora, la remisión correcta es sin fecha, que se lee como pendiente. *(Parche `un-enlace-con-fecha-promete-contenido`.)*

Si el manifiesto declara `despues_de_escribir`, córrelo ahora. Y si el cierre tomó el candado, suéltalo después: borra `quien` y `.cierre.lock/`, y comprueba que ya no existe.

## 5. Reportar

**Qué se corrigió y qué se dejó igual**, separando cambios de documentación de cambios en sistemas — son actos con reversibilidad distinta. Si algo se afirmó antes sin verificar y resultó falso, decirlo explícitamente en vez de corregirlo en silencio.

**Y una línea obligatoria sobre el método** — siempre, aunque la respuesta sea que no hubo nada:

| Lo que pasó | Qué se reporta |
|---|---|
| Salió un parche | Cuál, qué corrige, y en qué nota del vault quedó |
| No salió ninguno | **«Del método, nada esta vez»** — es un resultado válido y el más frecuente |
| Hubo dudas y no se resolvieron | Cuál fue la duda. **Ante la duda se escribe el parche**: uno de más cuesta un archivo, uno de menos cuesta que otra instancia repita el error meses después |

**Un reporte sin esa línea es un cierre incompleto**, y quien lo lea debe poder notarlo. Es la única forma de distinguir un dominio que no produjo lecciones de uno que dejó de buscarlas.

Si no había nada que corregir, decir eso: es un resultado válido y significa que el marco se está manteniendo solo.

---

> [!note] De dónde salió este motor
> Es la generalización del `checkpoint` del dominio de origen (2026-08-11), que medido resultó **92.5% método y 7.5% ataduras** — 29 líneas de dominio en 386. Antes de este comando, cada dominio copiaba el método entero para tropicalizar ese 7.5%, y las copias divergían en silencio. Ahora el método vive una vez aquí y **cambia por parche**; lo del dominio vive en su manifiesto. Si este motor algún día necesita nombrar un archivo de un dominio concreto, deja de ser universal — ésa es la señal de que algo se está colando al nivel equivocado.
