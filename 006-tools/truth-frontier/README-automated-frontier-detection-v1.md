# Automated Frontier Detection v1

## Purpose

Detects plausible next candidate truths from the current UTE truth network.

## Run

```bash
python 006-tools/truth-frontier/detect-frontier-v1.py
```

## Input

```text
003-machine-readable/truth-index-v1.json
```

## Output

```text
003-machine-readable/truth-frontier-report-v1.json
```

## Important

This tool does not accept truths.

It only generates candidate truths for human and LLM review.
