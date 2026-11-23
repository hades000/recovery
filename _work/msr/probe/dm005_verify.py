import json, re, pathlib
p = pathlib.Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM005 APP Migrate contact and promises v1.md")
t = p.read_text(encoding="utf-8")
cite = sorted(set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)))
print("cited:", cite)
g = [json.loads(l) for l in pathlib.Path("_work/msr/gaps/B-P1-04-DM005.part.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
a = [json.loads(l) for l in pathlib.Path("_work/msr/assumptions/B-P1-04-DM005.part.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print("gap ids:", [r["id"] for r in g])
print("asm ids:", [r["id"] for r in a])
print("orphan in jsonl:", [r["id"] for r in g+a if r["id"] not in cite])
print("missing row:", [c for c in cite if c not in {r["id"] for r in g+a}])
print("gap keys:", list(g[0].keys()))
print("asm keys:", list(a[0].keys()))
# section headings
heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
print("heads:", [h[0] for h in heads])
# 12.x
print("12 subs:", re.findall(r"^\*\*(12\.\d [^*]+)\*\*", t, re.M))
# TCs
print("TCs:", re.findall(r"TC-DM-005-\d{2}(?:-ITG)?", t))
print("scenarios:", re.findall(r"^\s*Scenario:.*$", t, re.M))
print("12.1-12.9 count:", len(re.findall(r"^\*\*12\.\d ", t, re.M)))
f = json.loads(pathlib.Path("_work/msr/fragments/RWB-P1-DM005-APP.json").read_text(encoding="utf-8"))
print("frag keys:", list(f.keys()))
