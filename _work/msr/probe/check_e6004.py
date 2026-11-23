import re, pathlib
SEC = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
base = pathlib.Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S6 rwb-debtsale (Debt sale)")
for p in [base / "RWB S6 E6004 APP Take buyer bids v1.md", base / "RWB S6 E6004 CON Take buyer bids - contract v1.md"]:
    t = p.read_text(encoding="utf-8")
    h = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    ok = [x[1] for x in h[:19]] == SEC and [int(x[0]) for x in h[:19]] == list(range(1, 20))
    print(p.name, "sections OK" if ok else ("BAD", h[:21]))
    print("  KB", round(len(t.encode("utf-8")) / 1024, 1), "| none-of markers", t.count("None"))
