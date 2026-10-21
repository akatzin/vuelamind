---
description: Empaca el dominio entero en un zip con sus notas de migración, sin mover nada en el origen, para que otro ambiente sepa qué trae y lo normalice allá
---

# /vuelamind-export — el dominio en un zip, con sus notas de migración

Copia el dominio **tal cual está** a un zip y le agrega `MIGRACION.md`: qué trae, dónde quedó cada pieza y qué no viaja. **No mueve, no borra y no corrige nada en el origen.** Normalizar es trabajo del destino, con la palabra de la persona.

## Qué hace, en orden

### 1. Localizar el dominio

Lee `.claude/vuelamind-commit.manifiesto.md` en el directorio de trabajo. **Sin manifiesto, se detiene**: empacar el dominio equivocado es peor que no empacar.

Del manifiesto salen las rutas: `vault`, `validador`, las seis `notas:`, `acta`, `alma` y `marco` (el registro de parches). Una clave ausente se anota como hueco; no se adivina.

### 2. Hacer el mapa de piezas

La estructura de referencia es la del master: la topología de la Fase 1.0, los archivos de la 1.1 y lo que el mismo master pone dentro del vault (el acta, `ALMA.md`, el registro de parches, `borradores/0_Borradores.md`). **Se lee del master, no de este archivo**: una lista copiada aquí envejece.

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
| Lo que el manifiesto declara **fuera** del proyecto y es del dominio, como un vault externo | `_fuera/<clave>/` |
| La memoria de Claude Code, si no vive ya dentro del proyecto | `_memoria/` |
| Los respaldos manuales: `*.bak*`, `*.antes-*`, `*.viejo-*`, `*.orig` | en su sitio, y listados en la nota |

**La memoria** es la carpeta de `~/.claude/projects/` cuyo nombre es la ruta absoluta del proyecto con cada carácter que no sea letra o número cambiado por `-` (`~/0_AI/casa` → `-Users-<usuario>-0-AI-casa`). Si `memory/` del proyecto es la real y la de Claude Code es un enlace hacia ella, va una sola vez, dentro de `proyecto/`. Si no se encuentra, se dice: nunca se elige una por parecido.

| No entra | Qué se escribe en la nota |
|---|---|
| Las transcripciones de Claude Code (`*.jsonl`) | que se excluyeron |
| Credenciales: archivos con permisos `600` o `400`, llaves, `.env`, `*.pem`, `*.key` | **solo el nombre y la ruta**, para recrearlas en el destino. El contenido, nunca |
| El clon del canon y cualquier otro clon público | de dónde se vuelve a clonar |
| Cachés y basura de sistema: `__pycache__/`, `.stversions/`, `.trash/`, `.DS_Store`, las instantáneas del vault | que se excluyeron |

**Un enlace simbólico no se sigue**: se anota adónde apunta. Seguirlo mete en el zip algo que no es del dominio, o lo mismo dos veces.

### 4. Barrer las rutas absolutas

En cada archivo de texto que entra, buscar la ruta raíz del proyecto, la de cada pieza de `_fuera/`, `$HOME` expandido y `~/`. Cada hallazgo, con archivo, renglón y ruta.

**La nota declara el patrón con que se buscó**, para que una lista vacía signifique «no hay» y no «no se buscó». Lo encontrado se **declara**, no se reescribe: reescribir es del destino.

### 5. Inventariar lo que no viaja

Lo que apunta a las rutas del dominio desde fuera, buscado **solo con patrones anclados a esas rutas**, nunca recorriendo el home:

- **Tareas programadas:** `~/Library/LaunchAgents/*.plist` en macOS; `~/.config/systemd/user/` y `crontab -l` en Linux.
- **Sincronización:** la configuración de Syncthing, si existe (macOS: `~/Library/Application Support/Syncthing/config.xml`; Linux: `~/.local/state/syncthing/` o `~/.config/syncthing/`), y qué carpetas suyas tocan el dominio.
- **Respaldos y réplicas:** los que declare el manifiesto.
- **Procesos** que corren desde el proyecto.

Cada uno, con la ruta que usa. Lo que no se pudo comprobar se dice con esas palabras.

### 6. Enseñar antes de empacar

Presentar a la persona el mapa de piezas, el tamaño de lo que entra (cada carpeta de más de 100 MB, por separado), lo excluido y dónde se va a escribir el zip. **Por omisión, en la carpeta padre del proyecto**: dentro de él se empacaría a sí mismo.

Se empaca solo con su sí.

### 7. Escribir y empacar

- `MIGRACION.md`, en la raíz del zip, con el formato de abajo.
- `HUELLAS.txt`: el `sha256` de cada archivo del zip, salvo él mismo, con su ruta dentro del zip.
- El zip: `<dominio>-<AAAA-MM-DD>.zip`, hecho con las herramientas del sistema (`zip`, o `ditto` en macOS).

### 8. Verificar en el zip, no en el origen

- `unzip -t` sin errores.
- El zip tiene exactamente un archivo más que las filas de `HUELLAS.txt`.
- Reportar la ruta y el tamaño del zip, cuántos archivos lleva, qué se excluyó y lo que no se pudo verificar.

Un zip escrito no es un zip que se puede abrir: se comprueba lo segundo.

## El formato de `MIGRACION.md`

La primera línea es `formato: 1`. Un importador que reciba un formato más nuevo del que entiende se detiene.

1. **Origen:** dominio, fecha en UTC, host, versión del marco, ruta raíz original y ruta original de cada pieza de `_fuera/` y de `_memoria/`.
2. **Mapa de piezas:** la tabla del paso 2.
3. **Desviaciones:** agrupadas por nivel.
4. **Rutas absolutas:** el patrón de búsqueda y la lista.
5. **Lo que no viaja:** el inventario del paso 5.
6. **Lo excluido:** el paso 3, con las credenciales solo por nombre.
7. **Respaldos manuales:** la lista.
8. **Configuración que se ejecuta:** los ganchos de `.claude/settings*.json` y los comandos del proyecto, por nombre. **El destino los revisa antes de activarlos**: importar un dominio es ejecutar lo que otro escribió.

## Qué NO hace

- **No toca el origen.** Ni mueve, ni borra, ni corrige.
- **No cifra.** El zip lleva el dominio entero: se trata como secreto.
- **No sube el zip a ningún lado.**
- **No corre los enganches del manifiesto** ni los ganchos del proyecto.
- **No importa.** Leer `MIGRACION.md` y normalizar es del destino.
