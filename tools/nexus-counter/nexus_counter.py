#!/usr/bin/env python3
"""nexus_counter.py v0.1.0 | agent_id: ID06 | status: ENTWURF | ticket: WO-NEXUS-CATALOG-01 (Slice B)

NEXUS-Zaehler: EIN Schreiber vergibt die laufende Artefaktnummer.
- sucht in --work Dateien, deren Name auf _LEDGER-PENDING oder _UNREGISTERED endet
- vergibt die naechste freie Nummer (hoechste ID im Ledger + 1), aelteste Datei zuerst
- haengt je Datei eine Zeile an das Ledger (CSV) und an das History-Logfile an
- benennt die Datei um: Marker -> Nummer (AGB v005: Artefaktnummer am Ende)

Loescht nichts, verschiebt nichts. Ohne --apply nur Vorschau (Dry-Run).
Nur Python-Standardbibliothek. Agenten vergeben selbst KEINE Nummern.

  python nexus_counter.py --work <WORK> --ledger <00_ID_LEDGER.csv> --log <HISTORYLOG> [--apply]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path

MARKER = re.compile(r"_(LEDGER-PENDING|UNREGISTERED)(?=\.[A-Za-z0-9]+$|$)")
NAME = re.compile(r"^(\d\d)_(\d\d)_(\d\d)_\d{4}_(ID\d\d)_([^_]+)_")
USED = re.compile(r"^\d\d_\d\d_\d\d_\d{4}_ID\d\d_.*_(\d{4})(?:\.[A-Za-z0-9]+)?$")


def next_id(ledger: Path, work: Path) -> tuple[int, list[str]]:
    """Hoechste ID aus Ledger UND bereits nummerierten WORK-Dateinamen + 1, dazu die Kopfzeile."""
    with open(ledger, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        raise SystemExit("Ledger ist leer: keine Kopfzeile")
    ids = [int(r[0]) for r in rows[1:] if r and r[0].strip().isdigit()]
    ids += [int(m.group(1)) for m in (USED.match(f.name) for f in work.iterdir()) if m]
    return (max(ids) + 1 if ids else 1), rows[0]


def pending(work: Path) -> list[Path]:
    """Offene Dateien direkt in WORK, aelteste zuerst (mtime, dann Name)."""
    files = [p for p in work.iterdir() if p.is_file() and MARKER.search(p.name)]
    return sorted(files, key=lambda p: (p.stat().st_mtime, p.name))


def ledger_row(header: list[str], num: str, new_name: str, path: Path) -> list[str]:
    """Zeile passend zur vorhandenen Kopfzeile; unbekannte Spalten bleiben leer."""
    m = NAME.match(new_name)
    values = {
        "ID": num,
        "DATE": f"20{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "",
        "TYPE": m.group(5) if m else "",
        "TITLE": new_name,
        "FOLDER": path.parent.name,
        "SHA256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "ACTOR": m.group(4) if m else "",
        "NAME_SCHEMA_OK": "1" if m else "0",
        "NOTE": "allocated by nexus_counter",
    }
    return [values.get(col.strip(), "") for col in header]


def allocate(work: Path, ledger: Path, log: Path, apply: bool) -> int:
    """Vergibt Nummern. Rueckgabe: Anzahl bearbeiteter Dateien."""
    number, header = next_id(ledger, work)
    todo = pending(work)
    for path in todo:
        num = f"{number:04d}"
        new_name = MARKER.sub(f"_{num}", path.name)
        target = path.with_name(new_name)
        print(f"{num} | {path.name} -> {new_name}")
        if apply:
            if target.exists():
                raise SystemExit(f"Ziel existiert bereits: {new_name}")
            with open(ledger, "a", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerow(ledger_row(header, num, new_name, path))
            stamp = datetime.now().astimezone().isoformat(timespec="seconds")
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(f"{stamp}|COUNTER|{num}|{path.name} -> {new_name}\n")
            path.rename(target)
        number += 1
    print(f"{'vergeben' if apply else 'vorschau'}={len(todo)} naechste_freie_id={number:04d}")
    return len(todo)


def main() -> int:
    ap = argparse.ArgumentParser(description="NEXUS-Zaehler fuer Artefaktnummern")
    ap.add_argument("--work", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--apply", action="store_true", help="ohne diesen Schalter nur Vorschau")
    args = ap.parse_args()
    lock = Path(args.ledger).with_suffix(".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)  # zweiter Lauf bricht ab
    except FileExistsError:
        print(f"Sperre vorhanden ({lock.name}): ein anderer Lauf ist aktiv oder abgebrochen")
        return 2
    try:
        allocate(Path(args.work), Path(args.ledger), Path(args.log), args.apply)
    finally:
        os.close(fd)
        os.remove(lock)  # nur die eigene Sperrdatei des Skripts
    return 0


if __name__ == "__main__":
    sys.exit(main())
