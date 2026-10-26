#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ctx_router.py -- Just-in-Time Context Router (Minimum Viable Context) ueber die MCP-ACCESS-TOOLS-Wissensbasis.

Idee (XTrace "Minimum Viable Context", 2026): nicht "was ist aehnlich zur Frage?", sondern
"was muss der Agent wissen, um teure Fehler zu vermeiden?" -> Ranking nach Relevanz x Cost-of-Ignorance (COI).

Score je Chunk:   S = rel(q, c) * (0.5 + COI(src))        rel = BM25-light (tf * idf, laengennormiert)
Auswahl:          greedy nach S / tokens, bis Budget B erreicht; ALWAYS-ON-Block (harte Regeln) immer zuerst.
JIT-Lookup:       zusaetzlich Treffer aus out\INVENTORY_LATEST.jsonl (306.980 Objekte) fuer die Frage-Keywords.

Modi:
  --mode MVP    always-on + Top-Chunks unter --budget (Default 1200 Tokens) + JIT-Inventar-Treffer
  --mode FULL   alle Dokumente in fester Reihenfolge, hart abgeschnitten bei --full-cap Tokens ("dump it all")
  --mode NAIVE  kein Kontext

Tokens: tiktoken cl100k_base (Schaetzung fuer alle Modelle); lokale Ollama-Laeufe liefern zusaetzlich exakte Werte.

  python scripts\ctx_router.py --task "Welche RFEM-Datei ist die aktuellste fuer Boeblingen?" --mode MVP --print
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

BASE = Path(os.environ.get('NEXUS_MCP_ROOT', r'G:\Meine Ablage\_developement\MCP-ACCESS-TOOLS'))
SSOT_DIR = Path(os.environ.get('NEXUS_SSOT_ROOT', r'G:\Meine Ablage\_developement\LLM-LOCAL-SSOT'))
OUT = BASE / "out"
INDEX_DIR = Path(r"G:\Meine Ablage\_INDEX")

# Quelle -> Cost-of-Ignorance-Prior (0..1). Hohe COI = teuer, wenn der Agent es nicht weiss.
SOURCES: List[Tuple[Path, float, str]] = [
    (INDEX_DIR / "2026-09-14_Statusbericht_Ereignisse_Prioritaeten.md", 0.9, "STATE"),
    (OUT / "STATS.md", 0.8, "STATE"),
    (BASE / "LESSONS_LEARNED.md", 0.7, "LESSONS"),
    (BASE / "ASSET_REGISTRY.csv", 0.6, "REGISTRY"),
    (BASE / "USECASE_REGISTRY.md", 0.6, "REGISTRY"),
    (BASE / "26_09_15_CLA_TOOL-ACCESS-MATRIX_v1.0.md", 0.6, "REGISTRY"),
    (BASE / "README.md", 0.5, "DOC"),
    (BASE / "26_09_15_CLA_RECOMMENDATIONS_ADDONS-PLUGINS_v1.0.md", 0.4, "DOC"),
    (BASE / "26_09_15_CLA_MVP-DEV-PROMPT_KEYWORD-GLOSSAR_v1.0.md", 0.4, "DOC"),
    (OUT / "TREE_GDRIVE.md", 0.3, "TREE"),
]

def policy_context() -> str:
    from nexus_contract import load_governance
    overrides = json.loads(os.environ.get('NEXUS_GOVERNANCE_FILES_JSON', '{}'))
    receipt = load_governance(SSOT_DIR / 'WORK', overrides)
    if not receipt['ready']:
        raise ValueError('BOOTSTRAP_BLOCKED:' + ','.join(receipt['missing_or_invalid']))
    blocks = ['NEXUS mandatory local policy bytes; source authority and human release are separate.']
    for key in ('agbs', 'manifest', 'baseline', 'folder'):
        item = receipt['policies'][key]
        blocks.append('[POLICY ' + key + ' SHA256 ' + item['sha256'] + ']\n' + item['text'])
    return '\n\n'.join(blocks)


STOP = set("""der die das und oder für fuer mit von zu im in am an auf ist sind wird werden wie was welche welcher
welches wo wann warum ein eine einer eines den dem des nicht kein keine bei aus nach vor über ueber unter zum zur
the a an of to for in on and or is are be with from by as at this that which what when where how ich du er sie es
wir ihr sich mir dir uns euch dass bitte gib nenne liste welchen einem einen welchem""".split())

# Zusatz-Stopwoerter nur fuer den JIT-Inventar-Lookup (Pfadsuche): Frage-Fuellwoerter, die in Pfaden nur Rauschen erzeugen
JIT_STOP = STOP | set("""datum aktuellste aktuelle aktuell insgesamt laut bereits vermutlich niemals wieviele viele thema
seine seiner ihre ihrer folgt daraus einzelne einzelner rolle wert achse zelle befehl ohne werte anzuzeigen gesamt
letzten letzte letzter letztem meisten dateien datei ordner top-ordner skript jetzt vorher gab gibt sind ist ueberschritten
nenne welche welcher welches""".split())

_enc = None


def n_tokens(text: str) -> int:
    global _enc
    if _enc is None:
        try:
            import tiktoken  # type: ignore
            _enc = tiktoken.get_encoding("cl100k_base")
        except Exception:  # noqa: BLE001
            _enc = False
    if _enc:
        return len(_enc.encode(text, disallowed_special=()))
    return max(1, len(text) // 4)


def truncate_tokens(text: str, cap: int) -> str:
    if _enc is None:
        n_tokens("x")
    if _enc:
        ids = _enc.encode(text, disallowed_special=())
        return text if len(ids) <= cap else _enc.decode(ids[:cap])
    return text[: cap * 4]


def norm_terms(text: str) -> List[str]:
    t = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return [w for w in re.findall(r"[a-z0-9_\-\.]{3,}", t) if w not in STOP]


# ---------------------------------------------------------------- chunking
def chunk_doc(path: Path, coi: float, kind: str, max_tokens: int = 350) -> List[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks: List[dict] = []
    if path.suffix.lower() == ".csv":
        lines = text.splitlines()
        header, rows = lines[0], lines[1:]
        # kleine CSV-Chunks (3 Zeilen ~ 300 Tokens): ein Chunk darf nie mehr als ~1/4 des MVP-Budgets kosten
        for i in range(0, len(rows), 3):
            body = header + "\n" + "\n".join(rows[i:i + 3])
            chunks.append({"src": path.name, "head": f"rows {i+1}-{i+3}", "text": body, "coi": coi, "kind": kind})
    else:
        cur_head, buf = path.name, []
        def flush():
            if buf:
                body = "\n".join(buf).strip()
                if body:
                    chunks.append({"src": path.name, "head": cur_head, "text": body, "coi": coi, "kind": kind})
        for line in text.splitlines():
            if re.match(r"^#{1,3} ", line):
                flush(); buf = []; cur_head = line.lstrip("# ").strip()[:80]
            buf.append(line)
            if n_tokens("\n".join(buf)) > max_tokens:
                flush(); buf = []
        flush()
    for c in chunks:
        c["tokens"] = n_tokens(c["text"])
        c["terms"] = Counter(norm_terms(c["head"] + " " + c["text"]))
    return chunks


def build_corpus() -> List[dict]:
    corpus: List[dict] = []
    for path, coi, kind in SOURCES:
        corpus.extend(chunk_doc(path, coi, kind))
    return corpus


# ---------------------------------------------------------------- scoring
def score_chunks(query: str, corpus: List[dict]) -> List[Tuple[float, dict]]:
    q = norm_terms(query)
    if not q:
        return []
    N = len(corpus)
    df = Counter()
    for c in corpus:
        for t in set(c["terms"]):
            df[t] += 1
    avg_len = sum(sum(c["terms"].values()) for c in corpus) / max(N, 1)
    scored = []
    for c in corpus:
        L = sum(c["terms"].values()) or 1
        rel = 0.0
        for t in q:
            tf = c["terms"].get(t, 0)
            if tf == 0:
                # Praefix-Match fuer zusammengesetzte Begriffe (boeblingen -> boeblingen_seilstatik)
                tf = sum(v for k, v in c["terms"].items() if k.startswith(t) or t in k) * 0.5
            if tf:
                idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
                rel += idf * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * L / max(avg_len, 1)))
        if rel > 0:
            scored.append((rel * (0.5 + c["coi"]), c))
    scored.sort(key=lambda x: -x[0])
    return scored


def jit_inventory(query: str, limit: int = 8, max_tokens: int = 380) -> str:
    """Keyword-Treffer aus dem 306k-Objekte-Inventar: erst nach Anzahl Treffer-Terme, dann Aenderungsdatum (nur Pfade)."""
    inv = OUT / "INVENTORY_LATEST.jsonl"
    terms = [t for t in norm_terms(query)
             if len(t) >= 5 and t not in JIT_STOP and not t.replace(".", "").replace("_", "").isdigit()]
    if not inv.exists() or not terms:
        return ""
    hits = []
    with inv.open(encoding="utf-8") as f:
        for line in f:
            low = line.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
            n = sum(1 for t in terms if t in low)
            if n < max(1, min(2, len(terms) - 1)):
                continue
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if r.get("object_type") != "FILE":
                continue
            hits.append((n, r["modified_at"], r["full_path"], r["size_bytes"]))
    if not hits:
        return ""
    # stabile Sortierung: erst Datum absteigend, dann Trefferzahl absteigend (letzter Sort dominiert)
    hits.sort(key=lambda h: h[1], reverse=True)
    hits.sort(key=lambda h: -h[0])
    top = hits[:limit]
    gd, cu = "G:\\Meine Ablage\\", "C:\\Users\\julia\\"
    lines = [f"[JIT-INVENTAR: {len(hits)} Treffer fuer {terms}; Top {len(top)} nach Trefferzahl, dann Datum; "
             f"GDRIVE = {gd}]"]
    for n, mod, p, sz in top:
        short = p.replace(gd, "GDRIVE\\").replace(cu, "")
        lines.append(f"- {short} | {mod[:10]} | {sz} B")
        if n_tokens("\n".join(lines)) > max_tokens:
            lines.pop()
            break
    return "\n".join(lines)


# ---------------------------------------------------------------- stage 2: hybrid (BM25 + lokale Embeddings)
_EMB_CACHE = OUT / "bench" / "chunk_embeddings.json"


def _embed_fn():
    sys.path.insert(0, str(BASE.parent / "LLM-LOCAL-SSOT" / "scripts"))
    from ollama_client import embed  # type: ignore
    return embed


def ensure_embeddings(corpus: List[dict]) -> None:
    """Embeddet alle Chunks einmal (nomic-embed-text, lokal) und cached nach Text-Hash."""
    import hashlib
    cache: Dict[str, List[float]] = {}
    if _EMB_CACHE.exists():
        cache = json.loads(_EMB_CACHE.read_text(encoding="utf-8"))
    todo = []
    for c in corpus:
        c["h"] = hashlib.sha1((c["src"] + c["head"] + c["text"]).encode("utf-8")).hexdigest()
        if c["h"] not in cache:
            todo.append(c)
    if todo:
        vecs = _embed_fn()([f"search_document: {c['head']}\n{c['text']}" for c in todo])
        for c, v in zip(todo, vecs):
            cache[c["h"]] = v
        _EMB_CACHE.parent.mkdir(parents=True, exist_ok=True)
        _EMB_CACHE.write_text(json.dumps(cache), encoding="utf-8")
        print(f"[i] {len(todo)} Chunks neu embedded (nomic-embed-text)", file=sys.stderr)
    for c in corpus:
        c["vec"] = cache[c["h"]]


def _cos(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def score_hybrid(query: str, corpus: List[dict], w_bm25: float = 0.5) -> List[Tuple[float, dict]]:
    """S = (w * bm25_norm + (1-w) * cos_norm) * (0.5 + COI). Beide Teil-Scores auf [0,1] normiert."""
    ensure_embeddings(corpus)
    qv = _embed_fn()([f"search_query: {query}"])[0]
    bm = {id(c): s / (0.5 + c["coi"]) for s, c in score_chunks(query, corpus)}  # reine Relevanz ohne COI
    bmax = max(bm.values(), default=1.0) or 1.0
    cos = {id(c): _cos(qv, c["vec"]) for c in corpus}
    cmin, cmax = min(cos.values()), max(cos.values())
    scored = []
    for c in corpus:
        b = bm.get(id(c), 0.0) / bmax
        s = (cos[id(c)] - cmin) / ((cmax - cmin) or 1.0)
        rel = w_bm25 * b + (1 - w_bm25) * s
        scored.append((rel * (0.5 + c["coi"]), c))
    scored.sort(key=lambda x: -x[0])
    return scored


# ---------------------------------------------------------------- assembly
def build_context(query: str, mode: str, budget: int = 1200, full_cap: int = 30000,
                  corpus: Optional[List[dict]] = None) -> Dict[str, object]:
    mode = mode.upper()
    if mode == "NAIVE":
        return {"mode": mode, "context": "", "tokens": 0, "chunks": [], "coverage": None}
    always = policy_context()
    corpus = corpus or build_corpus()
    if mode == "FULL":
        if n_tokens(always) > full_cap:
            raise ValueError('MANDATORY_POLICIES_EXCEED_CONTEXT_BUDGET')
        parts, used = [always], [('mandatory_policies', n_tokens(always))]
        for path, coi, kind in SOURCES:
            if path.exists():
                txt = path.read_text(encoding="utf-8", errors="replace")
                parts.append(f"\n\n===== {path.name} =====\n{txt}")
                used.append((path.name, n_tokens(txt)))
        full = "".join(parts)
        total = n_tokens(full)
        ctx = truncate_tokens(full, full_cap)
        return {"mode": mode, "context": ctx, "tokens": n_tokens(ctx), "chunks": used,
                "coverage": f"{min(total, full_cap)}/{total} Tokens ({100*min(total, full_cap)/max(total,1):.0f} %)"}
    # MVP
    if n_tokens(always) > budget:
        raise ValueError('MANDATORY_POLICIES_EXCEED_CONTEXT_BUDGET')
    jit = jit_inventory(query)
    spent = n_tokens(always) + (n_tokens(jit) if jit else 0)
    chosen, seen = [], set()
    ranked = score_hybrid(query, corpus) if mode == "MVP2" else score_chunks(query, corpus)
    # Diversifizierung (MMR-light): max. 1 Chunk je (Quelle, Ueberschrift), max. 3 je Quelle im ersten Durchgang;
    # zweiter Durchgang fuellt Restbudget ohne Caps. Verhindert, dass eine Quelle das Budget monopolisiert.
    per_src: Counter = Counter()
    for pass_no in (1, 2):
        for s, c in ranked:
            key = (c["src"], c["head"])
            if key in seen or spent + c["tokens"] > budget:
                continue
            if pass_no == 1 and per_src[c["src"]] >= 3:
                continue
            seen.add(key)
            per_src[c["src"]] += 1
            chosen.append((s, c))
            spent += c["tokens"]
            if len(chosen) >= 12:
                break
        if len(chosen) >= 12 or budget - spent < 60:
            break
    body = [always]
    for s, c in chosen:
        body.append(f"\n[SRC: {c['src']} > {c['head']} | COI {c['coi']:.1f} | score {s:.2f}]\n{c['text']}")
    if jit:
        body.append("\n" + jit)
    ctx = "\n".join(body)
    return {"mode": mode, "context": ctx, "tokens": n_tokens(ctx),
            "chunks": [(c["src"], c["head"], round(float(s), 3), c["tokens"]) for s, c in chosen],
            "coverage": f"{len(chosen)} Chunks + always-on + JIT"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--mode", default="MVP", choices=["MVP", "MVP2", "FULL", "NAIVE"])
    ap.add_argument("--budget", type=int, default=1200)
    ap.add_argument("--full-cap", type=int, default=30000)
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    r = build_context(a.task, a.mode, a.budget, a.full_cap)
    print(f"[{r['mode']}] tokens={r['tokens']} coverage={r['coverage']}")
    for c in r["chunks"]:
        print("   ", c)
    if a.print:
        print("\n" + str(r["context"]))


if __name__ == "__main__":
    main()
