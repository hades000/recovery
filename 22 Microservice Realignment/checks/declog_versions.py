"""Version-reference check for the Decision Log (sandbox prototype, D-RCV-60).

A decision row records the evidence it was taken on, so an older document version named in a row is
history and is never rewritten. For each decision row that names a version lower than the highest in
the Document Index, this script:
  - writes one Outdated finding (gaps.jsonl, the R9 fields), and
  - proposes a pointer in a new column "Current version of cited sources" of the next Decision Log
    version, leaving the decision text untouched. Whether the row's claim still holds in the current
    version is a reviewer step: the pointer says it has not been checked.
References to the Decision Log's own earlier versions are version history and are skipped.
The Read me sheet gets the next version line, a change-log row and its source line.

Usage: python -I declog_versions.py --root <ROOT> --out <dir> [--date "26 November 2026"] [--start 1]
Writes only under --out: gaps.jsonl, fixes.jsonl, summary.md. Apply with apply_fixes.py.
"""
import argparse, json, re, sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rwbsrc  # noqa: E402

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
OWN = "Decision Log"
COLUMN = "Current version of cited sources"


def old_refs(text, best):
    out = []
    for name, v in best.items():
        if name == OWN:
            continue
        for m in re.finditer(r"(?<![\w-])" + re.escape(name) + r" v(\d+)\b", text):
            if int(m.group(1)) < v:
                out.append((name, int(m.group(1)), v))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default="26 November 2026")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--wp", default="DLV")
    ap.add_argument("--declog", help="Decision Log path (default: the one in rwbsrc.SOURCES); used to re-check a next version")
    a = ap.parse_args(argv)
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    import openpyxl
    src = rwbsrc.Sources(root, out / "_cache")
    best = src.doc_versions()
    rel = a.declog or rwbsrc.SOURCES["declog"]
    m = re.search(r" v(\d+)\.xlsx$", rel)
    cur = int(m.group(1))
    wb = openpyxl.load_workbook(root / rel)
    rows, fixes, n = [], [], a.start - 1
    pointers = OrderedDict()
    for ws in wb:
        if ws.title == "Read me":
            continue
        hdr_row, hdr = None, {}
        for r in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 15)):
            vals = [c.value for c in r]
            if "ID" in vals:
                hdr_row, hdr = r[0].row, {v: i for i, v in enumerate(vals) if v}
                break
        if hdr_row is None:
            continue
        for r in ws.iter_rows(min_row=hdr_row + 1):
            key = r[hdr["ID"]].value
            if not key:
                continue
            refs, where = [], []
            for c in r:
                if COLUMN in hdr and c.column - 1 == hdr[COLUMN]:
                    continue
                if isinstance(c.value, str):
                    got = old_refs(c.value, best)
                    if got:
                        refs += got
                        where.append(f"{ws.title}!{c.coordinate}")
            if not refs:
                continue
            names = sorted({nm for nm, _, _ in refs})
            if COLUMN in hdr:  # already pointed at the current version: resolved
                ptr = r[hdr[COLUMN]].value or ""
                if all(f"{nm} v{best[nm]}" in ptr for nm in names):
                    continue
            olds = sorted({f"{nm} v{ov}" for nm, ov, _ in refs})
            curs = [f"{nm} v{best[nm]}" for nm in names]
            n += 1
            gid = f"CG-{a.wp}-{n}"
            rows.append(OrderedDict(
                id=gid, title=f"{key} cites {', '.join(olds)}; the current version is {', '.join(curs)}",
                source=rel, section=", ".join(where),
                description=(f"Decision {key} names {', '.join(olds)}. Document Index v14 lists {', '.join(curs)} as the "
                             "highest version. The row records the evidence the decision was taken on, so the older "
                             "version is kept; the row does not say whether its claim still holds in the current version."),
                evidence=f"A) Decision Log v{cur}, {', '.join(where)}. B) Document Index v14: {', '.join(curs)}.",
                type="Outdated", area="Versions", severity="P3", needed_by_wave="", legacy_ref="",
                owner_role="Business analyst", asm="",
                proposed=(f"Keep the decision text. Add '{COLUMN}' = {', '.join(curs)} in Decision Log v{cur + 1}, and have "
                          f"the decision owner confirm the claim against {', '.join(curs)}."),
                wp=a.wp, check="X20", story=key, auto=True))
            if ws.title not in pointers:
                pointers[ws.title] = OrderedDict()
            pointers[ws.title][key] = (f"{'; '.join(curs)} (Document Index v14). {', '.join(olds)}, named in this row, "
                                       f"{'is the source' if len(olds) == 1 else 'are the sources'} at the time of the decision and "
                                       f"{'is' if len(olds) == 1 else 'are'} kept as written. Not yet checked against "
                                       f"the current version ({gid}).")
    fid = 0

    def fix(**kw):
        nonlocal fid
        fid += 1
        f = OrderedDict(fix_id=f"FDL-{fid:03d}", finding=kw.pop("finding", ""), file=rel, **kw)
        fixes.append(f)

    for sheet, vals in pointers.items():
        fix(finding=", ".join(r["id"] for r in rows if r["section"].startswith(sheet)), op="xlsx_add_column",
            sheet=sheet, key_header="ID", header=COLUMN, values=vals, style_from="What it means for the build"
            if sheet == "Decisions taken" else "ID")
    if pointers:
        rm = wb["Read me"]
        a4 = rm["A4"].value or ""
        exp = f"Recovery Workbench Decision Log v{cur}. "
        if a4.startswith(exp):
            new = a4.replace(f"Decision Log v{cur}.", f"Decision Log v{cur + 1}.", 1) \
                    .replace(f"The next version of v{cur - 1}: every ID, number and date of v{cur - 1}",
                             f"The next version of v{cur}: every ID, number and date of v{cur}", 1)
            fix(op="xlsx_set_cell", sheet="Read me", cell="A4", old=a4, new=new)
        changelog = next((c.value for c in rm["A"] if isinstance(c.value, str) and c.value.strip() == "Change log"), None)
        ids = ", ".join(r["id"] for r in rows)
        decs = ", ".join(k for v in pointers.values() for k in v)
        if changelog:
            fix(op="xlsx_insert_row", sheet="Read me", after=changelog,
                values=[f"v{cur + 1}, {a.date}, D-RCV-60 version pointers: column '{COLUMN}' added to "
                        f"{', '.join(pointers)} for {decs}; the decision text and every ID, number and date of "
                        f"v{cur} are kept ({ids}). Tool: {TOOL}."])
        cur_date = next((mm.group(1) for c in rm["A"] if isinstance(c.value, str)
                         for mm in [re.match(rf"v{cur}, (\d{{1,2}} \w+ \d{{4}})", c.value)] if mm), None)
        for c in rm["A"]:
            if cur_date and isinstance(c.value, str) and c.value.startswith(f"Source: Recovery Workbench Decision Log v{cur - 1},"):
                new = re.sub(rf"Decision Log v{cur - 1}, [^.]*\.", f"Decision Log v{cur}, {cur_date}.", c.value, count=1)
                fix(op="xlsx_set_cell", sheet="Read me", cell=c.coordinate, old=c.value, new=new)
    # cell edits address fixed coordinates, so a row insert must come after them
    fixes = [f for f in fixes if f["op"] != "xlsx_insert_row"] + [f for f in fixes if f["op"] == "xlsx_insert_row"]
    for i, f in enumerate(fixes, 1):
        f["fix_id"] = f"FDL-{i:03d}"
    out.mkdir(parents=True, exist_ok=True)
    for name, data in (("gaps.jsonl", rows), ("fixes.jsonl", fixes)):
        with (out / name).open("w", encoding="utf-8") as f:
            for r in data:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lines = [f"# Decision Log version check ({a.wp})", "", f"Source: {rel}. Tool: {TOOL}.", "",
             f"{len(rows)} decision rows name an older document version; {len(fixes)} fix records.", "",
             "| Finding | Decision | Old | Current | Cells |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['id']} | {r['story']} | {r['title'].split(' cites ')[1].split(';')[0]} | "
                     f"{r['title'].split('current version is ')[1]} | {r['section']} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} decision rows with older versions, {len(fixes)} fix records -> {out}")


if __name__ == "__main__":
    main()
