import hashlib
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'mcp_bridge'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from nexus_contract import load_governance, report_filename
from drive_auth_check import check_access


class BootstrapContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.work = self.root / 'WORK'
        self.work.mkdir()
        self.paths = {'agbs': 'WORK/_AGBS.md', 'folder': 'WORK/Folder.md',
                      'manifest': 'manifest.md', 'baseline': 'baseline.md'}
        for key, relative in self.paths.items():
            (self.root / relative).write_text('policy-' + key, encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_reads_work_agbs_not_historical_parent(self):
        (self.root / '_AGBS_old.md').write_text('stale')
        result = load_governance(self.work, self.paths)
        self.assertTrue(result['ready'])
        self.assertEqual(result['policies']['agbs']['text'], 'policy-agbs')
        self.assertEqual(result['policies']['agbs']['sha256'], hashlib.sha256(b'policy-agbs').hexdigest())
        self.assertFalse(result['authority_verified'])

    def test_missing_or_truncated_policy_blocks(self):
        (self.work / '_AGBS.md').unlink()
        self.assertFalse(load_governance(self.work, self.paths)['ready'])
        (self.work / '_AGBS.md').write_bytes(b'x' * 200_001)
        result = load_governance(self.work, self.paths)
        self.assertFalse(result['ready'])
        self.assertNotIn('text', result['policies']['agbs'])

    def test_native_and_outside_paths_fail_closed(self):
        for path in ('../outside.md', 'native.gdoc'):
            result = load_governance(self.work, dict(self.paths, manifest=path))
            self.assertFalse(result['ready'])

    def test_vienna_date_boundary_and_ledger_required(self):
        moment = datetime(2026, 10, 26, 23, 30, tzinfo=timezone.utc)
        self.assertEqual(report_filename('Befund.md', '0123', 'ID-03', moment),
                         '26_10_27_0030_ID03_Befund_0123.md')
        with self.assertRaisesRegex(ValueError, 'LEDGER'):
            report_filename('Befund.md', None, 'ID03')

    def test_legacy_alias_and_non_markdown_rejected(self):
        for name, actor in [('Befund.json', 'ID03'), ('Befund.md', 'ID09')]:
            with self.assertRaises(ValueError):
                report_filename(name, '0123', actor)

    def test_missing_credentials_do_not_call_network(self):
        with patch.dict(os.environ, {}, clear=True), patch('drive_auth_check.get_access_token') as token:
            result = check_access(True)
        self.assertEqual(result['reason'], 'BLOCKED_DRIVE_CREDENTIALS')
        self.assertEqual(len(result['missing_names']), 3)
        token.assert_not_called()

    def test_read_access_is_not_a_write_or_release_receipt(self):
        from drive_auth_check import WORK
        body = json.dumps({'id': WORK, 'mimeType': 'application/vnd.google-apps.folder',
                           'capabilities': {'canAddChildren': True}}).encode()
        with patch.dict(os.environ, {'GOOGLE_ACCESS_TOKEN': 'fixture'}, clear=True), \
             patch('drive_auth_check.get_access_token', return_value='fixture'), \
             patch('drive_auth_check.DriveClient.call', return_value=body):
            result = check_access(True)
        self.assertEqual(result['status'], 'READ_ACCESS_VERIFIED')
        self.assertEqual(result['write_test'], 'NOT_RUN')
        self.assertNotIn('fixture', json.dumps(result))

    def test_readonly_account_does_not_pass_delivery_preflight(self):
        from drive_auth_check import WORK
        body = json.dumps({'id': WORK, 'mimeType': 'application/vnd.google-apps.folder',
                           'capabilities': {'canAddChildren': False}}).encode()
        with patch.dict(os.environ, {'GOOGLE_ACCESS_TOKEN': 'fixture'}, clear=True), \
             patch('drive_auth_check.get_access_token', return_value='fixture'), \
             patch('drive_auth_check.DriveClient.call', return_value=body):
            result = check_access(True)
        self.assertEqual(result['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
