"""Internal consistency check for the P6 PRD: ID counts, coverage, and citations that resolve to a register row."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PRD = ROOT / "03 Requirements and specifications" / "PRD" / "Recovery Workbench PRD P6 rwb-comms v1.md"
t = PRD.read_text(encoding="utf-8")

def ids(prefix):
    return sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", t)))

cap = [i for i in ids("CAP-P6")]
fr = [i for i in ids("FR-P6")]
nfr = [i for i in ids("NFR-P6")]
ac = [i for i in ids("AC-P6")]
rol = [i for i in ids("ROL-P6")]
jrn = [i for i in ids("JRN-P6")]
oq = [i for i in ids("OQ-P6")]
print("CAP", len(cap), cap[0], cap[-1])
print("FR", len(fr), fr[0], fr[-1])
print("NFR", len(nfr), nfr[0], nfr[-1])
print("AC", len(ac), ac[0], ac[-1])
print("ROL", len(rol), "JRN", len(jrn), "OQ", len(oq))

# gaps in the sequences
for name, lst in (("CAP", cap), ("FR", fr), ("NFR", nfr), ("AC", ac)):
    nums = [int(x.split("-")[-1]) for x in lst]
    missing = [n for n in range(1, max(nums) + 1) if n not in nums]
    if missing:
        print(name, "missing numbers:", missing)

# AC coverage of FR and NFR
cov = set()
for line in t.splitlines():
    if line.startswith("| AC-P6-"):
        cov.update(re.findall(r"\bFR-P6-\d{3}\b|\bNFR-P6-\d{3}\b", line))
print("FR/NFR never referenced by an AC row:", [x for x in fr + nfr if x not in cov])

# every FR row has a BR
fr_rows = [l for l in t.splitlines() if l.startswith("| FR-P6-")]
print("FR rows:", len(fr_rows))
bad = [l.split("|")[1].strip() for l in fr_rows if "REQ-" not in l.split("|")[4]]
print("FR rows without a BR:", bad)
nfr_rows = [l for l in t.splitlines() if l.startswith("| NFR-P6-")]
print("NFR rows:", len(nfr_rows))
print("NFR rows without a BR:", [l.split("|")[1].strip() for l in nfr_rows if "NFR-" not in l.split("|")[4]])

# citations resolve
gaps = {json.loads(l)["id"] for l in (ROOT / "_work/msr/gaps/B-REQ-PRD-P6.jsonl").read_text(encoding="utf-8").splitlines()}
asm = {json.loads(l)["id"] for l in (ROOT / "_work/msr/assumptions/B-REQ-PRD-P6.jsonl").read_text(encoding="utf-8").splitlines()}
cited = set(re.findall(r"\bCG-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
cited_a = set(re.findall(r"\bASM-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
print("CG cited", len(cited), "unresolved:", sorted(cited - gaps))
print("ASM cited", len(cited_a), "unresolved:", sorted(cited_a - asm))
print("CG rows never cited:", sorted(gaps - cited))
print("ASM rows never cited:", sorted(asm - cited_a))

# header lines and change log row
lines = t.splitlines()
print("header ok:", lines[0] == "SCB Collections and Recovery. Henka Group, 22 November 2026." and lines[1] == "(C) Siam Commercial Bank and Henka Pte Ltd")
print("change log row ok:", "| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |" in t)
print("sections:", [s for s in re.findall(r"(?m)^# (\d+)\. ", t)])
print("tentative count:", t.count("(tentative)"))
