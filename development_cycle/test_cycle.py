import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from development_cycle.cycle import append_run, replay, execute_cycle, freeze_review

class CycleTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.folder.cleanup)
        self.root=Path(self.folder.name)
        self.db=self.root/'runs.sqlite'
    def test_delta_replay_and_lookback(self):
        for output in ({'answer':1,'old':True},{'answer':2},{'answer':3,'new':[1,2]}):
            result=append_run(self.db,'task',output,{'acceptance':True},'baseline',[])
        self.assertEqual(replay(self.db,'task',3),{'answer':3,'new':[1,2]})
        self.assertEqual(result['compared_to'],[2,1])
        self.assertEqual(result['run_number'],3)
        with sqlite3.connect(self.db) as connection:
            rows=connection.execute('select checkpoint_json from cycle_runs order by run_number').fetchall()
        self.assertIsNotNone(rows[0][0]);self.assertIsNone(rows[1][0])
    def test_bounded_improvement(self):
        candidates=[({'answer':1},{'correct':False}),({'answer':2},{'correct':True})]
        result=execute_cycle(self.db,'task',candidates,'baseline',max_runs=3)
        self.assertEqual(result['termination'],'ACCEPTANCE_MET')
        self.assertEqual(result['run_number'],2)
    def test_plateau_delivers_partial(self):
        candidate=({'answer':1},{'correct':False})
        result=execute_cycle(self.db,'task',[candidate,candidate,candidate],'baseline',max_runs=3)
        self.assertEqual(result['termination'],'PLATEAU_PARTIAL_DELIVERY')
        self.assertEqual(result['run_number'],3)
    def test_undefined_metrics(self):
        result=append_run(self.db,'task',{}, {},'baseline',['missing source'])
        self.assertIsNone(result['acceptance_pass_rate'])
        self.assertIsNone(result['confidence'])
        self.assertFalse(result['acceptance_met'])
    def test_baseline_change(self):
        append_run(self.db,'task',{}, {'pass':True},'v1',[])
        result=append_run(self.db,'task',{}, {'pass':True},'v2',[])
        self.assertTrue(result['baseline_changed'])
    def test_corruption_detected(self):
        append_run(self.db,'task',{'answer':1},{'pass':True},'baseline',[])
        with sqlite3.connect(self.db) as connection:
            connection.execute("update cycle_runs set delta_json='{}'")
        with self.assertRaisesRegex(ValueError,'integrity'):replay(self.db,'task',1)
    def test_review_freeze(self):
        (self.root/'contract.md').write_text('contract')
        result=freeze_review(self.root,['contract.md'])
        self.assertEqual(len(result['bundle_sha256']),64)
        self.assertEqual(result['reviews']['claude']['status'],'NOT_RUN')
        with self.assertRaises(ValueError):freeze_review(self.root,['../escape'])
    def test_invalid_evaluation(self):
        with self.assertRaises(ValueError):append_run(self.db,'task',{}, {'pass':1},'b',[])
        with self.assertRaises(ValueError):execute_cycle(self.db,'task',[],'b',max_runs=0)

if __name__=='__main__':unittest.main()
