"""Normalise fragment acs[].text_first_line to the first Given of each scenario (E1020 convention)."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr" / "fragments"
IDS = ["RWB-PLT-E1047-APP", "RWB-PLT-E1047-CON", "RWB-PLT-E1072-APP",
       "RWB-PLT-E1072-CON", "RWB-PLT-TE006-APP", "RWB-PLT-TE006-CON", "RWB-PLT-NF02-APP"]

for sid in IDS:
    fp = WORK / f"{sid}.json"
    frag = json.loads(fp.read_text(encoding="utf-8"))
    text = (ROOT / frag["file"]).read_text(encoding="utf-8")
    m = re.search(r"```gherkin\n(.*?)\n```", text, re.S)
    if not m:
        print("NO GHERKIN", sid)
        continue
    first, title, cur = {}, {}, None
    for line in m.group(1).splitlines():
        s = line.strip()
        sm = re.match(r"Scenario: (AC\d+)", s)
        if sm:
            cur = sm.group(1)
            first[cur] = None
            title[cur] = s
            continue
        if cur and first.get(cur) is None and s.startswith("Given"):
            first[cur] = s
    changed = 0
    for ac in frag.get("acs", []):
        f = first.get(ac.get("id")) or title.get(ac.get("id"))
        if f and ac.get("text_first_line") != f:
            ac["text_first_line"] = f
            changed += 1
    fp.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(sid, "updated", changed)
