---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-16 · El delimitador de un reemplazo es una hipótesis sobre la estructura

## Qué corrige

Al editar un documento por sustitución, el tramo a reemplazar suele acotarse con un
delimitador estructural: *"desde este encabezado hasta el siguiente del mismo tipo"*.
Ese delimitador es una **hipótesis sobre el orden del archivo** — que entre los dos
encabezados solo vive el contenido del primero. Si el archivo tiene material intercalado
de otro nivel (una sección entera entre dos items, un bloque ajeno en medio), **queda
dentro del tramo y se borra sin ruido**: el reemplazo sale bien, el texto nuevo queda
perfecto, y lo desaparecido no deja síntoma en el punto de edición.

Es pariente de dos lecciones que el libro ya tiene, y distinta de ambas: *la escritura
puede romper el recipiente y no el dato* mira lo que quedó **mal escrito**; *un límite
de consulta responde otra pregunta* mira los **rangos de lectura**. Ésta mira el rango
de **escritura**: lo que el delimitador abarcó de más.

## Cómo se descubrió

**2026-08-16.** Al cerrar un item de la cola, un reemplazo automatizado acotó el tramo
como *"del encabezado del item al siguiente encabezado de item"*. Entre esos dos items
vivía —por un desorden histórico que nadie había visto— **la sección de resumen
completa del documento**, de un nivel de encabezado distinto que el delimitador no
miraba. El reemplazo la tragó entera: ~90 líneas, sin error, sin aviso.

Lo cazó el **validador estructural** en la corrida siguiente: 74 fallos de golpe,
porque cada item exigía presencia en la sección desaparecida. Sin ese instrumento, el
archivo habría quedado coherente a simple vista y la pérdida se habría descubierto
semanas después, o nunca. Y la reconstrucción destapó el desorden que hizo posible el
accidente — que llevaba días sin que ningún chequeo lo viera.

## Cómo aplicarlo

Antes de ejecutar un reemplazo acotado por estructura:

> **Mide el tramo, no lo supongas.** Dos comprobaciones baratas: **(1)** cuenta las
> líneas del tramo que el delimitador abarcó y compáralas con el tamaño esperado del
> contenido a reemplazar — una diferencia grande acusa material intercalado; **(2)**
> busca dentro del tramo encabezados o marcadores **de otro nivel** que el delimitador
> no distingue. Si aparece cualquiera de los dos, el delimitador está mal y el archivo
> probablemente también: repáralo antes de editar.

Y la red que lo vuelve recuperable: **correr el validador estructural inmediatamente
después de toda edición por sustitución**, no al final de la jornada — el costo de
detectar el hueco crece con cada edición que se le apila encima.

## Cómo verificar

- **Debe pasar:** un reemplazo sobre un tramo bien ordenado, con conteo de líneas
  cercano al esperado, se aplica y el validador sale limpio.
- **Debe seguir fallando:** un documento con una sección intercalada entre dos items —
  el escenario del caso real— debe delatar la diferencia de tamaño en la comprobación
  previa; y si el reemplazo se ejecuta de todos modos, el validador estructural debe
  gritar en la corrida inmediata. Si ninguna de las dos capas lo ve, no hay defensa.
