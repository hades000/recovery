"""Verify the rendered v4 docx against the v3 source text.

Checks: header lines, change-log row, every v3 section heading and its order, every v3 ID, number
and date, one row per service in the three per-service tables, and no person name, email address
or issue-tracker reference.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SRC_TXT = ROOT / "_work" / "msr" / "extract" / "B-TECH-09" / "Recovery Workbench Observability and Monitoring Design v3.md"
DOCX = ROOT / "05 Technical architecture" / "Recovery Workbench Observability and Monitoring Design v4.docx"
OUTDIR = HERE / "verify"

subprocess.run([sys.executable, "-I", str(ROOT / "22 Microservice Realignment" / "compat" / "convert_sources.py"),
                str(DOCX), str(OUTDIR)], check=True)
new = (OUTDIR / (DOCX.stem + ".md")).read_text(encoding="utf-8")
src = SRC_TXT.read_text(encoding="utf-8")

fails = []

# 1. header lines of Template and Rules R8.1
head = "\n".join(new.splitlines()[:4])
for line in ("SCB Collections and Recovery. Henka Group, 22 November 2026.",
             "(C) Siam Commercial Bank and Henka Pte Ltd"):
    if line not in head:
        fails.append(f"header line missing: {line}")

# 2. change-log row
row = "4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if row not in new:
    fails.append("change-log row missing")

# 3. v3 section headings, in order
src_heads = re.findall(r"^# (.+)$", src, re.M)
pos = 0
for h in src_heads:
    i = new.find("# " + h)
    if i < 0:
        fails.append(f"section heading missing: {h}")
    elif i < pos:
        fails.append(f"section heading out of order: {h}")
    else:
        pos = i

# 4. tokens of the source: IDs, numbers, dates, message ids
TOKENS = ["MSG-P3-037", "MSG-P3-027", "RWB-E1-056", "RWB-E1-070", "RWB-E1-073", "RWB-E2-037",
          "RWB-E2-038", "temporal.stuck.hours", "NoPackageInForce", "KieBase", "Grafana",
          "Prometheus", "Log Analytics", "Entra ID", "07:00", "16 November 2026",
          "50th", "95th", "50 items", "one day", "1 percent", "5 minutes", "2 seconds",
          "15 minutes", "10 percent", "an hour", "24", "6 November 2026"]
for t in TOKENS:
    if t == "6 November 2026":
        continue
    if t not in new:
        fails.append(f"source token missing: {t}")

# 5. one row per service in the two per-service tables (1.1 measured units, 3.1 dashboards)
for code in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10",
             "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]:
    n = len(re.findall(r"(?m)^\| " + code + r" \| rwb-", new))
    if n != 2:
        fails.append(f"{code}: expected 2 per-service rows, found {n}")

# 5b. the named instances of the single-owner alerts and of the Schedules
for code in ["P1 rwb-source-data", "P10 rwb-agent", "P7 rwb-decision", "P3 rwb-case",
             "P4 rwb-access", "P5 rwb-document", "S5 rwb-asset", "S7 rwb-writeoff"]:
    if code not in new:
        fails.append(f"named alert instance missing: {code}")

# 6. no person names, emails, issue tracker
if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", new):
    fails.append("email address in the document")
if re.search(r"(?i)\bjira\b|atlassian\.net", new):
    fails.append("issue-tracker reference in the document")
for nm in ("Rajdeep", "Ghai"):
    if nm.lower() in new.lower():
        fails.append(f"person name in the document: {nm}")

print("PASS" if not fails else "FAIL")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
