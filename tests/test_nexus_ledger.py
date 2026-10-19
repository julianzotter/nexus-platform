import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from nexus_ledger import Ledger, LedgerError


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.w = Path(self.tmp.name)
        (self.w / 'REPORTS').mkdir(); (self.w / 'REPORTS' / 'r.md').write_text('ergebnis')
        self.id02, self.id03, self.ver = (Ledger(self.w, a) for a in ('ID02', 'ID03', 'SYS-VERIFY'))

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_loop_to_verified(self):
        self.id02.send('WO-1', 'ID03', 'Statik pruefen')
        self.assertEqual([s['work_order_id'] for s in self.id03.inbox()], ['WO-1'])
        self.assertEqual(self.id02.inbox(), [])
        self.id03.ack('WO-1'); self.id03.done('WO-1', 'REPORTS/r.md')
        [r] = self.ver.verify_all()
        self.assertEqual((r['state'], r['human_acceptance']), ('VERIFIED', 'PENDING'))
        self.assertEqual(self.id03.inbox(), [])
        self.assertIn('VERIFIED', (self.w / 'LEDGER' / 'STATUS.md').read_text())
        self.assertEqual(len(list((self.w / 'LEDGER' / 'WO-1').glob('*.json'))), 4)  # one immutable file per event

    def test_guards(self):
        self.id02.send('WO-2', 'ID03', 't')
        with self.assertRaises(LedgerError):
            self.id02.ack('WO-2')            # only receiver
        with self.assertRaises(LedgerError):
            self.id03.done('WO-2', 'REPORTS/r.md')  # skip ACK
        self.id03.ack('WO-2')
        with self.assertRaises(LedgerError):
            self.id03.done('WO-2', '../x')    # path escape
        self.id03.done('WO-2', 'REPORTS/r.md')
        with self.assertRaises(LedgerError):
            self.id02._append('WO-2', 'VERIFIED')  # self-verification
        with self.assertRaises(LedgerError):
            self.ver._append('WO-2', 'APPROVED')   # human release is not a ledger state

    def test_tamper_blocks_and_returns_to_sender(self):
        self.id02.send('WO-3', 'ID03', 't'); self.id03.ack('WO-3'); self.id03.done('WO-3', 'REPORTS/r.md')
        (self.w / 'REPORTS' / 'r.md').write_text('geaendert')
        [r] = self.ver.verify_all()
        self.assertEqual(r['state'], 'BLOCKED')
        self.assertEqual([s['work_order_id'] for s in self.id02.inbox()], ['WO-3'])

    def test_ack_timeout(self):
        self.id02.send('WO-4', 'ID03', 't', ack_minutes=1)
        later = Ledger(self.w, 'SYS-VERIFY', now=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))
        [r] = later.verify_all()
        self.assertEqual(r['state'], 'TIMEOUT')
        self.id03.ack('WO-4')  # late ACK still possible

    def test_no_overwrite_of_events(self):
        ev = self.id02.send('WO-5', 'ID03', 't')
        f = next((self.w / 'LEDGER' / 'WO-5').glob('*.json'))
        self.assertEqual(json.loads(f.read_text())['event_id'], ev['event_id'])
        with self.assertRaises(FileExistsError):
            open(f, 'x')


if __name__ == '__main__':
    unittest.main()
