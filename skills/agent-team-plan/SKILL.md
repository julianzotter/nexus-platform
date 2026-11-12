---
name: agent-team-plan
description: Turn one large task into an orchestrator plus subagent plan with a verification gate per work package. Use for migrations, audits, formalisation, multi-file builds or any job too large for one context window.
version: 0.1.0
owner: Julian Zotter
tools: none
runtime: any
---

# Agent Team Plan

## Source
- https://www.anthropic.com/claude-fable-and-mythos-5-2 (snapshot 2026-11-10).
- Reported there: multi-agent runs with a coordinating model, large reviewer pools, and results accepted through machine-checkable evidence (tests, proofs, benchmarks).

## Principles
1. One orchestrator owns the plan and the state file; workers never share context by assumption.
2. Every work package fits one context window, input plus output.
3. Every package has a binary acceptance check that a different agent or a script runs.
4. The executing agent never approves its own package.
5. Simple packages go to smaller models; the strongest model plans and resolves conflicts.
6. Nothing counts as done without a written result, its hash, and a log line.

## Procedure
1. Pre-parse: measure the job (files, characters, items) with a script, not by estimate.
2. Split into packages; for each write: ID, input files, expected output, acceptance check, model tier, reviewer.
3. Order by dependency; mark what can run in parallel.
4. Define the state file (one row per package: status, output path, SHA-256, reviewer verdict).
5. Run a pilot of one to three packages; fix the template before fan-out.
6. Fan out; collect; re-run only failed packages.
7. Final check on the assembled result, then a human decision.

## Output
Table: `ID | Input | Output | Check | Model tier | Reviewer | Depends on`, followed by the state-file path and the pilot selection.

## Do not
- Start fan-out before the pilot passed.
- Report a package as verified when only the executor looked at it.
- Simulate runs or results.
