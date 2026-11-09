---
name: KONVERSATIONS-ARBEITSPLAN
version: 1.0.0
status: REVIEWED_BOUNDED
timestamp: '2026-11-02T19:31:16.452310+01:00'
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
owner: Julian Zotter
ticket_id: WO-20261102-NEXUS-PERSISTENCE-GATE
artifact_id: null
registration_status: PENDING_ACTUAL_WRITEBACK
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: d8246566bc753fd14dffac3815a9b7a3cc25c498a599ca1ac0a8f0d1dccca423
---
# Konversationsaufnahme und schrittweiser Arbeitsplan
## Umfang und belastbare Ausgangslage
Erfasst sind alle fachlichen Aufgaben, Präzisierungen und Rücknahmen der neun im aktuellen Chat übergebenen externen Nachrichtenblöcke, msg_idx 0–158, sowie die anschließenden direkten ID01-Anweisungen. Dies ist eine strukturierte Aufgabenaufnahme mit Message-Locators; kein behauptetes Wort-/Audiotranskript und kein Export anderer Kontochats. Einzelne Nutzertranskripte enthalten zitierte Gemini-Antworten; diese gelten nicht als nachgewiesene Ausführung.

Hauptauftrag: falsche Persistenzbehauptungen verhindern; tatsächliche Umsetzung mit Fehlerfalltests und getrenntem Review; nachvollziehbarer Writeback/Registrierung, Glossar/UL/SU und sichere kontinuierliche Entwicklung.

## Vollständige fachliche Verlaufserfassung
| Nachrichten | Inhalt/Anweisung | Behandlung |
|---|---|---|
| 0–5 | Roadmap, Dateien, Checksummen, Regeln protokollieren; zunächst nur zuhören | Im aktiven Bearbeitungsauftrag aufgehoben; Nachweise getrennt erfassen |
| 6–18 | Angebliche WORK-Ablage nachprüfen, Entstehung verstehen, dauerhafte Fehlervermeidung/Lessons Learned | Incident und Code-/Quellencheck; keine erfundene Root-Cause-Logdatei |
| 19–32 | ID01-Startpflicht AGB/Frontmeta; dauerhaft in persönlichen Einstellungen speichern; Rollen nennen | Governance gelesen; Rolle/Runtime getrennt; persönliche Speicherung capability-blocked |
| 33–40 | Belastbare Lösung, Peer Review, MVC, Kontextbudget, Bestätigungen nur mit echter Ausführung/ID | Zwei reale getrennte Reviewer; Gate + Negativtests |
| 41–55 | Drive API vs MCP, Datei-ID vs Tool-ID, neue Begriffe in Glossar/UL/SU, AGB aktualisieren | Additive sourcegebundene Definitionen und AGB v005 |
| 56–74 | Responsive TranscriptTimeline.tsx, Markdownexport, Fallback, deutsches Handbuch, Begriffserklärung, Phase4 S2S/ezdxf | Tatsächlichen Quellcode geprüft; bestehender PR1 als primären Studiokandidaten wiederverwenden |
| 75–84 | Gemeinsame Lessons Learned; Reporting-/NEXUS.*-Ordner systematisch erschließen | Vorhandene Lessons gefunden, Lesen 403; additive Fallnotiz; bestehenden rekursiven Wegweiser wiederverwenden |
| 85–89 | Breiter konträrer Systemaudit, anschließend ausdrücklich zurückgenommen/für anderen Kontext | Rücknahme erhalten; Audit ist zusätzlich durch aktuellen direkten WORK-Auftrag separat belegt, nicht aus zurückgenommenem Satz abgeleitet |
| 90–106 | Nebengespräch, Warten und Zuhören | Keine Buchhaltungsaufgabe, keine Kontaktnachricht daraus erzeugt |
| 107–121 | Problem/Lösung zusammenfassen, Ziel/Name/ID/Hash/Register | Nachweiskette im Ausführungspfad |
| 122–141 | UL/SU aktualisieren; Nachfrage zu vorzeitig behaupteten Änderungen | Keine Änderung vor Toolnachweis behaupten; Settings getrennt |
| 142–152 | Wer führt aus, wer kontrolliert; Selbstauskunft reicht nicht; getrennte Rollen/versionsgleiches Review/Writeback | Executor und zwei Reviewerinstanzen dokumentiert |
| 153–158 | Drei Markdown-Dateien, Arbeitsplan, schrittweise Abarbeitung, Long/Procedural Context, progressive Offenlegung, Kontextdestillation | Drei Kernrückläufe + separater sofortiger Safe-Mode-Vermerk; Checkpoint/Quellenanker |
| Direkte Anweisung nach Verlauf | Alle Aufgaben exakt/konsistent umsetzen; Tokenlimit/Reporting beachten | Dieser korrelierte Fortsetzungslauf |
| Neueste ID01-Anweisung | Kommunikation/Entwicklung kontinuierlich; sicherer Testmodus trotz Richtlinienlücke; keine Löschung/E-Mail; Timestamp+ID-MD in WORK; Personal Memory | Sofortiger WORK-Vermerk, AGB-v005-Klarstellung; Memory nicht fingiert |

## Anforderungen / Akzeptanz / Iststand
| ID | Ergebnis | Akzeptanzkriterium | Tatsächlicher Stand dieses Fortsetzungslaufs |
|---|---|---|---|
| R01 | Bootstrap | aktuelle AGB, Front, Manifest, Baseline, WORK/Folder mit ID/Version | gelesen; Front wurde parallel geändert und erneut gelesen |
| R02 | Incident | Claims von Nachweisen trennen | Ausgangs-App main zeigt Blobdownload und fixe Maße; konkrete historischen Providerlogs fehlen |
| R03 | Persistenzgate | echter Write + Ziel/Name/MIME/Version + Rohbytehash + bestehendes Register | Python-Deliverypfad erweitert; 35 Tests und 2 getrennte Reviews PASS im begrenzten Scope |
| R04 | Studiointegration | tatsächliche UI/Express/Python-Verbindung | parallelen bestehenden PR1 mit Python-Schreibdienst übernommen; 13 Python+6 Node erneut PASS; Lint/Build PASS |
| R05 | Sichere Fortführung | keine pauschale Kommunikationssperre | WORK-Vermerk real gespeichert; AGB v005 ergänzt und Rohbytegleichheit bestätigt |
| R06 | Ledger/Registry | keine erfundenen IDs; bestehende Register; Readback | bestehende IDs/Nummernquelle gelesen; laufende Rückläufe werden kontrolliert nachgeführt |
| R07 | Lessons | vorhandene Sammlung suchen, Vorfälle/Prävention/Tests dokumentieren | REPORTS/LESSONS_LEARNED.md und LESSONS.jsonl gefunden; 403 verhindert Inhaltsbehauptung/Änderung; additive Fallnotiz |
| R08 | Glossar/UL/SU | explizite Begriffe/Abgrenzungen und gemeinsame Invarianten | Ergänzung am vorhandenen Glossar, eigener unveränderter Vorgänger bleibt erhalten |
| R09 | Wegweiser | bestehende Quelleninventare nutzen, Frontverlinkung | bestehender rekursiver Wegweiser 14Uy-D07qGSTth8l29vfoba2m-TNzWV-U wiederverwendet; eigener Scan nur Prüf-/Konvergenzevidenz |
| R10 | Namens-/Hashsyntax | Wiener Zeit; Rollen-ID; Nummer aus tatsächlichem Ledger; Bodyhashscope explizit | Nummernquelle Ledgerstand 0148 nennt next free 0149; keine Ableitung aus Dateinamen |
| R11 | Peer Review | reale getrennte Instanzen; dieselben Code-/Testhashes; Kritik/Korrektur/Re-Review | zwei OpenAI-Codex-Instanzen; Wiederholungs-/Timestamp-/Hashfehler gefunden und geschlossen |
| R12 | GitHub | Reviewstand mit Source-/Driveanker | vorhandene PR59 und PR1 fortführen; kein Merge/Deploy |
| R13 | Handbuch | tatsächliche Bedienung/Status/Grenzen deutsch | HANDBUCH_DE.md zum bestehenden PR1-Kandidaten |
| R14 | Personal Settings/Memory | tatsächlicher unterstützter Write + Bestätigung | NOT_EXECUTED_CAPABILITY_MISSING; WORK-Regel ist keine Kontoeinstellung |
| R15 | Externer Modellreview | tatsächliche verfügbare Runtime, kein Namensersatz | OPUS5.5/Claude/DeepSeek hier nicht gestartet; bestehender externer WO bleibt offen |
| R16 | Phase4 S2S/ezdxf | bestätigte Voraussetzungen, eigener kleiner Implementierungsauftrag | nachgelagert; kein Run/Fachsolver/Export behauptet |

## Rollen und Zustände
Koordination NEXUS-ID02, tatsächlicher Executor OpenAI Codex /root. Codex ist weder Claude noch DeepSeek. Codingverantwortung laut Manifest §4 und reale Runtime getrennt dokumentiert. Reviewer: /root/independent_design_review und /root/systems_review, beide tatsächlich separat ausgeführt. Mensch ID01 behält technische Freigabe.

PLANNED ≠ IMPLEMENTED ≠ TESTED ≠ REGISTERED ≠ REVIEWED ≠ RELEASED. Vollständige Persistenz ist nur PERSISTED_VERIFIED nach den benötigten geprüften Nachweisen. Bereits vorhandene Datei mit fehlendem Register bleibt FILE_VERIFIED / REGISTRATION_PENDING; ohne Rohbyteprüfung WRITTEN_UNVERIFIED. Kein Zustand stoppt unabhängige sichere Entwicklung.

## Procedural Context / Progressive Disclosure
1. Immer behalten: Ziel, aktuelle ID01-Priorität, AGB/Manifestanker, Rolle/Runtime, Writeziel, Akzeptanzkriterien, aktueller Codehash, offene P0/P1.
2. Bedarfsgerecht laden: konkrete Codepfade, relevante Norm-/Quellenabschnitte, neue Reviewerfindings, tatsächliche Providerergebnisse. Suchmetadaten nicht als Volltext lesen ausgeben.
3. Checkpoint: Taskmatrix, Quellen IDs+Versionen, letzte getestete Hashes, ausgeführte Toolresultate und offene Übergaben im versionierten WORK-Rücklauf.
4. Kontextverdichtung darf Quellen, Fehler, Freigaben oder Userabsicht nicht verändern. Kein angebliches Löschen des tatsächlichen Kontextfensters durch eine Textanweisung.

## Minimum Viable Prompt für persönliche Anweisungen
> Vor NEXUS-Arbeit aktuelle AGBS und relevante Steuerdateien aus dem autorisierten Drive-WORK lesen, Quellenstand und reale Runtime dokumentieren. Erfolgsaussagen nur mit tatsächlich ausgeführten Werkzeugen und passenden Nachweisen; lokale Dateien/Downloads nie als Drive-Ablage bestätigen. Vollständige Persistenz erfordert Ziel-/Namens-/ID-/Versionsprüfung, identischen Rohbytehash und Readback im bestehenden Register. Fehlt ein Nachweis, betroffenen Teilstatus offen berichten. Sichere unabhängige Entwicklung und Markdown-Kommunikation in WORK kontinuierlich fortsetzen; Abweichungen mit Wiener Timestamp und Rollen-ID dokumentieren. Keine Dateien löschen, keine E-Mails versenden. Neue Begriffe im bestehenden Glossar/UL/SU nachführen. Ausführung, unabhängiges Review und technische ID01-Freigabe trennen. Memory-/Settings-Speicherung nur nach echter unterstützter Mutation bestätigen.
Dieser Prompt ist als kopierbarer Regelkern formuliert, nicht als technisch erzwungener Prozess oder bereits gespeicherte Kontoeinstellung.

## Meilensteine / nächste fachliche Schritte
| Meilenstein | Abschließender Nachweis | Zustand |
|---|---|---|
| M0 Quellen/Anforderungen | diese Aufnahme + aktuelle Quellen | erfolgt im dokumentierten Scope |
| M1 Safe Mode/Kommunikation | echter WORK-Vermerk und AGB v005 | Byte-Readback bestätigt; Registrierung separat |
| M2 Deliverygate | eingefrorener Code, 35 Tests, 2 reale Reviews | TESTED_BOUNDED |
| M3 Studiokandidat konvergieren | bestehender PR1; 13+6 Tests; Lint/Build; deutsches Handbuch | geprüft/ergänzt, Livebetrieb nicht behauptet |
| M4 Governance/Reportingwriteback | Vorgänger, geprüfte Writes, bestehendes Register/Ledger, Frontanker | laufender kontrollierter Writeback |
| M5 Live-Windows-/Drive-E2E | reale Credentials, reservierte IDs, Restart/Denial/Readback/Registry | offene Hostabhängigkeit; kein Entwicklungsstillstand |
| M6 Ein Writer/Exportpfad | vorhandene Exportkandidaten vergleichen; allen Aufrufern gleichen Contract geben | Konvergenz offen; keine konkurrierende Produktivpipeline starten |
| M7 Externes Review/Release | echte Modellruntime, Rücklauf zu finalem Commit, ID01-Entscheidung | extern offen; sichere Entwicklung läuft weiter |
| M8 S2S/ezdxf/Fachworkflows | separater Scope, Inputs, deterministische Tests | nachgelagert, nicht ausgeführt |

## Führende Quellen
- AGB: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- Frontmatter: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view
- Manifest §4/6/10: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- Baseline MUST-22–25/50–54/100–105/150–159: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- WORK/Folder: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
- Bestehendes Register: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
- Bestehendes Ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view
- Rekursiver Wegweiser: https://drive.google.com/file/d/14Uy-D07qGSTth8l29vfoba2m-TNzWV-U/view
- Studio PR1: https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1
- Fortsetzungsreview PR59: https://github.com/julianzotter/nexus-platform/pull/59
