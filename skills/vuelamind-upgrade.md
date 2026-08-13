---
description: Escala el dominio actual a la última versión MAYOR liberada del marco — preflight que aborta, herencia en bloque, huella verificada. Los parches del día a día NO son de aquí, son del arranque
---

# /vuelamind-upgrade — escalar a la línea base vigente

Sube el dominio actual a la **última versión mayor liberada** de la plantilla. Es el ejecutor de los saltos; no el canal del día a día.

**La división del trabajo, para no confundirlos:**

| Ritmo | Quién | Qué hace |
|---|---|---|
| **Diario** | el comando de **retomar** (arranque) | Trae los parches que otras instancias publicaron sobre la versión actual — el chequeo de parches los ofrece uno a uno, y **también trae el aviso** de que existe una mayor nueva, porque ese aviso viaja como parche-anuncio |
| **Al haber razón** | **este comando** | Ejecuta el salto que el aviso anunció |

## Qué hace

1. **Localizar el marco** — por el manifiesto del dominio (clave `marco:`); si no hay manifiesto, por las memorias; si tampoco, preguntar.
2. **Leer la versión del master vivo** y compararla con la copia local del dominio.
   - Misma versión mayor → **no hay nada que escalar**: "estás en la línea base vigente; los parches del día llegan por el arranque". Fin.
   - Mayor nueva liberada → sigue.
3. **Localizar el material del salto**: el documento `UPGRADE_v<N>.md` junto al master, con su `HUELLAS.md` y su matriz de incorporación. **Sin ese documento no hay salto**: una versión mayor sin upgrader publicado no está liberada, está a medias — repórtalo así.
4. **Ejecutarlo al pie de la letra.** El documento del salto manda: su preflight (que ABORTA con opciones si el dominio no está sano — copia editada a mano, registro inconsistente, validador en rojo, salto anterior a medias), su herencia en bloque con lista visible, el reemplazo con huella verificada, el manifiesto, la migración del cierre, los genéricos desde el canon, y la fila de registro.
5. **Cerrar con el validador del dominio en verde.** Un salto que deja el instrumento gritando no terminó.

## Qué NO hace

- **No aplica parches sueltos** — eso es del arranque, uno a uno, con juicio contra el dominio propio.
- **No crea la versión mayor** — las líneas base se cortan en el master con su matriz, huellas y upgrader; este comando las consume.
- **No corre desde fuera del dominio.** Como todo lo que escribe registro y memorias, se ejecuta en una sesión DENTRO del dominio que escala.

## Por qué es un comando y no un documento

El documento del salto (`UPGRADE_v<N>.md`) es **de esa versión**: sella la huella de SU plantilla y muere con el salto. Este comando es **el hábito estable** que los encuentra: dentro de un año, con v4 liberada, la instrucción sigue siendo la misma — *"corre el upgrade"* — sin recordar qué documento toca. Un párrafo se lee cuando alguien se acuerda; un comando está en el camino de todos los días.
