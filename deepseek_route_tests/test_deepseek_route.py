"""Offline DeepSeek request-contract checks for NEXUS orchestrator."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "orchestrator"))
from nexus_orch import providers


class DeepSeekRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = json.loads((ROOT / "orchestrator/config/routing.json").read_text(encoding="utf-8"))
        cls.settings = config["providers"]["deepseek"]
        assert config["routes"]["rfem_prompt"]["fallback"] == []

    def test_no_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(providers.ProviderError):
                providers.Provider("deepseek", self.settings).complete("synthetic test")

    def test_default_thinking_disabled_and_bounded(self):
        calls = []
        def fake_post(url, headers, body, timeout=120):
            calls.append((url, headers, body, timeout))
            return {"choices": [{"message": {"content": "OK"}}]}
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-not-real"}):
            with patch.object(providers, "_post", side_effect=fake_post):
                response = providers.Provider("deepseek", self.settings).complete("synthetic test")
        self.assertEqual(response["text"], "OK")
        url, headers, body, timeout = calls[0]
        self.assertEqual(url, "https://api.deepseek.com/chat/completions")
        self.assertEqual(body["thinking"], {"type": "disabled"})
        self.assertNotIn("temperature", body)
        self.assertEqual(body["max_tokens"], 512)
        self.assertEqual(timeout, 30)
        self.assertNotIn("synthetic-not-real", json.dumps(body))

    def test_review_thinking_high(self):
        captured = []
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "synthetic-not-real"}):
            with patch.object(providers, "_post", side_effect=lambda u, h, b, t: captured.append(b) or
                              {"choices": [{"message": {"content": "OK"}}]}):
                providers.Provider("deepseek", {**self.settings, "thinking": "enabled",
                                                "reasoning_effort": "high"}).complete("review")
        self.assertEqual(captured[0]["reasoning_effort"], "high")


if __name__ == "__main__":
    unittest.main()
