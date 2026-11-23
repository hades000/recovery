import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WP = "B2-S2-012"
APP = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3017 APP Release the collateral after settlement v1.md"
CON = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3017 CON Release the collateral after settlement - contract v1.md"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SEC = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
       "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
       "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]

fails = []
ids = set()

# jsonl rows
for kind, key in (("gaps", {"id", "title", "description", "type", "severity"}), ("assumptions", {"id", "text", "why"})):
    p = ROOT / "_work/msr" / kind / f"{WP}.jsonl"
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        r = json.loads(line)
        miss = key - set(r)
        if miss:
            fails.append(f"{kind}:{n} missing {miss}")
        ids.add(r["id"])

# fragments
for frag in ("RWB-S2-E3017-APP", "RWB-S2-E3017-CON"):
    f = json.loads((ROOT / "_work/msr/fragments" / f"{frag}.json").read_text(encoding="utf-8"))
    for g in f["gaps"] + f["assumptions"]:
        if g not in ids:
            fails.append(f"{frag}: cites {g} with no row")

for p, minid in ((APP, "RWB-S2-E3017-APP"), (CON, "RWB-S2-E3017-CON")):
    t = p.read_text(encoding="utf-8")
    if not p.exists():
        fails.append(f"missing {p}")
        continue
    if not t.startswith(f"# {minid} "):
        fails.append(f"{p.name}: title")
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in t:
        fails.append(f"{p.name}: header")
    if "D-RCV-60" not in t or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        fails.append(f"{p.name}: decision or tool line")
    head = t.split("### 1.", 1)[0]
    got = [r.strip() for r in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M) if r.strip() in META]
    if got != META:
        fails.append(f"{p.name}: metadata rows")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SEC or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fails.append(f"{p.name}: 19 sections")
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", line):
            fails.append(f"{p.name}: AC tag {line.strip()[:60]}")
    for grp in re.finditer(r"\brwb\.([a-z-]+)\.events\.v1\b", t):
        if grp.group(1) not in {"source-data", "integration", "case", "access", "document", "comms", "decision",
                                "payment", "reporting", "agent", "valuation", "treatment", "guarantee", "litigation",
                                "asset", "debtsale", "writeoff", "deviation", "partner"}:
            fails.append(f"{p.name}: bad short {grp.group(0)}")
    for grp in re.finditer(r"/api/recovery/([a-z-]+)/v1\b", t):
        if grp.group(1) != "treatment":
            fails.append(f"{p.name}: bad base {grp.group(0)}")
    if "/api/recovery/v1/" in t:
        fails.append(f"{p.name}: old monolith base")
    for c in set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t)):
        if c not in ids:
            fails.append(f"{p.name}: cites {c} with no row")
    for s in re.findall(r"^#### 12\.(\d) ", t, re.M):
        pass
    if [f"12.{i}" for i in range(1, 10)] != [f"12.{i}" for i in range(1, 10) if f"#### 12.{i} " in t]:
        fails.append(f"{p.name}: 12.1-12.9 tables")
    if "(tentative)" not in t:
        fails.append(f"{p.name}: release not tentative")
    print(p.name, len(t.encode("utf-8")) // 1024, "KB")

print("FAILS:", len(fails))
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
