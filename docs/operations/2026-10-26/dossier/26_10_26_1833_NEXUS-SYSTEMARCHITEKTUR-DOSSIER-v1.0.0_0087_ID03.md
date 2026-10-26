---
name: NEXUS-SYSTEMARCHITEKTUR-DOSSIER
version: 1.0.0
status: REVIEW
timestamp: 2026-10-26 18:33:51+01:00
agent_id: ID03
executor_instance: /root
gate: PENDING (Human Gate ID01)
source_manual: https://drive.google.com/file/d/1Xo4gL6N_OWcnnde70baStp0ATNVwu5Wo/view
ticket_id: WO-20261026-NEXUS-REPAIR-01
artifact_id: 0087
run_id: DOSSIER-20261026-183351-ID03
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: 733691c80fd10d76b6b6ab00127ab5db0e8401a7aa18c01a4bb36c3e857596b0
content_hash_sha256: 733691c80fd10d76b6b6ab00127ab5db0e8401a7aa18c01a4bb36c3e857596b0
---
# NEXUS AI-OS - Systemarchitektur, Hierarchie und Funktionslogik

PDF-Quelltextbasis: das vollständige aktuelle Handbuch v0.2.0, Architekturtafeln und die im Generator dokumentierten Dossierkapitel. Der Generator ist die vollständige reproduzierbare Layoutquelle.

# NEXUS AI-OS — System- und Betriebshandbuch

## 1. Zweck, Lesart und Geltungsbereich
Dieses Handbuch konsolidiert Architektur, Ablage, Zuständigkeiten, Bedienung, Reporting, Wissenspipeline und Abnahme für den konstruktiven Ingenieurbau. Es ist eine quellengebundene Review-Fassung. Es ersetzt keine freigegebene Governance und bescheinigt keinen autonomen Gesamtbetrieb. Die Dokumentation ist sofort nutzbar; geplante technische Durchsetzung bleibt separat gekennzeichnet.
Leseregel: VERIFIED = direkt beobachteter Teilnachweis; SOURCE_REPORTED = Angabe einer gelesenen Quelle; PROPOSED = Arbeitsvorschlag; UNVERIFIED = fehlender Nachweis. Ein Dokument kann vorhanden sein, während die beschriebene Funktion noch nicht betrieben wird.
Vorgänger: NEXUS_USER_MANUAL_v0.1.md, native Google-Datei. Dessen Inhalt wird als historischer Quelltext erhalten, nicht überschrieben. Ältere KES-Whitepaper und das Repository-Kurzmanual bleiben Quellen für einzelne Bausteine; ihre damaligen Fertigstellungswerte sind keine aktuellen Messwerte.

## 2. Schnellstart für ID01 und beteiligte Instanzen
1. Aktuelle Quellen lesen: Manifest und Baseline sowie spätere datierte ID01-Entscheidungen, insbesondere _AGBS.md v002. Danach WORK/Folder.md, Ticket Registry, relevantes Original-WO und ID-Ledger prüfen.
2. Tatsächliche Instanz, Provider, Rolle, Zugriff und gewünschten Auftrag deklarieren. Nur nachgewiesene Werkzeuge verwenden; Rollenname ist keine Authentifizierung.
3. Bestehendes Ticket übernehmen oder bestehende Idee konkretisieren. Ein AIM-Eintrag ist noch kein ausführbarer Work Order.
4. Bearbeiten, Ergebnis und Prüfungen als Markdown/Artefakte ablegen, Rohbytes zurücklesen, Hash vergleichen und Register/Wegweiser verknüpfen.
5. Im Bericht Fertiges, offene Nachweise und nächste Aktion angeben. Empfänger-ACK und ID01-Freigabe gesondert dokumentieren.

## 3. Governance und bekannte Konflikte
ID01 entscheidet über Adoption und Freigabe. Manifest §4 führt die kanonischen Rollen; §2 berücksichtigt spätere datierte Adoptionen. Baseline MUST-01–06 und MUST-130–134 regeln Vorrang, Nachfolger und Spiegel.
_AGBS.md v002 trägt FREIGEGEBEN_ID01 vom 23.10.2026 und erklärt sich zur führenden Steuerdatei. _FRONTMATTER.md v001 bleibt ENTWURF. Der ältere Manifest-/Baseline-Vorrangtext und neuere AGB-Vorrangtext sind in ihren Metadaten noch nicht konsolidiert. Dieses Handbuch dokumentiert beide und ändert ihre Autorität nicht still.
Benennungskonflikt: AGB v002 nennt YY_MM_DD_HHMM_THEMA_###_ID##.md; AGENTS.md und neuere WORK-Dateien verwenden YY_MM_DD_HH_mm_ID-XX_THEMA_vX.Y.Z.md. Neue Dokumente dieser Lieferung verwenden AGB-HHMM mit Ledger-ID; bestehende Dateinamen bleiben als historische Identitäten erhalten. Ein abschließender gemeinsamer Validator ist noch offen.
MUST-30 verlangt Name/Titel, Datum oder Version, Quelle/kanonischen Ort und Status. MUST-31 empfiehlt zusätzliche Maschinenmetadaten (SHOULD), Hash wenn verfügbar. Diese Lieferung enthält vollständige Hashnachweise für revisionskritische Änderungen; damit wird das Entwurfsschema nicht pauschal zur globalen Pflicht erklärt.

## 4. Systemarchitektur und Verantwortungsgrenzen
| Schicht | Inhalt | Autorität / Nachweis |
|---|---|---|
| Menschliche Steuerung | Ziele, Prioritäten, Adoption, technische Freigabe | ID01; tatsächlicher Entscheidungsnachweis |
| Dokument- und Kontrollschicht | Governance, AIM, Ledger, Tickets, WORK, Quellen | Drive / LLM-LOCAL-SSOT; eindeutige Datei-ID, Version, Hash |
| Ausführung | LLM-Routing, Parser, Python, Scheduler, Transporte | konkrete Runtime und versionierter Code; nicht aus Dokumentenpräsenz ableiten |
| Wissen und Retrieval | Quellenobjekte, Chunks, Kandidaten, Graph-/Vektorprojektionen | Ressourcenidentität und Locator; freigegebene Inhalte getrennt |
| Engineering | deterministische Fachrechnung, Einheiten- und Referenzprüfung | geprüfter Solver und menschliche Freigabe |
| Versionierung und Austausch | Quellcode, Tests, Reviews, Dokumentsnapshots | GitHub-Branch/Commit/PR; Dokumentkopie bleibt Spiegel |
LLM analysiert, strukturiert und orchestriert. Python/Fachsolver führt nachweisbare Rechnungen aus. ID01 gibt haftungssensible Ergebnisse frei. Ein LLM-Konsens oder Temperatur 0 belegt keine mathematische Deterministik oder fachliche Richtigkeit.

## 5. Ablagematrix: WORK, außerhalb WORK, GitHub
| Inhalt | Kanonischer Ort | WORK-Bezug | GitHub |
|---|---|---|---|
| Manifest, Baseline, datierte Architekturentscheidungen, ID-Ledger | LLM-LOCAL-SSOT Root, soweit spezifische Quelle nichts anderes bestimmt | Verweis und betroffener WO | lesbare Review-Snapshots mit Quell-ID/Hash |
| Aktive Work Orders, Rückläufe, Laufberichte, Fehler, Koordination | LLM-LOCAL-SSOT/WORK | Original und Ergebnisverweise | versionierte Austauschkopien dieser Lieferung |
| AIM-Konzeptregister | bestehende eine Datei in WORK, feste Drive-ID | dort fortführen | identifizierter Snapshot, kein zweiter Master |
| Betriebshandbuch | LLM-LOCAL-SSOT Root | Einstieg/Übergabe mit Link | docs/operations und Quellenmanifest |
| Wiederverwendbare Vorlagen und Methodenartefakte | vorhandene _INDEX/00_ARTEFAKTE-BIBLIOTHEK, sofern zugeordnet | Auftrag, Ergebnis und Locator | textuelle Vorlagen/Methodendoku; Binärartefakte separat verlinken |
| Historische Fassungen und Sicherungsarchive | vorhandenes LLM-LOCAL-SSOT/NEXUS.HISTORICAL | Snapshot-/Bundle-Link | kleine Textsnapshots; große Binärdateien über Manifest referenzieren |
| Berichte als dauerhafte Sammlung | vorhandenes NEXUS.REPORTS nach spezifischer Routingregel | operativer Originalnachweis bleibt in WORK referenziert | reports bzw. WORK/REPORTS |
| Rohquellen und lizenzierte Normen | ursprünglicher autorisierter Fachordner, z.B. AI-PYTHON-PARSE | Quell-ID, Rechte und Eingangsauftrag | nur zulässige Metadaten/Links; kein ungeprüfter Volltexttransfer |
| Parsercode, Tests, Konfiguration | jeweiliges GitHub-Repository | Liefer-/Abnahmenachweis | Code-SSOT: AI-ENGINEERING-SYSTEM PR4; Betriebsdoku: nexus-platform |
WORK ist kein automatisch zu leerender Temp-Ordner. MUST-21 weist dort auch Run-Outputs und Koordination zu. Abschluss oder rejected bewirken keinen automatischen Umzug. Eine spezifische Archivierung benötigt nachvollziehbares Ziel und Verweise; keine Idee löschen oder aus AIM herauslösen.
Drive ist Dokument-SSOT; GitHub ist Code-/Versions-/Review-System und Empfängeraustausch. OneDrive/Dropbox sind nur tatsächlich verifizierte Spiegel. Diese Lieferung behauptet keine globale bidirektionale Synchronisierung.

## 6. Verifizierte Ordnerhierarchie nach Datei-ID
| Bereich | Drive-ID | Bemerkung |
|---|---|---|
| LLM-LOCAL-SSOT | 1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV | aktuelle Root-Liste gelesen; lokale Entsprechung G: ist Nutzerkontext, hier kein Mountnachweis |
| WORK | 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP | operativer Originalbereich |
| NEXUS.HISTORICAL | 1Q0CYzEccpL6nfUetHHQjyU4BjAZgmJ7k | erhaltene Sicherungsarchive |
| NEXUS.REPORTS | 1mmLJyc8TpTqxPFhXASb4tmHI7515xpJn | Root-Unterordner; nicht mit WORK/REPORTS verwechseln |
| Capability-Umfrage | 1blG7BkL19NvIcNrB7qwglMCXIHNGlvok | bestehende Kompetenz-/Runtime-Rückläufe |
| _INDEX/00_ARTEFAKTE-BIBLIOTHEK | 1jXreTO8oEDblDcTCXAEHVWvioMFJPMXz | vorhandener Wegweiser und Templates |
| AI-PYTHON-PARSE | 1nbSlOQkCQ7Yhro3RxtIXW3QLP5yj9nBc | Parserquellen, eigene Quellidentitäten |
Weitere vorhandene Root-Bereiche: SCRIPTS, TESTS, NEXUS.INDEX.PARSER, NEXUS.PROMPTS, SKILLS und Rohformatordner. Das ist ein beobachteter Teilausschnitt, keine vollständige rekursive Inventur. Keine neuen parallelen Ordnerbäume für dieselben Inhalte anlegen.

## 7. Identität, Dateiname und Frontmatter
Dateiname dient Auffindbarkeit. Kanonische Identität entsteht aus bestehendem Register und Drive-ID; Hash bindet eine konkrete Repräsentation, nicht eine ganze Idee über alle Versionen. IDs niemals aus dem höchsten Dateinamen ableiten.
Neue Lieferdokumente enthalten: name, version, status, timestamp mit Europe/Vienna-Offset, agent_id, tatsächliche executor_instance, owner_id, ticket_id, run_id, artifact_id, gate, source_refs und expliziten hash_scope. NULL/UNKNOWN für fehlende Werte; keine erfundenen Modelle oder Runtimezuordnungen.
Vier Zustandsachsen getrennt führen: Dokumentstatus; Entwicklung/Adoption nach MUST-55; Aufgabenstatus; Evidenz/Teststatus. Ein Hash oder YAML-PASS ist kein Freigabestatus.
Bodyhash: SHA-256 über UTF-8-Body nach schließendem Frontmatter und LF. Gesamtdateihash: externes Manifest nach Speicherung. Keine vollständige Datei mit ihrem eigenen Vollfilehash zyklisch versehen. Nach jedem Bytewechsel Vollfilehash neu berechnen.

## 8. AIM — Advanced Idea Management
Eine versionierte Markdownliste, neun derzeitige IDs AIM-0001 bis AIM-0009. Originalgedanke erhalten; keine Idee löschen; Erweiterungen datiert markieren. Abgelehnte oder zurückgestellte Ideen bleiben mit Disposition und Wiederaufnahmebedingung sichtbar.
0 neu; 1 konkretisiert; 2 in_Umsetzung; 3 umgesetzt_und_validiert. Diese lokalen Codes sind ein Arbeitsvorschlag und keine globale Statusenum. active/deferred/rejected sind unabhängige Dispositionen. Ein redaktionell korrigiertes Register hebt keinen Ideenstatus an.
Eine Idee kann mehrere Work Orders und Ergebnisse referenzieren. Ein Pilot belegt den abgenommenen Teilumfang. Status 3 setzt alle definierten Abnahmekriterien des Tickets und geeignete Evidenz voraus; technische oder Produktionsfreigaben werden zusätzlich separat dokumentiert.
AIM-0009 beschreibt das allgemeine Markdown-Historiemuster. Das Feldmuster dieser Lieferung ist ein wiederverwendbarer Entwurf, kein global ausgerollter Validator. Pace Layers PL0–PL5 bleiben ausdrücklich NEXUS-Vorschlag, keine still adoptierte Begriffsänderung.

## 9. Auftragsalgorithmus — Sollvertrag und konkrete Stop-Regeln
Der folgende Gesamtalgorithmus ist der Betriebsvertrag zur Abnahme, kein Beweis einer laufenden automatischen Kette.
1. Bootstrap und Scope: Quellen, gültige Regeln, autorisierte Eingänge/Ausgänge, Laufzeit und Kostenrahmen ermitteln. Kritische Evidenz fehlt → BLOCKED.
2. Eingang: Initialbestand und Änderungen erfassen; bekannte ticket_id und Eingangsrepräsentation prüfen. Duplikate erkennen; nicht blind erneut ausführen.
3. Übernahme: tatsächlicher Executor erklärt CLAIM; aktive Zuständigkeit/Lease prüfen. Keine erreichbare Runtime → BLOCKED, kein erfundenes ACK.
4. Verarbeitung: eingefrorene Eingaben mit IDs/Hashes; Parser und Solver trennen; untrusted Kontext nicht als Anweisung ausführen.
5. Prüfung: Schema, Quellenauflösung, Locator, Hash, Einheiten, Referenzfälle und gegebenenfalls unabhängiges Review. Fehler → expliziter Befund, begrenzte Korrektur, gleiche eingefrorene Eingaben erneut prüfen.
6. Ablage: Ergebnis am autorisierten Ziel sichern, Rohbytes zurücklesen, vollständigen Hash vergleichen. Cursor/Ergebnisstatus erst nach gesichertem Nachweis fortschreiben.
7. Registrierung/Austausch: ID-Ledger und Ticket Registry verknüpfen; Versionssnapshots nach GitHub; Übergabereferenz veröffentlichen.
8. Abnahme: tatsächlicher Empfänger-ACK, Review und Human Gate unterscheiden. DONE nur bei erfüllten Kriterien oder explizitem ID01-Waiver.
9. Wiederanlauf: persistente Zustände/Cursors/Claims, begrenzte Retries, Ablaufzeit für Spezialmodus, Fehlerjournal; keine unbegrenzte Selbstrekursion.

## 10. Tatsächlich gelesene Softwarebausteine
| Baustein | Quellcodeverhalten / Grenze |
|---|---|
| orchestrator/nexus_orch/core.py | Aufgabentyp plus Privacy-Marker bestimmen Route; primary/fallback werden der Reihe nach aufgerufen; Modellantwort bleibt probabilistisch |
| council | mehrere Antworten, normalisierter Textvergleich, Quorum ab zwei gültigen Antworten; Synthese ist kein unabhängiger Nachweis |
| lessons | erforderliche Felder, Speicherung als PROPOSED; keine automatische globale Adoption |
| cli.py | status/run/council/lesson/lessons/registry/eval/eval-summary; expliziter Aufgabentyp, kein allwissendes Aufgabenrouting |
| tools/drive_changes_poll.py auf main | Read-only Changefeed; erster Lauf setzt Starttoken ohne Initialinventur; keine Auftragsausführung; fehlende Credentials können Exit 0 liefern; alter Stand ist daher nicht Betriebspass |
| nexus-drive-poll.yml auf main | cron 7,37 pro Stunde, also konfiguriertes 30-Minuten-Polling; tatsächliche Läufe/Credentials hier nicht geprüft |
| deliver_work.py / Übergabevertrag | Digest-/Readback-/Journal-Konzept im Repository dokumentiert; Actions-OAuth ist unabhängig vom Drive-Connector dieser Sitzung |
| Parser PR4 | rc3, Head 336f68e4283ef521cd0508936a27431d6f2d57d0, offen/unmerged bei Abruf; Review/Testzahlen im PR berichtet, in diesem Dokumentationslauf nicht neu ausgeführt |
Vorliegender Code ist kein Nachweis aktiver Accounts, API-Keys, Minutentakt, Geräte-Push oder einer Gemini-Dateibrücke. Geprüfte rc3-Integritätsarbeit ersetzt keine aktuelle CI-/Zielumgebungs- oder Inhaltsabnahme. rc2-Testzahlen nicht auf rc3 übertragen.

## 11. Bedienung vorhandener CLI — nur nach lokaler Einrichtung
Aus dem Repository-Verzeichnis orchestrator sind folgende in cli.py vorhandene Befehle dokumentiert:
```powershell
python -m nexus_orch.cli status
python -m nexus_orch.cli registry
python -m nexus_orch.cli eval --dry-run
python -m nexus_orch.cli lessons kmod
```
status prüft Verfügbarkeit gemäß Provideradapter, keine vollständige Konto-/Betriebsabnahme. eval --dry-run baut ein Kontextpaket, sendet aber keinen Modellaufruf. Reale run/council/eval-Aufrufe können externe Datenübertragung und Kosten auslösen und benötigen passende Freigabe und Credentials. In diesem Lauf wurden sie nicht gestartet.
Keine API-Schlüssel in Markdown/Logs/Git. Sichere Einrichtung über vorgesehene Secret-Verwaltung. Keine automatische Installation, Taskaktivierung oder Policyänderung aus diesem Handbuch ableiten.

## 12. Kommunikation und Intervallprofile
P1 1 Minute: nur expliziter Work Order plus Aufforderung, benannter Scope, Ablaufzeit und Stop-Nachweis. P2 10 Minuten, P3 30 Minuten, P4 60 Minuten: Evaluierungsprofile je Aufgabe/Runtime. P5 00/06/12/18 Europe/Vienna: vier Wandzeitprüfungen; Sommerzeit berücksichtigen. M1 wöchentlich: gesonderte Wartung mit noch festzulegendem Termin.
Die allgemeine 60-Sekunden-Zielanforderung im Technikachsen-Entscheid wird durch die spätere auftragsbezogene Begrenzung konkretisiert. Kein globaler Minuten-Dauerbetrieb wird behauptet. Kalendertermin, erkannte Datei, gestarteter Prozess, ausgeführter Auftrag und abgenommenes Ergebnis sind unterschiedliche Ereignisse.
Capability-Fragebogen WO-REG-CAP-001 zuerst nutzen; keine zweite Kompetenzregistry. Provider/Account/Instanz/Modell/Rechte/Quellenbeleg getrennt. Kommunikationspublikation ist kein Versandbeleg und kein ACK.

## 13. Wissensarchitektur und Fachsprache
Dokumentierte ID01-Entscheidung DEC-KG-TECHNIKACHSE v1.0.0, Ledger 0059: Technik ist Hauptachse, Recht Nebenpfad. Wissenschaft/Technik → Ingenieurwissenschaften → Bauingenieurwesen → konstruktiver Ingenieurbau → Fachanwendung → Werkstoff (initial Beton/Holz) → Eurocode-Teil → NAD → Abschnitt/Tabelle/Gleichung.
Deutsch ist primäre interne Fach- und Kommunikationssprache; englische Mappings referenzieren dieselben Begriffs-IDs. Quelltexte behalten ihre Sprache. Bestehende API-Feldnamen nicht ungeprüft umbenennen. Rechtliche Querverweise benötigen Belege; Tags allein begründen keine Rechtsgeltung.
Frühere Aussagen, die Achsenordnung sei überhaupt noch nicht schriftlich/adoptiert dokumentiert, sind überholt: Entscheidung 0059 liegt vor. Die beiden Whitepaper-Entwürfe und Quellenlisten müssen diese Festlegung noch konsistent übernehmen. Quellen-/Normgeltungsprüfung und Implementierungsabnahme bleiben offen.

## 14. Datenpipeline von Rohquelle zu Wiederverwendung
1 Quelle unverändert sichern; Lizenz/Zugriff, source_id, Darstellung, Version und Bytehash erfassen.
2 Ressourcenregister vor Semantik aktualisieren. Artefakt-Ledger-ID ist keine Chunk-ID.
3 PDF-/native Text-/OCR-Ausgabe in gemeinsames Seiten-/Blockmodell überführen. OCR-Ausgabe darf in Folgestufen nicht verloren gehen.
4 Struktursegmentierung und gegebenenfalls dokumentierte semantische Grenzen; Modell, Parameter und Version festhalten. Formeln, Tabellen, Kurztexte und Lesereihenfolge gesondert prüfen.
5 Kandidatenobjekte mit Quellen-Locator und stabilem Schema; unklare Klassifikation als UNCLASSIFIED/REVIEW_REQUIRED.
6 Labels, KeyValues mit Einheiten und Relationskandidaten anreichern. Ähnlichkeit belegt keine fachliche Beziehung.
7 Validierte Registry als Quelle für Graph-/Vektorprojektionen; identische Quellidentität und Versionsbindung erhalten. Kein zweiter kanonischer Wissensbestand im Index.
8 Register-/Indexsuche vor Vektorfallback; Antwort liefert Quelle und Locator oder enthält sich.
9 Engineering-Wiederverwendung nur mit passenden Normausgaben/nationalen Anhängen, geprüften Eingaben und deterministischem Rechenweg.
Keine allgemeine Behauptung einer bereits produktiven Graph-/Vektor-Integration. IFC und andere externe Schemas sind referenzierende Fachmappings; kein unbelegter Alleinstandard für sämtliche NEXUS-Daten.

## 15. Reporting und History
Jeder wesentliche Lauf erhält ticket_id, run_id, Instanz, Zeitpunkt, Quellen, erzeugte Artefakte, QA, offenen Blocker und next_action. Berichtsschema: STATUS, CHANGED, TESTS, SOURCE_STATUS, RISKS_GAPS, NEXT, QA_STATUS, LOG.
History enthält Version, tatsächlichen Zeitpunkt mit Offset, Autor/Instanz, Änderungsgrund, Quellen und Vorgänger. Unbekannte historische Zeiten bleiben UNKNOWN. Eine Historie allein garantiert keine WORM-Unveränderlichkeit. Snapshots plus Hashes erlauben Vergleich, ersetzen aber keine Zugriffskontrolle oder technische Schreibsperre.
Eine in-place aktualisierte Drive-Datei behält ihre ID. Deshalb immer Version/Hash dazunennen und Vorgängersnapshot verlinken. Alte Ledger-Zeilen bleiben historische Nachweise; neue Version erhält additive Zeile mit SUPERSEDES.

## 16. Backup, Austausch und Wiederherstellung
Diese Lieferung führt einen kontrollierten Einmallauf durch: Drive-Quellen lesen → eingefrorene Bytes → neue Dokumente → Drive-Readback → Ledger/Wegweiser → GitHub-Branch/Commit/PR → transportbezogener Nachweis. Das ist keine aktivierte Dauersynchronisierung.
Alle kommunizierten Dokumente dieser Lieferung sowie relevante bereits gespeicherte MDs werden in nexus-platform als identifizierte Snapshots mit Source-Manifest gesichert. Parsercode bleibt in AI-ENGINEERING-SYSTEM; Verweise verhindern zwei auseinanderlaufende Codemaster.
Archivpaket in NEXUS.HISTORICAL enthält eingefrorene Vorstände und Quellenmanifest. Wiederverwendbares Dokumentmuster in 00_ARTEFAKTE-BIBLIOTHEK. Keine großen Binärpakete, Secrets oder lizenzierten Normvolltexte ungeprüft ins Git. GitHub Actions Artefakt-Aufbewahrung allein ist kein dauerhaftes Backup.
Wiederherstellung: Zielversion aus Ledger/Manifest wählen; Snapshot herunterladen; SHA-256 prüfen; in isoliertem Ziel rekonstruieren; ursprüngliche Version nicht überschreiben; Registerreferenzen und Links prüfen; Wiederanlaufprobe protokollieren; operative Rücksetzung separat autorisieren.

## 17. Abnahme- und Prüfcheckliste
- Identitäten/Quellen auflösbar; Pflichtfelder und YAML konsistent; Hashumfang eindeutig.
- Gefrorene Eingaben und resultierende Artefakte vergleichbar; Replay ohne ungeplante Dubletten.
- Fehlende Credentials, Schreibfehler, doppelte Zustellung, Ausfall und abgelaufener Minutenmodus als Negativfälle.
- Claim/Lease/CAS und Berechtigungstest je Runtime; Frischlesevergleich allein ist kein atomarer CAS.
- Quell-/Seitenbezug, Tabellen/Formeln und fachliche Normausgaben separat geprüft.
- Reviewperspektiven Softwarearchitektur, AI-Governance, Systems/Innovation vor Vertrags-/Produktionsrelease gemäß AGENTS.md; Konsolidierung und Human Gate.
- Datei gespeichert, Register ergänzt, GitHub-Commit, Empfänger-ACK und Produktionsabnahme einzeln nachweisen.

## 18. Aktuelle offene Betriebsnachweise
Unabhängige Handbuch-/Governance-Abnahme; konsolidierter Namens-/Statusvalidator; echte externe Capability-Rückläufe; abgesicherte Writer/Claims; globale Auftragskette; Gemini-Schreibbrücke; PR4-Merge/aktuelle CI/Zielbetrieb; Quellenabnahme für Normdaten; Template-Installation; geprüfter Dauerbetrieb und Wiederherstellungstest.
Älterer WORK-Befund anyone:writer bleibt Warnquelle, bis frisch geprüft; diese Dokumentationslieferung verändert keine Rechte. Fehlende OAuth-Konfiguration in Actions bleibt unabhängig von erfolgreicher Connectorablage.

## 19. Änderungen gegenüber dem bisherigen Handbuchentwurf
GitHub nicht pauschal zur Dokument-SSOT erklärt. Kein automatisches Entfernen erledigter/rejected AIM-Ideen aus WORK. Watcher, rekursive Fehlerkorrektur und Gemini-Zugriffe nicht als laufend behauptet. Vollständige Ablagematrix, Zustandsachsen, Hashumfang, Provenienz, Bedienung und Wiederherstellungsablauf ergänzt.

## 20. Pflege und Historie
Diese Fassung v0.2.0 ist die quellengebundene Fortführung des vorhandenen v0.1.0-Entwurfs; die native Vorgängerdatei bleibt erhalten. Änderungen am Handbuch erfordern Quellen-/Ist-Abgleich und neue Version. Änderungen an CURRENT-Governance verlangen zusätzlich den dafür vorgesehenen ID01-Entscheid. Kein ungeprüftes Fortschreiben von Testzahlen oder Statusschätzungen.


## Dossier-Ergänzungen
Leseführung/Problemstellung/Methode, sechs Vektorarchitekturtafeln, Implementation Guide mit I1-I7, Schnittstellenverträge, Ausblick und Quellenverzeichnis werden vollständig im mitgelieferten Generator geführt.
