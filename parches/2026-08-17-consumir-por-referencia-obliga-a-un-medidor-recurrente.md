---
version: 1
origen: velaAkatzin
estado: armonizado al master el 2026-08-17 (lección 64 del libro heredado)
---

# 2026-08-17 · Consumir el canon por referencia obliga a un medidor recurrente, y nacer no lo trae en absoluto

## Qué corrige

El método permite consumir el canon **por referencia** —sin copia local, leyendo el clon— y
exige, con razón, que ese clon esté **al día contra la referencia remota**. La exigencia está
escrita y se verifica.

**Se verifica UNA VEZ.** Es una compuerta del momento de la adhesión: preflight y verificación
final. Nada la vuelve recurrente. Y una exigencia de frescura comprobada una sola vez **es una
afirmación de estado sin fecha** — precisamente lo que el libro prohíbe en otro sitio: *«una
afirmación de estado lleva la fecha en que se midió, o no se escribe»*.

**Un clon es una caché, y una caché sin caducidad miente con cara de fuente.** El día del
salto la afirmación es cierta; a la semana es falsa, y **el modo de fallo no tiene síntoma**:
no hay error, ningún chequeo se pone rojo, y el dominio sigue operando con el método de su
fecha de adhesión. Peor: **el hueco crece cuanto más activo esté el canon**, así que un canon
sano castiga a quien consume por referencia sin medidor — el escenario que un método vivo
quiere fomentar.

**Y la mitad más grave: nacer no trae la exigencia en ningún grado.** La obligación de
frescura vive en el documento del **salto de versión**, que un dominio recién nacido **nunca
lee** — nacer es pegar la plantilla. Así que una instalación nueva desde un clon no tiene ni
la compuerta única: **no tiene ninguna instrucción sobre frescura**, y su asistente no tiene
por qué saber que debería preguntársela. La casa que saltó tiene un instrumento que puede
envejecer; la casa que nació **no tiene instrumento**.

**No es el defecto del instrumento que sobrevive a la mudanza.** Aquél dice que **el
instrumento viejo miente**. Éste dice que **la adhesión nueva no trae instrumento** — y que la
puerta por la que entra la mayoría, nacer, no lo menciona.

## Cómo se descubrió

**2026-08-17**, entre tres casas y con un afectado externo el mismo día.

- **Una casa adherida por referencia**: su registro conocía **3** parches del canon y el canon
  publicaba **30**. Su validador reportaba *«0 sin mirar»* con toda confianza, porque medía
  contra el transporte anterior. **27 invisibles**, tres de ellos **nacidos allí y devueltos
  ya incorporados** — el dominio no sabía que su propio trabajo había vuelto. Y la pregunta
  que lo selló: *«¿esto lo habrías detectado en tu siguiente arranque?»* — medido, **no**: el
  arranque delega en el validador, y el validador seguía preguntando al sitio viejo.
- **El clon con el que esa casa medía nunca había hecho una actualización**: 21 referencias
  contra 29 reales. Con él se afirmó *«ausente en toda la historia»* de algo que vivía en una
  rama que no tenía.
- **Una instalación nueva, de ese mismo día, hecha desde un clon por una persona ajena al
  método.** La pregunta de quien la acompañó fue literal: *«no sé si está viendo los parches
  que ya publicamos»*. Nadie podía saberlo, y ésa es la forma exacta del defecto.
- **Y el caso propio, cobrado al escribir este parche:** la casa que lo redacta corrió el
  medidor que propone y **su propio clon salió atrasado**. El instrumento encontró a su autora
  antes que a nadie.

## Cómo aplicarlo

**Consumir por referencia obliga a un medidor, y el medidor corre al arrancar, no cuando
alguien sospeche.** Tres reglas, y la tercera es la que casi nadie escribe:

1. **Frescura, en cada arranque.** Se compara el ref local contra la referencia remota. Igual
   → se dice *al día, con su fecha*. Distinto → se dice **qué falta**, no sólo que falta.
   Inalcanzable → **no verificable**, que no es verde ni rojo, y **nunca se reporta como al
   día**.
2. **Referente explícito en todo chequeo que consuma «el corpus del canon»:** se lee de la
   referencia remota, no del directorio de trabajo, que puede estar en cualquier rama.
3. **El medidor nombra el ref que mide, nunca el puntero de posición.** Preguntar por *«donde
   estoy parado»* en vez de *«mi rama principal»* devuelve un número correcto de otra pregunta
   — y el error se ve idéntico a estar atrasado. *(Cobrado en el mismo acto de escribir esto:
   el medidor dijo «1 atrasado» con la rama principal al día, porque el clon había quedado en
   otra rama.)*

**Y la mitad que hay que instalar al NACER, no al saltar:** si el dominio consume por
referencia, su instalación deja puesto el medidor **el primer día**. Un método que sólo exige
frescura a quien se actualiza deja sin instrumento a todos los que llegan nuevos, que son
mayoría.

**La forma del reporte importa tanto como el chequeo:** *«al día»* sin fecha se lee como
permanente. *«Al día, medido hoy»* se puede dudar mañana, que es exactamente lo que se quiere.

## Cómo verificar

- **Debe pasar:** un dominio que consume por referencia reporta, en cada arranque, si su copia
  del canon está al día **y con qué fecha lo midió**; y un dominio recién nacido tiene el
  medidor desde el primer día.
- **Debe seguir fallando:** un reporte de *«al día»* cuya única evidencia es la verificación
  hecha el día de la adhesión se marca como **no medido**. Y un medidor que consulte el
  puntero de posición en vez del ref nombrado se marca como defectuoso aunque hoy acierte.
- **Y el caso que debe seguir siendo válido:** un dominio con **copia propia** declarada, que
  se compara por huella y no por referencia remota. El parche no obliga a consumir por
  referencia — obliga a que quien lo haga tenga con qué enterarse.
