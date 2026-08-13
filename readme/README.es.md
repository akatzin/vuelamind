# vuelamind

*Un marco para auditar y documentar un dominio complejo con un asistente de IA, sin que la documentación se despegue de la realidad.*

[← English](../README.md)

## El problema

Un asistente de IA olvida: su ventana de contexto se llena y el principio se disuelve, así que cada sesión nace huérfana — sin reglas, sin historia, sin cicatrices.

Y la documentación que no se reconcilia con la realidad **miente con confianza**. A los seis meses, la mitad de lo que afirman tus notas es falso y nada señala cuál mitad.

vuelamind rompe las dos cosas a la vez — no con una app, sino con disciplina escrita: **no se afirma nada que no se haya comprobado**, y toda afirmación conserva su procedencia: **medido**, **inferido** o **aportado**.

## Qué obtienes

Un vault de texto plano y un ciclo de cuatro actos: **nacer** una vez, **retomarse** al abrir cada sesión —midiendo el estado actual en vez de confiar en lo que se recuerda— y **reconciliarse** al cerrarla.

Dentro: una cola de trabajo ordenada por gravedad real, un registro de decisiones que anota *qué me haría cambiar de opinión*, y **un libro de errores con 38 lecciones, cada una pagada con una equivocación real**. Esa última parte es la valiosa: la estructura se reconstruye en una tarde; las cicatrices no.

## Cómo se empieza

1. Pega `MARCO_Inicial.md` completo en un contexto nuevo de tu asistente.
2. Di: **«inicializa este marco»**.
3. Contesta la entrevista — unos veinte minutos, y puedes pausar.

Sin servidor, sin herramientas, sin cuenta. Un asistente y dos carpetas locales.

**La pregunta cero es en qué idioma quieres trabajar**, y a partir de ahí todo sale en el tuyo.

## Requisitos

Un asistente, dos carpetas locales y **un shell tipo Unix** — macOS o Linux.

**Windows no es compatible de forma nativa.** Los scripts que el marco genera asumen
`sh`/`bash` y rutas POSIX. La vía conocida es correr tu asistente **dentro de un contenedor
Linux** (Docker, por ejemplo) y trabajar ahí: todo lo que el marco necesita vive dentro del
contenedor, y el sistema anfitrión deja de importar.

Esa vía está **inferida, no probada**: debería funcionar y nada sugiere lo contrario, pero
nadie la ha corrido todavía. Si tú lo haces, eso vale un parche — con lo que funcionó y lo
que hubo que ajustar.

El **núcleo** sí corre en cualquier sistema, Windows incluido: la entrevista, las plantillas,
las reglas y el libro de errores son texto plano. Estarías renunciando a la maquinaria
opcional y haciendo a mano lo que ella haría — menos cómodo, igual de válido.

## Cómo mejora

Por **parches**: lecciones con caso real, fecha y forma de verificarse, propuestas como pull requests. El único criterio de admisión es la prueba de genericidad — *reescribe tu lección sin nombres propios: ¿sobrevive?* — y **descartar con razón vale más que adoptar por cortesía**.

## Licencia

Uso personal, educativo, comunitario y de investigación: **libre**. Uso empresarial: **con licencia de pago**. Y una condición que no se negocia: este marco **no se usa para sustituir el trabajo de personas empleadas**. Detalle en `LICENSE.md` — es *source-available*, no open source según la OSI, y la licencia lo dice con esas palabras.
