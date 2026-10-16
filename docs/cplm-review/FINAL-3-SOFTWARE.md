# CPLM final recheck 3/3 — software architecture

Observed 2026-10-16T16:04:53Z. Independent software reviewer task instance, sequenced after final governance and systems by the coordinator. Read `Folder-current.md` first, then complete current core/tests, README and proposed `AGENTS.repo.md`. No other final review was used as evidence. Live Drive status was not independently accessed; this is a local snapshot/code review, not current cloud-governance verification. No implementation or external edits.

## Exact reviewed files

| File | SHA256 |
|---|---|
| `nexus_cplm/core.py` | `76bf6d3c1ae7b573b9cd7cfcaea3300da2e5c222d91f13ffeeb711339bb6c4a9` |
| `tests/test_cplm.py` | `31029ba9cd65d097feef476e4b7d5a0a9275a1cc4a50c4f53069d48389a0274a` |
| `README.md` | `490ec96c89bdea0c335d89e4ba524fd23a6ecc8e6b6a50bb22d6ad8082f74a0f` |
| `AGENTS.repo.md` | `c34435dcc6aa8f571f3114cfb072f91eb3f8b4697540e09b74d39849993ec581` |

Paths are relative to `cplm-implementation/`. Core/tests match the assigned final freeze.

## Execution and findings

Executed `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v`: **36 tests, 0.273 s, OK**, Python 3.12.14, local Linux filesystem.

**DSW01 is corrected in the reviewed local API.** `review()` explicitly rejects the configured human principal with `HUMAN_REVIEW_SEPARATION_REQUIRED`, even with a review grant. The new regression exercises that denial and then proves that three other reviewer principals can review and the human can release. Distinct reviewer/perspective constraints and author exclusion remain intact. The human/reviewer-string counterexample reported in DELTA-3 is closed; real identity and independence still require the external adapter.

DS01 actual child-process death/restart recovery and missing/ambiguous-evidence denial passed again. DS02 stale-policy receipt denial passed again. Earlier bounded manifest, source freshness, notification-key, artifact recovery and status checks remain green. No new blocking local software issue was identified in this checkpoint.

The proposed repository entrypoint correctly presents instructions rather than authentication/enforcement, requires current sources and explicit limits, and preserves final review/human gates. Its candidate filename is not evidence that an active repository `AGENTS.md` was installed or that its linked Drive source is accessible/current. Deployment and live-source verification remain coordinator work.

## Verdict and remaining boundaries

**PASS for the reviewed bounded local prototype and DSW01 correction**, suitable for consolidation and a concrete human review of this exact package. This supersedes DELTA-3's conditional local architecture verdict; the historical finding remains preserved.

Before adapter deployment, retain the existing improvement items: validated immutable policy configuration, lost-response reconciliation, notification rotation/recovery procedures and evidence retention/capacity controls. Filesystem/SQLite operations are not one atomic transaction; these finite process-death tests do not establish power-loss durability.

External authentication, actual human authorization, real reviewer independence, remote recipient ACK, Drive integration/atomicity, exclusive cloud writer access, provider reconciliation and arbitrary host mutations are **not certified**. Windows, network filesystems, multi-host operation and production deployment are not approved by this review. No absolute reliability claim or global rollout approval follows; consolidation and ID01's actual decision remain separate.
