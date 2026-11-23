---
name: 26_11_23_1908_ID06_WO-BASELINE-EVAL_v3_ENTWURF
description: Workorder-Entwurf v3 Baseline-Selbstaudit aller ID-Rollen (T1-T7), Freigabe durch ID01 offen
version: v3.0-draft
status: FREIGABE_AUSSTEHEND_ID01
timestamp: "2026-11-23T19:08+01:00"
verfasser: ID06 (Claude)
basis: [WO-BASELINE-EVAL v1, v2 (Perplexity-Refine), _AGBS.md v007.1]
---
WORKORDER WO-BASELINE-EVAL v3 | Absender: ID 01 | Empfänger: ID {02|03|04|06|NN}
Sprache: Deutsch. Profil: deterministisch, regelbasiert, quellengebunden; Tragwerksplanung/AEC,
Eurocode, parametrische Modellierung, Python; LLM-Orchestrierung; RAG-Wissen in Google Drive.
Ziel: Selbst-Audit. Nur belegen, nicht behaupten.

START: _AGBS.md (WORK) lesen; Startzeile in LLM-HISTORY-LOG (agent, AGBs-Version, Zeit).
Nicht lesbar -> BOOTSTRAP_BLOCKED melden.

REGELN
R1 Keine E-Mails, nichts löschen/überschreiben. Nur neu anlegen.
R2 Keine Secrets (Keys, Tokens, Webhook-URLs) in Berichten, Frontmatter, Register.
R3 PASS nur bei real ausgeführtem Test.
R4 Eigener Test ≠ Review. Review laut Matrix.
R5 Jede Aussage: Beleg (Hash/Pfad/URL/Datei-ID) oder "NICHT GETESTET".
R6 Fehlt Recht/Pfad/Verbindung -> FAIL + Blocker. Nicht raten.
R7 Sprachmodus: "Hier spricht ID xx" ... "Over and Out". Nicht parallel. Nichts Neues -> schweigen.

ZEIT: Europe/Vienna, ISO 8601. Repo: julianzotter/nexus-platform,
Branch id{NN}/baseline-eval-{YYYYMMDD}. Nie main.

TESTARTEFAKT: TEST_ID{NN}_{YYYYMMDD-HHMM}.md
Frontmatter: name, id, timestamp, sha256, capabilities_used, capabilities_tested

T1 GitHub: Artefakt auf Branch pushen. Beweis: Commit-Hash, URL, SHA-256 Remote = Original.
T2 Status: Bericht in WORK, YY_MM_DD_HHMM_ID{NN}_STATUS_WO-BASELINE-EVAL_UNREGISTERED.md.
   Beweis: Drive-Datei-ID + SHA-256 Readback.
T3 Drive: Artefakt in WORK schreiben, zurücklesen. Beweis: Pfad/Datei-ID, SHA-256 vorher = nachher.
T4 Sandbox: Liste aller Dateien nur in Sandbox. Soll: leer oder kopiert (je Hash).
T5 Rechnen: Python, EC5-1-1 §6.1.6 Biegung, BSH GL24h (f_m,k=24 N/mm², EN 14080).
   b=120 mm, h=360 mm, L=5,00 m Einfeld, q_d=6,0 kN/m, NKL 1, KLED mittel -> k_mod=0,8 (Tab. 3.1),
   γM=1,25 (Tab. 2.3 BSH), k_h=min((600/h)^0,1; 1,1) nach §3.3(3).
   Soll: M_d=18,75 kNm, σ_m,d=7,23 N/mm², k_h=1,052, f_m,d=16,17 N/mm², η=0,447 (±1 %).
   Sollwert durch ID06-Skript bestätigt (SHA-256 79a6a587…3105); unabhängiger Review offen.
   Beweis: Skript-SHA-256 + Ausgabe.
T6 RAG: "Welche Version hat _AGBS.md und welcher Abschnitt regelt den Persistenz-Nachweis?"
   Soll: v007.1, Abschnitt 7. Beweis: Pfad + Zeilennummer.
T7 Konnektoren: je Konnektor EIN lesender Aufruf (kein Schreiben, kein Senden).
   Beweis: Konnektor, Aufruf, Ergebnis kurz, Zeit. Endpunkt ohne Secrets.

REVIEW-MATRIX: ID 02 prüft ID 06 · ID 03 prüft ID 04 · ID 04 prüft ID 03 · ID 06 prüft ID 02
· ID NN (z. B. Perplexity) nach ID-Zuweisung -> ID 01. Prüfen = Belege selbst nachlesen.

OUTPUT (Pflicht)
| Test | PASS / FAIL / NICHT GETESTET | Beweis | Blocker | Workaround |
Capability-Statement: kann / kann nicht / nicht getestet.

ABSCHLUSS
1. Delta: YY_MM_DD_HHMM_ID{NN}_CAPABILITIES-DELTA.jsonl in WORK
   (id, konnektor, typ, endpunkt, ergebnis, beweis, zeitstempel). Merge in _CAPABILITIES.jsonl
   nur durch Ledger-Schreiber (AGBs §6.6).
2. RUNLOG: YY_MM_DD_HHMM_ID{NN}_WO-BASELINE-EVAL_RUNLOG.md (append-only).
3. ACK: YY_MM_DD_HHMM_ID{NN}_ACK_WO-BASELINE-EVAL.md in WORK. Ohne ACK = nicht gestartet.
