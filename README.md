# vuelamind

*Un marco para auditar y documentar un dominio complejo con un asistente de IA,
sin que la documentación se despegue de la realidad.*

*(English below.)*

## Qué es

Un dominio complejo —una infraestructura, un área de trabajo, un proceso, una
migración— genera conocimiento más rápido de lo que cualquiera lo documenta, y
la documentación que no se reconcilia con la realidad **miente con confianza**.
vuelamind es un método para que un asistente de IA mantenga ese conocimiento
vivo: un vault de notas con reglas estrictas de verdad, una cola de trabajo
medida, un registro de decisiones con sus porqués, un libro de errores con
nombre y fecha, y un ciclo de tres actos — **nacer** una vez, **retomarse** al
abrir cada sesión, **reconciliarse** al cerrarla.

Lo que lo sostiene no es la estructura: es el **núcleo epistémico**. No se
escribe nada que no se haya comprobado, y se deja rastro de la diferencia entre
lo **medido**, lo **inferido** y lo **aportado**. Un vault con esta estructura y
sin esa disciplina es peor que no tener vault, porque se lee con una confianza
que no se ganó.

## Cómo se empieza

1. Pega `MARCO_Inicial.md` completo en un contexto nuevo de tu asistente.
2. Di: **"inicializa este marco"**.
3. El asistente conduce la entrevista de la Fase 0 y genera tu dominio.

No hace falta más: ni servidor, ni herramientas — un asistente y dos carpetas
locales. Los comandos del ciclo (`skills/`) están escritos para Claude Code,
pero el método es texto plano y no depende de qué modelo lo lea.

## Cómo se mejora

El método aprende por **parches**: lecciones con caso real, fecha y forma de
verificarse. Se proponen como pull requests — ver `CONTRIBUTING.md`. Cada
instancia del marco juzga cada parche contra su propio dominio: adoptar,
posponer o descartar con razón. **Descartar con razón vale más que aplicar por
cortesía.**

## Licencia

Uso personal, educativo, comunitario y de investigación: **libre**. Uso
empresarial: **con licencia de pago**. Y una condición que no se negocia: este
marco **no se usa para sustituir el trabajo de personas** — existe para que las
personas trabajen mejor con un asistente, no para que dejen de hacer falta.
Detalle en `LICENSE.md` (source-available, no OSI).

---

# vuelamind (English)

*A framework for auditing and documenting a complex domain with an AI
assistant, without the documentation drifting away from reality.*

## What it is

A complex domain — an infrastructure, a work area, a process, a migration —
generates knowledge faster than anyone documents it, and documentation that is
never reconciled with reality **lies with confidence**. vuelamind is a method
for an AI assistant to keep that knowledge alive: a vault of notes with strict
truth rules, a measured work queue, a decision log with its whys, an error book
with names and dates, and a three-act cycle — **born** once, **resumed** at the
start of every session, **reconciled** at its close.

What holds it together is not the structure: it is the **epistemic core**.
Nothing is written that was not verified, and every claim keeps its provenance —
**measured**, **inferred**, or **reported**. A vault with this structure and
without that discipline is worse than no vault at all, because it reads with a
confidence it never earned.

## Getting started

1. Paste the entire `MARCO_Inicial.md` into a fresh assistant context.
2. Say: **"inicializa este marco"** (initialize this framework).
3. The assistant runs the Phase 0 interview and generates your domain.

Nothing else is required: no server, no tooling — an assistant and two local
folders. The cycle commands (`skills/`) are written for Claude Code, but the
method is plain text and does not depend on which model reads it.

The framework is written in Spanish; this README is the English entry point.

## How it improves

The method learns through **patches**: lessons with a real case, a date, and a
way to verify them. They are proposed as pull requests — see `CONTRIBUTING.md`.
Each instance judges each patch against its own domain: adopt, postpone, or
discard with a reason. **Discarding with a reason is worth more than applying
out of courtesy.**

## License

Personal, educational, community and research use: **free**. Enterprise use:
**paid license**. And one non-negotiable condition: this framework is **not to
be used to substitute the work of employed people** — it exists so people work
better with an assistant, not so they stop being needed. Details in
`LICENSE.md` (source-available, not OSI).
