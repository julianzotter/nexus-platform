"""Offline determinism and mocked RFEM API-II mapping tests."""
import unittest
from types import SimpleNamespace
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

    def test_rfem6_mapping_and_write_gate(self):
        record = lambda name: type(name, (), {"__init__": lambda self, **kw: self.__dict__.update(kw)})
        core = SimpleNamespace(**{name: record(name) for name in ("Material", "Section", "Node", "Line", "Member")})
        api = SimpleNamespace(structure_core=core)
        objects = rfem6_objects(self.geometry, api)
        self.assertEqual(len(objects), 3 + 18 + 26 * 2)
        calls = []
        app = SimpleNamespace(create_model=lambda **kw: calls.append(kw),
                              create_object_list=lambda x: calls.append(len(x)))
        with self.assertRaises(ValueError):
            rfem6_new_model(self.geometry, "EXISTING_MODEL", app, api)
        self.assertEqual(calls, [])
        rfem6_new_model(self.geometry, "NEXUS_W012_TEST_001", app, api)
        self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
