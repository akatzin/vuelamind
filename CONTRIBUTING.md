# Cómo contribuir a vuelamind

El método mejora por **parches**: correcciones descubiertas usándolo, con caso
real y forma de verificarse. Este repositorio es el canon; los parches se
proponen aquí, como pull requests.

## Qué es un parche

Un archivo en `parches/` con el nombre `AAAA-MM-DD-descripcion-corta.md` (la
fecha es la del **descubrimiento**) y este frontmatter:

```yaml
---
version: 1
origen: <tu handle, o "anonimo">
---
```

Y cuatro secciones: **Qué corrige** (el defecto, en una frase), **Cómo se
descubrió** (el caso real, con fecha — es lo que evita que alguien lo revierta
por parecerle arbitrario), **Cómo aplicarlo** (el texto genérico), y **Cómo
verificar** (incluido el caso que debe SEGUIR fallando).

## La única prueba que importa

**Reescribe tu lección sustituyendo todos los nombres propios por genéricos.
¿Sigue siendo cierta y útil?** Si sí, es del método y cabe aquí. Si solo es
cierta con tus nombres puestos, es de tu dominio — guárdala allá.

Quien revisa tu PR aplica esa misma prueba y ninguna otra: **no juzga la verdad
de tu caso** (no puede — pasó en tu dominio), juzga si la lección generaliza.
La verdad del caso la juzga cada dominio que adopte el parche, contra su propia
evidencia, con tres veredictos posibles: adoptar, posponer o **descartar con
razón** — y descartar con razón vale más que aplicar por cortesía.

## Antes de abrir el PR: anonimiza el CONJUNTO, no el fragmento

Dos detalles inocentes por separado pueden identificar tu operación juntos, y
el que los une suele ser un nombre que quedó en otro archivo por parecer
inofensivo. Quita nombres de personas, organizaciones, áreas, hosts, rutas,
IPs y dominios; **conserva el mecanismo del error, la consecuencia medida y la
señal que lo delató** — eso es lo que enseña. Publicar es irreversible: la
revisión va antes del push, no después del primer reporte.

## Qué no va aquí

- Configuración o experiencia de un dominio concreto (eso vive en cada
  instancia, no en el canon).
- Parches sin caso real ("se me ocurrió que...") — el método aprende de
  errores pagados, no de opiniones.
- Cambios al texto de un parche ya publicado sin subir su `version:` — la
  versión es lo que avisa a las instancias de que el original cambió.
