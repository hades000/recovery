"""Scratch check: citations resolve, id sets are complete and consistent, no forbidden strings."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PRD = ROOT / "03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md"
text = PRD.read_text(encoding="utf-8")

ids = set()
for kind in ("gaps", "assumptions"):
    for p in (ROOT / "_work/msr" / kind).glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["id"])

cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
cited = sorted(set(cite.findall(text)))
bad = [c for c in cited if c not in ids]
print("cited", len(cited), "unresolved", bad)

# id sets defined in the document
def seq(prefix, n):
    return [f"{prefix}-{i:03d}" for i in range(1, n + 1)]

caps = sorted(set(re.findall(r"CAP-S6-\d{3}", text)))
frs = sorted(set(re.findall(r"FR-S6-\d{3}", text)))
nfrs = sorted(set(re.findall(r"NFR-S6-\d{3}", text)))
acs = sorted(set(re.findall(r"AC-S6-\d{3}\b", text)))
print("CAP", len(caps), caps == seq("CAP-S6", 17))
print("FR", len(frs), frs == seq("FR-S6", 33))
print("NFR", len(nfrs), nfrs == seq("NFR-S6", 31))
print("AC", len(acs), acs == seq("AC-S6", 22))

# every FR used in section 11.1/11.2 exists and every FR appears in a trace row
tr = text.split("## 11.2 Requirement trace summary", 1)[1].split("## 11.3", 1)[0]
missing = [f for f in frs if f not in tr]
print("FR missing from trace summary:", missing)

# each FR row in section 6 has 8 pipe-separated columns worth of cells
sec6 = text.split("# 6. Functional requirements", 1)[1].split("# 7. Non-functional", 1)[0]
rows = [l for l in sec6.splitlines() if l.startswith("| FR-S6-")]
bad_rows = [l[:20] for l in rows if len(l.split("|")) != 10]
print("FR rows", len(rows), "malformed", bad_rows)

sec7 = text.split("# 7. Non-functional requirements", 1)[1].split("# 8. Data requirements", 1)[0]
nrows = [l for l in sec7.splitlines() if l.startswith("| NFR-S6-")]
print("NFR rows", len(nrows), "malformed", [l[:20] for l in nrows if len(l.split("|")) != 8])

sec5 = text.split("# 5. Capabilities and features", 1)[1].split("# 6. Functional requirements", 1)[0]
crows = [l for l in sec5.splitlines() if l.startswith("| CAP-S6-")]
print("CAP rows", len(crows), "malformed", [l[:20] for l in crows if len(l.split("|")) != 9])

sec11 = text.split("## 11.1 Acceptance criteria", 1)[1].split("## 11.2", 1)[0]
arows = [l for l in sec11.splitlines() if l.startswith("| AC-S6-")]
print("AC rows", len(arows), "malformed", [l[:20] for l in arows if len(l.split("|")) != 8])

for bad_word in ("Jira", "jira", "atlassian", "Claude", "co-authored"):
    if bad_word in text:
        print("FORBIDDEN", bad_word)

head = "\n".join(text.splitlines()[:6])
print("header ok", "SCB Collections and Recovery. Henka Group, 22 November 2026." in head)
print("tool line", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in text, "D-RCV-60" in text)
print("dates tentative:", text.count("(tentative)"))
