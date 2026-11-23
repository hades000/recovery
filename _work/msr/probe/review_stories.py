import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
WP = ROOT / "_work/msr/wp/B-ITG-W2-01.md"
wp = WP.read_text(encoding="utf-8")
slices = []
for line in wp.splitlines():
    s = line.strip()
    if s.startswith('{"id":'):
        slices.append(json.loads(s))

LEG = {
 "RWB-E2-001": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 001 EFS hand over with full history from the COLLINS load v1.md",
 "RWB-E2-002": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 002 ACE plan status on the case v2.md",
 "RWB-E2-003": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 003 Customer s other products on the case v1.md",
 "RWB-E2-004": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 004 Treatment entity and plan timers data model v2.md",
 "RWB-E2-005": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 005 Decision log query API for audit v1.md",
}
FIELDS = ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]

def scen(text):
    return [l.rstrip() for l in text.splitlines() if re.match(r"^\s*Scenario:\s*AC\d+", l)]

for s in slices:
    sid, p = s["id"], ROOT / s["file"]
    t = p.read_text(encoding="utf-8")
    print("=" * 30, sid)
    # metadata checks
    head = t.split("### 1.", 1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)
    checks = {
      "path_ok": p.name == Path(s["file"]).name,
      "title_id": t.splitlines()[0].startswith("# " + sid + " "),
      "header": "SCB Collections and Recovery. Henka Group, 22 November 2026." in t and "(C) Siam Commercial Bank and Henka Pte Ltd" in t,
      "drcv60": "D-RCV-60" in head, "tool": "T3 Code / OpenCode / DeepSeek v4.1 Flash" in t,
      "tentative": "31 December 2026 (tentative)" in t,
      "rows20": len([r for r in rows if r in ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]]) == 20,
      "irow": all(x in head for x in s["I"]),
      "patterns": ", ".join(s["patterns"]) in head,
      "sections": [h[1] for h in re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)][:19],
      "sub12": [f"12.{n}" in t for n in range(1,10)],
    }
    bad = {k: v for k, v in checks.items() if v is False or (isinstance(v, list) and not all(v))}
    print("meta bad:", bad if bad else "none")
    print("scenarios:", len(scen(t)), "| new:", sum("(new, D-RCV-60)" in l for l in scen(t)), "| legacy:", sum("(legacy" in l for l in scen(t)))
    for l in scen(t):
        if not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)$", l):
            print("  BAD TAG:", l[:120])
    # fragment
    f = json.loads((ROOT / "_work/msr/fragments" / f"{sid}.json").read_text(encoding="utf-8"))
    miss = [k for k in FIELDS if k not in f]
    diffs = {k: (f.get(k), s.get(k)) for k in ("epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","reqs","file") if f.get(k) != s.get(k)}
    print("frag missing:", miss or "none", "| diffs:", diffs or "none", "| acs:", len(f["acs"]), "tcs:", len(f["tcs"]), "gaps:", f["gaps"], "asm:", f["assumptions"])
    # legacy TCs present
    absent = [tc for tc in s["tcs_legacy"] if (tc + "-ITG") not in t]
    print("legacy TCs absent:", absent or "none")
    # copied AC verbatim (for E2001)
    if s["acs"]:
        leg = (ROOT / LEG[s["legacy"]]).read_text(encoding="utf-8")
        for ac in s["acs"]:
            m = re.search(rf"^  Scenario: {ac} .*?(?=^  Scenario: |^```)", leg, re.M | re.S)
            blk = [l.rstrip() for l in m.group(0).splitlines()[1:] if l.strip()] if m else []
            m2 = re.search(rf"^  Scenario: {ac} .*?(?=^  Scenario: |^```)", t, re.M | re.S)
            blk2 = [l.rstrip() for l in m2.group(0).splitlines()[1:] if l.strip()] if m2 else []
            print(f"  {ac}: verbatim body {'OK' if blk == blk2 else 'DIFF'} ({len(blk)} lines)")
    # leftover placeholders / banned
    for pat, name in ((r"\bJira\b|atlassian\.net", "jira"), (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "email"), (r"/api/recovery/v1/", "monolith-base"), (r"\bTODO\b|\bTBD\b|XXX", "placeholder")):
        if re.search(pat, t, re.I):
            print("  BANNED:", name)
