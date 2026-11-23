"""Structural self-check for the five B-ITG-W4-05 story files and their fragments."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
STORIES = {
    "RWB-ITG-E6028-ITG": "E6028",
    "RWB-ITG-E6029-ITG": "E6029",
    "RWB-ITG-E6030-ITG": "E6030",
    "RWB-ITG-E6031-ITG": "E6031",
    "RWB-ITG-E6032-ITG": "E6032",
}
SHORTS = {"source-data", "integration", "case", "access", "document", "comms", "decision", "payment", "reporting",
          "agent", "valuation", "treatment", "guarantee", "litigation", "asset", "debtsale", "writeoff", "deviation",
          "partner"}
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

gap_ids = {json.loads(l)["id"] for l in (WORK / "gaps" / "B-ITG-W4-05.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
asm_ids = {json.loads(l)["id"] for l in (WORK / "assumptions" / "B-ITG-W4-05.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
fails = []

for sid, key in STORIES.items():
    frag_p = WORK / "fragments" / f"{sid}.json"
    if not frag_p.exists():
        fails.append(f"{sid}: fragment missing")
        continue
    frag = json.loads(frag_p.read_text(encoding="utf-8"))
    p = ROOT / frag["file"]
    if not p.exists():
        fails.append(f"{sid}: story file missing at {frag['file']}")
        continue
    t = p.read_text(encoding="utf-8")
    lines = t.splitlines()
    if not re.match(rf"^# {re.escape(sid)} \S", lines[0]):
        fails.append(f"{sid}: bad title line")
    if "SCB Collections and Recovery. Henka Group," not in "\n".join(lines[:6]):
        fails.append(f"{sid}: header line missing")
    if "Siam Commercial Bank and Henka Pte Ltd" not in "\n".join(lines[:6]):
        fails.append(f"{sid}: copyright line missing")
    pre = t.split("### 1.", 1)[0]
    got = [r for r in re.findall(r"^\|\s*([^|]+?)\s*\|", pre, re.M) if r in META]
    if got != META:
        fails.append(f"{sid}: metadata rows wrong/missing: {[m for m in META if m not in got]}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads] != SECTIONS or [int(h[0]) for h in heads] != list(range(1, 20)):
        fails.append(f"{sid}: sections wrong: {[h[1] for h in heads][:20]}")
    for extra in re.findall(r"^### (?!\d+\.).+$", t, re.M):
        fails.append(f"{sid}: extra ### heading {extra[:60]}")
    acs = re.findall(r"^\s*Scenario: AC\d+.*$", t, re.M)
    for a in acs:
        if not re.search(rf"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, {re.escape(DEC)})\)", a):
            fails.append(f"{sid}: AC without origin tag: {a[:90]}")
    facs = [a["id"] for a in frag["acs"]]
    file_ids = [re.match(r"\s*Scenario: (AC\d+)", a).group(1) for a in acs]
    if file_ids != facs:
        fails.append(f"{sid}: AC ids in file {file_ids} vs fragment {facs}")
    if re.search(r"/api/recovery/v1/", t):
        fails.append(f"{sid}: monolith API base present")
    if "As built (monolith)" in t:
        fails.append(f"{sid}: as-built section on a non-preserved story")
    if "(tentative)" not in pre:
        fails.append(f"{sid}: release not tentative")
    if DEC not in pre or TOOL not in pre:
        fails.append(f"{sid}: change log row missing decision or tool")
    if re.search(r"(?i)\bjira\b|atlassian\.net", t):
        fails.append(f"{sid}: issue-tracker reference")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
        fails.append(f"{sid}: email address")
    for rx in (r"\brwb\.([a-z-]+)\.events\.v1\b", r"/api/recovery/([a-z-]+)/v1\b", r"\bqueue rwb-([a-z-]+)\b"):
        for m in re.finditer(rx, t):
            if m.group(1) not in SHORTS:
                fails.append(f"{sid}: unknown short '{m.group(1)}' in {m.group(0)}")
    for c in sorted(set(cite.findall(t)) | set(cite.findall(frag_p.read_text(encoding='utf-8')))):
        if c not in gap_ids and c not in asm_ids:
            fails.append(f"{sid}: cites {c} with no jsonl row")
    for k in ("id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
              "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
              "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"):
        if k not in frag:
            fails.append(f"{sid}: fragment key missing {k}")
    for tc in frag["tcs"]:
        if tc not in t:
            fails.append(f"{sid}: fragment TC {tc} not in the file")
    for op in frag["ops_consumed"]:
        path = op.split(" ", 1)[1]
        if path not in t:
            fails.append(f"{sid}: consumed op not in 12.2: {path}")
    if frag["gaps"] and not all(g in gap_ids for g in frag["gaps"]):
        fails.append(f"{sid}: fragment gap id not in the register")
    if frag["assumptions"] and not all(a in asm_ids for a in frag["assumptions"]):
        fails.append(f"{sid}: fragment assumption id not in the register")
    table = re.search(r"#### 12\.2 REST operations consumed(.*?)#### 12\.3", t, re.S)
    n = len(re.findall(r"^\| (GET|POST|PATCH|PUT|DELETE) \|", table.group(1), re.M)) if table else 0
    if n != len(frag["ops_consumed"]):
        fails.append(f"{sid}: 12.2 rows {n} vs fragment ops {len(frag['ops_consumed'])}")
    print(f"{sid}: {len(lines)} lines, {len(acs)} ACs, {len(frag['tcs'])} TCs, {n} ops")

print()
if fails:
    print("FAIL", len(fails))
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS all five stories and fragments")
