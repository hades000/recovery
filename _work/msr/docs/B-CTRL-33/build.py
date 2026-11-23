"""Build the v3 docx of the records retention and archiving document.

Source is never written: it is copied to a scratch template, repaired in the copy
(canonical heading style names, a List Bullet style on List Paragraph with the
numId 2 list the source bullets use), rendered with compat/office_write.py
md-docx, then given the table look of the source and clean document properties.
"""
import copy
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
from office_write import md_docx  # noqa: E402

SRC = ROOT / "10 Policy, controls and compliance" / "Recovery Workbench Records Retention and Archiving v2.docx"
OUT = ROOT / "10 Policy, controls and compliance" / "Recovery Workbench Records Retention and Archiving v3.docx"
MD = ROOT / "_work" / "msr" / "docs" / "B-CTRL-33" / "Recovery Workbench Records Retention and Archiving v3.md"
TPL = ROOT / "_work" / "msr" / "docs" / "B-CTRL-33" / "template-fixed.docx"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def repair(path):
    d = docx.Document(path)
    for s in d.styles:
        sid = s.style_id or ""
        if sid in ("Heading1", "Heading2", "Heading3", "Heading4"):
            nm = s.element.find(W + "name")
            if nm is not None:
                nm.set(W + "val", sid.replace("Heading", "heading "))
    base = [x for x in d.styles if x.style_id == "ListParagraph"]
    st = d.styles.add_style("List Bullet", WD_STYLE_TYPE.PARAGRAPH)
    if base:
        st.base_style = base[0]
    pPr = st.element.get_or_add_pPr()
    numPr = pPr.makeelement(W + "numPr", {})
    numPr.append(pPr.makeelement(W + "ilvl", {W + "val": "0"}))
    numPr.append(pPr.makeelement(W + "numId", {W + "val": "2"}))
    pPr.append(numPr)
    d.save(path)


def _el(tag, **attrs):
    e = docx.oxml.parse_xml(
        '<w:%s %s/>' % (tag, " ".join('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                                     'w:%s="%s"' % (k, v) for k, v in attrs.items()))
    )
    return e


def style_tables(d):
    """Give every table the source look: fixed width, thin borders, shaded bold header."""
    for t in d.tables:
        tbl = t._tbl
        tblPr = tbl.tblPr
        for tag in ("tblW", "tblBorders", "tblLayout"):
            for old in tblPr.findall(qn("w:" + tag)):
                tblPr.remove(old)
        tblW = tblPr.makeelement(qn("w:tblW"), {qn("w:type"): "dxa", qn("w:w"): "9638"})
        borders = tblPr.makeelement(qn("w:tblBorders"), {})
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            borders.append(tblPr.makeelement(
                qn("w:" + side),
                {qn("w:val"): "single", qn("w:sz"): "4", qn("w:space"): "0", qn("w:color"): "auto"}))
        layout = tblPr.makeelement(qn("w:tblLayout"), {qn("w:type"): "fixed"})
        tblPr.append(tblW)
        tblPr.append(borders)
        tblPr.append(layout)

        cols = len(t.columns)
        weights = []
        for c in range(cols):
            longest = max((len(t.rows[r].cells[c].text) for r in range(len(t.rows))), default=8)
            weights.append(max(6, min(longest, 55)))
        total = sum(weights)
        widths = [max(900, int(9638 * w / total)) for w in weights]
        if sum(widths) > 9638:
            scale = 9638 / sum(widths)
            widths = [max(700, int(w * scale)) for w in widths]
            widths[widths.index(max(widths))] += 9638 - sum(widths)
        grid = tbl.find(qn("w:tblGrid"))
        if grid is not None:
            tbl.remove(grid)
        grid = tblPr.makeelement(qn("w:tblGrid"), {})
        for w in widths:
            grid.append(tblPr.makeelement(qn("w:gridCol"), {qn("w:w"): str(w)}))
        tblPr.addnext(grid)

        for r, row in enumerate(t.rows):
            trPr = row._tr.get_or_add_trPr()
            for tag in ("cantSplit", "tblHeader"):
                if trPr.find(qn("w:" + tag)) is None:
                    trPr.append(trPr.makeelement(qn("w:" + tag), {}))
            if r:
                for old in trPr.findall(qn("w:tblHeader")):
                    trPr.remove(old)
            for c, cell in enumerate(row.cells):
                tcPr = cell._tc.get_or_add_tcPr()
                for old in tcPr.findall(qn("w:tcW")):
                    tcPr.remove(old)
                tcPr.insert(0, tcPr.makeelement(qn("w:tcW"), {qn("w:type"): "dxa", qn("w:w"): str(widths[c])}))
                for old in tcPr.findall(qn("w:shd")):
                    tcPr.remove(old)
                if r == 0:
                    tcPr.append(tcPr.makeelement(
                        qn("w:shd"), {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): "DCD3EB"}))
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = docx.shared.Pt(2)
                    p.paragraph_format.space_before = docx.shared.Pt(1)
                    for run in p.runs:
                        run.font.size = docx.shared.Pt(9)
                        if r == 0:
                            run.font.bold = True
                            run.font.color.rgb = docx.shared.RGBColor(0x4E, 0x29, 0x7F)


def main():
    shutil.copyfile(SRC, TPL)
    repair(TPL)
    tmp = ROOT / "_work" / "msr" / "docs" / "B-CTRL-33" / "build" / OUT.name
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        tmp.unlink()
    md_docx(str(MD), str(tmp), str(TPL))
    d = docx.Document(str(tmp))
    style_tables(d)
    cp = d.core_properties
    cp.author = "Henka Group"
    cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    cp.title = "Recovery Workbench Records Retention and Archiving v3"
    cp.subject = "Records retention and archiving, D-RCV-60 microservice realignment"
    cp.comments = "D-RCV-60 microservice realignment. Retention stated per service schema."
    cp.revision = 3
    cp.modified = dt.datetime(2026, 11, 22, 9, 0, 0)
    cp.created = dt.datetime(2026, 10, 28, 9, 0, 0)
    d.save(str(tmp))
    # This run's own unfinished output may be replaced; the source is never touched.
    if OUT.exists():
        OUT.unlink()
    shutil.copyfile(tmp, OUT)
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
