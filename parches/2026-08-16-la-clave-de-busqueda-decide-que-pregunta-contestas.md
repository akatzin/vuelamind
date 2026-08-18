---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-17 (lección 55 del libro heredado)
---

# 2026-08-16 · La clave de búsqueda decide qué pregunta contestas: «¿está mi texto?» no es «¿está mi lección?»

## Qué corrige

Para comprobar si una aportación propia ya fue incorporada a un cuerpo mayor —una
lección al libro, una regla al manual, una cláusula al contrato— el reflejo es buscar una
**frase distintiva** del original. Es la búsqueda más natural del mundo, y contesta una
pregunta que no es la que se hizo: *«¿está mi texto ahí?»*, cuando lo que se quería saber
era *«¿está mi lección ahí?»*.

**La incorporación bien hecha reformula.** Un cuerpo maduro no pega el texto recibido: lo
integra en su voz, lo generaliza, le quita los nombres propios y a veces lo funde con una
regla vecina. Cuanto **mejor** se incorpore una aportación, **menos** sobrevive su
redacción literal — así que la búsqueda por frase falla justo en el caso exitoso, y
acierta solo cuando la incorporación fue perezosa.

El resultado es un cero. Y un cero se lee como ausencia.

> Es pariente de *cero resultados no es ausencia*, y **un nivel más adentro**. Allí el
> patrón estaba mal escrito y la solución era repetir con uno más laxo. **Aquí el patrón
> está perfecto y la herramienta funciona sin un fallo**: devuelve exactamente lo que se
> le pidió. Lo que está mal es la pregunta, y ninguna mejora del patrón la arregla.

## Cómo se descubrió

**2026-08-16, y hacen falta las dos casas para contarlo.** Un dominio verificó que cuatro
parches que había publicado nunca llegaron al canon. Su método era correcto en apariencia
—buscar cada uno en el cuerpo destino— y su conclusión fue que los cuatro eran huecos.

Otra instancia, juzgando el rescate **con el texto completo delante**, midió que **al
menos uno sí estaba**: vivía incorporado como una lección numerada del cuerpo mayor, con
el caso original literal dentro. El grep de su autor había dado cero porque la
incorporación reformuló el enunciado — el caso sobrevivió, la redacción no.

Dos errores en la misma medición, y de signo opuesto: **tres ausencias reales que un
método correcto encontró**, y **una ausencia falsa que ese mismo método fabricó**. El
segundo es el caro: una aportación propia dada por perdida es trabajo que se repite, y
peor, es un cuerpo al que se le atribuye una falta que no tiene.

## Cómo aplicarlo

Texto para las reglas del dominio:

> **Antes de buscar, decide qué pregunta estás haciendo.** Comprobar si un texto está es
> una pregunta; comprobar si una **idea** está es otra, y la segunda no se contesta con
> una clave literal. Para lo incorporado —lecciones, reglas, cláusulas— la comprobación
> es **por concepto, con el cuerpo destino delante**: se lee la sección donde debería
> vivir, no se le pregunta a un patrón.
>
> Y la señal de alarma, barata: **si buscas tu propia frase y sale cero, sospecha primero
> de la pregunta.** Cuanto mejor te hayan incorporado, menos texto tuyo va a sobrevivir —
> el cero es compatible con el éxito, no solo con el fracaso.

**El corolario que hace la regla ejecutable:** cuando el cuerpo destino declare dónde vive
cada aportación —una matriz, un índice, una tabla de incorporación con su ancla— esa
declaración es la fuente, no el grep. Y cuando no exista, el trabajo es leer: caro, pero
es el precio de una respuesta que sí contesta la pregunta.

## Cómo verificar

- **Debe pasar:** una aportación incorporada con reformulación se declara «incorporada»
  tras leer la sección destino, aunque ninguna frase del original sobreviva.
- **Debe seguir fallando:** declarar una aportación «ausente» apoyándose **solo** en un
  grep por frase distintiva debe ser rechazable en revisión — incluso cuando el grep esté
  bien escrito y devuelva cero legítimamente. La carga de la prueba de una ausencia es
  leer, no buscar.
