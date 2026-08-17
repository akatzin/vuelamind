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
provenance: **measured**, **cited**, **inferred**, or **reported**.

## What you get

A vault of plain text files and a cycle of four acts:

- **Born**, once — an interview that produces your domain's birth record, in your words.
- **Resumed**, at the start of every session — the assistant measures the current state
  instead of trusting what it remembers.
- **Reconciled**, at the close — what aged gets corrected, what was learned gets written.
- **Joined**, when another machine comes in — the first step of a hive.

Inside: a work queue ordered by real severity, a decision log that records *what would
change my mind*, and **an error book — 49 lessons, each one paid for by a real mistake**.
And the method does not just claim to work: **ten scripted end-to-end runs, all clean** — see [PRUEBAS.md](PRUEBAS.md).
That last part is the valuable one. The structure you could rebuild in an afternoon; the
scars you could not.

## Getting started

Both paths start the same way — with the file, not with a command:

1. Make a folder for your domain and clone the method into it:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Open your assistant **in that folder** and tell it: **"Initialize MARCO_Inicial.md"**.

   No need to paste anything — step 1 already put the file on disk, so the assistant reads it.

The first question is your language. **The second one decides everything after it:** is this
domain being born here, or is this machine joining one that already lives?

> Where the canon lives — repository, branch, site — is declared once in
> [`config.yml`](config.yml), along with the defaults for where patches are consumed from and
> published to. Everything else references that file instead of repeating it, and a check
> fails the build if any copy drifts away from it.

- **Being born** — answer the interview. About twenty minutes, and you can pause. It generates
  the vault, the scaffolding and the cycle commands.
- **Joining** — no interview and nothing generated. It reaches the existing vault, checks it
  arrived whole, installs the cycle from the canon, and hands over to `/vuelamind-join`.

The assistant does not just take your word for it: it looks at the destination folder and
**stops** if you said *born* and found months of work inside — or if you said *joining* and
found nothing there.

**What you need:** an assistant that can read your files and run commands. Any of them works —
the method is plain text. If you have none, `npm install -g @anthropic-ai/claude-code` is a
known path.

Beyond that, the framework asks for no server of its own, no service and no account with it:
just two local folders.

The cycle commands in `skills/` are written for Claude Code, but the method is plain text
and does not depend on which model reads it.

## One machine, or several

Everything above assumes one: an assistant and two local folders. **That promise holds for being born** — nothing else is needed to start.

**A second machine needs to reach what the first one has**: the vault, the scaffolding — its manifest, its validator, its memory — and, if your domain verifies against live systems, the credentials to do that. *How* it reaches them is yours to pick: a shared folder, a mount, a clone, an automatic replica. The framework does not decide the transport.

`/vuelamind-join` walks that path, and its checks are the point: it confirms the vault arrived **whole** — half-synced is worse than empty, because the assistant measures over a hole and concludes with confidence — installs the cycle from the canon, and **runs your validator as the proof of being in**. Files being present is not the same as being able to measure.

**And that command is not on the new machine yet** — it ships with being born. So a machine that never was born starts where everyone starts: clone this repository and initialize `MARCO_Inicial.md`, answering *joining*. The file brings the commands with it; from there the command takes over.

A machine that can read the vault but cannot reach the systems is still a legitimate instance — it just has to **say so** when it declares itself, because from then on it documents without verifying.

And there is a legitimate instance that never writes at all — a board subscribed to the engineering memory, an auditor. Its registry row carries `access: writes | reads`, and **it does not declare itself: a writing instance declares it**, before it arrives. Whoever only reads keeps the thing that defines the role: closing every session without having written a letter.

## Requirements

An assistant, two local folders, and **a Unix-like shell** — macOS or Linux.

**Windows is not supported natively.** The scripts the framework generates assume `sh`/`bash`
and POSIX paths. The known way around it is running your assistant **inside a Linux
container** (Docker, for instance) and working there — everything the framework needs lives
inside the container, and the host stops mattering.

That container route is **measured, not inferred** — as of 2026-08-13. It was built and run:
`docker/` in this repository holds the image, with the method already baked into
`/opt/vuelamind`. Inside it, the four quadrants of the birth/join question were exercised
end to end, and the assistant stopped where it should stop.

What that test did **not** cover: reaching live systems from inside the container. A machine
that can read the vault but cannot reach what it documents is still a legitimate instance —
it just has to say so.

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

Someone has to judge what arrives. That role has a name and a definition of its own —
what it watches, what it measures, how it judges, and what is none of its business — in
`WATCHER.md`. It watches **what enters the canon, never who uses it**: there is no
registry of installations, and there will not be one.

## License

Personal, educational, community and research use: **free**. Enterprise use: **paid
license**. And one non-negotiable condition: this framework is **not to be used to
substitute the work of employed people** — it exists so people work better with an
assistant, not so they stop being needed.

Details in `LICENSE.md`. This makes it **source-available, not open source** by the OSI
definition, and the license says so plainly rather than hiding it.
