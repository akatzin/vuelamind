---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-17 (lección 58 del libro heredado)
---

# 2026-08-16 · Tocar el vigilante es el momento de máximo riesgo, y el paso que lo ordena no pide probarlo en rojo

## Qué corrige

El corpus ya tiene la disciplina: un chequeo arreglado puede quedar ciego, y todo arreglo
se verifica con dos casos —el que fallaba, que debe pasar; y uno inventado, que debe
seguir saliendo—.

Lo que falta es INVOCARLA DONDE EL PROPIO MÉTODO MANDA TOCAR EL INSTRUMENTO. El paso del
salto que reescribe un chequeo del validador del dominio no menciona la prueba en rojo, y
ése es precisamente el momento de máximo riesgo: se está modificando al que vigila, en
mitad de un acto cuya compuerta final ES ESE MISMO INSTRUMENTO.

La asimetría que lo vuelve caro: si el chequeo reescrito queda incapaz de fallar, la
verificación final SALE VERDE — y sale verde PORQUE está roto. El acto se declara completo
apoyándose en un instrumento muerto, y nada vuelve a mirar.

## Cómo se descubrió

MEDIDO 2026-08-16, ejecutando el paso que manda reescribir el chequeo de la plantilla para
que consulte el modo declarado.

La versión nueva salió VERDE Y CORRECTA. Al forzar el caso que debía fallar —copia local
presente con modo `referencia`— imprimió:

    validar_<dominio>.sh: line 394: fallo: command not found

…siguió, terminó con EXIT 0 y reportó «Fallas: 0». La función del validador se llama
`falla`, no `fallo`: un typo en la rama roja, que por definición no se ejecuta en la rama
verde.

Sin la prueba en rojo, ese dominio habría entregado un chequeo INCAPAZ DE FALLAR dentro
del propio acto de arreglar ese chequeo, y su verificación final habría certificado el
salto con el vigilante muerto.

## Qué añade

Cuando un paso del método modifique el instrumento del dominio, la prueba en rojo es parte
del paso, no una buena práctica aparte. El paso no está completo hasta que:

1. El caso que fallaba PASA.
2. Un caso inventado SIGUE FALLANDO — y se comprueban LAS DOS SALIDAS: lo que imprime y el
   código de retorno. La rama roja es donde viven los typos, porque es la que nadie
   ejecuta.
3. El escenario de prueba se deshace y la reversión se comprueba con un `diff` contra el
   estado previo, no con la memoria de haberlo deshecho.

## Señal de que falta

Cualquier paso de un procedimiento que diga «actualiza el chequeo», «ajusta el validador»
o «reescribe la comprobación» y no diga cómo probar que el resultado todavía sabe fallar.
