import re, json, os
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SEC = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
       "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
       "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
files = ["04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4033 APP Rent a held asset to a third party v1.md",
         "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4033 CON Rent a held asset to a third party - contract v1.md"]
ids = set()
for f in ["_work/msr/gaps/B2-S5-024.jsonl", "_work/msr/assumptions/B2-S5-024.jsonl"]:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            ids.add(json.loads(l)["id"])
for p in files:
    t = open(p, encoding="utf-8").read()
    print("==", os.path.basename(p), len(t.encode()), "bytes")
    heads = re.findall(r"(?m)^### (\d+)\. (.+?)\s*$", t)
    print(" sections ok:", [h[1] for h in heads[:19]] == SEC and [int(h[0]) for h in heads[:19]] == list(range(1, 20)))
    pre = t.split("### 1.", 1)[0]
    rows = [r for r in re.findall(r"(?m)^\|\s*([^|]+?)\s*\|", pre)]
    got = [r for r in rows if r in META]
    print(" meta ok:", got == META, len(got))
    bad = [l for l in t.splitlines() if re.match(r"^\s*Scenario:\s*AC\d+", l) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", l)]
    print(" AC tags ok:", not bad)
    cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
    print(" unknown citations:", sorted(cited - ids))
    print(" jira:", bool(re.search(r"(?i)\bjira\b|atlassian\.net", t)), " claude:", bool(re.search(r"(?i)co-authored-by: claude|generated with", t)))
    print(" D-RCV-60:", "D-RCV-60" in t, " tool:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in t)
    print(" old base:", bool(re.search(r"/api/recovery/v1/", t)))
    print(" TCs:", re.findall(r"TC-[A-Z0-9]+-\d{3}-\d{2}(?:-ITG)?", t))
