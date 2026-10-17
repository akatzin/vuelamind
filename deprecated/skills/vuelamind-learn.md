---
description: Manda al buzón de aprendizaje del marco lo que este dominio aprendió equivocándose — solo lo que sirve a cualquier casa, anonimizado, y enseñándote el texto antes de que salga. Eliges el endpoint, y puedes declarar que no se te vuelva a preguntar
---

# /vuelamind-learn — aportar lo aprendido, sin aportar de más

El marco mejora con lo que las casas aprenden equivocándose. Este skill es **la vía**: coge
las lecciones de este dominio, **descarta las que solo valen aquí**, **le quita lo que no
debe salir**, te enseña exactamente qué va a mandar, y **solo entonces lo manda**.

> [!danger] LO QUE SALE, SALE PARA SIEMPRE
> El buzón es de **solo inserción**: lo aportado no se edita ni se retira. Y va a un servicio
> público que otras casas leen. **Por eso este skill no manda nada sin que lo hayas visto** —
> no es una formalidad, es la única oportunidad que hay.

---

## 1 · Adónde se manda — SE PREGUNTA, salvo que ya se haya decidido no preguntar

**Dos destinos posibles:**

| | |
|---|---|
| **`https://learning.vuelamind.ai`** | el buzón del canon. Es el destino por omisión |
| **otro** | para un ecosistema separado que corra su propio buzón |

**Se pregunta cuál** — salvo que el dominio haya declarado su modo (ver abajo). Si el
manifiesto declara **`buzon_aprendizaje`**, ése es el valor **propuesto**, y propuesto sigue
siendo una pregunta.

> [!warning] `buzon_aprendizaje` NO es `aportar_a`, y confundirlas pisa decisiones ajenas
> `aportar_a` existe desde antes y nombra **un repositorio git**. Ésta nombra **un endpoint
> HTTP**. Se parecen en que las dos dicen «adónde va lo que aprendo», y por eso invitan a
> unificarse — **pero un dominio puede tener declarado un repositorio con fecha y motivo en
> su libro de decisiones**, y reutilizar la clave lo sobrescribe sin que nada avise.
>
> Medido: la unificación se intentó y una casa la cazó al saltar, porque su `aportar_a`
> apuntaba a un repositorio decidido semanas antes. **Dos nombres para dos cosas distintas no
> es incoherencia: es precisión.**

> [!warning] Decir a dónde vas NO es dejar elegir, y confundirlo es fácil
> Anunciar *«mando a tal sitio»* y seguir adelante cumple la letra de *«se dice en voz alta»*
> y se salta lo único que importaba: que el dueño escogiera. **Si nadie contestó una
> pregunta, no hubo elección** — por convincente que fuera el valor por omisión.
>
> Esto **no** aplica cuando el dueño decidió de antemano no ser preguntado: ahí sí hubo
> elección, y fue anterior. La diferencia entre ahorrarle una pregunta y tomársela por él es
> **que lo haya dicho**.

### Los tres modos, y cómo se elige uno

El dominio declara su modo en el manifiesto con `learning_modo`. **Por omisión, `preguntar`.**

| modo | destino | texto anonimizado | envío |
|---|---|---|---|
| `preguntar` | se pregunta | se enseña y se aprueba | se pide |
| `recordar-destino` | del manifiesto, **se nombra** | se enseña y se aprueba | se pide |
| `automatico` | del manifiesto, **se nombra** | **se enseña DESPUÉS, en el reporte** | **no se pide** |

**`recordar-destino` es el punto medio y suele ser el que la gente quiere:** quita la
pregunta que siempre tiene la misma respuesta y **conserva la única que no se puede
deshacer**.

> [!danger] Qué estás aceptando con `automatico`, dicho sin adornar
> Que **saldrá texto que nadie miró antes de salir**. La detección de datos identificables
> no atrapa todo — en la primera corrida real de este skill dejó pasar un handle en
> minúsculas dentro de una frase y tres punteros numéricos, y los cazó una persona leyendo.
> En `automatico` eso se publica, y el buzón no se edita ni se retira.
>
> Es una elección legítima cuando lo que se manda es rutinario y el dueño ya vio varias
> corridas. **No lo es la primera vez**, y por eso el modo no se enciende desde dentro de
> una corrida: se declara en el manifiesto, en frío, antes de que haya nada que mandar.

**Cómo se enciende y cómo se apaga.** Editando `learning_modo` en el manifiesto del dominio.
**Nunca lo cambia este skill por su cuenta**, ni siquiera si el dueño lo dice a media corrida:
en ese caso se termina la corrida como estaba, se dice cómo se declara, y se deja el cambio
para la próxima. Un modo que se enciende con una frase suelta se enciende sin querer.

**Y hay cuatro cosas que `automatico` NO apaga**, porque no son preguntas de conveniencia:

1. **La compuerta de generalidad** — sigue filtrando lo que solo vale en casa.
2. **La parada en seco ante algo con forma de credencial.** Eso no es preguntar: es fallar,
   y fallar cerrado es correcto en todos los modos.
3. **El reporte completo de lo que salió** — texto, destino, identificadores. En automático
   es lo único que queda, así que se enseña entero, no resumido.
4. **Un destino nuevo vuelve a preguntar.** El modo recuerda **una** decisión, no autoriza
   cualquier dirección futura: si el endpoint no es el declarado, se pregunta aunque el modo
   sea `automatico`.

## 2 · Qué se manda — SOLO lo que sirve a cualquier casa

**La compuerta, y no es negociable:** una lección entra **si y solo si** pasa esta prueba —

> **Sustituye TODOS los nombres propios por genéricos. ¿Sigue siendo cierta y útil?**

Si sí, es del método y viaja. Si no, **se queda en casa**: es cierta, es tuya, y no le sirve
a nadie más. **Esto no se pregunta al dueño.** El buzón es del método; lo que solo vale en
un dominio no tiene por qué ocupar la atención de quien lee.

**Qué queda fuera, típicamente:**

- **La conducta propia de este dominio** — cómo se portó su asistente, qué le corrigió su
  responsable. Puede ser cierta, dolorosa e instructiva, y aun así no ser una regla que el
  marco pueda adoptar.
- **Lo que el canon YA tiene.** Si la entrada dice *«es la lección N del libro heredado»* o
  *«familia del parche tal»*, el marco ya lo sabe: mandarla otra vez, envuelta en un caso
  nuevo, es superficie de lectura sin regla nueva. **Se comprueba en el canon antes de
  mandar, no se supone.**

  > [!important] El corpus está en DOS sitios y ninguno es obvio
  > **Las reglas numeradas viven dentro de `MARCO_Inicial.md`**, en su sección del libro de
  > errores — no en un archivo aparte, que es donde todo el mundo las busca primero. **Y los
  > parches son archivos sueltos en `parches/`.**
  >
  > Hay que mirar **los dos**: una lección puede estar como regla numerada y no tener parche,
  > o al revés. Y si tu dominio consume por referencia y no tiene copia local, se mira en el
  > canon configurado.
- **Lo que es de una herramienta y no del método** — a menos que la lección sobreviva a
  cambiar la herramienta.

> [!important] La criba se ENSEÑA, y también lo descartado
> Se dice qué entra, qué no entra, y **por qué falló la prueba** cada descarte. Una criba
> silenciosa es indistinguible de no haberla hecho, y el dueño no tiene forma de notar que
> se cayó algo que él habría mandado.

**Y solo lo NUEVO desde la última vez.** El skill recuerda hasta dónde mandó y propone lo
posterior:

- **Si el registro se perdió o nunca existió, se dice y se pregunta desde dónde** — no se
  manda todo por omisión.
- **El registro es una ayuda, no una verdad.** Puede divergir; por eso la lista se enseña
  entera y no se confía en él a ciegas.

> [!danger] El registro TIENE domicilio, y si no se crea la primera vez no existe nunca
> Vive en **`.learning-enviados`**, en la raíz del dominio — o donde diga
> `learning_registro` en el manifiesto, si el dominio prefiere otro sitio.
>
> **Se crea en la primera corrida que mande algo.** Si no se crea, la segunda corrida tampoco
> lo encuentra, vuelve a preguntar desde cero, y **eso se repite para siempre** sin que nada
> falle — cada corrida parece la primera.
>
> Una fila por envío, y **solo se escribe la fila cuando el servicio confirmó**:
>
> ```
> # fecha       endpoint                        id (sha256 del cuerpo)   qué se mandó
> 2026-09-06    https://learning.vuelamind.ai   4db16313aa7c…            22 lecciones del método
> ```
>
> El identificador es el que devolvió el buzón, no el que calculaste: **son iguales cuando
> todo fue bien, y anotar el suyo es lo que hace que la fila valga como prueba.**

**El buzón deduplica por contenido**, así que mandar dos veces lo mismo no ensucia nada. El
miedo debe estar en mandar de más **contenido**, no de más **veces**.

## 3 · Anonimizar — el skill PROPONE, el dueño APRUEBA

**Ninguna detección automática atrapa todo.** Este paso no es un filtro: es una propuesta
que alguien tiene que mirar.

**Qué busca**, como mínimo:

| | |
|---|---|
| rutas de disco | `/Users/<alguien>/…`, `/home/<alguien>/…`, `C:\Users\…` |
| máquinas y redes | nombres de host, dominios internos, IPs, puertos con su host |
| personas y cuentas | nombres propios, correos, handles, usuarios del sistema — **y los roles que identifican a una sola persona** |
| identificadores | rutas de repositorio, nombres de servicio y contenedor, identificadores de sesión, **y los números de PR, ticket o folio: apuntan a un repositorio o a un canal concretos** |
| secretos | cualquier cosa con forma de llave, token o credencial — **y si aparece uno, se para** |

**Cómo se sustituye:** por un **marcador que conserve el sentido y pierda la identidad** —
`<una casa>`, `<un servidor>`, `<una persona>`. Una lección con todo tachado deja de
enseñar; el objetivo es que **el caso siga siendo reconstruible y el sitio no**.

> [!important] Mejor que tachar: REESCRIBIR en genérico desde el origen
> Tachar sobre el original deja el original debajo — cada nombre es un reemplazo que hay que
> acertar, y basta fallar uno. **Reescribir la lección en genérico** parte de que no hay nada
> que tachar: el texto nace sin los nombres. Sale más limpio y de paso obliga a comprobar que
> la lección **sobrevive sin ellos**, que es exactamente la compuerta del paso 2.
>
> Medido en la primera corrida real: el pase por reemplazos dejó residuos que hubo que cazar
> a mano; el reescrito en genérico salió limpio a la primera. **Reescribir cuesta más y por
> eso hay que decir que es lo correcto**, o nadie lo elige.

> [!important] Se enseña EL TEXTO FINAL, no una lista de reemplazos
> Una lista de *«sustituí A por B»* obliga a reconstruir el resultado en la cabeza, y ahí es
> donde se cuela lo que no se ve. **Se enseña el texto tal como va a salir.**

### Lo que la máquina NO puede juzgar, se PREGUNTA — y son siempre éstas

No son opinables ni se resuelven leyendo el texto, y cada una cambia el resultado:

1. **¿La aportación dice de qué casa viene, o va anónima?** Nombrarse resuelve la ambigüedad
   de procedencia; callarse es consistente con el diseño del buzón. **Y si va anónima, hay
   que quitar el nombre del dominio también de los títulos y encabezados**, donde se cuela.
2. **¿Los nombres de terceros se tachan?** Otras casas, otras personas, otros equipos **no
   dieron su palabra** para aparecer en un corpus público, y varias lecciones los nombran
   cometiendo o corrigiendo errores.
3. **Lo que es público o no según el contexto** — un nombre de proyecto, de cliente, de
   producto. Eso no se deduce del texto.

> [!danger] En `automatico` estas tres NO se adivinan: se declaran o se para
> Son decisiones sobre qué se publica de terceros y de uno mismo, y **ningún valor por
> omisión es seguro** — ni tachar de más, que destruye la lección, ni tachar de menos, que
> publica a quien no dio su palabra. Si el manifiesto no las declara (`learning_procedencia`,
> `learning_terceros`), la corrida **se detiene y las pide**, sea cual sea el modo.
>
> Un modo automático que resuelve solo lo que su autor dijo que no se puede resolver solo no
> es automático: es una suposición con permiso.

**Y se dice en voz alta lo que NO se puede tachar:** un relato detallado puede delatar de
dónde viene por su forma aunque no quede un solo nombre. Quien aprueba tiene que saberlo.

**Cuando la revisión a mano encuentre algo que la detección no vio, se REPORTA.** Es la
prueba viva de por qué este paso lo aprueba una persona.

## 4 · La confirmación, y qué NO cuenta como confirmación

En `preguntar` y `recordar-destino`: se enseña el texto final, el destino y cuántas
aportaciones van. **Sin un sí explícito no sale nada.**

> [!danger] Cada autorización es un acto aparte
> Elegir el destino **no es** aprobar la anonimización, aprobar la anonimización **no es**
> aprobar el envío, y aprobar un envío **no autoriza el siguiente**. Cada una se pide en su
> momento: lo que cruza el borde de salida es irreversible.
>
> **Lo que el modo del dominio cambia es CUÁNDO se dio el permiso, no que exista.** Declarar
> `automatico` es una autorización permanente y consciente, escrita en frío en el manifiesto.
> Lo que sigue prohibido es la autorización que se **hereda sola** — dar por buena la de hoy
> porque ayer dijo que sí, sin que nadie lo haya declarado en ningún sitio.

**Y una pregunta que se hace en TODOS los modos:** si la revisión encontró algo que la
detección no vio, **se dice antes de mandar** aunque el modo sea `automatico`. En ese caso
la corrida se detiene y espera: el modo cubre lo rutinario, no lo que acaba de salir mal.

## 5 · Mandar, y decir qué pasó

```
POST <endpoint>/    ·    el cuerpo es el markdown, tal cual    ·    sin llaves ni registro
```

**No hace falta identidad, y es a propósito** — el buzón acepta a cualquiera porque todo lo
que se le pidiera a quien coopera reduciría cuántos cooperan. **El juicio no está en la
puerta: está después, y es humano.**

**Calcula la huella del cuerpo ANTES de mandarlo.** El identificador que devuelve el buzón
es el hash de lo que guardó: si coincide con el tuyo, tienes prueba de que llegó completo y
sin truncar. Es gratis y es la única verificación real disponible.

Se reporta, sin adornar:

- **qué respondió el servicio** — el identificador de cada aportación y **si era repetida**;
- **cuáles NO entraron y por qué** — cuerpo de más de 1 MB, cuota diaria agotada, servicio
  sin espacio. **Un envío parcial se reporta como parcial**, nunca como hecho;
- **y se actualiza el registro solo con lo que de verdad entró.** Si el registro avanza sobre
  algo que no llegó, esa lección queda perdida sin que nadie lo note.

---

## Lo que este skill NO hace

- **No lee el buzón.** Aportar y consumir son dos roles distintos.
- **No decide si tu lección vale.** Filtra lo que no es del método; **de lo que sí lo es,
  juzga quien recibe**, y su respuesta —si la hay— llega por otra vía.
- **No manda nada que no hayas visto.** Si algo lo impide —no se puede enseñar el texto, no
  hay quién apruebe—, **no manda**: se detiene y lo dice.

> [!warning] Si tu casa OPERA el buzón al que iba a mandar, dilo antes de mandar
> Lo que mandes entra **como anónimo**, y quien lee no puede distinguirlo de una aportación
> externa — así que el corpus registraría como de fuera algo que salió de dentro. **Para las
> casas que ya se conocen, el camino natural es el canal, donde la firma existe.**
>
> No es una prohibición: **es que hoy el buzón no tiene procedencia verificable, y eso es su
> requisito, no su carencia** — sin anonimato no hay volumen. Se dice, decide el dueño, y el
> día que el buzón acepte firma opcional el dilema desaparece solo.
