---
name: model-effort-router
description: Use before starting a task or work order to pick the Claude model, effort level and fast mode that fit its difficulty and budget, with a one-line reason.
version: 0.1.0
owner: Julian Zotter
tools: none
runtime: claude.ai, Claude Code
---

# Model and Effort Router

Goal: spend tokens where they change the result. Pick model, effort and speed per task, not per habit.

## Facts (snapshot 2026-11-10)
Source: https://www.anthropic.com/claude-fable-and-mythos-5-2 (published 2026-11-09). Re-fetch when a decision hinges on price, limit or availability; say the snapshot date if the fetch fails.
- Vendor guidance: start most coding and knowledge work on Opus 5.5; go up to Fable 5.2 for the most ambitious work; go down to Sonnet 5.5 or Haiku 5.5 when the task allows.
- Effort levels: Low, Medium (default in the apps and Claude Code), High, Xhigh, Max.
- Fable 5.2 price per million tokens: 8 USD input, 40 USD output. Fast mode: 16 / 80 USD, up to 2.5x faster generation.
- Pro and standard Team seats: Fable counts up to 50% of the weekly usage limit.
- Cyber, biology and some AI-R&D topics are blocked or answered by a fallback model; not relevant for structural engineering, relevant for security work.
- Context window size is not stated on the page: unknown.

## Procedure
1. Classify the task in one line: lookup or formatting | routine draft or code edit | multi-step analysis or design calculation | long autonomous run, hard debugging, cross-file refactor, review of safety-relevant results.
2. Map it:

| Class | Model | Effort |
|---|---|---|
| Lookup, formatting, renaming | Haiku 5.5 or Sonnet 5.5 | Low |
| Routine draft, small code edit | Sonnet 5.5 or Opus 5.5 | Medium |
| Multi-step analysis, design calculation, report | Opus 5.5 | Medium to High |
| Long run, hard debugging, final review of liability-relevant work | Fable 5.2 | High; Xhigh or Max only with a stated reason |

3. Fast mode only when waiting time costs more than double token price (deadline, live session). Otherwise off.
4. One step up if the first result fails its acceptance check; never start at Max.
5. Output exactly: `ROUTE: <model> | effort <level> | fast on/off | reason <max 10 words> | est. cost <low/medium/high>`.

## Rules
- The table is a starting rule, not a measurement. If run logs with cost and quality exist, prefer them and say so.
- Claude cannot switch the model itself in claude.ai; the user picks it in the model picker. State the recommendation, do not claim the switch.
- Do not invent prices, limits or benchmark numbers. Unknown stays unknown.
