"""Offline determinism and mocked RFEM API-II mapping tests."""
import unittest
import tempfile
import json
from pathlib import Path
from types import SimpleNamespace
from cli import make_receipt, write_receipt_exclusive
from geometry import FrameSpec, build_geometry
from targets import rfem5_manifest, rfem6_new_model, rfem6_objects

SAMPLE = {
    "project": "W012_EIBENGASSE_HOFTRAKT", "spans_x_m": [3.0, 4.0],
    "spans_y_m": [5.0], "storeys_m": [3.0, 3.0], "material": "TEST_MATERIAL",
    "section_columns": "TEST_COLUMN", "section_beams": "TEST_BEAM",
}


class ParametricTests(unittest.TestCase):
    def setUp(self):
        self.geometry = build_geometry(FrameSpec.from_dict(SAMPLE))

    def test_counts_and_coordinates(self):
        self.assertEqual(len(self.geometry["nodes"]), 18)
        self.assertEqual(len(self.geometry["members"]), 26)
        self.assertEqual(self.geometry["nodes"][-1]["x_m"], 7.0)

    def test_validation(self):
        for key, bad in [("spans_x_m", [0]), ("storeys_m", [float("nan")])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                FrameSpec.from_dict({**SAMPLE, key: bad})

    def test_determinism(self):
        self.assertEqual(self.geometry, build_geometry(FrameSpec.from_dict(SAMPLE)))

    def test_rfem5_is_preview(self):
        self.assertEqual(rfem5_manifest(self.geometry)["mode"], "TRANSFER_PREVIEW_ONLY")

    def test_json_receipt_hash_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            spec = root / "spec.json"
            spec.write_text(json.dumps(SAMPLE), encoding="utf-8")
            receipt = make_receipt(spec, "rfem6")
            report = root / "receipt.json"
            write_receipt_exclusive(report, receipt)
            self.assertEqual(json.loads(report.read_text(encoding="utf-8")), receipt)
            with self.assertRaises(FileExistsError):
                write_receipt_exclusive(report, receipt)

    def test_rfem6_mapping_and_write_gate(self):
        record = lambda name: type(name, (), {"__init__": lambda self, **kw: self.__dict__.update(kw)})
        core = SimpleNamespace(**{name: record(name) for name in ("Material", "CrossSection", "Node", "Line", "Member")})
        api = SimpleNamespace(structure_core=core)
        objects = rfem6_objects(self.geometry, api)
        self.assertEqual(len(objects), 3 + 18 + 26 * 2)
        calls = []
        app = SimpleNamespace(create_model=lambda **kw: calls.append(kw) or "NEW_MODEL_ID",
                              create_object_list=lambda **kw: calls.append(kw))
        with self.assertRaises(ValueError):
            rfem6_new_model(self.geometry, "EXISTING_MODEL", app, api, allow_new_model=True)
        self.assertEqual(calls, [])
        with self.assertRaises(PermissionError):
            rfem6_new_model(self.geometry, "NEXUS_W012_TEST_001", app, api)
        with self.assertRaises(NotImplementedError):
            rfem6_new_model(self.geometry, "NEXUS_W012_TEST_001", app, api, allow_new_model=True)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
