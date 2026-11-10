---
name: REPORT_SKILL-SYNC-FABLE52
description: Status report - three skills derived from the Fable/Mythos 5.2 release page, archived in WORK and pushed to GitHub as draft PR 67; ledger and registry rows not written
version: 0.1.0
status: PARTIAL - WORK archive DONE, GitHub draft PR DONE (CI pass), ledger/registry BLOCKED, human gate OPEN
timestamp: 2026-11-10T15:40+01:00
tasks_done: 3 SKILL.md archived in WORK; draft PR 67 with CI success; duplicate with PR 66 removed from branch
tasks_open: ledger row in 00_ID_LEDGER.csv; row in file-registry.jsonl; _FRONT_LOG.md append; ID01 decision on PR 67; save skills from proposal card
problems: Drive connector of this session creates files but cannot update content; three chats ran the same sync in parallel (PR 66, 67, 68)
open_questions: Which chat allocates ledger IDs; keep or close PR 67; where is the canonical skill path (skills/ or skills/claude-ai/)
result: byte source hashes below; upload bound to SHA-256 by the connector; size readback equal; no independent byte-hash readback
executor: ID06 Claude (claude-fable-5-2, cloud session), authorised by ID01 chat request 2026-11-10 15:31 and 15:33
---

# Report: skill sync, Fable 5.2 release page

## Evidence
| Artifact | SHA-256 (source bytes) | Bytes | Drive ID (WORK) | Size readback |
|---|---|---|---|---|
| model-effort-router/SKILL.md | 6767e2e28d0cf65c2fdeff7850d347cf2798d266f26e71c65c99dcb2fe3d67bd | 2122 | 1jC8cSTqfcBDmXnAXEoCOkdkeP_x6tVDG | 2122 |
| agent-team-plan/SKILL.md | dd84b42550aa9019f06162ebbc8c51fd61e63aba9d0523df8285d36b9d3bdaf1 | 1927 | 1xj08N7m6FwsNPj8H1vdAxDKMNjgUnO3B | 1927 |
| model-release-digest/SKILL.md | 27f29ea148248e9fabd3175595b569bdf479f80b6508edab37fb179483a19dc5 | 1707 | 1NKXoC_kB6VaoSQsGVMjAs9VOIfq_GFrX | 1707 |
| artifacts-capabilities/SKILL.md (duplicate, see below) | 9d4595d14698481f953a3a4fe48cbd2b0f8f968457d92d9e1df814c0f07c89e8 | 5215 | 12im3xNSF7qW5i4WSfRpBWL0lolloKSEm | 5215 |

## GitHub
- Repo julianzotter/nexus-platform, branch skills/artifacts-capabilities (name historical), head b495987621681c2cd45ae211d556e914750f9a70.
- Draft PR: https://github.com/julianzotter/nexus-platform/pull/67
- CI run (workflow CI, job test): success, https://github.com/julianzotter/nexus-platform/actions/runs/42835873734
- tools/skill_inventory.py --strict: 6 packages, 3 VALID_STRUCTURE (new), 3 INCOMPLETE (existing), 0 INVALID.

## Deviations (NEXUS continuity principle, safe mode: nothing deleted, no e-mail sent)
1. No ledger ID: 00_ID_LEDGER.csv and file-registry.jsonl were not changed. File names carry UNREGISTERED.
2. No _FRONT_LOG.md append and no Folder.md update, same cause.
3. Drive file 12im3xNSF7qW5i4WSfRpBWL0lolloKSEm (artifacts-capabilities) duplicates the snapshot of PR 66; left in place, not deleted.
4. Parallel sessions: PR 66 (nine account skills), PR 68 (nexus-start, workspace-housekeeping, nexus-settings-kit) were opened by other chats within one minute of PR 67.
5. Readback is by size plus connector-side SHA-256 binding of the upload, not by an independent hash of downloaded bytes.
6. The skills exist in Claude only as a proposal card until saved; saved frontmatter will differ from the repo copy (repo adds version, owner, tools, runtime).

## Source
- https://www.anthropic.com/claude-fable-and-mythos-5-2 (fetched 2026-11-10)

## Log
- 2026-11-10 15:33 PR 67 opened (first scope: artifacts-capabilities + CI step), CI success on c5430d7b.
- 2026-11-10 15:36 Rescoped to three new skills, duplicate removed, CI success on b4959876.
- 2026-11-10 15:37 Three SKILL.md files created in WORK.
- 2026-11-10 15:40 This report written.
