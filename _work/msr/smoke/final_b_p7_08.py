"""Final structural check of the five story files of WP B-P7-08."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P7 rwb-decision (Decision and rules)"
KEY = {"E1073": ("E1", "073", 1, 20), "E2001": ("E2", "001", 2, 10), "E2002": ("E2", "002", 2, 11),
       "E2004": ("E2", "004", 2, 16), "E2006": ("E2", "006", 2, 13)}
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic",
        "Release", "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane",
        "Ready to start", "Depends on (build)", "Contract dependencies", "Integration dependencies",
        "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]

bad = []
for key, (ep, num, ept, last) in KEY.items():
    story = f"RWB-P7-{key}-APP"
    files = [p for p in FOLDER.glob(f"RWB P7 {key} *.md")]
    if len(files) != 1:
        bad.append(f"{story}: found {len(files)} story files")
        continue
    p = files[0]
    t = p.read_text(encoding="utf-8")
    frag = json.loads((ROOT / "_work" / "msr" / "fragments" / f"{story}.json").read_text(encoding="utf-8"))

    head = t.split("### 1.", 1)[0]
    if not t.startswith(f"# {story} "):
        bad.append(f"{story}: title line")
    if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in head or \
       "(C) Siam Commercial Bank and Henka Pte Ltd" not in head:
        bad.append(f"{story}: header lines")
    if "D-RCV-60" not in head or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        bad.append(f"{story}: change-log row or tool line")
    rows = [m.strip() for m in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)]
    if [r for r in rows if r in META] != META:
        bad.append(f"{story}: metadata rows")

    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)[:19]
    if [h[1] for h in heads] != SECTIONS or [int(h[0]) for h in heads] != list(range(1, 20)):
        bad.append(f"{story}: 19 sections")

    acs = re.findall(r"(?m)^\s*Scenario:\s*AC\d+.*$", t)
    if not acs or any("(new, D-RCV-60)" not in a for a in acs):
        bad.append(f"{story}: AC origin tags")
    if frag["acs"]:
        bad.append(f"{story}: fragment acs not empty")

    tcs = {f"TC-{ep}-{num}-{i:02d}" for i in range(1, last + 1)}
    mint = tcs - set(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", t))
    if mint:
        bad.append(f"{story}: missing TCs {sorted(mint)}")
    if set(frag["tcs"]) != tcs:
        bad.append(f"{story}: fragment tcs differ")
    if f"TC-{ep}-{num}-" in t and re.search(rf"TC-{ep}-{num}-\d{{2}}-ITG", t):
        bad.append(f"{story}: unexpected -ITG copy")

    ids = set(re.findall(r"\b(?:CG|ASM)-B-P7-08-[A-Z0-9]+-\d+\b", t))
    known = set()
    for kind in ("gaps", "assumptions"):
        for line in (ROOT / "_work" / "msr" / kind / "B-P7-08.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                known.add(json.loads(line)["id"])
    unres = ids - known
    if unres:
        bad.append(f"{story}: unresolved citations {sorted(unres)}")

    print(f"{story}: ACs={len(acs)} TCs={len(tcs)} cites={len(ids)} fragkeys={len(frag)} file={p.name}")

if bad:
    print("\nFAILURES")
    for b in bad:
        print(" -", b)
    sys.exit(1)
print("\nall five story files pass the structural check")
