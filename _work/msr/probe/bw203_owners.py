import re,io,json,glob,os
own=json.load(io.open("_work/msr/plan/ownership.json",encoding="utf-8"))["api"]
for f in sorted(glob.glob("04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E201[2-6]*.md")):
    t=io.open(f,encoding="utf-8").read()
    sec=t.split("#### 12.2 REST operations consumed")[1].split("#### 12.3")[0]
    bad=[]
    for m in re.finditer(r"^\| (GET|POST|PATCH|PUT|DELETE) \| `([^`]+)` \| ([A-Z0-9]+) ",sec,re.M):
        method,path,owner=m.group(1),m.group(2),m.group(3)
        key=path.split("/v1",1)[1]
        rec=own.get(f"{method} {key}")
        if not rec: bad.append((method+" "+key,"NOT IN MAP"))
        elif rec["owner"]!=owner: bad.append((method+" "+key,f"{owner} vs {rec['owner']}"))
    print(os.path.basename(f)[:16],"owner mismatches:",bad)
