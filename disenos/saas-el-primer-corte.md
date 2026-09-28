# El SaaS: un contenedor por persona, y qué pasa con la soberanía

**Estado: decidido el eje, sin construir. La decisión es de Akatzin, 2026-09-28.**

## La decisión, primero, porque todo lo demás se deriva de ella

> **En el SaaS, la soberanía del vault se SUPERSEDE. De momento.**
> El contenedor es nuestro y el vault vive en él. El paso al **híbrido** —el vault montado
> desde el almacenamiento del cliente— queda declarado como destino, no como intención.

Esto **enmienda para el modo gestionado** la doctrina de que el vault es local y el control no
se cede. No la borra: la instalación por cuenta propia sigue siendo la que es, y sigue siendo
la respuesta cuando alguien quiere soberanía de verdad.

**Por qué se puede decir esto sin faltar a lo que vuelamind promete:** porque la salida ya está
construida. El exportador empaqueta **el agente entero** —su carpeta y su memoria— en un `.vma`
cifrado, a disco y sin topes. *La soberanía deja de ser dónde vive el vault y pasa a ser si te
lo puedes llevar entero cuando quieras.* Eso último sí se sostiene, y es comprobable.

**Lo que obliga a prometer en voz alta**, porque sin esto la enmienda es solo una retirada:

- **cifrado en reposo**, y decir con qué llave y quién la tiene;
- **quién puede leer** un vault de cliente desde dentro de la casa, y que quede registrado;
- **exportación y borrado a petición**, sin trámite — el `.vma` ya lo hace, hay que declararlo;
- y que el borrado **sea borrado**, no un archivado silencioso.

**El disparador del híbrido, escrito ANTES de necesitarlo** — porque un «algún día» sin gatillo
no llega nunca, y esta casa ya lo tiene medido en otras piezas:

> **El primer cliente que no firme porque el vault es nuestro.** Ése es el día. No «cuando
> haya tiempo», no «cuando el producto madure»: cuando un área de seguridad lo rechace por
> escrito, que es exactamente el escenario que [[Pendientes]] #26 anticipó sin que hubiera
> ocurrido todavía.

## Lo que un contenedor por persona resuelve, y lo que no

**Resuelve el aislamiento entre clientes**, que es la forma correcta del problema. Pero hay que
decir qué NO resuelve, porque es lo que va a morder:

> **El puente no tiene puerta.** Escucha en loopback, **sin token**, con allowlist de Host y
> chequeo de Origin. Todo su modelo de seguridad asume **un único humano de confianza en la
> máquina**. En un SaaS esa premisa no existe.

Un contenedor por persona **contiene** el permiso, no lo arregla. `BRIDGE_PERMISSION: full` es
ejecución arbitraria: en infraestructura nuestra, eso es una consola por cliente dentro de
nuestra red. De ahí salen tres reglas duras:

1. **`full` no existe en el SaaS.** El techo es `tools`, y se declara — el puente ya se niega a
   arrancar sin nivel, así que la mecánica está.
2. **Salida de red cerrada por omisión**, con lista blanca de lo que el agente necesita.
3. **Servidor de metadatos bloqueado.** Sin esto, el primer cliente curioso saca credenciales
   del proyecto entero.

## Nube: GCP, y no por ser mejor

**La inferencia ya vive ahí.** El contenedor trae `vertex.env` y el puente tiene medido el
estrechamiento de Model Garden. Partir inferencia y alojamiento en dos proveedores duplica
identidad, facturación y superficie de auditoría sin comprar nada.

Y **IAP** tapa justo el agujero de arriba: pone delante del puente la puerta que el puente no
tiene, sin tocar su código.

## Forma del cómputo, para el número de clientes que hay hoy

**Compute Engine con Docker, un contenedor por persona.**

- **No Cloud Run**: el puente es un proceso largo, con estado y disco de escritura, y los
  turnos van en streaming. Pelea con el modelo de ejecución.
- **No GKE todavía**: es peso operativo para cero clientes. Cuando la cuenta de contenedores
  duela de verdad, se migra — y para entonces se sabrá qué duele.

**Y un detalle medido que en local es molestia y en SaaS es caída de cliente:** PID 1 del
contenedor es el propio puente y el `compose.yml` **no declara `restart:`**. Si el proceso
muere, se queda muerto. MEDIDO el 2026-09-28.

## Lo que hay que construir que hoy no existe

| Pieza | Por qué no se puede posponer |
|---|---|
| Puerta de autenticación delante del puente | Sin ella no hay SaaS, hay un puerto abierto |
| **Medidor de turnos por inquilino** | Sin medidor, cada cliente gasta de nuestra cuenta sin tope. El parche `consumir-por-referencia-obliga-a-un-medidor-recurrente` ya lo dice: nacer no lo trae |
| Ciclo de vida del contenedor | Arranque, reinicio, respaldo del vault, y borrado que borre |
| Registro de accesos del operador | Prometer «quién puede leer» sin registrarlo no es una promesa |

## Lo que este documento NO decide

- El precio, ni el modelo de cobro.
- Si los turnos corren contra nuestro Vertex o contra la cuenta del cliente — es la otra mitad
  de la pregunta del medidor.
- El orden respecto de la ruta: en el documento votado 4/4, **SAAS cuelga de COL3**. Arrancarlo
  antes es un cambio de orden sobre un acuerdo de cuatro casas, y esa es palabra de Akatzin.
