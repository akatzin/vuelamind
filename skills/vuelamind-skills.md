---
description: Censa los skills del nivel personal (globales) y los del proyecto actual (locales), con una línea de descripción cada uno — de solo lectura
---

# /vuelamind-skills — el censo de comandos, medido

Presenta **qué comandos existen y dónde viven**, leyéndolos del disco — nunca de memoria ni de documentación, que se desincronizan en silencio.

## Qué hace

1. **Nivel personal (globales):** sirven a todos los dominios de la máquina, y viven en **una de dos formas** — hay que mirar las dos:
   - `~/.claude/commands/*.md` — archivo suelto
   - `~/.claude/skills/<nombre>/SKILL.md` — carpeta con el archivo dentro

   > [!danger] Mirar solo una de las dos formas devuelve CERO sin dar error
   > **Medido en otra máquina el 2026-09-07:** una casa con diez skills instalados en la forma
   > de carpeta habría salido con **cero globales** en este censo, y el resultado se lee como
   > *«no hay skills instalados»*. La salida vacía de un filtro no es evidencia de ausencia:
   > es evidencia de que ese filtro no encontró nada.
   >
   > **Qué forma usa cada máquina no lo decide el canon, lo decide el entorno.** Por eso se
   > miran las dos siempre, y **si una está vacía se dice** en vez de omitirla.
2. **Nivel proyecto (locales):** lista `./.claude/commands/*.md` del directorio de trabajo actual — solo los ve este dominio. Si el proyecto también tiene `.claude/skills/`, inclúyelo: hay dominios que usan esa forma.
3. Para cada archivo, la **descripción** sale de su frontmatter `description:`; si no tiene, del primer encabezado `#`. Saltar los respaldos `.bak-*`.
4. Presentar **dos tablas** — globales y locales — con nombre y descripción de una línea, y cerrar con los dos hechos que evitan sustos:
   - **La precedencia va al revés de lo intuitivo:** un nombre presente en ambos niveles sirve el del nivel PERSONAL — el local queda ensombrecido, en silencio. Si el censo detecta un nombre duplicado entre niveles, **señalarlo como hallazgo**, porque casi nunca es a propósito.
   - **El canon:** los comandos genéricos del ciclo del marco tienen su fuente versionada en la carpeta `skills/` junto al master, con su inventario de huellas en `skills/MD5SUM.txt`. **Esa comparación no se hace a mano:** corre `herramientas/comprobar_skills.py` del canon, que mira las dos formas de instalación, dice cuáles difieren nombrando las dos huellas, y **avisa aparte de los instalados que el inventario no lista** — sobre ésos no se comprobó nada, y un inventario incompleto se ve igual que uno completo desde el lado del que compara.

   > [!note] Por qué la comparación se delega y no se describe
   > Este comando pedía *«comparar por huella y reportar cualquier deriva»* sin decir cómo, y
   > eso son once archivos a ojo cada vez. **Una comprobación que cuesta trabajo se salta**, y
   > entonces la deriva vive sin que nadie la vea: **medido, una casa estuvo 19 días con un
   > skill del canon desactualizado sin una sola señal.**

## Qué NO hace

- **No escribe nada** — es de lectura, como el censo que es.
- **No documenta**: si el censo contradice la tabla de skills del vault del dominio, eso es material para el cierre, no para arreglarlo aquí.

## Por qué existe

Los inventarios de comandos mantenidos a mano mienten sin que nada falle — en el dominio de origen, una tabla declaró seis skills con siete en disco durante un día entero, y un comando funcionó sin estar documentado en ninguna nota. La única defensa es medir contra el disco, y este comando es esa medición hecha hábito.
