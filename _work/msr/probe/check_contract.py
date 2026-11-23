import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
own = json.loads((ROOT / "_work/msr/plan/ownership.json").read_text(encoding="utf-8"))
api = own["api"]
wp = (ROOT / "_work/msr/wp/B-ITG-W2-01.md").read_text(encoding="utf-8")
for line in wp.splitlines():
    if line.strip().startswith('{"id"'):
        s = json.loads(line.strip())
        t = (ROOT / s["file"]).read_text(encoding="utf-8")
        print("=" * 20, s["id"])
        paths = set(re.findall(r"`?(?:GET|POST|PATCH|PUT|DELETE) (/api/recovery/[a-z-]+/v1[^`\s|]*)`?", t))
        for p in sorted(paths):
            short = p.split("/api/recovery/")[1].split("/")[0]
            base = p.split("?")[0]
            # try to match the ownership key by suffix (map keys omit the base)
            cand = [k for k in api if base.endswith(k.split("?")[0])]
            owner = api[cand[0]]["owner"] if cand else "NO-MAP-ROW"
            print(f"  {short:12s} {owner:4s} {p}")
        evs = set(re.findall(r"\b(rwb\.[a-z-]+\.[A-Za-z]+\.v1)\b", t))
        print("  events:", sorted(evs))
        print("  queues:", sorted(set(re.findall(r"`(rwb-[a-z-]+)`", t))))
