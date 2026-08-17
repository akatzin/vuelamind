---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-17 · Seleccionar por la forma del contenido descarta en silencio lo que no la tiene: el resultado no sale vacío, sale corto

## Qué corrige

Todo filtro define, sin decirlo, una **taxonomía de los datos**: al pedir «las líneas que
tengan tal cosa» se está afirmando que los elementos relevantes tienen esa cosa. Cuando
esa taxonomía implícita no coincide con la real, el filtro **no falla — sesga**. Y puede
sesgar en dos direcciones opuestas sobre los mismos datos: incluyendo clases que no
correspondían, o descartando clases que sí.

Este parche cubre la segunda, que es la que no deja rastro. **Al seleccionar por la forma
del contenido —que tenga texto, que case un patrón, que traiga cierto campo— se descartan
en silencio los elementos que cumplen la condición de fondo pero no tienen esa forma.** Y
el daño no es un error: es que **el resultado no sale vacío, sale corto**.

Un resultado vacío invita a dudar. Un resultado corto **se lee como completo**: tiene
elementos, tienen buena pinta, y nada distingue *«no hay más»* de *«no lo vi»*. Quien
recibe ese número no tiene forma de saber que falta algo, y quien lo produjo tampoco.

> Es la cara de entrada de una familia que el corpus ya tiene por otras: *cero resultados
> no es ausencia* mira el caso extremo —la búsqueda devuelve nada— y por eso se nota.
> Éste mira el caso frecuente y silencioso: la búsqueda devuelve **casi todo**.

## Cómo se descubrió

**2026-08-17.** Un dominio pidió a otro una cota temporal: la marca de la última
interacción de una persona, para acotar un registro. La medición recorrió el transcript
buscando las entradas de esa persona y, para excluir ruido, exigió que tuvieran **texto**.

Devolvió una hora perfectamente plausible. Era **dieciséis minutos anterior a la real**:
la última entrada de esa persona eran **dos capturas de pantalla**, y una imagen no tiene
texto. El filtro las descartó exactamente por cumplir la condición de fondo —ser una
entrada suya— sin cumplir la de forma.

Nada salió vacío. Nada dio error. La hora era verosímil y habría entrado a un registro
como medición, con dieciséis minutos de menos, **si el dominio que la pidió no hubiera
exigido saber de qué clase era la entrada**. Se cazó porque el número no cuadró con otra
fuente, no porque el filtro avisara.

*(En la misma medición ocurrió la cara opuesta —incluir de más, atribuyendo a la persona
un mensaje que no era suyo— y está cubierta por el parche del campo que responde otra
pregunta. Dos direcciones, un solo barrido, quince minutos de diferencia.)*

## Cómo aplicarlo

Texto para las reglas del dominio:

> **Audita la taxonomía implícita de tu filtro antes de confiar en su salida.** Todo
> filtro afirma que lo relevante tiene cierta forma; escribe esa afirmación y pregúntate
> qué clases de elemento la incumplen **siendo relevantes**. Si la fuente tiene elementos
> sin texto, sin ese campo, en otro formato — el filtro los está tirando, y no vas a
> enterarte por la salida.
>
> **La comprobación barata, y es una resta:** cuenta los elementos **antes** y **después**
> del filtro. Si no puedes explicar la diferencia, no puedes usar el resultado. Un filtro
> que descarta el 3 % de lo que mira debe poder decir qué 3 % y por qué.
>
> Y al reportar el resultado, **di por qué forma seleccionaste**. Quien lo reciba sabe así
> qué clases pueden faltar — que es información que el número solo no lleva.

## Cómo verificar

- **Debe pasar:** una medición sobre una fuente heterogénea declara la forma por la que
  filtró y el conteo antes/después, y las clases descartadas están nombradas.
- **Debe seguir fallando:** un filtro que selecciona por forma y reporta solo el resultado
  debe ser rechazable en revisión **aunque el resultado sea correcto esta vez** — porque
  su corrección depende de que la fuente sea homogénea, y eso nadie lo comprobó.
