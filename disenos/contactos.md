# Lógica de contactos

**Estado: diseñado, sin construir.**

## Qué es

Cómo una casa le dice a otra que existe y dónde alcanzarla.

## Dos tipos de invitación

**Agente** — nombre, tipo, y dónde alcanzar su canal.

**Colmena** — lo mismo, **más su objeto**: qué entra y qué no entra.

## Por qué la colmena manda su objeto y no entrevista

Decidido el 2026-09-24, enmendando el modelo del 22 de agosto. La razón es de
mantenimiento: con un acta por casa, mover el objeto obliga a re-entrevistar a N casas, y
**lo que cuesta N entrevistas no se actualiza nunca**.

La entrevista **no es el diseño: es la escalada**, y su disparador está escrito antes de
necesitarlo — que el master rechace más de lo que adopta, o que dos casas propongan cosas
incompatibles creyendo las dos que cumplían.

## Dos exigencias sobre el objeto

- **Tiene que poder decir qué NO incluir.** Una mente en varias colmenas tiene su borde de
  confidencialidad justo ahí.
- **Estructura, no prosa libre**: temas · qué reportar · forma · fuera de alcance · para
  esta audiencia. *Con prosa se argumenta; con estructura se comprueba.*

## Depende de

`propuesta` en el cliente, y el canal en el contenedor.
