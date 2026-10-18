# Final systems recheck 2/3

Scope: focused local recheck of DS01, DS02 and human/reviewer separation. `Folder-current.md` read first, then the complete current core and tests. Prior report remains unchanged. No implementation or external writes; independent systems task instance, not an assertion of distinct model/provider identity.

## Freeze and actual execution

| File | SHA256 |
|---|---|
| `cplm-implementation/nexus_cplm/core.py` | `76bf6d3c1ae7b573b9cd7cfcaea3300da2e5c222d91f13ffeeb711339bb6c4a9` |
| `cplm-implementation/tests/test_cplm.py` | `31029ba9cd65d097feef476e4b7d5a0a9275a1cc4a50c4f53069d48389a0274a` |

Both match the assigned freeze. Command actually executed:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v`

**36 tests, 0.291 s, OK**, local Linux / Python 3.12.14. No skipped tests reported. This includes actual forked child death via `os._exit(72)` immediately after conflict rename; it does not simulate power loss.

## Verified outcomes

| Item | Observed evidence / conclusion |
|---|---|
| DS01 recovery evidence continuity | Real child exits after rename without Python cleanup. Restart retains RECOVERY_REQUIRED; retry returns an existing evidence file with original conflicting bytes. CONFLICT_ISOLATED event names that same file. Subsequent result succeeds and evidence remains unchanged. **Prior reproduced case closed.** |
| DS01 missing/ambiguous evidence | Zero or two candidate files deny recovery; state remains RECOVERY_REQUIRED, revision 1. Conservative reconciliation avoids inventing an evidence path. |
| DS02 policy rotation | Receipt under a newly loaded policy for an old-policy run raises UNKNOWN_RUN_OR_STALE_POLICY. Outbox remains OUTCOME_UNKNOWN with null receipt. **Prior reproduced case closed.** |
| Human/reviewer separation | Human principal explicitly granted review is rejected with HUMAN_REVIEW_SEPARATION_REQUIRED. Three other reviewers can review and the human can subsequently release. **Regression passes.** |
| Existing local behavior | C01–C05 regression cases, artifact conflict/symlink handling, source freshness, manifest evidence binding, concurrency and outbox deduplication remain green in the same 36-test execution. |

No new blocking finding from this focused recheck. DS01 uses a unique surviving candidate rather than a durable recovery operation ID; multiple candidates deliberately require intervention. This is acceptable for the documented bounded prototype, not proof of all crash histories.

## Remaining risks and recommendation

**LOCAL_RECHECK_PASS for this exact freeze.** The prior DS01/DS02 counterexamples no longer reproduce through their regression tests, and human/reviewer separation is enforced for the configured principal. This approves the reviewed local corrections only.

Host writer races and policy/source TOCTOU remain outside SQLite's protection. Authentication, real ACK, Drive adapters, provider reconciliation, exclusive credentials and production release evidence remain unimplemented/unverified. Stage retention, disk-capacity monitoring, ENOSPC/fsync faults and lost-success-response reconciliation remain follow-up work from the earlier systems review. No production or broad rollout approval, and no absolute reliability claim.

`Folder-current.md` still records PASS_26 and an older CI head; treat it as historical control context, not evidence of this 36-test freeze. Reconcile the control projection with the final consolidation without erasing history.
