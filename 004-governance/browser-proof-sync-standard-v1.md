# Browser Proof Sync Standard v1

## Purpose

This standard defines how proof files should be made available to the live UTE cosmos map.

## Core Principle

The Fact Vault remains the source of truth.

The browser-served proof files under:

```text
docs/data/proofs/
```

are generated serving copies.

They should not be treated as the primary proof record.

---

## Required Source

Each Core Truth should provide:

```text
001-fact-vault/UTE-FV-XXXX/proof.md
```

---

## Required Browser Copy

Each browser proof copy should be:

```text
docs/data/proofs/UTE-FV-XXXX-proof.md
```

---

## Map Requirement

Map node data should point to browser-accessible proof paths:

```json
"proof_file": "data/proofs/UTE-FV-XXXX-proof.md"
```

---

## Assurance Requirement

After running proof sync:

- verify browser proof files exist,
- verify `UTE-FV-0001` proof opens in the map,
- verify proof tabs display content,
- verify no map node points to a missing proof path.

---

## Final Principle

Proof accessibility is part of UTE's human-readability standard.
