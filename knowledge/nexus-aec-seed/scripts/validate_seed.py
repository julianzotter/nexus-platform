"""Validate the NEXUS TOP20 source contract and optionally materialize SQLite.

This tool deliberately does not fetch URLs, perform design calculations or
modify the canonical NEXUS AnythingSearch or ledger databases.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit


LANES = {
    "ASSEMBLY", "REGULATION", "META_WISSEN", "STANDARD_INDEX",
    "MATERIAL_LCA", "CIRCULARITY", "RESEARCH", "PRODUCT_ASSESSMENT",
    "ENGINEERING_API", "SUSTAINABILITY", "INTEROPERABILITY",
}
CADENCES = {"weekly", "monthly"}
ACCESS = {
    "PUBLISHER_TERMS_REVIEW", "PUBLIC_METADATA", "LICENSED_FULLTEXT_EXCLUDED",
    "API_AND_LICENSE_CHECK", "OPEN_ACCESS_LICENSE_CHECK", "DATASET_LICENSE_CHECK",
    "OFFICIAL_DOCS", "OFFICIAL_LEGAL_TEXT", "OFFICIAL_SPECIFICATION",
}


def validate(data: dict) -> list[str]:
    """Return deterministic errors; nothing is implicitly trusted or ingested."""
    errors: list[str] = []
    sources = data.get("sources", [])
    if data.get("schema_version") != "1.0.0":
        errors.append("unsupported schema_version")
    if len(sources) != 20:
        errors.append(f"expected 20 sources, got {len(sources)}")
    ids: set[str] = set()
    hosts: set[str] = set()
    ranks: set[int] = set()
    for source in sources:
        key = source.get("id")
        rank = source.get("rank")
        host = source.get("host", "").lower()
        url = source.get("url", "")
        parsed = urlsplit(url)
        actual_host = (parsed.hostname or "").lower().removeprefix("www.")
        if key in ids or not key:
            errors.append(f"duplicate/blank id {key!r}")
        if host in hosts or not host:
            errors.append(f"duplicate/blank host {host!r}")
        if rank in ranks or not isinstance(rank, int) or not 1 <= rank <= 20:
            errors.append(f"invalid/duplicate rank {rank!r}")
        if parsed.scheme != "https" or actual_host != host:
            errors.append(f"host/URL mismatch: {key}")
        if source.get("lane") not in LANES:
            errors.append(f"invalid lane: {key}")
        if source.get("cadence") not in CADENCES:
            errors.append(f"invalid cadence: {key}")
        if source.get("access") not in ACCESS:
            errors.append(f"invalid access: {key}")
        if source.get("priority") not in {"P0", "P1", "P2"}:
            errors.append(f"invalid priority: {key}")
        if not source.get("method"):
            errors.append(f"missing method: {key}")
        ids.add(key)
        hosts.add(host)
        ranks.add(rank)
    if ranks != set(range(1, 21)):
        errors.append("ranks must cover 1..20")
    edges: set[tuple[str, str, str]] = set()
    for link in data.get("links", []):
        edge = (link.get("from"), link.get("relation"), link.get("to"))
        if edge[0] not in ids or edge[2] not in ids or not edge[1]:
            errors.append(f"broken edge: {edge}")
        if edge in edges:
            errors.append(f"duplicate edge: {edge}")
        edges.add(edge)
    if not all(data.get("controls", {}).values()):
        errors.append("required safety controls absent/false")
    return errors


def create_sqlite(data: dict, output: Path) -> None:
    """Build a separate source-discovery index, never the canonical registry."""
    if output.exists():
        raise FileExistsError(f"Refusing to replace existing index: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(output)
    try:
        connection.executescript("""
            CREATE TABLE sources (
                source_id TEXT PRIMARY KEY, rank INTEGER UNIQUE NOT NULL,
                host TEXT UNIQUE NOT NULL, uri TEXT NOT NULL, lane TEXT NOT NULL,
                cadence TEXT NOT NULL, access TEXT NOT NULL,
                method TEXT NOT NULL, priority TEXT NOT NULL
            );
            CREATE TABLE links (
                from_id TEXT NOT NULL, relation TEXT NOT NULL, to_id TEXT NOT NULL,
                PRIMARY KEY (from_id, relation, to_id),
                FOREIGN KEY (from_id) REFERENCES sources(source_id),
                FOREIGN KEY (to_id) REFERENCES sources(source_id)
            );
        """)
        for source in sorted(data["sources"], key=lambda s: s["rank"]):
            connection.execute(
                "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)",
                tuple(source[k] for k in (
                    "id", "rank", "host", "url", "lane", "cadence",
                    "access", "method", "priority"
                )),
            )
        for link in data["links"]:
            connection.execute(
                "INSERT INTO links VALUES (?,?,?)",
                (link["from"], link["relation"], link["to"]),
            )
        connection.commit()
    except Exception:
        connection.close()
        output.unlink(missing_ok=True)
        raise
    connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, type=Path)
    parser.add_argument("--sqlite", type=Path, help="new independent discovery index")
    args = parser.parse_args()
    data = json.loads(args.seed.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    if args.sqlite:
        create_sqlite(data, args.sqlite)
    print(f"PASS: {len(data['sources'])} sources; {len(data['links'])} links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
