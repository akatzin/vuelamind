---
version: 1
origen: akatzin
estado: armonizado al master el 2026-08-16 (lección 51 del libro heredado)
---

# 2026-08-16 · Una pieza que se declara disuelta necesita que se busque dónde vivía

## Qué corrige

Cuando un pendiente agrupa varias piezas y una se resuelve **bien**, es fácil concluir
que otra *"dejó de tener sentido"* o *"era la misma cosa"*. A veces es verdad. Pero si
esa pieza describía un defecto **en otro componente**, la conclusión es falsa: el defecto
sigue vivo, y ahora está peor que antes — porque **queda escrito que ya no existe**, y
nadie vuelve a buscar lo que se declaró disuelto.

Es pariente de *cero resultados no es ausencia*, con una diferencia que lo hace más
traicionero: allí se afirma una ausencia tras **buscar mal**; aquí se afirma **sin buscar
nada**, apoyándose en la satisfacción de haber resuelto la pieza vecina. La disolución se
siente como consecuencia lógica del arreglo, no como una afirmación que necesita
evidencia — y por eso no dispara ninguna alarma interna.

## Cómo se descubrió

**2026-08-16.** Un pendiente instrumental agrupaba tres defectos de herramienta. Al
resolver el primero —un chequeo nuevo— se comprobó que el segundo quedaba disuelto: su
enfoque era la aproximación de cuando no existía el primero, y eso era **cierto y
medible**. Por arrastre, se escribió que el tercero —*"cierto extractor no entiende un
escape"*— también se había disuelto, suponiendo que hablaba del detector recién escrito.

**Veinte minutos después el defecto apareció solo**, destapado por el propio arreglo del
autor: al corregir los datos como el chequeo nuevo pedía, otro componente —un extractor
distinto, en otra parte del validador— empezó a fallar exactamente como el tercer punto
describía. La pieza nunca se disolvió: **vivía en un componente que nadie fue a mirar**.

El registro ya publicado afirmaba lo contrario, así que hubo que corregirlo con el error
dicho, no maquillado.

## Cómo aplicarlo

Texto para las reglas del dominio:

> **Una pieza no se declara disuelta sin ir a buscar dónde vivía.** Antes de escribir que
> un punto de un pendiente "ya no aplica" porque otro se resolvió: **localiza el
> componente concreto que describía** y compruébalo. Si no puedes nombrar el archivo, la
> función o el chequeo del que hablaba, no sabes si se disolvió — sabes que ya no te
> acuerdas de qué era.
>
> Y si la comprobación no es posible ahora, la salida honesta no es *disuelta* sino
> **«no localizada — se cierra el resto y esto queda abierto»**. Un punto huérfano
> declarado cuesta un renglón; uno declarado muerto cuesta que nadie lo busque nunca más.

**La señal barata de que estás por cometerlo:** la palabra *disuelta* (o *ya no aplica*,
*era lo mismo*) aparece en el mismo párrafo donde celebras haber resuelto la pieza vecina.
La satisfacción y la conclusión llegan juntas — y solo una de las dos tiene evidencia.

## Cómo verificar

- **Debe pasar:** un cierre que declare una pieza disuelta nombra el componente que la
  pieza describía y muestra por qué ahí ya no ocurre.
- **Debe seguir fallando:** un cierre que declare disuelta una pieza **sin nombrar dónde
  vivía** debe ser rechazable en revisión, aunque las otras piezas del pendiente estén
  impecablemente resueltas. Si la calidad del resto compra el punto sin evidencia, la
  regla no está aplicada.
