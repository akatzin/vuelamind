---
description: Escala el dominio actual a la última versión liberada del marco — mayor o menor — preflight que aborta, herencia en bloque, huella verificada. Los parches del día a día NO son de aquí, son del arranque
---

# /vuelamind-upgrade — escalar a la línea base vigente

Sube el dominio actual a la **última versión liberada** de la plantilla, **sea mayor o menor**. Es el ejecutor de los saltos; no el canal del día a día.

**La división del trabajo, para no confundirlos:**

| Ritmo | Quién | Qué hace |
|---|---|---|
| **Diario** | el comando de **retomar** (arranque) | Trae los parches que otras instancias publicaron sobre la versión actual — el chequeo de parches los ofrece uno a uno, y **también trae el aviso** de que existe una mayor nueva, porque ese aviso viaja como parche-anuncio |
| **Al haber razón** | **este comando** | Ejecuta el salto que el aviso anunció |

## Qué hace

1. **Localizar el marco** — por el manifiesto del dominio (clave `marco:`); si no hay manifiesto, por las memorias; si tampoco, preguntar.
2. **Leer la versión del master vivo** y compararla con la copia local del dominio. **Se comparan las versiones enteras, no solo la mayor.**
   - **Misma versión exacta** → no hay nada que escalar: *"estás en la línea base vigente; los parches del día llegan por el arranque"*. Fin.
   - **Hay una versión más nueva, mayor o menor** → sigue.

   > [!danger] Comparar solo la MAYOR deja los saltos menores invisibles
   > Este comando decía *«misma versión mayor → no hay nada que escalar»*, y con eso **un
   > dominio en 3.0 con la 3.6 publicada recibía «estás al día»** — con tres saltos menores
   > esperándolo y sin ninguna señal de que existían.
   >
   > **Medido el 2026-09-07:** las tres últimas versiones del marco —3.4, 3.5 y 3.6— son
   > **todas menores**. La rama que este comando trataba como el caso raro es la única que ha
   > ocurrido en un mes.

3. **Localizar el material del salto**: el documento `UPGRADE_v<N>.md` junto al master. **Sin ese documento no hay salto**: una versión sin upgrader publicado no está liberada, está a medias — repórtalo así.

   > [!important] Un salto MENOR no trae huellas ni matriz, y eso es correcto
   > Una **mayor** corta línea base: reemplaza el master, y por eso pide tres piezas —el
   > documento, sus huellas y su matriz de incorporación—. Una **menor** añade o retira algo
   > sin tocar la línea base, y **solo trae el documento**.
   >
   > **Exigirle las tres a un salto menor lo declara incompleto cuando está bien.** Se
   > comprueba qué tipo de salto es antes de pedir el material, no después.
4. **Ejecutarlo al pie de la letra.** El documento del salto manda: su preflight (que ABORTA con opciones si el dominio no está sano — copia editada a mano, registro inconsistente, validador en rojo, salto anterior a medias), su herencia en bloque con lista visible, el reemplazo con huella verificada, el manifiesto, la migración del cierre, los genéricos desde el canon, y la fila de registro.
5. **Cerrar con el validador del dominio en verde.** Un salto que deja el instrumento gritando no terminó.

## Qué NO hace

- **No aplica parches sueltos** — eso es del arranque, uno a uno, con juicio contra el dominio propio.
- **No crea versiones** — las líneas base se cortan en el master con su matriz, huellas y upgrader; los saltos menores se cortan con su upgrader. Este comando las consume, no las produce.
- **No corre desde fuera del dominio.** Como todo lo que escribe registro y memorias, se ejecuta en una sesión DENTRO del dominio que escala.

## Por qué es un comando y no un documento

El documento del salto (`UPGRADE_v<N>.md`) es **de esa versión**: sella la huella de SU plantilla y muere con el salto. Este comando es **el hábito estable** que los encuentra: dentro de un año, con v4 liberada, la instrucción sigue siendo la misma — *"corre el upgrade"* — sin recordar qué documento toca. Un párrafo se lee cuando alguien se acuerda; un comando está en el camino de todos los días.
