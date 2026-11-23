"""Self-check for one story file against the checks C02, C03, C05, C12, C13, C15 and C16.

Usage: python -I "_work/msr/logs/selfcheck.py" "<story file>"
Exit code 0 when every check passes. Read-only.
"""
import re
import sys
from pathlib import Path

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
             "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
SHORTS = {"source-data", "integration", "case", "access", "document", "comms", "decision", "payment", "reporting",
          "agent", "valuation", "treatment", "guarantee", "litigation", "asset", "debtsale", "writeoff", "deviation",
          "partner"}
ID_RE = re.compile(r"^RWB-(P10|P[1-9]|S[1-9]|PLT|ITG)-(E[1-8]\d{3}|TE\d{3}|AD\d{3}|DM\d{3}|ACE\d{3}|NF\d{2}|N\d{3}|W[1-4]J\d{2})-(CON|APP|DB|INF|OPS|ITG)(-[2-9])?$")
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    fails = []

    m = re.match(r"^# (\S+)", text)
    if not m or not ID_RE.match(m.group(1)):
        fails.append("title line must start with a valid story ID")
    head = text.split("### 1.", 1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M)
    got = [r for r in rows if r in META_ROWS]
    if got != META_ROWS:
        fails.append(f"metadata rows missing or out of order; missing {[r for r in META_ROWS if r not in got]}")

    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", text, re.M)
    if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        fails.append("the 19 section headings are not complete and in order")

    for line in text.splitlines():
        if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(rf"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, {DEC})\)", line):
            fails.append(f"AC line without origin tag: {line.strip()[:90]}")

    if re.search(r"(?i)\bjira\b|atlassian\.net", text):
        fails.append("refers to the issue tracker")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", text):
        fails.append("email address in the file")
    head6 = "\n".join(text.splitlines()[:6])
    if "SCB Collections and Recovery. Henka Group," not in head6:
        fails.append("header lines (Template and Rules R8.1) missing")
    if DEC not in text or TOOL not in text:
        fails.append("change-log row with D-RCV-60 and the tool line missing")
    if "| Release |" in text:
        rel = re.search(r"^\|\s*Release\s*\|\s*(.+?)\s*\|$", text, re.M)
        if rel and rel.group(1) not in ("None (new story)",) and "(tentative)" not in rel.group(1):
            fails.append("release date not marked (tentative)")

    for rx, grp in [(r"\brwb\.([a-z-]+)\.events\.v1\b", 1), (r"/api/recovery/([a-z-]+)/v1\b", 1),
                    (r"\bqueue rwb-([a-z-]+)\b", 1)]:
        for mm in re.finditer(rx, text):
            if mm.group(grp) not in SHORTS:
                fails.append(f"unknown service name '{mm.group(grp)}' in {mm.group(0)}")
    if re.search(r"/api/recovery/v1/", text) and "As built (monolith)" not in text:
        fails.append("old monolith API base outside the as-built section")

    for f in fails:
        print("FAIL", f)
    print(f"{path.name}: {'PASS' if not fails else f'{len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
