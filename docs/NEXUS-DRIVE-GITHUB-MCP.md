# NEXUS: GitHub <-> Drive <-> lokaler Mount <-> MCP-Bridge

State: REVIEW / NOT_MERGED. Transport-Erfolg ist keine Freigabe (human_acceptance=PENDING).

## Kanaele (genau ein Schreibweg je Richtung)

| Richtung | Mechanismus | Takt | Schreibt |
|---|---|---|---|
| GitHub -> Drive WORK | `nexus-monitor.yml` -> `nexus-delivery.yml` (`tools/deliver_work.py`) | push main + stuendlich :17 UTC | neue Datei + Receipt, sha256-Readback |
| Drive WORK/REPORTS -> GitHub | `nexus-drive-poll.yml` (`tools/drive_changes_poll.py`, changes.list + Page-Token) | alle 30 min (:07/:37) + manuell + `repository_dispatch: drive_change` | nur Artifact/Job-Summary, kein Commit |
| GitHub -> lokal G: | `orchestrator/sync_nexus.ps1` via `install_autosync.ps1` (Aufgabenplanung) | taeglich + Anmeldung | robocopy ohne Loeschen, testgated |
| lokal G: <-> drive.google.com | Google Drive for desktop | live | - |
| LLM <-> WORK + Repo | `mcp_bridge/nexus_mcp_server.py` (MCP stdio) | live | nur `submit_result`, nur bei `NEXUS_MCP_WRITE=1`, nur neue Dateien in WORK/REPORTS |

## Aktivierung

1. Drive-OAuth (einmalig, lokal): `pip install -r tools/oauth-setup-requirements.txt`, dann
   `python tools/configure_drive_oauth.py --client-json <Desktop-OAuth-Client.json> --publish`
   -> setzt `NEXUS_GOOGLE_CLIENT_ID/SECRET/REFRESH_TOKEN` als Repo-Secrets (Werte werden nie ausgegeben).
2. Test: `gh workflow run "NEXUS GitHub to WORK" -f source_run_id=<letzter Monitor-Run>` und
   `gh workflow run "NEXUS Drive to GitHub"` (erster Lauf = INITIALIZED, ab dem zweiten werden Aenderungen gemeldet).
3. MCP-Bridge: `cd mcp_bridge; .\install_mcp_bridge.ps1 [-ClaudeDesktop]`. Andere Clients: `mcp.local.example.json`.
4. Lokaler Sync: `orchestrator\install_autosync.ps1`.

## Webhooks (optional, Phase 2)

Drive-Push (`changes.watch`) braucht einen oeffentlichen HTTPS-Empfaenger; GitHub Actions kann keine Webhooks empfangen.
Muster: Drive -> Relay (z. B. Cloud Run/Function, prueft `X-Goog-Channel-Token`) -> `POST /repos/julianzotter/nexus-platform/dispatches`
mit `{"event_type":"drive_change"}` (fein-granulares Token, nur `contents:write` fuer dispatch). Kanal laeuft ab -> Erneuerung per Schedule.
Bis dahin deckt das 30-min-Polling dieselbe Funktion ohne oeffentliche Angriffsflaeche ab.

## Circular Loop: Ledger (Inbox/Outbox mit Empfangsbestaetigung)

`tools/nexus_ledger.py` - eine unveraenderliche JSON-Datei pro Ereignis unter `WORK/LEDGER/<work_order_id>/`
(exklusives Anlegen, keine gemeinsame JSONL-Datei -> keine Drive-Konfliktkopien bei parallelen Agenten).

`REQUESTED -> ACK -> DONE -> VERIFIED` (+ `BLOCKED`, `TIMEOUT`). ACK/DONE/BLOCKED nur durch den Empfaenger,
VERIFIED nur durch `SYS-VERIFY` nach sha256-Readback, Freigabe (ID01) bleibt ausserhalb des Ledgers.
`STATUS.md` und `_FRONT_LOG.md` werden vom Verifier aus den Ereignissen generiert (ein Schreiber).

MCP-Tools (Identitaet fest per `NEXUS_AGENT_ID` im Client-Eintrag): `my_inbox`, `send_order`, `ack_order`,
`complete_order`, `block_order`. Verifier lokal: `.\install_mcp_bridge.ps1 -Verifier` (alle 15 min, 0 Tokens).
