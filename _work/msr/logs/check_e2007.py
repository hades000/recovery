"""Check the three fragments against their story files and the part registers."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FRAG = ROOT / "_work/msr/fragments"
KEY = "RWB-P2-E2007-"
bad = 0
for wid in ("APP", "CON", "OPS"):
    sid = KEY + wid
    f = json.loads((FRAG / (sid + ".json")).read_text(encoding="utf-8"))
    t = (ROOT / f["file"]).read_text(encoding="utf-8-sig")
    sec7 = t.split("### 7. Acceptance criteria", 1)[1].split("### 8. Business rules", 1)[0]
    acs = []
    for m in re.finditer(r"(?m)^\s*Scenario:\s*(AC\d+)(.*)$", sec7):
        origin = "legacy RWB-E2-007 " + m.group(1) if "(legacy" in m.group(2) else "new, D-RCV-60"
        acs.append({"id": m.group(1), "origin": origin})
    sec16 = t.split("### 16. Test cases", 1)[1].split("### 17. Guardrails", 1)[0]
    tcs = re.findall(r"(?m)^\|\s*(TC-[A-Za-z0-9-]+)\s*\|", sec16)
    frag_acs = [{"id": a["id"], "origin": a["origin"]} for a in f["acs"]]
    print(sid, "acs ok" if frag_acs == acs else f"ACS MISMATCH {frag_acs} != {acs}")
    print(sid, "tcs ok" if f["tcs"] == tcs else f"TCS MISMATCH {f['tcs']} != {tcs}")
    bad += (frag_acs != acs) + (f["tcs"] != tcs)
    print(sid, "gaps", f["gaps"], "gap_rows", [r["id"] for r in f["gap_rows"]])
    print(sid, "asm", len(f["assumptions"]), [r["id"] for r in f["asm_rows"]] == f["assumptions"])

for name in ("_work/msr/gaps/B-P2-01-E2007.part.jsonl", "_work/msr/assumptions/B-P2-01-E2007.part.jsonl"):
    lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
    rows = [json.loads(x) for x in lines if x.strip()]
    print(name, len(rows), [r["id"] for r in rows])
    official = json.loads("[]")
src = ROOT / "_work/msr/gaps/B-P2-01.jsonl"
src2 = ROOT / "_work/msr/assumptions/B-P2-01.jsonl"
for p, pre in ((src, "CG-B-P2-01-E2007-"), (src2, "ASM-B-P2-01-E2007-")):
    reg = {}
    for raw in p.read_text(encoding="utf-8-sig").splitlines():
        if raw.strip():
            r = json.loads(raw)
            reg[r["id"]] = r
    part = ROOT / (str(p.parent.relative_to(ROOT)) + "/B-P2-01-E2007.part.jsonl")
    for raw in part.read_text(encoding="utf-8").splitlines():
        r = json.loads(raw)
        if json.dumps(r, sort_keys=True, ensure_ascii=False) != json.dumps(reg[r["id"]], sort_keys=True, ensure_ascii=False):
            print("ROW NOT VERBATIM:", r["id"])
            bad += 1
print("bad", bad)
