---
name: model-release-digest
description: Read an AI model release page and extract a checkable fact sheet for the benchmark register. Use when a new model, version or pricing page appears, or when comparing vendor claims.
version: 0.1.0
owner: Julian Zotter
tools: WebFetch
runtime: any
---

# Model Release Digest

## Purpose
Convert a vendor announcement into rows that can be compared across models and re-checked later. First applied to https://www.anthropic.com/claude-fable-and-mythos-5-2 on 2026-11-10.

## Procedure
1. Fetch the page. If only part was read, say so.
2. Extract into the tables below; copy numbers exactly, with units.
3. Tag every claim: `VENDOR_INTERNAL` | `CUSTOMER_REPORTED` | `EXTERNAL_EVALUATOR` | `NOT_STATED`.
4. Record the test condition next to each score: effort level, tools on or off, which variant of the model, comparison models.
5. List what the page does not state (for example context window or output limit) as `NOT_STATED`; never fill gaps from memory.
6. Mark scores from differing conditions as not directly comparable.
7. End with: three claims worth reproducing on own benchmark cases, and the open questions.

## Tables
- Identity: `Model | API string | Date | Availability | Predecessor`
- Cost: `Mode | Input price | Output price | Speed claim`
- Benchmarks: `Benchmark | Score | Condition | Compared with | Provenance tag`
- Restrictions: `Topic | Behaviour | Fallback`
- Usage guidance: `Recommendation | Source sentence location`

## Rules
- A vendor benchmark is a claim, not a measurement of own use cases.
- Keep the page URL and fetch date in the header of the digest.
- No recommendation without naming the acceptance test that would confirm it.
