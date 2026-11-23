"""Self-check for WP B-P10-01 key RWB-E1-062 (D-RCV-60). Read-only."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 APP Deviation screening agent in shadow [E2b] v1.md"
CON = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 CON Deviation screening agent in shadow [E2b] - contract v1.md"
FRAG_APP = ROOT / "_work/msr/fragments/RWB-P10-E1062-APP.json"
FRAG_CON = ROOT / "_work/msr/fragments/RWB-P10-E1062-CON.json"
GAPS = ROOT / "_work/msr/gaps/B-P10-01-E1062.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B-P10-01-E1062.jsonl"

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
             "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
SUB12 = ["12.1 REST operations provided", "12.2 REST operations consumed", "12.3 Events published", "12.4 Events consumed",
         "12.5 Workflows and activities", "12.6 Schedules", "12.7 Tables owned", "12.8 Contract fakes",
         "12.9 Call-type summary"]
FRAG_KEYS = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
             "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed", "events_published",
             "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]

fails = []
notes = []


def t(p):
    return Path(p).read_text(encoding="utf-8")


def check_story(path, story_id, title, acs_expected, ac_origin):
    text = t(path)
    lines = text.splitlines()
    if lines[0] != f"# {story_id} {title}":
        fails.append(f"{path.name}: title line is {lines[0]!r}")
    head = "\n".join(lines[:6])
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in head:
        fails.append(f"{path.name}: R8.1 header line 1 missing")
    if "(C) Siam Commercial Bank and Henka Pte Ltd" not in head:
        fails.append(f"{path.name}: R8.1 header line 2 missing")
    if "D-RCV-60" not in text.split("### 1.")[0]:
        fails.append(f"{path.name}: no change-log row naming D-RCV-60")
    if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in text:
        fails.append(f"{path.name}: tool line missing")
    before = text.split("### 1.", 1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", before, re.M)
    got = [r for r in rows if r in META_ROWS]
    if got != META_ROWS:
        fails.append(f"{path.name}: metadata rows wrong: {got}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", text, re.M)
    got_s = [h[1] for h in heads[:19]]
    got_n = [int(h[0]) for h in heads[:19]]
    if got_s != SECTIONS or got_n != list(range(1, 20)):
        fails.append(f"{path.name}: 19 sections wrong: {got_s}")
    if len(heads) != 19:
        fails.append(f"{path.name}: extra level-3 headings: {heads[19:]}")
    for name in SUB12:
        if f"#### {name}" not in text:
            fails.append(f"{path.name}: sub-table missing: {name}")
    scen = [l.strip() for l in lines if re.match(r"^\s*Scenario:\s*AC\d+", l)]
    if not scen:
        fails.append(f"{path.name}: no Scenario line")
    for s in scen:
        if not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)$", s):
            fails.append(f"{path.name}: Scenario without origin tag: {s[:70]}")
    ids = [re.match(r"Scenario: (AC\d+)", s).group(1) for s in scen]
    if ids != acs_expected:
        fails.append(f"{path.name}: AC ids {ids} != {acs_expected}")
    for s in scen:
        if ac_origin == "legacy" and not re.search(r"\(legacy RWB-E1-062 AC\d+\)$", s):
            fails.append(f"{path.name}: legacy origin missing: {s[:60]}")
        if ac_origin == "new" and not s.endswith("(new, D-RCV-60)"):
            fails.append(f"{path.name}: new origin missing: {s[:60]}")
    low = text.lower()
    for bad in ("jira", "atlassian.net", "/api/recovery/v1/"):
        if bad in low:
            fails.append(f"{path.name}: forbidden string {bad!r}")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", text):
        fails.append(f"{path.name}: email address")
    if "As built (monolith)" in text:
        fails.append(f"{path.name}: preserved heading on a non-preserved story")
    return text


def check_fragment(path, story_id, wt, lane, ready, acs, tcs, gaps, asms, file_path):
    f = json.loads(t(path))
    if list(f.keys()) != FRAG_KEYS:
        fails.append(f"{path.name}: keys {list(f.keys())}")
    if f["id"] != story_id or f["wt"] != wt or f["lane"] != lane or f["ready"] != ready:
        fails.append(f"{path.name}: id/wt/lane/ready mismatch")
    if f["owner"] != "TechX" or f["release"] != "30 November 2026" or f["service"] != "rwb-agent":
        fails.append(f"{path.name}: owner/release/service mismatch")
    if f["epic"] != "RWB-SVC-P10" or f["business_epic"] != "EP01" or f["wave"] != 1:
        fails.append(f"{path.name}: epic/business epic/wave mismatch")
    if f["legacy"] != "RWB-E1-062" or f["disposition"] != "Split (rework)":
        fails.append(f"{path.name}: legacy/disposition mismatch")
    if f["prd_ref"] != "Pending (C1)":
        fails.append(f"{path.name}: prd_ref")
    if f["file"] != file_path:
        fails.append(f"{path.name}: file path mismatch")
    if [a["id"] for a in f["acs"]] != acs:
        fails.append(f"{path.name}: acs")
    for a in f["acs"]:
        if set(a.keys()) != {"id", "origin", "text_first_line"}:
            fails.append(f"{path.name}: ac entry keys")
    if f["tcs"] != tcs:
        fails.append(f"{path.name}: tcs")
    if f["gaps"] != gaps:
        fails.append(f"{path.name}: gaps")
    if f["assumptions"] != asms:
        fails.append(f"{path.name}: assumptions")
    for k in ("H", "C", "I", "X", "reqs", "ops_provided", "ops_consumed", "events_published", "events_consumed", "workflows"):
        if not isinstance(f[k], list):
            fails.append(f"{path.name}: {k} not a list")
    return f


app_acs = ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7", "AC8", "AC9"]
con_acs = ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7"]
app_tcs = ["TC-E1-062-10", "TC-E1-062-01", "TC-E1-062-02", "TC-E1-062-03", "TC-E1-062-04",
           "TC-E1-062-05", "TC-E1-062-06", "TC-E1-062-07", "TC-E1-062-08", "TC-E1-062-09"]
con_tcs = [f"TC-P10-E1062-CON-0{n}" for n in range(1, 9)]

app_text = check_story(APP, "RWB-P10-E1062-APP", "Deviation screening agent in shadow [E2b]", app_acs, "legacy")
con_text = check_story(CON, "RWB-P10-E1062-CON", "Deviation screening agent in shadow [E2b]", con_acs, "new")

# legacy values the brief fixes
for v in ["RW-2026-000401", "RW-2026-000402", "RW-2026-000403", "RW-2026-000404", "DEATH_CERTIFICATE",
          "D-1001", "R-DEV-04", "RW-FRAUD", "RW-TEAMMGR", "2026-11-25", "2026-11-27", "0.72", "EV-16", "X9",
          "61 seconds", "SCREEN-S1", "screen", "0.9000", "0.7500"]:
    needle = v if v != "screen" else "SCREEN-S1"
    if needle not in app_text:
        fails.append(f"APP: legacy value missing: {needle}")
if "sample size 200" not in app_text:
    fails.append("APP: sample size 200 missing")
if "18 true positives, 2 false positives and 6 false negatives" not in app_text:
    fails.append("APP: X6 counts missing")
if "the 30 days" not in app_text:
    fails.append("APP: 30 days missing")
for v in ["confidence floor 0.80", "prompt \"PR1\"", "mode \"SHADOW\"", "R-DEV-02 to R-DEV-06"]:
    if v not in app_text:
        fails.append(f"APP: background value missing: {v}")

# legacy TCs and levels on the APP story
for tc in app_tcs:
    if tc not in app_text:
        fails.append(f"APP: legacy TC missing: {tc}")
sec16 = app_text.split("### 16. Test cases", 1)[1].split("### 17.", 1)[0]
rows16 = [l for l in sec16.splitlines() if l.startswith("| TC-E1-062-")]
if len(rows16) != 10:
    fails.append(f"APP: section 16 rows {len(rows16)} != 10")
if "| System |" in sec16:
    fails.append("APP: legacy Level value 'System' not mapped")
levels = {}
for l in rows16:
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if len(cells) == 4:
        levels[cells[0]] = cells[2]
    else:
        fails.append(f"APP: section 16 row not 4 columns: {l[:60]}")
if levels.get("TC-E1-062-10") != "Contract":
    fails.append(f"APP: TC-E1-062-10 level {levels.get('TC-E1-062-10')}")
for tc in app_tcs:
    if tc == "TC-E1-062-10":
        continue
    if levels.get(tc) != "Component":
        fails.append(f"APP: {tc} level {levels.get(tc)} != Component")
allowed_levels = {"Unit", "Component", "Contract", "Integration", "End to end", "NFR"}
for tc, lv in levels.items():
    if lv not in allowed_levels:
        fails.append(f"APP: {tc} level {lv!r} outside the §R7.2 list")
for tc in con_tcs:
    if tc not in con_text:
        fails.append(f"CON: own TC missing: {tc}")

# fragments
app_f = check_fragment(FRAG_APP, "RWB-P10-E1062-APP", "APP", "L-P10-A",
                       "After RWB-P10-E1058-APP, RWB-P10-TE013-APP", app_acs, app_tcs,
                       ["CG-B-P10-01-E1062-1"],
                       [f"ASM-B-P10-01-E1062-{n}" for n in range(1, 11)],
                       "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 APP Deviation screening agent in shadow [E2b] v1.md")
con_f = check_fragment(FRAG_CON, "RWB-P10-E1062-CON", "CON", "CG-W1", "Day 1", con_acs, con_tcs,
                       ["CG-B-P10-01-E1062-2"],
                       ["ASM-B-P10-01-E1062-1", "ASM-B-P10-01-E1062-2", "ASM-B-P10-01-E1062-3",
                        "ASM-B-P10-01-E1062-4", "ASM-B-P10-01-E1062-6", "ASM-B-P10-01-E1062-7",
                        "ASM-B-P10-01-E1062-9", "ASM-B-P10-01-E1062-10"],
                       "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 CON Deviation screening agent in shadow [E2b] - contract v1.md")
if app_f["H"] != ["RWB-P10-E1062-CON", "RWB-PLT-E1072-CON", "RWB-PLT-E1042-CON", "RWB-PLT-E1043-CON",
                  "RWB-PLT-TE006-CON", "RWB-PLT-E1044-CON", "RWB-PLT-N001-CON", "RWB-P10-TE013-CON",
                  "RWB-P10-E1058-APP", "RWB-P10-TE013-APP"]:
    fails.append("APP fragment: H list")
if app_f["C"] != ["RWB-P3-E1042-CON", "RWB-P3-E1043-CON"]:
    fails.append("APP fragment: C list")
if con_f["H"] or con_f["C"] or con_f["I"] or con_f["X"]:
    fails.append("CON fragment: H/C/I/X must be empty")
if len(app_f["acs"]) != 9 or len(con_f["acs"]) != 7:
    fails.append("fragment acs count")

# each AC first line must exist in its story text
for a in app_f["acs"] + con_f["acs"]:
    src = app_text if a["id"] in app_acs and a["origin"].startswith("legacy") else con_text
    if a["text_first_line"] not in src:
        fails.append(f"fragment acs: first line not in story: {a['text_first_line'][:60]}")

# metadata level checks on the two stories
app_head = app_text.split("### 1.", 1)[0]
for row, want in [("Work type", "APP (App development)"), ("Suggested owner", "TechX (suggested; any team may pick up this story)"),
                  ("Release", "30 November 2026 (tentative)"), ("Legacy key", "RWB-E1-062"),
                  ("Legacy disposition", "Split (rework)"), ("Build status", "Not started"),
                  ("Patterns applied", "DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20"),
                  ("Parallel lane", "L-P10-A"), ("Ready to start", "After RWB-P10-E1058-APP, RWB-P10-TE013-APP"),
                  ("Integration dependencies", "None"), ("External dependencies", "None"),
                  ("PRD reference", "Pending (C1)"), ("Status", "Draft (realignment v1)")]:
    if f"| {row} | {want} |" not in app_head:
        fails.append(f"APP: metadata row {row} != {want!r}")
con_head = con_text.split("### 1.", 1)[0]
for row, want in [("Work type", "CON (Contract)"), ("Parallel lane", "CG-W1"), ("Ready to start", "Day 1"),
                  ("Depends on (build)", "None"), ("Contract dependencies", "None"),
                  ("Release", "30 November 2026 (tentative)")]:
    if f"| {row} | {want} |" not in con_head:
        fails.append(f"CON: metadata row {row} != {want!r}")

# gaps and assumptions
gap_rows = [json.loads(l) for l in t(GAPS).splitlines() if l.strip()]
asm_rows = [json.loads(l) for l in t(ASMS).splitlines() if l.strip()]
GAP_KEYS = ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
            "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
ASM_KEYS = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]
for r in gap_rows:
    if list(r.keys()) != GAP_KEYS:
        fails.append(f"gap {r.get('id')}: keys {list(r.keys())}")
    if r.get("type") not in ("Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"):
        fails.append(f"gap {r['id']}: type")
    if r.get("severity") not in ("P1", "P2", "P3"):
        fails.append(f"gap {r['id']}: severity")
    if r.get("wp") != "B-P10-01":
        fails.append(f"gap {r['id']}: wp")
for r in asm_rows:
    if list(r.keys()) != ASM_KEYS:
        fails.append(f"asm {r.get('id')}: keys {list(r.keys())}")
    if r.get("confidence") not in ("High", "Medium", "Low"):
        fails.append(f"asm {r['id']}: confidence")
    if r.get("wp") != "B-P10-01":
        fails.append(f"asm {r['id']}: wp")
known = {r["id"] for r in gap_rows} | {r["id"] for r in asm_rows}
if len([g for g in gap_rows if g["id"].startswith("CG-B-P10-01-E1062-")]) != 2:
    fails.append("gaps: expected two CG rows")
if len([a for a in asm_rows if a["id"].startswith("ASM-B-P10-01-E1062-")]) != 10:
    fails.append("assumptions: expected ten ASM rows")
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
for name, text in (("APP", app_text), ("CON", con_text), ("frag-app", t(FRAG_APP)), ("frag-con", t(FRAG_CON))):
    for c in sorted(set(cite.findall(text))):
        if c not in known:
            fails.append(f"{name}: cites {c} with no jsonl row")
# every gap and asm row must be cited somewhere
for r in gap_rows + asm_rows:
    if r["id"] not in app_text + con_text + t(FRAG_APP) + t(FRAG_CON):
        fails.append(f"{r['id']}: not cited in any output")

print("APP lines", len(app_text.splitlines()), "CON lines", len(con_text.splitlines()))
print("gaps", len(gap_rows), "assumptions", len(asm_rows))
if fails:
    print("FAIL", len(fails))
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS: all self-checks green")
