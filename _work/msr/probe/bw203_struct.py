import re,json,glob,io,os
files = [
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2012 ITG Manual transfer and reassignment screen with reason - integration v1.md",
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2013 ITG Approval routing with the delegation of authority table - integration v1.md",
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2014 ITG Approval screen for D7.1 demand and recall notices - integration v1.md",
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2015 ITG Timers, escalation and the deviation flag on the case record view - integration v1.md",
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2016 ITG Full case record view with the history timeline - integration v1.md",
]
for f in files:
    t = io.open(f,encoding="utf-8").read()
    lines = t.splitlines()
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    secs = re.findall(r"^#### (12\.\d)", t, re.M)
    scen = [l for l in lines if re.match(r"^\s*Scenario:", l)]
    tags = [l for l in scen if not re.search(r"\((new, D-RCV-60)\)", l)]
    tcs = re.findall(r"^\| (TC-E2-\d{3}-\d{2}(?:-ITG)?) \|", t, re.M)
    noitg = [x for x in tcs if not x.endswith("-ITG")]
    dpr = re.findall(r"^\| (DP\d\d) \|", t, re.M)
    print(os.path.basename(f)[:22], "| lines",len(lines), "| heads",len(heads), "| secs",len(secs), "| scen",len(scen),"bad",len(tags),"| tcs",len(tcs),"noITG",noitg,"| dprows",len(dpr))
    print("   ", [h[1] for h in heads][:19])
    print("   ", secs)
    if tags: print("   BAD:",tags)
