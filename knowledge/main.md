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

A topic page's *kind* is decided by which folder it's in, never by guessing from
content — `derived/` pages are never hand-edited (frontmatter carries `source_ref` +
`locked: true` for traceability; see the next section for how the kind is decided).

## Two kinds of knowledge — never mixed, never the same file

The deciding question is **external resource vs. internal project work**:
- **External** (a file/doc/spec the user hands you, or anything under a domain's
  `sources/`) → always `derived/`, never `self/` — even after you rewrite it, and
  even if it isn't copied into `sources/` yet ("make a knowledge page from this file"
  is still external; land it in `sources/` first).
- **Internal** (produced by doing the project's own work — debugging, reading its
  code, a decision made mid-task, nothing external consulted) → `self/`.
- A topic can have both, as two separate files in different folders
  (`self/webhook.md` + `derived/webhook.md`) — never merged into one.
- If a fact already lives in `derived/`, link to it from `self/` (`[[topic]]`) instead
  of restating it.

Full write procedure, edge cases, and a worked example: see
`.claude/skills/knowledge-base/SKILL.md` and `knowledge/_example/`.

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
3. Add topic pages under `knowledge/<domain>/self/` or `knowledge/<domain>/derived/`
   (per the origin test above) as the work produces them — don't pre-create empty
   pages speculatively. This applies the same way for a brand-new project with no
   domains yet — the first task that touches a distinct area creates its domain, no
   special-casing needed.

## Keeping this up to date

- **Before ending any non-trivial task**, ask whether it taught a gotcha, constraint,
  decision, or integration quirk — mandatory to ask every time, even when the answer
  is "no." If yes, write it to `self/<topic>.md` as part of finishing the task, not
  deferred.
- A direct request to write/update a knowledge page follows the same procedure
  immediately — apply the origin test above rather than defaulting to `self/`.
- Fix a domain's `index.md` navigation table as part of the same task if it goes
  stale; prefer updating an existing page over creating a near-duplicate.
- Full procedure: `.claude/skills/knowledge-base/SKILL.md`.
