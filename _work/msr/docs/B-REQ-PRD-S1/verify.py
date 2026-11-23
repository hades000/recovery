"""Self-check for the B-REQ-PRD-S1 PRD: id sets, citations, counts, dates."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PRD = ROOT / "03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md"
t = PRD.read_text(encoding="utf-8")

def ids(pattern, text=t):
    seen = []
    for m in re.finditer(pattern, text):
        if m.group(0) not in seen:
            seen.append(m.group(0))
    return seen

cap = ids(r"CAP-S1-\d{3}")
fr = ids(r"FR-S1-\d{3}")
nfr = ids(r"NFR-S1-\d{3}")
ac = ids(r"AC-S1-\d{3}(?!-)")
rol = ids(r"ROL-S1-\d{2}")
jrn = ids(r"JRN-S1-\d{2}")
oq = ids(r"OQ-S1-\d{2}")

def span(prefix, lst):
    nums = sorted(int(x[len(prefix):]) for x in lst)
    missing = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []
    dup = [n for n in set(nums) if nums.count(n) > 1]
    return max(nums), missing, dup

print("CAP", span("CAP-S1-", cap))
print("FR", span("FR-S1-", fr))
print("NFR", span("NFR-S1-", nfr))
print("AC", span("AC-S1-", ac))
print("ROL", span("ROL-S1-", rol))
print("JRN", span("JRN-S1-", jrn))
print("OQ", span("OQ-S1-", oq))

# citations resolve
gids = {json.loads(l)["id"] for l in (ROOT / "_work/msr/gaps/B-REQ-PRD-S1.jsonl").read_text(encoding="utf-8").splitlines()}
aids = {json.loads(l)["id"] for l in (ROOT / "_work/msr/assumptions/B-REQ-PRD-S1.jsonl").read_text(encoding="utf-8").splitlines()}
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
unknown = sorted(c for c in cited if c not in gids and c not in aids)
print("citations", len(cited), "unknown:", unknown)

# every FR row has a CAP/BR/REQ
rows = [l for l in t.splitlines() if l.startswith("| FR-S1-")]
bad = []
for r in rows:
    cells = [c.strip() for c in r.strip("|").split("|")]
    if len(cells) != 7 or not cells[2].startswith("CAP-S1-") or not cells[3].startswith("BR-0") or not cells[4].startswith("REQ-S1-"):
        bad.append(r[:80])
print("FR rows", len(rows), "malformed", bad)

# every CAP row has BR and a feature
caprows = [l for l in t.splitlines() if re.match(r"\| CAP-S1-\d{3} \|", l)]
print("CAP rows", len(caprows))
badcap = [r[:60] for r in caprows if "| Must |" not in r and "| Should |" not in r]
print("CAP rows without a priority", badcap)

# NFR rows
nfrrows = [l for l in t.splitlines() if l.startswith("| NFR-S1-")]
print("NFR rows", len(nfrrows))

# AC rows
acrows = [l for l in t.splitlines() if re.match(r"\| AC-S1-\d{3} \|", l)]
print("AC rows", len(acrows))

# OQ rows
oqrows = [l for l in t.splitlines() if re.match(r"\| OQ-S1-\d{2} \|", l)]
print("OQ rows", len(oqrows))

# dates tentative
for d in re.findall(r"\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}", t):
    ctx = t[t.index(d):t.index(d) + len(d) + 14]
    if "(tentative)" not in ctx:
        print("DATE WITHOUT (tentative) nearby:", ctx.strip())
print("decision rows", t.count("D-RCV-60"))
print("jira word", bool(re.search(r"(?i)jira|atlassian", t)))
print("email", bool(re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t)))
print("first two lines:", "\n".join(t.splitlines()[:2]))
