---
title: Salto menor a v3.18.0 — la entrevista marca su tramo, y la lista de papeles
tipo: plantilla ejecutable
para: dominios en la v3.17.0
---

> [!note] De dónde tienes que venir
> **De la v3.17.0.** Desde una versión anterior, corre primero `UPGRADE_v3.17.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.18.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.18.0`. Dos códigos nuevos: `vuelamind:entrevista <tramo>` al final de cada mensaje que pregunta en la entrevista, y `vuelamind:entrevista-fin` en el que la termina. Los tramos son fijos: `idioma`, `nace`, `A`, `B`, `C`, `D`, `F`. Un código puede llevar un argumento | Traerlo (paso 1) |
| `MARCO_Inicial.md` | La sección **«Los papeles de un agente»**: la lista cerrada de papeles con su documento (`master`, `vigia`). Una herramienta que ofrece papeles los lee de ahí | Traerlo (paso 1) |
| Una herramienta que muestra la entrevista o que ofrece papeles | Puede pintar el avance con los tramos, y ofrecer solo los papeles de la lista. Si no conoce un código, no se rompe | Ajustarla, si quieres (paso 2) |
| Los skills, el manifiesto, `ALMA.md` y el vault | Sin cambios | Nada |

Un dominio ya nacido no vuelve a hacer la entrevista: para él, los dos códigos no cambian nada.

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.18.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Si una herramienta tuya muestra la entrevista u ofrece papeles**, que lea el código del final
   del mensaje con la forma que fija el master, y la tabla de papeles de la copia del canon que
   tiene el dominio.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                                   # version: 3.18.0
grep -c '^| `vuelamind:entrevista <tramo>` |' MARCO_Inicial.md          # 1
grep -c '^### Los papeles de un agente$' MARCO_Inicial.md               # 1
python3 herramientas/comprobar_skills.py; echo $?                       # todos al día, sin deriva, y 0
```
