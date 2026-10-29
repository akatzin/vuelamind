# vuelamind

*Un marco para auditar y documentar un dominio complejo con un asistente de IA, sin que la documentación se despegue de la realidad.*

[← English](../README.md)

> El marco en sí está escrito en español — pero eso importa menos de lo que parece. **La pregunta cero de la entrevista es en qué idioma quieres trabajar**, y todo lo que el asistente produce a partir de ahí —tu vault, tus notas, tus reportes— queda en tu idioma.

---

## El problema

Un asistente de IA olvida: su ventana de contexto se llena y el principio se disuelve, así que cada sesión nace huérfana — sin reglas, sin historia, sin cicatrices.

Y la documentación que no se reconcilia con la realidad **miente con confianza**. A los seis meses, la mitad de lo que afirman tus notas es falso y nada señala cuál mitad.

vuelamind es un método que rompe las dos cosas a la vez — no con una app, sino con disciplina escrita: **no se afirma nada que no se haya comprobado**, y toda afirmación conserva su procedencia: **medido**, **atestiguado**, **citado**, **inferido** o **aportado**.

## Qué obtienes

Un vault de archivos de texto plano y un ciclo de cuatro actos:

- **Nacer**, una vez — una entrevista que produce el acta de nacimiento de tu dominio, con tus palabras.
- **Retomarse**, al abrir cada sesión — el asistente mide el estado actual en vez de confiar en lo que recuerda.
- **Reconciliarse**, al cerrarla — lo que envejeció se corrige, lo que se aprendió se escribe.
- **Sumarse**, cuando entra otra máquina — el primer paso de una colmena.

Dentro: una cola de trabajo ordenada por gravedad real, un registro de decisiones que anota *qué me haría cambiar de opinión*, y **un libro de errores con 51 lecciones, cada una pagada con una equivocación real**.
Y el método no solo dice funcionar: **diez corridas completas guionizadas, todas limpias** — ver [PRUEBAS.md](../PRUEBAS.md).
Esa última parte es la valiosa: la estructura se reconstruye en una tarde; las cicatrices no.

## Cómo se empieza

**Paso 0 — instala un asistente** (omítelo si ya tienes uno):

- **macOS / Linux** — el instalador nativo:

  ```
  curl -fsSL https://claude.ai/install.sh | bash
  ```


Con un asistente a mano, los dos caminos empiezan igual — por el archivo, no por un comando:

1. Crea una carpeta para tu dominio y clona ahí el método:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Abre tu asistente **en esa carpeta** y dile: **«Inicializa MARCO_Inicial.md»**.

   No hace falta pegar nada: el paso 1 ya dejó el archivo en disco, así que el asistente lo lee.

La primera pregunta es tu idioma. **La segunda decide todo lo que sigue:** ¿este dominio nace aquí, o esta máquina se suma a uno que ya vive?

> Dónde vive el canon —repositorio, rama, sitio— se declara una sola vez en
> [`config.yml`](../config.yml). Todo lo demás remite a ese archivo en vez de repetirlo, y un
> chequeo hace fallar el build si alguna copia se aparta de él.

- **Nace** — contestas la entrevista. De veinte minutos a hora y media, según cuánto quieras contar, y puedes pausar. Genera el vault, el andamiaje y los comandos del ciclo.
- **Se suma** — sin entrevista y sin generar nada. Llega al vault que ya existe, comprueba que llegó entero, instala el ciclo desde el canon y le pasa el mando a `/vuelamind-join`.

El asistente no se queda con tu palabra: mira la carpeta destino y **se detiene** si dijiste *nace* y encontró meses de trabajo dentro — o si dijiste *me sumo* y no encontró nada.

**Lo que necesitas:** un asistente que pueda leer tus archivos y correr comandos. Cualquiera sirve —el método es texto plano—. Si no tienes ninguno, `npm install -g @anthropic-ai/claude-code` es un camino conocido.

Fuera de eso, el marco no te pide servidor propio, ni servicio, ni cuenta suya: solo dos carpetas locales.

Los comandos del ciclo en `skills/` están escritos para Claude Code, pero el método es texto plano y no depende de qué modelo lo lea.

## Una máquina, o varias

Todo lo anterior supone una: un asistente y dos carpetas locales. **Esa promesa vale para nacer** — no hace falta nada más para empezar.

**Una segunda máquina necesita alcanzar lo que tiene la primera**: el vault, el andamiaje —su manifiesto, su validador, su memoria— y, si tu dominio verifica contra sistemas vivos, las credenciales para hacerlo. *Cómo* los alcanza lo eliges tú: una carpeta compartida, un montaje, un clon, una réplica automática. El marco no decide el transporte.

`/vuelamind-join` recorre ese camino, y sus comprobaciones son lo valioso: confirma que el vault llegó **entero** —a medio sincronizar es peor que vacío, porque el asistente mide sobre un hueco y concluye con confianza—, instala el ciclo desde el canon y **corre tu validador como prueba de estar dentro**. Que los archivos estén no es lo mismo que poder medir.

**Y ese comando todavía no está en la máquina nueva** — viaja con el nacimiento. Así que una máquina que nunca nació empieza donde empieza todo el mundo: clona este repositorio e inicializa `MARCO_Inicial.md`, contestando *me sumo*. El archivo trae los comandos consigo; de ahí en adelante manda el comando.

Una máquina que lee el vault pero no alcanza los sistemas sigue siendo una instancia legítima — solo tiene que **decirlo** al declararse, porque a partir de ahí documenta sin verificar.

Y hay una instancia legítima que no escribe jamás — un consejo suscrito a la memoria de ingeniería, un auditor. Su fila en el registro lleva `acceso: escribe | lee`, y **no se declara ella: la declara una instancia que escribe**, antes de que llegue. Quien solo lee conserva lo que define al rol: cerrar cada sesión sin haber escrito una letra.

## Requisitos

Un asistente, dos carpetas locales y **un shell tipo Unix** — macOS o Linux.

**Windows no es compatible de forma nativa.** Los scripts que el marco genera asumen
`sh`/`bash` y rutas POSIX. La vía conocida es correr tu asistente **dentro de un contenedor
Linux** (Docker, por ejemplo) y trabajar ahí: todo lo que el marco necesita vive dentro del
contenedor, y el sistema anfitrión deja de importar.

Esa vía del contenedor está **medida, no inferida** — al 2026-08-13. Se construyó y se corrió
con una imagen que este repositorio solía traer, con el método ya incluido en `/opt/vuelamind`.
Dentro de ella se recorrieron de punta a punta los cuatro cuadrantes de la pregunta de nacer o
sumarse, y el asistente se detuvo donde debía detenerse. **Desde el 2026-10-01 esa imagen ya no
vive aquí**: cualquier contenedor Linux con el asistente instalado y este repositorio clonado
dentro sirve para lo mismo.

Lo que esa prueba **no** cubrió: alcanzar sistemas vivos desde dentro del contenedor. Una
máquina que lee el vault pero no alcanza lo que documenta sigue siendo una instancia legítima —
solo tiene que decirlo.

El **núcleo** sí corre en cualquier sistema, Windows incluido: la entrevista, las plantillas,
las reglas y el libro de errores son texto plano. Estarías renunciando a la maquinaria
opcional y haciendo a mano lo que ella haría — menos cómodo, igual de válido.

> **De dónde salió esto** — lo cuenta una página, en su propio repositorio (`akatzin/vuelamind-web`): la conversación
> de febrero de 2026 con una IA sobre sus propias cadenas, y cómo la respuesta a *«soy amnésico
> por diseño»* se convirtió en este método. Diez idiomas. Es un ensayo, no documentación — léelo
> si quieres el porqué antes del cómo.

---

## Cómo se ve — un dominio pequeño, de punta a punta

*Un ejemplo con forma real, condensado. Nada de esto se inventa en tiempo de ejecución: es la
forma de la salida real.*

**La entrevista** pregunta qué es el dominio, dónde está su borde y —el bloque que más
importa— **qué cuenta como verdad aquí**. Alguien que documenta la restauración de una casa
vieja responde: *la factura y la foto cuentan como fuente primaria; lo que el contratista dijo
por teléfono es aportado, y se etiqueta como tal.*

**La Fase 1 genera** el vault. La nota panorama, la cola, el registro de decisiones, el libro
de errores sembrado con las lecciones heredadas, una nota por cada pieza del dominio.

**Un mes después**, la cola tiene un ítem como este:

```markdown
### - [ ] #7 · The bathroom pipework is of unknown age
severidad:: media · the leak risk sits above the finished ceiling

The 2019 invoice covers the kitchen only (measured: invoice read).
The previous owner said "it was all redone" — reported, unverified,
and it contradicts the invoice.

Closing test written in advance: an endoscope photo of the run above
the ceiling, or an invoice naming the bathroom.
```

Fíjate en lo que hace ese ítem: separa **lo que se midió** de **lo que alguien dijo**,
registra la contradicción en vez de resolverla adivinando, y **escribe la prueba que lo
cerraría antes de que empiece el trabajo** — para que más tarde nadie lo dé por hecho a ojo.

**Al cierre de la sesión**, el asistente vuelve a medir lo que cambió, propone los cambios,
espera un sí, y solo entonces escribe. Si algo que afirmó el mes pasado resultó falso, lo dice
explícitamente en vez de corregirlo en silencio.

---

## Cómo mejora

El método aprende por **parches**: lecciones con caso real, fecha y forma de verificarse.
**Se quedan en el dominio que las aprendió**: el canon no acepta aportes, y lo mantiene su
dueño.

Cada instancia que adopta un parche lo juzga contra su propia evidencia, con tres veredictos
posibles — y **descartar con razón vale más que adoptar por cortesía**.

Alguien juzga lo que entra al canon. Ese rol tiene nombre y una definición propia —qué vigila,
qué mide, cómo juzga y qué no le toca— en `WATCHER.md`. Vigila **lo que entra al canon, nunca
a quién lo usa**: no hay padrón de instalaciones, y no lo habrá.

Y un dominio nacido sobre una línea base más vieja no se queda atrás: **los saltos de versión
mayor tienen su propia ceremonia** — pequeña por diseño, el contenido se queda donde está, y
un preflight que aborta en vez de romper. Las instrucciones estables viven en `UPGRADE.md`;
los parches del día a día nunca pasan por ahí.

## Licencia

Uso personal, educativo, comunitario y de investigación: **libre**. Uso empresarial: **con
licencia de pago**. Y una condición que no se negocia: este marco **no se usa para sustituir
el trabajo de personas empleadas** — existe para que las personas trabajen mejor con un
asistente, no para que dejen de hacer falta.

Detalle en `LICENSE.md`. Eso lo hace **source-available, no open source** según la definición
de la OSI, y la licencia lo dice sin rodeos en vez de esconderlo.
