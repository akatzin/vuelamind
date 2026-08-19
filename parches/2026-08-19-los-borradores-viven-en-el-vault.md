---
version: 1
origen: velaAkatzin
estado: armonizado al master el 2026-08-19 (cuarta regla de la topología + el taller en el diagrama del vault)
---

# 2026-08-19 · Los borradores viven en el vault — un borrador fuera del grafo es invisible para todo censo

## Qué corrige

El método dice dónde vive el conocimiento (el vault, con su grafo de enlaces) y dónde el
andamiaje (scripts, comandos, memoria). **No dice dónde viven los borradores** — el
material a medio hacer: el diseño de un feature en progreso, la idea que aún no es folio,
el documento que se está gestando. Y lo que no tiene lugar asignado aterriza donde caiga:
típicamente en una carpeta del proyecto, **fuera del vault**.

Esa colocación parece inocente y tiene un costo estructural: **todo lo que el método sabe
hacer con el conocimiento depende del grafo** — el radio del cambio se descubre por
enlaces, las búsquedas parten de los nodos, los censos cuentan lo enlazado, el validador
comprueba lo que resuelve. Un borrador fuera del vault queda fuera de todo eso a la vez:
no es wikilink-able, ningún nodo puede citarlo como cita a sus vecinas, ningún barrido lo
pisa, y el editor de notas ni siquiera lo muestra. **Es el material más vivo del dominio
guardado en el único lugar donde el método no mira.**

La firma del fallo es silenciosa y cruel: el contenido existe, está bien escrito y está
fresco — y una búsqueda hecha exactamente como el método manda (ir al nodo del tema)
devuelve un resultado incompleto sin ninguna señal de que falta algo. Los conteos
cuadran, los enlaces resuelven, el validador sale verde.

**La regla:** los borradores viven **EN el vault** — existen por algo (una idea para
crecer, un feature en progreso, el cuerpo de una propuesta) y deben ser **100%
referenciables y estar referenciados**: cada borrador con fila en un índice propio del
taller (`borradores/0_Borradores.md` o equivalente), y las piezas vivas citadas además
desde su nota dueña (el folio que las espera, el track que las junta). Un borrador que no
se puede clasificar es hallazgo — le falta dueño —, no estorbo.

## Cómo se descubrió

En un dominio con vault y carpeta de borradores separados, el responsable capturó en un
pizarrón el modelo de diseño más importante del track de crecimiento. La sesión lo
escribió — completo y bien — en un documento de la carpeta de borradores, fuera del
vault, y siguió con su día. El nodo del track no ganó el enlace, porque los borradores no
eran enlazables.

Días después el responsable pidió «revisa los objetivos del track». El asistente hizo lo
que el método manda: fue al nodo del track (que se declara a sí mismo como «el nodo que
junta todo lo del track») y lo leyó entero. **El modelo del pizarrón no estaba ni
enlazado.** Los barridos de respaldo tampoco lo encontraron, porque buscaron con el
vocabulario del track y el documento hablaba el vocabulario del modelo. Hubo que esperar
a que el humano — la memoria que el método existe para no necesitar — dijera las palabras
clave exactas para que un grep lo hallara. La sesión presentó mientras tanto un diagrama
viejo como si fuera el modelo vigente.

La autopsia mostró que no era un descuido puntual: **la carpeta entera** (50 archivos:
diseños, guiones, cuerpos de propuestas) vivía fuera del grafo, y un censo arrojó que
solo 7 de 50 tenían alguna referencia desde el vault. El responsable dictó la regla en
una frase: *los borradores están por algo — deben ser 100% referenciables y estar
referenciados.*

## Cómo aplicarlo

1. **Al nacer un dominio:** el vault incluye `borradores/` desde el día uno (ya está en
   el diagrama de topología del master), con su índice `0_Borradores.md`: la regla, y una
   tabla — borrador · qué es · nota dueña.
2. **Al crear un borrador:** fila en el índice **en el mismo acto**, y cita desde su nota
   dueña (el folio, el track, la decisión que lo espera). Los binarios (diagramas,
   capturas) se citan por ruta en código, no por wikilink, si el validador solo resuelve
   notas.
3. **Al fusionarse o superarse un borrador:** su fila lo declara (fusionado en X /
   superado por Y) — no se borra, porque el original es evidencia de qué se propuso.
4. **Para un dominio ya nacido con borradores afuera:** moverlos al vault en un solo
   acto, censar referencias (un grep por nombre de archivo sobre el vault), crear el
   índice con fila para el 100%, y re-correr el validador — los wikilinks nuevos pueden
   colgar.
5. **El chequeo del validador** (barato y recomendado): ningún archivo en `borradores/`
   sin mención en el índice.

## Cómo verificar

Elegir el borrador más importante del dominio — el diseño del que más depende lo que
sigue — y, sin usar la memoria de la sesión, intentar llegar a él **navegando desde el
nodo raíz del vault** en tres saltos o menos. Si no se llega, la regla no está aplicada.
Después el censo: por cada archivo en `borradores/`, un grep de su nombre sobre el vault
debe devolver al menos una mención fuera de la propia carpeta. Cero huérfanos, o cada
huérfano convertido en hallazgo con dueño.
