import json,subprocess,os,concurrent.futures as cf,re,time
os.environ["TESSDATA_PREFIX"]=os.path.abspath("tessdata")
d=json.load(open("out/NEXUS_PARSE_INVENTORY_v1.0.json"))
TXT={"md","txt","json","yaml","yml","py","csv","jsonl","html","ps1","js"}
IMG={"jpg","jpeg","png"}
R=[r for r in d["rows"] if r["r"]=="C" and ((r["e"] in TXT and r["s"]<2e6) or (r["e"] in IMG|{"pdf"} and r["s"]<5e6) or r["e"]=="gdoc")]
out={}; 
if os.path.exists("ocr_cache.json"): out=json.load(open("ocr_cache.json"))
def run(r):
    time.sleep(0.4)
    if r["id"] in out: return r["id"],out[r["id"]]
    fn=f"dl/{r['id']}.{r['e']}"; meth=""
    try:
        if r["e"]=="gdoc":
            subprocess.run(["gws","drive","files","export","--params",json.dumps({"fileId":r["id"],"mimeType":"text/plain"}),"--output",fn],capture_output=True,timeout=60)
        else:
            subprocess.run(["gws","drive","files","get","--params",json.dumps({"fileId":r["id"],"alt":"media"}),"--output",fn],capture_output=True,timeout=90)
        if not os.path.exists(fn): return r["id"],{"m":"fehler","t":""}
        if r["e"] in IMG:
            t=subprocess.run(["tesseract",fn,"-","-l","deu+eng"],capture_output=True,text=True,timeout=120).stdout;meth="ocr-bild"
        elif r["e"]=="pdf":
            t=subprocess.run(["pdftotext","-l","30",fn,"-"],capture_output=True,text=True,timeout=60).stdout;meth="pdftext"
            if len(t.strip())<200:
                subprocess.run(["pdftoppm","-r","150","-l","3","-png",fn,f"dl/{r['id']}_p"],timeout=120)
                t="";meth="ocr-pdf"
                for p in sorted(x for x in os.listdir("dl") if x.startswith(r["id"]+"_p")):
                    t+=subprocess.run(["tesseract","dl/"+p,"-","-l","deu+eng"],capture_output=True,text=True,timeout=120).stdout
        else:
            t=open(fn,encoding="utf-8",errors="ignore").read();meth="text"
        return r["id"],{"m":meth,"t":re.sub(r"\s+"," ",t)[:60000]}
    except Exception as e: return r["id"],{"m":"fehler","t":""}
    finally:
        for x in os.listdir("dl"):
            if x.startswith(r["id"]): os.remove("dl/"+x)
t0=time.time()
with cf.ThreadPoolExecutor(3) as ex:
    for i,(k,v) in enumerate(ex.map(run,R)):
        out[k]=v
        if i%50==0: print(i,len(R),int(time.time()-t0),flush=True); json.dump(out,open("ocr_cache.json","w"))
json.dump(out,open("ocr_cache.json","w"))
import collections;print(collections.Counter(v["m"] for v in out.values()))
