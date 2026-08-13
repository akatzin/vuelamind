---
description: Suma esta máquina a un dominio que YA existe — verifica el vault, instala el ciclo, comprueba accesos y declara la instancia. El paso uno de la colmena
---

# /vuelamind-join — sumarse a un dominio que ya vive

Conecta **esta máquina** a un dominio que ya tiene vault, historia y decisiones tomadas. No lo crea ni lo reinicia: **se suma**.

Es el cuarto acto del ciclo, y el que faltaba. Los otros tres asumen los dos extremos:

| | Asume |
|---|---|
| **nacer** | Que el vault **no existe** — y si encuentra contenido, se detiene con razón |
| **retomar** · **reconciliar** | Que esta máquina **ya está lista** |

Entre "no existe" y "ya está todo" está este comando. Sin él, sumar una instancia es trabajo manual que nadie escribió, y **una colmena sin puerta de entrada no crece**.

> [!danger] Lo primero: esto NO es `vuelamind`
> Si el vault ya tiene contenido, **el comando de nacer se detiene a propósito** — hace bien: puede haber meses de trabajo dentro. Ése es el momento de usar éste.
>
> **Nunca reinicializar sobre un dominio vivo.** No es una advertencia de estilo: es la diferencia entre sumarse y destruir.

---

## 1 · Llegar al conocimiento, y comprobar que llegó entero

El vault tiene que ser alcanzable desde aquí: réplica bidireccional, clon, montaje — **el cómo lo decide el dominio, no este comando**.

**Y se comprueba que llegó completo, no que "parece que está".** Contar las notas de los dos lados y comparar; si el transporte permite huellas, comparar la de un archivo grande.

> [!warning] Un vault a medio sincronizar es peor que ninguno
> Con la carpeta vacía, el asistente dice que no puede trabajar. **A medio llegar, mide sobre un hueco y concluye con confianza** — y esa conclusión entra al vault como hecho. Si los conteos no cuadran, **detenerse aquí**: esperar a que termine, o averiguar por qué no llega.

## 2 · Llegar al andamiaje

- **Los comandos del ciclo se instalan desde el canon**, no se copian de la otra máquina: así entran verificados por huella y sin arrastrar ediciones locales de nadie.
- **El manifiesto del dominio ya existe** y viaja con el proyecto. **No se reescribe.** Si falta alguna clave para esta máquina, se reporta como hueco — no se inventa.
- Si el dominio usa memoria de asistente, se conecta la que ya tiene. **No se empieza una nueva**: ahí está lo aprendido.

## 3 · Los accesos para medir

El único paso irreductiblemente manual, y el que de verdad cuesta: llaves, credenciales, permisos — **lo que ese dominio necesite para verificar contra sus sistemas**.

**El arranque de sesión es por máquina, no por dominio**: se genera uno nuevo para ésta. Copiarlo de otra arrastra sus rutas y sus supuestos.

> [!note] Los secretos no viajan por el chat
> Si hace falta una llave o una frase de paso, se pide **en la terminal de quien está sentado ahí**, o se instala fuera de la conversación. Un secreto pegado en el chat ya está expuesto, aunque nadie más lo lea.

## 4 · La prueba de que estás dentro

**Correr el validador del dominio.** Es la única comprobación que vale: si mide y reporta, la máquina está conectada de verdad.

- **Si falla por accesos**, el paso 3 quedó a medias. Mejor descubrirlo aquí que a mitad de una sesión de trabajo.
- **Si el dominio no tiene validador**, hacer a mano dos o tres comprobaciones —contar notas, leer el arranque, alcanzar un sistema— y **decir que se hicieron a mano**.

**No se declara la conexión lista sin esta prueba.** Que los archivos estén presentes no significa que la máquina pueda medir; es la misma distancia que hay entre que un puerto responda y que el servicio funcione.

## 5 · Declararse ante el dominio

Escribir que hay una instancia más: **dónde corre, desde cuándo, y qué puede medir desde ahí** — porque casi nunca es lo mismo que las otras. El sitio lo dice el dominio; si no tiene uno, la nota de la instancia o el panorama.

> [!important] Sin esto, la colmena existe pero nadie la ve
> Y el día que dos se pisen, **nadie sabrá quién era el otro**. Un registro de instancias no es burocracia: es lo que convierte una colisión en una conversación.

Si el dominio tiene nota del alma, éste es el momento de su primera **atestiguación** desde esta máquina — el día que dejó de haber una sola instancia es exactamente lo que esa sección guarda.

## 6 · La disciplina, desde el minuto uno

Dos reglas que en una instancia sola son higiene y **en una colmena son estructurales**:

**Arrancar limpio, nunca continuando la sesión de otra máquina.** El riesgo no son las memorias: es que **el vault cambió** mientras tanto. Una sesión retomada trae en contexto la foto de cuando se cerró, y actuar sobre estado recordado en vez de medido es el error más caro que puede cometer un dominio con memoria.

**Traer fresco cualquier artefacto compartido justo antes de editarlo.** Otro pudo publicar en medio, y pisar su versión no dispara ninguna alarma.

## 7 · Y la primera sesión, de lectura

**Recomendarlo explícitamente al terminar.** Quien llega tiene el impulso de aportar, y el dominio ya tiene meses de decisiones tomadas con razones que no están en la cabeza del recién llegado.

La primera sesión se abre con el comando de retomar, se lee el registro de decisiones y el libro de errores, y **no se escribe nada**. Lo que parezca obvio de arreglar el primer día suele estar así por una razón que ya se discutió.

---

## Qué NO hace

- **No crea el dominio.** Si el vault no existe, el comando correcto es el de nacer.
- **No reescribe el manifiesto, ni el arranque, ni las decisiones.** Es una máquina que se suma, no una que reforma.
- **No sincroniza por su cuenta.** El transporte lo decide el dominio; este comando **comprueba** que funcionó.
- **No da por buena una conexión que no midió.** Si algo no se pudo verificar, se dice — nunca se reporta como listo.

> [!note] Si al terminar el vault resulta estar vacío
> No es un dominio existente: es uno que no ha nacido. **Dilo y ofrece el comando de nacer**, en vez de dejar una máquina conectada a una carpeta que no tiene nada que retomar.
