---
description: "<one line: what this domain covers, in plain language>"
source_refs: "<key source dirs/files this domain owns, comma-separated>"
updated: <YYYY-MM-DD>
---
# <Domain Name>

## Navigation Hints — Self-knowledge (evolves with the project)

| When working on... | Read this page |
|---|---|
| <e.g. webhook signature verification> | `<topic-page>.md` |
| <e.g. order status sync> | `<topic-page>.md` |

## Navigation Hints — Sources-derived (locked, mirrors a raw file in sources/)

| When working on... | Read this page | Raw source |
|---|---|---|
| <e.g. official API field reference> | `<topic-page>.md` | `sources/<wherever the file actually is>` |

> Both tables point into the same flat set of files directly under
> `knowledge/<domain>/` — what makes a page sources-derived is its frontmatter
> (`locked: true` + `source_ref`), not its location. The raw file it mirrors lives in
> `knowledge/<domain>/sources/`, this domain's own data lake — any file type, any
> layout, no required structure. Pages under this heading must not be hand-edited —
> see SKILL.md's sync procedure. If this section has no rows yet, omit it.

## Overview

<2-5 sentences: what this domain is, what external system (if any) it talks to, and
anything a newcomer must know before making changes here.>
