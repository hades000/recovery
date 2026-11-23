import json,re,csv,sys
from pathlib import Path
sys.path.insert(0,"22 Microservice Realignment/compat")
from common import ROOT, WORK, SERVICES
SHORTS={s["short"] for s in SERVICES}
files=[Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2017 APP Contract, CA and mortgage document generation screens v1.md"),
 Path("_work/msr/fragments/RWB-P6-E2017-APP.json"),Path("_work/msr/gaps/B2-P6-008.jsonl"),Path("_work/msr/assumptions/B2-P6-008.jsonl")]
# names deny-list
names=set()
for p in ROOT.glob("21*/**/*"):
    if p.suffix.lower()==".csv":
        with open(p,encoding="utf-8",errors="ignore",newline="") as f:
            for row in csv.DictReader(f):
                for k,v in row.items():
                    if k and re.search(r"(?i)assignee|reporter|creator|watcher|author|updated by",k) and v and " " in v.strip():
                        names.add(v.strip().lower())
    elif p.suffix.lower()==".json":
        try: txt=p.read_text(encoding="utf-8",errors="ignore")
        except OSError: continue
        names.update(n.lower() for n in re.findall(r'"displayName"\s*:\s*"([^"@]+ [^"@]+)"',txt))
email=re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
bad=0
for p in files:
    for n,line in enumerate(p.read_text(encoding="utf-8",errors="replace").splitlines(),1):
        low=line.lower()
        if any(nm in low for nm in names): print("NAME",p.name,n,line[:90]); bad+=1
        if email.search(line) and "example" not in low and "noreply" not in low: print("EMAIL",p.name,n); bad+=1
print("name/email findings:",bad)
sf=files[0].read_text(encoding="utf-8")
for rx in [r"\brwb\.([a-z-]+)\.events\.v1\b", r"/api/recovery/([a-z-]+)/v1\b", r"\bqueue rwb-([a-z-]+)\b"]:
    for m in re.finditer(rx,sf):
        if m.group(1) not in SHORTS: print("SHORT?",m.group(0))
plan=json.loads((WORK/"plan"/"split_plan.json").read_text(encoding="utf-8"))
rel={x["id"]:x.get("release","") for x in plan["slices"]}
print("plan release:",rel.get("RWB-P6-E2017-APP"))
print("file listed in plan:", any(x["id"]=="RWB-P6-E2017-APP" for x in plan["slices"]))
