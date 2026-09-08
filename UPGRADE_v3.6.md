---
title: Salto menor a v3.6 — la entrevista de 25 preguntas pasa a 15
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — REQUIERE los artefactos de la v3.5
---

> [!danger] De dónde tienes que venir: REQUIERE la v3.5
> **El master que trae este salto nombra `/vuelamind-learn`**, que es el artefacto que
> instala la v3.5. Si saltas desde más atrás, quedas con un documento que **promete una pieza
> que no tienes** — haz antes la v3.5.
>
> *El mapa completo de saltos vive en `UPGRADE.md`, que no muere con ninguna versión.*

# UPGRADE a v3.6 — la entrevista adelgaza y gana un punto de control

> [!important] SI TU DOMINIO YA NACIÓ, ESTE SALTO NO TE CAMBIA NADA
> **Solo toca la Fase 0: el acto de nacer.** Tu acta ya está escrita, tu manifiesto declara
> lo que declara, y todo sigue igual. **Si no vas a hacer nacer a nadie, no saltes.**
>
> Lo que ganas saltando es para la próxima persona a la que le instales esto.

## Qué cambia

**La entrevista pasa de 25 preguntas a 15** (16 si el asistente toca sistemas reales).

| Bloque | Antes | Ahora | Qué pasó |
|---|---|---|---|
| A · Alcance | 4 | **4** | intacto |
| B · Entidades | 3 | **3** | intacto |
| C · Verificación | 4 | **4** | intacto |
| D · Confidencialidad | 3 | **1 + 1 condicional** | la 13 y la 14 se fusionan y solo se preguntan si hay acceso a sistemas reales |
| E · Dónde vive todo | 7 | **0** | lo resuelve el marco |
| F · Operación | 4 | **3 + cierre** | deja de recoger un ritmo y pasa a ser **punto de control** |

## Las tres cosas de fondo

**1 · El bloque E desaparece porque no era del usuario.** Sus siete preguntas eran el 28% de
la entrevista y la mayor concentración de fricción medida, y lo que producían era estructura
para el motor: rutas, carpetas, convenciones de nombres. **Preguntar dónde poner una carpeta
es pedirle al usuario que resuelva un problema del marco.**

Ahora lo trae el método:

| Qué | Convención |
|---|---|
| El vault del conocimiento | **`<proyecto>/vault/`** |
| El andamiaje del asistente | **`<proyecto>/.claude/`** |
| De dónde se trae el método | el canon oficial |
| Qué se comparte entre dominios | **nada: los vaults son personales, siempre** |
| Proponer lo aprendido | **apagado**; lo enciende `/vuelamind-learn` |

> [!important] La convención es por omisión y NO rompe nada
> `vault` sigue existiendo en el manifiesto y **declararla gana**. Los dominios que nacieron
> antes siguen exactamente donde están: ninguno se mueve, ninguno se rompe. Lo único que
> cambia es que **el que nace hoy no tiene que elegirlo**.

**2 · D pregunta lo que importa en un dominio personal.** El inventario ahora nombra
explícitamente **lo que se dice de otras personas** — nombres de compañeros en incidentes,
temas de personal— junto a credenciales y datos bajo confidencialidad. Y la 13, la de dónde
vive lo sensible y qué comandos lo exponen, **solo se pregunta si el asistente toca sistemas
reales**, que es la dependencia que la pregunta 10 ya declaraba sin usar.

**3 · F deja de recoger una respuesta y pasa a comprobar algo.** Su pregunta central se
**propone** en vez de preguntarse —igual que el nombre en la 4— y lo que se registra es **cómo
reacciona el usuario**: si corrige, si lo hace suyo, o si lo acepta tal cual sin tocarlo. Esa
última se anota **como señal débil**, no como un sí.

Y el bloque termina con un cierre en voz alta que va **después** de tomar el dato, nunca
antes: es la parte persuasiva, y persuadir a alguien de que va a usar algo a diario es lo
contrario de medir si lo va a usar.

## Cómo saltar

**Un solo paso, y es traer el master.**

1. **Trae `MARCO_Inicial.md` del canon y comprueba que dice `version: 3.6`.** Si tu copia
   está modificada, respáldala antes.

**Nada más.** No hay skills que reinstalar —ninguno cambió—, no hay claves nuevas que
declarar, y tu manifiesto sigue siendo válido tal como está.

**Cómo sabes que funcionó:** tu copia del master tiene un `### Bloque F — El punto de control`
y **no tiene** `### Bloque E — Dónde vive todo`.

## De dónde salió esto

De cruzar **las actas reales de cinco dominios ajenos** con lo que el canon dice que cada
bloque busca. Lo que apareció, medido:

- **D era el bloque más delgado en las cinco** —la mitad de contenido que cualquier otro— y
  **dos de ellas fusionaron sus tres preguntas por su cuenta**.
- La pregunta *«qué se comparte entre dominios»* **la contestó 1 de 5**; su hermana concreta
  *«¿quién más lo lee?»* la contestaron 5 de 5. **La formulación abstracta se salta.**
- **Ninguna acta nombró a personas en el inventario de confidencialidad salvo una**, y esa lo
  hizo reformulando la pregunta por su cuenta.

> [!note] Lo que este salto NO puede prometerte
> Que la entrevista corta funcione mejor es **inferido**: sale de cruzar cinco actas, y cinco
> es una señal, no una prueba. **La corrida que lo ascendería es la próxima que hagas.** Si al
> usarla algo se atora, eso es un hueco de este documento y se aporta con `/vuelamind-learn`.
