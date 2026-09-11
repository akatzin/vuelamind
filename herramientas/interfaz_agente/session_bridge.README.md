# session_bridge — puente HTTP local a sesiones de Claude Code

Servicio HTTP **en loopback, sin token**, que **crea y maneja varias conversaciones
de Claude Code** en esta máquina, cada una direccionable por nombre. Pensado para
uso local; accesible desde fuera **por túnel SSH** (nunca abre a la red).

## Qué SÍ y qué NO hace

- **SÍ:** crear N conversaciones headless, mandarles turnos y leer la respuesta
  (texto limpio, JSON), listarlas y borrarlas. Multi-sesión por nombre.
- **SÍ adjuntos** (paridad parcial con el cliente nativo, MEDIDO en Vertex/opus
  2026-09-10): **texto/código** (se embebe en el mensaje), **imágenes**
  (`png/jpeg/gif/webp`, bloque `image`) y **PDF** (bloque `document`). En la
  página web: botón 📎, pegar, o arrastrar y soltar. Botón **«Cerrar sesión»**
  (= `DELETE`) para detener y olvidar una conversación.
- **NO:** engancharse a una sesión interactiva ya abierta en una terminal. Claude
  Code **no tiene vía soportada** para eso; lo hace Remote Control y no hay
  equivalente auto-hospedado. Este puente maneja conversaciones que **él mismo**
  crea/continúa (vía `claude -p --resume`).

## Arrancar

```sh
python3 session_bridge.py            # 127.0.0.1:8787
PORT=9000 python3 session_bridge.py  # otro puerto
```

### Desde otra máquina — túnel SSH (así se "expone", sin abrir 0.0.0.0)

```sh
ssh -N -L 8787:127.0.0.1:8787 <usuario>@<esta-máquina>
# ahora http://127.0.0.1:8787 en tu máquina llega al puente
```

## Seguridad (sin token, dos candados en su lugar)

El modelo de confianza es **"solo esta máquina"**: no hay token. Loopback por sí
solo NO basta contra el navegador, así que hay dos candados:

- **Allowlist de Host** → sólo `127.0.0.1` / `localhost`. Corta el DNS-rebinding
  (una página en `attacker.com` resuelta a `127.0.0.1` llega con `Host=attacker.com`
  y se rechaza).
- **Chequeo de Origin** en los métodos que cambian estado (`POST`/`DELETE`): sin
  `Origin` (cliente no-navegador o navegación de nivel superior) se permite; con
  `Origin`, debe ser el propio. El navegador manda `Origin` verídico en cross-site,
  así que una página maliciosa no puede disparar una sesión (CSRF/RCE).

Lo que queda expuesto —y se asume— es **otro usuario/proceso LOCAL** en la máquina.

## API

| Método | Ruta | Cuerpo | Devuelve |
|---|---|---|---|
| GET | `/health` | — | `{"ok":true}` |
| GET | `/sessions` | — | registro local + salida de `claude agents --json --all` |
| POST | `/sessions` | `{name, prompt, cwd?, model?, permission?, attachments?}` | `{name, session_id, text}` |
| POST | `/sessions/<name>/messages` | `{message, attachments?}` | `{name, session_id, text}` (todo al final) |
| POST | `/sessions/<name>/stream` | `{message, attachments?}` | **NDJSON en vivo**: `init` / `tool` / `text` / `result` / `error` |
| POST | `/sessions/<name>/deliver` | `{message, attachments?}` | `{name, session_id, started}` — **entregar y soltar** |
| DELETE | `/sessions/<name>` | — | `{deleted, stopped_short_id}` |

`/stream` emite una línea JSON por evento según ocurre (progreso paso a paso: qué
herramienta corre y con qué). La web lo usa para pintar `🔧 Bash: …`, `📖 Read: …`
mientras el turno trabaja. `/messages` sigue existiendo (bloqueante) para `curl`.

### `/deliver` — entregar y soltar (despertar casas headless)

Existe para **despertar una casa que opera en sesiones headless**: quien dispara
(un trigger de mensajería, un cron) sólo necesita saber que el aviso **llegó** —que
el turno **arrancó**—, no esperar a que **termine**, que es trabajo ajeno de
duración no acotada.

- Arranca el turno en un **hilo propio**, espera el evento `init`, y **responde**
  `{"started": true, "session_id": …}` en cuanto arranca (segundos).
- El turno **sigue hasta terminar aunque el cliente cierre la conexión** — no se
  mata por desconexión, sólo por `BRIDGE_TIMEOUT`.
- Si el turno **no arranca** (p. ej. `claude` falla): `502 {"started": false}`.
  Si `init` no llega dentro de `BRIDGE_DELIVER_INIT_TIMEOUT`: `504`.
- Contrasta con `/stream` y `/messages`, que **atan el turno a la conexión**: si
  quien dispara cierra o su timeout corta, el turno muere. `/deliver` no.

Diferencia de diseño: `/deliver` **desacopla despertar de completar**. Confirma el
acto que el disparador de verdad provoca (llegó el aviso), no la terminación ajena.

`attachments`: lista de `{name, media_type, data}` con `data` en **base64**.
`media_type` soportado: `image/png|jpeg|gif|webp` (bloque `image`),
`application/pdf` (bloque `document`), `text/*` (se decodifica y embebe como
texto). Otros tipos se ignoran. Límites del cliente web: 5 MB imagen, 20 MB PDF,
512 KB texto.

### Ejemplo

```sh
B=http://127.0.0.1:8787

curl -s -X POST $B/sessions \
  -d '{"name":"demo","prompt":"Hola, preséntate en una línea"}'

curl -s -X POST $B/sessions/demo/messages \
  -d '{"message":"¿qué hora manejas?"}'

# entregar-y-soltar: responde apenas arranca el turno, no al final
curl -s -X POST $B/sessions/demo/deliver \
  -d '{"message":"[CANAL] tienes un mensaje: folio 1234"}'

curl -s $B/sessions | jq
curl -s -X DELETE $B/sessions/demo
```

## Niveles de permiso (por sesión)

Las sesiones corren **headless**: no hay quién apruebe permisos en vivo, así que
el nivel se fija al crearla (campo `permission`, o el selector en la web). Default
`full`. Persistido en el registro; se reusa en cada turno.

| Nivel | Banderas | Puede |
|---|---|---|
| `full` | `--permission-mode bypassPermissions` | **todo**: ejecutar, red, escribir/borrar, sin preguntar |
| `tools` | `--allowedTools "Bash(python3:*)" "Bash(python:*)" WebFetch` | correr Python y consultar la web; nada más auto |
| `safe` | (ninguna) | solo lo que no pide permiso (leer, `grep`, chat) |

> `full` significa que **cualquier proceso local que alcance el puerto puede
> ejecutar comandos arbitrarios con tus privilegios** en esta máquina (loopback).
> Es la razón de más peso para no atar el puente a `0.0.0.0` y respetar los límites
> del dominio (no producción, no escalar): con `full` ya no hay candado técnico,
> solo criterio.

## Condiciones (léelas, esto es capacidad-con-condición)

- **Modelo por defecto `opus`.** En este Model Garden (`sub-pro-dig-app`) **haiku
  NO está aprovisionado** — un subproceso a haiku devuelve `404 model_not_found`.
  No pases `"model":"haiku..."` salvo que primero lo aprovisionen.
- **Solo loopback.** Escucha en `127.0.0.1` a propósito; salir por túnel SSH. Si
  algún día se ata a `0.0.0.0`, eso es el escenario del `#119` y necesita decisión.
- **Facturación por consumo.** Quien alcance el puerto puede invocar modelos que
  **se facturan por consumo** en GCP. Otra razón para no exponerlo.
- **Permisos de herramientas en headless:** las sesiones creadas corren en el modo
  de permiso fijado al crearlas; si una tarea intenta usar herramientas que piden
  permiso y el nivel no las cubre, en headless no hay quién conteste.

## Variables de entorno

`PORT`, `BRIDGE_MODEL`, `BRIDGE_PERMISSION`, `BRIDGE_CWD`, `BRIDGE_TIMEOUT`,
`BRIDGE_DELIVER_INIT_TIMEOUT`, `BRIDGE_CLAUDE_BIN`, `BRIDGE_REGISTRY`.
</content>
</invoke>
