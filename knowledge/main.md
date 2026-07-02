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

## How this knowledge base is organized

- `knowledge/main.md` (this file) — lists all domains, nothing else.
- `knowledge/<domain>/index.md` — navigation hints for that domain: what's inside, which
  page to read for which kind of work.
- `knowledge/<domain>/<topic>.md` — the actual detail pages a domain's index points to.

Rule of thumb: **main.md tells you which domain, the domain's index.md tells you which
page.** Never put topic detail directly in main.md or in a domain's index.md — those two
are navigation only.

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

- When a task reveals knowledge worth keeping (a gotcha, a non-obvious constraint, an
  architectural decision, an integration quirk) — write it to the relevant domain's
  page, not into chat.
- When a domain's index.md navigation table stops matching reality (new pages, moved
  concerns), fix it as part of that task, not later.
- Prefer updating an existing page over creating a new one for closely related info.
