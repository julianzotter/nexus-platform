"""Actual SDK object shapes plus mocked host failures; never connects RFEM."""
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/rfem'))
from parametric_frame import FrameParameters,contract
from rfem_frame_adapter import objects_for,readback,create_live
try:
    from dlubal.api import rfem
    SDK=True
except ImportError:
    SDK=False

class FakeApp:
    def __init__(self):self.objects=[];self.created=0;self.solve=False
    def __enter__(self):return self
    def __exit__(self,*a):return False
    def get_application_info(self):return SimpleNamespace(version='6.16.0006',full_version='RFEM 6.16.0006')
    def create_model(self,**kw):self.created+=1;return SimpleNamespace(guid='synthetic-guid')
    def create_object_list(self,**kw):self.objects=kw['objs'];assert kw['skip_invalid_attributes'] is False
    def get_object_list(self,**kw):return [o for o in self.objects if o.DESCRIPTOR.name=='Node']
    def get_object(self,**kw):
        q=kw['obj'];return next(o for o in self.objects if o.DESCRIPTOR.name==q.DESCRIPTOR.name and o.no==q.no)
    def calculate_all(self,**kw):assert kw['skip_warnings'] is False;return SimpleNamespace(succeeded=self.solve)
    def save_model(self,**kw):Path(kw['path']).write_bytes(b'SYNTHETIC_TEST_FILE_NOT_RFEM')

@unittest.skipUnless(SDK,'optional SDK profile not installed in this test interpreter')
class SdkContractTests(unittest.TestCase):
    def setUp(self):self.p=FrameParameters(6.,3.,10000.);self.s=contract(self.p)
    def test_object_roundtrip_and_readback(self):
        objs=objects_for(self.p);self.assertEqual(len(objs),17)
        for o in objs:self.assertEqual(type(o).FromString(o.SerializeToString(deterministic=True)),o)
        app=FakeApp();app.objects=objs;readback(app,SimpleNamespace(guid='x'),objs,self.s)
    def test_isolated_create_no_calculation(self):
        app=FakeApp()
        with tempfile.TemporaryDirectory() as d,patch('dlubal.api.rfem.Application',return_value=app):
            out=create_live(self.p,self.s,Path(d),9000,False,self.s['input_sha256'])
            self.assertEqual(app.created,1);self.assertEqual(out['solver'],'NOT_RUN')
    def test_hash_sdk_solver_fail_closed(self):
        app=FakeApp()
        with tempfile.TemporaryDirectory() as d,patch('dlubal.api.rfem.Application',return_value=app):
            with self.assertRaises(ValueError):create_live(self.p,self.s,Path(d),9000,False,'bad')
            self.assertEqual(app.created,0)
            with patch('rfem_frame_adapter.version',return_value='2.12.8'):
                with self.assertRaises(RuntimeError):create_live(self.p,self.s,Path(d),9000,False,self.s['input_sha256'])
            self.assertEqual(app.created,0)
            with self.assertRaises(RuntimeError):create_live(self.p,self.s,Path(d),9000,True,self.s['input_sha256'])
            self.assertEqual(list(Path(d).glob('*.rf6')),[])

if __name__=='__main__':unittest.main()
