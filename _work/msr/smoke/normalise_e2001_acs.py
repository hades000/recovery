"""Normalise the fragment `acs` of RWB-P7-E2001-APP.

The WP line gives `acs: []` for a secondary slice that owns no legacy criterion:
the eight criteria of RWB-E2-001 in P2 and the integration epic. One key's
fragment listed its new criteria under `acs`; the other four keys and the P7
precedent (B-P7-03) leave it empty. Key order is preserved.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
p = ROOT / "_work" / "msr" / "fragments" / "RWB-P7-E2001-APP.json"
frag = json.loads(p.read_text(encoding="utf-8"))
print("before acs:", [(a["id"], a["origin"]) for a in frag["acs"]])
frag["acs"] = []
p.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print("after acs:", frag["acs"], "keys:", len(frag))
