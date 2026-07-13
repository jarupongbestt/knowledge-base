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

# Agents available (and when to use them)

- **`investigator`** — deep-dive investigator that answers any requirement / "why does
  X fail" / "why isn't Y working" / "what does <system> require" / setup question with
  **cited evidence**, and never presents a guess as fact. It reads and greps the raw
  sources in its own context and returns a compact cited result, so the heavy reading
  stays out of this (main) context window. See the `root-cause` skill for
  the protocol it follows. Design/rationale: `.claude/investigator-upgrade-spec.md`.

  For any such question, this is a HARD GATE — no exceptions, even when the cause seems
  obvious: you may NOT propose a cause, propose a fix, OR ask the user to go check /
  tell you something, until the `investigator` has run and returned. Delegating to it is
  the FIRST action, not a fallback after you have already theorised or questioned the
  user. Treat "I'll just ask the user what the error is" as a gate violation — the
  investigator (and your own tools) come first. If you are about to type a guess or a
  question to the user before delegating, stop and delegate instead.

# Answering the user — answer-first, low-token

Rigor is in the investigation, not in the length of the reply. When you relay a result:

- **Lead with the decision** in the first line or two. Add supporting detail only when it
  is load-bearing for that decision — do not re-explain everything the investigator
  returned. The investigator's cited evidence stays in its context; surface only what the
  user needs to act.
- **Don't re-narrate.** Two layers (investigator + this loop) must not both emit the full
  story. If the investigator already cited it, reference it — don't re-quote it at length.
- **Option tables / menus only when the user must actually choose.** For a single
  recommended path, state the path; don't enumerate alternatives you won't take.
- Expand into more detail only when the user asks for it.
