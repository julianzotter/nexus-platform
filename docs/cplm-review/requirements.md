---
document_id: NEXUS-CPLM-CHAT-REQUIREMENTS
version: 0.3.0
timestamp: '2026-10-16T18:02:55.438462+02:00'
status: EXECUTING_WITH_EXPLICIT_BLOCKERS
author: ChatGPT-Codex
scope: Vollständiger in dieser Sitzung verfügbarer direkter Chatverlauf und gelesene WorkOrders; keine Vollständigkeitsbehauptung
  für abgeschnittene externe Chats
authority: Aktuelle direkte ID01-Nutzeraufträge haben Vorrang vor älteren widersprechenden Entwürfen
main_goals:
- zentrale_Ideen_und_Regeln
- kontrollierte_Multiagent_Ausführung
- kontinuierliche_Prüfung_und_Informationsweiterleitung
requirements:
  R01:
    goal: Eine versionierte AIM-Markdownliste für vorläufige Ideen/Konzepte vor Workflows
    state: STORED_AND_READBACK_VERIFIED
  R02:
    goal: Fortlaufende stabile Konzept-Tickets; Originaltext/Dialog möglich; verworfene/umgesetzte Einträge erhalten
    state: STORED_AND_READBACK_VERIFIED
  R03:
    goal: 'Erste Idee: Minimalprüfung mit kleinstem Kontext/Prompt; Status neu bis umgesetzt/validiert'
    state: CONCEPT_STORED_NOT_IMPLEMENTED
    note: Statuskodierung bislang Vorschlag; keine abgeschlossene Umsetzung erfinden
  R04:
    goal: Shared Understanding und Ubiquitous Language vor Umsetzung
    state: DOCUMENTED_PARTIAL
    gap: Kein universell erzwungenes Start-Gate
  R05:
    goal: Neue WORK-Kommunikation als Raw-UTF8-MD, keine neuen Google Docs
    state: PASS_FOR_THIS_SESSION
  R06:
    goal: YY_MM_DD_HH_mm vorn, dann ID/semantischer Titel/Version; Zeitmetadaten und Änderungslog
    state: PASS_FOR_NEW_REPORTS
    gap: Keine globale Migration aller Bestandsdateien
  R07:
    goal: Jeder Agent liest Ordnerstatus vorher, speichert/verifiziert Ergebnis danach
    state: PASS_FOR_OBSERVED_RUNS_PARTIAL_SYSTEM
    gap: Andere Runtimes nicht technisch gezwungen
  R08:
    goal: Stabile Folder.md je Ordner als Timestamp-Ausnahme; Domain/Scope/Intent/Content/Actor/Artefakte/Taskstatus
    state: PASS_WORK_AND_REGISTRY
    gap: Weitere Ordner-Rollout offen
  R09:
    goal: Ordnerregeln nach unten vererben; Child darf Grundregeln nicht ungeprüft lockern
    state: LOCAL_PAIR_RESOLVER_TESTED_GLOBAL_OPEN
  R10:
    goal: Front-Log mit vollständigen Zuständen N/N-1/N-2/N-3 und Baseline; append-only
    state: HISTORY_EXISTS_PARTIAL
    gap: Single-Writer/Manipulationsschutz nicht global erzwungen
  R11:
    goal: DELTA nach Accuracy/Consistency/Scalability/Robustness/Resilience/Governance/Latency/Efficiency; Ursachenrückführung
      und Refinement
    state: CONTRACT_DEFINED
    gap: Messwerte ohne Testreferenz bleiben NOT_MEASURED
  R12:
    goal: CPLM/CICKS mit Dispatcher, Execution Bridge, Orchestrator, Regeln, GitHub Actions oder besserer Minimallösung
    state: LOCAL_KERNEL_36_TESTS_PASS_CLOUD_ADAPTER_OPEN
    evidence: Kern samt Regressionen in Review; Router und bestehender GitHub-CI-Pfad verifiziert
  R13:
    goal: Sync, Wartung, Health/Audit und Statusberichte im Hintergrund; aktuell stündliches WORK-Monitoring
    state: HOURLY_ENABLED_PILOT_OBSERVED
    gap: Kein nachgewiesener kompletter OneDrive→GitHub-Produktivsync
  R14:
    goal: 'Drei unabhängige Stellungnahmen: Software, AI Governance, Systems/Innovation; je Befunde/Risiken/Verbesserungen/Fragen/Empfehlung'
    state: THREE_SEPARATE_REVIEW_INSTANCES_COMPLETE
  R15:
    goal: Drei echte sequenzielle Reviewer-Runs, vierter separater Konsolidierungsrun; keine Simulation
    state: THREE_SEQUENTIAL_PLUS_FOURTH_CONSOLIDATION_COMPLETE
    limits: Getrennte Instanzen/Kontexte; verschiedene Provider/Modelle nicht belegt; vollständiges Tokenfenster nicht erzwingbar
  R16:
    goal: Nach Konsolidierung DELTA, erneute Prüfung, Human Gate; keine Eigenfreigabe
    state: MULTIPLE_DELTA_FIXES_TESTED_FINAL_LOCAL_REVIEW_RUNNING_HUMAN_BLOCKED
  R17:
    goal: Separate LLM-ID-Kompetenz/Rechte/Account/Modell-Matrix; WORK nur Wegweiser
    state: DRAFT_STORED_AND_PR18
    gap: Kanonische ID-Zuordnung und Fremdaccounttests offen
  R18:
    goal: Fähigkeitsumfrage Read/Write/Notify/ACK und Troubleshooting zu Business/Privat-Ace und Gemini-GitHub
    state: PREPARED_IN_REGISTRY
    gap: Zustellung/ACK/Antworten aus anderen Accounts fehlen
  R19:
    goal: Routing nach erforderlicher Kompetenz, Scope, Tools, freier Kapazität/Budget und Workload
    state: DESIGNED_NOT_DEPLOYED
    limits: Unbekannte Quotas bleiben UNKNOWN
  R20:
    goal: GitHub-versionierter überprüfbarer Stand ohne zweite unabhängig gepflegte SSOT
    state: CODE_TESTS_FOUR_REVIEWS_IN_DRAFT_PR18_FINAL_DELTA_NEXT
    gap: Umsetzungsdelta und vollständiger Reviewbericht werden ergänzt
  R21:
    goal: Nach Fertigstellung sichtbare Benachrichtigung; Pilot sofort ausführen
    state: EMAIL_TRANSPORT_VERIFIED
    evidence: 'Gmail 1a145489e35d9f01: SENT und INBOX'
    limits: Geräte-Push/Lesen nicht nachgewiesen
  R22:
    goal: Drei etablierte Methoden mit genauen offiziellen URLs
    state: DONE
    refs:
    - GitHub_Actions
    - n8n
    - Temporal
    - LangGraph_als_zusätzliche_Option
  R23:
    goal: Stewart-Brand-Pace-Layers auf NEXUS übertragen; langsame Grundlagen und schnelle Runtime trennen
    state: DESIGN_DOCUMENTED
    limits: L0–L5 Entwurf; P0-Priorität davon getrennt
  R24:
    goal: Jede Anforderung prüfen, Fehler verbessern, erneut prüfen, alternative Lösung suchen
    state: ITERATIVE_FIXES_ACTUALLY_EXECUTED_EXTERNAL_BLOCKERS_REMAIN
    limits: Kein Herabsetzen der Abnahme; externe Blocker und Human Gate bleiben offen statt Erfolg zu simulieren
  R25:
    goal: Keine Memory-/History-Snippets als Status-/Fachbeleg; aktuelle vollständige Quelldatei lesen
    state: PASS_FOR_CURRENT_REVIEW
    evidence: Neun vollständige Quellen im eingefrorenen Reviewbundle
  R26:
    goal: Gemini Argon benötigt echten Markdown-Read/Write-Zugriff ohne Copy-Paste; iterative Fehlerkorrektur und Selbstheilung
    state: BLOCKED_FOREIGN_RUNTIME
    evidence: NEXUS-WO-GEMINI-ARGON-BRIDGE-001 gespeichert und zurückgelesen
    gap: Argons Runtime hat hier keine aufrufbare authentifizierte Schreibverbindung
review_bundle:
  source_count: 9
  characters: 62660
  manifest_sha256: 1d0b94c0f3c0473736571fa0302f8a4adde7b04012d0c1c1ac038cd6a38cb162
blockers:
- Originale abgeschnittener anderer Chats sind über diese Sitzung nicht vollständig abrufbar.
- Fremdaccount-Anmeldungen und tatsächliche Toolrechte nicht verfügbar; genaue kanonische Rollen-ID-Matrix nicht belegt.
- Geräte-/Browser-Push-Einstellungen können mangels verbundenem Browser nicht geändert werden.
- Technisch erzwungene exklusive Drive-Schreibstelle und authentifizierte Freigabegrenze noch nicht installiert.
- Vertrags-/Produktionsfreigabe benötigt ID01 nach Delta/Re-Review; kein LLM darf diese selbst ersetzen.
source_refs:
- Aktuelle direkte Nutzerbeiträge dieses vollständig verfügbaren Sitzungsverlaufs
- https://drive.google.com/file/d/15EQRq80eyl6fqBj5Lnu9yBDUjgT2NbEnqF2Ii6XQfxo/view
- https://drive.google.com/file/d/1QekWzh3XPdhoYGFOw7V7-6PqTnEM5T1F/view
- https://drive.google.com/file/d/1JVapYaD6ezcKsH5cd8BaeezSDV1qp6Y1/view
next_action: Finalen lokalen 36-Test-Stand drei Perspektiven prüfen lassen und in PR18/CI nachweisen; Gemini-Runtime/Accounttests/exklusive
  Cloud-Auth/Humanfreigabe bleiben externe Voraussetzungen.
---
# Abschlussregel
Nur kriterienspezifisch bestätigte Ergebnisse als PASS melden. Ein Versandbeleg ersetzt keinen Empfangs-ACK; ein Pilot-PASS keine Produktionsfreigabe. Diese Matrix ist die vollständige verfügbare Auftragsabdeckung, kein pauschaler Erledigtvermerk.

