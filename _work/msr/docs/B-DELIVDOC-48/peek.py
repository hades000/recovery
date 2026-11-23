import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path, nums = sys.argv[1], sys.argv[2]
t = open(path, encoding="utf-8").read()
parts = re.split(r"(?m)^## Slide (\d+)\s*$", t)
d = {}
for i in range(1, len(parts), 2):
    d[int(parts[i])] = parts[i + 1]
for n in [int(x) for x in nums.split(",")]:
    print("=" * 20, n)
    print(d[n].strip()[:3000])
