---
title: Salto menor a v3.11.0 — varias instancias: el registro en el manifiesto y un cierre a la vez
tipo: plantilla ejecutable
para: dominios en la v3.10.4
---

> [!note] De dónde tienes que venir
> **De la v3.10.4.** Desde una versión anterior, corre primero `UPGRADE_v3.10.4.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.11.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.11.0`. Entra la clave `instancias` en el contrato del manifiesto (Fase 1.3), y el cierre con candado cuando escriben dos o más instancias (Fase 3) | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | Con dos o más instancias que escriben, toma `<proyecto>/.cierre.lock/` antes de medir y lo suelta al final | Reinstalarlo (paso 2) |
| `skills/vuelamind-join.md` | La instancia que se suma agrega su fila en `## instancias` | Reinstalarlo (paso 2) |
| El manifiesto | Sección nueva y opcional: `## instancias` | Solo con más de una instancia (paso 3) |
| Los demás skills y `ALMA.md` | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.11.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala los dos skills**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md skills/vuelamind-join.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Si en el dominio trabaja más de una instancia**, agrega al manifiesto una fila por cada una:

   ```markdown
   ## instancias

   | nombre | acceso | carril | dónde |
   |---|---|---|---|
   | <nombre> | escribe | <de qué se ocupa> | <máquina o carpeta> |
   ```

   Si el proyecto está en git, agrega `.cierre.lock/` a su `.gitignore`. Si la carpeta se
   sincroniza entre máquinas, exclúyela de la sincronización. Con una sola instancia, este paso
   no se hace.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.11.0
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
grep -A4 '^## instancias' <tu manifiesto>              # solo si hiciste el paso 3
```
