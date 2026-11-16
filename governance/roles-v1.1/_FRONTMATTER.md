---
name: _FRONTMATTER
version: v006-ID02-ROLE-ADOPTED
status: ENTWURF
timestamp: "2026-11-11T13:16:00.928632+01:00"
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
artifact_id: gdrive:1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi
gate: PENDING_HUMAN_TECHNICAL_RELEASE
supersedes: v004; additive navigation and AGB-v005 continuity reference; ENTWURF unchanged
role_authority_source: Manifest §4; NEXUS-ROLES-v1.1
capability_snapshot_status: HISTORICAL_WITH_CURRENT_ID01_OVERRIDE
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: 193b31e3ccdf634e2303135a0a51bf2c57a11a94173d0c0ded38523eae4e6e0f
hash: 193b31e3ccdf634e2303135a0a51bf2c57a11a94173d0c0ded38523eae4e6e0f
change_authority: ID01; direkte Anweisung sofort ändern am 2026-10-27
navigation_change_authority: Direct ID01 request in current conversation 2026-11-02
role_name: ChatGPT Private
role_amendment_status: FREIGEGEBEN_ID01
role_amendment_ticket: WO-20261111-ID02-PRIVATE-ROLLOUT
---
## ID01-Festlegung 2026-11-11 — verbindliche Rollenbezeichnung
ChatGPT Private = ID02 — ChatGPT Private / ChatGPT Chief Orchestrator.
Maßgeblich: NEXUS-ROLES-v1.1, Manifest §4: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Historische Zuordnungen „ChatGPT Private = ID03“ und „ChatGPT Business = ID02“ sind für die aktuelle Benennung überholt. ID03 bleibt ChatGPT Assistant / Peer Reviewer; keine automatische Neuzuordnung anderer Instanzen.
Rollen-ID und tatsächliche Runtime getrennt dokumentieren. Für diesen autorisierten Lauf: agent_id/role_id ID02; agent_name ChatGPT Private; executor OpenAI Codex; executor_instance /root; provider OpenAI; model_id null (nicht verifiziert).
Vor neuer Rollenentscheidung aktuellen Manifeststand lesen. Kennung ID02 in neuen Berichten dieser Instanz verwenden; historische Dateien unverändert erhalten.
Publikation, Zustellung, ACK und unabhängige Prüfung getrennt erfassen. Die Bereitstellung allein belegt keine Kenntnisnahme anderer LLMs.
Änderungsautorität: ausdrückliche ID01-Anweisung im Sprachdialog 2026-11-11 zur Ergänzung, Bekanntgabe, WORK/Frontmatter/AGB-Aktualisierung, GitHub-Synchronisierung, Sicherung und Ausrollung.
Koordination: WO-20261111-ID02-PRIVATE-ROLLOUT. Geltung ausschließlich Rollenbezeichnung und deren Verteilung; keine technische Produktionsfreigabe.

# Frontmatter-Controlling und NEXUS-Startpflicht — v003 ENTWURF

## Status und Vorrang
Die AGB v003 bleiben führend. ID01 hat am27.10.2026 ausdrücklich die Aufnahme der Rollen-/Capabilitymatrix und der Startpflicht beauftragt. Diese Datei bleibt ENTWURF; keine globale Freigabe sonstiger Entwurfsinhalte und keine technische Produktionsfreigabe. Das Manifest §4 bleibt die einzige maßgebliche Rollenautorität. Die eingebetteten Inhalte sind quellgebundene Lesesnapshots, kein zweites unabhängig gepflegtes Register.

## Startpflicht
Vor jeder neuen NEXUS-Arbeit, bei Session-/Taskstart und nach Kontextverlust vollständig lesen: (1) führende AGB, (2) diese Datei einschließlich beider vollständiger Rollen-/Matrixsnapshots unten, (3) aktuelle verlinkte Manifest-/Baselinequellen und die auftragsrelevanten WORK-Regeln. Quellen-ID, Version, Abrufzeit, tatsächliche Runtime und Rechte protokollieren. Im laufenden Kontext geladene Regeln bis zu Quellenänderung oder Kontextlücke wiederverwenden; keine unnötigen Wiederholungsabfragen. Memory-/History-Snippets ersetzen keinen erfolgreichen Abruf. Fehlt ein benötigter Abruf: BOOTSTRAP_BLOCKED; keine Rollen- oder Toolfähigkeit unterstellen. Die Anweisung ist kein technischer Nachweis ihrer automatischen Ausführung in beliebigen LLMs; Runtime-Durchsetzung braucht eigene Laufbelege.

## Aktuelle ID01-Festlegung27.10.2026 — Vorrang vor historischen Fähigkeitszeilen
- DeepSeek: Chattext oder manuelle Uploads, maximal15 Textdateien; kein ZIP, kein Drive-/GitHub-/Dateisystem-/Runtimezugriff, keine lokale Testausführung. Code und Tests liefern; eigene Ausführung NOT_RUN. Übergabe und Rücklauf über Julian.
- Claude Code: von ID01 benannte Ausführungsruntime. Tatsächlicher Host, Provider/Modell, Tools, Rechte und ausgeführte Tests müssen dennoch pro Lauf belegt sein. Die Benennung ist kein Rechte-/Laufnachweis.
- Aktuelle Codex-Connector-Schreibvorgänge widerlegen die Verwendung alter pauschaler gdoc_only-Zeilen als heutige Runtimegrenze. Rechte nicht aus Produkt-/Rollenlabels ableiten. Historische Matrix unverändert als Quelle erhalten.

## Speichern, Reporting und Aufgabenverteilung
Rolle, tatsächliche Instanz/Provider/Modell und Runtime getrennt angeben; Codex ist nicht Claude oder DeepSeek. Markdownberichte nach `YY_MM_DD_HHMM_ID##_THEMA_###.md`, Europe/Vienna; Artefaktnummer nur aus aktuellem Ledger. Steuerdateien behalten Underscore ohne Dateinamens-Timestamp. Dieses Entwurfsmuster nennt name, version, status, timestamp, agent_id, hash; für maschinelle Aufträge zusätzlich ticket_id/run_id/executor_instance/input_hash/hash_scope/reply_to nach Vertrag. Body-/Vollfilehash unterscheiden.
NEXUS-Artefakte im vereinbarten Drive-WORK sichern; kritische Änderungen mit Vorgängersnapshot, Konfliktprüfung, Rohbyte-/Hashreadback und direktem Link. Baseline MUST-41/45/50–54 beachten. Publikation, Zustellung, ACK, Review und Humanfreigabe getrennt führen. Autor nicht alleiniger Reviewer. Für die beauftragte Pipeline den Plan vor risikorelevanter Implementierung durch zwei getrennte Reviewerinstanzen prüfen lassen.

## HISTORICAL / STALE — Lesesnapshot1, ersetzt durch NEXUS-ROLES-v1.1
Quelle: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Revision NEXUS-CONSOLIDATION-20260928-v1.0; Abrufstand 2026-10-27T09:15:19.081586+01:00. SHA256 `d7da453b5c02390faa31b20152c23b0e86a13a1b4984f454d7634ddb6598da82` über den nachstehenden exakt extrahierten UTF8-Abschnittstext, kein Hash der nativen Google-Doc-Datei. Bei Quellenänderung Snapshot STALE und vor Rollenentscheidung frisch abgleichen.

````text
CANONICAL_ROLE_REGISTER: NEXUS-ROLES-v1.0 | ADOPTED 2026-09-28 by ID01. This section is the sole authoritative role register. Baseline, workorders, notifications and mirrors link here; they do not maintain another role table.
ID01 - Julian Zotter / Human-AI: strategic authority, priorities, final decisions and approvals. Human, not an LLM.
ID02 - ChatGPT Chief Orchestrator: operational coordination, routing, workorders, synthesis, conflict resolution, Manifest and rollout control.
ID03 - ChatGPT Assistant / Peer Reviewer: Golden Slice planning, acceptance tests, QA and peer review. Own designs require a separate reviewer.
ID04 - Gemini: protocol, evidence, source traceability, decision log and status logging. Hash claims require actual byte access.
ID05 - Perplexity: targeted external research, primary-source discovery, cross-check and contradiction search.
ID06 - Claude: responsible coding and implementation role; parser/registry integration, deterministic tools, evaluation, tests and regression loops. A Codex runtime may execute an explicitly assigned coding ticket under this responsibility; record the actual executor/provider/model/runtime. Codex is not Claude and receives no invented actor ID.
ID07 - DeepSeek: independent architecture/engineering auditor, consistency and gap analysis, falsification and code/test review. Never sole author and sole reviewer of the same result.
ID08 - Ollama: delegated local/private model execution; model/version and capabilities must be recorded. Optional for the first pilot.
ID09 - INACTIVE LEGACY ALIAS. Historical DeepSeek references map to current ID07 only when source identity/date establish that meaning. No new assignment to ID09; no global numeric replacement in historical documents.
ID10 - INACTIVE HISTORICAL RECORD (Meta AI). No current execution owner or capability claim. Activation requires a new explicit ID01 decision.
Role, model, runtime and permission are distinct. Before execution record actual executor, provider, model_id/version, runtime_instance, tool/filesystem scope and capability check. Independent review requires a separate reviewing instance; two role labels do not establish independence.
````

## HISTORICAL / STALE — Lesesnapshot2; Private-ID03-Zuordnung überholt
Quelle: https://drive.google.com/file/d/14HOFug29FjkQbjbCN0EucmaZTo1jBs5j/view
Stand v0.1.0 vom14.10.2026, DRAFT-for-ID01-review. SHA256 `0ea1f1efd9680c2079dfe5f950d24d209aa75ae8f014ee4e2739bc837ff266a8` über den vollständigen folgenden UTF8-Export; keine neue Verifikation alter Rechte/ACKs/Footprints. Bestandskopie1Sr_GOuR3oIFmdObFBBTu6t-96vVFWmHJ bleibt Referenz. Alte Vorschlags-IDs11/12 und nächste Ledgernummer0046 werden nicht neu vergeben. Aktuelle ID01-Festlegungen und Laufbelege haben im jeweiligen Scope Vorrang vor veralteten Fähigkeitszeilen.

````markdown
---
name: 26_10_14_LLM-CAPABILITY-MATRIX_v0.1
description: Matrix aller LLM-Rollen/Runtimes, die in _developement und _INDEX_LNK Artefakte hinterlassen haben – Rollen-ID (NEXUS-ROLES-v1.0), Konnektoren, Schreibrechte Drive/GitHub, Grenzen, ACK-Status; Entwicklungsstand im WORK-Ordner, Finalisierung → SSOT-Root + GitHub
version: 0.1.0
status: DRAFT-for-ID01-review
timestamp: 2026-10-14T23:45:00+02:00
author_role: ID06 (Claude Fable 5.1, Claude Code cloud session 01SLraDBKZReYg9UthTLVzXm, Device-Bridge auf Workstation jul)
evidence: TREE_developement.txt (3 375 Zeilen) + 26_09_28_TREELIST_INDEX_LNK.txt (Dateinamen-Footprints); 00_NEXUS_MANIFEST__CURRENT__2026-09-28 §4; NEXUS_CONTROL_PLANE__TICKET_REGISTRY (ACK-Zeilen); 26_09_15_CLA_TOOL-ACCESS-MATRIX_v1.0.md; git log nexus-platform/nexus-skills-factory
canonical_role_register: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit (§4)
next_free_ledger_id: 0046 (siehe 00_ID_LEDGER v0.8)
log: LOG → WORK/26_10_14_LLM-CAPABILITY-MATRIX_v0.1.md; nach ID01-Freigabe → LLM-LOCAL-SSOT/ + nexus-platform/registry/
---

# LLM-CAPABILITY-MATRIX v0.1 (Rollen · Konnektoren · Schreibrechte)

Legende: ✔ belegt · ◐ nur über Umweg (Mensch kopiert / Runtime eines anderen Akteurs) · ✖ nicht möglich/kein Beleg · ? nicht_pruefbar · FP = Dateinamen-Footprint (Treffer in beiden Tree-Listen)

| Rollen-ID (Manifest §4) | Modell / Produkt | Runtime(s) im Bestand | FP | Drive lesen | Drive schreiben | GitHub schreiben | weitere Konnektoren (belegt) | Grenzen / Hinweise | ACK NEXUS-ROLES |
|---|---|---|---|---|---|---|---|---|---|
| **ID01** | Julian (Human) | Workstation jul (G:, Drive for Desktop), GitHub-Account `julianzotter` | – | ✔ | ✔ | ✔ **einziger Commit-Autor** aller Repos (git log) | alle | entscheidet, startet alle LLMs | n/a |
| **ID02** | ChatGPT Business – Chief Orchestrator | chatgpt.com (Business), Drive-Connector (gdoc-Export), Custom-GPTs | 164 (GPT gesamt, inkl. GPT56SOL/ID03) | ✔ (Connector) | ◐ als **.gdoc** (native, kein Raw-MD) · Raw-Dateien nur via Mensch | ✖ kein eigener Account; Codex-Runtime unter ID06-Verantwortung | Perplexity-Projekt-Kontext (README orchestrator) | Sheet-Write für Ticket-Registry belegt (EXT-03 „Sheet-Zeile durch ID02“) | **OPEN** (PENDING_ACTUAL_RESPONSE) |
| **ID03** | ChatGPT Private – Assistant / Peer Reviewer | chatgpt.com (Private), Custom-GPTs (EC2-GPT, Bookkeeper) | (in 164) | ✔ | ◐ .gdoc / Export via Mensch | ✖ | – | eigene Entwürfe brauchen fremden Reviewer (§4) | **OPEN** |
| **ID04** | Gemini (3.8 Flash/Pro) – Protokoll/Evidenz | Google AI Studio (Apps/Build), Colab (`/gdrive/My Drive/…` direkt), NotebookLM, Gemini Desktop-Batch | 22 (+ AI-Studio/Colab-Artefakte ohne Namens-Tag) | ✔ (Colab-Mount) | ✔ **direkt** (Colab-Zelle W-NB-01, NEXUS_PARSE_2026-10-13, nexus_init_log) | ◐ AI-Studio „Export to GitHub“ (Repos GEMINI-LIVE-* 2026-10-13, Autor julianzotter) | Google Workspace, Vision/OCR (routing.json) | Hash-Claims nur mit Byte-Zugriff (§4); WO-EVAL-001 nennt Gemini als „Managing Orchestrator“ → **Konflikt mit §4 (ID02)** | **OPEN** |
| **ID05** | Perplexity (sonar-pro) | perplexity.ai, pplx-cli (Fork) | 10 | ◐ (nur Upload im Chat) | ◐ TXT/MD via Mensch (26_09_28_IMPLEMENTATION-EVALUATION-PERPLEXITY.txt) | ✖ | Web-Research mit Zitaten (orchestrator route `research`) | Primärquellen-Suche; keine Dateisystem-Schreibrechte | **OPEN** |
| **ID06** | Claude (Fable 5.1 / Opus 5.5 / Code) | claude.ai Chat (Drive/Dropbox/M365/Gmail/Notion/Gamma/Canva-Connectoren), Claude Code cloud + Device-Bridge (G:), Claude Code desktop (Workstation) | 17 (+ `CLA_`-Präfix) | ✔ | ✔ Connector (create/update/copy) **und** ✔ direkt auf G: via Bridge (diese Session: IOD.01, WORK, outbox) | ◐ clone/read via add_repo; Push nur mit expliziter `access:push`-Freigabe (nicht genutzt); Commits laufen unter Account julianzotter | 16 Konnektoren lt. TOOL-ACCESS-MATRIX v1.0; Wolfram, alphaXiv, HF | darf nicht Alleinautor + Alleinprüfer sein (§4); Codex-Runtime separat zu deklarieren | **DONE** (2026-09-28, RUNRECORD) |
| **ID07** | DeepSeek (V3/V4.1 Flash) | chat.deepseek.com (Chat-Exporte), DeepSeek_V4_1_Flash.ipynb (Colab) | 81 (26_09_09_DeepSeek-* Exporte, REPORTS/26_10_04_DeepSeek-*) | ◐ Upload | ◐ nur Export via Mensch (MD/TXT) | ✖ | API-Key in LLM_API_KEY.py (Gateway 127.0.0.1:8787) | Auditor-Rolle; nie Alleinautor+Prüfer | **OPEN** |
| **ID08** | Ollama (llama3.2, gemma3, qwen3-vl, nomic-embed) | lokal Workstation (MODEL_REGISTRY.md) | 3 | ✔ lokal | ✔ lokal (bench/out) | ✖ | – | Privacy-Gate-Ziel (`VERTRAULICH` → local) | **OPEN** |
| ID09 | – (Legacy-Alias DeepSeek) | – | – | – | – | – | – | inaktiv (§4) | – |
| ID10 | Meta AI | WhatsApp-Chat-Exporte, REPORTS/NEXUS_AUDIT_Meta AI (zip) | 14 | ✖ | ◐ Export via Mensch | ✖ | – | inaktiv (§4), nur historisch | – |
| **ohne ID** | OpenAI **Codex** (CLI/Cloud) | Codex-Konsolidierung 2026-09-28 (31 Drive-Änderungen, ZIP-Upload abgelehnt), 2026-10-13_Codex_NEXUS-VOICE-SSOT-HBV_RUN001.json, 26_07_04_CODEX_* | 8 | ✔ | ✔ Drive-API (native Docs + Raw) | ◐ lokal unter Account julianzotter | – | Manifest §4: Runtime unter ID06-Verantwortung, **keine eigene ID** → jeder Lauf mit executor/provider/model deklarieren | via ID06 |
| **ohne ID** | Microsoft **Copilot** (M365) | M365 Copilot Basic office@zotterconsult.at, OneDrive „Microsoft Copilot-Chatdateien“ | 6 | ◐ OneDrive/SharePoint | ◐ OneDrive (nicht Drive) | ✖ | M365 (Outlook/Teams/SharePoint) | **nicht im Rollenregister** → ID01-Entscheid (Vorschlag ID11, nur Office-Automation) | – |
| **ohne ID** | **Kimi** (Moonshot) | kimi.com Exporte (07-KIMI-EXPORT, KIMI_SSOT_ROHDATEN_INDEX, „Randomly Themed Kimi Folder“) | 4 | ✖ | ◐ Export via Mensch | ✖ | – | **nicht im Rollenregister** → ID01-Entscheid (Vorschlag ID12, Long-Context-Harvest) | – |
| Runtime | Google **Antigravity** (IDE) | 26_10_03_Exporting to Antigravity, 26_10_04_Debugging-Analyse ANTIGRAVITY | 2 (ohne Namens-Tag) | ✔ lokal | ✔ lokal | ◐ IDE-Git | – | Runtime für ID04/ID06-Code, keine Rolle | – |
| Runtime | Google **AI Studio / Colab / NotebookLM** | Voice Studio App d610e35d…, bootstrap_colab_workbench.ipynb | – | ✔ | ✔ | ◐ (AI Studio Export) | – | Runtimes von ID04 | – |

## Befunde
- B1 **GitHub = Single-Writer**: alle Commits in `nexus-platform`, `nexus-skills-factory`, `GEMINI-LIVE-*` tragen Autor `julianzotter` → kein LLM hat eigene Schreibidentität; Schreibpfad ist immer Mensch-Workstation oder vom Menschen gestartete Runtime (AI Studio Export, Codex, Claude Code mit Freigabe).
- B2 **Drive-Direktschreiber** (ohne Mensch im Loop): ID04 Gemini (Colab-Mount), ID06 Claude (Connector + Bridge), Codex (Drive-API). ID02/ID03 nur als `.gdoc` (nicht ML-readable → IOD.01-Verstoß, Beleg: 30+ `.md.gdoc`-Dubletten in SSOT-Root).
- B3 **Nur-Export-Akteure**: ID05, ID07, ID10, Kimi → jede Ablage ist ein manueller Kopiervorgang; für WorkOrders mit Reporting-Pflicht nur über Mensch (ID01) möglich.
- B4 **Registerlücke**: Copilot, Kimi, Antigravity schreiben Artefakte, haben aber keine Rollen-ID; Codex läuft korrekt unter ID06 (§4), muss aber je Lauf deklariert werden.
- B5 **ACK-Stand**: nur ID06 DONE; ID02/03/04/05/07/08 OPEN seit 2026-09-28 → Voraussetzung „Agenten-Registry sauber“ (Übergabebedingung) ist **nicht erfüllt**.

## Zuweisungsregel (Vorschlag für WorkOrder-Verteilung)
| Aufgabe braucht … | geeignete IDs |
|---|---|
| Raw-Datei in WORK schreiben (MD/JSON/YAML) | ID06, ID04 (Colab), Codex@ID06 |
| GitHub-Commit | ID01 (oder ID06/Codex mit expliziter Push-Freigabe durch ID01) |
| Web-Primärquellen | ID05, ID04 |
| Unabhängiger Audit | ID07 (Export) oder ID03 |
| Lokale/vertrauliche Verarbeitung | ID08 |
| Orchestrierung / WO-Formulierung | ID02 – **erst nach ACK** |

```json
{"version":"0.1.0","date":"2026-10-14","roles":[
 {"id":"ID01","actor":"Human","drive_write":"direct","github_write":"direct","ack":"n/a"},
 {"id":"ID02","actor":"ChatGPT Business","drive_write":"gdoc_only","github_write":"none","ack":"OPEN","footprint":164},
 {"id":"ID03","actor":"ChatGPT Private","drive_write":"gdoc_only","github_write":"none","ack":"OPEN"},
 {"id":"ID04","actor":"Gemini","drive_write":"direct_colab","github_write":"via_aistudio_export","ack":"OPEN","footprint":22},
 {"id":"ID05","actor":"Perplexity","drive_write":"human_copy","github_write":"none","ack":"OPEN","footprint":10},
 {"id":"ID06","actor":"Claude","drive_write":"direct_connector_and_bridge","github_write":"clone_read;push_only_with_explicit_grant","ack":"DONE","footprint":17},
 {"id":"ID07","actor":"DeepSeek","drive_write":"human_copy","github_write":"none","ack":"OPEN","footprint":81},
 {"id":"ID08","actor":"Ollama","drive_write":"local","github_write":"none","ack":"OPEN","footprint":3},
 {"id":"ID10","actor":"Meta AI","status":"inactive","footprint":14},
 {"id":null,"actor":"Codex","runs_under":"ID06","drive_write":"drive_api","footprint":8},
 {"id":null,"actor":"Copilot M365","drive_write":"onedrive_only","needs_decision":"ID01","footprint":6},
 {"id":null,"actor":"Kimi","drive_write":"human_copy","needs_decision":"ID01","footprint":4}],
 "findings":["B1 GitHub single-writer julianzotter","B2 gdoc-only writers violate IOD.01","B3 export-only actors need human relay","B4 Copilot/Kimi/Antigravity without role id","B5 ACK only ID06 DONE"]}
```
````

## Originalinhalt v001
````text
---
name: _FRONTMATTER
version: v001
status: ENTWURF
gate: PENDING (Human Gate ID01)
---
Pflichtfelder (Entwurf):
  name, version, status, timestamp, agent_id, hash

Status-Werte: ENTWURF | REVIEW | VERIFIED | APPROVED
Regel: REVIEWED != APPROVED
Freigabe nur durch ID01 (Human Gate)
````

## Quellen und Historie
- AGB: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- WORK: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
- Ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view
- Vollständiger Rohbyte-Vorgängersnapshot: https://drive.google.com/file/d/1B9xYQaQsqDuDcD9DK_s6z8Mg2bQCO9hw/view (284B, SHA256 b939f3cb1119ec67d0c29977d05092ed23cc10d816d72cc39a0542e8e5fcc1ff).
2026-10-27T09:15:19.081586+01:00: OpenAI Codex /root/finish_nexus_work_orders ergänzt auf direkte ID01-Anweisung Startpflicht, vollständige Matrix, Rollenlesesnapshot und aktuelle Zugriffsgrenzen. Gleiche Drive-ID; keine Rollen-Umnummerierung, eigenständige Rollenautorität oder Produktionsfreigabe.

## Namensregel — aktueller verbindlicher Stand
ID01-Anweisung vom 2026-10-27: Rollen-ID unmittelbar nach Timestamp. Ab jetzt gilt `YY_MM_DD_HHMM_ID##_THEMA_###.md`; Artefaktnummer am Ende. Steuerdateien behalten ihre Ausnahme. Historische Quelltexte und Logs bewahren ihren damaligen Stand. Freigabe betrifft ausschließlich diese Namensregel; keine technische oder sonstige globale Freigabe.

## Navigationsnachtrag — Run 1, 2026-11-02

- Rekursive generierte Navigationssicht (REVIEW_PENDING; kein neuer Master): https://drive.google.com/file/d/14Uy-D07qGSTth8l29vfoba2m-TNzWV-U/view
- Bereits parallel publizierter Depth-1-Wegweiser: https://drive.google.com/file/d/1e8LetZRMUC_bxkbDAwfjmRcxBTEvoTia/view
- Run-1-Implementierungsguide: https://drive.google.com/file/d/1sP0bh854_Llhk4oskCyRFMZohgG-yKt3/view
- Korrelierter Peerreviewauftrag: https://drive.google.com/file/d/1rGV_OdgRk4VpXsZKcQw77Ys2OqIp5WCa/view
- Studio-Codekandidat: https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1
- Vorherige Frontmatter-Rohfassung unverändert gesichert: https://drive.google.com/file/d/1T5Slj3_-E2aSdQ7WxRhssA7KSfUaK4hK/view

Diese Ergänzung ist ausschließlich Navigation auf direkte ID01-Anweisung dieses Runs.
AGB v004 bleiben führend; Entwurfsstatus, bestehende Register und Human Gate bleiben
maßgeblich. Metadaten-Discovery ist keine bestätigte Parser-/Ingestionabdeckung.
Die zwei Export-Lock-Kandidaten müssen vor produktiver Integration konvergiert werden.


## Fortsetzungsnachtrag — Persistenznachweise und kontinuierlicher Testbetrieb, 2026-11-02
Führend ist jetzt AGB v005: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view . Historische v004-Verweise oben behalten ihren damaligen Kontext. Frontmatter bleibt ENTWURF; kein gesamter Governance-/Produktionsrelease.
- Sofortiger ID01-Vermerk zum sicheren Weiterarbeiten: https://drive.google.com/file/d/19y0fc4s3-bVSGJKTsa8dbXWBhTEC-vyj/view
- Konversationsaufnahme, vollständige Aufgabenmatrix, Minimum Viable Prompt und Roadmap: https://drive.google.com/file/d/1u_4uRHrpQRSPLOueqd7UpXZAYeV0tW2V/view
- Korrelierter Auftrag mit tatsächlich abgeschlossenem zweifachem Codex-Code-Re-Review: https://drive.google.com/file/d/1c_8mdTSJLT5hlajgnwxNfPr9uMmqJXeJ/view
- Bestehendes Glossar mit UL/SU-Persistenz-/Safe-Mode-Ergänzung: https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view
- Bestehende GitHub-Reviewstände: https://github.com/julianzotter/nexus-platform/pull/59 ; https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1
Die bereits verlinkten rekursiven Wegweiser bleiben die Navigationssicht; kein weiterer Masterindex wird angelegt. REPORTS und NEXUS.REPORTS sind verschiedene tatsächlich vorhandene Ordner. Metadatenauffindbarkeit ist kein Nachweis der Volltext-/Ingestionabdeckung.
Keine pauschale Kommunikationssperre: sichere unabhängige Entwicklung/Tests und autorisierte additive Markdown-Berichte fortsetzen, Abweichungen dokumentieren. Keine Löschungen/E-Mails; keine ungeprüften Persistenz-/Memory-/Freigabeclaims. Vollständige Registrierung und technische Freigabe bleiben separate Abschlussbedingungen.
