# El paquete declara sus rutas, y el importador las reescribe

**Estado: diseñado, sin construir.**

## El problema, MEDIDO

Un dominio migrado llega entero y no funciona. Sus rutas absolutas apuntan a la máquina de
la que salió: **7 en el manifiesto** (vault, validador, acta, alma, instantánea…), **una en
cada uno de 6 instrumentos** y **una en un comando local**. Nada falla al copiar; falla al
usar, y cada choque parece un fallo del contenedor.

## Qué se añade

**Al exportar:** un `_RUTAS.json` dentro del paquete con cada ruta absoluta encontrada, de
qué archivo salió y en qué renglón. No las reescribe — las **declara**.

**Al importar:** se recorre esa lista y se sustituye por la ruta equivalente en la máquina
destino, que el importador sí conoce.

## Tres reglas que no son detalle

- **Se declara lo que se encontró, no lo que se supone.** Una ruta que el barrido no vio no
  se inventa: el acta dice con qué patrón se buscó, para que un silencio signifique algo.
- **La sustitución se enseña antes de aplicarse.** Reescribir archivos de otro dominio sin
  que nadie lo vea es exactamente lo que este marco no hace.
- **Y lo que no se pueda traducir se dice.** Una ruta que apunta fuera del paquete —un clon
  compartido, una herramienta del sistema— no tiene equivalente; se nombra en vez de
  adivinarse.

## Depende de

`#119` (el exportador está roto en `main`). Y lo necesita el importador.
