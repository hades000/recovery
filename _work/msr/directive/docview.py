"""Read-only, size-capped views of project documents for the document-level pass (D-RCV-60).

  python -I docview.py info  <file>                    sheets/tables/sections with sizes and headers
  python -I docview.py find  <file> <text> [<text>..]  rows/paragraphs/lines containing every text (cap 40)
  python -I docview.py rows  <file> <sheet> <from> <n> workbook rows with their header (cap 60 rows)
  python -I docview.py lines <file> <from> <n>         text lines (cap 150)
<file> is ROOT-relative; the staged next version is read when it exists (so a pass sees earlier changes).
Output is capped at 12,000 characters. Never writes.
"""
import re, sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
STAGE = D / "stage"
CAP = 12000
sys.path.insert(0, str(D))


def resolve(rel):
    import docwriter
    try:
        nrel, _ = docwriter.next_rel(rel)
        if (STAGE / nrel).exists():
            return STAGE / nrel, f"(staged next version {nrel})"
    except Exception:
        pass
    return ROOT / rel, "(project file)"


def cap(s):
    return s if len(s) <= CAP else s[:CAP] + f"\n[... output cut at {CAP} characters; narrow the search]"


def xl(p):
    import openpyxl
    return openpyxl.load_workbook(p, read_only=True, data_only=True)


def header(ws):
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=6, values_only=True), 1):
        vals = [str(v) for v in row if v not in (None, "")]
        if len(vals) >= 2:
            return i, [("" if v is None else str(v)) for v in row]
    return 1, []


def main():
    cmd, rel = sys.argv[1], sys.argv[2]
    p, where = resolve(rel)
    out = [f"{rel} {where}"]
    suf = p.suffix.lower()
    if suf == ".xlsx":
        wb = xl(p)
        if cmd == "info":
            for ws in wb.worksheets:
                hr, h = header(ws)
                out.append(f"sheet '{ws.title}': {ws.max_row} rows; header row {hr}: {' | '.join(h)[:600]}")
        elif cmd == "find":
            texts = [t.lower() for t in sys.argv[3:]]
            n = 0
            for ws in wb.worksheets:
                hr, h = header(ws)
                for i, row in enumerate(ws.iter_rows(values_only=True), 1):
                    line = " | ".join("" if v is None else str(v) for v in row)
                    if all(t in line.lower() for t in texts):
                        out.append(f"[{ws.title}!row {i}] {line[:700]}")
                        n += 1
                        if n >= 40:
                            break
                if n >= 40:
                    break
            out.append(f"{n} match(es)")
        elif cmd == "rows":
            ws = wb[sys.argv[3]]
            a, k = int(sys.argv[4]), min(int(sys.argv[5]), 60)
            hr, h = header(ws)
            out.append(f"header row {hr}: {' | '.join(h)}")
            for i, row in enumerate(ws.iter_rows(min_row=a, max_row=a + k - 1, values_only=True), a):
                out.append(f"row {i}: " + " | ".join("" if v is None else str(v) for v in row)[:700])
    elif suf == ".docx":
        import docx
        doc = docx.Document(str(p))
        if cmd == "info":
            heads = [x.text for x in doc.paragraphs if x.style is not None and x.style.name.lower().startswith("heading")]
            out.append(f"{len(doc.paragraphs)} paragraphs; headings: " + " | ".join(heads)[:3000])
            for k, t in enumerate(doc.tables):
                out.append(f"table {k}: {len(t.rows)} rows; header: " + " | ".join(c.text for c in t.rows[0].cells)[:300])
        elif cmd == "find":
            texts = [t.lower() for t in sys.argv[3:]]
            n = 0
            for x in doc.paragraphs:
                if all(t in x.text.lower() for t in texts):
                    out.append(f"[paragraph] {x.text[:700]}")
                    n += 1
            for k, t in enumerate(doc.tables):
                for i, row in enumerate(t.rows):
                    line = " | ".join(c.text for c in row.cells)
                    if all(tt in line.lower() for tt in texts):
                        out.append(f"[table {k} row {i}] {line[:700]}")
                        n += 1
                    if n >= 40:
                        break
            out.append(f"{n} match(es)")
        elif cmd == "rows":
            t = doc.tables[int(sys.argv[3])]
            a, k = int(sys.argv[4]), min(int(sys.argv[5]), 60)
            for i, row in enumerate(t.rows[a:a + k], a):
                out.append(f"row {i}: " + " | ".join(c.text for c in row.cells)[:700])
    else:
        L = p.read_text(encoding="utf-8", errors="replace").split("\n")
        if cmd == "info":
            heads = [f"L{i + 1}: {l[:120]}" for i, l in enumerate(L) if re.match(r"#{1,4} |[a-zA-Z_]+:$", l)]
            out.append(f"{len(L)} lines; headings/keys:\n" + "\n".join(heads[:150]))
        elif cmd == "find":
            texts = [t.lower() for t in sys.argv[3:]]
            hits = [f"L{i + 1}: {l[:700]}" for i, l in enumerate(L) if all(t in l.lower() for t in texts)]
            out += hits[:40] + [f"{len(hits)} match(es)"]
        elif cmd == "lines":
            a, k = int(sys.argv[3]), min(int(sys.argv[4]), 150)
            out += [f"L{i}: {l}" for i, l in enumerate(L[a - 1:a - 1 + k], a)]
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(cap("\n".join(out)))


if __name__ == "__main__":
    main()
