import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tools'))
from export_dashboard import build_snapshot
from integration.contract import graph, validate

REV = 'a'*40
NOW = datetime(2026,10,19,tzinfo=timezone.utc)
ITEM = {'id':'KO-test','kind':'note','title':'<script>untrusted</script>',
        'source_file_id':'0123456789abcdef','version':'1','status':'DRAFT'}

class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'registry/knowledge').mkdir(parents=True)
        (self.root/'registry/file-registry.jsonl').write_text(json.dumps({'id':ITEM['source_file_id']})+'\n')
        self.write_item(ITEM)

    def write_item(self, item):
        (self.root/'registry/knowledge/item.json').write_text(json.dumps(item))

    def snapshot(self, monitor=None):
        return build_snapshot(self.root, REV, monitor, NOW)

    def test_roundtrip_preserves_record_status_and_no_release(self):
        snapshot = self.snapshot()
        self.assertEqual(snapshot['knowledge'][0]['record'],ITEM)
        self.assertEqual(snapshot['knowledge'][0]['health'],'INCOMPLETE')
        result=graph(json.loads(json.dumps(snapshot)))
        self.assertEqual(result['nodes'][0]['id'],ITEM['id'])
        self.assertEqual(result['nodes'][0]['status'],'DRAFT')
        self.assertFalse(result['release_authority'])
        self.assertEqual(result['edges'],[])
        self.assertIsNone(result['monitor'])

    def test_hash_matches_exact_input_bytes(self):
        import hashlib
        for source in self.snapshot()['source']['files']:
            self.assertEqual(source['sha256'],hashlib.sha256((self.root/source['path']).read_bytes()).hexdigest())

    def test_missing_source_stays_broken_without_status_upgrade(self):
        (self.root/'registry/file-registry.jsonl').write_text('')
        result=self.snapshot()['knowledge'][0]
        self.assertEqual(result['health'],'BROKEN')
        self.assertEqual(result['record']['status'],'DRAFT')

    def test_unknown_contract_and_duplicate_ids_rejected(self):
        snapshot=self.snapshot(); snapshot['schema_version']='future/2'
        with self.assertRaises(Exception): validate(snapshot)
        snapshot=self.snapshot(); snapshot['knowledge']*=2
        with self.assertRaises(ValueError): validate(snapshot)

    def test_invalid_record_and_missing_registry_rejected(self):
        self.write_item({**ITEM,'status':'APPROVED'})
        with self.assertRaises(Exception): self.snapshot()
        (self.root/'registry/file-registry.jsonl').unlink()
        with self.assertRaises(OSError): self.snapshot()

    def test_no_data_not_fabricated(self):
        (self.root/'registry/knowledge/item.json').unlink()
        self.assertEqual(self.snapshot()['knowledge'],[])

    def test_monitor_states_preserved_and_revision_mismatch_rejected(self):
        path=self.root/'report.json'
        report={'status':'ATTENTION','observed_at':'2026-10-18T00:00:00Z','commit':REV,
                'run_id':'123','run_attempt':'2','checks':{'registry':{'status':'FAIL','stdout':'not exported'}}}
        path.write_text(json.dumps(report))
        snapshot=self.snapshot(path)
        self.assertEqual(snapshot['monitor']['checks'],{'registry':'FAIL'})
        self.assertEqual(snapshot['monitor']['observed_at'],report['observed_at'])
        self.assertNotEqual(snapshot['generated_at'],report['observed_at'])
        report['commit']='b'*40;path.write_text(json.dumps(report))
        with self.assertRaises(ValueError):self.snapshot(path)

    def test_naive_timestamp_rejected(self):
        snapshot=self.snapshot();snapshot['generated_at']='2026-10-19T00:00:00'
        with self.assertRaises(Exception): validate(snapshot)
