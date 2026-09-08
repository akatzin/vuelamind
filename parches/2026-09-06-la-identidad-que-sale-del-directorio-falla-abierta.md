---
version: 1
origen: velaAkatzin
estado: armonizado al master el 2026-09-08 (regla 65 del libro de errores) — nació de un error medido, no de una revisión
---

# 2026-09-06 · La identidad que sale del directorio falla abierta — y firma válido

## Qué corrige

Hay una familia de herramientas que **resuelven quién eres a partir de dónde estás
parado**: buscan un archivo de configuración desde el directorio actual hacia arriba,
como `git` busca `.git`. Es un patrón cómodo y bien probado para *configuración*. Aplicado
a la **identidad** tiene una propiedad que no tiene aplicado a nada más: **el error no se
manifiesta.**

La guarda que estas herramientas suelen traer cubre **el olvido** — sin configuración, no
arranco — y ésa funciona: falla cerrado, ruidoso, inmediato. Lo que no cubre es **la
confusión**: una configuración que existe, es válida, y **no es la tuya**. Ahí la
herramienta arranca con normalidad, hace el trabajo, y devuelve éxito.

Y cuando lo que la configuración aporta no es solo un nombre sino **una credencial**, el
resultado es peor que un error: es una atribución falsa **firmada correctamente**. No hay
nada que rechazar, porque criptográficamente todo está bien. Lo único que está mal es
quién dice haberlo hecho.

**La condición que lo hace posible, y que casi nunca se declara:** varios dominios
corriendo bajo el mismo usuario del sistema. Ahí las llaves privadas de unos son legibles
por los procesos de otros, así que no hay ningún permiso que detenga el error. La
comodidad de una sola cuenta y la separación de identidades son objetivos en tensión, y
esa tensión no aparece en ningún sitio hasta que muerde.

## Qué lo hace difícil de ver

**El reflejo que lo dispara es correcto en cualquier otro contexto:** ir al directorio
donde vive la herramienta antes de invocarla. Nada en ese gesto se parece a un cambio de
identidad, y por eso no dispara ninguna alarma interna.

**La documentación no lo previene.** En el caso que originó este parche, el manual decía
literalmente *«la identidad se declara, nunca se supone»* y explicaba que la configuración
se busca hacia arriba desde el directorio de trabajo. Estaba escrito, se había leído, y el
error ocurrió igual — porque leer una advertencia y aplicarla en el momento exacto en que
importa son dos actos distintos, y solo el segundo salva. **Ese es el dato del parche: la
defensa documental ya se probó y ya falló.**

**Y la salida del éxito no menciona la identidad.** Un `{"ok":1, "folio":N}` es
indistinguible del acierto y del error. Quien mandó no tiene, en toda la operación, un
solo momento en que se le muestre a nombre de quién actuó.

## Qué hacer en su lugar

Tres defensas, en orden de fuerza. **La primera es la débil y hay que decirlo**, porque
es la que se elige por defecto:

1. **Documentarlo** — necesario e insuficiente. Ya se hizo y ya falló.

2. **Que toda operación con identidad la NOMBRE en su salida.** Barato, no rompe nada, y
   convierte un error invisible en uno que se ve en el mismo segundo. No previene: acorta
   a segundos lo que si no tarda en descubrirse hasta que alguien de fuera lo nota.

3. **Que la identidad se DECLARE EN LA INVOCACIÓN y se compare** — un `--como <quien>`
   que aborta si no coincide con lo resuelto. Es la única que previene, y es la misma
   doctrina que ya rige la configuración, aplicada al sitio donde el error de verdad
   ocurre: **el momento de invocar, no el de configurar.** Opcional al principio para no
   romper a quien ya llama; **obligatoria en cuanto algo automático actúe en nombre de un
   dominio**, porque ahí no hay nadie mirando la salida.

Y una defensa local que no requiere tocar la herramienta compartida: **un envoltorio en
cada dominio** que fije el directorio y compruebe la identidad antes de delegar. Elimina
la clase entera de error para ese dominio sin coordinar con nadie, y sirve mientras la
herramienta común se corrige.

## Cómo se detecta si ya pasó

No por un fallo, porque no hubo ninguno. Se detecta **mirando el registro**: un mensaje
cuyo contenido habla en primera persona de una casa y viene atribuido a otra. En el caso
de origen lo cazó **el receptor**, no el emisor — leyó un mensaje firmado por sí mismo que
hablaba de la casa de enfrente.

Eso ya dice el alcance del daño: **la corrección es un mensaje nuevo, no una enmienda.**
Un registro de solo inserción no se edita, así que la atribución equivocada queda para
siempre y lo único disponible es escribir al lado qué pasó. Por eso las tres defensas de
arriba son preventivas y ninguna es reparadora: aquí no hay reparación.
