"""Rebuild the three RWB-P2-E2007 fragments and the two part registers from the shared registers."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FRAG = ROOT / "_work/msr/fragments"
GAPS = ROOT / "_work/msr/gaps/B-P2-01.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B-P2-01.jsonl"
KEY = "RWB-P2-E2007-"


def load_rows(path, prefix):
    out = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        s = raw.strip()
        if not s:
            continue
        row = json.loads(s)
        if row["id"].startswith(prefix):
            out[row["id"]] = row
    return out


gap_rows = load_rows(GAPS, "CG-B-P2-01-E2007-")
asm_rows = load_rows(ASMS, "ASM-B-P2-01-E2007-")
print("gap rows", sorted(gap_rows), len(gap_rows))
print("asm rows", len(asm_rows))

# citations per story file
for wid in ("APP", "CON", "OPS"):
    sid = KEY + wid
    frag_path = FRAG / (sid + ".json")
    frag = json.loads(frag_path.read_text(encoding="utf-8"))
    story = (ROOT / frag["file"]).read_text(encoding="utf-8-sig")
    cited_g = sorted({m for m in re.findall(r"CG-B-P2-01-E2007-\d+", story)}, key=lambda s: int(s.rsplit("-", 1)[1]))
    cited_a = sorted({m for m in re.findall(r"ASM-B-P2-01-E2007-\d+", story)}, key=lambda s: int(s.rsplit("-", 1)[1]))
    print(sid, "cited gaps", cited_g, "cited asm", cited_a)
    missing = [x for x in cited_g if x not in gap_rows] + [x for x in cited_a if x not in asm_rows]
    if missing:
        raise SystemExit(f"cited but no register row: {missing}")
    frag["gaps"] = cited_g
    frag["assumptions"] = cited_a
    frag["gap_rows"] = [gap_rows[x] for x in cited_g]
    frag["asm_rows"] = [asm_rows[x] for x in cited_a]
    order = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release",
             "legacy", "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
             "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file",
             "gap_rows", "asm_rows"]
    out = {k: frag[k] for k in order if k in frag}
    assert set(out) == set(order), set(order) ^ set(out)
    frag_path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

# part registers: every row cited by one of the three files, ids kept as they are
cited_g_all, cited_a_all = [], []
for wid in ("APP", "CON", "OPS"):
    f = json.loads((FRAG / (KEY + wid + ".json")).read_text(encoding="utf-8"))
    for x in f["gaps"]:
        if x not in cited_g_all:
            cited_g_all.append(x)
    for x in f["assumptions"]:
        if x not in cited_a_all:
            cited_a_all.append(x)

gp = ROOT / "_work/msr/gaps/B-P2-01-E2007.part.jsonl"
ap = ROOT / "_work/msr/assumptions/B-P2-01-E2007.part.jsonl"
gp.write_text("".join(json.dumps(gap_rows[x], ensure_ascii=False) + "\n" for x in cited_g_all), encoding="utf-8")
ap.write_text("".join(json.dumps(asm_rows[x], ensure_ascii=False) + "\n" for x in cited_a_all), encoding="utf-8")
print("part gaps", len(cited_g_all), "part asm", len(cited_a_all))
