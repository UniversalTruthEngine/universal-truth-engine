# Proof Inspector Restoration & Deep Linking v1

## Purpose

This update restores and strengthens the proof inspection experience inside the UTE interactive cosmos map.

Proof inspectability is a core architectural principle of UTE.

The map should not merely show nodes. It should allow humans and machines to inspect the reasoning structure beneath those nodes.

---

## Core Principle

Every visible truth should expose:
- human-readable explanation,
- proof structure,
- dependencies,
- reconstruction logic,
- and navigable reasoning pathways.

---

## Problems Addressed

As UTE evolved:
- generated preview mode,
- metadata-driven topology,
- proof layering,
- and dynamic graph systems

grew faster than the proof inspector UI integration.

This caused:
- proof rendering regression,
- inconsistent proof loading,
- weak inline inspection,
- and loss of navigable reasoning flow.

---

## Restoration Goals

### 1. Full Proof Rendering

The inspector should load and render:

```text
proof.md
```

for each Core Truth.

---

## 2. Structured Section Detection

The inspector should recognise sections such as:

- Claim
- Plain-Language Explanation
- Step-by-Step Reasoning
- Formal Structure
- Dependencies
- Reconstruction Method
- Failure Cases
- Review History

---

## 3. Dependency Deep Linking

Dependency IDs should become clickable traversal targets.

Clicking:

```text
UTE-FV-0015
```

should allow direct navigation to that truth node.

---

## 4. Curated + Generated Compatibility

Proof inspection should work consistently in:
- curated map mode,
- generated preview mode,
- and future dynamic topology modes.

---

## 5. Performance Stability

Proof loading should:
- lazy-load,
- cache results,
- and avoid large startup payloads.

---

## Final Principle

The map should function as navigable reasoning, not merely visual topology.
