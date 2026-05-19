# Storage Efficiency Standard v1

## Purpose

This document defines early principles for keeping UTE efficient as it scales to hundreds, thousands, or more Core Truths.

UTE should remain lightweight, portable, archivable, and inspectable.

---

## 1. Plain Text First

The primary archive should use durable plain-text formats:

- Markdown,
- JSON,
- plain text,
- SVG where diagrams are needed.

Avoid proprietary binary formats as primary sources.

---

## 2. Avoid Unnecessary Duplication

A truth should not repeat large proof text in multiple places.

Recommended pattern:

```text
entry.md
proof.md
machine-readable.json
```

The map should reference proof files rather than embedding full proofs repeatedly.

---

## 3. Summary vs Full Proof

Map data should contain compact summaries.

Full proof files should be loaded only when requested.

This keeps the interactive graph lightweight.

---

## 4. Compression-Friendly Structure

Consistent filenames, schemas, and repeated keys compress well in zip archives and Git storage.

Structured repetition is acceptable if it improves readability and compresses efficiently.

---

## 5. Image Discipline

Images and diagrams should be used carefully.

Prefer:

- SVG,
- simple line diagrams,
- compressed PNG only when necessary.

Avoid large decorative images in the core archive.

---

## 6. Generated Files

Generated files should be clearly marked.

If a file can be regenerated from source data, it may not need to be preserved in every archival copy.

---

## 7. Offline Bundle Goal

UTE should eventually support a compact offline bundle containing:

- Core Truth text,
- proof files,
- machine-readable graph,
- and a static viewer.

A thousand well-structured text-based Core Truths should remain relatively small compared with modern media files.

---

## 8. Practical Size Expectation

If each Core Truth averages 10–30 KB of text and metadata, then:

```text
1,000 truths ≈ 10–30 MB before compression
```

With compression, this may be much smaller.

This is highly practical for replication, offline storage, and long-term archiving.

---

## 9. Final Principle

UTE should be rich in structure but modest in storage demand.

The archive should prioritise durable knowledge, not heavy media.
