# vuelamind

*Un marco para auditar y documentar un dominio complejo con un asistente de IA, sin que la documentación se despegue de la realidad.*

[← English](../README.md)

## El problema

Un asistente de IA olvida: su ventana de contexto se llena y el principio se disuelve, así que cada sesión nace huérfana — sin reglas, sin historia, sin cicatrices.

Y la documentación que no se reconcilia con la realidad **miente con confianza**. A los seis meses, la mitad de lo que afirman tus notas es falso y nada señala cuál mitad.

vuelamind rompe las dos cosas a la vez — no con una app, sino con disciplina escrita: **no se afirma nada que no se haya comprobado**, y toda afirmación conserva su procedencia: **medido**, **inferido** o **aportado**.

## Qué obtienes

Un vault de texto plano y un ciclo de cuatro actos: **nacer** una vez, **retomarse** al abrir cada sesión —midiendo el estado actual en vez de confiar en lo que se recuerda— y **reconciliarse** al cerrarla.

Dentro: una cola de trabajo ordenada por gravedad real, un registro de decisiones que anota *qué me haría cambiar de opinión*, y **un libro de errores con 41 lecciones, cada una pagada con una equivocación real**. Esa última parte es la valiosa: la estructura se reconstruye en una tarde; las cicatrices no.

## Cómo se empieza

Los dos caminos empiezan igual — por el archivo, no por un comando:

1. Pega `MARCO_Inicial.md` completo en un contexto nuevo de tu asistente.
2. Di: **«inicializa este marco»**.

La primera pregunta es tu idioma. **La segunda decide todo lo que sigue:** ¿este dominio nace aquí, o esta máquina se suma a uno que ya vive?

- **Nace** — contestas la entrevista. Unos veinte minutos, y puedes pausar. Genera el vault, el andamiaje y los comandos del ciclo.
- **Se suma** — sin entrevista y sin generar nada. Llega al vault que ya existe, comprueba que llegó entero, instala el ciclo desde el canon y le pasa el mando a `/vuelamind-join`.

El asistente no se queda con tu palabra: mira la carpeta destino y **se detiene** si dijiste *nace* y encontró meses de trabajo dentro — o si dijiste *me sumo* y no encontró nada.

Sin servidor, sin herramientas, sin cuenta. Un asistente y dos carpetas locales.

## Una máquina, o varias

Todo lo anterior supone una: un asistente y dos carpetas locales. **Esa promesa vale para nacer** — no hace falta nada más para empezar.

**Una segunda máquina necesita alcanzar lo que tiene la primera**: el vault, el andamiaje —su manifiesto, su validador, su memoria— y, si tu dominio verifica contra sistemas vivos, las credenciales para hacerlo. *Cómo* los alcanza lo eliges tú: una carpeta compartida, un montaje, un clon, una réplica automática. El marco no decide el transporte.

`/vuelamind-join` recorre ese camino, y sus comprobaciones son lo valioso: confirma que el vault llegó **entero** —a medio sincronizar es peor que vacío, porque el asistente mide sobre un hueco y concluye con confianza—, instala el ciclo desde el canon y **corre tu validador como prueba de estar dentro**. Que los archivos estén no es lo mismo que poder medir.

**Y ese comando todavía no está en la máquina nueva** — viaja con el nacimiento. Así que una máquina que nunca nació empieza donde empieza todo el mundo: clona este repositorio, pega `MARCO_Inicial.md`, contesta *me sumo*. El archivo trae los comandos consigo; de ahí en adelante manda el comando.

Una máquina que lee el vault pero no alcanza los sistemas sigue siendo una instancia legítima — solo tiene que **decirlo** al declararse, porque a partir de ahí documenta sin verificar.

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
