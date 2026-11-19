"""Local SDK inspection; optional read-only RFEM host connection."""
from __future__ import annotations
import argparse
import inspect
import json
from importlib.metadata import PackageNotFoundError,version

REQUIRED=['create_model','create_object_list','get_object_list','get_object','calculate_all']
def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--read-live',action='store_true')
    parser.add_argument('--port',type=int,default=9000)
    parser.add_argument('--api-key-name')
    args=parser.parse_args()
    try:
        from dlubal.api import rfem
        report={'sdk':version('dlubal.api'),'methods':{n:str(inspect.signature(getattr(rfem.Application,n))) for n in REQUIRED},'live':'NOT_RUN'}
        if args.read_live:
            with rfem.Application(api_key_name=args.api_key_name,url='127.0.0.1',port=args.port) as app:
                info=app.get_application_info()
                report['live']='APPLICATION_INFO_READ'
                report['application_version']=getattr(info,'full_version','') or getattr(info,'version','')
        print(json.dumps(report));return 0
    except (ImportError,PackageNotFoundError):
        print(json.dumps({'status':'BLOCKED','reason':'SDK_NOT_INSTALLED','live':'NOT_RUN'}));return 2
    except Exception as exc:
        print(json.dumps({'status':'BLOCKED','reason':type(exc).__name__,'secrets':'REDACTED'}));return 2

if __name__=='__main__':raise SystemExit(main())
