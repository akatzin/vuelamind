---
title: Salto menor a v3.16.0 — el manifiesto declara los paquetes, y el export se lleva solo la declaración
tipo: plantilla ejecutable
para: dominios en la v3.15.0
---

> [!note] De dónde tienes que venir
> **De la v3.15.0.** Desde una versión anterior, corre primero `UPGRADE_v3.15.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.16.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.16.0` y la clave `paquetes` en el contrato del manifiesto: los paquetes premium instalados, `<paquete> <versión>` | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | La misma clave en su tabla del contrato | Reinstalarlo (paso 2) |
| `skills/vuelamind-export.md` | Deja fuera `.claude/<paquete>/` y `.claude/commands/<paquete>-*.md` de cada paquete declarado, y lleva su nombre y versión en `paquetes` de `MIGRACION.md`. Pregunta por una carpeta `.claude/vmp-*/` sin declarar | Reinstalarlo (paso 2) |
| El manifiesto | La clave es opcional | Nada, salvo que tengas un paquete instalado (paso 3) |
| Los demás skills y `ALMA.md` | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.16.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala los dos skills**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Si el dominio tiene un paquete premium instalado** (una carpeta `.claude/vmp-*/`), agrega al
   manifiesto la fila `paquetes` con su nombre y su versión, que dice su `PAQUETE.md`:

   ```
   | `paquetes` | `vmp-watchers 0.1.0` |
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                       # version: 3.16.0
grep -c '^| `paquetes` |' MARCO_Inicial.md                  # 1
grep -c '^| `paquetes` |' skills/vuelamind-commit.md        # 1
grep -c '^paquetes:' skills/vuelamind-export.md             # 1
python3 herramientas/comprobar_skills.py; echo $?           # todos al día, sin deriva, y 0
```
