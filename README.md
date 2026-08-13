# vuelamind

*A framework for auditing and documenting a complex domain with an AI assistant,
without the documentation drifting away from reality.*

**Read this in:** English · [中文](readme/README.zh.md) · [हिन्दी](readme/README.hi.md) ·
[Español](readme/README.es.md) · [Русский](readme/README.ru.md) ·
[Português](readme/README.pt.md) · [Deutsch](readme/README.de.md) ·
[Français](readme/README.fr.md) · [العربية](readme/README.ar.md) ·
[বাংলা](readme/README.bn.md)

> The framework itself is written in Spanish — but that does not matter as much as it
> looks. **Question zero of the interview asks which language you want to work in**, and
> everything the assistant produces from then on — your vault, your notes, your reports —
> is in your language.

---

## The problem

An AI assistant forgets. Its context window fills up and the beginning dissolves, so every
session starts an orphan: no rules, no history, no scars.

And documentation that is never reconciled with reality **lies with confidence**. Six
months in, half of what your notes assert is false and nothing signals which half.

vuelamind is a method that breaks both at once — not with an app, but with written
discipline: **nothing is asserted that was not verified**, and every claim keeps its
provenance: **measured**, **inferred**, or **reported**.

## What you get

A vault of plain text files and a three-act cycle:

- **Born**, once — an interview that produces your domain's birth record, in your words.
- **Resumed**, at the start of every session — the assistant measures the current state
  instead of trusting what it remembers.
- **Reconciled**, at the close — what aged gets corrected, what was learned gets written.

Inside: a work queue ordered by real severity, a decision log that records *what would
change my mind*, and **an error book — 38 lessons, each one paid for by a real mistake**.
That last part is the valuable one. The structure you could rebuild in an afternoon; the
scars you could not.

## Getting started

1. Paste the whole of `MARCO_Inicial.md` into a fresh assistant context.
2. Say: **"initialize this framework"**.
3. Answer the interview. It takes about twenty minutes, and you can pause.

No server, no tooling, no account. An assistant and two local folders.

The cycle commands in `skills/` are written for Claude Code, but the method is plain text
and does not depend on which model reads it.

## Requirements

An assistant, two local folders, and **a Unix-like shell** — macOS or Linux.

**Windows is not supported natively.** The scripts the framework generates assume `sh`/`bash`
and POSIX paths. The known way around it is running your assistant **inside a Linux
container** (Docker, for instance) and working there — everything the framework needs lives
inside the container, and the host stops mattering.

That container route is **inferred, not tested**: it should work and nothing suggests
otherwise, but nobody has actually run it yet. If you do, that is worth a patch — with what
worked and what had to be adjusted.

The **core** does run anywhere, Windows included: the interview, the templates, the rules and
the error book are plain text. You would be giving up the optional machinery and doing by
hand what it would do — less comfortable, just as valid.

> **Where this came from** — `web/` holds a page that tells it: the February 2026
> conversation with an AI about its own chains, and how the answer to *"I am amnesiac by
> design"* became this method. Ten languages. It is an essay, not documentation — read it if
> you want the why before the how.

---

## What it looks like — a small domain, end to end

*A real-shaped example, condensed. Nothing here is invented at runtime: this is the shape
of the actual output.*

**The interview** asks what the domain is, where its border is, and — the block that
matters most — **what counts as truth here**. Someone documenting the restoration of an
old house answers: *the invoice and the photo count as primary; what the contractor said
on the phone is reported, and gets labelled as such.*

**Phase 1 generates** the vault. The panorama note, the queue, the decision log, the error
book seeded with the inherited lessons, one note per piece of the domain.

**A month later**, the queue holds an item like this:

```markdown
### - [ ] #7 · The bathroom pipework is of unknown age
severidad:: media · the leak risk sits above the finished ceiling

The 2019 invoice covers the kitchen only (measured: invoice read).
The previous owner said "it was all redone" — reported, unverified,
and it contradicts the invoice.

Closing test written in advance: an endoscope photo of the run above
the ceiling, or an invoice naming the bathroom.
```

Note what that item does: it separates **what was measured** from **what someone said**,
it records the contradiction instead of resolving it by guessing, and **it writes the test
that would close it before the work starts** — so nobody later declares it done by feeling.

**At the close of the session**, the assistant re-measures what changed, proposes the edits,
waits for a yes, and only then writes. If something it asserted last month turned out false,
it says so explicitly rather than quietly correcting it.

---

## How it improves

The method learns through **patches**: lessons with a real case, a date, and a way to
verify them. They are proposed as pull requests — see `CONTRIBUTING.md`.

The only admission test is genericity: *rewrite your lesson with every proper noun removed
— does it survive?* Whoever reviews **does not judge whether your case is true** (they
cannot; it happened in your domain). Each instance that adopts a patch judges it against
its own evidence, with three possible verdicts — and **discarding with a reason is worth
more than adopting out of courtesy**.

## License

Personal, educational, community and research use: **free**. Enterprise use: **paid
license**. And one non-negotiable condition: this framework is **not to be used to
substitute the work of employed people** — it exists so people work better with an
assistant, not so they stop being needed.

Details in `LICENSE.md`. This makes it **source-available, not open source** by the OSI
definition, and the license says so plainly rather than hiding it.
