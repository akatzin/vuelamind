# La puerta del puente: quitar la dependencia del túnel

**Estado: diseño, sin construir. Nace de una objeción de Akatzin el 2026-09-28:
*«no estamos para el SaaS si necesitamos del túnel»*.**

## El problema

Para alcanzar el puente hoy hay que abrir un túnel. Eso vale para una persona técnica en su
máquina y **no vale para un producto**: nadie se suscribe a algo que exige `gcloud compute ssh`
antes de escribir un mensaje.

## Por qué el túnel no es un capricho: es la única cerradura que hay

MEDIDO sobre el código, 2026-09-28:

- el servicio **escucha en loopback**;
- **allowlist de `Host`**: solo `127.0.0.1`, `localhost`, `::1` — cualquier otro se rechaza;
- **chequeo de `Origin`** en `POST`/`DELETE`, contra `http://127.0.0.1:<puerto>`;
- **no hay token, ni sesión, ni usuario.**

Todo el modelo asume **un único humano de confianza en la máquina**. El túnel es lo que hace
cierta esa premisa. Quitarlo sin poner otra cosa no es abrir el producto: es abrir un puerto
con permiso de ejecutar.

## Tres caminos, y solo uno se sostiene

**1 · Un proxy que reescriba `Host` y `Origin` a loopback.**
Funciona hoy, sin tocar el canon. **Descartado:** es mentirle al puente. Sus dos comprobaciones
siguen ahí, pasan siempre, y dejan de significar nada — sin que nada lo delate. Una defensa que
se cumple por construcción es peor que no tenerla, porque se lee como que protege.

**2 · Balanceador HTTPS con IAP delante de la VM. ADOPTADO.**
El navegador entra por `https://`, Google autentica, e IAP inyecta una cabecera con un **JWT
firmado**. Ni túnel ni puerto expuesto, y la identidad la resuelve quien sabe hacerlo.

**3 · Sesión y login propios en el puente.**
**Descartado:** es reimplementar IAP y además mantenerlo — recuperación de contraseña, segundo
factor, rotación. Nada de eso es el negocio.

## El cambio en el canon, que es pequeño y tiene una condición

Dos piezas, y **viajan en el mismo commit o no viaja ninguna**:

| Pieza | Qué hace |
|---|---|
| `BRIDGE_PUBLIC_ORIGIN` | Declara un `Host` y un `Origin` externos como válidos, además de loopback |
| Verificación del JWT de IAP | **Obligatoria** siempre que la anterior esté puesta |

**Por qué juntas.** Hoy la única cerradura es *«solo loopback»*. La primera pieza la quita. Si
la segunda llega después —aunque sea una hora después— en medio hay un puente alcanzable desde
internet que ejecuta lo que le pidan. Separarlas no es una decisión de orden: es la ventana.

**Verificar significa verificar**, no mirar que la cabecera exista: firma contra las claves
públicas de Google, `audience` igual al backend declarado, y caducidad. Una cabecera que
cualquiera puede escribir no autentica a nadie.

**Falla cerrado, como el resto del puente.** Si `BRIDGE_PUBLIC_ORIGIN` está puesto y falta la
declaración del `audience`, **el servicio no arranca** — la misma doctrina que ya tiene
`BRIDGE_PERMISSION`, que se niega a correr sin nivel declarado en vez de suponer el más
permisivo.

**Y avisa fuerte si el origen público no es `https`.** Es el error que alguien va a cometer en
su portátil para «probar rápido».

## Lo que esto NO resuelve

- **No es multi-inquilino.** Un contenedor por persona significa que IAP solo tiene que probar
  que quien entra es *esa* persona. Qué contenedor le toca a cada identidad es trabajo del
  encaminador de delante, no del puente.
- **No cambia el permiso.** Con la puerta puesta sigue siendo verdad que `full` es ejecución
  arbitraria; el SaaS lo prohíbe por otra vía (ver `saas-el-primer-corte.md`).
- **No sirve para la instalación local**, que no lo necesita: ahí el túnel y el loopback siguen
  siendo la respuesta correcta y no se tocan.

## Cómo se comprueba que quedó bien

No basta con que la página cargue. Hay que ejercer los dos negativos:

1. petición **sin** la cabecera de IAP → `403`;
2. petición con una cabecera **fabricada a mano** → `403`.

Si el segundo pasa, no hay puerta: hay un cartel de puerta.
