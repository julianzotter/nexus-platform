import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from knowledge_health import assess_item, build_report, exit_code

NOW = datetime(2026, 10, 18, tzinfo=timezone.utc)
FID = '0123456789abcdef'


def item(**kw):
    base = {'id': 'k', 'kind': 'note', 'title': 'fixture', 'version': '1.0',
            'status': 'VALID', 'source_file_id': FID, 'engineering_result': True,
            'norm': {'standard': 'TEST ONLY', 'edition': '1', 'clause': 'fixture'},
            'signoff': {'reviewer': 'TEST FIXTURE, NOT HUMAN APPROVAL', 'decision': 'APPROVED',
                        'result_version': '1.0', 'decided_at': '2026-10-01T00:00:00Z'}}
    base.update(kw)
    return base


class HealthTests(unittest.TestCase):
    def assess(self, data, ids=None):
        return assess_item(data, {FID} if ids is None else ids, NOW, 180)['state']

    def test_schema_valid_approved_fixture(self):
        self.assertEqual(self.assess(item()), 'OK')

    def test_rejected_valid_is_broken(self):
        data = item(); data['signoff']['decision'] = 'REJECTED'
        self.assertEqual(self.assess(data), 'BROKEN')

    def test_draft_without_signoff_is_incomplete(self):
        data = item(status='DRAFT'); del data['signoff']
        self.assertEqual(self.assess(data), 'INCOMPLETE')

    def test_valid_without_signoff_is_broken(self):
        data = item(); del data['signoff']
        self.assertEqual(self.assess(data), 'BROKEN')

    def test_missing_reviewer_is_broken(self):
        data = item(); del data['signoff']['reviewer']
        self.assertEqual(self.assess(data), 'BROKEN')

    def test_broken_source_is_not_downgraded_by_stale_signoff(self):
        data = item(); data['signoff']['result_version'] = '0.9'
        self.assertEqual(self.assess(data, set()), 'BROKEN')

    def test_stale_version(self):
        data = item(); data['signoff']['result_version'] = '0.9'
        self.assertEqual(self.assess(data), 'STALE')

    def test_stale_age(self):
        data = item(); data['signoff']['decided_at'] = '2025-01-01T00:00:00Z'
        self.assertEqual(self.assess(data), 'STALE')

    def test_future_naive_and_invalid_dates(self):
        for value in ['2027-01-01T00:00:00Z', '2026-10-01T00:00:00', 'garbage']:
            with self.subTest(value=value):
                data = item(); data['signoff']['decided_at'] = value
                self.assertEqual(self.assess(data), 'BROKEN')

    def test_unapproved_identity_extension_is_not_human_authentication(self):
        data = item(); data['signoff']['approver_type'] = 'human'
        self.assertEqual(self.assess(data), 'BROKEN')

    def test_non_engineering_broken_source_still_checked(self):
        data = item(engineering_result=False, status='DRAFT'); del data['signoff']
        self.assertEqual(self.assess(data, set()), 'BROKEN')

    def test_non_object(self):
        self.assertEqual(self.assess([]), 'BROKEN')

    def test_no_data_is_explicit_and_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); registry = root / 'files.jsonl'; registry.write_text('')
            report = build_report(root / 'missing', registry, root / 'coverage.json', NOW, 180)
            self.assertEqual(report['status'], 'NO_DATA')
            self.assertEqual(exit_code(report), 2)
            self.assertEqual(exit_code(report, allow_empty=True), 0)
            self.assertEqual(exit_code(report, allow_empty=True, strict=True), 2)

    def test_malformed_registry_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); registry = root / 'files.jsonl'; registry.write_text('{bad')
            report = build_report(root, registry, root / 'coverage.json', NOW, 180)
            self.assertEqual(report['status'], 'FAIL')
            self.assertEqual(exit_code(report, allow_empty=True), 1)

    def test_missing_registry_is_not_no_data_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = build_report(root, root / 'missing', root / 'missing', NOW, 180)
            self.assertEqual(report['status'], 'FAIL')

    def test_strict_rejects_incomplete(self):
        self.assertEqual(exit_code({'status': 'INCOMPLETE'}), 0)
        self.assertEqual(exit_code({'status': 'INCOMPLETE'}, strict=True), 2)
