"""Embed repository datasets into the self-contained NEXUS data dashboard.

Reads a fixed git revision (default HEAD) and writes two tables - tracked files and
commits - as `window.DASHBOARD_DATA` between the DATA markers in index.html.
Output is deterministic for a given revision.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]  # archive/prototypes/data-dashboard -> repo root
HTML = HERE / "index.html"
MARKERS = re.compile(r"(/\*DATA:BEGIN\*/).*?(/\*DATA:END\*/)", re.S)

FILE_COLUMNS = [
    {"key": "pfad", "label": "Pfad", "type": "text", "aliases": ["pfad", "path", "datei", "file"]},
    {"key": "ordner", "label": "Ordner", "type": "category", "aliases": ["ordner", "folder", "verzeichnis", "bereich"]},
    {"key": "typ", "label": "Dateityp", "type": "category", "aliases": ["typ", "dateityp", "endung", "extension", "format"]},
    {"key": "bytes", "label": "Größe (B)", "type": "number", "aliases": ["größe", "groesse", "bytes", "size", "speicher"]},
    {"key": "zeilen", "label": "Zeilen", "type": "number", "aliases": ["zeilen", "lines", "loc"]},
    {"key": "commits", "label": "Commits", "type": "number", "aliases": ["commits", "änderungen", "aenderungen"]},
    {"key": "geaendert", "label": "Zuletzt geändert", "type": "date", "aliases": ["datum", "geändert", "geaendert", "date"]},
]
COMMIT_COLUMNS = [
    {"key": "hash", "label": "Hash", "type": "text", "aliases": ["hash", "sha", "id"]},
    {"key": "datum", "label": "Datum", "type": "date", "aliases": ["datum", "tag", "date", "zeit"]},
    {"key": "autor", "label": "Autor", "type": "category", "aliases": ["autor", "author", "wer"]},
    {"key": "art", "label": "Art", "type": "category", "aliases": ["art", "kind"]},
    {"key": "dateien", "label": "Dateien", "type": "number", "aliases": ["dateien", "files"]},
    {"key": "plus", "label": "Zeilen +", "type": "number", "aliases": ["plus", "insertions", "hinzugefügt", "hinzugefuegt"]},
    {"key": "minus", "label": "Zeilen −", "type": "number", "aliases": ["minus", "deletions", "gelöscht", "geloescht"]},
    {"key": "betreff", "label": "Betreff", "type": "text", "aliases": ["betreff", "nachricht", "message", "subject"]},
]


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=ROOT, input=data, capture_output=True, check=True).stdout


def file_rows(rev: str) -> list[dict]:
    entries = []
    for rec in git("ls-tree", "-r", "-l", "-z", rev).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        _, kind, sha, size = meta.split()
        if kind == b"blob":
            entries.append((path.decode("utf-8"), sha.decode(), int(size)))
    batch = git("cat-file", "--batch", data="".join(sha + "\n" for _, sha, _ in entries).encode())
    lines, pos = {}, 0
    for _, sha, _ in entries:
        header_end = batch.index(b"\n", pos)
        size = int(batch[pos:header_end].split()[2])
        body = batch[header_end + 1:header_end + 1 + size]
        lines[sha] = None if b"\0" in body else body.count(b"\n") + (0 if body.endswith(b"\n") or not body else 1)
        pos = header_end + 1 + size + 1
    last, count, current = {}, {}, None
    for line in git("log", rev, "--format=\x1e%aI", "--name-only").decode("utf-8").split("\n"):  # splitlines() would split on \x1e
        if line.startswith("\x1e"):
            current = line[1:11]
        elif line:
            last.setdefault(line, current)
            count[line] = count.get(line, 0) + 1
    rows = []
    for path, sha, size in sorted(entries):
        name = path.rsplit("/", 1)[-1]
        rows.append({"pfad": path, "ordner": path.split("/")[0] if "/" in path else "(root)",
                     "typ": "." + name.rsplit(".", 1)[1].lower() if "." in name.lstrip(".") else "(ohne)",
                     "bytes": size, "zeilen": lines[sha], "commits": count.get(path, 0), "geaendert": last.get(path)})
    return rows


def commit_rows(rev: str) -> list[dict]:
    rows = []
    out = git("log", rev, "--format=\x1e%h\x1f%aI\x1f%an\x1f%P\x1f%s", "--shortstat").decode("utf-8")
    for block in out.split("\x1e")[1:]:
        head, _, stat = block.partition("\n")
        short, date, author, parents, subject = head.split("\x1f")
        num = lambda word: int(m.group(1)) if (m := re.search(r"(\d+) " + word, stat)) else 0
        rows.append({"hash": short, "datum": date, "autor": author,
                     "art": "Merge" if len(parents.split()) > 1 else "Commit",
                     "dateien": num("file"), "plus": num("insertion"), "minus": num("deletion"), "betreff": subject})
    return rows


def build(rev: str = "HEAD") -> dict:
    full = git("rev-parse", rev).decode().strip()
    source = f"git {full[:12]}"
    return {"revision": full, "datasets": {
        "dateien": {"title": "Repository-Dateien", "source": source + " · ls-tree, cat-file, log",
                    "columns": FILE_COLUMNS, "rows": file_rows(full)},
        "commits": {"title": "Commit-Historie", "source": source + " · log --shortstat",
                    "columns": COMMIT_COLUMNS, "rows": commit_rows(full)},
    }}


def embed(html: str, data: dict) -> str:
    payload = "window.DASHBOARD_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"
    if not MARKERS.search(html):
        raise ValueError("DATA markers missing in index.html")
    return MARKERS.sub(lambda m: m.group(1) + payload + m.group(2), html, count=1)


def main(argv: list[str]) -> int:
    rev = argv[1] if len(argv) > 1 else "HEAD"
    data = build(rev)
    HTML.write_text(embed(HTML.read_text(encoding="utf-8"), data), encoding="utf-8", newline="\n")
    sets = data["datasets"]
    print(f"{len(sets['dateien']['rows'])} Dateien, {len(sets['commits']['rows'])} Commits @ {data['revision'][:12]} -> {HTML}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
