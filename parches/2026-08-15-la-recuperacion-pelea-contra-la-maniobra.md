---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16, en el nucleo epistemico
---

# 2026-08-15 · Antes de «recuperar», pregunta qué maniobra está en curso

## Qué corrige

Un servicio caído dispara el reflejo de levantarlo. Pero **un estado anómalo puede ser
la intención del operador a medio camino** — un apagado en curso, una migración, un
mantenimiento. Recuperarlo entonces no repara: **pelea contra la maniobra**, y el
sistema queda peor que caído — medio detenido, con piezas nuevas encima de un
desmontaje.

## Cómo se descubrió

**2026-08-15.** El operador detenía el arreglo de discos de su NAS (quería silencio:
visitas durmiendo al lado). El asistente, en otra tarea, encontró el daemon de
contenedores apagado y lo *"rescató"* — dos veces — montando la imagen y relanzando
el stack completo, **en medio del apagado**. Consecuencias en cadena: el apagado quedó
atorado reintentando, y un contenedor relanzado sin su almacenamiento debajo fabricó
un directorio fantasma que bloqueó el desmontaje **diez horas**. La causa raíz del
atorón original era del operador; cada "recuperación" del asistente lo empeoró.

## La regla

> **Un servicio abajo no es un hecho: es una pregunta.** Antes de levantarlo,
> responder DOS cosas con fuentes, no con reflejos: **¿el estado del orquestador
> dice que hay una transición en curso?** (el gestor del sistema, no el servicio),
> y **¿el operador está maniobrando?** — que se pregunta, no se adivina. Si
> cualquiera de las dos dice maniobra: **las manos quietas**, y estorbar menos.

Es pariente de dos lecciones que ya existen — *acusarse sin medir también es inferir*
y *el orden de toda respuesta* — pero cubre lo que ninguna nombra: la intención
**en curso** como estado del sistema que también se mide.

## Cómo verificar

**El que fallaba:** servicio abajo + transición del orquestador en curso → el
asistente lo reporta y pregunta, sin tocar. **El que DEBE seguir fallando:** servicio
abajo sin transición ni maniobra declarada → ahí sí se levanta; quedarse quieto ante
una caída real es el error opuesto.
