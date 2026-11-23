"""Build Recovery Workbench Error Handling and Resilience Standard v4 from the v3 template.

The v3 file is never written: it is copied to a scratch template, the copy is repaired for python-docx
(conventional style names, a List Bullet style with the numbering the v3 document uses), the full text is
rendered onto it, and the tables are re-styled to the v3 table look.
"""
import datetime
import shutil
import sys
from pathlib import Path

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx"
OUT = ROOT / "05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v4.docx"
MD = Path(__file__).with_name("Recovery Workbench Error Handling and Resilience Standard v4.md")
FIXED = Path(__file__).with_name("template-fixed.docx")

sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
from office_write import md_docx  # noqa: E402

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

if OUT.exists():
    raise SystemExit(f"REFUSED: {OUT} exists")
if FIXED.exists():
    FIXED.unlink()

shutil.copy2(SRC, FIXED)

# ---- repair the scratch copy so python-docx can find its styles ----
d = docx.Document(FIXED)
for s in d.styles:
    el = s.element.find(qn("w:name"))
    if el is None:
        continue
    val = el.get(qn("w:val")) or ""
    if val.startswith("Heading ") and val != val.lower():
        el.set(qn("w:val"), val.lower())

if not any(s.name == "List Bullet" for s in d.styles):
    bullet = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
    bullet.base_style = d.styles["List Paragraph"]
    pPr = bullet.element.get_or_add_pPr()
    for tag in ("w:keepNext", "w:keepLines"):
        pPr.append(OxmlElement(tag))
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId")
    numId.set(qn("w:val"), "2")  # the bullet definition the v3 document uses for its own lists
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.append(numPr)
    spaces = OxmlElement("w:spacing")
    spaces.set(qn("w:before"), "0")
    spaces.set(qn("w:after"), "120")
    pPr.append(spaces)

tblPr_template = deepcopy(d.tables[0]._tbl.tblPr)
trPr_template = deepcopy(d.tables[0].rows[0]._tr.find(qn("w:trPr")))
hdr_tcPr = d.tables[0].cell(0, 0)._tc.find(qn("w:tcPr"))
hdr_shd = deepcopy(hdr_tcPr.find(qn("w:shd")))
hdr_mar = deepcopy(hdr_tcPr.find(qn("w:tcMar")))
hdr_borders = deepcopy(hdr_tcPr.find(qn("w:tcBorders")))
d.save(FIXED)
print("repaired scratch template", FIXED)

# ---- render the full text ----
md_docx(str(MD), str(OUT), str(FIXED))

# ---- table look: v3 borders, header band, Aptos 8 pt, bold first column ----
d = docx.Document(OUT)
for t in d.tables:
    old = t._tbl.tblPr
    new = deepcopy(tblPr_template)
    old.getparent().replace(old, new)
    cols = len(t.columns)
    header_label = t.cell(0, 0).text.strip().lower() == "item"
    for ri, row in enumerate(t.rows):
        if ri == 0 and trPr_template is not None:
            tr = row._tr
            cur = tr.find(qn("w:trPr"))
            if cur is not None:
                tr.remove(cur)
            tr.insert(0, deepcopy(trPr_template))
        for ci, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            for child in list(tcPr):
                tcPr.remove(child)
            if ri == 0:
                if hdr_shd is not None:
                    tcPr.append(deepcopy(hdr_shd))
                if hdr_borders is not None:
                    tcPr.append(deepcopy(hdr_borders))
            if hdr_mar is not None:
                tcPr.append(deepcopy(hdr_mar))
            bold = ri == 0 or (ci == 0 and cols > 2 and not header_label)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Aptos"
                    r.font.size = Pt(8)
                    r.bold = True if bold else None
            if not cell.paragraphs[0].runs and cell.text == "":
                pass

cp = d.core_properties
cp.author = "Henka Group"
cp.last_modified_by = TOOL
cp.title = "Recovery Workbench Error Handling and Resilience Standard v4"
cp.revision = 4
cp.modified = datetime.datetime(2026, 11, 22, 0, 0, tzinfo=datetime.timezone.utc)
cp.comments = f"v4, 22 November 2026, D-RCV-60 microservice realignment, {TOOL}"
d.save(OUT)
print("WROTE", OUT)
