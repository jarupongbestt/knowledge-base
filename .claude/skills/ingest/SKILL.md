---
name: ingest
description: Turn a user-supplied docs site/URL into knowledge-base sources + derived pages. Use when the user gives a docs URL and asks to pull in / ingest / import its documentation, rather than a single file they already have in hand (that's the knowledge-base skill's sync procedure instead). Triggers on "ingest the docs at <url>", "pull in <product>'s API docs", "import this documentation site".
---

# Ingest

Turns a docs site into `knowledge/<domain>/sources/*` + `derived/*` pages, via a
bounded, reviewable pipeline — the agent researches and crawls, but only inside a
gated step, never as an open-ended autonomous crawl. Five stages:
**Acquire → Gate → Normalize → Compile → Re-sync.**

This is for a *docs site*, not a single file the user already has — if they hand you
one file/doc directly, use the `knowledge-base` skill's sync procedure instead (its
step 0 lands a copy in `sources/` first).

## 1. Acquire — discover the source set (deterministic, try in order)

1. `https://<domain>/llms.txt` and `llms-full.txt` — a curated, markdown, agent-ready
   manifest published for exactly this purpose. If present, acquisition is done: use
   `llms.txt` as the index and `llms-full.txt` (if present) as the full content dump.
   This pair is the common pattern on dev-tool/docs sites, and markdown instead of
   rendered HTML cuts roughly an order of magnitude of tokens.
2. `sitemap.xml` — filter to the docs path prefix the user asked about (e.g.
   `/docs/latest/api`).
3. Scoped crawl — only if neither of the above exists. Bound it hard: same path
   prefix, depth ≤ N (default 3), max pages ≤ M (default 50), respect `robots.txt`.

Output of this step is a **list of candidate URLs only** — nothing fetched in bulk
yet.

## 2. Gate — the bounded "research" step

Present the candidate manifest grouped, with a one-line rationale per group (e.g.
"12 pages = API reference core; 40 pages = tutorials — include which?"). The user
trims/approves before anything is fetched in bulk. This is the rail that stops a
crawl from dumping hundreds of low-signal pages into the lake — do not skip it even
if `llms.txt` looks small enough to just take whole.

## 3. Normalize

Fetch only the approved URLs. Strip nav/boilerplate and convert to clean markdown.
Write each page to `knowledge/<domain>/sources/<slug>.md` with frontmatter:

```yaml
source_url: https://example.com/docs/latest/api/...
fetched_at: YYYY-MM-DD
content_hash: <sha256 of the normalized markdown>
```

## 4. Compile

For each new/changed source file, follow the `knowledge-base` skill's existing sync
procedure: generate/update `knowledge/<domain>/derived/<slug>.md` (with its own
`content_hash` pointing at the `sources/` file), update the domain's `index.md` and
`main.md`, run contradiction handling if a claim conflicts with an existing page, run
`python3 knowledge/_scripts/lint.py` and fix anything it finds before moving to the
next page (catch a dead link right after compiling that page, not after the whole
batch — see the `knowledge-base` skill's "Linting" section for why this runs here and
not as a push-time check), and append `## [YYYY-MM-DD] ingest | <domain> | <slug>` to
`knowledge/log.md` for each compiled page. `self/` for this domain stays empty until
the project actually *uses* what was ingested and learns something from that (e.g.
"this endpoint rate-limits hard, batch it") — that's internal knowledge, recorded the
normal way.

## 5. Re-sync

On a later run: re-Acquire the same manifest, diff each page's `content_hash` against
what's already in `sources/`, and re-Normalize + re-Compile only the pages that
changed. `lint.py`'s stale-derived check (see `knowledge-base` skill) is the backstop
that surfaces any source that changed but wasn't re-synced.

## Guardrails

- `sources/` is input, never hand-edited outside this pipeline — see the
  `sources/` read-only CI check (`.github/workflows/sources-readonly.yml`), currently
  gated by the PR carrying an `ingest` label. Once this pipeline runs unattended, that
  gate is meant to switch to an identity check instead of a label — don't rely on the
  label being the permanent mechanism.
- Never fetch beyond what was approved at the Gate step, even if a page links further
  out into the same site.
- No vector DB / embeddings step here — output is plain markdown files navigated the
  same way as the rest of `knowledge/`.
