# DELTA 1/3 — Governance- und Falsifikations-Re-Review

**Ergebnis:** Die fünf ursprünglichen Gegenfälle C01–C05 sind im engen lokalen Kernel überwiegend wirksam korrigiert; alle 26 vorhandenen Tests bestehen unabhängig. C01 ist nur teilweise gegen den umfassenderen Manifestvertrag erfüllt. Weitere gezielte Gegenfälle zeigen verbleibende Grenzen bei finaler Quellenfrische, Recovery und semantischer Benachrichtigungsdeduplizierung. **Lokale Weiterentwicklung/Fehlerpilot: ja. Produktions- oder Vertragsfreigabe: nein.**

## Identität, Stand und vollständige Prüfung

Ausführender Task: `/root/cplm_run2_governance_falsification`, als eigener Governance-Re-Reviewer vom Koordinator erneut beauftragt. Keine anderen DELTA-Reviews gelesen; RUN-4 war ausdrücklich Prüfinput und wurde vollständig gelesen. Keine Codeänderung, externe Mutation, Nachricht an Dritte oder Subagenten. Fixturedateien entstanden ausschließlich temporär während Tests; dieser Bericht ist das beauftragte lokale Ergebnis. Account-/Modelldiversität und externe Authentifizierung bleiben unbekannt. Token/Kosten NOT_MEASURED.

Beobachteter Start: **2026-10-16T15:32:28Z**. Gelesen: vollständige `core.py` (369 Zeilen), `test_cplm.py` (318 Zeilen), RUN-4.md (185 Zeilen). Erster kombinierter Tooloutput war abgeschnitten; deshalb anschließend alle drei Dateien in getrennten vollständigen Abschnitten gelesen. Keine Schlussfolgerung beruht auf abgeschnittenem Text.

| Prüfinput | SHA-256 |
|---|---|
| core.py | `120f40ac4c43464b54c34501625a1d0ea8d73406c957244d86781a991b3fc42d` |
| tests/test_cplm.py | `7df39f45f9c466e467d9b77cac32a982e49a77aa88acd132077edd3c554164d3` |
| RUN-4.md | `d2515fb55917b29e166340eaa0db228275c1c172aa288532d06e416fa8e1a04e` |

Der angegebene Corehash stimmt mit dem Koordinatorauftrag überein. RUN-4 beschreibt einen älteren Codehash; seine historischen Gegenfälle werden gegen den jetzt angegebenen Stand erneut bewertet. Das ursprüngliche Neun-Dateien-Bundle wurde hier nicht erneut gelesen; dieses Delta bewertet den neuen Code, Tests und RUN-4, keine neue Gesamtfreigabe des ursprünglichen Systems.

## Tatsächlicher Testlauf

Ausgeführt, unveränderte Suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v
```

**Beobachtet: 26 Tests in 0,208 s, OK.** Relevante Fälle umfassen Ergebnisreihenfolge, Manifestintegrität, nachträgliche Quellen-/Codeänderung, fremde Akteure, unverifizierte Übergabe, drei unterschiedliche Reviewerstrings, Artefaktverlust, Paralleleinlieferung, konkurrierende Ergebnisse, Outboxkonkurrenz, Teilwrite vor Veröffentlichung, Crash nach fsync und nach vollständiger Veröffentlichung sowie manuelle Konfliktrecovery. Das sind lokale Tests mit Fixtureidentitäten und temporären Dateien. Keine Drive-/Gmail-/GitHubintegration, kein echter Humanprincipal und kein Authadapter wurden dadurch geprüft.

Danach sechs zusätzliche gezielte lokale Gegenfälle ausgeführt; Ergebnisse unten. Die Fälle wurden als Inline-Python unter Verwendung der bekannten CPLMTests-Fixture ausgeführt, ohne Tests oder Modul zu ändern. Ein Test benutzt Monkeypatch an der Prüf-/Commitgrenze, um einen deterministischen konkurrierenden Dateischreiber zu simulieren; diese Voraussetzung wird nicht als unprivilegierter API-Angriff ausgegeben.

## Bewertung der fünf behaupteten Fixes

| Fall | Beobachtete Korrektur | Urteil und Restgrenze |
|---|---|---|
| C01 Reviews vor Resultat / beliebiger bundle_hash | `review()` verlangt RESULT_VERIFIED; `_fresh_manifest()` verlangt gespeichertes, gehashtes Postresultatmanifest. Darin Resultat-, Policy-, Code- und referenzierte Quellhashes. Alter deklarierter bundle-v1 wird als Reviewmanifest abgewiesen. | **Ursprünglicher Exploit geschlossen. Umfassender Vertrag teilweise offen:** Anforderungen, Schema-/Dependency- und tatsächlicher Testsuitestand fehlen als Manifestinputs. Das Receipt meldet korrekt nur vier lokale Prüfungen; es darf nicht als Regressionstest- oder Fachabnahmebeleg bezeichnet werden. |
| C02 Quelle nach Reviews verändert | `_current_inputs()` validiert Quellen sowohl bei Validierung als auch bei Review und Release erneut. Regressionstest weist SOURCE_CHANGED nach; approved bleibt 0. | **Serieller Gegenfall geschlossen. Finale TOCTOU-Grenze offen:** Quelldateien sind nicht gemeinsam mit SQLite gesperrt oder unveränderlich archiviert. D1 zeigt Mutation nach letzter Prüfung und vor Commit. |
| C03 frei wählbare Outboxkeys | Caller gibt Kanal statt Schlüssel an; Key berechnet der Kern aus Run, Kanal, konfiguriertem Empfänger und Nachrichtentyp. Unbekannte Kanäle werden abgelehnt, gleiche Reservierung bleibt nach Restart gesperrt. | **Ursprünglicher freie-Key-Exploit geschlossen.** Semantik setzt eindeutige kanonische Kanäle voraus; zwei Aliase für denselben Transport/Empfänger können weiter zwei Reservierungen erzeugen (D3). Keine Exactly-once-Mailgarantie. |
| C04 partielles endgültiges Artefakt | Staging, fsync und atomarer Hardlink verhindern eigene partielle Veröffentlichung. Unterschiedliche vorhandene Datei führt zu persistiertem RECOVERY_REQUIRED; explizite Recovery erhält Konfliktbytes und erlaubt Retry. | **Ursprünglicher regulärer Teilfile-Gegenfall geschlossen.** Symlinkziel wird sicher abgelehnt, bleibt jedoch außerhalb der Recovery-FSM (D2). Crash-/Powerlossmatrix und alle externen Adaptergrenzen weiterhin nicht vollständig getestet. |
| C05 FAILED als RESULT_VERIFIED | Nur exakter YAML-Wert RESULT zulässig; FAILED/UNKNOWN/null/Liste etc. werden vor Artefakterstellung abgewiesen. | **Ursprünglicher Gegenfall geschlossen.** Doppelte YAML-Schlüssel werden von safe_load still auf den letzten Wert reduziert (D4). RESULT bedeutet weiterhin keine fachliche Richtigkeit. |

Die Einordnung unterscheidet den tatsächlich widerlegten alten Exploit von zusätzlichen strengeren Anforderungen. Ein alter Findingstatus kann enger geschlossen werden, ohne eine neue Restgrenze zu verschweigen. Keine bloße Umbenennung des ursprünglichen Ziels entdeckt: echte neue Zustands- und Persistenzprüfungen sind vorhanden.

## Zusätzliche Gegenfälle: erwartet gegen beobachtet

### DG-01 — HOCH bei Anspruch auf aktuelle Quellen zum Freigabecommit

**Quelle:** `core.py`, `_current_inputs`, `_fresh_manifest`, `release`; RUN-4 C02 und finale Commitgrenze.

**D1 tatsächlich ausgeführt:** prepare → drei PASS → Manifest holen. `_current_inputs` wurde temporär so umschlossen, dass es zunächst die echte Prüfung ausführt, danach die Fixturequelle verändert und erst dann die geprüften Inputs zurückgibt. Anschließend normaler Release. Der Code auf Disk blieb unverändert.

**Erwartet bei starkem Frischevertrag:** geänderte Quelle verhindert Abschluss oder ein unveränderlicher geprüfter Snapshot ist das ausdrückliche Releaseobjekt. **Beobachtet:** `execution=COMPLETED`, Quellinhalt `changed at final validation/commit boundary`.

Das ist ein deterministischer Test eines Dateischreibers mit Zugriff auf die Quelldatei während der Prüfung. Kein behaupteter Angriff durch einen Akteur ohne Dateirechte. SQLite serialisiert Kernelwriter, nicht externe Dateimutationen. Ein weiteres Read allein schließt das Zeitfenster nicht grundsätzlich.

**Minimal:** Vertragsentscheidung treffen: unveränderliche archivierte Quellen sind Releaseinputs, oder alle relevanten Dateiwriter müssen über dieselbe kontrollierte Commitgrenze laufen. Bis dahin Frische nur „zum letzten Prüfschritt“ behaupten. Fall als Negativtest behalten; für Produktion Snapshot-/Versionsbindung am externen Storeadapter prüfen.

### DG-02 — MITTEL: sicher abgewiesener Symlinkkonflikt ist über die öffentliche Recovery nicht auflösbar

**Quelle:** `result` prüft `target.is_symlink()` vor ARTIFACT_CONFLICT-Behandlung; `recover_artifact_conflict` verlangt RECOVERY_REQUIRED.

**D2:** nach submit Zielsymlink auf harmlose Fixturequelle angelegt; result und danach Recovery mit aktueller Revision aufgerufen.

**Erwartet:** sicher ablehnen, vorhandenes Objekt erhalten und dokumentierten Recoverypfad anbieten. **Beobachtet:** `SYMLINK_TARGET`; Zustand bleibt `RUNNING`; Recovery ergibt `RECOVERY_NOT_ALLOWED`. Kein unautorisiertes Überschreiben, aber festgefahrener Run ohne API-Reparaturpfad.

**Minimal:** Symlinkkonflikt in RECOVERY_REQUIRED überführen und das Linkobjekt selbst isolieren, nie das Linkziel verändern; alternativ klar dokumentierte administrative Recovery mit Ereignisreceipt. Test mit dangling und bestehendem Ziel ergänzen. Dies hebt den bestandenen regulären Teilfilefall C04 nicht auf.

### DG-03 — MITTEL: semantische Outboxeindeutigkeit hängt von Kanalnormalisierung ab

**Quelle:** `notification_key`, `reserve_notification`; RUN-4 C03.

**D3:** Fixturepolicy vor Kernelinitialisierung um erlaubten Kanal `gmail` mit identischem Empfänger wie `email` erweitert. Derselbe Run reserviert email und gmail.

**Erwartet bei Aliasen eines Transportkanals:** eine semantische Reservierung. **Beobachtet:** beide `True`, Schlüssel verschieden. **Keine echte Mail versandt.** Sind email/gmail absichtlich unterschiedliche autorisierte Kanäle, ist das erwartbares Verhalten; die aktuelle Policy besitzt jedoch keine explizite Transport-/Aliassemantik. Kein Caller kann mit unveränderter Ein-Kanal-Policy diesen Weg allein erzeugen.

**Minimal:** Bei Policyvalidierung kanonische Transportkanäle bzw. Zustellziel-ID bestimmen, Aliase abweisen/normalisieren. Einmaligkeit gilt pro logischem Run, kanonischem Kanal, Empfänger und Typ; neue task_keys für denselben externen Auftrag bleiben eine zusätzliche Eingangsvertragsfrage. OUTCOME_UNKNOWN und keine blinden Retries beibehalten.

### DG-04 — MITTEL: widersprüchliche Statusfelder werden still akzeptiert

**Quelle:** `result` und `yaml.safe_load`.

**D4:** Report mit `status: FAILED` gefolgt von `status: RESULT` im selben Frontmatter übergeben.

**Erwartet für verbindliches Statusschema:** Mehrdeutigkeit als INVALID_FRONTMATTER/DUPLICATE_KEY abweisen. **Beobachtet:** `RESULT_VERIFIED`; PyYAML verwendet letzten Wert. Der Leser kann den ersten Status als maßgeblich verstehen. Eine absichtlich falsch ausgefüllte einzelne RESULT-Angabe bleibt ohnehin kein Fachnachweis; hier geht es konkret um vermeidbare Parsermehrdeutigkeit.

**Minimal:** Loader mit Duplicate-Key-Ablehnung und anschließend striktes Schema. Auch Pflichtfeldtypen, unbekannte Schlüssel und Source-Ref-Elementtypen fail-closed validieren. Keine fachliche Erfolgsbewertung aus Statuswort ableiten.

### DG-05 — HOCH für vollständige Vertragsfreigabe: Manifest bindet noch nicht Tests und Anforderungen

**Quelle:** `_current_inputs`, `validate_result`; RUN-4 C01 und „Drei wesentliche nächste Änderungen“.

**D5:** gespeichertes Manifest nach echter Validierung ausgelesen. Beobachtete Inputkeys: `artifact_sha256`, `code_sha256`, `declared_input_bundle`, `policy_sha256`, `run_id`, `sources`, `task_key`. Receiptchecks: artifact_readback, source_freshness, result_status, policy_freshness, jeweils PASS. Keine Testdatei-/Testresultat-/Anforderungs-/Schemasignatur. `declared_input_bundle` bleibt Callerstring.

**Erwartet im umfassenden RUN-4-Vertrag:** Reviewer billigen das Resultat zusammen mit den tatsächlich geltenden Abnahmeanforderungen und dem belegten Teststand. **Beobachtet:** korrekt gehashtes, aber engeres lokales Prüfobjekt. Der Code behauptet ausdrücklich nicht, die Testsuite auszuführen; das ist ehrliche Scopebegrenzung, kein gefälschtes Testreceipt.

**Minimal:** Für Architekturrelease separates versioniertes Requirements-/Testreceipt als Manifestinput aufnehmen, mit tatsächlich ausgeführtem Kommando, Inputhashes und Ergebnis. Für den jetzigen Kernel ausdrücklich `local-post-result-validation-v1` verwenden; grüne lokale Checks nicht zu allgemeiner Fach- oder Integrationsabnahme aufwerten. Importierte Bibliotheken und übrige Laufzeitumgebung werden durch core.py-Hash ebenfalls nicht vollständig gebunden.

### DG-06 — NIEDRIG: unverändertes Manifest erlaubt keine revidierte Stellungnahme

**Quelle:** `review` UNIQUE-Constraints, `validate_result` löscht Reviews nur bei verändertem Manifest.

**D6:** Governanceunabhängiges Beispiel: review-a/software/FAIL speichern; identischen Stand erneut validieren; denselben Reviewer zu PASS revidieren lassen. **Beobachtet:** Manifest unverändert, erneuter Review `REVIEWER_OR_PERSPECTIVE_ALREADY_USED`.

Das ist fail-closed und kein Sicherheitsbypass. Dennoch benötigt der DELTA-Prozess einen dokumentierten Weg für Korrektur einer fehlbedienten Stellungnahme oder eine neue Reviewrunde. Aktuell nur neue logische Runs bzw. administrative Bearbeitung außerhalb der API ersichtlich. **Minimal:** append-only superseding Reviewreceipts mit expliziter Reviewrunde und aktuellen Zustimmungsständen, oder bewusst neuen Run verlangen und Rückverweis dokumentieren. Kein bestehendes FAIL überschreiben.

## Weitere offene Governancegrenzen, unverändert und nicht neu getestet

- `actor`, Empfänger, Reviewer und Human sind Strings. Der Modulkopf nennt Caller-Authentifizierung extern. **Kein Authadapter vorhanden oder durch dieses Review nachgewiesen.** Direkte freie Übernahme eines HTTP-Parameters als actor wäre keine sichere Integration.
- ACK-/VERIFIED-Evidenz sind freie nichtleere Strings. Kein tatsächlicher Empfang, Lesen, signierter ACK oder Gerätepush nachgewiesen. Drei verschiedene Reviewerstrings beweisen keine drei unabhängigen Personen/Accounts/Modelle.
- Die Kernelpolicy ist ein vertrauenswürdiges Pythonobjekt; direkter DB-/Hostzugriff und Monkeypatch gehören nicht zur abgesicherten Angreifergrenze. Datenbankevents sind kein manipulationsgeschütztes Auditlog. Prozess-/Dateirechte und Credentialexklusivität bleiben Voraussetzungen.
- `resolve_policy` bleibt Paarresolver, ohne rekursive Root-/Zyklus-/Ausnahmenprüfung oder nachgewiesene Einbindung in den Kernel. Insbesondere sind `notifications` nicht als geschütztes Parentfeld enthalten; Childrechte allein begrenzen Datenziele nicht. Nicht in diesem Delta als eigener Lauf reproduziert.
- Keine Cloud-Front/Log-Transaktion, kein Driveadapter, kein globaler Index, keine produktive Hintergrundüberwachung, kein Providerabgleich und kein Datenschutz-/Datenklassencontroller behauptet.
- Review-/Freigabewiderruf nach COMPLETED bei späterer Drift ist kein implementierter kontinuierlicher Kontrollpfad. Hier gilt die überprüfte Entscheidung nur am lokalen Releaseversuch, nicht dauerhaft.

Diese Punkte waren großteils bereits in RUN-4 offen. Sie werden durch C01–C05 weder automatisch geschlossen noch als fünf neue Rückfälle doppelt gezählt.

## Scopebegrenzte Empfehlung und nächster Schritt

**C01–C05 als Originalgegenfälle:** alle fünf alten Abläufe sind durch den gelesenen Code und die bestandenen Regressionstests lokal adressiert; C01 bleibt gegenüber dem umfassenden Manifestvertrag partiell. **26/26 Suite plus sechs zusätzliche Beobachtungsfälle** sind die tatsächliche Testdeckung dieses Reviews, keine Erfolgsquote des Gesamtsystems. Die Zusatzfälle liefern offene Befunde und sind keine sechs PASS-Abnahmetests.

Für einen beaufsichtigten lokalen Fehlerpilot ist der Stand geeignet: serieller kontrollierter Host, feste Fixtureidentitäten, genau definierte Kanäle, geschützte Quellen und keine produktiven Seiteneffekte. Vor nächstem weitergehenden Release mindestens DG-01/DG-05 vertraglich/technisch auflösen; DG-02/DG-04 als kleine lokale Robustheitskorrekturen angehen; DG-03 durch Policyvalidierung begrenzen. Authadapter und Driveintegration brauchen eigene reale Tests und Freigabe. Die nachfolgenden zwei unabhängigen DELTA-Perspektiven und Konsolidierung bleiben erforderlich; dieser Bericht nimmt sie nicht vorweg.

Keine Codeänderung durchgeführt. Kein externes Schreiben oder Senden. Keine 100%-Freigabe.

## Abschlussreceipt

Beobachtete Abschlusszeit der Berichtserstellung: **2026-10-16T15:35:00.229938+00:00**. Vollständiger lokaler UTF-8-Readback des Berichts durchgeführt; C01–C05 und DG-01–DG-06 enthalten. Code, Tests und RUN-4 unverändert gegen die oben erfassten Hashes geprüft.

Exakter Ausgabepfad: `/workspace/scratch/ecb96da71040/cplm-review-results/DELTA-1-GOVERNANCE.md`.
