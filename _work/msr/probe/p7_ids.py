"""Probe: cited CG/ASM ids vs register ids for the 14 B-P7-01 story files, and a light shape audit."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
WP = "B-P7-01"
STORY_DIR = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P7 rwb-decision (Decision and rules)"
IDS = ["RWB-P7-E1008-APP", "RWB-P7-E1008-CON", "RWB-P7-E1008-DB", "RWB-P7-E1008-OPS",
       "RWB-P7-E1027-APP", "RWB-P7-E1027-CON", "RWB-P7-E2005-APP", "RWB-P7-E2005-CON",
       "RWB-P7-E2013-APP", "RWB-P7-E2013-CON", "RWB-P7-E2013-OPS",
       "RWB-P7-E2014-APP", "RWB-P7-E2014-CON", "RWB-P7-E2014-OPS"]
FILES = {
    "RWB-P7-E1008-APP": "RWB P7 E1008 APP Decision log store v1, append only and hash chained v1.md",
    "RWB-P7-E1008-CON": "RWB P7 E1008 CON Decision log store v1, append only and hash chained - contract v1.md",
    "RWB-P7-E1008-DB": "RWB P7 E1008 DB Decision log store v1, append only and hash chained - ACE DB v1.md",
    "RWB-P7-E1008-OPS": "RWB P7 E1008 OPS Decision log store v1, append only and hash chained - deployment v1.md",
    "RWB-P7-E1027-APP": "RWB P7 E1027 APP Decision log writer v1 v1.md",
    "RWB-P7-E1027-CON": "RWB P7 E1027 CON Decision log writer v1 - contract v1.md",
    "RWB-P7-E2005-APP": "RWB P7 E2005 APP Decision log query API for audit v1.md",
    "RWB-P7-E2005-CON": "RWB P7 E2005 CON Decision log query API for audit - contract v1.md",
    "RWB-P7-E2013-APP": "RWB P7 E2013 APP Approval routing with the delegation of authority table v1.md",
    "RWB-P7-E2013-CON": "RWB P7 E2013 CON Approval routing with the delegation of authority table - contract v1.md",
    "RWB-P7-E2013-OPS": "RWB P7 E2013 OPS Approval routing with the delegation of authority table - deployment v1.md",
    "RWB-P7-E2014-APP": "RWB P7 E2014 APP Approval screen for D7.1 demand and recall notices v1.md",
    "RWB-P7-E2014-CON": "RWB P7 E2014 CON Approval screen for D7.1 demand and recall notices - contract v1.md",
    "RWB-P7-E2014-OPS": "RWB P7 E2014 OPS Approval screen for D7.1 demand and recall notices - deployment v1.md",
}
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
reg, dup = set(), []
for kind in ("gaps", "assumptions"):
    for p in sorted((WORK / kind).glob(f"{WP}.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                i = json.loads(line)["id"]
                if i in reg:
                    dup.append(i)
                reg.add(i)

used = {}
for i in IDS:
    for p in (STORY_DIR / FILES[i], WORK / "fragments" / f"{i}.json"):
        if p.exists():
            for c in set(cite.findall(p.read_text(encoding="utf-8"))):
                used.setdefault(c, []).append(p.name)
missing = {c: v for c, v in used.items() if c not in reg}
print("register ids:", len(reg), "| duplicated:", dup or "none", "| cited ids:", len(used))
print("cited but no row:", json.dumps(missing, indent=1) if missing else "none")
for i in IDS:
    f, frag = STORY_DIR / FILES[i], WORK / "fragments" / f"{i}.json"
    if not f.exists() or not frag.exists():
        print(i, "MISSING FILE", f.exists(), frag.exists()); continue
    t = f.read_text(encoding="utf-8")
    d = json.loads(frag.read_text(encoding="utf-8"))
    bad = [k for k in ("id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
                       "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
                       "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file") if k not in d]
    acs = len(re.findall(r"(?m)^\s*Scenario: AC\d+", t))
    tabs = len(re.findall(r"(?m)^#### 12\.\d", t))
    print(f"{i:18s} ACs={acs:2d} 12tables={tabs} fragkeys_ok={not bad} gaps={len(d['gaps'])} asm={len(d['assumptions'])}")
