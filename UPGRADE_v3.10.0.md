---
title: Salto menor a v3.10.0 — el marco sin narrativa, y vuelamind-export
tipo: plantilla ejecutable
para: dominios en la v3.9.3
---

> [!note] De dónde tienes que venir
> **De la v3.9.3.** Desde una v3 anterior, corre primero `UPGRADE_v3.9.3.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.10.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.10.0`. El master dice el hecho y la regla, sin narrativa: el libro de errores y las secciones de las cuatro fases. **Ninguna regla cambia.** La historia que salió vive en los `UPGRADE` de su versión | Traerlo (paso 1) |
| `ALMA.md` | Versión 1.1: el aprendizaje es local, y la pieza «la mente distribuida» ya no dice que los aprendizajes viajen al canon | Copiarlo de nuevo, conservando tus atestiguaciones (paso 2) |
| Los README | Las nueve traducciones dicen lo mismo que el inglés | Nada |
| `skills/vuelamind-export.md` | Nuevo: empaca el dominio en un zip con sus notas de migración, sin tocar el origen. El canon pasa de **8 skills a 9** | Instalarlo (paso 3) |
| El manifiesto | Sin cambios | Nada |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Copia `ALMA.md` del canon a tu vault, conservando tus atestiguaciones.** La ruta de tu copia
   la declara la clave `alma` del manifiesto. Desde la raíz del canon:

   ```sh
   ALMA="ruta/a/tu/ALMA.md"   # la clave `alma` de tu manifiesto
   cp "$ALMA" "$ALMA.antes-3.10.0"
   { sed '/^## Atestiguaciones de este dominio/,$d' ALMA.md
     sed -n '/^## Atestiguaciones de este dominio/,$p' "$ALMA.antes-3.10.0"; } > "$ALMA"
   ```

   Todo lo que está arriba de «Atestiguaciones de este dominio» es texto canónico y se reemplaza;
   esa sección es tuya y se conserva tal cual.

3. **Instala el skill nuevo**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   python3 herramientas/comprobar_skills.py           # sin deriva
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10.0
grep -m1 '^version:' "$ALMA"                           # version: 1.1
grep -c 'no hay camino de vuelta al canon' "$ALMA"     # 1
python3 herramientas/comprobar_skills.py               # 9 al día, sin deriva
diff <(sed -n '/^## Atestiguaciones de este dominio/,$p' "$ALMA.antes-3.10.0") \
     <(sed -n '/^## Atestiguaciones de este dominio/,$p' "$ALMA")   # sin salida
```

**Nada se borró:** la copia anterior de tu `ALMA.md` queda en `ALMA.md.antes-3.10.0`.
