---
version: 1
origen: akatzin
---

# 2026-08-16 · El método exige un MOMENTO para presentar lo que no publica solo, y no da dónde cumplirlo

## Qué corrige

**La regla ya existe y es correcta.** Desde el corte 3.0 (`db0bcfa`, *«vuelamind 3.0 — el
canon se muda a git»*, 2026-08-12) el master dice que un dominio puede decidir que toda
publicación pase por el responsable, y que si elige esa política debe definir **en el mismo
acto cuándo** se presentan los borradores pendientes — *«y que ese momento viva en un
comando, no en una intención»*. La diagnosis está escrita entera: *«una decisión delegada
sin momento definido de presentarla no se rechaza — no se toma nunca»*.

**Lo que falta es dónde cumplirla.** Ninguna superficie del método puede expresar ese
momento:

- **El manifiesto no tiene clave para él**, y no es un olvido: su contrato declara que
  *no declara flujo, porque el orden ES el método y no es tropicalizable*.
- **El motor genérico no tiene el paso.** Su cierre escribe el parche, lo reporta una vez
  como *pendiente de proponer* y termina. No hay acto que pida la decisión.
- **El arranque comprueba parches, pero los de entrada** — los que otras instancias
  publicaron y hay que juzgar al llegar. Un borrador propio no es ninguno de ésos.

Así que el dominio que obedece la regla tiene dos salidas, y las dos son malas: **forkear
el motor** —lo que el método desaconseja, porque las copias divergen en silencio— o dejar
el momento como intención, que es exactamente lo que la regla prohíbe. El resultado medido
es un backlog de solo escritura, con la asimetría que
`el-arranque-presenta-una-cola-y-esconde-la-otra` ya documentó para las ideas: **nada falla
cuando nadie decide, y cuanto más disciplinadamente escribe parches un dominio, más se le
acumulan invisibles.**

## Cómo se descubrió

**2026-08-16.** Un dominio cuyo `aportar_a` declara un repositorio cerró un folio, y del
cierre salió un hallazgo del método que se escribió como borrador. El responsable preguntó
lo obvio: *«¿en qué momento se publican? ¿hay un skill para eso? ¿me los propones en el
siguiente arranque?»*

Se midieron los tres instrumentos y las tres respuestas fueron que no: el cierre escribe y
reporta una vez, el arranque solo mira los parches de entrada, y el validador del dominio
solo recorre los **publicados** —lo que aún no se publicó le es invisible por
construcción—.

**El primer borrador de este parche afirmaba que al método le faltaba la regla. Era falso**,
y lo delató releer el master antes de proponer: la regla estaba desde el 3.0, con su caso y
su diagnosis. El hallazgo verdadero apareció al medir la distancia entre esa regla y las
superficies que deberían cumplirla — el manifiesto no puede declararla y el motor no la
ejecuta.

La forma que el responsable dictó al ver la medición: **si el dominio eligió proponer, los
parches pendientes se le presentan al final del cierre para que confirme su publicación.**

## Cómo aplicarlo

**El momento va en el ORDEN, no en el manifiesto.** Es la consecuencia de que el orden sea
el método: si el momento fuera una clave, cada dominio elegiría uno distinto y volveríamos
a que un dominio pueda quedarse sin ninguno. El cierre gana un acto final, **después de
reportar**, gobernado por la clave que ya existe:

| `aportar_a` | Qué hace el cierre al final |
|---|---|
| Un repositorio (con cuenta o sin ella) | **Presenta uno a uno los parches pendientes de proponer** —qué corrige cada uno y qué costaría publicarlo— y **pide confirmación de publicarlos**. Sin cuenta la confirmación sigue teniendo sentido: decide el responsable, y el transporte puede ser otra máquina u otro día |
| `ninguno` | **No presenta nada.** No hay decisión que pedir: el parche se queda en casa por diseño, y preguntarlo cada cierre sería ruido |
| Sin declarar | Se pregunta **una vez** por el destino, como ya manda el método — no se asume ni que sí ni que no |

**Y dos estados, porque en un listado se ven idénticos:**

> **`nunca presentado`** — se re-ofrece en **cada** cierre hasta que haya decisión.
> **`decidido no publicar`** — con su motivo escrito; **no se vuelve a ofrecer**.

Sin esa distinción la presentación degenera en una pregunta repetida, que enseña a
contestar que no sin mirar — peor que no preguntar.

**Toca las dos superficies en el mismo acto:** la fase del master que describe el cierre
—donde la sección del MOMENTO deja de mandar a inventarlo y remite al acto que ya existe—
y el motor que lo ejecuta.

## Cómo verificar

**El caso que fallaba.** Un dominio con `aportar_a` = un repositorio y al menos un parche
sin proponer cierra sesión. El cierre debe **terminar** presentándolo y pidiendo la
confirmación de publicarlo; si el responsable dice que espere, el siguiente cierre vuelve a
presentárselo. Hoy ese cierre termina sin preguntar nada.

**Los que DEBEN seguir fallando:**

- Un dominio con `aportar_a: ninguno` **no** debe recibir la pregunta.
- Un parche marcado `decidido no publicar` **no** debe reaparecer al siguiente cierre. Si
  reaparece, la presentación está leyendo la carpeta en vez del estado.
- **El manifiesto no debe ganar una clave nueva para esto.** Si la solución exige que cada
  dominio declare su momento, el defecto sigue vivo: el dominio que no la declare se queda
  sin momento, que es el caso que este parche cierra.
- El cierre **no** debe publicar al recibir la confirmación del checkpoint: confirmar lo
  escrito y confirmar una publicación son dos actos distintos, y el segundo cruza el borde
  de salida del dominio.
