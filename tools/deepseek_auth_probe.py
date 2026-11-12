"""Explicit read-only model-authentication probe; never print credentials."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'orchestrator'))
from nexus_orch.deepseek import models_probe

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    if not args.execute:
        print(json.dumps({'status':'NOT_RUN','endpoint':'GET https://api.deepseek.com/models','next':'--execute for an authorized read-only probe'}))
        return 0
    result=models_probe()
    print(json.dumps(result))
    return 0 if result['status']=='AUTHENTICATED' else 2

if __name__=='__main__':raise SystemExit(main())
