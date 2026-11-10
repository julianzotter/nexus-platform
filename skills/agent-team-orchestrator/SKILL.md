---
name: agent-team-orchestrator
description: Use when a job is too large for one run (inventory, migration, batch audit, multi-file build) and should be split into parallel sub-agents with separate reviewers and a hash-checked result ledger.
version: 0.1.0
owner: Julian Zotter
tools: sub-agents, file tools, shell (sha256), git
runtime: Claude Code and Claude sessions with sub-agent support
status: ENTWURF
timestamp: 2026-11-10T15:35:00+01:00
---

# Agent Team Orchestrator

Goal: finish large jobs by splitting them into small, independently checkable work packages. The orchestrator plans and verifies; it does not do the packages itself.

## Source

- https://www.anthropic.com/claude-fable-and-mythos-5-2 (read 2026-11-10): vendor-reported cases of long jobs run by agent teams (about 170 reviewer agents for a 10-12 h security audit; over 1,000 sub-agents coordinated over eight days; orchestrator delegating simple steps to smaller models).
- These cases show the pattern scales. They are not a test of this skill. Status of this skill: untested draft.

## When NOT to use

- The job fits one run. Sub-agents start cold and re-derive context; that costs more than it saves.
- Packages depend on each other's results step by step. Then run them in sequence in one session.

## Procedure

1. **Pre-parse run** (own run, no execution): list inputs, count items, estimate size. Output `PLAN.md`: goal, acceptance test per package, package list.
2. **Cut packages**: each package fits one context window, has one output file, one acceptance test, no shared write target. Start small: at most 5 packages in the first wave.
3. **Brief each executor** with a standalone prompt: goal, inputs (paths), output path, acceptance test, forbidden actions (no delete, no email, no writes outside the output path). No reference to chat history.
4. **Route models** with `model-effort-router`: orchestrator = strongest model; executors = smallest model that passes the acceptance test.
5. **Review**: every package is checked by a reviewer that did not produce it (EXEC != PEERREVIEW). The reviewer runs the acceptance test and reports PASS or FAIL with evidence. No opinions.
6. **Ledger**: append one line per package to `RUNLOG.jsonl`: `{package, executor, reviewer, output_path, sha256, test, result, timestamp}`. Append-only.
7. **Consolidate**: only PASS packages are merged. FAIL packages are re-issued once with the reviewer's finding; a second FAIL is escalated to the human with the evidence.
8. **Close**: status report = counts (planned / PASS / FAIL / open), deltas to the previous wave, links to `PLAN.md` and `RUNLOG.jsonl`.

## Rules

- A package is done only when its output exists, its hash is in the ledger and its test is PASS. A sent brief is not a done package.
- Never report simulated runs. If sub-agents are unavailable, say so and run the packages in sequence.
- Safe mode by default: nothing deleted, no emails, writes only to the planned output paths.
- Human gate (ID01) before anything is merged to a main branch or declared released.
