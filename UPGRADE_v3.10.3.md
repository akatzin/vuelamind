---
title: Salto menor a v3.10.3 — prueba del aviso de versión nueva
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
| Lo demás | Sin cambios. Esta versión existe para probar que el aviso de versión nueva llega a los dominios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10.3`. Si tu copia del
   master está modificada, respáldala antes.

## Cómo sabes que funcionó

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10.3
```
