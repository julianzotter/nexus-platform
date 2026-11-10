---
name: orchestrator-reviewer-split
description: Use when a task is too large for one run or needs independent checking, to split it into an orchestrator plan, small worker runs and separate reviewer runs with a merge rule.
version: 0.1.0
owner: Julian Zotter
tools: subagents when available, otherwise work-order files
runtime: claude.ai, Claude Code, other LLMs via work orders
---

# Orchestrator / Worker / Reviewer Split

Goal: one strong model plans and merges; cheaper runs do bounded pieces; reviewers that did not see the work check it. Executor and reviewer are never the same run.

## Background (snapshot 2026-11-10)
Source: https://www.anthropic.com/claude-fable-and-mythos-5-2. The release describes two roles: an orchestrator that hands simpler tasks to smaller models, and an advisor that smaller models consult on hard problems. It reports long agentic runs with many subagents, including a security audit run with about 170 reviewer agents. These are vendor reports, not own measurements.

## Procedure
1. **Scope line**: goal, deliverable, acceptance criteria that can be observed (test passes, value within tolerance, file exists with hash).
2. **Cut**: split into pieces that each fit one context window with their inputs. Each piece gets: input files, exact output file and schema, stop condition. No piece depends on chat memory.
3. **Assign**:
   - Orchestrator (strongest model): plan, cut, merge, final statement.
   - Workers (smaller model or other LLM): one piece per run.
   - Reviewers (fresh context, different model family where possible): get the output and the acceptance criteria, not the worker's reasoning.
   - Advisor call: a worker that is stuck writes a short question file; the orchestrator answers once.
4. **Review rule**: each reviewer returns PASS or FAIL with evidence (line, value, source). For calculations, at least one reviewer recomputes independently instead of reading along.
5. **Merge**: only PASS pieces are merged. FAIL goes back once with the finding; a second FAIL is reported as open, not smoothed over.
6. **Record**: per piece one line in the run log: piece, executor, reviewer, verdict, output hash.

## Output
```
PLAN <task>
Pieces: #1 <name> -> <executor> / <reviewer> ... 
Acceptance: <criteria>
Runs needed: <n>   Review runs: <n>
```

## Rules
- No simulated runs: a piece counts only if it was actually executed and its output exists.
- Reviewer count follows risk: 1 for drafts, 2 for code that ships, independent recomputation for structural results.
- Without subagents, write the pieces as work-order files and say that execution is pending.
- Final sign-off on liability-relevant results stays with the human.
