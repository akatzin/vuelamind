---
description: Instala y deja operando el puente de sesiones (control remoto local de Claude Code sobre Model Garden) — servicio en loopback SIN token (candados de Host/Origin), página de chat con adjuntos, permisos por sesión y progreso en vivo; portable a macOS, Windows y Linux
---

# /vuelamind-rc — control remoto local de sesiones de Claude Code

Levanta un **puente HTTP local** que crea y maneja varias conversaciones de Claude
Code en esta máquina, cada una direccionable por nombre, con una **página de chat**
para operarlas. Nace para cuando **no hay Remote Control** (p. ej. corriendo sobre
Vertex / Model Garden): da una interfaz propia, auto-hospedada, sin abrir nada a la
red.

> [!important] Qué SÍ y qué NO hace
> **SÍ:** crear N conversaciones headless, mandarles turnos (texto + **imágenes**
> + **PDF**), verlas trabajar **en vivo** (qué herramienta corre, con qué),
> listarlas y cerrarlas. Permisos **por sesión**.
> **NO:** engancharse a una sesión interactiva ya abierta en otra terminal — eso
> no tiene vía soportada; lo hace Remote Control y no hay equivalente. Este puente
> maneja conversaciones que **él mismo** crea/continúa (`claude -p --resume`).

> [!danger] REQUISITO: Python 3.10 o superior — y la máquina de fábrica NO lo trae
> **MEDIDO el 2026-09-11 en dos Macs distintas: las dos traen `3.9.6`** y nada más. Es lo
> que instalan las Command Line Tools; sin Homebrew o sin un intérprete bajado a mano, eso
> es todo lo que hay. **Windows no trae Python en absoluto** — y escribir `python` allí no
> falla: abre la Microsoft Store.
>
> El servicio usa anotaciones `X | None`, que en 3.9 **revientan al importar**. Tanto el
> servicio como el instalador se niegan y lo explican, así que no falla en silencio; pero
> **ese requisito se resuelve ANTES**, no durante:
>
> ```sh
> python3 --version      # tiene que decir 3.10 o más
> ```
>
> Si dice menos, instala uno más nuevo y **corre el instalador con ESE binario** — el
> autostart apunta al intérprete con el que lo invocaste, no al que encuentre después.

## Qué instala

- `session_bridge.py` — el servicio (loopback `127.0.0.1`, **sin token**; dos
  candados en su lugar: allowlist de Host + chequeo de Origin en POST/DELETE).
- `session_bridge.html` — la página de chat (misma-origen; el servicio la sirve).
- `install.py` — el instalador portable (abajo).

El código se copia a `~/.claude/vuelamind-rc/`, la config a `~/.claude/vuelamind-rc.env`
y el registro de sesiones a `~/.claude/vuelamind-bridge-sessions.json`.

## Cómo instalar (lo hace el instalador, no a mano)

Desde las herramientas del skill:

```sh
python3 herramientas/interfaz_agente/install.py \
        --permission safe \
        --cwd <ruta-de-trabajo-de-las-sesiones>
```

**`--permission` es obligatorio y no tiene valor por omisión**: `safe` solo lee y conversa,
`tools` añade Python y web, `full` ejecuta todo sin preguntar. Sin la bandera el instalador
se niega — ver la tabla de niveles abajo.

El instalador **detecta el SO** y arma el arranque automático que corresponde:

| SO | Mecanismo | Estado |
|---|---|---|
| macOS | LaunchAgent `com.vuelamind.rc` (`~/Library/LaunchAgents`) | **MEDIDO** |
| Windows | Tarea Programada `VuelamindRC` (`schtasks` desde XML, con `pythonw`) | **MEDIDO** |
| Linux | unidad `systemd --user` (`vuelamind-rc.service`) | INFERIDO |

### En Windows, cuándo arranca: `--sesion`

| | Qué hace | Precio |
|---|---|---|
| **`siempre`** *(default)* | arranca **con la máquina**, haya sesión iniciada o no, y sin guardar contraseña | corre sin escritorio ni credenciales de red — para un servicio en loopback no estorba |
| `interactiva` | arranca al **iniciar sesión**, dentro de la sesión del usuario | **sin sesión abierta no corre**, y el Programador acepta la orden sin ejecutar nada ni dar error |

El default es `siempre` porque es el que no depende de que alguien haya entrado. En macOS y
Linux la bandera no aplica.

> [!danger] Ejecutar el instalador puede requerir tu mano
> En modo auto, tocar el arranque del sistema (`launchctl` / `schtasks` /
> `systemctl`) suele **bloquearse por el clasificador de permisos**. Si pasa, el
> asistente te entrega el comando y **lo corres tú** con el prefijo `!` — no lo
> fuerces. El **núcleo portable** (copiar archivos, escribir el `.env`) sí es
> seguro de validar sin tocar el autostart.

Órdenes útiles del instalador:

```sh
python3 herramientas/interfaz_agente/install.py --status        # ¿está arriba?
python3 herramientas/interfaz_agente/install.py --uninstall     # quita el autostart
python3 herramientas/interfaz_agente/install.py --no-start      # copia los archivos y NO instala el autostart
python3 herramientas/interfaz_agente/install.py --sesion interactiva --permission safe   # Windows: arrancar solo con sesión
python3 herramientas/interfaz_agente/install.py --set CLAUDE_CODE_USE_VERTEX=1 \
        --set ANTHROPIC_VERTEX_PROJECT_ID=<proj> --set CLOUD_ML_REGION=<region>
```

### De dónde saca la config

El `.env` se arma fusionando, de menor a mayor prioridad:
**defaults → plist viejo (migración macOS) → entorno actual → `.env` previo → `--set`/flags.**
Por eso, reinstalando en la misma Mac **hereda solo** la config de Vertex del
servicio hecho a mano; en una máquina nueva hay que **darle las variables** (las
avisa si faltan). La config del **dominio/cuenta vive en el `.env`**; el **código
es portable** — ésa es la separación que hace esto mudable de SO.

## Cómo se opera

1. Abre `http://127.0.0.1:<PORT>/` (default `8850`). Desde otra máquina, **túnel SSH**:
   `ssh -N -L 8850:127.0.0.1:8850 <usuario>@<esta-máquina>` (nunca `0.0.0.0`).
2. **Nueva sesión**: nombre + primer mensaje + **nivel de permiso**. Chatea.
3. **Adjuntos**: botón 📎, pegar, o arrastrar — texto/código (embebido), imágenes
   (`png/jpeg/gif/webp`) y PDF (bloques nativos).
4. **En vivo**: cada turno muestra los pasos (`🔧 Bash`, `📖 Read`, `🌐 WebFetch`…)
   con cronómetro, hasta la respuesta. En la cabecera, el **medidor de contexto**
   sube en vivo: `🧠 42% · 84k/200k · ↑1.2k tok` (ocupación real de la ventana +
   tokens generados en el turno); si `claude` compacta en caliente, sale `🗜️`.
5. **Autocompletar `/`**: al empezar el mensaje con `/`, se despliega la lista de
   skills y comandos filtrada por prefijo (↑↓ para elegir, Enter/Tab para poner).
6. **Cerrar sesión**: botón que la detiene y la olvida.

## Niveles de permiso (por sesión) — la decisión que importa

Las sesiones corren **headless**: no hay quién apruebe permisos en vivo. El nivel
se fija al crear la sesión y se persiste.

> [!important] NO hay nivel por omisión, y es a propósito
> El servicio **se niega a arrancar** si `BRIDGE_PERMISSION` no está declarado en el
> `.env`, y el instalador **exige** `--permission`. Un nivel desconocido —una errata,
> un registro viejo— **no se degrada a `full`**: revienta. `full` concede ejecución
> arbitraria, y nadie debe heredarla por no haber escrito nada.

| Nivel | Banderas | Puede |
|---|---|---|
| `full` | `--permission-mode bypassPermissions` | **todo**: ejecutar, red, escribir/borrar, sin preguntar |
| `tools` | `--allowedTools "Bash(python3:*)" "Bash(python:*)" WebFetch` | Python y web; nada más auto |
| `safe` | (ninguna) | solo lo que no pide permiso: leer, `grep`, chat |

> [!danger] `full` sube la apuesta del acceso local
> Con `full`, **cualquier proceso local que alcance el puerto ejecuta comandos
> arbitrarios con tus privilegios** en esta máquina (por loopback + túnel). No lo
> ates a `0.0.0.0`. Y **respeta los límites del dominio** (no producción, no
> escalar): con `full` ya no hay candado técnico, solo criterio.

## Despertar casas headless — el modo `deliver`

Si un dominio **opera en sesiones headless**, una casa **en reposo** no tiene por
dónde recibir un aviso (los caminos que asumen una terminal interactiva no la
alcanzan). El puente ofrece `POST /sessions/<name>/deliver`: **entregar y soltar**
— arranca el turno, responde en cuanto **arranca** (`init` = el aviso llegó), y se
desengancha **sin matar el turno**. Desacopla *despertar* de *completar*: quien
dispara confirma el acto que de verdad provoca (llegó), no la terminación ajena de
duración no acotada. Detalle y contraste con `/stream` y `/messages` en
`herramientas/interfaz_agente/session_bridge.README.md`.

> [!warning] Lo que `deliver` NO cubre, declarado
> Confirma que el turno **arrancó**, no que terminó. Si el turno **muere después del
> arranque**, `deliver` ya contestó que llegó y **nadie comprueba el desenlace**: no hay
> reintento, no hay alarma, y quien disparó cree que entregó. Se asume a propósito —
> desacoplar despertar de completar es el punto—, pero **queda escrito** porque un
> centinela no puede delatar su propia muerte, y quien monte algo encima de esto tiene
> que saber que la comprobación posterior **no existe todavía y le toca a él**.

## Condiciones medidas (no creer, comprobar)

- **Multimedia headless: MEDIDO** — `claude -p --input-format stream-json` acepta
  bloques `image` y `document` (PDF), y `--resume` por esa vía **conserva memoria**.
- **Model Garden estrecho: MEDIDO** — en el despliegue original **solo `opus`
  estaba aprovisionado**; `haiku`/`opus-5` daban `404`. Por eso el default de
  modelo es **vacío = el del CLI**: el canon no congela un id que caduca ni exige un
  modelo que la casa quizá no tenga aprovisionado. Si tu cuenta necesita uno fijo, lo
  declaras en `BRIDGE_MODEL`.
- **Loopback siempre** — escucha en `127.0.0.1` a propósito; salir por túnel. Atar
  a `0.0.0.0` es un escenario que necesita decisión, no un default.

## Estructura en el canon

```
skills/
  vuelamind-rc.md              # este archivo
herramientas/
  interfaz_agente/
    install.py                 # instalador portable (mac/win/linux)
    session_bridge.py          # el servicio (lee ~/.claude/vuelamind-rc.env al arrancar)
    session_bridge.html        # la página de chat
    session_bridge.README.md   # API y detalle
```

## Por qué está al nivel personal

Como `/vuelamind-load`, este skill **no hardcodea el dominio**: el código es
portable y todo lo específico (proyecto de Vertex, región, `cwd`, puerto) vive en
el `.env`. Por eso puede servir a cualquier máquina o dominio. Si algún día
necesitara saber una ruta concreta de un dominio, ésa sería la señal para bajarlo.
</content>
