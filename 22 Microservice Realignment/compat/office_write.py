"""Office helpers for agents (replace the Anthropic docx/xlsx/pptx skills). Never overwrites an existing file."""
import argparse, json, re, shutil, sys
from pathlib import Path

def _guard(dst):
    if Path(dst).exists():
        raise SystemExit(f"REFUSED: {dst} exists (never edit an existing file; use the next version)")

def copy(src, dst):
    _guard(dst); src = Path(src)
    shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    print("COPIED", src, "->", dst)

def _rows(block):
    rows = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))] for l in block]
    return [r for r in rows if not all(set(c) <= set("-: ") for c in r)]

def md_docx(md, out, template=None):
    import docx
    _guard(out)
    doc = docx.Document(template) if template else docx.Document()
    if template:
        body = doc.element.body
        for el in list(body):
            if not el.tag.endswith("sectPr"):
                body.remove(el)
    lines = Path(md).read_text(encoding="utf-8").splitlines(); i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            blk = []
            while i < len(lines) and lines[i].startswith("|"):
                blk.append(lines[i]); i += 1
            rows = _rows(blk)
            if rows:
                w = max(len(r) for r in rows); t = doc.add_table(rows=len(rows), cols=w)
                try:
                    t.style = "Table Grid"
                except Exception:
                    pass
                for r, row in enumerate(rows):
                    for c in range(w):
                        t.cell(r, c).text = row[c] if c < len(row) else ""
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            doc.add_heading(m.group(2).strip(), min(len(m.group(1)), 4))
        elif re.match(r"^\s*[-*]\s+", l):
            try:
                doc.add_paragraph(re.sub(r"^\s*[-*]\s+", "", l), style="List Bullet")
            except KeyError:
                doc.add_paragraph("• " + re.sub(r"^\s*[-*]\s+", "", l))
        elif l.strip():
            doc.add_paragraph(l.replace("**", ""))
        i += 1
    doc.save(out); print("WROTE", out)

def xlsx_append(xlsx, sheet, rows_json):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx); rows = json.loads(Path(rows_json).read_text(encoding="utf-8"))
    ws = wb[sheet] if sheet in wb.sheetnames else wb.create_sheet(sheet[:31])
    for r in rows:
        ws.append(r)
    wb.save(xlsx); print("APPENDED", len(rows), "rows to", sheet)

def md_xlsx(md, out):
    from xlsx_write import write_book
    _guard(out); sheets, name, blk = {}, "Sheet", []
    def flush():
        rows = _rows(blk)
        if rows:
            sheets[name[:31] if name not in sheets else (name[:28] + str(len(sheets)))] = (rows[0], rows[1:])
    for l in Path(md).read_text(encoding="utf-8").splitlines() + [""]:
        if l.startswith("|"):
            blk.append(l); continue
        if blk:
            flush(); blk = []
        m = re.match(r"^#{1,6}\s+(.*)$", l)
        if m:
            name = re.sub(r"[\[\]:*?/\\]", " ", m.group(1)).strip() or "Sheet"
    write_book(out, sheets); print("WROTE", out)

def pptx_append(pptx, slides_md):
    from pptx import Presentation
    prs = Presentation(pptx); cur = None
    layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]
    for l in Path(slides_md).read_text(encoding="utf-8").splitlines():
        if l.startswith("## "):
            cur = prs.slides.add_slide(layout); cur.shapes.title.text = l[3:].strip()
            body = [s for s in cur.placeholders if s.placeholder_format.idx == 1]
            cur._body = body[0].text_frame if body else None; cur._first = True
        elif cur is not None and l.strip() and cur._body is not None:
            txt = re.sub(r"^\s*[-*]\s+", "", l)
            if cur._first:
                cur._body.text = txt; cur._first = False
            else:
                cur._body.add_paragraph().text = txt
    prs.save(pptx); print("APPENDED slides to", pptx)

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("copy"); a.add_argument("src"); a.add_argument("dst")
    a = sub.add_parser("md-docx"); a.add_argument("md"); a.add_argument("out"); a.add_argument("--template")
    a = sub.add_parser("md-xlsx"); a.add_argument("md"); a.add_argument("out")
    a = sub.add_parser("xlsx-append"); a.add_argument("xlsx"); a.add_argument("sheet"); a.add_argument("rows_json")
    a = sub.add_parser("pptx-append"); a.add_argument("pptx"); a.add_argument("slides_md")
    x = ap.parse_args()
    {"copy": lambda: copy(x.src, x.dst), "md-docx": lambda: md_docx(x.md, x.out, x.template),
     "md-xlsx": lambda: md_xlsx(x.md, x.out), "xlsx-append": lambda: xlsx_append(x.xlsx, x.sheet, x.rows_json),
     "pptx-append": lambda: pptx_append(x.pptx, x.slides_md)}[x.cmd]()
