"""Apply fix records to the next version of each file (sandbox prototype, D-RCV-60).

AGENTS.md rule 1: an existing file is never edited. Each target file is copied to its next version
(the last ' vN' of the name + 1) under --out, and only the listed edits are applied to the copy.
Every edit is exact: the old text must occur exactly `count` times (default 1). If any edit of a
file fails, nothing is written for that file and every fix of it is reported FAILED.

Fix record (one JSON object per line):
  fix_id, finding (CG/GAP id), file (ROOT-relative), op, source (the document that decides it), and
  op "replace":        old, new, count (default 1)
  op "delete_line":    old (one full line, exact)
  op "insert_after":   old (one full line, exact), new (text; may hold several lines)
  op "xlsx_append":    sheet, header_row_hint (a header cell value), rows (list of {header: value}),
                       key (header whose values must be new)
  op "xlsx_set":       sheet, key_header, key, header, old, new
  op "xlsx_set_cell":  sheet, cell (e.g. A4), old (exact current value), new
  op "xlsx_add_column": sheet, key_header, header (new; must not exist), values ({key: text}),
                       style_from (header of an existing column whose styles are copied)
  op "xlsx_insert_row": sheet, after (exact value of a column-A cell; must occur once), values (list, from column A)

Usage: python -I apply_fixes.py --root <ROOT> --fixes fixes.jsonl --out <dir> [--date "26 November 2026"]
       [--note "..."] [--dry-run]
Writes only under --out: the next-version files at their ROOT-relative folders, diffs/, apply_result.jsonl,
apply_log.md.
"""
import argparse, difflib, json, re, shutil, sys
from collections import OrderedDict
from pathlib import Path

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


class FixError(Exception):
    pass


def next_version(name):
    p = Path(name)
    m = list(re.finditer(r" v(\d+)$", p.stem))
    if not m:
        raise FixError(f"no ' vN' version in the file name: {name}")
    last = m[-1]
    return p.with_name(p.stem[:last.start()] + f" v{int(last.group(1)) + 1}" + p.suffix).name


def apply_text(text, fx):
    op = fx["op"]
    old = fx.get("old", "")
    if op == "replace":
        n = text.count(old)
        want = int(fx.get("count", 1))
        if not old:
            raise FixError("empty old text")
        if n != want:
            raise FixError(f"old text found {n} time(s), expected {want}: {old[:80]!r}")
        return text.replace(old, fx["new"])
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l == old]
    if len(idx) != 1:
        raise FixError(f"line found {len(idx)} time(s), expected 1: {old[:80]!r}")
    i = idx[0]
    if op == "delete_line":
        del lines[i]
    elif op == "insert_after":
        lines[i + 1:i + 1] = fx["new"].split("\n")
    else:
        raise FixError(f"op {op} is not a text op")
    return "\n".join(lines)


CL_TABLE = "| Version | Date | Change | Tool |"


def change_log(text, fixes, date, note, new_name=""):
    """Add one change-log entry in the file's own style: a '**Change log.**' line, a plain 'Change log:'
    line, or a row of the '| Version | Date | Change | Tool |' table (version from the new file name)."""
    ids = ", ".join(sorted({f["finding"] for f in fixes if f.get("finding")}))
    what = f"{note or 'fixes from the build-readiness review'}{' (' + ids + ')' if ids else ''}"
    body = f"D-RCV-60, {date}: {what}. Tool: {TOOL}."
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("**Change log.**")]
    if idx:
        lines[idx[-1] + 1:idx[-1] + 1] = ["", f"**Change log.** {body}"]
        return "\n".join(lines)
    idx = [i for i, l in enumerate(lines) if l.startswith("Change log: ")]
    if idx:
        lines[idx[-1] + 1:idx[-1] + 1] = ["", f"Change log: {body}"]
        return "\n".join(lines)
    idx = [i for i, l in enumerate(lines) if l.strip() == CL_TABLE]
    if len(idx) == 1:
        m = re.search(r" (v\d+)$", Path(new_name).stem)
        if not m:
            raise FixError("change-log table found, but the new file name has no ' vN' for its Version cell")
        end = idx[0] + 1
        while end < len(lines) and lines[end].lstrip().startswith("|"):
            end += 1
        lines[end:end] = [f"| {m.group(1)} | {date} | D-RCV-60: {what} | {TOOL} |"]
        return "\n".join(lines)
    raise FixError("no '**Change log.**' line, 'Change log:' line or single change-log table to add the entry to")


def header_row(ws, hint, keys):
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 40)):
        vals = [c.value for c in row]
        if hint in vals and all(k in vals for k in keys):
            return row[0].row, {v: i for i, v in enumerate(vals) if v is not None}
    raise FixError(f"header row with {hint!r} and {keys} not found in sheet {ws.title}")


def apply_xlsx(src, dst, fixes):
    import openpyxl
    wb = openpyxl.load_workbook(src)
    for fx in fixes:
        if fx["sheet"] not in wb.sheetnames:
            raise FixError(f"{fx['fix_id']}: no sheet {fx['sheet']}")
        ws = wb[fx["sheet"]]
        if fx["op"] == "xlsx_append":
            keys = sorted({k for r in fx["rows"] for k in r})
            hr, cols = header_row(ws, fx.get("header_row_hint", keys[0]), keys)
            kc = cols[fx["key"]]
            have = {ws.cell(row=r, column=kc + 1).value for r in range(hr + 1, ws.max_row + 1)}
            last = max((r for r in range(hr + 1, ws.max_row + 1)
                        if any(ws.cell(row=r, column=c + 1).value not in (None, "") for c in cols.values())), default=hr)
            for r in fx["rows"]:
                if r[fx["key"]] in have:
                    raise FixError(f"{fx['fix_id']}: {fx['key']} {r[fx['key']]} already in {fx['sheet']}")
                last += 1
                for h, v in r.items():
                    ws.cell(row=last, column=cols[h] + 1, value=v)
                have.add(r[fx["key"]])
        elif fx["op"] == "xlsx_set":
            hr, cols = header_row(ws, fx["key_header"], [fx["key_header"], fx["header"]])
            hits = [r for r in range(hr + 1, ws.max_row + 1)
                    if ws.cell(row=r, column=cols[fx["key_header"]] + 1).value == fx["key"]]
            if len(hits) != 1:
                raise FixError(f"{fx['fix_id']}: key {fx['key']} found {len(hits)} time(s)")
            c = ws.cell(row=hits[0], column=cols[fx["header"]] + 1)
            if (c.value or "") != fx.get("old", c.value or ""):
                raise FixError(f"{fx['fix_id']}: cell holds {str(c.value)[:60]!r}, expected {fx['old'][:60]!r}")
            c.value = fx["new"]
        elif fx["op"] == "xlsx_set_cell":
            c = ws[fx["cell"]]
            if (c.value or "") != fx["old"]:
                raise FixError(f"{fx['fix_id']}: {fx['cell']} holds {str(c.value)[:60]!r}, expected {fx['old'][:60]!r}")
            c.value = fx["new"]
        elif fx["op"] == "xlsx_add_column":
            from copy import copy
            hr, cols = header_row(ws, fx["key_header"], [fx["key_header"], fx["style_from"]])
            if fx["header"] in cols:
                raise FixError(f"{fx['fix_id']}: column {fx['header']!r} already in {fx['sheet']}")
            new_c = max(cols.values()) + 2  # 1-based, after the last header
            src_c = cols[fx["style_from"]] + 1
            keys = {ws.cell(row=r, column=cols[fx["key_header"]] + 1).value: r for r in range(hr + 1, ws.max_row + 1)}
            missing = [k for k in fx["values"] if k not in keys]
            if missing:
                raise FixError(f"{fx['fix_id']}: keys not in {fx['sheet']}: {missing}")
            for r in range(hr, ws.max_row + 1):
                s, d = ws.cell(row=r, column=src_c), ws.cell(row=r, column=new_c)
                if s.has_style:
                    d.font, d.fill, d.border, d.alignment, d.number_format = (copy(s.font), copy(s.fill), copy(s.border),
                                                                             copy(s.alignment), s.number_format)
            ws.cell(row=hr, column=new_c, value=fx["header"])
            for k, v in fx["values"].items():
                ws.cell(row=keys[k], column=new_c, value=v)
            from openpyxl.utils import get_column_letter
            w = ws.column_dimensions[get_column_letter(src_c)].width
            if w:
                ws.column_dimensions[get_column_letter(new_c)].width = w
        elif fx["op"] == "xlsx_insert_row":
            hits = [r for r in range(1, ws.max_row + 1) if ws.cell(row=r, column=1).value == fx["after"]]
            if len(hits) != 1:
                raise FixError(f"{fx['fix_id']}: {fx['after'][:60]!r} found {len(hits)} time(s) in column A")
            if ws.merged_cells.ranges:
                raise FixError(f"{fx['fix_id']}: {fx['sheet']} has merged cells; inserting a row is not safe")
            ws.insert_rows(hits[0] + 1)
            for i, v in enumerate(fx["values"]):
                ws.cell(row=hits[0] + 1, column=i + 1, value=v)
        else:
            raise FixError(f"{fx['fix_id']}: op {fx['op']} is not a workbook op")
    dst.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dst)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fixes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default="26 November 2026")
    ap.add_argument("--note", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    fixes = [json.loads(l) for l in Path(a.fixes).read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = [f["fix_id"] for f in fixes]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate fix_id in the fix records")
    by_file = OrderedDict()
    for f in fixes:
        by_file.setdefault(f["file"], []).append(f)
    results, log = [], []
    for rel, fl in by_file.items():
        src = root / rel
        try:
            if not src.exists():
                raise FixError(f"file not found: {rel}")
            new_name = next_version(src.name)
            if (src.parent / new_name).exists():
                raise FixError(f"next version already exists in ROOT: {new_name}")
            dst = out / Path(rel).parent / new_name
            if dst.exists():
                raise FixError(f"output exists: {dst} (never overwrite)")
            if src.suffix.lower() == ".xlsx":
                if not a.dry_run:
                    apply_xlsx(src, dst, fl)
                diff = f"{len(fl)} workbook edit(s)"
            else:
                text = src.read_text(encoding="utf-8")
                new = text
                for fx in fl:
                    try:
                        new = apply_text(new, fx)
                    except FixError as e:
                        raise FixError(f"{fx['fix_id']}: {e}")
                new = change_log(new, fl, a.date, a.note, new_name)
                d = list(difflib.unified_diff(text.splitlines(), new.splitlines(), str(src.name), new_name, lineterm="", n=1))
                diff = f"{sum(1 for x in d if x.startswith('+') and not x.startswith('+++'))} line(s) added or changed"
                if not a.dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_text(new, encoding="utf-8")
                    (out / "diffs").mkdir(parents=True, exist_ok=True)
                    (out / "diffs" / (new_name + ".diff")).write_text("\n".join(d) + "\n", encoding="utf-8")
            for fx in fl:
                results.append({"fix_id": fx["fix_id"], "file": rel, "status": "APPLIED", "to": new_name})
            log.append(f"| {rel} | {new_name} | {len(fl)} | APPLIED | {diff} |")
        except FixError as e:
            for fx in fl:
                results.append({"fix_id": fx["fix_id"], "file": rel, "status": "FAILED", "reason": str(e)})
            log.append(f"| {rel} | - | {len(fl)} | FAILED | {str(e)[:160]} |")
    out.mkdir(parents=True, exist_ok=True)
    with (out / "apply_result.jsonl").open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(1 for r in results if r["status"] == "APPLIED")
    (out / "apply_log.md").write_text(
        f"# Fix apply log\n\nTool: {TOOL}. Decision D-RCV-60. {'Dry run. ' if a.dry_run else ''}"
        f"{ok} of {len(results)} fixes applied, {len(by_file)} files.\n\n"
        "| File | Next version | Fixes | Result | Detail |\n|---|---|---|---|---|\n" + "\n".join(log) + "\n",
        encoding="utf-8")
    print(f"{ok}/{len(results)} fixes applied over {len(by_file)} files -> {out}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
