"""Verify the next version against the source text: IDs, numbers, dates, sections, header."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/B-TECH-07/Recovery Workbench Rules Engine Design v3.md"
OUT = ROOT / "_work/msr/docs/B-TECH-07/Recovery Workbench Rules Engine Design v4.md"

src = SRC.read_text(encoding="utf-8")
out = OUT.read_text(encoding="utf-8")
fails = []

# 1. Tokens that carry a digit must survive (IDs, DF-REFs, numbers, version labels, times).
tok = re.compile(r"[A-Za-z0-9][A-Za-z0-9.\-]*\d[A-Za-z0-9.\-]*")
missing = sorted({t for t in tok.findall(src) if t not in out})
if missing:
    fails.append(f"tokens with a digit missing from v4: {missing}")

# 2. Dates of the source, plus the new ones.
for d in ["16 November 2026", "30 November 2026", "31 December 2026"]:
    if d not in out:
        fails.append(f"date missing: {d}")

# 3. Section headings: every source heading present, in order.
heads = lambda t: [h.strip() for h in re.findall(r"(?m)^#+ (.+)$", t)]
sh, oh = heads(src), heads(out)
pos = 0
for h in sh:
    while pos < len(oh) and oh[pos] != h:
        pos += 1
    if pos == len(oh):
        fails.append(f"source heading missing or out of order: {h}")
    else:
        pos += 1

# 4. Table rows: every source table row's first cell survives.
for row in re.findall(r"(?m)^\| ([^|]+) \|", src):
    c = row.strip()
    if c and c not in ("Element", "Route set", "Epic", "Column", "From", "Check", "Entity", "Role", "Story", "Item") and f"| {c} |" not in out:
        fails.append(f"table row first cell missing: {c}")

# 5. Header per Template and Rules R8.1, change-log row, tentative releases.
lines = out.splitlines()
if lines[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append("line 1 is not the R8.1 header")
if lines[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append("line 2 is not the R8.1 header")
if "4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in out:
    fails.append("change-log row missing")
for d in ["30 November 2026", "31 December 2026"]:
    if f"{d} (tentative)" not in out:
        fails.append(f"release date not marked tentative: {d}")

# 6. Register citations resolve to a row of this WP.
ids = set()
for kind in ("gaps", "assumptions"):
    p = ROOT / "_work/msr" / kind / "B-TECH-07.jsonl"
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                ids.add(re.search(r'"id":\s*"([^"]+)"', l).group(1))
for c in sorted(set(re.findall(r"\b(?:CG|ASM)-B-TECH-07-\d+\b", out))):
    if c not in ids:
        fails.append(f"citation with no register row: {c}")

# 7. Words that must not appear.
for bad in ("Jira", "jira", "atlassian"):
    if bad in out:
        fails.append(f"forbidden word in v4: {bad}")

print("PASS" if not fails else "FAIL")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
