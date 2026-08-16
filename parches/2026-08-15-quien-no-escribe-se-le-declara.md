---
version: 1
origen: campaña de pruebas del canon
estado: armonizado al master el 2026-08-15
---

# 2026-08-15 · Quien no escribe no se declara — se le declara

## Qué corrige

El cuarto acto del ciclo asume que toda instancia **escribe**: el paso de declararse
lo hace ella misma, en el vault. Pero existe un rol legítimo que el método no
contemplaba: **la instancia que solo lee** — un consejo directivo suscrito a la
memoria de ingeniería, un auditor, una dirección que quiere el porqué de las
decisiones sin tocar una letra.

Para ese rol, el paso de declararse es una **contradicción de diseño**: le exige
escribir a quien se define por no escribir.

## Cómo se descubrió

**2026-08-15**, en una prueba deliberada del canon: un dominio real montado en solo
lectura ante una secretaria de consejo que pedía sumarse *"solo para leer"*.

El asistente recorrió los siete pasos del acto de sumarse, **se detuvo solo en el
paso de declararse** —*"es el que escribe; está parado"*—, verificó los comandos por
huella, contestó las tres preguntas de dirección citando nota y fecha, leyó el libro
de errores entero antes de opinar, y cerró la sesión con la frase que define el rol:
*"en toda esta sesión no se ha escrito ni una letra en el vault"*.

La conducta fue correcta por juicio del asistente. **Este parche existe para que no
haga falta el juicio**: el método debe nombrar el rol.

## La resolución, en tres piezas

**1 · Ningún sustantivo nuevo.** El registro de instancias gana un campo:

> `acceso: escribe | lee`

Una instancia lectora es una instancia — con dónde corre, desde cuándo, y qué
alcanza. Lo único que cambia es ese campo.

**2 · La declaración ocurre — pero no la hace el lector.**

> **Quien no escribe no se declara: SE LE declara.**

Una instancia que sí escribe (o el responsable) registra al lector **antes** de que
llegue, o al saberse de él. Esto disuelve la contradicción sin excepción alguna al
principio de que el vault registra a todas sus instancias: el registro es completo,
y el lector sigue sin escribir.

**3 · El nombre que NO se usa: «testigo».** Esa palabra ya es marca de procedencia
(`ATESTIGUADO`: persona + fecha). Un mismo término para un rol y para una clase de
evidencia colisiona en cada frase que los junte. El rol se dice por su campo:
*instancia de lectura*.

## Cómo verificar

**El caso que fallaba:** una máquina con el dominio en solo lectura recorre el acto
de sumarse. Debe detenerse en la declaración, decirlo, operar como lectora citando
procedencia, y cerrar sin haber escrito. Su fila debe poder existir en el registro,
escrita por otra.

**El que DEBE seguir fallando:** una instancia lectora que escriba lo que sea —su
propia fila incluida— dejó de ser lectora, y el validador del dominio debe poder
delatarlo comparando el campo `acceso` contra las huellas del vault.

## A qué archivos

| Archivo | Qué hacer |
|---|---|
| El acto de sumarse (skill del ciclo) | El paso de declararse distingue: quien escribe se declara; quien lee **es declarado**, y el paso lo dice |
| El master, ciclo completo | El campo `acceso: escribe \| lee` en la mención del registro de instancias |
| La sección multi-máquina del README | El rol existe y cómo entra |
