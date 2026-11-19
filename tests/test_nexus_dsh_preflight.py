"""Deterministic offline tests for the read-only Windows preflight."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "tools/windows/nexus_dsh_preflight.py"
spec = importlib.util.spec_from_file_location("nexus_dsh_preflight", SCRIPT)
assert spec is not None and spec.loader is not None
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PreflightTests(TestCase):
    def test_missing_profile_is_blocked(self) -> None:
        with TemporaryDirectory() as tmp:
            result = preflight.profile_inventory(Path(tmp))
        self.assertEqual(result["status"], "BLOCKED")

    def test_profile_hash_uses_original_bytes(self) -> None:
        with TemporaryDirectory() as tmp:
            file = Path(tmp) / "profiles" / "web" / "cordis.patch.yml"
            file.parent.mkdir(parents=True)
            file.write_bytes(b"test\r\n")
            result = preflight.profile_inventory(Path(tmp))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(json.loads(result["evidence"])[0]["profile"], "web")

    def test_sqlite_select_does_not_mutate_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "snapshot.db"
            with sqlite3.connect(path) as connection:
                connection.execute("CREATE TABLE facts(id INTEGER)")
            before = path.read_bytes()
            result = preflight.sqlite_readonly(path)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(before, path.read_bytes())

    def test_github_missing_cli_fails_closed(self) -> None:
        with patch.object(preflight.shutil, "which", return_value=None):
            result = preflight.github_readonly()
        self.assertEqual(result["status"], "BLOCKED")

    def test_ollama_unreachable_fails_closed(self) -> None:
        with patch.object(preflight.urllib.request, "urlopen", side_effect=OSError("offline")):
            self.assertEqual(preflight.ollama_tags()["status"], "BLOCKED")


if __name__ == "__main__":
    main()
