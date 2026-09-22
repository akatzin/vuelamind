# Qué está medido de este contenedor, y en qué máquina

Esto no es documentación del contenedor: son **las condiciones medidas** y, sobre todo,
**las que no lo están**. Si viajan sueltas del código, quien lo lea no las tiene — y lo que
más cuesta reconstruir después no es lo que funcionó, es qué nadie llegó a comprobar.

Cada fila dice **quién** midió. La casa que escribe el código y la que tiene la máquina no
son la misma, y esa separación es a propósito: en esta familia de dominios, **ninguna casa
encontró su propio error** en ocho días de vigilarse con lupa.

## macOS · Docker Desktop 4.83, motor 29.6.2, arm64

| Qué | Estado |
|---|---|
| Arranque, salud por el relevo, página servida | **MEDIDO** |
| Candados del puente a través del relevo: `Host` ajeno y `Origin` ajeno → 403 | **MEDIDO** |
| El puerto no responde desde la IP de LAN; `lsof` confirma solo loopback | **MEDIDO** |
| Si muere el puente, el contenedor muere con él (código 143) | **MEDIDO** |
| `node:22-slim` no trae `python3`; bookworm da 3.11 | **MEDIDO** |
| gcloud cuesta 870 MB (1.19 GB → 2.06 GB) | **MEDIDO** |
| Login de aplicación sin navegador: llega a pedir el código (SDK 585.0.0) | **MEDIDO** |
| Normalización de CRLF: imagen construida desde fuentes con CRLF a propósito | **MEDIDO** |
| `/login` interactivo completo | **SIN MEDIR** — no había credencial propia que gastar |

## Linux · Debian, Docker Engine 29.5.2, Compose v5.1.4

Medido por la casa que tiene la máquina, sobre el commit exacto de esta rama.

| Qué | Estado |
|---|---|
| Arranque y salud | **MEDIDO** |
| **La guardia de escritura salta en el PRIMER arranque de un clon nuevo** | **MEDIDO** — Docker crea `./trabajo` como `root`; el contenedor sale con 1 y no a media entrevista |
| El camino recomendado sin `sudo` (`mkdir -p trabajo && docker compose up -d`) | **MEDIDO** — ejercido tal cual, arranca |
| Puerto cerrado a la LAN, comprobado desde **dos** máquinas distintas | **MEDIDO** |
| `down -v` deja cero contenedores, cero volúmenes y el puerto libre | **MEDIDO** por separado, no por la salida del `down` |
| El camino con `sudo chown` — el que este repositorio documenta como segunda vía | **SIN MEDIR** — quien midió no tenía `sudo` sin contraseña |
| Normalización de CRLF | **SIN MEDIR aquí, y no aplica**: un clon en Linux trae LF |

## Windows 11 Pro (build 26200) · VM con virtualización anidada

Medido dentro de la máquina por la casa que la opera. El entorno se montó entero:
WSL2 2.7.14.0, Docker Desktop con backend `wsl-2`, git 2.55.0.

| Qué | Estado |
|---|---|
| `HypervisorPresent = True` dentro de la VM | **MEDIDO** |
| **El escenario de CRLF existe y es el camino normal** | **MEDIDO** — ver abajo |
| **El blindaje de CRLF, ejercido de punta a punta en Windows** | **SIN EJERCER** — el build no completó |
| El contenedor entero en Windows | **SIN MEDIR** |

### El escenario de CRLF: reproducido, y no hay que hacer nada raro

Clonando esta rama **en Windows** con git recién instalado y **opciones por omisión**, los
cuatro `.sh` que el `Dockerfile` copia llegan convertidos:

```
actualizar.sh   41 CRLF      puente.sh     118 CRLF
bienvenida.sh   60 CRLF      vertex.sh      61 CRLF
```

La causa es que **git para Windows trae `core.autocrlf = true` de fábrica**. Nadie tiene que
configurar nada mal: el camino de fábrica produce exactamente los archivos que dentro de una
imagen Linux fallan con «bad interpreter», un error que no menciona ni a Windows ni a los
saltos de línea.

**Eso valida la necesidad del `sed`, no su efecto.** El efecto está medido **en macOS**,
construyendo la imagen desde fuentes convertidos a CRLF a propósito. Lo que falta es la
cadena completa —clonar en Windows y construir en Windows—, y **no se pudo cerrar porque el
motor no se sostiene en esa VM**: tres intentos, tres modos de fallar, ninguno atribuible a
este contenedor.

```
vpnkit-bridge: /run/guest-services/socketforwarder-receive-fds.sock: does not exist
com.docker.backend.ipc [W] GET /ping: context deadline exceeded
```

Es WSL2 anidado dentro de KVM, no la imagen. **Declararlo «blindado en Windows» hoy sería un
verde inventado.**

### Tres cosas que muerden al probar esto en Windows por SSH

No son de este contenedor, pero quien lo pruebe en un banco sin pantalla se las encuentra:

1. **Docker Desktop muere con la sesión SSH que lo lanzó.** Vive en la sesión del usuario, no
   como servicio: hay que arrancarlo y usarlo sin soltar esa misma sesión.
2. **El almacén de credenciales no existe en sesión SSH** — `error getting credentials - A
   specified logon session does not exist`. Se rodea quitando `credsStore` de
   `%USERPROFILE%\.docker\config.json`.
3. **Sin sesión de escritorio no arranca**: Docker Desktop necesita una sesión iniciada, así
   que en una VM headless hace falta autologon.

## En ninguna plataforma fuera de macOS

**La página web entera sigue sin medirse**: la entrevista, el botón de nacer un dominio y la
validación de `Origin` desde un navegador real. Fuera de macOS solo se ha tocado `/health`
por `curl`.
