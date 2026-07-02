---
description: "Why payment retries must back off by order ID, not globally, or the gateway rate-limits the whole account"
source_refs: "src/payments/retry.ts"
updated: 2026-07-02
---
# Payment retry backoff

Retries are keyed per order ID, not global. A shared global backoff timer looked
simpler and was tried first, but the gateway's rate limit is per-account, and a burst
of unrelated retries hitting at the same moment triggered a full-account throttle that
also blocked brand-new (non-retry) payments for ~60s.

Decision: each order ID gets its own exponential backoff state, jittered independently,
so retries naturally spread out instead of clustering.

See `field-reference.md` for the exact status codes the gateway returns — this page
only covers the retry *strategy*, not the wire format.
