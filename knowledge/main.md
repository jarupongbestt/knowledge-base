---
description: "Root index of the knowledge base. Lists every domain and where its detail lives. Read this first before touching any part of the codebase."
updated: 2026-07-02
---
# Knowledge Base — Main Index

## Domains

| Domain | What it covers | Index |
|---|---|---|
| _(none yet)_ | | |

> No domains exist yet. See "Creating a new domain" below — the first task that touches
> a distinct area should create one.

## How to use this knowledge base

1. Read this file (`main.md`) — it lists every domain that exists.
2. Pick the domain(s) relevant to the task (a task can touch more than one).
3. Read that domain's `knowledge/<domain>/index.md` — its navigation table routes you
   to the specific topic page(s) for the kind of work you're doing.
4. Read the topic page(s) it points to — that's where the actual detail lives.
5. If a topic page's `source_refs` / `source_ref` names a specific raw file, read that
   file too if the task needs that level of detail.

`main.md` and each domain's `index.md` are navigation only — pointers, not content.
Detail always lives in topic pages. Never put topic detail directly in either of them.

## Where things live

```
knowledge/
  main.md                     # this file
  <domain>/index.md           # navigation table for that domain
  <domain>/self/<topic>.md    # self-knowledge topic pages, freely editable
  <domain>/derived/<topic>.md # sources-derived topic pages, locked, mirror a
                               # raw file under this domain's sources/
  <domain>/sources/...        # this domain's raw data lake: ANY file type, ANY
                               # layout — e.g. sources/Dockerfile, sources/ui/src/test.tsx,
                               # sources/spec.pdf. No required structure. This is
                               # INPUT, never knowledge, and never a topic page.
```

A topic page's *kind* is decided by which folder it's in — `self/` or `derived/` —
never by guessing from content:
- `knowledge/<domain>/self/<topic>.md` → self-knowledge, freely editable.
- `knowledge/<domain>/derived/<topic>.md` → sources-derived, never hand-edited;
  frontmatter still carries `source_ref` + `locked: true` for traceability.

## Two kinds of knowledge — never mixed, never the same file

- **Self-knowledge** (`knowledge/<domain>/self/<topic>.md`) — learned from doing
  project work: gotchas, decisions and why, constraints. Evolves freely as the
  project develops. This is the default kind; see "Keeping this up to date" below.
- **Sources-derived** (`knowledge/<domain>/derived/<topic>.md`) — generated from one
  raw file the user dropped somewhere under `knowledge/<domain>/sources/`. That file
  can be *any type* — markdown, PDF, code, config, schema, a vendor spec — the
  resulting knowledge page is always `.md`, but what it mirrors isn't limited to
  `.md`, and the raw file itself is never touched or moved. Must mirror it
  faithfully — no inference, no "improvements". Locked: never hand-edited during
  normal task work, only regenerated via the sync procedure in SKILL.md, and only
  when the user adds/changes a file under `sources/` or gives updated content
  directly.
- If a topic has both kinds of knowledge (e.g. a vendor's field reference *and* what
  the team learned integrating with it), that's two separate files with the same
  topic name in different folders — `self/webhook.md` and `derived/webhook.md` — never
  one file trying to hold both.
- Don't confuse a topic page with the raw file it mirrors — `sources/` holds only raw,
  untouched files; a `.md` page under `self/` or `derived/` is always curated
  knowledge about one topic, never a raw file itself.
- If a fact already lives in a sources-derived page, a self-knowledge page should link
  to it (`[[topic]]`) rather than duplicate it — the two must never say the same thing
  in two places that can drift apart.
- See `knowledge/_example/` for a filled-in worked example of both kinds side by side,
  including its own `sources/` fixture (illustrative only — not a real domain, don't
  add it to the Domains table).

## What counts as a "domain"

A domain is a bounded area with its own concerns, gotchas, and vocabulary — usually one
of:
- **An external integration** (e.g. a specific marketplace/platform: Shopee, Lazada,
  TikTok Shop, LINE, Facebook). Each has its own auth flow, payload shapes, signature
  verification, and rate limits — those don't leak into other domains.
- **A cross-cutting subsystem** used by multiple integrations (e.g. `auth`,
  `queue`, `deployment`, `observability`). Create one only when ≥2 domains would
  otherwise duplicate the same knowledge.

Don't create a domain for a single function or a one-off script — that belongs as a page
(or a section of a page) inside the domain that owns it.

## Creating a new domain

1. Copy `knowledge/_template/index.md` to `knowledge/<domain>/index.md`, fill in the
   frontmatter and the navigation table.
2. Add one row for it in the **Domains** table above.
3. Add topic pages under `knowledge/<domain>/` as the work produces them — don't
   pre-create empty pages speculatively.

## Keeping this up to date

- **Before ending any non-trivial task**, explicitly decide: did this task teach a
  gotcha, a non-obvious constraint, an architectural decision, or an integration
  quirk? This is a required check, not an optional afterthought — most routine tasks
  will genuinely answer "no" and that's fine, but the question must be asked every
  time, not skipped.
- If yes, write it to the relevant domain's `self/<topic>.md` page, not into chat, as
  part of finishing the task — not deferred to "later."
- When a domain's index.md navigation table stops matching reality (new pages, moved
  concerns), fix it as part of that task, not later.
- Prefer updating an existing page over creating a new one for closely related info.
