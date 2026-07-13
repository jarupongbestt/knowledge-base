# Knowledge-base machinery upgrade (spec)

Status: implemented (see `.claude/skills/knowledge-base/SKILL.md`,
`.claude/skills/ingest/SKILL.md`, `knowledge/log.md`, `knowledge/_scripts/lint.py`,
`.github/workflows/sources-readonly.yml`). Scope: **add maintenance machinery + an
ingestion pipeline. Data
model is NOT touched** — `self/` / `derived/` / `sources/`, domain partitioning, and
the external-vs-internal folder rule all stay exactly as they are.

The data model is the part that's already right and hard to change later; the machinery
below is the part that's cheap to add and currently missing. All of it is copied in
*procedure* form (SKILL rules + small scripts), not by adopting anyone else's runtime.

Minimalism gate: every unit below is either already needed at current size, or is a
deterministic check that fails loud. Nothing here adds a service, a DB, or an
autonomous loop. Do not add provenance-per-claim or wikilinks until the trigger
condition in their sections is actually met.

---

## Change 1 — `knowledge/log.md` (append-only action log)

New file at `knowledge/log.md`. Every create / update / sync / contradiction-flag on a
knowledge page appends one line. This is the missing "what changed in the KB and when"
record — needed both for human review and for the orientation read at task start.

Format (one line per action):

```
## [YYYY-MM-DD] <action> | <domain> | <subject>
```

`<action>` ∈ `create` | `update` | `sync` | `flag-contradiction` | `ingest`.

Rules:
- One `log.md` for the whole repo, NOT per-domain — the real query is "what did the KB
  learn this week", which is cross-domain.
- Rotate: when `log.md` exceeds ~500 entries, rename to `log-YYYY.md` and start fresh.
  The `lint` step checks size (Change 2). [ref: llm-wiki SKILL]
- Reading protocol at task start becomes: `main.md` → (already there) **+ last ~20–30
  lines of `log.md`** for recent activity, before touching any domain. Add this one
  line to `CLAUDE.md`'s read order. [ref: llm-wiki orientation protocol]

---

## Change 2 — `lint` operation (deterministic checks + one judgment check)

Add a `lint` procedure to the `knowledge-base` skill, split along the rails/judgment
line so most of it is a script that fails loud and only the last check spends an LLM.

**Deterministic (script — `knowledge/_scripts/lint.py`, exit non-zero on any finding):**
- **orphan pages** — a `.md` under a domain that no `index.md` / `main.md` links to.
- **index gap** — a page on disk not listed in its domain `index.md` (or a domain not
  in `main.md`).
- **stale derived** — a `derived/` page whose backing `sources/` file `content_hash`
  no longer matches the hash recorded in the derived page frontmatter.
- **broken links** — internal links / `sources/` references pointing at missing files.
- **log size** — `log.md` over the rotation threshold.

**Judgment (scoped subagent, only if the deterministic pass is clean):**
- **contradiction scan** — two pages that assert conflicting facts. Confine to one
  subagent call; it reports pairs, it does not edit. Feeds Change 3. [ref: llm-wiki
  `lint`: contradictions / orphans / stale / index completeness]

`lint` is run on demand and (optionally) in CI. It is not autonomous — it reports and
exits; a human or a gated step acts on the report.

---

## Change 3 — contradiction handling (rule in the skill)

When new information conflicts with an existing page, **never overwrite silently.**
[ref: llm-wiki contradiction rule]

Procedure:
1. Keep both claims, each with its date.
2. Set frontmatter `contradiction: true` and `review-needed: true` on the page.
3. Append a `flag-contradiction` line to `log.md`.
4. Surface to the user for resolution — do not auto-resolve.

This generalises what `derived/`-locking already does for source drift, to the case of
two knowledge claims disagreeing.

---

## Change 4 — provenance (CONDITIONAL — do not build yet)

Current state: `derived/` is a 1:1 mirror of one `sources/` file, so provenance is
already implicit (whole page = that one source). **No action needed now.**

Trigger to add per-claim markers: the first time a page synthesises **3+ sources**.
Only then, append a source marker to the end of paragraphs whose claims come from a
specific source, e.g. `^[sources/<file>.md]`, so a reader can trace a claim without
re-reading every source. [ref: llm-wiki provenance markers]

Adding this before the trigger violates the minimalism gate. Leave it in the spec as a
known next step.

---

## Change 5 — enforce `sources/` read-only at the filesystem level

Today "sources are input, never edited" is instruction-only. A misbehaving or
misreading model can overwrite a load-bearing source during ingest → data loss. This
was flagged as the top pitfall on the llm-wiki review and it applies here identically.
[ref: hermes-agent PR #5100 review]

Make it structural, not a prompt promise. Pick one:
- mount `sources/` read-only where the agent runs, or
- keep `sources/` in a separate location the write path can't reach and symlink in, or
- CI check: `git diff` touching any `sources/**` file in a non-`ingest` change fails.

At minimum, the CI check — it's the cheapest and it fails loud.

**Implemented as a two-phase gate** (`.github/workflows/sources-readonly.yml`):
- **Phase 1 (now)**: any PR touching `knowledge/*/sources/**` fails unless the PR
  carries the `ingest` label. Label-based because the `ingest` skill is still a
  human-in-the-loop flow (Acquire → **Gate** → Normalize → Compile), not yet an
  automated/bot-driven one.
- **Phase 2 (once `ingest` is automated)**: switch the bypass from the `ingest` label
  to an identity check — only a dedicated ingest bot/service account may touch
  `sources/**` — and make the check fail-always for any human-authored PR, no label
  bypass at that point.

---

## New skill — `ingest` (turn a user-supplied docs URL into knowledge)

New skill at `.claude/skills/ingest/SKILL.md`. Pipeline:
**Acquire → Gate → Normalize → Compile → Re-sync.** The agent researches and crawls,
but inside a bounded, reviewable step — not an autonomous crawl.

### 1. Acquire (discover the source set — deterministic, try in order)
1. `https://<domain>/llms.txt` and `llms-full.txt` — a curated, markdown, agent-ready
   manifest published exactly for this. If present, acquisition is done. The
   `llms.txt` (index) + `llms-full.txt` (full content dump) pair is the common 2026
   pattern on dev-tool/docs sites, and serving markdown instead of HTML cuts roughly an
   order of magnitude of tokens vs scraping rendered pages. [ref: llms.txt state-of /
   guides]
2. `sitemap.xml` — filter to the docs path prefix (e.g. `/docs/latest/api`).
3. Scoped crawl — only if neither exists. Bound hard: same path prefix, depth ≤ N,
   max pages ≤ M, respect `robots.txt`.

Output of this step is a **list of URLs only** — nothing fetched in bulk yet.

### 2. Gate (this is where "research" happens — and where it's bounded)
Agent presents the candidate manifest with a one-line rationale per group
("12 pages = API reference core; 40 pages = tutorials — include which?"). User
trims / approves. This is the rail that stops a crawl from dumping 400 low-signal
pages into the lake. Mirrors the existing Approve-gate discipline.

### 3. Normalize
Fetch only the approved URLs → strip nav / boilerplate → clean markdown (e.g.
Firecrawl / Docling / Trafilatura) → write to `knowledge/<domain>/sources/<slug>.md`
with frontmatter:

```yaml
source_url: https://www.metabase.com/docs/latest/api/...
fetched_at: YYYY-MM-DD
content_hash: <sha256>
```

### 4. Compile
The existing `derived/` sync: generate `derived/<slug>.md` from each source, update the
domain `index.md` and `main.md`, run contradiction handling (Change 3), append `ingest`
lines to `log.md`. `self/` stays empty for the new domain — it only fills once the
project learns something from *using* the tool (e.g. "this endpoint rate-limits hard,
batch it"), which is internal knowledge by the folder rule.

### 5. Re-sync
On a later run, re-Acquire → diff `content_hash` → re-Normalize + re-Compile **only**
changed pages. The `derived/`-locked-until-resync design already supports this; the
stored hash is what makes the diff automatic. `stale derived` in `lint` (Change 2)
surfaces sources that changed but weren't re-synced.

---

## Frontmatter additions (summary)

- `derived/` pages: `content_hash` (of backing source), for stale detection + re-sync.
- any page: `contradiction: true` / `review-needed: true` when Change 3 fires.
- `sources/` files (via ingest): `source_url`, `fetched_at`, `content_hash`.

## Files touched

```
knowledge/log.md                         # new (Change 1)
knowledge/_scripts/lint.py               # new (Change 2)
.claude/skills/knowledge-base/SKILL.md   # edit: lint + contradiction procedure, log rules
.claude/skills/ingest/SKILL.md           # new (ingest pipeline)
CLAUDE.md                                # edit: add log.md to read order
.github/ (or CI config)                  # new: sources/ read-only check (Change 5)
```

## Explicitly NOT doing (and why)

- **Adopting the Hermes agent runtime** — the self-improving / autonomous loop is the
  part previously rejected. Only the file-pattern *procedures* are borrowed. [ref:
  llm-wiki is separable from the Hermes runtime]
- **Vector DB / hybrid retrieval** — current scale is served by filesystem navigation
  + (later) full-text search. Add semantic retrieval only when queries stop being
  keyword-shaped, not before.
- **wikilinks everywhere** — optional, and only worth it for *cross-domain* references;
  within a domain the `index.md` already does the job, so blanket wikilinks duplicate
  the partitioning.

---

## References

- Hermes `llm-wiki` SKILL — log rotation (500-entry), contradiction handling, `lint`
  (contradictions / orphans / stale / index gaps), provenance markers, ingest/query/lint
  operations, "compile once vs RAG re-derive" framing (Karpathy LLM Wiki pattern):
  https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md
- Hermes PR #5100 — three-layer model (immutable raw → agent pages → schema) and the
  top pitfall: raw-source protection is instruction-only, not filesystem-enforced:
  https://github.com/NousResearch/hermes-agent/pull/5100
- LLM Wiki orientation protocol (start every session with SCHEMA + index + last 20–30
  log lines): https://arapaholabs.com/blog/2026-06-15-llm-wiki-karpathy-pattern
- llms.txt / llms-full.txt — spec, index+full-dump pattern, markdown-over-HTML token
  savings, dev-tool/docs adoption:
  https://presenc.ai/research/state-of-llms-txt-2026 ,
  https://codersera.com/blog/llms-txt-complete-guide-2026/ ,
  https://limy.ai/blog/llms.txt-in-2026-the-full-guide
- Normalization tooling (docs URL → clean markdown): Firecrawl, Docling, Trafilatura
  (evaluate at implementation time; named as options, not a fixed choice).
