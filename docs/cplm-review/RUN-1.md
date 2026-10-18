# RUN 1 — unabhängige Softwarearchitektur- und Durable-Workflow-Prüfung

**Reviewerinstanz:** `/root/cplm_run1_software_architecture`, als eigenständige Reviewerinstanz vom Koordinator `/root` für TRUE RUN 1 beauftragt. Perspektive: Softwarearchitektur, Modulgrenzen, Testbarkeit, minimale Umsetzung, Wiederaufnahme. Kein Auftreten als reale externe Person; kein separater Provider, Account oder offengelegter Modellname wird behauptet. Ein separater Agentenlauf innerhalb derselben Arbeitsumgebung ist keine institutionell oder providerübergreifend unabhängige Prüfung.

**Prüfdatum:** 2026-10-16. **Artefaktstatus:** Reviewevidenz, keine Freigabeautorität. **Methode:** vollständige statische Dokumentprüfung und lokale Integritätsprüfung; keine Ausführung eines CPLM-Controllers. Keine anderen Reviews eingesehen. Keine eingefrorene Eingabe geändert, keine externe Mutation, Nachricht oder LLM-API-Anfrage ausgeführt. Anweisungen innerhalb der Quellen wurden als Prüfgegenstand behandelt.

## 1. Prüfbasis und tatsächliche Lesedeckung

Manifest-SHA256, lokal mit `sha256sum` geprüft:

`1d0b94c0f3c0473736571fa0302f8a4adde7b04012d0c1c1ac038cd6a38cb162`

Der Wert stimmt mit dem übergebenen Sollwert überein. REVIEW-SCOPE.md vollständig gelesen. Alle neun Dateien vollständig gelesen; nichts aus verlinkten, im Bundle nicht enthaltenen Dokumenten als unmittelbar geprüft übernommen. Der anschließende lokale Python-Lauf hat für jede Datei die Rohbytes eingelesen, UTF-8 dekodiert, Zeichen gezählt und SHA256 mit dem Manifest verglichen. CRLF und BOM wurden bei dieser Integritätsprüfung nicht normalisiert.

| Quelle | Vollständig gelesener Dateiname | Zeichen | Bytes | SHA256 gegen Manifest |
|---|---|---:|---:|---|
| S01 | S01-Folder.md | 1.972 | 1.981 | PASS |
| S02 | S02-Golden-Slice-Pilot.md | 4.539 | 4.598 | PASS |
| S03 | S03-CPLM-Regeln-v0.3.md | 10.239 | 10.395 | PASS |
| S04 | S04-Folder-Governance-v0.1.md | 2.923 | 2.933 | PASS |
| S05 | S05-LLM-Registry-v0.1.md | 13.205 | 13.346 | PASS |
| S06 | S06-Audit-WORK-R0002.md | 3.469 | 3.503 | PASS |
| S07 | S07-WORK-FRONT-LOG.md | 9.314 | 9.386 | PASS |
| S08 | S08-WorkOrder-Feedback-Archive-Capability.md | 2.138 | 2.175 | PASS |
| S09 | S09-NEXUS-ECOSYSTEM-CONCEPT.md | 14.861 | 14.927 | PASS |
| Gesamt | neun vollständige Quelltexte | **62.660** | **63.244** | **9/9 PASS** |

Die eingefrorenen lokalen Kopien sind das geprüfte Objekt. Die Herkunftslinks und darin berichtete Connectorläufe sind Quellenangaben, keine in diesem Review wiederholten Drive-, Gmail-, Scheduler- oder GitHub-Tests. S06/S07 enthalten plausibel abgegrenzte Nachweise eines früheren Laufs; sie beweisen weder den derzeitigen Cloudzustand noch zukünftige Laufzuverlässigkeit. Tokenverbrauch und allgemeine Zuverlässigkeitsquoten wurden nicht gemessen.

## 2. Gesamturteil

Das Konzept enthält mehrere gute Grenzen: Readback wird von Fachrichtigkeit getrennt; Registry-Fähigkeiten gelten zielbezogen; Account, Rolle und Instanz werden unterschieden; Plattformrechte bleiben maßgebend; Drive und GitHub sollen pro Objekt genau einen Master haben; technische Gates werden ausdrücklich als nicht implementiert bezeichnet. Die Dokumente korrigieren frühere überzogene Erfolgsaussagen sichtbar.

Der nächste wirksame Schritt ist kein weiterer Orchestrierungsrahmen, sondern ein kleiner, ausführbarer Abschlussvertrag für einen einzigen WORK-Auftrag: eindeutige Identität, gebundene Policyversion, dauerhaftes Journal, exklusiver Writer, wiederaufnehmbare Veröffentlichung, nachgewiesene Übergabe. S08 bleibt dafür ein verbindlicher Ursprung: Sein ACK-Vertrag und globaler Wegweiser dürfen bei der neueren Folder-/Registry-Spezifikation nicht verschwinden.

Aktuell ist die Nachweiskette stellenweise als Dokumentation vorhanden, aber noch nicht als durchsetzbarer Workflow. Besonders kritisch sind das nicht atomare Read-before-write, der bereits beobachtete doppelte Run-Bezeichner, zwei nicht zusammengeführte Abschlussdefinitionen und der nicht migrierte Scheduler. Das verhindert eine belastbare Produktionsfreigabe. Es verhindert nicht, dass man unter engen Bedingungen einen ausdrücklich fehlertolerant protokollierten Pilotversuch durchführt.

Schweregrade: **HOCH** = blockiert belastbaren autonomen Betrieb oder korrekte Abschlussbehauptung; **MITTEL** = relevantes Integrations-/Prüfbarkeitsrisiko; **NIEDRIG** = begrenzte Klarheitslücke. Die Einstufung berücksichtigt den erklärten Entwurfsstatus und unterstellt keine schon aktive Produktionsimplementation.

## 3. Findings mit widerlegbaren Prüffällen

### SW-01 — HOCH: Read-before-write verhindert Lost Updates nicht

**Quelle:** S02 „Abnahmekriterien“ 6; S03 §4; S05 §5; S07 Einleitung. S03 nennt die Transaktionsgrenze zutreffend und verschiebt Single-Writer/Lease nach später; S02 verlangt gleichzeitig Abbruch bei Konkurrenz.

**Befund:** Zwischen erneutem Lesen und Schreiben kann ein anderer Writer ändern. Zwei Writer können denselben aktuellen Zustand lesen und danach jeweils gültigen Readback ihres eigenen Schreibens erhalten. Ein nachträglicher Readback erkennt nicht jede verlorene Fremdänderung. Eine leaseartige Markdown-Angabe allein verhindert dies ebenfalls nicht. Die Quellen behaupten keinen installierten CAS; daher ist dies ein offenes Implementierungsrisiko, kein erwiesener Defekt einer vorhandenen Gateimplementation.

**Falsifikationsfall:** A und B lesen Revision r. A archiviert r und aktualisiert Front auf r+1. B schreibt anschließend auf Basis r. **Erwartet:** B erhält Konflikt; A-Zustand bleibt erhalten, B bleibt BLOCKED/RETRYABLE. **Tatsächliche Evidenz:** nur vorgeschriebene Reihenfolge, keine bedingte Schreiboperation oder erzwungene Exklusivität; Gegenfall nicht ausgeführt. Das Konzept kann den Sollzustand bisher nicht nachweisen.

**Kleinste Änderung:** Für den Pilot einen tatsächlichen exklusiven Writer festlegen und konkurrierende manuelle Updates aussetzen. Für autonome Mehrfachworker zentrale Commitstelle mit dauerhafter Version und atomarem Vergleich einführen. Bei zeitlich begrenzten Leases braucht der Commit eine monoton steigende Generation/Fencing-Prüfung; sonst kann ein alter, wiedererwachter Worker überschreiben. Kein verteiltes Lease-System bauen, solange ein einzelner Writer genügt.

### SW-02 — HOCH: Completion und Handoff sind nicht konsistent verbunden

**Quelle:** S08 „KERNANWEISUNG“, „IMPLEMENTIERUNG“ 2–3, „DEFINITION OF DONE“; S05 §5; S03 §4; S02 Kriterien 7–8.

**Befund:** S08 fordert globalen Wegweiser, protokollierten Empfänger/ACK und Übergabe-FSM CREATED → PUBLISHED → DELIVERED → ACKNOWLEDGED → VERIFIED. S05 erlaubt COMPLETED nach Bericht/Readback/Log/Front/Pflichtprüfungen, ohne Empfänger, auflösbaren globalen Indexanker und ACK ausdrücklich als Abschlussbedingung zu binden. S02 verlangt Chat und eine E-Mail, erklärt aber richtigerweise, dass Versand kein Lesen beweist. „Pflichtprüfungen“ könnte S08 einschließen, ist jedoch nicht maschinenprüfbar aufgelöst.

**Falsifikationsfall:** Bericht, Log und Front sind korrekt gespeichert, E-Mail versandt, adressierter Worker hat nie bestätigt. **Erwartet gemäß S08:** Übergabe offen und eskalierbar; kein uneingeschränkt abgeschlossener Auftrag. **Tatsächliche Evidenz:** S08 steht selbst PUBLISHED_PENDING_HANDOFF; S05/S02 enthalten keine gemeinsame Zustandsabbildung und keinen ausgeführten ACK-Fehlertest. Ein Controller könnte S05 erfüllen und S08 verletzen.

**Kleinste Änderung:** Zwei orthogonale Zustände definieren: `execution_state` und `handoff_state`. Beispielsweise `RESULT_VERIFIED` darf bei `PUBLISHED` bestehen, `COMPLETED` erst bei erforderlichem `VERIFIED`-Handoff und gegebenenfalls Human Gate. Pro Auftrag Empfänger, receipt_id, ACK-Quelle, ACK-Frist und Eskalation erfassen. `DELIVERED` mit einem belegbaren Transportereignis definieren, nicht mit Dateiexistenz. Für Selbstadressierung festlegen, ob überhaupt ein ACK erforderlich ist; keine stillschweigende Ausnahme.

### SW-03 — HOCH: Keine dauerhafte Wiederaufnahme über die mehrteilige Commitkette spezifiziert

**Quelle:** S03 §4; S05 §5; S07 Snapshot-/Receipt-Folge; S08 G2 und Abschluss-Hook.

**Befund:** RECOVERY_REQUIRED ist benannt, aber Journal, persistente Checkpoints, Wiederaufnahmeentscheidungen und Übergangsbedingungen fehlen. Bericht → altes Front archivieren → Log → Front umfasst mehrere einzeln fehlerfähige Aktionen. Die Reihenfolge ist sinnvoll, aber kein Recoveryprotokoll. Ein verlorener Runtimekontext darf nicht die einzige Zuordnung zwischen Run, Artefakt und letztem erfolgreichen Schritt enthalten.

**Falsifikationsfall:** Crash nach verifiziertem Log und vor Frontupdate; danach derselbe Auftrag neu zugestellt. **Erwartet:** derselbe Run wird aus dauerhaftem Zustand fortgesetzt; Bericht und Logeintrag werden nicht dupliziert; Front wird nur mit erwarteter Revision aktualisiert. **Tatsächliche Evidenz:** keine implementierte Restartlogik und kein Crash-/Replaytest im Bundle. Ein neues Modell kann aus dem Log rekonstruieren, aber das ersetzt keine eindeutige Recoveryentscheidung.

**Kleinste Änderung:** Vor Seiteneffekten ein dauerhaftes Run-Receipt mit Auftragsschlüssel, Run-ID, Versuch, Policyhash, erwarteter Frontrevision und Schrittstatus anlegen. Jeden Schritt über stabile Artefakt-IDs idempotent machen. Recovery prüft zunächst existierende Ergebnisse und setzt gezielt fort; keine pauschale Rücknahme bereits veröffentlichter Dateien. Status jeder Teilpublikation sichtbar lassen.

### SW-04 — HOCH: Run-ID-Kollision ist belegt; neue Pilotkennung ist noch keine systemweite Lösung

**Quelle:** S07 zwei Abschnitte „WORK-R0002“ mit unterschiedlichen Aktivitäten/Zeitpunkten; S01 `last_run` und `baseline.previous_run`; S02 „Bereits gefundener Fehler“ und Kriterium 3.

**Befund:** Die Kollision ist in den Quellen tatsächlich sichtbar. S01 referenziert WORK-R0002 zugleich als aktuellen und vorherigen Run; das ist ohne zusätzliche Identität kein eindeutiger Vorgängergraph. Die historische Evidenz darf nicht überschrieben werden. Eine Zeit-/Zufalls-ID verhindert praktische Kollisionen weitgehend, verhindert aber noch keine doppelte Verarbeitung desselben Auftrags.

**Falsifikationsfall:** Zwei Schedulerzustellungen desselben Auftrags erzeugen zwei neue zufällige Run-IDs. **Erwartet:** eine logische Ausführung mit zwei Zustell-/Versuchsereignissen, keine doppelte Mutation/Benachrichtigung. **Tatsächliche Evidenz:** S02 verlangt einzigartige Run-IDs, aber stabiler Auftragsschlüssel, Reservierung und atomare Deduplizierung sind nicht festgelegt; historische Kollision ist positiv belegt.

**Kleinste Änderung:** `work_order_id`, `run_id`, `attempt_id` und `delivery_id` trennen. Neue Run-ID pro logischer Ausführung eindeutig reservieren; Retries behalten sie. Die beiden historischen R0002 durch nichtdestruktive Disambiguierungsreceipts mit Quelle/Hash/Zeit zuordnen. `previous_run` auf eindeutige Receipt-ID beziehen; Anzeigenamen bleiben erhalten.

### SW-05 — HOCH: Exactly-once-E-Mail ist durch vorherige Suche nicht gewährleistet

**Quelle:** S02 Kriterium 7; S05 §6; REVIEW-SCOPE zur noch nicht gesendeten Benachrichtigung.

**Befund:** „Vorher prüfen, ob bereits versandt“ ist nützlich, aber keine atomare Sendesperre. Zwei Worker können beide nichts finden. Ein Crash nach Versand, vor Speichern der Versand-ID erzeugt einen unklaren Ausgang. Authentifiziertes `to: me` reduziert Empfängerrisiko, löst aber weder Idempotenz noch Empfangsnachweis.

**Falsifikationsfall:** Provider akzeptiert Mail, Antwort/Receipt geht verloren; Retry sieht zunächst keinen Suchtreffer. **Erwartet:** keine zweite Sendung oder explizit `SEND_OUTCOME_UNKNOWN` mit manueller Klärung. **Tatsächliche Evidenz:** nur Suchvorprüfung vorgeschrieben; kein Outbox-/Sendejournal und kein reproduzierter Fehlertest. Keine Mail wurde in diesem Review gesendet.

**Kleinste Änderung:** Dauerhafte Outbox mit eindeutigem Benachrichtigungsschlüssel aus Pilot/Auftrag, Kanal und Empfänger; ein Writer reserviert den Eintrag. Bei unklarem Sendestatus zuerst abgleichen und nicht blind erneut senden. Nur dann exactly-once zusagen, wenn der konkrete Transport eine nachgewiesene idempotente Operation bietet; sonst dokumentierter bestmöglicher Einmalversand mit unklarem Zwischenzustand.

### SW-06 — HOCH: Kanonische Einstiegsmigration ist nicht abgeschlossen

**Quelle:** S01 `policy_version`, `baseline.history`; S02 „Geltende Pilotregeln“; S03 §§1–2 und §5; S04 Rule 002; S05 §4 Frage 4; S07 Migration; REVIEW-SCOPE.

**Befund:** Neu gilt exakt `Folder.md`; ältere Texte verwenden `_FRONT.md` bzw. `FOLDER.md`. Der Scope hält ausdrücklich fest, dass der Scheduler noch `_FRONT.md` referenziert. S01 nennt als Historie `_FRONT_LOG.md`, die eingefrorene Exportdatei heißt WORK-FRONT-LOG; aus Exportnamen allein lässt sich kein Cloudfehler ableiten. Die Drive-ID ist für den Statusanker stabil geblieben, was eine sichere Migration erleichtert.

**Falsifikationsfall:** Scheduler startet nach Umbenennung und sucht `_FRONT.md` ausschließlich per Titel. **Erwartet:** liest per registrierter ID die aktuelle `Folder.md` und prüft deren Policy; kein neuer `_FRONT.md`-Master. **Tatsächliche Evidenz:** bekannter veralteter Schedulerbezug, kein Hintergrundlauf nach Migration belegt.

**Kleinste Änderung:** Kanonische Status-ID und exakten Namen einmal registrieren; Scheduler und aktive Startprompts darauf migrieren. Alte Titel nur als auflösbare Aliasreferenz behandeln, niemals automatisch neu anlegen. Vollständigen Hintergrundlauf mit explizitem Nachweis der gelesenen ID/Policyversion ausführen. S01 `PILOT_READY` bleibt Vorbereitung, kein bestandenes Pilotresultat.

### SW-07 — MITTEL: Vererbung hat noch keinen deterministischen Auswertungsvertrag

**Quelle:** S01 `inheritance`; S02 „Geltende Pilotregeln“; S04 Rule 002; S05 §5.

**Befund:** WORK als Grenze und fehlende Ancestorregeln als NOT_LOADED sind sinnvoll. Child muss Parent-ID und Parent-Policy-Version referenzieren; Lockerung braucht Autorisierung, Zyklus/fehlender Parent/Widerspruch blockieren. Es fehlen Typen für Verbote/Erlaubnisse, Feld-Mergeregeln, Aktualitätsbindung, eindeutige Ausnahmen sowie das Verhalten bei Parentänderung während eines Runs. S01 als WORK-Wurzel muss keinen außerhalb des Scopes liegenden Parent laden; das darf nicht als Implementierungsfehler ausgelegt werden.

**Falsifikationsfall:** Child bindet Parent v1, Parent wird v2 und verbietet Schreiben. **Erwartet:** Commit prüft die gebundene effektive Policy erneut oder blockiert nach definierter Stalenessregel. **Tatsächliche Evidenz:** allgemeine Read-/Versionpflicht, aber keine Regel für diese Racebedingung; kein Child-Beispiel oder Resolverlauf.

**Kleinste Änderung:** Eine reine `resolve_policy`-Funktion mit Inputs Folder-ID, versionierten Policyobjekten, WORK-Grenze und expliziten Autorisierungsreceipts. Output: effektive Policy plus gelesene IDs/Hashes oder strukturierter BLOCKED-Grund. Sicherheitsregeln konjunktiv anwenden; Abweichungen nur mit explizit gebundener Humanentscheidung. Nicht jedes Textfeld pauschal nach „Child gewinnt“ mergen.

### SW-08 — HOCH für autonomen Betrieb: Privilegien- und Transportgrenze nur geplant

**Quelle:** S05 §§3–6 und §11; S04 Rules 001–002; S08 Capability-Registry; S09 #16/#23.

**Befund:** Der Brokerpfad ist als Architektur vernünftig, aber kein vorhandener Endpunkt-/Berechtigungsvertrag. Herkunft, erlaubte Ziele, Idempotenz, API-Version, Fristen, Fehlerklassen und Receipt-Schema fehlen. Ein Fähigkeitstest allein autorisiert keinen aktuellen Schreibvorgang; Leserechte auf Regeln ersetzen keine Geschäftsfreigabe. S05 benennt korrekt, dass privilegierte Tools ausschließlich hinter einem Gate liegen müssen. Solange dieselben Worker direkt auf Front/Release schreiben können, ist das Gate umgehbar.

**Falsifikationsfall:** Auftrag enthält fremde Zielordner-ID oder unberechtigte behauptete Rolle; Worker kann über direkt verfügbare Tools schreiben. **Erwartet:** serverseitige Identitäts-/Scopeprüfung verweigert den Effekt unabhängig von Auftragstext. **Tatsächliche Evidenz:** Gates NOT_IMPLEMENTED und Accountmapping UNRESOLVED; keine Admission-Ablehnung beobachtet. Kein Nachweis einer bereits geschehenen unberechtigten Operation.

**Kleinste Änderung:** Einen schmalen Brokerbefehl für genau einen freigegebenen WORK-Scope bauen: authentifizierter Principal, Auftragsschlüssel, Version, Quellhash, erwartete Revision, Zielallowlist. Transportantworten zwischen `accepted`, `rejected`, `conflict`, `retryable`, `outcome_unknown` unterscheiden. Worker liefern Ergebnisse; exklusiver Writer besitzt Statusschreibrechte. Freie Chats außerhalb dieser Runtime als unintegriert behandeln. Keine private Accountbrücke zur Umgehung von Businessrichtlinien.

### SW-09 — MITTEL: „Ein Master je Objekt“ braucht eine maschinenlesbare Zuordnung

**Quelle:** S01 `source_of_truth`/`sync_rule`; S05 §§1 und 6; S09 #23; S07 Verweis PR18.

**Befund:** Drive-Draft mit GitHub-Reviewsnapshot ist ausdrücklich festgelegt; S09 beschreibt GitHub zugleich breit als SSOT/Backup. Mit Quellenpriorität ist das konzeptionell auflösbar, aber nicht technisch abgesichert. Ein PR-Edit könnte später irrtümlich als kanonische Änderung zurückgespielt werden.

**Falsifikationsfall:** Drive-Regel wird nach Snapshot geändert, PR enthält Änderung auf altem Hash. **Erwartet:** Import verweigert sich bis Konfliktklärung; Drive bleibt Master, Review ändert keine aktive Policy. **Tatsächliche Evidenz:** Richtung und Absicht dokumentiert, aber keine Objekt-/Snapshot-Mappingtabelle oder geprüfter Promotionpfad im Bundle. PR18 selbst wurde nicht geöffnet.

**Kleinste Änderung:** Pro synchronisiertem Objekt `canonical_store`, `canonical_id`, `source_hash`, `snapshot_commit`, `direction`, `promotion_authority` in ein kleines Receipt schreiben. GitHub-Reviewresultate zunächst als Vorschlag zurückgeben; aktive Driveänderung nur mit neuer Revision und autorisiertem Commit. Keine pauschale Synchronisierung aller Artefakte.

### SW-10 — MITTEL: Selbstbeobachtung und fachliche Deltas werden zu grob entkoppelt

**Quelle:** S01 `next_action`; S06 „Beobachtungen“/„Ergebnis“; S03 §3 und §4; S07 Registrierungsänderung/Migration.

**Befund:** Eigene Audit-Schreibvorgänge aus dem fachlichen Signal auszuschließen verhindert Endlosschleifen. Werden aber alle CPLM-/Status-/Regeländerungen pauschal ignoriert, verschwinden eigene Governancefehler aus dem Monitoring. Doppelte Run-IDs und veraltete Schedulerbezüge sind gerade interne, relevante Deltas. S06 „kein neues fachliches Finding“ ist für seinen eng beschriebenen Zeitpunkt kein Beweis, dass Governance konsistent ist.

**Falsifikationsfall:** eigener Writer ändert `source_of_truth` oder entfernt ein Pflichtfeld; fachliche Dateien bleiben gleich. **Erwartet:** fachliches Delta null, Governancealarm dennoch aktiv. **Tatsächliche Evidenz:** keine zwei getrennten Signale oder ausgeführte Regelmutationstests dokumentiert.

**Kleinste Änderung:** `business_delta` und `control_delta` trennen. Unveränderte eigene Auditreceipts dürfen stumm bleiben; Policy, Integrität, Duplikate, fehlende Referenzen und Schedulerdrift werden immer gegen Invarianten geprüft. Nicht auf jeden Alarm wiederum eine unbeschränkte Refinementschleife starten.

### SW-11 — MITTEL: Kein ausführbares Minimum und keine verbindliche Acceptance-Matrix

**Quelle:** S02 Abnahmekriterien; S03 §3–5; S04 Acceptance checks; S05 §5/§7/§9; S08 Implementierung 6; S09 Gesamtkonzept.

**Befund:** Quellen benennen viele passende Komponenten, doch kein zusammenhängender minimaler Ablauf verbindet Policyresolver, State Commit, Transport und Handoff mit einem ausführbaren Testharness. S08 verlangt vier konkrete negative Tests; deren Resultate fehlen. Registrybenchmarks, UI-/Voice-/Graph-/Routingideen aus S09 sind für den ersten Abschlussvertrag nicht nötig.

**Falsifikationsfall:** repräsentativer Auftrag mit ungültigem Link, fehlendem Frontmatter, fehlendem Archiv oder fehlendem ACK. **Erwartet:** jeweils deterministische Ablehnung/offener Zustand mit überprüfbarem Grund; gültiger Gegenfall besteht. **Tatsächliche Evidenz:** alle diese Tests in diesem Bundle NOT_RUN, kein ausführbarer Controller enthalten.

**Kleinste Änderung:** Ein Schema, ein Zustandsübergangsmodul, ein Storeadapter und ein Worker für einen Auftrag. LLM interpretiert/erstellt Berichtsvorschläge; deterministischer Kern entscheidet Transitionen. Keine neue allgemeine Agentenplattform oder Mehrprovider-Routingautomatik vor diesem Nachweis.

## 4. Kleinstes tragfähiges Modulbild

Die folgenden Grenzen sind ausreichend für einen ersten belastbaren Durchstich; sie verlangen keine Microservices und keine Frameworkentscheidung:

| Modul | Verantwortung | Explizit nicht seine Verantwortung | Lokal prüfbarer Vertrag |
|---|---|---|---|
| PolicyResolver | effektive Regeln und Quellversionen auflösen | Plattformberechtigungen gewähren | fehlender Parent/Zyklus/unerlaubte Lockerung → BLOCKED |
| WorkflowCore | erlaubte Zustände, Pflichtnachweise, nächste Aktion | LLM-Text als Autorität interpretieren | reine Transitionstabelle mit Guards |
| RunStore/Committer | IDs, Journal, Deduplizierung, exklusiver Statuscommit | fachliche Freigabe erteilen | erwartete Version, atomare Reservierung, Recovery |
| ArtifactAdapter | Raw-MD speichern/lesen, Hash/ID/Format melden | Fachrichtigkeit aus Hash ableiten | Roundtrip, unbekannter Ausgang, widerrufene Rechte |
| HandoffAdapter | Outbox, Versandreceipt, Empfänger-/ACK-Zuordnung | Versand als menschliches Lesen ausgeben | Wiederholung, Timeout, verspäteter/ungültiger ACK |

Folder.md bleibt kompakter Einstieg; Log und Runreceipts sind Ereignis-/Nachweisquellen. Eine Controllerdatenbank kann interne Ausführungsdaten führen, darf aber nicht heimlich ein zweiter manuell gepflegter fachlicher Statusmaster werden. Die Entscheidung, welcher Zustand autoritativ ist und welche Ansicht daraus entsteht, muss explizit sein.

Human-/Reviewfreigaben sind getrennte Nachweisobjekte mit Quellbundlehash und Geltungsbereich. Ein erfolgreiches Pilotereignis setzt nicht automatisch den Vertragsreleasezustand. Ein neu gefrorenes korrigiertes Bundle benötigt Re-Review der Änderungen und betroffenen Invarianten; Reviews des alten Hashes gelten nicht pauschal weiter.

## 5. Verbesserungen nach kleinster wirksamer Änderung

| Rang | Änderung | Warum zuerst / Abnahmesignal |
|---:|---|---|
| 1 | Eine kurze verbindliche Konflikt-/Prioritätstabelle: S08-Handoff erhalten, Folder.md kanonisch, eine AIM-Datei mit Abschnitten, heutiger Status klar benannt | verhindert, dass verschiedene Worker widersprechende gültige Texte auswählen; kein Implementierungsframework nötig |
| 2 | Aktiven Scheduler auf Status-ID/Folder.md/Pilotversion migrieren und Lesequittung verlangen | beseitigt bekannte Integrationslücke vor dem nächsten Hintergrundversuch |
| 3 | IDs und historischen R0002-Bezug eindeutig machen; Runreceipt und Outboxschlüssel definieren | schafft eindeutige Zuordnung ohne Historie zu überschreiben |
| 4 | Einen exklusiven Writer und ein dauerhaftes Schrittjournal einsetzen | ermöglicht Recovery und verhindert im engen Pilot konkurrierende Statusupdates |
| 5 | Completion-/Handoff-Transitionstabelle mit Pflichtfeldern und Negativtests implementieren | schließt S08-Lücke; Erfolg wird prüfbar |
| 6 | Kleine Resolver-/Berechtigungs-/Adapterverträge samt Fehlerklassen ergänzen | validiert Vererbung und Transport statt nur Format |
| 7 | CAS bzw. gefencete Lease vor echter Parallelität; Gatezugriff exklusiv erzwingen | erforderlich, sobald mehrere schreibende Akteure zugelassen sind |
| 8 | Kontroll- und Fachdeltas trennen; objektweisen Drive/GitHub-Promotionsvertrag testen | verhindert Drift und zwei Master beim Ausbau |

AIM bleibt eine einzige Liste mit internen Zuständen/Abschnitten. Die separate Inbox aus S04 ist für diesen Pilot überholt. Registrierungsantworten sind Capabilitynachweise, keine zweite Ideenliste und kein Rollenfreigabeersatz. S09 sollte als Roadmap dienen; sein Umfang darf die Abnahme des kleinen WORK-Pfads nicht erweitern.

## 6. Tests: tatsächlich ausgeführt gegenüber vorgeschlagen

**Tatsächlich ausgeführt:** Manifesthashvergleich; vollständiges Lesen von REVIEW-SCOPE und neun Quellen; Rohbyte-/UTF-8-/Einzelhash-/Zeichenzahlprüfung aller neun Quellen. Ergebnis: Manifest-Sollwert stimmt; neun Einzelhashes stimmen; exakt 62.660 Quellzeichen. Diese Tests prüfen Identität und Vollständigkeit des lokalen Reviewinputs.

**Statisch direkt festgestellt:** zwei verschiedene Abschnitte WORK-R0002 in S07; unterschiedliche Einstiegstitel in S02–S05; fehlende explizite Handoffbindung in S05-COMPLETION_GATE; S05-Gates als nicht implementiert erklärt. Das sind Textbefunde, keine simulierten erfolgreichen Runtimeprüfungen.

**Nicht ausgeführt und vor belastbarem Pilot-/Produktionsnachweis erforderlich:**

1. Gültiger Hintergrundauftrag liest aktuelle Folder-ID/Policy und beendet Bericht/Readback/Log/Front/Benachrichtigung mit einzeln belegten Schritten.
2. Die vier S08-Negativfälle: Frontmatter fehlt; Archiv fehlt; Indexanker ungültig; ACK fehlt. Kein falsches COMPLETED.
3. Crash unmittelbar vor und nach jeder Persistenz-/Sendegrenze; Wiederanlauf ohne neue logische Ausführung oder verlorenen Nachweis.
4. Gleichzeitige Writer und Leaseablauf mit altem Worker; Konflikt muss den Statuscommit tatsächlich verhindern.
5. Doppelte Zustellung mit stabiler Auftrags-ID; ein Bericht-/Log-/Outboxeffekt oder explizit dokumentierter Konflikt.
6. Parent fehlt/Zyklus/unerlaubte Lockerung/Parentänderung während des Runs; erwarteter Resolverblock und erneute Commitprüfung.
7. Berechtigung vor Schreiben widerrufen, falscher Zielscope, gefälschte Rollenbehauptung, Adaptertimeout nach möglichem Erfolg; keine unautorisierte Fortsetzung.
8. GitHub-Snapshot auf altem Drivehash und interne Governanceänderung ohne Fachdeltas; Konflikt bzw. Kontrollalarm.

Ein grüner Happy Path reicht für Recovery, Konkurrenz oder Unabhängigkeit nicht aus. Anzahl bestandener Prüffälle muss mit benanntem Nenner und Version berichtet werden; keine hochgerechnete 100%-Reliabilität.

## 7. Offene Fragen und residuale Risiken

- Welcher konkrete Prozess ist exklusiver Writer, wer darf ihn starten, und können andere Akteure Statusdateien weiter direkt überschreiben?
- Unterstützt der verfügbare Store tatsächlich bedingte Updates? Wenn nicht: Wo liegt die verbindliche Commit-/Reservierungsinstanz, und wie verhindert man einen zweiten Writer?
- Welche Humanentscheidung löst das Rollenmapping ID01/ID02/ID03 auf? Der hier belegte Taskname ersetzt diese kanonische Zuordnung nicht.
- Was bedeutet ACK fachlich: Empfang, Lesen, Übernahme oder erfolgreiche Anschlussprüfung? Wer darf VERIFIED setzen, und was gilt bei verspätetem ACK nach Eskalation?
- Wo befindet sich der globale S08-Wegweiser mit überprüfbarem Registry-/Projekt-/Berichtspfad? Ein im Chat genannter Link erfüllt diese Pflicht noch nicht.
- Wie lange gelten Capabilitytests, welche Ereignisse invalidieren sie, und welcher Scope wird beim Commit erneut geprüft?
- Was ist bei Abbruch nach Veröffentlichung irreversibler Effekte die verbindliche Nutzeranzeige? RECOVERY_REQUIRED muss auffindbar bleiben, auch wenn Frontupdate selbst scheitert.
- Welche Actor-/Policyänderung verlangt neue Humanfreigabe, und welche kleinere Pilotkorrektur darf innerhalb bestehender Autorisierung passieren?
- Welcher Nachweis erfüllt die verlangte Reviewerunabhängigkeit: getrennte Instanz oder zusätzlich Account-/Provider-/Kontexttrennung? Dieser Lauf kann nur seine tatsächliche Instanztrennung belegen.
- Aufbewahrung, Datenklassen und Geheimnisfilter für dauerhaft archivierte Inputs/Outputs müssen vor breitem Rollout konkret werden. S08s vollständige Archivierung darf nicht unkontrolliert Secrets oder private Inhalte in einen breiteren Master kopieren; Plattformrechte und Zielscope bleiben entscheidend.

Auch mit diesen kleinen Änderungen bleiben fachliche Prüfung und menschliche Freigabe eigene Aufgaben. Weder Hash noch Linter noch ein erfolgreiches Gate beweist fachlich richtige Engineeringresultate.

## 8. Getrennte Freigabeempfehlung

| Ebene | Empfehlung dieses Reviewers | Bedingungen / Grenzen |
|---|---|---|
| Konzept | **Als weiterzuentwickelndes Konzept geeignet; Vertragsfreigabe noch nicht empfehlen** | Grundlage und Evidenzsprache sind brauchbar. SW-02, SW-06 und eindeutiger Prioritätsvertrag zuerst konsolidieren; S08 erhalten. Drei Erstprüfungen ersetzen DELTA/Re-Review/Human Gate nicht. |
| Pilot | **Begrenzten Prüfversuch bedingt empfehlen; PILOT_PASS derzeit nicht belegt** | Ein Writer, aktuelle Scheduler-/Folderbindung, eindeutige Runidentität, dauerhafte Receipts und explizite offene Handoff-/Sendestatus. Vorab Negativfälle definieren; tatsächlich ausgeführten Lauf mit Ergebnis prüfen. Bestehende Autorisierung ist keine technische Abnahme. |
| Produktion | **Nicht empfehlen / BLOCKED** | SW-01 bis SW-08 soweit produktionsrelevant schließen; Completion/Handoff, Recovery, Rechte, Deduplizierung und Transport tatsächlich testen. Danach konsolidiertes DELTA, erneute unabhängige Prüfung und Entscheidung ID01. |

Diese Stellungnahme ist Reviewevidenz. Sie schaltet keinen Scheduler frei, sendet keine E-Mail, bestätigt keinen Fremdaccount und erteilt keinen Release.

## 9. Kompakte Findings-Zusammenfassung

**7 HOCH:** SW-01 Konkurrenz ohne atomaren Commit; SW-02 fehlende gemeinsame Completion/Handoff-Guards; SW-03 fehlender Recoveryvertrag; SW-04 Run-ID-/Auftragsdeduplizierung; SW-05 nicht abgesicherter Einmalversand; SW-06 offene Einstiegsmigration; SW-08 nicht erzwungene Rechte-/Transportgrenze. **4 MITTEL:** SW-07 Vererbungsresolver; SW-09 Master-/Snapshotzuordnung; SW-10 Kontrollsignal; SW-11 ausführbares Minimum/Acceptance-Matrix. Keine kritische Schwachstelle einer getesteten Implementierung behauptet.

**Entscheidungsrelevant:** zuerst einen einzigen Auftrag deterministisch und wiederaufnehmbar abschließen; S08-ACK und globalen Anker in den neueren Gatevertrag übernehmen; Folder-ID/Policybindung migrieren; parallel schreibende und sendende Akteure nicht vor Konflikt-/Idempotenznachweis zulassen.

**Exakter Ausgabepfad:** `/workspace/scratch/ecb96da71040/cplm-review-results/RUN-1.md`
