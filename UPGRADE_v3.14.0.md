---
title: Salto menor a v3.14.0 — el cierre termina con un código, no con una frase
tipo: plantilla ejecutable
para: dominios en la v3.13.2
---

> [!note] De dónde tienes que venir
> **De la v3.13.2.** Desde una versión anterior, corre primero `UPGRADE_v3.13.2.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.14.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.14.0`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `skills/vuelamind-commit.md` | El cierre terminado acaba en dos líneas: la frase para la persona, en el idioma del dominio, y el código `vuelamind:cierre-ok`, sola en su línea, sin formato y sin traducir. La frase deja de ser fija | Reinstalarlo (paso 2) |
| Una herramienta que detecta el fin del cierre | Busca el código. Mientras haya dominios en la v3.13.1 o la v3.13.2, acepta también la frase *«Lo de esta sesión ya está en el vault.»* | Ajustarla, si tienes una (paso 3) |
| Los demás skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.14.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala el skill**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Si una herramienta tuya lee el fin del cierre**, que busque `^vuelamind:cierre-ok$` y acepte
   la frase vieja mientras quede algún dominio en la v3.13.1 o la v3.13.2.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.14.0
grep -c '^    vuelamind:cierre-ok$' skills/vuelamind-commit.md   # 1
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
