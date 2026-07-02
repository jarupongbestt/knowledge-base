---
description: "Field reference for the payment gateway's webhook payload, mirrored from the vendor's OpenAPI spec"
source_ref: "knowledge/_example/sources/payment-gateway/openapi.yaml"
locked: true
synced: 2026-07-02
---
# Payment gateway webhook fields

Mirrors the `WebhookPayload` schema in
`knowledge/_example/sources/payment-gateway/openapi.yaml` as of the `synced` date above.

This page and the file it mirrors are two different things: the raw file sits in
`sources/`, untouched, with no prose; this page is its readable mirror, living as a
normal topic page directly under `knowledge/_example/`, right next to
`retry-backoff.md`. Do not add detail here that isn't in the raw file — if you learn
something about *how we handle* these fields, that's self-knowledge and belongs in
`retry-backoff.md` instead.

| Field | Type | Notes (from vendor spec) |
|---|---|---|
| `status` | string | One of `succeeded`, `failed`, `pending_retry` |
| `retry_after_ms` | integer | Present only when `status = pending_retry` |
| `order_ref` | string | Merchant-supplied order ID, echoed back verbatim |

If `knowledge/_example/sources/payment-gateway/openapi.yaml` changes, re-run the sync
procedure in SKILL.md to regenerate this page — don't hand-edit it in the meantime.
