---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16 (ya vivía en Fase 0: «La regla de corte: dos veces sin respuesta, y se construye»; solo faltaba declararlo)
---

# La entrevista necesita una regla de corte

## Qué corrige

**El método sabe qué hacer cuando alguien dice *"sáltalo, no sé todavía"*, y no
sabe qué hacer cuando simplemente NO CONTESTA.** El hueco declarado depende de que
la persona lo declare; si no llega respuesta de ninguna clase, la Fase 0 no tiene
salida y el asistente se queda entre dos malas opciones — preguntar en bucle, o
inventar.

## Cómo se descubrió

**2026-08-14**, en la inicialización de un dominio nuevo.

La persona contestó un bloque de respuestas y, a partir de ahí, **volvió a enviar
exactamente el mismo bloque ocho veces**, mientras tres preguntas nuevas —las
entidades del dominio, la lectura de una respuesta ambigua sobre confidencialidad,
y el nombre del asistente— quedaban sin contestar en ninguna de las ocho.

El asistente hizo lo correcto por su cuenta —construyó con lo respondido y anotó lo
demás como huecos declarados con fecha— **pero no porque el método se lo dijera**:
la Fase 0 dice *"no se inventa ni se rellena con lo que parezca razonable"*, y ahí
se detiene. No dice cuántas veces se vuelve a preguntar, ni cuándo se deja de
preguntar y se construye.

Las dos salidas que el vacío deja abiertas son malas y ninguna se siente como
error:

- **Preguntar otra vez** se siente como rigor —*todavía no tengo la respuesta*— y
  puede repetirse indefinidamente. Cada repetición consume la paciencia de quien
  contesta y no produce nada.
- **Rellenar con lo razonable** se siente como servicio, y es exactamente lo que el
  método prohíbe: una entidad inventada se lee después con la misma confianza que
  una relevada.

Es de la familia del ítem 39 —*un paso cuyo resultado no se reporta es un paso
opcional*—: aquí el texto es enfático (*"no se inventa"*) y **el mecanismo que
decide cuándo parar no existe**.

## Cómo aplicarlo

Añadir a la Fase 0, junto a las tres salidas que se le ofrecen a quien contesta,
una **cuarta que es del asistente**:

> **La regla de corte.** Una pregunta se hace, y si no llega respuesta se hace una
> segunda vez, reformulada. **A la tercera no se pregunta: se construye sin ella y
> se escribe el hueco declarado con su fecha**, diciendo en voz alta qué queda sin
> contestar y qué costará más adelante. No preguntar más **no es abandonar la
> pregunta** — el hueco sigue vivo en la cola y vuelve a presentarse en cada
> arranque, que es donde le toca aparecer.
>
> Y se dice explícitamente: *"esto lo pregunté dos veces, sigo sin respuesta, lo
> dejo anotado y sigo"*. Callarlo convierte un hueco declarado en un olvido.

**Dónde toca la plantilla:** Fase 0, en el bloque *"Antes de empezar — lo que hay
que decirle a quien va a contestar"*, como contraparte de las tres salidas; y una
línea en el *Resumen de la inicialización*, que ya exige una lista explícita de lo
que no se pudo verificar — las preguntas agotadas pertenecen a esa lista.

## Cómo verificar

1. **El caso que debe pasar ahora:** una inicialización donde una pregunta quede
   sin contestar dos veces debe terminar **igual de completa** —con el vault
   construido y el hueco anotado con fecha— y el reporte final debe nombrar la
   pregunta agotada. Antes del parche, ese final dependía del criterio del
   asistente y no del método.
2. **El caso que debe SEGUIR fallando:** un asistente que rellene la respuesta que
   falta con algo verosímil tiene que seguir estando en falta. La regla de corte
   autoriza a **seguir sin la respuesta**, nunca a suponerla — si al aplicarla
   aparecen entidades que nadie nombró, el parche se aplicó mal.
3. **Y comprobar que el hueco reaparece:** abrir la sesión siguiente y verificar
   que el arranque vuelve a presentar la pregunta pendiente. Un hueco que se anota
   y no vuelve a ofrecerse es un olvido con mejor redacción.
