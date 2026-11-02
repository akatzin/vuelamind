---
title: Salto menor a v3.15.0 — las opciones, como código cuando no hay AskUserQuestion
tipo: plantilla ejecutable
para: dominios en la v3.14.0
---

> [!note] De dónde tienes que venir
> **De la v3.14.0.** Desde una versión anterior, corre primero `UPGRADE_v3.14.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.15.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.15.0` y la sección **«Los códigos que leen las herramientas»**: la lista completa de los códigos `vuelamind:` (`cierre-ok`, `opciones`, `opciones-varias`), su forma y el bloque de opciones | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | Paso 3: si la herramienta no tiene `AskUserQuestion`, el «Sí, continúa / No, tengo comentarios» va en un bloque `vuelamind:opciones` al final del mensaje | Reinstalarlo (paso 2) |
| Una herramienta sin `AskUserQuestion` que muestra lo que escribe el agente | Puede dibujar botones con el bloque. Si no lo reconoce, la pregunta se lee como texto | Ajustarla, si quieres (paso 3) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.15.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Si una herramienta tuya muestra lo que escribe el agente y no tiene `AskUserQuestion`**, que
   lea los bloques del final del mensaje con la forma que fija el master y dibuje una opción por
   botón, más «Otro».

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                                  # version: 3.15.0
grep -c '^### Los códigos que leen las herramientas$' MARCO_Inicial.md # 1
grep -c '^    vuelamind:opciones$' skills/vuelamind-commit.md          # 1
python3 herramientas/comprobar_skills.py; echo $?                      # todos al día, sin deriva, y 0
```
