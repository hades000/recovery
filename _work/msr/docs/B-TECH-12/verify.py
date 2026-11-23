"""Verification for WP B-TECH-12: fidelity of v3 to v2 plus the run rules."""
import json
import re
import sys
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[4]
SRC_MD = ROOT / "_work" / "msr" / "extract" / "B-TECH-12" / "Recovery Workbench Audit and Logging Design v2.md"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Audit and Logging Design v3.docx"
GAPS = ROOT / "_work" / "msr" / "gaps" / "B-TECH-12.jsonl"
ASMS = ROOT / "_work" / "msr" / "assumptions" / "B-TECH-12.jsonl"
OUTDIR = ROOT / "_work" / "msr" / "docs" / "B-TECH-12" / "roundtrip"

SEP = re.compile(r"^\|[\s\-:|]+\|$")


def norm(s):
    """One comparable form for a source markdown line and a rendered body line."""
    s = " ".join(s.split())
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^[-*]\s+", "", s)
    if "|" in s:
        cells = [c.strip() for c in s.strip().strip("|").split("|")]
        s = "|".join(cells)
    return s


def body_lines(path):
    d = docx.Document(str(path))
    out = []
    for child in d.element.body.iterchildren():
        if child.tag == qn("w:p"):
            out.append(Paragraph(child, d).text)
        elif child.tag == qn("w:tbl"):
            for row in Table(child, d).rows:
                out.append(" | ".join(c.text for c in row.cells))
    return out


def main():
    fails, notes = [], []
    lines = body_lines(OUT)
    text = "\n".join(lines)
    src = [norm(l) for l in SRC_MD.read_text(encoding="utf-8").splitlines()
           if l.strip() and not SEP.match(l.strip())]
    new = set(norm(l) for l in lines if l.strip())

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "v3.txt").write_text(text, encoding="utf-8")
    (OUTDIR / "v2-normalised.txt").write_text("\n".join(src), encoding="utf-8")

    # 1 header
    if [l.rstrip() for l in lines[:2]] != ["SCB Collections and Recovery. Henka Group, 22 November 2026.",
                                           "(C) Siam Commercial Bank and Henka Pte Ltd"]:
        fails.append(f"header lines 1-2 wrong: {lines[:2]}")

    # 2 change log
    if not re.search(r"3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", text):
        fails.append("D-RCV-60 change-log row missing")
    if "D-RCV-60" not in text:
        fails.append("D-RCV-60 not named")

    # 3 fidelity: every non-empty source line is present, or is a listed intended change
    changed = {norm(x) for x in [
        "SCB Collections and Recovery. Henka Group, 28 October 2026",
        "| Version | 1 |",
        "| Date | 28 October 2026 |",
        "| Decision log | Every decision: inputs, rule and model versions, recommendation, approver, action | Append only, hash chained, one entry per decision | ACE database; nightly copy to the data lake | Internal audit, Risk, center of excellence |",
        "| Interaction ledger | Every contact, letter, promise, payment and hand-over | Append only, one entry per interaction | ACE database | Case owners in scope; Conduct and QA |",
        "| Access log | Sign-ins, refusals, grants, removals, break-glass, versions in force | Append only | ACE database, inside the decision log store | Application owner, security administrator, Compliance, internal audit |",
        "| Application logs | Errors, warnings and traces with no personal data | Structured JSON | Log Analytics | Platform administrator, squads |",
    ]}
    missing = [l for l in src if l not in new and l not in changed]
    notes.append(f"source lines: {len(src)}; not present: {len(missing)}")
    for m in missing:
        fails.append(f"source line not carried: {m[:110]}")

    # 4 sections
    got = [l for l in lines if re.match(r"^\d\. ", l)]
    want = ["1. The records", "2. The decision log entry", "3. Tracing an action end to end", "4. Integrity",
            "5. Retention", "6. What is never logged", "7. Owners and contracts", "8. Decisions",
            "9. Realignment changes in version 3 (D-RCV-60)"]
    if got != want:
        fails.append(f"section headings differ: {got}")

    # 5 citations
    ids = set()
    for p in (GAPS, ASMS):
        for row in p.read_text(encoding="utf-8").splitlines():
            if row.strip():
                ids.add(json.loads(row)["id"])
    cites = set(re.findall(r"\b(?:CG|ASM)-B-TECH-12-\d+\b", text))
    unresolved = sorted(c for c in cites if c not in ids)
    if unresolved:
        fails.append(f"unresolved citations: {unresolved}")

    # 6 forbidden content
    if "\ufffd" in text:
        fails.append("replacement characters in the body")
    if re.search(r"\bjira\b", text, re.I):
        fails.append("issue tracker named in the body")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", text):
        fails.append("email address in the body")
    bullets = [l for l in lines if l.startswith("\u2022")]
    if bullets:
        fails.append(f"bullet fallback text: {bullets[:2]}")

    # 7 properties
    doc = docx.Document(str(OUT))
    cp = doc.core_properties
    if cp.author != "Henka Group" or cp.last_modified_by != "T3 Code / OpenCode / DeepSeek v4.1 Flash":
        fails.append(f"properties: {cp.author} / {cp.last_modified_by}")
    notes.append(f"properties: {cp.author} / {cp.last_modified_by} / rev {cp.revision}")
    notes.append(f"paragraphs {len(doc.paragraphs)}; tables {len(doc.tables)}")
    notes.append(f"cited ids {len(cites)} of {len(ids)} rows")

    print("\n".join(notes))
    print("PASS" if not fails else "FAIL")
    for f in fails:
        print(" -", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
