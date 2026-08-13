---
description: Prepara un proyecto nuevo con el marco de trabajo — crea la estructura en el repositorio, deja el instalador listo y entrega los pasos finales. Solo pregunta el nombre.
---

# /vuelamind — arrancar un dominio nuevo con el marco

Prepara todo lo **mecánico** de un proyecto nuevo para que luego se inicialice con el marco. Lo que requiere criterio —la entrevista, el transporte, qué es confidencial— **no** se decide aquí: se decide al inicializar.

> [!important] Este comando NO inicializa el marco
> Solo deja el andamio puesto. La inicialización ocurre después, en una sesión
> abierta **dentro** del proyecto nuevo, porque las memorias que genere la
> entrevista tienen que aterrizar en la memoria de ese dominio y no en la de
> éste.

## Lo único que se pregunta

**El nombre del dominio**, en minúsculas y sin espacios (`tesis`, `taller`, `mudanza`). Todo lo demás sale de convención.

Si vino como argumento (`/vuelamind taller`), úsalo sin volver a preguntar.

De ese nombre se derivan, tomando `$BASE` del **repositorio de dominios** (ver abajo):

| | Ruta |
|---|---|
| Andamiaje, repositorio | `$BASE/proyectos/<nombre>/` |
| Andamiaje, local | `~/proyectos/<nombre>/` |
| Conocimiento, repositorio | `$BASE/vaults/<nombre>/` |
| Conocimiento, local | `~/vaults/<nombre>_local/` |

Vaults y andamiaje viven separados a propósito: el conocimiento es del dominio, el andamiaje es de la herramienta. Las rutas de arriba son la convención por defecto — **cada instalación declara las suyas** y lo único que no se negocia es la separación.

### De dónde sale `$BASE`, y por qué no está escrito aquí

Este comando es el **arranque en frío**: crea dominios, así que vive en el nivel personal y no dentro de ninguno. Por eso **no puede hardcodear el repositorio de un usuario concreto** — si lo hiciera, dejaría de servir en cuanto cambiara la instalación, y sería el mismo defecto que obligó a bajar `/checkpoint` al proyecto el 2026-08-11.

Búscalo en este orden, y **no lo inventes**:

1. **Las memorias del proyecto**, que suelen traer la ruta del repositorio y el acceso.
2. Un dominio ya instalado en esta máquina: la ruta vive en su documentación del marco.
3. **Pregúntale al usuario.** Crear un dominio en el sitio equivocado es más caro que preguntar.


## Qué hacer

### 1. Comprobar que no existe ya

```bash
ssh <acceso al repositorio> 'ls -d "$BASE/proyectos/<nombre>"' 2>/dev/null
```

**Si existe, detente y avisa.** No sobrescribas: puede haber trabajo dentro. Ofrece continuar con otro nombre o revisar lo que hay.

### 2. Localizar la fuente del marco

En este orden, y **no la reescribas de memoria** — cópiala:

1. La copia local del canon, si esta máquina la tiene (un clon del repositorio de vuelamind)
2. Si no, del repositorio remoto que la instalación declare

Si no aparece en ninguno de los dos, **detente**: sin la plantilla no hay nada que instalar, y reconstruirla de memoria produciría una versión distinta de la que ya está probada.

### 3. Crear la estructura

En el repositorio:

```bash
ssh <acceso al repositorio> '
B=$BASE
P="$B/proyectos/<nombre>"
V="$B/vaults/<nombre>"
mkdir -p "$P/memory" "$P/.claude/skills" "$V/Entidades"
chown -R <usuario>:<grupo> "$B/proyectos"
chown -R <usuario>:<grupo> "$V"
chmod -R 777 "$P" "$V"'
```

Copia después `MARCO_Inicial.md` y `README.txt` a `$P/` con `scp`, y ajusta `chown nobody:users` y `chmod 666` sobre los archivos.

> [!warning] No crees la copia local todavía
> El proyecto local va **en la máquina donde se vaya a trabajar**, y esa
> decisión no la toma este comando. Crearlo aquí "por si acaso" ya salió mal
> una vez: se creó en el Mac un proyecto que iba a vivir en otra máquina, y hubo
> que borrarlo. El identificador interno se deriva de la ruta, así que un
> proyecto creado en la máquina equivocada no se aprovecha.

### 4. Escribir el `CONTEXTO_INICIAL.md` del dominio

Va en `$P/`. Es lo que evita que la sesión que inicializa repita lo ya resuelto. Debe contener, y nada más:

- **Las cuatro rutas** de la tabla de arriba.
- **Que el Bloque E de la entrevista ya está resuelto** y hay que saltárselo, igual que la sección 1.0 de la Fase 1.
- **La advertencia de precedencia:** en Claude Code el nivel personal (`~/.claude/`) **ensombrece** al del proyecto. Un comando del dominio puesto en su proyecto no corre si existe uno homónimo arriba — y falla en silencio.
- **Que la reconciliación NO se escribe desde cero** (cambió el 2026-08-11): el método vive en el motor global `/vuelamind-commit`, y lo que el dominio genera es su **manifiesto** — `.claude/vuelamind-commit.manifiesto.md` en su proyecto. La Fase 1.4 de la plantilla trae el contrato. Solo si la máquina no puede tener el motor —equipo administrado sin la carpeta personal sincronizada— se copia el método completo, y esa copia queda anotada como tal, porque deja de recibir mejoras.
- **Los pasos finales** del punto 6, tal cual.
- **Lo que sigue sin decidir**, explícito: los Bloques A, B, C, D y F; desde qué máquina se trabaja; y el transporte.

**Y dejar sembrado el esqueleto del manifiesto** en `$P/.claude/vuelamind-commit.manifiesto.md`, con las claves del contrato y `<pendiente de la entrevista>` en cada valor que aún no se sepa — la entrevista de la Fase 0 lo completa. Un esqueleto con huecos visibles vale más que un archivo ausente que nadie recuerda crear.

### 5. Verificar lo creado

No lo des por hecho: lista las rutas y confirma que los archivos llegaron con su tamaño. Un `mkdir` que falló en silencio deja al usuario siguiendo pasos sobre algo que no existe.

### 6. Entregar los pasos finales

Preséntalos así, adaptando `<nombre>`, y **di explícitamente cuáles son suyos**:

```
1. Crear en la máquina donde vayas a trabajar:
      ~/proyectos/<nombre>/          y      ~/vaults/<nombre>_local/

2. Traer el contenido del repositorio a esas dos carpetas
   (scp, o el transporte que decidas después).

3. Abrir Claude Code con cwd en ~/proyectos/<nombre>
   — eso crea el identificador interno del proyecto.

4. Sustituir  ~/.claude/projects/<identificador>/memory
   por un symlink hacia  ~/proyectos/<nombre>/memory
   Verificar con  stat -L  en ambas rutas: el inode debe coincidir.

5. Decir dentro de esa sesión:
      "lee CONTEXTO_INICIAL.md y MARCO_Inicial.md e inicializa este marco"

6. Responder la entrevista. Ahí se decide el transporte, y si toca,
   se genera rsync_project.sh (Fase 1.3 del marco).

7. Escribir una memoria, cerrar la sesión y abrir otra:
   si se carga en contexto, el ciclo quedó confirmado de punta a punta.
```

> [!danger] El orden del paso 4 no es negociable
> El symlink va **antes** de inicializar. La entrevista escribe memorias, y si
> el enlace no está puesto, aterrizan en la ruta que impone la herramienta y no
> viajan nunca. Recolocarlas después es más trabajo que ponerlo antes.

## Qué NO hace este comando

- **No inicializa el marco.** Eso es una sesión aparte, dentro del proyecto.
- **No crea nada en la máquina actual**, salvo que el usuario confirme que aquí se va a trabajar.
- **No decide el transporte.** Réplica automática, script de empuje o montaje directo se eligen en la entrevista, con la máquina ya conocida.
- **No copia comandos de otro dominio.** Cada uno escribe los suyos.

## Al terminar

Reporta **qué se creó y dónde**, separando lo que quedó en el repositorio de lo que le toca hacer a él. Y si algo no se pudo verificar, dilo — no lo reportes como hecho.
