# Repository Layering & Integrity Standard v1

## Purpose

This document defines structural repository-layering rules for the Universal Truth Engine (UTE).

As the project grows, architectural consistency must be preserved not only within Core Truths, but also within the repository itself.

The repository structure is part of the epistemic architecture.

---

# Core Principle

The root repository identity should remain stable.

Package updates should not accidentally overwrite the public-facing project presentation.

---

# Stable Root Files

The following files should be treated as stable high-level repository identity files:

```text
/README.md
/LICENSE
```

These files should only be intentionally modified when updating:
- overall project presentation,
- licensing,
- or major repository-wide architectural direction.

Routine package updates should not overwrite them.

---

# Package-Level Documentation

Package-specific documentation should be stored inside the package's relevant directory.

Examples:

```text
002-truth-topology/PACKAGE-README.md
003-machine-readable/PACKAGE-README.md
006-tools/PACKAGE-README.md
docs/PACKAGE-README.md
```

This prevents accidental replacement of the repository introduction.

---

# README Overwrite Prevention Rule

Generated update packages should avoid including:

```text
/README.md
```

unless the explicit purpose of the package is:
- repository presentation repair,
- public introduction updates,
- or intentional root documentation revision.

---

# Recommended Naming Convention

Use:

```text
PACKAGE-README.md
```

for package-scoped explanations.

This distinguishes:
- local package context,
- from repository-wide identity.

---

# Repository Layering Model

UTE repository layers should remain conceptually separated:

```text
Root Repository Identity
    ↓
Project Introduction
    ↓
Governance Layer
    ↓
Core Truth Layer
    ↓
Topology Layer
    ↓
Machine-Readable Layer
    ↓
Tooling Layer
    ↓
Visualisation Layer
```

Each layer should preserve:
- clear responsibility,
- minimal unintended coupling,
- and stable long-term structure.

---

# Archive Integrity Principle

Historical continuity matters.

The repository itself forms part of the UTE historical and epistemic record.

Accidental overwriting of high-level architectural documents should therefore be avoided.

---

# Future Extensions

Future repository integrity systems may include:
- automated overwrite detection,
- protected root files,
- structural consistency checks,
- governance validation pipelines,
- and repository health reports.

---

# Final Principle

The structure preserving the truths should itself be preserved structurally.
