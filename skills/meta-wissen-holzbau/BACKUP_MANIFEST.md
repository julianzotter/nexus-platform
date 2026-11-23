---
name: meta-wissen-holzbau-backup-manifest
description: Review snapshot of the meta-wissen-holzbau skill; Drive stays the document SSOT, newsletters are linked, not copied
version: 1.0.0
status: REVIEW_SNAPSHOT
timestamp: 2026-11-23 (Europe/Vienna)
agent_id: ID06 (Claude)
---
# meta-wissen-holzbau – backup manifest

| Item | Location |
|---|---|
| Skill (this folder) | `skills/meta-wissen-holzbau/SKILL.md` – copy of the skill saved in claude.ai |
| Validator | `tools/validate_holzbau_newsletter.py`, test `tests/test_holzbau_newsletter.py` (runs in existing `CI` workflow) |
| Scheduled task | claude.ai "METAWISSEN HOLZBAU – Wochen-Newsletter", id `trig_01M6Hd5UKgRAZRd2WtdT8utf`, cron `CRON_TZ=Europe/Vienna 47 6 * * 1` |
| Drive target folder | https://drive.google.com/drive/folders/1s3fE047BisUMEog-F_qY-U5p2CzOj5Pi |
| Newsletter KW46/2026 | https://drive.google.com/file/d/1msjtgMTBAdzmKvXhu6XnwuHWy0G-qxi3/view (6274 bytes) |

## Not in this snapshot
- Newsletter files themselves (Drive = document SSOT; sync rule in WORK/Folder.md: review snapshots only).
- No Drive -> GitHub auto-sync workflow: it would need Drive OAuth secrets and commits from Actions, which the WORK sync rule does not permit without ID01 authorization.

## Open finding (2026-11-23)
- Scheduled task fired 2026-11-16 and 2026-11-23, but no `*_METAWISSENHOLZBAU_NEWSLETTER_KW47/KW48.md` exists in the target folder. Cause not investigated.
