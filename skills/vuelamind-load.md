---
description: Carga el arranque de sesión del dominio actual — lee su initPrompt, corre el validador y comprueba si hay parches del marco esperando
---

# /vuelamind-load — retomar el trabajo en un dominio

Pone al asistente al día en el dominio donde está, **sin que el usuario tenga que pegar nada**. Es el compañero de `/vuelamind`: aquél crea el andamio de un dominio nuevo, éste **retoma** uno que ya vive.

> [!important] No es solo leer un archivo
> Cargar el `initPrompt` a secas deja al asistente con el contexto de la última
> sesión, que puede tener días. Este comando además **mide el estado actual** —
> por eso existe en vez de un "lee tal nota".

## Qué hace, en orden

### 1. Localizar el dominio

El `initPrompt.md` vive en el vault del dominio. Para encontrarlo, en este orden:

1. **Las memorias del proyecto** — suelen traer la ruta del vault. Es la vía fiable.
2. El directorio de trabajo actual, si el proyecto está ahí.
3. **Preguntar.** Si no hay forma de saberlo, se pregunta en vez de adivinar: cargar el `initPrompt` de otro dominio es peor que no cargar ninguno.

### 2. Leerlo entero

No en diagonal. Ese archivo suele traer las reglas de trabajo del dominio, los hechos que no hay que volver a suponer al revés, y los errores ya cometidos — que es lo que evita repetirlos.

### 3. Correr el validador del dominio

Cada dominio tiene el suyo. Reporta lo que envejeció desde la última sesión: conteos descuadrados, enlaces rotos, sincronización pendiente.

**El `initPrompt` describe un estado que puede tener días; el validador mide el de ahora.** Cuando se contradigan, gana el validador — y esa contradicción es material para el checkpoint.

### 4. Comprobar los parches del marco

Si el validador reporta parches **sin mirar** o **pospuestos**, léelos y **preséntalos uno a uno** antes de trabajar: qué corrige cada uno y qué costaría aplicarlo. Un parche puede cambiar cómo se escribe lo de hoy.

Los estados y su registro están en el marco del dominio. Recordar que **descartado** no vuelve a ofrecerse: para verlos hay que pedir el inventario completo al validador.

### 5. Presentar el estado, no un resumen del archivo

Cerrar con lo que el usuario necesita para decidir en qué trabajar:

- **Qué hay pendiente** y qué es lo primero según el propio dominio.
- **Qué oportunidades hay vivas**, en su propia tabla. Ver abajo.
- **Qué cambió desde la última sesión**, si el validador lo delata.
- **Qué está esperando algo externo** — un reinicio, una decisión, una sesión interactiva.
- **Los parches**, si hay.

> [!important] Las ideas también se presentan, y hay que hacerlo a propósito
> El marco separa **defectos** de **oportunidades**: lo que está mal va a la cola
> de pendientes, lo que podría estar mejor va al panorama. La cola es la que el
> validador cuenta y la que el documento de arranque enumera, así que preguntarse
> *"qué hay pendiente"* devuelve siempre **una sola de las dos listas**.
>
> Sin este paso las ideas **entran y no salen nunca**: un backlog de solo
> escritura. No dispara ninguna alarma —nada falla cuando nadie decide— y tiene
> una asimetría cruel: **cuanto mejor cumple un dominio la regla de no meter
> ideas en la cola de defectos, más se le acumulan invisibles.**
>
> Preséntalas **breves y aparte**, sin mezclarlas con los pendientes, y **solo las
> vivas** — las adoptadas y descartadas ya viven en el registro de decisiones, y
> volver a ofrecerlas es ruido.

> [!danger] Extráelas por EXCLUSIÓN, nunca por inclusión
> **Vivo es el estado por omisión.** El ciclo de vida manda marcar cuando una idea
> *deja* de estarlo —adoptada, descartada, invalidada—; nadie decora lo normal. Y
> la sección mezcla formatos: encabezados con emoji, encabezados sin emoji que
> agrupan viñetas, y viñetas sueltas.
>
> Así que un patrón que **nombre** el estado que quieres conservar responde otra
> pregunta —*"cuáles marcó alguien"*— y devuelve un puñado. La primera vez que se
> aplicó esta regla, la tabla salió con **3 ideas de 13**, y lo cazó el usuario
> preguntando *"¿no hay más?"*.
>
> La sección es corta por diseño: **léela entera antes de dar un número.** Un
> extractor sobre ella no ahorra nada y sí puede mentir.
>
> (Parche `2026-08-11-el-arranque-presenta-una-cola-y-esconde-la-otra`, nació aquí, v2.)

**Y ofrecer los comandos, en una línea al final.** Quien acaba de recibir el estado necesita saber qué puede pedir — sobre todo si el dominio es joven o la persona lleva poco usándolo:

> *«Si quieres ver qué más puedo hacer aquí: `/vuelamind-help`.»*

Una línea, no un catálogo: el catálogo es de ese comando y se genera solo. Si la persona ya lleva tiempo trabajando y va directo al grano, se omite — el recordatorio sirve una vez, no todas.

Y entonces **preguntar por dónde seguir**. No empezar a trabajar por cuenta propia: el `initPrompt` propone un orden, pero el usuario puede traer otra cosa en mente.

## Qué NO hace

- **No escribe nada.** Es de lectura. Lo que corrige documentación es el checkpoint.
- **No inicializa un dominio.** Eso es `/vuelamind` y la entrevista posterior.
- **No aplica parches solo.** Los presenta; la decisión es del usuario.

## Por qué está en el nivel personal

A diferencia del comando de reconciliación —que trae dentro las rutas y los nombres de notas de su dominio— **éste no hardcodea nada**: localiza el vault, lee el `initPrompt` que encuentre y corre el validador que ese dominio tenga. Por eso puede vivir arriba y servir a todos.

> [!note] Si algún día necesita saber un nombre de archivo concreto, deja de ser universal
> Ésa es la señal para bajarlo al dominio, junto con su comando de
> reconciliación. Ver el parche `2026-08-04-alias-vive-con-su-principal`, que
> documenta exactamente ese error cometido con `/commit`.

## En máquinas sin réplica automática

Este comando viaja por la carpeta sincronizada de comandos, así que llega solo a las máquinas de casa. **Un dominio en equipo administrado no lo recibe**: hay que copiarlo a mano a su carpeta de comandos, o pedirlo como parche.
