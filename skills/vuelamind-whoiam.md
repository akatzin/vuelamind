---
description: Relata quién es este dominio — la entrevista inicial y sus respuestas, leídas del acta de nacimiento. De solo lectura
---

# /vuelamind-whoiam — quién es este dominio

Relata la **entrevista inicial** del dominio actual y sus respuestas: para qué existe, cómo se llama su asistente, qué piezas tiene, cómo verifica, qué calla, dónde vive todo y cómo opera. Es la carta de identidad — lo que una sesión nueva necesitaría para entender **con quién está hablando y de qué**, antes de tocar nada.

## De dónde lee

Del **acta de la entrevista**: el documento que la Fase 0 del marco deja escrito al nacer el dominio, con las respuestas de los bloques del acta. Su ruta la declara el manifiesto del dominio (clave `acta:`); si el manifiesto no la declara, buscar `vuelamind-entrevista.acta.md` junto al manifiesto, y si tampoco, en el vault.

**Nunca relates de memoria ni desde otras notas sin decirlo**: el acta es la fuente. Las respuestas de una entrevista son decisiones del responsable, no deducciones del asistente.

> [!danger] El panorama NO es el acta — error cometido el 2026-08-12
> Al reconstruir un acta ausente, la tentación es rellenar los bloques del acta con lo que el **panorama** (`0_<Dominio>.md`) y las notas ya dicen. **Eso produce las paráfrasis del asistente, no las palabras del responsable** — y se lee como acta sin serlo. El usuario lo cazó de inmediato: *"No salió del transcript ni son las respuestas que yo emití."*
>
> La regla dura: **agota la fuente #1 (el transcript) antes de tocar la #2.** Si el transcript existe pero está en otra máquina apagada, la respuesta correcta es **pedir encenderla o decir que no se pudo**, NO caer al panorama. Un acta reconstruida de notas documenta lo que el dominio *parece ser* según su propia documentación — que es justo lo que el acta debía verificar contra la fuente, no repetir.
>
> **Y comprueba si hubo entrevista siquiera:** un dominio que nació orgánicamente (sin pasar por la entrevista del marco) NO tiene los bloques de la entrevista que responder. Inventarle la estructura de entrevista es el mismo error con otra cara. Relata lo que el transcript muestre — aunque sea una instrucción de arranque y no un cuestionario.

## Qué presenta

En este orden, que es el de la entrevista:

| Bloque | Qué relata |
|---|---|
| **A · El dominio y su frontera** | Para qué existe, qué queda dentro y qué fuera — y el **nombre del asistente** en este dominio, con la fecha en que se eligió |
| **B · Las entidades** | Las piezas: qué clase de cosas se documentan aquí |
| **C · La verificación** | Cómo se comprueba la verdad en este dominio — el bloque más importante de la entrevista |
| **D · Confidencialidad** | Qué no entra al vault ni al chat, sin listar los secretos mismos |
| **E · Dónde vive todo** | Vault, andamiaje, transporte, réplica |
| **F · Operación** | Ritmo de trabajo, cierres, quién decide qué |

Cerrar con las **enmiendas**, si el acta las tiene: qué respuestas cambiaron después del nacimiento, cuándo y por qué — un acta se enmienda con fecha, nunca se reescribe en silencio.

## Si el acta no existe

**Detente y dilo** — es el hallazgo, no un obstáculo. Ofrece **reconstruirla**, y las fuentes van en este orden:

1. **El transcript de la sesión que corrió la entrevista**, si sobrevive — el historial de sesiones del proyecto del dominio, en la máquina que la corrió. Es la fuente primaria: ahí están **las palabras del responsable**, no la lectura que alguien hizo de ellas. Las respuestas extraídas de ahí se marcan `del transcript original`.
2. **Lo escrito al nacer**: el contexto inicial del dominio y las notas fundacionales del vault — decisiones ya digeridas, segunda mano pero fechada.
3. **Preguntar** solo lo que ni el transcript ni las notas respondan.

La reconstrucción se marca **`reconstruida, no original`** en su frontmatter, con fecha y con la fuente de cada bloque — porque un acta reconstruida de notas documenta lo que el dominio ES hoy, no lo que se decidió al nacer, y esa diferencia no debe borrarse. La que sale del transcript sí recupera la decisión original: dilo.

## Qué NO hace

- **No escribe** (salvo generar el acta si el responsable acepta la reconstrucción).
- **No es el estado del dominio** — para eso está el comando de retomar. Esto es la identidad, que cambia poco; aquello es el estado, que cambia a diario.
