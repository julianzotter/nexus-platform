# CPLM delta review 2/3 — systems and resilience

Observed 2026-10-16T15:58:02Z. Independent task instance, sequentially assigned after governance; that review output was not read. Full core, tests and README read. RUN-4 was consulted for the earlier C01–C05 goals, not as evidence that this delta works. No implementation edits or external actions performed. This is a bounded local review, not production certification or proof of model/provider diversity.

## Reviewed freeze

| File | SHA256 |
|---|---|
| `cplm-implementation/nexus_cplm/core.py` | `d6f095a63e5d2e7d632fe5ec4a1ddd6946c136cbe612a1c63ed3e94f3c330ec1` |
| `cplm-implementation/tests/test_cplm.py` | `2cab5231c1cc85a26b55a515c1018475ebd4d9e9050e8ff060b94ab9ff59b2e0` |
| `cplm-implementation/README.md` | `490ec96c89bdea0c335d89e4ba524fd23a6ecc8e6b6a50bb22d6ad8082f74a0f` |

Core and tests match the assigned hashes. Python 3.12.14, local Linux filesystem.

## Actual execution

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v`

**32 tests, 0.405 s, OK.** Tests cover the C01–C05 regressions plus local concurrency, staged publication, symlinks, malformed frontmatter and release-evidence mutation. These are fixture tests, not real authentication, notification or remote-store tests.

Three additional probes ran against temporary fixture directories, using the existing test fixture and unmodified implementation. The first two terminated an actual child process with `os._exit`, rather than raising an exception that the transaction manager could catch.

| Probe | Observed result |
|---|---|
| Exit 71 after artifact publication and RESULT_VERIFIED event insertion, before SQLite commit | Restart: RUNNING, revision 0, complete final artifact present. Same result retry: RESULT_VERIFIED, exact expected bytes. Confirms this tested process-death window recovers without duplicate final artifact. |
| Exit 72 after conflict `os.replace`, before directory sync and recovery DB commit | Restart: RECOVERY_REQUIRED, revision 1, final path absent, one conflict file retaining `conflict`. Recovery retry then result retry succeeded. **Recovery returned a nonexistent new evidence path**, despite the earlier conflict file still existing. |
| Reserve email under policy P1; add policy revision field, restart under P2; attempt reservation and receipt | Reservation rejected `UNKNOWN_RUN_OR_STALE_POLICY`; `notification_receipt` nevertheless accepted and changed the old outbox row to SENT. |

These probes do not simulate power loss, storage-controller durability or disk failure.

## Findings and changes requested

**DS01 — medium: recovery evidence linkage is not crash-consistent.** `recover_artifact_conflict` moves evidence outside the SQLite transaction. Death after rename rolls back the DB transition. The next call invents a fresh evidence name, finds no target, records CONFLICT_ISOLATED with that unused name and returns it. Bytes remain preserved and execution can recover, so this is not observed data loss. It falsifies an unconditional interpretation that the returned/recorded recovery evidence path always identifies the preserved conflict. Persist a recovery operation/evidence identifier before rename, reconcile it on restart, and test death immediately after rename. Require the completed recovery receipt to identify the actual retained evidence or explicitly state that no target existed.

**DS02 — low/contract clarification: receipt transition omits the run-policy boundary.** `notification_receipt` checks current actor grants and current channel-derived key, but never checks the associated run's policy hash. Thus a stale-policy run rejected by reservation can still receive a SENT transition after restart. This has no observed release bypass or external send. Decide whether historical receipts should remain ingestible after policy rotation. If yes, bind them explicitly to the original reservation/policy and document this exception; otherwise enforce the same run-policy check as reservation. Add a regression for the intended decision.

**C01–C05:** the prior concrete counterexamples are addressed in the reviewed local scope: reviews require a post-result manifest; sources are rechecked before review/release; outbox keys are derived from canonical configuration; partial/conflicting artifacts have an explicit recovery state and preserved evidence; result status is constrained. DS01 qualifies the completeness of recovery auditing. Optional release-input roles bind file bytes, not actual execution or authenticity; README states this correctly.

## Risks, improvements and open questions

- Notifications have at-most-one local reservation, not guaranteed eventual delivery. A crash after reservation but before sending intentionally leaves OUTCOME_UNKNOWN; reconciliation is absent. Confirm the operational owner and escalation deadline for this stalled state before transport integration.
- Successful mutators are not uniformly replay-idempotent: e.g. a committed result or release retried at its old revision is rejected. Recovery can use `get`, but adapters need explicit reconciliation rules for lost success responses. Add focused lost-response tests when adapters are built.
- Stage files are intentionally retained, with no quota or cleanup policy. Repeated interrupted writes can exhaust storage. Define evidence retention and capacity monitoring; test ENOSPC/fsync failures and recovery-rename fault boundaries before expanding the resilience claim.
- SQLite serializes participating kernel writers; source/policy/host writer races remain outside this prototype's boundary. No claim is made here that read/hash/check sequences lock external files or prevent privileged edits.
- Open question: should result notifications be reservable while execution is still RUNNING? This is currently permitted; a future result-only adapter must enforce its trigger contract or add a state gate.

## Recommendation

Accept the C01–C05 corrections as demonstrated progress for the bounded Linux prototype, with **DS01 requiring repair and re-test before claiming complete crash-recovery evidence continuity**. Resolve/document DS02 before adapter integration. The observed local suite is green; resilience coverage remains finite. Production authentication, real recipient ACK, Drive adapters, provider reconciliation and host writer exclusion are explicitly unimplemented and are neither tested nor certified by this review. No absolute reliability or broad rollout approval is given.
