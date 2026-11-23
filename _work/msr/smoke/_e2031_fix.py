import os

base = r"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)"
names = [
    "RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v1.md",
    "RWB P10 E2031 CON Agent monitoring dashboard v2 [E3d] - contract v1.md",
    "RWB P10 E2031 OPS Agent monitoring dashboard v2 [E3d] - deployment v1.md",
]
old = "| DP-13 | `/api/recovery/v1` |"
new = "| DP-13 | `/api/recovery/` with one version segment for every module |"
for n in names:
    p = os.path.join(base, n)
    t = open(p, encoding="utf-8").read()
    c = t.count(old)
    t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    print(n, "replaced", c, "remaining", t.count("/api/recovery/v1"))
