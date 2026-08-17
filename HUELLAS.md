# Huellas del linaje de la plantilla

Tabla md5 → versión conocida. La consume el preflight del salto de versión: una copia
local que no case con ninguna fila **elegible** fue editada a mano, derivó, o es una
versión de la que nadie guardó huella — y eso se resuelve **antes** de hacer upgrade.

> [!important] En la era git, la huella vigente no vive en esta tabla
> Desde el corte 3.0 el canon es un repositorio: **el master cambia con cada parche
> fusionado**, así que una huella fija de "la v3 vigente" quedaría vieja en el siguiente
> merge. Esta tabla **congela el pasado** — sirve para identificar QUÉ versión tiene una
> copia vieja. El presente se verifica de otra forma: **contra el HEAD del canon remoto,
> recalculando ambos lados en el momento** — nunca contra una copia local o una réplica
> de red, que pueden estar divergidas y darse la razón entre sí.

> [!warning] El linaje mapea huella→versión — NUNCA dominio→versión
> La versión VIGENTE de un dominio se lee de la **fila de cierre de su último upgrade**,
> nunca de campos de nacimiento (`origen_plantilla:`) ni de frontmatters declarados: un
> campo de nacimiento **no cambia por diseño**, y leerlo como estado hace ver viejo a un
> dominio al día. Caso medido el 2026-08-16: un dominio en v2.0 verificada por artefacto
> fue leído como v1.3 porque el lector tomó su línea de nacimiento por su estado. Por lo
> mismo, cada fila de abajo que dependa de un registro **dice de qué campo salió**.

## El linaje

| md5 | versión | atestada por |
|---|---|---|
| `b4f2a62808605c1b9f7f07b03ddb09e9` | v1.4 | respaldo del master |
| `1f7344f9901d7881fd136dff257fc166` | v1.5 | respaldo del master |
| `838c37b8548291c72c5119d17528abad` | v1.6 | respaldo del master |
| `7275ff182822eed71e79f7386539fc74` | v1.7 | respaldo del master |
| `865eaaf9e6b4cb5d2996043d46132b9d` | v1.9 | respaldo del master |
| `35ab6e6768b9384a9154409b7b85eaf2` | v1.11 | respaldo del master |
| `f8147361afc4a511be703214cd85f74c` | v1.12 | respaldo del master |
| `917a8b714b91bd544fa69f8ab09ef219` | v1.13 | respaldo del master |
| `510a6a8b98b1f507d7ff52831a085573` | v1.17 | respaldo del master |
| `364cc9166e75159ccffb3bdfa17965d2` | v1.19 | respaldo del master |
| `38988d424b25ba2b7ccd1e80b67fb92e` | v1.22 | respaldo del master |
| `e40fd617d236015cf2a48e269b234757` | v1.23 | respaldo del master |
| `5175517e015205ec501a82ac0635c746` | v1.24 | respaldo del master |
| `7a0e33982bddf79c6f6310ab7f06aad5` | v1.25 | respaldo del master **y** el registro de una instancia — validación cruzada, coinciden |
| `ec18b0566f0a678c63aab425ac428cad` | v1.26 | respaldo del master |
| `10c745a8cf6b7eabb5c9368832e063ab` | v1.27 | respaldo del master |
| `076e32607308a267cadaeffa1cd812fd` | v1.28 | el master vivo al momento del corte |
| `c23a724500f963aeb5ef95ee5e3d6832` | v1.3 | el campo `origen_plantilla:` del registro de una instancia — **campo de NACIMIENTO, no de estado**: dice qué plantilla la parió, nunca su versión vigente. Y desde el 2026-08-16, **también un artefacto medido**: el respaldo `pre-v2` de esa instancia casa con esta huella y es el **único ejemplar conocido de la v1.3** (ningún respaldo del master anterior al 2026-08-05 existe). No es «sin respaldo»: es «cuídalo — no hay otro» |
| `02d578cf9c91345869be7efde037c180` | v1.18 | **solo una copia local, y por campo DECLARADO** (su frontmatter dice v1.18 — sin artefacto independiente que lo confirme). Los respaldos del master saltan de v1.17 a v1.19 — el preflight debe tratarla con la opción de diff |
| `b7c51925e63af917c805dcafb1c19b6a` | v2.0 | respaldo del master |
| `f132843ae45aacf6ffb0e28e2620dd2a` | v2.1 | respaldo del master |
| `2c9f8a2e77269d257befcab2fb80d049` | v2.2 | respaldo del master |
| `0fdeaa3bf5a0b8f6ffde3a4cb2d67249` | v2.3 | respaldo del master |
| `f136bb9a53146958c5c1a7f9ae703906` | v2.4 | respaldo del master |
| `1b55797a13658809bf152da3743df861` | v2.5 | respaldo del master |
| `828a610418e8e6b8b72805cba707838d` | v2.6 | respaldo del master |
| `9266c78e87a693f48c6348a2432dcd2d` | v2.7 | respaldo del master |
| `1ec18ec39926db7ed8ab2740fa00cd2a` | v2.8 | respaldo del master |
| `e46a2e9695054f6c07fa20fe7eec4c60` | v2.9 | respaldo del master |
| `a1f73fada5c8c71cdb96e9b198030ce4` | v2.10 | respaldo del master |
| `79971c4cc5164d7a068f95af7d943774` | v2.11 | respaldo del master — publicada por una instancia al incorporar sus dos parches del 2026-08-12 |
| `67fc4260745654e301cde5bf117c58d0` | v3.0 ~preliminar~ | **borrador — NO ELEGIBLE para casar en preflight.** El linaje lo daba por «nunca liberado»; MEDIDO el 2026-08-16 que al menos un dominio hizo upgrade a esta huella el 2026-08-12 y su registro lo atesta. Quien case aquí: ver «huellas huérfanas», abajo |
| `0a301cc775140ae47e6851ca738a1a8b` | v3.0 ~preliminar~ | **borrador nunca liberado — NO ELEGIBLE para casar en preflight** (llegó a marcarse v3.1 y se revirtió: la mayor se armoniza dentro de sí en vez de encadenar menores) |
| `84a950eccdb84047aa3fd6bbd473f2a8` | **v3.0** | el corte de la mudanza a git, armonizado, 2026-08-13. **Última huella congelada del linaje**: desde aquí el master vive en el repo y su huella vigente es la de HEAD, recalculada |

**Versiones sin huella conocida:** v1.0–v1.2, v1.8, v1.10, v1.14–v1.16, v1.20, v1.21.
Una copia que declare una de éstas cae en el modo de fallo *«versión declarada sin huella
en el linaje»* del preflight, con sus opciones.

## Huellas huérfanas conocidas — medidas, no en el linaje

| md5 | qué se midió |
|---|---|
| `aec3a85e6a526ed0abae3573c268c805` | Copia del dominio de origen y su espejo de red, idénticas entre sí y **fuera del linaje**, con frontmatter que declara v3.0 con confianza. INFERIDO (no medido): deriva del borrador tras la armonización del corte. Es el caso ejemplar de dos advertencias del preflight v3: **el frontmatter no es evidencia de versión**, y **una copia y su réplica pueden darse la razón estando ambas huérfanas** |
