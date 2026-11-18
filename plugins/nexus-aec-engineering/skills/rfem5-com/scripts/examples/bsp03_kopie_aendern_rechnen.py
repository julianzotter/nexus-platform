"""
Beispiel 3 – sicherer Änderungs-Workflow: Original -> datierte Kopie -> Knoten verschieben -> rechnen -> speichern.

  python bsp03_kopie_aendern_rechnen.py --quelle X:\\orig.rf5 --ziel-ordner X:\\SANDBOX --knoten 12 --dz 0.10
  python bsp03_kopie_aendern_rechnen.py ... --trocken        # nur Kopie + Protokoll, keine Änderung

Regeln (im Skript erzwungen):
  - Das Original wird nur gelesen (SHA-256 vorher/nachher muss gleich sein), geöffnet wird nur die Kopie.
  - Ziel-Ordner muss "SANDBOX" im Pfad enthalten (änderbar mit --guard).
  - Änderung in PrepareModification/FinishModification, bei Fehler CancelModification.
  - Nach der Änderung wird zurückgelesen und gegen den Sollwert geprüft, erst dann gerechnet und gespeichert.
  - JSON-Protokoll (alt -> neu, Hashes, Fehlerliste der Berechnung) neben der Kopie.
"""
import argparse, datetime as dt, json, os, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from rfem_connect import rfem_session, find_model, sha256          # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quelle", required=True)
    ap.add_argument("--ziel-ordner", required=True)
    ap.add_argument("--guard", default="SANDBOX")
    ap.add_argument("--knoten", type=int, required=True)
    ap.add_argument("--dx", type=float, default=0.0)
    ap.add_argument("--dy", type=float, default=0.0)
    ap.add_argument("--dz", type=float, default=0.0)
    ap.add_argument("--trocken", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    src = os.path.abspath(a.quelle)
    if a.guard.lower() not in os.path.abspath(a.ziel_ordner).lower():
        sys.exit(f"Abbruch: Ziel-Ordner enthält '{a.guard}' nicht.")
    os.makedirs(a.ziel_ordner, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
    dst = os.path.join(os.path.abspath(a.ziel_ordner), f"{os.path.splitext(os.path.basename(src))[0]}_WORK_{stamp}.rf5")
    h0 = sha256(src)
    shutil.copy2(src, dst)
    log = dict(zeit=stamp, quelle=src, quelle_sha256=h0, kopie=dst, kopie_sha256_vorher=sha256(dst), aenderungen=[])
    if not a.trocken:
        with rfem_session() as (app, R):
            m = find_model(app, dst) or app.OpenModel(dst)
            d = m.GetModelData()
            ni = d.GetNode(a.knoten, R.AtNo)
            nd = ni.GetData()
            alt = (nd.X, nd.Y, nd.Z)
            soll = (alt[0] + a.dx, alt[1] + a.dy, alt[2] + a.dz)
            d.PrepareModification()
            try:
                nd.X, nd.Y, nd.Z = soll
                ni.SetData(nd)
                d.FinishModification()
            except Exception:
                d.CancelModification(); raise
            ist = d.GetNode(a.knoten, R.AtNo).GetData()
            ist = (ist.X, ist.Y, ist.Z)
            assert max(abs(i - s) for i, s in zip(ist, soll)) < 1e-9, f"Rücklesen weicht ab: {ist} != {soll}"
            log["aenderungen"].append(dict(knoten=a.knoten, alt=alt, neu=ist))
            C = m.GetCalculation()
            C.Clean()                                    # alte Ergebnisse löschen -> echte Neuberechnung
            errs = C.CalculateAll() or []
            log["berechnung"] = [dict(Nr=e.ErrorNo, Last=e.Load, Typ=int(e.Type), Text=e.Description) for e in errs]
            m.Save(dst)                                  # immer mit Pfad
    log["kopie_sha256_nachher"] = sha256(dst)
    log["quelle_unveraendert"] = sha256(src) == h0
    json.dump(log, open(dst[:-4] + "_PROTOKOLL.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(log, ensure_ascii=False, indent=1))
    if not log["quelle_unveraendert"]:
        sys.exit("WARNUNG: Hash der Quelle hat sich geändert!")


if __name__ == "__main__":
    main()
