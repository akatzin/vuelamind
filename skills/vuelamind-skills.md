---
description: Censa los skills del nivel personal (globales) y los del proyecto actual (locales), con una línea de descripción cada uno — de solo lectura
---

# /vuelamind-skills — el censo de comandos, medido

Presenta **qué comandos existen y dónde viven**, leyéndolos del disco — nunca de memoria ni de documentación, que se desincronizan en silencio.

## Qué hace

1. **Nivel personal (globales):** lista `~/.claude/commands/*.md` — sirven a todos los dominios de la máquina.
2. **Nivel proyecto (locales):** lista `./.claude/commands/*.md` del directorio de trabajo actual — solo los ve este dominio. Si el proyecto también tiene `.claude/skills/`, inclúyelo: hay dominios que usan esa forma.
3. Para cada archivo, la **descripción** sale de su frontmatter `description:`; si no tiene, del primer encabezado `#`. Saltar los respaldos `.bak-*`.
4. Presentar **dos tablas** — globales y locales — con nombre y descripción de una línea, y cerrar con los dos hechos que evitan sustos:
   - **La precedencia va al revés de lo intuitivo:** un nombre presente en ambos niveles sirve el del nivel PERSONAL — el local queda ensombrecido, en silencio. Si el censo detecta un nombre duplicado entre niveles, **señalarlo como hallazgo**, porque casi nunca es a propósito.
   - **El canon:** los comandos genéricos del ciclo del marco tienen su fuente versionada en la carpeta `skills/` junto al master. Si esta máquina la alcanza, comparar por huella los del ciclo contra ella y reportar cualquier deriva.

## Qué NO hace

- **No escribe nada** — es de lectura, como el censo que es.
- **No documenta**: si el censo contradice la tabla de skills del vault del dominio, eso es material para el cierre, no para arreglarlo aquí.

## Por qué existe

Los inventarios de comandos mantenidos a mano mienten sin que nada falle — en el dominio de origen, una tabla declaró seis skills con siete en disco durante un día entero, y un comando funcionó sin estar documentado en ninguna nota. La única defensa es medir contra el disco, y este comando es esa medición hecha hábito.
