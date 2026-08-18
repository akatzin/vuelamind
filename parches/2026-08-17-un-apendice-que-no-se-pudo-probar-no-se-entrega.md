---
version: 1
origen: velaAkatzin
estado: armonizado al master el 2026-08-17 (lección 62 del libro heredado)
---

# 2026-08-17 · Declarar que no pudiste probar un procedimiento no lo vuelve entregable

## Qué corrige

El método ya tiene dos reglas buenas que, juntas, dejan un hueco por el que se cuela un
entregable roto:

- *Un comando que va a correr otro se prueba antes.*
- *Lo que no se pudo comprobar se dice **dentro** de la entrega.*

La segunda existe para que quien ejecuta no suponga verificado lo que no lo está. Pero al
aplicarse **se lee como si liberara de la primera**: se escribe la salvedad, se entrega
igual, y la conciencia queda tranquila porque *se avisó*. **Avisar no es un sustituto de no
entregar.**

Un procedimiento numerado que nadie ejecutó **no es un apéndice: es una hipótesis con
formato de instrucción** — y el formato comunica más que la advertencia, porque una lista de
pasos numerados se lee como algo que funcionó.

**Y el agravante que lo hace frecuente:** cuando el procedimiento corre en el entorno de
otro, probarlo es imposible por definición. Entonces la salvedad no es una excepción rara:
es el caso normal, y la regla se erosiona justo donde más se necesita.

## Cómo se descubrió

**2026-08-17.** Un dominio le entregó a otro un apéndice ejecutable de cinco pasos para
estrenar un carril de publicación: añadir un remoto, cortar una rama, empujar, abrir la
propuesta. Se declaró honestamente, dentro de la entrega, que **no se había podido probar**
porque corría en la máquina del otro.

El destinatario **midió su propio entorno antes de ejecutar** y encontró que no tenía
ninguna credencial de escritura: los pasos de empuje **no podían funcionar**, ni con permiso
ni sin él. El procedimiento no era discutible — era **inejecutable**, y la salvedad no lo
había detectado porque la salvedad hablaba de *no haberlo probado*, no de *no haber medido
el entorno donde iba a correr*.

Peor: el mismo dominio tenía, en sus propios scripts, una guarda que se negaba a actuar en
esas condiciones. **La herramienta era correcta y la prosa la rodeaba.** Lo que se sigue es
la prosa.

## Cómo aplicarlo

**Cuando un procedimiento no se puede ejecutar, no se entrega como procedimiento.** Se
entrega como una de estas dos cosas, y se dice cuál:

1. **Una pregunta al entorno del otro** — *«mide esto y dime qué sale; con eso te escribo los
   pasos»*. Es lo que convierte una suposición en un dato antes de que cueste.
2. **Un procedimiento con su precondición al principio**, no al final: la primera línea
   comprueba que existe lo que los pasos siguientes dan por hecho, y **aborta** si no.

Y la regla de forma: **la salvedad va antes de la lista, no después.** Una advertencia
colocada al final de un apéndice llega cuando ya se leyó como verificado.

**La prueba de que se aplicó:** si la única verificación que ofreces de un entregable es
*«avisé de que no lo probé»*, no está verificado y tampoco está acotado. Acotarlo es nombrar
**qué asumiste del entorno ajeno** — eso sí se puede contestar desde el otro lado en una
línea.

## Cómo verificar

- **Debe pasar:** todo procedimiento entregado a otro entorno abre con una comprobación de
  sus precondiciones, o llega en forma de pregunta.
- **Debe seguir fallando:** una lista de pasos numerados acompañada sólo de *«no pude
  probarlo»* se marca como no entregable — la advertencia no acota nada y el formato la
  contradice.
- **Y el caso que debe seguir siendo válido:** entregar pasos sin ejecutar **cuando las
  precondiciones están declaradas y son comprobables por quien recibe**. Lo que el parche
  persigue no es la falta de ejecución: es la falta de **acotación**.
