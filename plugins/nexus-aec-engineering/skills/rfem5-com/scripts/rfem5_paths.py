"""
rfem5_paths.py – Inventar aller wichtigen RFEM-5.29- und Python-Pfade (+ optional Sicherung der Benutzer-Einstellungen).

NUR LESEND auf RFEM-Dateien und Registry. RFEM muss nicht laufen.

  python rfem5_paths.py                         # Tabelle: Kategorie | Zweck | vorhanden | Größe | Datum | Pfad
  python rfem5_paths.py --json inventar.json    # zusätzlich maschinenlesbar (mit SHA-256 der Einzeldateien)
  python rfem5_paths.py --backup "G:\\...\\rfem5-com_BACKUPS"
        -> RFEM529_EINSTELLUNGEN_<JJJJMMTT_HHMM>.zip: Benutzerbibliotheken, Anzeige-Konfiguration, Einheiten,
           Protokoll-Konfiguration, Registry-Export HKCU\\Software\\Dlubal\\RFEM\\5.29 + SHA256SUMS.txt + MANIFEST.json

Umgebungsvariablen zum Überschreiben: RFEM5_PROGRAM, RFEM5_GENERALDATA, RFEM5_PUBLICDOCS, RFEM5_TYPELIB
"""
import argparse, datetime as dt, glob, hashlib, json, os, subprocess, sys, tempfile, zipfile

PROG = os.environ.get("RFEM5_PROGRAM", r"C:\Program Files\Dlubal\RFEM 5.29")
GD = os.environ.get("RFEM5_GENERALDATA", r"C:\ProgramData\Dlubal\RFEM 5.29\General Data")
PUB = os.environ.get("RFEM5_PUBLICDOCS", r"C:\Users\Public\Documents\Dlubal")
COMMON = r"C:\Program Files\Common Files\Dlubal"
TYPELIB = os.environ.get("RFEM5_TYPELIB", COMMON + r"\RFEM5_64.dll")
REG_USER = r"HKCU\Software\Dlubal\RFEM\5.29"

# (Kategorie, Zweck, Pfad oder Glob, gehört in Sicherung?)
CATALOG = [
    ("PROGRAMM", "RFEM-Programm (COM-Server)", PROG + r"\RFEM64.exe", False),
    ("PROGRAMM", "Programm-INI (externe Module/Menüeinträge)", PROG + r"\RFEM.ini", False),
    ("PROGRAMM", "Handbuch RFEM 5 (deutsch)", PROG + r"\Help\RFEM_DEU.pdf", False),
    ("COM_TYPBIBLIOTHEK", "RFEM-5-Typbibliothek (comtypes.GetModule)", TYPELIB, False),
    ("COM_TYPBIBLIOTHEK", "ältere Typbibliothek v3.4 (Querschnittswerte)", COMMON + r"\RFEM3_64.tlb", False),
    ("COM_TYPBIBLIOTHEK", "Typbibliotheken der Zusatzmodule", COMMON + r"\*_64.tlb", False),
    ("COM_DOKU", "RF-COM-5-Hilfe (Methodenreferenz)", PUB + r"\SDK\RF-COM-5.chm", False),
    ("COM_DOKU", "Hilfen der Zusatzmodul-Schnittstellen", PUB + r"\SDK\*.chm", False),
    ("COM_DOKU", ".NET-Interop + XML-Doku", PUB + r"\SDK\Reference Assemblies\x64\Dlubal.RFEM5.*", False),
    ("COM_BEISPIELE", "C#-Beispiele (Lösungen)", PUB + r"\SDK\Examples\RFEM\C#\*\*.sln", False),
    ("COM_BEISPIELE", "VB.NET-Beispiel", PUB + r"\SDK\Examples\RFEM\VB.NET\RFEMModeller\MainForm.vb", False),
    ("RF-COM-5_DATEN", "Excel/VBA-Vorlagen Modell/Lasten/Ergebnisse/Isolinien (SDK)", PUB + r"\SDK\Examples\RFEM\Excel\*.xlsm", False),
    ("MATERIALBIBLIOTHEK", "Materialbibliothek Dlubal", GD + r"\Materialien.dbd", False),
    ("MATERIALBIBLIOTHEK", "Materialbibliothek Benutzer", GD + r"\Materialien_User.dbd", True),
    ("MATERIALBIBLIOTHEK", "Querschnittsbibliothek (Profile)", GD + r"\profile_ro.*.db", False),
    ("MATERIALBIBLIOTHEK", "Benutzer-Querschnitte", GD + r"\EigProf.dat", True),
    ("PROGRAMMEINSTELLUNGEN", "Anzeige-/Farbkonfiguration", GD + r"\Config\*", True),
    ("PROGRAMMEINSTELLUNGEN", "Einheitenprofile", GD + r"\Units\*", True),
    ("PROGRAMMEINSTELLUNGEN", "Ebenen/Layer", GD + r"\layers.db3", True),
    ("PROGRAMMEINSTELLUNGEN", "Kombinatorik-Normen", GD + r"\KombiNorm.dat", True),
    ("PROGRAMMEINSTELLUNGEN", "Werkseinstellungen", GD + r"\Default\*", False),
    ("AUSDRUCKPROTOKOLL", "Protokoll-Konfiguration", GD + r"\RfemProtocolConfig.cfg", True),
    ("AUSDRUCKPROTOKOLL", "Protokoll-Benutzertexte", GD + r"\ProtocolTextsUser.db3", True),
    ("AUSDRUCKPROTOKOLL", "Übersetzungen Benutzer", GD + r"\AutoTranslate_User.txt", True),
    ("LASTDATEN", "Wind/Schnee/Erdbeben-Zonen", GD + r"\*.db3", False),
    ("RECHENBEISPIELE", "Beispielmodelle Dlubal", PUB + r"\Projects\Examples\*.rf5", False),
    ("RECHENBEISPIELE", "Bauteil-Blöcke (.rss, Unterordner)", PUB + r"\Blocks\**\*.rss", False),
    ("LOGS", "Installations-/Import-Logs", PUB + r"\Logs\*", False),
]
REGISTRY = [
    ("REGISTRY", "COM-ProgID", r"HKCR\RFEM5.Application"),
    ("REGISTRY", "COM-Server-Start (LocalServer32)", r"HKCR\CLSID\{5C397AC7-A317-4EE3-887C-0416236A44B1}\LocalServer32"),
    ("REGISTRY", "Benutzereinstellungen RFEM 5.29", REG_USER + r"\64-bit"),
    ("REGISTRY", "zuletzt geöffnete Dateien", REG_USER + r"\64-bit\Recent File List"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def reg_query(key):
    r = subprocess.run(["reg", "query", key], capture_output=True, text=True, encoding="cp850", errors="replace")
    return r.returncode == 0, [l.strip() for l in r.stdout.splitlines() if l.strip()][:12]


def python_info():
    info = dict(executable=sys.executable, version=sys.version.split()[0], bits=64 if sys.maxsize > 2**32 else 32)
    try:
        import comtypes, comtypes.gen
        info.update(comtypes=comtypes.__version__, comtypes_gen_cache=os.path.dirname(comtypes.gen.__file__))
    except Exception as e:
        info["comtypes"] = f"FEHLT ({type(e).__name__})"
    return info


def inventory(with_hash):
    rows = []
    for cat, what, pat, bkp in CATALOG:
        files = sorted(f for f in glob.glob(pat, recursive=True) if os.path.isfile(f)) if any(c in pat for c in "*?") else [pat]
        if not files:
            rows.append(dict(kategorie=cat, zweck=what, pfad=pat, vorhanden=False, sicherung=bkp))
        for f in files:
            ok = os.path.isfile(f)
            r = dict(kategorie=cat, zweck=what, pfad=f, vorhanden=ok, sicherung=bkp)
            if ok:
                st = os.stat(f)
                r.update(bytes=st.st_size, geaendert=dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"))
                if with_hash:
                    r["sha256"] = sha256(f)
            rows.append(r)
    for cat, what, key in REGISTRY:
        ok, lines = reg_query(key)
        rows.append(dict(kategorie=cat, zweck=what, pfad=key, vorhanden=ok, werte=lines, sicherung=False))
    return rows


def backup(rows, target):
    os.makedirs(target, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
    zpath = os.path.join(target, f"RFEM529_EINSTELLUNGEN_{stamp}.zip")
    sums, files = [], [r for r in rows if r["sicherung"] and r["vorhanden"]]
    with tempfile.TemporaryDirectory() as tmp:
        regfile = os.path.join(tmp, "HKCU_Dlubal_RFEM_5.29.reg")
        rr = subprocess.run(["reg", "export", REG_USER, regfile, "/y"], capture_output=True, text=True)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for r in files:
                arc = "GeneralData/" + os.path.relpath(r["pfad"], GD).replace("\\", "/")
                z.write(r["pfad"], arc); sums.append(f"{sha256(r['pfad'])}  {arc}")
            if rr.returncode == 0:
                z.write(regfile, "registry/HKCU_Dlubal_RFEM_5.29.reg"); sums.append(f"{sha256(regfile)}  registry/HKCU_Dlubal_RFEM_5.29.reg")
            z.writestr("SHA256SUMS.txt", "\n".join(sums) + "\n")
            z.writestr("MANIFEST.json", json.dumps(dict(
                erstellt=dt.datetime.now().astimezone().isoformat(timespec="seconds"), rechner=os.environ.get("COMPUTERNAME"),
                quelle_general_data=GD, registry=REG_USER, registry_export_ok=rr.returncode == 0, dateien=len(files),
                hinweis="Wiederherstellen: RFEM schließen, Dateien nach General Data kopieren, .reg doppelklicken"), ensure_ascii=False, indent=1))
    return zpath, len(files), rr.returncode == 0, sha256(zpath)


def main():
    ap = argparse.ArgumentParser(description="RFEM-5.29-Pfadinventar und Einstellungs-Sicherung")
    ap.add_argument("--json", help="Inventar als JSON schreiben (mit SHA-256)")
    ap.add_argument("--backup", help="Zielordner für ZIP-Sicherung der Benutzer-Einstellungen")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    rows = inventory(with_hash=bool(a.json))
    py = python_info()
    print(f"PYTHON {py['version']} {py['bits']} bit | {py['executable']} | comtypes {py.get('comtypes')} | gen-Cache {py.get('comtypes_gen_cache', '-')}")
    for r in rows:
        mark = "OK " if r["vorhanden"] else "-- "
        size = f"{r['bytes']:>10,}".replace(",", ".") if "bytes" in r else " " * 10
        print(f"{mark}{r['kategorie']:<22}{r['zweck'][:46]:<47}{size}  {r.get('geaendert', '')[:10]:<10}  {r['pfad']}")
    missing = [r for r in rows if not r["vorhanden"]]
    print(f"\n{len(rows)} Einträge, {len(rows) - len(missing)} vorhanden, {len(missing)} fehlen")
    if a.json:
        json.dump(dict(erstellt=dt.datetime.now().astimezone().isoformat(timespec="seconds"), python=py, eintraege=rows),
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("JSON:", a.json)
    if a.backup:
        z, n, regok, h = backup(rows, a.backup)
        print(f"SICHERUNG: {z} | {n} Dateien | Registry-Export {'OK' if regok else 'FEHLER'} | SHA-256 {h}")


if __name__ == "__main__":
    main()
