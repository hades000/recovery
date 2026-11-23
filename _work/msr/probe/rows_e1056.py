"""Build the candidate rows for RWB-PLT-E1056-OPS (WP B-PLT-OBS-01) as scratch jsonl.

Writes _work/msr/probe/rows-e1056-gaps.jsonl and _work/msr/probe/rows-e1056-assumps.jsonl.
Append with: python -I "_work/msr/probe/append_rows.py" B-PLT-OBS-01 gaps <rows-file>
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROBE = ROOT / "_work" / "msr" / "probe"

GAP = {
    "id": "CG-B-PLT-OBS-01-E1056-1",
    "title": "The job-run record, the run book home and the catalogue-to-run join are not specified after the split",
    "source": "Template and Rules v1 R7.2 s12 and R9; ownership.json (job_catalog, GET /admin/jobs, POST /admin/jobs/{jobId}/rerun, GET /admin/scheduled-jobs); Architecture v5 Text Extract v1 slides 22 and 44; legacy RWB-E1-056 sections 11, 12 and 13; FSD P7 v3 A2.14",
    "section": "3 Preconditions; 12.2 REST operations consumed; 12.7 Tables owned; 13 Solution plan",
    "description": "No source read gives the run identifier shared by the P1 job run log, the P2 job_catalog row and the platform telemetry, the fields of the job-run record, the repository and path of the run books after the split, the default expected duration and alert threshold, the workbook layout and its panels, or the mapping of the 16 legacy job IDs to the v5 mechanisms (JOB-05 durable timers, JOB-11 outbox relay, JOB-13 continuous ingest, AGT-01 and CHK-01 as platform jobs).",
    "evidence": "The ownership map splits the run view and the rerun to P1 rwb-source-data and the catalogue to P2 rwb-integration without a join key, while the legacy story keeps the catalog, the job run log and the restart in one module; FSD P7 v3 A2.14 still lists 13 jobs against the 16 of the legacy story; and no source read gives the run book repository, the job-run record fields or the thresholds beyond the legacy 1.5 times the expected duration.",
    "type": "Missing",
    "area": "Platform and observability",
    "severity": "P2",
    "needed_by_wave": "0",
    "legacy_ref": "RWB-E1-056",
    "owner_role": "Solution architect",
    "asm": "ASM-B-PLT-OBS-01-E1056-1",
    "proposed": "Publish the job-run record and its identifier, the run book repository and path, the default expected duration and alert threshold per job, the workbook panel set and the 16-row to v5 mechanism mapping at the wave 0 entry check, and agree the join key with the P1 and P2 owners at the same review.",
    "wp": "B-PLT-OBS-01",
}

ASSUMPTIONS = [
    {
        "id": "ASM-B-PLT-OBS-01-E1056-1",
        "text": "The 16-row Epic 1 catalogue of the legacy story is the baseline (JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15, JOB-17, AGT-01 and CHK-01) and the 13-row list in FSD P7 v3 A2.14 is the older count; nothing is dropped from the legacy set.",
        "why": "Two sources give different job counts and the story must fix one baseline for the catalogue load, the pipeline gate and the workbook, otherwise a job can be monitored in one artefact and missing from another.",
        "read": "Legacy RWB-E1-056 section 3 and section 7 Background (16 rows with first release E1); Architecture v5 Text Extract v1 slide 44 (the job map that gives each of the 16 a mechanism and an owner service); FSD P7 v3 A2.14 (the older 13-row list); ownership.json jobs JOB-01 to JOB-22",
        "gap": "CG-B-PLT-OBS-01-E1056-1",
        "applied_in": "Section 3 Preconditions, section 7 Acceptance criteria and section 11 Data",
        "confidence": "High",
        "confirm": "Solution architect",
        "impact": "The gate and the workbook check 16 rows; adding or retiring a job is a catalogue row changed through the P2 admin operation, not a code change. A later reconciliation with the FSD list adds rows, it does not remove them.",
        "wp": "B-PLT-OBS-01",
    },
    {
        "id": "ASM-B-PLT-OBS-01-E1056-2",
        "text": "job_catalog stays with P2 rwb-integration and the 16-row Epic 1 baseline is loaded through its admin operation as data; the job view and the rerun stay with P1 rwb-source-data; this story owns the run books, the pipeline gate, the workbook and the guard definitions only.",
        "why": "The ownership map puts the catalogue with P2 and the run view and rerun with P1, while the legacy story owns all three in one module; the story cannot keep writing the table once P2 owns it, and it must still deliver the run books and the workbook on Day 1.",
        "read": "ownership.json tables job_catalog (owner P2) and api GET /admin/jobs, POST /admin/jobs/{jobId}/rerun (owner P1) and GET /admin/scheduled-jobs (owner P2); Architecture v5 Text Extract v1 slide 41 (rwb-integration owns interface config and file runs, rwb-source-data owns freshness and reconciliation)",
        "gap": "CG-B-PLT-OBS-01-E1056-1",
        "applied_in": "Section 3 Preconditions, section 11 Data, section 12.1, section 12.7 and section 13 Solution plan",
        "confidence": "Medium",
        "confirm": "Solution architect",
        "impact": "If the read is wrong the catalogue load moves to whichever service is named owner, and the story keeps the run books, the gate and the workbook unchanged; the guard definitions move with the rerun operation.",
        "wp": "B-PLT-OBS-01",
    },
    {
        "id": "ASM-B-PLT-OBS-01-E1056-3",
        "text": "The job-run signal is a structured telemetry record (OpenTelemetry span attributes) plus the P1 job run log, not a Kafka topic, because the v5 event catalogue carries no job-run event and the platform baseline (RWB-PLT-N005-OPS) carries the telemetry.",
        "why": "The legacy story writes a rwb.job.run event, but the v5 event catalogue has no job-run event and the realignment forbids inventing a topic; the workbook still needs one signal per run at start and end.",
        "read": "Architecture v5 Text Extract v1 slides 42 and 43 (event catalogue 1/2 and 2/2: 30 rows, no job-run event); slide 8 (Observability: OpenTelemetry across the 19 services); legacy RWB-E1-056 section 4 step 5 (rwb.job.run at start and end with job ID, business date, status and duration)",
        "gap": "CG-B-PLT-OBS-01-E1056-1",
        "applied_in": "Section 4 step 5, section 12.3, section 12.9 and section 13 Solution plan",
        "confidence": "Medium",
        "confirm": "Solution architect",
        "impact": "The workbook and the alerts read the span attributes and the P1 job run log; if a topic is later required, the record is published from the same fields and no run book or alert changes.",
        "wp": "B-PLT-OBS-01",
    },
    {
        "id": "ASM-B-PLT-OBS-01-E1056-4",
        "text": "The run books live in the platform repository at docs/operations/runbooks/<job ID>.md and are named by the catalogue row's runbook_path, so the gate can check them without reaching into another service's repository.",
        "why": "After the split the 16 jobs run in 12 different owning services, and a run book per service repository would leave the gate with 16 checkouts; the legacy story already fixed the folder name but not the repository.",
        "read": "Legacy RWB-E1-056 section 4 step 2 and section 13 (run books in docs/operations/runbooks/); Architecture v5 Text Extract v1 slide 44 (each job runs in its owning service); ownership.json (no run book repository is named)",
        "gap": "CG-B-PLT-OBS-01-E1056-1",
        "applied_in": "Section 4 step 2, section 12.7, section 13 Solution plan and section 16 Test cases",
        "confidence": "Medium",
        "confirm": "DevOps lead",
        "impact": "The gate resolves every run book from one repository and one folder; a move of the folder changes the runbook_path column in 16 catalogue rows and one constant in the gate, and no run book content changes.",
        "wp": "B-PLT-OBS-01",
    },
    {
        "id": "ASM-B-PLT-OBS-01-E1056-5",
        "text": "The story keeps wave 0 with the business epic tag EP01, because the Epic 1 jobs need the run books and the monitoring before wave 1 starts and the platform epic is wave 0 by the wave map.",
        "why": "The wave map puts EP01 in wave 1 and the platform epics in wave 0; the story carries both, and the earlier wave is the one that lets the run books and the alerts exist before the first Epic 1 job runs.",
        "read": "Template and Rules v1 R5.6 (wave map: EP01 wave 1, platform and NF wave 0) and R5.7 (Day-1 rules); WP B-PLT-OBS-01 story line (wave 0, business epic EP01, ready Day 1)",
        "gap": "CG-B-PLT-OBS-01-E1056-1",
        "applied_in": "Metadata Wave and Business epic rows, section 2 Business rationale and section 3 Preconditions",
        "confidence": "High",
        "confirm": "Delivery lead",
        "impact": "The story is scheduled in wave 0 and marks the Epic 1 business epic; if the wave is moved to 1 the run books and the alerts land after the first Epic 1 job run, and only the schedule moves.",
        "wp": "B-PLT-OBS-01",
    },
]


def dump(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(path.name, len(rows))


dump(PROBE / "rows-e1056-gaps.jsonl", [GAP])
dump(PROBE / "rows-e1056-assumps.jsonl", ASSUMPTIONS)
