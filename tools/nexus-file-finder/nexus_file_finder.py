#!/usr/bin/env python3
"""NEXUS File Finder v0.1.0 – Stichwort-Routing + SQLite-FTS5 über files.csv (AnythingSearch-Export).

Build:   python -I nexus_file_finder.py build  --csv files.csv --db nexus_index.db
Search:  python -I nexus_file_finder.py search --db nexus_index.db --route rfem6_api --top 20
         python -I nexus_file_finder.py search --db nexus_index.db --q "grpc 9000" --ext py,md
Read-only auf der Quelle; schreibt nur nexus_index.db. Komplexität: Build O(n), Suche O(log n + k).
"""
from __future__ import annotations
import argparse, csv, re, sqlite3, sys, time
from pathlib import Path

# Routentabelle: Route -> (Suchbegriffe inkl. Synonyme, bevorzugte Endungen, Pfad-Boost-Wörter)
ROUTES: dict[str, tuple[list[str], list[str], list[str]]] = {
    "rfem5_com":  (["rfem5", "rf5", "com", "comtypes", "pywin32", "RFEM5.Application", "LockLicense", "5.29"],
                   ["py", "ps1", "txt", "md", "docx", "rf5"], ["SEILSTATIK", "RFEM5_COM"]),
    "rfem6_api":  (["rfem6", "rf6", "dlubal.api", "grpc", "api-ii", "9000", "webservice", "RFEM6Server"],
                   ["py", "md", "txt", "json", "html", "url"], ["RFEM6", "API", "MCP"]),
    "rfem_mcp":   (["mcp", "dlubal-mcp", "dlubal_mcp", "bridge", "stdio", "FastMCP", "mcp_config"],
                   ["py", "md", "json", "txt"], ["MCP", "skills", "plugins"]),
    "python":     (["python", "py", "venv", "pip", "notebook", "ipynb", "colab"],
                   ["py", "ipynb", "md"], ["_developement", "skills", "WORK"]),
    "anything":   (["anythingsearch", "AnythingSearch.db", "files.csv", "refresh", "index"],
                   ["py", "db", "csv", "md", "json"], ["00-AnythingSearch", "_INDEX_LNK"]),
}

def build(csv_path: Path, db_path: Path) -> int:
    """CSV (path,name,ext,size,mtime) -> FTS5-Tabelle mit Trigram-Tokenizer (Substring-Suche in Pfaden)."""
    con = sqlite3.connect(db_path)
    con.executescript("""
    DROP TABLE IF EXISTS files; DROP TABLE IF EXISTS fts;
    CREATE TABLE files(id INTEGER PRIMARY KEY, path TEXT, name TEXT, ext TEXT, size INTEGER, mtime TEXT);
    CREATE VIRTUAL TABLE fts USING fts5(path, name, content='files', content_rowid='id', tokenize='trigram');
    """)
    n = 0
    with csv_path.open(encoding="utf-8", errors="replace", newline="") as fh:
        rd = csv.DictReader(fh)
        rows = []
        for r in rd:  # Spaltennamen tolerant lesen
            p = r.get("path") or r.get("FullPath") or r.get("full_path") or ""
            nm = r.get("name") or Path(p).name
            ext = (r.get("ext") or Path(p).suffix.lstrip(".")).lower()
            rows.append((p, nm, ext, int(r.get("size") or 0), r.get("mtime") or r.get("modified") or ""))
            if len(rows) >= 5000:
                con.executemany("INSERT INTO files(path,name,ext,size,mtime) VALUES(?,?,?,?,?)", rows); n += len(rows); rows = []
        if rows:
            con.executemany("INSERT INTO files(path,name,ext,size,mtime) VALUES(?,?,?,?,?)", rows); n += len(rows)
    con.execute("INSERT INTO fts(fts) VALUES('rebuild')")
    con.commit(); con.close()
    return n

def fts_query(terms: list[str]) -> str:
    """Trigram-FTS: Begriffe als OR-Verknüpfung in Anführungszeichen (>=3 Zeichen)."""
    safe = [t.replace('"', "") for t in terms if len(t) >= 3]
    return " OR ".join(f'"{t}"' for t in safe) or '"___"'

def search(db_path: Path, terms: list[str], exts: list[str], boosts: list[str], top: int) -> list[tuple]:
    """BM25-Ranking + Boost für Endung und Pfadwörter + Recency; gibt (score, path, ext, size, mtime)."""
    con = sqlite3.connect(db_path)
    sql = """SELECT f.path, f.ext, f.size, f.mtime, bm25(fts) AS rank FROM fts
             JOIN files f ON f.id = fts.rowid WHERE fts MATCH ? ORDER BY rank LIMIT ?"""
    out = []
    for path, ext, size, mtime, rank in con.execute(sql, (fts_query(terms), top * 10)):
        score = -rank  # bm25: kleiner = besser
        score += 2.0 if ext in exts else 0.0
        score += sum(1.5 for b in boosts if b.lower() in path.lower())
        score += 1.0 if mtime[:4] >= "2026" else 0.0
        out.append((round(score, 2), path, ext, size, mtime))
    con.close()
    return sorted(out, reverse=True)[:top]

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--csv", type=Path, required=True); b.add_argument("--db", type=Path, required=True)
    s = sub.add_parser("search"); s.add_argument("--db", type=Path, required=True)
    s.add_argument("--route", choices=sorted(ROUTES)); s.add_argument("--q", default="")
    s.add_argument("--ext", default=""); s.add_argument("--top", type=int, default=20)
    a = ap.parse_args(); t0 = time.time()
    if a.cmd == "build":
        n = build(a.csv, a.db); print(f"indexed {n} rows -> {a.db} in {time.time()-t0:.1f}s"); return 0
    terms, exts, boosts = ([], [], [])
    if a.route:
        terms, exts, boosts = ROUTES[a.route]
    terms = terms + [t for t in re.split(r"[\s,;]+", a.q) if t]
    exts = [e.strip().lower() for e in a.ext.split(",") if e.strip()] or exts
    for sc, p, e, sz, mt in search(a.db, terms, exts, boosts, a.top):
        print(f"{sc:6.2f} | {e:5} | {mt[:10]:10} | {p}")
    print(f"-- {time.time()-t0:.3f}s", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
