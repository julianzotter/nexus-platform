---
name: nexus-admin-debug
version: 1.0.0
status: FIXES_MERGED_EXTERNAL_BLOCKERS_OPEN
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
provider: OpenAI
model_id: null
ticket_id: nexus-platform#92
registration_status: REGISTRATION_PENDING_UNSAFE_MULTIWRITER_REPLACEMENT
ledger_number: null
technical_approval: false
observed_at: 2026-11-16T23:07:00+01:00
---
# NEXUS Admin-Debug: verifizierter Delta-Bericht
## Ergebnis
PR #92 gemergt: https://github.com/julianzotter/nexus-platform/pull/92
Merge-Commit: b9dc1b18b2761d92bba13b4c55fa8abf8dd0a7ac.
Autorisierung: aktueller direkter ID01-Auftrag zur Ausführung von Admin-/Debug-Arbeiten einschließlich Merge, wenn möglich. Keine neue Governance-Regel oder technische Freigabe.
| Bereich | Evidenzstatus | Ergebnis |
|---|---|---|
| Claude-Auszug | VERIFIED: überholt | PR90 bereits gemergt; Folder.md und CSV-Ledger inzwischen geändert |
| Governance-MD | VERIFIED | Beide vollständigen Rohdateien stimmen mit den veröffentlichten SHA256 überein |
| Folder.md | VERIFIED | Neue ID 1nDjF78dq3l8PGpXsauzBz1bzHescDSwv, YAML gültig; offene Kollaboration dokumentiert |
| AGENTS + Bridge | VERIFIED: FIX_MERGED | Veraltete Folder-Referenzen im aktiven Einstieg und SOURCE_IDS korrigiert |
| Berichtsnamen | VERIFIED: FIX_MERGED | YY_MM_DD_HHMM_ID##_TOPIC_NUMBER.md; zuvor ID am Ende |
| Offline-Diagnose | VERIFIED: FIX_MERGED | Lesbarkeit, Benutzerbestätigung der Netztrennung und unbekanntes Pinning getrennt |
| GitHub→WORK | VERIFIED: BLOCKED | OAuth-Refresh HTTP_400; CI-Erfolg behebt keine Zugangsdaten |
| Kanonisches JSONL-Register | VERIFIED: REGISTRATION_PENDING | Vier neue Governance-/Steuerdatei-IDs fehlen im gelesenen Register |
| INDEX_LNK_BENCHMARK | VERIFIED / DERIVED | Vier Dateipaare byteidentisch; operativer Parserordner und datierter Snapshot getrennt erhalten |
## Implementierung und QA
Geprüfter Code-Head: abfa194e7115506973787bb70e8a3fa439ea2b31.
CI: https://github.com/julianzotter/nexus-platform/actions/runs/43966597928
Beide Jobs PASS: vollständige Repository-Testpipeline und Windows-PowerShell-5.1-Diagnosetests.
Zusätzlich drei neue Contract-Regressionstests lokal und unabhängig ausgeführt: PASS. Winter-/Sommerzeitgrenze in Europe/Vienna und Quellen-ID geprüft.
Unabhängiger Reviewer: getrennte OpenAI-Codex-Instanz /root/review_admin_fix, REVIEW_PASS auf obigem Head. Keine externe Claude-/DeepSeek-Ausführung behauptet.
Frühere Findings korrigiert: tatsächliche AGENTS-Linkzeile, exakter Fixture-SHA statt Längenprüfung, gesperrte Datei/READ_ERROR und Fortsetzung. Erste Windows-Ausführung: alle Assertions PASS, Job wegen geerbtem erwartetem Unterprozess-Exitcode 1 rot; explizites Teststarter-exit 0 ergänzt. Folge-CI 43966340333 und aktuelle CI 43966597928 beide grün.
Nach Merge alle sieben geänderten Dateien vom Merge-Commit zurückgelesen und exakt mit dem geprüften Inhalt verglichen: 7/7 identisch.
Geänderte Dateien: AGENTS.md; mcp_bridge/nexus_contract.py; tools/windows/drive_offline_check.ps1; tests/test_bootstrap_contract.py; tests/test_nexus_contract_current.py; tests/windows/test_drive_offline_check.ps1; .github/workflows/ci.yml.
Offline-Diagnose: Exit 2 bei lesbaren Dateien ohne Netztrennungsbestätigung; Exit 1 bei Datei-/Encodingfehlern; Exit 0 nur bei lesbaren Dateien und expliziter Benutzerbestätigung. SHA256 über tatsächliche Bytes; Latenz rein informativ. Pinning und Policy-Autorisierung werden nicht als geprüft ausgegeben.
Grenze: synchrones ReadAllBytes ohne Anwendungstimeout; ein Drive-Platzhalter kann bis zum Provider-Timeout blockieren. Echter Offline-Test auf Julians PC NOT_RUN.
## Governance: Quellenidentität und Rohbyteprüfung
| Quelle | Drive-ID | Bytes | SHA256 |
|---|---|---:|---|
| Manifest-MD | 1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn | 7720 | cfcb2ea6088a474a6bb41654a86ed6de3e32e2b572aa57b9ce7ea6527238fdee |
| Baseline-MD | 1CdwNHr6i8lMG3k8A939kiznLMw8q7J69 | 18680 | 015a635ff2745f6ae0bf61f02d3028039ea45acb86f24363db7185786d854858 |
| Folder.md | 1nDjF78dq3l8PGpXsauzBz1bzHescDSwv | 7733 | 59340dd798d19862f12049c13ffd296a2629a38426232389d87c43e5b8ffb977 |
| CSV-Ledger | 1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK | 62889 | 8b7cafe7f00d3e0b0db9792a1fe8c81fc258cc5de81e6760bcbfd24b37a89cff |
| JSONL-Register | 15m8T5cWbogIup9snzFwiB1g9HqNCoGow | 418786 | e233e9acbeb835413f3a6950393e03028cdfd0aad4c7387e083440ef850d4eac |
_AGBS.md v006 vollständig gelesen: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
Ticketregister gelesen: https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit
Alte Folder-ID 11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH gehört jetzt zu Folder_2026-11-12_SUPERSEDED.md. Historische Berichte und Quellensnapshots bleiben unverändert.
Google Docs als Editierquelle plus manuell exportierte MD-Spiegel: Drift-Risiko weiterhin offen. Byteprüfung dieser MD-Dateien beweist keine automatische Nachführung nach künftigen Doc-Änderungen.
## Ledger und Registry: unterschiedliche Nachweise
CSV: 201 Datensätze; keine doppelten ID-Feldwerte. Einträge 0208/0209 enthalten die MD-Datei-IDs und korrekten Hashes.
Eintrag 0210: DRIVE_ID leer; SHA256 enthält SEE_REPORT_LOG statt eines Hashes. Eintrag 0211: DRIVE_ID und SHA256 leer. Vollständigkeit des Ledgers deshalb nicht bestätigt.
JSONL: 460 syntaktisch parsebare Ereignisse; Provider-Änderungsdatum 2026-11-12T18:47:37.749Z.
Keine exakten Treffer der vier oben genannten IDs für Manifest-MD, Baseline-MD, neue Folder.md und neuen CSV-Ledger. CSV-Nummerierung ersetzt die laut AGB vorgeschriebene Registrierung in diesem JSONL nicht.
Keine ungeschützte Ersetzung des kanonischen Registers ausgeführt. Aktueller Drive-Update-Connector kann Rohbytes unter derselben ID ersetzen; keine nachgewiesene atomare Revision-/CAS-Bedingung oder exklusive Mehrschreiber-Sperre. Rename-old/upload-new würde erneut stabile IDs brechen. Die frühere Behauptung, CSV könne generell nicht in-place aktualisiert werden, ist damit zu weitgehend; sichere Konkurrenzkontrolle bleibt der tatsächliche Blocker.
Nächste Writer-Aktion: bestehendes Register unter belegtem exklusivem Writer/Lease oder CAS öffnen; fehlende Identitäten per artifact_id=gdrive:<ID> prüfen und append-only registrieren; CSV-Ereignisse 0210/0211 vervollständigen; Rohbyte-Readback und neue Version nachweisen. Keine Nummer aus Dateinamen oder max(ID)+1 ableiten.
Dieses Ergebnis hat bis dahin REGISTRATION_PENDING; keine neue fortlaufende Nummer zugeteilt.
## INDEX_LNK_BENCHMARK: keine blinde Duplikatverschiebung
Operativer Parserpfad: LLM-LOCAL-SSOT/NEXUS.INDEX.PARSER/INDEX_LNK_BENCHMARK
https://drive.google.com/drive/folders/1k2QbG06-Pj5JCAdJzUgkyxTfHSYYIVTb
Datierter Snapshot: NEXUS_PARSE_2026-10-13/INDEX_LNK_BENCHMARK
https://drive.google.com/drive/folders/1trPeZ3wTNkdi1uniIZpXo1onXtEVSaFg
Beide enthalten direkt vier Parser-Ausgaben, keine aufgelisteten fachlichen Benchmark-Quelldateien. Identischer Inhalt allein beweist keine entbehrliche Kopie bei unterschiedlicher Snapshot-Funktion.
| Dateipaar | Rohbytes identisch | SHA256 |
|---|---|---|
| DASHBOARD v1.0 | ja | be656934c79216bc6e0ef644d20f5b6bd4144cfde378efcb03235282b6da6aa5 |
| DASHBOARD v1.1 | ja | 0365374b89fa67f28d7b345eb4d146417929de0440b5da146ae91ea9b791daca |
| REPORT v1.0 | ja | d6f636e0ddec6638ec1741e1f41f62e9e448a2698b7ff823d9ff6761d7f92940 |
| REPORT v1.1 | ja | e04602ab6b187e6a8bc5d3a885d8628cc6eb3a8a31d4de50222378027c893c4a |
Verschobener Root-Benchmarkordner 14t8bMmDDp-kIa9EvQDWncLGtlRrWX8hz: aktuelle vollständige direkte Suche leer. Kein Datenverlust daraus belegt. Pfadabhängigkeiten außerhalb des untersuchten GitHub-Repositories nicht vollständig geprüft.
Parserbericht v1.1 nennt NEXUS_PARSE_INVENTORY_v1.1.json und parse.py; beide fehlen in den vier direkten Kindern dieser Benchmarkordner. Das beweist keine globale Abwesenheit. Vollständige Reproduzierbarkeit dieser alten Pipeline hier nicht bestätigt.
## Weitere Probleme / nächste Schritte
1. P0 Sync: OAuth-Refresh reparieren und echten Delivery-Run samt WORK-Rohbyte-Readback nachweisen. Fehlerlauf https://github.com/julianzotter/nexus-platform/actions/runs/43964638659; operation oauth.token_refresh, reason HTTP_400. Fehlerursache invalid_grant o.ä. aus diesem Log NICHT ableitbar. Sichere Rekonfiguration: bestehendes tools/configure_drive_oauth.py verwenden; Credentials nicht in WORK oder Chat ablegen.
2. P0 Registry: oben genannte Schreibkonkurrenz und fehlende Identitäten lösen. Relevante Aufträge #73 und #86 bleiben offen. OAuth-Reparatur allein garantiert keine sichere Registry-Schreiboperation.
3. P1 Monitor/PRs: Monitorlauf 43964479565 INCOMPLETE; Inventory-Summary INCOMPLETE=9, VALID_STRUCTURE=7, INVALID=4. Diese Zahlen sind Inventory-Zustände, keine Behebung durch CI-Green. Offene PRs live: 68,82,83,84,85,87; #85 basiert auf #83-Branch, #84 auf claude/skills-daily-recall-fable52. Abhängige PRs zuerst gegen ihren tatsächlichen Base-Branch prüfen. Kein pauschaler Auto-Merge fremder ungeprüfter Engineering-Arbeit.
4. PC: aktuellen Bugfix aus main übernehmen, Drive-Ordner lokal verfügbar machen; Netzwerk manuell trennen, dann tools/windows/drive_offline_check.ps1 -OfflineConfirmed -AsJson ausführen und Resultat ablegen.
Keine Branch-/Dateilöschung, keine Freigabeänderung, keine Secrets-Mutation. WORK-Offenheit entspricht dem gelesenen ID01-Entscheid und bleibt getrennt vom Nachweis eines exklusiven Registry-Writers.
CAVEMAN: im bereitgestellten Skillkatalog nicht verfügbar; keine Installation oder gemessene Tokenersparnis behauptet.
## Reproduktion der Registerprüfung
Vollständige CSV-/JSONL-Rohdateien vom oben bezeichneten Stand herunterladen, dann:
```python
import csv, json, hashlib
from pathlib import Path
ledger = list(csv.DictReader(open('ledger.csv', encoding='utf-8-sig')))
registry = [json.loads(line) for line in Path('registry.jsonl').read_text().splitlines() if line.strip()]
assert len({row['ID'] for row in ledger}) == len(ledger)
for source_id in ('1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn', '1CdwNHr6i8lMG3k8A939kiznLMw8q7J69', '1nDjF78dq3l8PGpXsauzBz1bzHescDSwv', '1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK'):
    print(source_id, sum(source_id in json.dumps(event) for event in registry))
for name in ('ledger.csv', 'registry.jsonl'):
    print(name, hashlib.sha256(Path(name).read_bytes()).hexdigest())
```
