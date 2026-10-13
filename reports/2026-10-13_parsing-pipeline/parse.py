import json,subprocess,collections
def gws(q,tok=None):
    p={"q":q,"pageSize":1000,"fields":"nextPageToken,files(id,name,mimeType,size,modifiedTime,md5Checksum)"}
    if tok:p["pageToken"]=tok
    return json.loads(subprocess.run(["gws","drive","files","list","--params",json.dumps(p)],capture_output=True,text=True).stdout)
roots={"1MDir6QolBWV8S8mNcd1S9Wn7JT_W9Yqx":"LLM_LOCAL_SSOT (A)","1uBRBCYUQTu-4tsu0MZEAN17HfqUlbIgW":"LLM_LOCAL_SSOT (B)","1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV":"LLM-LOCAL-SSOT (C)"}
files=[]
for rid,rn in roots.items():
    stack=[(rid,"")];n=0
    while stack and n<4000:
        fid,path=stack.pop();tok=None
        while True:
            r=gws(f"'{fid}' in parents and trashed=false",tok)
            for f in r.get("files",[]):
                n+=1;f["path"]=path+"/"+f["name"];f["root"]=rn
                if f["mimeType"].endswith("folder"):stack.append((f["id"],f["path"]))
                files.append(f)
            tok=r.get("nextPageToken")
            if not tok:break
repos=json.loads(subprocess.run(["gh","repo","list","julianzotter","--limit","200","--json","name,visibility,updatedAt,description,url,diskUsage,primaryLanguage"],capture_output=True,text=True).stdout)
repos=[r for r in repos if any(k in r["name"].lower() for k in["nexus","ai","llm","agent","ssot"])]
md5=collections.defaultdict(list)
for f in files:
    if f.get("md5Checksum"):md5[f["md5Checksum"]].append(f["root"]+f["path"])
dups=[v for v in md5.values() if len(v)>1]
json.dump({"files":files,"repos":repos,"dups":dups},open("inventory.json","w"),ensure_ascii=False)
print(len(files),len(repos),len(dups))
for rn in roots.values():
    fs=[f for f in files if f["root"]==rn];print(rn,len(fs),sum(int(f.get("size",0)) for f in fs))
