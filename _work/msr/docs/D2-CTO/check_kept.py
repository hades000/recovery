import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def slides(md):
    txt = Path(md).read_text(encoding="utf-8")
    parts = re.split(r"^## Slide \d+\s*$", txt, flags=re.M)
    return [p.strip() for p in parts[1:]]


def clean(block):
    out = []
    for line in block.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.isdigit():
            continue
        out.append(s)
    return out


v3 = [clean(b) for b in slides(sys.argv[1])]
v4 = [clean(b) for b in slides(sys.argv[2])][-len(v3):]
ok = True
for i, (a, b) in enumerate(zip(v3, v4), 1):
    if a != b:
        ok = False
        print(f"DIFF in kept slide {i}")
        for x, y in zip(a, b):
            if x != y:
                print("  v3:", x)
                print("  v4:", y)
        if len(a) != len(b):
            print("  line counts", len(a), len(b))
print("kept slides identical:", ok, "| count", len(v3))
