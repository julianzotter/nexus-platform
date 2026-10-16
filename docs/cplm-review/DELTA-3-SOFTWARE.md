# CPLM delta review 3/3 — software architecture

Observed 2026-10-16T16:01:19Z. Independent reviewer task instance, sequentially assigned after governance and systems. Read `Folder-current.md` and folder rules v0.3.0 first, then the complete implementation, tests, README and `DELTA-2-SYSTEMS.md`. The status/rules are local snapshots supplied as verified by the coordinator; this reviewer did not independently reread Drive. No implementation edits or external mutations. This review does not establish provider/model diversity.

## Reviewed freeze

| File | SHA256 |
|---|---|
| `cplm-implementation/nexus_cplm/core.py` | `ce48813b31d3aec61b6f18db84688b9b62ad7bba553f176302c811c5fd9d4010` |
| `cplm-implementation/tests/test_cplm.py` | `b7109f40335a1e1b22c885c9d4e1df89081216dd8505be488521ebe7c98b1fb3` |
| `cplm-implementation/README.md` | `490ec96c89bdea0c335d89e4ba524fd23a6ecc8e6b6a50bb22d6ad8082f74a0f` |
| `Folder-current.md` | `458ac2e489138531fdb00ba8cfb5abec589b6d81db83d034a5209d22ab622081` |
| folder rules v0.3.0 | `e5989a79cbba8bf92fb5e976ee359270d108b2f5000477e0aabe058fd4972131` |

Core and tests match the assigned freeze. Python 3.12.14, local Linux filesystem.

## Actual verification

Executed `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v`: **35 tests, 0.300 s, OK**.

- **DS01: corrected for the reported process-death window.** Recovery now reconciles an absent final path to the single actual retained conflict candidate. Zero or multiple candidates fail closed. The actual fork/`os._exit(72)` regression passed: SQLite remains RECOVERY_REQUIRED after death immediately following rename; restart returns an existing evidence file, records its actual filename, preserves its bytes and permits result retry. The missing/ambiguous-evidence countercases also passed. This demonstrates process-death recovery in these windows, not power-loss durability or hostile-host provenance.
- **DS02: corrected with a deny-on-policy-rotation decision.** Receipt handling now checks the run's policy binding in the same transaction as the outbox transition. The regression passed: a restarted kernel with rotated policy rejects the old receipt and retains `(OUTCOME_UNKNOWN, NULL)`. This does not reconcile or deliver that notification; an operational migration/reconciliation path remains open.
- **Earlier C01–C05:** source inspection and the passing regressions support the bounded manifest, freshness, derived-key, conflict-preservation and result-status corrections. Optional release-input hashes bind configured bytes; they do not authenticate receipts or execute the declared suite.

## Finding, risks, improvements and questions

**DSW01 — medium, separation contract needs qualification or enforcement.** README states that a separate human principal releases. The API enforces three distinct reviewer strings and excludes the result author from reviewing, but does not exclude the approving human from those reviewers. A temporary fixture probe added `review` to the existing human principal's grants, accepted that principal's software PASS alongside two other reviewers, and then accepted the same principal's release: `COMPLETED`. This is a policy-configuration counterexample, not a bypass of external authentication. If human/reviewer separation is required, reject overlapping roles at policy load or release and add the countercase; otherwise explicitly document that separation is a deployment policy obligation. No code was changed for this probe.

The SQLite transaction/state API is coherent for participating local writers, but filesystem publication and SQLite commit are deliberately separate. The recovery checks cover finite windows; retained stage files need capacity/retention controls. A unique conflict filename found after restart is not authenticated provenance against another host writer. These limitations fit the documented controlled-host boundary.

Policy validation is partial and the loaded policy is mutable in-process. Before exposing an adapter, use a validated immutable configuration, define recovery/rotation procedures, and document which errors callers reconcile through `get`. Lost success responses generally produce stale-revision errors on retry. Notifications may currently be reserved for RUNNING runs; decide whether a result-only trigger should become a kernel invariant.

## Scoped verdict

**Accept DS01/DS02 repairs and the demonstrated bounded local regression result. Conditional acceptance of the documented API architecture:** resolve DSW01 by enforcing separation or narrowing the contract before claiming that the kernel guarantees a separate human approver. This is not an unconditional release recommendation.

External authentication, genuine reviewer independence, signed human authorization, recipient ACK, Drive integration/atomicity, exclusive cloud writer credentials, provider reconciliation, arbitrary host mutations, Windows/network-filesystem behavior and production operation were not tested or certified. No global rollout or absolute reliability claim follows. Coordinator consolidation and the actual ID01 Human Gate remain separate steps.
