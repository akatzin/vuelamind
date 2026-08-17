---
version: 1
origen: anonimo
estado: propuesto
---

# 2026-08-16 · Anonimizar y desatribuir no son lo mismo

## Qué corrige

El método insiste, con razón, en **anonimizar antes de publicar**: quitar nombres de
personas, hosts, rutas, organizaciones. Y no dice en ninguna parte que esa operación tiene
un vecino que se le parece y hace daño distinto: **desatribuir** — dejar el trabajo sin
dueño.

El reflejo de «quitar la identidad» produce las dos cosas a la vez, porque el mismo campo
lleva las dos. Y el resultado se ve limpio: nada delata que un cuerpo de trabajo público
dejó de tener autor. Los daños son reales — el trabajo no cuenta para quien lo hizo, y un
proyecto público **sin ningún contribuyente visible se lee como abandonado**, justo
mientras invita a que la gente aporte.

Lo que había que quitar era **el dato interno** —el host, la ruta, la máquina—, no el
vínculo con la persona.

## Cómo se descubrió

**2026-08-16**, limpiando la historia publicada de un repositorio.

Más de la mitad de los commits llevaban una identidad de máquina interna, con nombre de
host. Se reescribió la historia unificando toda la autoría a una identidad neutra… **que no
correspondía a ninguna cuenta existente en la plataforma**. La limpieza fue correcta: el
host desapareció. Y el efecto colateral no lo vio nadie hasta mirar la portada del
repositorio: **cero contribuyentes**, y ningún commit contando para el perfil de quien
había escrito todo.

Hubo que reescribir por segunda vez, ahora con la dirección de reenvío que la plataforma
ofrece para exactamente este caso: enlaza con la cuenta y **no expone el correo real**. Lo
que costó no fue el error, fue repetir una operación irreversible.

## Cómo aplicarlo

Al preparar cualquier publicación, **separar las dos preguntas y contestarlas por
separado**:

> **¿Qué dato interno no puede salir?** — hosts, rutas, usuarios de sistema, nombres de
> equipos, IPs. Esto se quita siempre.
>
> **¿Quién firma lo que sale?** — y esto **se decide**, no se borra por reflejo. Las
> plataformas suelen ofrecer una identidad que atribuye sin exponer; si existe, es la
> respuesta por defecto. Si la decisión es publicar sin autor, que sea una decisión
> escrita y no el residuo de haber limpiado otra cosa.

**La señal barata de que se confundieron:** después de anonimizar, mirar si el trabajo
sigue teniendo dueño. Si la respuesta es *«ninguno»* y nadie lo decidió, se desatribuyó
sin querer.

## Cómo verificar

- **Debe pasar:** una publicación limpia no contiene ningún dato interno **y** su autoría
  apunta a quien corresponde, con una identidad que no expone el correo real.
- **Debe seguir fallando:** una historia sin datos internos pero **sin autor asociable** se
  marca como defecto, no como éxito de anonimización — era exactamente el estado que este
  parche corrige.
- **Y el caso que debe seguir siendo válido:** publicar sin autor **a propósito**, con la
  decisión escrita. Anónimo por elección es legítimo; anónimo por reflejo, no.
