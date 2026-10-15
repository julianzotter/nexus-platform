"""Read-only NEXUS Source Atlas query gateway. Python standard library only."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any

ALLOWED_TOOLS = frozenset({"atlas.health", "atlas.lookup"})

def open_atlas(path: str) -> sqlite3.Connection:
    """Open an existing atlas database without creating or modifying it."""
    database = Path(path).expanduser().resolve(strict=True)
    if not database.is_file():
        raise ValueError("Atlas path must be an existing file")
    conn = sqlite3.connect(f"file:{database.as_posix()}?mode=ro&immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn

def invoke(tool: str, database: str, term: str = "", limit: int = 20) -> dict[str, Any]:
    """Run explicit read-only calls; never execute arbitrary SQL or model-produced code."""
    if tool not in ALLOWED_TOOLS:
        raise ValueError("Tool not authorized")
    with open_atlas(database) as conn:
        if tool == "atlas.health":
            count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
            return {"tool": tool, "file_locations": count, "status": "OK"}
        if not 1 <= limit <= 100:
            raise ValueError("limit must be 1..100")
        if not term.strip():
            raise ValueError("term required")
        rows = conn.execute(
            "SELECT file_name, source_system, source_class, scan_status, sha256 "
            "FROM files WHERE file_name LIKE ? ESCAPE '\\' ORDER BY file_name LIMIT ?",
            ("%" + term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%", limit),
        ).fetchall()
        return {"tool": tool, "results": [dict(row) for row in rows],
                "status": "UNVERIFIED_SOURCE_METADATA"}

def to_json(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True)
