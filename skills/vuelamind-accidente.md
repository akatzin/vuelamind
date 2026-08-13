---
description: El usuario canceló una acción por accidente — reintentarla tal cual, sin pedir confirmación ni cambiar de enfoque.
---

# /accidente

El usuario escribió **`/accidente`** justo después de cancelar o rechazar una llamada a herramienta. Eso significa: esa cancelación fue un error suyo —tecla equivocada, prisa— **no una decisión sobre el enfoque.**

## Qué hacer

1. **Reintentar la llamada cancelada, verbatim.** Mismos parámetros, mismo archivo, mismo comando. No pedir confirmación de nuevo ni proponer una alternativa distinta.
2. **No leer la cancelación como retroalimentación.** No era un "no hagas eso" — fue un resbalón. Seguir con el plan que se traía, como si la interrupción no hubiera pasado.
3. **Excepción — acciones destructivas o irreversibles.** Si lo cancelado borraba datos, sobrescribía algo sin respaldo, publicaba hacia fuera o tocaba un sistema en producción, confirmar una vez antes de reintentar. Un accidente al cancelar no debe convertirse en un accidente al ejecutar.

## Alcance

Es un comando **universal**: va sobre *cómo* trabajar, no sobre *qué* se trabaja, así que aplica igual en cualquier dominio. Por eso vive en el nivel personal (`~/.claude/commands/`) y no dentro de un proyecto.

Reemplaza a la memoria `comando-errorcancel.md` (`/errorcancel`), que hacía lo mismo pero como regla invisible en vez de comando — se consolidó aquí el 2026-08-01.
