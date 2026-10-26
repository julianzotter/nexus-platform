---
name: EVAL-REPARATUR-KOMMUNIKATION-PROFILE
version: 1.0.0
status: OPEN_FOR_RESPONSES
timestamp: 2026-10-26T15:54:37+01:00
agent_id: ID03
executor_instance: /root
executor: OpenAI Codex
owner_id: ID01
ticket_id: WO-REG-CAP-001
coordination_ticket: WO-20261026-NEXUS-REPAIR-01
source_of_truth: DRIVE_WORK_CAPABILITY_FOLDER
content_hash_sha256: 2ca6afdd9c90b59d6e72fdb0bcfceec0e856c442865ffd2be815d99f717eda5c
hash_scope: body_utf8
---

# Evaluierungsbogen: Reparaturkonzept, Kommunikation und Arbeitsprofile

## 1 Auftrag und Rücklauf
Fortsetzung von WO-REG-CAP-001 / AIM-0005, keine zweite Account- oder Kompetenzregistry. Koordination: WO-20261026-NEXUS-REPAIR-01. Vorhandene Umfrage bleibt Referenz: https://drive.google.com/file/d/1JVapYaD6ezcKsH5cd8BaeezSDV1qp6Y1/view
Zuerst Fähigkeiten und Lösungsvorschläge erheben, dann vergleichen, kleinsten durchgängigen Slice auswählen, testen und gesondert freigeben. Die nachstehenden Arbeitsprofile sind Evaluierungsgegenstand; keine Aktivierung eines Dauerbetriebs.
Adressaten: tatsächlich beteiligte Instanzen der Rollen ID02–ID08 sowie weitere durch ID01 autorisierte Instanzen. Rolle, Provider, Account und Runtime getrennt angeben; keine fremde Identität übernehmen. Aus dieser Ablage folgt weder Zustellung noch ACK.
Antwort auf Deutsch; Englisch nur Begriffsmapping. Eigene Datei im vorhandenen Capability-Ordner oder autorisierter WORK-Inbox: YY_MM_DD_HH_mm_ID-XX_EVAL-REPARATUR-ANTWORT_vX.Y.Z.md. Unbekannte Rollen-ID als UNASSIGNED kennzeichnen, nicht erfinden.

## 2 Einheitliche Fragen an jede Instanz
| Nr. | Frage | Erforderlicher Nachweis |
|---|---|---|
| E01 | Welche konkrete Rolle, Provider-/Account-/Runtime-Instanz und Modellkennung antwortet? | Rollenquelllink, Instanz-ID, Modell UNKNOWN falls nicht offengelegt |
| E02 | Kann diese Instanz WORK tatsächlich lesen, neue Raw-MD-Dateien schreiben, updaten und unveränderte Bytes zurücklesen? | Jede Operation separat mit Datei-ID, UTC-Offset-Zeit, SHA256/Hashumfang; kein pauschales Ja |
| E03 | Welcher Auslöser kann ohne offenen Chat laufen: Aufgabenfunktion, Betriebssystem-Scheduler, API, Webhook, Worker? | Offizielle Primärquelle oder echter Lauf; Installation/Aktivierung/Betrieb getrennt |
| E04 | Welche der Profile unten sind technisch möglich und welches Mindestintervall gilt? | Account-/Runtime-bezogene Limits, Verzögerung, Timeout, maximale Laufzeit; UNKNOWN zulässig |
| E05 | Wie aktiviert ein konkreter Work Order das Minutenprofil und beendet es wieder? | ticket_id, activation_ref, erlaubter Scope, Ablaufzeit/Endbedingung, vorheriges Profil, Stop-Nachweis |
| E06 | Wie werden Initialbestand, Änderungen, doppelte Zustellung, Ausfälle und Schreibfehler verarbeitet? | Test: gleiche ID nicht doppelt ausführen; Cursor erst nach sicherer Ablage; Fehler statt falschem Grün |
| E07 | Wie wird aus Erkennung eine echte Auftragsübernahme und Rückmeldung? | CLAIM/Lease, Dispatch, erreichbare Runtime, tatsächlicher ACK und Ergebnis-Readback; Erkennung allein reicht nicht |
| E08 | Wie funktionieren parallele eigene Dateien und sichere zentrale Konsolidierung? | Zeitstempel+Rollen-ID+Instanz-ID+run_id; Konflikt-/Single-Writer/CAS-Verfahren; History erhalten |
| E09 | Unterstützt die Lösung deutsche Hauptbegriffe, stabile Begriffs-IDs und englische Mappings? | Quellengebundene Taxonomie; technische Feldnamen kompatibel; UNCLASSIFIED statt erfundener Labels |
| E10 | Welche Lösung empfiehlst du für dich UND andere Instanzen? | Höchstens 3 Vorschläge: bestehender Baustein, konkrete Lücke, Aufwand/Kosten nur belegt oder UNKNOWN, kleinster Test, Abhängigkeit, Risiko |
| E11 | Welche Zugriffs-/Betriebsgrenzen blockieren aktuell? | Keine Secrets; WORK anyone:writer ist aktuell belegt. Autorisierte Writer erhalten; Rechteänderung gesondert prüfen |
| E12 | Welche Ideen sollen jetzt zurückgestellt werden? | Bestehende AIM-ID verlinken; Originalgedanke erhalten; Disposition deferred + Wiederaufnahme-Auslöser |

### Antwortfelder
answer_id, survey_version, ticket_id, timestamp, timezone, role_claim, role_source, provider, account_alias, instance_id, model_id, answers[E01..E12], capability_tests[], proposals[], restrictions[], source_refs[], produced_artifacts[], hash_scope, qa_status, next_action.
Pro Fähigkeit: capability, target_id, operation, observed_at, result (VERIFIED / USER_REPORTED / PROPOSED / UNVERIFIED / BLOCKED), evidence_ref, limitations. Leere Beweise nicht mit VERIFIED versehen.

## 3 Zu evaluierende Intervall-/Aufgabenmatrix
| Profil | Intervall / Wiener Zeit | Aufgaben-Zuordnung | Aktivierung / Status |
|---|---|---|---|
| P1 | 1 Minute | ausdrücklich benannte Spezialaufgabe / intensive Entwicklung | nur expliziter Work Order + Aufforderung; begrenzter Scope und Laufzeit; nie globaler Standard |
| P2 | 10 Minuten | aktive Entwicklung mittlere Frequenz | Zuordnung Vorschlag; per Aufgabe evaluieren |
| P3 | 30 Minuten | laufende Entwicklung niedrige Frequenz | Zuordnung Vorschlag; vorhandener GitHub-Observer derzeit 30min, kein Dispatcher-Beweis |
| P4 | 60 Minuten | reguläre Überwachung | Zuordnung Vorschlag; aktuelle Aufgabenfunktion dieser Sitzung erlaubt höchstens stündlich |
| P5 | 00:00 / 06:00 / 12:00 / 18:00 | vier Tagesprüfungen | Wandzeit Europe/Vienna; Sommerzeitwechsel berücksichtigen, kein fester 360min-Ersatz |
| M1 | wöchentlich | globale Wartung / Konsistenz / Backups / offene Ideen | eigener Auftragstyp; Wochentag und Uhrzeit noch offen |
Die Intervalle wurden von ID01 als zu untersuchende Profile genannt. Konkrete Aufgaben-Zuordnungen und Automatik sind noch keine abgenommene Betriebsregel. Umschaltung ausdrücklich; tatsächliche Nutzeraktivität nicht erraten.

## 4 Gemeinsame Auswertung und Abnahme
- Befunde nach Problem/Capability/Runtime konsolidieren; belegte Fakten, Vorschläge, unbekannte Werte und Blocker getrennt.
- Kleinster sicher ausführbarer Slice zuerst: Erkennung -> CLAIM -> Bearbeitung -> Ablage -> Hash-Readback -> ACK -> Abschluss, durchgehend dieselbe ticket_id.
- Negative Tests für fehlende Credentials, Doppelzustellung, Worker-Ausfall, Schreibfehler und abgelaufene Minutenaktivierung.
- Ein grüner Zeitplan ist kein erfolgreicher Auftrag. Keine Deployment-/Produktionsfreigabe aus diesem Fragebogen.
- Rückläufe dürfen spätere Verbesserungsaufträge begründen. Gute nicht priorisierte Vorschläge in derselben AIM-Liste zurückstellen, kein weiteres Ideenregister.

## 5 Quellen und aktueller Ausgangspunkt
Reparatur-One-Pager: https://drive.google.com/file/d/1_gGFxQ0lQli-DIkbDpogaXXt25FkntTc/view
CURRENT Baseline MUST-20/21/40–55/90–96/150–159: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
AIM-Konzeptregister: https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view
WORK-Policy: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
Speed-Team-Auftrag: https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view
Parser-Reparatur: https://github.com/julianzotter/AI-ENGINEERING-SYSTEM/pull/4
