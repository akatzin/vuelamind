---
title: Salto menor a v3.10 — el cierre usa vecinas, la instantánea deja la carpeta temporal y el control remoto sale del canon
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — REQUIERE los artefactos de la v3.5
---

> [!danger] De dónde tienes que venir: REQUIERE la v3.5
> El master de este salto nombra `/vuelamind-learn`, que instala la v3.5. Su master ya incluye de
> la v3.6 a la v3.9.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.10

> [!important] Este salto pide reinstalar un skill
> Traer el master no basta: el skill `vuelamind-commit` cambió. Si no lo reinstalas, tu cierre
> sigue haciendo el barrido del radio a mano, sin síntoma.

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `skills/vuelamind-commit.md` | El barrido del radio (quién enlaza una nota y a quién enlaza ella) lo hace `herramientas/vecinas.py`, en vez de un `grep` del nombre | **Reinstalarlo** |
| `herramientas/vecinas.py` | Nuevo. Lleva un registro de uso **por vault**, para decidir si sirve | Si usabas una copia propia, usar la del canon |
| `herramientas/instantanea_vault.py` | Reporta las notas que **se mudaron** de carpeta. Guarda su copia **fuera de la carpeta temporal**, que el sistema borra sola | Nada, si usas la del canon: la copia se muda sola la primera vez |
| `vuelamind-rc`, `vuelamind-rc-update` | Salieron del canon con el puente: el canon pasa de 13 skills a 11 | Quitarlos, o declararlos locales |
| `MARCO_Inicial.md` | `version: 3.10`. El paso del radio nombra `vecinas.py`, y el de releer dice cuándo se toma la copia: al terminar el cierre anterior | Traerlo |

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.10`. Si tu copia está
   modificada, respáldala antes.

2. **Reinstala `vuelamind-commit`**: copia `skills/vuelamind-commit.md` a donde tu instalación
   guarde los comandos. Después comprueba que no quede deriva:

   ```sh
   python3 herramientas/comprobar_skills.py
   ```

3. **Si tenías `vuelamind-rc` o `vuelamind-rc-update`**, quítalos o decláralos locales. Lo que ya
   corre sigue funcionando; lo que se pierde son las actualizaciones. Ver *«Fuera de la cadena»* en
   `UPGRADE.md`.

4. **Si usabas una copia propia de `vecinas.py`**, usa la del canon. Su registro nuevo es
   `.vecinas-uso-<nombre de tu vault>.tsv`, en la carpeta que contiene tu vault. **El registro viejo
   (`.vecinas-uso.tsv`) no se migra**: no dice de qué vault viene cada fila, y si esa carpeta tiene
   varios vaults, sus corridas se mezclaron. Se deja como histórico.

5. **Si usabas una copia propia de la instantánea**, compárala antes de pasarte: corre las dos con
   `diff` sobre tu vault. Si dan lo mismo, cambia las claves `antes_de_medir` y
   `despues_de_escribir` de tu manifiesto al `.py` del canon, y retira la tuya. Para no perder la
   relectura del cierre siguiente, copia tu copia actual a la ruta donde la busca el canon:

   ```sh
   python3 -c "import sys,pathlib; sys.path.insert(0,'herramientas'); import instantanea_vault as i; print(i.donde(pathlib.Path('<tu vault>').resolve()))"
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md                  # version: 3.10
python3 herramientas/comprobar_skills.py               # sin deriva
python3 herramientas/vecinas.py --informe <tu vault>   # corre, y cuenta solo tu vault
python3 herramientas/instantanea_vault.py diff <tu vault>
```

El último **no** debe decir «NO HAY INSTANTÁNEA», salvo la primera vez que se usa en un dominio.

*Medido en la casa que vigila el canon, el 2026-10-04: su instantánea propia y la del canon dieron
el mismo diff, línea por línea, antes de retirar la propia.*
