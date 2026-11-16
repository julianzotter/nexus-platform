---
name: oauth-registry-repair
description: Repair GitHub<->Drive OAuth (HTTP_400) and run the pending CAS registry/ledger append
version: 1.0
status: READY – step 1 needs ID01 on PC (browser consent); steps 2-3 automated
timestamp: 2026-11-16T23:30+01:00
---
# OAuth + Registry repair (ID06, 2026-11-16)

## Diagnosis
- `oauth.token_refresh` → HTTP_400 on every GitHub→WORK / Drive→GitHub run since **2026-11-13 00:06 UTC** (37 failures, 0 successes in last 100 runs).
- Continuous failure from one point in time = refresh token invalid (`invalid_grant`), not a code bug.
- Most likely cause (not proven): OAuth consent screen in **Testing** status → Google expires refresh tokens after 7 days. Other causes: password change, manual revoke, >100 tokens per client.

## Step 1 – ID01 on PC (≈5 min)
1. Google Cloud Console → APIs & Services → OAuth consent screen → **Publish app** ("In production"). Unverified own-use app is fine; prevents the 7-day expiry.
2. In `C:\Users\<USER>\nexus-platform`: `git pull` then
   `pip install -r tools/oauth-setup-requirements.txt`
   `python tools/configure_drive_oauth.py --client-json <Desktop-client.json> --publish` (first rename an existing `.nexus-credentials/drive-oauth.json`; browser consent with julian.zotter@gmail.com; writes the 3 secrets, prints no values).
3. Check: GitHub → Actions → "NEXUS GitHub to WORK" → Run workflow (latest Monitor run id) → preflight must not show HTTP_400.

## Step 2 – registry/ledger append (automated, single writer)
GitHub → Actions → **NEXUS Registry Append** → plan `registry/pending/2026-11-16_ID06_registry-append.json`.
- Ledger `00_ID_LEDGER.csv` (same ID 1Qso4VQE…): fill-only 0210 DRIVE_ID/SHA256, 0211 DRIVE_ID + `SELF_SEE_FILE_REGISTRY`.
- `file-registry.jsonl` (same ID 15m8T5cW…): +13 events (0201–0211 artifacts, Folder.md, ID02 report 2308), idempotent.
- CAS: aborts with `CAS_CONFLICT` if either file changed since 2026-11-16 23:20 (expected SHA in plan) → regenerate plan, rerun.
- Dry-run against live bytes 2026-11-16: PASS (ledger → c810907f…, registry 460→473 lines, 69c81adf…).

## Step 3 – verify
Artifact `registry-append-result.json`: `status=REGISTERED_VERIFIED`, readback SHA = written SHA.

## Rule going forward
Registry/ledger writes only via this workflow (concurrency group `nexus-registry-single-writer`); no rename+re-upload (changes Drive IDs).
