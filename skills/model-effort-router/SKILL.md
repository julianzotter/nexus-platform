---
name: model-effort-router
description: Use before starting a costly or multi-step task, or when asked which Claude model or effort level to use, to pick model, effort and advisor/orchestrator pattern with a stated reason.
version: 0.1.0
owner: Julian Zotter
tools: none (decision table); web fetch for re-verification
runtime: Claude web, desktop app, Claude Code
status: ENTWURF
timestamp: 2026-11-10T15:35:00+01:00
---

# Model and Effort Router

Goal: spend tokens where they buy quality. One routing decision per task, stated in one line, before work starts.

## Source

- https://www.anthropic.com/claude-fable-and-mythos-5-2 (read 2026-11-10).
- Prices, benchmarks and defaults change. If the decision hinges on a number, re-fetch the page first. If the fetch fails, use the snapshot below and say it is dated 2026-11-10.
- Benchmarks are vendor-reported. They rank options; they do not prove fitness for a specific NEXUS task. Fitness = own test run.

## Snapshot (2026-11-10)

- Vendor guidance: start with Opus 5.5 for most coding and knowledge work; go up to Fable 5.2 for the hard part, down to Sonnet 5.5 / Haiku 5.5 for simple volume work.
- Fable 5.2 price: 8 USD / 1M input tokens, 40 USD / 1M output tokens. Fast mode: up to 2.5x speed at 16 / 80 USD.
- Default effort in apps and Claude Code: medium.
- FrontierCode 2.0: Xhigh 49.1 %, High about 45.3 % at roughly half the cost per task. Delta = 3.8 points for about 2x cost.
- Two documented patterns: Advisor (small model works, consults Fable on hard steps) and Orchestrator (Fable plans, delegates simple steps to small models).
- Fable 5.2 limits: AI-R&D topics (accelerator kernels, LLM architecture) are held near Opus 5.5 level; blocked cyber / biology queries fall back to older Opus models. For those topics Fable gives no gain.

## Decision table

| Task | Model | Effort | Pattern |
|---|---|---|---|
| Lookup, formatting, renaming, short summary | Haiku 5.5 / Sonnet 5.5 | low | single |
| Routine code, report, WorkOrder draft | Opus 5.5 | medium | single |
| Structural calculation chain, norm check, review of own draft | Opus 5.5 executes, Fable 5.2 reviews | high | Advisor |
| Large job with many similar sub-tasks (inventory, migration, batch audit) | Fable 5.2 plans, small models execute | medium | Orchestrator |
| Novel or stuck problem after one failed run | Fable 5.2 | high | single |
| Xhigh / Max effort | only with a stated measurable gain | - | - |
| Fast mode | only when a deadline is at risk (2x price) | - | - |

## Procedure

1. Classify the task with the table. If two rows fit, take the cheaper one.
2. State the decision in one line: `ROUTE: <model> | <effort> | <pattern> | reason: <=8 words`.
3. Escalate one step only after a measured failure (wrong result, failed test), never on feeling. Log the escalation in the same line format.
4. Executor and reviewer must differ (EXEC != PEERREVIEW).
5. One run = one main goal. If the task does not fit one context window, split it first, then route each part.

## Rules

- Never claim a model was used that the session cannot select. If the model cannot be switched here, output the recommendation and mark it `NOT APPLIED`.
- No routing line for trivial one-step answers.
