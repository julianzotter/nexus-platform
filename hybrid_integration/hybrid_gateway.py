"""Read-only NEXUS Source Atlas gateway for immutable SQLite snapshots."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any

ALLOWED_TOOLS = frozenset({'atlas.health', 'atlas.lookup'})
REQUIRED_COLUMNS = {'file_name', 'source_system', 'source_class', 'scan_status', 'sha256'}


class AtlasSchemaError(ValueError):
    """The database is readable but not compatible with this adapter."""


def open_atlas(path: str) -> sqlite3.Connection:
    """Open only an existing, immutable SQLite snapshot; never create it."""
    database = Path(path).expanduser().resolve(strict=True)
    if not database.is_file():
        raise ValueError('Atlas path must be an existing file')
    # Path.as_uri() percent-encodes URI control characters (#, ?, %, spaces).
    uri = database.as_uri() + '?mode=ro&immutable=1'
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute('PRAGMA query_only = ON')
        row = conn.execute("SELECT type FROM sqlite_master WHERE name='files'").fetchone()
        if row is None or row[0] != 'table':
            raise AtlasSchemaError("Incompatible Atlas schema: required table 'files' not found")
        columns = {item[1] for item in conn.execute('PRAGMA table_info(files)')}
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise AtlasSchemaError('Incompatible Atlas schema: missing files columns: ' + ', '.join(sorted(missing)))
        return conn
    except Exception:
        conn.close()
        raise


def invoke(tool: str, database: str, term: str = '', limit: int = 20) -> dict[str, Any]:
    """Allow only bounded read-only queries, with no arbitrary SQL execution."""
    if tool not in ALLOWED_TOOLS:
        raise ValueError('Tool not authorized')
    if tool == 'atlas.lookup':
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
            raise ValueError('limit must be 1..100')
        if not isinstance(term, str) or not term.strip():
            raise ValueError('term required')
    with open_atlas(database) as conn:
        if tool == 'atlas.health':
            count = conn.execute('SELECT COUNT(*) FROM files').fetchone()[0]
            return {'tool': tool, 'file_locations': count, 'status': 'OK'}
        escaped = term.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        rows = conn.execute(
            "SELECT file_name, source_system, source_class, scan_status, sha256 "
            "FROM files WHERE file_name LIKE ? ESCAPE '\\' ORDER BY file_name LIMIT ?",
            ('%' + escaped + '%', limit),
        ).fetchall()
        return {'tool': tool, 'results': [dict(row) for row in rows],
                'status': 'UNVERIFIED_SOURCE_METADATA'}


def to_json(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True)
