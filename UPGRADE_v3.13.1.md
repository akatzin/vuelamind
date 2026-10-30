---
title: Salto menor a v3.13.1 — tras el cierre, sesión limpia y carga
tipo: plantilla ejecutable
para: dominios en la v3.13.0
---

> [!note] De dónde tienes que venir
> **De la v3.13.0.** Desde una versión anterior, corre primero `UPGRADE_v3.13.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.13.1

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.13.1`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | La última línea del reporte del cierre dice: *«Lo de esta sesión ya está en el vault. Si sigues trabajando: `/clear` y luego `/vuelamind-load`.»* | Reinstalarlo (paso 2) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.13.1`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.13.1
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
