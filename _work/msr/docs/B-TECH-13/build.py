"""Build Recovery Workbench Document Management Design v3.docx from the v3 markdown.

The source v2 docx is never written. A scratch copy is repaired only in the two ways that
compat/office_write.py md-docx needs for this document family:

1. w:name/@w:val of the heading styles is "Heading 1", while python-docx looks the style up as
   "heading 1", so add_heading raises KeyError. The copy writes "heading 1".
2. The family has no "List Bullet" style, so add_paragraph(text, style="List Bullet") appends the
   paragraph and then raises, and md_docx appends a second, prefixed copy. The copy adds a
   "List Bullet" style based on "List Paragraph" with the bullet numbering (numId 2) that the v2
   document uses for its own lists.

The rendered document keeps the v2 styles, section properties, page setup and footer. A polish
step then restores the family look of version 2 (title block 26 pt and 17 pt in the family
colour 4E297F, 10 pt Aptos body, bullets as bullets, tables 9 pt with the DCD3EB header row,
C8C8C8 rules and the EEEAF6 label column of the control table), because the v2 document carries
all of that as direct formatting and a style-driven render does not reproduce it.

Core properties are set to the organisation and the tool: the v2 file carries a person name in
author and last-modified-by, which AGENTS.md rule 4 forbids in an output.
"""
import shutil
import sys
from pathlib import Path

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
from office_write import md_docx  # noqa: E402

SRC = ROOT / "05 Technical architecture" / "Recovery Workbench Document Management Design v2.docx"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Document Management Design v3.docx"
MD = ROOT / "_work" / "msr" / "docs" / "B-TECH-13" / "Recovery Workbench Document Management Design v3.md"
TPL = ROOT / "_work" / "msr" / "docs" / "B-TECH-13" / "template-fixed.docx"

PURPLE = "4E297F"
PURPLE2 = "604A7B"
INK = "1F1F1F"
HEAD_FILL = "DCD3EB"
LABEL_FILL = "EEEAF6"
RULE = "C8C8C8"


def fix_template():
    if TPL.exists():
        TPL.unlink()
    shutil.copy2(SRC, TPL)
    d = docx.Document(str(TPL))
    for s in d.styles:
        el = s.element
        if not el.tag.endswith("}style") or not s.name or not s.name.startswith("Heading "):
            continue
        el.find(qn("w:name")).set(qn("w:val"), s.name.lower())
    if "List Bullet" not in [s.name for s in d.styles]:
        st = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = d.styles["List Paragraph"]
        pPr = st.element.get_or_add_pPr()
        numPr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        num_id = OxmlElement("w:numId")
        num_id.set(qn("w:val"), "2")
        numPr.append(ilvl)
        numPr.append(num_id)
        pPr.insert(0, numPr)
    d.save(str(TPL))
    print("WROTE", TPL)


def _runs(p):
    for r in p.runs:
        yield r


def _fmt_run(run, size, colour, bold=False):
    run.font.name = "Aptos"
    run.font.size = docx.shared.Pt(size)
    run.font.bold = bold
    rPr = run._r.get_or_add_rPr()
    col = rPr.find(qn("w:color"))
    if col is None:
        col = OxmlElement("w:color")
        rPr.append(col)
    col.set(qn("w:val"), colour)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for a in ("w:ascii", "w:cs", "w:eastAsia", "w:hAnsi"):
        rFonts.set(qn(a), "Aptos")


def _borders(tbl):
    tblPr = tbl._tbl.tblPr
    for tag in ("w:tblBorders", "w:tblW", "w:tblLayout"):
        el = tblPr.find(qn(tag))
        if el is not None:
            tblPr.remove(el)
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "auto")
        b.append(e)
    tblPr.append(b)
    w = OxmlElement("w:tblW")
    w.set(qn("w:type"), "dxa")
    w.set(qn("w:w"), "9638")
    tblPr.append(w)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)


def _shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn("w:shd"))
    if old is not None:
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def _margins(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn("w:tcMar"))
    if old is not None:
        tcPr.remove(old)
    mar = OxmlElement("w:tcMar")
    for tag, width in (("top", "50"), ("left", "113"), ("bottom", "50"), ("right", "80")):
        e = OxmlElement(f"w:{tag}")
        e.set(qn("w:type"), "dxa")
        e.set(qn("w:w"), width)
        mar.append(e)
    tcPr.append(mar)


def polish():
    d = docx.Document(str(OUT))

    first_body = None
    for p in d.paragraphs:
        txt = p.text.strip()
        style = p.style.name.lower()
        if style.startswith("heading 1"):
            p.paragraph_format.space_before = docx.shared.Pt(15)
            p.paragraph_format.space_after = docx.shared.Pt(6)
            size, colour = 15, PURPLE
        elif style.startswith("heading 2"):
            p.paragraph_format.space_before = docx.shared.Pt(12)
            p.paragraph_format.space_after = docx.shared.Pt(3)
            size, colour = 12, PURPLE2
        elif style.startswith("heading 3"):
            p.paragraph_format.space_before = docx.shared.Pt(10)
            p.paragraph_format.space_after = docx.shared.Pt(2)
            size, colour = 10, PURPLE
        elif style.startswith("list"):
            p.paragraph_format.space_before = docx.shared.Pt(0)
            p.paragraph_format.space_after = docx.shared.Pt(3)
            p.paragraph_format.line_spacing = 1.15
            size, colour = 10, INK
        elif txt == "Recovery Workbench" and first_body is None:
            first_body = p
            p.paragraph_format.space_before = docx.shared.Pt(0)
            p.paragraph_format.space_after = docx.shared.Pt(6)
            size, colour = 26, PURPLE
            for r in _runs(p):
                _fmt_run(r, size, colour, bold=True)
            continue
        elif txt == "Document management design":
            p.paragraph_format.space_before = docx.shared.Pt(0)
            p.paragraph_format.space_after = docx.shared.Pt(6)
            size, colour = 17, PURPLE
            for r in _runs(p):
                _fmt_run(r, size, colour, bold=True)
            continue
        else:
            p.paragraph_format.space_before = docx.shared.Pt(0)
            p.paragraph_format.space_after = docx.shared.Pt(6)
            p.paragraph_format.line_spacing = 1.15
            size, colour = 10, INK
        for r in _runs(p):
            _fmt_run(r, size, colour)

    for idx, tbl in enumerate(d.tables):
        _borders(tbl)
        for r_i, row in enumerate(tbl.rows):
            for c_i, cell in enumerate(row.cells):
                _margins(cell)
                if r_i == 0:
                    _shade(cell, HEAD_FILL)
                elif idx == 0 and c_i == 0:
                    _shade(cell, LABEL_FILL)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = docx.shared.Pt(0)
                    p.paragraph_format.space_after = docx.shared.Pt(2)
                    p.paragraph_format.line_spacing = 1.05
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        _fmt_run(r, 9, PURPLE if r_i == 0 else INK, bold=(r_i == 0))

    d.save(str(OUT))
    print("POLISHED", OUT)


def set_props():
    d = docx.Document(str(OUT))
    c = d.core_properties
    c.author = "Henka Group"
    c.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    c.title = "Recovery Workbench Document Management Design v3"
    c.subject = "Recovery Workbench document management design"
    c.comments = "D-RCV-60 microservice realignment. Version 3, 22 November 2026."
    c.category = "Technical architecture"
    c.revision = 3
    c.modified = c.modified.replace(year=2026, month=11, day=22)
    d.save(str(OUT))
    p = docx.Document(str(OUT)).core_properties
    print("PROPS", p.author, "|", p.last_modified_by, "|", p.title, "|", p.modified, "|", p.revision)


if __name__ == "__main__":
    fix_template()
    if OUT.exists():
        raise SystemExit(f"REFUSED: {OUT} exists (never edit an existing file; use the next version)")
    md_docx(str(MD), str(OUT), template=str(TPL))
    polish()
    set_props()
    d = docx.Document(str(OUT))
    print("paragraphs", len(d.paragraphs), "tables", len(d.tables))
    for sec in d.sections:
        for part in (sec.header, sec.footer):
            txt = " / ".join(p.text for p in part.paragraphs if p.text.strip())
            if txt:
                print("HEADER/FOOTER:", txt)
