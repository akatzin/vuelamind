---
title: Salto menor a v3.13.2 — la línea final del cierre, solo al terminar
tipo: plantilla ejecutable
para: dominios en la v3.13.1
---

> [!note] De dónde tienes que venir
> **De la v3.13.1.** Desde una versión anterior, corre primero `UPGRADE_v3.13.1.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.13.2

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.13.2`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | La línea *«Lo de esta sesión ya está en el vault…»* sale solo cuando el cierre terminó: el paso 4 escrito, el validador otra vez en verde, la instantánea renovada y el candado suelto. Después de ella no va nada, tampoco una pregunta | Reinstalarlo (paso 2) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.13.2`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.13.2
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
