import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from delivery_errors import DeliveryError
from registry_append import append_events, cas_write, patch_ledger, run

LEDGER = b'ID,TITLE,DRIVE_ID,SHA256\r\n0210,r,,SEE_REPORT_LOG\r\n0211,l,,\r\n'


class FakeDrive:
    def __init__(self, files):
        self.files = dict(files); self.writes = 0

    def read(self, file_id):
        return self.files[file_id]

    def replace(self, file_id, data, mime_type):
        self.files[file_id] = data; self.writes += 1


def sha(b):
    return hashlib.sha256(b).hexdigest()


class RegistryAppendTests(unittest.TestCase):
    def test_ledger_fill_only_keeps_crlf(self):
        out = patch_ledger(LEDGER, {'0210': {'DRIVE_ID': 'X', 'SHA256': 'abc'}})
        self.assertIn(b'0210,r,X,abc\r\n', out)
        self.assertIn(b'0211,l,,\r\n', out)

    def test_ledger_refuses_overwrite(self):
        data = b'ID,TITLE,DRIVE_ID,SHA256\n0210,r,OLD,\n'
        with self.assertRaises(DeliveryError):
            patch_ledger(data, {'0210': {'DRIVE_ID': 'NEW'}})

    def test_ledger_unknown_id(self):
        with self.assertRaises(DeliveryError):
            patch_ledger(LEDGER, {'9999': {'DRIVE_ID': 'X'}})

    def test_append_is_idempotent(self):
        base = json.dumps({'artifact_id': 'gdrive:a', 'content_sha256': 'h'}).encode() + b'\n'
        events = [{'artifact_id': 'gdrive:a', 'content_sha256': 'h'}, {'artifact_id': 'gdrive:b', 'content_sha256': 'h2'}]
        out, added = append_events(base, events, 'T')
        self.assertEqual(added, ['gdrive:b'])
        self.assertTrue(out.startswith(base))
        again, added2 = append_events(out, events, 'T')
        self.assertEqual((again, added2), (out, []))

    def test_cas_conflict_blocks_write(self):
        drive = FakeDrive({'f': b'live'})
        with self.assertRaises(DeliveryError):
            cas_write(drive, 'f', sha(b'stale'), b'new', 'text/plain')
        self.assertEqual(drive.writes, 0)

    def test_run_resolves_live_hash_after_ledger_patch(self):
        drive = FakeDrive({'L': LEDGER, 'R': b''})
        plan = {'ledger': {'file_id': 'L', 'expected_sha256': sha(LEDGER),
                           'fills': {'0211': {'DRIVE_ID': 'L', 'SHA256': 'SELF'}}},
                'registry': {'file_id': 'R', 'expected_sha256': sha(b''),
                             'events': [{'artifact_id': 'gdrive:L', 'content_sha256': '@SHA_OF:L'}]}}
        result = run(drive, plan, 'T')
        event = json.loads(drive.files['R'])
        self.assertEqual(event['content_sha256'], sha(drive.files['L']))
        self.assertEqual(event['registered_at'], 'T')
        self.assertEqual(result['status'], 'REGISTERED_VERIFIED')

    def test_pending_plan_is_well_formed(self):
        plan = json.loads((Path(__file__).resolve().parents[1] / 'registry/pending/2026-11-16_ID06_registry-append.json').read_text())
        ids = [e['artifact_id'] for e in plan['registry']['events']]
        self.assertEqual(len(ids), len(set(ids)))
        for e in plan['registry']['events']:
            self.assertTrue(e['content_sha256'].startswith('@SHA_OF:') or len(e['content_sha256']) == 64)


if __name__ == '__main__':
    unittest.main()
