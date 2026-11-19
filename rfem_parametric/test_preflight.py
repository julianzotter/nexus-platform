"""Offline/secret-safe RFEM and DeepSeek preflight tests."""
import unittest
from unittest.mock import patch

from preflight import inspect_host


class PreflightTests(unittest.TestCase):
    def test_never_probes_host_or_credential_store(self):
        with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "synthetic-secret"}):
            data = inspect_host()
        self.assertTrue(data["deepseek"]["process_key_present"])
        self.assertNotIn("synthetic-secret", str(data))
        self.assertEqual(data["rfem5"]["com_application"], "NOT_PROBED")
        self.assertEqual(data["rfem6"]["grpc_server"], "NOT_PROBED")
        self.assertEqual(data["model_creation"], "BLOCKED")
        self.assertEqual(data["solver"], "NOT_RUN")

    def test_missing_deepseek_key(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(inspect_host()["deepseek"]["process_key_present"])
