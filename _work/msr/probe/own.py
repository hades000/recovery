import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
d = json.loads((ROOT / "_work/msr/plan/ownership.json").read_text(encoding="utf-8"))
keys = sys.argv[1:] or ["tables"]
for k in keys:
    v = d[k]
    print("==", k)
    if isinstance(v, dict):
        for name, row in sorted(v.items()):
            if isinstance(row, dict):
                print(f"{name:40s} {row.get('owner','')}")
            else:
                print(name, row)
    else:
        print(v)
