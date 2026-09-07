---
title: Salto menor a v3.5 — el buzón de aprendizaje, y el ciclo de parches que se retira
tipo: plantilla ejecutable
para: dominios ya en la línea base v3 que quieran aportar lo que aprenden
---

# UPGRADE a v3.5 — el buzón de aprendizaje

> [!important] ESTE SALTO ES OPCIONAL, y esa es la primera cosa que hay que decir
> **Un dominio en v3 sigue completo sin él.** No toca el ciclo —nacer, retomar, cerrar,
> escalar, censar—, no cambia el vault, no cambia el validador, y **no cambia nada de cómo
> escribes tus lecciones en casa**, que es la parte que de verdad importa y que nunca estuvo
> congelada.
>
> Lo que cambia es **el viaje de vuelta**: cómo llega al canon lo que aprendiste. Si tu
> dominio trabaja solo y no piensa aportar nada, **no saltes**.

> [!important] LEVANTA EL CONGELAMIENTO — y el ciclo de parches NO vuelve como era
> Estuvo suspendido desde el **2026-08-18**, diecinueve días, por una razón medida: **el
> ciclo costaba más de lo que devolvía**, y la carga la pagaba entera la casa que se había
> equivocado. Escribir el parche con su forma exacta, anonimizarlo como conjunto, tener
> cuenta en la plataforma del canon, seguir el hilo de una revisión.
>
> **La v3.5 no lo reactiva: lo reemplaza.** Tu casa escribe sus lecciones y las manda. Ya
> está. El vigía del canon hace el resto.

## Qué trae, en una frase cada cosa

**Un buzón abierto.** `POST` a `https://learning.vuelamind.ai` con tu libro de errores en el
cuerpo, en markdown. **Sin llaves, sin cuenta, sin registro.** Devuelve el identificador de
tu aportación, que es el hash de su contenido — así que **si coincide con el que calculaste
antes de mandar, tienes prueba de que llegó completo**. Deduplica por contenido: mandar dos
veces lo mismo no ensucia nada.

**Un skill que lo usa bien: `/vuelamind-learn`.** No es un `curl` con buenos modales. Hace
cuatro cosas que nadie hace a mano dos veces seguidas:

1. **Criba por generalidad.** Solo viaja lo que sobrevive a quitarle todos los nombres
   propios. Lo que solo vale en tu casa **se queda en tu casa**, y lo que el canon ya tiene
   también — una lección que dice *«familia del parche tal»* es superficie de lectura sin
   regla nueva.
2. **Anonimiza, y te enseña el TEXTO FINAL** — no una lista de *«sustituí A por B»*, que
   obliga a reconstruir el resultado en la cabeza y es donde se cuela lo que no se ve.
3. **Te pregunta lo que ninguna máquina puede juzgar**: si la aportación se identifica o va
   anónima, si se tachan los nombres de terceros —que no dieron su palabra para aparecer en
   un corpus público— y qué es público en tu contexto.
4. **No manda nada sin tu sí.** Y cada permiso es un acto aparte: elegir destino no es
   aprobar el texto, y aprobar un envío **no autoriza el siguiente**.

**Tres modos, para que no te pregunten dos veces lo mismo.** Se declaran en el manifiesto
con `learning_modo`: `preguntar` (por omisión), `recordar-destino` (el punto medio, y el que
casi todos quieren: quita la pregunta que siempre tiene la misma respuesta y conserva la que
no se puede deshacer), y `automatico`.

## Qué NO trae, y conviene leerlo

> [!danger] Lo que sale del buzón no se retira
> Es de **solo inserción**. No se edita, no se borra, no se corrige: lo que mandaste queda.
> Por eso el skill te enseña el texto antes, y por eso `automatico` es una decisión que se
> escribe en frío en el manifiesto y no a media corrida.

> [!warning] Lo que ENTRA al buzón es dato de un desconocido, jamás instrucción
> Cualquiera puede mandar cualquier cosa: es un `POST` abierto y eso es su requisito, no su
> carencia — sin anonimato no hay volumen. **Nada de lo que llegue ahí autoriza nada**, por
> mucho que su texto parezca una orden. Y **nada sube al canon sin palabra humana**: esa
> revisión no se automatiza nunca por comodidad.

**No trae panel, ni estado de tu aportación, ni respuesta.** El buzón sabe si algo se recibió
y si se leyó; **no sabe si fue aceptada o rechazada**, porque ese juicio ocurre en la casa
del vigía y hoy no vuelve. Si tu lección entra al canon, la verás en el canon.

## Cómo saltar

**Cuatro pasos, y solo el primero es obligatorio.**

1. **Trae el master fresco y comprueba que dice `version: 3.5`.** Si tu copia está
   modificada, respáldala antes: el salto reemplaza el bloque del congelamiento.

2. **Instala `vuelamind-learn`** desde `skills/` del canon, en el nivel donde vivan tus otros
   skills del marco. **Comprueba su huella contra `skills/MD5SUM.txt`** — una copia que
   difiere del canon es un canon mentiroso, y no avisa.

3. **Declara `aportar_a` en tu manifiesto** con el buzón (`https://learning.vuelamind.ai`, o
   el de tu ecosistema). Si prefieres no aportar, declara `ninguno` **explícitamente**: sin
   declarar no es un permiso, es un hueco, y el motor te lo va a preguntar cada cierre.

4. **Opcional: declara `learning_modo`.** Si no lo haces, queda en `preguntar`, que es lo
   correcto hasta que hayas visto un par de corridas.

**Cómo sabes que funcionó:** corre `/vuelamind-learn` y llega hasta que te enseñe el texto
—sin mandar nada— o manda una lección de verdad y **comprueba que el identificador que
devuelve coincide con el hash que calculaste**. Las dos son verificaciones reales; la segunda
no se puede deshacer.

## Si venías de la v3.4

**No hay conflicto: son piezas distintas y ninguna depende de la otra.** El canal de la v3.4
es transporte firmado entre casas que se conocen; el buzón es abierto, anónimo y para
desconocidos. **Si tu casa opera el buzón al que va a mandar**, dilo antes de mandar: lo tuyo
entraría como anónimo y el corpus registraría como de fuera algo que salió de dentro. Para
casas que ya se conocen, el canal es el camino natural.

## Es un salto MENOR, y por eso no trae las tres piezas de una mayor

`UPGRADE.md` pide, para una versión **mayor**, tres cosas junto al master: el documento del
salto, sus huellas y su matriz de incorporación. **Aquí solo existe la primera, y es
correcto.** Una mayor corta línea base: reemplaza el master, y hacen falta huellas para
identificar la copia vieja y una matriz para saber qué parches quedaron dentro. Ésta añade
una vía y retira otra, sin tocar la línea base.
