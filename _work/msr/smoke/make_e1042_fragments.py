"""Writes the three RWB-PLT-E1042 fragments from the story files (scratch helper, D-RCV-60)."""
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
LIB = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-PLT-LIB Shared libraries"
OUT = ROOT / "_work" / "msr" / "fragments"

OPS_CONSUMED = [
    "GET /api/recovery/case/v1/admin/parameters",
    "POST /api/recovery/case/v1/admin/reference-loads",
    "POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve",
    "POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback",
]
EVENT = "rwb.case.ParameterVersionApproved.v1"
REQS = ["REQ-DRI-010", "REQ-ACA-005"]

SPEC = [
    dict(
        id="RWB-PLT-E1042-APP",
        wt="APP", lane="L-PLT-LIB-F", owner="TechX",
        H=["RWB-PLT-E1042-CON", "RWB-PLT-E1043-CON", "RWB-PLT-E1027-CON", "RWB-PLT-TE006-CON",
           "RWB-PLT-E1047-CON", "RWB-PLT-E1044-CON", "RWB-PLT-N001-CON"],
        C=["RWB-P3-E1042-CON", "RWB-P3-E1043-CON"],
        tcs=[f"TC-PLT-E1042-APP-0{n}" for n in range(1, 8)],
        gaps=["CG-B-PLT-LIB-01-E1042-1"],
        assumptions=["ASM-B-PLT-LIB-01-E1042-1", "ASM-B-PLT-LIB-01-E1042-2", "ASM-B-PLT-LIB-01-E1042-3"],
        file="04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 APP Central configuration service and parameter catalog v1.md",
    ),
    dict(
        id="RWB-PLT-E1042-CON",
        wt="CON", lane="CG-W0", owner="TechX",
        H=[], C=[],
        tcs=[f"TC-PLT-E1042-CON-0{n}" for n in range(1, 6)],
        gaps=["CG-B-PLT-LIB-01-E1042-2"],
        assumptions=["ASM-B-PLT-LIB-01-E1042-4", "ASM-B-PLT-LIB-01-E1042-5"],
        file="04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 CON Central configuration service and parameter catalog - contract v1.md",
    ),
    dict(
        id="RWB-PLT-E1042-OPS",
        wt="OPS", lane="L-PLT-LIB-E", owner="DEVOPS",
        H=[], C=[],
        tcs=[f"TC-PLT-E1042-OPS-0{n}" for n in range(1, 7)],
        gaps=["CG-B-PLT-LIB-01-E1042-3"],
        assumptions=["ASM-B-PLT-LIB-01-E1042-6", "ASM-B-PLT-LIB-01-E1042-7"],
        file="04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 OPS Central configuration service and parameter catalog - deployment v1.md",
    ),
]


def scenarios(text):
    out, lines = [], text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\s*Scenario:\s*(AC\d+)\b", line)
        if not m:
            continue
        origin = re.search(r"\((new, [^)]+)\)\s*$", line)
        first = lines[i + 1].strip()
        out.append({"id": m.group(1), "origin": origin.group(1) if origin else "", "text_first_line": first})
    return out


for s in SPEC:
    text = (ROOT / s["file"]).read_text(encoding="utf-8")
    frag = {
        "id": s["id"], "epic": "RWB-PLT-LIB", "service": "platform", "wt": s["wt"],
        "lane": s["lane"], "ready": "Day 1", "owner": s["owner"], "business_epic": "EP01",
        "wave": 0, "release": "30 November 2026", "legacy": "RWB-E1-042",
        "disposition": "Preserved + delta", "H": s["H"], "C": s["C"], "I": [], "X": [],
        "acs": scenarios(text), "tcs": s["tcs"], "reqs": REQS,
        "ops_provided": [], "ops_consumed": OPS_CONSUMED, "events_published": [],
        "events_consumed": [EVENT], "workflows": [], "prd_ref": "Pending (C1)",
        "gaps": s["gaps"], "assumptions": s["assumptions"], "file": s["file"],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{s['id']}.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(s["id"], len(frag["acs"]), "acs;", [a["id"] for a in frag["acs"]])
