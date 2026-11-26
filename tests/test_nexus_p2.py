"""Decision and receipt tests. Fixtures are passed in process only."""
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import nexus_p2 as p2

class DecisionTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "approved.json"
        self.base.write_bytes(json.dumps({"branch":"main", "repository":p2.REPO, "github_commit":"f"*40,
                                         "max_age_seconds":300}).encode())
        self.pin = p2.sha(self.base.read_bytes())
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.until = (self.now + timedelta(seconds=100)).isoformat()
        self.actions = {"deliveries":[{"file_id":"example"}], "valid_until":self.until}
        self.gates = {key:{"status":"PASS"} for key in p2.EVIDENCE_GATES}
        self.gates["SNAPSHOT"]["valid_until"] = self.until

    def evaluate(self):
        def evidence(doc, directory, now, *, deliveries):
            self.assertEqual(deliveries,self.actions["deliveries"])
            return self.gates
        return p2.decide(str(self.base), self.pin, self.root, self.now,
                         lambda doc,now: self.actions, evidence)

    def test_each_required_gate_blocks_individually(self):
        for gate in p2.EVIDENCE_GATES:
            with self.subTest(gate=gate):
                self.gates[gate]["status"]="BLOCKED"
                self.assertEqual(p2.finish(self.evaluate(),self.now),2)
                self.gates[gate]["status"]="PASS"

    def test_success_requires_evidence_and_emits_verifiable_report(self):
        report=self.evaluate()
        self.assertEqual(p2.finish(report,self.now),0)
        self.assertEqual(report["decision"],"SYNC_VERIFIED")
        self.assertEqual(report["production_release"],"NOT_GRANTED")
        p2.save_report(report,self.root)
        for line in (self.root/"SHA256SUMS").read_text().splitlines():
            digest,name=line.split("  ")
            self.assertEqual(digest,hashlib.sha256((self.root/name).read_bytes()).hexdigest())
        body=json.loads((self.root/"status.json").read_bytes())
        self.assertEqual(body["payload_sha256"],p2.sha(p2.canonical(report)))
        with self.assertRaises(FileExistsError):
            p2.save_report(report,self.root)

    def test_expiry_at_end_blocks_approved_evidence(self):
        self.assertEqual(p2.finish(self.evaluate(),self.now+timedelta(seconds=100)),2)
        self.gates["SNAPSHOT"].pop("valid_until")
        self.assertEqual(p2.finish(self.evaluate(),self.now),2)

    def test_changed_missing_or_duplicate_baseline_never_contacts_sources(self):
        self.base.write_bytes(self.base.read_bytes()+b' ')
        for path,pin in ((str(self.base),self.pin),(None,None)):
            result=p2.decide(path,pin,self.root,self.now,None,None)
            self.assertEqual(p2.finish(result,self.now),2)
            self.assertEqual(result["gates"]["BASELINE"]["status"],"BLOCKED")
        self.base.write_bytes(b'{"branch":"main","branch":"other"}')
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            p2.read_baseline(self.base,p2.sha(self.base.read_bytes()))

    def test_missing_gate_or_absent_delivery_receipts_fail_closed(self):
        del self.gates["PANEL"]
        self.assertEqual(p2.finish(self.evaluate(),self.now),2)
        self.actions["deliveries"]=[]
        self.assertEqual(self.evaluate()["gates"]["ACTIONS_DELIVERY"]["status"],"BLOCKED")
