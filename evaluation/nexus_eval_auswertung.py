"""NEXUS-AI Evaluierung – Auswertung mehrerer Prüfberichte.
Aufruf:  python nexus_eval_auswertung.py <Ordner mit *.md/*.json Prüfberichten>
Ausgabe: NEXUS_EVAL_AUSWERTUNG.md + .json im selben Ordner."""
import json, re, sys, pathlib, statistics as st, collections
W = {"K1": .30, "K2": .25, "K3": .25, "K4": .20}
NAME = {"K1": "Funktion", "K2": "Sicherheit/Governance", "K3": "Architektur/Wartbarkeit", "K4": "Betrieb/Nutzen"}
def load(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    if p.suffix == ".json": return json.loads(t)
    m = re.findall(r"```json\s*(\{.*?\})\s*```", t, re.S)
    if not m: raise ValueError("kein JSON-Block")
    return json.loads(m[-1])
def gesamt(n):
    g = round(sum(W[k] * n[k] for k in W), 1)
    return max(g, 4.0) if max(n.values()) >= 5 else g
d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
R, err = [], []
for p in sorted(d.glob("*")):
    if p.suffix not in (".md", ".json") or p.name.startswith("NEXUS_EVAL_"): continue
    try:
        j = load(p); n = {k: float(j["noten"][k]) for k in W}
        assert all(1 <= v <= 5 for v in n.values())
        R.append({"datei": p.name, "modell": j.get("modell") or p.stem, "noten": n, "gesamt_neu": gesamt(n),
                  "gesamt_modell": j.get("gesamt"), "pp": j.get("pruefpunkte", {}), "mass": j.get("massnahmen", []), "krit": j.get("kritisch", [])})
    except Exception as e: err.append(f"{p.name}: {e}")
if not R: sys.exit("Keine gültigen Prüfberichte gefunden. " + "; ".join(err))
L = ["# NEXUS-AI – Auswertung der Prüfberichte", f"Berichte: {len(R)}" + (f" · verworfen: {len(err)}" if err else ""), "",
     "## Noten je Modell", "| Modell | " + " | ".join(f"{k} {NAME[k]}" for k in W) + " | Gesamt (nachgerechnet) | Gesamt (Modell) |", "|---" * 7 + "|"]
for r in R: L.append(f"| {r['modell']} | " + " | ".join(f"{r['noten'][k]:.0f}" for k in W) + f" | {r['gesamt_neu']:.1f} | {r['gesamt_modell']} |")
L += ["", "## Konsens je Kriterium", "| Kriterium | Mittel | Median | Spannweite | Streuung | Konsens |", "|---|---|---|---|---|---|"]
agg = {}
for k in W:
    v = [r["noten"][k] for r in R]; s = st.pstdev(v) if len(v) > 1 else 0
    agg[k] = {"mittel": round(st.mean(v), 2), "median": st.median(v), "min": min(v), "max": max(v), "sd": round(s, 2)}
    L.append(f"| {k} {NAME[k]} | {agg[k]['mittel']:.2f} | {agg[k]['median']} | {min(v):.0f}–{max(v):.0f} | {s:.2f} | {'stabil' if max(v)-min(v) <= 1 else 'ABWEICHUNG prüfen'} |")
G = gesamt({k: agg[k]["mittel"] for k in W})
L += ["", f"**Gesamtnote (gewichtetes Mittel aller Modelle): {G:.1f}**", "", "## Prüfpunkte mit Mehrheitsbefund", "| ID | erfüllt | teilweise | nicht erfüllt | nicht prüfbar |", "|---|---|---|---|---|"]
ids = sorted({i for r in R for i in r["pp"]}, key=lambda x: (x[:2], float(x[3:]) if x[3:].replace('.','').isdigit() else 0))
for i in ids:
    c = collections.Counter(r["pp"].get(i, "") for r in R)
    L.append(f"| {i} | {c['erfuellt']} | {c['teilweise']} | {c['nicht_erfuellt']} | {c['nicht_pruefbar']} |")
L += ["", "## Kritische Befunde (alle Modelle)"]
for r in R:
    for k in r["krit"]:
        if k.get("befund"): L.append(f"- [{r['modell']}] {k['befund']} – {k.get('datei','')} → {k.get('massnahme','')}")
L += ["", "## Maßnahmen-Backlog (nach Nennungen, dann Rang)", "| Maßnahme | Datei | Kriterium | Wirkung | Aufwand | Modell | Rang |", "|---|---|---|---|---|---|---|"]
M = sorted(((m, r["modell"]) for r in R for m in r["mass"] if m.get("massnahme")), key=lambda x: (x[0].get("rang", 9)))
for m, mod in M: L.append(f"| {m['massnahme']} | {m.get('datei','')} | {m.get('kriterium','')} | {m.get('wirkung','')} | {m.get('aufwand','')} | {mod} | {m.get('rang','')} |")
if err: L += ["", "## Verworfene Dateien"] + [f"- {e}" for e in err]
(d / "NEXUS_EVAL_AUSWERTUNG.md").write_text("\n".join(L), encoding="utf-8")
(d / "NEXUS_EVAL_AUSWERTUNG.json").write_text(json.dumps({"gesamt": G, "kriterien": agg, "berichte": R, "fehler": err}, ensure_ascii=False, indent=2), encoding="utf-8")
print("\n".join(L[:12 + len(R)]))
