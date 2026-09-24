# Soñar: las relaciones que faltan

**Estado: en el apéndice de la ruta crítica como V4·B, sin construir.**

## Qué es

Un proceso largo que lee el vault entero —empezando por lo recién tocado y terminando en
los nodos aislados— descubriendo las relaciones que faltan, con bitácora propia.

## Por qué el orden es la pieza

`vecinas` contesta **quién enlaza** una nota. Éste contesta **qué debería enlazarla y no lo
hace**, que hoy no lo mira ningún instrumento. Y **un nodo aislado es invisible para
`vecinas` por construcción**, porque nadie lo enlaza.

Medido sobre un vault real de 119 notas: **60 sin ninguna cita**.

## No es idea nueva

La escalera del 2026-08-21 ya pedía *«un sugeridor de enlaces tipo GraphRAG como chequeo
del validador — estas dos notas comparten vocabulario y no se enlazan»*. Lo que se añade es
**el recorrido** y **la bitácora**.

## Dos restricciones, las dos de errores medidos aquí

- **Lo que proponga nace INFERIDO**, marcado y fechado. Un enlace inventado que entra sin
  marca se hereda como si lo hubiera puesto una mano.
- **Su bitácora tiene que poder registrar un sueño que no encontró nada.** Un registro que
  solo sabe anotar aciertos siempre dice que funciona.

## Cómo se acepta

Las relaciones se proponen **localmente** y el usuario las acepta o rechaza **en el arranque
siguiente**, al terminar el barrido. No se escriben solas.

## Depende de

`#101` (`vecinas`) y se lleva mejor con el grafo del `#116`.
