---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16 (lección 47 del libro heredado)
---

# 2026-08-16 · Un filtro por la raíz de una palabra excluye justo su negación

## Qué corrige

Un chequeo que separa lo hecho de lo pendiente busca la palabra que marca lo hecho —
*armonizado*, *aplicado*, *cerrado*— y para ser tolerante busca su **raíz**. Y la raíz está
también dentro de la negación: **«sin armonizar» contiene «armoniz»**. El filtro excluye
del reporte exactamente el caso que existía para reportar.

Es el peor modo de fallo posible para un instrumento de vigilancia: **no da error, da un
número más chico**. Un listado que dice *«siete pendientes»* cuando son ocho se lee igual
de bien, y nadie audita un chequeo que ya está funcionando.

Y tiene una asimetría cruel: el defecto **solo esconde lo pendiente**. Nunca inventa
trabajo de más, así que nunca molesta a nadie — solo tranquiliza de menos.

## Cómo se descubrió

**2026-08-16**, al bajar a código una medición que hasta entonces vivía como instrucciones
en prosa.

El instrumento reportó **siete** elementos a medio camino. El octavo —que llevaba días
declarando explícitamente *«sin armonizar»*— quedó fuera, porque su texto contenía la
misma raíz que el filtro usaba para dar algo por terminado. **La víctima fue el caso más
claro de todos**: el único que decía en voz alta que estaba pendiente.

Lo detectó una comprobación a mano de una sola fila contra la fuente, no el propio
chequeo.

## Cómo aplicarlo

> **Al filtrar por estado, exige la forma afirmativa y descarta explícitamente su
> negación.** No basta con buscar la raíz: hay que comprobar que el texto **no** venga
> precedido de *sin*, *no*, *pendiente de* o equivalente en el idioma del dominio.
>
> Y donde se pueda elegir, **mejor un campo cerrado que una frase libre**: un estado que
> solo admite valores conocidos no puede contener su propia negación.

La regla general, que va más allá de las palabras: **una subcadena no es un significado**.
Aplica igual a *«descartada»* dentro de *«no descartada»*, a *«verificado»* dentro de *«sin
verificar»*, y a cualquier búsqueda por fragmento sobre texto escrito por humanos.

**Y la comprobación barata que lo caza:** toma **una** fila del resultado y compárala a
mano contra la fuente; después toma una que **no** salió y pregunta por qué. Revisar la
salida entera no sirve — lo que falta no se ve, y por eso este defecto sobrevive.

## Cómo verificar

- **Debe pasar:** un elemento cuyo estado dice *«sin <verbo>»* aparece en el listado de
  pendientes, con su texto completo a la vista.
- **Debe seguir fallando:** un elemento cuyo estado dice *«<verbo>»* **no** aparece. Si el
  arreglo hace que salgan todos, el chequeo no se corrigió: se apagó.
- **Y la prueba que este parche añade:** el chequeo se ejercita con las dos formas —la
  afirmativa y la negada— **antes** de darlo por bueno. Probarlo solo con el caso que
  funciona es cómo llegó a existir el defecto.
