---
title: Salto menor a v3.8 — cinco defectos de coherencia del propio master
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — el master que trae nombra piezas de la v3.5
---

# UPGRADE a v3.8 — el master deja de contradecirse

> [!note] De dónde tienes que venir: REQUIERE la v3.5
> El master es un solo archivo acumulativo, y el que trae este salto nombra
> `/vuelamind-learn`, el artefacto de la v3.5. Si saltas desde más atrás, el documento
> promete una pieza que no tienes.
>
> *El mapa completo de saltos vive en `UPGRADE.md`, que no muere con ninguna versión.*

> [!important] NO CAMBIA NINGUNA REGLA — corrige lo que el documento decía mal de sí mismo
> No hay claves nuevas, ningún skill cambia y no hay nada que instalar. **Si tu dominio ya
> nació, lo único que cambia es que la plantilla de la que nació dejó de contradecirse.**
>
> Salta si vas a hacer nacer a alguien, o si quieres leer un master coherente.

## Los cinco

**1 · El documento se contradecía sobre el Bloque E.** En un sitio decía *«duplicaría **el
Bloque E de la entrevista**»* y en otro *«**Bloque E — no existe**»*. Ahora el encabezado dice
**qué es** —*lo resuelve el marco, no la entrevista*— y las referencias apuntan a eso.

**2 · Una sección mezclaba dos actores sin decirlo.** *«Cómo se propone un parche al canon»*
anunciaba que los parches ya no se proponen por pull request **y a continuación explicaba cómo
abrir el pull request**. No era residuo: **esas instrucciones son del vigía del canon**, y
faltaba decirlo. Ahora la sección se llama *«Cómo llega un parche al canon — y quién hace cada
parte»* y nombra a los dos: la casa escribe y manda; **el vigía juzga, armoniza y abre el PR**.

> **Por qué importaba:** una casa que leyera las instrucciones del vigía como suyas **iría a
> buscar una cuenta que no necesita** — exactamente lo contrario de lo que la v3.5 consiguió.

**3 · La lección 64 era un título sin cuerpo.** Su desarrollo —el medidor de frescura del clon,
la caché que miente con cara de fuente— había quedado embebido al final de la lección 65 al
insertarla. Devuelto a su sitio, verificado contra el historial: **es su texto original, ni una
palabra de más ni de menos.**

**4 · La lista de la Fase 3 tenía dos ítems numerados `8.`** Va de 1 a 10 sin repetidos.

**5 · Una afirmación falsa dentro del documento.** Decía que *«en la dirección contraria no hay
nada equivalente»* cuando el último punto de esa misma lista **es** el equivalente. El aviso
que lo contenía deja de denunciar un hueco cerrado y pasa a explicar **por qué ese punto
existe** — lo que dice qué hacer es el punto; el aviso dice qué pasa cuando no se hace.

## Cómo saltar

1. **Trae `MARCO_Inicial.md` del canon y comprueba que dice `version: 3.8`.** Si tu copia está
   modificada, respáldala antes.

**Nada más.** Ningún skill, ninguna clave, ningún archivo que mover.

**Cómo sabes que funcionó:** tu master **no contiene** la cadena `Bloque E de la entrevista`, y
la lista de verificación de la Fase 3 llega hasta el punto 10.

> [!note] Por qué esto es una versión y no una corrección de estilo
> Tres de los cinco cambian **lo que el documento afirma**: dos afirmaciones eran falsas y una
> instrucción estaba dirigida a quien no debía seguirla. Eso no es cosmético.
>
> **Lo que sí es de estilo —quitar del master la narración de su propia historia— va aparte**,
> y con razón: al validarlo se midió que **una de cada cuatro reescrituras perdía norma**, y
> mezclarlo aquí habría escondido el contenido detrás de la redacción.
