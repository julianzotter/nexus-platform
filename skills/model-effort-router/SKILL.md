---
name: model-effort-router
description: Pick the Claude model and effort level for a task before starting it. Use when planning a run, splitting a work order, or when cost, speed or token budget matters.
version: 0.1.0
owner: Julian Zotter
tools: WebFetch
runtime: any
---

# Model and Effort Router

## Source
- https://www.anthropic.com/claude-fable-and-mythos-5-2 (snapshot 2026-11-10, page dated 2026-11-09).
- Prices, limits and model names change: re-fetch the page before quoting a number. If the fetch fails, say the figure is from the snapshot.

## Rules (from the source)
1. Default for coding and knowledge work: Opus 5.5.
2. Move up to Fable 5.2 only for the most ambitious, open-ended work.
3. Move down to Sonnet 5.5 or Haiku 5.5 for simple, high-volume steps.
4. Advisor pattern: a smaller model does the work and consults Fable 5.2 on the hard parts.
5. Orchestrator pattern: Fable 5.2 plans and delegates simple subtasks to smaller models.
6. Effort levels: Low, Medium, High, Xhigh, Max. Medium is the app default. Raise effort only when a lower level failed a stated check.
7. Fast mode costs twice the standard token price; use it only when waiting time is the bottleneck.

## Snapshot figures
| Item | Value |
|---|---|
| Fable 5.2 standard | 8 USD in / 40 USD out per million tokens |
| Fable 5.2 fast mode | 16 USD in / 80 USD out, up to 2.5x faster generation |
| Speed vs 5.1 | up to 30 percent faster output |

## Procedure
1. Classify the task: routine | standard | open-ended or long-horizon.
2. Name the acceptance check (test, hash, hand calculation, reviewer).
3. Choose the cheapest model and effort that can plausibly pass the check.
4. State the escalation step if the check fails (one level of effort first, then one model tier).
5. Output one line: `MODEL | EFFORT | PATTERN | CHECK | ESCALATION`.

## Limits
- Topics routed away from Fable 5.2 (most cyber work, most research biology, some accelerator-kernel work) run on a fallback model: do not plan Fable-level quality for them.
- Benchmark scores do not prove fitness for a structural calculation; the acceptance check decides.
