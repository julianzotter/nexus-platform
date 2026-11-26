"""WORK file-name rule (_AGBS.md v005) and ID03 gate header - shared by the MCP gateway and CI.

Moved from tools/nexus-tower/nexus_tower.py v0.2.1 (archived 2026-11-26, ID01 decision).
Rule: YY_MM_DD_HHMM_ID##_THEMA_###; ending LEDGER-PENDING/UNREGISTERED = number still open.
Verdict strings are kept unchanged because tools/naming_gate.py compares them.
"""
from __future__ import annotations

import os
import re
from datetime import date, datetime
from pathlib import Path

GATE_KEYS = ("status", "problems", "open_questions", "tasks_open")


def name_check(title: str) -> tuple[str, str]:
    """(verdict, reason) for one file name; verdict in konform, Nummer offen, Abweichung, Verstoss, Steuerdatei, ueberholt."""
    if title.startswith("_"):
        return "Steuerdatei", ""
    if re.search(r"_UEBERHOLT(\.[A-Za-z0-9]+)?$", title):
        return "ueberholt", ""
    if not re.match(r"^\d\d_\d\d_\d\d_", title):
        return "Verstoss", "kein Datumspraefix JJ_MM_TT"
    if re.match(r"^\d\d_\d\d_\d\d_\d\d_\d\d_", title):
        return "Verstoss", "Zeit als HH_MM statt HHMM"
    m = re.match(r"^\d\d_\d\d_\d\d_(\d\d)(\d\d)_", title)
    if not m:
        return "Verstoss", "kein HHMM nach dem Datum"
    if int(m.group(1)) > 23 or int(m.group(2)) > 59:
        return "Verstoss", "vier Ziffern nach dem Datum sind keine Uhrzeit"
    if not re.match(r"^\d\d_\d\d_\d\d_\d{4}_ID\d\d_", title):
        return "Verstoss", "keine Rollen-ID direkt nach HHMM"
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", title)
    if re.search(r"_\d{3,4}$", stem):
        return "konform", ""
    if re.search(r"_(LEDGER-PENDING|UNREGISTERED)$", stem):
        return "Nummer offen", ""
    return "Abweichung", "Ende ohne Artefaktnummer oder LEDGER-PENDING"


def list_files(folder: Path, limit: int = 300) -> tuple[list[dict], int]:
    """Newest regular files directly in folder (name, mtime ms, size) and total count. Symlinks are skipped."""
    rows = []
    with os.scandir(folder) as it:
        for entry in it:
            try:
                if entry.is_file(follow_symlinks=False):
                    st = entry.stat(follow_symlinks=False)
                    rows.append({"name": entry.name, "mtime": int(st.st_mtime * 1000), "size": st.st_size})
            except OSError:
                continue
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows[:limit], len(rows)


def naming_report(folder: Path, day: date | None = None) -> dict:
    """Counts and problems for files in folder modified on day (default: today, local time). Hidden files are skipped."""
    day = day or datetime.now().date()
    files, _ = list_files(folder, limit=10_000)
    counts: dict[str, int] = {}
    problems = []
    for f in files:
        if f["name"].startswith(".") or datetime.fromtimestamp(f["mtime"] / 1000).date() != day:
            continue
        verdict, reason = name_check(f["name"])
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict in ("Verstoss", "Abweichung"):
            problems.append({"name": f["name"], "verdict": verdict, "reason": reason})
    return {"date": day.isoformat(), "counts": counts, "problems": problems}


def _header_value(lines: list[str], key: str) -> str | None:
    for i, ln in enumerate(lines):
        if ln.startswith(key + ":"):
            value = ln[len(key) + 1:].strip().strip("'\"")
            if value:
                return value
            items = []
            for nxt in lines[i + 1:]:
                if not nxt.startswith("- "):
                    break
                items.append(nxt[2:])
            return ", ".join(items)
    return None


def read_gate(folder: Path) -> dict:
    """Frontmatter keys of the newest ID03 status report in folder ({} if none)."""
    files, _ = list_files(folder, limit=10_000)
    hit = next((f for f in files if "ID03_STATUSREPORT" in f["name"]), None)
    if not hit:
        return {}
    try:
        head = (folder / hit["name"]).read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return {"title": hit["name"], "mtime": hit["mtime"], "status": "nicht lesbar"}
    lines = [ln.strip() for ln in head.splitlines()]
    out = {"title": hit["name"], "mtime": hit["mtime"]}
    for key in GATE_KEYS:
        value = _header_value(lines, key)
        if value is not None:
            out[key] = value
    return out
