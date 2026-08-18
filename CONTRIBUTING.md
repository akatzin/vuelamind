> [!important] FROZEN until v3.5 (2026-08-18) · CONGELADO hasta la v3.5
> The patch cycle is suspended: do not open patch PRs for now. Keep writing your error
> book locally — v3.5 replaces this flow with a central inbox where a watcher does all
> the ceremony. / El ciclo de parches está suspendido: no abras PRs de parches por ahora.
> Sigue escribiendo tu libro de errores en tu casa — la v3.5 reemplaza este flujo con un
> buzón central donde el vigía hace toda la ceremonia.

# Contributing to vuelamind

*Español abajo.*

The method improves through **patches**: corrections discovered by using it, with a real
case and a way to verify them. This repository is the canon; patches are proposed here as
pull requests.

**Where "here" is, exactly, is declared in [`config.yml`](config.yml)** — repository, branch
and site, written once so nothing else has to repeat them. That file also holds the two
defaults: a domain **consumes** patches from the canon by default (read-only, it exposes
nothing about the domain), and when a domain chooses to **publish**, the canon is the default
destination. Publishing itself stays opt-in — a patch carries its case, and the case says
something about the domain that wrote it. What you send cannot be un-sent.

## What a patch is

A file in `parches/` named `YYYY-MM-DD-short-description.md` — the date is the date of
**discovery** — with this frontmatter:

```yaml
---
version: 1
origen: <your handle, or "anonimo">
---
```

And four sections: **What it corrects** (the defect, in one sentence), **How it was
discovered** (the real case, with a date — this is what stops someone reverting it later
for seeming arbitrary), **How to apply it** (the generic text), and **How to verify** —
including the case that must **keep failing**.

## The only test that matters

**Rewrite your lesson with every proper noun replaced by a generic one. Is it still true
and useful?** If yes, it belongs to the method. If it is only true with your names in it,
it belongs to your domain — keep it there.

Whoever reviews your PR applies that same test and no other. They **do not judge whether
your case is true** — they cannot; it happened in your domain. The truth of the case is
judged by each domain that adopts the patch, against its own evidence, with three possible
verdicts: adopt, postpone, or **discard with a reason** — and discarding with a reason is
worth more than adopting out of courtesy.

## Before opening the PR: anonymise the WHOLE, not the fragment

Two innocent details can identify your operation **together**, and what links them is
usually a proper noun left in another file for looking harmless. Remove names of people,
organisations, teams, hosts, paths, IPs and domains; **keep the mechanism of the error, the
measured consequence, and the signal that gave it away** — that is what teaches. Publishing
is irreversible: the review happens before the push, not after the first report.

## You need an account to propose — and nothing breaks if you do not have one

**Consuming the method is free and anonymous.** Anyone can clone the canon and receive every
correction without registering anywhere. **Reading does not require an account.**

**Proposing does**, because a pull request needs an identity on the platform. If you do not
have one — or do not want one — you are not out of the method, only out of the return
channel:

- You keep **pulling** every published correction, like everyone else.
- You **write your patches anyway**, in your own `parches/` folder, with their frontmatter
  and their four sections. Do not skip them for being unable to send them: they are your
  error book, and they matter most to the domain that paid for them.
- That local corpus is **your own legacy** — it accumulates what your domain learned, and it
  teaches the next instance that opens your vault.

**And it is not a closed door.** If you open an account later, those accumulated patches are
**still proposable as they are**: they carry the date, the case and the verification from the
day they were written. A patch does not expire for having waited.

## You do not have to contribute here

The framework can be consumed without sending anything back, and a domain can point its
`aportar_a` at **a different repository** — your own fork, your organisation's — or at
`ninguno`, keeping what it learns at home. A domain handling sensitive material may want
exactly that. **Writing the patch is a matter of honesty; where it goes is a matter of
transport.**

## What does not belong here

- Configuration or experience specific to one domain — that lives in each instance.
- Patches without a real case ("it occurred to me that…") — the method learns from mistakes
  that were paid for, not from opinions.
- Edits to a published patch's text without bumping its `version:` — the version is what
  tells other instances the original changed.

---

# Cómo contribuir a vuelamind

El método mejora por **parches**: correcciones descubiertas usándolo, con caso real y forma
de verificarse. Este repositorio es el canon; los parches se proponen aquí como pull
requests.

## Qué es un parche

Un archivo en `parches/` con el nombre `AAAA-MM-DD-descripcion-corta.md` —la fecha es la
del **descubrimiento**— y este frontmatter:

```yaml
---
version: 1
origen: <tu handle, o "anonimo">
---
```

Y cuatro secciones: **Qué corrige** (el defecto, en una frase), **Cómo se descubrió** (el
caso real, con fecha — es lo que evita que alguien lo revierta por parecerle arbitrario),
**Cómo aplicarlo** (el texto genérico) y **Cómo verificar**, incluido el caso que debe
**seguir fallando**.

## La única prueba que importa

**Reescribe tu lección sustituyendo todos los nombres propios por genéricos. ¿Sigue siendo
cierta y útil?** Si sí, es del método. Si solo es cierta con tus nombres puestos, es de tu
dominio — guárdala allá.

Quien revisa aplica esa misma prueba y ninguna otra: **no juzga la verdad de tu caso** —no
puede, pasó en tu dominio—. La verdad la juzga cada dominio que adopte el parche, contra su
propia evidencia, con tres veredictos posibles: adoptar, posponer o **descartar con razón**
— y descartar con razón vale más que adoptar por cortesía.

## Antes de abrir el PR: anonimiza el CONJUNTO, no el fragmento

Dos detalles inocentes pueden identificar tu operación **juntos**, y el que los une suele
ser un nombre propio que quedó en otro archivo por parecer inofensivo. Quita nombres de
personas, organizaciones, equipos, hosts, rutas, IPs y dominios; **conserva el mecanismo del
error, la consecuencia medida y la señal que lo delató** — eso es lo que enseña. Publicar es
irreversible: la revisión va antes del push, no después del primer reporte.

## Proponer pide una cuenta — y no pasa nada si no la tienes

**Consumir el método es libre y anónimo.** Cualquiera puede clonar el canon y recibir cada
corrección sin registrarse en ningún sitio. **Leer no requiere cuenta.**

**Proponer sí**, porque un pull request necesita una identidad en la plataforma. Quien no la
tenga —o no la quiera— no queda fuera del método, solo del canal de vuelta:

- Sigue **jalando** todas las correcciones publicadas, igual que el resto.
- **Escribe sus parches igual**, en su propia carpeta `parches/`, con su frontmatter y sus
  cuatro secciones. No se omiten por no poder enviarlos: son su libro de errores, y valen
  sobre todo para el dominio que los sufrió.
- Ese corpus local es **legado propio** — acumula lo que su dominio aprendió, y le enseña a
  la siguiente instancia que abra ese vault.

**Y no es una puerta cerrada.** Si algún día abres una cuenta, esos parches acumulados
**siguen siendo proponibles tal cual**: llevan fecha, caso y forma de verificarse desde el día
que se escribieron. Un parche no caduca por haber esperado.

## No estás obligado a contribuir aquí

El marco se puede consumir sin devolver nada, y un dominio puede apuntar su `aportar_a` a
**otro repositorio** —un derivado propio, el de tu organización— o a `ninguno`, guardando en
casa lo que aprenda. Un dominio con material sensible puede querer exactamente eso.
**Escribir el parche es una cuestión de honestidad; a dónde va es una de transporte.**

## Qué no va aquí

- Configuración o experiencia de un dominio concreto — eso vive en cada instancia.
- Parches sin caso real (*"se me ocurrió que…"*) — el método aprende de errores pagados, no
  de opiniones.
- Cambios al texto de un parche publicado sin subir su `version:` — la versión es lo que
  avisa a las demás instancias de que el original cambió.
