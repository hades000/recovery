import json,re,io
from pathlib import Path
base=Path(".")
app=base/"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3007 APP Send the offer and start the validity timer v1.md"
con=base/"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3007 CON Send the offer and start the validity timer - contract v1.md"
META=["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
SEC=["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria","Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages","Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
for p in (app,con):
    t=p.read_text(encoding="utf-8")
    print("==",p.name, len(t),"bytes")
    print(" title ok:", bool(re.match(r"^# (RWB-\S+) ", t)), re.match(r"^# (\S+)",t).group(1))
    pre=t.split("### 1.",1)[0]
    rows=[r for r in re.findall(r"^\|\s*([^|]+?)\s*\|",pre,re.M) if r in META]
    print(" meta ok:", rows==META, [m for m in META if m not in rows])
    heads=re.findall(r"^### (\d+)\. (.+?)\s*$",t,re.M)
    print(" sects ok:", [h[1] for h in heads[:19]]==SEC, [int(h[0]) for h in heads[:19]]==list(range(1,20)), len(heads))
    bad=[l for l in t.splitlines() if re.match(r"^\s*Scenario:\s*AC\d+",l) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)",l)]
    print(" AC tags bad:", bad)
    print(" old base:", "/api/recovery/v1/" in t, "jira:", bool(re.search(r"(?i)\bjira\b|atlassian\.net",t)), "email:", bool(re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",t)))
    print(" tentative:", "(tentative)" in t, " D-RCV-60:", "D-RCV-60" in t, " tool:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in t)
    print(" rwb topics:", sorted(set(re.findall(r"rwb\.([a-z-]+)\.(?:events\.v1|[A-Za-z]+\.v1)",t))))
    print(" cites:", sorted(set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b",t))))
for f in ["_work/msr/fragments/RWB-S2-E3007-APP.json","_work/msr/fragments/RWB-S2-E3007-CON.json"]:
    print(f, "json ok", bool(json.loads(Path(f).read_text(encoding="utf-8"))))
for f in ["_work/msr/gaps/B2-S2-002.jsonl","_work/msr/assumptions/B2-S2-002.jsonl"]:
    rows=[json.loads(l) for l in Path(f).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f,"rows",len(rows),[r["id"] for r in rows])
g=[json.loads(l) for l in Path("_work/msr/gaps/B2-S2-002.jsonl").read_text(encoding="utf-8").splitlines()]
print("gap missing:",[{k for k in ("id","title","description","type","severity") if not r.get(k)} for r in g])
a=[json.loads(l) for l in Path("_work/msr/assumptions/B2-S2-002.jsonl").read_text(encoding="utf-8").splitlines()]
print("asm missing:",[{k for k in ("id","text","why") if not r.get(k)} for r in a])
