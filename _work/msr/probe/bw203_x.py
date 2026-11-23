import re,io,glob,os
for f in sorted(glob.glob("04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E201[2-6]*.md")):
    t=io.open(f,encoding="utf-8").read()
    sec5=t.split("### 5. Exception paths")[1].split("### 6.")[0]
    ids=re.findall(r"^\| (X[A-Z0-9]+) \|",sec5,re.M)
    print(os.path.basename(f)[:16], ids)
