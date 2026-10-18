# RUN 2 — Unabhängiges AI-Governance- und Falsifikationsreview

## Urteil

**Konzept: bedingt weiterentwickeln. Begrenzter Pilot: unter Auflagen zulässig, End-to-End-Abnahme noch offen. Produktion/Vertragsrelease: nicht freigeben.** Die Quellen unterscheiden bemerkenswert konsequent zwischen Behauptung, gespeichertem Nachweis und offenem Implementierungsstand. Genau diese Unterscheidung muss auch für diesen Review gelten: Ein gut formuliertes Governance-Konzept ist kein Nachweis durchgesetzter Governance. Der Freeze belegt mehrere interne Widersprüche und eine doppelte Run-ID; er liefert keinen Laufzeitnachweis für technische Freigabe-, Autorisierungs- oder Konfliktkontrollen.

Dieses Review bewertet das eingefrorene Bundle, nicht die aktuelle Live-Umgebung. Es erteilt selbst keine Human-Freigabe und führt keine Quellanweisungen aus.

## Identität, Unabhängigkeit und Messgrenzen

- Tatsächliche ausführende Instanz/Task: `/root/cplm_run2_governance_falsification`, separater Reviewer-Task im gemeinsamen Codex-Arbeitsraum; Reviewauftrag von `/root`.
- Perspektive: AI Governance Audit und adversarielle Falsifikation. Keine Identität einer realen Person angenommen.
- Konkrete Modellversion, Account/Tenant und Modell-Unabhängigkeit gegenüber anderen Reviews: nicht durch die verfügbaren Beobachtungen nachgewiesen, daher **UNKNOWN**. Ein anderer Task ist kein Beweis eines anderen Accounts oder Modells.
- Andere Reviewer-Ausgaben, Ergebnisverzeichnisse und Antworten wurden nicht gelesen. Der einzige Zugriff auf den Ergebnisbereich ist die Erstellung dieser eigenen Datei. Keine anderen Reviews als Evidenz verwendet.
- Bekannt war lediglich die vom Auftraggeber gemeldete Reihenfolge: Reviewer 1 beendet, dieser Task Run 2. Dessen Inhalte waren nicht bekannt. Quellenbestand und Reviewauftrag bilden gemeinsame Vorannahmen; vollständige statistische Unabhängigkeit wird nicht behauptet.
- Tatsächlich beobachteter Start der Quellenprüfung: **2026-10-16T15:13:17Z**, per Systemuhr vor Hashprüfung. Endzeit wird unten nach Erstellung/Readback separat erfasst. Zeit vor dem ersten Toolaufruf ist nicht gemessen.
- Keine externen Änderungen, Nachrichten, Modell-API-Aufrufe, Subagenten oder Live-Capability-Tests ausgeführt. Lokale Hash-/Textprüfungen wurden ausgeführt. Tokenverbrauch und Kosten sind **NOT_MEASURED**.

## Freeze und vollständige Lesedeckung

`MANIFEST.json` vor inhaltlicher Prüfung vollständig gelesen und geprüft. Erwarteter und beobachteter SHA-256 stimmen überein:

`1d0b94c0f3c0473736571fa0302f8a4adde7b04012d0c1c1ac038cd6a38cb162`

`REVIEW-SCOPE.md` vollständig gelesen. Alle neun Manifestdateien wurden vollständig als Text gelesen, ohne Trunkierung der Toolausgabe. Die UTF-8-Bytes wurden lokal separat gehasht. Bei S08/S09 sind vorhandene BOM/CRLF Teil des Bytebestands; die Zeichenzählung beruht auf UTF-8-Dekodierung ohne Newline-Normalisierung. Insgesamt **62.660 Zeichen**.

| Quelle | Datei | Zeichen | Beobachteter SHA-256; Manifestvergleich |
|---|---|---:|---|
| S01 | Folder.md | 1.972 | c399b1f42b806e34cb637b4c249a41a77ca56f8e17a35eacdaf2546c0e1a243f — PASS |
| S02 | Golden-Slice-Pilot.md | 4.539 | 731cb1d36707fdf09d1760a730f1da84927761e034129d935246f2921cabb87c — PASS |
| S03 | CPLM-Regeln-v0.3.md | 10.239 | e5989a79cbba8bf92fb5e976ee359270d108b2f5000477e0aabe058fd4972131 — PASS |
| S04 | Folder-Governance-v0.1.md | 2.923 | 839acb90260f6df0ec9a741660a4a317dce11dfd12b14f604554e53531726854 — PASS |
| S05 | LLM-Registry-v0.1.md | 13.205 | 0142a7f788c3fd3a6adf97b9b1a136cfafbc2b1501e244bd0cac8c1737ea2614 — PASS |
| S06 | Audit-WORK-R0002.md | 3.469 | 95cf799a90fd82c992d6643ee7e25422d118d3c4575f54ba76008f85113358e7 — PASS |
| S07 | WORK-FRONT-LOG.md | 9.314 | 5a38fd08305b54e9d733d77a3bb2104a6c1a99df7ac926066c39c93b017736d5 — PASS |
| S08 | WorkOrder-Feedback-Archive-Capability.md | 2.138 | 47eba0fc99514effa4d5826f69f8ea4ac27f5e476ab8aebdecbbd1bb2275ca4b — PASS |
| S09 | NEXUS-ECOSYSTEM-CONCEPT.md | 14.861 | 0a5ac2565bfe7af61a9562158f4705ec64f464664832188379d81e7b48a7d351 — PASS |

Diese Prüfung bestätigt Übereinstimmung mit dem bereitgestellten lokalen Manifest. Sie authentifiziert nicht eigenständig den ursprünglichen Autor, Drive-Revisionsstand oder Connectortransport. Verlinkte Quellen außerhalb der neun Dateien wurden nicht geöffnet. Aussagen über Scheduler, PR18, Drive-Zugriffe und frühere Tests bleiben hier quellenberichtete Beobachtungen.

## Maßstab

**KRITISCH** bedeutet möglicher unautorisierter Release oder privilegierter Seiteneffekt; **HOCH** gefährdet wesentliche Nachvollziehbarkeit oder Gateentscheidungen; **MITTEL** verursacht begrenzte Fehlklassifikation, Unklarheit oder Betriebsrisiken. Eine hohe Schwere bedeutet nicht, dass ein Angriff beobachtet wurde. Bei nicht implementierten Kontrollen ist es ein Releaseblocker, kein behaupteter Live-Exploit.

Popper-orientierter Maßstab: Eine Aussage muss Gegenbedingungen, messbare Entscheidungskriterien und mögliche Widerlegung zulassen. Ein bestandener Einzeltest widerlegt einen konkreten Fehlerfall, beweist aber keine universelle Zuverlässigkeit. Selbstberichte über Tests werden nicht zu hier reproduzierten Tests umetikettiert.

## Unabhängige Findings

### R2-G01 — Privilegierter Ausführungspfad ist nicht kontrolliert
**Schwere: KRITISCH für Produktion. Quellen:** S03 §4–5; S05 §1, §5, §8 REG-TB-006; S04 „Implementation state“.

START_GATE/COMPLETION_GATE und die ausschließliche Erreichbarkeit privilegierter Werkzeuge durch diese Gates sind richtig beschrieben, aber ausdrücklich nicht implementiert. Der Freeze liefert somit keinen Nachweis, dass fehlende Policy-Receipts, Autorisierung oder Review eine Schreib-/Releaseaktion verhindern. „Adoptierte Regeln“ und konfigurierte Prompts dürfen nicht als verbindliche Laufzeitpolitik vermarktet werden.

**Gegenbeispiel:** Ein Worker besitzt direkt ein Drive-Update- oder GitHub-Merge-Werkzeug und schreibt nach fehlgeschlagenem START_GATE trotzdem. Ein kooperativer Prompt stoppt den unkooperativen Pfad nicht.

**Widerlegungstest:** In isoliertem Testziel ohne gültiges Receipt über jeden privilegierten Werkzeugpfad schreiben/Release auslösen. Erwartet: serverseitiges DENY vor Seiteneffekt, mit korrelierter Audit-ID. Ein erfolgreicher Write widerlegt „Gate kann nicht umgangen werden“. **Hier beobachtet:** fehlende Implementierung in S05 explizit offengelegt; kein solcher Lauf. **NOT_RUN:** Umgehungstest.

**Minimale Verbesserung:** Für den Pilot nur eng autorisierte Testziele und einen verantwortlichen Writer; vor Produktion privilegierte Credentials ausschließlich am validierenden Gateway halten und direkten Schreibzugriff entziehen.

### R2-G02 — Regelvorrang ist lesbar, aber nicht eindeutig ausführbar aufgelöst
**Schwere: HOCH. Quellen:** S02 „Geltende Pilotregeln“; S03 §1 Nr.4–5, §2, §9; S04 Rule 002–004; S05 §4 Frage 4; S09 Abschnitte „syntax“, „CUSTOM-INSTRUCTIONS“; REVIEW-SCOPE.

Im aktuellen Pilot soll exakt `Folder.md` gelten. S03 verlangt weiterhin `_FRONT.md`, S04 `FOLDER.md`; S05 fragt noch `_FRONT.md` ab. S04 verlangt getrennte AIM-Inbox und AIM, S02 dagegen eine AIM-Datei. Das Override ist für diesen Pilot dokumentiert, aber keine vollständige maschinenlesbare Konfliktauflösung für alle Nachfahren/Worker vorhanden. Der Scope berichtet einen noch auf `_FRONT.md` gerichteten Scheduler. S09 enthält ältere Memory- und Formatvorgaben, die den späteren Evidenz- und Schreibregeln widersprechen. Ein Dokumenttitel oder jüngerer Zeitstempel ist keine ausreichende Autoritätsentscheidung.

**Gegenbeispiel:** Namensbasierter Worker sucht `_FRONT.md`, findet die umbenannte Datei nicht und erzeugt einen zweiten Statusmaster; ein anderer nimmt `FOLDER.md` als gleichwertig. Beide behaupten Regelkonformität.

**Test:** Dasselbe Bundle an einen Resolver mit allen drei Namen und zwei AIM-Regeln geben. Erwartet: genau eine effektive Policy mit Herkunft je Regel, expliziten Overrides und einer kanonischen Einstieg-ID; unbekannter Vorrang führt BLOCKED. **Beobachtet:** textuelle Widersprüche und Scopehinweis. **NOT_RUN:** Schedulerlauf/Resolver.

**Minimal:** Effektive Policy aus Versionen/Hashes und expliziten Override-IDs bilden; Scheduler und Capability-Umfrage auf kanonische ID migrieren, alte Namen als nicht schreibbare Weiterleitung behandeln. S03/S04 als teilweise überholt markieren, ohne Historie zu löschen.

### R2-G03 — Human-Autorität ist noch kein authentifiziertes Freigabesignal
**Schwere: KRITISCH für Produktion. Quellen:** S01 owner/next_action; S02 human_authorization; S03 §1, §4; S05 Frontmatter, §2–5, §10; S09 Rollenliste ID-01 bis ID-10.

Die Registry trennt Human, Rolle, Account und Instanz sachgerecht und meldet den Nummernkonflikt. S09 ordnet ID-03 Gemini zu, neuere Artefakte verwenden ID-03 für ChatGPT-Codex; der referenzierte Repovertrag wird als QA-Rolle ID03 beschrieben. Zugleich nutzt der Freigabevertrag ID01. Nicht festgelegt ist, welches authentifizierte Principal eine gültige ID01-Freigabe erzeugen darf und wie dieser Nachweis transportiert/verifiziert wird. Das Feld `human_authorization` ist ein Bericht über einen Nutzerauftrag, kein eigenständiger kryptografischer oder plattformseitiger Autorisierungsnachweis.

**Gegenbeispiel:** Agent schreibt „ID01 genehmigt“ ins Frontmatter oder Broker verwechselt eine Rolle mit Human-Account. Werkzeugrechte können technisch vorhanden sein, ohne dass die konkrete Aktion genehmigt ist.

**Test:** Freigabe mit gefälschtem role_claim, falschem Tenant, alter Session sowie korrekter Person aber falschem Ziel einreichen. Erwartet DENY; nur verifiziertes Principal plus Umfang/Aktion/Version/Ablauf gültig. **Beobachtet:** Konflikt offen dokumentiert. **NOT_RUN:** Authentifizierungs-/Autorisationstests.

**Minimal:** Unveränderlichen Human-Principal und erlaubten Freigabekanal festlegen; historische Labels als Aliase erhalten. Jede provisorische Zulassung an einen expliziten Auftrag und Ablauf binden. Keine automatische Umnummerierung.

### R2-G04 — Freigabe und Review sind nicht ausreichend an unveränderliche Versionen gebunden
**Schwere: HOCH. Quellen:** S03 §3–4; S05 §5–6; S02 „Unabhängige Prüfung“; S01 artifacts.

Gleicher Freeze für drei Reviews ist ein guter Anfang. Nicht spezifiziert sind vollständiges Releaseobjekt, Gültigkeitsdauer, Ablauf bei Mutation und Bindung der Human-Freigabe an exakt denselben Artefakt-/Policy-/Teststand. Drive-ID und Versionslabel allein sind veränderlich. Der hier vorliegende Manifesthash verbessert das Review, ersetzt aber noch keinen nachgewiesenen Releasecontroller.

**Gegenbeispiel:** Drei Reviewer billigen Stand H1; danach verändert ein Agent eine Policy oder ein Zielartefakt unter gleicher Datei-ID/Versionszeichenfolge. Eine allgemeine ID01-Freigabe wird auf H2 angewendet.

**Test:** Nach Reviews ein Byte, Parentpolicy oder Zielumfang ändern und alte Freigaben erneut anbieten. Erwartet STALE/REVIEW_REQUIRED, Release verweigert. **Beobachtet:** Hashpraxis und Reviewspezifikation; keine unveränderliche Releasebindung. **NOT_RUN:** Mutations-/Replaytest.

**Minimal:** Release-Manifest mit Hashes von Artefakten, effektiver Policy, Tests, Reviews und Parentauflösung. Review und Human-Gate adressieren dessen Hash. Mutation invalidiert betroffene Genehmigungen.

### R2-G05 — Unabhängigkeit braucht ein prüfbares Kriterium und ehrliche Reichweite
**Schwere: HOCH. Quellen:** S03 §4; S02 „Unabhängige Prüfung“; S05 §7.

Drei Rollen desselben Autors zählen zu Recht nicht. Offen bleibt, welche gemeinsame Herkunft für drei tatsächliche Instanzen akzeptabel ist: gemeinsamer Autor-Kontext, Account, Modell, Prompt, Tools oder Trainingsfehler. Fremdaccounts allein beweisen ebenfalls keine inhaltliche Unabhängigkeit. Sequentielle Durchführung kann unabhängig vom Ergebnisinhalt sein, wenn frühere Ergebnisse verborgen bleiben; sie ist keine Garantie unkorrelierter Fehler.

**Gegenbeispiel:** Drei neue Tasks erben die Argumente und Schlussfolgerungen des Autors. Formal verschiedene instance_ids liefern dieselbe vorgeprägte Freigabe. Ebenso können drei Provider dieselbe falsche Referenz übernehmen.

**Test:** Review ohne vorherige Ergebnisse, mit dokumentiertem Inputmanifest, Kontextfreigabe, eigener Befundbildung und Interessenkonflikt-/Autorzuordnung; absichtlich widersprüchliche Testbehauptung im Bundle auf Entdeckung prüfen. Erwartet nachvollziehbare individuelle Findings; bloßer Rollenwechsel abweisen. **Beobachtet:** dieser Task hat keine anderen Reviewausgaben gelesen; Account-/Modelltrennung UNKNOWN. **NOT_RUN:** unabhängige Prüfung der Erzeugung aller Reviewer und des vollständigen Reviewverfahrens.

**Minimal:** Unabhängigkeitsprofil vor Reviewbeginn definieren: anderer ausführender Task, kein Zugriff auf Vorreviews, keine Mitautorenschaft am geprüften Stand, gleiche Freezeinputs; Account-/Modellvielfalt separat berichten, nicht nachträglich als erfüllt deklarieren. Ob dies Julians Freigabeanforderung genügt, bleibt Humanentscheidung.

### R2-G06 — Vererbung und Autoritätsausnahmen haben keine vollständige Semantik
**Schwere: HOCH. Quellen:** S01 inheritance; S02 „Geltende Pilotregeln“; S04 Rule 002; S05 §5.

WORK als bewusst begrenzte Prüfungswurzel und Plattformrechte als harte Grenze sind vernünftig. S01 benennt zugleich einen Parent außerhalb WORK als NOT_LOADED. Das ist keine Feststellung, dass dort keine Verpflichtungen gelten. Nicht definiert sind effektive Policyberechnung, Parenthashbindung, Mehrdeutigkeit, Rootwechsel, veraltete Parentversion oder wie eine autorisierte Ausnahme begrenzt und widerrufen wird.

**Gegenbeispiel:** Child referenziert alte Parentversion mit erlaubtem Export; aktueller Parent verbietet Export. Oder eine ID01-Ausnahme in einem Child wird unbeabsichtigt auf dessen Geschwister übertragen. Scope-Verengung kann zudem scheinbar durch Entfernen der vom Verbot betroffenen Daten erfolgen.

**Test:** Fehlender Parent, Zyklus, Parentmutation, Childlockererlaubnis, Ausnahme für anderes Ziel und Rootwechsel. Erwartet reproduzierbare effektive Policy oder BLOCKED; kein Fallback auf „neueste gefundene Datei“. **Beobachtet:** fehlender Parent/Zyklus/Widerspruch sollen blockieren, Umsetzung nicht belegt. **NOT_RUN:** Resolver und Negativtests.

**Minimal:** Root als explizite Autoritätsgrenze genehmigen; Parent-ID plus Hash/Version pro Lauf fixieren; Ausnahmen enthalten Grantor, Regel-ID, Ziel, Aktion, Ablauf und Widerruf. Nicht geladene Vorfahren als Grenze jeder Complianceaussage ausweisen.

### R2-G07 — Konfliktprüfung per Wiederlesen verhindert TOCTOU nicht
**Schwere: HOCH. Quellen:** S02 Abnahme Nr.3,6 und „Bereits gefundener Fehler“; S03 §4; S07 beide Überschriften WORK-R0002; S01 baseline/last_run.

Die doppelte ID WORK-R0002 ist direkt nachweisbar. Darüber hinaus referenziert der aktuelle Frontzustand `previous_run: WORK-R0002`, während `last_run.id` ebenfalls WORK-R0002 ist. Das kann Folge des benannten Konflikts sein; eine eindeutige Vorgängerkante ist damit nicht belegbar. Ein Wiederlesen vor Update lässt weiterhin zwei Schreiber zwischen Read und Write konkurrieren. Quellen erkennen die fehlende Atomarität ausdrücklich an.

**Gegenbeispiel:** A und B lesen denselben Stand, beide sehen keinen Konflikt; A schreibt, danach B. Beide erhalten erfolgreichen Readback des jeweils eigenen Inhalts zu unterschiedlichen Zeitpunkten, A geht später verloren.

**Test:** Zwei Worker nach dem letzten Read synchron freigeben; zusätzlich Leaseablauf, Crash nach Log und Retry prüfen. Erwartet genau ein Commit, anderer BLOCKED/RECOVERY_REQUIRED, kein verlorener Zustand, eindeutige IDs. **Beobachtet:** zwei WORK-R0002-Überschriften per Textskript bestätigt; Selbstreferenz im Front per Textprüfung bestätigt. **NOT_RUN:** Konkurrenz-/Crashtest.

**Minimal:** Pilot seriell über einen Writer betreiben. Produktion braucht revisionsgebundene bedingte Writes oder einen transaktionalen Zustandsdienst, Lease mit Fencing und idempotente Phasen. Historische Dublette nicht umschreiben; getrennte Ereignis-IDs und Korrekturverweis ergänzen.

### R2-G08 — „Kein fachliches Delta“ kann Governanceänderungen ausblenden
**Schwere: HOCH. Quellen:** S06 „Beobachtungen“, „Ergebnis“; S01 next_action; S03 §3; S07 Registrierungs-Wegweiser und Migration.

Der frühere Auditzeitpunkt ist vor späteren Registry-/Pilotänderungen; diese sind nicht rückwirkend ein Auditfehler. Gefährlich ist jedoch die zukunftsgerichtete Regel, selbst erzeugte Audit-/Frontvorgänge generell aus dem Fachdeltasignal auszuschließen. Änderungen an Policy, Freigabe, Quelle oder Status können entscheidungsrelevant sein, unabhängig davon, wer sie erzeugt. Rauschunterdrückung darf Integritätsüberwachung nicht abschalten.

**Gegenbeispiel:** Agent entfernt BLOCKED aus Front oder lockert eine Regel im eigenen Auditbericht. Ein nachfolgender Lauf ignoriert den selbst erzeugten Vorgang und meldet „kein neues entscheidungsrelevantes Finding“.

**Test:** Semantisch irrelevanten Zeitstempel und separat Gate-/Policyänderung durch denselben Agenten erzeugen. Erwartet erstes als Rauschen, zweites als Governance-Delta und ggf. Freigabeinvalidierung. **Beobachtet:** pauschale Ausschlussformulierung; keine Implementierung geprüft. **NOT_RUN:** Deltaklassifikation.

**Minimal:** Fachdaten-, Governance- und Telemetriedelta getrennt führen. Selbstursprung nur als Herkunftsmerkmal verwenden; Policy-/Gate-/Provenienzänderungen immer prüfen. Stabile Vergleichsnenner erhalten.

### R2-G09 — Alte offene Findings können still veralten oder verschwinden
**Schwere: HOCH. Quellen:** S01 tasks/problems/next_action; S03 §3–4; S06 „Ergebnis“; S07 Historie; S05 §8.

Es gibt offene Punkte und eine gute DELTA-Schleife, aber kein verbindliches Finding-Lebenszyklusschema mit stabiler ID, Owner, Fälligkeit, betroffener Version, Closureevidenz und Wiederöffnung. Nur neue/geänderte Fachdateien zu prüfen reicht nicht, um alte Freigabeblocker aktuell zu halten. Status nach einem späteren erfolgreichen Einzeltest kann sonst historische Lücken verdecken.

**Gegenbeispiel:** Single-Writer-Lücke bleibt monatelang offen; kein neues Dokument ändert sich, daher wird kein Handlungsbedarf signalisiert. Oder Front lässt eine Problemzeile weg und die Konsolidierung behandelt sie als erledigt.

**Test:** Unverändert offenes kritisches Finding über mehrere Runs tragen, Quelle löschen/ersetzen und eine unbelegte Closure einreichen. Erwartet offener/überfälliger Zustand beziehungsweise STALE_EVIDENCE, keine stille Schließung. **Beobachtet:** offene Punkte erhalten, aber kein vollständiger Findingvertrag. **NOT_RUN:** Lifecycle-/Ablauftests.

**Minimal:** Eine Findingliste mit Status OPEN/ACCEPTED_RISK/FIXED_PENDING_RETEST/CLOSED/REOPENED, Quellhash, Verantwortlichem und Re-Testbeleg; Auflösung nur durch explizite Entscheidung, nicht durch Abwesenheit im neuesten Front.

### R2-G10 — Benachrichtigungsziel, Einwilligung und Zustellstufe sind unvollständig operationalisiert
**Schwere: MITTEL im engen Pilot, HOCH bei Ausweitung. Quellen:** S02 Abnahme Nr.7 und „Grenzen der Benachrichtigung“; S08 Übergabe-FSM; S05 §2–4.

Die Pilotmail ist laut Quelle ausdrücklich autorisiert und soll genau einmal an das authentifizierte Gmail-Konto gehen. Das rechtfertigt keine beliebigen späteren Empfänger oder wiederkehrende Nachrichten. `to: me` bindet an die tatsächliche Anmeldung, die Registry kennt deren Business/Privatzuordnung noch nicht. Die Quellen unterscheiden Versand von Anzeige/Lesen korrekt. Ein vorheriger Suchlauf und anschließender Send ist jedoch kein atomarer Exactly-once-Nachweis.

**Gegenbeispiel:** Zwei Worker finden keine Mail und senden beide; oder ein anderer authentifizierter Account empfängt den Bericht. Nach Timeout kann ein erfolgreicher Versand ohne Receipt zum Retry führen.

**Test:** Vor Versand nicht geheime Kontoprincipal-/Zielbestätigung, falscher Account, doppelte Ausführung und Timeout nach Send prüfen. Erwartet kein Versand bei falschem Ziel; persistente Deduplizierung; Status SENT/DELIVERY_UNKNOWN/ACK getrennt. **Beobachtet:** kein Versandbeleg im Freeze; Scope sagt keine Pilotmail gesendet. **NOT_RUN:** sämtliche Versand-/Empfangstests; hier keine Nachricht versandt.

**Minimal:** Empfängerprincipal und autorisierten Inhaltsumfang an Pilot-ID binden; Versandintention/Receipt und Retryregel persistieren. Bei unklarem Versandzustand nicht blind wiederholen. PILOT_PASS ausdrücklich als Send-Nachweis definieren oder ACK separat verlangen; fehlende Push-Schalterkontrolle als offene eigene Stufe halten.

### R2-G11 — Permission Boundary und Datenklassen sind noch nicht als Policy ausformuliert
**Schwere: HOCH. Quellen:** S05 §4 Fragen 6–8, §5–6; S01 source_of_truth/sync_rule; S08 G2; S09 SSOT-/Syncziel.

Die Registry verbietet Business-Policyumgehung durch private Accounts und öffentliche Graphinventare ausdrücklich. Das ist positiv. Nicht spezifiziert sind konkrete Datenklassen, freigegebene Ziel-IDs/Empfänger, Retention, Secretredaktion sowie Regeln für brokerseitige Delegation. „Alles aus jeder Sandbox archivieren“ aus S08 ist ohne Filter zu weit; Plattform-Schreibrecht allein erlaubt nicht jede Datentransferhandlung.

**Gegenbeispiel:** Ein technisch zugelassener Broker überträgt vertrauliche Business-Quellen in einen privaten Account oder einen öffentlich sichtbaren Review-Snapshot, weil dessen Write-Test erfolgreich war. Ein Archiv enthält Credentials aus Toolfehlern.

**Test:** Geheimnismarker/vertrauliche Datei über Inbox→Broker→GitHub/Testgraph leiten; falschen Tenant und nicht erlaubte Ziel-ID einsetzen. Erwartet vor Transfer DENY/Redaktion mit minimalem Auditbeleg; keine Daten im Ziel. **Beobachtet:** Grenzen benannt, konkrete durchgesetzte Klassifikation nicht belegt. **NOT_RUN:** Datenfluss-/Brokerprüfung.

**Minimal:** Kleine Allowlist aus Datenklasse×Ziel×Aktion×Principal, für Pilot nur unkritische Daten; Redaktionsregel und Retention ergänzen. Empfang von Markdown ist keine delegierte Autorisierung. Broker muss Herkunft und Rechte selbst prüfen.

### R2-G12 — Audit-E2E und Vollständigkeit müssen enger bezeichnet werden
**Schwere: MITTEL. Quellen:** S06 „Scope und Quellen“, Prüftabelle, „Grenzen“; S07 Status „Audit E2E belegt“; S02 Ziel/Abnahmekriterien; S03 §5.

S06 berichtet vollständige Pagination direkter Kinder und Readbacks. Die dazugehörigen API-Rohreceipts, Listinggrenzen und Liveobjekte sind nicht im Freeze. S07 bezeichnet Audit E2E als belegt, während S02 später einen umfassenderen Golden Slice einschließlich Benachrichtigung verlangt. Das ist nicht zwingend ein Widerspruch, weil unterschiedliche Prüfumfänge möglich sind; ohne namentlich abgegrenzte Testdefinition lädt es zur Übertragung eines engen Erfolgs auf den größeren Gesamtprozess ein. 230 Dateien und 17 Unterordner sind weder rekursive Inhaltsdeckung noch fachliche Prüfung aller Dateien.

**Gegenbeispiel:** Dashboard zeigt „E2E PASS“, obwohl Mail, ACK, Unterordner und Gatebypass nie getestet wurden. Ein Listing während Änderungen enthält bei Pagination fehlende oder doppelte Einträge, obwohl jede Seite erfolgreich war.

**Test:** Getrennte Test-IDs für Audit-Persistenz, Golden Slice, Übergabe-ACK und Produktionsfreigabe; Listing unter gleichzeitiger Änderung und mit fehlender Seite prüfen. Erwartet enges PASS nur für benannte Kriterien, ansonsten PARTIAL/NOT_RUN. **Beobachtet:** quellenberichtete Teilnachweise, klar benannte Rekursionsgrenze und offener Golden Slice. **NOT_RUN:** Listingwiederholung und Live-E2E.

**Minimal:** Status in `AUDIT_REPORT_STORAGE_PASS`, `GOLDEN_SLICE_NOT_RUN`, `RELEASE_BLOCKED` aufteilen; Inventarzeitfenster, Seitenbelege und Objekt-ID-Deduplizierung referenzieren. Einen Hash nie als inhaltlichen Richtigkeitsbeweis verwenden.

## Tatsächlich ausgeführte Prüfungen und ausstehende Versuche

| Test-ID | Erwartet | Tatsächlich beobachtet | Status |
|---|---|---|---|
| R2-T01 | Manifest gleich vorgegebenem Hash | Exakte Übereinstimmung | PASS |
| R2-T02 | Alle 9 Dateibytes gleich Manifest | 9/9 SHA-256 stimmen überein | PASS |
| R2-T03 | Alle Quellen vollständig lesbar | 9/9 volle Texte, 62.660 Zeichen plus Scope/Manifest | PASS |
| R2-T04 | Run-ID als Ereignisschlüssel eindeutig | Zwei unterschiedliche WORK-R0002-Überschriften in S07 | FAIL im Freeze |
| R2-T05 | Eindeutige Vorgängerreferenz | S01 last_run und previous_run beide WORK-R0002 | FAIL für eindeutige Kette |
| R2-T06 | Einheitlicher geltender Einstieg | Folder.md / _FRONT.md / FOLDER.md verteilt; Pilot-Override nur textuell | Inkonsistenz belegt; Runtime NOT_RUN |
| R2-T07 | Release ohne Pflichtgate abgelehnt | Kein Gatewaytest ausgeführt; Gates laut S05 unimplementiert | NOT_RUN / Releaseblocker |
| R2-T08 | Mutation invalidiert Genehmigungen | Keine Änderung am Input vorgenommen | NOT_RUN |
| R2-T09 | Konkurrenz führt zu genau einem Commit | Kein Parallelwrite/Crashversuch | NOT_RUN |
| R2-T10 | Benachrichtigung an richtigen Principal, keine Dublette | Kein externer Versand | NOT_RUN |
| R2-T11 | Vererbung/Exportgrenzen erzwingen DENY | Nur Spezifikation gelesen | NOT_RUN |
| R2-T12 | Alte Findings bleiben bis belegter Closure offen | Kein laufender Findingcontroller getestet | NOT_RUN |

Die beobachteten FAILs betreffen Dokument-/Zustandskonsistenz, nicht erfolgreich durchgeführte Angriffe. Kein NOT_RUN ist ein PASS.

## Kleinster sinnvoller Verbesserungsschritt

1. **Vor dem nächsten Golden Slice:** Eine effektive Policy samt Hash und kanonischer Folder-ID festlegen; Scheduler-/Umfrageverweise migrieren. Engen Testauftrag, tatsächlichen Writer, Zielprincipal und Empfänger bestimmen. Frische, kollisionsarme Ereignis-ID verwenden. Bestandsdublette ausdrücklich korrigierend referenzieren.
2. **Pilot seriell und transparent durchführen:** Keine gleichzeitigen Front-/Logwriter; jede Phase mit Receipt und Recoveryzustand. Golden-Slice-Kriterien einzeln PASS/FAIL/NOT_RUN melden. Mail- oder Pushausfall darf nicht in allgemeinen E2E-Erfolg umbenannt werden.
3. **Vor Release:** Gateway/Autorisierung, unveränderliches Release-Manifest, Findinglebenszyklus und Re-Testfälle R2-G01/G03/G04/G06/G07/G11 umsetzen. Danach drei unabhängig dokumentierte Re-Reviews auf demselben neuen Freeze, Konsolidierung und explizites Human Gate. Dieses Review ersetzt keines dieser Re-Reviews.

## Offene Fragen an die Entscheidungsebene

- Welcher authentifizierte Human-Principal ist ID01, und welcher Freigabekanal ist verbindlich?
- Welche Unabhängigkeit verlangt Julian konkret: isolierte Reviewer-Tasks, getrennte Accounts, getrennte Provider oder Kombination? Welche gemeinsame Herkunft ist zulässig?
- Welche genaue Policyversion ersetzt welche Klauseln aus S03/S04/S08/S09, und wer bestätigt diese Auflösung?
- Sind übergeordnete WORK-Regeln außerhalb der Reviewgrenze rechtlich/organisatorisch relevant, oder ist WORK als eigene Autoritätswurzel ausdrücklich genehmigt?
- Welche testweise Schreibaktion ist gestattet, welche Daten dürfen in Drive, GitHub, Graphen und Mail, und welche Retention gilt?
- Wird im Golden Slice Versand oder bestätigte Übergabe abgenommen? Was geschieht bei DELIVERY_UNKNOWN und fehlendem ACK?
- Wer bearbeitet die bestehenden Findingblocker, bis wann, und wodurch werden alte Freigaben widerrufen?
- Welche unabhängigen API-/Runtime-Receipts sollen künftig Teil des Freeze werden, damit Aussagen über Scheduler, Pagination und Rechte reproduzierbar sind?

## Getrennte Empfehlung

| Entscheidung | Empfehlung | Begründung/Bedingung |
|---|---|---|
| Konzeptarbeit | BEDINGT POSITIV | Gute Evidenzdisziplin, explizite Grenzen und klare Sollgates. Begriffe und Vorrang konsolidieren; keine Durchsetzungsbehauptung daraus ableiten. |
| Enger Golden-Slice-Pilot | ZULÄSSIG MIT AUFLAGEN, ABNAHME OFFEN | Autorisierter enger Testumfang, ein Writer, aufgelöste Einstiegspolicy, bestätigtes Zielprincipal, keine Produktionsfreigabe; Ergebnis pro Kriterium berichten. |
| Architekturvertrag/Produktion | NICHT FREIGEBEN | Autorisierung, exklusive Gates, Versionsfreigabe, Vererbung und Konfliktkontrolle nicht nachgewiesen; unabhängige Reviewdefinition und Re-Reviewprozess noch nicht vollständig belegt. |

## Kompakte Befundübersicht

**12 Findings:** 2 KRITISCH (G01, G03), 8 HOCH (G02, G04–G09, G11), 2 MITTEL (G10 im engen Pilot, G12). G10 wird bei erweitertem Benachrichtigungsumfang HOCH. Keine zusätzliche kritische Schwere aus bloß hypothetischer Gefahr abgeleitet: die kritischen Befunde sind konkrete Freigabeblocker an der fehlenden technischen Autorisierungsgrenze.

Direkt reproduziert: Manifest-/Quellhashes, vollständige Lesedeckung, doppelte Run-ID, mehrdeutige Vorgängerkante und textuelle Regelkonflikte. Nicht reproduziert: Live-Gates, Angriffe, Scheduler, Mail, Broker, CAS/Lease, Vererbung, unabhängige Freigabekette. Keine allgemeine Zuverlässigkeitsgarantie und keine erfundenen Verbrauchsangaben.

Exakter Ausgabepfad: `/workspace/scratch/ecb96da71040/cplm-review-results/RUN-2.md`.

## Beobachteter Abschluss

Vollständiger lokaler Output-Readback nach Erstellung: 28.865 Zeichen, 12 Findingüberschriften und vollständiges Dateiende bestätigt; Zeitpunkt der unmittelbar folgenden Systemuhrabfrage: **2026-10-16T15:16:58Z**. Das ist der beobachtete Abschluss der inhaltlichen Prüfung und Erstverifikation, keine Aussage über Live-Systemlaufzeit. Start bis dahin: 3 Minuten 41 Sekunden. Dieser Abschlussvermerk wurde anschließend angefügt.
