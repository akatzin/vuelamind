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
python3 herramientas/interfaz_agente/install.py --cwd <ruta-de-trabajo-de-las-sesiones>
```

El instalador **detecta el SO** y arma el arranque automático que corresponde:

| SO | Mecanismo | Estado |
|---|---|---|
| macOS | LaunchAgent `com.vuelamind.rc` (`~/Library/LaunchAgents`) | **MEDIDO** |
| Windows | Tarea Programada `VuelamindRC` al iniciar sesión (`schtasks`, con `pythonw`) | INFERIDO (escrito, no probado en Windows) |
| Linux | unidad `systemd --user` (`vuelamind-rc.service`) | INFERIDO |

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
python3 herramientas/interfaz_agente/install.py --no-start      # instala sin arrancar
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

1. Abre `http://127.0.0.1:<PORT>/` (default `8787`). Desde otra máquina, **túnel SSH**:
   `ssh -N -L 8787:127.0.0.1:8787 <usuario>@<esta-máquina>` (nunca `0.0.0.0`).
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

## Condiciones medidas (no creer, comprobar)

- **Multimedia headless: MEDIDO** — `claude -p --input-format stream-json` acepta
  bloques `image` y `document` (PDF), y `--resume` por esa vía **conserva memoria**.
- **Model Garden estrecho: MEDIDO** — en el despliegue original **solo `opus`
  estaba aprovisionado**; `haiku`/`opus-5` daban `404`. Por eso el default de
  modelo es un id de opus explícito. En otra cuenta, ajusta `BRIDGE_MODEL`.
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
