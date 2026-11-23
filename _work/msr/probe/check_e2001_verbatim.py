import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
story = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md"
legacy = ROOT / "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 001 EFS hand over with full history from the COLLINS load v1.md"

def scen(txt):
    out = {}
    cur = None
    for line in txt.splitlines():
        m = re.match(r"^\s*Scenario: (AC\d+)(.*)$", line)
        if m:
            cur = m.group(1)
            out[cur] = [line.strip()]
            continue
        if cur and (line.strip().startswith(("Given","When","Then","And","Background","Feature","```")) or line.strip()==""):
            if line.strip()=="":
                cur=None
            continue
        if cur is not None and line.strip():
            out[cur].append(line.strip())
    # keep only Given/When/Then/And and Scenario lines
    for k,v in out.items():
        out[k]=[x for x in v if x.startswith(("Scenario:","Given","When","Then","And"))]
    return out

a = scen(legacy.read_text(encoding="utf-8")); b = scen(story.read_text(encoding="utf-8"))
for k in ["AC1","AC3","AC5","AC6"]:
    la = a[k]; lb = b[k]
    lb = [re.sub(r" \(legacy RWB-E2-001 AC\d\)$","",x) for x in lb]
    print(k, "OK" if la==lb else "DIFF")
    if la!=lb:
        for x,y in zip(la,lb):
            if x!=y: print("  L:",x,"\n  S:",y)
# background + feature lines
def feats(txt):
    return [l.strip() for l in txt.splitlines() if l.strip().startswith(("Feature:","Given parameter","Given the ACE batch for ALS with business date 2026-12-14"))]
print(feats(legacy.read_text(encoding='utf-8')))
print(feats(story.read_text(encoding='utf-8')))
