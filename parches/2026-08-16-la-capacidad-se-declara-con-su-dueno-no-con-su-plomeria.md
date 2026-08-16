---
version: 1
origen: akatzin
estado: fusionado al canon el 2026-08-16 · armonizado a la pregunta de acceso de la entrevista el 2026-08-16
---

# 2026-08-16 · La capacidad se declara con su dueño, no con su plomería

## Qué corrige

Cuando la entrevista pregunta *"¿qué acceso tengo?"*, la respuesta natural es el
**mecanismo**: el usuario, el host, la ruta, el comando de transporte, la condición del
agente de llaves. Todo eso es **plomería de otro dominio** — el que hospeda la copia o
el servicio — y anotarla en el acta produce dos daños que no hacen ruido:

1. **Caduca en silencio.** La llave rota, la ruta se muda, el host se renombra — y el
   acta sigue describiendo la plomería de hace meses con tono de vigencia, en una casa
   que ni se entera del cambio porque el cambio ocurre en otra.
2. **Confunde de quién es el pendiente.** Si el acceso falla, un acta llena de
   mecanismo invita a arreglar la plomería desde donde no se posee — cuando lo
   correcto es registrar el fallo y devolverlo a su dueño.

## Cómo se descubrió

En la entrevista fundacional de un dominio que documenta un artefacto compartido entre
varias casas. La pregunta de acceso se contestó con el mecanismo completo — transporte,
condición de llaves, rutas del dominio vecino — y lo cazó el fundador leyendo el acta:
*"la respuesta lleva mucho análisis que es de otro rol; eso a esta casa no le importa"*.
Al separar, quedó claro que la respuesta útil era otra cosa: **una tabla de capacidades
con dueño**, donde cada fila dice si se puede medir, bajo qué condición, y **de quién es
que se pueda**.

De ahí salió también el estado que la plomería escondía: había una copia **ilegible por
diseño** (cifrada para su tránsito), y el acta la habría registrado como acceso roto en
vez de como lo que es — una fila que **solo puede citarse, nunca medirse**, de forma
permanente y sana.

## Cómo aplicarlo

Texto para las reglas del dominio y para la respuesta de acceso en la entrevista:

> **Este dominio documenta qué copias y capacidades existen y si concuerdan — no cómo
> se llega a ellas.** Cada acceso se declara como capacidad con dueño: *puedo medir X,
> condicionado a Y, y que se pueda es responsabilidad de Z*. La plomería —usuarios,
> hosts, rutas, llaves, comandos— vive en el dominio que la posee y se le pide a él.
> Si una copia se vuelve inalcanzable, **no es un defecto de esta casa**: es un
> pendiente del dominio que la hospeda; lo de aquí es registrar *"no pude medir, y por
> qué"* — que dicho así es un **dato completo**, no un hueco.

Con el corolario que evita el parche de pánico: una copia a oscuras **por diseño** no
es una excepción incómoda — es el caso ejemplar de que "solo citable" es un estado de
primera clase, no un acceso pendiente de arreglar.

## Cómo verificar

- **Debe pasar:** el acta responde el acceso con la tabla capacidad · condición · dueño,
  y ninguna fila contiene transporte, rutas ajenas ni estado de llaves.
- **Debe seguir fallando:** un acta que registre comandos de conexión, rutas de otro
  dominio o la condición de un agente de llaves como respuesta de acceso tiene que
  seguir siendo detectable como defecto — era el estado exacto que este parche corrige.
