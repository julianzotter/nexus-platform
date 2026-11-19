"""Invoke the existing DSH headless profile; never copy GUI credentials."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
from typing import Any


def configured(cfg: dict[str, Any]) -> bool:
    cwd = os.environ.get("NEXUS_DSH_WORKDIR")
    return bool(shutil.which(cfg.get("executable", "dsh")) and cwd and Path(cwd).is_dir())


def complete(cfg: dict[str, Any], prompt: str, system: str = "") -> dict[str, Any]:
    # Import lazily to avoid a Provider/dsh module initialization cycle.
    from .providers import ProviderError
    executable = shutil.which(cfg.get("executable", "dsh"))
    cwd = os.environ.get("NEXUS_DSH_WORKDIR")
    if not executable or not cwd or not Path(cwd).is_dir():
        raise ProviderError("DSH executable or NEXUS_DSH_WORKDIR unavailable")
    command = [executable, "--profile", "headless", "--permission-mode", "read-only",
               "--approval-policy", "never", "--json", "-"]
    task = (system + "\n\n" if system else "") + prompt
    try:
        result = subprocess.run(command, input=task, cwd=cwd, text=True,
                                capture_output=True, timeout=cfg.get("timeout", 180), shell=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ProviderError(f"DSH launch failed: {type(error).__name__}") from None
    if result.returncode:
        raise ProviderError(f"DSH failed with exit {result.returncode}; inspect local sanitized logs")
    try:
        events = [json_event(line) for line in result.stdout.splitlines() if line.strip()]
        final = [event for event in events if event.get("type") == "final"]
        if any(event.get("type") == "error" for event in events) or len(final) != 1:
            raise ValueError("No unique successful final event")
        event = final[0]
        if (not isinstance(event.get("reason"), dict) or event["reason"].get("kind") != "completed"
                or not isinstance(event.get("text"), str) or not event["text"].strip()):
            raise ValueError("Incomplete DSH final event")
        return {"text": event["text"], "citations": [], "model": None,
                "runtime": "dsh-headless", "session_id": event.get("sessionId")}
    except (ValueError, TypeError, AttributeError) as error:
        raise ProviderError("DSH event contract failed") from None


def json_event(line: str) -> dict[str, Any]:
    import json
    event = json.loads(line)
    if not isinstance(event, dict): raise ValueError("DSH event must be an object")
    return event
