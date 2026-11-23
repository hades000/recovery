import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
SHORTS = {"source-data","integration","case","access","document","comms","decision","payment","reporting","agent",
          "valuation","treatment","guarantee","litigation","asset","debtsale","writeoff","deviation","partner"}
META = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key",
        "Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)",
        "Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
SEC = ["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria",
       "Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages",
       "Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
FKEYS = ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X",
         "acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]
STORIES = {
 "RWB-ITG-E2029-ITG": dict(rel="31 January 2027", ep="EP03", legacy="RWB-E2-029",
    I=["RWB-P3-E2015-APP","RWB-P10-E2029-APP","RWB-S8-E2029-APP","RWB-P7-E2029-APP"],
    pats="DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19", reqs=["REQ-DVH-001","REQ-DVH-006"],
    tcs=["TC-E2-029-11","TC-E2-029-01","TC-E2-029-02","TC-E2-029-03","TC-E2-029-04","TC-E2-029-05","TC-E2-029-06",
         "TC-E2-029-07","TC-E2-029-08","TC-E2-029-09","TC-E2-029-10","TC-E2-029-12"]),
 "RWB-ITG-E2030-ITG": dict(rel="31 January 2027", ep="EP03", legacy="RWB-E2-030",
    I=["RWB-P5-E2025-APP","RWB-P10-E2030-APP","RWB-P5-E2030-APP"],
    pats="DP01, DP06, DP07, DP09, DP13, DP19", reqs=["REQ-DCM-011"],
    tcs=["TC-E2-030-10","TC-E2-030-01","TC-E2-030-02","TC-E2-030-03","TC-E2-030-04","TC-E2-030-05","TC-E2-030-06",
         "TC-E2-030-07","TC-E2-030-08","TC-E2-030-09"]),
 "RWB-ITG-E2031-ITG": dict(rel="31 December 2026", ep="EP02", legacy="RWB-E2-031",
    I=["RWB-P7-E2005-APP","RWB-P10-E2031-APP","RWB-P4-E2031-APP"],
    pats="DP03, DP07, DP10, DP13, DP15, DP19", reqs=["REQ-DRI-009","REQ-APD-005"],
    tcs=["TC-E2-031-08","TC-E2-031-01","TC-E2-031-02","TC-E2-031-03","TC-E2-031-04","TC-E2-031-05","TC-E2-031-06","TC-E2-031-07"]),
 "RWB-ITG-E2032-ITG": dict(rel="31 December 2026", ep="EP02", legacy="RWB-E2-032",
    I=["RWB-P3-E2004-APP","RWB-P10-E2032-APP","RWB-S2-E2032-APP","RWB-P7-E2032-APP"],
    pats="DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19", reqs=["REQ-CHO-006","REQ-DRI-001"],
    tcs=["TC-E2-032-09","TC-E2-032-01","TC-E2-032-02","TC-E2-032-03","TC-E2-032-04","TC-E2-032-05","TC-E2-032-06",
         "TC-E2-032-07","TC-E2-032-08","TC-E2-032-10"]),
 "RWB-ITG-E2033-ITG": dict(rel="31 December 2026", ep="EP02", legacy="RWB-E2-033",
    I=["RWB-P3-E1018-APP","RWB-P3-E1031-APP","RWB-P3-E2011-APP","RWB-P2-E2033-APP","RWB-P3-E2033-APP","RWB-P4-E2033-APP","RWB-S8-E2033-APP"],
    pats="DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19", reqs=["REQ-WKM-002","REQ-DVH-006","REQ-ACA-006"],
    tcs=["TC-E2-033-12","TC-E2-033-01","TC-E2-033-02","TC-E2-033-03","TC-E2-033-04","TC-E2-033-05","TC-E2-033-06",
         "TC-E2-033-07","TC-E2-033-08","TC-E2-033-09","TC-E2-033-10","TC-E2-033-11"]),
}
files = [ROOT / f["file"] for f in (json.loads(p.read_text(encoding="utf-8")) for p in (WORK/"fragments").glob("RWB-ITG-E20*.json")) if f["id"] in STORIES]
fails = []
gaps = [json.loads(l) for l in (WORK/"gaps/B-ITG-W2-06.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
asms = [json.loads(l) for l in (WORK/"assumptions/B-ITG-W2-06.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ids = {r["id"] for r in gaps} | {r["id"] for r in asms}
if len(gaps) != 5: fails.append(f"gaps rows {len(gaps)}")
if len(asms) != 5: fails.append(f"assumptions rows {len(asms)}")
for r in gaps:
    for k in ("id","title","description","type","severity","source","section","evidence","area","needed_by_wave","legacy_ref","owner_role","asm","proposed","wp"):
        if r.get(k) in (None, ""): fails.append(f"gap {r.get('id')} missing {k}")
for r in asms:
    for k in ("id","text","why","read","gap","applied_in","confidence","confirm","impact","wp"):
        if r.get(k) in (None, ""): fails.append(f"asm {r.get('id')} missing {k}")

for sid, exp in STORIES.items():
    fp = WORK/"fragments"/f"{sid}.json"
    if not fp.exists(): fails.append(f"{sid}: fragment missing"); continue
    f = json.loads(fp.read_text(encoding="utf-8"))
    if list(f.keys()) != FKEYS: fails.append(f"{sid}: fragment keys/order {list(f.keys())}")
    p = ROOT / f["file"]
    if not p.exists(): fails.append(f"{sid}: story file missing {p}"); continue
    t = p.read_text(encoding="utf-8"); lines = t.splitlines()
    if lines[0] != f"# {sid} {f.get('title','')}" and not lines[0].startswith(f"# {sid} "): fails.append(f"{sid}: title line {lines[0]!r}")
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in lines[:6]: fails.append(f"{sid}: header missing")
    if "(C) Siam Commercial Bank and Henka Pte Ltd" not in lines[:6]: fails.append(f"{sid}: copyright missing")
    pre = t.split("### 1.",1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", pre, re.M)
    got = [r for r in rows if r in META]
    if got != META: fails.append(f"{sid}: meta rows {got}")
    def val(label):
        m = re.search(r"^\|\s*"+re.escape(label)+r"\s*\|\s*(.*?)\s*\|$", pre, re.M)
        return m.group(1) if m else None
    checks = {"Story key":sid, "Work type":"ITG (Integration)", "Suggested owner":"TechX (suggested; any team may pick up this story)",
              "Service":"integration", "Service epic":"RWB-ITG-W2", "Wave":"2", "Business epic":exp["ep"],
              "Release":exp["rel"]+" (tentative)", "Legacy key":exp["legacy"], "Legacy disposition":"Split (rework)",
              "Build status":"Not started", "Patterns applied":exp["pats"], "Parallel lane":"L-ITG-W2", "Ready to start":"Day 1",
              "Depends on (build)":"None", "Contract dependencies":"None", "Integration dependencies":", ".join(exp["I"]),
              "External dependencies":"None", "PRD reference":"Pending (C1)", "Status":"Draft (realignment v1)"}
    for k,v in checks.items():
        if (val(k) or "") != v: fails.append(f"{sid}: meta {k}={val(k)!r} want {v!r}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SEC or [int(h[0]) for h in heads[:19]] != list(range(1,20)): fails.append(f"{sid}: sections {heads[:19]}")
    for n in range(1,10):
        if len(re.findall(rf"^#### 12\.{n} ", t, re.M)) != 1: fails.append(f"{sid}: 12.{n} heading")
    acs = [l for l in lines if re.match(r"^\s*Scenario:\s*AC\d+", l)]
    if len(acs) < 6: fails.append(f"{sid}: only {len(acs)} scenarios")
    for l in acs:
        if not l.rstrip().endswith(f"(new, {DEC})"): fails.append(f"{sid}: AC tag {l[:70]}")
    if DEC not in t or "Change log." not in t: fails.append(f"{sid}: no decision")
    if TOOL not in t: fails.append(f"{sid}: tool line")
    # TCs
    story_tcs = [x+"-ITG" for x in exp["tcs"]]
    for tc in story_tcs:
        if len(re.findall(r"\b"+re.escape(tc)+r"\b", t)) < 1: fails.append(f"{sid}: TC {tc} missing")
    if f["tcs"] != story_tcs: fails.append(f"{sid}: fragment tcs differ")
    # 16 table order
    t16 = t.split("### 16. Test cases",1)[1].split("### 17.",1)[0]
    order = re.findall(r"^\|\s*(TC-[A-Z0-9]+-\d{3}-\d{2}-ITG)\s*\|", t16, re.M)
    if order != story_tcs: fails.append(f"{sid}: s16 order {order}")
    if "| TC ID | Covers | Level | Data |" not in t16: fails.append(f"{sid}: s16 header")
    for lvl in re.findall(r"^\|\s*TC-[^|]+\|[^|]*\|\s*([^|]+?)\s*\|", t16, re.M):
        if lvl not in ("Unit","Component","Contract","Integration","End to end","NFR"): fails.append(f"{sid}: level {lvl!r}")
    # ops/events
    t12 = t.split("#### 12.2",1)[1].split("#### 12.3",1)[0]
    ops = re.findall(r"^\|\s*(GET|POST|PATCH|PUT|DELETE)\s*\|\s*(`?[^|`]+?`?)\s*\|", t12, re.M)
    ops = [f"{m} {p.strip('`').strip()}" for m,p in ops]
    if f["ops_consumed"] != ops: fails.append(f"{sid}: ops fragment {f['ops_consumed']} vs table {ops}")
    t14 = t.split("#### 12.4",1)[1].split("#### 12.5",1)[0]
    evs = list(dict.fromkeys(re.findall(r"^\|\s*`(rwb\.[^`]+)`\s*\|", t14, re.M)))
    if sorted(f["events_consumed"]) != sorted(evs): fails.append(f"{sid}: events fragment {f['events_consumed']} vs table {evs}")
    if f["ops_provided"] != [] or f["events_published"] != []: fails.append(f"{sid}: provided/published not empty")
    # citations
    for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
        if c not in ids: fails.append(f"{sid}: cite {c} unresolved")
    # forbidden
    low = t.lower()
    if "jira" in low or "atlassian" in low: fails.append(f"{sid}: tracker reference")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t): fails.append(f"{sid}: email")
    bad = [l for l in lines if "/api/recovery/v1" in l and "DP-13" not in l]
    if bad: fails.append(f"{sid}: monolith base outside DP-13: {bad[0][:90]}")
    for m in re.finditer(r"rwb\.([a-z-]+)\.events\.v1", t):
        if m.group(1) not in SHORTS: fails.append(f"{sid}: bad topic {m.group(0)}")
    for m in re.finditer(r"/api/recovery/([a-z-]+)/v1", t):
        if m.group(1) not in SHORTS: fails.append(f"{sid}: bad base {m.group(0)}")
    for m in re.finditer(r"queue rwb-([a-z-]+)", t):
        if m.group(1) not in SHORTS: fails.append(f"{sid}: bad queue {m.group(0)}")
    # fragment identity
    for k,v in (("id",sid),("epic","RWB-ITG-W2"),("service","integration"),("wt","ITG"),("lane","L-ITG-W2"),("ready","Day 1"),
                ("owner","TechX"),("business_epic",exp["ep"]),("wave",2),("release",exp["rel"]),("legacy",exp["legacy"]),
                ("disposition","Split (rework)"),("H",[]),("C",[]),("I",exp["I"]),("X",[]),("acs",[]),("reqs",exp["reqs"]),
                ("prd_ref","Pending (C1)"),("gaps",[f"CG-B-ITG-W2-06-{sid.split('-')[2]}-1"]),("assumptions",[f"ASM-B-ITG-W2-06-{sid.split('-')[2]}-1"])):
        if f.get(k) != v: fails.append(f"{sid}: fragment {k}={f.get(k)!r} want {v!r}")
    if f["file"] != str(p.relative_to(ROOT)).replace("\\","/"): fails.append(f"{sid}: fragment file path")

print("FAILS", len(fails))
for x in fails[:80]: print(" -", x)
