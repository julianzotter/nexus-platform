"""Isolated RFEM 6.16 / SDK 2.16.6 pilot; dry-run is the default."""
from __future__ import annotations
import argparse
import json
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4
from parametric_frame import FrameParameters,contract

def objects_for(p:FrameParameters)->list:
    from dlubal.api import common,rfem
    spec=contract(p);core=rfem.structure_core;load=rfem.loads.MemberLoad
    fixed=float('inf')
    objects=[core.Material(no=1,name=p.material_name),
             core.CrossSection(no=1,material=1,name=p.section_name)]
    objects += [core.Node(no=n['no'],coordinate_1=n['x_m'],coordinate_2=n['y_m'],coordinate_3=n['z_m']) for n in spec['nodes']]
    for m in spec['members']:
        objects += [core.Line(no=m['no'],definition_nodes=m['nodes']),
                    core.Member(no=m['no'],line=m['no'],cross_section_start=1,type=core.Member.TYPE_BEAM)]
    for n in (1,2):
        objects.append(rfem.types_for_nodes.NodalSupport(no=n,nodes=[n],
            spring=common.Vector3d(x=fixed,y=fixed,z=fixed),
            rotational_restraint=common.Vector3d(x=fixed,y=fixed,z=fixed)))
    objects += [rfem.loading.StaticAnalysisSettings(no=1,analysis_type=rfem.loading.StaticAnalysisSettings.ANALYSIS_TYPE_GEOMETRICALLY_LINEAR),
                rfem.loading.LoadCase(no=1,name='SYNTHETIC_ROOF_LOAD',static_analysis_settings=1,self_weight_active=False),
                load(no=1,members=[3],load_case=1,load_is_over_total_length=True,
                    load_type=load.LOAD_TYPE_FORCE,load_distribution=load.LOAD_DISTRIBUTION_UNIFORM,
                    load_direction=load.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH,
                    magnitude=p.roof_line_load_N_m)]
    return objects

def readback(app,model,objects:list,spec:dict)->None:
    from dlubal.api import rfem
    nodes=app.get_object_list(objs=[rfem.structure_core.Node()],model_id=model)
    actual={n.no:(n.coordinate_1,n.coordinate_2,n.coordinate_3) for n in nodes}
    expected={n['no']:(n['x_m'],n['y_m'],n['z_m']) for n in spec['nodes']}
    if actual!=expected:raise RuntimeError('NODE_READBACK_MISMATCH')
    fields={'Material':('name',),'CrossSection':('name','material'),'StaticAnalysisSettings':('analysis_type',),'Line':('definition_nodes',),'Member':('line','type','cross_section_start'),
            'NodalSupport':('nodes','spring','rotational_restraint'),
            'LoadCase':('static_analysis_settings','self_weight_active'),
            'MemberLoad':('members','load_case','load_type','load_distribution','load_direction','magnitude','load_is_over_total_length')}
    for expected_object in objects:
        names=fields.get(expected_object.DESCRIPTOR.name)
        if not names:continue
        locator=type(expected_object)(no=expected_object.no)
        if expected_object.DESCRIPTOR.name=='MemberLoad':locator.load_case=1
        actual_object=app.get_object(obj=locator,model_id=model)
        if any(getattr(actual_object,k)!=getattr(expected_object,k) for k in names):
            raise RuntimeError('OBJECT_READBACK_MISMATCH:'+expected_object.DESCRIPTOR.name)

def create_live(p:FrameParameters,spec:dict,out:Path,port:int,calculate:bool,approved_input_sha:str)->dict:
    import re
    if approved_input_sha!=contract(p)['input_sha256'] or spec!=contract(p):
        raise ValueError('HUMAN_INPUT_HASH_ATTESTATION_REQUIRED')
    from dlubal.api import rfem
    if version('dlubal.api')!='2.16.6':raise RuntimeError('SDK_PROFILE_MISMATCH_EXPECT_2_16_6')
    name='NEXUS_PILOT_'+spec['input_sha256'][:10]+'_'+uuid4().hex[:10]
    target=out.resolve()/(name+'.rf6')
    if target.exists():raise RuntimeError('TARGET_EXISTS')
    objects=objects_for(p)
    with rfem.Application(url='127.0.0.1',port=port) as app:
        info=app.get_application_info()
        if not re.search(r'(?<!\d)6\.16(?=\D|$)',str(info.version)+' '+str(info.full_version)):
            raise RuntimeError('RFEM_BUILD_PROFILE_MISMATCH_EXPECT_6_16')
        model=app.create_model(name=name)
        # Partial writes are preserved in the isolated model for inspection on error.
        app.create_object_list(objs=objects,model_id=model,skip_invalid_attributes=False)
        readback(app,model,objects,spec)
        if calculate:
            result=app.calculate_all(model_id=model,skip_warnings=False)
            if not result.succeeded:raise RuntimeError('SOLVER_NOT_SUCCEEDED')
        out.mkdir(parents=True,exist_ok=True)
        app.save_model(model_id=model,path=str(target),results=calculate)
        if not target.is_file() or target.stat().st_size==0:raise RuntimeError('SAVE_NOT_CONFIRMED')
        return {'model_id':model.guid,'path':str(target),'input_readback':'PASS_GEOMETRY_REFERENCES_LOADS_ANALYSIS_CATALOG_IDENTITIES',
                'solver':'SUCCEEDED' if calculate else 'NOT_RUN','engineering_acceptance':'NOT_GRANTED'}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--span-m',type=float,required=True)
    parser.add_argument('--height-m',type=float,required=True)
    parser.add_argument('--roof-line-load-N-m',type=float,required=True)
    parser.add_argument('--out',type=Path,default=Path('runs/rfem-pilot'))
    parser.add_argument('--port',type=int,default=9000)
    parser.add_argument('--create-live',action='store_true')
    parser.add_argument('--calculate',action='store_true')
    parser.add_argument('--approved-input-sha')
    args=parser.parse_args()
    try:
        p=FrameParameters(args.span_m,args.height_m,args.roof_line_load_N_m);spec=contract(p)
        if args.calculate and not args.create_live:raise ValueError('CALCULATE_REQUIRES_ISOLATED_CREATE')
        if not args.create_live:
            print(json.dumps({'status':'PLAN_ONLY','contract':spec},indent=2));return 0
        if args.approved_input_sha!=spec['input_sha256']:raise ValueError('HUMAN_INPUT_HASH_ATTESTATION_REQUIRED')
        result=create_live(p,spec,args.out,args.port,args.calculate,args.approved_input_sha)
        print(json.dumps({'status':'LIVE_OPERATION_COMPLETED','input_sha256':spec['input_sha256'],**result}));return 0
    except Exception as exc:
        print(json.dumps({'status':'BLOCKED_OR_PARTIAL','error_type':type(exc).__name__,
                          'message':str(exc) if isinstance(exc,ValueError) else 'Inspect local RFEM model and sanitized diagnostics before retry.',
                          'automatic_retry':False,'engineering_acceptance':'NOT_GRANTED'}));return 2

if __name__=='__main__':raise SystemExit(main())
