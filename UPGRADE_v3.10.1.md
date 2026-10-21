---
title: Salto menor a v3.10.1 — comprobar_skills.py sale con 1 si falta un skill
tipo: plantilla ejecutable
para: dominios en la v3.10.0
---

> [!note] De dónde tienes que venir
> **De la v3.10.0.** Desde una versión anterior, corre primero `UPGRADE_v3.10.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.10.1

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.10.1`. **Ninguna regla cambia** | Traerlo (paso 1) |
| `herramientas/comprobar_skills.py` | Sale con 1 también si un skill del inventario no está instalado; antes, solo si difería. Un instalado que el inventario no lista no cambia la salida | Nada: viene con el canon |
| Los skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10.1`. Si tu copia del
   master está modificada, respáldala antes.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10.1
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
```
