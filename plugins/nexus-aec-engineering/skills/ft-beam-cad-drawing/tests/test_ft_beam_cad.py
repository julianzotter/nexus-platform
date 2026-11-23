import json
import tempfile
import unittest
from pathlib import Path

import ezdxf

from scripts.ft_beam_cad import make_dxf, validate_spec


FIXTURE = {
    "beam_id": "TEST-FT-01",
    "drawing_level": "SCHEMATIC",
    "outline_mm": [[0, 0], [8000, 0], [8000, 800], [0, 800]],
    "corbels": [],
    "openings": [{"id": "DB1", "station_mm": 3000, "width_mm": 450, "height_mm": 150, "bottom_mm": 310}],
    "rebar": [
        {"id": "R1", "position_id": "P1", "designation_raw": "4d10", "geometry_status": "RAW_ONLY", "label_anchor_mm": [2700, 1050]},
        {"id": "R2", "position_id": "P2", "designation_raw": "2d10/20", "geometry_status": "RAW_ONLY", "label_anchor_mm": [2700, 1150]},
    ],
    "provenance": {"source_id": "SYNTHETIC_TEST", "source_sha256": "0" * 64},
    "qa": {"status": "PENDING"},
}


class TestFtBeamCad(unittest.TestCase):
    def test_schematic_valid(self):
        validate_spec(FIXTURE)

    def test_rebar_detail_fails_without_verified_geometry(self):
        x = dict(FIXTURE)
        x["drawing_level"] = "REBAR_DETAIL"
        with self.assertRaises(ValueError):
            validate_spec(x)

    def test_dxf_roundtrip_layers_and_opening(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "x.dxf"
            make_dxf(FIXTURE, out)
            doc = ezdxf.readfile(out)
            layers = {x.dxf.name for x in doc.layers}
            self.assertIn("FT_SCHALUNG", layers)
            self.assertIn("FT_DURCHBRUCH", layers)
            self.assertGreaterEqual(len(list(doc.modelspace().query("LWPOLYLINE"))), 2)


if __name__ == "__main__":
    unittest.main()
