---
title: Salto menor a v3.9 — la entrevista recoge lo que se dijo antes de preguntar, y la identidad se escribe
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — REQUIERE los artefactos de la v3.5
---

> [!danger] De dónde tienes que venir: REQUIERE la v3.5
> **El master que trae este salto nombra `/vuelamind-learn`**, que es el artefacto que instala
> la v3.5. Si saltas desde más atrás, quedas con un documento que **promete una pieza que no
> tienes** — haz antes la v3.5.
>
> *El mapa completo de saltos vive en `UPGRADE.md`, que no muere con ninguna versión.*

# UPGRADE a v3.9 — tres cosas que la entrevista perdía

> [!important] ESTE SALTO SÍ TE PIDE ALGO AUNQUE TU DOMINIO YA HAYA NACIDO
> A diferencia de la v3.6, aquí **hay que escribir dos líneas y mover un archivo**. Se hace
> una vez. Si traes el master y no lo haces, el salto queda **a medias y sin síntoma**: todo
> seguirá funcionando, tu dominio seguirá sin poder decir cómo se llama, y su acta seguirá
> sin viajar con él.

## Las tres cosas

**1 · La señal cero: el nombre con el que llegó la carpeta.**

Quien abre el asistente lo abre dentro de una carpeta que ya nombró. Ese nombre es **lo único
que esa persona dijo en frío** — antes de que el marco le diera una sola palabra de vocabulario.
Todo lo demás del acta se dirá ya anclado, con los términos que el asistente acaba de enseñarle.

`logistica`, `tesis-doctoral`, `planta2-mantenimiento` traen un dominio entero dentro. `agente`,
`claude`, `proyecto`, `prueba` no traen nada. **El marco ahora lee ese nombre antes de saludar**,
lo trata como **hipótesis que se confirma** —nunca como dato— y lo escribe en el acta con las
palabras de quien lo puso, diciendo que se dijo antes de la primera pregunta.

Cuando no hay señal, no se menciona: no se comenta el nombre, no se pregunta por qué lo eligió,
y la entrevista arranca como siempre.

**2 · La identidad deja de vivir solo en prosa.**

El marco bautiza al asistente en la presentación —*«me llamo Vuelamind de nacimiento… pero el
nombre es tuyo»*— y hasta ahora **no mandaba escribirlo en ningún campo**. El nombre quedaba
suelto en la conversación y en la narrativa de las notas.

Desde la v3.9, el frontmatter del panorama lo declara:

```yaml
---
title: <Dominio> — Panorama
asistente: <cómo se llama el asistente de este dominio>
dominio: <cómo se llama el dominio>
alcance: entrada al vault · lectura de 5 minutos
actualizado: <AAAA-MM-DD>
---
```

Es lo que permite que **cualquier pieza sepa a quién está mirando sin deducirlo leyendo prosa**
— un panel que liste los dominios de una máquina, un instalador, un validador cruzado. Y lo
deducido de la prosa no es un dato: es una lectura del asistente disfrazada de hecho.

**3 · El acta de nacimiento se muda dentro del vault.**

Vivía fuera, junto al manifiesto del proyecto. Es donde nadie la busca y, peor, **donde no
viaja**: el vault es lo que la gente copia, respalda y se lleva a otra máquina. El dominio
llegaba entero al destino salvo por **el documento que dice quién es**.

Y es lo único del dominio que no se puede rehacer: las notas se reconstruyen midiendo otra
vez; **una entrevista de nacimiento no se vuelve a tener**. Las palabras con las que alguien
explicó su caso el primer día se dicen una vez.

El manifiesto la sigue declarando con `acta:` — la clave no cambia, cambia a dónde apunta.

> [!note] Lo que este salto NO mueve
> `memory/` y el manifiesto siguen fuera del vault, cada uno por su motivo: la memoria vive
> donde la herramienta la espera, y el manifiesto es configuración, no contenido. **La unidad
> que se lleva uno es la carpeta del dominio, no el vault.** Quien empaquete solo el vault se
> deja cosas — ahora se deja menos, y sobre todo no se deja el acta.

## Cómo saltar

**Tres pasos, y los dos últimos son los que se olvidan.**

1. **Trae `MARCO_Inicial.md` del canon y comprueba que dice `version: 3.9`.** Si tu copia está
   modificada, respáldala antes.

2. **Añade `asistente:` y `dominio:` al frontmatter de tu `0_<Dominio>.md`.** Con el nombre que
   tu asistente use de verdad hoy — si nunca se lo pusiste, es el de nacimiento.

3. **Muda el acta al vault. Lo hace el asistente, no la persona** — es mover un archivo y
   reescribir una clave, y un paso manual dentro de un salto es el paso que se queda sin dar:

   ```sh
   # donde dice el manifiesto que está hoy, y adónde va
   ACTA_VIEJA=<lo que declare la clave `acta:` de tu manifiesto>
   VAULT=<lo que declare la clave `vault:`>

   mv "$ACTA_VIEJA" "$VAULT/vuelamind-entrevista.acta.md"
   ```

   **Se MUEVE, no se copia.** Dos actas es peor que una mal colocada: un acta se enmienda
   con fecha, y con dos copias nadie sabrá dentro de un mes cuál recibió la enmienda.

   > [!danger] ¿Y si no hay ninguna acta que mover? Entonces este paso no es un `mv`
   > **Un dominio nacido antes del 2026-08-12 puede no tener acta en absoluto**: el acta la
   > instauró un parche de esa fecha y **nunca se aplicó con retroactividad**. Su manifiesto
   > no declara `acta:` y no hay archivo en ningún sitio. Para ése, `$ACTA_VIEJA` no existe y
   > el paso, tal como está arriba, no dice qué hacer.
   >
   > **Lo que toca no es saltárselo: es RECONSTRUIRLA**, y el protocolo ya existe y no es de
   > este documento — vive en `vuelamind-whoiam` y en el parche `la-entrevista-deja-acta`. En
   > una línea: **transcript de la sesión fundacional → notas fundacionales fechadas →
   > preguntar**, en ese orden, agotando cada fuente antes de bajar a la siguiente, y
   > **marcando en el frontmatter que es reconstruida y no original**.
   >
   > Se escribe **directo en el vault**, que es donde la v3.9 la quiere. Y ahí no hay riesgo
   > de duplicado: nunca hubo una primera.
   >
   > *Encontrado en la PRIMERA corrida real de este upgrader, por una casa distinta de la que
   > lo escribió y el mismo día de publicarse: su dominio nació el 2026-08-04 y tuvo que
   > salirse de este documento para saber qué hacer. Un salto que asume un archivo que no
   > todos tienen deja al que no lo tiene sin instrucción, y con la sensación de estar
   > haciéndolo mal.*

   Después, **reescribe la clave `acta:` del manifiesto** apuntando al sitio nuevo — si la
   tienes con ruta absoluta, la ruta entera.

   Y **compruébalo ejerciendo**, no dando por hecho que el `mv` salió bien:

   ```sh
   ls "$VAULT/vuelamind-entrevista.acta.md"     # está
   ls "$ACTA_VIEJA" 2>/dev/null && echo "OJO: quedaron dos"
   ls "$(ruta que declara ahora tu manifiesto)" # la clave apunta a algo que existe
   ```

> [!warning] Al entrar al vault, el acta entra en todo lo que copia el vault
> Es el punto del cambio y también su precio. La entrevista pregunta por sistemas reales,
> por lo que está bajo confidencialidad y por lo que se dice de otras personas: **hay actas
> con material que su dominio no querría que viajara**. Hasta hoy se quedaba fuera por
> accidente, no por decisión.
>
> **Éste es el momento de leerla.** Si algo de ahí no debe salir de esta máquina, se resuelve
> ahora —enmendando el acta con fecha, que es como se corrige un acta— y no el día que
> alguien comparta una copia del vault sin pensarlo.
>
> **Este aviso NO aplica si estás reconstruyendo el acta**, y conviene decirlo para que nadie
> lo cumpla de mentira: quien la escribe sabe su contenido mientras la escribe, y sus fuentes
> ya viven dentro del vault. No hay ninguna «primera lectura de algo ajeno» que hacer. El
> mismo cuidado existe, pero en otro momento — **al decidir qué se cita**, no al decidir qué
> se tapa. Donde este aviso hace todo el trabajo es en un acta **original**, escrita por la
> entrevista misma, con material que nadie ha vuelto a mirar desde entonces.

**Cómo sabes que funcionó**, y compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md               # version: 3.9
grep -E '^(asistente|dominio):' <tu vault>/0_*.md   # dos líneas, con valores
ls <tu vault>/vuelamind-entrevista.acta.md          # el acta, dentro
grep -n 'acta' <tu manifiesto>                      # la clave, apuntando ahí
```

> [!tip] Si tu dominio tiene validador, ata las dos claves a él
> Son dos líneas de comprobación y convierten este salto en algo que **no se puede dejar a
> medias en silencio**. Un salto cuya única prueba es acordarse de haberlo hecho es un salto
> que la mitad de las casas va a creer hecho sin estarlo.

## De dónde salió esto

**De una observación de campo y de dos cosas medidas.**

- **La observación**, del fundador del marco: al crear la carpeta, *«el usuario se ve forzado a
  pensar algo»*. Unos escriben `agente` o `vuelamind`, que no aportan; otros escriben
  `agenteOperacion` o `logistica`, **y eso por sí solo ya alimenta la entrevista**.
- **El marco ya supo esto y lo perdió.** Su comando de inicialización retirado decía
  literalmente **«Solo pregunta el nombre»**, y los ejemplos que eligió son del tipo que aporta:
  *`tesis`, `taller`, `mudanza`*. Al retirarse esa pieza, la señal dejó de recogerse — y el
  master pasó a **proponer** el nombre al final de la entrevista sin mirar nunca con cuál
  había llegado la carpeta.
- **Y la tercera salió de una pregunta de operación**, no de un fallo: *«si me llevo el vault
  a otra máquina, ¿se va con acta?»*. Medido en un dominio real: **no**. El acta, las memorias
  y el manifiesto vivían fuera; llevarse el vault se llevaba todo lo que el dominio sabe y
  dejaba atrás lo que el dominio es.
- **Y el caso que motivó la segunda pieza**: un dominio real llevaba cinco semanas con su
  asistente llamándose de una forma que **no estaba escrita en ningún campo de su vault** —
  solo suelta en tres notas de narrativa. Se descubrió al intentar listar los dominios de una
  máquina y no poder nombrarlos sin inventar.

> [!note] Lo que este salto NO puede prometerte
> Que la señal cero rinda en el uso real es **inferido**: sale de una observación sobre cómo
> nombra la gente sus carpetas y de un precedente documental del propio canon. **La corrida
> que lo ascendería a medido es la próxima entrevista que hagas** — si el nombre de la carpeta
> no aporta nada en diez nacimientos seguidos, esta sección sobra y hay que decirlo.
>
> Y hay un riesgo que conviene tener a la vista: **un asistente entusiasta puede tomarse la
> hipótesis como dato** y arrancar la entrevista afirmando de qué es el dominio. Eso es
> exactamente lo que la sección prohíbe, y es lo primero que hay que vigilar al usarla.
