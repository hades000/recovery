"""Ad-hoc verification for WP B-PLT-LIB-01 stories (scratch; not a deliverable). Run: python -I this.py"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
ENV = "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries"

IDS = ["RWB-PLT-N009-APP", "RWB-PLT-N009-CON", "RWB-PLT-E1027-APP", "RWB-PLT-E1027-CON",
       "RWB-PLT-E1037-APP", "RWB-PLT-E1037-CON", "RWB-PLT-E1042-APP", "RWB-PLT-E1042-CON",
       "RWB-PLT-E1042-OPS", "RWB-PLT-E1043-APP", "RWB-PLT-E1043-CON"]

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SEC = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
       "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
       "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
SHORTS = {"source-data", "integration", "case", "access", "document", "comms", "decision", "payment", "reporting",
          "agent", "valuation", "treatment", "guarantee", "litigation", "asset", "debtsale", "writeoff", "deviation", "partner"}

fails = []

def note(i, m):
    fails.append(f"{i}: {m}")

ids = set()
for p in list((WORK / "gaps").glob("*.jsonl")) + list((WORK / "assumptions").glob("*.jsonl")):
    for line in p.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            ids.add(json.loads(line)["id"])
        except Exception:
            pass
for p in (WORK / "smoke" / "regs").glob("B-PLT-LIB-01-*.jsonl"):
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])

files = []
for i in IDS:
    fr = WORK / "fragments" / f"{i}.json"
    if not fr.exists():
        note(i, "fragment missing")
        continue
    d = json.loads(fr.read_text(encoding="utf-8"))
    f = ROOT / d["file"]
    files.append(f)
    if not f.exists():
        note(i, "story file missing")
        continue
    t = f.read_text(encoding="utf-8")
    # header
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in t:
        note(i, "header line missing")
    if "D-RCV-60" not in t or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        note(i, "change log / tool line missing")
    # title + metadata
    if not t.startswith(f"# {i} "):
        note(i, "title line must be '# <id> <title>'")
    head = t.split("### 1.", 1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)
    got = [r for r in rows if r in META]
    if got != META:
        note(i, f"metadata rows wrong: {[r for r in META if r not in got]}")
    # sections
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SEC or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        note(i, "19 section headings wrong")
    # AC tags
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and "(new, D-RCV-60)" not in line and not re.search(r"\(legacy RWB-\S+ AC\d+\)", line):
            note(i, f"AC without tag: {line.strip()[:60]}")
    # fragment AC first lines
    for a in d.get("acs", []):
        if a["text_first_line"] not in t:
            note(i, f"fragment AC first line not in file: {a['text_first_line'][:60]}")
    # tcs present
    for tc in d.get("tcs", []):
        if tc not in t:
            note(i, f"TC not in file: {tc}")
    # forbidden
    low = t.lower()
    for bad in ("atlassian", "jira", "rwb.platform", "/api/recovery/v1/", "queue rwb-platform", "platform/v1"):
        if bad in low:
            note(i, f"forbidden string: {bad}")
    # service shorts
    for rx, g in ((r"rwb\.([a-z-]+)\.events\.v1", 1), (r"/api/recovery/([a-z-]+)/v1", 1), (r"queue rwb-([a-z-]+)", 1)):
        for m in re.finditer(rx, t):
            if m.group(g) not in SHORTS:
                note(i, f"unknown short '{m.group(g)}' in {m.group(0)}")
    # 12.x tables
    for n in range(1, 10):
        if f"#### 12.{n}" not in t:
            note(i, f"12.{n} missing")
    # citations resolve
    for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
        if c not in ids:
            note(i, f"citation does not resolve: {c}")
    # metadata vs fragment
    def cell(label):
        m = re.search(rf"^\|\s*{re.escape(label)}\s*\|\s*(.+?)\s*\|$", head, re.M)
        return m.group(1) if m else ""
    if cell("Service") != "platform":
        note(i, "service must be platform")
    if cell("Service epic") != d["epic"]:
        note(i, "epic mismatch with fragment")
    if cell("Parallel lane") != d["lane"]:
        note(i, "lane mismatch with fragment")
    rel = cell("Release")
    if d["release"] and not rel.startswith(d["release"]):
        note(i, f"release mismatch: {rel}")
    if not d["release"] and rel != "None (new story)":
        note(i, f"release should be 'None (new story)': {rel}")
    if "(tentative)" not in rel and d["release"]:
        note(i, "release not marked (tentative)")
    if cell("Status") != "Draft (realignment v1)":
        note(i, "status wrong")
    if cell("PRD reference") != "Pending (C1)":
        note(i, "prd reference wrong")
    # fragment H/C present in metadata rows
    for h in d.get("H", []):
        if h not in cell("Depends on (build)"):
            note(i, f"H {h} not in metadata")
    for c in d.get("C", []):
        if c not in cell("Contract dependencies"):
            note(i, f"C {c} not in metadata")

print("files checked:", len(files))
print("FAILS:", len(fails))
for x in fails:
    print(" -", x)
