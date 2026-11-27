"""Safe next-version writer for the cross-document pass (D-RCV-60). AGENTS.md rule 1: never edit an existing file.

write_next(rel, fixes, stage) writes the next version of ROOT/rel under <stage>, applying every fix or none:
  .md .txt .csv .yaml .yml .json   apply_fixes text ops: replace, delete_line, insert_after
  .xlsx                            apply_fixes workbook ops: xlsx_append, xlsx_set, xlsx_set_cell, xlsx_add_column,
                                   xlsx_insert_row
  .docx                            docx_replace (old text exactly once in one paragraph or table cell),
                                   docx_insert_after (new paragraph after the paragraph whose text is old),
                                   docx_table_append (table whose header row contains header_has; values list)
Versioning: ' vN' in the file name -> vN+1. Otherwise the nearest parent folder with ' vN' is copied once to vN+1
(e.g. API Specification v5/rwb-access.yaml -> API Specification v6/rwb-access.yaml). Otherwise ' v2' is added.
A next version that already exists in ROOT is refused. Repeated calls for files of the same copied folder reuse it.
Change log: md via apply_fixes.change_log (falls back to a '**Change log.**' line after the title); yaml a '#'
comment line at the top; docx a final paragraph; xlsx a 'Read me' row when that sheet exists; csv and json none
(recorded in the Cross-document Change Register instead).
"""
import copy, json, re, shutil, sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment/checks"))
import apply_fixes as AF  # noqa: E402

DATE = "26 November 2026"
TOOL = AF.TOOL
TEXT = {".md", ".txt", ".csv", ".yaml", ".yml", ".json"}


class WriteError(Exception):
    pass


def next_rel(rel):
    """ROOT-relative path of the next version, and the folder that has to be copied first (or None)."""
    p = Path(rel)
    if re.search(r" v\d+$", p.stem):
        return (p.parent / AF.next_version(p.name)).as_posix(), None
    for k, part in enumerate(p.parts[:-1]):
        pass
    parts = list(p.parts)
    for k in range(len(parts) - 2, -1, -1):
        m = re.search(r" v(\d+)$", parts[k])
        if m:
            newp = parts[:]
            newp[k] = parts[k][:m.start()] + f" v{int(m.group(1)) + 1}"
            return Path(*newp).as_posix(), (Path(*parts[:k + 1]).as_posix(), Path(*newp[:k + 1]).as_posix())
    return (p.parent / f"{p.stem} v2{p.suffix}").as_posix(), None


def docx_apply(src, dst, fixes, note):
    import docx
    doc = docx.Document(str(src))

    def paras():
        for p in doc.paragraphs:
            yield p
        for t in doc.tables:
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        yield p

    def set_text(p, text):
        runs = p.runs
        if not runs:
            p.add_run(text)
            return
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""

    for fx in fixes:
        op = fx["op"]
        if op == "docx_replace":
            hits = [p for p in paras() if fx["old"] in p.text]
            n = sum(p.text.count(fx["old"]) for p in hits)
            if n != 1:
                raise WriteError(f"{fx['fix_id']}: old text found {n} time(s) in paragraphs, expected 1")
            set_text(hits[0], hits[0].text.replace(fx["old"], fx["new"], 1))
        elif op == "docx_insert_after":
            hits = [p for p in doc.paragraphs if p.text.strip() == fx["old"].strip()]
            if len(hits) != 1:
                raise WriteError(f"{fx['fix_id']}: paragraph found {len(hits)} time(s), expected 1")
            new_p = copy.deepcopy(hits[0]._p)
            hits[0]._p.addnext(new_p)
            para = docx.text.paragraph.Paragraph(new_p, hits[0]._parent)
            set_text(para, fx["new"])
        elif op == "docx_table_append":
            ts = [t for t in doc.tables if t.rows and fx["header_has"] in " | ".join(c.text for c in t.rows[0].cells)]
            if len(ts) != 1:
                raise WriteError(f"{fx['fix_id']}: table with header '{fx['header_has']}' found {len(ts)} time(s)")
            t = ts[0]
            vals = fx["values"]
            if len(vals) != len(t.rows[0].cells):
                raise WriteError(f"{fx['fix_id']}: {len(vals)} values for {len(t.rows[0].cells)} columns")
            new_tr = copy.deepcopy(t.rows[-1]._tr)
            t._tbl.append(new_tr)
            row = t.rows[-1]
            for c, v in zip(row.cells, vals):
                for p in c.paragraphs[1:]:
                    p._p.getparent().remove(p._p)
                set_text(c.paragraphs[0], str(v))
        else:
            raise WriteError(f"{fx['fix_id']}: op {op} is not a docx op")
    last = doc.paragraphs[-1] if doc.paragraphs else None
    p = doc.add_paragraph(f"Change log. D-RCV-60, {DATE}: {note}. Tool: {TOOL}.")
    if last is not None and last.style is not None:
        p.style = last.style
    dst.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(dst))


def text_apply(src, dst, fixes, note, new_name):
    text = src.read_text(encoding="utf-8")
    new = text
    for fx in fixes:
        try:
            new = AF.apply_text(new, fx)
        except AF.FixError as e:
            raise WriteError(f"{fx['fix_id']}: {e}")
    suf = src.suffix.lower()
    if suf == ".md":
        try:
            new = AF.change_log(new, fixes, DATE, note, new_name)
        except AF.FixError:
            ls = new.split("\n")
            k = next((i for i, l in enumerate(ls) if l.startswith("# ")), -1)
            ls[k + 1:k + 1] = ["", f"**Change log.** D-RCV-60, {DATE}: {note}. Tool: {TOOL}."]
            new = "\n".join(ls)
    elif suf in (".yaml", ".yml"):
        new = f"# Change log. D-RCV-60, {DATE}: {note}. Tool: {TOOL}.\n" + new
        import yaml
        try:
            list(yaml.safe_load_all(new))
        except yaml.YAMLError as e:
            raise WriteError(f"the result is not valid YAML: {str(e)[:200]}")
    elif suf == ".json":
        try:
            json.loads(new)
        except json.JSONDecodeError as e:
            raise WriteError(f"the result is not valid JSON: {e}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(new.replace("\r\n", "\n").replace("\n", "\r\n" if "\r\n" in text else "\n").encode("utf-8"))


def write_next(rel, fixes, stage, note="cross-document changes under the programme directive", dry=False):
    """Returns the ROOT-relative path written (inside stage). Raises WriteError; nothing is written then."""
    stage = Path(stage).resolve()
    src = ROOT / rel
    if not src.exists():
        raise WriteError(f"file not found: {rel}")
    nrel, folder = next_rel(rel)
    if (ROOT / nrel).exists():
        raise WriteError(f"next version already exists in ROOT: {nrel}")
    if folder and (ROOT / folder[1]).exists():
        raise WriteError(f"next folder version already exists in ROOT: {folder[1]}")
    dst = stage / nrel
    if dry:
        return nrel
    tmp = dst.with_name(dst.name + ".tmp" + dst.suffix)
    if folder and not (stage / folder[1]).exists():
        shutil.copytree(ROOT / folder[0], stage / folder[1])
    base = dst if dst.exists() else src  # later passes build on the staged next version (still one version)
    suf = src.suffix.lower()
    try:
        if suf == ".xlsx":
            try:
                AF.apply_xlsx(base, tmp, fixes)
            except AF.FixError as e:
                raise WriteError(str(e))
            if any(f.get("op", "").startswith("xlsx") for f in fixes):
                import openpyxl
                wb = openpyxl.load_workbook(tmp)
                if "Read me" in wb.sheetnames:
                    rm = wb["Read me"]
                    rm.cell(rm.max_row + 2, 1).value = f"Change log. D-RCV-60, {DATE}: {note}. Tool: {TOOL}."
                    wb.save(tmp)
        elif suf == ".docx":
            docx_apply(base, tmp, fixes, note)
        elif suf in TEXT:
            text_apply(base, tmp, fixes, note, Path(nrel).name)
        else:
            raise WriteError(f"no writer for {suf} files")
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    tmp.replace(dst)
    return nrel
