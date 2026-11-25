"""NEXUS local supervisor: owns all local tasks, restarts them with backoff, publishes status.

Run:  pythonw -m nexus_local.supervisor --config %LOCALAPPDATA%\\NEXUS\\local\\nexus-local.json
Diag: python  -m nexus_local.supervisor --config ... --foreground   (console logging)
"""
from __future__ import annotations

import argparse
import json
import logging
import random
import sys
import threading
import time
import traceback
import urllib.request
from pathlib import Path
from typing import Callable

from . import __version__
from .util import atomic_write_json, ensure_token, expand, iso, load_config, load_json, setup_logging
from .winproc import AlreadyRunning, InstanceLock, JobObject, controlled_env, spawn

log = logging.getLogger("nexus_local.supervisor")

BACKOFF = (5, 10, 30, 60, 120, 300)
CIRCUIT_FAILS = 8          # consecutive failures -> circuit OPEN (manual restart required)


class Task:
    kind = "task"

    def __init__(self, name: str, desc: str = ""):
        self.name, self.desc = name, desc
        self.status = "STOPPED"   # STOPPED | STARTING | RUNNING | BACKOFF | FAILED | CIRCUIT_OPEN | EXTERNAL | BLOCKED
        self.restarts = 0
        self.consecutive_fail = 0
        self.last_ok: str | None = None
        self.last_error: str | None = None
        self.started_at: float | None = None
        self.next_try = 0.0
        self.desired = "running"
        self.info: dict = {}
        self.lock = threading.RLock()

    def fail(self, err: str) -> None:
        with self.lock:
            self.consecutive_fail += 1
            self.last_error = f"{iso()} {err}"[:400]
            if self.consecutive_fail >= CIRCUIT_FAILS:
                self.status = "CIRCUIT_OPEN"
            else:
                self.status = "BACKOFF"
                delay = BACKOFF[min(self.consecutive_fail - 1, len(BACKOFF) - 1)]
                self.next_try = time.monotonic() + delay * (0.8 + 0.4 * random.random())
        log.warning("task %s failed: %s", self.name, err[:300])

    def ok(self, **info) -> None:
        with self.lock:
            self.consecutive_fail = 0
            self.last_ok = iso()
            self.info.update(info)

    def snapshot(self) -> dict:
        with self.lock:
            up = int(time.monotonic() - self.started_at) if self.started_at and self.status in ("RUNNING", "EXTERNAL") else 0
            return {"name": self.name, "kind": self.kind, "desc": self.desc, "status": self.status,
                    "desired": self.desired, "restarts": self.restarts, "uptime_s": up,
                    "last_ok": self.last_ok, "last_error": self.last_error, "info": self.info}

    # lifecycle hooks
    def tick(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


class PeriodicTask(Task):
    kind = "periodic"

    def __init__(self, name: str, fn: Callable[[], dict], interval: float, desc: str = ""):
        super().__init__(name, desc)
        self.fn, self.interval = fn, interval
        self.thread: threading.Thread | None = None
        self.stop_ev = threading.Event()
        self.run_now_ev = threading.Event()

    def _loop(self) -> None:
        while not self.stop_ev.is_set():
            t0 = time.monotonic()
            try:
                result = self.fn() or {}
                self.ok(last_run=iso(), duration_s=round(time.monotonic() - t0, 2), result=result)
                self.status = "RUNNING"
                wait = self.interval
            except Exception as exc:  # noqa: BLE001 - task isolation
                self.fail(f"{type(exc).__name__}: {exc}")
                log.debug(traceback.format_exc())
                if self.status == "CIRCUIT_OPEN":
                    return
                wait = max(1.0, self.next_try - time.monotonic())
            self.run_now_ev.wait(wait)
            self.run_now_ev.clear()

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.stop_ev.clear()
        self.status, self.started_at, self.consecutive_fail = "RUNNING", time.monotonic(), 0
        self.thread = threading.Thread(target=self._loop, name=self.name, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self.stop_ev.set()
        self.run_now_ev.set()
        self.status = "STOPPED"

    def run_now(self) -> None:
        self.run_now_ev.set()

    def tick(self) -> None:
        if self.desired == "running" and self.status != "CIRCUIT_OPEN" and not (self.thread and self.thread.is_alive()):
            self.restarts += 1
            self.start()


class ServerTask(Task):
    kind = "server"

    def __init__(self, name: str, factory: Callable[[], object], desc: str = ""):
        super().__init__(name, desc)
        self.factory, self.server, self.thread = factory, None, None

    def start(self) -> None:
        try:
            self.server = self.factory()
        except OSError as exc:
            self.fail(f"PORT_IN_USE_OR_BIND_FAILED: {exc}")
            return
        self.thread = threading.Thread(target=self.server.serve_forever, name=self.name, daemon=True)
        self.thread.start()
        self.status, self.started_at = "RUNNING", time.monotonic()
        self.ok(port=self.server.server_address[1], instance=getattr(self.server, "instance_id", None))

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        self.status = "STOPPED"

    def tick(self) -> None:
        if self.desired != "running" or self.status == "CIRCUIT_OPEN":
            return
        alive = self.thread and self.thread.is_alive()
        if not alive and (self.status != "BACKOFF" or time.monotonic() >= self.next_try):
            if self.status == "RUNNING":
                self.fail("SERVER_THREAD_DIED")
                return
            self.restarts += 1
            self.start()


class ProcessTask(Task):
    """Owned child process (started by us, assigned to our job object)."""
    kind = "process"

    def __init__(self, name: str, cmd: list[str], cwd: str | None, env: dict, log_dir: Path, job: JobObject,
                 health_url: str | None = None, desc: str = ""):
        super().__init__(name, desc)
        self.cmd, self.cwd, self.env, self.log_dir, self.job, self.health_url = cmd, cwd, env, log_dir, job, health_url
        self.proc = None

    def start(self) -> None:
        try:
            self.proc = spawn(self.cmd, self.cwd, controlled_env(self.env),
                              self.log_dir / f"{self.name}_{time.strftime('%Y%m%d')}.log", self.job)
        except OSError as exc:
            self.fail(f"SPAWN_FAILED: {exc}")
            return
        self.status, self.started_at = "RUNNING", time.monotonic()
        self.ok(pid=self.proc.pid)

    def stop(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(10)
            except Exception:
                self.proc.kill()
        self.status = "STOPPED"

    def tick(self) -> None:
        if self.desired != "running" or self.status == "CIRCUIT_OPEN":
            return
        if self.proc and self.proc.poll() is not None and self.status == "RUNNING":
            self.fail(f"EXITED code={self.proc.returncode}")
            self.proc = None
            return
        if self.proc is None and (self.status != "BACKOFF" or time.monotonic() >= self.next_try):
            self.restarts += 1
            self.start()
        elif self.health_url and self.proc and self.status == "RUNNING":
            if http_ok(self.health_url):
                self.ok()


class ExternalMonitorTask(Task):
    """Monitor-only (e.g. Ollama tray app): never started, stopped or restarted by NEXUS."""
    kind = "external"

    def __init__(self, name: str, probe: Callable[[], dict], desc: str = ""):
        super().__init__(name, desc)
        self.probe = probe
        self._last = 0.0

    def start(self) -> None:
        self.started_at = time.monotonic()
        self.tick(force=True)

    def stop(self) -> None:
        self.status = "STOPPED"  # monitoring paused; external process untouched

    def tick(self, force: bool = False) -> None:
        if self.desired != "running" or (not force and time.monotonic() - self._last < 15):
            return
        self._last = time.monotonic()
        try:
            info = self.probe()
            self.status = "EXTERNAL"
            self.ok(**info)
        except Exception as exc:  # noqa: BLE001
            self.status = "BLOCKED"
            self.last_error = f"{iso()} NOT_REACHABLE {exc}"[:300]


def http_ok(url: str, timeout: float = 3.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.status < 300
    except Exception:
        return False


def http_json(url: str, timeout: float = 5.0, data: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read(2_000_000).decode("utf-8"))


class Supervisor:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.runtime = Path(cfg["_runtime"])
        self.log_dir = self.runtime / "logs"
        self.state_dir = self.runtime / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.token = ensure_token(self.runtime / "token.txt")
        self.job = JobObject()
        self.tasks: dict[str, Task] = {}
        self.stop_ev = threading.Event()
        self.boot_id = f"{int(time.time())}-{random.randrange(16**6):06x}"
        self.started = iso()
        self.desired_path = self.state_dir / "desired.json"
        self.desired = load_json(self.desired_path, {}) or {}

    # ---------------------------------------------------------------- registry
    def add(self, task: Task, enabled: bool = True) -> None:
        task.desired = self.desired.get(task.name, "running" if enabled else "stopped")
        self.tasks[task.name] = task

    def set_desired(self, name: str, state: str) -> None:
        self.desired[name] = state
        atomic_write_json(self.desired_path, self.desired)

    def action(self, name: str, action: str) -> dict:
        t = self.tasks.get(name)
        if not t:
            return {"error": "UNKNOWN_TASK"}
        if action == "stop":
            self.set_desired(name, "stopped"); t.desired = "stopped"; t.stop()
        elif action == "start":
            self.set_desired(name, "running"); t.desired = "running"
            t.consecutive_fail = 0
            if t.status in ("STOPPED", "CIRCUIT_OPEN", "FAILED", "BLOCKED"):
                t.status = "STOPPED"; t.start()
        elif action == "restart":
            t.stop(); t.consecutive_fail = 0; t.desired = "running"; self.set_desired(name, "running"); t.start()
        elif action == "run_now" and isinstance(t, PeriodicTask):
            t.run_now()
        else:
            return {"error": "UNSUPPORTED_ACTION"}
        log.info("action %s %s", action, name)
        return {"ok": True, "task": t.snapshot()}

    def status(self) -> dict:
        return {"service": "nexus-local-supervisor", "version": __version__, "boot_id": self.boot_id,
                "started": self.started, "now": iso(), "agent_id": self.cfg.get("agent_id"),
                "config": self.cfg.get("_config_path"), "job_object": bool(self.job.handle),
                "tasks": [t.snapshot() for t in self.tasks.values()]}

    # ---------------------------------------------------------------- run
    def run(self) -> int:
        from .wiring import wire
        wire(self)
        for t in self.tasks.values():
            if t.desired == "running":
                t.start()
        log.info("supervisor %s started boot=%s tasks=%s", __version__, self.boot_id, list(self.tasks))
        while not self.stop_ev.is_set():
            for t in self.tasks.values():
                try:
                    t.tick()
                except Exception as exc:  # noqa: BLE001
                    t.fail(f"TICK {type(exc).__name__}: {exc}")
            try:
                atomic_write_json(self.state_dir / "status.json", self.status())
            except OSError as exc:
                log.warning("status write failed: %s", exc)
            self.stop_ev.wait(5)
        for t in self.tasks.values():
            try:
                t.stop()
            except Exception:  # noqa: BLE001
                pass
        log.info("supervisor stopped")
        return 0

    def shutdown(self) -> None:
        self.set_desired("_supervisor", "stopped")
        self.stop_ev.set()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--foreground", action="store_true")
    ap.add_argument("--clear-stop", action="store_true", help="clear a persisted stop intent and start")
    ap.add_argument("--clear-stop-only", action="store_true", help="clear a persisted stop intent and exit")
    a = ap.parse_args(argv)
    cfg = load_config(Path(a.config))
    runtime = Path(cfg["_runtime"])
    logger = setup_logging(runtime / "logs", console=a.foreground)

    def hook(et, ev, tb):
        logger.error("UNCAUGHT %s", "".join(traceback.format_exception(et, ev, tb))[-4000:])
    sys.excepthook = hook
    threading.excepthook = lambda args: hook(args.exc_type, args.exc_value, args.exc_traceback)

    desired = load_json(runtime / "state" / "desired.json", {}) or {}
    if a.clear_stop_only:
        if desired.get("_supervisor") == "stopped":
            desired["_supervisor"] = "running"
            atomic_write_json(runtime / "state" / "desired.json", desired)
        return 0
    if a.clear_stop and desired.get("_supervisor") == "stopped":
        desired["_supervisor"] = "running"
        atomic_write_json(runtime / "state" / "desired.json", desired)
    elif desired.get("_supervisor") == "stopped":
        logger.info("stop intent persisted -> exit 0 (use Start-NexusLocal.cmd)")
        return 0
    try:
        lock = InstanceLock(runtime / "state" / "supervisor.lock").acquire()
    except AlreadyRunning:
        logger.info("another supervisor holds the lock -> exit 0")
        return 0
    try:
        return Supervisor(cfg).run()
    finally:
        lock.release()


if __name__ == "__main__":
    raise SystemExit(main())
