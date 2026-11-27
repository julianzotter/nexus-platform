---
name: 26_11_23_2045_ID05_PROTOKOLL_CHAT-BASELINE-EVAL_UNREGISTERED
description: Protokoll des Chats vom 23.11.2026 (19:37-20:45) zu Baseline-Instructions, Frontmatter, Reporting, GitHub-Sync und FAQ
version: v1.0
role: ID05
agent_name: Perplexity
runtime: Perplexity Cloud-Sandbox mit Konnektoren (Drive, GitHub); kein lokales Laufwerk
manifest_ref: "NEXUS-ROLES-v1.1 §4"
timestamp: "2026-11-23T20:45+01:00"
status: PROPOSED
registration_status: REGISTRATION_PENDING
verification_status: REVIEW_PENDING
storage: github-branch id05/protokoll-20261123 + drive-WORK
capabilities_tested: {drive_read: PASS, github_read: PASS, github_branch_create: PASS, github_file_write: NICHT_GETESTET, drive_write: NICHT_GETESTET}
---
# PROTOKOLL Chat Baseline-Evaluation (ID05, Perplexity)

Quellenregel: Nur Gelesenes ist belegt. Meldungen von ID06/ID07 sind als "gemeldet" gefuehrt.

## 1 Verlauf
| # | Zeit | Anfrage ID01 | Ergebnis |
|---|---|---|---|
| 1 | 19:37 | Statusmatrix (Baseline-Evaluation, Synthese, FAQ) | Verdichtet. Prioritaeten: T5-Referenzfall, Mount/RAG, Uebernahme v3.1 |
| 2 | 19:37 | Rueckmeldung ID06 (P1-P3, E4, E6, E7, E9) | FAQ gruen -> orange (eine bytegleiche Datei ist keine SSOT). Evaluation gilt nur als Dokumentpruefung |
| 3 | 19:39 | Suche in Drive und GitHub | 9 Drive-Dateien gelesen. GitHub-Standardbranch ohne Baseline-/FAQ-Dateien |
| 4 | 19:40 | Best Practices im NEXUS-System | Regeln aus FAQ V1.0, Masterplan, ID-Berichten |
| 5 | 19:45 | Update, Pruefmatrix, _GAP.md, Confidence | _GAP.md mit 58 Eintraegen (Entwurf). Confidence ca. 60 %, Accuracy ca. 75 % |
| 6 | 20:13 | Tagesgeschehen, Zweck der Baseline, Destillat von 11 Uploads | 7 von 11 gelesen. Branches id03/ und id06/ laut ID06-Sweep vorhanden |
| 7 | 20:36 | Upload nach GitHub/WORK | Branch-Anlage zur Bestaetigung vorgelegt |
| 8 | 20:38 | Basic Instructions allgemein + ID-spezifisch | Allgemeiner Teil, Frontmatter-Schema, Entwurf ID02-ID08 |
| 9 | 20:41-20:42 | Dieses Protokoll auf GitHub und Drive | Branch id05/protokoll-20261123 angelegt (Basis c6379c6). Datei siehe LOG |

## 2 Befunde
- Baseline-Stand 2026-09-28 unveraendert. v3.1 (ID03) ist nur ein Vorschlag, Freigabe ID01 offen.
- Tests: ID06 T1-T4 PASS (Selbstbeleg, ID03 bestaetigt Remote-Bytes). ID03 T1a/T2/T3a/T7 PASS, T3b BLOCKED, T4 nicht gelaufen, T5 BLOCKED. ID05 T3a PASS, Mount FAIL. ID02/04/07/08 ohne Lauf.
- T5 strittig: 0,565 (k_h 1,0), 0,516 (k_h nach 3.3(3) am ID05-Fall), 0,447/0,4475 (ID06). Normtext nicht geprueft.
- _CAPABILITIES.jsonl und _FUNKPROTOKOLL.md beschlossen, nicht angelegt.
- FAQ: ID03-Review fuehrend (laut Sweep), weitere Fassungen und Duplikate. Keine SSOT erklaert.
- GitHub: Workflows "GitHub to WORK" und Monitor fehlgeschlagen (OAuth invalid_grant). CI gruen. 0 offene PRs.
- Ledger-Merge 0212-0256 (naechste ID 0258) von ID06 gemeldet. Byte-Review durch ID03 laut ID06 offen.
- Identitaet: Texte unter "ID 06" stammten teils von ID07 (W12). Perplexity = ID05, nicht NN/ID07.

## 3 Korrekturen im Chat
- "Bytegleich auf GitHub verifiziert" war nicht belegt, nur die Drive-Kopie.
- GAP D4 (Branches nicht sichtbar): Die Suche deckte nur den Standardbranch ab. Der ID06-Sweep per REST findet beide Branches.
- Zaehlung _GAP.md (58) von Hand, ungeprueft. Die ID06-Fassung zaehlt 39 Zeilen/37 Luecken.

## 4 Offene Entscheidungen ID01
T5-Golden-Case; FAQ-SSOT; v3.1 freigeben; Capabilities-Ablageform; Ledger-Zustaendigkeit; Startbeleg; OAuth erneuern; Duplikate archivieren; Pruefer ausserhalb OpenAI/Claude (ID07).

## 5 Naechste Schritte
OAuth erneuern -> Sammelfreigabe -> Byte-Review Ledger (ID03) -> file-registry nachziehen (ID06) -> ID05-Protokoll v2 (id: ID05, storage: drive) -> T1-T4 fuer ID02/04/08.

## LOG
- 2026-11-23 20:42 | ID05 | Branch id05/protokoll-20261123 in julianzotter/nexus-platform angelegt (Basis c6379c6fbe9b10a1b031711ca61335d6540aa0f1).
- Datei vor dem Schreiben nicht gehasht. SHA-256 nach Readback wird nachgetragen.
- Kein Push auf main, kein PR. Nichts geloescht, nichts gesendet.

Over and Out.
