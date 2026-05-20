# 2026-05-20 — Public State Sync Repair v1

## Purpose

This update repairs public-facing drift found during Level 1 assurance.

## Verified Issues Addressed

- Raw root README formatting was compressed.
- Public truth index listed only 29 truths while the Fact Vault had expanded to UTE-FV-0037.
- Live map remained stuck at the loading stage due to malformed `docs/graph.js`.
- Browser-facing map data needed to include UTE-FV-0030 through UTE-FV-0037.

## Included Fixes

- Rewrites root README with normal Markdown structure.
- Replaces `docs/graph.js` with a syntactically clean viewer script.
- Updates `docs/data/truth-index-v1.json` to include UTE-FV-0001 through UTE-FV-0037.
- Updates `docs/data/truth-map-v1.json` to include UTE-FV-0001 through UTE-FV-0037.
- Adds browser-accessible proof copies for all current map nodes.

## Manual Cleanup Still Required

Delete the accidental root folder:

```text
upload-these-files/ 000-introduction
```

This cannot be reliably removed by a web upload package.
