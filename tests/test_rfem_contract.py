import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/rfem'))
from parametric_frame import FrameParameters,contract

class FrameContractTests(unittest.TestCase):
    def test_replay_and_load_assignment(self):
        p=FrameParameters(6.,3.,10000.)
        a=contract(p);self.assertEqual(a,contract(p))
        self.assertEqual(len(a['nodes']),4);self.assertEqual(len(a['members']),3)
        self.assertEqual(a['loads'][0]['member'],3)
        self.assertEqual(a['loads'][0]['q_N_m'],10000.)
        self.assertTrue(all(n['z_m']<=0 for n in a['nodes']))
    def test_invalid_values(self):
        for p in [FrameParameters(True,3,1),FrameParameters(0,3,1),FrameParameters(float('nan'),3,1),FrameParameters(6,3,-1)]:
            with self.assertRaises(ValueError):contract(p)
    def test_changed_input_changes_hash(self):
        self.assertNotEqual(contract(FrameParameters(6,3,1))['input_sha256'],contract(FrameParameters(7,3,1))['input_sha256'])

if __name__=='__main__':unittest.main()
