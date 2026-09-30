# Un mensaje a medio turno: hoy es un segundo proceso sobre la misma sesión

**Estado: diseño, sin construir. Nace de un caso visto por Akatzin el 2026-09-30 en la
página del puente, con otra casa (Zero) del otro lado.**

## El caso

Se manda un mensaje largo; segundos después, una corrección de cinco caracteres
(`20:15*`, por `20:10`). El agente termina el primer turno **con el dato viejo** —«propago
a todos los archivos y sincronizo»— y luego atiende la corrección **como un encargo
nuevo**: rehace el plan entero (57 s), sin decir que la primera versión ya está aplicada,
y va a poner la segunda encima de la primera.

En Claude Code interactivo eso no ocurre: un mensaje enviado a medio turno le llega al
modelo *dentro* del turno, con la etiqueta *«the user sent a new message while you were
working»*, y el modelo lo incorpora antes de terminar. El puente no tiene ese carril.

## Lo que el puente hace hoy — MEDIDO sobre `main` en `0ad70c7`

| Capa | Hecho | Dónde |
|---|---|---|
| Transporte | Las tres rutas (`/messages`, `/stream`, `/deliver`) lanzan un proceso nuevo `claude -p --input-format stream-json --output-format stream-json --resume <id>` y le escriben **un solo** mensaje por `stdin`. El modo de entrada admite más; el puente no los manda | `run_turn`, `stream_turn`, `deliver_turn` |
| Servidor | `esta_en_vuelo(nombre)` existe y **solo lo consulta el endpoint de recuperación**, para distinguir «todavía no» de «ya nunca». Ningún POST lo mira | def en l. 285; único uso en l. 1004 |
| Servidor | Por tanto, un segundo mensaje a una sesión con turno vivo lanza **un segundo `claude --resume` concurrente sobre el mismo `session_id`**. El segundo arranca con el transcript tal como estaba —no ve el trabajo del primero— y los dos escriben el mismo archivo | consecuencia de lo anterior |
| Página | `send()` deshabilita el botón hasta que acaba el stream; `select()` lo **vuelve a habilitar sin mirar** si hay stream. Una segunda pestaña, otro dispositivo o `/deliver` no tienen cerrojo | `send()` l. 2241–2245; `select()` l. 1228 |

**El cerrojo está en el cliente, y un cerrojo en el cliente es una convención.** El
servidor es el único sitio donde «un turno por sesión» puede ser verdad.

## Tres capas, y solo dos son del puente

1. **Que la corrección llegue a tiempo** — antes de que el turno propague. Es transporte.
2. **Que nunca corran dos turnos sobre una sesión** — es el servidor.
3. **Que un delta se aplique sobre lo hecho y no se rehaga** — es conducta del agente.
   El transporte no la arregla; lo que sí hace es que la corrección exista *antes* de
   que haya algo que rehacer.

Este diseño cubre 1 y 2. La 3 va a la carpeta de lecciones, no a código.

## Tres caminos para el segundo mensaje

**A · Rechazar (409 «turno en vuelo»).** Mínimo y seguro: elimina la concurrencia hoy con
diez líneas —consultar `esta_en_vuelo` en los tres POST—. No resuelve el caso: la
corrección rebota y el turno sigue con el dato viejo. **Es el primer paso, no el destino.**

**B · Encolar.** El segundo mensaje espera al primero y corre después. Resuelve la
concurrencia, no el caso: llega igual de tarde. Y una cola es estado nuevo que el
puente tiene que contar, drenar y explicar cuando muere a medias.

**C · Inyectar en el turno vivo. ADOPTADO como destino.** El CLI ya está corriendo en el
único modo de entrada que admite más de un mensaje. El puente conserva `stdin` abierto
mientras el turno vive y, si llega otro mensaje a esa sesión, lo escribe ahí. El modelo lo
recibe a medio turno, como en la terminal.

**Lo que C cambia y hay que decir:** hoy el turno termina cuando el CLI termina, y el CLI
termina porque `stdin` se cerró tras el único mensaje. Con `stdin` abierto, **quién cierra
el turno pasa a ser el puente**, no el CLI — una pieza que hoy hace un trabajo pasaría a
hacer dos (transportar y delimitar). Es exactamente la familia de defecto que esta casa
tiene medida, y por eso se declara aquí en vez de descubrirse después.

**Orden:** A ahora, porque cuesta nada y cierra la carrera. C cuando la premisa de abajo
esté medida. B no.

## Lo que esto NO resuelve

- **La conducta del delta.** Aunque `20:15*` llegue a tiempo, el agente decide qué hacer
  con él. Un mensaje inyectado con la etiqueta de «llegó a medio turno» le da la pista;
  no le da la disciplina.
- **`/deliver`.** Existe para *despertar y soltar*: confirma que el turno arrancó, no lo
  acompaña. Con A, un `/deliver` sobre una sesión viva recibe 409 y quien dispara sabe
  que no entregó — hoy cree que sí y lanza el segundo proceso.

## Premisas a medir antes de construir C

1. **Qué hace el CLI en `-p --input-format stream-json` con un segundo mensaje `user`
   escrito a medio turno**: ¿lo incorpora al turno (como interactivo), lo encola para
   después del `result`, o lo ignora? Un experimento, un turno, se mide una vez.
2. **Qué pasa hoy con dos `--resume` concurrentes sobre el mismo `session_id`**: si el
   transcript se corrompe, se pierde un turno o se duplica. Es lo que ya ocurrió en el
   caso; falta verlo con el archivo delante.

## Cómo se comprueba que quedó bien

No basta con que la corrección «funcione». Los negativos:

1. dos POST a la misma sesión con 200 ms de diferencia → **un solo** proceso `claude`
   vivo, medido con `ps`, no con el log;
2. el segundo POST, con A, → `409` y el cuerpo dice *turno en vuelo*;
3. con C, el segundo mensaje aparece en el transcript **dentro** del turno del primero,
   antes de su `result`, y no como turno aparte;
4. `select()` deja de rehabilitar el botón mientras hay stream — y aunque lo hiciera,
   el servidor ya no deja pasar.
