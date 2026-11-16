# OAuth, Registry und Ledger reparieren
Stand 2026-11-16. Code-Kandidat; echte Google-Anmeldung und Provider-CAS-Test sind eigene Laufnachweise.

## Ein lokaler Start
Im aktuellen `nexus-platform`-Checkout nach Übernahme der freigegebenen Änderungen:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows\repair_nexus_sync.ps1
```
Der Starter benötigt `py` und `gh`. Er erneuert die Google-Zustimmung, prüft den Zugriff mit genau diesen neuen Credentials und veröffentlicht die GitHub-Secrets. Fehlt eine bestehende private OAuth-Konfiguration, fragt er nach dem originalen Google-Desktop-OAuth-Client-JSON als lokaler Datei. Keine Tokens in Chat oder WORK eingeben.
Danach führt er `repair_control_registers.py --apply` aus und stößt die Delivery des letzten abgeschlossenen Monitorlaufs auf `main` an. `DELIVERY_DISPATCHED` bestätigt nur die Anforderung; erfolgreiche Delivery und Registry-Readbacks stehen im späteren Actions-Lauf.

## Was der Reparaturlauf tatsächlich macht
- Zwölf eingefrorene Artefakt-IDs und SHA256 aus `config/control-register-repair-2026-11-16.json` gegen vollständige aktuelle Drive-Bytes prüfen. Änderungen an einer Quelle sperren deren Übernahme.
- CSV-Ledger mit bestehender Drive-ID erhalten. Nur 0210/0211 ergänzen; keine neue Nummer vergeben. 0210 erhält Report-ID und Rohbytehash. 0211 erhält seine bestehende Datei-ID und den explizit als historische Vorreparatur-Version bezeichneten Hash. Der neue aktuelle Ledgerhash steht im JSONL-Ereignis und externen Receipt; keine unmögliche Selbsthash-Behauptung.
- Vor jedem kanonischen Write auf einer neu vorab identifizierten Probe-Datei nachweisen: absichtlich falsches ETag -> HTTP412; zwei Writes mit gleichem ETag -> genau ein Commit; erneuter alter Write -> HTTP412; Rohbyte-Readback unverändert. Probe-Datei und Journal bleiben als Evidenz erhalten, auch bei Fehlern.
- Erst nach `CAS_PROBE_PASS` kanonische ID-erhaltende Writes mit genau dem gelesenen ETag versuchen. Kein unbedingter Ersatz. 412 -> Konflikt; Timeout -> Rücklesen, kein blinder Retry.
- Bestehendes `file-registry.jsonl` als unveränderten Byte-Präfix erhalten und fehlende verifizierte Versionsereignisse anhängen. Gleichwertige registrierte Datei/Revision/Hash-Kombinationen werden auch bei anderer Writer-/Operation-ID wiederverwendet. Widersprüchliche Hashes derselben Provider-Revision stoppen den Lauf.
- Ledger, Artefakte, Probe und Register nachlesen. Pro Lauf eigene unveränderliche Vorher-Dateien und Receipt; Wiederholungen überschreiben keine älteren Wiederherstellungskopien.

## Betrieb und Grenzen
Die Actions-Workflows `NEXUS GitHub to WORK` und `NEXUS Control Register Repair` verwenden dieselbe Concurrency-Gruppe `nexus-drive-canonical-writer`. Dies serialisiert diese Workflows; externe Agenten mit direktem Drive-Zugriff werden dadurch nicht gesperrt. Bedingte Writes schützen den jeweiligen geprüften Schreibvorgang, sind keine globale Schreibberechtigungsgrenze.
Die normale GitHub-Delivery verlangt nun ebenfalls Registry-Registrierung im bedingten Modus. Ein reiner Upload wird nicht als vollständige Persistenz ausgegeben.
Die Drive-v2-Medienroute ist ein getesteter Kandidat. Ein Mock-Test oder generischer HTTP-Standard ist kein Live-Nachweis, dass der Provider diese Route unterstützt. Fehlende ETags, ignorierte Preconditions oder erfolglose Konkurrenzprobe blockieren kanonische Writes. Es gibt keinen Umweg über einen bloßen Drive-Lockdateinamen.
Ledger-Update und Registry-Append sind zwei getrennte Vorgänge, keine verteilte Transaktion. Ein Registry-Konflikt nach bereits geändertem Ledger wird ausdrücklich als unbestätigter Teilzustand gemeldet. Wiederholung erkennt den bereits reparierten Ledger und versucht die fehlende Registrierung erneut.
Das geerbte `exclusive-writer`-Verfahren bleibt nur für separat tatsächlich belegte Exklusivität verfügbar; ein CLI-Flag selbst ist kein Sperrnachweis. Automatische Delivery verwendet es nicht.

## Einzelaufrufe
```powershell
py tools/configure_drive_oauth.py --renew --publish
py tools/repair_control_registers.py
py tools/repair_control_registers.py --apply
gh workflow run nexus-register-repair.yml --repo julianzotter/nexus-platform
```
Der zweite Aufruf ist lesend in Drive und schreibt nur lokale Diagnose. Bei fehlenden Credentials: `BLOCKED_DRIVE_CREDENTIALS`, keine kanonische Änderung.
Reparatur-Receipts: `reports/control-repair/<run-id>/`; jüngster Zeiger: `reports/control-repair/repair-receipt.json`. Die Dateien können interne Registry-Inhalte enthalten; nur in den autorisierten privaten Ablagen aufbewahren.

Primärreferenzen: [Google Drive v2 files.update](https://developers.google.com/workspace/drive/api/reference/rest/v2/files/update), [Drive-v2-Dateiressource mit ETag](https://developers.google.com/workspace/drive/api/reference/rest/v2/files), [OAuth für native Apps](https://developers.google.com/identity/protocols/oauth2/native-app), [OAuth-Tokenablauf/-widerruf](https://developers.google.com/identity/protocols/oauth2#expiration). Die tatsächliche HTTP400-Ursache wird ausschließlich aus dem bereinigten realen Fehlercode abgeleitet; Ablauf ist keine ungeprüfte Diagnose.
