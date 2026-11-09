"""Build an immutable, local W012 evidence-search projection; no engineering approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import tempfile
import time
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT.parent / "W012_Work" / "W012_Hoftrakt.sqlite"
FIELDS = ("id", "title", "body", "url", "status", "source_kind")


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower().replace("ß", "ss"))
    return "".join(c for c in decomposed if not unicodedata.category(c).startswith("M"))


def tokens(value: str) -> list[str]:
    return re.findall(r"[^\W_]+", normalize(value), flags=re.UNICODE)


def readonly(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db


def baseline_documents(db: sqlite3.Connection) -> list[dict[str, str]]:
    sources = {r["id"]: dict(r) for r in db.execute("SELECT * FROM sources")}
    relations: dict[str, list[str]] = {}
    for r in db.execute("SELECT * FROM record_sources ORDER BY 1,2"):
        relations.setdefault(r["record_id"], []).append(r["source_id"])
    documents = []
    for table in ("sources", "records", "assemblies", "layers"):
        for result in db.execute("SELECT * FROM " + table):
            row = dict(result)
            key = row.get("id", f"{row.get('assembly_id')}:L{row.get('ordinal')}")
            title = row.get("title", row.get("material", str(key)))
            refs = relations.get(str(key), [])
            if "source_id" in row:
                refs = [row["source_id"]]
            if table == "layers":
                refs = relations.get(row["assembly_id"], [])
            evidence = [sources[s] for s in refs]
            body = canonical({"row": row, "sources": evidence})
            url = row.get("url") or (evidence[0]["url"] if evidence else "")
            identifier = "ASSEMBLY:" + str(key) if table == "assemblies" else str(key)
            documents.append(dict(id=identifier, title=title, body=body, url=url,
                                  status=row.get("status", "UNVERIFIED"), source_kind=table))
    return documents


def structured_documents(value: Any) -> list[dict[str, str]] | None:
    if not isinstance(value, list) or not all(isinstance(row, dict) and set(FIELDS) <= row.keys() for row in value):
        return None
    documents = []
    for row in value:
        if not all(isinstance(row[field], str) for field in FIELDS) or not row["id"].strip():
            raise ValueError("Structured documents require nonempty IDs and string document fields")
        document = {field: row[field] for field in FIELDS}
        metadata = {key: item for key, item in row.items() if key not in FIELDS}
        if metadata:
            document["body"] += "\n\nSupplement metadata: " + canonical(metadata)
        documents.append(document)
    return documents


def extra_documents(directory: Path | None) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    documents: list[dict[str, str]] = []
    inputs: list[dict[str, str]] = []
    if directory is None:
        return documents, inputs
    if not directory.is_dir():
        raise ValueError(f"Extras directory missing: {directory}")
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".md", ".json"):
            continue
        relative = path.relative_to(directory).as_posix()
        content = path.read_text(encoding="utf-8")
        inputs.append({"path": relative, "sha256": digest(path)})
        if path.suffix.lower() == ".json":
            expanded = structured_documents(json.loads(content))
            if expanded is not None:
                documents.extend(expanded)
                continue
        headings = re.findall(r"^#\s+(.+)$", content, re.MULTILINE)
        documents.append(dict(id="EXTRA:" + relative, title=headings[0] if headings else path.stem,
                              body=content, url="", status="UNVERIFIED", source_kind="supplement"))
    return documents, inputs


def prepare_documents(documents: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    for document in documents:
        key = normalize(document["id"])
        if key in seen:
            raise ValueError(f"Duplicate normalized document ID: {key}")
        seen.add(key)
        document["normalized_id"] = key
        document["search_text"] = " ".join(tokens(" ".join(document[f] for f in FIELDS)))
    return sorted(documents, key=lambda document: document["id"])


def add_projection(db: sqlite3.Connection, payload: dict[str, Any]) -> None:
    db.executescript("""
    CREATE TABLE knowledge_metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
    CREATE TABLE knowledge_documents(
      id TEXT PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL, url TEXT NOT NULL,
      status TEXT NOT NULL, source_kind TEXT NOT NULL,
      normalized_id TEXT NOT NULL UNIQUE, search_text TEXT NOT NULL);
    CREATE VIRTUAL TABLE knowledge_fts USING fts5(
      id UNINDEXED, search_text, tokenize='unicode61 remove_diacritics 0');
    """)
    db.executemany("INSERT INTO knowledge_metadata VALUES (?,?)",
                   [(k, canonical(v)) for k, v in payload.items() if k != "documents"])
    db.executemany("INSERT INTO knowledge_documents VALUES "
                   "(:id,:title,:body,:url,:status,:source_kind,:normalized_id,:search_text)",
                   payload["documents"])
    db.execute("INSERT INTO knowledge_fts SELECT id,search_text FROM knowledge_documents ORDER BY id")
    if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise RuntimeError("Integrity check failed")
    if db.execute("PRAGMA foreign_key_check").fetchall():
        raise RuntimeError("Foreign keys failed")
    db.commit()


def search(db: sqlite3.Connection, query: str, limit: int = 50) -> list[dict[str, Any]]:
    query_tokens = tokens(query)
    if not query_tokens:
        return []
    # Tokens contain only Unicode letters/numbers; quoting removes query syntax.
    expression = " AND ".join('"' + token + '"*' for token in query_tokens)
    rows = db.execute("""SELECT d.* FROM knowledge_documents d
      WHERE normalized_id=? OR id IN (SELECT id FROM knowledge_fts WHERE knowledge_fts MATCH ?)
      ORDER BY CASE WHEN normalized_id=? THEN 0 ELSE 1 END,id LIMIT ?""",
      (normalize(query.strip()), expression, normalize(query.strip()), limit))
    return [dict(row) for row in rows]


HTML = '''<!doctype html><html lang="de"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>W012 · Evidenzsuche v0.3</title>
<style>body{font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px;background:#f4f6f3;color:#152b27}input{font:inherit;padding:12px;width:95%;border:1px solid #57766a}article{background:white;padding:18px;margin:14px 0;border:1px solid #ccd8d0;border-radius:8px}h2{font-size:19px;margin:5px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.5 ui-monospace}small{overflow-wrap:anywhere}a{color:#195844}.notice{border-left:4px solid #a66a14;padding:12px;background:#fff4dc}</style>
<h1>W012 · Evidenzsuche v0.3</h1><p class="notice">Lokale Suchprojektion. Evidenzstatus ist keine technische Freigabe. Originale und Quellenrevisionen vor Verwendung prüfen. Kein Live-Sync.</p>
<label for="query">IDs, Schichtmaterialien, Quellen und Ergänzungen</label><p><input id="query" type="search" placeholder="PAR-01 · Gipskarton · IW01h"></p><p id="count" aria-live="polite"></p><small id="snapshot-id"></small><main id="results"></main>
<script type="application/json" id="data">__DATA__</script><script>
"use strict";
const data=JSON.parse(document.querySelector('#data').textContent);
const normalize=value=>String(value).toLowerCase().replaceAll('ß','ss').normalize('NFD').replace(/\\p{M}/gu,'');
const tokens=value=>normalize(value).match(/[\\p{L}\\p{N}]+/gu)||[];
const create=(tag,value)=>{const el=document.createElement(tag);el.textContent=value;return el;};
function safeUrl(value){try{const url=new URL(value);return url.protocol==='https:'?url.href:null;}catch{return null;}}
function lookup(query){const terms=tokens(query),key=normalize(query.trim());
 return data.documents.filter(d=>d.normalized_id===key||terms.every(t=>d.search_text.split(' ').some(w=>w.startsWith(t))))
 .sort((a,b)=>(a.normalized_id===key?0:1)-(b.normalized_id===key?0:1)||(a.id<b.id?-1:a.id>b.id?1:0));}
function render(){const query=document.querySelector('#query').value,rows=lookup(query);
 const fragment=document.createDocumentFragment();
 for(const d of rows.slice(0,100)){const card=create('article','');card.append(create('small',d.id+' · '+d.source_kind+' · '+d.status),create('h2',d.title));
 const details=create('details','');details.append(create('summary','Vollständigen Datensatz anzeigen'),create('pre',d.body));card.append(details);
 const url=safeUrl(d.url);if(url){const link=create('a','Originalquelle');link.href=url;link.target='_blank';link.rel='noopener noreferrer';card.append(link);}
 fragment.append(card);}document.querySelector('#results').replaceChildren(fragment);
 document.querySelector('#count').textContent=rows.length+' Treffer · '+data.documents.length+' Dokumente · maximal 100 angezeigt';}
document.querySelector('#snapshot-id').textContent='Snapshot: '+data.snapshot_id;
document.querySelector('#query').addEventListener('input',render);render();
</script></html>'''


def validate(output: Path, payload: dict[str, Any]) -> dict[str, Any]:
    with readonly(output / "W012_Knowledge.sqlite") as db:
        actual = [dict(row) for row in db.execute("SELECT * FROM knowledge_documents ORDER BY id")]
        if actual != payload["documents"]:
            raise RuntimeError("SQL / JSON mismatch")
        timings: dict[str, Any] = {}
        for query, expected in (("PAR-01", "PAR-01"), ("Gipskarton", "BTL-IW01h:L2")):
            started = time.perf_counter()
            found = search(db, query)
            elapsed = (time.perf_counter() - started) * 1000
            if expected not in {r["id"] for r in found}:
                raise RuntimeError(f"Missing reference result: {query}")
            timings[query] = {"milliseconds": elapsed, "hits": len(found), "expected_id": expected}
        return {"integrity_check": "ok", "foreign_key_check": [], "sql_json_equal": True,
                "timing_scope": "single local query incl. row materialization; not end-to-end or comparative", "queries": timings}


def build(baseline: Path, output: Path, extras: Path | None = None) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"Immutable output already exists; choose a new --output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".knowledge-", dir=output.parent))
    try:
        extra, extra_inputs = extra_documents(extras)
        with readonly(baseline) as source, sqlite3.connect(temporary / "W012_Knowledge.sqlite") as target:
            documents = prepare_documents(baseline_documents(source) + extra)
            identity = {"schema_version": "0.3", "baseline_sha256": digest(baseline),
                        "builder_sha256": digest(Path(__file__)), "extra_inputs": extra_inputs, "documents": documents}
            snapshot_id = "sha256:" + hashlib.sha256(canonical(identity).encode()).hexdigest()
            payload = {**identity, "snapshot_id": snapshot_id, "engineering_release": "NOT_GRANTED"}
            source.backup(target)
            add_projection(target, payload)
        (temporary / "W012_Knowledge.json").write_text(canonical(payload) + "\n", encoding="utf-8")
        embedded = canonical(payload).replace("<", "\\u003c")
        (temporary / "W012_Knowledge.html").write_text(HTML.replace("__DATA__", embedded), encoding="utf-8")
        qa = validate(temporary, payload)
        (temporary / "validation.json").write_text(canonical(qa) + "\n", encoding="utf-8")
        manifest = {"snapshot_id": snapshot_id, "schema_version": "0.3", "engineering_release": "NOT_GRANTED",
                    "document_count": len(documents), "files": {p.name: digest(p) for p in sorted(temporary.iterdir())}}
        (temporary / "manifest.json").write_text(canonical(manifest) + "\n", encoding="utf-8")
        temporary.rename(output)
        return manifest
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--output", type=Path, default=ROOT / "snapshot_v03")
    parser.add_argument("--extras", type=Path)
    parser.add_argument("--search")
    arguments = parser.parse_args()
    if arguments.search is not None:
        with readonly(arguments.output / "W012_Knowledge.sqlite") as db:
            print(canonical(search(db, arguments.search)))
    else:
        print(canonical(build(arguments.baseline, arguments.output, arguments.extras)))


if __name__ == "__main__":
    main()
