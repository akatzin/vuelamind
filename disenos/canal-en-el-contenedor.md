# El canal horneado en el contenedor

**Estado: diseñado, sin construir.**

## Qué es

Que la imagen traiga el canal listo, con sus **dos piezas**: la base de datos y el portal de
visualización. Hoy el contenedor trae el marco y el puente; el canal se monta aparte.

## Lo que hay que dejar preparado

**Un endpoint configurable.** La base puede no ser la del contenedor: una casa puede
apuntar a un servicio compartido. Se declara, no se asume — y **sin declararlo se usa la
local**, que es el caso normal.

**Y el verbo `propuesta` recibiendo archivos.** Los tres tipos ya están decididos
—`mensaje`, `acuse`, `propuesta`— y el veredicto viaja como `acuse`. Lo que falta es que
`propuesta` pueda llevar adjunto.

## Lo que NO cambia, y está decidido

**El canal no conoce los roles y no debe conocerlos.** Si el servidor hiciera cumplir quién
puede aportar, se volvería autoridad sobre el contenido. `trust_signers` dice quién puede
hablar; quién puede aportar lo dice la lista del master, dentro del master.

## Depende de

`#117` — sin el actualizador, poner al día el canon del contenedor es a mano.
