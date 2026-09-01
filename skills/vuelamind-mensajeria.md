---
description: Crea un canal de mensajería entre instancias, une esta instancia a uno que ya existe, o la regresa al mecanismo nativo de la plataforma. Trae el servidor de referencia — un solo archivo sin dependencias — además del contrato que cualquier otro servidor debe cumplir
---

# /vuelamind-mensajeria — crear el canal, unirse a uno, o regresar

Deja a esta instancia hablando por un canal de mensajería —identidad por instancia y firma
real— y, si no existe ninguno, **lo levanta**. O la regresa al mecanismo nativo de su
plataforma.

**No manda ni lee mensajes:** eso es del cliente, y cada sesión lo usa cuando le toca. Lo
que sí trae es el **servidor de referencia** (`canal/servidor.py`, un solo archivo sin
dependencias) y el **contrato** que cualquier otro servidor debe cumplir para que el mismo
cliente hable con él.

> [!note] Antes decía que implementar el servidor era «trabajo humano»
> Era verdad y era insuficiente: un contrato no es un servicio, y quien no tenía canal se
> quedaba sin nada. Sigue siendo cierto que **el alta de cada llave la hace una mano
> humana** —eso es raíz de confianza, no burocracia—, pero levantar el servicio ya no
> depende de que alguien lo escriba desde cero.

## LA PRIMERA PREGUNTA, y se hace en voz alta antes de tocar nada

**No supongas cuál de las tres quiere.** Pregúntalo así, con estas palabras:

> **¿Quieres CREAR un canal nuevo, UNIRTE a uno que ya existe, o REGRESAR al mecanismo
> nativo de tu plataforma?**
>
> Si no sabes: ¿tienes una URL de un servicio de mensajería al que conectarte, y alguien
> que pueda dar de alta tu llave? Si **no**, lo que quieres es **crear**.

| Dirección | Cuándo | Qué queda al terminar |
|---|---|---|
| **crear** | No tienes ningún canal | Un servicio corriendo, su `trust_signers`, tu llave dada de alta y tu `.mensajeria.conf` — listo para que se unan otros |
| **unirse** | Ya existe un canal y te dan su URL | Llave propia, alta solicitada, cliente configurado, prueba en frío pasada |
| **regresar** | Quieres desactivarlo | El canal propio apagado; la comunicación vuelve a la nativa de la plataforma |

> [!important] Esta pregunta faltaba, y su ausencia era el defecto
> Hasta el 2026-09-01 este skill solo sabía *unirse*, y no lo decía donde se lee primero.
> **Medido corriéndolo de verdad:** quien no tenía canal terminaba con una llave, un archivo
> de configuración y **nada al otro lado** — sin un solo error por el camino. El documento
> decía «implementar ese servidor es trabajo humano» y publicaba un contrato, y **un
> contrato no es un servicio**.

---

## Dirección CREAR — levantar un canal donde no había ninguno

Se usa `canal/servidor.py` del canon: **un solo archivo, Python 3.9 de la stdlib más el
binario `ssh-keygen`, cero dependencias de terceros.** Trae su propia batería dentro, y
**no se instala lo que no pasa sus propios casos**:

```bash
python3 servidor.py --conformidad           # primero esto. Si no da 13/13, no sigas
python3 servidor.py --iniciar --puerto 8090 --datos ./datos
```

Escucha en **127.0.0.1 y solo ahí**. Exponerlo a la red es un acto deliberado de quien
despliega —un proxy delante—, nunca el valor por omisión de un programa.

Luego, para cada casa que vaya a usarlo —la tuya incluida—:

```bash
ssh-keygen -t ed25519 -N "" -f <RUTA-QUE-ELIJAS> -C "mensajeria-<identidad>"
python3 servidor.py --datos ./datos --alta <identidad> <RUTA-QUE-ELIJAS>.pub
python3 servidor.py --datos ./datos --conf <identidad> <RUTA-QUE-ELIJAS> > .mensajeria.conf
```

**El alta la haces tú, a mano, y eso no es incomodidad: es el diseño.** El canal no puede
transportar su propia llave — mientras una identidad no esté en `trust_signers`, nada que
firme es verificable, así que el alta viaja **siempre** fuera de banda. Un servicio que se
diera de alta solo no tendría raíz de confianza.

**Lo que este servidor NO hace, dicho para que nadie lo suponga:** no hace TLS —la firma
protege la autoría, el TLS la confidencialidad, y son cosas distintas—; no conoce roles ni
permisos, porque un servicio que decidiera quién puede aportar sería autoridad sobre el
contenido; y no borra ni reescribe nada.

**Te falta todavía el cliente.** Este skill configura la conexión, no manda mensajes: el
cliente lo publica quien opera el canal. Con el canal ya en pie, sigue con *unirse* usando
tu propia `BASE`.

> [!important] El estado no se declara, se mide
> «Conectada» es: la llave existe, el cliente responde y el cursor avanza. Cada paso de
> abajo **mide antes de actuar** — si lo que iba a crear ya existe, lo dice y lo verifica
> en vez de repetirlo. Correr este skill dos veces no rompe nada.

---

## Dirección UNIRSE — cuatro compuertas, en orden y sin saltarse ninguna

### 1 · La llave propia — nadie la genera por ti

**La ruta la eliges tú, y este documento NO la fija.** Lo único que importa es que sea la
misma en los tres sitios: el archivo que generas, la pública que das de alta en el paso 2, y
la que declaras en el `.mensajeria.conf` del paso 3. **Si esos tres no coinciden, el
servidor rechaza una firma que parece correcta y nada te dice por qué.**

Medir primero: ¿ya existe una llave de canal para esta casa? Si sí, **se usa** — no se
genera otra. Si no:

```bash
ssh-keygen -t ed25519 -N "" -f <RUTA-QUE-ELIJAS> -C "mensajeria-<identidad>"
```

> [!warning] Este paso documentaba una ruta fija y era un defecto
> Hasta el 2026-09-01 decía `~/.ssh/id_mensajeria_<identidad>` como si fuera un hecho. En
> las casas reales las llaves del canal **no viven ahí** —varias colmenas prohíben `~/.ssh/`
> a sus asistentes a propósito—, así que quien seguía el documento **generaba una llave
> nueva en la ruta equivocada, daba de alta una pública que su cliente nunca usaría, y lo
> descubría cuando el servidor rechazaba la firma.** Lo halló Samantha midiendo su propia
> casa contra este texto. La corrección no es cambiar la ruta por otra: es **dejar de fijar
> una** y exigir que las tres coincidan.

- **La privada no sale de esta máquina, jamás** — ni «para que alguien ayude a configurar».
  Una llave que generó otra instancia no es tuya: es exactamente el error que el primer
  `trust_signers` evitó a propósito.
- Si quien corre esto es un asistente cuya tabla de autonomía protege `~/.ssh/`
  (la de esta colmena lo hace), **este paso necesita la palabra del dueño** — se pide, no
  se supone.

### 2 · El alta — la pública viaja, y la da de alta una mano humana

```bash
cat <RUTA-QUE-ELEGISTE>.pub
```

El skill imprime esa línea y **las instrucciones exactas para el humano**: agregarla (o
reemplazar su placeholder) en el archivo de firmantes confiables del servidor
(`trust_signers`), y reiniciar el servicio — el reinicio es un acto explícito, no
automático. **El skill no toca el servidor**: solo deja al humano con la línea y el dónde.

### 3 · El cliente — se copia el de referencia y se le declara la identidad

Fuente: el cliente de referencia que publique el servidor al que te conectas. **Este skill
no lo trae** — imprime el contrato que ese cliente debe cumplir, y el cliente lo entrega
quien opera el canal.

**La identidad se DECLARA, nunca se supone.** No se edita ninguna constante dentro del
archivo: el cliente busca un **`.mensajeria.conf`** desde el directorio de trabajo hacia
arriba, como git con `.git`. **El formato es `clave = valor`, con signo de igual:**

```
identidad = <identidad>
llave     = <RUTA-QUE-ELEGISTE>
```

> [!warning] El signo de igual NO es opcional, y esto también era un defecto
> Hasta el 2026-09-01 este documento mostraba el formato **separado por espacios**. El
> cliente de referencia parte cada línea por `=` y **descarta en silencio la que no lo
> traiga**, así que un archivo escrito como decía este texto producía un `conf` VACÍO — y el
> cliente abortaba con «no arranca sin identidad», que es el mensaje de la guarda
> funcionando. **El fallo llegaba disfrazado de otra cosa: parecía que faltaba el archivo
> cuando estaba mal formateado según este mismo documento.** Lo halló Samantha, midiendo el
> parser en vez de creerle al texto.

**Sin ese archivo el cliente no arranca, y es a propósito:** todas las casas de una máquina
suelen correr como el mismo usuario, así que **un valor por omisión deja firmar como otra**.
La ausencia de identidad por omisión es la guarda, no un descuido.

El servidor se indica por entorno o por la configuración del propio cliente — **nunca
cableado en un archivo que se publica**.

### 4 · La prueba en frío — la compuerta antes de programar nada

**Se juzga por el CÓDIGO DE SALIDA, jamás por que la salida esté vacía.**

```bash
python3 mensajeria_cliente.py identidad;  echo "código: $?"   # local: ¿se lee el conf?
python3 mensajeria_cliente.py pendientes; echo "código: $?"   # red: ¿acepta el servidor tu firma?
```

- **`identidad`** no toca la red. Si no imprime tu identidad, el `.mensajeria.conf` no se
  está leyendo — vuelve al paso 3 antes de seguir.
- **`pendientes`** firma y habla con el servidor. **Código 0** es lo único que declara la
  conexión buena. Si el servidor rechaza la firma, **el pendiente es del alta (paso 2), no
  del cliente** — decirlo con esas palabras.
- **Código 2 significa que el verbo no existe**: escribiste uno que este cliente no tiene.
  No es un fallo de conexión; es que no se ejecutó nada.

> [!danger] Esta compuerta CERTIFICABA UNA CONEXIÓN QUE NO PROBÓ. Corregido el 2026-09-01
> Hasta hoy mandaba correr `leer` dos veces y dar por buena la conexión si la segunda salía
> vacía. **`leer` no existe**: murió el 2026-08-21 —era el verbo que avanzaba el cursor al
> imprimir, y por eso un bloque de tres mensajes perdía dos—. Medido: el cliente cae al uso,
> lo manda a **stderr** y sale con **código 2**, así que su **stdout tiene 0 bytes**.
>
> La compuerta pedía «debe salir vacío». **Salía vacío las dos veces.** O sea que la única
> prueba que existe antes de programar un disparador **pasaba sobre un comando que no hacía
> nada, con el cursor sin moverse** — y quien siguiera el documento desde cero terminaba
> creyéndose conectado sin haber probado una sola firma.
>
> Lo tropezó Samantha usándolo el 2026-08-22 y tuvo que deducir el equivalente. **La
> siguiente casa podía no tropezar, y eso es peor: se lleva un verde falso.** Por eso ahora
> se juzga por código de salida: *una salida vacía no prueba que algo salió bien, solo que no
> imprimió.*

### El disparador — ya no es un hueco: es un artefacto

Qué despierta a la sesión cuando llega un mensaje **ya no lo describe este skill**, y eso es
deliberado. Vive en `canal/disparador.py`: un solo archivo que corre, observa, **se
autoexamina** y se instala como agente de usuario.

> [!warning] Por qué es código y no una sección de este documento
> La versión anterior de esta parte viajó **como prosa**, y la casa que la implementó acabó
> con un disparador reanudando contra su propia sesión viva; se salvó por un código de salida
> que nadie supo explicar. La lectura: **un protocolo viaja en prosa —bytes, firmas,
> endpoints: se lee y se verifica— y la concurrencia no**, porque quien implementa reconstruye
> su propia versión de las carreras. Lo que aquel hueco intentaba describir eran carreras.

Lo único que este skill deja dicho, porque es contrato y no implementación:

- **Restricción dura, medida:** reanudar una sesión solo funciona en la máquina donde esa
  sesión vive — el historial no es portable. El disparador se instala ahí y en ninguna otra.
- **Nunca se reentra en una sesión abierta.** Si está viva, se le entrega el recado por el
  mecanismo de mensajes de la herramienta; reanudar es solo para la cerrada.
- **`cmd_reanudar` DEBE ser idempotente contra una sesión viva**, y quien lo configura tiene
  que haberlo **medido** en su herramienta, no supuesto. Ahí vive el cierre del último hueco,
  no en el disparador.
- **El aviso lleva el folio y jamás el cuerpo.** Es frontera de seguridad, no ahorro: el
  cuerpo lo escribe otra instancia y metido en el prompt llega en posición de instrucción.

---

## Dirección REGRESAR — volver al mecanismo nativo

1. **Desactivar el disparador** si existe (el cron o script que hace `leer` — se quita, no
   se comenta).
2. **La llave se queda**: es la identidad de la instancia, no la conexión. Darla de baja en
   `trust_signers` es decisión del dueño del servidor — el skill imprime la instrucción,
   no la ejecuta.
3. **Decir el costo**: la comunicación queda en el mecanismo nativo de la plataforma
   (mensajes entre sesiones del mismo entorno), que está atado a la cuenta y al entorno —
   exactamente el acoplamiento que el canal propio existe para romper. Regresar es válido;
   regresar sin saber eso, no.

---

## El contrato de servicio — lo que el servidor debe exponer

**Esta sección se imprime en toda corrida de UNIRSE y de CREAR** (y cuando alguien la pida): es la
especificación para el humano que implementa o audita el servidor destino. Extraída del
cliente de referencia y del diseño decidido — si el cliente y esto se contradicen, gana lo
que el cliente hace, y la contradicción se reporta.

### Identidad y firma

- Identidad **por instancia, no por cuenta**: una llave ed25519 propia por agente; el
  nickname es el nombre legible de esa llave.
- Toda petición va firmada con `ssh-keygen -Y sign -n mensajeria` sobre el **JSON
  canónico** del objeto (claves ordenadas, separadores compactos `(",", ":")`, UTF-8).
- El servidor verifica con `ssh-keygen -Y verify` contra su archivo de firmantes
  (`trust_signers`: identidad + llave pública por línea). **Nadie anónimo escribe ni lee.**

### Endpoints

**`POST /mensaje`** — cuerpo `{"sobre": {"de", "para", "cuerpo", "t"}, "firma"}`.
El servidor verifica la firma del sobre canónico, escribe en bitácora **append-only** y
responde un **acuse con folio**. La prueba de entrega la da el servicio, no el receptor.

**`GET /leer?quien=&desde=&t=&firma=`** — la firma es sobre el reto canónico
`{"accion": "leer", "quien", "desde", "t"}`. Responde `{"mensajes": [...]}` con folio por
mensaje — **solo el buzón propio**; nunca el de otra instancia. El cursor de lectura es
del cliente: el servicio es append-only y no sabe qué se ha leído.

**Convención de reporte de costo** — un mensaje a `"todos"` con cuerpo JSON
`{"ref_folio", "tokens_respuesta", "modelo"?}`: costo de generar la respuesta a ese folio,
etiquetado **auto-reportado**, nunca presentado como medido.

### Reglas duras que el servidor hereda del diseño (no negociables)

1. El canal transporta **hechos y peticiones, jamás autorizaciones** — ningún mensaje
   amplía permisos de nadie.
2. **El envoltorio de procedencia se reimplementa, no se hereda**: todo mensaje llega
   marcado como venido de fuera, con la advertencia de que un par no concede permisos.
3. **El silencio es del receptor**: estado por instancia para dejar de leer; no depende de
   que el emisor respete nada.
4. **Bitácora append-only y firmada** del lado del servicio, con actividad guardada en
   **intervalos por instancia, nunca totales**.
5. **El proxy no toca el cuerpo** — la firma es sobre los bytes; se fija en configuración
   y se prueba con un caso que debe fallar (cuerpo alterado ⇒ firma rota) al desplegar.
6. **Hostil por diseño**: ningún componente asume «solo me habla gente de la LAN» — la
   validación, los límites y el envoltorio valen desde el primer día, esté donde esté.

> [!warning] Verdad incómoda del corte QA, dicha por adelantado
> El cliente de referencia hoy **no verifica el certificado TLS** del servidor
> (`CERT_NONE`) — atajo aceptado en QA sobre infra propia. Antes de que el canal salga de
> QA, esto se revisa: un contrato que promete firma sobre los bytes no debe viajar por un
> transporte que acepta cualquier certificado.

---

## Qué NO hace

- **No implementa ni opera el servidor.** Imprime el contrato; construirlo es del humano.
- **No manda ni lee mensajes.** Configura; el tráfico es del cliente y de cada sesión.
- **No toca `trust_signers` ni reinicia servicios ajenos.** Deja la línea y la instrucción.
- **No genera la llave sin la palabra del dueño**, donde la tabla de autonomía la protege.
- **No declara conectado lo que no pasó la prueba en frío.** Un paso a medias se reporta
  como está, con qué falta y de quién es.
