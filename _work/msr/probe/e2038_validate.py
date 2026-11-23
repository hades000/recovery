import json, re
from pathlib import Path

base = Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform")
files = [
    base / "RWB PLT E2038 APP Temporal security, codec server and admin audit v1.md",
    base / "RWB PLT E2038 CON Temporal security, codec server and admin audit - contract v1.md",
]
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
for f in files:
    t = f.read_text(encoding="utf-8")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    print(f.name)
    print("  monolith base:", "/api/recovery/v1/" in t)
    print("  queue rwb- unbackticked:", bool(re.search(r"(?<!`)queue rwb-", t)), "| task queue rwb-platform:", "task queue `rwb-platform`" in t)
    print("  platform topic:", "rwb.platform.events" in t)
    print("  sections ok:", [h[1] for h in heads[:19]] == SECTIONS and [int(h[0]) for h in heads[:19]] == list(range(1, 20)))
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
    got = [r for r in rows if r in META]
    print("  metadata order ok:", got == META)
    print("  scenarios:", re.findall(r"^\s*Scenario: (AC\d+).*\((legacy RWB-E2-038 AC\d+|new, D-RCV-60)\)", t, re.M))
    print("  change log:", "D-RCV-60" in t, "| tool line:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in t)
    for m in re.finditer(r"\brwb\.([a-z-]+)\.events\.v1\b", t):
        print("  topic mention:", m.group(0))
    for m in re.finditer(r"/api/recovery/([a-z-]+)/v1\b", t):
        print("  base mention:", m.group(0))

for p in ["_work/msr/fragments/RWB-PLT-E2038-APP.json", "_work/msr/fragments/RWB-PLT-E2038-CON.json"]:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    keys = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
            "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
            "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]
    print(p, "key order ok:", list(d.keys()) == keys, d["id"], "acs", len(d["acs"]), "tcs", len(d["tcs"]),
          "gaps", d["gaps"], "asm", d["assumptions"])

for r in ["_work/msr/gaps/B-PLT-WF-01.jsonl", "_work/msr/assumptions/B-PLT-WF-01.jsonl"]:
    rows = [json.loads(l) for l in Path(r).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(r, [x["id"] for x in rows], "all parse ok")
