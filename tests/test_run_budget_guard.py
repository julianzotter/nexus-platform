import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / 'tools' / 'run_budget_guard.py'
SPEC = importlib.util.spec_from_file_location('run_budget_guard', PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BudgetGuardTests(unittest.TestCase):
    def setUp(self):
        self.request = b'fixture: full provider request'
        self.receipt = dict(provider='fixture', model_id='fixture-model',
            tokenizer_or_count_api='fixture-counter', measurement_ref='fixture:1',
            measurement_kind='EXACT_FULL_REQUEST',
            request_sha256=hashlib.sha256(self.request).hexdigest(),
            context_limit=100, input_tokens=70, output_reserve=15,
            tool_reserve=10, safety_margin=5)

    def check(self, **changes):
        return MODULE.assess(self.request, dict(self.receipt, **changes))

    def test_exact_boundary(self):
        r = self.check()
        self.assertEqual(r['status'], 'PASS_BUDGET_ARITHMETIC')
        self.assertEqual(r['remaining_tokens'], 0)
        self.assertEqual(r['measurement_authenticity'], 'NOT_VERIFIED_BY_GUARD')

    def test_one_token_over(self):
        self.assertIn('CONTEXT_BUDGET_EXCEEDED', self.check(input_tokens=71)['reasons'])

    def test_estimate(self):
        self.assertEqual(self.check(measurement_kind='ESTIMATED')['status'], 'BLOCKED')

    def test_hash_mismatch(self):
        self.assertEqual(self.check(request_sha256='0'*64)['status'], 'BLOCKED')

    def test_missing_model(self):
        self.assertEqual(self.check(model_id=None)['status'], 'BLOCKED')

    def test_bool_not_int(self):
        self.assertEqual(self.check(input_tokens=True)['status'], 'BLOCKED')

    def test_negative_count(self):
        self.assertEqual(self.check(tool_reserve=-1)['status'], 'BLOCKED')

    def test_missing_limit(self):
        self.assertEqual(self.check(context_limit=None)['status'], 'BLOCKED')

    def test_no_output_reserve(self):
        self.assertEqual(self.check(output_reserve=0)['status'], 'BLOCKED')

    def test_reserve_exceeds_cap(self):
        self.assertEqual(self.check(output_reserve=120)['status'], 'BLOCKED')

    def test_empty_request(self):
        receipt = dict(self.receipt, request_sha256=hashlib.sha256(b'').hexdigest())
        self.assertEqual(MODULE.assess(b'', receipt)['status'], 'BLOCKED')

    def test_zero_input_count(self):
        self.assertEqual(self.check(input_tokens=0)['status'], 'BLOCKED')

    def test_duplicate_receipt_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory); (p/'request').write_bytes(self.request)
            raw=json.dumps(self.receipt)[:-1]+', "input_tokens": 70}'
            (p/'receipt').write_text(raw, encoding='utf-8')
            command=[sys.executable,str(PATH),'--request',str(p/'request'),
                     '--receipt',str(p/'receipt')]
            result=subprocess.run(command,capture_output=True,text=True,check=False)
            self.assertEqual(result.returncode,2)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory); (p/'request').write_bytes(self.request)
            (p/'receipt').write_text(json.dumps(self.receipt), encoding='utf-8')
            command=[sys.executable,str(PATH),'--request',str(p/'request'),
                     '--receipt',str(p/'receipt')]
            result=subprocess.run(command,capture_output=True,text=True,check=False)
            self.assertEqual(result.returncode,0)
            (p/'receipt').write_text('[]',encoding='utf-8')
            result=subprocess.run(command,capture_output=True,text=True,check=False)
            self.assertEqual(result.returncode,2)


if __name__ == '__main__':
    unittest.main()
