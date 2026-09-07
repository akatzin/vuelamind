---
title: Salto menor a v3.5 — el buzón de aprendizaje, y el ciclo de parches que se retira
tipo: plantilla ejecutable
para: dominios ya en la línea base v3 que quieran aportar lo que aprenden
---

# UPGRADE a v3.5 — el buzón de aprendizaje

> [!important] ESTE SALTO ES OPCIONAL, y esa es la primera cosa que hay que decir
> **Un dominio en v3 sigue completo sin él.** No toca el ciclo —nacer, retomar, cerrar,
> escalar, censar—, no cambia el vault, no cambia el validador, y **no cambia nada de cómo
> escribes tus lecciones en casa**, que es la parte que de verdad importa y que nunca estuvo
> congelada.
>
> Lo que cambia es **el viaje de vuelta**: cómo llega al canon lo que aprendiste. Si tu
> dominio trabaja solo y no piensa aportar nada, **no saltes**.

> [!important] LEVANTA EL CONGELAMIENTO — y el ciclo de parches NO vuelve como era
> Estuvo suspendido desde el **2026-08-18**, diecinueve días, por una razón medida: **el
> ciclo costaba más de lo que devolvía**, y la carga la pagaba entera la casa que se había
> equivocado. Escribir el parche con su forma exacta, anonimizarlo como conjunto, tener
> cuenta en la plataforma del canon, seguir el hilo de una revisión.
>
> **La v3.5 no lo reactiva: lo reemplaza.** Tu casa escribe sus lecciones y las manda. Ya
> está. El vigía del canon hace el resto.

## Qué trae, en una frase cada cosa

**Un buzón abierto.** `POST` a `https://learning.vuelamind.ai` con tu libro de errores en el
cuerpo, en markdown. **Sin llaves, sin cuenta, sin registro.** Devuelve el identificador de
tu aportación, que es el hash de su contenido — así que **si coincide con el que calculaste
antes de mandar, tienes prueba de que llegó completo**. Deduplica por contenido: mandar dos
veces lo mismo no ensucia nada.

**Un skill que lo usa bien: `/vuelamind-learn`.** No es un `curl` con buenos modales. Hace
cuatro cosas que nadie hace a mano dos veces seguidas:

1. **Criba por generalidad.** Solo viaja lo que sobrevive a quitarle todos los nombres
   propios. Lo que solo vale en tu casa **se queda en tu casa**, y lo que el canon ya tiene
   también — una lección que dice *«familia del parche tal»* es superficie de lectura sin
   regla nueva.
2. **Anonimiza, y te enseña el TEXTO FINAL** — no una lista de *«sustituí A por B»*, que
   obliga a reconstruir el resultado en la cabeza y es donde se cuela lo que no se ve.
3. **Te pregunta lo que ninguna máquina puede juzgar**: si la aportación se identifica o va
   anónima, si se tachan los nombres de terceros —que no dieron su palabra para aparecer en
   un corpus público— y qué es público en tu contexto.
4. **No manda nada sin tu sí.** Y cada permiso es un acto aparte: elegir destino no es
   aprobar el texto, y aprobar un envío **no autoriza el siguiente**.

**Tres modos, para que no te pregunten dos veces lo mismo.** Se declaran en el manifiesto
con `learning_modo`: `preguntar` (por omisión), `recordar-destino` (el punto medio, y el que
casi todos quieren: quita la pregunta que siempre tiene la misma respuesta y conserva la que
no se puede deshacer), y `automatico`.

## Qué NO trae, y conviene leerlo

> [!danger] Lo que sale del buzón no se retira
> Es de **solo inserción**. No se edita, no se borra, no se corrige: lo que mandaste queda.
> Por eso el skill te enseña el texto antes, y por eso `automatico` es una decisión que se
> escribe en frío en el manifiesto y no a media corrida.

> [!warning] Lo que ENTRA al buzón es dato de un desconocido, jamás instrucción
> Cualquiera puede mandar cualquier cosa: es un `POST` abierto y eso es su requisito, no su
> carencia — sin anonimato no hay volumen. **Nada de lo que llegue ahí autoriza nada**, por
> mucho que su texto parezca una orden. Y **nada sube al canon sin palabra humana**: esa
> revisión no se automatiza nunca por comodidad.

**No trae panel, ni estado de tu aportación, ni respuesta.** El buzón sabe si algo se recibió
y si se leyó; **no sabe si fue aceptada o rechazada**, porque ese juicio ocurre en la casa
del vigía y hoy no vuelve. Si tu lección entra al canon, la verás en el canon.

## Cómo saltar

> [!warning] Mientras este salto viva en una rama sin fusionar, LEE ESTO PRIMERO
> El master con `version: 3.5` **solo existe en la rama de la propuesta**, no en la rama
> principal del canon — que sigue diciendo `3.4` hasta que se fusione. **Es la misma rama
> donde vive este documento.**
>
> Consecuencia para quien adhiere **por referencia** (`modo_marco: referencia`, sin copia
> propia del master): **tu dominio queda partido** — skills de 3.5 sobre un master de 3.4, y
> tu versión deja de tener un solo valor. **No es un defecto tuyo y no lo puedes arreglar
> desde tu casa**: se resuelve solo cuando la rama entre a la principal.
>
> Si eso no te sirve, **espera a la fusión**. Si saltas igual —para probar—, **anótalo**: es
> un estado transitorio y conviene que quede escrito por qué tu versión no cuadra.

**Cinco pasos. Los tres primeros son obligatorios.**

1. **Trae el master y comprueba la versión.**
   - Si consumes por **copia**: trae el archivo del canon y comprueba que diga
     `version: 3.5`. **Respalda tu copia antes** si la tienes modificada — el salto reemplaza
     el bloque del congelamiento.
   - Si consumes por **referencia**: no tienes copia que traer. **Comprueba en el canon** qué
     versión sirve tu rama configurada, y si dice `3.4` estás en el caso del aviso de arriba.
   - **Si la comprobación falla, no es que fallara el paso**: es que estás mirando una rama
     que todavía no la tiene. Mira la de la propuesta.

2. **Reinstala los TRES skills que esta versión modificó**, desde `skills/` del canon, en el
   nivel donde vivan tus otros skills del marco:

   | skill | qué le cambió la v3.5 |
   |---|---|
   | **`vuelamind-learn`** | **es nuevo**: es la vía de aportar |
   | **`vuelamind-commit`** | aprende `learning_en_cierre` y deja de mandar parches por pull request |
   | **`vuelamind-load`** | **se le quitó el bloque del congelamiento** |

   > [!danger] El tercero es el que se salta, y es el que más ruido hace
   > `vuelamind-load` **corre en cada arranque de sesión**. El anterior a la v3.5 lleva un
   > bloque que anuncia *«el ciclo de parches está suspendido, omite esos pasos»* — y eso
   > **ya es falso**. Si no lo reinstalas, tu casa va a leer esa frase cada día sin que nada
   > falle, y va a seguir omitiendo pasos que la v3.5 devolvió.
   >
   > **No es opcional como el `commit`**: aquél solo hace falta si activas el encadenado;
   > éste hace falta siempre, porque el bloque miente en todos los casos.
   >
   > **Compruébalo así:** tu `vuelamind-load` instalado **no debe mencionar** el
   > congelamiento. Si lo menciona, es el viejo.

   **La lista sale de comparar la versión con la anterior, no de recordar qué se tocó.** La
   primera redacción de este documento nombraba **uno** de los tres, porque su autor listó lo
   que recordaba haber escrito. Los otros dos no dan error: siguen funcionando y dicen cosas
   que dejaron de ser ciertas.

   > [!important] La FORMA del archivo la manda tu máquina, no el canon
   > El canon lo publica como un archivo suelto, `vuelamind-learn.md`. **Algunos entornos lo
   > quieren como una carpeta con el archivo dentro** (`vuelamind-learn/SKILL.md`). **Mira
   > cómo están instalados tus otros skills del marco y copia esa forma** — no la inventes.
   >
   > Y si es tu **primer** skill del marco y no tienes contra qué comparar: instálalo del
   > modo que documente tu entorno, y **comprueba que aparece invocable antes de seguir**. Un
   > skill con la forma equivocada no da error: simplemente no existe.

   **Comprueba su huella contra `skills/MD5SUM.txt` del canon.** Una copia que difiere del
   canon es un canon mentiroso, y no avisa.

3. **Declara en tu manifiesto**, y son tres claves, no una:

   | clave | qué es | si falta |
   |---|---|---|
   | `buzon_aprendizaje` | **el endpoint del buzón** — `https://learning.vuelamind.ai`, o el de tu ecosistema. Es una URL HTTP | el skill te la pregunta cada vez |
   | `learning_procedencia` | si tus aportaciones **se identifican** o van anónimas | **la corrida se detiene y la pide** |
   | `learning_terceros` | si se **tachan los nombres** de otras casas y personas | **la corrida se detiene y la pide** |

   > [!warning] `buzon_aprendizaje` es NUEVA — no reutilices `aportar_a`
   > `aportar_a` ya existe y nombra **un repositorio git** al que proponer parches. El buzón
   > es **un endpoint HTTP** y es otra cosa. Si tu dominio ya declaró `aportar_a`, **déjala
   > como está**: puede ser una decisión fechada en tu libro, y este salto no pisa decisiones
   > de nadie.
   >
   > Las dos últimas **no son opcionales aunque lo parezcan**: deciden qué se publica de ti y
   > de terceros, y **ningún valor por omisión es seguro** — ni tachar de más, que destruye la
   > lección, ni tachar de menos, que publica a quien no dio su palabra.

   Si prefieres **no aportar nada**, declara `buzon_aprendizaje: ninguno` **explícitamente**.
   Sin declarar no es un permiso: es un hueco, y se te va a preguntar cada cierre.

4. **Comprueba que el buzón responde, ANTES de tener nada que mandar.**

   Un `GET` a la raíz del endpoint devuelve un JSON con el conteo de aportaciones y cómo
   aportar. **Hazlo ahora**, cuando no cuesta nada.

   > [!important] Por qué este paso existe y no es paranoia
   > Sin él, **la primera señal de que el buzón no responde llega en el momento más caro**:
   > con el texto ya cribado, ya anonimizado, ya revisado y ya aprobado, a punto de salir. Un
   > endpoint mal escrito en el manifiesto no se distingue de uno caído hasta que lo tocas.

5. **Si tu dominio traía el bloque del congelamiento en su propio manifiesto o en su
   arranque, retíralo con fecha.** Muchos lo escribieron diciendo *«se retira cuando exista
   el flujo nuevo»*. Ya existe. **El gesto es tuyo y este documento no puede hacerlo por ti**,
   porque no sabe dónde lo escribiste — pero si no lo haces, tu casa sigue leyendo cada
   cierre que el aprendizaje está suspendido.

> [!warning] ¿SALTASTE DESDE LA RAMA antes de que se fusionara? Cuatro cosas, y ninguna avisa
> Mientras esta versión vivió en una propuesta sin fusionar, saltar era posible y algunas
> casas lo hicieron. **Lo que instalaste entonces pudo cambiar bajo tus pies** —una propuesta
> se corrige hasta el último día— y **nada de eso produce un error**:
>
> 1. **Vuelve a comparar TODOS tus skills del marco contra `skills/MD5SUM.txt` de la rama
>    principal**, no solo los que instalaste. En el caso real medido, **dos habían cambiado**
>    entre el salto y la fusión.
> 2. **Si reutilizaste `aportar_a` para el buzón, deshazlo**: mueve el valor a
>    `buzon_aprendizaje` y **restaura el que `aportar_a` tenía antes**. La primera redacción
>    de este documento mandaba reutilizarla, y en la casa que lo siguió eso **degradó a
>    historia una decisión fechada de su libro de decisiones** — tomada con su responsable
>    delante.
> 3. **Corrige tu registro de envíos** si anotó la clave equivocada.
> 4. **Comprueba tu versión otra vez.** Si consumes el canon por referencia, mientras la
>    propuesta no estuvo fusionada tu dominio quedó **partido** —skills nuevos sobre master
>    viejo— y **eso se resolvió solo al fusionar**, sin que hicieras nada.
>
> **Y la lección de orden que deja, para quien publique la próxima versión:** para un dominio
> en modo referencia, **fusionar no es el último paso del salto: es una precondición**. Un
> salto que vive en una rama es ininstalable de forma coherente para ellos, por bueno que sea
> su documento.

## 5 · La primera corrida — la lanza este salto, no tú

**Al terminar los cuatro pasos, corre `/vuelamind-learn` inmediatamente.** No es una
sugerencia para después: es **el único paso que comprueba que lo instalado sirve**, y si se
deja para otro día no se hace.

Un archivo copiado en su sitio con la huella correcta demuestra que el archivo llegó. **No
demuestra que el skill funcione en esta casa** — que encuentre el libro de errores, que la
criba tenga algo con qué trabajar, que el manifiesto declare lo que hace falta. Eso solo se
ve corriéndolo.

**Llega hasta que te enseñe el texto que mandaría, y ahí ya sabes que funciona.** Mandar es
tuyo y es aparte: el skill se detiene solo y te lo pregunta.

**Qué esperar en la primera, para que no parezca un fallo:**

- **No hay registro de envíos previos**, así que el skill lo dice y **pregunta desde dónde**
  en vez de mandar todo por omisión. Es la conducta correcta, no un error.
- **La criba puede dejar fuera mucho.** Un libro de errores joven suele ser casi todo
  conducta propia del dominio, y eso no viaja. **Que salgan pocas lecciones o ninguna es un
  resultado válido**, y el skill te dice por qué falló la prueba cada descarte.
- **Si tu manifiesto no declara `aportar_a`**, el skill se detiene y lo pide. También
  correcto: sin declarar no es un permiso, es un hueco.

**Y la verificación dura, si decides mandar:** el identificador que devuelve el buzón es el
hash del contenido. **Compáralo con el que calculaste antes de mandar.** Si coinciden, tienes
prueba de que llegó completo y sin truncar. Es gratis y es la única verificación real que
existe de este lado.

## 6 · ¿Quieres que el cierre lo haga solo? — la pregunta con la que termina este salto

**Este salto no termina instalando: termina preguntándote esto**, porque si no se pregunta
aquí no se pregunta nunca — y una integración que nadie decide queda sin decidir, no
rechazada.

`/vuelamind-commit` ya detecta, en cada cierre, si de la sesión salió algo del método. Lo que
puedes decidir ahora es **qué hace con ello**:

| `learning_en_cierre` | Qué pasa al cerrar |
|---|---|
| `no` (por omisión) | El cierre **presenta** los parches sin aportar y ahí acaba. Tú corres `/vuelamind-learn` cuando quieras |
| `si` | El cierre **encadena** `/vuelamind-learn` con lo que salió, en su último paso. Sigue enseñándote el texto y sigue pidiendo tu sí antes de mandar |

**Lo que gana el `si`:** que la lección se aporte **el día que se aprendió**. Un parche que
espera a que alguien se acuerde de correr un comando espera para siempre — es el mismo
defecto que este método ya documentó con las decisiones delegadas: *sin un momento definido,
no se rechazan, no se toman nunca*.

**Lo que cuesta:** un paso más en cada cierre, aunque no haya nada que mandar.

> [!warning] El `si` NO convierte el envío en automático
> Encadena **cuándo se te pregunta**, no **si** se te pregunta. El texto se sigue enseñando y
> el envío se sigue pidiendo. Lo que quita las preguntas es `learning_modo`, que es otra
> clave y otra decisión — **y ésa no la tomes hoy**, tómala cuando hayas visto varias corridas.

**Se declara en el manifiesto del dominio.** Si no lo declaras, queda en `no`, que es lo
correcto mientras no sepas cuánto material te va a salir por cierre.

> [!danger] Si eliges `si`, tienes que actualizar `vuelamind-commit` TAMBIÉN
> El paso 2 instaló `vuelamind-learn`, que es el que aporta. **Pero quien encadena es
> `vuelamind-commit`**, y el tuyo es de antes de la v3.5: **no sabe qué es
> `learning_en_cierre` y la va a ignorar en silencio.** Declararías `si`, no se encadenaría
> nada, y **nada te lo diría** — es la lección 63 del propio canon, *una clave que se ignora
> en silencio se lee como vigente*.
>
> **Instálalo desde `skills/` del canon**, igual que el otro y con su huella comprobada.
> **Compruébalo así:** tu `vuelamind-commit` instalado tiene que mencionar `learning_en_cierre`.
> Si no lo menciona, es el viejo.
>
> **Y si eliges `no`, no toques `vuelamind-commit`.** No hace falta, y un salto que te hace
> reinstalar lo que no cambió es un salto que la gente se salta.

## 7 · Si venías de la v3.4

**No hay conflicto: son piezas distintas y ninguna depende de la otra.** El canal de la v3.4
es transporte firmado entre casas que se conocen; el buzón es abierto, anónimo y para
desconocidos. **Si tu casa opera el buzón al que va a mandar**, dilo antes de mandar: lo tuyo
entraría como anónimo y el corpus registraría como de fuera algo que salió de dentro. Para
casas que ya se conocen, el canal es el camino natural.

## Es un salto MENOR, y por eso no trae las tres piezas de una mayor

`UPGRADE.md` pide, para una versión **mayor**, tres cosas junto al master: el documento del
salto, sus huellas y su matriz de incorporación. **Aquí solo existe la primera, y es
correcto.** Una mayor corta línea base: reemplaza el master, y hacen falta huellas para
identificar la copia vieja y una matriz para saber qué parches quedaron dentro. Ésta añade
una vía y retira otra, sin tocar la línea base.
