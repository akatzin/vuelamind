# El watcher — el rol que vigila lo que entra al canon

Un método que se corrige por parches necesita alguien que juzgue los parches. Este
documento define ese rol: **qué vigila, qué mide, cómo juzga y qué no le toca.** No
describe una instalación concreta — describe un papel que cualquier dominio puede
adoptar sobre el repositorio que ya lee.

> [!important] Vigila lo que ENTRA, no a quién lo usa
> Un watcher **no lleva padrón de instalaciones** y no va a llevarlo. Consumir el método
> es libre y anónimo: nadie se registra, nadie pide permiso. La responsabilidad del
> watcher **empieza cuando una instancia manda un aporte** — antes de eso no hay nada
> que vigilar, y fabricar un censo de usuarios sería vigilar a las personas en vez de
> al canon.

## Por qué es un dominio aparte

Mientras el método vivió dentro del dominio donde nació, mejorarlo significaba hacerlo
en medio de una cola que hablaba de otra cosa: el trabajo del método competía por
atención con la operación diaria, y perdía siempre — porque la operación tiene fechas y
el método no.

Un watcher le da al desarrollo del canon lo que el canon le da a cualquier dominio: **su
cola, sus decisiones, su libro de errores.** Y le da un objeto propio que ninguna otra
casa tiene: el corpus de parches y quién los aporta.

## Las dos direcciones, y por qué las dos necesitan instrumento

El error más común al montar un watcher es medir solo una mitad.

**Entrada** — lo que llega a juzgar. Aportes de otras instancias: parches, correcciones,
casos. El watcher los recibe, los juzga y responde **con razón**, adopte o rechace.

**Salida** — lo que el watcher mismo produce. Un dominio que usa el método también lo
corrige, y esos parches viajan hacia el canon como los de cualquier otro.

Las dos fallan igual de silenciosamente y por el mismo mecanismo: **nada se rompe cuando
nadie decide.** Un aporte sin juzgar y un parche propio sin proponer se ven idénticos a
un día tranquilo. Por eso ninguna de las dos puede quedar en la intención de revisarlas:
las dos necesitan un momento fijo y un instrumento que las cuente.

## Qué mide, y la trampa que casi todos los instrumentos tienen

El vigía mínimo mide tres cosas, y la tercera es la que se olvida:

1. **Los aportes abiertos** — cuántos esperan juicio.
2. **La edad desde nuestra última respuesta**, no desde que se abrieron. Es el número que
   vigila la confianza de quien aporta: un aporte contestado tarde enseña a no volver.
3. **Lo que llegó fuera de cola.** Un aporte puede llegar por un canal que el instrumento
   no mira — empujado como rama en vez de propuesto, mandado por otro medio, dejado en un
   archivo. Entonces el instrumento reporta **cero y tiene razón**, y esa es exactamente
   la forma más cara de mentir: un cero limpio no genera ninguna reacción.

> [!danger] El fallo del watcher no dispara ningún evento
> Cuando un servicio se cae, algo avisa. Cuando un aporte se pierde, **no pasa nada**:
> nadie reclama, ningún chequeo se pone en rojo, y el daño ocurre **fuera del sistema** —
> una persona que aportó, no recibió respuesta y no vuelve. De eso no se entera ninguna
> alarma, así que el watcher no se sostiene con alarmas: se sostiene con **cadencia**.
> Un piso semanal instrumentado vale más que la mejor intención de revisar seguido.

## Cómo juzga

**La única prueba que decide.** Reescribe la lección del aporte sustituyendo **todos** los
nombres propios por genéricos. ¿Sigue siendo cierta y útil? Entonces es del método. Si
solo es cierta con sus nombres puestos, es de su dominio.

**Lo que el watcher NO juzga: la verdad del caso ajeno.** No puede — pasó en otra casa, y
no tiene su evidencia. La verdad la juzga cada dominio que adopte el parche, contra su
propia evidencia, con tres veredictos: **adoptar, posponer o descartar con razón.**

**Descartar con razón vale más que adoptar por cortesía.** Un rechazo con su porqué
escrito enseña; una fusión amable mete ruido en el corpus para siempre.

**Dos capas, un solo veredicto.** El veredicto interno puede llevar toda la evidencia y el
error de quien aporta con nombre; el publicado generaliza y recorta detalle. Lo que **no**
puede pasar es que difieran **en la razón**: si el motivo real solo existe en el privado,
el veredicto público es falso. El error se nombra, el caso se generaliza.

**El orden de fusión es parte del juicio.** Dos aportes correctos por separado pueden
depender uno del otro — uno introduce un término y el otro lo usa. Fusionados al revés, el
segundo cita un vocabulario que el canon todavía no tiene. Un watcher que solo juzga
aportes de uno en uno no ve esto nunca.

**Y la revisión de huellas va ANTES del merge.** Lo fusionado entra a la historia, y la
historia no se des-publica. Señalar un dato identificable en un aporte es parte del
juicio, no una cortesía.

## La identidad hacia afuera

Un watcher **actúa sobre un repositorio público**, así que hereda la pregunta que casi
ninguna instalación se hace: **¿con qué identidad firma lo que sale?**

**Preparar y publicar son actos distintos**, y la respuesta fuerte es estructural, no una
promesa: que la copia de trabajo diaria **no pueda** firmar hacia afuera. El watcher
prepara —escribe el parche, arma la rama, redacta el veredicto— y la publicación cruza por
una mano distinta o una identidad concedida a propósito, declarada con su dueño y su
condición. Una identidad de escritura **no se hereda por omisión** solo porque el clon
esté en el árbol.

Y lo mismo hacia dentro del juicio: **fusionar no es juzgar.** Un watcher puede tener
veredicto sobre todo y capacidad de fusionar sobre nada; separarlo no le quita autoridad,
se la da — porque su firma vale por la razón que escribe, no por el botón que aprieta.

## Qué NO es un watcher

- **No administra el repositorio.** No gobierna releases, ni infraestructura, ni el sitio.
- **No lleva padrón de instalaciones**, ya dicho, y es la línea que lo separa de vigilar
  personas.
- **No decide por el dominio que adopta.** Publica el parche; cada casa lo juzga contra su
  evidencia.
- **No es un revisor automático.** Ninguna de sus decisiones sale de un chequeo: los
  chequeos miden lo que espera, la razón la escribe alguien.

## Cómo nace uno

Un watcher es un dominio del método como cualquier otro —nace pegando la plantilla y
contestando su entrevista— con tres cosas propias que su inicialización debe dejar puestas:

| Pieza | Qué es |
|---|---|
| **El objeto** | El repositorio vigilado, declarado: de dónde se jala el canon y a dónde se aportan los parches |
| **El vigía** | El instrumento de cadencia: aportes abiertos, edad desde el último acuse nuestro, y lo que llegó fuera de cola |
| **La mano separada** | Quién publica y con qué identidad — y qué puede preparar el watcher sin ella |

Lo demás es el ciclo normal: cola, decisiones, errores, bitácora, arranque y cierre.
