---
version: 1
origen: velaAkatzin
estado: armonizado al master el 2026-08-17 (lección 63 del libro heredado)
---

# 2026-08-17 · Una decisión escrita en una clave deprecada deja de aplicarse sin avisar, y el archivo sigue leyéndose como vigente

## Qué corrige

El método confía en el **registro escrito**: una decisión anotada es una decisión que no
hay que volver a tomar. Esa confianza tiene una grieta que ningún chequeo cubre — **cuando
la decisión vive en la configuración de una herramienta, la herramienta puede dejar de
obedecerla y el archivo no cambia.**

Una clave deprecada **no falla**: se ignora. No hay error, no hay aviso, no hay línea roja.
El ajuste sigue ahí, escrito con la palabra correcta de su época, y **quien lo lea concluye
que está vigente** — porque un archivo de configuración no distingue *«esto manda»* de
*«esto ya no se lee»*.

Es el mismo daño que un dato falso, con un agravante: **el dato falso puede medirse contra
la realidad; una clave muerta se autovalida**, porque lo que dice es exactamente lo que la
persona quería.

## Cómo se descubrió

**2026-08-17**, midiendo por qué un pie de atribución seguía apareciendo en los mensajes de
un repositorio público. El responsable **ya había tomado esa decisión** y la había escrito
en su configuración personal, con la clave que existía cuando la tomó.

Medido: **24 commits con ese pie**, con la clave puesta en `false`. La clave estaba
deprecada y su documentación lo decía —*«use X instead»*—; la herramienta la ignoraba desde
hacía versiones. Nadie mintió y nada falló: la decisión estaba tomada, escrita, verificable
y **sin efecto**.

Salió a la luz por un camino lateral —una revisión de qué se estaba publicando— y no por
ningún mecanismo que vigilara la configuración. Sin esa revisión, seguiría corriendo.

## Cómo aplicarlo

**Una decisión que se implementa en la configuración de una herramienta ajena no está
cerrada cuando se escribe: está cerrada cuando se comprueba su EFECTO.** Dos actos:

1. **Al tomarla, verificar el efecto una vez** — no que la clave esté puesta, sino que el
   comportamiento cambió. Son cosas distintas y sólo la segunda es evidencia.
2. **Anotar en el registro de decisiones contra qué versión se verificó.** Es lo que
   convierte *«lo decidimos»* en algo re-medible: sin la versión, un lector futuro no puede
   distinguir *«sigue funcionando»* de *«nadie ha vuelto a mirar»*.

**Y la señal barata para encontrar las que ya están muertas:** cuando una decisión de
configuración produzca un resultado que la contradiga, **sospechar de la clave antes que de
la decisión**. El reflejo es asumir que alguien la cambió; la causa frecuente es que la
herramienta dejó de leerla.

## Cómo verificar

- **Debe pasar:** toda decisión implementada en configuración externa lleva, en el registro,
  la fecha y la versión contra la que se verificó su efecto.
- **Debe seguir fallando:** una decisión anotada como cerrada cuya única evidencia es *«la
  clave está puesta»* se marca como no verificada — la presencia de la clave no es evidencia
  de que se lea.
- **Y el caso que debe seguir siendo válido:** una clave deprecada que se conserva a
  propósito por compatibilidad, **junto a su reemplazo**, con una nota de por qué. Lo que el
  parche persigue no es la clave vieja: es la clave vieja **sola**, haciéndose pasar por la
  política vigente.
