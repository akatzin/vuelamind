---
description: Empaca el dominio entero en un zip con sus notas de migración, sin mover nada en el origen, para que otro ambiente sepa qué trae y lo normalice allá
---

# /vuelamind-export — el dominio en un zip, con sus notas de migración

Copia el dominio **tal cual está** a un zip y le agrega `MIGRACION.md`: qué trae, dónde quedó cada pieza y qué no viaja. **No mueve, no borra y no corrige nada en el origen.** Normalizar es trabajo del destino, con la palabra de la persona.

## Qué hace, en orden

### 1. Localizar el dominio

Lee `.claude/vuelamind-commit.manifiesto.md` en el directorio de trabajo. **Sin manifiesto, se detiene.**

Del manifiesto salen las rutas: `vault`, `validador`, las seis `notas:`, `acta`, `alma` y `marco` (el registro de parches). Una clave ausente se anota como hueco; no se adivina.

### 2. Hacer el mapa de piezas

La estructura de referencia es la del master: la topología de la Fase 1.0, los archivos de la 1.1 y lo que el mismo master pone dentro del vault (el acta, `ALMA.md`, el registro de parches, `borradores/0_Borradores.md`). **Se lee del master, no de este archivo.**

Para cada pieza, una fila: dónde está en el origen, dónde queda en el zip, o `no existe`.

Cada diferencia con la referencia se clasifica en uno de tres niveles:

| Nivel | Qué es | Ejemplo |
|---|---|---|
| **Viola una regla** | El master lo manda y el dominio no lo cumple | el acta fuera del vault (regla desde la v3.9) · borradores fuera del vault |
| **Declarado** | Fuera de la convención, pero permitido porque el manifiesto lo declara | el vault fuera del proyecto · un validador con otro nombre |
| **Desorden** | Ni regla ni declaración | respaldos manuales sueltos · instantáneas viejas |

En el destino, solo el primer nivel se corrige sin discusión. Los otros dos se respetan o se proponen.

### 3. Decidir qué entra

| Entra | Dónde, en el zip |
|---|---|
| La carpeta del proyecto, tal cual | `proyecto/` |
| El clon del canon del dominio, con su `.git`: es la versión del método que el dominio eligió, y volver a clonar trae otra | donde esté: dentro de `proyecto/`, o en `_fuera/canon/` |
| Lo que el manifiesto declara **fuera** del proyecto y es del dominio, como un vault externo | `_fuera/<clave>/` |
| La memoria de Claude Code, si no vive ya dentro del proyecto | `_memoria/` |
| Los respaldos manuales: `*.bak*`, `*.antes-*`, `*.viejo-*`, `*.orig` | en su sitio, y listados en la nota |

**La memoria** es la carpeta de `~/.claude/projects/` cuyo nombre es la ruta absoluta del proyecto con cada carácter que no sea letra o número cambiado por `-` (`~/0_AI/casa` → `-Users-<usuario>-0-AI-casa`). Si `memory/` del proyecto es la real y la de Claude Code es un enlace hacia ella, va una sola vez, dentro de `proyecto/`. Si no se encuentra, se dice: nunca se elige una por parecido.

| No entra | Qué se escribe en la nota |
|---|---|
| Las transcripciones de Claude Code (`*.jsonl`) | que se excluyeron |
| Credenciales: llaves, `.env`, `*.pem`, `*.key`, `*secret*`, y los archivos con permisos `600` o `400` que lo parezcan | **solo el nombre y la ruta**, para recrearlas en el destino. El contenido, nunca. Un archivo con `600` o `400` que no parezca secreto —una imagen, una nota— se le pregunta a la persona en el paso 6 |
| Cualquier otro clon público que no sea del dominio | de dónde se vuelve a clonar |
| `.git/worktrees/` de cualquier repositorio: son copias de trabajo de esta máquina | que se excluyeron; en el destino, `git worktree prune` |
| Cachés y basura de sistema: `__pycache__/`, `.stversions/`, `.trash/`, `.DS_Store`, las instantáneas del vault | que se excluyeron |

**Un enlace simbólico no se sigue**: se anota adónde apunta. Seguirlo mete en el zip algo que no es del dominio, o lo mismo dos veces.

**Una ruta del manifiesto que no existe en esta máquina, con la pieza en otra ruta de esta máquina, es un alias**: pasa en una réplica y en un dominio que vive en varias máquinas. Se empaca lo que existe, y la ruta declarada va en `alias` de su entrada de `fuera`. La raíz del proyecto con que la nombra otra máquina va en `raiz_alias`: es la ruta absoluta de una pieza que el manifiesto declara dentro del proyecto, menos la parte que coincide exacta con donde quedó aquí. Dónde está la pieza lo dicen la persona, la configuración de sincronización o esa coincidencia exacta; nunca se elige por parecido, y lo que no se sepa se pregunta en el paso 6.

### 4. Barrer las rutas absolutas

En cada archivo de texto que entra, buscar la ruta raíz del proyecto, la de cada pieza de `_fuera/`, cada `alias` y `raiz_alias`, `$HOME` expandido y `~/`. Cada hallazgo, con archivo, renglón y ruta.

**La nota declara el patrón con que se buscó**, para que una lista vacía signifique «no hay» y no «no se buscó». Lo encontrado se **declara**, no se reescribe: reescribir es del destino.

### 5. Inventariar lo que no viaja

Lo que apunta a las rutas del dominio desde fuera, buscado **solo con patrones anclados a esas rutas**, nunca recorriendo el home:

- **Tareas programadas:** `~/Library/LaunchAgents/*.plist` en macOS; `~/.config/systemd/user/` y `crontab -l` en Linux.
- **Sincronización:** la configuración de Syncthing, si existe (macOS: `~/Library/Application Support/Syncthing/config.xml`; Linux: `~/.local/state/syncthing/` o `~/.config/syncthing/`), y qué carpetas suyas tocan el dominio.
- **Respaldos y réplicas:** los que declare el manifiesto.
- **Procesos** que corren desde el proyecto, **incluidas las sesiones de Claude Code** abiertas en él. Si alguna está abierta, el plan del paso 6 lo dice: un archivo que se escribe mientras se empaca entra a medias.

Cada uno, con la ruta que usa. Lo que no se pudo comprobar se dice con esas palabras.

### 6. Enseñar antes de empacar

Presentar a la persona el mapa de piezas, cada alias con de dónde salió, el tamaño de lo que entra (cada carpeta de más de 100 MB, por separado), lo excluido y dónde se va a escribir el zip.

**Dónde:** la carpeta que se pase como argumento (`/vuelamind-export <carpeta>`); sin argumento, la carpeta padre del proyecto, porque dentro de él se empacaría a sí mismo.

Se empaca solo con su sí.

### 7. Escribir y empacar

- `MIGRACION.md`, en la raíz del zip, con el formato de abajo.
- `RUTAS.tsv`: una fila por ruta absoluta encontrada en el paso 4, con tres columnas separadas por tabulador: archivo dentro del zip, renglón y **la ruta completa como aparece en el renglón**, desde donde empieza la coincidencia hasta el primer espacio, comilla, acento grave o cierre de paréntesis o corchete. No basta el pedazo que coincidió: `~/` a secas no dice si la ruta es del dominio o de otra parte.
- `HUELLAS.txt`: el `sha256` de cada archivo del zip, salvo él mismo, con su ruta dentro del zip.
- El zip: `<dominio>-<AAAA-MM-DD>T<HHMM>Z.zip`, con la hora en UTC para que dos exportaciones del mismo día no choquen. Se escribe **en la carpeta de destino y con el nombre temporal `<nombre>.zip.parcial`**: quien lo lea mientras se escribe vería un zip roto.
- **Cada nombre que no sea ASCII va marcado como UTF-8** (el bit 11 de su entrada); sin la marca, el destino lee «Topología» como «Topologi╠üa». `zip` y `ditto` de macOS no la ponen (MEDIDO el 2026-10-21); `bsdtar --format zip --options zip:hdrcharset=UTF-8` y el `zipfile` de Python, sí.

### 8. Verificar en el zip, no en el origen

- `unzip -t` sin errores.
- Toda entrada con un nombre que no sea ASCII tiene la marca UTF-8.
- **Por nombre, no por conteo:** los nombres del zip, en NFC, son exactamente los de `HUELLAS.txt` más él mismo. Un conteo cuadra aunque los nombres lleguen cambiados.
- Cada archivo de la primera columna de `RUTAS.tsv` está en el zip.
- Solo con todo en verde se renombra `<nombre>.zip.parcial` a `<nombre>.zip`, con `mv` en la misma carpeta, que es un solo paso. Si alguna falla, se borra el `.parcial` y se reporta `NO EXPORTADO`.
- Reportar la ruta y el tamaño del zip, cuántos archivos lleva, qué se excluyó y lo que no se pudo verificar.
- **La última línea del reporte es exactamente `EXPORTADO: <ruta absoluta del zip>`**, para que un programa que invoque el skill recoja el zip sin adivinar. Si no se exportó, la última línea es `NO EXPORTADO: <motivo>`.

Un zip escrito no es un zip que se puede abrir: se comprueba lo segundo.

## El formato de `MIGRACION.md`

Dos partes: un **frontmatter YAML para máquina** y un cuerpo para la persona. **Un importador lee solo el frontmatter y los archivos que nombra**; el cuerpo explica lo mismo, en prosa.

La primera clave es `formato`. Un importador que reciba un formato más nuevo del que entiende se detiene.

```yaml
---
formato: 1
dominio: <nombre>
exportado_utc: <AAAA-MM-DDTHH:MM:SSZ>
host: <host de origen>
version_marco: <versión del master del dominio>
raiz_original: <ruta absoluta del proyecto en el origen>
raiz_alias: [<ruta>, ...]      # la raíz con que la nombran otras máquinas; [] si no hay
piezas:                        # pieza estándar → ruta dentro del zip | no-existe
  manifiesto: proyecto/.claude/vuelamind-commit.manifiesto.md
  vault: <ruta>
  panorama: <ruta>             # las seis notas, con las claves del manifiesto
  cola: <ruta>
  archivo: <ruta>
  decisiones: <ruta>
  bitacora: <ruta>
  arranque: <ruta>
  acta: <ruta>
  alma: <ruta>
  registro_parches: <ruta>
  borradores_indice: <ruta>
  validador: <ruta>
  init: [<ruta>, ...]
  memoria: <ruta>
fuera:                         # ruta dentro del zip → ruta original
  - {zip: _fuera/<clave>/, origen: <ruta absoluta>, alias: [<ruta>, ...]}
memoria_origen: <ruta absoluta de la memoria en el origen>
canon: {zip: <ruta del clon dentro del zip> | no-existe, ref: <commit en que está>, remoto: <url de origin>}
desviaciones:
  - {nivel: regla | declarado | desorden, pieza: <pieza o ruta>, detalle: <una línea>}
rutas: {archivo: RUTAS.tsv, patron: <expresión con que se buscó>}
no_viaja:
  - {tipo: launchd | systemd | cron | syncthing | replica | proceso, ref: <nombre o archivo>, ruta: <ruta que usa>}
excluido:
  credenciales: [<ruta original>, ...]   # solo el nombre: el contenido nunca
  otros: [<patrón o ruta>, ...]
respaldos_manuales: [<ruta dentro del zip>, ...]
se_ejecuta: [<ruta dentro del zip>, ...]  # todo archivo bajo cualquier .claude/ menos el manifiesto, y .mcp.json
huellas: HUELLAS.txt
no_verificado: [<una línea por cosa>, ...]
---
```

**El frontmatter tiene que ser YAML válido**, y se comprueba cargándolo antes de empacar. Un valor con `: ` dentro, como una URL, va entre comillas dobles; el patrón de rutas, entre comillas simples, porque sus barras invertidas no son escapes de YAML.

Toda ruta de `piezas`, `respaldos_manuales` y `se_ejecuta` es relativa a la raíz del zip. **Lo de `se_ejecuta` el destino lo revisa antes de activarlo**: importar un dominio es ejecutar lo que otro escribió.

**`se_ejecuta` lista todo archivo bajo cualquier `.claude/` del zip**, a cualquier profundidad y con cualquier nombre —respaldos, `skills/` y subcarpetas incluidos—, **excepto el manifiesto, y además `proyecto/.mcp.json`** si existe. Declarar de más no rompe nada; dejar uno fuera, sí.

Los nombres de archivo se comparan en NFC, en el zip, en `HUELLAS.txt`, en `RUTAS.tsv` y en el frontmatter: macOS puede guardarlos en NFD.

El exportador escribe siempre `raiz_alias` y el `alias` de cada entrada de `fuera`, con `[]` si no hay. Siguen en el `formato: 1`: una clave ausente es de un paquete anterior y el importador puede deducirla; una presente manda sobre lo que deduzca, clave por clave.

## Qué NO hace

- **No toca el origen.** Ni mueve, ni borra, ni corrige.
- **No cifra.** El zip lleva el dominio entero: se trata como secreto.
- **No sube el zip a ningún lado.**
- **No corre los enganches del manifiesto** ni los ganchos del proyecto.
- **No importa.** Leer `MIGRACION.md` y normalizar es del destino.
