import re,io,json,glob,os
for f in sorted(glob.glob("04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E201[2-6]*.md")):
    t=io.open(f,encoding="utf-8").read()
    sid=re.match(r"^# (\S+)",t).group(1)
    frag=json.load(io.open(f"_work/msr/fragments/{sid}.json",encoding="utf-8"))
    sec=t.split("#### 12.2 REST operations consumed")[1].split("#### 12.3")[0]
    ops=[m.group(1)+" "+m.group(2) for m in re.finditer(r"^\| (GET|POST|PATCH|PUT|DELETE) \| `([^`]+)`",sec,re.M)]
    sec16=t.split("### 16. Test cases")[1].split("### 17.")[0]
    tcs=re.findall(r"^\| (TC-E2-\d{3}-\d{2}-ITG) \|",sec16,re.M)
    print(os.path.basename(f)[:16], "| ops match", ops==frag["ops_consumed"], len(ops), "| tcs match", tcs==frag["tcs"], len(tcs))
    if ops!=frag["ops_consumed"]:
        print("  story:",ops); print("  frag :",frag["ops_consumed"])
    if tcs!=frag["tcs"]:
        print("  story:",tcs); print("  frag:",frag["tcs"])
    # every TC in fragment appears in story and vice versa
    print("   sec18 rows:", len(re.findall(r"^\| REQ-",t.split("### 18. Traceability")[1].split("### 19.")[0],re.M)), "reqs", len(frag["reqs"]))
