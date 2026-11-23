"""docx/pptx/xlsx/md/sql/yaml -> markdown. Replaces textutil (macOS) and the Anthropic docx/pptx/xlsx skills."""
import argparse, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, latest_path, header

def _cell(s):
    return " ".join(str(s if s is not None else "").split()).replace("|", "\\|")

def _table(rows):
    rows = [r for r in rows if any(str(c or "").strip() for c in r)]
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [list(r) + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(_cell(c) for c in rows[0]) + " |", "|" + "---|" * w]
    out += ["| " + " | ".join(_cell(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(out) + "\n"

def docx_to_md(p):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = docx.Document(p); out = []
    for el in d.element.body.iterchildren():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "p":
            para = Paragraph(el, d); txt = para.text.strip()
            if not txt:
                continue
            st = (para.style.name or "").lower()
            if st.startswith("heading"):
                lvl = int("".join(ch for ch in st if ch.isdigit()) or 1)
                out.append("#" * min(lvl, 6) + " " + txt)
            elif st == "title":
                out.append("# " + txt)
            elif "list" in st:
                out.append("- " + txt)
            else:
                out.append(txt)
        elif tag == "tbl":
            t = Table(el, d)
            out.append(_table([[c.text for c in r.cells] for r in t.rows]))
    return "\n\n".join(out) + "\n"

def pptx_to_md(p):
    from pptx import Presentation
    prs = Presentation(p); out = []
    for i, s in enumerate(prs.slides, 1):
        title = s.shapes.title.text.strip() if s.shapes.title is not None and s.shapes.title.has_text_frame else ""
        out.append(f"## Slide {i}: {title}".rstrip(": "))
        def walk(shapes):
            for sh in shapes:
                if sh.shape_type == 6 and hasattr(sh, "shapes"):
                    walk(sh.shapes); continue
                if getattr(sh, "has_table", False) and sh.has_table:
                    out.append(_table([[c.text for c in r.cells] for r in sh.table.rows]))
                elif sh.has_text_frame and sh != s.shapes.title:
                    t = "\n".join(pp.text for pp in sh.text_frame.paragraphs if pp.text.strip())
                    if t.strip():
                        out.append(t)
        walk(s.shapes)
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            out.append("Notes: " + s.notes_slide.notes_text_frame.text.strip())
    return "\n\n".join(out) + "\n"

def xlsx_to_md(p, max_rows=5000):
    import openpyxl
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True); out = []
    for ws in wb.worksheets:
        rows = [list(r) for _, r in zip(range(max_rows), ws.iter_rows(values_only=True))]
        out.append(f"## Sheet: {ws.title}\n\n" + _table(rows))
    wb.close()
    return "\n".join(out)

def convert(src, outdir):
    src, outdir = Path(src), Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower(); dst = outdir / (src.stem + ".md")
    if ext == ".docx":
        dst.write_text(docx_to_md(src), encoding="utf-8")
    elif ext == ".pptx":
        dst.write_text(pptx_to_md(src), encoding="utf-8")
    elif ext in (".xlsx", ".xlsm"):
        dst.write_text(xlsx_to_md(src), encoding="utf-8")
    elif ext in (".md", ".txt", ".sql", ".yaml", ".yml", ".json", ".csv"):
        dst = outdir / src.name; shutil.copy2(src, dst)
    else:
        return None
    return dst

def convert_any(src, outdir):
    src = Path(src)
    if src.is_dir():
        return [convert(f, Path(outdir) / src.name / f.parent.relative_to(src)) for f in sorted(src.rglob("*")) if f.is_file()]
    return [convert(src, outdir)]

A3 = [  # (folder, family stem, kind) ; kind: file|dir
    ("Proposed Arch", "Recovery Microservice Architecture", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Program", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Epic 1", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Epic 2", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Lean BRD Epic 1", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Lean BRD Epic 2", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Epics 3 to 8 Specification", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Non Functional Specification", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Functional Specifications by Module", "dir"),
    ("05 Technical architecture", "Recovery Workbench Technical Specifications by Module", "dir"),
    ("05 Technical architecture", "Recovery Workbench Architecture Decision Records", "file"),
    ("05 Technical architecture", "Recovery Workbench Event and Messaging Design", "file"),
    ("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design", "file"),
    ("05 Technical architecture", "Recovery Workbench API Specification", "file"),
    ("02 Business architecture and process", "Recovery Workbench Business Rules and Routing Logic", "file"),
    ("06 Data", "Recovery Workbench Physical Schema", "file"),
    ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary", "file"),
    ("01 Decisions and governance", "Recovery Workbench Decision Log", "file"),
]

def run_a3():
    ex = WORK / "extract"; done = []
    for folder, stem, kind in A3:
        p = latest_path(ROOT / folder, stem, "dir" if kind == "dir" else None)
        if p is not None and kind == "file" and p.is_dir():
            p = latest_path(ROOT / folder, stem, ".docx") or latest_path(ROOT / folder, stem, ".md") or p
        if p is None:
            print("MISSING", folder, stem); continue
        done += [x for x in convert_any(p, ex) if x]
    for src, title, name in [
        (ROOT / "Proposed Arch" / "Recovery Microservice Architecture v5.pptx", "Architecture v5 Text Extract", "Recovery Workbench Architecture v5 Text Extract v1.md"),
        (ROOT / "Proposed Arch" / "Recovery Temporal and Drools Detailed Design v1.pptx", "Temporal and Drools Design Text Extract", "Recovery Workbench Temporal and Drools Design Text Extract v1.md")]:
        body = pptx_to_md(src)
        (R22 / name).write_text(f"# Recovery Workbench {title} v1\n\n{header()}\nSource: `{src.relative_to(ROOT)}` (read-only).\n\n{body}", encoding="utf-8")
        (ex / name).write_text(body, encoding="utf-8")
    print(f"A3 OK {len(done)} files converted into {ex}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?"); ap.add_argument("outdir", nargs="?")
    ap.add_argument("--a3", action="store_true")
    a = ap.parse_args()
    if a.a3:
        run_a3()
    else:
        for x in convert_any(a.src, a.outdir):
            print("WROTE", x)

if __name__ == "__main__":
    main()
