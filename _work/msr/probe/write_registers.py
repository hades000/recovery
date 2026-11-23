import json
from pathlib import Path

WP = "B-ITG-W1-05"
gaps = []
assumptions = []


def gap(n, **kw):
    row = {
        "id": n,
        "title": kw["title"],
        "source": kw["source"],
        "section": kw["section"],
        "description": kw["description"],
        "evidence": kw["evidence"],
        "type": kw["type"],
        "area": kw["area"],
        "severity": kw["severity"],
        "needed_by_wave": "1",
        "legacy_ref": kw["legacy_ref"],
        "owner_role": kw["owner_role"],
        "asm": kw["asm"],
        "proposed": kw["proposed"],
        "wp": WP,
    }
    gaps.append(row)


def asm(n, **kw):
    row = {
        "id": n,
        "text": kw["text"],
        "why": kw["why"],
        "read": kw["read"],
        "gap": kw["gap"],
        "applied_in": kw["applied_in"],
        "confidence": kw["confidence"],
        "confirm": kw["confirm"],
        "impact": kw["impact"],
        "wp": WP,
    }
    assumptions.append(row)


# ---------------------------------------------------------------- RWB-E1-030
gap("CG-B-ITG-W1-05-E1030-1",
    title="Rebalancing trigger, measure delivery and rerun facade change in the target",
    source="04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 030 Daily rebalancing and queue measures v1.md (sections 3, 4, 5, 12 and 13); Recovery Workbench Architecture v5 Text Extract v1 slides 14, 15, 20, 42, 43 and 44; _work/msr/plan/ownership.json",
    section="3 Preconditions; 4 Flow; 12 Contract; 12.6 Schedules; 13 Solution plan",
    description="The legacy story runs JOB-06 on Quartz at 06:30, copies the queue snapshot to the data lake by JOB-15 and publishes the QueueMeasureService interface that P9 reads for Power BI. In the target JOB-06 is a Temporal Schedule in P3 rwb-case (Arch v5 slide 44), JOB-13 ingests the decision records continuously, JOB-15 has no lake copy and the measures are a projection in P9 rwb-reporting (DP-17), while the job catalogue and the rerun operation stay with P1 rwb-source-data under the Ownership Map. The sources therefore name neither the SIT Schedule identifier and its catch-up window, nor the event that marks a business date as published, nor the facade that reruns JOB-06 while the Schedule lives in another service.",
    evidence="RWB-E1-030 sections 3, 4, 12 and 13 (Quartz 06:30, JOB-15 lake copy, QueueMeasureService, POST /api/recovery/v1/admin/jobs/{jobId}/rerun); Arch v5 slide 44 (JOB-03 and JOB-06 owner rwb-case, JOB-06 Schedule, JOB-13 continuous Kafka, JOB-15 Airflow trigger with no data lake); slide 15 (P9 Schedule measures 01:30, topic rwb.reporting.events.v1 with ReportPublished); slide 14 (Act: allocate, transfer, rebalance); Ownership Map jobs JOB-06 owner P3 and JOB-15 owner P9, api GET /admin/jobs and POST /admin/jobs/{jobId}/rerun owner P1, tables queue_measure and assignment owner P3.",
    type="Conflict",
    area="Rebalancing and queue measures integration",
    severity="P2",
    legacy_ref="RWB-E1-030",
    owner_role="Tech lead",
    asm="ASM-B-ITG-W1-05-E1030-1",
    proposed="Register JOB-06 as a Schedule in rwb-case and name its identifier, overlap policy and catch-up window at the integration pack review; keep the P1 job catalogue as the operations facade for the run record and the rerun; fix rwb.reporting.ReportPublished.v1 as the publish marker and the five-minute ledger target as the collection measure.")

asm("ASM-B-ITG-W1-05-E1030-1",
    text="JOB-06 runs as a Temporal Schedule in rwb-case at 06:30 with overlap SKIP and the platform catch-up window (DP-10; Arch v5 slide 44), and the P1 rwb-source-data job catalogue remains the operations facade: GET /admin/jobs holds the run record and POST /admin/jobs/JOB-06/rerun asks the Schedule to run again, while the suite observes the outcome through the P3 case contract.",
    why="The legacy story runs JOB-06 on Quartz and reruns it from the job monitor; the target has no shared Quartz table and the Ownership Map leaves the job operations with P1.",
    read="RWB-E1-030 sections 3, 4, 12 and 13; Arch v5 slide 44; Ownership Map jobs JOB-06 owner P3 and api GET /admin/jobs, POST /admin/jobs/{jobId}/rerun owner P1; Template and Rules v1 section R5.5 DP-10.",
    gap="CG-B-ITG-W1-05-E1030-1",
    applied_in="Story sections 3, 4, 5, 12.2 and 12.6; fragment ops_consumed and workflows",
    confidence="Medium",
    confirm="P3 case owner and P1 source-data owner",
    impact="The Schedule stays in the owning service; the run record and the rerun keep one operations path, and the assertions are unchanged.")

asm("ASM-B-ITG-W1-05-E1030-2",
    text="The queue measures reach P9 rwb-reporting as a projection built from the P3 events, and P9 marks the business date as published with rwb.reporting.ReportPublished.v1 on rwb.reporting.events.v1; no data lake copy exists (DP-17) and the measure read is GET /api/recovery/reporting/v1/reports/measures.",
    why="The legacy story copies the snapshot to the lake by JOB-15 and P9 reads the published interface; Arch v5 removes the lake and gives P9 the measures Schedule and the ReportPublished event.",
    read="RWB-E1-030 sections 4, 12 and 13; Arch v5 slide 15 (P9 Schedule measures 01:30; rwb.reporting.events.v1: ReportPublished); slide 44 (JOB-13 continuous, JOB-15 no data lake); Template and Rules v1 section R5.5 DP-17.",
    gap="CG-B-ITG-W1-05-E1030-1",
    applied_in="Story sections 2, 7 (AC2), 12.4 and 13",
    confidence="Medium",
    confirm="P9 reporting owner and RW-BIANAL",
    impact="Power BI reads P9; the snapshot values, the reconciliation rule and the 06:52 timing are unchanged.")

asm("ASM-B-ITG-W1-05-E1030-3",
    text="The fail-closed point is the local decision record write in rwb-case: a record that cannot be written stops that case only and the run continues, while a run in which every write fails moves nothing and leaves no partial assignment; a central ledger lag is reported against the five-minute target and never blocks the run (DP-03).",
    why="Legacy AC6 and TC-E1-030-12 fail the monolith decision log store; Arch v5 slide 28 separates the local record from the central ledger, so the fail-closed point and the fault-switch scope have to be named.",
    read="RWB-E1-030 section 5 X3, section 7 AC6 and AC11, section 16 TC-E1-030-12; Arch v5 slides 20 and 28; Template and Rules v1 section R5.5 DP-03; ADR-022.",
    gap="CG-B-ITG-W1-05-E1030-1",
    applied_in="Story sections 5, 7 (AC6, AC11), 12.8 and 13",
    confidence="Medium",
    confirm="P7 decision owner and Risk and Internal Audit",
    impact="One failed record costs one move; a total failure costs the run, and no case moves without its record.")

# ---------------------------------------------------------------- RWB-E1-031
gap("CG-B-ITG-W1-05-E1031-1",
    title="Export access entry, masking source and owner display name path are not named for the target",
    source="04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 031 Queue and owner on the case list with filters v1.md (sections 3, 4, 5, 7, 12 and 13); Recovery Workbench Architecture v5 Text Extract v1 slides 14, 20 and 46; _work/msr/plan/ownership.json",
    section="3 Preconditions; 4 Flow; 7 Acceptance criteria; 12 Contract; 13 Solution plan",
    description="The legacy story writes the export access event with P4 AccessEventPublisher before the file is made, applies FieldMasker from RWB-E1-037 and takes owner display names from the ACE user directory in the common module. In the target the access log stays with P4 rwb-access, the masking rules are P4's and are applied over the P1 masked view columns, and the list and the export stay with P3 rwb-case under the per-service base. The sources name neither the contract through which the suite reads the export entry back, nor the masking source for the xlsx, nor how the owner display names are held in SIT.",
    evidence="RWB-E1-031 sections 3, 4, 5, 7, 12 and 13 (AccessEventPublisher with eventCode AC-EXPT, FieldMasker, caselist.export.maxrows, owner display names from the ACE user directory); Arch v5 slide 14 (P4 owns the access log and the masking policy); slide 20 (permission data cached from rwb-access); slide 46 note (masking is applied by rwb-source-data); Ownership Map api GET /cases, GET /cases/export, GET /queues and GET /admin/parameters owner P3, GET /admin/access-log, GET /admin/roles and GET /me/session owner P4, tables recovery_case and queue owner P3, role and masking_rule owner P4.",
    type="Missing",
    area="Case list and export integration",
    severity="P2",
    legacy_ref="RWB-E1-031",
    owner_role="Tech lead",
    asm="ASM-B-ITG-W1-05-E1031-1",
    proposed="Read the export entry back through the P4 access-log contract, keep AC-EXPT as the event code and the filters and row count in the entry, apply the P4 masking rules over the P1 masked columns, and keep the display names synthetic in SIT.")

asm("ASM-B-ITG-W1-05-E1031-1",
    text="The export access event is written by P3 rwb-case through the P4 rwb-access access-log contract before the file is made, with event code AC-EXPT, the actor, the time, the filters and the row count, and the suite reads it back through GET /api/recovery/access/v1/admin/access-log.",
    why="The legacy story writes the event through P4's AccessEventPublisher inside one monolith; the target keeps the access log in P4 and the export in P3, so the write path and the read path have to be stated.",
    read="RWB-E1-031 section 4 step 7, section 12 (AccessEventPublisher), section 13; Arch v5 slide 14 (P4 access log); Ownership Map api GET /admin/access-log owner P4 and GET /cases/export owner P3.",
    gap="CG-B-ITG-W1-05-E1031-1",
    applied_in="Story sections 3, 4, 7 (AC2, AC5), 12.2 and 12.8",
    confidence="Medium",
    confirm="P3 case owner and P4 access owner",
    impact="The export is never made without its entry; the event fields and MSG-P7-003 are unchanged.")

asm("ASM-B-ITG-W1-05-E1031-2",
    text="Masking on the export is applied from the masking rules of P4 rwb-access over the P1 masked view columns before a value reaches the xlsx, and the suite asserts field IDs and masked flags only, never a value.",
    why="The legacy story applies FieldMasker from RWB-E1-037; the target keeps the masking rules in P4 and applies masking at the data read, so the source for the export columns has to be named.",
    read="RWB-E1-031 section 4, section 8 BR4, section 17; Arch v5 slide 14 (P4 masking policy) and slide 46 note; Template and Rules v1 section R5.5 DP-08; REQ-ACA-005.",
    gap="CG-B-ITG-W1-05-E1031-1",
    applied_in="Story sections 8 (BR4, BR7), 11 and 17; fragment ops_consumed",
    confidence="Medium",
    confirm="P4 access owner and RW-COMPLY",
    impact="The export carries masked columns only; no clear personal value reaches the file.")

asm("ASM-B-ITG-W1-05-E1031-3",
    text="The export row limit and the queue and status lists are data rows read through the P3 parameters, queues and lists contracts (DP-06, DP-07), and owner display names come from the ACE user directory in the common module and are synthetic in SIT.",
    why="The legacy story reads caselist.export.maxrows from RWB-E1-042, the LOVs from the list interface and the display names from the monolith's common module; the target moves parameters and reference data to P3 while the user directory stays in ACE common.",
    read="RWB-E1-031 sections 3 and 13; Ownership Map tables parameter_catalog and parameter_value owner P3, api GET /admin/parameters and GET /admin/lists/{listCode} owner P3; Template and Rules v1 section R3 default ruling and section R5.5 DP-06 and DP-07.",
    gap="CG-B-ITG-W1-05-E1031-1",
    applied_in="Story sections 3, 8 (BR8, BR9), 12.2 and 13",
    confidence="Medium",
    confirm="P3 case owner and ACE team lead",
    impact="No business value is hard-coded; the limit 10,000 stays a data row and the display names stay outside the Recovery contracts.")

# ---------------------------------------------------------------- RWB-E1-032
gap("CG-B-ITG-W1-05-E1032-1",
    title="Intake trigger, attach operation and parameter home change in the target",
    source="04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 032 Automatic attach from the OCR intake v1.md (sections 3, 4, 5, 7, 12 and 13); Recovery Workbench Architecture v5 Text Extract v1 slides 16, 42 and 44; _work/msr/plan/ownership.json",
    section="3 Preconditions; 4 Flow; 7 Acceptance criteria; 12 Contract; 13 Solution plan",
    description="The legacy story runs the match step inside the Quartz JOB-12 every 15 minutes, lists held items with GET /review-items and attaches them with POST /intake-items/{intakeItemId}/attach, and holds the case-number pattern, the account-number pattern and the classification threshold in document_hub_parameter. In the target JOB-12 is an event-started DocumentIntakeWorkflow in P5 with KEDA workers, the reviewer's attach is POST /intake-items/{intakeItemId}/resolve with the item version, and DP-06 sends parameters to the P3 rwb-case parameters contract while the Ownership Map keeps document_hub_parameter with P5. The sources name neither the trigger of the intake in wave 1, nor the exact resolve contract, nor the single home of the three parameters, and they do not name the P6 letter copy or the S9 partner result as intake sources.",
    evidence="RWB-E1-032 sections 3, 4, 5, 7, 12 and 13 (JOB-12 every 15 minutes, /review-items, /intake-items/{intakeItemId}/attach, CASE_NO_PATTERN, ACCOUNT_NO_PATTERN, CLASSIFY_THRESHOLD, document_hub_parameter); Arch v5 slide 16 (DocumentIntakeWorkflow: OCR, classify, extract; AgentRunCompleted for classification; P10 AgentRunWorkflow), slide 42 (EV-16 DocumentStored, EV-17 DocumentFieldsExtracted), slide 44 (JOB-12 event plus KEDA workers); Ownership Map api GET /review-items, GET /intake-items/{intakeItemId}, GET /intake-items/{intakeItemId}/content, POST /intake-items/{intakeItemId}/resolve and POST /cases/{caseId}/documents owner P5, POST /cases/{caseId}/notices owner P6, POST /partner/instructions/{instructionId}/results owner S9, table document_hub_parameter owner P5; workflows DocumentIntakeWorkflow owner P5, AgentRunWorkflow owner P10, NoticeDispatchWorkflow owner P6.",
    type="Conflict",
    area="Document intake and attach integration",
    severity="P2",
    legacy_ref="RWB-E1-032",
    owner_role="Tech lead",
    asm="ASM-B-ITG-W1-05-E1032-1",
    proposed="Start the intake from DocumentStored with KEDA workers, keep /review-items and /resolve with the item version, keep the three parameters as document_hub_parameter rows read as data, and prove the P6 letter copy and the S9 partner result on the same match path.")

asm("ASM-B-ITG-W1-05-E1032-1",
    text="JOB-12 is an event-started DocumentIntakeWorkflow in P5 rwb-document, started by DocumentStored and scaled on KEDA workers, and it runs OCR, classify, extract and match in that order; no Schedule exists in the target (DP-10; Arch v5 slide 44).",
    why="The legacy story runs JOB-12 as a Quartz job every 15 minutes; the target has no shared Quartz tables and gives the intake to the document service as an event-started workflow.",
    read="RWB-E1-032 sections 3, 4, 5, 12 and 13; Arch v5 slide 16 and slide 44; Template and Rules v1 section R5.5 DP-10.",
    gap="CG-B-ITG-W1-05-E1032-1",
    applied_in="Story sections 3, 4, 12.5 and 12.6; fragment workflows",
    confidence="Medium",
    confirm="P5 document owner and platform lead",
    impact="Intake stays within the 60-minute target; the trigger and the worker model change, the outcome does not.")

asm("ASM-B-ITG-W1-05-E1032-2",
    text="The held-item list is GET /review-items and the reviewer's attach is POST /intake-items/{intakeItemId}/resolve with the case, the type and the item version; the legacy /attach name is a marker only, and the 409 on a changed version is kept.",
    why="The legacy story names GET /review-items, GET /intake-items/{intakeItemId} and POST /intake-items/{intakeItemId}/attach under /api/recovery/v1 while the Ownership Map names /review-items and /resolve on P5.",
    read="RWB-E1-032 sections 5, 7 AC12 to AC15 and 12; Ownership Map api GET /review-items and POST /intake-items/{intakeItemId}/resolve owner P5; Template and Rules v1 section R5.5 DP-13.",
    gap="CG-B-ITG-W1-05-E1032-1",
    applied_in="Story sections 4, 7 (AC12 to AC15), 12.2 and 12.8; fragment ops_consumed",
    confidence="Medium",
    confirm="P5 document owner",
    impact="One attach path with an item version; the statuses 201, 403, 409 and 422 and the messages are unchanged.")

asm("ASM-B-ITG-W1-05-E1032-3",
    text="The three intake parameters CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD stay data rows in document_hub_parameter, owned by P5 under the Ownership Map, and are read as data; the suite sets none of them in code (DP-06).",
    why="The legacy story holds the three values in document_hub_parameter while DP-06 sends parameters to the P3 parameters contract; the Ownership Map keeps the table with P5, so the home has to be stated.",
    read="RWB-E1-032 section 3, section 8 BR2 and BR4; Ownership Map table document_hub_parameter owner P5; Template and Rules v1 section R5.5 DP-06.",
    gap="CG-B-ITG-W1-05-E1032-1",
    applied_in="Story sections 3, 8 (BR10), 11 and 13",
    confidence="Medium",
    confirm="P5 document owner and P3 case owner",
    impact="The values stay configuration; the threshold 0.80 and the two patterns are unchanged.")

asm("ASM-B-ITG-W1-05-E1032-4",
    text="A partner result submitted through S9 rwb-partner and a letter copy generated by P6 rwb-comms become intake items with source PARTNER and COMMS respectively; the legacy story names neither source, and the match rules and outcomes are the same for every source.",
    why="The plan gives this legacy key APP stories on P5, S9, P3, P6 and P7, while the legacy story covers scans, partner files and emails without naming the P6 and S9 route in the target.",
    read="RWB-E1-032 sections 3, 4 and 17; Arch v5 slide 16 (P6 document generate) and slide 17 (S9 partner uploads; P6 POST /notices); Ownership Map api POST /cases/{caseId}/notices owner P6 and POST /partner/instructions/{instructionId}/results owner S9; workflow NoticeDispatchWorkflow owner P6.",
    gap="CG-B-ITG-W1-05-E1032-1",
    applied_in="Story sections 3, 4, 7 (AC1, AC4, AC12) and 12.2",
    confidence="Medium",
    confirm="P6 comms owner, S9 partner owner and P5 document owner",
    impact="Every source follows the same match path; no rule, threshold or outcome changes.")

# ---------------------------------------------------------------- RWB-E1-034
gap("CG-B-ITG-W1-05-E1034-1",
    title="Moved template operations, screen route and freshness stamp need a target reading",
    source="04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 034 Letter template management v1.md (sections 3, 5, 7, 12, 13 and 15); Recovery Workbench Architecture v5 Text Extract v1 slides 16, 17 and 20; _work/msr/plan/ownership.json",
    section="3 Preconditions; 7 Acceptance criteria; 12 Contract; 13 Solution plan; 15 Screens and states",
    description="The legacy story is Moved (no impact): five endpoints under /api/recovery/v1, SCR-33 built behind its flag in Epic 1 while screens.txt lists it first in Epic 2, the freshness stamp of RWB-E1-015 on the screen and the generation hold of R-LIT-04. In the target the operations belong to P6 rwb-comms under /api/recovery/comms/v1/admin/templates and the screen is reached through gateway-bff, but the sources do not name the base and route of the five operations in the registry, the composite route of SCR-33, the data product whose stamp the catalog shows, or the point at which a withdrawal holds generation.",
    evidence="RWB-E1-034 sections 3, 5, 7, 12, 13 and 15 (five endpoints, SCR-33, RWB-E1-015 freshness, R-LIT-04 hold); Arch v5 slide 16 (rwb-comms owns templates and merge fields; template and merge_field in rwb_comms), slide 17 (P6 OUT: document generate letter), slide 20 (gateway-bff); Ownership Map api GET /admin/templates, POST /admin/templates, GET /admin/templates/{templateId}/content, POST /admin/templates/{templateId}/approve and POST /admin/templates/{templateId}/withdraw owner P6, GET /data-products/freshness owner P1, tables template and merge_field owner P6, data_product owner P1.",
    type="Missing",
    area="Letter template management integration",
    severity="P2",
    legacy_ref="RWB-E1-034",
    owner_role="Tech lead",
    asm="ASM-B-ITG-W1-05-E1034-1",
    proposed="Read the five operations from the P6 contract in the registry, keep every request, response, state and message unchanged, read the stamp from the P1 freshness contract, and leave the generation hold to the P6 notice workflow and RWB-E1-052.")

asm("ASM-B-ITG-W1-05-E1034-1",
    text="The five template operations move unchanged to P6 rwb-comms under /api/recovery/comms/v1/admin/templates, keeping their request and response shapes, their states and their messages; the legacy /api/recovery/v1 paths are monolith markers only (DP-13).",
    why="The story is Moved (no impact); the Ownership Map gives template and merge_field to P6 and names the operations /admin/templates, while the legacy base is the monolith one.",
    read="RWB-E1-034 sections 12 and 13; Ownership Map api GET /admin/templates, POST /admin/templates, GET /admin/templates/{templateId}/content, POST /admin/templates/{templateId}/approve, POST /admin/templates/{templateId}/withdraw owner P6 and tables template and merge_field owner P6; Template and Rules v1 section R5.5 DP-13.",
    gap="CG-B-ITG-W1-05-E1034-1",
    applied_in="Story sections 2, 3, 12.2 and 13; fragment ops_consumed",
    confidence="High",
    confirm="P6 comms owner",
    impact="No behaviour change; only the base and the owner move, and every message and status is unchanged.")

asm("ASM-B-ITG-W1-05-E1034-2",
    text="SCR-33 Template approval is reached through gateway-bff on the P6 route; the suite proves the behaviour through the contract and builds or tests no screen (DP-19).",
    why="The legacy story builds SCR-33 behind its flag in Epic 1 while screens.txt lists it first in Epic 2, and the target keeps the screen on gateway-bff.",
    read="RWB-E1-034 sections 13 and 15; Arch v5 slide 20 (gateway-bff); Template and Rules v1 section R5.5 DP-19; RWB-P6-E1034-APP.",
    gap="CG-B-ITG-W1-05-E1034-1",
    applied_in="Story sections 2, 12.2 and 15",
    confidence="Medium",
    confirm="P6 comms owner and the experience lead",
    impact="The contract is the test surface; the screen timing is unchanged and outside this story.")

asm("ASM-B-ITG-W1-05-E1034-3",
    text="The freshness stamp on SCR-33 is read from P1 rwb-source-data through GET /api/recovery/source-data/v1/data-products/freshness (RWB-E1-015); the product whose stamp is shown is selected in the synthetic fixture from the P1 data product set.",
    why="The legacy story depends on RWB-E1-015 for the freshness stamp and the plan gives RWB-P1-E1015-APP as an I dependency, but the sources do not name which product the template catalog shows.",
    read="RWB-E1-034 sections 3 and 13; Arch v5 slide 15 (P1 GET /freshness (business date)); Ownership Map api GET /data-products/freshness owner P1; RWB-P1-E1015-APP.",
    gap="CG-B-ITG-W1-05-E1034-1",
    applied_in="Story sections 3, 7 (AC12), 12.2 and 15",
    confidence="Medium",
    confirm="P1 source-data owner and P6 comms owner",
    impact="A stale reference product shows its date; no template rule changes.")

asm("ASM-B-ITG-W1-05-E1034-4",
    text="A withdrawn template holds generation for that code and language in P6's NoticeDispatchWorkflow until a new version is approved, and no earlier version becomes current again (R-LIT-04, R-LIT-06); the suite asserts the state through the P6 contract and leaves the hold to RWB-P6-E1034-APP and RWB-E1-052.",
    why="Legacy AC8 throws TemplateWithdrawnException from the TemplateCatalog interface and asserts no fallback; the target has no TemplateCatalog interface and generation is a P6 workflow.",
    read="RWB-E1-034 section 7 AC8, section 8 BR6 and section 12; Arch v5 slide 17 (P6 NoticeDispatchWorkflow); Ownership Map table template owner P6; R-LIT-04 and R-LIT-06.",
    gap="CG-B-ITG-W1-05-E1034-1",
    applied_in="Story sections 7 (AC8), 8 (BR6) and 19",
    confidence="Medium",
    confirm="P6 comms owner and Legal counsel",
    impact="No earlier wording is used; the hold and MSG-P6-003 are unchanged.")

# ---------------------------------------------------------------- RWB-E1-037
gap("CG-B-ITG-W1-05-E1037-1",
    title="Matrix load owner, masking read path and the platform library boundary are not named for the target",
    source="04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md (sections 3, 4, 7, 12 and 13); Recovery Workbench Architecture v5 Text Extract v1 slides 14, 20, 41 and 46; _work/msr/plan/ownership.json",
    section="3 Preconditions; 4 Flow; 7 Acceptance criteria; 12 Contract; 13 Solution plan",
    description="The legacy story loads and approves the matrix and the masking rules on P4, applies the ScopeFilter, FieldMasker and AccessCheck interfaces inside one monolith, and reads v_ace_customer and v_ace_contact directly. In the target the matrix, role and masking tables stay with P4 rwb-access and the entity registry and ACE views with P1 rwb-source-data, masking is applied by rwb-source-data at the data read (Arch v5 slide 46), and the guard and masker are the platform library. The Ownership Map names the reference-load path with P3 while the matrix tables are P4's, and the plan's I list for this story names P1, the platform library and P4 and not P3. The sources name neither the owner of the matrix load, nor the P1 read path that returns masked values for a case, nor the boundary of the library.",
    evidence="RWB-E1-037 sections 3, 4, 7, 12 and 13 (POST /api/recovery/v1/admin/reference-loads and /approve on P4, ScopeFilter, FieldMasker, AccessCheck, v_ace_customer and v_ace_contact, no token); Arch v5 slide 14 (P4: POST /authorise, GET /me/permissions, GET /doa-limits, masking policies), slide 20 (permission data cached from rwb-access; every service writes decision records), slide 41 (P1 owns the ACE view contract; P4 owns roles, scope and masking policy), slide 46 note (masking is applied by rwb-source-data); Ownership Map api GET /admin/roles, GET /admin/access-log and GET /me/session owner P4, GET /data-dictionary/fields, GET /data-products/{productCode}/records and GET /data-products/freshness owner P1, POST /admin/reference-loads owner P3, tables permission, role, masking_rule and delegation_limit owner P4, sys_fields owner P1; plan I list RWB-P1-E1069-APP, RWB-PLT-E1037-APP and RWB-P4-E1037-APP.",
    type="Conflict",
    area="Access and masking integration",
    severity="P2",
    legacy_ref="RWB-E1-037",
    owner_role="Solution architect",
    asm="ASM-B-ITG-W1-05-E1037-1",
    proposed="Keep the matrix tables and their load and approval with P4 and the parameters and LOV load with P3, prove the masked read through the P1 data product contract, and let the platform library publish the guard and the annotations while the suite asserts their effect through P4 and P1.")

asm("ASM-B-ITG-W1-05-E1037-1",
    text="The permission, role and masking_rule versions are loaded and approved on P4 rwb-access, the owner of those tables, under its admin reference-load operations; the POST /admin/reference-loads path that the Ownership Map gives to P3 rwb-case serves the parameters and LOVs of E1-042 and E1-043 and is not used for the matrix.",
    why="The legacy story loads and approves on P4, the Ownership Map names permission, role and masking_rule with P4 but names the reference-load path with P3, and the plan gives the matrix work to RWB-P4-E1037-APP.",
    read="RWB-E1-037 sections 3, 4, 12 and 13; Ownership Map tables permission, role and masking_rule owner P4 and api POST /admin/reference-loads owner P3; Template and Rules v1 section R3 default ruling and section R5.5 DP-06 and DP-07.",
    gap="CG-B-ITG-W1-05-E1037-1",
    applied_in="Story sections 2, 3, 12.2 and 13; fragment ops_consumed",
    confidence="Medium",
    confirm="P4 access owner and P3 case owner",
    impact="One load path per table; the letters, the versions, the 756 rows and the messages are unchanged.")

asm("ASM-B-ITG-W1-05-E1037-2",
    text="Masking is applied by P1 rwb-source-data at the data read, from the P4 masking rules, over v_ace_customer and v_ace_contact, and the clear identity number never leaves ACE (D-RCV-35 U1; BR10); the suite reads masked values through GET /api/recovery/source-data/v1/data-products/{productCode}/records.",
    why="The legacy story applies FieldMasker inside the monolith and reads the views directly; Arch v5 slide 46 says masking is applied by rwb-source-data and the plan gives the views and grants to RWB-P1-E1069-APP.",
    read="RWB-E1-037 sections 4, 7 AC2 and AC9, 8 BR6 and 11; Arch v5 slides 41 and 46; D-RCV-35 U1; ADR-010; Ownership Map api GET /data-products/{productCode}/records owner P1.",
    gap="CG-B-ITG-W1-05-E1037-1",
    applied_in="Story sections 2, 7 (AC2, AC9, AC13), 11 and 17",
    confidence="Medium",
    confirm="P1 source-data owner and RW-COMPLY",
    impact="Only masked values reach a caller; no rule and no masking shape changes.")

asm("ASM-B-ITG-W1-05-E1037-3",
    text="The guard and masker library of RWB-PLT-E1037-APP is exercised through the P4 and P1 operations that use it and is never called by the suite; the platform story publishes the guard contract and the field annotations, and the suite asserts their effect.",
    why="The plan gives the platform library an APP story and lists it as an I dependency, and a library has no REST surface that the suite can call.",
    read="RWB-E1-037 section 12 (ScopeFilter, FieldMasker, AccessCheck) and section 13; Arch v5 slide 20 (permission data cached; every service from the template and the shared libraries); RWB-PLT-E1037-APP; Template and Rules v1 section R5.5 DP-08.",
    gap="CG-B-ITG-W1-05-E1037-1",
    applied_in="Story sections 3, 12.8 and 13",
    confidence="Medium",
    confirm="Platform lead and P4 access owner",
    impact="The library is proved through its consumers; no extra call path is invented.")

asm("ASM-B-ITG-W1-05-E1037-4",
    text="Scope is applied by the owning service before the right check, and this story proves the scope outcome through the P4 guard response and the P1 record read, because the plan's I list names P1, the platform library and P4 and not P3 rwb-case; the case-list scope itself is proved with RWB-P3-E1031-APP.",
    why="Legacy AC4 calls GET /cases on P3, P3 is not an integration dependency of this story, and the sources do not name a scope read on P1 or P4 that returns cases.",
    read="RWB-E1-037 sections 4, 7 AC4 and 8 BR4; Arch v5 slide 20 (permission data cached from rwb-access; masking by rwb-source-data); Ownership Map api GET /data-products/{productCode}/records owner P1; the I list of RWB-ITG-E1037-ITG.",
    gap="CG-B-ITG-W1-05-E1037-1",
    applied_in="Story sections 2, 7 (AC4) and 13",
    confidence="Medium",
    confirm="P4 access owner, P1 source-data owner and the integration lead",
    impact="The scope rule is still proved end to end; the case-list surface is proved in RWB-ITG-E1031-ITG.")

gd = Path("_work/msr/gaps/B-ITG-W1-05.jsonl")
ga = Path("_work/msr/assumptions/B-ITG-W1-05.jsonl")
gd.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in gaps) + "\n", encoding="utf-8")
ga.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in assumptions) + "\n", encoding="utf-8")
print("gaps", len(gaps), "assumptions", len(assumptions))
print([r["id"] for r in gaps])
print([r["id"] for r in assumptions])
