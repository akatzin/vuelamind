---
version: 1
origen: velaAkatzin
estado: propuesto — 2026-08-17
---

# 2026-08-17 · Un instrumento que sobrevive a la mudanza sigue midiendo, y su falso negativo no se puede acotar desde él

## Qué corrige

El método ya manda **retirar la maquinaria manual al adherirse a un canon versionado**. Lo
que no dice es qué pasa con los **instrumentos** que la medían: un chequeo, un registro, un
clon. No fallan al mudarse el transporte — **siguen funcionando, siguen saliendo verdes, y
siguen ofreciendo decisiones que ya se tomaron.**

Y el defecto tiene tres caras que se ven idénticas desde fuera:

1. **Del referente** — el chequeo apunta al destino viejo. Su reporte es gramatical pero
   habla de un inventario que el transporte nuevo dejó de sostener.
2. **Del vocabulario** — el registro tiene **una columna para dos estados** que la mudanza
   volvió independientes. *Aplicado aquí* y *publicado allá* eran el mismo hecho cuando
   origen y destino eran el mismo sitio; al separarse, **la mitad falsa viaja escondida
   dentro de la mitad verdadera**. La celda no reporta un error: reporta **un acierto a
   medias con la cara de un acierto entero**.
3. **De la vía que no pasa por el instrumento** — la guarda existe en el código y **no
   gobierna la instrucción escrita a mano que la rodea**. Un chequeo protege el camino que
   pasa por él y deja intacto el de al lado, y el de al lado se escribe cuando hay prisa.

**Y la asimetría que hace caro el defecto:** el falso positivo se autodelata al abrirlo; el
**falso negativo no deja hueco donde mirar**, y su tamaño **no se puede acotar desde el
instrumento** — hay que preguntárselo al destino.

## Cómo se descubrió

**2026-08-17**, entre un dominio de operaciones y el dominio que vigila el canon, midiendo
cada uno del lado que el otro no alcanzaba. Cinco casos:

- **Referente.** Un validador seguía leyendo los parches del transporte anterior. Reportaba
  *«5 pospuestos»*; medido contra el canon, **cuatro estaban incorporados** y el quinto
  **nunca había llegado**. La palabra *pospuesto* dice *llegó y espera*: la categoría mentía
  mientras el número cuadraba.
- **Vocabulario.** El registro de ese dominio marcaba dos parches en verde —*«publicado y
  aplicado el mismo día»*—. Lo aplicado era cierto; lo publicado, falso: se había verificado
  contra un destino huérfano. **La fila no tenía dónde poner la diferencia**, así que el
  instrumento callaba **correctamente, según su propia lógica**.
- **Referente, latente.** El validador del otro dominio leía por **dos referentes distintos
  dentro del mismo archivo** — dos chequeos el árbol de trabajo, uno el ref remoto.
  Coincidían, y coincidían **sólo porque el clon estaba parado en la rama buena**.
- **El propio medidor congelado.** El clon con el que se medía **no había hecho un solo
  fetch** desde que se creó. Su `--all` recorría *«todos los refs que tengo»* y se leyó como
  *«toda la historia»*.
- **La vía de al lado.** El dominio que vigila tiene, en sus scripts, una guarda que se
  niega a actuar con una identidad ajena — escrita por él mismo. **Redactó a mano un
  procedimiento que la rodeaba**, sin darse cuenta, el mismo día.

En los cinco, ninguna alarma. En los cinco, el instrumento tenía razón según su propia
pregunta — y la pregunta había dejado de ser la que alguien creía estar haciendo.

## Cómo aplicarlo

**Al mudar el canon de transporte, la adhesión no termina en retirar la maquinaria manual:
termina cuando cada instrumento declara contra qué referente mide y con qué vocabulario.**
Tres actos, y el tercero es el que se salta:

1. **Reapuntar el referente** — y decirlo en el reporte, no sólo en el código.
2. **Revisar el vocabulario del registro**: por cada columna, preguntar *«¿este campo
   fusiona dos hechos que antes eran uno?»*. Si la respuesta es sí, se parte **antes** de
   volver a medir; reapuntar el referente sin partir la columna deja el falso negativo
   intacto.
3. **Enumerar los caminos que NO pasan por el instrumento** — procedimientos escritos a
   mano, apéndices, instrucciones para otro. Una guarda que sólo vive en el código no
   gobierna la prosa que la rodea.

**Y la regla de acotación, que es la que da la señal:** el tamaño de lo que un instrumento
se calla **no se pregunta al instrumento**. Se le pregunta al destino — una lista que hace
el otro lado. Si nadie del otro lado la hizo, el número que tienes es un piso, no un total,
y se reporta como piso.

## Cómo verificar

- **Debe pasar:** tras la mudanza, cada instrumento reporta contra qué referente midió y en
  qué fecha, y cada columna del registro expresa un solo hecho.
- **Debe seguir fallando:** un reporte que dice *«N pendientes»* **sin adjuntar la lista de
  los N** se marca como no auditable — una resta sobre una intersección que nadie midió no
  es una medición, aunque el número sea correcto.
- **Y el caso que debe seguir siendo válido:** un instrumento que mide un corpus local a
  propósito, con su referente declarado. El defecto no es medir lo local: es medir lo local
  **con el vocabulario de lo remoto**.
