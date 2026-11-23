"""B-P4-01 verifier: checks the 14 story files the quick run cannot see, plus fragments and registers."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

FOLDER = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P4 rwb-access (Access and authority)"

STORIES = [
 ("RWB-P4-E1022-APP","RWB-P4-E1022-APP.json","Sign-on with SSO, MFA and the first roles","APP","L-P4-A","Day 1","TechX","rwb-access","EP01","30 November 2026","RWB-E1-022","Split (rework)",
  ["DP01","DP03","DP07","DP08","DP11","DP13","DP15","DP19"],
  ["RWB-P4-E1022-CON","RWB-PLT-E1027-CON","RWB-PLT-E1043-CON","RWB-PLT-E1037-CON","RWB-P4-E1037-CON","RWB-PLT-E1044-CON","RWB-PLT-N001-CON"],
  ["RWB-P3-E1043-CON","RWB-P3-E1019-CON"],[], ["RWB-P4-E1022-DB"],
  "RWB P4 E1022 APP Sign-on with SSO, MFA and the first roles v1.md"),
 ("RWB-P4-E1022-CON","RWB-P4-E1022-CON.json","Sign-on with SSO, MFA and the first roles","CON","CG-W1","Day 1","TechX","rwb-access","EP01","30 November 2026","RWB-E1-022","Split (rework)",
  ["DP01","DP03","DP07","DP08","DP11","DP13","DP15","DP19"],[],[],[],[],
  "RWB P4 E1022 CON Sign-on with SSO, MFA and the first roles - contract v1.md"),
 ("RWB-P4-E1022-DB","RWB-P4-E1022-DB.json","Sign-on with SSO, MFA and the first roles","DB","L-P4-S","Day 1","ACE","rwb-access","EP01","30 November 2026","RWB-E1-022","Split (rework)",
  ["DP01","DP03","DP07","DP08","DP11","DP13","DP15","DP19"],[],[],[],[],
  "RWB P4 E1022 DB Sign-on with SSO, MFA and the first roles - ACE DB v1.md"),
 ("RWB-P4-E1037-APP","RWB-P4-E1037-APP.json","Role to permission matrix as data and PDPA field masking by role","APP","L-P4-A","After RWB-P4-E1022-APP","TechX","rwb-access","EP01","30 November 2026","RWB-E1-037","Split (rework)",
  ["DP01","DP02","DP03","DP05","DP06","DP07","DP08","DP10","DP11","DP13","DP15","DP17","DP19"],
  ["RWB-P4-E1037-CON","RWB-PLT-E1027-CON","RWB-PLT-E1042-CON","RWB-PLT-E1043-CON","RWB-PLT-E1037-CON","RWB-PLT-E1071-CON","RWB-PLT-E1044-CON","RWB-PLT-N001-CON","RWB-P4-E1022-APP"],
  ["RWB-P3-E1042-CON","RWB-P3-E1043-CON","RWB-P7-E1027-CON"],[],[],
  "RWB P4 E1037 APP Role to permission matrix as data and PDPA field masking by role v1.md"),
 ("RWB-P4-E1037-CON","RWB-P4-E1037-CON.json","Role to permission matrix as data and PDPA field masking by role","CON","CG-W1","Day 1","TechX","rwb-access","EP01","30 November 2026","RWB-E1-037","Split (rework)",
  ["DP01","DP02","DP03","DP05","DP06","DP07","DP08","DP10","DP11","DP13","DP15","DP17","DP19"],[],[],[],[],
  "RWB P4 E1037 CON Role to permission matrix as data and PDPA field masking by role - contract v1.md"),
 ("RWB-P4-E1039-APP","RWB-P4-E1039-APP.json","Access log into the decision log and break-glass admin","APP","L-P4-A","After RWB-P4-E1022-APP","TechX","rwb-access","EP01","30 November 2026","RWB-E1-039","Split (rework)",
  ["DP01","DP03","DP06","DP07","DP11","DP13","DP17","DP19"],
  ["RWB-P4-E1039-CON","RWB-PLT-E1027-CON","RWB-PLT-E1042-CON","RWB-PLT-E1043-CON","RWB-PLT-N001-CON","RWB-P4-E1022-APP"],
  ["RWB-P3-E1042-CON","RWB-P3-E1043-CON","RWB-P7-E1008-CON","RWB-P7-E1027-CON"],[],["RWB-P4-E1039-DB","RWB-P4-E1039-OPS"],
  "RWB P4 E1039 APP Access log into the decision log and break-glass admin v1.md"),
 ("RWB-P4-E1039-CON","RWB-P4-E1039-CON.json","Access log into the decision log and break-glass admin","CON","CG-W1","Day 1","TechX","rwb-access","EP01","30 November 2026","RWB-E1-039","Split (rework)",
  ["DP01","DP03","DP06","DP07","DP11","DP13","DP17","DP19"],[],[],[],[],
  "RWB P4 E1039 CON Access log into the decision log and break-glass admin - contract v1.md"),
 ("RWB-P4-E1039-DB","RWB-P4-E1039-DB.json","Access log into the decision log and break-glass admin","DB","L-P4-W","Day 1","ACE","rwb-access","EP01","30 November 2026","RWB-E1-039","Split (rework)",
  ["DP01","DP03","DP06","DP07","DP11","DP13","DP17","DP19"],[],[],[],[],
  "RWB P4 E1039 DB Access log into the decision log and break-glass admin - ACE DB v1.md"),
 ("RWB-P4-E1039-OPS","RWB-P4-E1039-OPS.json","Access log into the decision log and break-glass admin","OPS","L-P4-V","Day 1","DEVOPS","rwb-access","EP01","30 November 2026","RWB-E1-039","Split (rework)",
  ["DP01","DP03","DP06","DP07","DP11","DP13","DP17","DP19"],[],[],[],[],
  "RWB P4 E1039 OPS Access log into the decision log and break-glass admin - deployment v1.md"),
 ("RWB-P4-E2019-APP","RWB-P4-E2019-APP.json","Partner identities through the external gateway","APP","L-P4-A","After RWB-P4-E1022-APP, RWB-P4-E1039-APP","TechX","rwb-access","EP02","31 December 2026","RWB-E2-019","Split (rework)",
  ["DP01","DP03","DP05","DP06","DP07","DP08","DP11","DP13","DP15","DP19"],
  ["RWB-P4-E2019-CON","RWB-PLT-E1027-CON","RWB-PLT-E1042-CON","RWB-PLT-E1043-CON","RWB-PLT-E1037-CON","RWB-P4-E1037-CON","RWB-PLT-E1044-CON","RWB-PLT-N001-CON","RWB-P4-E1022-APP","RWB-P4-E1039-APP"],
  ["RWB-P3-E1042-CON","RWB-P3-E1043-CON"],[],["RWB-P4-E2019-INF"],
  "RWB P4 E2019 APP Partner identities through the external gateway v1.md"),
 ("RWB-P4-E2019-CON","RWB-P4-E2019-CON.json","Partner identities through the external gateway","CON","CG-W2","Day 1","TechX","rwb-access","EP02","31 December 2026","RWB-E2-019","Split (rework)",
  ["DP01","DP03","DP05","DP06","DP07","DP08","DP11","DP13","DP15","DP19"],[],[],[],[],
  "RWB P4 E2019 CON Partner identities through the external gateway - contract v1.md"),
 ("RWB-P4-E2019-INF","RWB-P4-E2019-INF.json","Partner identities through the external gateway","INF","L-P4-AM","Day 1","INFRA","rwb-access","EP02","31 December 2026","RWB-E2-019","Split (rework)",
  ["DP01","DP03","DP05","DP06","DP07","DP08","DP11","DP13","DP15","DP19"],[],[],[],[],
  "RWB P4 E2019 INF Partner identities through the external gateway - infrastructure v1.md"),
 ("RWB-P4-AD001-APP","RWB-P4-AD001-APP.json","Map Entra ID groups to Workbench roles","APP","L-P4-A","After RWB-P4-E1022-APP","TechX","rwb-access","EP08","30 June 2027","RWB-AD-001","Split (rework)",
  ["DP03","DP05","DP06","DP13","DP19"],
  ["RWB-P4-AD001-CON","RWB-PLT-E1027-CON","RWB-PLT-E1042-CON","RWB-PLT-N001-CON","RWB-P4-E1022-APP"],
  ["RWB-P3-E1042-CON"],[],[],
  "RWB P4 AD001 APP Map Entra ID groups to Workbench roles v1.md"),
 ("RWB-P4-AD001-CON","RWB-P4-AD001-CON.json","Map Entra ID groups to Workbench roles","CON","CG-W4","Day 1","TechX","rwb-access","EP08","30 June 2027","RWB-AD-001","Split (rework)",
  ["DP03","DP05","DP06","DP13","DP19"],[],[],[],[],
  "RWB P4 AD001 CON Map Entra ID groups to Workbench roles - contract v1.md"),
]
OWNER = {"TechX":"TechX (suggested; any team may pick up this story)",
         "ACE":"ACE team (suggested; any team may pick up this story)",
         "INFRA":"SCB IT infrastructure (suggested; any team may pick up this story)",
         "DEVOPS":"DevOps team (suggested; any team may pick up this story)",
         "QA":"QA team (suggested; any team may pick up this story)"}
WT = {"CON":"Contract","APP":"App development","DB":"ACE DB","INF":"Infrastructure","OPS":"DevOps","ITG":"Integration"}
WT_LABEL = {"CON":"Contract","APP":"App development","DB":"ACE DB","INF":"Infrastructure","OPS":"DevOps","ITG":"Integration"}

fails = []
def meta(t):
    rows = {}
    for m in re.finditer(r"(?m)^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$", t.split("### 1.", 1)[0]):
        rows.setdefault(m.group(1), m.group(2))
    return rows

gaps = R.read_jsonl(ROOT / "_work" / "msr" / "gaps" / "B-P4-01.jsonl")
asms = R.read_jsonl(ROOT / "_work" / "msr" / "assumptions" / "B-P4-01.jsonl")
gids = {g["id"] for g in gaps}
aids = {a["id"] for a in asms}
own = R.read_json(ROOT / "_work" / "msr" / "plan" / "ownership.json", {})

files = []
for (sid, frag, title, wt, lane, ready, owner, svc, bepic, rel, legacy, disp, pats, H, C, I, X, name) in STORIES:
    p = FOLDER / name
    files.append(p)
    if not p.exists():
        fails.append(f"MISSING FILE {name}"); continue
    t = p.read_text(encoding="utf-8")
    if f"# {sid} {title}" not in t.splitlines()[0]:
        fails.append(f"{sid}: title line mismatch: {t.splitlines()[0]}")
    m = meta(t)
    exp = {
      "Story key": sid, "Work type": f"{wt} ({WT_LABEL[wt]})", "Suggested owner": OWNER[owner],
      "Service": svc, "Service epic": "RWB-SVC-P4", "Wave": "", "Business epic": bepic,
      "Release": f"{rel} (tentative)", "Legacy key": legacy, "Legacy disposition": disp,
      "Build status": "Not started", "Patterns applied": ", ".join(pats), "Parallel lane": lane,
      "Ready to start": ready,
      "Depends on (build)": ", ".join(H) if H else "None",
      "Contract dependencies": ", ".join(C) if C else "None",
      "Integration dependencies": ", ".join(I) if I else "None",
      "External dependencies": ", ".join(X) if X else "None",
      "PRD reference": "Pending (C1)", "Status": "Draft (realignment v1)"}
    for k, v in exp.items():
        if k not in m:
            fails.append(f"{sid}: metadata row missing: {k}")
        elif v and m[k].strip() != v:
            fails.append(f"{sid}: {k} = {m[k]!r} expected {v!r}")
    # sections
    heads = re.findall(r"(?m)^### (\d+)\. (.+?)\s*$", t)
    if [h[1] for h in heads[:19]] != R.SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fails.append(f"{sid}: 19 headings not complete/in order")
    # AC tags
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", line):
            fails.append(f"{sid}: AC line without origin tag: {line.strip()[:70]}")
    # section 12 sub-tables 12.1-12.9
    s12 = t.split("### 12.", 1)[1].split("### 13.", 1)[0] if "### 12." in t else ""
    for n in range(1, 10):
        if not re.search(rf"12\.{n}\b", s12):
            fails.append(f"{sid}: section 12 lacks sub-table 12.{n}")
    # DP list present in body
    for dp in pats:
        if not re.search(rf"\b{dp}\b", t):
            fails.append(f"{sid}: pattern {dp} not mentioned in the file")
    # citations resolve
    for c in set(re.findall(r"\b(?:CG|ASM)-(?:B-P4-01|A6)-[A-Za-z0-9]+-\d+\b", t)):
        if c.startswith("CG-") and c not in gids:
            fails.append(f"{sid}: cites {c} with no gap row")
        if c.startswith("ASM-") and c not in aids:
            fails.append(f"{sid}: cites {c} with no assumption row")
    # fragment
    f = R.read_json(ROOT / "_work" / "msr" / "fragments" / frag, {})
    if not f:
        fails.append(f"{sid}: fragment missing")
    else:
        for k in ("id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy",
                  "disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed",
                  "events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"):
            if k not in f:
                fails.append(f"{frag}: key {k} missing")
        if f.get("id") != sid: fails.append(f"{frag}: id mismatch")
        if f.get("H") != H: fails.append(f"{frag}: H mismatch")
        if f.get("C") != C: fails.append(f"{frag}: C mismatch")
        if f.get("X") != X: fails.append(f"{frag}: X mismatch")
        if f.get("lane") != lane: fails.append(f"{frag}: lane mismatch")
        if f.get("ready") != ready: fails.append(f"{frag}: ready mismatch")
        if f.get("owner") != owner: fails.append(f"{frag}: owner mismatch")
        if f.get("prd_ref") != "Pending (C1)": fails.append(f"{frag}: prd_ref mismatch")
        if f.get("legacy") != legacy: fails.append(f"{frag}: legacy mismatch")
        for g in f.get("gaps", []):
            if g not in gids: fails.append(f"{frag}: fragment gap {g} has no row")
        for a in f.get("assumptions", []):
            if a not in aids: fails.append(f"{frag}: fragment asm {a} has no row")
    # service names
    for rx in (r"\brwb\.([a-z-]+)\.events\.v1\b", r"/api/recovery/([a-z-]+)/v1\b"):
        for mm in re.finditer(rx, t):
            if mm.group(1) not in R.SHORTS:
                fails.append(f"{sid}: unknown service name {mm.group(1)}")

print("story files:", len(files), "existing:", sum(p.exists() for p in files))
print("gap rows:", len(gaps), "assumption rows:", len(asms))
print("FAILS:", len(fails))
for x in fails[:60]:
    print(" -", x)
