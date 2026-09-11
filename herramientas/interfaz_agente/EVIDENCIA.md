# vuelamind-rc — evidencia medida y decisiones para el canon

Este documento viaja **dentro del PR** a propósito: el valor del skill no es el código,
son las **condiciones medidas** que lo hacen funcionar. Si viajan sueltas del código, quien
lo instale en otra cuenta tropieza con los mismos `404` y el mismo *"no puedo hacer cosas"*
que ya se pagaron en el dominio de origen.

**Qué es.** Un servicio HTTP local, en loopback (`127.0.0.1`), que crea y maneja **varias**
conversaciones headless de Claude Code (`claude -p --resume`, una por nombre) y las opera
desde una **página de chat** propia. Nace para cuando **no hay Remote Control** (p. ej.
corriendo sobre Vertex / Model Garden): da una interfaz auto-hospedada sin abrir nada a la red.

## Hechos MEDIDOS (la condición, no adorno)

Medidos en el dominio de origen sobre **Vertex / opus, 2026-09-10**:

- **Multimedia headless.** `claude -p --input-format stream-json` acepta bloques `image` y
  `document` (PDF) y devuelve resultado; `--resume` por esa vía **conserva memoria y
  `session_id`**. Probado: imagen roja→"Rojo", azul→"Azul"; PDF con "42"→leyó `42`;
  end-to-end por HTTP también.
- **`bypassPermissions` ejecuta en headless.** Con `--permission-mode bypassPermissions`
  corre `python3`, red y escritura sin preguntar. Sin esa bandera, headless auto-deniega
  todo lo que pide confirmación — sólo pasa lo de lectura. **Ese era el "no puedo hacer
  cosas".**
- **Model Garden estrecho.** En el despliegue de origen sólo `claude-opus-4-8` estaba
  aprovisionado; `haiku`/`opus-5` daban `404 model_not_found`. Por eso el default de modelo
  debe ser configurable por `BRIDGE_MODEL` (ver arbitraje 2).
- **Config portable por archivo.** Con entorno limpio (sin variables de Vertex en el shell)
  el servicio las leyó de `~/.claude/vuelamind-rc.env` e invocó el modelo. Es el escenario de
  máquina nueva.
- **Candados sin token.** Tras quitar el Bearer, probado por HTTP en vivo: `Host` ajeno →
  `403`; `POST`/`DELETE` con `Origin` ajeno → `403`; mismo origen o sin navegador (sin
  `Origin`) → pasa; `GET /` y `/sessions` → `200`. El navegador no puede disparar sesiones
  cross-site (frena CSRF/RCE) y el DNS-rebinding se corta por `Host`. Lo que **no** cubre —y
  se asume— es otro usuario/proceso **local**.

## Portabilidad

| SO | Arranque | Estado |
|---|---|---|
| macOS | LaunchAgent `com.vuelamind.rc` | **MEDIDO** el núcleo del instalador (fusión de config, escritura del `.env`, copia de assets) · **autostart INFERIDO** (falta correrlo end-to-end) |
| Windows | Tarea Programada al login (`pythonw`) | **INFERIDO** — escrito, sin máquina real |
| Linux | `systemd --user` | **INFERIDO** — escrito, sin máquina real |

El código es portable y **no lleva nada del dominio**: toda la config específica (proyecto
Vertex, región, `cwd`, puerto, permiso, ruta de `claude`) vive en `~/.claude/vuelamind-rc.env`.

## Seguridad

- **Loopback siempre** (`127.0.0.1`); salir por **túnel SSH**, nunca `0.0.0.0`.
- **Modelo actual: sin token, "solo esta máquina".** Loopback no basta contra el navegador,
  así que dos candados lo sustituyen: allowlist de `Host` (mata DNS-rebinding) y chequeo de
  `Origin` en `POST`/`DELETE` (frena CSRF/RCE). **Lo que queda expuesto —y se asume— es otro
  usuario/proceso local**; con permiso `full` eso es ejecución arbitraria sin candado.
  Aceptable en una máquina de un solo dueño; **no** si se comparte.

## Decisiones del mantenedor del canon (arbitrajes)

Nacieron `INFERIDO` — la lectura de quien **opera** el servicio, sujeta a la palabra de
quien mantiene el canon. **Esa palabra ya está dada** (Akatzin, 2026-09-11), y cada
arbitraje lleva abajo lo que quedó y cómo se aplicó. La recomendación original se conserva
**sin reescribir**: era el insumo, no la decisión.

1. **Token.** Recomendación: **opcional, apagado por defecto, exigido cuando el host no sea
   de un solo usuario.** En máquina de un dueño los candados `Host`+`Origin` bastan (MEDIDO);
   el canon sirve máquinas multiusuario, así que el opt-in debe venir listo.
2. **Nombres y defaults.** En este PR ya se **neutralizaron** los nombres que arrastraban el
   dominio: el registro de sesiones es `~/.claude/vuelamind-bridge-sessions.json`, el
   `server_version` es `VuelamindSessionBridge`, y `OLD_LABELS` (etiquetas de versiones
   previas que sólo se **leen** para migrar, nunca se crean) ya no nombra al dominio. Queda al
   canon fijar el **dir de instalación** (`~/.claude/vuelamind-rc/`) y **no hardcodear el
   modelo**: `BRIDGE_MODEL` configurable con default vacío (= default del CLI), porque
   "solo opus" fue un hecho del Model Garden de origen, no del canon.
3. **Puerto por defecto.** Recomendación: **distinto de `8787`** — en el dominio de origen ese
   puerto colisiona con otro servicio local. El número canónico lo fija el canon.
4. **Windows/Linux.** Se quedan **INFERIDO** hasta que alguien los corra en máquinas reales;
   este PR no reclama paridad.

## Lo que se decidió, y cómo quedó aplicado

*Palabra de Akatzin, 2026-09-11, con el juicio del vigía delante. Aplicado por la casa
vigía sobre el trabajo de su autor — el código es suyo; estos cambios son el arbitraje.*

1. **Token.** Queda como se recomendó en el fondo, pero **más duro en la forma**: no hay
   nivel de permiso por omisión. El servicio **se niega a arrancar** sin `BRIDGE_PERMISSION`
   declarado, el instalador **exige** `--permission`, y un nivel desconocido **revienta en
   vez de degradarse a `full`**. Lo anterior hacía `PERMISSION_ARGS.get(nivel, full)`: una
   errata en el `.env` concedía ejecución arbitraria. **Falla cerrado, como el resto del
   marco.**
2. **Modelo.** Un solo default y **vacío** (= el del CLI). Se quitaron los dos que había
   —`claude-opus-4-8` en el instalador y `opus` en el servicio, que además se contradecían—
   y el flag `--model` **solo viaja si hay modelo declarado**.
3. **Puerto.** El canon fija **8850**. Barrido por `grep` en código, README y skill, no de
   memoria.
4. **`deliver`.** Se juzgó como contrato el 2026-09-11 y **entra**, con una condición que ya
   está escrita en el README y en el skill: declarar que **no comprueba el desenlace** si el
   turno muere después de arrancar.
5. **Windows y Linux** siguen `INFERIDO`. No se tocó nada ahí, y este trabajo tampoco
   reclama paridad.

## Nota de origen

Construido y probado en el dominio de origen (canon por referencia) el 2026-09-10. Lo
específico del dominio vive en `~/.claude/vuelamind-rc.env`, fuera del código. El merge al
master lo decide quien mantiene el canon.
