# Knowledge Base

Template repo for setting up a durable, domain-organized knowledge base for a project,
used with Claude Code.

## How it works

- `CLAUDE.md` — instructs Claude Code to always read `knowledge/main.md` first.
- `knowledge/main.md` — root index, lists all domains and routes to their index pages.
- `knowledge/<domain>/index.md` — navigation hints for one domain (which page to read
  for which kind of work).
- `knowledge/<domain>/self/<topic>.md` — self-knowledge: gotchas, decisions,
  constraints — evolves with the project, freely editable.
- `knowledge/<domain>/derived/<topic>.md` — sources-derived: mirrors one raw file from
  that domain's own `sources/` folder, marked `locked: true` in its frontmatter, and
  locked until the user asks for a re-sync.
  The folder, not just the frontmatter, is what marks a page as sources-derived —
  `self/` and `derived/` are never the same file.
- `knowledge/<domain>/sources/...` — that domain's raw data lake: drop external
  material here, any file type, any layout (a Dockerfile, `ui/src/test.tsx`, a PDF
  spec — whatever, wherever). This is input, never knowledge, and never itself a topic
  page.
- `knowledge/_template/` — copy `index.md` / `self-topic.md` / `source-topic.md` from
  here when creating a new domain or page.
- `knowledge/_example/` (with its own `sources/` fixture) — a filled-in worked example
  of both kinds side by side. Illustrative only, not a real domain.
- `.claude/skills/knowledge-base/SKILL.md` — the read/write procedure Claude follows to
  keep this structure up to date as it learns things from tasks.
- `.claude/agents/investigator.md` + `.claude/skills/root-cause/SKILL.md` — the
  investigator subagent and the cited-evidence protocol it must follow before Claude
  proposes a cause or fix for any requirement/error/setup question.

## Usage

1. Use this repo as a template (or copy its structure) into a new or existing project.
2. Drop external material into `knowledge/<domain>/sources/` as it comes in, in
   whatever layout makes sense; let Claude Code generate the matching sources-derived
   page only when you ask it to sync.
3. Let Claude Code create domains and self-knowledge topic pages as work happens —
   don't pre-create empty pages speculatively.
4. Keep `main.md` and each domain's `index.md` as navigation only; put actual knowledge
   in topic pages.
5. Before ending any non-trivial task, Claude Code checks whether it learned something
   durable (a gotcha, a constraint, a decision and why) and records it under `self/` if
   so — this check is mandatory even when the answer turns out to be "no."

## Reading knowledge (as an agent or a person)

`main.md` → pick domain(s) → domain's `index.md` → topic page(s) → the specific raw
file under that domain's `sources/` if you need more detail than the mirrored page has.
