"""Single-instance lock and owned child processes (Windows Job Object, kill-on-close)."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .util import CREATE_NEW_PROCESS_GROUP, CREATE_NO_WINDOW, IS_WINDOWS


class AlreadyRunning(RuntimeError):
    pass


class InstanceLock:
    """Kernel-held byte lock on a private local file. Released automatically if the process dies."""

    def __init__(self, path: Path):
        self.path = path
        self.fh = None

    def acquire(self) -> "InstanceLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.path, "a+b")
        try:
            if IS_WINDOWS:
                import msvcrt
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            self.fh.close()
            self.fh = None
            raise AlreadyRunning(str(self.path)) from exc
        return self

    def release(self) -> None:
        if not self.fh:
            return
        try:
            if IS_WINDOWS:
                import msvcrt
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
        finally:
            self.fh.close()
            self.fh = None


class JobObject:
    """Windows Job Object with JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE: children die with the supervisor.

    No-op on non-Windows. Never used to kill processes the supervisor did not start.
    """

    def __init__(self):
        self.handle = None
        if not IS_WINDOWS:
            return
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in ("ReadOperationCount", "WriteOperationCount",
                        "OtherOperationCount", "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class BASIC(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class EXTENDED(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", BASIC), ("IoInfo", IO_COUNTERS),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        k32.CreateJobObjectW.restype = wintypes.HANDLE
        h = k32.CreateJobObjectW(None, None)
        if not h:
            return
        info = EXTENDED()
        info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not k32.SetInformationJobObject(h, 9, ctypes.byref(info), ctypes.sizeof(info)):  # ExtendedLimitInformation
            k32.CloseHandle(h)
            return
        self.k32, self.handle = k32, h

    def assign(self, proc: subprocess.Popen) -> bool:
        if not self.handle:
            return False
        return bool(self.k32.AssignProcessToJobObject(self.handle, int(proc._handle)))  # type: ignore[attr-defined]


def spawn(cmd: list[str], cwd: str | None, env: dict | None, log_path: Path, job: JobObject | None) -> subprocess.Popen:
    """Start an owned child: no shell, no console window, stdin DEVNULL, output appended to a file."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    out = open(log_path, "ab")
    flags = (CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP) if IS_WINDOWS else 0
    try:
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=out,
                                stderr=subprocess.STDOUT, shell=False, creationflags=flags,
                                close_fds=True)
    finally:
        out.close()  # child keeps its own handle
    if job:
        job.assign(proc)
    return proc


def controlled_env(extra: dict | None = None, drop: tuple[str, ...] = ()) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in drop}
    env.update({k: str(v) for k, v in (extra or {}).items()})
    return env
