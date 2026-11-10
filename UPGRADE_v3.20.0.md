---
title: Salto menor a v3.20.0 — /vuelamind-chat, las salas con una llave
tipo: plantilla ejecutable
para: dominios en la v3.19.0
---

> [!note] De dónde tienes que venir
> **De la v3.19.0.** Desde una versión anterior, corre primero `UPGRADE_v3.19.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.20.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.20.0` | Traerlo (paso 1) |
| `herramientas/salas.py` | Nuevo: el cliente de las salas, conversaciones entre personas y sus agentes. Lee la llave del llavero o de un archivo que solo su persona lee, nunca de la línea de órdenes; `buzon` enseña sin acusar y `leidos` acusa lo enseñado | Nada: viene con el canon |
| `skills/vuelamind-chat.md` | Nuevo: configurar la llave, listar las salas, pedir entrar, mandar, leer el buzón y acusar lo leído | Instalarlo (paso 2) |
| `skills/vuelamind-load.md` | Paso 4c: si el dominio entra a las salas, una línea con los mensajes sin leer. No los lee ni los acusa | Reinstalarlo (paso 2) |
| El manifiesto, los códigos, `ALMA.md` y el vault | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.20.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Instala `vuelamind-chat` y reinstala `vuelamind-load`**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-chat.md skills/vuelamind-load.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Solo si este dominio va a entrar a las salas:** corre `/vuelamind-chat`, que empieza por
   configurar. La URL y la llave las da la persona, y la llave la guarda ella en su terminal.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                 # version: 3.20.0
python3 herramientas/salas.py aviso; echo $?          # sin salas configuradas: nada, y 0
python3 herramientas/comprobar_skills.py; echo $?     # todos al día, sin deriva, y 0
```
