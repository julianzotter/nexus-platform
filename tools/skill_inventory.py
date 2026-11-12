#!/usr/bin/env python3
"""Read-only inventory of SKILL.md packages with structural checks and SHA-256.

Structure and byte identity only. Functional behaviour needs execution tests,
and human release needs its own recorded approval. Missing fields are UNKNOWN.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("name", "description")
OPTIONAL = ("version", "owner", "tools", "runtime")


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Parse a flat `key: value` YAML frontmatter block without external deps."""
    if not text.startswith("---\n"):
        return None, "NO_FRONTMATTER"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "FRONTMATTER_NOT_CLOSED"
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or line[0] in " \t":
            return None, "FRONTMATTER_NOT_FLAT"
        if key in fields:
            return None, f"DUPLICATE_KEY:{key}"
        fields[key.strip()] = value.strip().strip('"')
    return fields, None


def inventory_skill(path: Path, root: Path = ROOT) -> dict[str, Any]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="strict")
    fields, error = parse_frontmatter(text)
    issues: list[str] = [] if error is None else [error]
    fields = fields or {}
    missing = [k for k in REQUIRED if not fields.get(k)]
    issues += [f"MISSING_REQUIRED:{k}" for k in missing]
    record: dict[str, Any] = {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "id": fields.get("name") or None,
    }
    for key in REQUIRED + OPTIONAL:
        record[key] = fields.get(key) or "UNKNOWN"
    unknown = [k for k in OPTIONAL if record[k] == "UNKNOWN"]
    if error or missing:
        record["status"] = "INVALID"
    elif unknown:
        record["status"] = "INCOMPLETE"
    else:
        record["status"] = "VALID_STRUCTURE"
    record["issues"] = issues + [f"UNKNOWN:{k}" for k in unknown]
    return record


def find_duplicate_ids(records: list[dict[str, Any]]) -> list[str]:
    seen: dict[str, int] = {}
    for rec in records:
        if rec.get("package_kind") == "ARCHIVAL_SNAPSHOT":
            continue
        if rec["id"]:
            seen[rec["id"]] = seen.get(rec["id"], 0) + 1
    return sorted(k for k, n in seen.items() if n > 1)


def classify_snapshot(record: dict[str, Any], root: Path) -> None:
    """Only manifest-hash-verified frozen Claude artifacts are archival."""
    rel = Path(record["path"])
    snapshot_root = root / "skills" / "claude-ai"
    if rel.parts[:2] != ("skills", "claude-ai"):
        record["package_kind"] = "EXECUTABLE_CANDIDATE"
        return
    manifest = snapshot_root / "MANIFEST.sha256"
    expected: dict[str, str] = {}
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                expected[Path(parts[1].lstrip("*")).as_posix()] = parts[0]
    snapshot_rel = (root / rel).relative_to(snapshot_root).as_posix()
    record["raw_structure_status"] = record["status"]
    if expected.get(snapshot_rel) == record["sha256"]:
        record["package_kind"] = "ARCHIVAL_SNAPSHOT"
        record["status"] = "ARCHIVAL_SNAPSHOT"
    else:
        record["package_kind"] = "UNVERIFIED_SNAPSHOT"
        record["status"] = "INVALID"
        record["issues"].append("SNAPSHOT_MANIFEST_HASH_MISSING_OR_MISMATCH")


def build_report(root: Path = ROOT) -> dict[str, Any]:
    paths = sorted(root.glob("skills/**/SKILL.md"))
    records = [inventory_skill(p, root) for p in paths]
    for record in records:
        classify_snapshot(record, root)
    dups = find_duplicate_ids(records)
    for rec in records:
        if rec["id"] in dups and rec.get("package_kind") != "ARCHIVAL_SNAPSHOT":
            rec["issues"].append("DUPLICATE_ID")
            rec["status"] = "INVALID"
    counts: dict[str, int] = {}
    for rec in records:
        counts[rec["status"]] = counts.get(rec["status"], 0) + 1
    return {"packages": records, "duplicate_ids": dups, "counts": counts,
            "scope": "structure_and_bytes_only"}


def to_markdown(report: dict[str, Any]) -> str:
    lines = ["# Skill-/Agent-Inventar (Struktur und SHA-256)", "",
             "Geprüft: Frontmatter, Pflichtfelder, Duplikate, Bytehash. "
             "Nicht geprüft: Funktion, Freigabe.", "",
             "| Pfad | ID | Status | SHA-256 | Probleme |", "|---|---|---|---|---|"]
    for r in report["packages"]:
        lines.append(f"| {r['path']} | {r['id'] or 'UNKNOWN'} | {r['status']} | "
                     f"`{r['sha256'][:16]}…` | {', '.join(r['issues']) or '-'} |")
    lines += ["", f"Zählung: {report['counts']}", f"Duplikat-IDs: {report['duplicate_ids'] or 'keine'}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "reports" / "skills"))
    parser.add_argument("--strict", action="store_true", help="exit 1 on INVALID packages")
    args = parser.parse_args(argv)
    report = build_report()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "skill-inventory.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "skill-inventory.md").write_text(to_markdown(report), encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False))
    invalid = report["counts"].get("INVALID", 0)
    return 1 if (args.strict and invalid) else 0


if __name__ == "__main__":
    sys.exit(main())

