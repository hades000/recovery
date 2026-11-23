import json, re, sys
from pathlib import Path

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
story = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2002 APP ACE plan status on the case v1.md"
frag = ROOT / "_work/msr/fragments/RWB-P7-E2002-APP.json"
gaps = ROOT / "_work/msr/gaps/B-P7-08-E2002.part.jsonl"
asms = ROOT / "_work/msr/assumptions/B-P7-08-E2002.part.jsonl"

t = story.read_text(encoding="utf-8")
fails = []

# fragment
f = json.loads(frag.read_text(encoding="utf-8"))
want = ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]
if list(f.keys()) != want:
    fails.append(f"fragment keys: {list(f.keys())}")

# jsonl
def load(p, req):
    rows = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        r = json.loads(line)
        rows.append(r)
        if list(r.keys()) != req:
            fails.append(f"{p.name}:{i} keys {list(r.keys())}")
    return rows

greq = ["id","title","source","section","description","evidence","type","area","severity","needed_by_wave","legacy_ref","owner_role","asm","proposed","wp"]
areq = ["id","text","why","read","gap","applied_in","confidence","confirm","impact","wp"]
g = load(gaps, greq); a = load(asms, areq)
gid = {r["id"] for r in g}; aid = {r["id"] for r in a}
for r in g:
    if r["asm"] not in aid: fails.append(f"gap {r['id']} asm {r['asm']} missing")
    if r["type"] not in ("Missing","Conflict","Ambiguous","Outdated","ID collision"): fails.append(f"gap {r['id']} type {r['type']}")
    if r["severity"] not in ("P1","P2","P3"): fails.append(f"gap {r['id']} severity")
    if r["wp"] != "B-P7-08" or r["legacy_ref"] != "RWB-E2-002": fails.append(f"gap {r['id']} wp/legacy")
for r in a:
    if r["gap"] not in gid: fails.append(f"asm {r['id']} gap {r['gap']} missing")
    if r["confidence"] not in ("High","Medium","Low"): fails.append(f"asm {r['id']} confidence")
    if r["wp"] != "B-P7-08": fails.append(f"asm {r['id']} wp")
if [r["id"] for r in g] != [f"CG-B-P7-08-E2002-{i}" for i in range(1,4)]: fails.append("gap ids")
if [r["id"] for r in a] != [f"ASM-B-P7-08-E2002-{i}" for i in range(1,11)]: fails.append("asm ids")

# fragment cross refs
if f["gaps"] != [r["id"] for r in g]: fails.append("fragment gaps mismatch")
if f["assumptions"] != [r["id"] for r in a]: fails.append("fragment asm mismatch")

# every CG/ASM cited in the story exists
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
for c in sorted(cited):
    if c not in gid | aid: fails.append(f"story cites {c} with no row")

# placeholders
for m in re.findall(r"Not specified in the source documents \(([^)]*)\)", t):
    for c in re.findall(r"(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+", m):
        if c not in gid | aid: fails.append(f"placeholder cites {c}")

# sections, metadata, TCs, ACs, contract tables
heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
if [int(h[0]) for h in heads] != list(range(1,20)): fails.append(f"sections {[h[0] for h in heads]}")
acs = re.findall(r"^\s*Scenario: (AC\d+)(.*)$", t, re.M)
if len(acs) != 7: fails.append(f"AC count {len(acs)}")
for n, rest in acs:
    if "(new, D-RCV-60)" not in rest: fails.append(f"{n} origin tag")
tcs = re.findall(r"^\|\s*(TC-E2-002-\d{2})\s*\|", t, re.M)
want_tcs = ["10","01","02","03","04","05","06","07","08","09","11"]
if [x.split("-")[-1] for x in tcs] != want_tcs: fails.append(f"TCs {tcs}")
if re.search(r"TC-[A-Z0-9]+-\d{3}-\d{2}-ITG", t): fails.append("ITG copy present")
for n in range(1,10):
    if f"#### 12.{n} " not in t: fails.append(f"12.{n} missing")
# metadata
meta = t.split("### 1.",1)[0]
rows = re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", meta, re.M)
meta_d = {k: v for k, v in rows if k not in ("Item","---")}
expect = {
 "Story key":"RWB-P7-E2002-APP","Work type":"APP (App development)",
 "Suggested owner":"TechX (suggested; any team may pick up this story)","Service":"rwb-decision",
 "Service epic":"RWB-SVC-P7","Wave":"2","Business epic":"EP02","Release":"31 December 2026 (tentative)",
 "Legacy key":"RWB-E2-002","Legacy disposition":"Split (rework)","Build status":"Not started",
 "Patterns applied":"DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19",
 "Parallel lane":"L-P7-R","Ready to start":"Day 1","Depends on (build)":"None",
 "Contract dependencies":"RWB-P2-E2002-CON","Integration dependencies":"None",
 "External dependencies":"None","PRD reference":"Pending (C1)","Status":"Draft (realignment v1)"}
for k, v in expect.items():
    if meta_d.get(k) != v: fails.append(f"meta {k}={meta_d.get(k)!r} want {v!r}")
if len(meta_d) != 20: fails.append(f"meta rows {len(meta_d)}")

print("FAILS:", len(fails))
for x in fails: print(" -", x)
print("CG:", len(g), "ASM:", len(a))
print("cited:", sorted(cited))
