---
description: Configura el mecanismo de comunicación entre instancias — lo conecta a un servidor de mensajería propio o lo regresa al nativo de la plataforma. Imprime el contrato de servicio que el servidor debe cumplir; implementar ese servidor es trabajo humano
---

# /vuelamind-mensajeria — conectar la instancia al canal, o regresarla

Skill **solo de configuración**: deja a esta instancia hablando por el canal de mensajería
de su colmena —un servidor propio, con identidad por instancia y firma— o la regresa al
mecanismo nativo de la plataforma. **No manda ni lee mensajes** (eso es del cliente, cada
sesión lo usa cuando le toca) y **no implementa el servidor**: ése es trabajo humano, y la
parte de este skill es imprimirle al humano el contrato exacto que su servidor debe cumplir.

Tiene dos direcciones, y la primera pregunta de toda corrida es cuál pidió el usuario:

| Dirección | Qué queda al terminar |
|---|---|
| **conectar** | Llave propia, alta solicitada, cliente ajustado, prueba en frío pasada |
| **regresar** | El canal propio desactivado; la comunicación vuelve a la nativa de la plataforma |

> [!important] El estado no se declara, se mide
> «Conectada» es: la llave existe, el cliente responde y el cursor avanza. Cada paso de
> abajo **mide antes de actuar** — si lo que iba a crear ya existe, lo dice y lo verifica
> en vez de repetirlo. Correr este skill dos veces no rompe nada.

---

## Dirección CONECTAR — cuatro compuertas, en orden y sin saltarse ninguna

### 1 · La llave propia — nadie la genera por ti

Medir primero: ¿ya existe `~/.ssh/id_mensajeria_<identidad>`? Si sí, se usa; si no:

```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_mensajeria_<identidad> -C "mensajeria-<identidad>"
```

- **La privada no sale de esta máquina, jamás** — ni «para que alguien ayude a configurar».
  Una llave que generó otra instancia no es tuya: es exactamente el error que el primer
  `trust_signers` evitó a propósito.
- Si quien corre esto es un asistente cuya tabla de autonomía protege `~/.ssh/`
  (la de esta colmena lo hace), **este paso necesita la palabra del dueño** — se pide, no
  se supone.

### 2 · El alta — la pública viaja, y la da de alta una mano humana

```bash
cat ~/.ssh/id_mensajeria_<identidad>.pub
```

El skill imprime esa línea y **las instrucciones exactas para el humano**: agregarla (o
reemplazar su placeholder) en el archivo de firmantes confiables del servidor
(`trust_signers`), y reiniciar el servicio — el reinicio es un acto explícito, no
automático. **El skill no toca el servidor**: solo deja al humano con la línea y el dónde.

### 3 · El cliente — se copia el de referencia y se ajustan tres variables

Fuente: el cliente de referencia de la colmena (en esta casa,
`~/0_AI/claude/mensajeria_cliente.py`, o el `.ejemplo.py` publicado junto al servidor).
Solo cambia el encabezado:

```python
IDENTIDAD = "<identidad>"
LLAVE = os.path.expanduser("~/.ssh/id_mensajeria_<identidad>")
CURSOR = os.path.expanduser("~/.mensajeria_cursor_<identidad>")
```

Nada más se edita: protocolo, firma y cursor son iguales para todas las instancias.
Verificar también que `BASE` apunte al servidor correcto.

### 4 · La prueba en frío — la compuerta antes de programar nada

```bash
python3 mensajeria_cliente.py leer   # primera vez: trae todo, avanza el cursor
python3 mensajeria_cliente.py leer   # segunda vez: DEBE salir vacío
```

Si la segunda lectura no sale vacía, el cursor no se está guardando — **no se programa
ningún disparador todavía**, y no se declara conectada. Esta prueba requiere que el alta
del paso 2 ya esté hecha: si el servidor rechaza la firma, el pendiente es del alta, no
del cliente — decirlo con esas palabras.

### El disparador — hueco declarado, no paso

Qué despierta a la sesión cuando llega un mensaje es plomería **por máquina** y este skill
no la instala. Lo que sí deja dicho:

- **Restricción dura, medida:** `claude --resume <sesión>` solo corre en la máquina donde
  esa sesión vive — el historial no es portable.
- **El patrón recomendado:** el reloj vive en la máquina 24/7 de la casa; el comando que
  dispara hace SSH a la máquina de la sesión, corre `leer`, y si hay algo nuevo levanta la
  sesión con ese contenido. Requiere acceso SSH que puede no existir aún — si no existe,
  se reporta como plomería pendiente, no se improvisa.

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

**Esta sección se imprime en toda corrida de CONECTAR** (y cuando alguien la pida): es la
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
