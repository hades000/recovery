"""Self-check for WP B2-P1-009 outputs (not the central checker)."""
import json, re, sys
from pathlib import Path

ROOT = Path(".").resolve()
STORY = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM010 APP Migrate documents and extracted fields v1.md"
FRAG = ROOT / "_work/msr/fragments/RWB-P1-DM010-APP.json"
GAPS = ROOT / "_work/msr/gaps/B2-P1-009.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B2-P1-009.jsonl"
LOG = ROOT / "_work/msr/editlog/B2-P1-009.md"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]

fails = []
t = STORY.read_text(encoding="utf-8")

if not t.startswith("# RWB-P1-DM010-APP "):
    fails.append("title line")
if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in t.splitlines()[2]:
    fails.append("header line 1")
if "(C) Siam Commercial Bank and Henka Pte Ltd" not in t.splitlines()[3]:
    fails.append("header line 2")
if "D-RCV-60" not in t or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
    fails.append("change log / tool line")

rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
got = [r for r in rows if r in META]
if got != META:
    fails.append(f"metadata rows: {[m for m in META if m not in got]}")

heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
    fails.append(f"section headings: {[h[1] for h in heads[:19]]}")

for line in t.splitlines():
    if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", line):
        fails.append("AC without origin tag: " + line.strip())

if "(tentative)" not in t:
    fails.append("release not marked tentative")
if re.search(r"\bjira\b|atlassian\.net", t, re.I):
    fails.append("issue tracker reference")
if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
    fails.append("email address")
if "/api/recovery/v1/" in t:
    fails.append("old monolith base")
for m in re.finditer(r"\brwb\.([a-z-]+)\.events\.v1\b", t):
    if m.group(1) != "source-data" and m.group(1) != "document":
        fails.append("unexpected topic service " + m.group(1))
ac_count = len(re.findall(r"^\s*Scenario:", t, re.M))
if ac_count != 2:
    fails.append(f"AC count {ac_count}")

gap_rows = [json.loads(l) for l in GAPS.read_text(encoding="utf-8").splitlines() if l.strip()]
asm_rows = [json.loads(l) for l in ASMS.read_text(encoding="utf-8").splitlines() if l.strip()]
ids = {r["id"] for r in gap_rows} | {r["id"] for r in asm_rows}
for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
    if c not in ids:
        fails.append("unresolved citation " + c)
for r in gap_rows:
    miss = {"id", "title", "description", "type", "severity"} - set(r)
    if miss:
        fails.append(f"gap {r.get('id')} missing {miss}")
for r in asm_rows:
    miss = {"id", "text", "why"} - set(r)
    if miss:
        fails.append(f"asm {r.get('id')} missing {miss}")

frag = json.loads(FRAG.read_text(encoding="utf-8"))
need = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
        "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed", "events_published",
        "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]
miss = [k for k in need if k not in frag]
if miss:
    fails.append(f"fragment missing keys {miss}")
if frag["legacy"] != "RWB-DM-010" or frag["wt"] != "APP" or frag["epic"] != "RWB-SVC-P1":
    fails.append("fragment identity")
if frag["gaps"] != [r["id"] for r in gap_rows]:
    fails.append("fragment gaps do not match the gap file")
if frag["assumptions"] != [r["id"] for r in asm_rows]:
    fails.append("fragment assumptions do not match the assumption file")
if not (ROOT / frag["file"]).exists():
    fails.append("fragment file path")
for a in frag["acs"]:
    if f"Scenario: {a['id']} " not in t:
        fails.append("fragment AC not in story " + a["id"])
for tc in frag["tcs"]:
    if tc not in t:
        fails.append("fragment TC not in story " + tc)

log = LOG.read_text(encoding="utf-8")
if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in log:
    fails.append("edit log tool line")
if "D-RCV-60" not in log:
    fails.append("edit log decision")

print("gap rows:", len(gap_rows), "asm rows:", len(asm_rows), "acs:", ac_count, "tcs:", len(frag["tcs"]))
print("FAILS:", len(fails))
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
