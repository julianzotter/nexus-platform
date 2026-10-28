#!/usr/bin/env python3
"""Export a consistent read-only AnythingSearch snapshot. Metadata only, no source writes."""
import argparse,csv,hashlib,json,sqlite3,tempfile,os
from pathlib import Path
from datetime import datetime,timezone

def export(source,out):
 source=Path(source).resolve();out=Path(out);out.mkdir(parents=True,exist_ok=True)
 if not source.is_file():raise FileNotFoundError(source)
 now=datetime.now(timezone.utc).isoformat()
 # URI mode=ro still reads matching WAL. backup API includes committed transactions.
 with tempfile.TemporaryDirectory() as td:
  snapshot=Path(td)/'snapshot.db'
  with sqlite3.connect(source.as_uri()+'?mode=ro',uri=True) as src,sqlite3.connect(snapshot) as dst:src.backup(dst)
  with sqlite3.connect(snapshot.as_uri()+'?mode=ro',uri=True) as db:
   check=db.execute('PRAGMA quick_check').fetchall()
   if check!=[('ok',)]:raise ValueError('quick_check failed: '+repr(check))
   schema={t:[r[1] for r in db.execute('PRAGMA table_info("'+t+'")')] for t in ['Files','Folders']}
   expected={'Files':{'Id','Name','FolderId','Ext','Size','Modified','IsFolder'},'Folders':{'Id','Path'}}
   for t,cols in expected.items():
    if not cols.issubset(schema[t]):raise ValueError('Unsupported schema '+json.dumps(schema))
   sql='SELECT f.Id,f.Name,d.Path,f.Ext,f.Size,f.Modified,f.IsFolder FROM Files f LEFT JOIN Folders d ON d.Id=f.FolderId ORDER BY f.Id'
   tmp=out/'files.csv.tmp';count=0;missing=0
   with tmp.open('w',newline='',encoding='utf-8-sig') as stream:
    w=csv.writer(stream);w.writerow(['Id','Name','Folder','Ext','Size','Modified_raw','IsFolder'])
    for row in db.execute(sql):
     # Exclude configurations and credential-like names from exported metadata.
     import re
     if str(row[1]).startswith('.') or re.search(r'sk-proj-|credential|password|secret|token',str(row[1]),re.I):continue
     w.writerow(row);count+=1;missing+=row[2] is None
   digest=hashlib.sha256(snapshot.read_bytes()).hexdigest()
  tmp.replace(out/'files.csv')
  report={'status':'METADATA_EXPORTED','observed_at':now,'source':str(source),'source_mtime':datetime.fromtimestamp(source.stat().st_mtime,timezone.utc).isoformat(),'snapshot_sha256':digest,'exported_rows':count,'missing_parent_rows':missing,'schema':schema,'quick_check':'ok','timestamp_units':'UNINTERPRETED','content_validated':False,'freshness':'NOT_ESTABLISHED_BY_QUICK_CHECK','wal_present':Path(str(source)+'-wal').exists()}
  (out/'refresh.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 try:print(json.dumps(export(a.db,a.out),indent=2))
 except Exception as e:
  Path(a.out).mkdir(parents=True,exist_ok=True);(Path(a.out)/'files.csv').unlink(missing_ok=True);(Path(a.out)/'refresh.json').write_text(json.dumps({'status':'FAILED','reason':str(e),'observed_at':datetime.now(timezone.utc).isoformat()}));raise
