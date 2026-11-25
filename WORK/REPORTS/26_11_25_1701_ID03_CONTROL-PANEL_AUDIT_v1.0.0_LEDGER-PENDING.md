---
name: NEXUS_CONTROL_PANEL_AUDIT
version: 1.0.0
status: AUDIT_COMPLETE_WITH_BLOCKERS
timestamp: "2026-11-25T17:01:33+01:00"
agent_id: ID03
executor: OpenAI Codex Work
executor_instance: /root
model_id: null
role_register_version: NEXUS-ROLES-v1.2
source_commit: 0f43fd44faa685cd59b7732100523158fe181cc5
registration_status: REGISTRATION_PENDING
technical_release: NOT_REQUESTED
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: 217d9eed120e49c4211dfcb825726da077a1ec5be747b1d89bd57e338f1d88a3
---
# NEXUS Control Panel — Ideen, Live-Test und Drive/GitHub-Sync

Prüfauftrag von ID01: bestehendes Dashboard, versionierten Quellcode, generierte Daten und Aktualisierung prüfen; konkrete Testzugänge nennen. Prüfung am 25.11.2026, Zeitzone Europe/Berlin (an diesem Datum identisch mit Wien). Rolle ID03 / ChatGPT Private; Runtime OpenAI Codex Work, Instanz `/root`; genaue providerseitige Modell-ID nicht ausgelesen (`null`).

## 1. Ergebnis und Testzugänge

Das bestehende Panel ist erreichbar. Quellcode und JSON-Generator sind auf GitHub übernommen und der Generator wurde in CI erfolgreich ausgeführt. Die veröffentlichte Ansicht zeigt weiterhin den alten Basisdatensatz. Der automatische Drive/GitHub-Sync scheitert nachweislich am OAuth-Refresh. Ein frischer Seitenabruf belegt deshalb keine frischen WORK-Daten.

| Zugang | Zweck und geprüfter Stand |
|---|---|
| [Öffentliches Control Panel](https://nexus-sync-diagnose.julianzotter.chatgpt.site/#overview) | Tatsächlich im Browser geöffnet. Übersicht funktioniert. Angezeigte UI-Version v4.1. |
| [Rollenansicht](https://nexus-sync-diagnose.julianzotter.chatgpt.site/#roles) | Sichtbar noch ID02 Chef-Orchestrierung / ID03 Peer Review; widerspricht CURRENT NEXUS-ROLES-v1.2. |
| [Live-Meldungen](https://nexus-sync-diagnose.julianzotter.chatgpt.site/#live) | Zeigt 10-s-Abruf eines veröffentlichten Snapshots. Snapshot-Datum bleibt 23.11.2026. |
| [Neuer CI-Build zum Herunterladen](https://github.com/julianzotter/nexus-platform/actions/runs/45648182044/artifacts/15038881706) | Enthält `apps/control-panel/dist/` mit generierter `control-data.json`; GitHub-Anmeldung kann erforderlich sein. Keine neue öffentliche Preview dieses Builds belegt. |
| [Versionierter Panel-Code](https://github.com/julianzotter/nexus-platform/tree/0f43fd44faa685cd59b7732100523158fe181cc5/apps/control-panel) | Revisionsgebundene Code- und Datenbasis aus PR136. |
| [Drive CONTROL-PANEL](https://drive.google.com/drive/folders/1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g) | 23 direkte Einträge vor diesem Writeback: Konzepte, Berichte, Screenshots, HTML-Draft, Quellcode-Snapshots und Verknüpfung. |

### Den neuen Build lokal ansehen

Das oben verlinkte CI-Artefakt entpacken. Im entpackten Stammverzeichnis mit installiertem Python starten:

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory apps/control-panel/dist
```

Dann `http://127.0.0.1:8765` öffnen. Dies zeigt den gebauten statischen Stand; es repariert keinen OAuth-Zugang und startet keinen Drive-Sync. Diese lokale Startanleitung ist aus dem tatsächlich vorhandenen Build-Verzeichnis abgeleitet, wurde auf dem Rechner von ID01 nicht ausgeführt. Für eigenes Bauen siehe [Panel-README](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/apps/control-panel/README.md).

## 2. Versionsstände sauber auseinanderhalten

| Ebene | Tatsächlich belegt |
|---|---|
| Sites-Veröffentlichung | Öffentliche Site `appgprj_6afbb82d7b348191a51f51911f49b717`, Sites-Version 9; Deployment `appgdep_6b070226b3fc81918a8255b5921f4b69` am 25.11.2026, 16:43:45 MEZ mit Status `succeeded`. |
| Sites-Quellrevision | `2f36e517a3061b79c994d8299946a50fe5c197c7`; von Sites für Version9 zurückgegeben. Diese Revision gehört zum Sites-Quellpfad, nicht automatisch zum GitHub-main. |
| UI-Beschriftung | Im Browser weiterhin „Control Panel v4.1“. Diese Beschriftung ist keine Sites-Versionsnummer. |
| GitHub-Panelbestand | README bezeichnet ihn als „v8, versioniert“; PR136 stellt diesen Code plus Generator bereit. |
| Neuer generierter Datensatz | Schema4.2.0, `nexus.sourceCommit=0f43fd44faa685cd59b7732100523158fe181cc5`. |
| Weitere Prototypen | HTML-Draft v0.3.0, v1.1.0 und lokaler Adapter v1.2.0 haben eigene Versionsräume. |

Damit ist die pauschale Aussage „es wurde nichts deployed“ falsch: Sites-Version9 wurde veröffentlicht. Richtig ist: Der neu generierte GitHub-Datensatz ist in der geprüften Liveansicht nicht angekommen. Die Site-Metadaten und der Deploymentbeleg wurden über die Sites-Verwaltung gelesen; keine Veröffentlichung wurde durch diesen Audit ausgelöst.

## 3. Der entscheidende Datenabgleich

| Gegenstand | SHA-256 |
|---|---|
| Live-UI: angezeigter Panel-JSON-Hash | `d07b191e6d8cee3906c3ab35046a344f3745ef10b4950192c00353ff0386b5a2` |
| Repository-Basisdatensatz `control-data.base.json` | `d07b191e6d8cee3906c3ab35046a344f3745ef10b4950192c00353ff0386b5a2` |
| Tatsächlich heruntergeladene CI-`control-data.json` | `cc302f0d3c004e03d479499fa86645bdd54feda4dca30a7ddfae29c9b974e851` |
| Heruntergeladenes CI-ZIP | `4ac7fe7acb57dda2e9dcf9b3d1c01cacf7ba569aa93bb98965f0643053d72a0f` |

Der Browser-Reload änderte den Seitenabruf von 16:49:02 auf 16:50:07 MEZ. Datenstand 23.11.2026, 13:43:51 MEZ und angezeigter Hash blieben gleich. Der Live-Hash wurde aus der Oberfläche abgelesen; die CI-Datei und das CI-ZIP wurden aus heruntergeladenen Bytes gehasht. Der Basis-Hash ist zusätzlich im generierten Inputmanifest enthalten. Keine Behauptung eines direkten Rohbyte-Abrufs der Live-JSON.

Belege: [Basisdatensatz](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/apps/control-panel/data/control-data.base.json), [Generatorlauf](https://github.com/julianzotter/nexus-platform/actions/runs/45648182044), öffentliche Übersicht oben.

## 4. Was GitHub inzwischen wirklich implementiert

[PR136](https://github.com/julianzotter/nexus-platform/pull/136) wurde am 25.11.2026, 16:42:23 MEZ gemergt; Merge-SHA `0f43fd44faa685cd59b7732100523158fe181cc5`. Die geprüfte Hauptrevision entspricht diesem Stand. Der [Generator](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/tools/build_control_data.py) übernimmt folgende Quellen:

| Abschnitt | Herkunft | Abdeckung |
|---|---|---|
| Rollen | `registry/roles/role_capability_matrix.json` | 10 Rollen im geprüften Build; ersetzt alte manuelle Rollen. |
| Workflows | `orchestrator/registry/workflow-registry.json` | 17 Einträge. |
| Skills | `skills/**/SKILL.md` über Skill-Inventar | 26 Pakete im geprüften Repositorylauf; keine weltweite/geräteübergreifende Skillzählung. |
| Ledger | `governance/work-snapshot/00_ID_LEDGER.csv` | 201 Einträge; Repository-Spiegel vom 16.11.2026, kein Live-Drive-Ledger. |
| Berichtsdateien | `reports/**` und `WORK/REPORTS/**` | Dateinamen-/Ledgerklassifikation im Repository. |
| Monitor | `reports/monitor/nexus.snapshot.json` | Laufbeleg, andernfalls `NO_DATA` beziehungsweise `STALE_COMMIT`. |
| Projekte, Work Orders, Architektur und weitere Hauptansichten | `data/control-data.base.json` | Weiterhin manuell gepflegte Abschnitte. Nicht aus aktuellen Drive-WORK-Inhalten generiert. |

Der Build-Schritt und Artefakt-Upload im Monitorlauf45648182044 sind erfolgreich. Der Gesamtmonitor bleibt fehlerhaft: `coverage=INCOMPLETE`, `scheduler_runtime=FAIL`; die Drive-Abdeckung enthält keine belegten Zählwerte. Build-Erfolg und betriebliche Synchronisation sind unterschiedliche Prüfergebnisse.

[PR135](https://github.com/julianzotter/nexus-platform/pull/135), Merge-SHA `2af35c51a7081a5fde484c02825b92cd39295565`, enthält zusätzlich einen lokalen lesenden Drive-/GitHub-Metadatenadapter. Er ist trotz „DRAFT“ im Titel gemergt. Laut [Adapter-README](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/prototypes/nexus-control-tower-draft-v1/live/README.md) läuft er auf `127.0.0.1:8766`, braucht gültigen autorisierten OAuth-Kontext und ist kein Deployment auf die öffentliche Site. Seine Listen sind aus Dateinamen abgeleitete Teilmengen, kein vollständiger WORK-Ledger.

## 5. Drive und automatische Synchronisation

| Prüfung | Ergebnis und Beleg |
|---|---|
| Drive-Ordner lesen | PASS; 23 direkte Einträge im exakt identifizierten CONTROL-PANEL-Ordner. Aktueller Implementation-Plan zuletzt geändert 25.11.2026, 16:32:46 MEZ. |
| HTML-Quellcode v1.1.0 | In Drive als natives Google-Dokument mit HTML-Quelltext abgelegt; keine ausführbare `.html`-Datei. [Snapshot](https://docs.google.com/document/d/1uJjdxRGOJjhXTWXQ2tuzjMoIYJhD4yiUwFUZWD5zbKM/edit). |
| GitHub → WORK | FAIL im [Run45648281482](https://github.com/julianzotter/nexus-platform/actions/runs/45648281482): `OAUTH_HTTP_400_INVALID_GRANT`, `REAUTHORIZE_GOOGLE_CONSENT`, `write_test=NOT_RUN`; Zustellung übersprungen. |
| Drive → GitHub | FAIL im [Run45594293029](https://github.com/julianzotter/nexus-platform/actions/runs/45594293029): derselbe OAuth-Fehler, Gate `DRIVE_POLL_NOT_OPERATIONAL`. |
| Hauptbranch-CI | [Run45648182364](https://github.com/julianzotter/nexus-platform/actions/runs/45648182364): 416 bestanden, 2 übersprungen, 1 fehlgeschlagen; `test_committed_manifest_matches_build` der Design Gallery. |
| Vorliegende Korrektur | [PR139](https://github.com/julianzotter/nexus-platform/pull/139) offen zum Prüfzeitpunkt; dessen [CI45648841379](https://github.com/julianzotter/nexus-platform/actions/runs/45648841379) erfolgreich. Kein Merge durch diesen Audit. |
| Öffentliche Sites-Zeitplanung | Sites-Verwaltung liefert für das Panel `automations=[]`. Das sagt nichts gegen den separat konfigurierten GitHub-Scheduler, belegt aber keine Sites-eigene periodische Aktualisierung. |
| Privater Datenpunkt | Anderes Sites-Projekt: `appgprj_6b0618d628b48191b31ca037b31cd0b5`. Zugeordnete stündliche Automation ist laut Hosting-Metadaten deaktiviert. Feed-Inhalt nicht geprüft. |

Der erfolgreiche Drive-Zugriff dieses ChatGPT-Laufs verwendet einen anderen Zugriffspfad als die fehlgeschlagenen GitHub-Actions. Deshalb kann der Ordner hier lesbar sein, während der automatische Sync scheitert. Ein neuer Bericht im Drive oder ein Git-Commit behebt diesen OAuth-Fehler nicht. Das vorhandene [OAuth-Recovery-Runbook](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/docs/NEXUS-OAUTH-RECOVERY.md) und [WORK-Troubleshooting T04](https://drive.google.com/file/d/1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR/view) verorten die erneute Google-Autorisierung bei ID01; keine Tokens wurden gelesen oder geändert.

Die Bezeichnung „Drive→GitHub“ meint beim geprüften [Workflow](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/.github/workflows/nexus-drive-poll.yml) einen lesenden Drive-Änderungsfeed in Actions-Artefakte und Job Summary. Dieser Workflow schreibt ausdrücklich keine Git-Commits und keine Drive-Dateien. Auch nach OAuth-Reparatur wäre dadurch allein kein vollständiger bidirektionaler Dateisync hergestellt.

## 6. Bewertung der Ideen und gezielte nächste Umsetzung

Das Zielbild aus einem Datenvertrag, einem Generator, einer gemeinsamen Oberfläche und einem lokalen/authentifizierten Backend ist für diesen Bestand sinnvoll. Der vorhandene [Konsolidierungsvorschlag](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/apps/control-panel/README.md) sollte weitergeführt werden. Zusätzliche unabhängige Dashboard-Master würden die bereits sichtbaren Versions- und Datenwidersprüche vergrößern.

Das tatsächliche Verhalten des geprüften [Repository-Refreshhandlers](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/apps/control-panel/site/app.js) ist ein GET auf `control-data.json` plus ein GET auf einen festen Work-Order-Beleg. Sein 10-s-Timer lädt nur die veröffentlichte JSON neu; er startet weder Generator noch GitHub-Workflow. Die in der Liveversion zusätzlich beobachteten Bedienelemente `startFeed`/`autoFeed` sind in diesem geprüften main-Handler nicht enthalten. Ihre erfolgreiche Quellenaktualisierung wurde daher nicht aus dem älteren Code abgeleitet und nicht als getestet dargestellt.

### Priorität 1 — Quellenpfad reparieren und belegen

OAuth im tatsächlich ausführenden Sync-Dienst erneuern; anschließend Drive-Poll und GitHub→WORK jeweils mit erfolgreichem Laufbeleg prüfen. Den neuesten freigegebenen Ledger-Stand kontrolliert übernehmen. Fehlende Quelle bleibt `UNKNOWN`/`STALE`; kein Erfolg aus einem bloßen HTTP200 oder frischen Seitenzeitstempel ableiten.

### Priorität 2 — Generierten Stand gezielt veröffentlichen

Den gebauten `dist/`-Stand aus einer konkret festgehaltenen Revision in das bestehende öffentliche Sites-Projekt bringen. Dabei die bereits vorhandene neuere Sites-Version9 berücksichtigen und deren Zusatzfunktionen nicht durch einen älteren Repository-Snapshot überschreiben. Abnahme: veröffentlichter JSON-Hash entspricht dem ausgewählten Build, Rollen stimmen mit Manifestv1.2, Versionsangaben benennen UI/Schema/Deployment/Quellrevision getrennt.

### Priorität 3 — Button und Zeitangaben fachlich korrekt machen

„Anzeige neu laden“ darf einen vorhandenen Snapshot lesen. „Quellen jetzt prüfen“ muss dagegen einen autorisierten Backend-Lauf mit Run-ID anstoßen beziehungsweise dessen neue Quellenprüfung nachweisen. Manueller und geplanter Trigger sollten denselben geprüften Sync-Code nutzen. Der Browser erhält keine OAuth-Secrets. Darzustellen sind getrennt: Quellenstand je Quelle, letzte erfolgreiche Quellenprüfung, Buildrevision, veröffentlichte Revision und Browserabruf.

Konkrete Generatorlücke: `asOf` wird derzeit auf die Commitzeit gesetzt, obwohl Projekte/Orders aus dem älteren Basisdatensatz übernommen werden. Eine neue Buildzeit darf diese Abschnitte nicht frisch erscheinen lassen. Zusätzlich darf das aus einem Ledger-Spiegel berechnete `nextFreeId` keine tatsächliche Nummernvergabe autorisieren. Fehlende Zeitwerte müssen als „unbekannt“ erscheinen; die Liveansicht zeigt aktuell bei manchen Rollen fälschlich 01.01.1970.

## 7. Abnahme, Grenzen und Prüfprovenienz

Für eine echte Ende-zu-Ende-Abnahme sind drei Fälle noch offen: autorisierte Quelländerung bis in dieselbe Browseransicht verfolgen; unveränderte Wiederholung ohne künstliche fachliche Revision; OAuth-/Quellenfehler bei erhaltenem letzten gültigen Stand. Jeder Fall braucht Quellenrevision, Run-ID, Payload-Hash und Browserbeleg.

Drei getrennte OpenAI-Instanzen prüften Anhänge/Konzepte, Repository/CI und Live-UI. Keine externen Claude-/DeepSeek-/Gemini-Läufe behauptet. Der unveränderte beigefügte v0.3.0-Draft wurde zusätzlich in drei isolierten Mock-Fällen ausgeführt: alte Daten erhalten Erfolgsanzeige ohne Altersprüfung; Revision wird nicht geprüft; HTTP503 erhält vorhandene Daten. Diese Tests sind keine Live-E2E-Prüfungen und keine Aussage über den späteren v1.1.0-Code.

Der Aufruf des als privat gekennzeichneten Feedlinks wurde von der automatischen Browser-Freigabeprüfung abgelehnt, weil eine eindeutige Autorisierung für private Feedinhalte aus Sicht dieser Prüfung fehlte. Kein manueller Nutzerabbruch. Kein Login, Retry, alternativer Abruf oder Umgehen der Prüfung. Die Abgleichbuttons wurden deshalb nicht betätigt. Ein zusätzlicher privater Feedtest benötigt eine gezielte Freigabe dieses Tests; öffentliche Ansicht, Quellcode, Hosting-Metadaten und Action-Läufe konnten unabhängig geprüft werden.

Governance gelesen: [AGBs v007.2](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view), [Manifest v1.2 §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view), [CURRENT Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view), [WORK/Folder.md](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view), Frontmatter-Lesesnapshot v008 und [GitHub AGENTS](https://github.com/julianzotter/nexus-platform/blob/0f43fd44faa685cd59b7732100523158fe181cc5/AGENTS.md).

Persistierter [START_ACK](https://drive.google.com/file/d/1Q-B6lMfsRdfmKHwov3v3KrXltwBoVhfQ/view): Rohbyte-Readback PASS, SHA-256 `762c22b2dbcba46e8ef71cdd2b53c341c16f4bcb4d7266536599dc5320d42896`. Abweichung offengelegt: Der persistierte ACK wurde erst nach Beginn der lesenden Prüfungen erstellt, nicht rückdatiert. Nummernregistrierung bleibt `REGISTRATION_PENDING`; kein zentraler Ledger geändert. Kein Produktionscode, Deployment, OAuth-Kontext oder Rollenregister wurde durch diesen Audit verändert. Abschließende Speicher- und Hashbelege stehen im separaten Writeback-Receipt.
