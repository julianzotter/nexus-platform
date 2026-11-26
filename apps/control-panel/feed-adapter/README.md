# NEXUS Private Feed authorized sync adapter — DRAFT

**Status:** Importable route module and dependency-mocked tests. NOT DEPLOYED. This must be mounted in the existing private Feed Worker, not as a second scheduler, separate public backend, or browser auth proxy.

Routes: POST /api/v1/sync-runs (nexus:sync, Origin + CSRF, returns 202/runId); GET /api/v1/sync-runs/{runId} (nexus:read, owner-bound run status); GET /api/v1/snapshots/current (nexus:read, immutable verified snapshot, no side effects).

## Integration contract

Mount makeSyncRoutes({authorize,verifyCsrf,runs,runner,snapshots,origin}) before existing Feed router and fall through when null is returned. Existing worker must supply real cryptographically verified login/scope, server-validated CSRF token for cookie sessions, durable/shared run store, a runner used by both existing scheduled sync and manual POST, and immutable snapshot store.

authorize(request,scope) may return {id,allowed:true} only after real authorization; never trust client-provided scope, origin, cookies without session verification or X-User headers.

runner.enqueueCoalesced must atomically prevent duplicate jobs across instances and exclusively read configured Drive WORK folder and GitHub commit pinned at start. Runner owns credentials and must not echo secrets to responses.

snapshots.currentFor(principal) must enforce tenant/owner isolation, immutable byte persistence, hash readback, and a valid revision; it must return verified:true only with trustworthy evidence. Failed sync leaves last verified snapshot unchanged. Local-only inventory remains non-authoritative.

The existing Panel and Feed URLs have different origins. Do not relax CORS to pass Feed cookies. Panel permanent integration requires an authenticated server-side panel-origin proxy. Reuse the existing refresh button: POST -> poll runId -> GET current -> match snapshotRevision. On failures preserve previous data. A successful but unchanged source may keep the same revision.

## QA

node --test apps/control-panel/feed-adapter/sync-routes.test.mjs

Tests cover anonymous denial, Origin + CSRF, unknown routes, owner isolation, invalid payload, and immutable GET. They do NOT validate the production external service identities, shared worker locks, browser deployment, or complete P2 evidence.

Before release: integration test shared coalescing, real Drive OAuth, GitHub App access pinned at commit, source normalization, registry/ledger evidence, owner ACL, CSRF, raw manifest readback, protected snapshots, panel proxy and actual Chrome/Edge E2E. Keep SYNC_VERIFIED=FALSE and #140 draft.

Track dependencies: #73, #141, Draft PR #140.
