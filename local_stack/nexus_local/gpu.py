"""GPU telemetry (Control-Tower tile) and start-up GPU health check.

Read-only: runs nvidia-smi, reads registry/file metadata and the Ollama server log tail.
Never installs, deletes or modifies anything. Statuses: PASS / WARN / FAIL / NOT_RUN.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

SMI_FIELDS = ("name", "driver_version", "utilization.gpu", "memory.used", "memory.total",
              "temperature.gpu", "power.draw", "power.limit", "compute_cap")
DISCOVERY_FAIL = re.compile(r"failure during llama-server GPU discovery|0xc0000005|no compatible GPUs were discovered",
                            re.IGNORECASE)
VCREDIST_KEY = r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"


def _num(v: str):
    v = v.strip()
    if v in ("", "[N/A]", "N/A", "[Not Supported]"):
        return None
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return v


def find_smi() -> str | None:
    p = shutil.which("nvidia-smi")
    if p:
        return p
    cand = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "nvidia-smi.exe"
    return str(cand) if cand.is_file() else None


def run_smi(args: list[str], timeout: float = 5.0) -> str:
    exe = find_smi()
    if not exe:
        raise FileNotFoundError("nvidia-smi nicht gefunden")
    flags = 0x08000000 if sys.platform == "win32" else 0  # CREATE_NO_WINDOW
    return subprocess.run([exe, *args], capture_output=True, text=True, timeout=timeout,
                          creationflags=flags, check=True).stdout


def parse_smi_csv(text: str) -> list[dict]:
    gpus = []
    for line in text.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < len(SMI_FIELDS):
            continue
        d = dict(zip(SMI_FIELDS, parts))
        gpus.append({"name": d["name"], "driver": d["driver_version"], "util_pct": _num(d["utilization.gpu"]),
                     "mem_used_mib": _num(d["memory.used"]), "mem_total_mib": _num(d["memory.total"]),
                     "temp_c": _num(d["temperature.gpu"]), "power_w": _num(d["power.draw"]),
                     "power_limit_w": _num(d["power.limit"]), "compute_cap": d["compute_cap"]})
    return gpus


def parse_cuda_max(header: str) -> str | None:
    m = re.search(r"CUDA Version:\s*([\d.]+)", header)
    return m.group(1) if m else None


def offload_alerts(ps_models: list[dict]) -> list[str]:
    out = []
    for m in ps_models:
        size, vram = m.get("size") or 0, m.get("size_vram") or 0
        if size and vram < size:
            out.append(f"{m.get('name')}: nur {round(100 * vram / size)}% GPU "
                       f"(ctx {m.get('context_length', '?')}) -> CPU-Offload")
    return out


def gpu_probe(cfg: dict, smi: Callable[[list[str]], str] = run_smi,
              ps: Callable[[], list[dict]] | None = None) -> Callable[[], dict]:
    """Live probe for the Control-Tower tile (every 15 s via ExternalMonitorTask)."""
    g = cfg.get("gpu", {})
    temp_warn, mem_warn = float(g.get("temp_warn_c", 83)), float(g.get("mem_warn_pct", 95))

    def probe() -> dict:
        gpus = parse_smi_csv(smi([f"--query-gpu={','.join(SMI_FIELDS)}", "--format=csv,noheader,nounits"]))
        if not gpus:
            raise RuntimeError("nvidia-smi lieferte keine GPU")
        alerts = []
        for x in gpus:
            if isinstance(x["temp_c"], (int, float)) and x["temp_c"] >= temp_warn:
                alerts.append(f"{x['name']}: Temperatur {x['temp_c']} C >= {temp_warn:g} C")
            if x["mem_total_mib"] and isinstance(x["mem_used_mib"], (int, float)) \
                    and 100 * x["mem_used_mib"] / x["mem_total_mib"] >= mem_warn:
                alerts.append(f"{x['name']}: VRAM {x['mem_used_mib']}/{x['mem_total_mib']} MiB >= {mem_warn:g}%")
        if ps:
            try:
                alerts += offload_alerts(ps())
            except Exception:  # noqa: BLE001 - Ollama down is reported by its own task
                pass
        return {"gpus": gpus, "alerts": alerts, "state": "WARN" if alerts else "OK"}
    return probe


def read_vcredist() -> str | None:
    if sys.platform != "win32":
        return None
    import winreg
    for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, VCREDIST_KEY, 0, winreg.KEY_READ | view) as k:
                return str(winreg.QueryValueEx(k, "Version")[0]).lstrip("v")
        except OSError:
            continue
    return None


def _ver_tuple(v: str) -> tuple:
    return tuple(int(p) for p in re.findall(r"\d+", v)[:4])


def tail_text(path: Path, max_bytes: int = 200_000) -> str:
    with open(path, "rb") as f:
        f.seek(0, 2)
        f.seek(max(0, f.tell() - max_bytes))
        return f.read().decode("utf-8", "replace")


def health_check(cfg: dict, expand: Callable, smi: Callable[[list[str]], str] = run_smi,
                 vcredist: Callable[[], str | None] = read_vcredist) -> dict:
    """Start-up GPU health check. Returns {'state', 'checks': [{id, name, status, detail}]}."""
    g = cfg.get("gpu", {})
    lib = expand(g.get("ollama_lib_dir", r"%LOCALAPPDATA%\Programs\Ollama\lib\ollama"))
    log = expand(g.get("ollama_server_log", r"%LOCALAPPDATA%\Ollama\server.log"))
    vc_min = str(g.get("vcredist_min", "14.40"))
    win = sys.platform == "win32"
    checks = []

    def add(cid, name, status, detail):
        checks.append({"id": cid, "name": name, "status": status, "detail": detail})

    # G01 driver / nvidia-smi
    try:
        header = smi([])
        gpus = parse_smi_csv(smi([f"--query-gpu={','.join(SMI_FIELDS)}", "--format=csv,noheader,nounits"]))
        if gpus:
            x = gpus[0]
            add("G01", "NVIDIA-Treiber + GPU", "PASS",
                f"{x['name']} · Treiber {x['driver']} · CUDA max {parse_cuda_max(header) or '?'} · "
                f"{x['mem_total_mib']} MiB · CC {x['compute_cap']}")
        else:
            add("G01", "NVIDIA-Treiber + GPU", "FAIL", "nvidia-smi ohne GPU-Zeile")
    except FileNotFoundError:
        add("G01", "NVIDIA-Treiber + GPU", "FAIL" if win else "NOT_RUN", "nvidia-smi nicht gefunden")
    except Exception as exc:  # noqa: BLE001
        add("G01", "NVIDIA-Treiber + GPU", "FAIL", f"{type(exc).__name__}: {exc}"[:200])

    # G02 Ollama bundled CUDA runtime dirs
    if lib and Path(lib).is_dir():
        found = sorted(d.name for d in Path(lib).iterdir() if d.is_dir() and d.name.startswith("cuda_v"))
        dll_ok = [d for d in found if any(Path(lib, d).glob("ggml-cuda*"))]
        add("G02", "Ollama CUDA-Runtime (cuda_v12/v13)", "PASS" if dll_ok else "FAIL",
            f"{lib}: {', '.join(found) or 'keine cuda_v*'}; ggml-cuda in: {', '.join(dll_ok) or '-'}")
    else:
        add("G02", "Ollama CUDA-Runtime (cuda_v12/v13)", "FAIL" if win else "NOT_RUN", f"Ordner fehlt: {lib}")

    # G03 VC++ 2015-2022 x64 redistributable
    v = vcredist()
    if v is None:
        add("G03", "VC++ 2015-2022 x64 Redistributable", "WARN" if win else "NOT_RUN",
            "nicht gefunden" if win else "nur Windows")
    else:
        ok = _ver_tuple(v) >= _ver_tuple(vc_min)
        add("G03", "VC++ 2015-2022 x64 Redistributable", "PASS" if ok else "WARN",
            f"Version {v} (Minimum {vc_min})" + ("" if ok else " -> aktualisieren, sonst CPU-Fallback moeglich"))

    # G04 Ollama server.log: GPU discovery failures
    if log and Path(log).is_file():
        hits = [ln.strip()[:200] for ln in tail_text(Path(log)).splitlines() if DISCOVERY_FAIL.search(ln)]
        add("G04", "Ollama GPU-Erkennung (server.log)", "FAIL" if hits else "PASS",
            hits[-1] if hits else "keine Discovery-Fehler im Log-Ende")
    else:
        add("G04", "Ollama GPU-Erkennung (server.log)", "NOT_RUN", f"Log fehlt: {log}")

    order = {"FAIL": 3, "WARN": 2, "PASS": 1, "NOT_RUN": 0}
    worst = max((c["status"] for c in checks), key=lambda s: order[s])
    return {"state": worst, "checks": checks}
