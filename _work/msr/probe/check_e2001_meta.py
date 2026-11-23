import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
t = (ROOT/"04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md").read_text(encoding="utf-8")
frag = json.load(open(ROOT/"_work/msr/fragments/RWB-ITG-E2001-ITG.json", encoding="utf-8"))
meta = t.split("| Item | Value |\n|---|---|\n",1)[1].split("\n\n",1)[0]
rows = [r for r in meta.splitlines() if r.startswith("|")]
print("meta rows:", len(rows))
for r in rows:
    c=[x.strip() for x in r.strip("|").split("|")]
    print(f"  {c[0]} = {c[1][:90]}")
tcs = re.findall(r"(?m)^\| (TC-[A-Za-z0-9-]+) \|", t)
print("tc rows:", len(tcs))
print(tcs)
print("frag tcs match:", tcs == frag["tcs"])
print("cite:", t.count("CG-B-ITG-W2-01-E2001-1"), t.count("ASM-B-ITG-W2-01-E2001-1"))
print("gap rows:", len((ROOT/"_work/msr/gaps/B-ITG-W2-01.jsonl").read_text(encoding="utf-8").strip().splitlines()))
print("asm rows:", len((ROOT/"_work/msr/assumptions/B-ITG-W2-01.jsonl").read_text(encoding="utf-8").strip().splitlines()))
