"""No-network tests for model-ID binding and geometry comparison."""
import unittest
from types import SimpleNamespace

from rfem6_readback import compare_nodes, compare_member_topology, unique_model_id


class HostReadbackTests(unittest.TestCase):
    def test_unique_model_name_required(self):
        model = SimpleNamespace(name="TEST", guid="id-1")
        common = SimpleNamespace(ModelId=lambda **kw: SimpleNamespace(**kw))
        self.assertEqual(unique_model_id(SimpleNamespace(model_info=[model]), "TEST", common).guid, "id-1")
        with self.assertRaises(ValueError):
            unique_model_id(SimpleNamespace(model_info=[model, model]), "TEST", common)

    def test_coordinate_comparison(self):
        expect = [{"no": 1, "x_m": 1.0, "y_m": 2.0, "z_m": 3.0}]
        observed = [SimpleNamespace(no=1, coordinate_1=1.0, coordinate_2=2.0, coordinate_3=3.0)]
        self.assertEqual(compare_nodes(expect, observed, 1e-6)["status"], "MATCH")
        observed[0].coordinate_3 = 4.0
        self.assertEqual(compare_nodes(expect, observed, 1e-6)["status"], "MISMATCH")

    def test_member_topology(self):
        expected = [{"no": 1, "start": 3, "end": 5}]
        member = [SimpleNamespace(no=1, line=8)]
        line = [SimpleNamespace(no=8, definition_nodes=[3, 5])]
        self.assertEqual(compare_member_topology(expected, member, line)["status"], "MATCH")
        line[0].definition_nodes = [5, 3]
        self.assertEqual(compare_member_topology(expected, member, line)["status"], "MISMATCH")
