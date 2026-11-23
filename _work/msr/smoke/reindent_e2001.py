"""Rewrite the RWB-P7-E2001-APP fragment with the indent of its four peers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
p = ROOT / "_work" / "msr" / "fragments" / "RWB-P7-E2001-APP.json"
frag = json.loads(p.read_text(encoding="utf-8"))
p.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print("keys", len(frag), "acs", frag["acs"])
print("file", frag["file"])
print("exists", (ROOT / frag["file"]).exists())
