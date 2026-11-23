"""Verify Recovery Workbench Document Management Design v3.docx against the v2 source text.

Checks: header lines 1-2, the D-RCV-60 change-log row, fidelity of every v2 line (verbatim or
extended), no template artefacts, no person name or email, no issue-tracker reference, properties.

A source line counts as kept when
  - a heading: the same heading text is a heading of version 3;
  - a bullet or a paragraph: the same text, or a version 3 paragraph that starts with it;
  - a table row: a version 3 row whose cells start with the cells of the source row, in order.
"""
import re
import sys
from pathlib import Path

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[4]
SRC_MD = ROOT / "_work" / "msr" / "extract" / "B-TECH-13" / "Recovery Workbench Document Management Design v2.md"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Document Management Design v3.docx"


def norm(s):
    s = s.replace("\u00a0", " ").replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", s).strip()


def body_items():
    """[(kind, payload)] in document order: ('p', text) or ('row', [cells])."""
    d = docx.Document(str(OUT))
    items = []
    for child in d.element.body.iterchildren():
        if child.tag.endswith("}p"):
            items.append(("p", norm(Paragraph(child, d).text)))
        elif child.tag.endswith("}tbl"):
            for row in Table(child, d).rows:
                items.append(("row", [norm(c.text) for c in row.cells]))
    return items


def main():
    fails = []
    items = body_items()
    paras = [p.text for p in docx.Document(str(OUT)).paragraphs]
    ptexts = [t for k, t in items if k == "p" and t]
    rows = [c for k, c in items if k == "row"]

    if not paras or norm(paras[0]) != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
        fails.append(f"header line 1 wrong: {paras[0]!r}" if paras else "no paragraphs")
    if len(paras) < 2 or norm(paras[1]) != "(C) Siam Commercial Bank and Henka Pte Ltd":
        fails.append(f"header line 2 wrong: {paras[1]!r}")

    text = "\n".join(ptexts) + "\n" + "\n".join("| " + " | ".join(c) + " |" for c in rows)
    if "3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in text:
        fails.append("change-log row with D-RCV-60 and the tool line is missing")

    # The three intended changes of the version row, the date row and the source date line.
    INTENDED = {
        "SCB Collections and Recovery. Henka Group, 28 October 2026":
            "replaced by the R8.1 header; the date 28 October 2026 is kept in the Source version row",
        "| Version | 1 |": "the version row reads 3, as R8.2 numbers the next version",
        "| Date | 28 October 2026 |": "the date row reads 22 November 2026, the run date",
    }

    src = [l.rstrip() for l in SRC_MD.read_text(encoding="utf-8").splitlines()]
    exact, extended, intended, missing = 0, [], [], []
    for raw in src:
        n = norm(raw)
        if not n or re.fullmatch(r"\|[-: |]+\|", n):
            continue
        if n in INTENDED:
            intended.append((n, INTENDED[n]))
            continue
        if raw.lstrip().startswith("#"):
            head = norm(re.sub(r"^#+\s*", "", raw))
            if any(h.startswith(head) for h in ptexts):
                exact += 1
            else:
                missing.append(n)
        elif n.startswith("|"):
            cells = [c.strip() for c in n.strip("|").split("|")]
            same = [r for r in rows if r[: len(cells)] == cells]
            if same:
                exact += 1
            elif any(len(r) >= len(cells) and all(r[i].startswith(cells[i]) for i in range(len(cells))) for r in rows):
                extended.append(n)
            else:
                missing.append(n)
        else:
            body = norm(re.sub(r"^-\s+", "", n))
            if body in ptexts:
                exact += 1
            elif any(t.startswith(body) for t in ptexts):
                extended.append(body)
            else:
                missing.append(n)

    for bad in ("List Bullet", "\ufffd", "None | None"):
        if bad in text:
            fails.append(f"artefact {bad!r} in the document")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", text):
        fails.append("email address in the document")
    if re.search(r"(?i)\bjira\b|atlassian\.net", text):
        fails.append("issue-tracker reference in the document")

    c = docx.Document(str(OUT)).core_properties
    if c.author != "Henka Group":
        fails.append(f"author {c.author!r}")
    if c.last_modified_by != "T3 Code / OpenCode / DeepSeek v4.1 Flash":
        fails.append(f"last_modified_by {c.last_modified_by!r}")

    d = docx.Document(str(OUT))
    heads = [p.text.strip() for p in d.paragraphs if p.style.name.lower().startswith("heading")]
    print("PARAGRAPHS", len(d.paragraphs), "TABLES", len(d.tables))
    print("HEADINGS", " | ".join(heads))
    print(f"SOURCE LINES: exact/kept {exact}, extended {len(extended)}, intended {len(intended)}, missing {len(missing)}")
    for l in extended:
        print("  EXTENDED:", l[:110])
    for l, why in intended:
        print("  INTENDED:", l[:100], "->", why)
    for l in missing:
        print("  MISSING:", l[:150])
    for f in fails:
        print("FAIL:", f)
    ok = not fails and not missing
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
