<!--
Append-only action log for the whole knowledge base (not per-domain — this is a
cross-domain "what changed and when" record). One line per action:

## [YYYY-MM-DD] <action> | <domain> | <subject>

<action> ∈ create | update | sync | flag-contradiction | ingest

When this file exceeds ~500 entries, rename it to log-YYYY.md and start a fresh
log.md. `knowledge/_scripts/lint.py` flags when the threshold is crossed.
-->
