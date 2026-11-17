"""
rfem_interfaces_probe.py – Schnittstellen-Landkarte RFEM 5 / RFEM 6 live prüfen (NUR LESEN, keine Modelländerung).

Prüft:
  A  RFEM 5 COM          – Typbibliothek, laufende Instanz, Version, COM-Lizenz (LockLicense/Unlock)
  B  RFEM 6 gRPC (API II) – Port, dlubal.api-Version ↔ RFEM-Version, Aufruf get_application_info
                           (B0 ohne Key, B1 mit Key aus dem Dlubal-Key-Store per NAME)
  C  RFEM 6 WebServices (API I, SOAP, RFEM_Python_Client) – Port 8081 + /wsdl
  D  Installationen       – RFEM-5/6-Versionen, RFEM6Server.exe, bin\\python.exe (Dlubal-MCP ab 6.13.0002)

API-Key: wird NIE ausgegeben oder gespeichert. Quelle nur (1) Umgebungsvariable RFEM_API_KEY oder
(2) --key-name <Name> aus dem Dlubal-Key-Store %LOCALAPPDATA%\\Dlubal\\api\\config.ini [api_keys].
Aufrufe: get_application_info / get_subscription_info / get_model_list (lesend).

  python rfem_interfaces_probe.py                         # ohne Key (B0)
  python rfem_interfaces_probe.py --key-name nexus_aec_engine
  python rfem_interfaces_probe.py --json probe.json
"""
import argparse, configparser, datetime as dt, glob, json, os, socket, sys, urllib.request

LOCAL_KEYSTORE = os.path.expandvars(r"%LOCALAPPDATA%\Dlubal\api\config.ini")


def port_open(port, host="127.0.0.1", t=0.7):
    s = socket.socket(); s.settimeout(t)
    try:
        s.connect((host, port)); return True
    except OSError:
        return False
    finally:
        s.close()


def err(e):
    import html, re
    txt = html.unescape(re.sub(r"<br\s*/?>", " ", str(e).strip()))
    return f"{type(e).__name__}: {txt[:1200]}"


def probe_rfem5():
    out = dict(typelib=os.path.exists(r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll"))
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from rfem_connect import rfem_session
        with rfem_session() as (app, R):
            out.update(status="PASS", version=app.GetVersion(), com_licensed=bool(app.IsComLicensed()),
                       models=app.GetModelCount())
    except Exception as e:
        out.update(status="FAIL", error=err(e))
    return out


def resolve_key(key_name):
    """Key-Wert aus Env oder Key-Store holen – Wert verlässt diese Funktion nur Richtung Application()."""
    if os.environ.get("RFEM_API_KEY"):
        return os.environ["RFEM_API_KEY"], "env:RFEM_API_KEY"
    if key_name:
        c = configparser.ConfigParser(); c.read(LOCAL_KEYSTORE)
        v = c.get("api_keys", key_name, fallback=None)
        return v, f"keystore:{key_name}" if v else f"keystore:{key_name}:NICHT_GEFUNDEN"
    return None, "kein Key"


def grpc_call(key_value, port):
    from dlubal.api import rfem
    from google.protobuf.json_format import MessageToDict
    r = {}
    with rfem.Application(api_key_value=key_value, port=port) as app:
        info = app.get_application_info()
        r["application"] = MessageToDict(info, preserving_proto_field_name=True)
        for name in ("get_subscription_info", "get_model_list"):
            try:
                r[name] = MessageToDict(getattr(app, name)(), preserving_proto_field_name=True)
            except Exception as e:
                r[name] = err(e)
    return r


def probe_rfem6(key_name, port):
    out = dict(port=port, port_open=port_open(port))
    try:
        from importlib.metadata import version
        out["dlubal_api"] = version("dlubal.api")
    except Exception:
        out["dlubal_api"] = None
    if not out["port_open"] or not out["dlubal_api"]:
        out["status"] = "BLOCKED"; return out
    try:                                                         # B0: ohne Key
        out["B0_ohne_key"] = dict(status="PASS", **grpc_call(None, port))
    except Exception as e:
        out["B0_ohne_key"] = dict(status="FAIL", error=err(e))
    val, src = resolve_key(key_name)
    out["key_quelle"] = src                                      # nur Quelle, nie der Wert
    if val:
        try:
            out["B1_mit_key"] = dict(status="PASS", **grpc_call(val, port))
        except Exception as e:
            out["B1_mit_key"] = dict(status="FAIL", error=err(e))
    passed = [k for k in ("B0_ohne_key", "B1_mit_key") if out.get(k, {}).get("status") == "PASS"]
    out["status"] = "PASS" if passed else "FAIL"
    app = next((out[k]["application"] for k in passed), None)
    if app and out["dlubal_api"]:
        v = app.get("version", ""); parts = v.split(".")
        out["versionspaar"] = f"RFEM {v} ↔ dlubal.api {out['dlubal_api']}"
        out["minor_passt"] = len(parts) > 2 and out["dlubal_api"].split(".")[1:3] == parts[1:3]
    return out


def probe_soap(port=8081):
    out = dict(port=port, port_open=port_open(port))
    if out["port_open"]:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/wsdl", timeout=3) as r:
                body = r.read(400).decode("utf-8", "replace")
            out.update(status="PASS" if "definitions" in body or "wsdl" in body.lower() else "UNKLAR", head=body[:120])
        except Exception as e:
            out.update(status="FAIL", error=err(e))
    else:
        out["status"] = "BLOCKED"
    return out


def installs():
    d = {}
    for p in sorted(glob.glob(r"C:\Program Files\Dlubal\RFEM *")):
        v = os.path.basename(p).split()[-1]
        b = os.path.join(p, "bin")
        d[v] = dict(rfem6server=os.path.exists(os.path.join(b, "RFEM6Server.exe")),
                    bin_python=os.path.exists(os.path.join(b, "python.exe")),
                    mcp_modul=bool(glob.glob(os.path.join(b, "**", "rfem_mcp_server*"), recursive=True)),
                    rfem5_com=os.path.exists(os.path.join(p, "RFEM64.exe")))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-name", help="Name eines Keys im Dlubal-Key-Store (Wert wird nie ausgegeben)")
    ap.add_argument("--port", type=int, default=int(os.environ.get("RFEM_API_PORT", 9000)))
    ap.add_argument("--json")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    rep = dict(zeit=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
               keystore_vorhanden=os.path.exists(LOCAL_KEYSTORE),
               A_rfem5_com=probe_rfem5(), B_rfem6_grpc=probe_rfem6(a.key_name, a.port),
               C_rfem6_soap=probe_soap(), D_installationen=installs())
    s = json.dumps(rep, ensure_ascii=False, indent=1, default=str)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
