---
title: Salto menor a v3.17.0 — los entregables viven en el vault, en artefactos/
tipo: plantilla ejecutable
para: dominios en la v3.16.0
---

> [!note] De dónde tienes que venir
> **De la v3.16.0.** Desde una versión anterior, corre primero `UPGRADE_v3.16.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.17.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.17.0`. La topología suma `artefactos/` y la quinta regla: todo entregable vive ahí, con fila en `artefactos/0_Artefactos.md`, y lo publicado conserva aquí su original | Traerlo (paso 1) |
| `skills/vuelamind-export.md` | Cuenta `artefactos/0_Artefactos.md` entre las piezas (`artefactos_indice`), y un entregable fuera del vault como regla violada | Reinstalarlo (paso 2) |
| El vault | La carpeta `artefactos/` con su índice | Crearla (paso 3) y traer los entregables (paso 4) |
| El manifiesto, los demás skills y `ALMA.md` | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.17.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Crea `artefactos/` en el vault**, con su índice. `<vault>` es el que declara el manifiesto:

   ```sh
   mkdir -p <vault>/artefactos
   ```

   Y dentro, `0_Artefactos.md`:

   ```markdown
   # Artefactos

   Lo entregado: reportes, PDF, imágenes, páginas. Un archivo por entregable y una fila por
   archivo. Lo publicado conserva aquí su original. Al reemplazarse, la fila lo declara.

   | Artefacto | Qué es | Para quién | Dónde se publicó | Nota dueña |
   |---|---|---|---|---|
   ```

4. **Trae los entregables que vivan fuera del vault**, con el sí de la persona: lista los que
   haya en el proyecto o en otras carpetas del dominio, muévelos a `artefactos/` y dales su fila.
   Lo que los generaba —un script, un comando— se cambia en el mismo acto para que escriba en
   `artefactos/`; si no se puede ahora, la fila lo dice y queda un pendiente.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                       # version: 3.17.0
grep -c 'artefactos/0_Artefactos.md' MARCO_Inicial.md       # 1 o más
grep -c '^  artefactos_indice:' skills/vuelamind-export.md  # 1
test -f <vault>/artefactos/0_Artefactos.md && echo ok        # ok
python3 herramientas/comprobar_skills.py; echo $?           # todos al día, sin deriva, y 0
```
