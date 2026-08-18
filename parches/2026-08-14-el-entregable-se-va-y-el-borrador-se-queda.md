---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-17 (lección 53 del libro heredado)
---

# 2026-08-14 · El entregable se va y el borrador se queda

**Origen:** un dominio de operaciones · **Estado:** aplicado en la instancia el 2026-08-14

## Qué corrige

El método tiene una regla para **escribir a través de una capa**: el código de salida
solo prueba que la capa aceptó el encargo, así que hay que cruzarla y leer desde el
otro lado. Esa regla cubre el momento de la escritura.

**No cubre lo que queda de este lado después.**

Cuando un ciclo produce un artefacto que se deposita en un sistema ajeno —una hoja de
cálculo, un ticket, una presentación, el repositorio de otro equipo— el vault se queda
con **la versión que redactó**, no con **la que se entregó**. Entre las dos hay
ediciones: alguien recortó un párrafo, cambió el título, movió un dato de celda. El
entregable siguió evolucionando fuera; el borrador se quedó quieto dentro.

**Y la firma es la peor posible: el borrador existe, está completo y está bien
escrito.** Ningún validador lo marca —no hay enlace roto, no hay conteo descuadrado, la
fecha es de hoy—. La sesión siguiente lo abre y lo lee **creyendo que lee el
entregable**, porque no hay nada que sugiera lo contrario.

> [!note] La lección que generaliza
> **Un borrador de algo entregado deja de ser la fuente en el instante en que se
> entrega.** A partir de ahí es evidencia de qué se propuso, no de qué existe. El vault
> tiene que decirlo **en el propio archivo**, porque el archivo es lo único que la
> sesión siguiente va a mirar.

## Cómo se descubrió

**2026-08-14.** Un dominio redactó un canvas de presupuesto en dos archivos locales y
lo fue puliendo con el responsable a lo largo de la sesión. El responsable lo vació en
la hoja corporativa y siguió editándolo ahí: cambió el título, reformuló el bloque
inicial, quitó una viñeta, movió un texto a otra celda.

Al cerrar, el vault contenía dos borradores impecables **y desactualizados**, que
además todavía llevaban marcadores `[FALTA]` en tres campos ya resueltos. El asistente
nunca pudo ver la hoja —la vía de acceso devolvía `401`— así que **ni siquiera podía
comparar**: solo podía saber que lo que tenía no era lo entregado.

Lo que hizo visible el problema no fue un chequeo: fue que el responsable **pegó el
canvas en el chat** para revisarlo. Sin ese gesto, el borrador habría pasado a la
siguiente sesión como si fuera el documento.

## Por qué merece parche

Porque **no depende del sistema ajeno ni del dominio**. Cualquier instancia que produzca
entregables para fuera —y casi todas lo hacen— acumula borradores que se van separando
de su original sin avisar. El método ya sabe desconfiar de lo que escribe a través de
una capa; le falta desconfiar de **lo que se queda de este lado**.

Y porque la corrección obvia es la equivocada: *"actualiza el borrador con lo que
quedó"* solo funciona si puedes leer el entregable. Cuando no puedes —acceso denegado,
sistema cerrado, edición hecha por otra persona— actualizar es imposible y **marcar es
lo único que queda**.

## Cómo aplicarlo

> **Todo artefacto del vault que se haya entregado a un sistema externo lleva, en su
> propio encabezado, una línea que diga: dónde vive el entregable, en qué fecha se
> entregó, y que este archivo es la versión redactada — no la entregada.**
>
> Si el entregable es legible desde el vault, se compara y se anota la diferencia. **Si
> no lo es, se dice que no se pudo comparar** — eso es un resultado, no un hueco.

**Los tres movimientos:**

1. **Al cerrar, censa lo que salió.** ¿Este ciclo produjo algo que ahora vive fuera? Si
   sí, el borrador correspondiente **entra a la lista de notas a tocar**, aunque nadie
   lo haya editado — precisamente porque nadie lo editó.
2. **Marca el archivo, no solo la nota que lo cita.** La marca tiene que estar donde
   caiga el lector: en el borrador. Una advertencia en la nota de la entidad no sirve
   si la sesión siguiente abre el archivo directo.
3. **Y marca también los `[FALTA]` que ya se resolvieron fuera.** Un marcador de hueco
   sobre un dato que ya existe en el entregable es peor que no tenerlo: manda a
   averiguar algo que ya está averiguado.

## Cómo verificar

**El caso que fallaba:** abre el borrador como si fuera la primera vez. **Debe quedar
claro, sin salir del archivo, que no es la fuente.** Si hay que leer otra nota para
saberlo, la marca está en el sitio equivocado.

**El caso que DEBE SEGUIR FALLANDO:** un borrador que **todavía no se ha entregado**
tiene que seguir siendo la fuente, sin advertencia. Si al aplicar el parche todos los
borradores quedan marcados, se sobrecorrigió: lo que dispara la marca es **la entrega**,
no la existencia del archivo.

**Comprobación de mesa:** por cada entregable externo que el dominio recuerde haber
producido, busca su borrador. Los que no tengan marca son los que la próxima sesión va
a leer como si fueran el documento.

## A qué archivos

| Archivo | Qué hacer |
|---|---|
| El procedimiento de cierre | Un paso: censar lo que salió del vault en este ciclo y marcar sus borradores |
| Los borradores ya entregados | La línea de encabezado: dónde vive el entregable, cuándo salió, y que esto es lo redactado |
| La nota que cita el entregable | El enlace al sistema externo como fuente, con el borrador degradado a evidencia |
| El libro de errores del método | La lección — un artefacto correcto y completo puede ser falso por estar quieto |
