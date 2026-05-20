# Level 2 Assurance Protocol v1

## Purpose

Level 2 Assurance is a deeper verification exercise for the Universal Truth Engine before external review, major expansion, or public demonstration.

Level 1 checks whether obvious repository and map components are present.

Level 2 checks whether the system is internally consistent enough to be reviewed by external humans or AI systems.

---

# When to Run Level 2 Assurance

Run Level 2 Assurance:

- before sending UTE for external review,
- after major map repairs,
- after adding a new Core Truth cluster,
- after changing `docs/`,
- after changing machine-readable graph/index files,
- after proof-system changes,
- or whenever Level 1 finds drift.

---

# Verification Classifications

All findings must be labelled as:

| Classification | Meaning |
|---|---|
| Verified | Directly inspected from repository, live site, or raw file |
| Inferred | Derived from verified evidence |
| Proposed | Suggested action |
| Unverified | Not checked yet |

---

# Level 2 Checklist

## 1. Repository Identity

Verify:

- root `README.md` renders as Universal Truth Engine overview,
- root does not contain `PACKAGE-README.md`,
- root structure is clean,
- `ORIGIN.md` and `LICENSE.md` remain present.

## 2. Fact Vault Integrity

Verify:

- all expected Core Truth folders exist,
- each truth folder has `entry.md`,
- each truth folder has `proof.md`,
- each truth folder has `metadata.json`,
- IDs are not duplicated,
- metadata IDs match folder names.

## 3. Truth Index Alignment

Verify:

- `docs/data/truth-index-v1.json` exists,
- `003-machine-readable/truth-index-v1.json` exists if expected,
- truth index includes the current highest truth ID,
- truth index and Fact Vault agree.

## 4. Map Data Alignment

Verify:

- `docs/data/truth-map-v1.json` exists,
- map node IDs match truth index IDs,
- all map dependencies resolve to known truth IDs,
- no map node points to a missing proof file.

## 5. Proof Accessibility

Verify:

- browser-accessible proof files exist under `docs/data/proofs/`,
- proof paths in map data point to those browser-accessible files,
- selecting a node in the live map shows proof text,
- key node `UTE-FV-0001` shows detailed Pythagorean proof.

## 6. JavaScript / Viewer Integrity

Verify:

- `docs/graph.js` is syntactically valid,
- live site does not remain stuck on loading,
- search/fly-to controls populate,
- clicking nodes opens inspector,
- dependency traversal still works.

## 7. Update Log Integrity

Verify:

- `updates/README.md` exists,
- recent significant updates have entries,
- update logs do not replace root README.

## 8. Assurance Report

Create or update:

```text
003-machine-readable/level-2-assurance-report-vX.json
```

The report should include:

- verified findings,
- failures,
- corrective actions,
- unresolved risks,
- whether external review is approved.

---

# Pass / Fail Criteria

## Level 2 Pass

External review may proceed if:

- root README is correct,
- live map loads,
- truth index matches current Fact Vault,
- map data matches truth index,
- proof inspection works for `UTE-FV-0001`,
- no broken dependency references exist,
- no root `PACKAGE-README.md` exists.

## Level 2 Fail

Do not send for external review if:

- live site is stale,
- map data is stale,
- proof inspection is broken,
- root README is wrong,
- or truth index omits newly added truths.

---

# Final Principle

External review should only happen after UTE can truthfully represent its current state.
