import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md"
t = open(p, encoding="utf-8").read()
parts = re.split(r"^## Slide (\d+)\s*$", t, flags=re.M)
want = {int(x) for x in sys.argv[1].split(",")} if len(sys.argv) > 1 else set()
lim = int(sys.argv[2]) if len(sys.argv) > 2 else 1400
for i in range(1, len(parts), 2):
    n = int(parts[i]); body = parts[i + 1].strip()
    if n in want:
        print("=== SLIDE", n)
        print(body[:lim])
