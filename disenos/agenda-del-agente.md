# La agenda del agente: turnos programados

**Estado: idea, sin construir. Nace de una pregunta de Akatzin el 2026-09-28.**

## Qué es

Que un agente pueda tener **turnos programados**: un texto que se le manda solo, cuando toca,
sin que haya nadie delante. El texto puede ser un skill (`/vuelamind-commit`) o prosa; son lo
mismo, y por eso la pieza es una sola.

```
entrada = { cuándo · a qué sesión · qué texto · hasta cuándo · con qué techo }
```

## No es inventar: es mudar un reloj que ya existe

En la máquina del vigía ya corren **dos disparadores** como LaunchAgents del sistema
(`ai.vuelamind.disparador.*`), despertando a otras casas. MEDIDO el 2026-09-28 con
`launchctl list`. O sea que el patrón está probado; lo que no existe es que el reloj **viva
dentro del agente** y viaje con él.

## Dónde vive el reloj: el puente, no cron

**El contenedor no tiene cron** — MEDIDO el 2026-09-28 dentro del contenedor en marcha:
`cron`, `crond`, `anacron`, `at` y `systemd-run` ausentes; existen `/etc/cron.d` y
`/etc/cron.daily` vacías, que son decoración del sistema base. Y **PID 1 es el propio
puente**, así que meter cron obliga antes a decidir quién supervisa a quién.

Pero el motivo de no usar cron no es ése, que se resolvería:

| | cron (dentro o fuera) | el puente |
|---|---|---|
| ¿Sabe si el agente está ocupado? | **no** | sí |
| ¿Viaja con el agente? | no | sí |
| ¿El disparo queda registrado donde alguien lo lee? | en un log que nadie abre | en el registro de la sesión |

**El puente ya sabe despertar una sesión sin humano** —eso es `deliver`— y lo único que le
falta es el *cuándo*. Poner cron al lado serían dos mecanismos que no se hablan.

## Dónde vive la agenda: con el agente, y llega apagada

En la carpeta del agente, para que **viaje en el `.vma`** junto a su vault y su memoria.

> **La agenda viaja, y llega SIEMPRE APAGADA.** El importador declara «esta agenda trae N
> entradas, ninguna activa». Encenderla es un acto de quien recibe, en su máquina.

Sin esa regla, importar un agente lo pone a gastar turnos solo, en una máquina que no eligió
esa cadencia y probablemente sin que nadie lo note hasta la factura.

## Los cinco problemas donde esto se gana el sueldo

**1 · Dispara mientras hay un turno corriendo.** Saltar, encolar o matar. **Saltar**, y
anotarlo. Encolar construye una cola que se vacía de golpe cuando el agente se libera, que es
justo el peor desenlace sin nadie mirando.

**2 · Nadie mira el resultado.** `deliver` ya trae declarada su grieta: confirma que el turno
**arrancó**, no que terminó, y **no hay comprobación posterior**. Un programador la multiplica
— ahora nadie mira *por diseño*, y en repetición. Así que la agenda **no está completa sin su
bitácora**, y con **tres estados**: `corrió` · `falló` · `se saltó`. Dos estados no bastan: un
registro que solo sabe anotar aciertos siempre dice que funciona.

**3 · La máquina estaba apagada a la hora.** Al despertar, **no se recuperan** los disparos
perdidos: se anota «no corrió, la casa estaba apagada». Que se pueda declarar lo contrario por
entrada, pero que **el silencio signifique no** — seis turnos de golpe al arrancar es un
estropicio, no una recuperación.

**4 · Cuesta, y nadie está mirando.** Cada disparo es un turno que se paga. **Techo declarado
de disparos por día**, y al pasarse **la entrada se apaga sola diciendo por qué**. No sigue
avisando: avisar en bucle es cómo se entrena a ignorar el aviso.

**5 · El vigía que no sabe que su tarea terminó.** Ya cobrado aquí: *más de cuarenta informes
idénticos en casi veinte horas sobre una producción ya cerrada*. Una entrada **exige fecha de
caducidad o condición de parada**; «para siempre» no debería poder escribirse sin teclearlo a
propósito.

## El permiso, que es lo que más pesa

Un turno programado corre con el permiso de su sesión. Si esa sesión es `full`, esto se
convierte en **ejecución arbitraria desatendida con temporizador**.

> Los turnos programados llevan **su propio techo**, que **nunca puede superar** al de la
> sesión. Y `full` programado **no se hereda: se teclea**.

Es la misma doctrina que ya gobierna `BRIDGE_PERMISSION`, que se niega a arrancar sin nivel
declarado y no degrada a `full` por omisión.

## Lo que NO es

- **No ejecuta comandos**: manda prompts. Quien decide qué hacer con ellos es el agente, con
  el permiso que tenga.
- **No es un motor de flujos**: las entradas no se encadenan. En cuanto una dependa del
  resultado de otra, eso es otra cosa y merece su propia decisión.
- **No sustituye a los disparadores del anfitrión**, que seguirán haciendo falta para despertar
  a una casa que no tiene puente.

## Con qué encaja

- **Soñar** (V4·B) es exactamente un proceso largo que quiere correr de madrugada.
- **Proponer en masa** querrá cadencia en cuanto haya colmenas suscritas.
- **El ciclo de conciliación** es el caso obvio, y también el más peligroso: un cierre
  desatendido escribe en el vault. Si algún día se programa, que sea con el techo de permiso
  más bajo que le sirva, y jamás heredando `full`.

## Lo que habría que medir antes de construirlo

- **Cuántos turnos programados querría de verdad una casa en una semana.** Si la respuesta es
  «uno», esto no merece un mecanismo: merece un disparador del anfitrión, que ya existe.
- **Si un turno desatendido sin nadie que lea su desenlace aporta algo** o solo genera texto
  que nadie abre. Es la pregunta que decide si la pieza vale, y hoy no está medida.
