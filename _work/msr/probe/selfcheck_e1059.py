"""Self-check for the two story files and two fragments of legacy key RWB-E1-059 (WP B-P10-01)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SVC = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)"
APP = SVC / "RWB P10 E1059 APP Case intake agent in shadow [E1b] v1.md"
CON = SVC / "RWB P10 E1059 CON Case intake agent in shadow [E1b] - contract v1.md"
FRAG = ROOT / "_work/msr/fragments"
GAPS = ROOT / "_work/msr/gaps/B-P10-01-E1059.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B-P10-01-E1059.jsonl"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
SLOTS = ["12.1 REST operations provided", "12.2 REST operations consumed", "12.3 Events published",
         "12.4 Events consumed", "12.5 Workflows and activities", "12.6 Schedules", "12.7 Tables owned",
         "12.8 Contract fakes", "12.9 Call-type summary"]

fails = []


def chk(cond, msg):
    if not cond:
        fails.append(msg)


def rows(text):
    head = text.split("### 1.", 1)[0]
    got = [r.strip() for r in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)]
    return [r for r in got if r in META]


def check_story(path, sid, title, meta, acs, tagre):
    chk(path.exists(), f"{path.name}: missing")
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    first = t.splitlines()[0]
    chk(first == f"# {sid} {title}", f"{path.name}: title line is {first!r}")
    chk("SCB Collections and Recovery. Henka Group, 22 November 2026." in t.splitlines()[:4],
        f"{path.name}: header line 1")
    chk("(C) Siam Commercial Bank and Henka Pte Ltd" in t.splitlines()[:5], f"{path.name}: header line 2")
    chk("D-RCV-60" in t.split("### 1.", 1)[0], f"{path.name}: no D-RCV-60 change-log row")
    chk("T3 Code / OpenCode / DeepSeek v4.1 Flash" in t, f"{path.name}: tool line missing")
    chk(rows(t) == META, f"{path.name}: metadata rows wrong: {rows(t)}")
    for k, v in meta.items():
        chk(f"| {k} | {v} |" in t, f"{path.name}: metadata {k} is not {v!r}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    chk([h[1] for h in heads[:19]] == SECTIONS and [int(h[0]) for h in heads[:19]] == list(range(1, 20)),
        f"{path.name}: the 19 headings are not complete and in order: {[h[1] for h in heads[:19]]}")
    scen = [l.strip() for l in t.splitlines() if re.match(r"^\s*Scenario:\s*AC\d+", l)]
    chk(len(scen) == len(acs), f"{path.name}: {len(scen)} scenarios, expected {len(acs)}")
    for l in scen:
        chk(bool(tagre.search(l)), f"{path.name}: scenario line without origin tag: {l[:90]}")
    for a in acs:
        chk(any(l.startswith(f"Scenario: {a} ") for l in scen), f"{path.name}: scenario {a} missing")
    for s in SLOTS:
        chk(s in t, f"{path.name}: subsection {s!r} missing")
    low = t.lower()
    chk("jira" not in low, f"{path.name}: names the issue tracker")
    chk(not re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t), f"{path.name}: email address")
    chk("/api/recovery/v1/" not in t, f"{path.name}: monolith base written out")
    chk("RWB-P10-E1059" in t, f"{path.name}: story id absent from the body")
    return t


app_meta = {
    "Story key": "RWB-P10-E1059-APP",
    "Work type": "APP (App development)",
    "Suggested owner": "TechX (suggested; any team may pick up this story)",
    "Service": "rwb-agent",
    "Service epic": "RWB-SVC-P10",
    "Wave": "1",
    "Business epic": "EP01",
    "Release": "30 November 2026 (tentative)",
    "Legacy key": "RWB-E1-059",
    "Legacy disposition": "Split (rework)",
    "Build status": "Not started",
    "Patterns applied": "DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20",
    "Parallel lane": "L-P10-A",
    "Ready to start": "After RWB-P10-E1058-APP, RWB-P10-TE013-APP",
    "Depends on (build)": "RWB-P10-E1059-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-TE013-CON, RWB-P10-E1058-APP, RWB-P10-TE013-APP",
    "Contract dependencies": "RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1030-CON",
    "Integration dependencies": "None",
    "External dependencies": "None",
    "PRD reference": "Pending (C1)",
    "Status": "Draft (realignment v1)",
}
con_meta = dict(app_meta)
con_meta.update({"Story key": "RWB-P10-E1059-CON", "Work type": "CON (Contract)", "Parallel lane": "CG-W1",
                 "Ready to start": "Day 1", "Depends on (build)": "None", "Contract dependencies": "None"})

APP_ACS = ["AC1", "AC2", "AC3", "AC4", "AC6", "AC7", "AC8"]
CON_ACS = ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7"]
legacy_tag = re.compile(r"\(legacy RWB-[A-Z0-9-]+ AC\d+\)")
new_tag = re.compile(r"\(new, D-RCV-60\)")

ta = check_story(APP, "RWB-P10-E1059-APP", "Case intake agent in shadow [E1b]", app_meta, APP_ACS, legacy_tag)
tc = check_story(CON, "RWB-P10-E1059-CON", "Case intake agent in shadow [E1b]", con_meta, CON_ACS, new_tag)

if ta:
    chk("Scenario: AC5 " not in ta, "APP: owns AC5, which it must not")
    for v in ["2026-11-30", "2026-12-04", "INTAKE-S1", "182", "MISSING_DOCUMENT", "RW-2026-000301",
              "RW-2026-000302", "2026-11-28", "0.9100", "180"]:
        chk(v in ta, f"APP: legacy value {v} missing")
    for tc_id in [f"TC-E1-059-{i:02d}" for i in range(1, 10)]:
        chk(tc_id in ta, f"APP: test case {tc_id} missing")
    chk("| TC-E1-059-01 | AC1, BR1 | Component" in ta or "TC-E1-059-01 | AC1, BR1 | Component" in ta,
        "APP: TC-E1-059-01 not at Component level")
    chk("TC-E1-059-09 | Access | Contract" in ta, "APP: TC-E1-059-09 not at Contract level")

if tc:
    for v in ["/api/recovery/agent/v1", "rwb.agent.AgentRunCompleted.v1", "rwb.agent.events.v1",
              "rwb.agent.events.v1.dlt", "rwb-recovery" if False else "rwb-agent", "intake-summary-v1"]:
        chk(v in tc, f"CON: {v} missing")
    for i in range(1, 9):
        chk(f"TC-P10-E1059-CON-{i:02d}" in tc, f"CON: test case TC-P10-E1059-CON-{i:02d} missing")

# fragments
keys = {"id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
        "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
        "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"}
for name, wid, acs, tcs in (("RWB-P10-E1059-APP", 0, APP_ACS, [f"TC-E1-059-{i:02d}" for i in range(1, 10)]),
                            ("RWB-P10-E1059-CON", 1, CON_ACS, [f"TC-P10-E1059-CON-{i:02d}" for i in range(1, 9)])):
    p = FRAG / f"{name}.json"
    chk(p.exists(), f"{name}.json missing")
    if not p.exists():
        continue
    f = json.loads(p.read_text(encoding="utf-8"))
    chk(set(f) == keys, f"{name}.json: key set differs: {sorted(set(f) ^ keys)}")
    chk(f["id"] == name and f["service"] == "rwb-agent" and f["owner"] == "TechX", f"{name}.json: identity fields")
    chk(f["release"] == "30 November 2026", f"{name}.json: release")
    chk(f["prd_ref"] == "Pending (C1)", f"{name}.json: prd_ref")
    chk([a["id"] for a in f["acs"]] == acs, f"{name}.json: acs {[a['id'] for a in f['acs']]}")
    want = "legacy RWB-E1-059" if wid == 0 else "new, D-RCV-60"
    for a in f["acs"]:
        chk(a["origin"].startswith(want), f"{name}.json: origin {a['origin']}")
        chk(a["text_first_line"].startswith("Given "), f"{name}.json: first line of {a['id']}")
        chk(a["text_first_line"] in (ta if wid == 0 else tc),
            f"{name}.json: first line of {a['id']} is not in the story")
    chk(f["tcs"] == tcs, f"{name}.json: tcs")
    chk((ROOT / f["file"]).exists(), f"{name}.json: file path does not exist")
    chk(f["I"] == [], f"{name}.json: I must be empty")

# gaps and assumptions
gap_ids, asm_ids = set(), set()
gap_keys = {"id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
            "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"}
asm_keys = {"id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"}
for p, ids, req in ((GAPS, gap_ids, gap_keys), (ASMS, asm_ids, asm_keys)):
    chk(p.exists(), f"{p.name}: missing")
    for line in (p.read_text(encoding="utf-8").splitlines() if p.exists() else []):
        if not line.strip():
            continue
        r = json.loads(line)
        chk(set(r) == req, f"{p.name}: {r.get('id')} key set differs: {sorted(set(r) ^ req)}")
        chk(all(r.get(k) not in (None, "") for k in req), f"{p.name}: {r.get('id')} has an empty value")
        ids.add(r["id"])
chk(len(gap_ids) == 2, f"gaps: expected one row per story, got {len(gap_ids)}")
chk(len(asm_ids) == 8, f"assumptions: expected 8 rows, got {len(asm_ids)}")

cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
docs = [APP, CON, FRAG / "RWB-P10-E1059-APP.json", FRAG / "RWB-P10-E1059-CON.json"]
for d in docs:
    if not d.exists():
        continue
    for c in set(cite.findall(d.read_text(encoding="utf-8"))):
        chk(c in gap_ids | asm_ids, f"{d.name}: cites {c} with no jsonl row")

print("FAIL" if fails else "PASS", len(fails))
for f in fails:
    print("-", f)
sys.exit(1 if fails else 0)
