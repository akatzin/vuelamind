---
title: Salto menor a v3.19.0 — la entrevista en voz alta
tipo: plantilla ejecutable
para: dominios en la v3.18.0
---

> [!note] De dónde tienes que venir
> **De la v3.18.0.** Desde una versión anterior, corre primero `UPGRADE_v3.18.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.19.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.19.0`. La entrevista hace **una pregunta por mensaje**: la introducción de la Fase 0 ya no dice «agrupa de tres o cuatro», y la regla vale también para las dudas del asistente. Una medición que contradice lo que el dominio supone se pregunta sola y primero | Traerlo (paso 1) |
| `MARCO_Inicial.md` | **Cinco partes de preguntas**, no seis bloques: cada parte se anuncia al abrirse. «Antes de empezar» va en su propio mensaje. Al terminar las preguntas, un aviso de cuánto tarda construir, y `vuelamind:entrevista-fin` al final del turno que construye | Traerlo (paso 1) |
| `MARCO_Inicial.md` | **En voz alta, en llano**: los términos del método son de las notas, no del chat. La presentación y la pregunta 8 se dicen sin jerga | Traerlo (paso 1) |
| `MARCO_Inicial.md` | **Cuándo va un bloque de opciones**: al elegir, `vuelamind:opciones`; al confirmar, quitar o sumar en una lista, `vuelamind:opciones-varias`. Un código cuenta solo en el último mensaje del turno | Traerlo (paso 1) |
| `MARCO_Inicial.md` | **El cierre**: los avisos de dónde vive el vault y de lo que el asistente usa de la persona, primero y solos; un mensaje final corto, con el inventario en `initPrompt.md`; y el traspaso en una línea si la herramienta abre la sesión nueva por la persona | Traerlo (paso 1) |
| Los skills, el manifiesto, los códigos, `ALMA.md` y el vault | Sin cambios | Nada |

Un dominio ya nacido no vuelve a hacer la entrevista: para él, este salto no cambia nada.

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.19.0`. Si tu copia del
   master está modificada, respáldala antes.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                                   # version: 3.19.0
grep -c 'agrupa de tres o cuatro' MARCO_Inicial.md                       # 0
grep -c '^\*\*Cuándo va un bloque de opciones\.\*\*' MARCO_Inicial.md   # 1
grep -c '^> \[!danger\] En voz alta, en llano' MARCO_Inicial.md          # 1
python3 herramientas/comprobar_skills.py; echo $?                       # todos al día, sin deriva, y 0
```
