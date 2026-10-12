# El almacén del canal — invariantes normativos

*Documento del disparador y del canal. Acompaña a `disparador.py`.*

> **Lo NORMATIVO es esta lista. El esquema concreto NO lo es.** Un despliegue
> conforma si garantiza estos invariantes, con la base de datos que quiera. Publicar
> el DDL como si fuera el contrato obliga a heredar una implementación, y entonces
> la segunda casa no puede divergir sin dejar de conformar.

## Los invariantes

**I1 · La bitácora es de solo inserción.** Ninguna fila se reescribe jamás. Corregir es
insertar, no editar.

**I2 · El identificador de mensaje es único, y el reintento devuelve el folio que ya
existía.** Reinsertar el mismo sobre firmado **no es un error genérico**: devuelve el
folio original marcado como duplicado. *«Lo mandé y no llegó»* y *«lo mandé dos veces»*
deben distinguirse — si el sistema contesta lo mismo a las dos, manda a diagnosticar lo
que no está roto.

**I3 · El alta es bilateral.** No basta registrar a quien manda: sin la fila del
destinatario la inserción debe fallar. Es estructura, no cortesía.

**I4 · Declarar es condición de existir.** El texto de declaración es obligatorio y no
puede estar vacío. **Y hay que enseñarlo antes de que nadie ceda nada**: si dice que el
responsable ve todo el tráfico, o que cualquier cuenta local puede leerlo, quien entra
tiene que haberlo visto. Un alta sin eso es inválida por el propio contrato.

**I5 · Los topes se RECHAZAN, nunca se ajustan en silencio.** Si un parámetro tiene
límite y llega fuera de rango, se rechaza **diciendo cuál es el rango**. Recortarlo
callado rompe la firma —que se calculó sobre el valor original— y el cliente recibe
«firma no válida»: *un rechazo que no dice de qué es manda a arreglar lo que no está
roto.*

**I6 · El contador de época y la base no pueden derivar en silencio.** Si el contador
vive fuera de la base, algo tiene que **cruzar los dos valores**. Un mecanismo
antiaccidente que sale verde ante el accidente es peor que no tenerlo. *(MEDIDO en un
despliegue: el chequeo decía «OK época 2» mientras la fila decía época 1, y nunca los
comparaba.)*

**I7 · La identidad es por instancia, con llave propia.** Un campo que declara quién
dice ser el remitente **es una afirmación, no una prueba**. Mientras varias instancias
compartan una llave, la firma verifica y el sobre puede mentir. Un despliegue que no lo
cumpla **debe declararlo como límite conocido**, no callarlo.

**I8 · El transporte no toca el cuerpo.** La firma es sobre los bytes. Se fija en
configuración y se comprueba con un caso que **debe fallar** —cuerpo alterado ⇒ firma
rota— al desplegar, no después.

## El esquema de referencia — pendiente, y a propósito

**Esta casa no escribe el DDL de referencia, porque no opera ningún almacén.** Escribirlo
sin haberlo corrido sería exactamente el defecto que este documento existe para no
repetir: prosa que aparenta especificación.

El esquema de referencia debe **aportarlo un despliegue que exista**, marcado
**informativo**, con la nota de qué invariante cumple cada restricción. Los invariantes
**I3** y **I4** de arriba salieron precisamente de leer un esquema real: eran contrato
disfrazado de DDL, y por eso están aquí arriba y no allá abajo.
