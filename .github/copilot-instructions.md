# NEXUS · GitHub Copilot

Lies AGENTS.md und die dort referenzierten aktuellen Governance-Quellen.

Jeder Agent meldet zum Start und nach Kontextverlust im START_ACK die Rollen-ID, die tatsächliche Runtime mit Instanz, die vom Anbieter ausgewiesene Modell-ID und den geprüften Zugriff. Je Ziel und Operation Ergebnis, Prüfzeit und Beleg angeben. Unbekannte Modell-ID als null und ungeprüfte Operationen als NOT_TESTED führen. Lese- und Schreibzugriff getrennt ausweisen. Prüfen im Umfang des Auftrags.

Für jeden NEXUS-GitHub-Copilot-Task die Task-URL, das vollständige Repository (owner/repo), den PR-Link und den vollen Commit-SHA im WORK-Auftrag oder zugehörigen Nachweis erfassen. Den aktuellen PR-Head aus GitHub lesen, mit Abrufzeit festhalten und nach einem Push erneut prüfen. Einen Merge-SHA bei Bedarf separat ausweisen. Task-zu-PR-Zuordnung durch den Task oder einen expliziten Rückverweis belegen. Fehlende Zuordnung als UNRESOLVED und einen laut Task fehlenden PR als NO_PR ausweisen. Fehlende Werte sind null. Auftragsstatus und Vollständigkeit der Verknüpfung getrennt führen.

Bei authentifiziertem GitHub-CLI-Benutzerzugriff auf Agent tasks (lesen) kann das zentrale Werkzeug den Bestand abrufen: `python tools/copilot_task_links.py julianzotter/nexus-platform`. Weitere NEXUS-Repos als separate Argumente angeben. Der JSON-Bericht trennt verifizierte Verknüpfungen, fehlende PR-Artefakte und ungeklärte Zuordnungen.
