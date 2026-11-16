import csv
import hashlib
import io
import json
import sys
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from delivery_errors import DeliveryError
from drive_conditional import ConditionalDrive, Snapshot, append_events, strong_etag, registered_revision
from repair_control_registers import LEDGER_ID, LEDGER_NOTE, patch_ledger


class FakeCAS(ConditionalDrive):
    def __init__(self):
        self.client = self
        self.probe_receipt = None
        self.probe_journal = None
        self.files = {"registry": b'{"historic":true}\n'}
        self.versions = {"registry": 1}
        self.guard = threading.Lock()
        self.ignore_match = False
        self.timeout_after_commit = False
        self.force_conflict = False
        self.writes = 0

    def generate_id(self):
        return "probe"

    def create(self, identity, folder, key, name, data):
        self.files[identity] = data
        self.versions[identity] = 1

    def read(self, identity):
        return self.files[identity]

    def etag(self, identity):
        return '"' + str(self.versions[identity]) + '"'

    def put(self, identity, data, mime, etag):
        with self.guard:
            if self.force_conflict or (not self.ignore_match and etag != self.etag(identity)):
                raise DeliveryError("HTTP_412")
            self.files[identity] = data
            self.versions[identity] += 1
            self.writes += 1
            if self.timeout_after_commit:
                raise DeliveryError("CONDITIONAL_REQUEST_OUTCOME_UNKNOWN")


class ConditionalTests(unittest.TestCase):
    def test_no_canonical_write_without_live_probe(self):
        client = FakeCAS()
        before = client.files["registry"]
        with self.assertRaisesRegex(DeliveryError, "CAS_PROBE_REQUIRED"):
            client.replace_conditional("registry", client.snapshot("registry"), b"x", "text/plain")
        self.assertEqual(client.files["registry"], before)
        self.assertEqual(client.writes, 0)

    def test_probe_rejects_stale_and_serializes_same_etag(self):
        client = FakeCAS()
        receipt = client.probe("work")
        self.assertEqual(sorted(receipt["outcomes"]), ["COMMITTED", "HTTP_412"])
        self.assertEqual(client.files["registry"], b'{"historic":true}\n')

    def test_ignored_if_match_blocks_canonical_write(self):
        client = FakeCAS()
        client.ignore_match = True
        with self.assertRaisesRegex(DeliveryError, "IF_MATCH_NOT_ENFORCED"):
            client.probe("work")
        self.assertEqual(client.probe_receipt["status"], "CAS_PROBE_FAILED")
        self.assertEqual(client.probe_receipt["file_id"], "probe")
        self.assertEqual(client.files["registry"], b'{"historic":true}\n')

    def test_append_preserves_history_and_is_idempotent(self):
        client = FakeCAS()
        client.probe("work")
        event = {"operation_id": "one", "artifact_id": "gdrive:a", "registered_at": "first"}
        old = client.files["registry"]
        self.assertEqual(append_events(client, "registry", [event])["inserted"], 1)
        after = client.files["registry"]
        self.assertTrue(after.startswith(old))
        event["registered_at"] = "later"
        self.assertEqual(append_events(client, "registry", [event])["inserted"], 0)
        self.assertEqual(client.files["registry"], after)

    def test_same_operation_with_different_content_conflicts(self):
        client = FakeCAS()
        client.probe("work")
        append_events(client, "registry", [{"operation_id": "one", "value": 1}])
        with self.assertRaisesRegex(DeliveryError, "OPERATION_CONFLICT"):
            append_events(client, "registry", [{"operation_id": "one", "value": 2}])

    def test_provider_conflict_never_overwrites(self):
        client = FakeCAS()
        client.probe("work")
        before = client.files["registry"]
        client.force_conflict = True
        with self.assertRaisesRegex(DeliveryError, "SOURCE_CONFLICT"):
            append_events(client, "registry", [{"operation_id": "one"}])
        self.assertEqual(client.files["registry"], before)

    def test_lost_response_after_commit_is_reconciled(self):
        client = FakeCAS()
        client.probe("work")
        client.timeout_after_commit = True
        before = client.writes
        append_events(client, "registry", [{"operation_id": "one"}])
        self.assertEqual(client.writes, before + 1)

    def test_weak_wildcard_and_injected_etags_rejected(self):
        for etag in (None, "*", 'W/"x"', '"x"\r\nIf-Match: *'):
            with self.assertRaises(DeliveryError):
                strong_etag(etag)

    def test_equivalent_registration_from_another_writer_is_reused(self):
        from tempfile import TemporaryDirectory
        from test_persistence_gate import Drive
        from deliver_work import deliver, WORK
        from persistence_gate import REGISTRY_ID, register_delivery
        with TemporaryDirectory() as directory:
            drive = Drive()
            receipt = deliver(drive, b"fixture", WORK, "source", "fixture.zip", Path(directory) / "journal.json")
            register_delivery(drive, receipt, b"fixture", "fixture.zip", "application/octet-stream", "WO", "ID02", "exclusive-writer")
            event = json.loads(drive.registry)
            event["operation_id"] = "another-writer-operation"
            event["owner"] = "ID06"
            drive.registry = json.dumps(event).encode() + b"\n"
            client = ConditionalDrive(drive)
            client.probe_receipt = {"status": "CAS_PROBE_PASS"}
            with patch.object(client, "snapshot", return_value=Snapshot(drive.registry, '"1"')), patch.object(client, "replace_conditional") as replace:
                result = register_delivery(client, receipt, b"fixture", "fixture.zip", "application/octet-stream", "WO", "ID02", "conditional-cas")
            replace.assert_not_called()
            self.assertEqual(result["registration_status"], "REGISTERED")

    def test_invalid_registration_cannot_suppress_good_revision(self):
        event = {"artifact_id": "gdrive:a", "provider_file_id": "a", "name": "a.md",
                 "canonical_uri": "https://drive.google.com/file/d/a/view", "version": "time",
                 "provider_version": "1", "content_sha256": "a" * 64, "sha256_scope": "complete_raw_file_bytes",
                 "provenance": {}, "verification_status": "BYTE_READBACK_VERIFIED_REVIEW_PENDING",
                 "registration_status": "REGISTERED", "registered_at": "2026-11-16T22:00:00+00:00",
                 "owner": "ID02", "ticket_id": "WO"}
        self.assertTrue(registered_revision(event, event))
        for key, wrong in (("provider_file_id", "wrong"), ("canonical_uri", "wrong"), ("name", "wrong"), ("registered_at", None)):
            self.assertFalse(registered_revision(dict(event, **{key: wrong}), event))

    def test_permanent_oauth_failures_are_blocked(self):
        from deliver_work import failure_status
        self.assertEqual(failure_status("OAUTH_HTTP_400_INVALID_GRANT"), "BLOCKED")


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.raw = b"ID,DRIVE_ID,SHA256,NOTE,TITLE\r\n0200,old,keep,historical,old\r\n0210,,SEE_REPORT_LOG,report,report.md\r\n0211,,,ledger,ledger.csv\r\n"
        self.original = hashlib.sha256(self.raw).hexdigest()
        self.report = {"file_id": "report-id", "sha256": "a" * 64}

    def apply(self, raw=None):
        with patch("repair_control_registers.ORIGINAL_LEDGER_SHA", self.original):
            return patch_ledger(self.raw if raw is None else raw, self.report)

    def test_patch_only_two_records_and_preserve_fields(self):
        patched, changed = self.apply()
        self.assertTrue(changed)
        rows = list(csv.DictReader(io.StringIO(patched.decode())))
        self.assertEqual(rows[0], list(csv.DictReader(io.StringIO(self.raw.decode())))[0])
        self.assertEqual(rows[1]["DRIVE_ID"], "report-id")
        self.assertEqual(rows[1]["SHA256"], "a" * 64)
        self.assertEqual(rows[2]["DRIVE_ID"], LEDGER_ID)
        self.assertEqual(rows[2]["SHA256"], self.original)
        self.assertIn(LEDGER_NOTE, rows[2]["NOTE"])
        self.assertEqual(self.apply(patched), (patched, False))

    def test_changed_source_is_not_silently_rewritten(self):
        with self.assertRaisesRegex(DeliveryError, "SOURCE_CONFLICT"):
            self.apply(self.raw.replace(b"historical", b"changed"))

    def test_existing_conflicting_identity_is_not_replaced(self):
        with self.assertRaisesRegex(DeliveryError, "VALUE_CONFLICT"):
            self.apply(self.raw.replace(b"0210,,", b"0210,someone-else,"))

    def test_duplicate_ids_rejected(self):
        with self.assertRaisesRegex(DeliveryError, "DUPLICATE"):
            self.apply(self.raw + b"0210,other,hash,note,title\r\n")


if __name__ == "__main__":
    unittest.main()
