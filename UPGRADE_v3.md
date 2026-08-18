---
title: Salto a la línea base v3 — adhesión al canon
tipo: plantilla ejecutable
para: dominios en v1.x o v2.x — y copias que declaran v3 con huella fuera del linaje (adhesión correctiva)
---

# UPGRADE a v3 — adhesión al canon

Sube un dominio existente a la línea base v3. **Se ejecuta DENTRO del dominio** — en una
sesión abierta en su proyecto, nunca desde otro dominio hacia él: el registro y las
memorias tienen que aterrizar en su casa.

**Qué es v3:** el canon vive en un repositorio git y el método cambia por parche. Subir
es **adherirse**: el manifiesto gana las claves que le falten (`canon`, `aportar_a`), la
semilla del libro se refresca a la vigente, entra la fila de adhesión al registro, y las
copias locales viejas del master **se archivan con fecha — no se migran, no se quedan
como trampas**. El contenido del dominio (folios, decisiones, bitácora, acta) **no se
toca**.

> [!important] Este documento no trae huella fija del master — a propósito
> El upgrader v2 sellaba `md5_marco_v2` en su frontmatter porque el master era un
> archivo congelado. En la era git **el master cambia con cada parche fusionado**: una
> huella fija estaría vieja en el siguiente merge, y el primer dominio en saltar
> abortaría contra una huella que ya nadie tiene. La verificación v3 es **contra el HEAD
> del canon remoto, recalculada de ambos lados en el momento** — git garantiza la
> integridad del transporte que el md5 del bundle garantizaba en v2.

**Material que acompaña:** `HUELLAS.md` (el linaje, para identificar la copia vieja) y un
clon fresco del canon oficial. Nada más viaja en bundle.

> [!warning] La matriz de incorporación del corte 3.0 NO existe — lápida, no relleno
> El corte 3.0 declaró un corpus de 62 parches incorporados y **su matriz nunca se
> escribió** (la que existe es del corte v2.0: 46 parches, con frases ancla). No se
> reconstruye de memoria: una matriz redactada meses después tendría tono de evidencia
> sin serlo. Consecuencia operativa: la herencia del paso 2 se hace **por fila única de
> línea base**, no por fila-por-parche; y la verificación por frase ancla de los
> descartados queda limitada a los parches que declaren la suya. Si algún día la matriz
> se escribe, será desde los archivos históricos del corte, marcada como reconstrucción
> con fecha.

---

## PREFLIGHT — compuerta todo-o-nada

**Si CUALQUIER punto falla: CERO escritura.** Se reporta el modo de fallo con sus
opciones y el salto se reintenta cuando esté resuelto. No hay «casi pasa».

### P0 · El canon de referencia es el REMOTO

`git clone` (o `git fetch`) del canon oficial, y verificar que el `main` local del clon
coincide con el remoto (`git rev-parse origin/main` contra el publicado). **La
comparación de referencia de TODO el preflight es contra ese HEAD — nunca contra una
réplica local o de red.** Caso medido que motiva la regla: una copia y su espejo de red,
idénticas entre sí y ambas fuera del linaje — todo chequeo que las comparaba entre sí
salía verde mirando dos huérfanas.

### P1 · La copia local casa con el linaje — y el frontmatter NO es evidencia

`md5` de la copia local de `MARCO_Inicial.md` del dominio, buscado en `HUELLAS.md`.
**Lo que el frontmatter declare no cuenta**: hay una copia medida que declara «v3.0» con
toda confianza y su huella no existe en el linaje.

| Resultado | Qué hacer |
|---|---|
| Casa con una versión atestada | ✅ sigue |
| Casa con una versión atestada **solo por el propio dominio** | ✅ sigue — la palabra del dominio en su nacimiento vale; anótalo en la fila de adhesión |
| Casa con una huella **NO ELEGIBLE** (borradores v3.0-preliminares) | ⛔ **abort duro con camino**: el dominio subió a un borrador que el linaje no libera. Se archiva esa copia con fecha, la adhesión sigue contra HEAD, y la fila del registro viejo **no se reescribe** — gana una nota al lado (el registro es historia, no se maquilla) |
| Declara versión **sin huella** en el linaje | ⛔ opciones del v2: diff contra la atestada más cercana y adoptar; o tratarla como editada; o abortar y abrir pendiente |
| No casa con NADA | ⛔ **editada a mano o derivada.** Opciones del v2: diff y rescatar lo local como tropicalización del manifiesto o parche propio; o seguir con respaldo `MARCO_Inicial.md.pre-v3-<fecha>` MÁS la lista literal de líneas que se pierden, impresa antes de tocar nada; o abortar |

### P2 · El registro de parches del dominio es consistente

Igual que en v2: existe, es legible, estados válidos, no registra parches inexistentes,
ninguna versión registrada mayor que la publicada. ⛔ Si contradice el linaje se listan
**las filas exactas a cuadrar** con arreglo propuesto. Las filas históricas que citen
huellas no elegibles **se anotan, no se reescriben**.

> [!important] Los parches PRE-corte no viven en el repo — y eso no es inconsistencia
> El repo publica **solo los parches posteriores al corte vigente**; el corpus anterior
> está incorporado a la plantilla y sus archivos individuales viven en el archivo
> histórico, fuera del repo. Un registro v1/v2 que cite parches de antes del corte **no
> está citando inexistentes**: está citando historia real que el repo ya no publica como
> archivos. Se comprueba contra la línea base heredada, no contra `parches/`. *(Todo
> dominio viejo que salte choca con esto; el tercero en saltar lo preguntó en vez de
> suponerlo, y ésa es la conducta que este texto quiere volver innecesaria.)*
>
> **Y la línea que separa anotar de reescribir, dicha de una vez:** lo que es HISTORIA
> —hechos, fechas, veredictos— se anota y nunca se reescribe. Lo que es **estado
> consumido por un parser** —el vocabulario de las filas (`aplicado`/`pospuesto`/
> `descartado`)— **se normaliza al vocabulario vigente, con UNA nota fechada** que
> registre la normalización: cambiar la forma legible de una afirmación que sigue
> siendo la misma no es maquillar historia, y dejarla ilegible es condenar al dominio a
> que sus parches se re-ofrezcan para siempre.

### P3 · El validador del dominio corre y pasa — con la excepción del arranque

⛔ Si falla por algo ajeno al salto, primero se arregla lo roto — la lista de fallos es
el trabajo previo. Sin validador no es fallo: se declara y se pide confirmación
explícita. Un hallazgo **conocido-benigno** puede quedar como excepción explícita
anotada en el registro, como en v2.

> [!important] La circularidad del arranque, y cómo se resuelve sin ablandar el abort
> Hay fallos cuya **causa es exactamente lo que este salto viene a arreglar** — el más
> obvio: un chequeo que grita «plantilla desfasada del canon». Exigir verde absoluto ahí
> vuelve el salto imposible por construcción: el requisito solo se satisface haciendo lo
> que el requisito bloquea. Esos fallos **no bloquean, pero tampoco se perdonan en
> bloque**: se enumeran **uno a uno**, se juzga de cada uno si el salto de verdad lo
> resuelve, y cada uno queda como **excepción explícita con su folio o su nota** en el
> registro antes de seguir. Y la contraparte que mantiene el rigor: en la verificación
> final, **cada fallo excepcionado debe estar apagado** — uno que sobreviva al salto
> reabre el abort retroactivamente: el salto no terminó.
>
> Lo que NO autoriza esta excepción: leerla hacia la propia conveniencia. Si hay duda de
> si un fallo es «del salto» o es deuda propia del dominio, **se trata como deuda propia
> y bloquea** — la carga de la prueba es del fallo, no del preflight.
>
> *(Descubierto en la primera ejecución real: el preflight abortó contra un dominio cuyo
> único fallo era el desfase que el salto resolvía — y el ejecutor se negó, con razón, a
> interpretarlo por su cuenta. Este texto existe para que no haga falta el juicio.)*

### P4 · No hay un salto anterior a medias

Señales: respaldo `pre-v3-*` existente, manifiesto con claves sin valor, copia que ya
declara v3 sin fila de adhesión. ⛔ Estado «upgrade interrumpido»: reanudar desde el
primer paso sin línea en el registro, o rollback y reinicio limpio.

---

## Los pasos — cada uno anota su línea en el registro al completar

1. **Diagnóstico.** Versión local detectada (por huella, no por frontmatter), parches del
   registro por estado, y qué claves le faltan al manifiesto.

2. **Herencia del corte 3.0 — fila única de línea base.** Se escribe:
   *«corpus del corte 3.0 (62 parches) heredado saldado en bloque — la matriz del corte
   es la fuente; lápida: matriz pendiente de reconstrucción marcada»*. **Salen aparte,
   siempre, uno a uno:** los **pospuestos** del dominio (posponer fue decisión activa) y
   los **descartados** — si el parche descartado declara frase ancla, se verifica contra
   el master de HEAD y se resuelve como en v2 (`✅ vía v3` o `🚫 sostenido`, con la
   desviación en los `avisos:` del manifiesto, **nunca en la copia**); si no la declara,
   queda *«sostenido, sin verificar contra plantilla»*. Los parches **posteriores al
   corte** llegan por el arranque, uno a uno — no son de este acto.

   > El vocabulario de las filas lo fija el **parser** del validador del dominio, no la
   > prosa: la fila lleva literalmente `aplicado`, `pospuesto` o `descartado` — una fila
   > que diga solo «incorporado» no casa con nada y el parche se re-ofrece para siempre.

3. **La copia vieja se ARCHIVA, el clon manda — y el modo queda DECLARADO.**
   `MARCO_Inicial.md` local → `MARCO_Inicial.md.pre-v3-<fecha>` (o al archivo histórico
   del dominio). El dominio pasa a leer el master **desde el clon del canon**; si su
   operación exige copia propia, se toma de HEAD y se anota con la huella recalculada.

   > [!important] El modo no se infiere de una ausencia: se declara
   > «Sin copia porque adherido al clon» y «sin copia porque alguien la borró» son
   > **estados opuestos con la misma cara**, y ningún instrumento puede distinguirlos
   > mirando el disco. El modo queda declarado donde ya vive esa respuesta: **la clave
   > `marco` del manifiesto** apunta al clon del canon (por referencia) o a la ruta de
   > la copia propia — y esa clave, no la ausencia, es lo que consultan la verificación
   > final y el validador del dominio. Un chequeo escrito en la era de la copia propia
   > («sin copia no vigilo nada») queda midiendo con el criterio de la era anterior:
   > parte de este paso es **actualizarlo para que consulte el modo declarado** — por
   > referencia exige que NO haya copia local y que el clon esté al día contra HEAD;
   > copia propia exige la copia y su huella.
   >
   > **La forma legible por máquina del modo** (pagada en la segunda corrida): dentro de
   > la sección `marco` del manifiesto, una línea `modo_marco: referencia | copia_propia`,
   > documentada ahí mismo como *la forma legible de la clave `marco`, no una segunda
   > clave*. Y el candado que impide que se vuelva una segunda verdad: **el validador
   > falla si `modo_marco` contradice lo que la prosa de `marco` declara** — dos formas
   > de la misma clave que divergen son exactamente el defecto que la regla de las
   > claves únicas quiere impedir.
   >
   > **Lo que el candado NO cubre, y hay que saberlo al instalarlo:** es un chequeo de
   > **presencia**, no de coherencia — detecta que la declaración falte o esté negada,
   > no que la sección se contradiga a sí misma. Caso medido el día que se diseñó: la
   > prosa afirmaba «por referencia» y a la vez conservaba una fila con la ruta de la
   > copia local recién archivada — y el candado dio verde, porque encontró la frase que
   > buscaba. **La coherencia interna de la sección es del PASO, no del chequeo**: al
   > declarar el modo, se actualizan TODAS las filas de la sección `marco` —copia,
   > parches, skills, conteos—, porque una fila vieja junto a la declaración nueva es
   > prosa que se desmiente y ningún candado barato la ve.
   >
   > **Y al tocar el chequeo, la prueba en ROJO es parte del paso, no cortesía aparte:**
   > se fuerza el caso que debe fallar —la copia resucitada en modo referencia— y se
   > comprueba que falla DE VERDAD, con su código de salida. Estás tocando al que vigila:
   > es el momento de máximo riesgo, y un chequeo probado solo en verde no está probado.
   > *(Pagado en la segunda corrida: el chequeo reescrito salió verde y correcto, y al
   > forzar el rojo imprimió `command not found` con exit 0 — un typo en el nombre de la
   > función lo había vuelto incapaz de fallar, dentro del propio acto de arreglarlo.)*
   >
   > *(Descubierto en la primera ejecución real: el ejecutor cumplió el paso al pie de
   > la letra y su validador se puso en rojo por ausencia — un chequeo suyo, correcto en
   > v2, midiendo la adhesión como defecto.)*

4. **Manifiesto.** Gana `canon` (default: el oficial) y `aportar_a` (**solo si el dominio
   dijo que sí** — `ninguno` es el fallback mientras no se decida), y **su clave `marco`
   se actualiza al modo elegido en el paso 3** — el clon, o la ruta de la copia propia.
   Si no hay manifiesto, se genera del contrato de la plantilla preguntando solo lo no
   deducible. *(No se añade clave nueva al contrato: `marco` ya responde «dónde vive el
   master», y una segunda clave para lo mismo sería una segunda verdad.)*

5. **El cierre migra al motor — donde lo haya.** Igual que v2: con motor en la máquina,
   el comando propio se vuelve alias fino; sin motor posible, copia declarada con
   `copia_declarada_de:` versión + md5 + fecha.

   **5b · Los genéricos del ciclo, desde el canon** (`skills/`, hoy nueve comandos con su
   `MD5SUM.txt`): verificar por huella recalculada; instalar del canon lo que falte.
   **El formato de instalación varía por máquina** —hay instalaciones de archivo plano y
   de directorio-por-skill— y el canon aún no declara los formatos: la verificación es
   por huella del **contenido**, y la traducción de formato que cada máquina haga queda
   anotada en su manifiesto. *(Deuda declarada del canon: publicar los formatos, para que
   la traducción no se invente en cada casa.)*

6. **La semilla del libro se refresca a la vigente.** Si el canon queda clonado al lado,
   por referencia (una copia junto a su original solo puede divergir); si el dominio vive
   lejos del clon, copia con la huella y fecha de lo copiado.

7. **La fila de adhesión y el instrumento.**
   `⬆️ adhesión al canon v3 · <fecha> · HEAD <hash git corto> · <notas del P1>` — y
   **correr el validador del dominio una vez más**. El salto no está terminado con la
   última escritura: está terminado cuando el instrumento del dominio lo mira y no grita.

---

## Verificación final

1. **Según el modo que declare `marco`:** por referencia → NO hay copia local y el clon
   está al día contra HEAD; copia propia → la copia casa con HEAD por huella
   recalculada. En ambos: la vieja está archivada con fecha ✅
2. El registro tiene la fila de adhesión, y las históricas anotadas sin reescribir ✅
3. El arranque del dominio ya no ofrece parches del corpus como «sin mirar» ✅
4. El manifiesto existe y sus claves obligatorias tienen valor — `canon` y `aportar_a`
   incluidas ✅
5. Si hubo migración al motor: el alias existe y el método copiado ya no está duplicado —
   *comprobable solo en la sesión siguiente; se reporta «movido, sin verificar»* ✅

## La primera ejecución paga el caso

Este documento se escribió **antes de que nadie lo corriera**: el caso de ejecución del
salto v3 está declarado pendiente en el corpus, y quien lo corra primero lo paga — en
parches, que es la moneda buena. Corre con el deshacer asegurado (la réplica no es
deshacer — lección 49), deja que el preflight aborte lo que tenga que abortar, y escribe
lo que duela.
