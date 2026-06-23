# Candidate Generation Workflow Execution Standard v1

## Purpose

Ensure the UTE Assurance workflow executes candidate generation rather than leaving placeholder reports in the repository.

## Workflow Principle

The repository may contain placeholder report files, but GitHub Actions should generate live reports during workflow execution.

## Execution Order

```text
1. Regenerate truth index and truth graph
2. Generate frontier candidates
3. Run truth arithmetic engine
4. Run truth merge review
5. Run truth derivation audit
6. Run UTE Assurance
7. Detect topology gaps
8. Upload generated reports as artifacts
```

## Key Artifact

```text
ute-frontier-candidates
```

This artifact should contain:

```text
003-machine-readable/frontier-candidates-v1.json
003-machine-readable/frontier-report-v1.md
docs/data/frontier-candidates-v1.json
```

## Governance Rule

Generated candidates are not accepted truths. They are review prompts only.
