---
title: Salto menor a v3.10.3 — vuelamind-export marca los nombres como UTF-8 y amplía se_ejecuta
tipo: plantilla ejecutable
para: dominios en la v3.10.2
---

> [!note] De dónde tienes que venir
> **De la v3.10.2.** Desde una versión anterior, corre primero `UPGRADE_v3.10.2.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.10.3

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.10.3`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `skills/vuelamind-export.md` | Los nombres del zip que no son ASCII van marcados como UTF-8: `zip` y `ditto` de macOS no los marcan. El paso 8 compara por nombre, no por conteo, y en NFC. `se_ejecuta` lista todo archivo bajo cualquier `.claude/` menos el manifiesto, y `proyecto/.mcp.json`. `MIGRACION.md` sigue en `formato: 1` | Reinstalarlo (paso 2) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10.3`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10.3
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
