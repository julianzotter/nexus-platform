---
name: model-release-watch
description: Use when the user shares a model or product release page (Anthropic, OpenAI, Google, DeepSeek and others) and wants it analysed, to extract dated facts and derive concrete changes to routing rules, skills and work orders.
version: 0.1.0
owner: Julian Zotter
tools: web fetch
runtime: claude.ai, Claude Code
---

# Model Release Watch

Goal: turn a release announcement into a small set of dated facts and at most three concrete changes, without marketing language.

## Procedure
1. Fetch the page the user gave. If it cannot be fetched, say so and stop; do not answer from memory.
2. Extract into a fact table, each row with the page as source and the fetch date:
   - model names and IDs, availability, plans
   - prices, speed modes, effort or reasoning settings
   - limits (context, usage share, retention); write `not stated` when absent
   - new roles or features (orchestration, advisor, tools)
   - restrictions and fallbacks (blocked topics, fallback models)
   - benchmark numbers only as `vendor-reported`, with the comparison model
3. Delta: compare against the current routing rules and skills (model-effort-router, orchestrator-reviewer-split, work-order templates). List only rows where something changes.
4. Derive at most three actions, each as: `#A1 -> <what changes> -> <where> -> <test that shows it helped>`.
5. Mark what is unverified: vendor claims, missing numbers, anything not on the page.

## Output
```
RELEASE <name> <date>  source <URL>  fetched <YYYY-MM-DD>
Facts: table
Delta: bullets
Actions: #A1..#A3
Unverified: bullets
```

## Rules
- Benchmarks are the vendor's own results; never restate them as own findings.
- No recommendation to switch models without a named task class and a way to measure the difference.
- Keep quotes out; restate in own words and link the source.
- One release per run.
