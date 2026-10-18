import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from monitor_llm import AdvisoryError, analyze, safe_summary

REPORT = {'status': 'INCOMPLETE', 'commit': 'a' * 40,
          'checks': {'knowledge': {'status': 'NO_DATA', 'stdout': 'NEVER SEND PRIVATE DATA'}}}


def response(data=None, status='completed'):
    data = data or {'summary': 'Unvollständig', 'next_actions': ['Quelle prüfen'], 'limitations': ['Keine Abnahme']}
    return {'id': 'resp_fixture', 'model': 'fixture', 'status': status,
            'output': [{'content': [{'type': 'output_text', 'text': json.dumps(data)}]}]}


class AdvisoryTests(unittest.TestCase):
    def test_only_allowlisted_metadata_leaves_runtime(self):
        self.assertNotIn('NEVER SEND', json.dumps(safe_summary(REPORT)))

    def test_missing_key_no_request(self):
        transport = Mock()
        self.assertEqual(analyze(REPORT, '', transport=transport)['state'], 'BLOCKED_API_KEY_NOT_CONFIGURED')
        transport.assert_not_called()

    def test_pass_does_not_spend_tokens(self):
        transport = Mock()
        self.assertEqual(analyze({**REPORT, 'status': 'PASS'}, 'fixture', transport=transport)['state'], 'SKIPPED_NO_FINDINGS')
        transport.assert_not_called()

    def test_valid_output_remains_advisory_and_not_approved(self):
        transport = Mock(return_value=response())
        result = analyze(REPORT, 'TEST_SECRET_NEVER_PRINT', transport=transport)
        self.assertTrue(result['advisory_only']); self.assertEqual(result['human_acceptance'], 'PENDING')
        payload = transport.call_args.args[0]
        self.assertFalse(payload['store']); self.assertEqual(payload['max_output_tokens'], 700)
        self.assertNotIn('TEST_SECRET', json.dumps(payload))

    def test_incomplete_response_not_success(self):
        with self.assertRaisesRegex(AdvisoryError, 'NOT_COMPLETED'):
            analyze(REPORT, 'fixture', transport=Mock(return_value=response(status='incomplete')))

    def test_schema_and_action_limits(self):
        bad = {'summary': 'x', 'next_actions': ['x'] * 4, 'limitations': []}
        with self.assertRaisesRegex(AdvisoryError, 'ACTION_LIMIT'):
            analyze(REPORT, 'fixture', transport=Mock(return_value=response(bad)))

    def test_refusal_not_success(self):
        with self.assertRaisesRegex(AdvisoryError, 'REFUSAL'):
            analyze(REPORT, 'fixture', transport=Mock(return_value={'status': 'completed', 'output': []}))


class ExportConsentTests(unittest.TestCase):
    def test_missing_export_approval_prevents_analysis_even_with_key(self):
        import tempfile
        import os
        from unittest.mock import patch
        from monitor_llm import main
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'advisory.json'
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'FIXTURE'}, clear=True), patch('sys.argv', ['monitor_llm', '--output', str(output)]), patch('monitor_llm.analyze') as call, patch('builtins.print'):
                self.assertEqual(main(), 0)
            call.assert_not_called()
            self.assertEqual(json.loads(output.read_text())['state'], 'BLOCKED_INTERNAL_DATA_EXPORT_APPROVAL')
