# Knowledge base

Before reading or searching any other file in this repo, ALWAYS read `knowledge/main.md`
first — no exceptions, even for tasks that look trivial. It routes you to the domain
that already has the relevant context, so you don't need to scan the whole repo.

This repo keeps durable, domain-organized knowledge in `knowledge/` (separate from
code). Use the `knowledge-base` skill for the full read/write procedure — which domain
to follow from `main.md`, and how to record anything a task teaches you.

Before writing any knowledge page, ask **external resource vs. internal project
work** — this decides the folder, not how important or permanent the fact feels:
- **External** — a file/doc/spec/data the user gives you, or anything already under a
  domain's `sources/` — even after you summarize/reformat/translate it, and even if
  it isn't copied into `sources/` yet (land a copy there first) → `derived/`. Never
  `self/`, no matter how much rewriting you did or how directly the user asked for it
  ("make a knowledge page from this file" is still an external source → `derived/`).
- **Internal** — came from doing the project's own work (debugging, reading its code,
  a decision made during a task), with no external file or doc involved → `self/`.
