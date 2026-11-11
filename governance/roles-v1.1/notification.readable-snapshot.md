ID01-Festlegung 2026-11-11 — verbindliche Rollenbezeichnung
ChatGPT Private = ID02 — ChatGPT Private / ChatGPT Chief Orchestrator.
Maßgeblich: NEXUS-ROLES-v1.1, Manifest §4: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Historische Zuordnungen „ChatGPT Private = ID03“ und „ChatGPT Business = ID02“ sind für die aktuelle Benennung überholt. ID03 bleibt ChatGPT Assistant / Peer Reviewer; keine automatische Neuzuordnung anderer Instanzen.
Rollen-ID und tatsächliche Runtime getrennt dokumentieren. Für diesen autorisierten Lauf: agent_id/role_id ID02; agent_name ChatGPT Private; executor OpenAI Codex; executor_instance /root; provider OpenAI; model_id null (nicht verifiziert).
Vor neuer Rollenentscheidung aktuellen Manifeststand lesen. Kennung ID02 in neuen Berichten dieser Instanz verwenden; historische Dateien unverändert erhalten.
Publikation, Zustellung, ACK und unabhängige Prüfung getrennt erfassen. Die Bereitstellung allein belegt keine Kenntnisnahme anderer LLMs.
Änderungsautorität: ausdrückliche ID01-Anweisung im Sprachdialog 2026-11-11 zur Ergänzung, Bekanntgabe, WORK/Frontmatter/AGB-Aktualisierung, GitHub-Synchronisierung, Sicherung und Ausrollung.
Koordination: WO-20261111-ID02-PRIVATE-ROLLOUT. Geltung ausschließlich Rollenbezeichnung und deren Verteilung; keine technische Produktionsfreigabe.


NEXUS Statusreport Rollenregister und Konsolidierung
VERSION: NEXUS-CONSOLIDATION-20260928-v1.0 | ADOPTED 2026-09-28
AN: alle beteiligten NEXUS-Rollen und deren ausführende Runtime-Instanzen
ZWECK: verbindliche Bekanntgabe zur Kenntnisnahme; ersetzt die bisherige Agent Notification dieses Drive-Objekts.


Beschluss
ID01 hat am 2026-09-28 den Vorschlag NEXT_STEPS_UND_ROLLEN.md angenommen: „dein Vorschlag ist angenommen und damit fix verbindlich vereinbart“. Dieser Beschluss autorisiert Rollenfestlegung, Konfliktbereinigung und Bekanntgabe; er behauptet keine Implementierung, externe Ausführung oder Kenntnisnahme.


Ein einziges Rollenregister
Verbindlich ist ausschließlich NEXUS-ROLES-v1.1 im CURRENT Manifest, Abschnitt 4:
https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Die Rollenliste wird in diesem Report nicht parallel gepflegt. ID09 bleibt ausschließlich historischer Alias; ID10 bleibt inaktiv. Codex-Ausführung wird als tatsächliche Runtime dokumentiert und nicht als Claude oder als erfundene neue Rolle ausgegeben.


Bereinigte Vorgaben
1. CURRENT-Autorität umfasst ausdrückliche spätere ID01-Adoptionen. Der alte Stichtag sperrt die Freigabe vom 28.09. nicht mehr.
2. Baseline verweist auf das einzige Rollenregister. Kenntnisstand, Adoption, Ticketstatus, Evalstatus und Betriebsnachweis bleiben getrennt.
3. Eindeutige Auftragsreferenzen: WO9-MVC und WO9-SEIL-FT; WO10-EVIDENCE und WO10-INDEX-FIRST. Alte Namen/IDs bleiben auffindbare Aliase, keine blinde Umnummerierung.
4. Ein Semantic-Pilot: maßgeblicher Input https://drive.google.com/file/d/1_N-J3pSAcHtr5sv0jGFmyWHpYQYz4TJj/view . Die gleichnamige zweite v1.1-Datei wird zum Verweis; die ältere Langfassung bleibt historische Referenz. WO12 und Index-first werden in diesen Pilot integriert.
5. WO0 und WO5–7 verwenden denselben expliziten M2-Testvertrag. Keine Korrektur realer Eingaben nur zur Anpassung an einen verborgenen Sollwert.
6. WO14 berücksichtigt bestehende Namenskonventionen, IN/OUT und Versionen. Titel/Größe begründen nur Dublettenverdacht. WO15 verlangt unabhängige Prüfung von Code und Testfällen.
7. Baseline-/Systemprompt-Spiegel sind Discovery-Verweise, keine konkurrierenden Governance-Kopien. Das RUNLOG bleibt historische Evidenz; aktuelle Ticketstände gehören in die Ticket Registry.


Verbindliche Abarbeitungsfolge
WO16/WO1 Identitäts- und Statusabgleich -> WO12 + Semantic MVP (25–50 Ressourcen) -> WO-GPT-03 durchgängiger Golden Slice.
ID02 koordiniert. ID04 liefert Quellennachweise. ID06 verantwortet Implementierung und Toolausführung. ID03 plant/prüft die Abnahme; ID07 prüft unabhängig. ID01 entscheidet über die fachliche Promotion.
WO3/WO0/WO4 ergänzen den Testpfad. WO14/WO15 folgen kontrolliert. WO13 bleibt zurückgestellt. SEIL/FT bleibt separater Fachpfad; HBV bleibt bis zum Nachweis seiner Voraussetzungen blockiert. Keine automatische Start- oder DONE-Meldung.


Kenntnisnahme und Arbeitseinstieg
Jede beteiligte ausführende Instanz liest Manifest und Baseline und gibt beim nächsten Aufruf zurück:
ACK NEXUS-ROLES-v1.1 | role_id | executor_instance | provider/model_id | read_at | conflicts
ACK-Erfassung: bestehende Ticket Registry, dedizierte ACK-Zeilen. WORK_REFERENCES enthält die eindeutige Zuordnung alter WO-Aliase zu Drive-IDs und gemeinsamem Koordinationsauftrag. Anfangsstatus OPEN; keine Empfangsbestätigung wird erfunden. Ein ACK-Ticket ist erst DONE, wenn die tatsächliche Rückmeldung mit Quellenbeleg erfasst ist.
Danach CLAIM <ticket_id> <role_id>; Status OPEN -> CLAIMED -> RUNNING -> DONE, alternativ BLOCKED / REVIEW_REQUIRED / FAILED. DONE benötigt Abnahme und QA. Ergebnis: FINDINGS | EVIDENCE/SOURCES | ARTIFACTS | RISKS | NEXT_ACTION | QA_STATUS.


Kanonische Einstiegspunkte
Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
Tickets und ACK-Nachweise: https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit
Operative Ablage: _developement/LLM-LOCAL-SSOT/WORK. Discovery: _INDEX.MASTER und _INDEX_LNK/10-STATUS-AI-STACK-Implementierung.


Verifikation und Grenzen
WRITE_READBACK_STATUS: PASS — 31 Inhaltsänderungen rückgelesen; 10 native Dokumente textgleich zum Patch; 21 Raw-Dateien nach erneutem Download SHA-256-identisch. Baseline-Ablage und Ticket-Registry verifiziert. Testnachweis betrifft Dokumentänderungen, keinen Pipelinebetrieb.
Bekanntgabe bedeutet Bereitstellung im gemeinsamen Drive-Kanal. Drive allein aktiviert keine externen LLMs. Externe Ausführung und Kenntnisnahme sind bis zur belegten Rückmeldung UNCONFIRMED.
Autor: OpenAI Codex. Unabhängiger Gegencheck: separater Codex-Reviewer gleicher Modellfamilie. Keine externe Claude-/DeepSeek-Prüfung behauptet. Originaldateien, native Revisionen, Patchsatz und Read-back sind lokal im Änderungsnachweis gesichert. Ein zusätzlicher ZIP-Upload wurde durch automatische Freigabeprüfung abgelehnt; das Sicherungsarchiv bleibt lokal. Dies blockiert die verifizierten In-place-Korrekturen nicht.
Scope: die im Audit identifizierten CURRENT-Dokumente, WORK-Aufträge, Semantic-Doppelung und geprüften Mirrors. Keine Behauptung einer vollständigen Bereinigung sämtlicher Drive-Archive.