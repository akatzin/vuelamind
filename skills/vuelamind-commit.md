---
description: Motor genérico de reconciliación — lee el manifiesto del dominio actual y ejecuta el ciclo completo: medir, confirmar, escribir, sincronizar, reportar
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
| `vault` | dónde vive el conocimiento en esta máquina |
| `validador` | el script de comprobaciones mecánicas, con su ruta — o `—` si el dominio no tiene, y entonces los chequeos se hacen a mano y se dice |
| `acceso_vivo` | cómo se llega a los sistemas que hay que verificar |
| `notas:` `cola` · `archivo` · `panorama` · `decisiones` · `bitacora` · `arranque` | los nombres reales de las seis notas del ciclo |
| `marco` | dónde vive el master del método y sus parches |
| `antes_de_medir` | enganche opcional: qué correr antes del paso 0 (desbloquear una llave, montar algo) |
| `despues_de_escribir` | enganche opcional: qué correr tras el paso 4 (un empuje manual, si el transporte lo pide) |
| `avisos_del_dominio` | lista corta de trampas propias que el motor debe respetar al escribir |

**Si el manifiesto no existe, detente y dilo.** Ofrece generarlo desde este contrato preguntando las claves una a una — no inventes rutas ni corras un checkpoint "genérico" sin él: reconciliar el vault equivocado es peor que no reconciliar.

**Si existe pero le falta una clave, repórtalo como hueco** y sigue con lo que sí declara. Un manifiesto incompleto que avisa vale más que uno que aparenta completitud.

Si declara `antes_de_medir`, córrelo ahora.

## 0. Correr el validador del dominio

**Empieza siempre por aquí.** El validador hace las comprobaciones mecánicas de una vez, y no se cansa ni se salta pasos. Corre el que declare el manifiesto; sus banderas y chequeos concretos son del dominio.

**Corre el script antes de revisar nada a mano.** Este método nació de un cierre donde se reportó "sin defectos" habiendo saltado una verificación entera.

Los **avisos** de enlaces colgantes no son errores en un vault que los use a propósito para marcar trabajo pendiente. Lo que hay que confirmar es que cada uno siga siendo deliberado.

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
2. **Hacia adentro**: quién la enlaza (`grep` del nombre de la nota sobre el vault) — ¿alguien cita como hecho lo que este cambio vuelve falso?

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

**Preguntárselo en cada cierre, antes de confirmar la lista.** La prueba: reescribe el hallazgo sustituyendo **todos** los nombres propios por genéricos. ¿Sigue siendo cierto y útil? Es del método → **parche** en la carpeta de parches del marco (ruta en el manifiesto). Ante la duda, se escribe: un parche de más cuesta un archivo; uno de menos cuesta que otra instancia repita el error meses después.

> [!danger] Aplicar un parche no termina en la instancia
> Termina cuando la plantilla del master es coherente con él **y eso está publicado**. Es un solo acto y no se escala al usuario. Cuatro movimientos: corregir la instancia; mapear a qué sección de la plantilla toca; **traer el master fresco justo antes de editarlo** —otro dominio pudo publicarlo en medio, y pisar su versión no dispara ninguna alarma—, respaldar, publicar y **verificar por huella del otro lado**; y anotar la fila con su versión. Añadir también la fila al índice del README de parches, **comparando por nombre y no por conteo**.

### Cómo se pide la confirmación

Con **`AskUserQuestion`**, no con una pregunta suelta — así el visto bueno es un clic sin ambigüedad. Dos opciones: **"Sí, continúa"** y **"No, tengo comentarios"**. Con la segunda: ajustar, **volver a presentar la lista completa** y preguntar de nuevo. **No se escribe nada hasta el "Sí, continúa".**

## 4. Escribir la documentación

El **único** paso que escribe en el vault. En este orden, porque cada uno depende del anterior — los nombres reales los da el manifiesto:

1. **La cola** — items cerrados condensados a un párrafo, correcciones, conteos.
2. **Las notas de componente** — la lección se promueve **antes** de archivar: archivar una lección es perderla. **Y también a la nota que hacía la PREGUNTA**: si el item nació de un *"por confirmar"* escrito en una nota temática, esa nota es destino obligatorio de la respuesta — hacia atrás no va nadie, y una pregunta sin tachar invita a re-medir lo ya medido. *(Parche `la-leccion-va-tambien-a-la-nota-que-preguntaba`.)*
3. **El archivo de cerrados** — el registro completo, con su evidencia.
4. **El registro de decisiones** — si hubo elección con alternativa defendible: qué se descartó y qué haría cambiar de opinión.
5. **El panorama** — solo si cambió de verdad, refrescando su fecha. **Es una FOTO, no una crónica**: presente, sin fechas de jornada. La prueba: ¿esta frase seguirá siendo cierta y útil en seis meses? Al convertir crónica en foto, rescatar el hecho y tirar la jornada — y comprobar que ningún hecho vivía solo en la parte narrativa.
6. **La bitácora** — la entrada **del día**, al final; si ya existe la de hoy, se amplía con un `###`, no se abre otra. Solo entradas con fecha — las lecturas de conjunto van al registro de decisiones. Se escribe **en voz alta, para contárselo a un amigo**: si una frase no se entendería en una cocina, se reescribe. **Los errores propios van, y van con nombre** — es lo que separa una bitácora de un boletín de logros.
7. **El parche**, si el paso 3 detectó algo del método.
8. **El documento de arranque** — al final, porque resume todo lo anterior y es lo que más envejece: le habla a una sesión que no tiene el contexto de ésta. Revisar que el conteo cuadre con la cola, que no mande a rehacer trabajo hecho, que los hechos de arquitectura sigan ciertos, y que liste los errores más instructivos con fecha.

Al terminar, **volver a correr el validador**: los cambios pueden romper conteos o dejar un enlace colgante nuevo.

**Y barrer las remisiones con fecha que se escribieron hoy.** Una frase del tipo *"ver `<nota>`, `<fecha>`"* **promete una sección**, y el chequeo de enlaces no puede verla: comprueba que el archivo destino exista —y existe siempre—, no que la entrada de ese día esté dentro. Una remisión a una sección no escrita **pasa en verde y se lee como respaldo**, que es peor que no citar nada: quien la sigue encuentra el archivo lleno de otras entradas y concluye que buscó mal.

Es un `grep` por fecha, no una lectura: por cada remisión con la fecha de hoy, comprobar que el destino tenga una sección con esa fecha. Lo que **no** debe reportarse es un enlace **sin** fecha — ése no promete nada. Y la regla al escribir: **la entrada primero, aunque sea su título y una línea; el enlace después.** Si no va a escribirse ahora, la remisión correcta es sin fecha, que se lee como pendiente. *(Parche `un-enlace-con-fecha-promete-contenido`.)*

Si el manifiesto declara `despues_de_escribir`, córrelo ahora.

## 5. Confirmar la réplica

Que el vault local y su réplica coincidan — **por huella, no por fe**. El cómo lo da el manifiesto (su `acceso_vivo` y la ruta remota). **Esperar a que coincida antes de reportar**: dar por sincronizado lo que no se midió es exactamente lo que este método intenta evitar. Si no hay forma de comprobar, reportar *"escrito, réplica no verificada"* — nunca darla por buena.

## 6. Reportar

**Qué se corrigió y qué se dejó igual**, separando cambios de documentación de cambios en sistemas — son actos con reversibilidad distinta. Si algo se afirmó antes sin verificar y resultó falso, decirlo explícitamente en vez de corregirlo en silencio.

Si no había nada que corregir, decir eso: es un resultado válido y significa que el marco se está manteniendo solo.

---

> [!note] De dónde salió este motor
> Es la generalización del `checkpoint` del dominio de origen (2026-08-11), que medido resultó **92.5% método y 7.5% ataduras** — 29 líneas de dominio en 386. Antes de este comando, cada dominio copiaba el método entero para tropicalizar ese 7.5%, y las copias divergían en silencio. Ahora el método vive una vez aquí y **cambia por parche**; lo del dominio vive en su manifiesto. Si este motor algún día necesita nombrar un archivo de un dominio concreto, deja de ser universal — ésa es la señal de que algo se está colando al nivel equivocado.
