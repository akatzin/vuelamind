---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-16 (lección 50 del libro heredado)
---

# 2026-08-16 · La deuda retroactiva de una regla nueva se salda con lápida, no con reconstrucción

## Qué corrige

Toda regla nueva **nace debiendo**: lo hecho antes de que existiera no la cumple. El
reflejo es saldar esa deuda hacia atrás — reconstruir los registros que faltan, rellenar
los campos que nadie puso, completar el archivo. **Ese reflejo produce datos falsos con
formato de datos buenos**: un registro escrito semanas después del hecho **se escribe de
memoria**, y entra al corpus con el mismo aspecto que los redactados en caliente. Nadie
podrá distinguirlos después, y su tono de evidencia es exactamente lo que el método
combate.

El daño real de la deuda casi nunca es el hueco: es que **quien lo encuentre no sepa que
es un hueco** y concluya que buscó mal. Eso se cura nombrando el vacío, no llenándolo.

## Cómo se descubrió

**2026-08-16.** Un dominio midió que **18 de sus items cerrados** no tenían el registro
completo que su regla exigía — casi todos cerrados **antes de que esa regla existiera**.
El item llevaba días abierto con la decisión pendiente: reconstruir los 18, o ajustar la
regla.

El responsable eligió ajustar. El argumento que decidió no fue el costo en horas sino el
de método: reconstruir habría producido **18 registros de memoria con tono de evidencia
en un solo acto de limpieza** — multiplicando por 18 el error más caro del dominio,
mientras se creía estar ordenando.

En su lugar, el archivo ganó una **lápida**: la lista completa de los 18 folios, la razón
por la que no tienen sección, y un puntero por cada uno a donde sí vive lo que importa de
él. El hueco dejó de ser invisible sin fabricar nada.

## Cómo aplicarlo

Texto para las reglas del dominio:

> **Una regla nueva no se aplica hacia atrás rellenando: se aplica hacia adelante y se
> declara hacia atrás.** Cuando una regla deja en falta a lo ya hecho, se escribe una
> **lápida** en el sitio donde el lector buscará: qué elementos quedan fuera, **por qué**
> (nacieron antes de la regla), y **dónde vive lo que sí se conservó** de cada uno. No se
> reconstruyen registros de memoria para que el archivo "se vea completo": un vacío
> nombrado es información; un vacío rellenado a posteriori es ficción con formato de
> evidencia.
>
> **La excepción, y es individual:** si un elemento concreto hace falta de verdad, se
> reconstruye **ese**, marcado explícitamente como reconstrucción y con la fecha en que
> se hizo — nunca el lote entero por simetría.

Y la señal de que la regla nueva está bien planteada: **debe poder cumplirse desde hoy
sin tocar nada de ayer.** Si exige trabajo retroactivo para valer, probablemente es
demasiado ambiciosa y conviene acotarla antes de adoptarla.

## Cómo verificar

- **Debe pasar:** un dominio con deuda retroactiva declarada tiene, en el sitio donde se
  buscaría, la lista de lo que falta con su razón y sus punteros — y un lector que busque
  uno de esos elementos encuentra la explicación en vez del silencio.
- **Debe seguir fallando:** un registro reconstruido semanas después **sin marca de
  reconstrucción** debe ser detectable como defecto. Si el corpus no distingue lo
  redactado en caliente de lo rellenado después, la regla no se aplicó: se maquilló.
