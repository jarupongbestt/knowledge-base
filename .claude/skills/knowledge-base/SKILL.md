---
name: knowledge-base
description: Read or update this repo's domain-organized knowledge base under knowledge/. Use before working on any non-trivial task (to find existing knowledge) and after a task teaches something durable (to record it). Triggers on "check the knowledge base", "what do we know about X", "record this as knowledge", "create a new domain".
---

# Knowledge base

This repo keeps durable knowledge in `knowledge/`, separate from code and from
`CLAUDE.md`. Layout:

```
knowledge/
  main.md                  # root index: lists every domain, nothing else
  <domain>/index.md         # navigation table for that domain: what's inside, which page for what
  <domain>/<topic>.md       # actual detail pages
  _template/index.md        # copy this to start a new domain
  _template/topic.md        # copy this to start a new topic page
```

`main.md` and each domain's `index.md` are navigation only — pointers, not content.
Detail always lives in topic pages.

## Before working on a task

1. `CLAUDE.md` already mandates reading `knowledge/main.md` before touching any other
   file, every time — so it should already be read. If not, read it now. It lists the
   domains that currently exist.
2. If the task's area matches a domain, read that domain's `index.md`, then follow its
   navigation table to the relevant topic page(s) before scanning code.
3. If no domain fits, proceed with the task normally — don't force-fit it into an
   existing domain. Whether a new domain should be *created* is decided at write time
   (below), not read time.

## After a task teaches something durable

Durable = a gotcha, a non-obvious constraint, an integration quirk, an architectural
decision and why — something a future task in this area would benefit from knowing.
Don't record routine implementation detail that's already obvious from reading the code.

1. **Decide the domain.** A domain is a bounded area with its own concerns and
   vocabulary:
   - An **external integration** (a specific marketplace/platform, e.g. Shopee,
     Lazada, TikTok Shop, LINE, Facebook) — each has its own auth, payload shapes,
     signature verification, rate limits.
   - A **cross-cutting subsystem** shared by ≥2 integrations (e.g. `auth`, `queue`,
     `deployment`, `observability`). Only create one of these once a second domain
     would otherwise duplicate the same knowledge — don't pre-create it speculatively.
   Don't create a domain for a single function or one-off script; that's a page (or
   section of a page) inside the domain that owns it.

2. **New domain:**
   - Copy `knowledge/_template/index.md` to `knowledge/<domain>/index.md`, fill in
     `description`, `source_refs`, `updated`, and an initial navigation table row.
   - Add one row for it to the **Domains** table in `knowledge/main.md`.

3. **New or updated topic page:**
   - Copy `knowledge/_template/topic.md` to `knowledge/<domain>/<topic>.md` if new, or
     edit the existing page if the topic already has one — prefer updating over
     creating a near-duplicate page.
   - Fill in `description`, `source_refs`, `updated` in the frontmatter.
   - Write the knowledge itself: factual, specific, reference material — not a
     narrated changelog of what you did this session.
   - Update the domain's `index.md` navigation table if the page is new or its
     "when working on..." scope changed.

## Frontmatter rules

All `knowledge/` pages use flat, inline YAML frontmatter only — no lists/arrays, no
nested objects. `source_refs` is a comma-separated string, not a YAML list.
