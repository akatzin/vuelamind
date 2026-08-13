---
description: Presenta los comandos del marco que existen en ESTA máquina, generados del disco — qué hace cada uno y cuándo se usa. De solo lectura
---

# /vuelamind-help — los comandos del marco, tal como están hoy

Presenta **la familia `vuelamind-*` que de verdad existe en esta máquina**, con qué hace cada uno y cuándo conviene usarlo.

> [!important] Se genera al vuelo. Aquí no hay lista.
> Este comando **no enumera los comandos**: los **lee del disco** cada vez. Una lista escrita aquí sería una segunda copia que nadie compara — envejecería en silencio mientras el comando sigue funcionando, que es el ítem 38 del libro de errores.
>
> Consecuencia deliberada: si mañana nace un comando nuevo del marco, **aparece aquí sin que nadie toque este archivo**. Y si uno se retira, desaparece solo.

## Cómo se arma

1. **Lista los comandos de la familia** en el nivel personal: los `vuelamind-*.md` de la carpeta de comandos del usuario. Ésos son los del método.
2. **Lee de cada uno su `description`** del frontmatter y su primer párrafo. Eso es lo que dice de sí mismo — no lo parafrasees más de lo necesario para que quepa.
3. **Mira también el nivel del proyecto**: si el dominio tiene comandos propios, se mencionan aparte y en una línea. No son del marco, pero quien pregunta *"¿qué puedo hacer aquí?"* los necesita igual.
4. Si un comando existe en los dos niveles, **dilo**: el personal ensombrece al del proyecto, y esa es una fuente de confusión real.

## Cómo se presenta

**No un volcado alfabético.** Agrupado por el momento en que se usan, que es como la persona los va a necesitar:

| Momento | Qué se busca ahí |
|---|---|
| **Al abrir sesión** | El que pone al día: lee el arranque del dominio, mide su estado y dice por dónde seguir |
| **Durante el trabajo** | Los de consulta — el estado de la cola, quién es este dominio, qué es el marco, el censo de comandos |
| **Al cerrar** | El de reconciliación: mide, confirma, escribe, verifica |
| **De vez en cuando** | Nacer un dominio nuevo, escalar de versión |
| **Cuando algo sale mal** | Los de rescate |

Para cada uno: **el nombre exacto que se teclea**, una línea de qué hace, y —si aporta— *cuándo* conviene. Nada de opciones ni banderas: eso vive en cada comando.

**Cierra con lo mínimo que hay que recordar.** Si alguien solo se va a quedar con dos, que sean el de abrir y el de cerrar: el resto se descubre solo.

## Cuándo se ofrece

- Cuando el usuario lo pide.
- **Al final del arranque de sesión**, como sugerencia de una línea — sobre todo si el dominio es joven o si la persona lleva poco tiempo usándolo.
- Cuando alguien pregunta *"¿qué puedo hacer?"*, *"¿qué comandos hay?"* o se nota que está buscando la forma de pedir algo.

## Qué NO hace

- **No los ejecuta.** Presenta y se detiene.
- **No inventa comandos que no estén en disco.** Si el usuario esperaba uno que no aparece, eso es el hallazgo: o no está instalado en esta máquina, o se llama distinto. Decirlo.
- **No repite la documentación de cada comando.** Una línea por cada uno; quien quiera el detalle, abre el comando.

> [!note] Si no hay ninguno
> Puede pasar en una máquina donde el marco no se instaló, o donde la carpeta personal no se replica. **Dilo tal cual** y señala de dónde se instalan —el canon del método—, en vez de listar de memoria comandos que aquí no existen.
