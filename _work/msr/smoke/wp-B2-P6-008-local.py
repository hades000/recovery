import json,re
from pathlib import Path
R=Path(".")
frag=json.loads(Path("_work/msr/fragments/RWB-P6-E2017-APP.json").read_text(encoding="utf-8"))
print("frag keys ok:", all(k in frag for k in ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]))
gaps=[json.loads(l) for l in Path("_work/msr/gaps/B2-P6-008.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
asms=[json.loads(l) for l in Path("_work/msr/assumptions/B2-P6-008.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print("gaps",len(gaps),"asms",len(asms))
ids={r["id"] for r in gaps}|{r["id"] for r in asms}
story=Path(frag["file"]).read_text(encoding="utf-8")
cite=re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
used=set(cite.findall(story))|set(cite.findall(json.dumps(frag)))
print("cited not in jsonl:", sorted(used-ids))
print("frag refs:", frag["gaps"], frag["assumptions"])
print("tentative:", "(tentative)" in story, "oldbase:", "/api/recovery/v1/" in story)
heads=re.findall(r"^### (\d+)\. (.+?)\s*$",story,re.M)
print("sections:",len(heads), [int(h[0]) for h in heads][:19]==list(range(1,20)))
rows=re.findall(r"^\|\s*([^|]+?)\s*\|",story.split("### 1.",1)[0],re.M)
META=["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
got=[r for r in rows if r in META]
print("meta ok:", got==META)
print("scenarios:", [l.strip() for l in story.splitlines() if l.strip().startswith("Scenario:")][:3])
print("all tagged:", all(re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)",l) for l in story.splitlines() if l.strip().startswith("Scenario: AC")))
print("jira:", bool(re.search(r"(?i)\bjira\b|atlassian\.net",story)))
print("tcs in story:", len(set(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b",story))))
print("frag tcs:",len(frag["tcs"]))
