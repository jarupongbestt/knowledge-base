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
content or frontmatter alone — see "Two kinds of knowledge" below before writing
anything. `knowledge/<domain>/sources/` holds only raw, untouched files (a Dockerfile,
a test file, a PDF, a spec — whatever, wherever); it is input, never itself a topic
page. `knowledge/_example/` is a filled-in worked example of both kinds side by
side, including its own `sources/` fixture — illustrative only, not a real domain.

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

The deciding question is **external resource vs. internal project work**, not how
important, permanent, or well-written the result is:
- **External** — any file, doc, spec, or data the user hands you, or that already
  lives under a domain's `sources/` — even after you summarize, reformat, or
  translate it, and even if it isn't copied into `sources/` yet at the moment you're
  asked (land a copy there first — step 0 of the sync procedure below). → always
  `derived/`, never `self/`.
- **Internal** — produced by doing the project's own work: debugging, reading its
  code, a decision made mid-task. Nothing external was handed to you or consulted as
  the source of the fact. → `self/`.

The mistake to watch for: treating "not yet copied into `sources/`" or "the user
asked me directly" as license to default to `self/`. Neither changes the answer —
only whether the source was external does. A vendor doc turned into readable prose is
still `derived/`; so is "make a knowledge page from this file" when the file hasn't
been dropped into `sources/` yet.

`derived/` pages (any type of raw file, mirrored faithfully — no inference, no
filling gaps, no "improving" the wording) carry `source_ref` + `locked: true` and are
**never hand-edited** during normal task work — only regenerated via the sync
procedure below. The folder is the enforcement mechanism, not the frontmatter: if
you're about to edit a file under `derived/`, stop — that edit belongs in `self/`
instead (either the matching-named file there, or a new one).

A topic can legitimately have both a `self/<topic>.md` and a `derived/<topic>.md`
with the same name (e.g. `derived/webhook.md` for the vendor's field reference,
`self/webhook.md` for the team's integration gotchas) — two files side by side, never
merged into one. If a fact already lives in `derived/`, link to it from `self/`
(`[[topic]]`) instead of restating it — replace any existing duplicate the same way.

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
   a knowledge page. The phrasing ("record this as knowledge", "ทำ knowledge file ให้
   หน่อย") never decides the kind — re-run the origin test before writing anything:
   - Hands you a file/doc, or points at one — even if it's not under `sources/`
     yet — → `derived/` via the sync procedure below (step 0 lands it in `sources/`
     first if needed). Never shortcut straight to `self/` just because the request
     was direct.
   - Asks you to write down something learned from the project's own work, no
     external file involved → `self/`.

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
   - Run `python3 knowledge/_scripts/lint.py` now, before considering the page done —
     catches a broken `[[wikilink]]`/`source_ref` or an index gap while you still have
     full context to fix it. Fix any finding it reports before moving on.
   - Append one line to `knowledge/log.md`: `## [YYYY-MM-DD] create|update | <domain> | <topic>`.

## Contradiction handling

When new information conflicts with an existing page, never overwrite silently:

1. Keep both claims in the page, each labeled with its date.
2. Set `contradiction: true` and `review-needed: true` in that page's frontmatter.
3. Append `## [YYYY-MM-DD] flag-contradiction | <domain> | <subject>` to `knowledge/log.md`.
4. Surface it to the user for resolution — do not auto-resolve, even if one claim
   looks obviously more current than the other.

This is the same principle as `derived/`-locking (don't let one version silently
clobber another) applied to two knowledge claims disagreeing instead of a source
drifting from its derived page.

## Linting

Run `python3 knowledge/_scripts/lint.py` right after you finish creating, updating, or
syncing any page — that's the point where you still have full context to fix whatever
it finds, so this is a step inside the write/sync/ingest procedures, not a separate
occasional chore. This is deliberately not a CI/push-time check: catching a dead link
at push time only tells you it broke sometime earlier, after the context that would
let you fix it easily is gone. (A CI gate on `knowledge/**`, if ever added, would serve
a different purpose — a final backstop before merge — not this one.) It is not
autonomous: it reports findings and exits non-zero, it never edits anything.

Deterministic (the script itself):
- **orphan pages** — a `.md` under a domain's `self/`/`derived/` not linked from that
  domain's `index.md`.
- **index gap** — a domain not listed in `main.md`, or an index row pointing at a
  missing file.
- **stale derived** — a `derived/` page whose frontmatter `content_hash` no longer
  matches a fresh hash of its `source_ref` file.
- **broken links** — `source_ref`/`source_refs` or `[[wikilink]]` targets that don't
  resolve.
- **log size** — `knowledge/log.md` over ~500 entries (rotate to `log-YYYY.md`).

Judgment (only run once the deterministic pass is clean — don't spend this on a
tree that's already known to have gaps):
- **contradiction scan** — one scoped subagent call that reads pages likely to
  overlap and reports pairs of conflicting claims. It reports only; it does not edit
  — findings feed the "Contradiction handling" procedure above.

## Syncing knowledge from sources/ (sources-derived)

Only run this when the user explicitly asks — e.g. "generate knowledge from
`sources/webhook-spec.pdf` in the shopee domain", "sync knowledge from
`sources/infra/Dockerfile`", "this file in sources/ changed, update the knowledge",
"make a knowledge page from this file/doc/spec" (even if what they hand you isn't
under `sources/` yet — see step 0). Never trigger it automatically from routine task
work, and never infer that a file "must have changed" — only re-sync on explicit
instruction.

The raw file can be any type — markdown, PDF, code, config, schema, a Dockerfile,
anything, at any path under `knowledge/<domain>/sources/` (no required layout). Read it
with whichever tool fits its type (Read handles text, markdown, and PDF directly).

0. If the user handed you external material directly (a file path outside
   `knowledge/`, pasted content, an attachment) instead of pointing at something
   already under `sources/`, place a copy of it under
   `knowledge/<domain>/sources/<sensible-path>` first — that copy is the raw material
   `source_ref` will point to. Don't skip straight to writing a `.md` page from the
   external content without landing a raw copy in `sources/` first.
1. Read the raw file in full.
2. Decide the domain (same rule as above — usually already implied by which domain's
   `sources/` the file is under) and a topic name for it.
3. Copy `knowledge/_template/source-topic.md` to
   `knowledge/<domain>/derived/<topic>.md` if new — never inside `sources/` itself —
   or overwrite the existing page in place if this is a re-sync.
4. Fill in frontmatter: `description`, `source_ref` (the raw file's path, e.g.
   `knowledge/<domain>/sources/<file>`), `locked: true`, `synced` (today's date),
   `content_hash` (sha256 of the raw file at `source_ref` — this is what `lint`'s
   stale-derived check compares against on future runs).
5. Write only what the raw file says — a faithful mirror or faithful summary, not
   commentary, not inferred detail, not merged-in self-knowledge.
6. Update the domain's `index.md` — add/update a row under its "Sources-derived" table
   (create that section if this is the domain's first sources-derived page).
7. Add a row for the domain in `main.md` if it's new.
8. Check for conflicts with existing pages (any domain) before finishing — if found,
   follow "Contradiction handling" above instead of overwriting.
9. Run `python3 knowledge/_scripts/lint.py` now and fix any finding — same reasoning
   as in "Recording self-knowledge": catch it while the context is fresh.
10. Append `## [YYYY-MM-DD] sync | <domain> | <topic>` to `knowledge/log.md`.

If the user gives you updated info for a sources-derived fact directly in chat (rather
than adding/changing a file under `sources/`), treat it the same way: update the
sources-derived page and bump `synced` and `content_hash`, don't just drop it into a
self-knowledge page.

Per-claim provenance markers (e.g. `^[sources/<file>.md]` at the end of a paragraph)
are deliberately **not** used yet — today's `derived/` pages are a 1:1 mirror of one
`sources/` file, so provenance is already implicit. Only add them the first time a
page synthesizes claims from 3+ sources; adding them before that is unneeded
overhead.

## Frontmatter rules

All `knowledge/` pages use flat, inline YAML frontmatter only — no lists/arrays, no
nested objects. `source_refs` and `source_ref` are plain strings, not YAML lists.

Additional optional fields:
- `content_hash` (`derived/` pages only) — sha256 of the file at `source_ref`, set at
  sync time, used by `lint` to detect drift.
- `contradiction: true` / `review-needed: true` — set on a page when the
  "Contradiction handling" procedure fires; cleared once a human resolves it.

## Action log

`knowledge/log.md` is one append-only file for the whole repo (not per-domain — "what
changed in the KB this week" is a cross-domain query). Every create / update / sync /
flag-contradiction appends one line (format at the top of the file); see the relevant
procedure above for exactly when to append. When it exceeds ~500 entries (`lint`
flags this), rename it to `log-YYYY.md` and start a fresh `log.md`.
