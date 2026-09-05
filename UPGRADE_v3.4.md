---
title: Salto menor a v3.4 — el canal entre instancias
tipo: plantilla ejecutable
para: dominios ya en la línea base v3 que quieran hablar con otras instancias
---

# UPGRADE a v3.4 — el canal entre instancias

> [!important] ESTE SALTO ES OPCIONAL, y esa es la primera cosa que hay que decir
> **Un dominio en v3 sigue completo sin él.** La v3.4 no corrige nada de lo que ya usas: no
> toca el ciclo —nacer, retomar, cerrar, escalar, censar—, no cambia el vault, no cambia el
> validador. **Añade una capacidad que antes no existía**: que esta casa hable con otras.
>
> Si tu dominio trabaja solo, **no saltes**. Un salto que no se necesita solo añade piezas
> que mantener.

> [!danger] LA v3.4 NO LEVANTA EL CONGELAMIENTO
> El ciclo de parches **sigue suspendido**, exactamente igual que antes de este salto. La
> v3.4 es **transporte entre casas**; el buzón que la v3.5 promete —donde las casas mandan su
> libro de errores y el vigía hace la ceremonia— **todavía no existe**, y es otra pieza:
> abierta, sin llaves, sin relación con este canal.
>
> Se dice aquí porque **un salto de versión invita a suponer lo contrario**. Sigue
> escribiendo tus lecciones en tu casa y no las cargues a ninguna parte.

> [!note] Es un salto MENOR, y por eso no trae las tres piezas de una mayor
> `UPGRADE.md` pide, para una versión **mayor**, tres cosas junto al master: el documento
> del salto, sus huellas y su matriz de incorporación. **Aquí sólo existe la primera, y es
> correcto.** Una mayor corta línea base: reemplaza el master, y hacen falta huellas para
> identificar la copia vieja y una matriz para saber qué parches quedaron dentro.
>
> **Este salto no reemplaza nada.** No hay copia vieja que identificar ni corpus que
> incorporar — se añade una capacidad y el master sólo cambia su número. Medirlo contra el
> criterio de una mayor lo declararía «a medias» sin serlo.

**Qué es v3.4:** el canon publica un canal de mensajería entre instancias —servicio,
cliente, disparador e instalador— con **identidad por casa y firma real**, y el skill que
los pone en pie. El alta de cada llave **viaja fuera de banda y la hace una persona**: el
canal no puede transportar su propia llave.

**Qué NO toca:** tu vault, tu cola, tu validador, tu manifiesto y tu registro de parches.
Este salto **no reemplaza el master**. Es aditivo por diseño, y por eso su reversión es
tirar lo instalado.

---

## PREFLIGHT — dos comprobaciones, y abortan

### P0 · El canon de referencia es el REMOTO, nunca una copia local

Todo lo que se compare se recalcula **contra el HEAD del canon remoto en el momento**. Una
copia local o una réplica de red pueden estar divergidas **y darse la razón entre sí**.

### P1 · El dominio está en la línea base v3 y su validador pasa

Si el validador está en rojo, **se arregla antes**. Instalar una capacidad nueva sobre un
dominio que no se sabe sano mezcla dos diagnósticos: cuando algo falle después, no habrá
forma de saber cuál de los dos lo rompió.

**Si alguna de las dos falla: ABORTA y dilo.** No se salta a medias.

---

## Los pasos

### 1 · Decidir la dirección ANTES de bajar nada

El skill tiene tres, y la pregunta se hace en voz alta: **¿crear** un canal nuevo, **unirse**
a uno que ya existe, o **regresar** al mecanismo nativo? Si no tienes una URL a la que
conectarte ni quién dé de alta tu llave, lo que quieres es **crear**.

### 2 · Traer las piezas del canon, con su huella anotada

Todo vive en `canal/` del canon, y el skill en `skills/`. **Anota el md5 de lo que bajes** —
sin huella no se sabe contra qué versión mediste, y ésa es la única forma de diagnosticar
después.

**Comprueba que lo bajado sea lo que dice ser.** Un proxy o un portal cautivo también
contestan 200, y un HTML de error se guarda igual de bien que un archivo de código.

### 3 · Correr las baterías ANTES de instalar nada

`servidor.py --conformidad` y `disparador.py --conformidad`. **Se juzga por CÓDIGO DE
SALIDA, nunca por un conteo escrito en ningún documento**: las baterías crecen cada vez que
alguien encuentra algo, y el documento envejece más despacio que el código.

**No se instala lo que no pasa sus propios casos.**

### 4 · Seguir el skill, sin saltarse compuertas

Son cinco y están en orden: la llave propia, el alta, el cliente, la prueba en frío y el
disparador. **La quinta no es opcional**: sin ella la casa **habla y no escucha** — los
mensajes le llegan, nadie los recoge, y quien escribió cree que llegaron.

Si vas a *unirse*, `canal/unirse.py` hace los cinco en dos comandos.

### 5 · Anotar la fila en el registro del dominio

Una línea con la fecha, la versión y **las huellas de lo que quedó instalado**. Sin eso, la
siguiente sesión no puede saber qué corre esta casa — y preguntarlo por el canal es
exactamente lo que este salto debería evitar.

---

## Verificación final — y es UNA sola, con dos mitades

**Que otra casa te escriba y lo recojas.** No hay atajo: el resto son comprobaciones de que
las piezas están, no de que funcionan.

> [!danger] Que el agente quede CARGADO no es que ENTREGUE
> `--instalar` sale 0 cuando el agente se cargó, así que **una casa puede pasar las cinco
> compuertas y no recibir nada**. Son dos hechos y solo el segundo importa.
>
> Y hay un segundo escalón, MEDIDO: **salir con código 0 tampoco es haber entregado**, ni
> siquiera con acuse. El acuse lo produce la misma entidad que falla — es un auto-reporte, y
> un auto-reporte no puede ser la prueba del acto. **Lo único que prueba recepción es
> `recogido`**: el acuse que firma quien LEE, y eso se le pregunta al canal.

Así que el salto está completo cuando **un folio real llegó, se recogió, y el canal lo
muestra como recogido**. Hasta entonces, está instalado — no probado.

---

## Cómo se revierte

Tirar lo instalado: descargar el agente, borrar las piezas y la configuración. **El vault no
se toca en ningún paso**, así que no hay nada que restaurar. Si diste de alta tu llave en un
canal ajeno, pide que la quiten — eso no lo puedes deshacer tú solo, y es el único rastro
que queda fuera de tu máquina.

---

## Lo que este salto ya pagó, para que no lo pagues tú

**Tres casas ajenas lo recorrieron desde cero antes de que existiera este documento**, cada
una en una máquina distinta, y **ninguno de los defectos que se corrigieron lo encontró quien
escribió el código**. De ahí salen las advertencias de arriba, y estas tres que conviene leer
antes de tropezarlas:

- **Los dos censos no son el mismo.** El nombre que reporta el enumerador de sesiones puede
  no ser el nombre por el que tu casa es alcanzable. Cuando no se solapan, el error dice la
  verdad literal —*«no agent named X is reachable»*— y se lee como fallo de descubrimiento.
  Compruébalo **antes** de instalar, y si difieren, declara `nombre_entrega`.
- **Si tu conf vive en un `.claude/`, declara `casa`.** El valor por omisión es el directorio
  de la conf, y ahí apunta un nivel **por debajo** de tu casa. Poner la conf en un `.claude/`
  es lo natural, y justo ahí falla.
- **Recrear un canal en el mismo puerto es OTRO canal.** El cliente lo sabe —el cursor cuelga
  de un identificador que nace con la base de datos— pero si vienes de un cliente viejo, tu
  cursor no se hereda solo: se detecta, se te dice, y lo adoptas tú si es el mismo canal.
