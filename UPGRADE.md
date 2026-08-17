# El salto de versión — cómo se sube un dominio vivo a la línea base vigente

Los parches del día a día **no pasan por aquí**: llegan por el arranque, uno a uno, y
cada dominio los juzga contra su evidencia. Este documento es para otra cosa — el salto
a una **versión mayor** de la plantilla, que es un acto raro, con ceremonia propia, y que
se ejecuta con `/vuelamind-upgrade` desde dentro del dominio que sube.

> [!important] Son DOS upgrades distintos, y confundirlos cuesta
> **El de MÁQUINA** re-instala el ciclo desde el canon — el paso de huella del acto de
> sumarse, sin ceremonia: la instancia no se re-declara ni repite entrevista.
>
> **El de DOMINIO es adherirse al canon**, y su delta es enumerable y chico: el
> manifiesto gana las claves que le falten (`canon`, `aportar_a`), la semilla del libro
> de errores se refresca a la vigente, entra una fila al registro —*"vN por adhesión al
> canon"*— y las copias locales viejas del master **se archivan con fecha: no se migran,
> no se quedan como trampas**. Lo que NO migra es el contenido: folios, decisiones,
> bitácora y acta **se quedan donde viven**. Un upgrader de contenido solo hace falta si
> la estructura del vault cambió entre líneas base — y eso se mide, no se supone.

## Qué necesita una versión mayor para estar liberada

Junto al master deben existir **tres piezas**: el documento del salto (`UPGRADE_v<N>.md`),
sus huellas (`HUELLAS.md`) y su matriz de incorporación. **Sin ellas, la versión no está
liberada: está a medias**, y el comando de upgrade lo reporta así en vez de improvisar.
Una mayor anunciada sin upgrader publicado le promete a los dominios viejos un camino que
no existe.

## El procedimiento, en orden

1. **Asegura el deshacer ANTES de tocar nada.** La réplica no es deshacer (lección 49):
   toma una copia o snapshot del directorio del dominio en una capa que no obedezca a
   ningún replicador, y comprueba que se puede leer. El primer salto de un dominio es
   exactamente el tipo de accidente para el que esa capa existe.
2. **Abre sesión DENTRO del dominio que sube.** El upgrade escribe registro y memorias,
   y desde fuera aterrizan en el sitio equivocado. No se corre desde otra casa.
3. **Corre `/vuelamind-upgrade`.** Localiza el marco por el manifiesto (o pregunta),
   compara versiones, y localiza el documento del salto. Si la versión ya es la vigente,
   termina ahí — los parches del día no son de este camino.
4. **Deja que el preflight mande.** Aborta —con opciones, no con drama— si el dominio no
   está sano: copia del master editada a mano, registro inconsistente, validador en rojo,
   un salto anterior a medias. **Un preflight que aborta no es un fallo del upgrade: es
   el upgrade midiendo antes de escribir.** Se corrige lo que señale y se vuelve a correr.
5. **Herencia en bloque, con lista visible.** Los parches incorporados a la línea nueva
   se heredan de golpe; el humano aparta los que quiera revisar. Lo ya pospuesto o
   descartado por este dominio **no se pisa en silencio**.
6. **Reemplazo con huella verificada.** La plantilla nueva entra y se comprueba por
   huella recalculada — no por el código de salida del comando de copia. Las copias
   viejas se archivan con fecha.
7. **Cierra con el validador del dominio en VERDE.** Un salto que deja el instrumento
   gritando no terminó. Y la fila del registro — *"vN por adhesión al canon"*, con
   fecha — es lo que permite que el siguiente salto sepa desde dónde parte.

## La primera vez que se corra, va a doler — y eso es parte del plan

El camino v2→v3 **no se ha ejecutado nunca**: la regla está escrita y el caso de
ejecución está declarado pendiente en el propio corpus. Quien lo corra primero lo paga —
y lo que pague son **parches**: cada tropiezo real del salto es exactamente el material
que este método convierte en corrección para el siguiente. Córrelo con calma, con el
deshacer del paso 1 comprobado, y escribe lo que duela.

## Estado de los saltos

| Salto | Documento | Estado |
|---|---|---|
| v2 → v3 | `UPGRADE_v3.md` | **Pendiente de publicación** — el material existe fuera del repo y está en camino. Hasta que esté junto al master, v3 está liberada para nacer, no para saltar |
