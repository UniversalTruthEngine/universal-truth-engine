# 2026-06-02 — Run Candidate Generation in Workflow v1

## Purpose

Updates the UTE Assurance workflow so candidate generation actually runs in GitHub Actions.

## Updated File

```text
.github/workflows/ute-assurance.yml
```

## Expected Result

The workflow should produce a real generated artifact:

```text
ute-frontier-candidates
```

rather than relying on placeholder candidate JSON files committed to the repository.
