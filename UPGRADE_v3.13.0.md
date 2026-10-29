---
title: Salto menor a v3.13.0 — la escala de procedencia pasa a cinco marcas
tipo: plantilla ejecutable
para: dominios en la v3.12.1
---

> [!note] De dónde tienes que venir
> **De la v3.12.1.** Desde una versión anterior, corre primero `UPGRADE_v3.12.1.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.13.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.13.0`. La escala de procedencia (Fase 2 §1) tiene cinco marcas: **medido** (lo viste tú, con instrumento), **atestiguado** (lo viste tú, sin instrumento), **citado** (alguien atestiguó que lo vio, con su fuente), **inferido** y **aportado** | Traerlo (paso 1) |
| Los README | La lista de marcas dice las cinco, en los diez idiomas | Nada |
| Los skills, `ALMA.md` y el manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.13.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Si tu dominio ya usaba una marca propia para lo que se presencia sin instrumento**, cámbiala
   por `atestiguado`. Si tu validador o tus notas enumeran las marcas, agrega la quinta. Lo ya
   escrito con cuatro marcas sigue siendo válido.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.13.0
grep -c 'cinco marcas' MARCO_Inicial.md                # 1
```
