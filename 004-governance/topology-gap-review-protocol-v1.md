# Topology Gap Review Protocol v1

## Purpose

Define how UTE reviewers should respond to detected topology gaps.

## Core Rule

A topology gap is not a truth.

It is a review prompt.

---

## Review Questions

For each detected gap, ask:

1. Is this a genuine missing region?
2. Is the gap caused by incomplete data?
3. Is the current truth chain too shallow?
4. Is there a missing bridge truth?
5. Should the Truth Frontier Engine propose candidates?
6. Should the gap be dismissed?

---

## Review Outcomes

- confirm_gap
- dismiss_gap
- request_candidate_generation
- request_human_review
- request_llm_review
- defer

---

## Governance Principle

Gap detection should precede candidate generation.

UTE should first identify where knowledge may be missing before attempting to name the missing truth.
