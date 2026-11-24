# P205 FT-Traeger-Matrix: read-only Excel error audit (Status: REVIEW, ungetestet an Originaldatei)
# pip install openpyxl
import re, csv, json, sys
from collections import defaultdict
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries, get_column_letter

ERR = {"#REF!","#DIV/0!","#N/A","#VALUE!","#NAME?","#NUM!","#NULL!","#SPILL!","#CALC!"}
REF = re.compile(r"(?:(?:'([^']+)'|([A-Za-z0-9_\.]+))!)?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?")
MAX_RANGE = 5000

def refs(sheet, f):
    out = []
    for m in REF.finditer(f.replace('"', ' " ')):
        sh = m.group(1) or m.group(2) or sheet
        c1, r1, c2, r2 = m.group(3), m.group(4), m.group(5), m.group(6)
        if c2:
            a, b, c, d = range_boundaries(f"{c1}{r1}:{c2}{r2}")
            if (c-a+1)*(d-b+1) > MAX_RANGE: continue
            out += [(sh, f"{get_column_letter(x)}{y}") for x in range(a, c+1) for y in range(b, d+1)]
        else:
            out.append((sh, f"{c1}{r1}"))
    return out

def main(path, outdir="."):
    wf = load_workbook(path, data_only=False, read_only=False)
    wv = load_workbook(path, data_only=True,  read_only=False)
    val = lambda s, a: wv[s][a].value if s in wv.sheetnames else "#SHEET?"
    errs, forms = {}, {}
    for ws in wf.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    forms[(ws.title, c.coordinate)] = c.value
                v = val(ws.title, c.coordinate)
                if isinstance(v, str) and v.strip() in ERR:
                    errs[(ws.title, c.coordinate)] = v.strip()
    deps = defaultdict(set); rows = []
    for k, e in errs.items():
        f = forms.get(k, "")
        pre = refs(k[0], f) if f else []
        bad = [p for p in pre if p in errs or p[0] not in wv.sheetnames]
        empty = [p for p in pre if p[0] in wv.sheetnames and val(*p) is None]
        for p in bad: deps[p].add(k)
        cls = ("DIRECT_DEFECT" if "#REF!" in f else
               "ROOT" if not bad else "PROPAGATED")
        rows.append(dict(sheet=k[0], cell=k[1], error=e, cls=cls,
                         missing_input=len(empty), bad_precedents=";".join(f"{s}!{a}" for s, a in bad[:5]),
                         empty_precedents=";".join(f"{s}!{a}" for s, a in empty[:5]), formula=f[:300]))
    def reach(k, seen):
        for d in deps.get(k, ()):
            if d not in seen: seen.add(d); reach(d, seen)
        return seen
    sys.setrecursionlimit(100000)
    for r in rows: r["downstream"] = len(reach((r["sheet"], r["cell"]), set()))
    rows.sort(key=lambda r: (r["cls"] == "PROPAGATED", -r["downstream"]))
    with open(f"{outdir}/p205_errors.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["none"], delimiter=";"); w.writeheader(); w.writerows(rows)
    summ = dict(file=path, formulas=len(forms), errors=len(errs),
                by_class={c: sum(r["cls"] == c for r in rows) for c in ("DIRECT_DEFECT","ROOT","PROPAGATED")},
                by_type={t: sum(r["error"] == t for r in rows) for t in ERR if any(r["error"] == t for r in rows)},
                by_sheet=dict(sorted(((s, sum(r["sheet"] == s for r in rows)) for s in {r["sheet"] for r in rows}), key=lambda x: -x[1])),
                top_roots=[f'{r["sheet"]}!{r["cell"]} {r["error"]} -> {r["downstream"]}' for r in rows if r["cls"] != "PROPAGATED"][:20])
    json.dump(summ, open(f"{outdir}/p205_errors_summary.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(json.dumps(summ, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
