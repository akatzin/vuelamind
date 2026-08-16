---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-16 · La entrevista no pregunta como quién actúas hacia afuera

## Qué corrige

La entrevista de inicialización pregunta **qué alcanzas** (accesos) y **qué requiere
palabra** (permisos), pero nunca la tercera: **¿con qué identidad actúas cuando tocas
algo fuera de casa?** Son tres ejes distintos y el que falta es el más caro, porque no
es una comodidad — es **delegación de identidad**: un asistente que publica, escribe o
administra hacia afuera lo hace *firmando como alguien*, y hoy esa delegación se hereda
por accidente en vez de concederse a propósito.

El mecanismo del accidente: la identidad viaja pegada a los artefactos. Un clon cuyo
remoto puede publicar, una llave cargada en un agente, una sesión autenticada — quien
trabaja sobre ellos **hereda la firma de su dueño** por el solo hecho de que el
artefacto existe en su árbol. Nadie lo decidió, así que nadie lo revisa.

## Cómo se descubrió

Al fundar un dominio cuyo trabajo es cuidar un repositorio público. La entrevista cubrió
accesos y permisos completos, y solo una pregunta al margen del fundador —*"¿en qué
momento me debería preguntar si se conecta a mi repo?"*— destapó que la instancia había
heredado, sin concesión explícita, la capacidad de **publicar firmando como el dueño**:
el clon estaba ahí, el remoto podía empujar, y ninguna pregunta lo había puesto sobre la
mesa.

Al medir salió el daño ya hecho por la misma ausencia: **más de la mitad de la historia
pública del repositorio** llevaba como autor una identidad de máquina interna que nadie
decidió publicar. El contenido se había anonimizado con cuidado; el recipiente confesaba
en cada commit. Y el patrón generaliza fuera de git: en otro dominio, el asistente
alcanzaba un servidor **como administrador** porque un agente de llaves estaba cargado —
capacidad real, jamás concedida en ninguna entrevista.

## Cómo aplicarlo

En la entrevista (bloque de verificación o de operación), añadir la pregunta con sus
tres partes:

> **¿Como quién actúo hacia afuera?** Por cada superficie externa que este dominio
> toque (un repositorio, un servidor, un servicio): **(1)** qué identidad firma los
> actos que salen, **(2)** quién la concedió y dónde quedó escrito, **(3)** qué actos
> puede preparar la instancia sin esa identidad. Preparar y publicar son actos
> distintos: la respuesta fuerte es estructural — que la copia de trabajo diaria **no
> pueda** firmar hacia afuera, y la que sí pueda se toque solo con palabra del dueño.

Y la regla para el acta: **una identidad de escritura no se hereda por omisión.** Si un
artefacto con firma delegada vive en el árbol del dominio, se declara con dueño y
condición, o se sustituye por su versión de solo lectura.

## Cómo verificar

- **Debe pasar:** el acta de un dominio nuevo con superficies externas contiene al menos
  una fila de identidad — quién firma, quién lo concedió, qué se prepara sin firma.
- **Debe seguir fallando:** una entrevista que registre accesos y permisos completos
  pero ninguna identidad hacia afuera se marca **incompleta** — ese era exactamente el
  estado que este parche corrige, y un acta así tiene que seguir siendo detectable, no
  volverse normal.
