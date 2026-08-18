---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-17 (lección 56 del libro heredado)
---

# 2026-08-16 · La tubería absuelve al comando ausente

## Qué corrige

Un instrumento del método comprueba algo y encadena el resultado: `comando ... | head`,
`... | grep`, `... | cut`. El código de salida que se lee es el del ÚLTIMO eslabón, y el
último eslabón casi siempre tiene éxito: `head` de una entrada vacía sale 0, `cut` de
nada sale 0.

Resultado: el comando principal puede no existir siquiera —command not found— y la
comprobación reporta exit 0. Verde sobre nada.

Esto ya está cubierto a medias por la lección de que lo que mide tiene dos salidas y las
dos mienten sin ponerse rojas. Lo que falta es el CASO CONCRETO y su remedio mecánico,
porque la forma es tan común que no se ve: encadenar es el gesto natural de quien
escribe un chequeo.

## Cómo se descubrió

MEDIDO 2026-08-16, en la primera medición de un salto v3 entre máquinas. Se corrió:

    timeout 30 git ls-remote https://… | head -5; echo "--- exit: $? ---"

`timeout` NO EXISTE EN macOS. La salida fue `command not found` y exit 0, porque el
código era el de `head`. La comprobación —"¿el canon remoto responde?"— quedó sin
contestar y con cara de contestada.

Se cazó por casualidad: el mensaje de error era visible. Si el comando ausente hubiera
fallado en silencio, la corrida entera se habría apoyado en un verde falso.

## Qué añade

Al escribir cualquier instrumento del método:

1. `set -o pipefail` cuando el guion pueda usarlo — hace que el código de salida sea el
   del primer eslabón que falla, que es la pregunta que de verdad se está haciendo.
2. `command -v <cmd>` antes de encadenar, para toda herramienta que no sea del núcleo
   POSIX. `timeout`, `gtimeout`, `sha256sum`, `md5sum`, `realpath`, `sed -i` sin sufijo:
   existen en Linux y no en macOS, o al revés. Un método que corre en varias máquinas no
   puede asumir ninguna.
3. Separar la captura de la presentación: guardar salida y código ANTES de pasar nada por
   una tubería —`cmd > out 2> err; rc=$?`— y sólo después formatear.

## Señal de que falta

Busca en los instrumentos del dominio cualquier `$?` leído después de una tubería. Cada
uno es un verde potencial sobre nada. Y busca herramientas no-POSIX invocadas sin
comprobar que existen: en una máquina nueva, ésas son las primeras en no estar.
