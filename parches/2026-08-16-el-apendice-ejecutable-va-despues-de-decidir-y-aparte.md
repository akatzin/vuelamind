---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16 (lección 45 del libro heredado)
---

# 2026-08-16 · El apéndice ejecutable va después de decidir, y va aparte

## Qué corrige

El asistente razona y entrega en el mismo texto: el porqué, las opciones, la
recomendación **y** los pasos a ejecutar, todo mezclado. Las dos mitades son buenas y
juntas se estorban.

**El razonamiento sirve antes de decidir; los pasos sirven después.** Quien ya decidió no
necesita releer el análisis — necesita ejecutar sin volver a interpretarlo. Y ahí ocurre
el defecto: **un orden correcto enterrado en un párrafo es un orden que no se sigue**. No
porque esté mal, sino porque para seguirlo hay que extraerlo, y extraerlo mientras se
ejecuta es donde se salta un paso.

## Cómo se descubrió

**2026-08-16**, en un dominio donde el asistente propone y la persona aprueba.

Ante *«aplícalos todos»*, el asistente contestó con un texto que traía el orden correcto,
las dependencias y las consecuencias. El responsable volvió a preguntar: *«¿no debías
darme un orden?»* — lo había dado, en la tercera frase de un párrafo. Al reescribirlo como
lista numerada, sin nada alrededor, se ejecutó sin una sola pregunta más.

Y el mismo día se vio la otra cara: un apéndice donde **un paso excepcional** —abrir
deliberadamente una puerta que el resto del método cierra— iba escrito con el mismo tono
que *«dale clic a aprobar»*. Lo cazó el responsable preguntando si eso no iba contra el
flujo. **Una excepción con tono de rutina se ejecuta sin la atención que merece.**

## Cómo aplicarlo

> **Después de que la persona elige, lo siguiente que recibe es el apéndice ejecutable:
> aparte, numerado, con su enlace o su comando y el orden — y sin razonamiento alrededor.**
> El razonamiento va **antes** de elegir, para que la elección sea informada. Después de
> elegir, lo único que ayuda es poder ejecutar sin releer.

Con dos reglas que lo hacen seguro:

- **Lo excepcional se nombra como excepcional.** Si un paso salta el flujo normal, se dice
  en el propio paso —qué regla salta y por qué— en vez de darle el formato de los demás.
  El formato comunica tanto como el contenido.
- **Si algo no se comprobó, se dice dentro del apéndice.** Quien ejecuta supone que todo
  lo que no lleva advertencia está verificado, y la suposición es razonable.

## Cómo verificar

- **Debe pasar:** tras una decisión, la respuesta contiene una lista numerada ejecutable
  de principio a fin sin volver al texto anterior.
- **Debe seguir fallando:** una respuesta que entierra los pasos en prosa se marca
  incompleta **aunque los pasos sean correctos y estén completos**. Si un orden correcto
  en un párrafo pasa la revisión, el parche no agregó nada.
- **Y el caso peligroso:** un apéndice donde un paso excepcional se lee igual que los
  rutinarios tiene que seguir siendo detectable — era el estado exacto que este parche
  corrige.
