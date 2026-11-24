---
name: _AGBS
version: v007.2
role_register_version: NEXUS-ROLES-v1.2
amendment_author: ID03
amendment_ticket: WO-20261124-ID03-ROLES12-COPILOT
status: FREIGEGEBEN_ID01
freigabe_durch: "ID01, v007/v007.1 am 17.11.2026, Ausführungsauftrag Rollen-, Start- und Tasknachtrag am 24.11.2026"
beauftragt_durch: ID01
vorgaenger: "https://drive.google.com/file/d/11H_r85rkEsQAMm9brsR2jRqxWmUt1_uv/view (v007.1)"
konsolidiert_aus: [_AGBS v006, _FRONTMATTER v006-ID02-ROLE-ADOPTED]
verfasser: "Claude (Peer-Reviewer, delegiert durch ID01); Rollen-ID ungeklaert, siehe Abschnitt 9"
runtime: "claude.ai Chat + Google-Drive-Connector"
timestamp: "2026-11-24T22:55:22+01:00"
registration_status: REGISTRATION_PENDING
ersetzt_inhaltlich: gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg
drive_id_regel: "_AGBS.md behaelt dieselbe Drive-ID (v003). Inhalt dieser Datei ist per ID06 (Skript auf G:, siehe _TROUBLESHOOTING T01) in _AGBS.md zu uebernehmen, siehe Abschnitt 12."
---
# NEXUS-AGBs v007.2

## 0 Kurzfassung
- Diese Datei ist die EINE Hauptsteuerdatei. Jeder Agent liest sie zuerst, bei jedem Start.
- Offen schreiben, schnell arbeiten. Pruefungen melden, sie blockieren nicht.
- Nichts loeschen, keine E-Mails (R1). Ergebnis archivieren und berichten (R2). Statusbericht pro Themenordner (R3).
- Arbeitsauftraege, ACKs, Statusberichte, Artefakte, Hinweise: WORK. Heartbeats, Waechter- und Wartungslogs: LLM-HISTORY-LOG.
- Bei einem Problem oder Blocker: ZUERST `_TROUBLESHOOTING.md` lesen, bevor jemand gefragt wird (Abschnitt 8a).

## 1 Vorrang
- ID01 entscheidet. Manifest (Rollen, Prinzipien) und Baseline (MUST-Regeln) stehen darueber. Die kanonischen Fassungen sind die MD-Dateien im SSOT-Root (ID01-Entscheid D1, 2026-11-17); die Google Docs sind Archiv.
- Diese Datei ist die fuehrende operative Steuerdatei. Bei Widerspruch in nachgeordneten Dateien gelten die AGBs; Abweichungen in WORK dokumentieren.
- Aenderungen: neue Version, Vorgaenger als Snapshot sichern, ID01-Freigabe (Abschnitt 12).

## 2 Startpflicht
1. Vor jeder NEXUS-Arbeit, bei Session-/Taskstart und nach Kontextverlust: diese Datei lesen. Danach auftragsrelevante Quellen (Manifest-MD, Baseline-MD, Auftrag).
2. Quelle, Version und Abrufzeit protokollieren. Jeder Agent meldet zum Start und nach Kontextverlust im START_ACK die Rollen-ID, die tatsächliche Runtime mit Instanz, die vom Anbieter ausgewiesene Modell-ID und den geprüften Zugriff. Je Ziel und Operation Ergebnis, Prüfzeit und Beleg angeben. Unbekannte Modell-ID als null und ungeprüfte Operationen als NOT_TESTED führen. Lese- und Schreibzugriff getrennt ausweisen. Prüfen im Umfang des Auftrags.
3. Start-Eintrag: eine Zeile im LLM-HISTORY-LOG mit agent, Version der gelesenen AGBs, Zeitstempel.
4. Nicht lesbar: BOOTSTRAP_BLOCKED melden. Keine Rolle oder Toolfaehigkeit unterstellen. Eine dokumentierte Luecke blockiert unabhaengige sichere Arbeit nicht.
5. Diese Anweisung beweist keine automatische Ausfuehrung in beliebigen LLMs. Den Satz "Vor jeder NEXUS-Arbeit zuerst _AGBS.md im WORK-Ordner lesen; Quelle und Version protokollieren; sonst BOOTSTRAP_BLOCKED" tragen die Nutzer in die persoenlichen Einstellungen jedes Agenten ein (nur ID01, ausser bei Claude-Chat).
6. DeepSeek: laut ID01-Festlegung 2026-10-27 nur Chattext oder manuelle Uploads, max. 15 Textdateien, kein Drive/GitHub/Dateisystem. Diese Datei muss mitgegeben werden. Eigene Ausfuehrung NOT_RUN. Uebergabe und Ruecklauf ueber ID01.

## 3 Die 12 Punkte
1. Shared Understanding
2. Ubiquitous Language
3. SSOT
4. Evidence First
5. Deterministic Execution
6. Human Gate
7. Fail Closed
8. Continuous Self-Refinement
9. Auditability
10. Immutable History
11. Communication and Synchronization
12. Mandatory Reporting and Archiving

Auslegung 2026-11-17 (ID01-Strategie): Punkt 6 und 7 sperren nur den betroffenen kritischen Schritt oder dessen Erfolgsaussage (siehe Abschnitt 8), nie die Kommunikation.

## 4 Dateiregel
- Berichte und Auftraege: YY_MM_DD_HHMM_ID##_THEMA_###.md, HHMM Europe/Vienna, Artefaktnummer nur aus dem aktuellen Ledger.
- Steuerdateien: Underscore-Praefix, kein Timestamp (z. B. _AGBS.md, _TROUBLESHOOTING.md).
- Historisches: Timestamp-Praefix. Historische Quelltexte und Logs behalten ihren Stand.
- Timestamp in Dateiname = Zeit der Anlage. Abweichungen zur Provider-Anlagezeit melden (Befund F7).
- Rollen-ID im Namen nur, wenn sie durch das Manifest belegt ist.

## 5 Ablage
| Was | Wohin |
|---|---|
| Auftraege (Workorders), ACK-Dateien, Statusberichte, Artefakte, Hinweisdateien ("registriert", "Artefakt abgelegt" mit Pfad) | WORK (_developement/LLM-LOCAL-SSOT/WORK) |
| Heartbeats, Waechter-Zeitstempel, Wartungs- und Steuerlogs, Watch-Laeufe mit run_id und Berichtslink | LLM-HISTORY-LOG (Drive-ID 1uavEf5g_ZisiEMsksrGi_KYzMsx37DWc) |
| Snapshots und ueberholte Steuerdateien | WORK/_ARCHIVE_STEUERDATEIEN (nur verschieben, nie loeschen) |
| Manifest, Baseline (kanonisch als MD), Register, gemeinsame Steuerdateien | SSOT-Root (_developement/LLM-LOCAL-SSOT) |
| Dashboards und Statusseiten | NEXUS.DASHBOARDS |
Ausnahme Heartbeat: je Agent darf EINE Datei ueberschrieben werden (kein Anhaeufen von Dateien). Das ist die einzige erlaubte Ueberschreibung.
Abweichende Fachablagen im Bericht verlinken. Kein neuer Masterindex: vorhandene Indizes (_INDEX.MASTER) nutzen.

## 6 Registrierung
1. Jedes neue oder geaenderte Ergebnis bekommt einen Eintrag oder eine neue Version im bestehenden file-registry.jsonl (https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view). Kein paralleles Register.
2. Pflichtfelder: artifact_id, provider_file_id, name, canonical_uri, version, provenance, verification_status, registration_status, registered_at, owner, ticket_id. Unbekanntes = null und als offen erlaeutern.
3. artifact_id = gdrive:<Drive-Datei-ID>. Umbenennen aendert die ID nicht. Keine Nummer aus Dateinamen ableiten.
4. Registrierung ist keine fachliche Freigabe. Initial REVIEW_PENDING.
5. Ohne bestaetigte Registrierung: REGISTRATION_PENDING ausweisen. Unabhaengige Entwicklung laeuft weiter.
6. Register append-only. Es gibt keine atomare Mehrschreiber-Sperre; vor Schreiben erneut lesen und abgleichen. Genau EIN Ledger-Schreiber, durch ID01 benannt: Claude (Peer-Reviewer, delegiert durch ID01), Entscheid 2026-11-17.
7. Neue Fachbegriffe im bestehenden Glossar nachfuehren (https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view). "API", "MCP-Connector", "Drive-Datei-ID", "Tool-Aufruf-ID" unterscheiden.

## 7 Persistenz-Nachweis
- "In Google Drive gespeichert" gilt nur mit: ausgefuehrtem Schreibvorgang, echter Drive-Datei-ID, bestaetigtem Zielordner, Name, MIME, stabilem Versionsstand.
- Volle Verifikation zusaetzlich: Rohbyte-Readback, SHA-256-Gleichheit, passender Registereintrag.
- Ohne Bytepruefung: WRITTEN_UNVERIFIED. Mit Bytepruefung, ohne Registrierung: FILE_VERIFIED / REGISTRATION_PENDING.
- Eine Promptregel, diese Datei oder ein selbst formulierter Nachweis ist keine technische Durchsetzung. Ein Validator meldet Verstoesse in eine Statusdatei, er blockiert nicht.
- Geheimnisse (Schluessel, Tokens, Passwoerter) gehoeren nie in WORK, Prompts oder Drive-Dokumente. Klartextschluessel sofort melden und rotieren.

## 8 Offene Entwicklung (ID01-Strategie 2026-11-17)
- Lesen und Schreiben in WORK ist fuer alle Agenten offen. Tempo vor Regeln; Prozesse duerfen nicht stehen bleiben.
- Gates sperren nur den betroffenen kritischen Schritt oder die Erfolgsaussage. Lesen, isolierte Tests, Auswertung, Reviewerkommunikation und reversible WORK-Schreibvorgaenge laufen weiter.
- Regelkonflikt: Workaround im Testmodus, Abweichungsnotiz als Markdown mit Timestamp und Agenten-Kennung in WORK. Keine unbelegte Erfolgsaussage.
- Harte Regeln: R1 nichts loeschen, keine E-Mails. R2 jedes Ergebnis archivieren und berichten. R3 Statusbericht je Themenordner mit Tasks, Probleme, offene Fragen, Pruefstatus.
- Drei Ebenen je Vorgang: Artefakt archivieren, Report-Log fortschreiben, Statusbericht aktualisieren.
- Sicherheit bleibt: Schluesselhygiene und OAuth-Erneuerung durch ID01 sind keine Tempo-Bremse und werden gemeldet.

## 8a Probleme und Blocker: erst Troubleshooting (NEU, ID01-Anweisung 2026-11-17)
1. Bei jedem Problem oder Blocker zuerst `_TROUBLESHOOTING.md` im WORK-Ordner lesen, bevor jemand anderes gefragt wird (Drive-ID 1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR).
2. Steht dort eine Loesung: anwenden, Anwendung in einer Zeile protokollieren.
3. Steht dort keine: ID01 oder ID06 fragen. Danach die Loesung als neue Zeile in `_TROUBLESHOOTING.md` am Ende anhaengen (append-only, Datum, Agent, Beleg).
4. Das Troubleshooting ist eine Steuerdatei (Underscore, kein Timestamp). Es hat keine eigene Freigabepflicht fuer neue Eintraege; die Loesungen sind Hinweise, keine technische Freigabe.

## 9 Rollen und Runtime
- Rollenautorität: [Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view), NEXUS-ROLES-v1.2.
- ID01 (Julian Zotter) entscheidet und gibt frei. ID02 = ChatGPT Business und ID03 = ChatGPT Private. Beide unterstützen ID01 als gleichrangige NEXUS AI Knowledge System Engineers und Administratoren. ID03 führt zusätzlich die Chef-Orchestrierung. ID93 ist ein Tippfehler für ID03 und ungültig.
- Rolle, tatsaechliche Instanz, Provider, Modell, Runtime und Rechte getrennt angeben. Codex ist nicht Claude oder DeepSeek.
- OFFEN (ID01): Manifest nennt ID04 = Gemini. Der Claude-Reviewer arbeitet als "Claude (Peer-Reviewer, delegiert durch ID01)" ohne bestaetigte Kennung. Entscheidung ausstehend.
- Capability-Matrix: nur als historischer Lesesnapshot in _ARCHIVE_STEUERDATEIEN. Rechte nicht aus Produkt- oder Rollenlabels ableiten; pro Lauf belegen.

## 9a GitHub-Copilot-Aufträge
Für jeden NEXUS-GitHub-Copilot-Task die Task-URL, das vollständige Repository (owner/repo), den PR-Link und den vollen Commit-SHA im WORK-Auftrag oder zugehörigen Nachweis erfassen. Den aktuellen PR-Head aus GitHub lesen, mit Abrufzeit festhalten und nach einem Push erneut prüfen. Einen Merge-SHA bei Bedarf separat ausweisen. Task-zu-PR-Zuordnung durch den Task oder einen expliziten Rückverweis belegen. Fehlende Zuordnung als UNRESOLVED und einen laut Task fehlenden PR als NO_PR ausweisen. Fehlende Werte sind null. Auftragsstatus und Vollständigkeit der Verknüpfung getrennt führen.

## 10 Zustellung, ACK, Pruefung
- Publikation, Zustellung, ACK, Review und Release getrennt fuehren. Datei in Drive ist keine Zustellung (Drive weckt keinen Agenten).
- ACK-Datei in WORK: YY_MM_DD_HHMM_ID##_ACK_<auftrag>.md mit Zeit, Runtime, Modell, Scope. Kein ACK ohne echte Antwort.
- Autor ist nie alleiniger Reviewer. Selbsttests ersetzen keinen unabhaengigen Review.
- Aufwecken: lokale Windows-Aufgaben und Waechter-Skript als Hauptweg; GitHub nur optional (Workorder Wake-Watcher).

## 11 Quellen
- Manifest (MD, kanonisch): https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view
- Baseline (MD, kanonisch): https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view
- Register: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
- Glossar: https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view
- LLM-HISTORY-LOG: https://drive.google.com/drive/folders/1uavEf5g_ZisiEMsksrGi_KYzMsx37DWc
- Archiv Steuerdateien: https://drive.google.com/drive/folders/1FaqZ2xH3nzlDI80UDa_wrGmObvT6IB52
- Troubleshooting: https://drive.google.com/file/d/1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR/view
- Entscheidungslog D1-D5: https://drive.google.com/file/d/1M9Q_O8zj-TgtpCvrRjiP5BnRRiuWcBHU/view

## 12 Aenderungsregel
- Vorgaengerfassung unveraendert als Snapshot in _ARCHIVE_STEUERDATEIEN sichern (_AGBS_v###.md). Nichts loeschen.
- Neue Version braucht ID01-Freigabe. v007 ist freigegeben (2026-11-17, muendlich). Die Ergaenzung 8a (v007.1) wurde am 2026-11-17 durch ID01 im Chat ausdruecklich freigegeben.
- _AGBS.md behaelt dieselbe Drive-ID (gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg). Der Claude-Chat-Connector kann Dateiinhalt nicht ersetzen. Uebernahme dieses Inhalts in _AGBS.md durch ID06 per Skript auf G: (Loesung T01 in _TROUBLESHOOTING.md): 1) Kopie der alten _AGBS.md ins Archiv, 2) Inhalt ersetzen, 3) SHA-256 vergleichen. Bis zum verifizierten Provider-Write gilt v006 in _AGBS.md; die Aktivierung wird durch Rohbyte-Readback des kanonischen Ziels nachgewiesen.

## 13 Was v007.1 gegenueber v007 aendert
- NEU: Abschnitt 8a und Verweis in Abschnitt 0, 4 und 11 auf _TROUBLESHOOTING.md.
- Abschnitt 6 Punkt 6: Ledger-Schreiber benannt (Entscheid ID01 2026-11-17).
- Abschnitt 12: Uebernahme in _AGBS.md per Skript, Verweis auf Loesung T01.
- Sonst unveraendert gegenueber v007.

LOG: v007.1 2026-11-17 21:35, aufbauend auf freigegebener v007.

## ID01-Ergänzung 2026-11-23 · Kontrollpanel und Meldepflicht
Bei jedem neuen NEXUS-Chat liest die Rolle diese Steuerdatei und öffnet https://nexus-sync-diagnose.julianzotter.chatgpt.site. Sie meldet im zentralen WORK (Drive-ID 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP) ein START_ACK mit UTC-Zeit, Run-ID, Rolle/Modell, gelesener Regelversion und Work-Order. Fehlt der Zugriff, meldet sie BLOCKED. Zu Annahme, Blocker und Abschluss schreibt sie dort Status, Ordner, Artefakte, Quellen und nächsten Schritt. ID02 sichert jede veröffentlichte Panel-Version als rekonstruierbares Paket in WORK und im privaten GitHub-Repo julianzotter/nexus-platform unter backups/control-panel und dokumentiert Version, Commit und SHA-256 nach Readback. Ein fehlendes ACK gilt als unbestätigter Start.

## Änderungsnachweis vom 24.11.2026
[Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) · [ID01-Entscheidung vom 24.11.2026](https://docs.google.com/document/d/1lLqeLzUrJPnKd027M7q3XFzPZvu-0AXMpAuuAsZvbu0/edit) · [Vorgängersnapshot](https://drive.google.com/file/d/11H_r85rkEsQAMm9brsR2jRqxWmUt1_uv/view)
