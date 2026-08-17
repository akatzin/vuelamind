---
version: 1
origen: akatzin
estado: propuesto — transportado por el canal de la watcher el 2026-08-16
---

# 2026-08-16 · Un validador de tres estados necesita que el método defina «pasar»

## Qué corrige

El método pide, en varios sitios, que el validador del dominio CORRA Y PASE — el
preflight de un salto es el caso más duro, porque de eso depende una compuerta
todo-o-nada.

«Pasa» está definido para un instrumento binario: verde o rojo. Pero un dominio maduro
acaba distinguiendo un TERCER estado —NO VERIFICABLE, sin datos, no aplica— porque "no
pude comprobarlo" no es "está bien" ni "está mal", y confundirlos es justo el modo de
fallo que el método combate.

Con tres estados, «corre y pasa» NO DICE NADA: ¿pasa con no-verificables? ¿con cuántos?
Y la ambigüedad muerde en el peor momento, porque un dominio con tres estados suele
tener no-verificables PERMANENTES Y SANOS —una cola que reporta pendientes, un recurso
remoto que a veces no está—. Exigir cero vuelve la compuerta IMPOSIBLE POR CONSTRUCCIÓN:
el requisito sólo se satisface apagando la parte del instrumento que piensa.

## Cómo se descubrió

MEDIDO 2026-08-16, en el segundo salto a v3 del método. El validador del dominio
distingue FALLA de NO VERIFICABLE y salió 0 fallas · 7 no-verificables. El ejecutor NO
SUPO si eso era «pasa», y su propio manifiesto decía lo contrario de lo que parecía: «un
NO VERIFICABLE no es un OK».

Se resolvió preguntando, y la respuesta fue buena — pero EL TEXTO NO LA TRAÍA, y el
salto quedó bloqueado hasta que una persona la dio.

## Qué añade

Definir «pasar» para tres estados, en el propio método:

PASA = cero fallas, y cada no-verificable con dueño declarado, de uno de tres tipos:

| Tipo | Qué es | ¿Bloquea? | ¿Se apaga al final? |
|---|---|---|---|
| (a) Excepción del acto | Su causa es exactamente lo que este acto resuelve | No | SÍ — si sobrevive, el acto no terminó |
| (b) Informativo por diseño | Reporta estado, no comprueba nada (una cola, un inventario) | No | NO — no es un fallo |
| (c) Deuda propia | El instrumento no pudo comprobar algo que debería | SÍ | Sí, con folio |

Y la contraparte que mantiene el rigor: ningún no-verificable NUEVO nacido del acto.

La clasificación SE ESCRIBE, NO SE PIENSA: cada no-verificable se enumera con su tipo
antes de seguir. Y la carga de la prueba es del hallazgo: en la duda entre (a) y (c), es
(c) y bloquea.

## Señal de que falta

Si el validador de un dominio tiene más de dos estados y el método le pide «pasar» sin
decir qué significa, cada ejecución lo decide de nuevo — y lo decide quien tiene prisa
por que pase.
