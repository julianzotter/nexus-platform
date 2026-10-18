# RUN 4 — Konsolidierung und Prüfung des neuen lokalen CPLM-Kerns

**Ergebnis:** Konzept weiterführen; den beobachteten Golden Slice als engen Transport-/Persistenzpilot anerkennen; vollständige Übergabe, Vertragsrelease und Produktion bleiben offen. Der neue lokale Kern ist ein konkreter Fortschritt, enthält aber reproduzierte Abnahmelücken. Die drei Erstprüfungen geben diesem neuen Stand keine Freigabe.

## Tatsächliche Identität und Prüfdeckung

Ausführende Instanz: `/root/cplm_run4_consolidation`, separat vom Koordinator `/root` beauftragter vierter Task nach den drei abgeschlossenen Revieweraufgaben. Keine reale fremde Person vertreten; keine fremden Accounts, Provider oder Modellversionen behauptet. Dies ist eine absichtlich informierte Konsolidierung, keine vierte blinde Erstprüfung. Modell-/Accountdiversität und vollständige statistische Unabhängigkeit sind nicht belegt. Tokens und Kosten: NOT_MEASURED.

Alle drei Reviewdateien vollständig einzeln gelesen. Die erste kombinierte Ausgabe war abgeschnitten und wurde deshalb durch vollständige Einzellesungen ersetzt. MANIFEST, REVIEW-SCOPE, alle neun ursprünglichen Quelldateien, vollständiges POST-FREEZE-EVIDENCE.json und alle drei Python-Quelldateien des lokalen Kerns/Tests gelesen. Keine verlinkten Außenquellen oder aktuellen Cloudobjekte nachgeladen. Keine externen Mutationen, Nachrichten oder Modell-API-Aufrufe; keine Subagenten; Code und Freeze nicht verändert. Lokale Ausführung in temporären Testverzeichnissen; Bytecodeerzeugung beim Testlauf deaktiviert.

Erster ausdrücklich abgefragter Zeitbeleg innerhalb dieser Prüfung: **2026-10-16T15:24:36Z**; die vorangegangenen Leseschritte begannen vorher, deren Start wurde nicht gemessen. Folgender Zeitbeleg nach Testausführung: **15:25:15Z**. Abschlusszeit und Readback stehen am Dateiende. Keine erfundene Startzeit aus Taskmetadaten.

Die Manifest-SHA256 wurde tatsächlich erneut geprüft: `1d0b94c0f3c0473736571fa0302f8a4adde7b04012d0c1c1ac038cd6a38cb162`; alle neun Einzelhashes stimmen; 62.660 UTF-8-dekodierte Zeichen. Dies belegt den lokalen Prüfinput, keine Herkunftsauthentifizierung oder Live-Cloudrevision.

| Zusätzlich geprüfter Stand | SHA256 bei dieser Prüfung |
|---|---|
| RUN-1.md | f89e93fb385aae1c1a1026facee75834cb6e87b3a6f3d1a4b187e81cd089a535 |
| RUN-2.md | f8796543e3517592705c375681e4b4dc09638c295c1b060c16ad792468070dda |
| RUN-3.md | b59c5bb88c28315508521e447c9625c05153d331dd3cce5c05c67190101017c8 |
| POST-FREEZE-EVIDENCE.json | f300f11729e9266cbae5ce2d790c017b97d34035fee1b13f40637fb5ccc8e3ed |
| nexus_cplm/core.py | 5ddae192d26a92e59da23eb3145c774d318f4fefde6629997db6714efaece6ec |
| tests/test_cplm.py | 42412d292b113a5fa0b815a3edd1d06bf0f493c400dfc9424545fabe41b354e2 |

Die Vorreviews beziehen sich ausschließlich auf den alten neun Dateien umfassenden Freeze. Das Postfreeze-JSON ist ein zusätzlicher, vom Koordinator zusammengestellter Nachweis mit eingebettetem Pilotbericht und Anforderungen. Seine berichteten Connectorbeobachtungen wurden hier nicht erneut an den Providern durchgeführt. Der neue Kern wurde von den ersten drei Instanzen nicht geprüft. Ein späterer Fix verändert den hier angegebenen Codehash und benötigt neue Prüfung seiner betroffenen Invarianten.

## Gemeinsame Befunde ohne Dreifachzählung

Die Reviewer sind in der Richtung einig: brauchbare Grundidee, enger Pilot unter Bedingungen, keine Produktionsfreigabe. Unterschiedliche Schweregrade sind Perspektiven, keine unterschiedlichen beobachteten Schadensfälle: R2 bewertet die fehlende privilegierte Grenze und Humanidentität als KRITISCH für Produktion; R1/R3 überwiegend als HOCH. Für die nächste Arbeit zählt die konkrete Blockierwirkung.

| Konsolidat | Beibehaltene Reviewer-IDs | Gemeinsamer Kern und heutige Einordnung |
|---|---|---|
| K01 Kontrollierte privilegierte Wirkung / Humanidentität | SW-08; R2-G01/G03/G11; R3-08 | Credentials und Freigaben müssen am Gateway geprüft werden. Lokal nur Principalstrings; keine installierte externe Authgrenze. Produktionsblocker bleibt. |
| K02 Effektive Policy / Einstieg / Vererbung | SW-06/07; R2-G02/G06; R3-01/10 | Folder.md und eine AIM-Datei sind die aktuelle Pilotentscheidung. Postfreeze meldet Schedulerumstellung und Childmetadaten. Ein rekursiver, ausführbarer Policyresolver und Widerrufspfad bleiben offen. |
| K03 Konkurrenz / eindeutige Aufträge | SW-01/04; R2-G07; R3-02 | Historische R0002-Dublette bleibt. SQLite serialisiert lokale Kernelwrites und dedupliziert task_key, schützt aber keine direkten Driveupdates oder andere Hosts. |
| K04 Recovery / belastbare Historie | SW-03; R2-G07; R3-03 | Lokaler vollständiger Dateischreibabbruch wird getestet; Teilwrite bleibt defekt. Drive-Bericht/Archiv/Log/Front noch ohne getesteten Recoveryadapter. |
| K05 Abschluss / Handoff / Sendesemantik | SW-02/05; R2-G10/G12; R3-04/07 | Mailtransport ist zusätzlich belegt, menschlicher ACK nicht. Lokale FSM trennt Schritte, prüft aber nur freie Evidenzstrings. Outbox besitzt noch keinen semantisch eindeutigen Zustellschlüssel. |
| K06 Versionsgebundene Reviews / Freigabe | SW-11; R2-G04/G05; R3-04 | Drei unterschiedliche Tasks auf demselben Freeze abgeschlossen. Keine automatische Freigabe der Postfreezeänderungen; neuer Kern bindet Reviews nicht an das tatsächliche Resultatmanifest. |
| K07 Kontroll- und Fachdeltas / Findingpflege | SW-10; R2-G08/G09; R3-11 | Selbstursprung darf Kontrolländerung nicht ausblenden. Stabiler Findingstatus mit Closurebeleg fehlt; ein neuer PASS schließt alte Lücken nicht. |
| K08 Ein Master je Objekt / Projektionen | SW-09; R2-G11; R3-09 | Drive-Draft und GitHub-Reviewkopie sind sinnvoll; maschinenlesbare Herkunft, erlaubte Datenflüsse und Promotion bleiben auszuführen. |
| K09 Betrieb / Ausfall / Skalierung | R2-G12; R3-05/06/12 | Aktivierter Stundenplan ist keine Frischegarantie. Watchdog, Fristen, Überlappungs-/Nachholregeln, Reconciliation und Lastnachweise fehlen. |
| K10 Kleines ausführbares Minimum / Sprache | SW-11; R2-G02; R3-13 | Neues lokales Minimum liegt tatsächlich vor. Shared Understanding, fachliche Richtigkeit und SILOFEM-Analogie sind durch Schema-PASS nicht bewiesen; kein zusätzlicher Plattformbau erforderlich. |

Damit bleiben alle 11 SW-, 12 Governance- und 13 Systembefunde auffindbar; kein Mehrheitsvotum ersetzt einen Widerlegungstest. SW-07 gegenüber R2-G06 ist vor allem eine Schwereabweichung. R1 bevorzugt zwei Hauptzustände, R3 mehrere Dimensionen: praktisch genügen Ausführung und Handoff als FSM plus separate Archiv-/Review-/Release-Receipts. Es braucht keine sechs voneinander unabhängigen veränderlichen Statusmaster.

WORK als ausdrücklich begrenzte Root ist kein bewiesener Parentfehler. Nicht geladene Vorfahren begrenzen die Complianceaussage. Ältere Namen und Ideen in S09 bleiben historische Quellen, keine aktuelle ausführbare Autorität. Die spätere Pilotentscheidung löst Folder.md/AIM für den Pilot; sie löscht die widersprechenden Ursprungstexte nicht.

## Postfreeze-Pilot: was sich wirklich geändert hat

Im alten Freeze: PILOT_READY, kein Mailversand, Scheduler mit altem Einstieg. Diese Aussagen waren zum Freeze korrekt und werden durch spätere Ereignisse nicht zu Reviewerfehlern.

Postfreeze meldet der Koordinator Schedulerupdate, bestätigten Trigger und einen tatsächlich existierenden Bericht v0.2.0, Run `CPLM-ID03-20261016T171113+0200-b4ef0310`. Der eingebettete Bericht referenziert Pilot- und Folder-ID, meldet 233 direkte Dateien/18 Unterordner, Childprüfung, Readbacks, Archivierung sowie eine Gmail. Separat im JSON: vom Koordinator gelesene Gmailmetadaten für `1a145489e35d9f01`, `SENT`, `INBOX`, `UNREAD`, erwarteter Betreff und Empfänger. Das ist stärker als bloß ein Startauftrag oder eine Versandabsicht. RUN 4 hat diese Liveabrufe nicht wiederholt.

| S02-Kriterium | Konsolidierte Bewertung des neuen Nachweises |
|---|---|
| 1 vollständiges Lesen aktuelle Pilot-/Folderquelle | Im Laufbericht behauptet und konkret ID-/versionsbezogen dokumentiert; keine eigenen Laufzeit-Rohreceipts in RUN 4. |
| 2 Raw-MD / YAML / Parent | Bericht konkretisiert MIME/Felder und einen Child. Metadatenprüfung, keine allgemeine Vererbungsdurchsetzung. |
| 3 eindeutige Run-ID | Konkrete neue Kennung und Suchvorprüfung dokumentiert. Kein global atomarer Reservierungsnachweis; alte Dublette bleibt offen. |
| 4 Bericht mit Einzelstatus | Eingebetteter vollständiger Bericht enthält Befunde/Risiken/offene Punkte und acht Statuszeilen. Lokal als Text sichtbar. |
| 5 Speicherung / Readback | Drive-ID und bytegleicher Readback berichtet. Hier keine erneute Cloudprüfung. |
| 6 Konflikt / Status / Log | Wiederlesen/modifiedTime/Archiv und Zwischenreadback berichtet. Das zeigt einen beobachteten seriellen Pfad; keine atomare Konfliktverhinderung und kein Konkurrenzgegenfall. |
| 7 Task-Chat und eine Mail | Transport wird durch getrennt berichtete Metadaten gestützt. Genau ein Suchtreffer zum Zeitpunkt ist keine Exactly-once-Garantie. Task-Chat-Abschluss steht im Bericht noch im Futur („wird ... ausgegeben“); tatsächlicher Chatoutput ist im JSON nicht enthalten. |
| 8 sauberer Endstatus | PILOT_PASS und NOT_RELEASED stehen im Bericht; das Label ist kein unabhängiger Test. |

**Urteil über PILOT_PASS:** Als Eigenbewertung des normalen, eng begrenzten Persistenz-/Mailpfads plausibel und mit zusätzlichen Mailmetadaten gestützt. Keine vollständige unabhängige Bestätigung aller acht Kriterien durch RUN 4: insbesondere Task-Chatoutput nicht im bereitgestellten Nachweis, Konfliktverhinderung/Recovery nicht demonstriert. Daher hier `PILOT_OBSERVED_WITH_OPEN_ACCEPTANCE`, keine pauschale Umdeutung zu „alles FAIL“, aber auch kein hochgerechneter Gesamterfolg. S08s geforderte bestätigte Übergabe bleibt offen. UNREAD ist kein menschlicher ACK; auch ein READ-Label allein wäre keiner. Gerätepush, Anzeige, Lesen und Übernahme sind nicht belegt.

Ein gültiger technischer Pilot darf Mailannahme als Teilziel ausweisen; er darf die ausdrücklich geforderte Übergabe nicht stillschweigend abbedingen. Neue Kriterien wie Watchdog und gezielter Crash waren Reviewerempfehlungen, nicht nachträglich angeblich schon bestehende acht Pilotkriterien.

## Neuer Kern: tatsächlich ausgeführte Tests und neue Gegenbeweise

Der vom Koordinator berichtete Erstlauf laut JSON: **15 Tests, 0,074 s**. RUN 4 hat unabhängig erneut denselben vorhandenen Testsatz ausgeführt:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v`

**Beobachtet: 15 Tests, 0,099 s, OK.** Alle laufen lokal mit Fixtureidentitäten und temporären Dateien. Das ist ein enger Funktionsnachweis für unbekannten Actor, falschen Policyhash, Auftragsdeduplizierung, lokale Schreibkonkurrenz, vollständigen Artifactwrite vor DB-Rollback, fehlende Pflichtmetadaten, Quellenprüfung bei result(), FSM, drei unterschiedliche Reviewerstrings und lokal behaupteten Humanprincipal. Keine externe Authentifizierung, Drive-/GitHubintegration oder echte Humanfreigabe wird dadurch getestet.

Zusätzlich fünf gezielte lokale Gegenfälle mit unverändertem Code ausgeführt. Ausführung nutzte dieselbe Testfixture und TemporaryDirectory; weder Originalquellen noch Kernel wurden manipuliert. Die Gegenfälle sind **erfolgreiche Reproduktionen einer Lücke**, keine bestandenen Abnahmekriterien.

| RUN-4-ID / Schwere | Reproduzierbarer Ablauf | Tatsächliches Ergebnis | Erforderliche Korrektur / Solltest |
|---|---|---|---|
| C01 HOCH — Reviewobjekt ungebunden | submit → drei PASS-reviews auf `bundle-v1` → erst danach result → Handoff mit beliebigem nichtleerem String → release | `COMPLETED` | Review nur für ein versiegeltes Manifest nach Resultat zulassen. Manifest enthält Resultathash, Code-/Policy-/Quell-/Teststände und Anforderungen. Neues Resultat oder Manifestmutation → alte Reviews STALE. |
| C02 HOCH — Quelle nach Prüfung geändert | prepare → drei PASS → `source.md` verändern → release | `COMPLETED` | Quellen als unveränderliche Reviewinputs archivieren und hashen. Soll die aktuelle Quelle gelten, deren Revision vor Commit erneut prüfen. Geänderte relevante Quelle muss STALE_SOURCE/REVIEW_REQUIRED ergeben. |
| C03 HOCH für Einmalversand — freie Outboxkeys | Derselbe Run, Actor mit notify: reserve_notification(key=`one`), danach key=`two`) | `[True, True]` | Kanonischen Schlüssel serverseitig aus logischem Auftrag/Pilot, Kanal, Empfänger und Nachrichtentyp bilden, UNIQUE erzwingen. Clientwahl darf die semantische Deduplizierung nicht umgehen. Dies reproduziert zwei Reservierungen, keine zwei echten Mails. |
| C04 HOCH für Recovery — Teilwrite | Nach submit Datei `<run>.md` mit ersten 20 Bytes des richtigen Reports anlegen; Kernel neu öffnen; identisches result wiederholen | `ARTIFACT_CONFLICT`; DB bleibt `RUNNING` | Teilwrite als Crashzustand modellieren: temporäre Datei, fsync, atomare Veröffentlichung und Recoveryjournal. Verwaistes Teilstück nach dokumentierter Prüfung isolieren/erhalten; nicht blind überschreiben. Wiederanlauf mit identischem Inhalt muss gezielt abschließen oder sichtbar RECOVERY_REQUIRED melden. |
| C05 MITTEL — Statussemantik fehlt | Gültiger Report, aber `status: FAILED` statt RESULT; result() | `RESULT_VERIFIED` | Erlaubte Metadatenwerte und Ergebnisart prüfen. RESULT_VERIFIED derzeit höchstens Speicherung/Quellreferenz geprüft; darf nicht als bestandene Fachprüfung gelesen werden. Alternativ ausdrücklich ARCHIVE_VERIFIED nennen und inhaltlichen FAIL separat binden. |

C01 zeigt mehr als die ehrlicherweise ausgelagerte Authgrenze: selbst bei korrekt authentifizierten Rollen kann der Gatevertrag das falsche Reviewobjekt akzeptieren. `bundle_hash` ist derzeit ein beliebiger, vom Caller übergebener String, kein berechnetes Manifest. C02 kann auch bei unverändertem Code/Report auftreten. Nachträgliche Quellenänderung ist nicht automatisch ein Fehler, wenn eine unveränderliche historische Kopie ausdrücklich Reviewobjekt wäre; genau diese Kopie fehlt hier. Der aktuelle Kern bewahrt nur Bericht und Digest, nicht vollständige Quellinputs.

Weitere statische Grenzen, **nicht als zusätzlich ausgeführte Gegenfälle zählen**:

- `_guard()` prüft geladene Policydatei, teilweise vor der DB-Transaktion; eine Änderung danach oder an Quelldateien außerhalb der DB kann noch zwischen Prüfung und Wirkung erfolgen. Alle relevanten finalen Guards müssen an derselben kontrollierten Commitgrenze gelten; lokale Dateirechte bleiben Teil des Vertrauensmodells.
- `resolve_policy()` prüft genau ein Parent-/Child-Paar und Grants sowie einige geschützte Felder. Keine rekursive Rootauflösung, Mehrknotenzyklen, TTL, Datenklassen-/Zielrestriktionen oder Integration des Resolveroutputs in Kernelstart nachgewiesen. Parenthash ist Hash sortierter JSON-Serialisierung, Kernelpolicyhash Hash der Rohbytes: beide Hasharten müssen ausdrücklich benannt werden, sonst entstehen Verwechslungen.
- ACK/VERIFIED akzeptieren einen beliebigen nichtleeren Evidence-String vom Empfängerstring. Keine Signatur, zugestellte Nachricht, Frist oder Inhalts-/Versionsbindung wird geprüft. Reviewers und Human sind ebenfalls nur Strings aus Grants. Der Modulkopf sagt korrekt, dass Caller-Authentifizierung extern liegt; der reale Authadapter ist aber nicht vorhanden. Eine API, die frei `actor='human-test'` übernimmt, wäre kein Human Gate.
- SQLite schützt nur Writes dieser einen Datenbank. Lokale Dateien und DB sind für entsprechend privilegierte Hostprozesse weiterhin veränderlich; DB-Events sind nicht technisch unveränderlich. Kein Schutz aller externen Direkttools. Kein Drive-Front/Log-Adapter, globaler Indexresolver, Capability-TTL-/Budgetgate oder unabhängiger Watchdog enthalten.
- Ein Outboxeintrag beginnt vorsichtig mit OUTCOME_UNKNOWN und blockiert denselben Key nach Restart; das ist sinnvoll. Es fehlen aber ein belegter Providerabgleich, tatsächliche Senderexklusivität und Scope-/Empfängerbindung. SENT entsteht durch einen freien Receiptstring.

Keine dieser Grenzen wird durch 15/15 Tests widerlegt. Die Suite prüft relevante Positiv- und Negativfälle, aber beispielsweise nur einen Crash **nach vollständigem** Artifactwrite, nicht mitten im Write. Ein grüner Testsatz ist weder vollständige Anforderungsdeckung noch 100%-Reliabilität.

## Vollständige Anforderungszuordnung R01–R25

Basis ist die bereitgestellte Matrix aus dem vollständig verfügbaren Chatkontext; abgeschnittene andere Chats sind ausdrücklich nicht vollständig erschlossen. Hier wird ihr eingefrorener Zwischenstatus aktualisiert, ohne unbekannte spätere Erledigungen zu erfinden.

| Req | Stand nach RUN 4 | Verbleibender Schritt / Blocker |
|---|---|---|
| R01 eine versionierte AIM-Liste | IN_PROGRESS laut Matrix; kein fertiger Inhalt vorgelegt | Eine Datei mit Abschnitten anlegen/lesen/verifizieren, keine zweite Inbox. |
| R02 stabile Konzepttickets / Historie | IN_PROGRESS | Ticket-ID, Ursprung, Status, Änderungen; auch verworfen/umgesetzt erhalten. |
| R03 erste Idee Minimalpromptprüfung | IN_PROGRESS | Ersten konkreten AIM-Eintrag mit Hypothese, kleinstem Kontext, Vergleichstest und Lebenszyklus. |
| R04 Shared Understanding / Sprache | dokumentiert, nicht erzwungen | Abnahmesätze in WorkOrder und Gateobjekt binden; Schema allein genügt nicht. |
| R05 Raw-UTF8-MD | beobachtete Session-/Pilotbelege | Keine globale Fremdruntimegarantie; Archivierung künftig auch Inputs mit Datenfilter. |
| R06 Syntax / Zeit / Version / Log | neue Cloudberichte berichtet; lokale Reviewnamen sind explizite Reviewartefakte | Bestehende Dateien nicht pauschal migrieren. Neue veröffentlichte WORK-Dateien nach aktueller Syntax. |
| R07 Read first / Ergebnis speichern | beobachtete Läufe teilweise belegt | Exklusiver Werkzeugpfad und Fremdruntimeintegration fehlen. |
| R08 Folder.md je Ordner | WORK und Registry berichtet | Weitere Ordner nicht inventarisiert/installiert; schrittweiser Rollout. |
| R09 Vererbung | Childmetadaten berichtet; Paarresolver lokal | Rekursive Bindung, Ausnahmen/Widerruf, finaler Commitguard offen. |
| R10 vollständige Historie / Baseline | bestehende Snapshots; lokale Events | Historische Dublette annotieren; Manipulationsschutz/Recovery nicht global. |
| R11 quantitative DELTA-Kriterien | Vertrag vorhanden | Vergleichbare Referenzsätze/Nenner und echte Messungen; keine geschätzten Scores. |
| R12 Dispatcher / Bridge / Kern | lokaler Kern plus berichtete Router/CI | C01–C05 beheben; privilegierte Adapter und Deployment nicht vorhanden. |
| R13 Hintergrundpflege / Sync | Stundenplan und Pilot berichtet | Watchdog/Frische/Retry; OneDrive→GitHubproduktiver Sync unbewiesen. |
| R14 drei Fachreviews | drei vollständige Dateien tatsächlich gelesen | Erfüllt für alten Freeze und Tasktrennung, keine fremden Accounts/Modelle belegt. |
| R15 sequenziell drei + separate vierte Instanz | Reihenfolge beauftragt, drei Outputs vor RUN 4 vorhanden; dieser Task real | Vollständiges Modellfenster/Providerdiversität nicht nachweisbar. |
| R16 DELTA / Re-Review / Human Gate | Konsolidierung hier; neue Gegenfälle geliefert | Korrekturen, gleicher neuer Freeze, erneute drei Perspektiven und gebundene Humanentscheidung offen. |
| R17 separate Registry / Rollen | Draft/PR18 berichtet | Humanmapping und authentifizierte Accounts noch ungeklärt. |
| R18 Capabilityumfrage / Trouble | vorbereitet, kein Antwortbeleg | Betroffene Accountnutzer müssen tatsächliche Proben/ACK liefern. |
| R19 Routing / Kapazität / Budget | Entwurf | Keine deployte Automatik; UNKNOWN-Quotas nicht als frei buchen. |
| R20 versionierter GitHubstand | PR18 berichtet; lokaler Kern uncommitted laut Evidenz | Code/Tests/Konsolidat als Reviewdelta versionieren, Herkunfts-/Mastervertrag erhalten. |
| R21 sichtbare Benachrichtigung / Pilot | Mailtransport gestützt, Pilot beobachtet | Task-Chatoutput konkret beilegen; Geräteanzeige/Lesen/ACK unbewiesen. |
| R22 Methoden / offizielle URLs | laut Matrix DONE; S03 enthält Actions/Temporal/LangGraph | n8n-Beleg nur als Matrixbehauptung hier; keine neue URL-/Aktualitätsprüfung. |
| R23 Pace Layers | L0–L5 dokumentiert | Änderungs-/Widerrufsregeln praktisch testen; keine neue Ontologie nötig. |
| R24 prüfen / korrigieren / erneut prüfen | tatsächlich 15 Tests + fünf Gegenfälle | Nächster Delta muss Gegenfälle schließen; externe Blocker weiter sichtbar. |
| R25 Quellen statt Memory | alle neun Quellen hier vollständig gelesen | Nachweise gelten nur für die gelesenen Hashes; abgeschnittene Chats bleiben unbekannt. |

Die Matrix verhindert insbesondere, dass ein bestandener Pilot die fehlende AIM-Liste, Capabilityantworten, Codeintegration, Re-Review oder Folderrollout unsichtbar macht. Von 25 Zielen darf keine pauschale Completionquote abgeleitet werden: Ziele haben unterschiedliche Abnahmekriterien und teilweise berichtete statt reproduzierte Nachweise.

## Drei wesentliche nächste Änderungen

**1. Review- und Freigabeobjekt versiegeln, lokale Recovery korrigieren.** Den vorhandenen Kern gezielt erweitern, keine neue Agentenplattform. Resultatmanifest berechnen und nach Ergebnisprüfung festschreiben; Quellen/Schemas/Code/Teststand/Policy/Abnahmeanforderungen einbeziehen. Reviews erst darauf; Änderungen invalidieren relevante Reviews. Partialwrite-Recovery samt sichtbarem Zustand ergänzen; Metadatenstatus und kanonischen Outboxkey prüfen. Akzeptanz: C01–C05 werden zu benannten Regressionstests mit vorher dokumentiertem Soll, 15 bestehende Fälle bleiben grün. Einen Test nicht durch Umbenennen des Ziels „grün“ machen.

**2. Einen tatsächlichen privilegierten Pfad anbinden.** Enger WORK-Writer, dessen Credentials andere Worker nicht direkt besitzen; authentifizierter Principal aus vertrauenswürdigem Session-/Servicekontext. Humanentscheid, ACK und Reviewreceipt an Manifest/Aktion/Ziel/Ablauf binden. Ein Storeadapter für Bericht→Archiv→Log→Folder mit dauerhaften Phasenreceipts; Drift/Widerruf vor finaler Wirkung. Outboxschlüssel und Providerabgleich implementieren. Akzeptanz: erlaubter Auftrag erfolgreich, falscher Principal/Ziel/Tenant/abgelaufene Freigabe abgelehnt, Crash an jeder Adaptergrenze wiederaufnehmbar, konkurrierender Writer ohne Lost Update. Hostzugriff und Credentialverwaltung sind hierfür reale Voraussetzungen.

**3. Verbleibende Nutzerziele als einen überprüfbaren Abschlusslauf liefern.** AIM mit R01–R03 fertigstellen; diese Matrix/Findingliste als fortgeführte Quelle nutzen; kanonische Einstiegsregeln markieren; vollständigen Chat-/Mail-/Index-/ACKnachweis je geforderter Dimension führen. Einen benannten unabhängigen Fristprüfer sowie maximale Staleness und Retrybudget einsetzen. Danach neuen Gesamtfreeze bilden, Delta plus relevante Gegenfälle drei Perspektiven erneut prüfen lassen, Ergebnis konsolidieren und konkrete Humanentscheidung einholen. Fremdaccountproben und Gerätebestätigung dürfen als offene externe Tickets stehen bleiben; die lokal ausführbaren Teile können vorher erledigt werden.

Minimaler Datenvertrag für diese Änderungen: WorkOrder mit task_key, erwarteter Policy und erforderlichen Abnahmedimensionen; versiegeltes Resultatmanifest; Runjournal mit erwarteter Revision und Phasen; Auth-/Review-/ACK-/Humanreceipts; kanonische Outbox. Folder.md bleibt lesbare aktuelle Projektion; die autoritative Commitstelle und der Master je Objekt müssen explizit sein. LLM erstellt Vorschläge/Reports, deterministischer Kern entscheidet erlaubte Übergänge.

## Konkrete Abnahmefälle für das Delta

| Fall | Erwartete beobachtbare Entscheidung | Heutiger Status |
|---|---|---|
| Reviews vor Resultat / Resultatmanifest verändert | REVIEW_NOT_READY bzw. STALE; kein Release | C01 reproduziert unzulässigen Abschluss |
| Quelle nach Resultat verändert | immutable Snapshot gültig belegt oder STALE_SOURCE | C02 reproduziert Abschluss ohne beides |
| Zwei Notifykeys, ein semantischer Zustellauftrag | eine Reservierung; Wiederholung gibt gleichen Receipt | C03 zwei Reservierungen |
| Crash nach 1 Byte, nach fsync, vor/nach DBcommit | eindeutiger Recoverypfad, keine verlorene/duplizierte Wirkung | vollständiger Write getestet; Teilwrite C04 offen |
| Fehlendes Archiv / Frontmatter / Index / ACK | gesonderter Blockgrund; kein uneingeschränkt COMPLETED | Archiv/Metadaten/fehlender Handoff lokal teilweise getestet; globaler Index nicht implementiert |
| Quellen-/Tenant-/Ziel-/Principalfälschung | DENY vor externer Wirkung | nur unbekannter String lokal abgewiesen; externe Auth NOT_RUN |
| Scheduler migriert, läuft tatsächlich | gelesene Folder-ID/Policy und tatsächlicher Chatoutput | Pilotbericht stützt Migration; Chatoutput beilegen |
| Zwei Hostwriter / abgelaufener Worker | höchstens ein gültiger Commit, alter Worker DENY | lokales SQLite-Rennen PASS; externe Host-/Drivegrenze NOT_RUN |
| Provider nimmt Mail an, Receipt verloren | UNKNOWN, Abgleich statt blindem Retry | nur lokaler gleicher Outboxkey nach Restart PASS |
| Kontrollpolicy geändert ohne Fachdelta / Audit bleibt aus | Kontrollalarm bzw. Stalealarm ohne Endlosschleife | NOT_RUN |
| Neuer Code nach drei Reviews | alter Freeze als ungültig für neuen Release erkannt | prozessual benannt, technisch unvollständig |

## Exakte externe und menschliche Blocker

| Blocker | Wer oder welche Berechtigung tatsächlich fehlt | Was ohne diesen Zugriff weitergeht |
|---|---|---|
| Fremdaccountcapabilities und Ace-/Gemini-Probleme | Betroffene Business-/Privat-/Gemini-Session, ggf. Workspaceadmin/Graphowner; reale Probe im freigegebenen Testziel | Umfrage/Adapter/Fehlerreceipt vorbereiten; keine Impersonation und keine Datenbrücke zur Policyumgehung. |
| Authentifizierte Rollen- und Humanzuordnung | Julian entscheidet kanonisches Mapping; Host-/Gatewaybetreiber bindet es an verifizierte Identität | Keine automatische Umnummerierung; Fixturetests und Rollenaliases erhalten. |
| Exklusiver Drive-/Releasepfad | Deployment-/Credential-/ACLkontrolle beim Host/Servicebetreiber; bestehende direkte Schreibpfade begrenzen | Lokaler Kern kann gehärtet und getestet werden; kein weltweiter Gateanspruch. |
| Humanfreigabe des korrigierten Vertrags | Explizite Entscheidung Julians auf neuem Manifest nach Delta/Re-Review | Konkretes prüfbares Releasepaket vorher vollständig vorbereiten; LLM setzt die Freigabe nicht selbst. |
| Gerätepush und echtes Lesen/ACK | Nutzergerät/Browserbenachrichtigungsrechte bzw. Bestätigung des tatsächlichen Empfängers | Mailannahme/Metadaten getrennt ausweisen; Versand nicht wiederholen, um ACK zu erzwingen. |
| Vollständige abgeschnittene andere Chats | Originalexport oder befugter Zugriff auf diese Originale | Verfügbare 25 Anforderungen abarbeiten; keine universelle Vollständigkeitsbehauptung. |
| Nachgewiesener OneDrive→GitHubsync / weiterer Rollout | Reale installierte Bridge, Hostzugriff, Scheduler-/Zielallowlist und freigegebener Scope | Engen Adaptertest und Inventar planen; keine Mountpfade als zugängliche Cloudsysteme ausgeben. |

Nicht jeder offene Punkt braucht eine neue Erlaubnis: lokale Fehlerkorrektur, AIM-Erstellung, Regressionstests und reviewfähiges Paket sind ausführbare Arbeit innerhalb des bestehenden Auftrags. Echte Fremdanmeldung, Freigabeidentität, Zugriff auf Nutzergeräte und Entscheidung des Human Gate können dagegen nicht aus einem Markdownstring hergestellt werden.

## Getrenntes Schlussurteil

| Ebene | Entscheidung von RUN 4 |
|---|---|
| Konzept | Weiterentwicklung sinnvoll. Gemeinsamer Vertrag und kleiner deterministischer Kern sind die richtige nächste Konkretisierung. Keine neue allgemeine Architektur nötig. |
| Enger Pilot | Normaler Speicher-/Mailpfad nach Postfreeze beobachtet und teilweise zusätzlich gestützt. Keine unabhängige vollständige Acht-Kriterien-Abnahme; ACK, Crash-/Konkurrenz-/Ausfallfälle offen. Beaufsichtigter Fehlerpilot und gezieltes Refinement sinnvoll. |
| Vertragsrelease / Produktion / breiter Rollout | BLOCKED. Neue Codegegenfälle, fehlende externe Auth-/Exklusivgrenze, Recoveryadapter, Fristbeobachtung, aktuelle Re-Reviews und gebundene Humanentscheidung bleiben offen. |

Diese vierte Prüfung konsolidiert tatsächlich vorliegende drei Reviews und prüft zusätzlich den neuen lokalen Code. Sie erklärt weder alle Ziele für erledigt noch eine absolute Zuverlässigkeit. Besonders wichtig ist die Reihenfolge: ausführbare lokale Lücken schließen, neuen Stand einfrieren, Auswirkungen erneut prüfen, erst dann konkrete Freigabeentscheidung.


## Abschlussreceipt

Beobachteter Abschluss der Berichtserstellung: **2026-10-16T15:28:31Z**. Vollständiger lokaler UTF-8-Readback durchgeführt; R01–R25, K01–K10 und C01–C05 vorhanden. Drei Vorreviews und neun Originalquellen vollständig gelesen; Originalmanifest und neun Einzelhashes stimmen. Lokaler Kern und Tests unverändert zum oben bezeichneten Hash. Die Korrekturen sind Folgearbeit, nicht in diesem Review bereits als behoben bewertet.
