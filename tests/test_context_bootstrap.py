import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'mcp_bridge'))
import ctx_router


class ContextBootstrapTests(unittest.TestCase):
    def test_all_mandatory_policies_are_loaded_before_ranking(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);work=root/'WORK';work.mkdir()
            for relative in ('WORK/_AGBS.md','WORK/Folder.md',
                '00_NEXUS_MANIFEST__CURRENT__2026-09-28.md',
                '00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md'):
                (root/relative).write_text('POLICY:' + relative)
            with patch.object(ctx_router,'SSOT_DIR',root):
                text=ctx_router.policy_context()
            self.assertIn('POLICY:WORK/_AGBS.md',text)
            self.assertIn('POLICY:WORK/Folder.md',text)
            self.assertEqual(text.count('[POLICY '),4)

    def test_missing_policy_is_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as td, patch.object(ctx_router,'SSOT_DIR',Path(td)):
            with self.assertRaisesRegex(ValueError,'BOOTSTRAP_BLOCKED'):
                ctx_router.policy_context()

    def test_budget_cannot_clip_mandatory_rules(self):
        with patch.object(ctx_router,'policy_context',return_value='x'*4000):
            for mode,kwargs in [('MVP',{'budget':2}),('FULL',{'full_cap':2})]:
                with self.assertRaisesRegex(ValueError,'MANDATORY_POLICIES_EXCEED_CONTEXT_BUDGET'):
                    ctx_router.build_context('lookup',mode,corpus=[{'text':'fixture'}],**kwargs)


if __name__=='__main__':unittest.main()
