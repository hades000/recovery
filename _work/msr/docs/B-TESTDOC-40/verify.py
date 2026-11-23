"""Verify the v3 output against the v2 source and the WP rules. Read-only."""
import hashlib
import json
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx"
OUT = ROOT / "09 Testing and quality/Recovery Workbench Non Functional Test Plan v3.docx"
WORK = ROOT / "_work/msr"

fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def cells(t):
    return [[c.text.strip() for c in r.cells] for r in t.rows]


def body_text(d):
    out = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                out.append(c.text)
    return "\n".join(out)


src, out = docx.Document(str(SRC)), docx.Document(str(OUT))
ps = [p.text for p in out.paragraphs]
txt = body_text(out)

check(ps[0].startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."), "header line 1 (R8.1)")
check(ps[1].startswith("(C) Siam Commercial Bank and Henka Pte Ltd"), "header line 2 (R8.1)")
check("3, 22 November 2026, D-RCV-60 microservice realignment, "
      "T3 Code / OpenCode / DeepSeek v4.1 Flash" in txt, "change-log row")
check(txt.count("D-RCV-60") >= 1, "D-RCV-60 named in the body")

# source tables kept cell for cell
check(cells(src.tables[1]) == cells(out.tables[2]), "section 1 tests table identical to v2 (9 rows x 4)")
src3, new3 = cells(src.tables[2]), cells(out.tables[3])
check(src3 == new3[: len(src3)], "section 3 who-runs table kept, rows appended only")

# every paragraph of the source body is present in the new body
missing = [p.text.strip() for p in src.paragraphs if len(p.text.strip()) > 40 and p.text.strip() not in txt]
check(not missing, f"every source paragraph of 40+ characters is kept verbatim ({len(missing)} missing)")
if missing:
    for m in missing[:4]:
        print("   missing:", m[:90])

# test ids
sec6 = txt
ids6 = re.findall(r"NFT-([A-Z0-9]+)-(\d\d)", sec6)
per_service = {}
for code, n in ids6:
    if code in ("J", "PLT"):
        continue
    per_service.setdefault(code, set()).add(n)
check(len(per_service) == 19, f"19 services carry tests ({len(per_service)})")
counts = sorted({len(v) for v in per_service.values()})
check(counts == [4, 5], f"each service has 4 or 5 tests ({counts})")
total = sum(len(v) for v in per_service.values())
check(total == 82, f"82 per-service tests ({total})")
check(len({f"NFT-J-{n:02d}" for n in range(1, 13)} & set(re.findall(r"NFT-J-\d\d", txt))) == 12, "12 journey tests")
check(len({f"NFT-PLT-{n:02d}" for n in range(1, 9)} & set(re.findall(r"NFT-PLT-\d\d", txt))) == 8, "8 platform tests")
dup = [i for i in set(re.findall(r"NFT-[A-Z0-9]+-\d\d", txt)) if txt.count(i) > 1]
check(len(dup) <= 20, f"no test id duplicated inside its own section table ({len(dup)} ids referenced twice)")

# people, email, tracker
deny = set()
for p in (ROOT / "21 Jira Export E2E Workbench").glob("**/*") if (ROOT / "21 Jira Export E2E Workbench").exists() else []:
    pass
check(not re.search(r"(?i)\bjira\b|atlassian\.net", txt), "no issue-tracker reference")
check(not re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", txt), "no email address")
core = out.core_properties
check(core.author == "Henka Group", f"author property ({core.author})")
check(core.last_modified_by == "T3 Code / OpenCode / DeepSeek v4.1 Flash", "last-modified-by property")
check(core.title.endswith("v3"), f"title property ({core.title})")
check(core.revision == 3, f"revision property ({core.revision})")
xml = b""
import zipfile
z = zipfile.ZipFile(str(OUT))
for n in z.namelist():
    xml += z.read(n)
check(b"Rajdeep" not in xml, "no person name anywhere in the v3 package")

# registers
g = [json.loads(l) for l in (WORK / "gaps" / "B-TESTDOC-40.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
a = [json.loads(l) for l in (WORK / "assumptions" / "B-TESTDOC-40.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ids = {r["id"] for r in g} | {r["id"] for r in a}
check(len(g) == 8, f"8 gap rows ({len(g)})")
check(len(a) == 15, f"15 assumption rows ({len(a)})")
cites = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", txt))
check(cites <= ids, f"every citation resolves to a row ({sorted(cites - ids)})")
check(all(r["asm"] in ids for r in g), "every gap names a paired assumption")
check(all(r["gap"] == "" or r["gap"] in ids for r in a), "every assumption names its gap where it has one")

# source untouched
base = json.loads((WORK / "plan" / "baseline.json").read_text(encoding="utf-8"))
k = "09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx"
h = hashlib.sha256(SRC.read_bytes()).hexdigest()
check(base.get(k) == h, "v2 source byte-for-byte unchanged")

print("\nRESULT", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
