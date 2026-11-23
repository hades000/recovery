import json, glob, os
from pathlib import Path

W = Path("_work/msr")
keys = ["DM005","DM006","DM007","DM008","DM009"]
CONFIRM = "Solution architect at the wave 4 entry check"
ASM_ORDER = ["id","text","why","read","gap","applied_in","confidence","confirm","impact","wp"]

def load(kind, k):
    p = W/kind/f"B-P1-04-{k}.part.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

asm_all, gap_all, added = [], [], 0
for k in keys:
    for r in load("gaps", k):
        gap_all.append(r)
    for r in load("assumptions", k):
        if "confirm" not in r:
            r["confirm"] = CONFIRM
            added += 1
        asm_all.append({key: r[key] for key in ASM_ORDER})

(W/"gaps"/"B-P1-04.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False)+"\n" for r in gap_all), encoding="utf-8")
(W/"assumptions"/"B-P1-04.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False)+"\n" for r in asm_all), encoding="utf-8")
print("gaps", len(gap_all), "assumptions", len(asm_all), "confirm added", added)

for kind in ("gaps","assumptions"):
    for k in keys:
        p = W/kind/f"B-P1-04-{k}.part.jsonl"
        p.unlink()
        print("removed", p)
