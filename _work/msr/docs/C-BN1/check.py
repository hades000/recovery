from pathlib import Path

p = Path(__file__).resolve().parents[4] / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v7.md"
lines = p.read_text(encoding="utf-8").splitlines()
for l in lines:
    if l.startswith("| `RWB-E1-001`") or l.startswith("| `RWB-"):
        print(l.count("|"), "|".join(x.strip() for x in l.split("|"))[:400])
        break
# count cells of all map rows
bad = [l[:80] for l in lines if l.startswith("| `RWB-") and l.count("|") != 8]
print("map rows with wrong cell count:", len(bad))
for b in bad[:5]:
    print(b)
