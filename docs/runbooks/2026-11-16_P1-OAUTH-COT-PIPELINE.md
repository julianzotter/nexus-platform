---
name: p1-oauth-cot-pipeline
description: Stepwise CoT pipeline with binary gates to repair Drive OAuth (HTTP_400) and run the pending registry append
version: 1.0
status: READY_FOR_ID01 – S1-S6 manual on PC/browser, S7-S9 GitHub
timestamp: 2026-11-16T23:30+01:00
---
# #P1 OAuth repair – CoT pipeline (ID06)

Rule: each step = Reason → Action → Gate (binary). Gate FAIL → stop, take the listed fallback, log it.

| S | Reason (why) | Action | Gate PASS when | FAIL → |
|---|---|---|---|---|
| S0 | Know the baseline | GitHub → Actions → last "NEXUS GitHub to WORK" run | preflight shows `oauth.token_refresh` `HTTP_400` | other reason → stop, report text |
| S1 | Find the OAuth client in use | console.cloud.google.com → APIs & Services → Credentials | a **Desktop** OAuth client exists in the NEXUS project | none → create "Desktop app" client |
| S2 | Remove 7-day token expiry | OAuth consent screen → Publishing status | status = **In production** (click *Publish app*) | org policy blocks → accept 7-day renew, schedule weekly S4 |
| S3 | Need client secret file | Credentials → Desktop client → **Download JSON** → save e.g. `C:\Users\<USER>\nexus-oauth-client.json` (outside Drive) | file has `"installed"` key | `"web"` key → wrong client type, back to S1 |
| S4 | Tool refuses existing target | in `C:\Users\<USER>\nexus-platform`: if `.nexus-credentials\drive-oauth.json` exists → **rename** to `drive-oauth_OLD_2026-11-16.json` (move-only) | target path free | — |
| S5 | Prepare tooling | `git pull` · `pip install -r tools/oauth-setup-requirements.txt` · `gh auth status` | all exit 0; gh logged in as julianzotter | gh not logged in → `gh auth login` |
| S6 | New refresh token + secrets | `python tools/configure_drive_oauth.py --client-json C:\Users\<USER>\nexus-oauth-client.json --publish` → browser: julian.zotter@gmail.com → Allow | output `"oauth_complete": true, "published": true` | `No refresh token` → revoke app at myaccount.google.com/permissions, repeat S6 |
| S7 | Prove read+write access | `python tools/configure_drive_oauth.py --check --require-write` | `status: READ_ACCESS_VERIFIED` | HTTP_400 again → S2 not effective / wrong client → S1 |
| S8 | Restore sync | GitHub → Actions → "NEXUS GitHub to WORK" → Run workflow (latest Monitor run id) | job green; receipt `DELIVERY_VERIFIED` | read job log, report |
| S9 | Close registry gap | GitHub → Actions → "NEXUS Registry Append" → plan `registry/pending/2026-11-16_ID06_registry-append.json` | result `REGISTERED_VERIFIED`; registry 460→473 lines | `CAS_CONFLICT` → ask ID06 to regenerate plan |

## Done criteria (all binary)
- S7 PASS · S8 green · S9 REGISTERED_VERIFIED · next scheduled sync run green without manual trigger.

## Log
Record per step: time, PASS/FAIL, evidence (run URL / output line) → append to WORK status 0213 or reply to ID06 in chat.

## Security
Never paste token/secret values into chat, Drive or GitHub files; the tool prints none. Client JSON stays outside synced folders.
