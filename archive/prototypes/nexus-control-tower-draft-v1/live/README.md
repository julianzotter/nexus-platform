# NEXUS Control Panel: read-only live adapter (DRAFT-v1.2.0) · ARCHIVIERT 2026-11-27

> Abgelöst (`registry/ui-surfaces.json` UI-03). Übernommen ins kanonische Panel `apps/control-panel`:
> Aktualitäts-Guard `site/freshness.js` (Beobachtungszeit ≠ Abrufzeit, STALE statt grün).
> Offener Befund: Standardport 8766 kollidiert mit dem Local-Stack-MCP-Gateway (`127.0.0.1:8766/mcp`);
> ein Drive/GitHub-Metadatenabruf gehört in den Local Stack (UI-02), nicht in einen zweiten Server.
> Unit-Tests laufen weiter (`.github/workflows/nexus-control-panel-live-tests.yml`).

This is a deployable **local integration prototype**, not a deployment to the existing `chatgpt.site` project.

## Execution (Windows PowerShell / Python 3.12)
```powershell
$env:GOOGLE_DRIVE_ACCESS_TOKEN = "<short-lived authorized OAuth token>"
$env:GITHUB_TOKEN = "<optional token; public GitHub metadata otherwise>"
$env:NEXUS_STATE_FILE = "$env:LOCALAPPDATA\NEXUS\control-panel-state.json"
py .\archive\prototypes\nexus-control-tower-draft-v1\live\server.py
```
Open `http://127.0.0.1:8766`, click ↻. Do **not** commit credentials or post them in Drive/WORK. Use the existing [NEXUS OAuth recovery runbook](https://github.com/julianzotter/nexus-platform/blob/main/docs/NEXUS-OAUTH-RECOVERY.md) to obtain a valid authorized runtime context. A short-lived token is only a pilot mechanism; a production deployment needs managed OAuth refresh/service identity.

## Source contract
- Google Drive API: list actual children of canonical WORK folder `1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP`; results are metadata only. The endpoint does not read restricted file bodies.
- GitHub API: list open PR metadata for `julianzotter/nexus-platform`.
- `observedAt`: newest available WORK file modification timestamp, **not** browser refresh time.
- `checkedAt`: attempt timestamp. `sourceRevision`: SHA-256 of canonicalized Drive and GitHub metadata.
- `workOrders[]` and `reports[]` are **filename-pattern subsets**, not a complete canonical ledger; all ACK and registration states remain `NOT_OBSERVED` or `UNVERIFIED`.
- Historical inventory `219 / 44 / 1967` is not a live census.
- Upstream permission/error/page overflow: return STALE retaining prior source revision, or HTTP 503 with no prior snapshot. Never show a fresh state on failure.

## Security and operational boundaries
- HTTP server binds loopback only; **never** expose it directly to the internet.
- Any future reverse proxy needs TLS, authenticated identity, tenant ACL, CSRF controls for writes, rate limiting and source identity validation.
- Cache contains WORK metadata and must remain on an access-controlled local disk, not a public repository. Atomic replacement and mode 0600 used where supported.
- Production GitHub/Drive connector credentials must be provisioned out of band.
- Current Sites panel v4.1 is **unchanged**; the actual Sites editor, existing backend and owner-browser acceptance are required for that URL.
- Never represent the current provider API as complete: only folder metadata and GitHub open PRs are in scope.

## Test
```powershell
cd archive\prototypes\nexus-control-tower-draft-v1\live
py -m unittest -v test_server
```

## Gates
1. Validate Google Drive OAuth from the actual running service without leaking token bytes.
2. Confirm the same authorized WORK sample updated between two source revisions, inspect the owner-browser view.
3. Test repeat read, upstream OAuth error, page overflow, stale preservation, and service restart.
4. Independent ID02/ID06 review and ID01 approval. GitHub CI is a test receipt, **not** a production release.
