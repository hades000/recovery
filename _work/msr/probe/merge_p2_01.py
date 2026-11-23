"""Coordinator consistency pass and register merge for B-P2-01."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work/msr"
KEYS = ["E1007", "E2001", "E2002", "E2007", "E2033"]
IDS = ["RWB-P2-E1007-APP", "RWB-P2-E1007-CON", "RWB-P2-E1007-INF", "RWB-P2-E1007-OPS",
       "RWB-P2-E2001-APP", "RWB-P2-E2001-CON", "RWB-P2-E2001-OPS",
       "RWB-P2-E2002-APP", "RWB-P2-E2002-CON", "RWB-P2-E2002-OPS",
       "RWB-P2-E2007-APP", "RWB-P2-E2007-CON", "RWB-P2-E2007-OPS",
       "RWB-P2-E2033-APP", "RWB-P2-E2033-CON"]
REQ = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release",
       "legacy", "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided",
       "ops_consumed", "events_published", "events_consumed", "workflows", "prd_ref", "gaps",
       "assumptions", "file"]


def rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def keynum(i):
    m = re.match(r"^(CG|ASM)-B-P2-01-([A-Z]\d+)-(\d+)$", i)
    return (KEYS.index(m.group(2)), m.group(1), int(m.group(3)))


problems = []
reg_g = {r["id"]: r for r in rows(WORK / "gaps/B-P2-01.jsonl")}
reg_a = {r["id"]: r for r in rows(WORK / "assumptions/B-P2-01.jsonl")}

for i in IDS:
    f = json.loads((WORK / "fragments" / f"{i}.json").read_text(encoding="utf-8"))
    for k in REQ:
        if k not in f:
            problems.append(f"{i}: fragment key {k} missing")
    t = (ROOT / f["file"]).read_text(encoding="utf-8")
    # ACs
    scen = re.findall(r"(?m)^\s*Scenario:\s*(AC\d+):?\s*(.*)$", t.split("### 7.", 1)[1].split("### 8.", 1)[0])
    got = [(a, b.strip()) for a, b in scen]
    if [a for a, _ in got] != [a["id"] for a in f["acs"]]:
        problems.append(f"{i}: acs ids {[a['id'] for a in f['acs']]} != story {[a for a,_ in got]}")
    for (ac, line), obj in zip(got, f["acs"]):
        if obj["id"] != ac:
            continue
        expect = f"Scenario: {ac} {line}".strip()
        if obj["text_first_line"].strip() != expect:
            problems.append(f"{i}: {ac} text_first_line differs: {obj['text_first_line']!r} vs {expect!r}")
        if obj["origin"] not in line:
            problems.append(f"{i}: {ac} origin {obj['origin']} not on the scenario line")
    # TCs
    sec = t.split("### 16. Test cases", 1)[1].split("### 17", 1)[0]
    tcs = re.findall(r"(?m)^\|\s*(TC-[A-Za-z0-9-]+)\s*\|", sec)
    if tcs != f["tcs"]:
        problems.append(f"{i}: tcs fragment {f['tcs']} != story {tcs}")
    # citations
    cg = set(re.findall(r"CG-B-P2-01-[A-Za-z0-9]+-\d+", t))
    asm = set(re.findall(r"ASM-B-P2-01-[A-Za-z0-9]+-\d+", t))
    if set(f["gaps"]) != cg:
        problems.append(f"{i}: gaps {sorted(set(f['gaps']) ^ cg)}")
    if set(f["assumptions"]) != asm:
        problems.append(f"{i}: assumptions {sorted(set(f['assumptions']) ^ asm)}")
    if {r["id"] for r in f.get("gap_rows", [])} != set(f["gaps"]):
        problems.append(f"{i}: gap_rows ids")
    if {r["id"] for r in f.get("asm_rows", [])} != set(f["assumptions"]):
        problems.append(f"{i}: asm_rows ids")
    for r in f.get("gap_rows", []):
        if reg_g.get(r["id"]) != r:
            problems.append(f"{i}: gap row {r['id']} differs from the register")
    for r in f.get("asm_rows", []):
        if reg_a.get(r["id"]) != r:
            problems.append(f"{i}: asm row {r['id']} differs from the register")
    if f.get("prd_ref") != "Pending (C1)":
        problems.append(f"{i}: prd_ref")
    if (ROOT / f["file"]).name not in f["file"]:
        problems.append(f"{i}: file path")

# merge the part registers
merged_g, merged_a = [], []
for k in KEYS:
    for kind, acc in (("gaps", merged_g), ("assumptions", merged_a)):
        p = WORK / kind / f"B-P2-01-{k}.part.jsonl"
        for r in rows(p):
            acc.append(r)
merged_g.sort(key=lambda r: keynum(r["id"]))
merged_a.sort(key=lambda r: keynum(r["id"]))
ids_g = [r["id"] for r in merged_g]
ids_a = [r["id"] for r in merged_a]
if len(ids_g) != len(set(ids_g)) or len(ids_a) != len(set(ids_a)):
    problems.append("duplicate ids after the merge")
if set(ids_g) != set(reg_g):
    problems.append(f"gap ids changed: {sorted(set(ids_g) ^ set(reg_g))}")
if set(ids_a) != set(reg_a):
    problems.append(f"assumption ids changed: {sorted(set(ids_a) ^ set(reg_a))}")

cited = set()
for i in IDS:
    t = (ROOT / json.loads((WORK / "fragments" / f"{i}.json").read_text(encoding="utf-8"))["file"]).read_text(encoding="utf-8")
    cited |= set(re.findall(r"(?:CG|ASM)-B-P2-01-[A-Za-z0-9]+-\d+", t))
uncited = (set(ids_g) | set(ids_a)) - cited
if uncited:
    problems.append(f"uncited rows: {sorted(uncited)}")

print("problems:", len(problems))
for p in problems:
    print(" -", p)

if not problems:
    for kind, data in (("gaps", merged_g), ("assumptions", merged_a)):
        p = WORK / kind / "B-P2-01.jsonl"
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in data), encoding="utf-8")
    print("merged:", len(merged_g), "gap rows,", len(merged_a), "assumption rows, all cited")
