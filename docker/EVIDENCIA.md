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

Medido dentro de la máquina por la casa que la opera.

| Qué | Estado |
|---|---|
| `HypervisorPresent = True` dentro de la VM | **MEDIDO** — la anidada llega; el camino existe |
| Docker Desktop instalado | **NO lo está** (`Get-Command docker` vacío) |
| WSL y VirtualMachinePlatform | **Disabled** las dos |
| **El contenedor entero en Windows** | **SIN MEDIR** |
| La normalización de CRLF en su escenario real (clonar *en* Windows) | **SIN MEDIR** — atada a lo mismo |

**Por qué sin medir, y no es una excusa:** sin WSL2 no hay Docker Desktop, sin las dos
características no hay WSL2, y habilitarlas es DISM más reinicio. Sumado a ~500 MB de
descarga y 5-6 GB en disco, **eso convierte una VM que nació «para medir, no para quedarse»
en otra cosa** — y eso lo decide su dueño, no quien quiere el dato.

El día que se desbloquee, el camino está despejado: no hay que pelearse con la
virtualización, solo instalar.

## En ninguna plataforma fuera de macOS

**La página web entera sigue sin medirse**: la entrevista, el botón de nacer un dominio y la
validación de `Origin` desde un navegador real. Fuera de macOS solo se ha tocado `/health`
por `curl`.
