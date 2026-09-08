---
title: Salto menor a v3.7 — la regla dura de fechas
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — el master que trae nombra piezas de la v3.5
---

> [!important] LA CADENA DE SALTOS — de dónde tienes que venir
> Los saltos menores de la línea base v3 **no forman una sola fila**: hay una rama suelta.
>
> ```
>   v3.0 ──┬── v3.4  el canal        ORTOGONAL: no la necesita nadie
>          │                          y ella no necesita a nadie
>          │
>          └── v3.5  el buzón  ──▶  v3.6  la entrevista  ──▶  v3.7  las fechas
> ```
>
> **La v3.4 es independiente en las dos direcciones.** Sáltala solo si vas a hablar con otras
> casas; ningún otro salto la nombra ni la necesita.
>
> **De la v3.5 en adelante sí hay orden**, y por una razón concreta: **el master de la v3.6 y
> el de la v3.7 nombran `/vuelamind-learn`**, que es el artefacto que instala la v3.5. Traer
> ese master sin haber hecho la v3.5 deja un documento que **promete una pieza que no tienes**.
>
> **Y el master es un solo archivo acumulativo:** traer el de la v3.7 te trae también la v3.6.
> Lo que NO trae son los artefactos —skills, código, claves del manifiesto—, que viven fuera y
> hay que instalar salto a salto.
>
> **Si vienes de la v3.0, la ruta corta es: haz la v3.5, luego trae el master de la v3.7.**
> Dos pasos, y quedas con las tres. El canal, aparte y solo si lo necesitas.

# UPGRADE a v3.7 — las fechas dejan de ser costumbre y pasan a ser regla

> [!important] ESTE SALTO NO TE OBLIGA A CORREGIR NADA HOY
> Añade **una regla permanente** al método. No cambia ningún skill, ningún comando y ninguna
> estructura. **Tu vault sigue siendo válido tal como está.**
>
> Lo que gana tu dominio es que la regla existe escrita, así que **el próximo relevo la
> hereda** en vez de reinventarla.

## Qué entra: Fase 2 §6, la regla de fechas

**Tres partes, y las tres salen de algo medido en un vault real.**

**1 · Toda fecha que sea DATO se escribe `YYYY-MM-DD`.** Es **ISO 8601** —no ANSI, que es
`MM/DD/YYYY` y es justo el ambiguo—. Ordena solo (alfabético = cronológico), no se confunde
entre países, y se encuentra con una sola expresión.

**2 · La zona se declara.** Un vault que fecha en una zona distinta a la del sistema tiene que
decirlo en su arranque. Si no, durante las horas de solapamiento **sus entradas llevan un día
distinto al del reloj de la máquina** y son indistinguibles de un error.

> **El caso:** una casa cuyo vault fechaba en UTC leyó sus propias entradas como adelantadas y
> **llevó doce fechas correctas a una lista de correcciones**. Lo paró pedir la hora a dos
> servicios externos antes de escribir.

**3 · Las fechas relativas, solo con ancla.** *«Hoy»*, *«ayer»*, *«la semana pasada»* valen
**solo si la nota que las contiene lleva su propia fecha absoluta**. En la cola, en decisiones
o en el panorama **no tienen contra qué resolverse y envejecen sin que nadie las toque**.

> **El caso:** en ese mismo vault, *«cualquiera que clone hoy nace con los parches apagados»*
> era cierto el día que se escribió y **falso tres días después**. Nadie lo editó.

**Y la prosa no se prohíbe: se ubica.** El dato en ISO, el relato en prosa. Un encabezado
`## 2026-09-08 — El día que...` tiene las dos: la fecha se ordena y se busca, el título se lee
en voz alta.

## Cómo saltar

1. **Trae `MARCO_Inicial.md` del canon y comprueba que dice `version: 3.7`.** Si tu copia está
   modificada, respáldala antes.

**Nada más.** Ningún skill cambió, ninguna clave nueva, ningún archivo que mover.

**Cómo sabes que funcionó:** tu master tiene una sección `### 6. Las fechas — regla dura` en
la Fase 2.

## Qué hacer con lo que ya está escrito

> [!warning] NO barras tu vault entero hoy
> **Corrige lo que la regla vuelve FALSO** —una fecha relativa que ya no es cierta— y **anota
> como pendiente lo que solo vuelve inconsistente**. Barrer cientos de líneas a mano cambia
> una deuda conocida por un riesgo nuevo.
>
> Medido en el vault donde nació la regla: **411 fechas ya en ISO y cero en otro formato de
> dato** — el formato no había que arreglarlo. Lo que había eran **136 relativas**, y de ésas
> solo una era falsa.

> [!note] Por qué se escribe una regla que ya se cumplía
> La convención existía en la práctica y **no estaba en ninguna parte del canon**. El próximo
> dominio no tenía de dónde heredarla: la habría reinventado, o no.
>
> **Una convención que solo vive en la costumbre se pierde en el primer relevo.**
