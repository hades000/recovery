import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[4]
gaps = [json.loads(l) for l in (ROOT / "_work/msr/gaps/B-TECH-12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
asms = [json.loads(l) for l in (ROOT / "_work/msr/assumptions/B-TECH-12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
gid = {g["id"] for g in gaps}
aid = {a["id"] for a in asms}
print("gaps", len(gaps), "assumptions", len(asms))
print("gap keys missing:", [(g["id"], k) for g in gaps for k in ("id", "title", "source", "section", "description", "evidence", "type", "area", "severity", "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp") if not g.get(k) and k != "legacy_ref"])
print("asm keys missing:", [(a["id"], k) for a in asms for k in ("id", "text", "why", "read", "applied_in", "confidence", "confirm", "impact", "wp") if not a.get(k)])
print("gap.asm unresolved:", [(g["id"], g["asm"]) for g in gaps if g["asm"] not in aid])
print("asm.gap unresolved:", [(a["id"], a["gap"]) for a in asms if a["gap"] and a["gap"] not in gid])
print("types:", sorted({g["type"] for g in gaps}))
print("severity:", sorted({g["severity"] for g in gaps}))
print("confidence:", sorted({a["confidence"] for a in asms}))
print("duplicate ids:", len(gid) - len(gaps), len(aid) - len(asms))
