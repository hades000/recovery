"""Scratch verifier for WP B-S2-06 (not a deliverable)."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
W = ROOT / "_work" / "msr"
wp = (W / "wp" / "B-S2-06.md").read_text(encoding="utf-8")
rows = [json.loads(l) for l in wp.splitlines() if l.startswith("{") and '"id": "RWB-S2-E20' in l]
bad = 0
for r in rows:
    f = json.loads((W / "fragments" / f"{r['id']}.json").read_text(encoding="utf-8"))
    for k in ("epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "legacy", "disposition", "H", "C", "I", "X", "file"):
        if f.get(k) != r.get(k):
            print("MISMATCH", r["id"], k, "|fragment:", f.get(k), "|wp:", r.get(k)); bad += 1
    if f.get("release") != r["release"]:
        print("RELEASE", r["id"], f.get("release")); bad += 1
    if f.get("prd_ref") != "Pending (C1)":
        print("PRD", r["id"], f.get("prd_ref")); bad += 1
    miss = set(r["tcs_legacy"]) - set(f["tcs"])
    if miss:
        print("TC missing", r["id"], sorted(miss)); bad += 1
    cit = set()
    txt = (ROOT / f["file"]).read_text(encoding="utf-8")
    for c in ("CG-B-S2-06-", "ASM-B-S2-06-"):
        for m in __import__("re").findall(c + r"([A-Za-z0-9]+-\d+)", txt):
            cit.add(c + m)
    own = set(f["gaps"]) | set(f["assumptions"])
    extra = cit - own
    if extra:
        print("cited but not in fragment", r["id"], sorted(extra)); bad += 1
    print(r["id"], "acs", len(f["acs"]), "tcs", len(f["tcs"]), "gaps", len(f["gaps"]), "asm", len(f["assumptions"]))
print("problems:", bad)
