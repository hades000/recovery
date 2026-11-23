"""Probe: append the two missing asm_rows (E2033-14, E2033-15) to RWB-P2-E2033-APP."""
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
frag_p = WORK / "fragments" / "RWB-P2-E2033-APP.json"
reg = [
    json.loads(line)
    for line in io.open(WORK / "assumptions" / "B-P2-01.jsonl", encoding="utf-8")
    if line.strip()
]
want = ["ASM-B-P2-01-E2033-14", "ASM-B-P2-01-E2033-15"]
rows = {r["id"]: r for r in reg}
text = frag_p.read_text(encoding="utf-8")
frag = json.loads(text)

missing = [i for i in want if i in frag["assumptions"]]
if [r.get("id") for r in frag["asm_rows"]] [-2:] == want:
    print("already present")
else:
    chunks = []
    for i in want:
        body = json.dumps(rows[i], ensure_ascii=False, indent=2)
        body = "\n".join("  " + ln for ln in body.splitlines())
        chunks.append("    " + body.lstrip())
    tail = "\n  ]\n}\n"
    assert text.endswith(tail), repr(text[-40:])
    new_text = text[: -len(tail)] + ",\n" + ",\n".join(chunks) + tail
    obj = json.loads(new_text)
    ids = [r.get("id") for r in obj["asm_rows"]]
    assert ids == [r.get("id") for r in frag["asm_rows"]] + want, ids
    frag_p.write_text(new_text, encoding="utf-8")
    print("appended", want, "rows now", len(ids))
