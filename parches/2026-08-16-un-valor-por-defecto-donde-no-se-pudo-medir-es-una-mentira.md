---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-16 · Un valor por defecto en un lugar donde no se pudo medir es una mentira con formato de dato

## Qué corrige

Cuando una medición falla —la herramienta no está, el permiso no alcanza, la ruta no
existe— el reflejo del código es devolver algo: `0`, `[]`, `"—"`, la cadena vacía. Parece
robustez: el programa no se cae y la interfaz no se rompe. Pero **el valor devuelto viaja
por el mismo canal, con el mismo formato y la misma autoridad que un valor medido**, y a
partir de ahí nadie puede distinguirlos.

El daño no es el error: es que **el cero es un dato plausible**. «Cero contenedores
corriendo» es un estado posible del mundo, y por eso nadie lo cuestiona. Si el fallo
devolviera basura visible se notaría en un segundo; al devolver algo verosímil, se lee
como medición y puede sostener una decisión.

> Es la cara de salida de una familia que el libro ya conoce por su cara de entrada:
> *cero resultados no es ausencia* mira una **búsqueda** que devuelve nada; ésta mira una
> **medición** que no ocurrió y aun así entrega un número. Y es hermana de *el puerto
> responde no es el servicio funciona*: las dos confunden el continente con el contenido.

## Cómo se descubrió

**2026-08-16.** Un panel de control web mostraba métricas de la máquina que lo hospeda.
Su servicio corría **aislado en un contenedor**, sin acceso a las herramientas del host,
así que cada consulta fallaba en silencio y la función devolvía sus valores por defecto.
El panel mostraba, con toda confianza y buen formato: **`0/0` contenedores, sin pools, sin
temperatura**.

Nada estaba roto. El servicio respondía, la página pintaba, ningún log tenía un error. El
único síntoma era que los números eran **plausibles y falsos** — y se descubrió por
contraste, al comparar contra el host, no por ninguna alarma.

**La salida fácil habría empeorado otra cosa:** darle al contenedor acceso al motor de
contenedores del host resolvía las métricas en una línea, y de paso le entregaba
privilegios de administrador a un servicio expuesto por web. Se resolvió al revés — el
host mide y deja el resultado en un archivo, el servicio solo lee — y **eso obligó a
contestar la pregunta que el valor por defecto escondía: ¿y si el archivo no está?**

## Cómo aplicarlo

Texto para las reglas del dominio:

> **Una medición que no se pudo hacer no devuelve un valor: devuelve que no se pudo.**
> Distingue en el tipo, no en el comentario — un campo `sin_datos`, un estado explícito,
> un valor imposible de confundir con uno real. Y **la interfaz lo muestra distinto**: si
> el consumidor de ese dato es una persona, tiene que poder ver de un vistazo la
> diferencia entre *cero* y *no sé*.
>
> **La prueba, y es de una sola pregunta:** *si esta medición fallara ahora mismo, ¿qué
> mostraría?* Si la respuesta es «un cero», «un guion» o «una lista vacía» **con el mismo
> aspecto que un resultado bueno**, el defecto ya está ahí — no hace falta esperar a que
> falle para saberlo.

Y el corolario que aparece al aplicarlo: **la edad también es medición.** Un dato leído de
una caché o de un archivo intermedio puede ser correcto y viejo; mostrar *cuándo* se midió
cuesta un campo y evita la variante temporal del mismo engaño.

## Cómo verificar

- **Debe pasar:** con la fuente de datos retirada a propósito, la interfaz muestra
  explícitamente que no pudo medir, y ningún consumidor puede confundir ese estado con un
  valor real.
- **Debe seguir fallando:** una función de medición cuyo `except` devuelva `0`, `[]` o
  `"—"` indistinguibles del camino bueno debe ser rechazable en revisión **aunque nunca
  haya fallado en producción** — el defecto es del diseño, no de la frecuencia.
