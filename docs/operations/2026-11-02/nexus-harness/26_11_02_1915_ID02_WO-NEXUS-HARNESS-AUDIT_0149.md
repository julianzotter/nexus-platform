---
version: "0.1.0"
timestamp: "2026-11-02T19:15:53.649170+01:00"
agent_id: "ID02"
executor: "OpenAI Codex"
executor_instance: "/root"
model_id: null
ticket_id: "WO-20261102-NEXUS-HARNESS"
run_id: "NEXUS-HARNESS-20261102T191553+0100"
development_status: "PROPOSED"
technical_release: "NOT_GRANTED"
role_authority: "Manifest NEXUS-ROLES-v1.0 section 4"
hash_scope: "body_utf8_after_closing_frontmatter_lf"
name: "26_11_02_1915_ID02_WO-NEXUS-HARNESS-AUDIT_0149.md"
status: "BLOCKED"
content_hash_sha256: "49a7d49e8ffba97640e1a50afbc436a6119d0305ab631efb6882e96fea58e4dd"
---
# Audit- und Implementierungsauftrag
## Verdichteter Auftrag / Shared Understanding
NEXUS soll quellengebunden und auditfähig arbeiten. Ein LLM analysiert und orchestriert; deterministischer Code entscheidet Status und I/O-Erfolg; getrennte Instanzen prüfen; ID01 gibt technisch frei. Modellselbstauskunft gilt nicht als Ausführungsnachweis.
Erfasst ist die gesamte in diesem Thread bereitgestellte Konversation einschließlich Voice-Nachtrag und verlinktem Originalauftrag S6. Ein vollständiger Export sämtlicher Kontochats ist hier nicht vorhanden. Wiederholungen wurden zusammengeführt, zusätzliche Projektarbeiten aus Memory nicht als neue Aufträge übernommen.
## Kanonische Auftragsfelder
- TICKET_ID: WO-20261102-NEXUS-HARNESS
- CREATED_AT: siehe Frontmatter; OWNER_ID: ID02; PRIORITY: P0; STATUS: BLOCKED für Live-Implementierung.
- SOURCE/SSOT_ANCHOR: S1–S6; INPUTS: Originalauftrag, Voice-Verlauf, Governance, Backend-Entwurf, vorhandener Repositorypfad S8.
- OBJECTIVE: Ist-Audit, bestehendes serverseitiges Validierungsgate, getrenntes Review, überprüfter Writeback und Roadmap.
- CONSTRAINTS: keine Ersatzarchitektur, keine erfundenen Rollen/ACKs/Ergebnisse, kein Produktivdeploy; unveränderte Historie; keine Secrets; Drive bleibt Dokument-SSOT.
- TASK/EXPECTED_OUTPUT: Arbeitspakete unten; drei MD-Dateien plus Prüfarchiv und privater GitHub-Review-Snapshot.
- DEPENDENCIES: kanonische nexus_server.py und Frontend-Exportstelle mit Commit/Host/Schnittstelle; autorisierte Testumgebung; authentifizierter exklusiver Writer.
- RISKS: ungeprüfte Erfolgsbehauptungen, Mehrschreiberkonflikt, Tokenverlust, Quellenverwechslung, Verbindungsabbruch.
- NEXT_ACTION: vorhandene Mechanismen wiederverwenden; Zielcode und Laufzeit binden; erst danach Integration.
## Vollständige Aufgabenzerlegung
| Paket | Aufgabe / Entscheidung | Abnahme / Nachweis | Zuständigkeit / Zustand |
|---|---|---|---|
| P0 | Quellenstand und Regeln einfrieren | S1–S5 mit Version, Fundstelle und Hashrepräsentation | ID02 / gelesen |
| P1 | Lateral-Audit: Algorithmen, Steuerdateien, Hierarchie, Links, SSOT | jeder Befund belegt oder UNVERIFIED; keine globale Ist-Behauptung aus Promptmatrix | ID02 / im Bericht |
| P2 | REPORTS und nexus.* unter LLM-LOCAL-SSOT systematisch inventarisieren | vollständige paginierte Traversierung; Coverage und unzugängliche Pfade; bestehende Index-/Registryreferenzen wiederverwenden | Discovery begonnen; Vollscan BLOCKED/ausstehend |
| P3 | Wegweiser für bestehende Frontmatter entwerfen | stabile IDs, Quelle/Version/Hash/Status; nur Referenzen; Governanceänderung separat prüfen | PROPOSED; _FRONTMATTER unverändert |
| P4 | Hard-Lock im bestehenden nexus_server.py-Pfad und Client anbinden | nachstehender Testvertrag; keine lokale Blob-Erfolgssimulation | ID06 verantwortlich; tatsächlicher Zielcode/Host BLOCKED |
| P5 | Zwei getrennte Planreviews und Review derselben Endfassung | Instanz-ID, Befunde, Hashbindung, Korrekturen, Rückprüfung | zwei separate Codex-Instanzen; keine externen Modelle behauptet |
| P6 | WORK-Writeback und bestehende Register ergänzen | Rawbyte-Readback, SHA256, Drive-ID, unveränderte Registerhistorie | ID02; Ergebnis separat nachweisen |
| P7 | GitHub-Synchronisierung | privater Reviewbranch + Commit; kein Merge/Deploy; kanonische Drivequellen verlinkt | ID02; Transportnachweis separat |
| P8 | Bericht, Roadmap, offene Rückläufe | FINDINGS/EVIDENCE/ARTIFACTS/RISKS/NEXT_ACTION/QA_STATUS | hier und Statusbericht |
## Algorithmen / Implementierungsvertrag (PROPOSED)
1. Quellidentität: Drive-Datei-ID beziehungsweise Repository+Commit+Pfad vor Parsing und Semantik. AnythingSearch.db als Discoveryindex behandeln, bis kanonische Autorität belegt ist; kein pauschaler SSOT-Wechsel.
2. Schema-first: UTF-8, vollständiges Frontmatter, erlaubte Typen/Statuswerte, Quellen- und Namensprüfung vor Write. Unbekannte oder ungültige Werte blockieren; keine Reparatur durch freies Modellurteil.
3. Serverpfad: vorhandenes deliver_work.deliver mit authentifiziertem Adapter wiederverwenden, nicht als fertige API-Integration ausgeben. Zielordner aus serverseitiger Allowlist, idempotenter Schlüssel aus Ticket+Eingabehash+Ziel, dauerhafter Journalzustand vor Netzschreiben.
4. Registry: identische Dateiversion/Bytes an Registryereignis binden. Bestehendes file-registry.jsonl append-only; unter exklusivem Writer oder CAS/Lease. Bloßes Lesen vor Update ist kein atomarer CAS. Diese Connectorrunde beweist keine systemweite Sperre.
5. Zustandsautomat: VALIDATED -> WRITE_PENDING -> BYTES_VERIFIED -> REGISTRY_VERIFIED. Erst dann technischer Persistenzerfolg. REVIEW_PENDING -> REVIEWED -> HUMAN_ACCEPTED getrennt. Fehler und Timeout bleiben BLOCKED/INCONCLUSIVE; kein DONE oder erfundener ACK.
6. Restart: Timeout nach erfolgreichem Create durch gespeicherte Datei-ID und Readback auflösen; keine blinde zweite Create-Anfrage. Ein Journal muss Prozess-/Runnerverlust überstehen, ein RAM-Lock reicht nicht.
7. Client: Serverantwort/Receipt exakt prüfen; Blob-Download aus dem autorisierten Persistenzpfad entfernen, sobald Serverintegration real geprüft ist; bei Fehler sichtbarer Fehlerstatus, kein Erfolg nur wegen Download.
8. Kontext: Seed mit Ziel, Quellen-IDs, Constraints und offenen Gates; pro Paket nur benötigte Quellen; Fortschritt in WORK checkpointen. Kein unbeschränktes Mergen aller Steuerdateien. Tokenbudget mit Reserve vor Aufruf prüfen; Langtext in nummerierte Pakete splitten, keine stillen Kürzungen.
## Akzeptanztests für P4
| ID | Fall | Erwartung |
|---|---|---|
| A01 | gültige Bytes, Ziel und Registry | genau eine Datei; Rawbytes gleich; Registry gleiche Version/Hash; Persistenzstatus erst danach |
| A02 | fehlende/abgelaufene Berechtigung, 401/403 | kein Erfolg, Fehler protokolliert, keine unzulässigen Retries |
| A03 | Timeout nach Create, erneuter Aufruf, Neustart | bestehende ID wiederverwenden; keine Dublette |
| A04 | veränderte Readbackbytes oder falscher Zielordner | INTEGRITY_FAILED/BLOCKED; kein Persistenzerfolg |
| A05 | fehlender/fehlerhafter Registereintrag | REGISTRATION_PENDING/BLOCKED trotz erfolgreichem Upload |
| A06 | alte Reviewversion bei neuen Bytes | Review ungültig; erneute Prüfung erforderlich |
| A07 | zwei Prozesse/Writer und verlorene Lease | höchstens ein autorisierter Commit; keine verlorenen Altzeilen |
| A08 | kaputtes YAML/JSON, falscher Feldtyp, falsche Provider-ID | kontrollierte Ablehnung; kein ungefangener Fehler/Write |
| A09 | Kontextbudget überschritten | bedarfsgerechter Split oder STOP; keine Kernregel abgeschnitten |
| A10 | Verbindungsabbruch im Graph/API-Lauf | persistierter Zustand rekonstruierbar, keine vorzeitige Fertigmeldung |
| A11 | Frontend Serverfehler | kein Blob-Erfolgsfallback; reproduzierbarer UI-Fehler |
| A12 | externer Änderungsversuch/ungeprüfte Quellen | keine unautorisierte Statuspromotion; Auditspur |
## Zuständigkeiten und Zeit
ID02 orchestriert; ID06 verantwortet Implementierung; ID03 QA; ID07 unabhängiger externer Audit. Tatsächliche Ausführung hier: OpenAI Codex /root plus zwei getrennte Codex-Reviewinstanzen. Diese Instanzen sind weder Claude noch DeepSeek. OPUS 5.5 nicht verfügbar/verifiziert und NOT_RUN.
10–15 Minuten aus dem Voice-Verlauf waren nur eine damalige Dokumentationsschätzung. Keine belastbare Implementierungsdauer ohne gebundenen Zielcode/Host. Externe Rückläufe brauchen erreichbare Ausführungsinstanz; Veröffentlichung einer WO startet kein Modell.

## Quellen und Geltungsbereich
[S1] _AGBS.md v004, FREIGEGEBEN_ID01, geändert 2026-11-01T07:53:04.390Z: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view ; Dateiregel und Abschnitt Verbindliche Artefaktregistrierung, Punkte 1–8.
[S2] CURRENT Manifest, NEXUS-CONSOLIDATION-20260928-v1.0, §§4,6,7,10: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
[S3] CURRENT Baseline, Revision 2026-09-28, MUST-41/45/50–54/92–96/150–159: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
[S4] _FRONTMATTER.md v003 ENTWURF; Startpflicht und Rollenlesesnapshot: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view
[S5] WORK Folder.md 0.4.0-pilot, historischer Lauf 2026-10-18: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
[S6] ID01-Originalauftrag, geändert 2026-11-02T18:08:54.900Z: https://drive.google.com/file/d/1CQFX1ryfAEkwop8--DXpJ9DZtvDRJbGg/view
[S7] Historischer Backend-Entwurf nexus_backend_server_5.0.txt, geändert 2026-10-19T02:15:19.604Z: https://drive.google.com/file/d/1-UVQl-jzgRzOsrV7DT22dX1AYRnivK-7/view
[S8] Geprüfter GitHub-Stand: https://github.com/julianzotter/nexus-platform/tree/fb103dbe6b0bd392c8bc6adc1b5988bac9cc5735 ; tools/deliver_work.py, tools/artifact_registry_gate.py, zugehörige Tests und AGENTS.md.
[S9] Bestehendes Artefaktregister: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view ; bestehendes ID-Ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view
Abruf: dieser Lauf; exakte lokale Bytehashes in Prüfunterlagen. Native Docs sind Textexporte, kein Hash ihrer nativen Providerrepräsentation. Aktueller Auftrag autorisiert WORK-Ablage, Registrierung, Review und GitHub-Review-Snapshot; keine Produktivfreigabe oder Berechtigungsänderung.

## Nachtrag: ID01-Kontinuitätsanweisung dieses Laufs
Direkte ID01-Anweisung vom 2026-11-02: sichere Kommunikation und Entwicklung trotz dokumentierter Richtlinienabweichungen fortsetzen; kein Löschen, keine E-Mails. Offene Gates blockieren nur den jeweils kritischen Schritt. Autorisierte WORK-Kommunikation wird nicht pauschal gestoppt. Dauerhafte Anweisungsdatei: https://drive.google.com/file/d/1n91iKIuiQz0H1Id1-mRwVXdxXMFQ6ycP/view . Persönliches ChatGPT-Memory ist mangels Schreibwerkzeug nicht aktualisiert.
