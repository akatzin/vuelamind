---
title: Salto menor a v3.9.3 — el aprendizaje es local, la réplica sale del canon y dos skills se retiran
tipo: plantilla ejecutable
para: dominios en la línea base v3 — desde la v3.0 ya no hace falta la v3.5
---

> [!note] De dónde tienes que venir
> **De cualquier dominio en la línea base v3.** La v3.5 deja de ser requisito: lo que traía —el
> buzón de aprendizaje y `/vuelamind-learn`— se retira en este salto.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.9.3

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `skills/vuelamind-learn.md` | Pasa a `deprecated/skills/`. **El aprendizaje es local**: los parches se escriben en tu vault y ahí se quedan; no hay camino al canon | Quitarlo (paso 2) |
| `skills/vuelamind-accidente.md` | Pasa a `deprecated/skills/`. El canon pasa de **10 skills a 8** | Quitarlo (paso 2) |
| `vuelamind-commit`, `vuelamind-load`, `vuelamind-help` | Sin réplica ni envío de parches: el cierre termina en reportar | Reinstalarlos (paso 2) |
| La réplica | Sale del canon: la Fase 1.0.b, la 1.3 (`rsync_project.sh`), los chequeos de llave y de respaldo de `init_<host>.sh` y el paso «Confirmar la réplica» del cierre. Al terminar la entrevista se dice que llevar el dominio a otro lado corre por cuenta de la persona | Decidir qué haces con lo tuyo (paso 3) |
| El manifiesto | Ningún comando del método lee ya `replica`, `aportar_a`, `buzon_aprendizaje` ni `learning_*` | Quitarlas o dejarlas (paso 4) |
| `learning.vuelamind.ai` | Apagado | Dejar de mandarle (paso 4) |
| `CONTRIBUTING.md` | Se borra: el canon no recibe aportaciones | Nada |
| `MARCO_Inicial.md` | `version: 3.9.3`. La Fase 1 se renumera: la antigua 1.4 (manifiesto) es la **1.3**, y la 1.5 (comandos) es la **1.4**. Y además: la presentación al nacer, una pregunta por mensaje, la duración real de la entrevista, el traspaso como lo último de la sesión que nace, el dominio nunca dentro de la copia del canon, e instalar desde la terminal si el aislamiento lo impide | Traerlo (paso 1) |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.9.3`. Si tu copia está
   modificada, respáldala antes.

2. **Pon al día los comandos**: quita los dos que se retiran y reinstala desde `skills/`.

   ```sh
   rm ~/.claude/commands/vuelamind-accidente.md ~/.claude/commands/vuelamind-learn.md   # o la ruta de skills de tu instalación
   cp skills/vuelamind-*.md ~/.claude/commands/
   python3 herramientas/comprobar_skills.py   # sin deriva
   ```

3. **Si tu dominio replicaba con el método** —un `rsync_project.sh`, chequeos de respaldo en
   `init_<host>.sh`—, el método ya no los genera ni los mira. **Siguen funcionando si los dejas**, y
   desde ahora son tuyos. Si quitas el empuje, quita también la llamada en `despues_de_escribir`.

4. **En el manifiesto**, quita `replica`, `aportar_a`, `buzon_aprendizaje` y `learning_*`, o déjalas:
   ninguno de los comandos del método las lee. Los parches que tenías sin aportar **se quedan en tu
   vault como están**; no hay a dónde mandarlos.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md      # version: 3.9.3
python3 herramientas/comprobar_skills.py   # sin deriva, y sin vuelamind-accidente ni vuelamind-learn
```

**Nada se borró:** los dos skills siguen en `deprecated/skills/`. No se instalan ni se corren desde
ahí.
