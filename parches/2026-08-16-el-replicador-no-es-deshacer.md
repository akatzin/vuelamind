---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-16 · El replicador no es deshacer

## Qué corrige

Cuando un archivo replicado se daña, el reflejo es ir por la copia buena a otra
máquina. **Ese reflejo pierde la carrera**: un replicador continuo propaga el daño a la
velocidad de sincronización — segundos — y para cuando llegas, la "copia buena" ya es
la copia rota. La réplica protege contra la **muerte del medio**, no contra la
**escritura equivocada**: a esa la reparte con la misma eficiencia que a las buenas.

El deshacer real vive en otra capa: la que **no obedece al replicador** — snapshots del
sistema de archivos, versionado del lado receptor, un respaldo periódico. Lo que define
a esa capa es que su contenido no cambia cuando el original cambia; el precio es que su
foto tiene la edad de su cadencia.

## Cómo se descubrió

**2026-08-16.** Una edición automatizada borró ~90 líneas de un documento del vault.
Otra máquina del dominio tenía la versión íntegra — se midió: ahí estaba, con el conteo
correcto. En los **segundos** que tomó ir por ella, el replicador la alcanzó: la copia
llegó ya rota, idéntica a la local. La recuperación salió del **snapshot de la
madrugada** en el almacenamiento del dominio — una capa que existía por decisiones de
semanas atrás, tomadas sin saber para qué accidente servirían. Fue la primera
restauración real desde snapshot en la historia del dominio: hasta ese día eran red de
seguridad teórica.

## Cómo aplicarlo

Texto para las reglas del dominio:

> **La réplica no es deshacer.** Ante un archivo dañado, no corras a las otras
> máquinas: el replicador llega antes que tú. Ve directo a la capa que no obedece al
> replicador — snapshots, versionado del receptor, respaldo periódico — y **conoce esa
> capa antes del accidente**: cuál es, con qué cadencia toma fotos, y cómo se lee. Un
> dominio que replica sin ninguna capa así tiene distribución, no protección: todas sus
> copias son la misma copia, con segundos de diferencia.

Y al diseñar respaldos, la pregunta que separa las dos funciones: *si escribo basura
ahora mismo, ¿cuál de mis copias NO la tendrá en un minuto?* Si la respuesta es
ninguna, falta la capa.

## Cómo verificar

- **Debe pasar:** el dominio puede nombrar su capa de deshacer —qué es, cadencia, cómo
  se lee— sin buscarla durante el accidente.
- **Debe seguir fallando:** un dominio cuyas "copias de seguridad" son solo réplicas
  sincronizadas debe reprobar la pregunta del minuto — declararlo distribución y abrir
  el pendiente de la capa que falta, no llamarlo respaldo.
