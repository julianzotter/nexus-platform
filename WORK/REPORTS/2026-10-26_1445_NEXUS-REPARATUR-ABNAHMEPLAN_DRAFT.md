# NEXUS — Reparatur- und Abnahmeplan | 1-Pager

Stand: 26.10.2026, 14:45 Europe/Vienna. DRAFT. Review-Snapshot, keine Betriebsfreigabe. Agenten-ID und laufende Nummer nicht vergeben; Dateiname vorläufig.

## Präzisierte Fassung
- Bestandsintegration statt Neubau: vorhandenen Drive↔Runtime-Transport reparieren, Pilot absichern, einen Auftrag vollständig abnehmen.
- OCR, KG-Achsen, Taxonomie und Berechnungsmodule bleiben separate Arbeitsstränge.

## Ursache
- Vorhanden ≠ erkannt ≠ übernommen ≠ ausgeführt ≠ zugestellt ≠ geprüft.
- Connector im Chat ≠ Runtime-Zugang; Grün ≠ fachlicher Erfolg; Ablage ≠ ACK; Push ≠ Merge ≠ Deployment.

## Priorität 1: Transport und Zugriffsschutz
- Fehlende Credentials/Rechte: BLOCKED mit Fehler-Exitcode. Teilverarbeitung: PARTIAL. Keine Änderungen: NO_CHANGE.
- Starttoken sichern, WORK-Bestand inventarisieren, Änderungen nachziehen und deduplizieren. Löschung, Verschiebung und Zugriffsverlust behandeln. Fortschritt erst nach dauerhafter Verarbeitung bestätigen.
- Benannte Identitäten prüfen; öffentliche Schreibrechte nur nach Freigabe entfernen; unberechtigten Zugriff negativ testen.

## Priorität 2: Minimaler Betriebsvertrag
- AGBs, Manifest, Baseline, Frontmatter, Glossar und AGENTS.md auf einen eindeutigen Pilot-Regelstand beziehen.
- Pflichtdaten: Ticket-ID, Eingabe-/Regelversion, Rolle, Executor/Runtime, Tools/Ziele, Run-ID, Versuch, Reservierungsfrist, Ergebnis, Review und Freigabe.
- OPEN → CLAIMED → RUNNING → DONE; alternativ BLOCKED / REVIEW_REQUIRED / FAILED. Empfang, Readback und Review separat protokollieren. Ungültige Aufträge zurückweisen.

## Priorität 3: Auftrag abschließen
- Bestehende kleine WO mit synthetischen oder freigegebenen Daten. Eingang → Reservierung → Ausführung → Ablage → Readback → ACK → unabhängiger Review.
- Zwei getrennte Instanzen: A führt aus, B prüft die konkrete Artefaktversion. Identität, Modell, Runtime, Rechte und Capability-Test erfassen.
- Störtests: Doppelzustellung, Parallelübernahme, Neustart, Zugangsausfall, Eingabeänderung, fehlende Freigabe.

## Dauerbetrieb
- Zentraler Dienst beobachtet WORK; persistentes Register hält Reservierungen, Versuche und Wiederaufnahme. Unverändert: kein LLM-Aufruf.
- Pilotvorschlag: Änderungen alle 5 Minuten, Hänger alle 15 Minuten, täglich Delta-/Fehlerbericht und Sicherung. Restore testen; Zeit-, Kosten- und Wiederholungslimits.

## Nächste Arbeitspakete
- Prüfen: Integrations-WO, Perplexity-v1.2, Ticketregister/Ledger, drive_changes_poll.py, Delivery-Tooling, Workflows, WORK-Rechte und PR-40-Diff.
- PR 40: tatsächlichen Diff prüfen, Regelkonflikte klären, Tests und unabhängigen Review durchführen; ID01-Freigabe vor Merge, danach Deploymentnachweis. Transportfix getrennt halten.
- Gemeldete Laufreferenzen: Poller 40282473365, Delivery 40278665032. Benötigt: Job-/Step-Logs, Commit/Workflowversion, Run/Versuch, Zeit, Exit-/Fachstatus, Cursor, IDs, Fehler, Journal, Hash/Readback/ACK. Keine Secretwerte.

## Abnahme
- Getrennte technische Reviewinstanz; endgültige begrenzte Pilotfreigabe durch ID01 / Julian Zotter.
- Normalfall und Störtests bestanden; keine falsche Erfolgsmeldung, Doppelaktion oder Selbstfreigabe. Keine pauschale Produktionsfreigabe.
