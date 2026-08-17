---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16 (lección 43 del libro heredado)
---

# 2026-08-16 · Un orden de fusión no es una revisión de coherencia

## Qué corrige

Cuando llegan varios cambios juntos y el asistente entrega **el orden en que aplicarlos**,
quien lo recibe lee ese orden como **el resultado de haberlos revisado**. Y casi nunca lo
es: un orden razonado sale de mirar **dependencias** —qué cambio necesita el vocabulario o
la pieza de cuál— y eso es una pregunta mucho más chica que la coherencia.

El daño no está en el orden, que suele ser correcto. Está en lo que el orden **hace
suponer**: un listado con criterio se lee como un veredicto, y quien lo ejecuta deja de
preguntar lo que habría preguntado ante una lista sin criterio.

## Cómo se descubrió

**2026-08-16**, en el primer ciclo real de un dominio que recibe cambios y los publica a
un repositorio compartido.

Ante *«aplícalos todos»*, el asistente entregó la lista de pasos con su orden y una
dependencia bien identificada. El responsable los aplicó. **Solo entonces** pidió la
revisión de coherencia — y al hacerla aparecieron tres cosas que habrían cambiado su
decisión: que el documento maestro **ni siquiera mencionaba** un término que su propia
portada pública anunciaba; que ese término vivía en **diez archivos** y no en uno, así que
el costo era diez veces el estimado; y que uno de los cambios publicaba una regla **más
estricta que la práctica** de la casa que lo proponía.

La regla que lo habría evitado ya estaba escrita en el método —*la revisión va **antes**
del merge*— y se aplicó al revés. No por olvido: porque **entregar el orden se sintió como
haber revisado**.

## Cómo aplicarlo

Antes de entregar cualquier lista de aplicación, contestar **por escrito** tres preguntas,
y entregarlas con la lista:

> 1. **¿Se contradicen entre sí?** Dos cambios correctos por separado pueden negarse el
>    uno al otro, o tocar la misma sección con instrucciones incompatibles.
> 2. **¿Contradicen lo ya publicado?** Un cambio puede ser cierto y dejar el corpus
>    diciendo dos cosas a la vez — y eso no lo detecta ningún chequeo, porque los
>    conteos cuadran y los enlaces resuelven.
> 3. **¿Contradicen lo que esta casa hace?** Publicar una regla que la propia
>    implementación de referencia no cumple le quita autoridad a todo lo demás.

**Y si alguna no está contestada, decirlo dentro de la lista.** Ésa es la mitad que
importa: quien ejecuta va a suponer que sí lo está, y la suposición es razonable.

**El orden de dependencias sigue haciendo falta** — no lo sustituye, lo acompaña. Lo que
no se vale es que ocupe su lugar.

## Cómo verificar

- **Debe pasar:** una entrega de varios cambios llega con sus tres preguntas contestadas,
  y quien decide puede señalar cuál de ellas le hizo cambiar de opinión.
- **Debe seguir fallando:** una lista que solo trae el orden —aunque el orden sea
  correcto— se marca **incompleta**. Si un listado bien ordenado y sin revisión se lee
  igual que uno revisado, el parche no agregó nada.
- **Y el caso tramposo:** una revisión entregada **después** de que el cambio se aplicó no
  cuenta como hecha. Su valor era cambiar una decisión que ya se tomó.
