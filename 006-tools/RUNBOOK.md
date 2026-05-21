# UTE Toolchain Runbook v1

## Purpose

This runbook defines the recommended operating order for UTE tooling.

It exists to reduce manual drift between:
- the Fact Vault,
- browser proof files,
- topology data,
- machine-readable indexes,
- the live cosmos map,
- and assurance reports.

---

## Standard Workflow

Use this workflow after adding or updating Core Truths.

---

## 1. Add or Update Core Truths

Create or edit truth folders under:

```text
001-fact-vault/UTE-FV-XXXX/
```

Each truth should contain:

```text
entry.md
proof.md
metadata.json
```

---

## 2. Sync Browser Proof Files

Run:

```bash
python 006-tools/proof-sync/sync-browser-proofs-v1.py
```

This copies:

```text
001-fact-vault/UTE-FV-XXXX/proof.md
```

to:

```text
docs/data/proofs/UTE-FV-XXXX-proof.md
```

The Fact Vault remains the source of truth.

---

## 3. Generate Topology Data

Run:

```bash
python 006-tools/topology-generator/generate-topology-v1.py
```

This generates:

```text
docs/data/truth-index-v1.json
docs/data/truth-map-v1.json
docs/data/truth-map-generated-preview.json
docs/data/topology-health-preview.json
003-machine-readable/truth-index-v1.json
003-machine-readable/truth-graph-generated-v1.json
003-machine-readable/topology-health-generated-v1.json
```

---

## 4. Run Assurance Checks

Perform at least Level 1 Assurance before uploading or pushing.

Check:

- root README still correct,
- no PACKAGE-README.md files,
- truth index matches Fact Vault,
- map data matches truth index,
- proof files are browser-accessible,
- `UTE-FV-0001` proof displays in the map,
- live map loads after deployment.

Use Level 2 Assurance before external review or major releases.

---

## 5. Commit and Push

Commit with a clear message.

Examples:

```text
Add spatial geometry foundations v1
Run topology generation after truth update
Sync browser proofs
```

---

## 6. Verify Live Map

After GitHub Pages redeploys, check:

```text
https://universaltruthengine.github.io/universal-truth-engine/
```

Verify:

- map loads,
- node count looks correct,
- proof tabs work,
- dependencies are clickable,
- search and fly-to controls work.

---

## Recommended Tool Order

```text
1. edit Fact Vault
2. sync browser proofs
3. generate topology
4. run assurance
5. commit/push
6. verify live map
```

---

## Important Principle

Manual map repairs should become rare.

UTE should increasingly operate from:

```text
Fact Vault metadata
        ↓
generated topology
        ↓
live cosmos map
```

The long-term goal is a self-consistent, metadata-driven truth topology.
