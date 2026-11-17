"""
rfem5_api_inspect.py – erzeugt eine vollständige API-Referenz der RFEM-5-COM-Schnittstelle direkt aus der
installierten Typbibliothek (RFEM5_64.dll). RFEM muss dafür NICHT laufen, keine Lizenz nötig.

Ergebnis: Markdown mit allen Interfaces (Methoden, Ein-/Ausgabeparameter, Hilfetext), Strukturen (Felder) und
Aufzählungen (Werte). Deterministisch – gleiche Typbibliothek ergibt die gleiche Datei.

Aufruf
  python rfem5_api_inspect.py                          # schreibt ..\\references\\API_REFERENZ_RFEM5.md
  python rfem5_api_inspect.py --out X:\\ref.md
  python rfem5_api_inspect.py --find Nodal             # nur Namen suchen (Interfaces/Methoden/Strukturen/Enums)
"""
import argparse, ast, hashlib, os, sys

TYPELIB_DEFAULT = r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll"


def generated_source(typelib):
    import comtypes.client as cc
    R = cc.GetModule(typelib)                      # erzeugt comtypes.gen.RFEM5 (+ Modul mit GUID-Namen)
    impl = [m for n, m in sys.modules.items() if n.startswith("comtypes.gen._5A027F61")]
    path = impl[0].__file__ if impl else R.__file__
    return R, path, open(path, encoding="utf-8").read()


def tname(node):
    """Typ-Ausdruck aus AST lesbar machen: POINTER(c_int) -> c_int*, _midlSAFEARRAY(Node) -> Node[]"""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        f = tname(node.func); a = tname(node.args[0]) if node.args else "?"
        if f == "POINTER":
            return a + "*"
        if f == "_midlSAFEARRAY":
            return a + "[]"
        return f"{f}({a})"
    return ast.unparse(node)


def parse(src):
    tree = ast.parse(src)
    enums, structs, ifaces, cur_enum = {}, {}, {}, None
    # Enums: Kommentarzeilen "# values for enumeration 'X'" + folgende NAME = int
    for line in src.splitlines():
        if line.startswith("# values for enumeration '"):
            cur_enum = line.split("'")[1]; enums[cur_enum] = []
        elif cur_enum and " = " in line and not line.startswith(" "):
            k, v = [s.strip() for s in line.split("=", 1)]
            if v.lstrip("-").isdigit():
                enums[cur_enum].append((k, int(v)))
            else:
                cur_enum = None
        elif not line.strip():
            cur_enum = None
    for st in tree.body:
        if not (isinstance(st, ast.Assign) and isinstance(st.targets[0], ast.Attribute)):
            continue
        owner, attr = st.targets[0].value, st.targets[0].attr
        if not isinstance(owner, ast.Name) or not isinstance(st.value, ast.List):
            continue
        if attr == "_fields_":
            structs[owner.id] = [(e.elts[0].value, tname(e.elts[1])) for e in st.value.elts if isinstance(e, ast.Tuple)]
        elif attr == "_methods_":
            ms = []
            for c in st.value.elts:
                if not (isinstance(c, ast.Call) and tname(c.func) == "COMMETHOD"):
                    continue
                help_ = ""
                for h in c.args[0].elts if isinstance(c.args[0], ast.List) else []:
                    if isinstance(h, ast.Call) and tname(h.func) == "helpstring":
                        help_ = h.args[0].value
                name = c.args[2].value
                ins, outs = [], []
                for p in c.args[3:]:
                    flags = [f.value for f in p.elts[0].elts]
                    (outs if "out" in flags else ins).append(f"{p.elts[2].value}: {tname(p.elts[1]).rstrip('*') if 'out' in flags else tname(p.elts[1])}")
                ms.append((name, ins, outs, help_))
            ifaces[owner.id] = ms
    return enums, structs, ifaces


def render(R, path, src, enums, structs, ifaces):
    sha = hashlib.sha256(src.encode("utf-8")).hexdigest()[:16]
    L = ["# RFEM 5 COM – API-Referenz (automatisch aus der Typbibliothek erzeugt)", "",
         f"Quelle: `{TYPELIB_DEFAULT}` → comtypes-Modul `{os.path.basename(path)}` (SHA-256 {sha}…) · "
         f"{len(ifaces)} Interfaces · {len(structs)} Strukturen · {len(enums)} Aufzählungen", "",
         "Lesart: `Methode(ein: Typ, …) → aus: Typ` – in Python liefert comtypes die `out`-Parameter als Rückgabewert "
         "(mehrere als Tupel). `X[]` = Array (SAFEARRAY) → Python-Liste/Tupel. Einheiten SI (N, Nm, m).", "",
         "## Inhalt", "", "1. Interfaces", "2. Strukturen", "3. Aufzählungen", "", "## 1. Interfaces", ""]
    for i in sorted(ifaces):
        L += [f"### {i}", "", "| Methode | Eingabe | Ausgabe | Hilfetext |", "|---|---|---|---|"]
        for n, ins, outs, h in ifaces[i]:
            L.append(f"| `{n}` | {', '.join(ins) or '–'} | {', '.join(outs) or '–'} | {h.replace('|', '/')} |")
        L.append("")
    L += ["## 2. Strukturen", ""]
    for s in sorted(structs):
        L.append(f"- **{s}**: " + ", ".join(f"`{n}` ({t})" for n, t in structs[s]))
    L += ["", "## 3. Aufzählungen", ""]
    for e in sorted(enums):
        L.append(f"- **{e}**: " + ", ".join(f"{k}={v}" for k, v in enums[e]))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="RFEM-5-COM-API-Referenz aus der Typbibliothek erzeugen")
    ap.add_argument("--typelib", default=os.environ.get("RFEM5_TYPELIB", TYPELIB_DEFAULT))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "API_REFERENZ_RFEM5.md"))
    ap.add_argument("--find", help="nur suchen (Teilstring, Groß/Klein egal)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.exists(a.typelib):
        sys.exit(f"FEHLER: Typbibliothek fehlt: {a.typelib}")
    R, path, src = generated_source(a.typelib)
    enums, structs, ifaces = parse(src)
    if a.find:
        q = a.find.lower()
        for i, ms in sorted(ifaces.items()):
            for n, ins, outs, h in ms:
                if q in n.lower() or q in i.lower():
                    print(f"{i}.{n}({', '.join(ins)}) -> {', '.join(outs) or '-'}   # {h}")
        for s, fs in sorted(structs.items()):
            if q in s.lower():
                print(f"struct {s}: {', '.join(n for n, _ in fs)}")
        for e, vs in sorted(enums.items()):
            if q in e.lower() or any(q in k.lower() for k, _ in vs):
                print(f"enum {e}: {', '.join(f'{k}={v}' for k, v in vs)}")
        return
    open(a.out, "w", encoding="utf-8").write(render(R, path, src, enums, structs, ifaces))
    print(f"geschrieben: {a.out} | Interfaces {len(ifaces)} | Strukturen {len(structs)} | Aufzählungen {len(enums)}")


if __name__ == "__main__":
    main()
