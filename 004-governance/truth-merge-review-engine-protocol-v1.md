# Truth Merge Review Engine Protocol v1

## Purpose

Define how UTE should detect and review duplicate or near-duplicate truth concepts.

## Core Rule

One active concept should normally have one authoritative Core Truth unless there is a clear scope distinction.

## Review Actions

Allowed recommendations:

```text
retain
merge
supersede
historical_alias
scope_distinguish
review_required
```

## Safety Rule

No automated process may delete or merge a truth.

A merge review report is advisory only.

## Why This Matters

Candidate generation will sometimes rediscover existing truths.

Before UTE can self-expand safely, it must distinguish:

```text
existing truth
near duplicate
refinement
new candidate
```
