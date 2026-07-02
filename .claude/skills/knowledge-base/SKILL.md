---
name: knowledge-base
description: Read or update this repo's domain-organized knowledge base under knowledge/. Use before working on any non-trivial task (to find existing knowledge) and after a task teaches something durable (to record it). Triggers on "check the knowledge base", "what do we know about X", "record this as knowledge", "create a new domain", "sync knowledge from sources".
---

# Knowledge base

This repo keeps durable knowledge in `knowledge/`, separate from code and from
`CLAUDE.md`. Each domain owns its own raw data lake at `knowledge/<domain>/sources/` —
that folder holds only raw material, never a curated `.md` knowledge page.

```
knowledge/
  main.md                     # root index: lists every domain, nothing else
  <domain>/index.md           # navigation table for that domain: what's inside,
                               # which page for what
  <domain>/self/<topic>.md    # self-knowledge topic pages, freely editable
  <domain>/derived/<topic>.md # sources-derived topic pages, locked, mirror a raw
                               # file under this domain's sources/
  <domain>/sources/...        # this domain's raw data lake: ANY file type, ANY
                               # layout — e.g. sources/Dockerfile, sources/ui/src/test.tsx,
                               # sources/spec.pdf. No required structure. This is
                               # INPUT, never knowledge, and never a topic page.
  _template/index.md          # copy this to start a new domain
  _template/self-topic.md     # copy this to start a new self-knowledge topic page
  _template/source-topic.md   # copy this to start a new sources-derived topic page
```

A topic page's *kind* is decided by which folder it's in, never by guessing from
content or frontmatter alone:
- `knowledge/<domain>/self/<topic>.md` → self-knowledge, freely editable.
- `knowledge/<domain>/derived/<topic>.md` → sources-derived, never hand-edited;
  frontmatter still carries `source_ref` + `locked: true` for traceability, but the
  folder is what enforces the boundary — an agent should never need to open a file
  and check its frontmatter just to know whether it's allowed to edit it.

Never confuse a topic page with the raw file it mirrors. `knowledge/<domain>/sources/`
holds only raw, untouched files (a Dockerfile, a test file, a PDF, a spec — whatever,
wherever, no imposed layout). A `.md` page under `self/` or `derived/` is always
curated knowledge about exactly one topic — it is never itself a raw file, and a raw
file is never itself knowledge.

There are two kinds of topic page and they must never overlap in content — see
"Two kinds of knowledge" below before writing anything. `knowledge/_example/` is a
filled-in worked example of both kinds side by side, including its own `sources/`
fixture — read it if the structure below is unclear. It's illustrative only, not a
real domain.

## How to use this knowledge base (read path)

1. `CLAUDE.md` already mandates reading `knowledge/main.md` before touching any other
   file, every time — so it should already be read. If not, read it now. It lists the
   domains that currently exist.
2. Pick the domain(s) relevant to the task — a task can span more than one domain.
3. Read that domain's `index.md`, then follow its navigation table to the relevant
   topic page(s) — self-knowledge, sources-derived, or both.
4. Read the topic page(s). If a page's `source_refs` / `source_ref` names a specific
   raw file and the task needs that level of detail, read that file too.
5. If no domain fits, proceed with the task normally — don't force-fit it into an
   existing domain. Whether a new domain should be *created* is decided at write time
   (below), not read time.

## Two kinds of knowledge — never mixed, never the same file

The deciding question is **where the fact came from**, not how important, permanent,
or well-written it is:
- Did it come from a raw file under `sources/` (or content the user handed you that
  mirrors one) — even after you summarized, reformatted, or translated it? → always
  `derived/`, never `self/`.
- Did it come from doing the project's own work — debugging, reading its code, a
  decision made mid-task? → `self/`.

A common mistake: reading a vendor doc / spec dropped in `sources/`, turning it into
readable prose, and filing that under `self/` because it "feels like knowledge you
figured out." It isn't — extracting and rephrasing a source file is still mirroring
it, so it belongs in `derived/`.

- **Self-knowledge** (`knowledge/<domain>/self/<topic>.md`) — learned by doing
  project work: gotchas, decisions and why, constraints, integration quirks.
  Evolves freely as the project develops. This is the default kind — most tasks write
  here.
- **Sources-derived** (`knowledge/<domain>/derived/<topic>.md`) — generated from one
  raw file somewhere under `knowledge/<domain>/sources/`. That file can be *any
  type* — a markdown doc, a PDF spec, a code file, a Dockerfile, a config/schema
  file, anything, at any path, no imposed layout. The knowledge page itself is
  always `.md`; what it mirrors isn't, and the raw file is never edited or moved.
  Must mirror it faithfully: no inference, no filling gaps, no "improving" the
  wording. Frontmatter still carries `source_ref` + `locked: true`. **Locked** —
  never hand-edit these during normal task work. Only touch them via the sync
  procedure below, and only when the user adds/changes a file under `sources/` or
  gives you updated content for one directly.
- The folder is the enforcement mechanism, not a suggestion: if you're about to edit
  a file under a domain's `derived/`, stop — that edit belongs in `self/` instead
  (either the matching-named file there, or a new one).
- If a fact already lives in a sources-derived page, a self-knowledge page must link to
  it (`[[topic]]`) instead of restating it — the two must never say the same thing in
  two places that can drift apart. If you notice self-knowledge duplicating a
  sources-derived page, replace the duplicate with a link as part of that task.
- A topic can legitimately have both a `self/<topic>.md` and a `derived/<topic>.md`
  with the same name (e.g. the vendor's field reference in `derived/webhook.md` and
  the team's integration gotchas in `self/webhook.md`) — that's the two kinds living
  side by side without ever merging into one file.

## Recording self-knowledge

Two separate triggers land here — same procedure either way:

1. **End-of-task check (automatic, mandatory).** Before ending any non-trivial task,
   ask: did this teach a gotcha, a non-obvious constraint, an integration quirk, an
   architectural decision and why — something a future task in this area would
   benefit from knowing? Asking is mandatory every time, even when the honest answer
   is no — skipping the question (as opposed to answering "no") is the failure mode
   this step exists to prevent. Not durable = routine implementation detail already
   obvious from reading the code, or a narrated log of what you did this session.
   Most routine tasks (typo fixes, trivial lookups, small mechanical edits) will
   honestly answer "no" — that's fine, don't force a page into existence.
2. **Direct request (explicit, always acts).** The user asks outright to write/update
   a knowledge page about something — e.g. "ทำ knowledge file xxx ให้หน่อย", "record
   this as knowledge", "write down what we just learned about X." If the content
   doesn't point at (or mirror) a raw file under some domain's `sources/`, it's
   self-knowledge by the origin test above — write it to `self/`, never `derived/`,
   regardless of how the user phrased the request.

In both cases, including on a brand-new project with an empty Domains table in
`main.md`, run the same steps below — creating the first domain from scratch is not a
special case, just step 1 with no existing rows to match against.

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
   - Copy `knowledge/_template/self-topic.md` to `knowledge/<domain>/self/<topic>.md`
     if new, or edit the existing page if the topic already has one there — prefer
     updating over creating a near-duplicate page.
   - Fill in `description`, `source_refs`, `updated` in the frontmatter.
   - Write the knowledge itself: factual, specific, reference material — not a
     narrated changelog of what you did this session.
   - Update the domain's `index.md` navigation table if the page is new or its
     "when working on..." scope changed.

## Syncing knowledge from sources/ (sources-derived)

Only run this when the user explicitly asks — e.g. "generate knowledge from
`sources/webhook-spec.pdf` in the shopee domain", "sync knowledge from
`sources/infra/Dockerfile`", "this file in sources/ changed, update the knowledge".
Never trigger it automatically from routine task work, and never infer that a file
"must have changed" — only re-sync on explicit instruction.

The raw file can be any type — markdown, PDF, code, config, schema, a Dockerfile,
anything, at any path under `knowledge/<domain>/sources/` (no required layout). Read it
with whichever tool fits its type (Read handles text, markdown, and PDF directly).

1. Read the raw file in full.
2. Decide the domain (same rule as above — usually already implied by which domain's
   `sources/` the file is under) and a topic name for it.
3. Copy `knowledge/_template/source-topic.md` to
   `knowledge/<domain>/derived/<topic>.md` if new — never inside `sources/` itself —
   or overwrite the existing page in place if this is a re-sync.
4. Fill in frontmatter: `description`, `source_ref` (the raw file's path, e.g.
   `knowledge/<domain>/sources/<file>`), `locked: true`, `synced` (today's date).
5. Write only what the raw file says — a faithful mirror or faithful summary, not
   commentary, not inferred detail, not merged-in self-knowledge.
6. Update the domain's `index.md` — add/update a row under its "Sources-derived" table
   (create that section if this is the domain's first sources-derived page).
7. Add a row for the domain in `main.md` if it's new.

If the user gives you updated info for a sources-derived fact directly in chat (rather
than adding/changing a file under `sources/`), treat it the same way: update the
sources-derived page and bump `synced`, don't just drop it into a self-knowledge page.

## Frontmatter rules

All `knowledge/` pages use flat, inline YAML frontmatter only — no lists/arrays, no
nested objects. `source_refs` and `source_ref` are plain strings, not YAML lists.
