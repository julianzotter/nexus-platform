import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'mcp_bridge'))
from nexus_mcp_server import BridgeError, NexusBridge


class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.work = root / 'SSOT' / 'WORK'; (self.work / 'REPORTS').mkdir(parents=True)
        (self.work / 'order.md').write_text('# WO-1', encoding='utf-8')
        (self.work / '.env').write_text('X=1')
        (root / 'SSOT' / 'outside.txt').write_text('no')
        for name in ('_AGBS.md', 'Folder.md'):
            (self.work / name).write_text('fixture policy')
        for name in ('00_NEXUS_MANIFEST__CURRENT__2026-09-28.md', '00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md'):
            (root / 'SSOT' / name).write_text('fixture policy')
        self.repo = root / 'repo'; self.repo.mkdir()
        g = lambda *a: subprocess.run(['git', '-C', str(self.repo), *a], check=True, capture_output=True)
        g('init', '-q'); (self.repo / 'AGENTS.md').write_text('rules')
        g('add', '.'); g('-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-qm', 'init')

    def tearDown(self):
        self.tmp.cleanup()

    def test_read_and_provenance(self):
        b = NexusBridge(self.work, self.repo)
        r = b.read_work_file('order.md')
        self.assertEqual(r['text'], '# WO-1'); self.assertEqual(len(r['sha256']), 64)
        self.assertEqual(b.read_repo_file('AGENTS.md')['text'], 'rules')
        self.assertTrue(any(e['path'] == 'order.md' for e in b.list_work()))

    def test_path_guards(self):
        b = NexusBridge(self.work, self.repo)
        for bad in ('../outside.txt', '/etc/passwd', '.env', ''):
            with self.assertRaises(BridgeError):
                b.read_work_file(bad)
        with self.assertRaises(BridgeError):
            b.read_repo_file('AGENTS.md', ref='--output=/tmp/x')

    def test_write_gate_and_no_overwrite(self):
        with self.assertRaises(BridgeError):
            NexusBridge(self.work, self.repo).submit_result('WO-1', 'r.md', 'x', 'ID-02')
        b = NexusBridge(self.work, self.repo, write_enabled=True)
        meta = b.submit_result('WO-1', 'r.md', 'ergebnis', 'ID-02', artifact_id='0123')
        self.assertEqual((meta['status'], meta['approval']), ('REVIEW', 'PENDING'))
        out = self.work / 'REPORTS' / meta['file']
        self.assertEqual(out.read_text(encoding='utf-8'), 'ergebnis')
        self.assertEqual(json.loads(out.with_name(out.name + '.meta.json').read_text())['sha256'], meta['sha256'])
        with self.assertRaises(BridgeError):
            b.submit_result('WO-1', '../x.md', 'x', 'ID-02')


if __name__ == '__main__':
    unittest.main()
