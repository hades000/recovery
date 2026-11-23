import io, json, re, os

ROOT = os.getcwd()
APP = "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 APP Sell a post charge-off population v1.md"
CON = "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 CON Sell a post charge-off population - contract v1.md"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]

for p in (APP, CON):
    t = io.open(p, encoding="utf-8").read()
    print("==", os.path.basename(p), len(t.encode("utf-8")), "bytes")
    m = re.match(r"^# (\S+)", t)
    print("title:", m.group(1) if m else "MISSING")
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
    got = [r for r in rows if r in META]
    print("meta ok:", got == META, [r for r in META if r not in got])
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    print("sections ok:", [h[1] for h in heads[:19]] == SECTIONS and [int(h[0]) for h in heads[:19]] == list(range(1, 20)))
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", line):
            print("BAD AC LINE:", line)
    for n in range(1, 10):
        if ("#### 12.%d" % n) not in t:
            print("missing 12.%d" % n)
    for bad in ("/api/recovery/v1/", "jira", "Jira", "Atlassian"):
        if bad in t:
            print("forbidden:", bad)
    print("D-RCV-60:", "D-RCV-60" in t, "| tentative:", "(tentative)" in t)

# legacy fidelity
leg = io.open("04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md", encoding="utf-8").read()
start = leg.index("## RWB-E6-028")
blk = leg[start:start + 6000]
g = blk.split("```gherkin", 1)[1].split("```", 1)[0]
leg_lines = [l.rstrip() for l in g.splitlines() if l.strip()]
app = io.open(APP, encoding="utf-8").read()
appg = app.split("```gherkin", 1)[1].split("```", 1)[0]
app_lines = [l.rstrip() for l in appg.splitlines() if l.strip()]
missing = [l for l in leg_lines if l not in app_lines]
print("legacy lines kept:", len(leg_lines), "missing:", missing)
extra = [l for l in app_lines if l not in leg_lines]
print("added lines:", len(extra))
for e in extra:
    print("  +", e)

# json
for f in ("_work/msr/fragments/RWB-S7-E6028-APP.json", "_work/msr/fragments/RWB-S7-E6028-CON.json"):
    d = json.load(io.open(f, encoding="utf-8"))
    print(f, "ok", d["id"], len(d["acs"]), len(d["tcs"]))
ids = set()
for f in ("_work/msr/gaps/B2-S7-016.jsonl", "_work/msr/assumptions/B2-S7-016.jsonl"):
    n = 0
    for line in io.open(f, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        ids.add(o["id"])
        n += 1
    print(f, n, "rows")
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
for p in (APP, CON, "_work/msr/fragments/RWB-S7-E6028-APP.json", "_work/msr/fragments/RWB-S7-E6028-CON.json"):
    for c in sorted(set(cite.findall(io.open(p, encoding="utf-8").read()))):
        if c not in ids:
            print("UNRESOLVED", p, c)
print("citations ok")
