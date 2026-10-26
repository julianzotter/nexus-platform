"""Build designs.manifest.js for the NEXUS design gallery.

Scans tracked repository files for HTML designs, prototype JS modules and the
concept catalog, merges curated architecture drafts and writes a JS file that
index.html loads via <script src> (works from file:// without a server).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

GALLERY = Path(__file__).resolve().parent
ROOT = GALLERY.parents[1]
CATALOG = "docs/concepts/2026-10-13/catalog.json"
DEMOS = {"prototypes/nexus-dashboard-v3/ec5_solver.js": "ec5",
         "prototypes/nexus-dashboard-v3/osr9_mmr.js": "mmr"}


def tracked_files(root: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True)
        return sorted(out.stdout.splitlines())
    except (OSError, subprocess.CalledProcessError):
        return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)


def commit(root: Path) -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def html_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    start = text.find("<title>")
    end = text.find("</title>", start)
    return text[start + 7:end].strip() if start >= 0 and end > start else path.stem


def readme_summary(folder: Path) -> str:
    readme = folder / "README.md"
    if not readme.exists():
        return ""
    lines = [l.strip() for l in readme.read_text(encoding="utf-8").splitlines()]
    return " ".join(l for l in lines if l and not l.startswith("#"))[:420]


def scan(root: Path) -> list[dict]:
    designs = []
    gallery_rel = GALLERY.relative_to(ROOT).as_posix() if root == ROOT else "prototypes/design-gallery"
    for rel in tracked_files(root):
        path = root / rel
        if rel.startswith(gallery_rel + "/") or not path.is_file():
            continue
        if rel.endswith(".html"):
            designs.append({
                "id": "HTML-" + hashlib.sha1(rel.encode()).hexdigest()[:8].upper(),
                "title": html_title(path), "kind": "html", "path": rel,
                "preview": "../../" + rel, "sha256": sha256(path), "bytes": path.stat().st_size,
                "status": "prototype_unreviewed", "summary": readme_summary(path.parent),
                "tags": [p for p in rel.split("/")[:-1]],
            })
        elif rel in DEMOS:
            designs.append({
                "id": "JS-" + path.stem.upper(), "title": path.name, "kind": "module", "path": rel,
                "demo": DEMOS[rel], "script": "../../" + rel, "sha256": sha256(path),
                "bytes": path.stat().st_size, "status": "prototype_not_certified",
                "summary": path.read_text(encoding="utf-8").splitlines()[1].lstrip("/ ").strip(),
                "tags": ["nexus-dashboard-v3", DEMOS[rel]],
            })
    catalog = root / CATALOG
    if catalog.exists():
        data = json.loads(catalog.read_text(encoding="utf-8"))
        for c in data.get("concepts", []):
            designs.append({
                "id": c["id"], "title": c["title"], "kind": "concept", "path": CATALOG,
                "status": c.get("status", "unknown"), "sha256": sha256(catalog),
                "summary": "Module: " + ", ".join(c.get("module_boundaries", [])) if c.get("module_boundaries") else "",
                "sources": c.get("source_ids", []), "related": c.get("related_concept_ids", []),
                "tags": ["concept", data.get("reviewed_on", "")],
            })
    return designs


def build(root: Path = ROOT, curated_path: Path = GALLERY / "curated.json") -> dict:
    curated = json.loads(curated_path.read_text(encoding="utf-8")) if curated_path.exists() else []
    for c in curated:
        c.setdefault("kind", "architecture")
    return {"schema": "nexus-design-gallery/1", "commit": commit(root), "designs": scan(root) + curated}


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else GALLERY / "designs.manifest.js"
    manifest = build()
    out.write_text("window.NEXUS_DESIGNS = " + json.dumps(manifest, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8", newline="\n")
    print(f"{len(manifest['designs'])} designs -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
