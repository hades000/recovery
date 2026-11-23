"""B-TECH-06 verify: source -> next version. Read-only."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/B-TECH-06/Recovery Workbench Workflow Engine Design v3.md"
NEW = ROOT / "_work/msr/docs/B-TECH-06/Recovery Workbench Workflow Engine Design v4.md"

def t(p):
    return p.read_text(encoding="utf-8")

s, n = t(SRC), t(NEW)
fails = []

# 1. sections
for h in re.findall(r"^# (.+)$", s, re.M):
    if not re.search(r"^# " + re.escape(h) + r"\s*$", n, re.M):
        fails.append(f"section missing: {h}")

# 2. identifiers and numbers
tok = re.compile(r"\b(?:JOB-\d{2}|E\d-\d{3}|E1-0\d\d|ADR-\d{3}|MSG-P\d-\d{3}|R-[A-Z]{3}-\d{2,3}|DL\d{2}|EV-\d{2}|REQ-[A-Z]+-\d{3}|T\d|SY-[A-Z]+|DT\d\d|DP-\d\d|RWB-[A-Z0-9]+-|LOV-STAGE|NoPackageInForce|temporal\.[a-z.]+|drools\.[a-z.]+|rules\.testcases\.min=\d+|RW-[A-Z]+)\b")
src_tok, new_tok = set(tok.findall(s)), set(tok.findall(n))
fails += [f"token missing in v4: {x}" for x in sorted(src_tok - new_tok)]

num = re.compile(r"\b\d[\d,.]*\b")
fails += [f"number missing in v4: {x}" for x in sorted(set(num.findall(s)) - set(num.findall(n)), key=lambda z: (len(z), z))]

# 3. dates kept, release dates tentative
for d in sorted(set(re.findall(r"\b\d{1,2} (?:November|December) 2026\b", s))):
    if d not in n:
        fails.append(f"date missing: {d}")
for d in ("30 November 2026", "31 December 2026"):
    if f"{d} (tentative)" not in n:
        fails.append(f"release date not marked tentative: {d}")

# 4. header and change log
lines = n.splitlines()
if lines[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append("header line 1")
if lines[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append("header line 2")
if "| Change | v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |" not in n:
    fails.append("change-log row missing")
if s.count("| Change |") != 1:
    fails.append("source Change row count changed")
if "v3, 16 November 2026, D-RCV-36" not in n:
    fails.append("v3 change row not kept")

# 5. realignment must-haves
for need, label in [("workflow kit", "workflow kit"), ("child workflow per stage", "child workflow per stage"),
                    ("Temporal Schedule", "Schedules"), ("rwb-decision", "P7 owner"), ("rwb-litigation", "S4 owner"),
                    ("D-RCV-60", "decision"), ("Version | 4", "version 4")]:
    if need not in n:
        fails.append(f"realignment value missing: {label}")

# 6. citations resolve to jsonl ids
ids = set()
for kind in ("gaps", "assumptions"):
    p = ROOT / f"_work/msr/{kind}/B-TECH-06.jsonl"
    if p.exists():
        ids |= set(re.findall(r'"id":\s*"([^"]+)"', t(p)))
for c in sorted(set(re.findall(r"\b(?:CG|ASM)-B-TECH-06-\d+\b", n))):
    if c not in ids:
        fails.append(f"citation without a jsonl row: {c}")

# 7. no old monolith base, no person-name pattern
if "/api/recovery/v1" in n:
    fails.append("old monolith API base present")
if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", n):
    fails.append("email address present")

print("FAIL" if fails else "PASS")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
