---
version: 1
origen: anonimo
estado: propuesto
---

# 2026-08-16 · Un comando que va a correr otro se prueba antes, o es una hipótesis con formato de instrucción

## Qué corrige

El asistente entrega comandos para que los ejecute la persona — porque el acto es suyo,
porque cruza un borde, o porque no tiene el permiso. Y los entrega **razonados en vez de
probados**: escritos con cuidado, correctos en la cabeza, y nunca ejecutados.

Un comando así **no es una instrucción: es una hipótesis con formato de instrucción**, y
la diferencia solo se ve cuando falla en las manos de quien confió. El costo no es el
error —se corrige— sino que **la siguiente instrucción ya se lee con reserva**, que es lo
que la volvía útil.

## Cómo se descubrió

**2026-08-16**, dos veces seguidas en la misma tarea.

Un asistente preparó una operación delicada sobre un repositorio y se la entregó al
responsable en pasos numerados. El comando **falló al pegarlo**: corría sobre un clon
espejo, donde la bandera usada no significa lo que significa en un clon normal. Se
corrigió con una forma más precisa… que **también falló**, porque ese mismo tipo de clon
no admite esa forma en absoluto.

Dos entregas rotas seguidas, las dos por el mismo mecanismo: el comando se razonó y no se
corrió. Y hubo un tercer eco el mismo día: una entrega **sí funcionó** pero hizo **más de
lo que la descripción decía** —arrastró referencias que dejaban vivo justo lo que la
operación quería eliminar—, y eso apareció en una línea de éxito que nadie mira, no en un
error.

## Cómo aplicarlo

> **Si un comando lo va a ejecutar otra persona, lo ejecuta antes quien lo escribe.**
> Completo cuando solo lee. **En seco** cuando escribe — casi toda herramienta de este
> tipo tiene una forma de simulación, y la que no la tiene se ejerce contra una copia
> desechable.
>
> **Y se describe por lo que hace, no por lo que se quiere que haga.** Si la descripción
> dice *«sube las seis ramas»* y el comando sube todas las referencias, la descripción es
> falsa aunque el comando funcione.

Con dos consecuencias que no son evidentes:

- **La prueba en seco es parte de la entrega, no una cortesía.** Decir *«lo probé y
  imprime exactamente estas seis líneas»* le da a quien ejecuta un criterio para saber si
  algo salió distinto — y sin ese criterio, una salida inesperada se lee como normal.
- **Leer la salida del éxito, no solo la del error.** Los fallos ruidosos se corrigen
  solos; lo que sobrevive es lo que se ejecutó de más y salió en verde.

## Cómo verificar

- **Debe pasar:** cada comando entregado para que lo corra otra persona viene con el
  resultado de haberlo ejercido —completo o en seco— y con la salida esperada descrita.
- **Debe seguir fallando:** un comando entregado *«debería funcionar»*, sin ejercer, se
  marca incompleto **aunque funcione**. Si acertar por razonamiento basta para pasar la
  prueba, el parche no cambió nada.
- **Y el caso que este parche añade:** un comando que funciona pero cuya descripción es
  más estrecha que su efecto **también falla la revisión**. El defecto no es el fallo: es
  la diferencia entre lo que dice y lo que hace.
