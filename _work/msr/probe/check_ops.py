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
        for m in set(re.findall(r"`?(GET|POST|PATCH|PUT|DELETE) (/api/recovery/[a-z-]+/v1[^`\s|;]*)`?", t)):
            meth, path = m
            short = path.split("/api/recovery/")[1].split("/")[0]
            rest = path.split(f"/api/recovery/{short}/v1", 1)[-1] or "/"
            key = f"{meth} {rest}"
            owner = api.get(key, {}).get("owner")
            print(f"  {'OK ' if owner else 'MISS'} {owner or '---':4s} {key:60s} ({short})")
