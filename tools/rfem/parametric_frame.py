"""Generate an SI model contract; RFEM live changes are never implicit."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from dataclasses import asdict,dataclass
from typing import Any

@dataclass(frozen=True)
class FrameParameters:
    span_m:float
    height_m:float
    roof_line_load_N_m:float
    material_name:str='S235'
    section_name:str='IPE 300'

    def validate(self)->None:
        for key,value in asdict(self).items():
            if key.endswith(('_m','_N_m')):
                if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
                    raise ValueError('FINITE_NUMERIC_SI_REQUIRED:'+key)
        if not 0<self.span_m<=100 or not 0<self.height_m<=100:
            raise ValueError('GEOMETRY_OUT_OF_PILOT_BOUNDS')
        if not 0<=self.roof_line_load_N_m<=1_000_000:
            raise ValueError('LOAD_OUT_OF_PILOT_BOUNDS')
        if not self.material_name.strip() or not self.section_name.strip():
            raise ValueError('CATALOG_NAMES_REQUIRED')

def contract(p:FrameParameters)->dict[str,Any]:
    p.validate()
    nodes=[{'no':1,'x_m':0.,'y_m':0.,'z_m':0.},
           {'no':2,'x_m':p.span_m,'y_m':0.,'z_m':0.},
           {'no':3,'x_m':0.,'y_m':0.,'z_m':-p.height_m},
           {'no':4,'x_m':p.span_m,'y_m':0.,'z_m':-p.height_m}]
    members=[{'no':1,'nodes':[1,3]},{'no':2,'nodes':[2,4]},{'no':3,'nodes':[3,4]}]
    data={'schema_version':'0.1.0','scope':'SYNTHETIC_PORTAL_FRAME',
          'adapter_version':'0.1.0','sdk_profile':'2.16.6','rfem_profile':'6.16','analysis_type':'GEOMETRICALLY_LINEAR','parameters':asdict(p),'coordinates':'global X horizontal; global Z positive down',
          'nodes':nodes,'members':members,'fixed_support_nodes':[1,2],
          'loads':[{'load_case':1,'member':3,'q_N_m':p.roof_line_load_N_m,'direction':'GLOBAL_Z_TRUE_LENGTH'}],
          'self_weight_active':False,'approval_status':'REVIEW_REQUIRED','rfem_live':'NOT_RUN'}
    payload=json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return {**data,'input_sha256':hashlib.sha256(payload).hexdigest()}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--span-m',type=float,required=True)
    parser.add_argument('--height-m',type=float,required=True)
    parser.add_argument('--roof-line-load-N-m',type=float,required=True)
    args=parser.parse_args()
    print(json.dumps(contract(FrameParameters(args.span_m,args.height_m,args.roof_line_load_N_m)),indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
