"""Render Recovery Workbench Observability and Monitoring Design v4.docx from the v4 markdown.

The source v3 docx is never written. A scratch copy is repaired only in the two ways that
compat/office_write.py md-docx needs for this document family:

1. w:name/@w:val of the heading styles is "Heading 1", while python-docx looks the style up
   as "heading 1", so add_heading raises KeyError. The copy writes "heading 1".
2. The family has no "List Bullet" style, so add_paragraph(text, style="List Bullet") appends
   the paragraph and then raises, and md_docx appends a second, prefixed copy. The copy adds a
   "List Bullet" style based on "List Paragraph" with the bullet numbering the v3 document
   uses for its own lists.

The rendered document keeps the v3 styles, section properties and page setup. Core properties
are then set to the organisation and the tool: the v3 file carries a person name in author and
last-modified-by, which AGENTS.md rule 4 forbids in an output.
"""
import shutil
import sys
from pathlib import Path

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
from office_write import md_docx  # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench Observability and Monitoring Design v3.docx"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Observability and Monitoring Design v4.docx"
MD = HERE / "Recovery Workbench Observability and Monitoring Design v4.md"
TPL = HERE / "template-fixed.docx"


def fix_template():
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
        num_id.set(qn("w:val"), "3")
        numPr.append(ilvl)
        numPr.append(num_id)
        pPr.insert(0, numPr)
    d.save(str(TPL))
    print("WROTE", TPL)


def set_props():
    d = docx.Document(str(OUT))
    c = d.core_properties
    c.author = "Henka Group"
    c.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    c.title = "Recovery Workbench Observability and Monitoring Design v4"
    c.subject = "Recovery Workbench observability and monitoring design"
    c.comments = "D-RCV-60 microservice realignment. Version 4, 22 November 2026."
    c.category = "Technical architecture"
    c.revision = 4
    c.modified = c.modified.replace(year=2026, month=11, day=22)
    d.save(str(OUT))
    p = docx.Document(str(OUT)).core_properties
    print("PROPS", p.author, "|", p.last_modified_by, "|", p.title, "|", p.modified, "|", p.revision)


if __name__ == "__main__":
    fix_template()
    if OUT.exists():
        OUT.unlink()
        print("REMOVED the file built by the previous run of this script (it is this WP's own output)")
    md_docx(str(MD), str(OUT), template=str(TPL))
    set_props()
    d = docx.Document(str(OUT))
    print("paragraphs", len(d.paragraphs), "tables", len(d.tables))
    for sec in d.sections:
        for part in (sec.header, sec.footer):
            txt = " / ".join(p.text for p in part.paragraphs if p.text.strip())
            if txt:
                print("HEADER/FOOTER:", txt)
