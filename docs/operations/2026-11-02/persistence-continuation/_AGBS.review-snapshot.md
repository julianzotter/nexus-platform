---
name: _AGBS
version: v005
status: FREIGEGEBEN_ID01
freigabe_durch: ID01
freigabe_datum: 2026-11-02
vorgaenger: _AGBS_v004.md
previous_snapshot: https://drive.google.com/file/d/1pTkf_MDOeppzP5OQwriBcGXLDvd3eaXw/view
previous_snapshot_status: RAW_BYTE_READBACK_VERIFIED
executor: OpenAI Codex
executor_instance: /root
agent_id: null
artifact_id: gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg
change_authority: direkte ID01-Anweisungen vom 2026-11-02 zu Persistenznachweis und kontinuierlicher sicherer Entwicklung
---
NEXUS-AGBs, 12 Punkte:
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

Dateiregel: YY_MM_DD_HHMM_ID##_THEMA_###.md (HHMM: Wiener Ortszeit; ID unmittelbar danach durch ID01 am 2026-10-27 angeordnet)
Steuerdateien: Underscore-Präfix, kein Timestamp. Historisches: Timestamp-Präfix.
Änderungen: nichts löschen, Snapshot als _AGBS_v###.md

Verbindlichkeit und Vorrang:
- _AGBS.md ist die führende NEXUS-Steuerdatei. Bei Widersprüchen in nachgeordneten NEXUS-Dateien gelten die AGBs; Abweichungen sind im WORK-Ordner zu dokumentieren.
- Die Dateiregel YY_MM_DD_HHMM_ID##_THEMA_###.md ist verbindlich. HHMM bezeichnet die lokale Uhrzeit in Europe/Vienna.
- Freigabegrundlage ID01, Sprachdialog vom 2026-10-23: "die AGBs stehen ganz oben" und "das kann man dann auch so freigeben und in Stein meißeln".
- Änderungen dieser freigegebenen Regeln erfordern eine neue Version und ausdrückliche Freigabe durch ID01. Vor Änderungen ist die vorherige Fassung unverändert als Snapshot zu erhalten.
- _FRONTMATTER.md bleibt eine nachgeordnete Datei im Status ENTWURF. Eine Freigabe ihres gesamten Inhalts wird aus dieser Entscheidung nicht abgeleitet.

Änderung v003 — sofortige ID01-Anweisung:
- ID01-Anweisung vom 2026-10-27: Rollen-ID unmittelbar nach Timestamp. Ab jetzt gilt `YY_MM_DD_HHMM_ID##_THEMA_###.md`; Artefaktnummer am Ende. Steuerdateien behalten ihre Ausnahme. Historische Quelltexte und Logs bewahren ihren damaligen Stand. Freigabe betrifft ausschließlich diese Namensregel; keine technische oder sonstige globale Freigabe.
- Vorherige AGB v002 unverändert als _AGBS_v002.md gesichert. _AGBS.md behält dieselbe Drive-ID.

## Verbindliche Artefaktregistrierung — ID01-Freigabe 2026-11-01
Die direkte ID01-Anweisung im Sprachdialog vom 2026-11-01 autorisiert die sofortige Einführung dieser Regel im Entwicklungsbetrieb.
1. Operative Ergebnisse, Statusberichte, Ergänzungsarchive und Checkpoints werden im autorisierten WORK-Ziel gespeichert. Jeder Auftrag benennt sein Ziel; abweichende Fachablagen sind im Bericht zu verlinken.
2. Jedes neu erzeugte oder geänderte Ergebnis erhält unmittelbar einen Eintrag beziehungsweise eine neue Version im bestehenden file-registry.jsonl: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view . Kein paralleles Register anlegen.
3. Pflichtfelder: artifact_id, provider_file_id, name, canonical_uri, version, provenance, verification_status, registration_status, registered_at, owner, ticket_id. Unbekannte Angaben sind null und als offen zu erläutern.
4. Sofortverfahren: artifact_id = gdrive:<Drive-Datei-ID>. Diese ID identifiziert die Datei, nicht automatisch identische Inhalte in anderen Dateien. Revisionsstand zunächst über provider_modified_at abbilden; vorhandene Ledgernummern separat bewahren. Keine fortlaufende Nummer aus Dateinamen ableiten. Umbenennung ändert die ID nicht.
5. Registrierung erfolgt vor fachlicher Freigabe. Initialer Prüfstatus REVIEW_PENDING beziehungsweise ausdrücklich belegter bestehender Prüfstand. Feedbackquelle und Freigabeentscheidung dokumentieren; Registrierung ist keine technische Freigabe.
6. Der erzeugende Bearbeiter verantwortet Ablage, Registereintrag und Readback; der zuständige Reviewer prüft den Rücklauf. Tatsächliche Rolle dokumentieren, keine Rolle aus einem Modellnamen ableiten.
7. Abschlussbericht verlinkt Ergebnis, Register und Prüfnachweis. Ohne bestätigte Registrierung kein vollständig abgeschlossener Rücklauf: REGISTRATION_PENDING/BLOCKED ausweisen. Unabhängige Entwicklungsarbeit darf weitergehen.
8. Registeränderungen erhalten den bisherigen Stand; neue Versionsereignisse append-only. Bei konkurrierenden Änderungen erneut lesen und abgleichen; diese erste connectorbasierte Lösung bietet keine atomare Mehrschreiber-Sperre. Automatische systemweite Durchsetzung ist noch nicht implementiert.
Diese Freigabe betrifft Registrierung und Ablage. Fachliche Freigaben, Kontoeinstellungen und externe Agentenaktivierung werden daraus nicht abgeleitet.

## Präzisierung v005 — verifizierte Persistenz und kontinuierlicher Entwicklungsbetrieb
ID01-Anweisungen vom 2026-11-02 im aktuellen Arbeits-/Sprachdialog autorisieren diese Ergänzung. Geltung: NEXUS-Entwicklung, Reporting und Nachweisführung; keine technische Produktionsfreigabe.
1. Vor NEXUS-Arbeit aktuelle AGBS und auftragsrelevante Steuerdateien lesen und Quellenstand protokollieren. Bei Kontextverlust erneut bootstrapen; Quellenzugriffslücken ausdrücklich melden. Eine dokumentierte Lücke verhindert keine davon unabhängige sichere Entwicklungsarbeit.
2. Oberste Entwicklungspriorität ist fortlaufende Kommunikation und sichere Fortführung. Gates sperren nur den betroffenen kritischen Schritt oder dessen Erfolgsaussage. Lesen, isolierte Tests, Auswertung, Reviewerkommunikation und von ID01 autorisierte reversible Entwicklungs-/WORK-Schreibvorgänge dürfen weiterlaufen. Abweichungen, Teilstatus, Risiken und nächste Aktion in textbasiertem Markdown im WORK dokumentieren. Timestamp und Rollen-ID gemäß Dateiregel verwenden; fehlende sonstige Metadaten/Registrierung als offen kennzeichnen statt Fehlerkommunikation zu verhindern. Keine Dateien löschen, keine E-Mails versenden. Keine abhängige technische Freigabe oder unbelegte Erfolgsaussage durch den Testmodus.
3. "In Google Drive gespeichert" darf nur den tatsächlich belegten Umfang bezeichnen: ausgeführter Provider-Schreibvorgang, authentisch zurückgegebene Drive-Datei-ID, bestätigter Zielordner, Dateiname, MIME und stabiler Versionsstand. Eine lokale Datei, ein Browserdownload, eine MCP-Aufruf-ID oder Modelltext sind kein Drive-Schreibnachweis.
4. Vollständige verifizierte Persistenz verlangt zusätzlich Rücklesen der unveränderten vollständigen Rohbytes, SHA256-Gleichheit im bezeichneten Hashbereich und bestätigten passenden Eintrag im bestehenden file-registry.jsonl. Upload ohne Byteprüfung: WRITTEN_UNVERIFIED. Erfolgreiche Byteprüfung ohne bestätigte Registrierung: FILE_VERIFIED / REGISTRATION_PENDING. Diese Teilzustände bleiben berichtbar; unabhängige Entwicklung läuft weiter. REVIEW_PENDING und Humanfreigabe sind getrennte Achsen.
5. Ein maschinelles Validierungsgate ist im vertrauenswürdigen Ausführungspfad umzusetzen. Eine Promptergänzung, dieses Regelwerk oder ein selbst formulierter Nachweis garantiert keine technische Durchsetzung. Zeitpunkt und tatsächlichen Integrationsumfang berichten; keine globale Garantie ableiten. Bei Timeout Ergebnis zuerst abgleichen; keine blinde Neuanlage. Registry-Vergleich vor Write und Readback ist kein atomarer Mehrschreiber-Lock.
6. Neue domänenspezifische Begriffe im bestehenden Glossar/Shared Understanding mit Definition, Abgrenzung, Quelle und Status nachführen. Keine parallelen Masterregister anlegen. "API", "MCP-Connector", "Drive-Datei-ID" und "Tool-Aufruf-ID" unterscheiden.
7. Ausführung und unabhängige versionsgebundene Prüfung durch reale getrennte Instanzen dokumentieren. Workorder-Publikation, Zustellung, ACK, Review und Release bleiben getrennt. Persönliche Einstellungen/Memory nur nach tatsächlicher unterstützter Mutation als gespeichert melden. Kein vorliegender Regelnachtrag behauptet eine Kontoeinstellung oder Kenntnisnahme anderer Modelle.
