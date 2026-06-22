# Truth Frontier Engine v1

## Purpose

Identifies candidate next truths enabled by the current UTE truth network.

## Run

```bash
python 006-tools/truth-frontier/generate-truth-frontier-v1.py
```

## Important

This tool does not accept truths automatically.

It only proposes candidates for:

- human review,
- LLM review,
- assurance,
- soundness review,
- adversarial review.

## Output

```text
003-machine-readable/truth-frontier-candidates-v1.json
```
