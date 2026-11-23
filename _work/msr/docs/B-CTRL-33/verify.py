"""Verify the v3 docx against the v2 source text and the registers."""
import json
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC_MD = ROOT / "_work" / "msr" / "extract" / "B-CTRL-33" / "Recovery Workbench Records Retention and Archiving v2.md"
OUT = ROOT / "10 Policy, controls and compliance" / "Recovery Workbench Records Retention and Archiving v3.docx"
RT = ROOT / "_work" / "msr" / "docs" / "B-CTRL-33" / "roundtrip3" / "Recovery Workbench Records Retention and Archiving v3.md"
GAPS = ROOT / "_work" / "msr" / "gaps" / "B-CTRL-33.jsonl"
ASMS = ROOT / "_work" / "msr" / "assumptions" / "B-CTRL-33.jsonl"

fails = []


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


src_lines = [norm(l) for l in SRC_MD.read_text(encoding="utf-8").splitlines() if norm(l)]
rt = RT.read_text(encoding="utf-8")
rt_lines = [norm(l) for l in rt.splitlines() if norm(l)]
rt_blob = "\n".join(rt_lines)

INTENDED = [
    "Recovery Workbench",
    "Records retention and archiving",
    "SCB Collections and Recovery. Henka Group, 28 October 2026",
    "| Document | Recovery Workbench records retention and archiving |",
    "| Version | 1 |",
    "| Date | 28 October 2026 |",
    "Copy kept in the data lake",
    "| Decision log | DP12 | 10 years after the case closes | Copy kept in the data lake | Audit and regulatory |",
    "| Scores | DP11 | 2 years | Delete | Model monitoring |",
    "| Access log | None | Per the bank security standard | Archive | Security and audit |",
    "| Application logs | None | 90 days | Archive for 1 year | Operations |",
    "| Case record and case history | DP03 | 10 years after the case closes | Archive after 2 years closed | Legal claims and audit |",
    "| Account, payments and money | DP01, DP13 | 10 years after the case closes | Archive after 2 years closed | Accounting and tax records |",
    "| Customer and party | DP02 | 10 years after the last case closes | Archive after 2 years closed | Legal claims |",
    "| Treatments and offers | DP04 | 10 years after the treatment ends | Archive after 2 years | Contract evidence |",
    "| Contact and interaction ledger | DP05 | 5 years after the case closes | Archive after 1 year closed | Conduct review |",
    "| Collateral and assets | DP06 | 10 years after disposal | Archive after 2 years | Legal claims |",
    "| Legal actions and notices | DP07 | 10 years after the legal action ends | Archive after 2 years | Legal claims |",
    "| Partner performance | DP08 | 5 years | Archive after 1 year | Contract management |",
    "| Debt sale | DP09 | 10 years after transfer | Archive after 2 years | Legal claims |",
    "| Legal documents | DP10 | 10 years after the case closes; write-once | Archive after 2 years closed | Legal claims |",
    "| Other documents | DP10 | 5 years after the case closes | Archive after 1 year closed | Operations |",
    "| Reference data versions | DP14 | 10 years after superseded | Archive | Audit: which rule applied |",
    "| Active | ACE database and document storage | By role and scope |",
    "| Archived | Archive tier of storage; database partitions detached to the archive | Compliance and internal audit on request |",
    "| Destroyed | Removed from every store and backup cycle | None; the disposal decision is kept |",
]

missing = []
for line in src_lines:
    if line in rt_blob:
        continue
    # table rows gained a trailing cell: test the source cells as a prefix
    if line.startswith("|") and any(rtl.startswith(line[:-1].rstrip()) for rtl in rt_lines):
        continue
    if line in INTENDED:
        continue
    missing.append(line)

if missing:
    fails.append("source lines not found: %s" % missing[:8])

# header lines 1 and 2 as the first two paragraphs of the docx
d = docx.Document(str(OUT))
paras = [p.text.strip() for p in d.paragraphs]
first = [p for p in paras if p][:2]
if first != ["SCB Collections and Recovery. Henka Group, 22 November 2026.", "(C) Siam Commercial Bank and Henka Pte Ltd"]:
    fails.append("first two paragraphs are not the R8.1 header: %s" % first)

if "3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in rt:
    fails.append("change-log row of the metadata table missing")

# sections 1-4 kept, in order, and the added ones after
heads = [p.text.strip() for p in d.paragraphs if p.style.style_id in ("Heading1", "Heading2")]
heads = [h for h in heads if h != "Change log"]
want = ["1. Retention schedule, proposed", "1.1 Retention by schema", "2. Where records move",
        "2.1 The same three stages in the target", "3. How destruction happens", "3.1 The monthly job in the target",
        "4. Legal hold", "4.1 Legal hold in the target", "5. Change register for this version", "6. Decisions",
        "7. Open items and out of scope"]
if heads[:len(want)] != want:
    fails.append("headings differ: %s" % heads)

# citations resolve
ids = set()
for p in (GAPS, ASMS):
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", rt))
unresolved = sorted(c for c in cited if c not in ids)
if unresolved:
    fails.append("unresolved citations: %s" % unresolved)

# every schema named once in 1.1
schemas = ["rwb_source_data", "rwb_integration", "rwb_case", "rwb_access", "rwb_document", "rwb_comms", "rwb_decision",
           "rwb_payment", "rwb_reporting", "rwb_agent", "rwb_valuation", "rwb_treatment", "rwb_guarantee",
           "rwb_litigation", "rwb_asset", "rwb_debtsale", "rwb_writeoff", "rwb_deviation", "rwb_partner"]
sec = rt.split("1.1 Retention by schema", 1)[1].split("# 2. Where records move", 1)[0]
for s in schemas:
    if "| " + s + " |" not in sec:
        fails.append("schema row missing in 1.1: " + s)

cp = d.core_properties
if cp.author != "Henka Group" or "DeepSeek" not in (cp.last_modified_by or ""):
    fails.append("document properties: %s / %s" % (cp.author, cp.last_modified_by))
if "\ufffd" in rt:
    fails.append("replacement character in the text")

print("source lines:", len(src_lines), "| unexplained missing:", len(missing))
print("tables:", len(d.tables), "| headings:", len(heads), "| citations:", len(cited), "| unresolved:", len(unresolved))
print("PASS" if not fails else "FAIL")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
