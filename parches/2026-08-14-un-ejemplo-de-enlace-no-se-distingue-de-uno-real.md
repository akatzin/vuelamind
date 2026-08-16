---
version: 1
origen: anonimo
estado: armonizado al master el 2026-08-16 (la leccion 27 ya describia los enlaces en vez de usarlos; se anadio la advertencia de colgantes legitimos en Fase 3)
---

# Un ejemplo de enlace no se distingue de uno real

## Qué corrige

**Un texto que enseña una sintaxis usándola produce, en todo vault que lo copie, un
defecto que el propio método manda reportar en rojo** — y la culpa no es del vault,
sino del texto que se heredó.

## Cómo se descubrió

**2026-08-14**, primera ejecución del validador de un dominio recién nacido, el
mismo día de su inicialización.

El validador reportó `ROT — Toter Verweis: [[Verweise]]`. El enlace nunca fue un
enlace: la semilla heredada del libro de errores explica, en la lección sobre el
radio del cambio, que lo que delata las notas vecinas son *"los `[[enlaces]]`
salientes"* — y escribe la sintaxis **usándola**, para que se entienda.

Al traducir esa lección al idioma del dominio, el ejemplo viajó tal cual. El
chequeo de enlaces de la Fase 3 §3 no puede distinguir un enlace exhibido de uno
pretendido: **son el mismo texto**.

Lo que lo hace algo del método y no de una casa: el defecto **nace con cada
dominio nuevo**, porque la semilla se copia al `Errores.md` de todos ellos desde el
día uno. Y su primera manifestación es la peor posible — **el primer validador que
alguien corre en su vida sale en rojo por un defecto heredado**, justo en el
momento en que se está decidiendo si esta herramienta merece confianza. Quien no
sepa de dónde viene concluirá que su vault está mal, o que el validador miente; las
dos conclusiones son falsas y las dos enseñan a ignorar el rojo.

Es hermano del ítem 38 del libro de errores —*un lector no describe lo que lee*—
pero al revés: allá el texto que sobra es una paráfrasis; aquí es una **demostración
que el instrumento toma por dato**.

> **Y volvió a ocurrir el mismo día, al documentarlo.** Al escribir la entrada del
> libro de errores propio, el enlace se citó **entre comillas de código** para
> nombrar lo que había fallado — y el chequeo lo reportó otra vez, idéntico. Las
> comillas de código no protegen: el barrido busca el patrón, no el contexto.
>
> Esto no es una anécdota, es **la prueba de que el defecto no depende del
> descuido**: se reprodujo en el acto mismo de corregirlo, por alguien que acababa
> de entenderlo. Un defecto que se comete mientras se explica no se arregla
> avisando; se arregla cambiando la forma de escribir el ejemplo. Y refuerza la
> parte del parche que más se olvidaría: **la corrección no es sólo quitar el
> ejemplo de la lección 27, es no volver a escribirlo en ninguna parte**, ni
> siquiera para citarlo.

## Cómo aplicarlo

Regla general, para cualquier convención que se explique con un ejemplo:

> **No enseñes una sintaxis usándola si algún chequeo va a recorrer ese mismo
> texto.** Nómbrala, descríbela, o escríbela de una forma que la comprobación no
> lea como uso real. Si se exhibe de todos modos, el chequeo necesita saberlo — y
> entonces la excepción se escribe donde vive el chequeo, no en la cabeza de quien
> lo mantiene.

Aplica igual a marcadores de plantilla, a comodines y a cualquier cosa que un
barrido pueda confundir con su propio objeto.

**Dónde toca la plantilla:** Fase 2 §2, lección 27 —sustituir el ejemplo
`` `[[enlaces]]` `` por *"los wikilinks salientes"*, que dice lo mismo sin ser uno—
y una línea en Fase 3 §3, junto al chequeo de enlaces, advirtiendo que un texto
didáctico dentro del vault puede generar colgantes legítimos.

## Cómo verificar

1. **El caso que debe pasar ahora:** correr el chequeo de enlaces sobre un vault
   recién inicializado, con la semilla del libro de errores dentro. Debe salir
   limpio. Antes del parche salía en rojo con un colgante que nadie escribió.
2. **El caso que debe SEGUIR fallando** —y es la mitad que importa—: añadir a
   cualquier nota un enlace a una nota inexistente. El chequeo tiene que seguir
   reportándolo. *(Medido el 2026-08-14: sigue reportándolo. Un chequeo arreglado
   que ya no encuentra nada no se corrigió: se apagó.)*
3. **Deshacer el escenario** y comprobar la reversión con una huella del archivo
   tocado, no con el recuerdo de haberlo revertido.
