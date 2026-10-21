---
title: Salto menor a v3.12.0 — un archivo por pendiente, y un script que hace cumplir el cierre
tipo: plantilla ejecutable
para: dominios en la v3.11.0
---

> [!note] De dónde tienes que venir
> **De la v3.11.0.** Desde una versión anterior, corre primero `UPGRADE_v3.11.0.md`.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.12.0

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `MARCO_Inicial.md` | `version: 3.12.0`. La cola pasa a un archivo por pendiente (`pendientes/<folio>.md`) con un índice generado; el ciclo de vida del pendiente y la Fase 3 los comprueba `herramientas/pendientes.py` | Traerlo (paso 1) |
| `herramientas/pendientes.py` | Nuevo: `nuevo`, `cerrar`, `indice`, `revisar` y `migrar` | Nada: viene con el canon |
| `skills/vuelamind-commit.md` y `skills/vuelamind-load.md` | Corren `pendientes.py revisar`; el cierre cierra con `cerrar` | Reinstalarlos (paso 2) |
| `skills/vuelamind-export.md` | Declara la pieza `pendientes` | Reinstalarlo (paso 2) |
| La cola del dominio | De un archivo a una carpeta | Migrarla (paso 3) |
| El validador del dominio | Llama a `pendientes.py revisar` | Agregarlo (paso 4) |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.12.0`. Si tu copia del
   master está modificada, respáldala antes.

2. **Reinstala los tres skills**, desde la raíz del canon:

   ```sh
   cp skills/vuelamind-commit.md skills/vuelamind-load.md skills/vuelamind-export.md ~/.claude/commands/   # o la ruta de skills de tu instalación
   ```

3. **Migra la cola.** Con dos o más instancias que escriben, con el candado del cierre puesto
   (`.cierre.lock/`, Fase 3). Desde la raíz del canon:

   ```sh
   python3 herramientas/pendientes.py migrar <vault>              # ensayo: cuenta, y comprueba que no se pierde ninguna línea
   python3 herramientas/pendientes.py migrar <vault> --escribir   # escribe; la cola de antes queda en Pendientes.md.antes-migrar-<fecha>
   ```

   Con `--cola` y `--archivo` si el manifiesto les da otro nombre a la cola y al archivo de
   cerrados. Los cerrados que estaban en la cola llevan `migrado::` y no se les exige párrafo;
   los folios del archivo de cerrados de antes cuentan como existentes. Si el ensayo avisa de
   enlaces a una sección de la cola (`[[Pendientes#…]]`), cámbialos a `[[pendientes/<folio>]]`.

4. **Que el validador del dominio llame a `pendientes.py revisar`** y salga en rojo si éste sale
   con 1. Si el validador contaba las casillas de la cola, ese chequeo se quita: ahora lo hace
   `revisar`.

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.12.0
python3 herramientas/comprobar_skills.py; echo $?      # 9 al día, sin deriva, y 0
python3 herramientas/pendientes.py revisar <vault>; echo $?   # 0
grep -c '^### - \[' <vault>/Pendientes.md               # 0: el índice ya no lleva pendientes dentro
```

**Nada se borró:** la cola de antes queda en `Pendientes.md.antes-migrar-<fecha>`, y el archivo de
cerrados de antes no se toca.
