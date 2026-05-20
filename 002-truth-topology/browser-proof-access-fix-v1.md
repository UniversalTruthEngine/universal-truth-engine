# Browser Proof Access Fix v1

## Verified Issue

The cosmos map could not display proof files because node proof paths pointed outside the GitHub Pages served `docs/` directory.

Example broken browser path:

```text
../001-fact-vault/UTE-FV-0001/proof.md
```

GitHub Pages serves the site from `docs/`, so the browser could not reliably access repository files outside that served site context.

## Fix

This update creates browser-accessible proof copies under:

```text
docs/data/proofs/
```

and updates map data so nodes use:

```text
data/proofs/UTE-FV-XXXX-proof.md
```

It also restores tabbed inspector display:
- Summary
- Proof
- Dependencies
- Raw Proof

## Rule Going Forward

The Fact Vault remains the source of truth.

The `docs/data/proofs/` files are browser-serving copies for the live map.

Future tooling should generate these copies automatically from the Fact Vault.
