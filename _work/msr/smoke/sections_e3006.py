import re, pathlib
files = [
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3006 APP Calculate the plan installment v1.md",
 "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3006 CON Calculate the plan installment - contract v1.md",
]
for f in files:
    t = pathlib.Path(f).read_text(encoding="utf-8")
    parts = re.split(r"^### (\d+)\. ", t, flags=re.M)
    print("==", pathlib.Path(f).name)
    # parts[0] header, then pairs
    for i in range(1, len(parts), 2):
        num = parts[i]; body = parts[i+1]
        lines = [l for l in body.splitlines()[1:]]
        nonblank = [l for l in lines if l.strip()]
        tableish = [l for l in nonblank if l.strip().startswith("|") or l.strip().startswith("```") or l.strip().startswith("Given") or l.strip().startswith("When") or l.strip().startswith("Then") or l.strip().startswith("Scenario") or l.strip().startswith("Background") or l.strip().startswith("Feature")]
        prose = [l for l in nonblank if l not in tableish]
        print(f"  s{num}: total {len(nonblank)} prose {len(prose)} chars {len(body)}")
