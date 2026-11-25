---
name: 26_11_25_1629_ID03_NEXUS-CONTROL-PANEL_REAL-REFRESH_v1.2.0_LEDGER-PENDING.md
created_at: 2026-11-25T16:29:00+01:00
role_id: ID03
owner_id: ID01
version: DRAFT-v1.2.0
runtime: ChatGPT + GitHub/Google Drive connectors
registration_status: LEDGER-PENDING
review_status: PEER_REVIEW_REQUIRED
release_status: NO_RELEASE
---
# NEXUS Control Panel v1.2.0 — Engineering status / independent review request
## Source evaluation
ID05 acknowledged non-deployment of Perplexity offline drafts. Production Sites panel v4.1 displays data observed 2026-11-23 13:43:51 CET on 2026-11-25. No evidence that its refresh triggers actual provider synchronization. ID05 v0.3.0 is client-only awaiting a feed.

## Delivered (actual GitHub commit + test)
- GitHub draft PR https://github.com/julianzotter/nexus-platform/pull/135
- Branch id03/control-panel-real-refresh-20261125
- commit ced5dc62147054384bedfccb78cc09b85d4c5bf7
- Actual read-only server.py requests OAuth-authorized WORK Drive folder metadata and GitHub open PR metadata using real HTTP calls, exposing GET /api/v1/control-panel/snapshot on local 127.0.0.1:8766.
- Dashboard HTML ↻ fetches server endpoint, validates response/revision/timestamp, shows STALE failures and last source data. Historical inventory clearly marked.
- Persistence via local atomic state; no private data or credentials committed; OAuth token must be provisioned by executor. Metadata-derived WORK/REPORT lists are not a complete or canonical ledger.
- Automated seven-case unit suite, GitHub Actions run 45645657843 PASS (unit job 139315851876); covers deterministic source revision, no ACK inference, missing OAuth, last-good preservation and pagination failures.

## Peer-review: critical findings
P0-01 LIVE SITE DEPLOY BLOCKED: current tools lack authenticated Sites editor/project deployment capability. This PR does not change nexus-sync-diagnose.julianzotter.chatgpt.site.
P0-02 DRIVE OAUTH BLOCKED: current Google Drive connector permits interactive reads but does not grant a refreshable OAuth credential to the separate local service. Existing GitHub OAuth recovery documented invalid_grant; ID01 or authorized credential owner must reauthorize via tools/windows/repair_drive_oauth.ps1. No credentials in WORK.
P0-03 CANONICAL LEDGER ABSENT: filename classification cannot provide authoritative ACK, 16-WO parity, source files or project-specific P205/Eibengasse statuses; require canonical Registry/API adapters and independent validation before production.
P0-04 SITE OWNER BROWSER E2E NOT_RUN: no verified source delta -> service snapshot -> owner-browser readback; UI unit tests only.
P1-05 SECURITY: loopback-only local service. For public/private cloud deployment use validated identity middleware, TLS, per-user ACL, rate-limit and service credentials; do not simply expose port 8766.

## Required independent reviews
ID02 – Dashboard UI, source schema, KB catalog, accessible interactions.
ID06 – API/security, deterministic snapshot, OAuth renewal/secret handling, CI.
ID05 – compare Perplexity transcript and historical panel/source revision.
ID03 – Governance and artifact registry coordination; do not count self-check as independent review.
ID01 – authorize site owner deploy only after true E2E.

## Gates
GitHub branch + PR: PASS
GitHub dedicated unit CI: PASS
Drive runtime read (via ChatGPT connector): PASS
Drive service OAuth in server: NOT_TESTED
Live source refresh in owner browser: NOT_TESTED
Deploy on existing Sites URL: NOT_DONE
Independent peer review: PENDING
Work order ACK: PENDING
Ledger: PENDING
Production readiness: BLOCKED.

## Decision
Keep existing v4.1 unchanged. No production announcement. Next: provision real authorized source service; run three real Delta / Replay / Fail-closed tests; then deploy to the **existing** Sites project using its authorized editor and verify owner browser.
