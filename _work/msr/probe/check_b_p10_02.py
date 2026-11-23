"""Local completeness check for WP B-P10-02 output before the repo checker runs."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SD = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P10 rwb-agent (Agent)"
WORK = ROOT / "_work" / "msr"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECT = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
        "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan",
        "Validation and messages", "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]

STORIES = [
    ("RWB-P10-TE013-APP", "RWB P10 TE013 APP Agent runtime client with fallback v1.md"),
    ("RWB-P10-TE013-CON", "RWB P10 TE013 CON Agent runtime client with fallback - contract v1.md"),
    ("RWB-P10-TE013-OPS", "RWB P10 TE013 OPS Agent runtime client with fallback - deployment v1.md"),
    ("RWB-P10-E2028-APP", "RWB P10 E2028 APP Case intake agent live at L1 [E3a] v1.md"),
    ("RWB-P10-E2028-CON", "RWB P10 E2028 CON Case intake agent live at L1 [E3a] - contract v1.md"),
    ("RWB-P10-E2028-OPS", "RWB P10 E2028 OPS Case intake agent live at L1 [E3a] - deployment v1.md"),
    ("RWB-P10-E2029-APP", "RWB P10 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v1.md"),
    ("RWB-P10-E2029-CON", "RWB P10 E2029 CON Deviation screening agent evaluation and L1 on one segment [E3b] - contract v1.md"),
    ("RWB-P10-E2030-APP", "RWB P10 E2030 APP Legal document agent in shadow on Epic 1 data [E3c] v1.md"),
    ("RWB-P10-E2030-CON", "RWB P10 E2030 CON Legal document agent in shadow on Epic 1 data [E3c] - contract v1.md"),
    ("RWB-P10-E2031-APP", "RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v1.md"),
    ("RWB-P10-E2031-CON", "RWB P10 E2031 CON Agent monitoring dashboard v2 [E3d] - contract v1.md"),
    ("RWB-P10-E2031-OPS", "RWB P10 E2031 OPS Agent monitoring dashboard v2 [E3d] - deployment v1.md"),
]

fails, notes = [], []

# jsonl rows
gap_rows, asm_rows = [], []
for p in sorted((WORK / "gaps").glob("B-P10-02-*.part.jsonl")):
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            gap_rows.append(json.loads(line))
        except Exception as e:
            fails.append(f"{p.name}:{n}: bad json {e}")
for p in sorted((WORK / "assumptions").glob("B-P10-02-*.part.jsonl")):
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            asm_rows.append(json.loads(line))
        except Exception as e:
            fails.append(f"{p.name}:{n}: bad json {e}")

ids = [r.get("id") for r in gap_rows + asm_rows]
dups = {i for i in ids if ids.count(i) > 1}
if dups:
    fails.append(f"duplicate jsonl ids: {sorted(dups)}")
for r in gap_rows:
    miss = {"id", "title", "description", "type", "severity"} - {k for k, v in r.items() if v not in (None, "")}
    if miss:
        fails.append(f"gap {r.get('id')} missing {sorted(miss)}")
for r in asm_rows:
    miss = {"id", "text", "why"} - {k for k, v in r.items() if v not in (None, "")}
    if miss:
        fails.append(f"asm {r.get('id')} missing {sorted(miss)}")
notes.append(f"gap rows {len(gap_rows)}: {[r.get('id') for r in gap_rows]}")
notes.append(f"asm rows {len(asm_rows)}: {[r.get('id') for r in asm_rows]}")

FRAG_KEYS = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
             "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
             "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]

for sid, name in STORIES:
    p = SD / name
    if not p.exists():
        fails.append(f"MISSING story {name}")
        continue
    t = p.read_text(encoding="utf-8")
    lines = t.splitlines()
    if not lines or not lines[0].startswith(f"# {sid} "):
        fails.append(f"{sid}: title line wrong: {lines[0][:70] if lines else '<empty>'}")
    head = "\n".join(lines[:8])
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in head:
        fails.append(f"{sid}: header line missing")
    if "(C) Siam Commercial Bank and Henka Pte Ltd" not in head:
        fails.append(f"{sid}: copyright line missing")
    if "D-RCV-60" not in t:
        fails.append(f"{sid}: no D-RCV-60 change log row")
    if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        fails.append(f"{sid}: tool line missing")
    if "(tentative)" not in t:
        fails.append(f"{sid}: release not tentative")
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
    got = [r for r in rows if r in META]
    if got != META:
        fails.append(f"{sid}: metadata rows: {[r for r in META if r not in got]}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SECT or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fails.append(f"{sid}: 19 headings wrong")
    if len(heads) != 19:
        fails.append(f"{sid}: extra ### headings: {len(heads)}")
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", line):
            fails.append(f"{sid}: AC line without tag: {line.strip()[:70]}")
    if len(re.findall(r"^\s*Scenario:", t, re.M)) == 0:
        fails.append(f"{sid}: no scenarios")
    for n in range(1, 10):
        if not re.search(rf"^#### 12\.{n} ", t, re.M):
            fails.append(f"{sid}: 12.{n} missing")
    tc_block = t.split("### 16. Test cases", 1)[-1].split("### 17.", 1)[0]
    if "| TC ID | Covers | Level | Data |" not in tc_block:
        fails.append(f"{sid}: section 16 header wrong")
    if "/api/recovery/v1/" in t:
        fails.append(f"{sid}: monolith base present")
    low = t.lower()
    for bad in ("jira", "atlassian"):
        if bad in low:
            fails.append(f"{sid}: issue-tracker word '{bad}'")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
        fails.append(f"{sid}: email address")
    # citations resolve
    for c in set(re.findall(r"\b(?:CG|ASM)-B-P10-02-(?:TE013|E2028|E2029|E2030|E2031)-\d+\b", t)):
        if c not in ids:
            fails.append(f"{sid}: cites {c} with no row")
    # fragment
    fp = WORK / "fragments" / f"{sid}.json"
    if not fp.exists():
        fails.append(f"MISSING fragment {fp.name}")
    else:
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            fails.append(f"{fp.name}: bad json {e}")
            continue
        miss = [k for k in FRAG_KEYS if k not in d]
        if miss:
            fails.append(f"{fp.name}: keys missing {miss}")
        if d.get("id") != sid:
            fails.append(f"{fp.name}: id {d.get('id')}")
        if d.get("file") != f"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/{name}":
            fails.append(f"{fp.name}: file path mismatch")
        if d.get("prd_ref") != "Pending (C1)":
            fails.append(f"{fp.name}: prd_ref")
        if d.get("epic") != "RWB-SVC-P10" or d.get("service") != "rwb-agent":
            fails.append(f"{fp.name}: epic/service")
        if d.get("I"):
            fails.append(f"{fp.name}: I dependencies not allowed")
        for g in d.get("gaps", []):
            if g not in ids:
                fails.append(f"{fp.name}: gap {g} has no row")
        for a in d.get("assumptions", []):
            if a not in ids:
                fails.append(f"{fp.name}: asm {a} has no row")
        for a in d.get("acs", []):
            if a.get("id") not in [x for x in re.findall(r"Scenario:\s*(AC\d+)", t)]:
                fails.append(f"{fp.name}: ac {a.get('id')} not in story")

print("\n".join(notes))
if fails:
    print(f"\nFAIL {len(fails)}")
    print("\n".join(fails))
    sys.exit(1)
print("\nALL LOCAL CHECKS PASS")
