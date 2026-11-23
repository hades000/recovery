import io, re
from pathlib import Path

p = Path("03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md")
lines = io.open(p, encoding="utf-8").read().splitlines()
i = 0
bad = []
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        block = []
        while j < len(lines) and lines[j].startswith("|"):
            block.append((j + 1, lines[j]))
            j += 1
        widths = {}
        for ln, s in block:
            ncol = s.count("|")
            widths.setdefault(ncol, []).append(ln)
        if len(widths) > 1:
            bad.append((block[0][0], {k: v[:4] for k, v in widths.items()}))
        i = j
    else:
        i += 1

print("tables with inconsistent column counts:", len(bad))
for b in bad[:10]:
    print(b)

# empty cells check in FR/NFR/AC tables
for sec, pat in [("FR", r"^\| FR-S8-\d{3} \|"), ("NFR", r"^\| NFR-S8-\d{3} \|"), ("AC", r"^\| AC-S8-\d{3} \|"), ("CAP", r"^\| CAP-S8-\d{3} \|")]:
    for line in lines:
        if re.match(pat, line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if any(c == "" for c in cells):
                print("empty cell", sec, line[:120])
print("done")
