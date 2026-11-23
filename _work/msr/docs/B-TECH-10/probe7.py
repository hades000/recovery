from pathlib import Path

p = Path(r"_work/msr/docs/B-TECH-10/Recovery Workbench Error Handling and Resilience Standard v4.md")
lines = p.read_text(encoding="utf-8").splitlines()


def kind(l):
    s = l.strip()
    if not s:
        return "blank"
    if s.startswith("#"):
        return "head"
    if s.startswith("|"):
        return "table"
    if s.startswith("- "):
        return "bullet"
    return "para"


prev = None
for i, l in enumerate(lines, 1):
    k = kind(l)
    if k == "para" and prev == "para":
        print(f"WRAPPED at {i}: {l[:100]}")
    prev = k

print("paragraph count:", sum(1 for l in lines if kind(l) == "para"))
print("bullet count:", sum(1 for l in lines if kind(l) == "bullet"))
print("max line length:", max(len(l) for l in lines))
