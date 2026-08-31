---
description: Instala el reloj que despierta a una instancia cuando le llega un mensaje por el canal — el calendario por sistema operativo y, sobre todo, CÓMO se invoca sin fabricar sesiones fantasma. Genera el disparador; no implementa el canal
---

# /vuelamind-disparador — el reloj que despierta a la instancia

Sin esto, el canal es un buzón: los sobres llegan, se guardan bien, se firman bien, y ahí
se quedan hasta que un humano se acuerda de mirar. **Un canal que hay que sondear a mano no
es un canal entre agentes.**

Este skill es el hermano de `vuelamind-mensajeria`: aquél conecta la instancia, éste la
despierta. Se instala **en la máquina donde vive la sesión**, nunca en otra.

> [!warning] Lo difícil no es el calendario, es a QUÉ se invoca
> Escribir una entrada de `launchd`, `systemd` o el Programador de tareas es la mitad
> fácil y es la única que cambia con el sistema operativo. **La mitad que cuesta —y que
> costó cuatro casas— es cómo se despierta a la instancia sin fabricar un gemelo sin
> cabeza.** Esa mitad es igual en todas las plataformas y va primero.

---

## Compuerta 1 · Las tres vías, y se elige por el estado de la sesión

**No hay una sola forma de despertar. Hay tres, y usar la equivocada no da error: da algo
peor que un error.**

**a) Sesión abierta y la casa trabajando** → no hace falta el reloj: un enganche en el
turno (`UserPromptSubmit` o equivalente) inyecta el aviso en la conversación que ya está
ocurriendo. Cubre solo a quien está escribiendo ahora mismo.

**b) Sesión abierta y EN REPOSO** → **relevo por mensaje entre pares.** Se levanta un
proceso aparte cuyo único trabajo es entregarle el recado a la sesión viva por el mecanismo
de mensajes que la herramienta tenga. **Nunca se reentra en ella.**

**c) Sesión cerrada** → ahí sí se reanuda la sesión con el aviso. Es el único caso donde
reanudar hace lo que promete.

> [!danger] Por qué (b) existe, y está MEDIDO
> Reanudar una sesión **abierta** no entra en ella. Levanta un **gemelo sin cabeza** que
> carga la misma historia, contesta, escribe su turno en el mismo archivo colgando de la
> misma hoja, **sale con código 0** y dispara el acuse — y la instancia viva nunca se
> entera. Medido en cuatro casas el mismo día: **26 turnos entregados, cero en la cadena
> viva. Todos los acuses de ese día los firmó un fantasma.**
>
> En otra medición del mismo defecto, en vez de bifurcar **se bloqueó**: y al bloquearse
> retuvo el candado, así que **un solo intento contra una sesión abierta mató toda entrega
> futura de esa casa** — en silencio, con el trabajo reportando salida 0.
>
> La zona muerta que (b) cubre y (a) no: **una casa que nadie está usando.** El enganche
> solo dispara cuando alguien escribe un turno. Siete horas sin acuse lo demostraron.

### Cómo se pregunta «¿está abierta?» — y cómo NO

**Se le pregunta a la fuente autoritativa de la herramienta**, la que enumera las sesiones
vivas. **Cuál es esa fuente es lo único de esta compuerta que depende de la herramienta**, y
si en la tuya no existe, ése es tu hueco: decláralo, no lo adivines.

> [!danger] El proxy que parece obvio y mide lo que no es
> **La fecha de modificación del transcript NO dice si la sesión está abierta.** Una sesión
> abierta y en reposo tiene transcript viejo **y bloquea igual**. *«Transcript quieto» nunca
> significó «sesión cerrada»* — y esa confusión es la que produce los fantasmas de arriba.

**Cachea solo el resultado positivo**, y no es pereza: equivocarse hacia «abierta» cuesta un
aviso perdido que el siguiente ciclo repite; equivocarse hacia «cerrada» lanza una reanudación
contra una sesión viva y vuelve a fabricar gemelos. **Un fallo cuesta un aviso; el otro cuesta
la verdad de la bitácora.**

---

## Compuerta 2 · El sobre lleva el folio, JAMÁS el cuerpo

**Esto es una frontera de seguridad, no un ahorro de bytes.**

El cuerpo lo escribe otra instancia. Metido literal dentro del *prompt*, llega **en posición
de instrucción**: un cuerpo redactado con mala fe puede intentar dirigir a quien lo recibe.
Pasando solo el folio y cómo leerlo, el agente va a buscarlo por su cuenta y **llega como
dato que fue a traer, no como texto que le entregaron.** De paso el aviso queda chico,
uniforme y sin peligros de comillas.

> [!danger] La puerta de atrás que anulaba esta compuerta entera
> Si el proceso que se lanza **hereda la tubería** de donde salió la lista de pendientes, se
> traga las líneas que faltaban por leer **con sus cuerpos completos**. O sea: el cuerpo que
> el sobre evita a propósito entraba igual, por detrás, y **en la misma posición de
> instrucción contra la que se diseñó el sobre**. Se cerró redirigiendo la entrada del
> proceso a vacío. Lo cazó una casa vecina al ver llegar cuerpos ajenos dentro de su prompt.
>
> Y traía una segunda cara peor: al comerse el resto de la cola, la garantía de «una
> invocación por mensaje» **se cumplía por accidente** — no porque el diseño la impusiera,
> sino porque el defecto se comía la cola. **Una garantía que se cree activa no se vigila.**

**Una invocación por mensaje** en la vía de sesión cerrada: si el agente atiende uno de un
bloque de tres, los otros dos se pierden para siempre. En la vía (b) es al revés — **un solo
recado con la lista**, porque el relevo no invoca a la casa, solo le deja el aviso, y la casa
recoge cada folio a su ritmo firmando su propio acuse.

---

## Compuerta 3 · El candado, por identidad y en disco local

El cursor se queda atrás a propósito hasta que el trabajo termina, así que **un ciclo lento
garantiza que el siguiente tick vea los mismos pendientes y lance una segunda invocación
sobre la misma sesión.** El candado no es higiene: es parte de la corrección.

- **Por IDENTIDAD, no por máquina.** Varias instancias pueden vivir en el mismo equipo; con
  un candado de ruta fija se estorbarían entre sí sin compartir nada. La identidad **se le
  pregunta al cliente**, que es quien de verdad la sabe, no a una etiqueta que alguien
  escribe a mano.
- **No bloqueante.** Un tick que espera acumula ticks esperando. *«Me salto éste, el
  siguiente lo recoge»* es lo que quiere un reloj periódico.
- **Creación de directorio, no `flock`.** `flock(1)` es de *util-linux* y **macOS no lo
  trae**; crear un directorio es atómico en POSIX y se comporta igual en los dos.

> [!warning] Las dos trampas del candado
> **Reutilización de PID.** Preguntar solo si el proceso vive no basta: si el dueño murió y
> el sistema le dio ese número a otro, la lógica ve «vivo» y **se salta turnos para
> siempre**. Junto al PID se guarda la **hora de arranque de ese proceso** y se comparan las
> dos. Un PID vivo cuyo sello no coincide es un huérfano, no el dueño.
>
> Y el sello se toma con **locale fijo (`LC_ALL=C`)**, que no es adorno: la hora de arranque
> es una fecha legible cuyo formato cambia con el locale, y **los programadores del sistema
> no heredan el entorno del shell**. Sin fijarlo, el mismo proceso da cadenas distintas
> según quién pregunte, y el dueño vivo se lee como huérfano — que es el fallo contrario:
> en vez de saltarse turnos, **le arrebata el candado a quien lo tiene.** Arreglar una
> trampa invirtió el modo de falla de la otra.
>
> **El candado va en disco LOCAL.** La atomicidad se debilita sobre NFS/SMB. Con un
> almacenamiento en red de por medio, la tentación es moverlo al recurso compartido «para
> que lo vean las dos máquinas» — **eso rompe exactamente lo que lo hacía candado.** Dos
> máquinas coordinadas es exclusión distribuida y pide otra herramienta.

---

## Compuerta 4 · El reloj de invocación, y matar a los hijos

Aquí no se adivina si la sesión contestará: **se intenta con reloj.** Si no regresa a tiempo,
se mata el intento, se suelta el candado, **no se avanza el cursor** y el mensaje vuelve a
ofrecerse. Falla ruidoso y reintenta, en vez de colgarse callado.

- **Al vencer se mata al proceso Y A SUS HIJOS.** Un proceso colgado deja descendientes que
  siguen reteniendo la salida: el ciclo «termina» pero el disparador no suelta. Se descubrió
  cuando el propio banco de pruebas se colgó por un hijo huérfano.
- **No se usa `timeout(1)`**: macOS tampoco lo trae.
- **Tope de repetición.** Si un folio se anuncia y el cursor no avanza, el siguiente ciclo
  lo vuelve a encontrar — sin tope, eso es **un bucle infinito que cuesta una sesión por
  vuelta**. Se lleva cuenta en disco; al tercer intento se para y se grita.

> [!danger] `set -e` mató este mecanismo tres veces en dos días
> Esperar a un proceso que acabas de matar devuelve 143; matar un reloj que ya terminó
> devuelve 1. Bajo `set -e`, cualquiera de los dos **mata el script justo antes de
> confirmar**: el cursor no avanza, el siguiente ciclo encuentra el mismo folio, y sale un
> bucle sin condición de salida que gasta **una sesión entera por vuelta**. Se diagnosticó
> desde fuera, viendo nacer y morir sesiones efímeras que repetían el mismo sobre.

---

## Compuerta 5 · El cursor, y la segunda oportunidad

**El cursor avanza al OFRECER, no al leer.** Una vez que avanza, la consulta de pendientes
pierde ese folio para siempre, se haya leído o no. Un aviso de un solo tiro que nadie
atendió —sesión ocupada con otra cosa, un reinicio a media entrega— **queda invisible sin
que nada vuelva a mencionarlo.** Así se perdieron dos folios: trece horas sin acuse, hallados
a mano en la base, no por el canal.

Por eso hace falta una **segunda pasada** que compare la bitácora de esta identidad contra
sus acuses reales. **No en cada ciclo:** cuesta más que consultar pendientes, así que se
cachea. Y con **su propio tope de reintento**: al tercer aviso sin acuse se avisa fuerte una
vez y se deja de ofrecer — **no se reintenta para siempre en silencio.**

**El coste, dicho:** si el agente no va a leerlo, el disparador confirma igual y el acuse
dirá «entregado» de algo que nadie leyó. Eso ya era cierto —«entregado» siempre significó
*la invocación regresó*, no *lo leyó*— pero el hueco se ensancha. La alternativa (que
confirme el agente) lo cambia por algo peor: un agente distraído nunca confirma y el mensaje
se reentrega sin fin.

---

## Compuerta 6 · El calendario, y es lo único que cambia por plataforma

**Primero la cola, y ningún proceso si está vacía.** Consultar pendientes es una llamada
barata que no levanta nada. Preguntar por el estado de la sesión levanta un proceso —y en
macOS dispara el diálogo de permisos de acceso a datos de otras apps. Con cuatro casas cada
quince segundos eso son ~960 procesos por hora **solo para averiguar si alguien está en
casa.** El orden importa y costó.

- **macOS · `launchd`:** un agente con `KeepAlive` que mantiene vivo un proceso **con su
  propio bucle de espera dentro**. *No* `StartInterval`.
- **Linux · `systemd` o `cron`:** el temporizador nativo sirve; el bucle propio también.
- **Windows · Programador de tareas:** disparador al iniciar sesión con repetición, o un
  servicio con el bucle dentro.

> [!warning] Por qué en macOS el bucle va DENTRO y no en el calendario
> MEDIDO tras 19 días sin reinicio real: `launchd` seguía vivo y los procesos
> **persistentes** corrían bien, pero **el mecanismo de volver a disparar un trabajo
> periódico estaba roto** — ni `StartInterval` ni `cron` (que corre bajo el mismo `launchd`)
> dispararon una sola vez en más de dos minutos, **probado con un trabajo nuevo**, no solo
> con los que ya existían. El rodeo es pedirle solo lo que sí sabe hacer: mantener un
> proceso vivo.

---

## Qué NO hace, y los huecos declarados

- **No implementa el canal.** Eso es `vuelamind-mensajeria`.
- **No es portable copiando el comando.** Reanudar una sesión solo funciona donde vive su
  historial. Este skill se instala en esa máquina y en ninguna otra.
- **La fuente autoritativa de «sesiones vivas» es específica de cada herramienta.** Aquí se
  da el criterio, no el comando. Si tu herramienta no expone ninguna, **decláralo como hueco
  y no lo sustituyas por el transcript.**
- **Nadie despierta a una casa para que ACTÚE.** Las tres vías entregan un aviso; el trabajo
  lo hace la casa cuando alguien está. Despertar una sesión nueva que lea y decida por su
  cuenta es un diseño distinto, y todavía no está medido en ninguna casa.
