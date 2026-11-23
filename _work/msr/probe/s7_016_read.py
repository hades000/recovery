import json, io, sys
p = "_work/msr/wp/B2-S7-007.md"
txt = io.open(p, encoding="utf-8").read()
for line in txt.splitlines():
    line = line.strip()
    if line.startswith("{"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        print(o.get("id"), "reqs=", o.get("reqs"), "acs=", o.get("acs"), "lane=", o.get("lane"))
