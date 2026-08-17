---
version: 1
origen: akatzin
estado: propuesto
---

# 2026-08-16 · Renombrar al asistente después de nacer: el alcance es la decisión, no el nombre

## Qué corrige

El método ya tiene un parche que pone nombre al asistente en la fase de inicialización,
y ese parche trae una advertencia excelente:

> "un dominio de seis meses con «el asistente» incrustado en su registro de decisiones
> y su bitácora ya no se renombra sin reescribir historia"

La advertencia es correcta y no sirve de nada cuando el renombrado ocurre igual.
Nombrar es una decisión del responsable, y los responsables cambian de opinión: el
nombre es lo más personal de la relación de trabajo, así que es justo lo que más
probablemente se revise. El método avisa del costo y NO dice qué hacer cuando se paga —
así que la instancia improvisa, y las dos improvisaciones obvias son malas:

- Reemplazo global. Un `sed` sobre todo el vault. Deja un solo nombre y ningún lector
  tropieza — y reescribe entradas fechadas: un error registrado hace meses pasa a estar
  firmado por un nombre que ese día no existía. El registro de errores es la pieza de la
  que depende la salud del marco, y su valor entero es decir lo que se escribió entonces.
- No hacer nada, o "lo hacemos luego". Deja las reglas y el manifiesto contradiciendo al
  responsable por tiempo indefinido, que es la forma fiable de que no se haga nunca.

## Qué añade

Un renombrado posterior a la inicialización se resuelve por alcance, y el alcance se
mide antes de decidirlo. Tres pasos:

1. Medir primero, y enseñar el número. Contar las menciones por archivo antes de tocar
   nada. El tamaño ES la información que hace falta para decidir, y suele sorprender: en
   el caso que originó este parche fueron 112, y el responsable cambió de postura al verlo.

2. Partir el vault en dos, que no es lo mismo que partirlo por carpetas.
   - Normativo — lo que dice quién es el asistente AHORA: la regla del nombre, la nota de
     identidad, las claves del manifiesto que leen las herramientas, el frontmatter del
     acta. CAMBIA.
   - Fechado — lo que registra qué pasó y cuándo: registro de errores, bitácora, registro
     de parches, entradas antiguas de decisiones. NO CAMBIA.

   La prueba para clasificar una mención: ¿esta frase gobierna lo que se hará mañana, o
   describe lo que pasó un día concreto? Una regla se renombra; un acta de lo ocurrido, no.

3. Pagar la deuda de legibilidad con un aviso, y decir que es un aviso. El vault queda
   con dos nombres conviviendo, y eso es real. Se escribe en los sitios normativos —no en
   las notas históricas, que no se tocan— una línea del tipo "antes se llamó X; si lees X
   en una entrada con fecha, es la misma entidad". Esto MITIGA, NO ELIMINA, y el parche
   pide decirlo así en la decisión.

Y va al acta como enmienda nueva, sin retirar la anterior. Las dos secciones conviven a
propósito: la primera dice qué nombre hubo entre tal fecha y tal otra. Un acta que sólo
muestra el nombre actual ha perdido justo el dato que la hacía un acta.

## Cómo se descubrió

Un dominio de operaciones con trece días de vida renombró a su asistente. Al medir, 112
menciones en 22 archivos — 96 en el vault y 16 en el andamiaje, incluidas seis claves de
un manifiesto que leen las herramientas de cierre.

Lo revelador es de dónde salió el criterio: no del método, que no lo tenía, sino de una
frase que el propio dominio se había escrito nueve días antes, en el parche que le puso
el primer nombre. La advertencia estaba redactada, fechada y archivada —y describía
exactamente la situación que se estaba viviendo— pero como no venía con un procedimiento,
sólo servía para confirmar el arrepentimiento después.

Ésa es la forma del defecto que este parche corrige: una advertencia sin procedimiento es
un lamento con fecha de emisión anticipada.

## Señal de que falta

Busca en el método una advertencia del tipo "esto es barato ahora y caro después"
—nombrar, elegir una convención, fijar una estructura de carpetas, escoger un
identificador—. Si la encuentras y no viene acompañada del procedimiento para cuando se
haga después, falta este parche aplicado a ese caso.

## Cómo se aplica

- En la sección de inicialización, junto al parche que pone el nombre: una nota de que el
  renombrado posterior existe, es legítimo y tiene procedimiento, con los tres pasos.
- En el ciclo de cierre: al renombrar cualquier cosa citada por otras notas, medir el
  alcance y presentarlo antes de escribir — caso particular de "el radio del cambio sale
  del grafo".
- El caso de referencia queda en el registro de decisiones y en el acta del dominio de
  origen, fechados el 2026-08-16.
