---
name: model-effort-router
description: Choose a Claude model, supported effort and single, Advisor or Orchestrator pattern before costly or multistep work. Use for work-order planning, model selection, cost, speed and token budgets. Require an acceptance check and escalation plan before cost-relevant routing.
---

# Model and Effort Router

Version: 0.2.0
Status: ENTWURF
Owner: Julian Zotter
Runtime: any; actual model and effort controls depend on the execution surface.
Tools: read-only official documentation fetch; deterministic tests where available.
Updated: 2026-11-12
Activation: BLOCKED until skill validation, current-head PR CI, independent review, official model-information verification and explicit ID01 approval all pass.

Choose one route per task before execution. Spend tokens only where they improve the named acceptance result. This draft recommends routes; it does not activate another model or authorize delegation, spend, credentials, merges or engineering release.

## Evidence and verification

Keep the 2026-11-10 snapshot as historical input, not operational truth. Recheck official model IDs, availability, effort support, prices, benchmarks and surface-specific fallback behavior before activation and whenever a routing decision depends on them. Record source URL, section, retrieved date, surface and claim status. Failed fetch or missing entitlement means BLOCKED for the dependent route; never use an unverified price to authorize spend.

Official sources inspected 2026-11-12:
- https://www.anthropic.com/claude-fable-and-mythos-5-2 — announcement, 2026-11-09, Introduction and Evaluating sections. VERIFIED as vendor publication: Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5 names; Advisor/Orchestrator patterns; Fable standard USD 8 input / 40 output per million tokens; fast USD 16 / 80; vendor-reported FrontierCode 2.0 score 49.1% at Xhigh. Not an independent benchmark replication.
- https://platform.claude.com/docs/en/models/fable-5-2/overview — Specifications and How it compares. VERIFIED as current API documentation: claude-fable-5-2, default effort high.
- https://platform.claude.com/docs/en/models/opus-5-5/overview — Specifications and How it compares. VERIFIED as current API documentation: claude-opus-5-5, default effort medium, USD 4 input / 20 output per million tokens.

Do not generalize an API default to Claude apps or Claude Code. Snapshot claim “medium everywhere” is superseded by the documented model-specific API defaults. Account access, exact effort choices per surface, High ~45.3% / half-cost benchmark comparison and fallback targets remain UNVERIFIED here. Do not infer fallback quality or eligibility. Inspect the current official refusal/fallback documentation for the actual surface before relying on it; do not route to evade safeguards.

Historical snapshot provenance: both PR #69 and main used the announcement above, dated 2026-11-10 in their snapshots. Preserve the original versions in Git history. Up-to-30% output speed and up-to-2.5x fast-mode claims are vendor upper bounds, not latency guarantees or whole-task speedups.

## Decision table

All concrete model selections below are recommendations, contingent on verified availability and supported effort. Compare estimated total task cost, including retries and review; “cheapest” requires current pricing and a task-specific estimate.

| Task | Candidate | Effort | Pattern | Mandatory acceptance check |
|---|---|---|---|---|
| Lookup, formatting, renaming, short summary | Haiku 5.5 / Sonnet 5.5 | lowest supported that passes | single | exact match / readback; full mapping for batch changes |
| Routine code, report, work-order draft | Opus 5.5 | medium if supported | single | tests / diff / required-field checks |
| Structural calculation chain or norm check | Opus 5.5 executor; Fable 5.2 independent reviewer | high if supported | Advisor | deterministic solver + independent reference + input/norm review |
| Many similar inventory, migration or audit items | Fable 5.2 planner; eligible smaller model executors | supported task-specific level | Orchestrator | every item validated + justified sample review |
| Novel problem after measured failure | eligible stronger model, potentially Fable 5.2 | high if supported | single | reproducible acceptance result |
| Xhigh / Max | only if surface supports it and measurable gain is stated | supported level | selected pattern | same acceptance check; explicit budget |
| Fast mode | only if waiting time threatens the deadline | supported level | selected pattern | same quality check; verified premium and budget |

## Mandatory acceptance gate

Before EVERY cost-relevant route, including paid low-effort or Haiku work, name the observable acceptance check, threshold, inputs, budget boundary and escalation trigger. No acceptance check → no route. Do not define cost relevance by model tier or effort alone.

Use tests, exact diffs, byte hashes, deterministic reference calculations and independent review as appropriate. A hash proves byte identity only; sampling three files cannot certify all forty renames. An LLM is not the numerical authority for structural calculations. Use deterministic software, applicable norm edition/national annex and an independent reference before any engineering claim.

EXEC != PEERREVIEW: require a real separate reviewing instance that did not produce the draft, with recorded executor_instance and reviewer_instance. Merely changing a model label is insufficient. The same model family in a separate instance can review independently; a different model name alone does not prove independence. Self-review may supplement, never replace, the independent check. If the required reviewer is unavailable, keep REVIEW_PENDING and block acceptance/release.

Advisor consultation is assistance, not automatically independent peer review. Keep the reviewer separate from both the executor and any advisor that co-produced the result. Escalation to a reviewer model must use a new executor instance and preserve an independent reviewer.

## Procedure

1. Classify the task. If two rows fit, choose the lower estimated total cost among candidates that can pass the check.
2. State acceptance threshold and budget before cost is incurred. Missing check, evidence or spend authorization → BLOCKED for execution.
3. Verify current official model data and actual runtime selection/effort capability. If switching is unavailable, mark the recommendation NOT APPLIED.
4. For review patterns, record actual independent instances and their roles. Obtain separate authorization before spawning agents.
5. Output: `ROUTE: <model> | <effort> | <pattern> | check: <threshold> | esc: <trigger/step> | budget: <boundary> | reason: <=8 words | applied: <YES/NOT APPLIED>`.
6. One run = one main goal. Split oversized work into bounded contexts, route each part and preserve a shared evidence/result ledger without concurrent writes.
7. Execute only an authorized route. Record actual model, surface, test result and cost evidence; report missing fields as unknown.

## Escalation and limits

- Escalate one step after a measured failure: raise supported effort first, then model tier if necessary. Never change both at once. Reconfirm budget and independent review. Stop after the agreed retry limit; never loop unboundedly.
- Log `ESCALATE: <old route> -> <new route> | cause: <failed check> | evidence: <test reference>`. A benchmark score never replaces the acceptance check.
- Use fast mode only for waiting-time constraints; a token-price multiplier is not a measured task-cost multiplier.
- Do not promise Fable-level output for blocked or fallback-routed topics; actual fallback behavior and suitability remain surface-specific and must be verified.
- Do not add routing ceremony for trivial non-cost-relevant one-step answers. Retain the acceptance gate for any cost-relevant case.

## Worked examples

Illustrative recommendations, NOT APPLIED; model availability, effort support and task budget must be confirmed first.

1. Single — “Rename these 40 files and summarize each in one line.”
   `ROUTE: Haiku 5.5 | lowest supported | single | check: all 40 source-target pairs unique + complete readback; inspect 3 summaries as sample only | esc: failed mapping -> Sonnet 5.5 at same supported effort | budget: ID01-approved task cap required | reason: simple volume | applied: NOT APPLIED`.
2. Advisor — “Check this beam against EC3 and review your own numbers.”
   `ROUTE: Opus 5.5 exec + Fable 5.2 advisor; separate reviewer instance | high if supported | Advisor | check: deterministic calculation + independent reference; norm edition/NA and units verified | esc: failed check -> one supported effort step; retain independent reviewer | budget: approved calculation/review cap required | reason: calculation needs independent verification | applied: NOT APPLIED`.
3. Orchestrator — “Migrate 200 config files to the new schema.”
   `ROUTE: Fable 5.2 plan + Sonnet 5.5 exec | supported task-specific effort | Orchestrator | check: schema + semantic checks on all 200; independent 10% sample with all failures reviewed | esc: failed files -> Opus 5.5 at same supported effort | budget: approved batch/retry cap required | reason: many similar independent items | applied: NOT APPLIED`.

## Promotion checklist

- PASS: frontmatter contains exactly name and description; no conflict markers; three examples retained.
- REQUIRED: current-head skill validation and repository CI receipts; disclose existing failures instead of weakening gates.
- REQUIRED: official verification of all operational model assumptions, especially surface effort and fallback behavior; unresolved snapshot values cannot drive routing.
- REQUIRED: actual independent review with version/hash; explicit ID01 activation approval. Merge approval and activation approval are distinct. Until then keep v0.2.0 / ENTWURF.
