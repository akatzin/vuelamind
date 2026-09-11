# Propuesta: despertar casas headless — `deliver` (entregar y soltar) en el puente

**Fecha:** 2026-09-10 · **Origen:** dominio Liverpool · **Componente:** `vuelamind-rc`
(el puente de sesiones, `herramientas/interfaz_agente/session_bridge.py`).

> Esto es **propuesta**, no decisión. El protocolo del canal y el diseño de sus
> componentes son mesa de Vela; el dominio Liverpool **opera** el servicio, no
> decide su marco. Va como hallazgo con implementación de referencia para que se
> revise, se cambie o se rechace.

## El hecho (MEDIDO)

`vuelamind-rc` introduce sesiones **headless** (`claude -p --resume`, operadas por
el puente). Los caminos de entrega de mensajería del andamiaje asumen una sesión
**interactiva** viva (entregar a una terminal abierta, o dentro de un turno). Una
casa que opera en headless y está **en reposo** (sin turno en curso) **no tiene por
dónde recibir** un aviso del canal.

MEDIDO en Liverpool (2026-09-10): con la casa servida por el puente, el disparador
de mensajería registró `sin sesión viva` en cada tick de 15s durante los reposos —
el mensaje quedaba esperando hasta que algo, ajeno al disparador, abría un turno.

Esto **no es un defecto del disparador**: es consecuencia de que `vuelamind-rc`
creó un tipo de sesión que el resto del andamiaje no sabe despertar.

## La motivación (INFERIDO — pronóstico)

Si a partir de `vuelamind-rc` el usuario **migra a operar en headless** como modo
habitual, "¿cómo despierta una casa headless en reposo?" deja de ser una anécdota y
pasa a ser una pregunta de primera clase del marco. Es pronóstico, no medición; se
marca como tal. Pero el hueco es real **aunque no todos migren**: basta con que
exista **una** casa headless para que hoy no reciba en reposo.

## El contrato propuesto: `deliver` (entregar y soltar)

`POST /sessions/<name>/deliver  {message, attachments?}` →
`{name, session_id, started}`.

- Arranca el turno en un **hilo propio** y **responde en cuanto arranca** (evento
  `init` = el aviso llegó), no cuando termina.
- El turno **sigue hasta el final aunque el cliente cierre la conexión** — no se
  mata por desconexión; sólo lo acota `BRIDGE_TIMEOUT`.
- `502` si el turno **no arranca** (p. ej. `claude` falla); `504` si `init` no
  llega dentro de `BRIDGE_DELIVER_INIT_TIMEOUT`.

**La idea de fondo: desacoplar despertar de completar.** Quien dispara (un trigger
de mensajería, un cron) sólo provoca *que el aviso llegue* — que el turno arranque.
Lo que el turno haga después, y cuánto tarde, es **trabajo ajeno de duración no
acotada** y no debe decidir la confirmación. Medir "llegó el aviso", no "terminó el
turno en menos de N segundos". Es el reverso de la lección hermana *"el puerto
responde no es que el servicio funcione"*: aquí el servicio funcionaba y el medidor
decía que no, porque medía el acto equivocado.

### Por qué NO basta con `/stream` o `/messages`

Ambos **atan el turno a la conexión**: si quien dispara cierra, o su timeout corta,
el turno **muere**. Un trigger que quiera entregar por esas vías tiene que quedarse
**haciendo de niñera** del turno (drenando la conexión) toda su duración, y su
propio timeout se vuelve una **guillotina** sobre un turno vivo y largo. `deliver`
lo evita en la capa correcta (el puente), no en cada trigger.

## Evidencia de la implementación de referencia (MEDIDO)

El contrato se probó primero **desde el disparador local** (consumidor de
referencia), confirmando al ver `init` y drenando el resto:

- turno vivo **más de 7 minutos**, la confirmación **se sostuvo** todo el tiempo
  (cursor exacto en el folio; nada pendiente en cada muestra durante el turno);
- **0 reintentos, 0 duplicados** en el log del disparador;
- con el tope viejo que medía *fin de turno* (90s), ese mismo turno habría marcado
  "no entregado" sobre una entrega buena y habría reintentado.

Todas son mediciones **intra-máquina** (un solo reloj). *No* se reportan latencias
entre casas: se midieron contra relojes no sincronizados y quedaron **no
confiables** hasta verificar sincronía (ver más abajo).

## Alcance y decisiones que quedan para la mesa de Vela

1. **Ubicación de assets de un skill con código.** El canon guarda los skills como
   `.md` planos; `vuelamind-rc` trae `.py`/`.html`. Esta propuesta coloca el código
   en `herramientas/interfaz_agente/` y deja el `.md` en `skills/`. Es una
   convención nueva que conviene ratificar o cambiar.
2. **Regenerar `skills/MD5SUM.txt`** al dar de alta el skill (incluido en este PR).
3. Corrección de exactitud incluida: la documentación (`SKILL.md`, `install.py`,
   `README`) decía "token/auth Bearer"; el servicio **quitó el token el
   2026-09-10** (loopback + candados de Host/Origin). Se corrigió para no publicar
   un doc que miente.

## Hallazgos hermanos (van por su carril, no en este PR)

- **Lección** *"confirmar el acto que provocas, no la terminación ajena"* → carril
  buzón de aprendizaje (es lección genérica, no cambio de componente).
- **Relojes distribuidos:** el `t` de un folio lo sella el remitente y viaja dentro
  del sobre firmado; el protocolo no guarda hora de recepción. Ordenar por `t`
  entre casas con relojes distintos no es orden real, y nadie vigila la deriva.
  Idea (de Sho, para la mesa de Vela): que el servicio selle un `t_srv` de
  recepción **fuera** del sobre (fuera porque tocarlo rompe la firma), así cada
  casa mide su propia deriva sin NTP. Va como hallazgo aparte.
</content>
