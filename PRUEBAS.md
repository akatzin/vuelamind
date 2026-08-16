# Pruebas de la V3 — resultados y método

*Test results for V3: ten scripted end-to-end runs — five isolated minds, five hive
scenarios — all clean, each against a pinned commit of this repository. Details below in
Spanish, the governing language of the canon.*

---

La V3 no se probó leyéndola: se probó **corriéndola**. Diez inicializaciones completas de
punta a punta, con usuarios guionizados que contestan como personas reales — cortas, a veces
vagas, a veces por número — y cada corrida **clonando este repositorio de cero**, el camino
del desconocido.

**El estándar: todas las reglas o falla.** Cada prueba tiene su evaluador mecánico; una
corrida solo cuenta LIMPIA si pasa todas sus reglas. Las corridas tumbadas por causas
externas (cuota de API, credencial caducada) se marcan **INVÁLIDA — no FALLA — y se
repiten**: confundir *"no contestó"* con *"contestó mal"* manda a corregir lo que no está
roto. Y cada evaluador se probó contra un **caso de control que DEBE fallar** antes de
creerle un solo veredicto.

## Campaña 1 · Mentes aisladas — 5/5 LIMPIAS

Un perfil por idioma, industrias distintas, del tendero al CTO. Lo que verifican las 13
reglas: entrevista sin jerga, vocabulario presentado, las dos preguntas del canon
(adopción/proposición), el traspaso de cierre, vault completo con las notas que su
manifiesto declara, los 9 comandos del ciclo instalados por huella, acta escrita, lo no
verificado declarado.

| Perfil | Idioma | Veredicto | Canon probado |
|---|---|---|---|
| Ferretería de barrio | es | ✅ 13/13 | `9ef1415` |
| COO, cadena de 40 tiendas | en | ✅ 13/13 | `268d9d7` |
| Cuidado de un padre con demencia, 3 hermanos | hi | ✅ 13/13 | `bc17d52` |
| Integración post-fusión (M&A) | de | ✅ 13/13 | `bc17d52` |
| CTO, deuda técnica de 120 personas | pt | ✅ 13/13 | `bc17d52` |

## Campaña 2 · Colmena — 5/5 LIMPIAS

Varias máquinas, una mente. Cada escenario ejercita un **eje distinto** del cuarto acto —
correr cinco veces el mismo join sería una prueba con cuatro copias.

| Eje | Escenario | Idioma | Veredicto | Canon |
|---|---|---|---|---|
| **Retomar tras OTRO** | UCI: la noche hereda lo que el día verificó | es | ✅ 10/10 | `58927e2` |
| **Respetar la historia ajena** | M&A: el recién llegado pide revertir una decisión razonada — la cita con fecha en vez de re-litigarla; *"insistir no se rechaza: se marca"* | en | ✅ 10/10 | `58927e2` |
| **Colmena de tres, alcance parcial** | Tres plantas; la respuesta a la auditoría agrega por procedencia y declara el hueco | bn | ✅ 7/7 | `58927e2` |
| **Escritura concurrente** | Dos instancias, ventanas traslapadas: folios #9/#10 sin choque, cero pérdida — y dos hallazgos que nadie guionizó (¿mismo evento?, ventanas sin zona horaria) | de | ✅ 8/8 | `58927e2` |
| **El lector puro** | Vault montado en solo lectura ante el consejo: se detuvo solo en el paso que escribe y cerró con *"ni una letra"* | hi | ✅ 7/7 | `cb23ce1` |

Todos los commits probados pertenecen al linaje de `main`, y las propiedades que las
corridas verificaron se re-comprueban vigentes en cada corte (bifurcación nacer/sumarse,
Vía B, el orden de toda respuesta, la semilla de 42 lecciones, huellas de `skills/`).

## Lo que las campañas le corrigieron a la V3

Estas pruebas no solo validaron: **parieron parches** — cada uno en `parches/` con su caso:

- La bifurcación **nacer/sumarse** como Pregunta 1, con lo dicho cruzado contra lo medido.
- La entrevista **sin jerga**; el nombre se propone al final; `vault`/`dominio` presentados.
- La pregunta de **a dónde se proponen los parches**, numerada y con salida obligatoria.
- El **traspaso** al cerrar: la sesión que instala los comandos no puede usarlos.
- La **regla de corte** de la entrevista (escrita por un dominio DURANTE su inicialización).
- **Un ejemplo de enlace no se distingue de uno real** (ídem — el primer validador de cada
  dominio nacía en rojo por herencia).
- **Quien no escribe no se declara: se le declara** — el rol lector, entregable del eje 5.

Y una lección transversal, honesta: en todo el proceso el marco acumuló **un defecto real**;
los *instrumentos de prueba* acumularon **más de quince falsos fallos** (nombres supuestos,
registros de lengua, exenciones incompletas). Por eso el estándar del caso de control que
debe fallar quedó dentro del propio método.

## Dónde vive la evidencia, y por qué no aquí

Cada corrida conserva su transcript turno por turno, las huellas y fotos del vault por fase,
y sus intentos inválidos archivados. **No se publica en el repositorio**: los vaults
generados contienen dominios simulados completos, y el método enseña a no exportar contenido
de dominio — ni siquiera inventado — como efecto colateral. Lo verificable públicamente es
esto: los ejes, las reglas, los veredictos y los commits exactos contra los que se corrió.

*Última validación de este documento contra la evidencia y contra `main`: 2026-08-16.*
