"""Structural verifier for WP B-PLT-DB-01 (RWB-PLT-N011-DB, RWB-PLT-NF06-DB). Read only."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
SECS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
        "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan",
        "Validation and messages", "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
FKEYS = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
         "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
         "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]

SLICES = [
    {"id": "RWB-PLT-N011-DB", "legacy": "N011", "wt": "DB", "epic": "RWB-PLT-DB", "lane": "L-PLT-DB-A",
     "business_epic": "NEW", "wave": 0, "ready": "Day 1", "service": "platform", "disposition": "New",
     "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-DB ACE DB schemas and logins/"
             "RWB PLT N011 DB PgBouncer pools, migrator role and grant check - ACE DB v1.md"},
    {"id": "RWB-PLT-NF06-DB", "legacy": "NF-06", "wt": "DB", "epic": "RWB-PLT-DB", "lane": "L-PLT-DB-B",
     "business_epic": "NF", "wave": 0, "ready": "Day 1", "service": "platform", "disposition": "Moved (no impact)",
     "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-DB ACE DB schemas and logins/"
             "RWB PLT NF06 DB Create the 19 rwb_  schemas and logins - ACE DB v1.md"},
]

fails = []


def fail(m):
    fails.append(m)


def rows_of(text):
    return [r.strip() for r in re.findall(r"^\|\s*([^|]+?)\s*\|", text.split("### 1.", 1)[0], re.M)]


gap_ids, asm_ids = set(), set()
for kind, bucket in (("gaps", gap_ids), ("assumptions", asm_ids)):
    p = WORK / kind / "B-PLT-DB-01.jsonl"
    if not p.exists():
        fail(f"{kind} file missing")
        continue
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        bucket.add(r["id"])
        req = ({"id", "title", "description", "type", "severity"} if kind == "gaps"
               else {"id", "text", "why"})
        miss = req - {k for k, v in r.items() if v not in (None, "")}
        if miss:
            fail(f"{r.get('id')}: missing {sorted(miss)}")
        if r.get("wp") != "B-PLT-DB-01":
            fail(f"{r.get('id')}: wp key is {r.get('wp')!r}")

cited = set()
for s in SLICES:
    p = ROOT / s["file"]
    if not p.exists():
        fail(f"missing story file {s['file']}")
        continue
    t = p.read_text(encoding="utf-8")
    if not t.startswith(f"# {s['id']} "):
        fail(f"{s['id']}: title line wrong")
    got = [r for r in rows_of(t) if r in META]
    if got != META:
        fail(f"{s['id']}: metadata rows {got}")
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SECS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fail(f"{s['id']}: headings {[h[1] for h in heads[:19]]}")
    for line in t.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\(new, D-RCV-60\)$", line.strip()):
            fail(f"{s['id']}: untagged AC: {line.strip()[:90]}")
    acs = re.findall(r"^\s*Scenario:\s*(AC\d+)", t, re.M)
    if acs != [f"AC{i}" for i in range(1, len(acs) + 1)]:
        fail(f"{s['id']}: AC numbering {acs}")
    tcs = re.findall(r"^\|\s*(TC-PLT-[A-Z0-9]+-DB-\d{2})\s*\|", t, re.M)
    if not tcs:
        fail(f"{s['id']}: no TC rows")
    if "D-RCV-60" not in t:
        fail(f"{s['id']}: no D-RCV-60 change log")
    if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        fail(f"{s['id']}: no tool line")
    if re.search(r"(?i)\bjira\b|atlassian\.net", t):
        fail(f"{s['id']}: issue-tracker reference")
    cites = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
    cited |= cites
    for c in cites:
        if c not in gap_ids | asm_ids:
            fail(f"{s['id']}: cites {c} with no row")
    frag_p = WORK / "fragments" / f"{s['id']}.json"
    if not frag_p.exists():
        fail(f"{s['id']}: fragment missing")
        continue
    f = json.loads(frag_p.read_text(encoding="utf-8"))
    for k in FKEYS:
        if k not in f:
            fail(f"{s['id']}: fragment key {k} missing")
    extra = set(f) - set(FKEYS)
    if extra:
        fail(f"{s['id']}: fragment extra keys {sorted(extra)}")
    for k in ("id", "epic", "wt", "lane", "business_epic", "wave", "ready", "service", "legacy", "disposition", "file"):
        if f.get(k) != s[k]:
            fail(f"{s['id']}: fragment {k} {f.get(k)!r} != {s[k]!r}")
    if f.get("file", "").replace("\\", "/") != s["file"] or not (ROOT / f.get("file", "")).exists():
        fail(f"{s['id']}: fragment file path")
    if [a["id"] for a in f.get("acs", [])] != acs:
        fail(f"{s['id']}: fragment acs {[a['id'] for a in f.get('acs', [])]} vs {acs}")
    for a in f.get("acs", []):
        if a.get("origin") != "new, D-RCV-60" or not a.get("text_first_line", "").startswith(f"Scenario: {a['id']} "):
            fail(f"{s['id']}: ac object {a}")
        if a.get("text_first_line") not in t:
            fail(f"{s['id']}: ac line not in story: {a.get('text_first_line')[:70]}")
    if f.get("tcs") != tcs:
        fail(f"{s['id']}: fragment tcs {f.get('tcs')} vs {tcs}")
    if f.get("prd_ref") != "Pending (C1)":
        fail(f"{s['id']}: prd_ref")
    for c in f.get("gaps", []) + f.get("assumptions", []):
        if c not in gap_ids | asm_ids:
            fail(f"{s['id']}: fragment cites {c} with no row")
        if c.split("-")[5] != s["legacy"].replace("-", ""):
            fail(f"{s['id']}: fragment row {c} not of this legacy key")
    for c in f.get("gaps", []):
        if c not in t:
            fail(f"{s['id']}: gap {c} not cited in the story")

for c in gap_ids | asm_ids:
    if c not in cited:
        fail(f"row {c} is cited by no story")

print("rows:", len(gap_ids), "gaps,", len(asm_ids), "assumptions")
for m in fails:
    print("FAIL", m)
print("RESULT", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
