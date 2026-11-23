import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = "03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md"
lines = open(p, encoding="utf-8").read().split("\n")

def block(start, end):
    i = next(n for n, l in enumerate(lines) if l.startswith(start))
    j = next(n for n, l in enumerate(lines[i:], i) if l.startswith(end))
    return lines[i:j]

for name, (s, e) in {"FR table": ("| FR ID |", "# 7."), "NFR table": ("| NFR ID |", "# 8."),
                     "AC table": ("| AC ID |", "## 11.2"), "CAP table": ("| CAP ID |", "## 5.1")}.items():
    rows = [l for l in block(s, e) if l.startswith("|")]
    body = [r for r in rows[2:] if r.strip().strip("|").strip()]
    ids = [r.split("|")[1].strip() for r in body]
    cols = {len(r.split("|")) for r in rows}
    print(name, "rows", len(ids), "first", ids[0], "last", ids[-1], "col-counts", cols,
          "dupes", [x for x in set(ids) if ids.count(x) > 1])

# every FR cited in the trace summary exists
fr = {x for x in re.findall(r"FR-P9-\d{3}", "\n".join(block("| FR ID |", "# 7.")))}
allfr = {x for x in re.findall(r"FR-P9-\d{3}", "\n".join(lines))}
print("FR defined-not-cited-anywhere:", sorted(fr - allfr))
print("empty cells in FR table:", sum(1 for l in block("| FR ID |", "# 7.")[2:] if re.search(r"\|\s*\|", l)))
