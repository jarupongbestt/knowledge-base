# Knowledge Base

Template repo for setting up a durable, domain-organized knowledge base for a project,
used with Claude Code.

## How it works

- `CLAUDE.md` — instructs Claude Code to always read `knowledge/main.md` first.
- `knowledge/main.md` — root index, lists all domains and routes to their index pages.
- `knowledge/<domain>/index.md` — navigation hints for one domain (which page to read
  for which kind of work).
- `knowledge/<domain>/<topic>.md` — actual detail pages (gotchas, decisions, constraints).
- `knowledge/_template/` — copy `index.md` / `topic.md` from here when creating a new
  domain or page.
- `.claude/skills/knowledge-base/SKILL.md` — the read/write procedure Claude follows to
  keep this structure up to date as it learns things from tasks.

## Usage

1. Use this repo as a template (or copy its structure) into a new or existing project.
2. Let Claude Code create domains and topic pages as work happens — don't pre-create
   empty pages speculatively.
3. Keep `main.md` and each domain's `index.md` as navigation only; put actual knowledge
   in topic pages.
