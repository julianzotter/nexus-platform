"""Synthetic software QA only. Run: python -m unittest discover -s W012_Review -v."""
from __future__ import annotations
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import ezdxf
from jsonschema import Draft202012Validator, FormatChecker, ValidationError
import w012_dxf as drawing

ROOT = Path(__file__).resolve().parent


def fixture() -> dict:
    """Invented dimensions; never a project source or engineering input."""
    provenance = {'source_id': 'SYNTHETIC', 'locator': 'test-only', 'source_status': 'VERIFIED_SOURCE'}
    def entity(identifier: str, **fields: object) -> dict:
        return dict(provenance, id=identifier, **fields)
    return {
        'schema_version': '1.0', 'project': 'SYNTHETIC-NOT-W012', 'revision': 'TEST-1',
        'units': 'm', 'drawing_status': 'REVIEW', 'drawing_selection_confirmed': True,
        'engineering_release': False, 'plan_revision': 'TEST-1', 'coordinate_basis': 'synthetic XY metres',
        'level_id': 'TEST-LEVEL', 'source_register': [{'id': 'SYNTHETIC', 'url': 'urn:w012:test-only', 'revision': 'TEST-1'}],
        'nodes': [entity('N1', xy_m=[0, 0], level_id='TEST-LEVEL'),
                  entity('N2', xy_m=[2, 1], level_id='TEST-LEVEL')],
        'axes': [entity('X0', direction='X', ordinate_m=0), entity('X1', direction='X', ordinate_m=1),
                 entity('Y0', direction='Y', ordinate_m=0), entity('Y2', direction='Y', ordinate_m=2)],
        'members': [entity('M1', start='N1', end='N2')],
        'columns': [entity('C1', node='N1', section_xy_m=[0.2, 0.3], rotation_deg=0)]}


def canonical_hash(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class DrawingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'synthetic.dxf'
        self.data = fixture()

    def generate(self) -> tuple[dict, object]:
        receipt = drawing.generate(self.data, self.target)
        return receipt, ezdxf.readfile(self.target)

    def test_positive_geometry_and_hashes(self) -> None:
        receipt, doc = self.generate()
        self.assertEqual(receipt['status'], 'CAD_AUDIT_AND_GEOMETRY_PASS')
        self.assertFalse(receipt['engineering_release'])
        self.assertEqual(receipt['input_sha256'], canonical_hash(self.data))
        self.assertEqual(receipt['sha256'], hashlib.sha256(self.target.read_bytes()).hexdigest())
        self.assertEqual(receipt, json.loads(self.target.with_suffix('.checks.json').read_text()))
        msp = doc.modelspace()
        self.assertEqual(doc.units, 4)
        line = msp.query('LINE[layer=="TRAEGER"]')[0]
        self.assertEqual(tuple(line.dxf.start), (0.0, 0.0, 0.0))
        self.assertEqual(tuple(line.dxf.end), (2000.0, 1000.0, 0.0))
        column = msp.query('LWPOLYLINE[layer=="STUETZEN"]')[0]
        self.assertTrue(column.closed)
        self.assertEqual(list(column.get_points('xy')), [(-100, -150), (100, -150), (100, 150), (-100, 150)])
        self.assertEqual([d.get_measurement() for d in msp.query('DIMENSION')], [2000, 1000])
        self.assertFalse(doc.audit().has_errors)

    def test_input_gate_negative_cases(self) -> None:
        mutations = {
            'unconfirmed': lambda d: d.update(drawing_selection_confirmed=False),
            'not_review': lambda d: d.update(drawing_status='APPROVED'),
            'wrong_units': lambda d: d.update(units='mm'),
            'wrong_schema': lambda d: d.update(schema_version='2'),
            'bad_revision_type': lambda d: d.update(revision=True),
            'blank_revision': lambda d: d.update(revision=' '),
            'engineering_release': lambda d: d.update(engineering_release=True),
            'missing_plan_revision': lambda d: d.update(plan_revision=None),
            'missing_basis': lambda d: d.update(coordinate_basis=None),
            'missing_level': lambda d: d.update(level_id=None),
            'missing_project': lambda d: d.update(project=''),
            'empty_source_register': lambda d: d.update(source_register=[]),
            'duplicate_source': lambda d: d['source_register'].append(copy.deepcopy(d['source_register'][0])),
            'missing_source_id': lambda d: d['source_register'][0].pop('id'),
            'missing_source_revision': lambda d: d['source_register'][0].pop('revision'),
            'missing_source_url': lambda d: d['source_register'][0].pop('url'),
            'unresolved_source': lambda d: d['nodes'][0].update(source_id='MISSING'),
            'missing_locator': lambda d: d['nodes'][0].pop('locator'),
            'unverified_source': lambda d: d['nodes'][0].update(source_status='UNVERIFIED'),
            'mixed_levels': lambda d: d['nodes'][0].update(level_id='OTHER'),
            'node_without_level': lambda d: d['nodes'][0].pop('level_id'),
            'duplicate_entity': lambda d: d['nodes'][0].update(id='M1'),
            'missing_nodes': lambda d: d.update(nodes=[]),
            'missing_members': lambda d: d.update(members=[]),
            'missing_axes': lambda d: d.update(axes=[]),
            'nan': lambda d: d['nodes'][0].update(xy_m=[float('nan'), 0]),
            'infinity': lambda d: d['nodes'][0].update(xy_m=[float('inf'), 0]),
            'bool_coordinate': lambda d: d['nodes'][0].update(xy_m=[True, 0]),
            'axis_direction': lambda d: d['axes'][0].update(direction='Z'),
            'axis_nonfinite': lambda d: d['axes'][0].update(ordinate_m=float('nan')),
            'unknown_node': lambda d: d['members'][0].update(end='UNKNOWN'),
            'zero_member': lambda d: d['members'][0].update(end='N1'),
            'negative_section': lambda d: d['columns'][0].update(section_xy_m=[-1, 1]),
            'zero_section': lambda d: d['columns'][0].update(section_xy_m=[0, 1]),
            'unknown_column_node': lambda d: d['columns'][0].update(node='UNKNOWN'),
            'rotated_column': lambda d: d['columns'][0].update(rotation_deg=90),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                data = fixture()
                mutate(data)
                with self.assertRaises(ValueError):
                    drawing.generate(data, self.target)
                self.assertFalse(self.target.exists())
                self.assertFalse(self.target.with_suffix('.checks.json').exists())

    def test_unfilled_project_is_blocked(self) -> None:
        data = json.loads((ROOT / 'W012_P2_Modellvertrag.json').read_text())
        with self.assertRaises(ValueError):
            drawing.generate(data, self.target)

    def test_overwrite_drawing(self) -> None:
        self.target.write_bytes(b'EXISTING DXF')
        with self.assertRaises(FileExistsError):
            drawing.generate(self.data, self.target)
        self.assertEqual(self.target.read_bytes(), b'EXISTING DXF')
        self.assertFalse(self.target.with_suffix('.checks.json').exists())

    def test_overwrite_receipt(self) -> None:
        checks = self.target.with_suffix('.checks.json')
        checks.write_bytes(b'EXISTING RECEIPT')
        with self.assertRaises(FileExistsError):
            drawing.generate(self.data, self.target)
        self.assertFalse(self.target.exists())
        self.assertEqual(checks.read_bytes(), b'EXISTING RECEIPT')

    def test_readback_failure_leaves_no_outputs(self) -> None:
        with patch.object(drawing.ezdxf, 'readfile', side_effect=RuntimeError('readback failed')):
            with self.assertRaises(RuntimeError):
                drawing.generate(self.data, self.target)
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_readback_unit_failure_leaves_no_outputs(self) -> None:
        readfile = ezdxf.readfile
        def corrupt(path: Path) -> object:
            doc = readfile(path)
            doc.units = 6
            return doc
        with patch.object(drawing.ezdxf, 'readfile', side_effect=corrupt):
            with self.assertRaises(RuntimeError):
                drawing.generate(self.data, self.target)
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_geometry_failure_leaves_no_outputs(self) -> None:
        with patch.object(drawing, 'check_geometry', side_effect=RuntimeError('geometry failed')):
            with self.assertRaises(RuntimeError):
                drawing.generate(self.data, self.target)
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_receipt_link_failure_rolls_back_drawing(self) -> None:
        link = drawing.os.link
        def fail_receipt(source: Path, destination: Path) -> None:
            if str(destination).endswith('.checks.json'):
                raise OSError('synthetic receipt failure')
            link(source, destination)
        with patch.object(drawing.os, 'link', side_effect=fail_receipt):
            with self.assertRaises(OSError):
                drawing.generate(self.data, self.target)
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_nonfinite_metadata_hash_blocks_publication(self) -> None:
        self.data['extra_metadata'] = float('nan')
        with self.assertRaises(ValueError):
            drawing.generate(self.data, self.target)
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_hash_canonical_and_sensitive_to_revision(self) -> None:
        first, _ = self.generate()
        self.data = dict(reversed(list(self.data.items())))
        self.target = self.target.with_name('reordered.dxf')
        second, _ = self.generate()
        self.assertEqual(first['input_sha256'], second['input_sha256'])
        self.data['revision'] = 'TEST-2'
        self.target = self.target.with_name('changed.dxf')
        third, _ = self.generate()
        self.assertNotEqual(first['input_sha256'], third['input_sha256'])

    def test_geometry_corruption_is_rejected(self) -> None:
        _, doc = self.generate()
        corruptions = {
            'member_coordinate': lambda m: setattr(m.query('LINE[layer=="TRAEGER"]')[0].dxf, 'end', (2001, 1000, 0)),
            'member_z': lambda m: setattr(m.query('LINE[layer=="TRAEGER"]')[0].dxf, 'end', (2000, 1000, 1)),
            'missing_member': lambda m: m.delete_entity(m.query('LINE[layer=="TRAEGER"]')[0]),
            'axis_coordinate': lambda m: setattr(m.query('LINE[layer=="ACHSEN"]')[0].dxf, 'start', (10, 10, 0)),
            'missing_axis': lambda m: m.delete_entity(m.query('LINE[layer=="ACHSEN"]')[0]),
            'column_position': lambda m: m.query('LWPOLYLINE')[0].translate(1, 0, 0),
            'column_shape': lambda m: m.query('LWPOLYLINE')[0].set_points([(-100,-150), (100,-150), (0,150)]),
            'column_open': lambda m: setattr(m.query('LWPOLYLINE')[0], 'closed', False),
            'column_elevation': lambda m: setattr(m.query('LWPOLYLINE')[0].dxf, 'elevation', 1),
            'column_bulge': lambda m: m.query('LWPOLYLINE')[0].set_points([(-100,-150,1), (100,-150,0), (100,150,0), (-100,150,0)], format='xyb'),
            'missing_column': lambda m: m.delete_entity(m.query('LWPOLYLINE')[0]),
            'missing_dimension': lambda m: m.delete_entity(m.query('DIMENSION')[0]),
            'dimension_value': lambda m: setattr(m.query('DIMENSION')[0].dxf, 'defpoint3', (2050, 0, 0)),
        }
        for name, corrupt in corruptions.items():
            with self.subTest(name=name):
                doc = ezdxf.readfile(self.target)
                corrupt(doc.modelspace())
                with self.assertRaises(RuntimeError):
                    drawing.check_geometry(doc, self.data, drawing.validate(self.data))

    def test_schema_validates_fixture_and_rejects_template(self) -> None:
        schema = json.loads((ROOT / 'W012_Drawing.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        validator.validate(self.data)
        template = json.loads((ROOT / 'W012_P2_Modellvertrag.json').read_text())
        with self.assertRaises(ValidationError):
            validator.validate(template)
        for field, value in [('revision', True), ('engineering_release', True), ('units', 'mm')]:
            with self.subTest(field=field):
                data = fixture()
                data[field] = value
                with self.assertRaises(ValidationError):
                    validator.validate(data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
