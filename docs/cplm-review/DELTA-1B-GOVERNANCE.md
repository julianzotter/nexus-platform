# DELTA 1B — unabhängige Governance-Nachprüfung

**Urteil: lokaler, beaufsichtigter Prototyp bedingt geeignet; Produktions- und Vertragsfreigabe weiterhin gesperrt.** Die angefragten kleinen Governancekorrekturen sind nachvollziehbar umgesetzt. Kein neuer blockierender Fehler innerhalb der dokumentierten lokalen Systemgrenze gefunden.

Prüfer: `/root/cplm_delta_governance`, getrennte Instanz vom Codeautor; keine Behauptung unterschiedlicher Provider, Accounts oder institutioneller Unabhängigkeit. Vollständig gelesen: aktueller Core, vollständige Tests, README und DELTA-1-GOVERNANCE. Ein zunächst abgeschnittener kombinierter Output wurde durch vollständige separate Abschnitte ergänzt. Keine Codeänderung und keine externen Schreibaktionen. Zeit, Token und Kosten sind keine Vollkontext- oder Unabhängigkeitsgarantie.

| Input | SHA-256 |
|---|---|
| core.py | `d6f095a63e5d2e7d632fe5ec4a1ddd6946c136cbe612a1c63ed3e94f3c330ec1` |
| tests/test_cplm.py | `2cab5231c1cc85a26b55a515c1018475ebd4d9e9050e8ff060b94ab9ff59b2e0` |
| README.md | `e09dd238ebf86664b25ad662aed723d18f81beb5e72e5584018ecfeb5c73e2e1` |
| DELTA-1-GOVERNANCE.md | `11f31bc90ecdb4497311fd737c9765220d91f35b405cfe833c664b04926ba450` |

Tatsächlich ausgeführt:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v
```

**Beobachtet: 32 Tests, 0,226 Sekunden, OK.** Dies ist eine eigene erneute Ausführung der vorhandenen Regressionstests, keine neue Cloudintegration und keine zusätzliche Erfolgsquote des Gesamtsystems.

| Befund | Verifiziertes Delta | Bewertung |
|---|---|---|
| DG-02 | Bestehende und dangling Symlinks gehen in RECOVERY_REQUIRED; Recovery isoliert das Linkobjekt; Retry funktioniert, Zielbytes bleiben erhalten. | Im lokalen Vertrag geschlossen. |
| DG-03 | Nur kanonische Kanäle email/sms/push/webhook; gmail wird schon bei Policyinitialisierung abgewiesen. Schlüssel bleiben serverseitig aus Run/Kanal/Empfänger/Typ abgeleitet. | Ursprünglicher Alias-Gegenfall geschlossen; keine Exactly-once-Zustellgarantie. |
| DG-04 | UniqueKeyLoader weist doppelte YAML-Schlüssel ab; exakte drei Feldnamen, task_id-Typ und eindeutige nichtleere String-Source-Refs werden geprüft. | Mehrdeutiger Status und getestete ungültige Feldtypen geschlossen. |
| DG-05 | Optional konfigurierte release_inputs verlangen exakt requirements, schema, tests, test_receipt, dependencies. Jede Datei wird unter Policyroot auf Pfad und tatsächlichen SHA-256 geprüft; fünf Hashes sind Manifestinput. Mutation jeder Rolle blockiert Validierung, Review und Release. Partielle/ausbrechende Konfiguration wird abgewiesen. | Bytebindung implementiert; tatsächliche Ausführung und Wahrheit eines externen Testreceipts werden ausdrücklich nicht attestiert. |
| Parentregeln | notifications und release_inputs sind zusätzlich vor Childüberschreibung geschützt. | Dokumentierter Paarresolver verbessert; keine rekursive globale Durchsetzung behauptet. |

Die optional fehlende release_inputs-Konfiguration liefert bewusst ein leeres Mapping im lokalen Modus. Eine lokale COMPLETED-Fixture darf daher nicht als vollständige Architekturfreigabe ausgegeben werden. Auch ein gehashtes externes Testreceipt kann fachlich falsch sein; seine Authentizität und tatsächliche Ausführung bleiben beim späteren vertrauenswürdigen Adapter/Evaluator. Der Core benennt diese Grenze ausdrücklich. Das README begrenzt das Produkt auf Linux/einen Host und erklärt freie actor-/ACK-Strings als externe Vertrauensgrenze.

Unverändert offen: DG-01 externe Dateimutationen zwischen letzter Prüfung und Commit; reale Authentifizierung und signierte Humanfreigabe; echte Empfänger-ACKs und Providerabgleich; Drive-/GitHub-/Gemini-Integration; globaler Index, Watchdog und Windowsbetrieb. Diese Punkte wurden hier nicht als neue lokale Exploits getestet und werden nicht doppelt als neue Befunde gezählt. DG-06 bleibt eine fail-closed Bediengrenze: eine revidierte Stellungnahme auf identischem Manifest braucht weiterhin einen bewusst neuen Run oder eine künftige append-only Reviewrunde.

**Empfehlung:** Die hier geprüften Governancekorrekturen können in den Reviewkandidaten übernommen werden. Weitere unabhängige Delta-Perspektiven, Konsolidierung und Human Gate bleiben erforderlich. Keine Freigabe für produktive autonome Seiteneffekte, keine Aussage „alle Chatziele erfüllt“, keine 100%-Zuverlässigkeitsbestätigung.
