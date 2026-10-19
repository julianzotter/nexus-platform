"""Offline regressions; no RFEM, network, credentials or engineering release."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    spec = importlib.util.spec_from_file_location(Path(relative).stem, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


result = load("skills/rfem6-mcp-engineering/scripts/validate_result.py")
audit = load("skills/aec-connectivity-audit/scripts/create_audit_bundle.py")


class ResultTests(unittest.TestCase):
    def setUp(self):
        self.value = {
            "schema_version": "0.1.0", "mode": "LIVE", "source": "RFEM",
            "run_id": "fixture-only", "model_fingerprint": "fixture-model",
            "calculation_id": "fixture-calc", "combination_id": "CO1",
            "converged": True, "observed_at": "2026-10-19T16:00:00Z",
            "units": {"force": "N", "length": "m", "moment": "N*m"},
            "values": {"N_max": 12000.0}}
        self.value["result_sha256"] = result.values_hash(self.value["values"])

    def check(self, **changes):
        value = copy.deepcopy(self.value)
        value.update(changes)
        return result.validate(value, "fixture-model", "fixture-calc")

    def test_fixture_envelope_consistency(self):
        self.assertEqual(self.check(), [])

    def test_demo_not_live(self):
        self.assertIn("MISMATCH:mode", self.check(mode="DEMO"))

    def test_stale_model(self):
        self.assertIn("MISMATCH:model_fingerprint", self.check(model_fingerprint="other"))

    def test_stale_calculation(self):
        self.assertIn("MISMATCH:calculation_id", self.check(calculation_id="old"))

    def test_nonconvergence(self):
        self.assertIn("NOT_CONVERGED", self.check(converged=False))
        self.assertIn("NOT_CONVERGED", self.check(converged="true"))

    def test_units(self):
        self.assertIn("UNITS_NOT_SI_CONTRACT", self.check(units={"force": "kN"}))

    def test_payload_tamper(self):
        self.assertIn("RESULT_HASH_MISMATCH", self.check(values={"N_max": 12001.0}))

    def test_nan_and_boolean(self):
        self.assertIn("NONFINITE:N_max", self.check(values={"N_max": float("nan")}))
        self.assertIn("INVALID_VALUE:N_max", self.check(values={"N_max": True}))

    def test_missing_identity_and_timestamp(self):
        self.assertIn("MISSING:run_id", self.check(run_id=""))
        self.assertIn("TIMESTAMP_WITHOUT_ZONE", self.check(observed_at="2026-10-19"))


class AuditTests(unittest.TestCase):
    def test_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evidence = {"status": "PRECHECK_BLOCKED", "observations": ["RFEM not connected"]}
            target = audit.create_bundle(root, "fixture-001", evidence)
            audit.verify_bundle(target)
            with self.assertRaises(FileExistsError):
                audit.create_bundle(root, "fixture-001", evidence)

    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = audit.create_bundle(Path(folder), "fixture-002", {
                "status": "BLOCKED", "observations": []})
            (target / "evidence.json").write_text("changed")
            with self.assertRaisesRegex(ValueError, "READBACK_MISMATCH"):
                audit.verify_bundle(target)

    def test_path_and_status_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            for run in ("../escape", "/absolute", ""):
                with self.assertRaises(ValueError):
                    audit.create_bundle(Path(folder), run, {
                        "status": "BLOCKED", "observations": []})
            with self.assertRaises(ValueError):
                audit.create_bundle(Path(folder), "fixture", {
                    "status": "PRODUCTION_READY", "observations": []})


if __name__ == "__main__":
    unittest.main()
