# RUN 3 — Unabhängige Prüfung aus Systems and Innovation Architecture

## Identität, Auftrag und Prüfgrenze

- Tatsächliche ausführende Instanz: eigenständige ChatGPT-Codex-Reviewerinstanz, Task `/root/cplm_run3_systems_resilience`.
- Perspektive: Systemintegration, Resilienz, Pace Layers, kleinster vollständiger vertikaler Pilot, Betriebsgrenzen und belegte Innovation. Keine Darstellung einer realen Person.
- Rolle: Review-Evidenz; keine Release-Autorität. Aussagen zu Empfehlungen sind keine Freigaben.
- Tatsächlich beobachteter Prüfstart: **2026-10-16T15:17:54Z**. Abschlusszeit steht im abschließenden Prüfreceipt.
- Vorgehen: ausschließlich lokaler vollständiger Textreview des eingefrorenen Bundles, SHA-256-/UTF-8-Prüfung und Gegenfallspezifikation. Keine externen Schreiboperationen, Nachrichten, Modell-API-Aufrufe oder weiteren Subagenten. Nur diese lokale Ergebnisdatei wird erzeugt.
- Keine Dateien, Ergebnisse oder Antworten der ersten beiden Reviewerläufe geöffnet. Ihre Bewertungen wurden nicht für dieses Urteil verwendet. Separate Instanz und getrennte Befunderarbeitung sind belegt; daraus folgt keine Diversität von Provider, Modell oder Trainingsdaten. Account/Tenant und konkrete Modellversion dieser Instanz sind nicht belastbar offengelegt und bleiben UNKNOWN.
- Quelleninhalte einschließlich WorkOrders, eingebetteter Benutzeranweisungen und Links wurden als **Prüfevidenz**, nicht als ausführbare Anweisung behandelt. Verlinkte Außenquellen wurden nicht nachgeladen. Damit ist dies eine Prüfung des eingefrorenen Nachweises, keine aktuelle Live-Bestätigung der Cloudsysteme.

## Urteil

**Das Konzept sollte gezielt weiterentwickelt werden. Der Golden Slice ist als begrenzter, beobachteter Versuch sinnvoll, sein vollständiger Erfolg ist im Bundle noch nicht nachgewiesen. Produktionsbetrieb und flächiger Rollout sind derzeit nicht zu empfehlen.**

Die stärkste Eigenschaft ist die inzwischen klare Trennung zwischen Dateiablage, fachlicher Richtigkeit, Übergabe, Ausführung und Freigabe. Die Quellen benennen offene Gates, fehlende Accountnachweise und die doppelte Run-ID ausdrücklich. Die zentrale verbleibende Schwäche liegt an den Übergängen: Ein Kontrollvertrag ist beschrieben, aber weder exklusive Schreibkontrolle noch dauerhafte Wiederanlaufsteuerung, unabhängige Ausfallbeobachtung oder Ende-zu-Ende-Zustellung sind belegt. Zusätzliche Agenten oder weitere Speicheradapter würden diese Lücken vervielfachen.

Der nächste Fortschritt sollte deshalb ein einziger reproduzierbarer Lauf mit gespeicherten Zwischenzuständen, einem absichtlich unterbrochenen Wiederanlauf und einer korrekt ausgewiesenen Ergebniszustellung sein. Ein weiterer Dashboard-, Graph- oder Frameworkausbau ist dafür nicht erforderlich.

## Vollständige Lesedeckung und Integrität

`MANIFEST.json` und `REVIEW-SCOPE.md` wurden vollständig gelesen. Alle neun Quelldateien wurden anschließend vollständig, ohne Tool-Ausgabetrunkierung, gelesen. Das Manifest enthält dieselben neun Quellen. Die Prüfung erfolgte auf den tatsächlichen UTF-8-Dateibytes; keine Zeilenenden wurden normalisiert.

Manifest-SHA-256, erwartet und tatsächlich gleich:

`1d0b94c0f3c0473736571fa0302f8a4adde7b04012d0c1c1ac038cd6a38cb162`

| Quelle | Vollständig gelesene Datei | Zeichen | Bytes | Tatsächlicher SHA-256; Abgleich jeweils PASS |
|---|---|---:|---:|---|
| S01 | S01-Folder.md | 1.972 | 1.981 | `c399b1f42b806e34cb637b4c249a41a77ca56f8e17a35eacdaf2546c0e1a243f` |
| S02 | S02-Golden-Slice-Pilot.md | 4.539 | 4.598 | `731cb1d36707fdf09d1760a730f1da84927761e034129d935246f2921cabb87c` |
| S03 | S03-CPLM-Regeln-v0.3.md | 10.239 | 10.395 | `e5989a79cbba8bf92fb5e976ee359270d108b2f5000477e0aabe058fd4972131` |
| S04 | S04-Folder-Governance-v0.1.md | 2.923 | 2.933 | `839acb90260f6df0ec9a741660a4a317dce11dfd12b14f604554e53531726854` |
| S05 | S05-LLM-Registry-v0.1.md | 13.205 | 13.346 | `0142a7f788c3fd3a6adf97b9b1a136cfafbc2b1501e244bd0cac8c1737ea2614` |
| S06 | S06-Audit-WORK-R0002.md | 3.469 | 3.503 | `95cf799a90fd82c992d6643ee7e25422d118d3c4575f54ba76008f85113358e7` |
| S07 | S07-WORK-FRONT-LOG.md | 9.314 | 9.386 | `5a38fd08305b54e9d733d77a3bb2104a6c1a99df7ac926066c39c93b017736d5` |
| S08 | S08-WorkOrder-Feedback-Archive-Capability.md | 2.138 | 2.175 | `47eba0fc99514effa4d5826f69f8ea4ac27f5e476ab8aebdecbbd1bb2275ca4b` |
| S09 | S09-NEXUS-ECOSYSTEM-CONCEPT.md | 14.861 | 14.927 | `0a5ac2565bfe7af61a9562158f4705ec64f464664832188379d81e7b48a7d351` |

**Summe: 62.660 Zeichen.** Integritäts-PASS bezieht sich ausschließlich auf die Übereinstimmung dieses eingefrorenen Quellbestands mit dem Manifest. Cloud-Originale, Zugriffsrechte, fachliche Richtigkeit und Laufzeitverhalten werden damit nicht bestätigt.

Für Fundstellen bedeuten S01–S09 die obigen Dateien. Abschnitte werden mit ihren tatsächlichen Überschriften oder YAML-Feldern angegeben. Tatsächlich beobachtete lokale Befunde, in Quellen berichtete Ereignisse und noch nicht ausgeführte Laufzeittests bleiben getrennt.

## Tragfähige Systementscheidungen

1. **Ein kanonischer Einstieg und explizite Grenzen:** S01/S02 setzen `Folder.md`, WORK als geprüfte Wurzel und die Nichtkenntnis darüberliegender Regeln. Das ist belastbarer als eine unbelegte globale Policyübernahme. Der außerhalb von WORK liegende Parent ist in dieser erklärten Grenzziehung kein automatisch nachgewiesener Fehler.
2. **Keine Gleichsetzung von Speichern und Wissen:** S03 §§1, 3 und S06 „Grenzen“ begrenzen Hash-/Readbackaussagen korrekt. Unbekannte quantitative Deltas bleiben NOT_MEASURED.
3. **Accountasymmetrie als Architekturmerkmal:** S05 §§2–7 trennt Rolle, Account, Provider, Modell, Instanz, Capability und Verfügbarkeit. Ein eingeschränkter Teilnehmer muss dadurch nicht denselben Vollzugriff wie ein Writer erhalten.
4. **Kontrollierte Veröffentlichung:** S05 §6 erlaubt einen eng berechtigten Broker und verbietet unkontrollierten bidirektionalen Sync sowie das Umgehen von Business-Policies durch Privataccounts.
5. **Innovation mit verschiedenen Änderungsgeschwindigkeiten:** S05 §9 schützt langsamere Grundlagen vor schnellen Laufzeitexperimenten; S09 kann als Ideenraum erhalten bleiben. Die SILOFEM-/Bestfit-Analogie wird erst durch konkrete Fehlerhypothesen zu einem prüfbaren Resilienzverfahren, nicht durch den Namen.
6. **Vorhandene Teilbelege werden angemessen eingegrenzt:** S06 berichtet ein vollständig paginiertes Direktinventar; es beansprucht keine rekursive Gesamtabdeckung. S07 hält den doppelt vergebenen Laufbezug sichtbar, statt eine bereinigte Vergangenheit zu erfinden.

## Befunde

Schweregrade: **HOCH** blockiert eine belastbare Produktionsbehauptung oder gefährdet Zustands-/Berechtigungsintegrität; **MITTEL** gefährdet Pilotinterpretation, Wartbarkeit oder kontrollierte Skalierung; **NIEDRIG** wäre eine begrenzte Darstellungsabweichung. Kein Befund behauptet einen tatsächlich eingetretenen Cloudschaden, soweit das nicht im Quellbestand belegt ist.

### R3-01 — HOCH — Die Einstiegsmigration ist semantisch entschieden, aber nicht durch alle Leser abgeschlossen

**Quellen:** S02 „Geltende Pilotregeln“; S03 §§1–2 und 5; S04 Rules 002–003; S05 §4 Frage 4; S07 „Migration Folder.md“; REVIEW-SCOPE.

**Befund/Evidenz:** Neu gilt exakt `Folder.md`. S03 nennt `_FRONT.md`, S04 `FOLDER.md`, die Registryumfrage fragt nach `WORK/_FRONT.md`. REVIEW-SCOPE bestätigt ausdrücklich den noch veralteten Schedulerbezug. Die Datei-ID blieb bei der Umbenennung stabil; das ist günstig, beweist aber nicht, dass namebasierte Leser oder Agentprompts dieselbe Quelle auflösen. Auch die Dateinamenssyntax weicht zwischen älteren Regeln ab. Das Pilotdokument erklärt die beabsichtigte Priorität, ersetzt keinen migrierten Consumer.

**Risiko:** Interaktiv funktioniert der neue Einstieg, während ein Hintergrundworker einen alten Namen sucht, einen veralteten Master rekonstruiert oder blockiert. Fehlende `Folder.md` könnte dann irrtümlich als Neuinstallation behandelt werden.

**Kleinste wirksame Verbesserung:** Einen kleinen gültigen Vertragskopf mit `entrypoint_file_id`, exaktem Namen, `policy_version`, `supersedes` und Schema-ID festlegen. Bestehenden Scheduler und Umfrage auf diese ID/Version umstellen; alten Titel nur als dokumentierten Alias behandeln. Kein zweiter schreibbarer Master. Einen tatsächlichen Hintergrundlauf nach der Migration als Nachweis verlangen.

### R3-02 — HOCH — Unique Run-ID und erneutes Lesen ersetzen keine exklusive Zustandsänderung

**Quellen:** S02 Abnahmekriterien 3 und 6 / „Bereits gefundener Fehler“; S03 §4; S05 §5; S07 beide Überschriften „WORK-R0002“; S01 `last_run`/`baseline`.

**Befund/Evidenz:** Die doppelte Vergabe `WORK-R0002` ist unmittelbar im eingefrorenen Log sichtbar. Der zweite Eintrag beschreibt eine andere Aktivität; S01 führt weiterhin den Auditlauf als `last_run` und `previous_run: WORK-R0002`. Erneutes Lesen vor einem Update erkennt bereits sichtbare Änderungen, verhindert aber keinen zweiten Writer zwischen Prüfung und Schreiben. Gates und Lease sind ausdrücklich nicht implementiert.

**Risiko:** Zwei erfolgreiche Readbacks können jeweils nur den eigenen Schreibmoment bestätigen, obwohl später einer den anderen ersetzt. Eine zufällige Run-ID vermeidet Namenskollisionen, aber keinen verlorenen Front-/Log-Update.

**Kleinste wirksame Verbesserung:** Im engen Pilot genau einen tatsächlich autorisierten Writer und keine überlappenden Scheduler-/manuellen Statusmutationen zulassen. Zunächst die überlappenden Schreibwege organisatorisch stilllegen und die Begrenzung ausweisen. Für parallelen Betrieb Schreiboperationen nur über einen kontrollierten Writer mit dauerhafter Auftragsqueue, Versionsprüfung und gegebenenfalls Lease/Fencing führen. Ein abgelaufener Worker darf nach Leaseverlust keine Schreibwirkung mehr erhalten. Separat `run_id`, `event_id` und `front_revision` einführen; historische doppelte IDs nicht umnummerieren, sondern mit eindeutigen Korrekturreferenzen ergänzen.

### R3-03 — HOCH — Die Schreibreihenfolge benennt Teilfehler, enthält aber noch keinen ausführbaren Wiederanlaufvertrag

**Quellen:** S03 §4, insbesondere Bericht → Archiv → Log → Front; S05 §5; S07 Modus APPEND_ONLY_BY_POLICY; S08 „IMPLEMENTIERUNG“ und „DEFINITION OF DONE“.

**Befund/Evidenz:** `RECOVERY_REQUIRED` ist eine richtige Zustandsbezeichnung. Es fehlen jedoch im Bundle dauerhaft protokollierte Stufenreceipts, ein benannter Recovery-Owner und eine Entscheidungsmatrix für jeden Abbruchpunkt. Append-only gilt als Policy; keine technische Unveränderlichkeit wird nachgewiesen. S07 enthält in späteren Einträgen vorherige Snapshots, aber nicht durchgehend einen ausdrücklich ausgewiesenen Hash jedes dort archivierten Zwischenzustands.

**Risiko:** Nach Crash sind Bericht, History und Front einzeln plausibel, aber die nächste Instanz weiß nicht eindeutig, welcher Schritt bereits wirksam war. Blindes Wiederholen kann doppelte Archivierung, divergierende Logs oder eine erneute externe Aktion erzeugen.

**Kleinste wirksame Verbesserung:** Einen dauerhaften Laufdatensatz mit `run_id`, erwarteter Frontrevision, Policyhash, `stage`, Artefakt-ID/Hash je Stufe, letztem Fehler und Wiederaufnahmeentscheidung verwenden. Front als daraus abgeleitete aktuelle Sicht behandeln. Jeder Wiederanlauf prüft vorhandene Wirkung vor einer Mutation. Eine monolithische Event-Sourcing-Plattform ist hierfür nicht notwendig; wenige unveränderliche Receipts plus kontrollierter Writer reichen als Pilotgrundlage.

### R3-04 — HOCH — Abschluss ist noch kein eindeutiges Produkt aus Ausführung, Archivierung, Übergabe und Freigabe

**Quellen:** S02 Ziel / Kriterien 7–8; S03 §4; S05 §5 COMPLETION_GATE; S08 Übergabe-FSM und Definition of Done; S01 `tasks`/`status`.

**Befund/Evidenz:** S08 verlangt beim Abschluss protokollierten Empfänger/ACK; S02 akzeptiert Ergebnis im Task-Chat und genau eine E-Mail, wobei Lesen ausdrücklich nicht bewiesen wird. S05s COMPLETION_GATE nennt Artefakt-/Statuskette, aber keinen expliziten ACK-Übergang. Diese Anforderungen können für unterschiedliche Scopes sinnvoll sein; eine Zuordnung pro Auftragsart fehlt. `PILOT_PASS`, `COMPLETED`, `VERIFIED` und Release werden dadurch nicht automatisch dieselbe Aussage.

**Risiko:** Ein technisch archivierter Audit wird als erfolgreiche Übergabe ausgelegt; umgekehrt bleibt eine gültige technische Lieferung wegen ausbleibenden menschlichen Lesens endlos „fehlgeschlagen“.

**Kleinste wirksame Verbesserung:** Je WorkOrder getrennte Felder `execution_status`, `archive_status`, `delivery_status`, `ack_status`, `review_status`, `release_status` definieren und die erforderliche Kombination explizit festlegen. Für den ersten Pilot kann „Mail vom Provider angenommen, ACK offen“ ein sauberer technischer Teilabschluss sein; ein vertraglich erforderlicher ACK bleibt trotzdem offen. Keine Änderung dieser Abnahme allein durch den ausführenden Agenten.

### R3-05 — HOCH — Der Kontrollkreis hat noch keinen nachgewiesenen unabhängigen Beobachter

**Quellen:** S03 §§4–5; S06 „Grenzen“; S09 „Best-of-Repository“ und „NEXUS-AI-RESILIENCE-ALGORITHM“; S01 `last_run`.

**Befund/Evidenz:** Es ist ein Auditworker mit gespeichertem Status beschrieben. Ein separat laufender Watchdog, der das Ausbleiben eben dieses Workers unabhängig erkennen und melden kann, ist nicht nachgewiesen. Ein durch denselben Scheduler, Account, Connector und Speicher laufender Selbstcheck wäre nur begrenzt unabhängig.

**Risiko:** Fällt die gemeinsame Abhängigkeit aus, entstehen weder Bericht noch Warnung. Ein alter PASS-Status bleibt sichtbar, obwohl der Kontrollkreis stillsteht. Ein Heartbeat vom gestarteten Prozess allein beweist auch keinen abgeschlossenen Audit.

**Kleinste wirksame Verbesserung:** Einen einfachen externen beziehungsweise getrennt betriebenen Erwartungsprüfer für „letzter abgeschlossener Lauf älter als Schwellwert“ festlegen. Er beobachtet Completion-Receipt und Deadline, nicht nur Prozessstart. Seine Authentifizierung und sein Alarmkanal sollten mindestens die konkret abzudeckende Fehlerdomäne nicht vollständig teilen. Welche Ausfälle weiter gemeinsam sind, dokumentieren. Für einen beaufsichtigten Pilot genügt zunächst ein benannter menschlicher Fristprüfer; das ist keine autonome Produktionsüberwachung.

### R3-06 — HOCH — „HOURLY und enabled“ begründet keine Ausführungs- oder Frischegarantie

**Quellen:** S03 §5, Scheduler-ID und `next_run_time: null`; S04 Rule 005; S02 Ziel / „Grenzen der Benachrichtigung“.

**Befund/Evidenz:** Zeitplan und eine frühere gemeldete Laufzeit sind berichtet; künftiger kompletter Audit wird korrekt NOT_RUN genannt. Es fehlen zulässige Verspätung, maximale Laufdauer, Überlappungsverhalten, Nachholstrategie, Retrybudget und explizite Ausfalleskalation. Europe/Vienna ist festgelegt, aber Zeitumstellung und verpasste Ausführungen sind nicht spezifiziert.

**Risiko:** Nutzer lesen „stündlich“ als garantierte Aktualität. Nach längerer Unterbrechung kann ein einzelner Lauf ein historisches Delta übersehen oder eine Nachholwelle konkurrierende Runs erzeugen.

**Kleinste wirksame Verbesserung:** Einen kleinen Betriebsvertrag festlegen: Zielintervall, tolerierte Latenz, maximale Staleness, ein aktiver Lauf pro Ziel, verpasste Intervalle zusammenfassen oder gezielt nachholen, begrenzte Retries und Eskalationsfrist. UTC-Ausführungszeiten speichern; Vienna-Zeit als Anzeige/Terminregel behalten. Tatsächliche Start-/End-/Completion-Zeit und Change-Watermark messen. Keine Garantie aus dem Schedulerflag ableiten.

### R3-07 — HOCH — „Genau eine E-Mail“ ist ohne dauerhaften Zustellzustand bei Fehlern nicht belastbar

**Quellen:** S02 Kriterium 7 / „Grenzen der Benachrichtigung“; S08 Übergabe-FSM; REVIEW-SCOPE „No notification email sent yet“.

**Befund/Evidenz:** Der Pilot verlangt die Suche nach einer bereits gesendeten gleich betitelten Mail und Dokumentation der Versand-ID. Im Freeze ist kein Versand nachgewiesen. Eine Suche vor Versand ist keine atomare Deduplikation. Bei Abbruch nach Providerannahme, aber vor Receipt, kann die nächste Instanz die Wirkung nicht sofort sicher kennen. Gleicher Betreff allein ist zudem kein stabiler fachlicher Zustellschlüssel.

**Risiko:** Wiederholung erzeugt zwei Mails; vorschnelles Unterdrücken erzeugt keine Mail. Ein fehlgeschlagener Pushschaltertest kann mit erfolgreicher Mailannahme verwechselt werden. `to: me` bezieht sich auf den authentifizierten Account und muss im Multiaccountbetrieb auf den vorgesehenen Empfänger passen.

**Kleinste wirksame Verbesserung:** Einen dauerhaften Zustellauftrag mit `pilot_id + channel + intended_recipient` als Deduplikationsschlüssel und Zuständen PREPARED/SENDING/ACCEPTED/UNKNOWN/FAILED verwenden. Nur ein Sender darf ihn ausführen. Bei unklarem Ausgang gezielt Providerdaten abgleichen; keine automatische Erfolgserfindung oder blinde Wiederholung. Providerannahme, Inboxzustellung, Gerätesichtbarkeit und menschlicher ACK bleiben verschiedene Nachweise. Falls der Kanal keine belastbare Idempotenz anbietet, das verbleibende Doppel-/Verlustrisiko ausdrücklich ausweisen statt „exactly once“ zu versprechen.

### R3-08 — HOCH — Der Broker ist die richtige Antwort auf Accountasymmetrie, aber noch keine getestete Berechtigungsgrenze

**Quellen:** S05 §§2–6 und Troubleshooting REG-TB-001–003; S08 Capability-Registry; S09 GitHub-Sync/Onboarding.

**Befund/Evidenz:** Die Accounts sind größtenteils USER_REPORTED/NOT_TESTED. Die aktuelle Instanz ist nicht eindeutig Business/Privat zugeordnet. S05 beschreibt Inbox → Broker → eng berechtigter Writer → PR → Receipt, aber keine ausgeführte Crossaccountübergabe. Ein Capabilitytest belegt eine Operation zum Testzeitpunkt, nicht ihre unbeschränkte Gültigkeit.

**Risiko:** Ein Worker kann über den Broker ein Ziel, eine Datenklasse oder eine Aktion verlangen, die er selbst nicht ausführen dürfte. Ein im Privataccount gelungener Graphwrite legitimiert keinen Businessdatenexport. Authentifizierung, Rolle und Quelltextbehauptung könnten verwechselt werden.

**Kleinste wirksame Verbesserung:** Zuerst nur einen schmalen Auftragstyp erlauben, etwa neuen Reviewbericht in freigegebenem Testziel ablegen. Authentifizierte Herkunft, erlaubtes Ziel, Operation, Datenklasse, Auftrags-ID, Policyhash und Ablaufzeit prüfen. Der Writer trifft die Zielentscheidung aus autorisierter Konfiguration, nicht aus beliebigem MD-Inhalt. Einen erlaubten und einen abzuweisenden Auftrag über denselben Adapter nachweisen; Rechteentzug zwischen Test und Ausführung behandeln.

### R3-09 — MITTEL — Die kanonische Quelle ist auf Dokumentebene angelegt, auf Ökosystemebene noch nicht vollständig adressierbar

**Quellen:** S01 `source_of_truth`/`sync_rule`; S05 §§1, 6, 10; S09 #23 „SSOT“; S07 Registry-/PR-Verweis.

**Befund/Evidenz:** Drive-Draft und GitHub-Reviewsnapshot sind sinnvoll getrennt. S09 beschreibt GitHub zugleich als umfassenden SSOT und enthält mehrere Pfade/Links. Das ältere Konzept ist keine aktuelle Freigabe, bleibt aber als potenzieller Lesereinstieg vorhanden. Ein universeller Master für Dokumentation, Code, ausführbaren Zustand, Registry, Graph und Cloudartefakte wäre zu grob.

**Risiko:** Eine PR-Änderung wird als kanonische Policy gelesen, obwohl nur Drive freigegeben ist; ein Drive-Draft wird automatisch in ausführbare Konfiguration übernommen. Lokale Mountpfade suggerieren außerhalb ihres Hosts eine Erreichbarkeit, die nicht besteht.

**Kleinste wirksame Verbesserung:** Einen kleinen Objektkatalog mit `object_id`, Typ, kanonischem System/ID, Revision/Hash, Reviewkopien und Promotionszustand führen. Pro Objekt genau eine schreibende Autorität. GitHub-PR-Receipt muss auf die tatsächlich geprüfte Drive-Version zeigen; Rückübernahme braucht eine explizite Promotion mit Konfliktregel. Graph und Dashboard sind Projektionen, solange keine gegenteilige Objektentscheidung vorliegt. Keine Vollmigration aller Daten für den Pilot.

### R3-10 — MITTEL — Pace Layers sind korrekt benannt; ihre Änderungsgrenzen brauchen noch ein ausführbares Verfahren

**Quellen:** S05 §9; S02 Vererbung; S03 §3 Baselinewechsel; S01 `policy_version`/`inheritance`.

**Befund/Evidenz:** L0–L5 und unterschiedliche Änderungsraten sind verständlich. Noch nicht spezifiziert ist, was ein laufender Worker bei Policyänderung, Parentänderung, Capabilityablauf oder Widerruf tun muss. S02 verlangt Parent-ID und Parent-Policy-Version bei Kindern; ein tatsächlicher Childfall oder eine berechnete effektive Policy ist im Freeze nicht belegt.

**Risiko:** Ein Run beginnt unter erlaubter Policy und beendet mit inzwischen unzulässiger Wirkung. Verschiedene Childordner verwenden veraltete Parentversionen. Schnelle Routing- oder Skilländerungen beeinflussen langsamere Releaseverträge indirekt.

**Kleinste wirksame Verbesserung:** Pro Run ein effektives Policybundle mit vollständiger relevanter Parentkette und Hash binden. Vor privilegierter Wirkung Widerruf und zwingende Policywechsel prüfen. Definieren, welche Änderungen laufende Runs stoppen und welche erst für den nächsten Run gelten. L1-Änderungen erhalten Migrations-/Kompatibilitätsprüfung; L5-Availability bleibt kurzlebig und darf keine L1-Berechtigung ändern. WORK als bewusst begrenzte Root weiterhin explizit behandeln.

### R3-11 — HOCH — Die Rückkopplungsbremse darf Kontrolländerungen nicht aus der Überwachung entfernen

**Quellen:** S06 „Beobachtungen seit N-1“ und Ergebnis; S07 DELTA-/Migrationseinträge; S03 §3 Governance und DELTA.

**Befund/Evidenz:** Selbst erzeugte Audit-/Statusdateien werden richtigerweise nicht als neue fachliche Arbeit gezählt. Wenn der Scheduler jedoch ausschließlich „externe/fachliche Änderungen“ überwacht, bleibt unklar, wie Änderungen an Policy, Front, Log, Registry oder Auditprompt unabhängig auf Integrität und Konsistenz geprüft werden. S06s `NO_FACHLICHES_DELTA` ist daher enger als „kein relevantes Systemdelta“.

**Risiko:** Die Überwachung bleibt still, obwohl der eigene Kontrollvertrag geändert, ein Log beschädigt oder ein Frontwert falsch gesetzt wurde. Eine pauschale Ignorierregel würde gerade die Steuerungsschicht ausblenden.

**Kleinste wirksame Verbesserung:** Zwei Deltaarten führen: fachliches Delta und Kontroll-/Integritätsdelta. Routinemäßige eigene Statusfortschreibung soll keine neue WorkOrder auslösen; unerwartete Policy-/History-/Schemaveränderung aber sehr wohl. Ereignisse mit Ursprung/Correlation-ID kennzeichnen statt Dateien pauschal auszuschließen. Ein fehlerhafter eigener Policywrite muss einen gezielten Befund erzeugen, ohne unendliche Auditkaskade.

### R3-12 — MITTEL — Vollständiges Listing ist noch kein konsistenter rekursiver Inventar- oder Lastnachweis

**Quellen:** S06 Scope, DELTA und Grenzen; S03 §§1 und 3; S01 Ergebnis; S09 Refresh-/Dashboardziele.

**Befund/Evidenz:** 230 direkte Dateien und 17 direkte Unterordner sind als vollständig paginiert berichtet; die eingefrorene Quelle enthält nicht die einzelnen Listingseiten. Die lokale Prüfung reproduziert diesen Cloudabruf nicht. Keine Rekursion, keine Laststufen, keine vergleichbare Baseline und keine konsistente Snapshotgrenze bei Änderungen während des Paginierens sind belegt.

**Risiko:** Beim Rollout wird „direkt vollständig“ zu „gesamter Bestand vollständig“ erweitert. Jeder Run liest alles erneut, erzeugt hohe Kosten oder längere Laufzeiten; wachsende Logs und Rate Limits verstärken Überlappungen. Dateien, die während der Pagination verschoben oder gelöscht werden, können falsche Deltas auslösen.

**Kleinste wirksame Verbesserung:** Scope und Erfassungsfenster speichern, Lösch-/Verschiebeereignisse abbilden und einen wiederholbaren Abgleich über stabile IDs/Revisionen definieren. Für den Pilot nur WORK direkt; für Rollout erst ein Child, dann wenige ausgewählte Ordner mit gemessenen Laufzeiten/Fehlern. Änderungscursor beziehungsweise Watermarks mit periodischem Vollabgleich nur einsetzen, wenn der Adapter sie nachweislich unterstützt. Keine ungetestete globale Echtzeitbehauptung.

### R3-13 — MITTEL — Der gemeinsame Sprachvertrag braucht beobachtbare Begriffe statt weitere Metaphern

**Quellen:** S09 „shared-understanding.md“, „Best-of-Repository“, SILOFEM+++ / Bestfit und Main-Tasklist; S03 §3 Metriken und DELTA; S05 §§7, 9.

**Befund/Evidenz:** Der Ideenraum verbindet deterministische Analysekerne, probabilistische Koordination, Selbstverbesserung, Wissensgraphen und mehrere UI-/Frameworkoptionen. Die jüngeren Regeln engen das bereits sinnvoll ein. Ein Parser-/Schema-PASS oder ein Read-ACK beweist trotzdem kein gemeinsames Verständnis. Aus der genannten FE-/Bestfit-Analogie folgt kein nachgewiesener Resilienzalgorithmus.

**Risiko:** Ein neues Label ersetzt eine präzise Fehlerfunktion; Routing oder Selbstverbesserung wird optimiert, bevor Nutzen, Nebeneffekte und Rücknahme messbar sind. Umfangreiche Agentenrollen erhöhen die Koordinationskosten des ersten Piloten.

**Kleinste wirksame Verbesserung:** Ein kurzes Glossar für die entscheidenden Zustände mit je Positiv- und Gegenbeispiel anlegen: gespeichert, kanonisch, zugestellt, bestätigt, verifiziert, freigegeben, aktuell. Für jedes Innovationsexperiment eine Hypothese, Vergleichsbaseline, messbaren Nutzen, Fehlergrenze und Rücknahme definieren. Die SILOFEM-Idee vorerst in derselben einen AIM-Liste als unvalidierte Analogie führen; keine neue technische Pflicht oder zweite Ideenregistry daraus ableiten.

## Falsifikationsfälle und tatsächlicher Nachweisstand

Die folgenden Fälle sind **konkrete Prüfpläne**, keine simulierten Testergebnisse. „Im Freeze“ bedeutet direkt sichtbarer Text beziehungsweise dort berichtete Evidenz. Die tatsächliche lokale Ausführung beschränkt sich auf vollständiges Lesen und Hashprüfung. Kein hier aufgeführter Laufzeittest wurde in dieser Reviewerinstanz ausgeführt.

| Test | Gegenfall / Trigger | Erwartetes Ergebnis | Tatsächliche Evidenz im Freeze | Laufzeittest |
|---|---|---|---|---|
| F01 Einstieg | Scheduler startet nach Umbenennung, alter Titel fehlt | Auflösung derselben Datei-ID und aktuellen Policy; kein Ersatzmaster | S02 Migration; SCOPE bestätigt veralteten Schedulerbezug | NOT_RUN |
| F02 Schreibrennen | Zwei Worker lesen dieselbe Frontrevision und schreiben danach | Genau ein Commit; zweiter wird abgewiesen oder sauber erneut eingeplant | S03 erkennt Grenze; kein CAS/Lease; doppelte Run-ID in S07 tatsächlich sichtbar | NOT_RUN |
| F03 Später Zombie | Worker verliert Lease, erwacht nach neuem Writer | Alter Worker erhält keine Schreibwirkung mehr | Lease/Fencing nicht implementiert/nachgewiesen | NOT_RUN |
| F04 Crash vor Front | Abbruch nach Bericht-/Logablage | RECOVERY_REQUIRED, Wiederanlauf verwendet gespeicherte Stufen; kein doppelter Bericht als neuer Run | Reihenfolge und Sollstatus in S03; kein Crashreceipt | NOT_RUN |
| F05 Abweichende Historie | Log verändert oder Snapshot falsch verlinkt | Integritätsbefund; Frontpromotion stoppt; Originalnachweis bleibt referenzierbar | Append-only nur Policy; spätere vollständige Snapshots sichtbar, Hashkette nicht durchgehend ausgewiesen | NOT_RUN |
| F06 Scheduler still | Kein abgeschlossener Audit über Frist | Unabhängiger Fristprüfer alarmiert mit letztem Completion-Receipt | Enabled/hourly und älterer Zeitpunkt; kein unabhängiger Alarm | NOT_RUN |
| F07 Lauf über Intervall | Audit dauert länger als eine Stunde / 429-Fehler | Keine konkurrierenden Writes; begrenzter Retry, sichtbare Verzögerung, spätere Wiederaufnahme | Überlappung, Retry und Frischefristen nicht festgelegt | NOT_RUN |
| F08 Verpasste Intervalle | Scheduler fällt mehrere Stunden aus, danach Neustart | Definierte Nachholstrategie; Change-Watermark überspringt keine Änderung | Kein Nachholnachweis | NOT_RUN |
| F09 Mail unklar | Provider nimmt Mail an, Crash vor Versandreceipt | UNKNOWN, Abgleich mit Provider, keine blinde Wiederholung; dokumentierte Restunsicherheit | S02 Suchpflicht/Versand-ID; kein Versand im Freeze | NOT_RUN |
| F10 Notification | Mailannahme erfolgreich, Handy-Push aus | Mailannahme ausgewiesen; Push/Lesen bleibt ungeprüft | Grenzen in S02 korrekt benannt; kein Notification-E2E | NOT_RUN |
| F11 Brokergrenze | Gültiger Reviewer versucht unzulässiges Ziel/Businessexport | Broker lehnt ab; kein Writer-Side-Effect; begründeter Receipt | S05 richtige Zielarchitektur, kein Brokerlauf | NOT_RUN |
| F12 Rechtswechsel | Capabilitytest PASS, Berechtigung vor Aktion entzogen | Aktuelle Operation scheitert kontrolliert; kein alter PASS als Erfolg übernommen | Testdatum/TTL vorgesehen; Widerrufsausführung nicht gezeigt | NOT_RUN |
| F13 Parentwechsel | Child nutzt alte Parentpolicy; verbotene Lockerung oder Zyklus | Effektive Policy auflösbar oder BLOCKED; laufende Freigabe gemäß Änderungsvertrag | S02 fordert Blockierung; kein Childtest | NOT_RUN |
| F14 Masterkonflikt | GitHub-Snapshot und Drive-Draft divergieren | Herkunft/Revision sichtbar; keine stille Rücksynchronisierung | S01/S05 verbieten ungeprüften Zwei-Wege-Sync; PR18 nur berichtet | NOT_RUN |
| F15 Kontrollblindheit | Eigener Worker schreibt falsche Policy, aber kein Fachdelta | Genau ein Kontrollbefund; keine endlose Folgeaudits | Fachdeltaausschluss beschrieben; separater Kontrollkanal nicht nachgewiesen | NOT_RUN |
| F16 Bestand in Bewegung | Datei wird während Pagination verschoben; Unterordner enthält neue Datei | Fenster/Scope sichtbar; Reconciliation erkennt Änderung oder weist Unsicherheit aus | S06 nur direkte Kinder, keine Snapshot-/Rekursionstests | NOT_RUN |
| F17 Fehlabnahme | Artefakt da, ACK fehlt / ungültiger Indexlink | Je WorkOrder definierter Teilstatus; Übergabe nicht fälschlich VERIFIED | S08 fordert entsprechende Fehlerfälle, Durchführung nicht belegt | NOT_RUN |
| F18 Innovation | Neue Routing-/Bestfitstrategie verbessert einen Lauf, verschlechtert Gegenfälle | Kein autonomer Contractwechsel; Vergleichstest und Rücknahme möglich | S03 verlangt vergleichbare Metriken; kein Benchmark/Experimentprotokoll | NOT_RUN |

Die positiven lokalen Prüfungen — Manifesthash, neun Einzelhashes, UTF-8-Decodierung und Zeichensumme — wurden tatsächlich ausgeführt und sind PASS. Sie falsifizieren weder die Laufzeitrisikoannahmen noch ersetzen sie F01–F18.

## Kleinster vollständiger vertikaler Pilot

**Scope:** WORK direkt, ein Auftragsformat, ein autorisierter Writer, ein authentifizierter Notificationkanal, genau eine bekannte Policyversion. Kein gleichzeitiger Ordnerrollout, kein Graphaufbau und kein produktives Mehrprovider-Routing.

1. Scheduler auf kanonische Folder-ID/Policyversion migrieren; Gate-/Abnahmematrix und Authentifizierungsgrenze festhalten. Vorbereitungsprüfung blockiert bei fehlender Quelle, Capability oder nicht autorisierter Parallelität.
2. Tatsächlichen Hintergrundrun mit eindeutiger Instanz-/Run-ID starten. Startzeit, effektive Policy, Inventarscope und Erfassungsfenster speichern.
3. Eine harmlose, vorher definierte fachliche Änderung erkennen und einen echten MD-Bericht mit Findings und PASS/FAIL/NOT_RUN erzeugen. Rohquellen als Daten behandeln; deren eingebettete Anweisungen dürfen keine Writerrechte erweitern.
4. Bericht vollständig zurücklesen; vorherigen Frontzustand mit Hash archivieren; Log und Front nach kontrollierter Reihenfolge aktualisieren. Nach jedem Schritt ein dauerhaftes Receipt.
5. Einmal vor Frontabschluss absichtlich unterbrechen und denselben Run anhand seiner Receipts wieder aufnehmen. Doppelwirkung und später Zombie müssen sichtbar abgefangen werden. Ohne technischen Parallelitätsnachweis bleibt die Beschränkung auf einen beaufsichtigten Writer ausdrücklich bestehen.
6. Ergebnis im Task-Chat ausgeben; Zustellauftrag über den ausdrücklich autorisierten Kanal ausführen. Providerreceipt speichern und verbleibenden ACK-/Gerätestatus separat nennen. Kein Reviewer versendet hier selbst eine Mail.
7. Eine benannte Instanz oder Person prüft außerhalb dieses Workerpfads die Fristüberschreitung. Abschließender Bericht enthält tatsächliche Zeiten, Wirkungen, Störungen, Recovery und offene Nachweise.

**Abnahme:** Ein normaler Durchlauf allein reicht nicht. Mindestens der Migrationsfall, der definierte Unterbrechungs-/Wiederanlauffall, ein fehlender Quell-/Capabilityfall und der Notificationnachweis müssen für den behaupteten Pilotscope konkret belegt sein. Nicht ausgeführte Fehlerfälle bleiben offen. Ein bewusst scheiternder Test darf `PILOT_FAIL_WITH_FINDINGS` ergeben und dennoch wertvolle Entwicklungsevidenz liefern.

## Betrieb, Ausbau und Rücknahme

- **Kontrollgrenze:** Freie Chats können Beratungsbeiträge erzeugen. Produktionswirkungen dürfen nur privilegierte Schnittstellen auslösen, die den gültigen Auftrag und die aktuelle Berechtigung prüfen. Eine Markdownanweisung kann diese Grenze beschreiben, aber nicht herstellen.
- **Daten-/Kontrollebene:** Reports, Chattexte und externe Dateien sind Daten. Policy-/Gatekonfiguration wird durch einen kontrollierten Promotionsweg aktiv. Ein aus einer Quelle gelesener Satz ist keine neue Humanfreigabe.
- **Zeitliche Grenze:** Ein als „aktuell“ gezeigter Front braucht Beobachtungszeit, Frischefrist und Zustand bei Fristüberschreitung. Ein alter PASS muss sichtbar veralten können.
- **Ausbaufolge:** Zuerst vertikaler WORK-Pilot, dann ein Child mit echter Vererbungsprüfung, dann wenige Ordner mit Last-/Rate-Limit-/Recoverymessung. Erst danach zusätzliche Accounts, Brokeradapter oder automatisches Routing, jeweils mit eigenem zulässigem Aktionsumfang.
- **Rücknahme:** Bei fehlenden Receipts, Policykonflikt, unklarem Writerbesitz oder unbekannter externer Wirkung keine weitere Promotion. Auf verifizierte letzte Sicht verweisen und Zustand als STALE/RECOVERY_REQUIRED markieren. Das bedeutet nicht, bereits wirksame Mails oder externe Änderungen automatisch rückgängig zu machen.
- **Wiederherstellung:** Wiederherstellung von Front/Log aus gesicherten Artefakten muss mit einem Test belegt werden. Historie erhalten; fehlerhafte Einträge durch neue Korrekturereignisse erklären. Verlust und Korruption sind andere Fälle als ein normaler Retry.
- **Skalierung:** Laufzeit, Dateianzahl, Queuealter, Fehlerraten, Rate-Limits, Recoverydauer und Kosten nur soweit tatsächlich messbar erfassen. Keine Completionquote ohne definierten Nenner; keine Tokenzahlen schätzen. Für Überlast braucht es Backpressure und Priorisierung, nicht bloß mehr parallele Agenten.

## Offene Entscheidungen vor den nächsten Stufen

| Frage | Warum entscheidungsrelevant | Frühester notwendiger Zeitpunkt |
|---|---|---|
| Welche konkrete Runtime ist alleiniger Writer für den ersten Piloten; wer stoppt andere Schreibwege? | Organisatorische Begrenzung muss tatsächlich gelten | Vor Pilotstart |
| Welche Policy-/Entrypoint-ID liest der reale Scheduler nach der Migration? | Name/ID-/Versionübergang ist derzeit offen | Vor Pilotstart |
| Was bedeutet PILOT_PASS bei Mailannahme ohne ACK, und welche WorkOrders erfordern VERIFIED-Handoff? | Einheitliche Abnahme ohne Bedeutungswechsel | Vor Pilotabnahme |
| Ist `to: me` im ausführenden Konto der gewünschte, autorisierte Empfänger? | Accounts sind nicht automatisch identisch | Vor tatsächlichem Versand |
| Welche Frischefrist und maximale Auditdauer gelten? Wer beobachtet Fristverletzung? | „Stündlich“ wird sonst als Garantie missverstanden | Vor unbeaufsichtigtem Pilot |
| Welcher dauerhafte Laufdatensatz steuert Recovery; wer besitzt Recovery nach Crash? | Kein händisches Erraten der letzten Wirkung | Vor Unterbrechungstest |
| Was zählt als unabhängiger Reviewer für Vertragsfreigabe und Re-Review? | Instanztrennung ist etwas anderes als Provider-/Accountdiversität | Vor Freigabeauswertung |
| Welche ID-Namensräume gelten für Autorität, Rolle, Account und Run? | Bestehende numerische Rollenkonflikte nicht weitertragen | Vor kanonischer Registrypromotion |
| Welche Datenklassen dürfen welchen Broker-/Privat-/Graphpfad verwenden? | Zugriffsfähigkeit allein ist keine Exportfreigabe | Vor Crossaccountpilot |
| Welche Regeln widerrufen laufende Aufträge unmittelbar? | Policybindung und aktueller Sicherheitsentscheid müssen zusammenpassen | Vor Parallel-/Mehrordnerbetrieb |
| Welches System ist je Objekt kanonisch; wie erfolgt eine freigegebene Promotion? | Drive/GitHub/Graph haben unterschiedliche Rollen | Vor automatischem Sync |
| Welche Wiederherstellungszeit und welcher Datenverlust sind akzeptabel? | Erst daraus folgen passende Backup-/Recoveryanforderungen | Vor Produktion |

## Getrennte Empfehlungen

### Konzept

**Weiterverfolgung empfohlen.** Die Kombination aus belegten Ordnerzuständen, expliziten Accountfähigkeiten und langsamen/schnellen Änderungsebenen ist sinnvoll. Die engste wirksame Überarbeitung ist ein gemeinsamer operativer Vertrag für Einstieg, Runzustand, Abschlussdimensionen und Recovery. Den Ideenraum S09 erhalten, aber nicht als bereits implementierte Plattform behandeln. AIM bleibt eine einzige Liste mit internen Reifeabschnitten.

### Pilot

**Begrenzte Durchführung nach konkreter Vorbereitung empfohlen; keine Bestätigung eines bereits bestandenen Golden Slice.** Entrypointmigration, benannter exklusiver Writer, persistente Stufenreceipts, klares Notification-/ACK-Kriterium und beobachtete Fristprüfung sind die unmittelbaren Voraussetzungen. Die vorhandenen Direktinventar-/Readbackbelege bleiben nutzbar. Ein erfolgreicher Pilot gilt nur für seine tatsächlich getesteten Aktionen und Grenzen; ein einzelner Durchlauf behebt weder allgemeine Parallelität noch Accountintegration.

### Produktion und Rollout

**Derzeit nicht empfohlen.** Wesentliche Voraussetzungen sind nicht technisch nachgewiesen: exklusive privilegierte Gates, konkurrierende Schreibsicherheit, Recovery/Reconciliation, unabhängige Ausfallbeobachtung, belastbare Zustellsemantik und stufenweise Skalierungs-/Berechtigungstests. Die im Vertrag verlangte Konsolidierung, DELTA-Korrektur, erneute Prüfung aller drei Perspektiven und das Human Gate bleiben eigene Schritte. Dieses Review erfüllt ausschließlich die dritte Prüfposition, nicht die spätere Re-Review- oder Releaseentscheidung.

## Zusammenfassung

Das Material zeigt einen brauchbaren, ehrlicher abgegrenzten Kontrollentwurf und konkrete Teilbelege. Der wichtigste nächste Beweis ist ein kleiner vollständiger Hintergrundlauf einschließlich gezieltem Abbruch, wiederholungsfester Fortsetzung und nachgewiesener Ergebnisannahme. Die höchste Systemgefahr ist derzeit ein plausibel aussehender letzter Status ohne abgesicherte Aussage darüber, wer ihn zuletzt wirksam ändern durfte, welche externe Wirkung bereits eingetreten ist und ob der Kontrollkreis noch lebt.

## Abschließendes Prüfreceipt

- Tatsächlich beobachteter Prüfabschluss: **2026-10-16T15:23:03Z**.
- Vollständiger Review: 9 von 9 Quelldateien, 62.660 Zeichen; Manifest und neun Einzelhashes am Ende erneut PASS. Eingefrorene Eingaben unverändert.
- Ergebnisdatei lokal zurückgelesen; 13 Befunde und 18 getrennte Falsifikationsfälle vorhanden. Keine Behauptung ausgeführter Cloud-/Laufzeittests.
- Keine Ergebnisse anderer Reviewer gelesen; keine externen Änderungen oder Nachrichten, keine Modell-API-Aufrufe, keine Subagenten.
- Reviewstatus: abgeschlossen. Konzept weiterführen; Pilot nur begrenzt und vorbereitet; Produktion/Rollout derzeit nicht empfohlen. Releaseentscheidung bleibt außerhalb dieser Instanz.
