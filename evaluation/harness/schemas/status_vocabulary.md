# STATUS VOCABULARY v1.1 (freeze candidate) — source v1.0 line 129
| status | definition | trigger | next states |
|---|---|---|---|
| PASS | all hard gates PASS | loop exit | SUPERSEDED |
| FAIL | ≥1 gate FAIL, refinements remain | G3/G1 fail, r<3 | PASS, FAIL, NEEDS_REVIEW |
| NEEDS_REVIEW | 3 refinements exhausted OR judge disagreement; input complete | r==3 & no PASS; judge≠grader | PASS, FAIL (after human) |
| BLOCKED | required input/tool/permission missing — cannot run | G1 fail, missing file/hash | FAIL, PASS (after input) |
| SOURCE_GAP | claim without source; run otherwise valid | G2 fail, source absent | PASS (source added), NEEDS_REVIEW |
| SOURCE_CONFLICT | ≥2 sources disagree, no authority_rule | G2/G3 fail with conflict | PASS (rule set by human) |
| REGRESSION | child run worse than parent on golden case | G4 fail | FAIL, SUPERSEDED |
| SUPERSEDED | replaced by later run/version | new run_id with same case | — (terminal) |
| ~~PARTIAL~~ | **MERGE → FAIL** | — | — |

MERGE PROPOSAL (Human Gate)
- PARTIAL overlaps FAIL (some gates pass, some fail). FAIL already carries gates{} per gate → PARTIAL adds no information. DROP.
- NEEDS_REVIEW vs SOURCE_GAP: distinct — NEEDS_REVIEW = input complete, judgement needed; SOURCE_GAP = input incomplete. KEEP both.
- Result: 8 states, 1 terminal (SUPERSEDED), 2 human-only exits (NEEDS_REVIEW, SOURCE_CONFLICT).
NEW markers: G5.scope=production_only; deltas max 3; auto_apply const false; escalation enum.
