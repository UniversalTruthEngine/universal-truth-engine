# UTE Core Truth Soundness Review v1

## Purpose

Performs a lightweight conceptual soundness review of Core Truth entries.

This tool does not prove truths automatically. It flags review risks for human/AI inspection.

## Usage

Run from repository root:

```bash
python 006-tools/soundness-review/run-soundness-review-v1.py
```

## Checks

- entry presence
- proof presence
- metadata validity
- metadata ID consistency
- dependency presence
- proof section completeness
- proof depth heuristic
- overclaiming language

## Output

```text
003-machine-readable/core-truth-soundness-review-v1.json
```
