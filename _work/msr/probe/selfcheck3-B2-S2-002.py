import re
from pathlib import Path
files=[p for p in Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)").glob("RWB S2 E3007*.md")]
for p in files:
    t=p.read_text(encoding="utf-8"); lines=t.splitlines()
    print("==",p.name[:40])
    # table integrity: group consecutive lines starting with |
    i=0; probs=[]
    while i<len(lines):
        if lines[i].startswith("|"):
            j=i
            while j<len(lines) and lines[j].startswith("|"): j+=1
            block=lines[i:j]; cols=[b.count("|") for b in block]
            if len(set(cols))>1: probs.append((i+1,block[0][:60],cols))
            i=j
        else: i+=1
    print(" table blocks uneven:",probs[:5])
    print(" bare section ref:", [l[:60] for l in lines if "§R7.2 s17" in l and "Template and Rules" not in l])
    # section sizes (non-table lines count)
    secs=re.split(r"^### (\d+)\. ",t,flags=re.M)
    for k in range(1,len(secs),2):
        body=secs[k+1]; n=len([l for l in body.splitlines() if l.strip() and not l.startswith("|")])
        if n>30: print("  section",secs[k],"long non-table lines:",n)
