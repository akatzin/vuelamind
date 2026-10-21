---
title: Salto menor a v3.10.2 — vuelamind-export declara los alias de las rutas
tipo: plantilla ejecutable
para: dominios en la v3.10.1
---

> [!note] De dónde tienes que venir
> **De la v3.10.1.** Desde una versión anterior, corre primero `UPGRADE_v3.10.1.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.10.2

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.10.2`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `skills/vuelamind-export.md` | Si una ruta del manifiesto no existe en esta máquina y la pieza está en otra ruta, la del manifiesto va en `alias` de su entrada de `fuera`, y la raíz con que otra máquina nombra el proyecto, en `raiz_alias`. El barrido de rutas busca también esos alias. `MIGRACION.md` sigue en `formato: 1` | Reinstalarlo (paso 2) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10.2`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10.2
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
