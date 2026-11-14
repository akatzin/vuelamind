# Proponer en masa

**Estado: diseñado, sin construir.**

## Qué es

Barrer el vault entero y proponer a cada colmena lo que le aplique.

## Y no es una pieza aparte

Es **la lógica de proponer corriendo sobre todo el vault** en vez de sobre lo que tocó una
sesión. Tratarla como mecanismo propio produce **dos caminos de proponer que divergen**, y
el día que uno se corrija el otro se queda atrás sin que nada falle.

## Lo que sí es suyo

**El primer barrido es distinto de los siguientes.** Uno sobre un vault que nunca ha
propuesto nada puede generar cientos de propuestas de golpe, y eso no es aportar: es
inundar. Hace falta decidir el corte **antes** de la primera corrida — por antigüedad, por
nota, o enseñando el total y dejando elegir.

**Y el registro de lo ya propuesto es lo que lo hace repetible.** Sin él, cada barrido
vuelve a proponer todo.

## Depende de

La lógica de proponer, entera.
