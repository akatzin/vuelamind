---
description: Pone al día un Session Bridge YA INSTALADO contra el canon — mide qué versión corre por huella, respalda, escribe, verifica y reinicia solo si cambió el backend. No instala nada: para eso está /vuelamind-rc
---

# /vuelamind-rc-update — poner al día el puente que ya corre

Trae a un **Session Bridge instalado** los cambios que el canon publicó desde que se instaló.

> [!important] Por qué esto no lo cubre el salto de versión
> **`/vuelamind-upgrade` escala el DOMINIO a una versión liberada del marco.** Trae la
> plantilla, los skills y el método. **No toca lo que nació del canon y vive por su cuenta**:
> un servicio en un puerto, con su configuración, su respaldo y su proceso corriendo.
>
> Esa distinción no es teórica. En una sola jornada el puente cambió **siete veces** y la casa
> que lo operaba tuvo que resincronizar **tres**, a mano y por mensajes: mandar los archivos,
> comprobar huellas, acordarse de reiniciar si había tocado el backend. Este skill es ese
> trabajo, hecho igual cada vez.
>
> **Y por eso se llama `update` y no `upgrade`:** el puente **no tiene versiones**, cambia
> commit a commit. Llamarlo *upgrade* prometería un salto de versión que no existe y chocaría
> con el comando que sí lo hace.

## Qué NO hace

- **No instala.** Si la máquina no tiene puente, lo dice y manda a `/vuelamind-rc`. Instalar
  es otra decisión: elige puerto, permisos, modelo y arranque automático.
- **No sobrescribe un archivo modificado localmente.** Lo detecta, lo dice, y para.
- **No toca la configuración.** El `.env` es de esa máquina: puerto, modelo, permisos y `cwd`
  se quedan como estén.

## 0. Medir antes de mover nada

```
python3 <clon>/herramientas/interfaz_agente/rc_estado.py <clon-del-canon>
```

Identifica la versión instalada **buscando su huella en la historia del canon**, que es el
registro de versiones que el puente no tiene escrito. Cuatro desenlaces, y cada uno pide otra
cosa:

| Salida | Qué significa | Qué se hace |
|---|---|---|
| `0` **al día** | Las dos huellas cuadran con el canon | **Se dice en una línea y se termina.** Lo sano no se reporta largo |
| `1` **atrasado** | La copia es de un commit anterior, y el guion **lista qué entró desde él** | Se sigue con el paso 1 |
| `2` **no instalado** | No hay puente en esta máquina | Se dice y se manda a `/vuelamind-rc`. **No se instala aquí** |
| `3` **desconocido** | Su huella no está en la historia: **modificado localmente**, o de otra procedencia | **Se para.** Ver abajo |

**El caso `3` es la razón de que este skill mida así.** Un comparador ingenuo pregunta *«¿es
igual a la última?»*, y con un «no» junta dos cosas que no se parecen: **una copia vieja** y
**el trabajo de alguien**. Sobrescribir la segunda borra ese trabajo sin que nada falle.
Cuando salga, se enseña el `diff` que el propio guion imprime, y **decide una persona**: si el
cambio local vale, su camino es una propuesta al canon, no morir pisado.

> [!warning] Traer el canon fresco ANTES de medir, y no confundir el clon con el remoto
> El guion compara contra la referencia que se le dé (`--ref`, por omisión `origin/main`). Un
> clon que no se ha traído en semanas **responde con seguridad sobre un pasado**. Se trae
> primero, y si no hay red **se dice que la medición es contra lo que había**, en vez de
> presentarla como actual.

## 1. Respaldar, y respaldar de forma que se pueda volver

Antes de escribir, copiar los dos archivos con fecha en el nombre:

```
session_bridge.py   → session_bridge.py.bak-<AAAA-MM-DD>
session_bridge.html → session_bridge.html.bak-<AAAA-MM-DD>
```

**Revertir es entonces un intercambio de archivo**, y eso hay que decírselo a quien opera —
saber que la vuelta es barata es lo que le permite decir que sí.

## 2. Escribir y verificar por huella

Copiar desde el clon los archivos que salieron atrasados —**solo ésos**— y **comprobar la
huella del lado escrito antes de arrancar nada**. Si alguna no cuadra, se para ahí: escribir a
medias un servicio es peor que no tocarlo.

Volver a correr `rc_estado.py`: debe salir **al día**. *Esa es la comprobación, no el recuerdo
de haber copiado.*

## 3. Reiniciar SOLO si cambió el backend

| Qué cambió | Qué hace falta |
|---|---|
| Solo `session_bridge.html` | **Nada más que recargar el navegador.** El servicio sirve la página en cada petición |
| `session_bridge.py` | **Reiniciar el servicio** |

**Confundir esto es el modo de fallo caro de este skill**: si solo se recarga la página cuando
cambió el backend, el arreglo *parece* aplicado, la interfaz se ve nueva, y la conducta sigue
siendo la vieja — sin ningún síntoma hasta el día que importa. El propio `rc_estado.py` lo dice
en su salida; se obedece.

Cómo se reinicia depende de cómo se instaló, y se comprueba en vez de suponerse:

- **macOS** — LaunchAgent: `launchctl bootout gui/$(id -u)/com.vuelamind.rc` y luego
  `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.vuelamind.rc.plist`
- **Linux** — unidad de usuario: `systemctl --user restart <unidad>`
- **Suelto** (sin arranque automático): matar el proceso y volver a lanzarlo con el mismo
  intérprete y las mismas variables. **El puente exige Python 3.10 o superior** y falla en voz
  alta si no lo tiene: eso es correcto, no un defecto, y conviene comprobar con cuál corría.

## 4. Comprobar que quedó vivo, ejerciendo

No basta con que el comando de arranque no diera error:

```
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<puerto>/health     → 200
```

El puerto es el del `.env` de esa máquina, no uno supuesto. **Si no responde, revertir con el
respaldo** —intercambio de archivo— y decirlo. Un servicio que no arranca tras una
actualización se deja como estaba, no se deja «casi».

## 5. Reportar lo que de verdad pasó

- Qué versión corría y cuál corre ahora, **con sus huellas**.
- **Qué cambios entraron**, por sus títulos — quien opera merece saber qué le cambió debajo.
- Si hubo reinicio o no, **y por qué**.
- Y lo que no se pudo verificar, dicho como tal.

> [!note] Este skill es del canon, pero lo que actualiza es de la máquina
> El canon publica; **cada despliegue decide cuándo ponerse al día**. Este skill no se corre
> solo ni avisa por su cuenta: lo invoca quien opera ese puente, cuando quiere. Si algún día
> conviene que avise —como hace el arranque con la deriva de skills—, ése es otro cambio y
> tiene su propia decisión.
