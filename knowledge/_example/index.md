---
description: "Worked example domain — shows the self-knowledge vs sources-derived split in practice. Not a real domain, ignore for actual work."
source_refs: "n/a — illustrative only"
updated: 2026-07-02
---
# Example Domain (illustrative only)

> This domain is not real. It exists so people and agents can see the two-kinds
> structure filled in with actual content, instead of just an empty template. Do not
> add rows for it to `knowledge/main.md`'s Domains table.

## Navigation Hints — Self-knowledge (evolves with the project)

| When working on... | Read this page |
|---|---|
| payment retries timing out silently | `self/retry-backoff.md` |

## Navigation Hints — Sources-derived (locked, mirrors a raw file in sources/)

| When working on... | Read this page | Raw source |
|---|---|---|
| exact fields/values the payment gateway's webhook sends | `derived/field-reference.md` | `sources/payment-gateway/openapi.yaml` |

## Overview

A payment integration domain. The two pages below live in separate folders under
`knowledge/_example/` — that folder is what distinguishes them, not just their
frontmatter:

- `self/retry-backoff.md` has no `source_ref` — it's a lesson the team learned while
  building the retry logic (self-knowledge; nobody handed this to us, we found it the
  hard way, and it'll keep changing as the retry logic evolves).
- `derived/field-reference.md` has
  `source_ref: knowledge/_example/sources/payment-gateway/openapi.yaml` and
  `locked: true` — it's a straight mirror of that raw file (sources-derived; only
  updated when that file changes).

The raw file itself lives in `knowledge/_example/sources/`, this domain's own data lake
— any file type, any layout, whatever a real vendor drop looks like (a Dockerfile, a
nested `ui/src/test.tsx`, a PDF spec, this OpenAPI YAML, anything). Compare
`derived/field-reference.md` against `sources/payment-gateway/openapi.yaml` directly:
the raw file is untouched YAML with no prose; the knowledge page is its readable,
faithful mirror. Never confuse the two — a raw file is not knowledge, and a knowledge
page is not a raw file.
