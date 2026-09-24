# Importar un agente

**Estado: hay rama vieja y obsoleta; se rehace.**

## Qué es

La vuelta del exportador: subir un paquete y que el dominio quede operando en esta máquina.

## Dos pasos, y el primero no escribe

El paquete trae `.claude/` dentro, y eso **no son datos: es configuración que el arnés
ejecuta** — en una casa medida, su `settings.json` no contenía otra cosa que ganchos.
Importar el agente de otra persona es ejecutar lo que esa persona escribió.

Así que se **revisa y se enseña** —los ganchos textuales y los comandos propios, uno a uno—
y solo después se escribe, con tu sí.

## Lo que se rechaza sin preguntar

Rutas absolutas, rutas con `..`, enlaces simbólicos, más de una carpeta raíz, y un paquete
de **formato más nuevo** del que este puente entiende. Preguntar ahí sería ofrecer una
opción mala.

Un paquete **sin sello** sí entra —hacerlo a mano es legítimo— pero se dice, porque de ése
no se conoce la forma.

## Lo que hay que rehacer de la rama vieja

Tiene un **tope de 64 MB inventado**, no sabe de `_vault/`, ni del formato 2, ni del `.vma`
cifrado. Nació antes que todo eso.

## Y lo que no puede faltar

**La memoria se traduce, no se copia**: su carpeta se llama según la ruta absoluta del
proyecto, así que en la máquina destino es otra. Es la única pieza del paquete que no se
puede poner tal cual, y la que nadie iba a colocar a mano.

**Nunca encima de un dominio vivo.** Puede haber meses dentro.

## Depende de

El archivo de rutas, y `#119`.
