"""Self-check for the three RWB-P10-E1063 stories of WP B-P10-01 (D-RCV-60). Read only."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STORY_DIR = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)"
FILES = {
    "APP": STORY_DIR / "RWB P10 E1063 APP Agent monitoring dashboard v1 [E2c] v1.md",
    "CON": STORY_DIR / "RWB P10 E1063 CON Agent monitoring dashboard v1 [E2c] - contract v1.md",
    "OPS": STORY_DIR / "RWB P10 E1063 OPS Agent monitoring dashboard v1 [E2c] - deployment v1.md",
}
TITLE = {
    "APP": "# RWB-P10-E1063-APP Agent monitoring dashboard v1 [E2c]",
    "CON": "# RWB-P10-E1063-CON Agent monitoring dashboard v1 [E2c]",
    "OPS": "# RWB-P10-E1063-OPS Agent monitoring dashboard v1 [E2c] - deployment v1",
}
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
SUBS = ["12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7", "12.8", "12.9"]
GAPS = ROOT / "_work/msr/gaps/B-P10-01-E1063.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B-P10-01-E1063.jsonl"
FRAGS = [ROOT / f"_work/msr/fragments/RWB-P10-E1063-{w}.json" for w in ("APP", "CON", "OPS")]
FKEYS = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
         "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
         "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]

fails = []


def text(p):
    return p.read_text(encoding="utf-8")


ids = set()
for p in (GAPS, ASMS):
    for line in text(p).splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])

for wt, p in FILES.items():
    t = text(p)
    lines = t.splitlines()
    if not lines or lines[0].strip() != TITLE[wt]:
        fails.append(f"{wt}: title line wrong: {lines[0] if lines else '<empty>'}")
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in "\n".join(lines[:4]):
        fails.append(f"{wt}: header line missing")
    if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        fails.append(f"{wt}: tool line missing")
    if "D-RCV-60" not in t:
        fails.append(f"{wt}: no D-RCV-60 change log")
    head = t.split("### 1.", 1)[0]
    got = [r for r in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M) if r in META]
    if got != META:
        fails.append(f"{wt}: metadata rows missing or out of order")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fails.append(f"{wt}: the 19 headings are not complete and in order")
    for line in lines:
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(
                r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)\s*$", line):
            fails.append(f"{wt}: AC line without a trailing origin tag: {line.strip()[:70]}")
    for s in SUBS:
        if not re.search(rf"^#### {re.escape(s)} ", t, re.M):
            fails.append(f"{wt}: sub-table {s} missing")
    if re.search(r"/api/recovery/v1/", t):
        fails.append(f"{wt}: old monolith base present")
    if re.search(r"(?i)\bjira\b|atlassian\.net", t):
        fails.append(f"{wt}: issue tracker named")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
        fails.append(f"{wt}: email address present")
    if re.search(r"Co-Authored-By: Claude|Generated with \[Claude Code\]", t):
        fails.append(f"{wt}: wrong tool attribution")
    if "(tentative)" not in t:
        fails.append(f"{wt}: release not marked tentative")
    for c in sorted(set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))):
        if c not in ids:
            fails.append(f"{wt}: cites {c} with no jsonl row")
    if wt == "APP":
        for n in range(1, 8):
            if f"(legacy RWB-E1-063 AC{n})" not in t:
                fails.append(f"APP: AC{n} not tagged as legacy")
        for n in range(1, 9):
            if f"TC-E1-063-0{n}" not in t:
                fails.append(f"APP: TC-E1-063-0{n} missing")
    if wt == "CON":
        for n in range(1, 7):
            if f"(new, D-RCV-60)" not in t:
                break
        for n in range(1, 7):
            if f"TC-P10-E1063-CON-0{n}" not in t:
                fails.append(f"CON: TC-P10-E1063-CON-0{n} missing")
    if wt == "OPS":
        for n in range(1, 9):
            if f"TC-P10-E1063-OPS-0{n}" not in t:
                fails.append(f"OPS: TC-P10-E1063-OPS-0{n} missing")

frag_ids = set()
for p in FRAGS:
    d = json.loads(text(p))
    missing = [k for k in FKEYS if k not in d]
    if missing:
        fails.append(f"{p.name}: fragment keys missing {missing}")
    if d["release"] != "30 November 2026":
        fails.append(f"{p.name}: release changed")
    if d["prd_ref"] != "Pending (C1)":
        fails.append(f"{p.name}: prd_ref wrong")
    for a in d["acs"]:
        if a["origin"] != "legacy RWB-E1-063 AC" + a["id"][2:] and a["origin"] != "new, D-RCV-60":
            fails.append(f"{p.name}: bad AC origin {a['origin']}")
    for g in d["gaps"]:
        if g not in ids:
            fails.append(f"{p.name}: gap {g} not in jsonl")
    for a in d["assumptions"]:
        if a not in ids:
            fails.append(f"{p.name}: assumption {a} not in jsonl")
    frag_ids.add(d["id"])
    if not Path(ROOT / d["file"]).exists():
        fails.append(f"{p.name}: file path does not exist")

for line in text(GAPS).splitlines():
    if line.strip():
        r = json.loads(line)
        for k in ("id", "title", "description", "type", "severity"):
            if not r.get(k):
                fails.append(f"gap {r.get('id')} missing {k}")
        if r["type"] not in ("Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"):
            fails.append(f"gap {r.get('id')} bad type")
        if r["severity"] not in ("P1", "P2", "P3"):
            fails.append(f"gap {r.get('id')} bad severity")
for line in text(ASMS).splitlines():
    if line.strip():
        r = json.loads(line)
        for k in ("id", "text", "why"):
            if not r.get(k):
                fails.append(f"assumption {r.get('id')} missing {k}")

print("fragments:", sorted(frag_ids))
print("ids:", len(ids))
if fails:
    print("FAIL", len(fails))
    for f in fails:
        print(" -", f)
else:
    print("PASS: all Story B-P10-01 E1063 checks")
