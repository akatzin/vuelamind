---
title: Salto menor a v3.9.2 — la mensajería entre instancias se depreca
tipo: plantilla ejecutable
para: dominios en v3.5 o posterior — REQUIERE los artefactos de la v3.5
---

> [!danger] De dónde tienes que venir: REQUIERE la v3.5
> El master de este salto nombra `/vuelamind-learn`, que instala la v3.5. Su master ya incluye de
> la v3.6 a la v3.9.1.
>
> *El mapa completo de saltos vive en `UPGRADE.md`.*

# UPGRADE a v3.9.2

> [!important] Si nunca instalaste el canal, este salto es solo traer el master
> El canal entre instancias era la v3.4, una rama **opcional**. Si tu dominio no la instaló, lo
> único que cambia para ti es el número de versión y una nota histórica.

## Qué cambia

| Pieza | Cambio | Qué te toca |
|---|---|---|
| `canal/` | Sale entero: servidor, cliente, disparador, instalador y su ejemplo | Si lo usabas, desarmarlo (paso 2) |
| `skills/vuelamind-mensajeria.md` | Sale. El canon pasa de **11 skills a 10** | Quitarlo, o declararlo local |
| `UPGRADE_v3.4.md` | Retirado: **no se corre**, porque instala piezas que ya no están | Nada |
| `MARCO_Inicial.md` | `version: 3.9.2`. La nota de la v3.4 dice que se retiró | Traerlo |

**Lo que no se va:** el buzón de aprendizaje (`/vuelamind-learn`) es otra pieza, sin relación con
el canal, y sigue igual.

## Cómo saltar

1. **Trae el canon** y comprueba que `MARCO_Inicial.md` dice `version: 3.9.2`. Si tu copia está
   modificada, respáldala antes.

2. **Si tu dominio usaba el canal, desármalo.** El servicio ya no está en pie: lo instalado no
   tiene a quién hablar y falla en cada intento.
   - El disparador: el `launchd`, `systemd` o tarea programada que lo corre.
   - Los ganchos de arranque que consulten el canal: fallarán en cada turno.
   - Las llaves del canal: solo servían para él.

3. **Quita el skill**, o decláralo local:

   ```sh
   rm ~/.claude/commands/vuelamind-mensajeria.md   # o la ruta de skills de tu instalación
   python3 herramientas/comprobar_skills.py        # sin deriva
   ```

## Cómo sabes que funcionó

Compruébalo en el disco, no de memoria:

```sh
grep -m1 '^version:' MARCO_Inicial.md      # version: 3.9.2
python3 herramientas/comprobar_skills.py   # sin deriva, y sin vuelamind-mensajeria
```

**La historia no se pierde:** cada archivo sigue en el historial de este repositorio, hasta el
commit anterior a su salida.
