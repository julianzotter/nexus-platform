"""IOD.01: Run-Ordner finalisieren – YAML-Frontmatter in MD ergaenzen, Manifest-Dateiliste, SHA256-Hashes.

  python tools/iod01_finalize.py runs/<RUN_ID> [--check]

--check: nur pruefen (Frontmatter vorhanden, Hashes stimmen), Exitcode 1 bei Abweichung.
"""
import datetime as dt, hashlib, json, pathlib, sys

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def files(run):
    return sorted(p for p in run.rglob("*") if p.is_file() and p.name not in ("08_ARTIFACT_HASHES.json", "SYNC_STAMP.txt"))

def frontmatter(p, run, ts):
    t = p.read_text(encoding="utf-8")
    if t.startswith("---\n"):
        return False
    rel = p.relative_to(run).as_posix()
    head = (f"---\nschema: IOD.01/1.0\nrun_id: {run.name}\ntype: artifact\nartifact: {rel}\n"
            f"archived_ts: {ts}\nsha256_original: {hashlib.sha256(t.encode('utf-8')).hexdigest()}\n---\n\n")
    p.write_text(head + t, encoding="utf-8")
    return True

def main(argv):
    run = pathlib.Path(argv[1]).resolve(); check = "--check" in argv
    ts = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    if check:
        bad = [p.name for p in files(run) if p.suffix == ".md" and not p.read_text(encoding="utf-8").startswith("---\n")]
        ref = json.loads((run / "08_ARTIFACT_HASHES.json").read_text(encoding="utf-8"))["files"]
        cur = {p.relative_to(run).as_posix(): sha(p) for p in files(run)}
        diff = sorted(k for k in set(ref) | set(cur) if ref.get(k) != cur.get(k))
        print(json.dumps({"ok": not bad and not diff, "missing_frontmatter": bad, "hash_mismatch": diff}, indent=2))
        return 0 if not bad and not diff else 1
    added = [p.name for p in files(run) if p.suffix == ".md" and frontmatter(p, run, ts)]
    mpath = run / "06_RUN_MANIFEST.json"
    m = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {}
    m["finalized_ts"] = ts
    m["files"] = [p.relative_to(run).as_posix() for p in files(run) if p.name != "06_RUN_MANIFEST.json"]
    mpath.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    h = {"schema": "IOD.01/1.0", "run_id": run.name, "algorithm": "SHA256", "created_ts": ts,
         "files": {p.relative_to(run).as_posix(): sha(p) for p in files(run)}}
    (run / "08_ARTIFACT_HASHES.json").write_text(json.dumps(h, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"frontmatter_added": added, "files": len(h["files"])}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
