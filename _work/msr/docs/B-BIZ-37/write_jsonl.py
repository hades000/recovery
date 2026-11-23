import json
from pathlib import Path

WORK = Path(r"_work/msr")

gaps = [
    {
        "id": "CG-BIZ-37-1",
        "title": "No rwb-valuation table in the Ownership Map for the route decision",
        "source": "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
        "section": "Tables; Workflows and activities",
        "description": "The Ownership Map lists RouteDecisionWorkflow as S1 rwb-valuation, but the Tables sheet has no owner S1 row (no valuation table and no route-decision table). The Case and Workflow Model v6 needs the S1 tables owned for the RouteDecisionWorkflow row.",
        "evidence": "Ownership Map v1 Tables: no owner S1; Workflows and activities: RouteDecisionWorkflow owner S1; Architecture v5 Text Extract v1 slide 41: rwb-valuation owns valuations and the D6 route decision.",
        "type": "Missing",
        "area": "Data",
        "severity": "P3",
        "needed_by_wave": "3",
        "legacy_ref": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.xlsx (Case file: Valuation)",
        "owner_role": "Architecture owner",
        "asm": "ASM-BIZ-37-1",
        "proposed": "Add the S1 valuation and route-decision tables to the Ownership Map, or confirm that S1 writes only decision_log_entry in P7 and reads valuation_ext in P1.",
        "wp": "B-BIZ-37",
    },
    {
        "id": "CG-BIZ-37-2",
        "title": "CCMS collateral has no target service in the Ownership Map",
        "source": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
        "section": "Case file",
        "description": "The v5 Case file sheet records collateral as coming from CCMS. The Ownership Map has no collateral table and no target service for CCMS; the Case and Workflow Model v6 needs the owner of collateral data after the realignment.",
        "evidence": "Case file v5 row 'Collateral | Collateral records | CCMS'; Ownership Map v1 Tables has no collateral table; Architecture v5 Text Extract v1 slide 41 gives no collateral table to any of the 19 services.",
        "type": "Missing",
        "area": "Data",
        "severity": "P3",
        "needed_by_wave": "3",
        "legacy_ref": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.xlsx (Case file: Collateral)",
        "owner_role": "Architecture owner",
        "asm": "ASM-BIZ-37-2",
        "proposed": "Confirm that CCMS stays an outside system and its data is read through the P1 source-data contract, or name an owning service and table.",
        "wp": "B-BIZ-37",
    },
]

assumptions = [
    {
        "id": "ASM-BIZ-37-1",
        "text": "The RouteDecisionWorkflow (S1 rwb-valuation) owns no table in the current Ownership Map; the route outcome is recorded as decision_log_entry in P7 rwb-decision and valuation_ext stays P1.",
        "why": "The Ownership Map lists the workflow owner S1 but no S1 table, and the model needs an owner for the route decision row.",
        "read": "Ownership Map v1 Tables and Workflows and activities; Architecture v5 Text Extract v1 slide 41",
        "gap": "CG-BIZ-37-1",
        "applied_in": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (Workflow model (v5))",
        "confidence": "Medium",
        "confirm": "Architecture owner",
        "impact": "Documentation only; the S1 service contract and DB story may need a table in a later stage.",
        "wp": "B-BIZ-37",
    },
    {
        "id": "ASM-BIZ-37-2",
        "text": "CCMS stays an outside system; collateral data is read through the P1 rwb-source-data ACE view contract and no Recovery service owns a collateral table.",
        "why": "The v5 Case file names CCMS as the source, and the Ownership Map has no collateral table or target service.",
        "read": "Case file v5; Ownership Map v1 Tables; DP-05",
        "gap": "CG-BIZ-37-2",
        "applied_in": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (Case file ownership (v5))",
        "confidence": "Medium",
        "confirm": "Architecture owner",
        "impact": "Documentation only; integration reads collateral through P1.",
        "wp": "B-BIZ-37",
    },
]

for name, rows in [("gaps", gaps), ("assumptions", assumptions)]:
    p = WORK / name / "B-BIZ-37.jsonl"
    with p.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("WROTE", p)
