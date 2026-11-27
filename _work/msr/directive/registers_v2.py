"""Write Assumptions Register v2 and Gap Register v2 (md + xlsx) into the stage area (D-RCV-60 directive run).

  assumptions  final now: Accept assumption -> Confirmed; Deferred (tied to a business gap) -> Unconfirmed
  gaps         business gaps -> Open (business decision); the others from the merged story dispositions and the
               document-level pass (--final), or 'Accepted (directive); resolution in progress' before that

Usage: python -I registers_v2.py assumptions|gaps --stage <dir> [--final]
Never edits v1. Writes <stage>/23 Document Gaps/Recovery Workbench <Name> Register v2.{md,xlsx}.
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
sys.path.insert(0, str(D))
GAPS = ROOT / "23 Document Gaps"
RULINGS = ROOT / "_work/msr/rulings/All stories rulings v4.xlsx"
DATE = "26 November 2026"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
ST_CONF = "Confirmed (programme directive, 26 November 2026)"
ST_UNCONF = "Unconfirmed (business decision pending)"
ST_BIZ = "Open (business decision)"


def decisions():
    import openpyxl
    ws = openpyxl.load_workbook(RULINGS, read_only=True)["Rulings"]
    it = ws.iter_rows(values_only=True)
    h = list(next(it))
    k, i, d, r = h.index("Kind"), h.index("Item ID"), h.index("Decision"), h.index("Ruling ID")
    return {row[i]: (row[k], row[d], row[r]) for row in it if row[i]}


def rewrite_md(src, dst, idcol_prefix, status_of, title_old, title_new, note):
    lines = src.read_text(encoding="utf-8").split("\n")
    out, c = [], Counter()
    for l in lines:
        if l.startswith(f"# {title_old}"):
            l = l.replace(title_old, title_new, 1)
        if l.startswith(f"| {idcol_prefix}"):
            cells = l.split(" | ")
            iid = cells[0][2:].strip()
            new = status_of(iid, cells[-1].rstrip(" |").strip())
            if new is not None:
                cells[-1] = new + " |"
                l = " | ".join(cells)
            c[l.split(" | ")[-1].rstrip(" |")] += 1
        out.append(l)
    # change log line after the Tool line
    for n, l in enumerate(out):
        if l.startswith("Tool: "):
            out.insert(n + 1, "")
            out.insert(n + 2, f"**Change log.** D-RCV-60, {DATE}: {note} Tool: {TOOL}.")
            break
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(out), encoding="utf-8")
    return c


def rewrite_xlsx(src, dst, sheet, status_of, title_old, title_new, note):
    import openpyxl
    wb = openpyxl.load_workbook(src)
    ws = wb[sheet]
    hdr = [c.value for c in ws[1]]
    si = hdr.index("Status") + 1
    for row in ws.iter_rows(min_row=2):
        iid = row[0].value
        if not iid:
            continue
        new = status_of(str(iid), str(row[si - 1].value or ""))
        if new is not None:
            row[si - 1].value = new
    for w in wb.worksheets:
        for row in w.iter_rows():
            for c in row:
                if isinstance(c.value, str) and title_old in c.value:
                    c.value = c.value.replace(title_old, title_new)
    if "Read me" in wb.sheetnames:
        rm = wb["Read me"]
        rm.cell(rm.max_row + 2, 1).value = f"Change log. D-RCV-60, {DATE}: {note} Tool: {TOOL}."
    dst.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dst)


def assumptions(stage):
    dec = decisions()
    def status_of(iid, old):
        k = dec.get(iid)
        if not k or "assumption" not in (k[0] or "").lower():
            return None
        return ST_CONF if k[1] == "Accept assumption" else ST_UNCONF if k[1] == "Deferred" else None
    note = ("statuses set under the programme directive: every assumption is confirmed except those tied to a "
            "business-decision gap, which stay unconfirmed until the business owner decides.")
    out = Path(stage) / "23 Document Gaps"
    c = rewrite_md(GAPS / "Recovery Workbench Assumptions Register v1.md",
                   out / "Recovery Workbench Assumptions Register v2.md", "ASM-", status_of,
                   "Recovery Workbench Assumptions Register v1", "Recovery Workbench Assumptions Register v2", note)
    rewrite_xlsx(GAPS / "Recovery Workbench Assumptions Register v1.xlsx",
                 out / "Recovery Workbench Assumptions Register v2.xlsx", "Assumptions", status_of,
                 "Recovery Workbench Assumptions Register v1", "Recovery Workbench Assumptions Register v2", note)
    print("assumptions v2:", dict(c))


def gap_status(final):
    """GAP id -> status, from the decisions and the merged dispositions."""
    import esc
    dec = decisions()
    per = defaultdict(list)
    stories = [s for s, _ in json.loads((D / "mp/stories.json").read_text())]
    for s in stories:
        for r, d in esc.merged_dispositions(s).items():
            if str(d.get("item", "")).startswith("GAP-"):
                per[d["item"]].append(d)
    doc = {}
    dp = D / "mp/docpass/dispositions.jsonl"
    if dp.exists():
        for l in dp.read_text(encoding="utf-8").splitlines():
            if l.strip():
                x = json.loads(l)
                doc[x["item"]] = x
    def status_of(iid, old):
        k = dec.get(iid)
        if not k:
            return None  # not in the rulings (Closed, Duplicate): unchanged
        if k[1] == "Deferred":
            return ST_BIZ
        ds = per.get(iid, []) + ([doc[iid]] if iid in doc else [])
        st = Counter(d["status"] for d in ds)
        if not final and not ds:
            return "Accepted (directive); resolution in progress"
        if st["Resolved"]:
            return "Resolved (directive)"
        if st["Cross-document"]:
            return ("Resolved (directive); change written to the target document" if iid in doc and
                    doc[iid]["status"] == "Resolved" else
                    "Accepted (directive); change listed in the Cross-document Change Register v1")
        if st["Not applied"]:
            return "Accepted (directive); not applied: value not in the source documents"
        return "Accepted (directive); resolution in progress"
    return status_of


def gaps(stage, final):
    status_of = gap_status(final)
    note = ("statuses set under the programme directive: the recommended resolution of every gap is accepted, "
            "except business-decision gaps, which stay open for their owner role.")
    out = Path(stage) / "23 Document Gaps"
    c = rewrite_md(GAPS / "Recovery Workbench Gap Register v1.md", out / "Recovery Workbench Gap Register v2.md",
                   "GAP-", status_of, "Recovery Workbench Gap Register v1", "Recovery Workbench Gap Register v2", note)
    rewrite_xlsx(GAPS / "Recovery Workbench Gap Register v1.xlsx", out / "Recovery Workbench Gap Register v2.xlsx",
                 "Gaps", status_of, "Recovery Workbench Gap Register v1", "Recovery Workbench Gap Register v2", note)
    print("gaps v2:", dict(c))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["assumptions", "gaps"])
    ap.add_argument("--stage", required=True)
    ap.add_argument("--final", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    (assumptions(a.stage) if a.what == "assumptions" else gaps(a.stage, a.final))
