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

> [!important] NO CAMBIA NINGUNA REGLA — pero SÍ hay algo nuevo que instalar
> **No hay claves nuevas del manifiesto** y ninguna regla del método cambia: si tu dominio ya
> nació, la plantilla de la que nació dejó de contradecirse y nada más.
>
> **Lo que sí cambia es el inventario de skills: el canon pasó de once a doce.** Ver abajo.
>
> Salta si vas a hacer nacer a alguien, o si quieres leer un master coherente.

## Lo que hay que instalar: el skill doce

El canon incorporó **`vuelamind-rc`** y sus herramientas en `herramientas/interfaz_agente/`.
Es un puente HTTP local que crea y opera varias sesiones headless de Claude Code desde una
página de chat propia; nace para donde no hay control remoto nativo.

**Aunque no lo vayas a usar, tu dominio se entera.** El inventario de skills del canon es el
que comprueban `comprobar_skills.py` y el validador de cada casa: con doce en el canon y once
instalados, **tu validador sale ROJO** con *«skill del canon no instalado»*.

**MEDIDO el 2026-09-11 en la casa vigía**, que fue la primera a la que le pasó en cuanto el
skill entró a `main`.

**Qué hacer, y son dos líneas:**

```sh
cp <clon-del-canon>/skills/vuelamind-rc.md ~/.claude/commands/
python3 <clon-del-canon>/herramientas/comprobar_skills.py     # debe decir: AL DIA 12
```

*(Si tu máquina recibe los comandos por réplica automática, llegará solo; el comando de
arriba sirve igual para comprobarlo.)*

> [!warning] Instalar el skill NO es instalar el puente
> Copiar el archivo solo pone el comando al día. **Levantar el servicio es otra cosa** y tiene
> requisitos propios —Python 3.10 o superior, el CLI `claude` presente, y elegir a mano el
> nivel de permiso, que no tiene valor por omisión a propósito—. El skill los explica. En
> Windows, su camino de arranque automático **está sin medir del todo** al publicarse esto.

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
