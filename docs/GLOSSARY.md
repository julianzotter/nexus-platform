# NEXUS-AI SYSTEM — SHARED LANGUAGE & GLOSSARY

**Status:** canonical system glossary · updated 2026-10-27  
**Scope:** NEXUS-AI-AEC OS · governance · knowledge · deterministic engineering · runtime · delivery · Critical Gate Watch  
**Rule:** technical workflow status ≠ evidence status ≠ gate status ≠ human approval ≠ production release.

## Core system language

| Term | Canonical meaning |
|---|---|
| Task | Scoped unit of work with owner, acceptance criteria, dependencies and a human gate (`schemas/task.schema.json`). |
| Agent | Role with an explicit list of allowed skills and tools. |
| Skill | Module/folder with manifest, I/O schemas, tests and owner. |
| Evidence | Measured, reproducible fact backing a claim. Never pre-filled or guessed. |
| Gate | Binding control/approval condition. Missing mandatory evidence is not PASS. |
| Human Gate | Explicit authorized human decision point; absence of decision is never approval. |
| Knowledge item | Registered unit of knowledge with stable ID shared with the NEXUS-AI-AEC knowledge graph. |
| Norm | Standard clause with edition, national annex and validity status. |
| Solver | Deterministic, unit-tested calculation authority. LLMs orchestrate/call solvers; they are not arithmetic authority. |
| Run | One execution of a task/workflow with recorded inputs, outputs and scores. |
| Delta | Verified difference between a run/current observation and its baseline. |
| Baseline | Previous verified comparison state. |
| Score | Measured accuracy, confidence and cost of a run. |
| SSOT | Single Source of Truth: designated authoritative source for a defined information domain. |
| Canonical | Authoritative under applicable NEXUS governance. |
| Governance | Binding rules for authority, ownership, evidence, transitions, review, merge, release and human decisions. |
| Fail-closed / FAIL_CLOSED | Missing, contradictory or incomplete critical evidence cannot produce a positive gate/release state. |
| P0 | Highest Watch criticality; immediate critical control/security/integrity condition. |
| P1 | High-priority blocking control/operational defect below P0. |

## Integrity · ledger · evidence

| Term | Canonical meaning |
|---|---|
| Vollhash-Readback | Retrieve complete persisted object and verify full-content cryptographic hash (normally SHA-256) against expected hash. |
| Rohbyte-Readback | Verification from actual retrieved bytes, not metadata/filename/summary alone. |
| ID Ledger / 00_ID_LEDGER.csv | Governed registry mapping stable NEXUS IDs to artifact identity/version/state. |
| Ledger-Konsistenz | Ledger IDs, versions, names, hashes and state markers agree with verified artifacts and ledger rules. |
| Kanonischer Ledger-Konflikt | Authoritative ledger identity/state contradicts verified artifact evidence. |
| SSOT-Konflikt | Authoritative source contradicts verified system reality or another source expected to represent the same canonical state. |
| CURRENT | Ledger marker for governed current version; stale/contradictory CURRENT records are integrity conflicts. |
| append-only | Preserve history by appending successor versions instead of destructively replacing historical evidence. |
| CAS | Compare-And-Swap: accept write only if prior observed state/version still equals expected state. |
| Drive-Metadaten | Provider properties such as stable file ID, filename, timestamps and ACL; not a substitute for content hash where byte identity matters. |
| Drive-ID | Stable provider object identifier independent of filename. |
| ACL / WORK-ACL | Access permissions; Watch treats WORK `anyone:writer` as critical. |
| Primärnachweis | Evidence emitted/owned directly by the system/component whose state is asserted. |

## Runtime · repository · delivery

| Term | Canonical meaning |
|---|---|
| MAIN / CI | Repository `main` state plus relevant Continuous Integration result. CI SUCCESS proves only executed CI checks passed. |
| Merge | Integration of PR/branch into target. Merge ≠ review ≠ governance approval ≠ release. |
| Branchschutz | Repository controls restricting changes/merges and requiring defined reviews/checks. |
| Scheduler | Mechanism triggering workflows at configured intervals. |
| Slot | Expected scheduled execution occurrence. |
| Schedule-Liveness | Evidence scheduled automation executes at expected slots. |
| P1-Liveness-Lücke | Expected slots lack execution evidence; continuous operation is not demonstrated. |
| Monitor | Workflow/component evaluating critical gates and emitting evidence/status. |
| Monitorartefakt | Persisted Monitor output; semantic payload controls gate interpretation, not wrapper SUCCESS alone. |
| Poller | Repeating component checking upstream state/events/results. |
| Joblog | Execution record/output used to inspect actual job behavior. |
| Native Delivery | Intended production-like delivery path executed by native automation, not connector/manual substitute. |
| Credential-Preflight | Check that required credentials/secrets exist and are usable before delivery. |
| BLOCKED_DRIVE_CREDENTIALS | Native Drive delivery blocked by unavailable/invalid/unusable credentials. |
| E2E | Complete intended chain from source through processing/delivery to target verification. |
| E2E-Erfolg | Verified native end-to-end completion including required final readback/integrity verification. |
| Coverage | Completeness of required checks/gates/skills. |
| FALSE_GREEN | Outer workflow reports SUCCESS while internal evidence is BLOCKED/INCOMPLETE/failed. |

## Status vocabulary

| Status | Canonical interpretation |
|---|---|
| SUCCESS | Technical execution completed successfully; NOT automatically gate PASS or release. |
| FAILURE | Workflow/job terminated unsuccessfully. |
| INCOMPLETE | Required evidence/coverage/output missing; never promote to PASS. |
| BLOCKED | Required completion cannot proceed because prerequisite/blocker remains unresolved. |
| NO_NEW_P0_P1 | No newly detected P0/P1 vs baseline; existing blockers may remain open. |
| NO_NEW_TECHNICAL_P0_P1 | No new technical P0/P1; governance/human issues may remain. |
| NEWLY_DETECTED_P1 / NEW_P1_* | New P1 or newly verified contradiction since baseline. |
| KNOWN_BLOCKERS_OPEN | Previously identified blockers remain unresolved. |
| LEDGER_CONFLICT_OPEN | Known ledger conflict remains unresolved. |
| NATIVE_E2E_BLOCKED | Native E2E delivery/verification cannot be proven successful. |
| HUMAN_GATE_PENDING | Required human decision has not been evidenced. |
| HUMAN_GATE_REQUIRED | Next valid transition requires explicit human decision. |
| HUMAN_REVIEW_REQUIRED | Human review required before approval/release semantics. |
| P1_HUMAN_CHECKPOINT_OVERDUE | Defined human checkpoint passed without required authenticated decision evidence. |
| NOT_GRANTED | Required permission/approval has not been granted. |
| NO_PRODUCTION_RELEASE | Production release explicitly not authorized/proven. |
| GOVERNANCE_SSoT_CONFLICT | Governance-controlled SSOT contradicts verified system state. |
| NEW_P1_LEDGER_CONFLICT | Newly detected P1 ledger inconsistency. |

## ACK · ownership · release

| Term | Canonical meaning |
|---|---|
| CLAIM | Authenticated assertion that assigned actor has taken ownership of dispatched work. |
| ACK | Authenticated acknowledgement of receipt/review/acceptance under the workflow. |
| Consumer ACK | Authenticated acknowledgement by designated downstream consumer. |
| Owner | Role accountable for resolving a gate/blocker or producing evidence. |
| Next Action | Required action assigned to owner; not evidence the action occurred. |
| Release / Produktionsfreigabe | Explicit authorization for production use/deployment. |
| ID01 | Source role associated with governance review, ACL and Human-Gate/release decisions; exact authority remains in governance records. |
| ID03 | Source role associated with ledger/registry correction/reconciliation. |
| ID05 | Review/acceptance role referenced in human-checkpoint chain. |

## CPLM

| Term | Canonical meaning |
|---|---|
| CPLM | Named NEXUS audit/reporting process. No acronym expansion asserted without authoritative source. |
| CPLM-Bericht | Versioned CPLM output documenting observed state, blockers and/or evidence. |
| CPLM-Audit | CPLM report used as audit input; subject to canonicality and independent verification, not automatically SSOT. |

## Critical semantic invariants

1. `workflow SUCCESS` ≠ `gate PASS`.
2. `CI SUCCESS` ≠ `Native Delivery SUCCESS`.
3. `Merge` ≠ `Review` ≠ `Production Release`.
4. `NO_NEW_P0_P1` ≠ `NO_OPEN_P0_P1`.
5. `INCOMPLETE` or missing critical evidence ⇒ `FAIL_CLOSED`.
6. formal `SUCCESS` + internal `BLOCKED/INCOMPLETE` ⇒ `FALSE_GREEN`.
7. Connector-assisted readback ≠ native E2E proof.
8. Metadata consistency ≠ full-content integrity.
9. Missing ACK/CLAIM/Human-Gate evidence ≠ implicit acceptance.
10. New documentation ≠ new runtime/delivery/release evidence.
11. Known blocker remains open until positive resolution evidence is verified.
12. Conflicting canonical state ⇒ raise SSOT/ledger conflict; never silently reconcile.

## Critical Gate Watch owner mappings

- **CI-Ops → Schedule-Liveness:** restore/prove expected executions.
- **Repository-Admin → Native Delivery:** establish authorized prerequisites and native E2E evidence.
- **Repository-Admin → Branchschutz:** establish/verify required `main` controls.
- **ID03 → Ledger-Korrektur:** reconcile IDs/names/hashes/version states while preserving history.
- **ID01 → ACL/Human Gate:** explicit governance/access/release decision.

## State precedence

```yaml
evidence: [VERIFIED, INCOMPLETE, CONFLICT]
delta: [NO_NEW_P0_P1, NEW_P0, NEW_P1, RESOLUTION_VERIFIED]
gate: [PASS, INCOMPLETE, BLOCKED, FAIL]
human_gate: [NOT_GRANTED, PENDING, GRANTED]
release: [NO_PRODUCTION_RELEASE, RELEASE_GRANTED]
rule: positive downstream state requires all mandatory upstream evidence/gates
missing_or_conflicting_evidence: FAIL_CLOSED
```

## Interpretation boundary

Definitions above consolidate the pre-existing repository glossary with the verified Critical Gate Watch vocabulary. Where an authoritative source does not define an expansion or exact role authority (notably CPLM and full ID01/ID03/ID05 authority), this glossary does not invent one.
