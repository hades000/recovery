# Build note B-DATA-25 — Recovery Workbench Data Quality and Reconciliation Rules v4

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What the source says

`06 Data/Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx` has three sheets, no
version number, no release date and no owner column anywhere.

- `Load checks` (A1:J102): a note, then 98 retired load checks DQ-001 to DQ-098 with interface,
  source, data product, check, what it tests, tolerance, failure action, owner and status. Every
  status reads "Moved to ACE ingestion (RWB-ACE-001)".
- `Reconciliations` (A1:G13): a note, then nine reconciliations REC-01 to REC-09 comparing ACE,
  read through a `v_ace_*` view, with the case list or the Workbench record it feeds.
- `Quality measures` (A1:C10): six measures (Completeness, Validity, Timeliness, Accuracy,
  Uniqueness, Referential completeness) with a meaning and a target.

## What the realignment changed

Three source cells change and no other source cell moves.

| Cell | v3 | v4 | Why |
|---|---|---|---|
| Reconciliations!B12 | Decision log copy | Local decision record of each of the 19 services (rwb.decision-record.v1, via the rwb-decision contract) | CG-B-DATA-25-3 |
| Reconciliations!C12 | Live decision log | Central decision ledger, rwb-decision (decision_log_entry), with its hash chain | CG-B-DATA-25-3 |
| Quality measures!B7 | The ACE batch for the business date is complete when the Workbench reads it | The ACE batch for the business date is complete when rwb-source-data reads it and publishes AceDataReady | CG-B-DATA-25-9 |

Two columns are appended to `Reconciliations` (H Owner, I Per-service reconciliation) on all nine
rows, one to `Quality measures` (D Owner service) on all six rows. Two notes sit below the
`Reconciliations` table, two below the `Load checks` table and one below the `Quality measures`
table. `Load checks` keeps all 98 rows cell for cell.

One new sheet is added.

- `Per-service reconciliation` — first block: one row per service (19 rows, columns Service,
  Service name, Schema, Owns in its schema, Reconciles its own rows and against what, Key,
  Tolerance, When, Break and result route, Pattern, Basis). Second block: the nine reconciliations
  split by the service that holds each side. Third block: the REC numbering, because the source
  numbers the notice-barcode check REC-05 and the business-key check REC-09 while RWB-E1-011 and
  every realigned slice number them the other way round.
- `Read me` — first sheet. Rows 1 and 2 are the two header lines of Template and Rules R8.1; row 9
  is the change-log row
  `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.

Every owner value comes from `Recovery Workbench Microservice Ownership Map v1.xlsx`: sheet
`Services` for the service name and schema of each of the 19 rows, sheet `Tables` for the tables of
each service (93 tables; P1 18, P10 8, P2 3, P3 15, P4 5, P5 12, P6 3, P7 6, P8 1, P9 3, PLT 6,
S2 1, S3 1, S4 2, S5 2, S6 2, S7 1, S8 1, S9 3, and none for S1).

## What did not change

The 98 load checks keep every value, including DQ-001 to DQ-098, INT-01 to INT-16 and DP01 to DP13.
REC-01 to REC-09 keep their IDs, source side, Workbench side (except REC-08), compared-on,
tolerance, cadence and break route (except REC-08). The six measures keep their names, meanings
(except Timeliness) and targets. Every identifier is copied character for character, including
`recovery.v_ace_account`, `v_ace_plan`, `v_ace_payment`, `v_ace_write_off`, `v_ace_npa_asset`,
`v_ace_pod`, `v_ace_efs_action_code` and `v_ace_product`. The source carries no version number and
no release date, so no date is changed and no release date is marked "(tentative)".

## Open points and where each one lands

| Row | Point | Where it lands |
|---|---|---|
| CG-B-DATA-25-1 / ASM-B-DATA-25-1 | One run against a Workbench side held in seven schemas | Reconciliations H5 to H13; Per-service reconciliation, all 19 rows |
| CG-B-DATA-25-2 / ASM-B-DATA-25-2 | No owner on any reconciliation or measure | Reconciliations H and I; Quality measures D |
| CG-B-DATA-25-3 / ASM-B-DATA-25-3 | REC-08 compares a retired decision-log copy | Reconciliations B12, C12, H12, I12; row P7 |
| CG-B-DATA-25-4 / ASM-B-DATA-25-4 | No per-service rule, cadence or result route | Per-service reconciliation, rows 5 to 23 and the nine-reconciliation block |
| CG-B-DATA-25-5 / ASM-B-DATA-25-5 | No tolerance for ten services | Per-service reconciliation, tolerance cells of P2, P4, P5, P10, S1, S3, S4, S6, S8, S9 |
| CG-B-DATA-25-6 / ASM-B-DATA-25-6 | REC-05 and REC-09 transposed against RWB-E1-011 | Per-service reconciliation, numbering block; rows P6 and P1 |
| CG-B-DATA-25-7 / ASM-B-DATA-25-7 | No S1 table in the Ownership Map | Per-service reconciliation, row S1 |
| CG-B-DATA-25-8 / ASM-B-DATA-25-8 | No S2 or P8 slice for REC-03 and REC-04 | Per-service reconciliation, rows S2 and P8; REC-03 and REC-04 in the split block |
| CG-B-DATA-25-9 / ASM-B-DATA-25-9 | Timeliness reads a Workbench read only P1 makes | Quality measures!B7, D7, note A12 |

## Evidence used

- `Recovery Workbench Architecture v5 Text Extract v1.md`: lines 1077 to 1081 and 1113 to 1115
  (P1 contract: ACE view contract, freshness, reconciliation; 30 views), lines 2341 to 2342
  (Airflow never reads or writes an `rwb_*` schema), line 2294 (AceDataReady starts the morning
  run), lines 2880 to 2898 (service catalogue), lines 2909 to 2963 (event catalogue), lines 2978
  to 2995 (job map: JOB-02, JOB-03, JOB-04, JOB-07, JOB-08, JOB-10, JOB-12, JOB-13, JOB-14,
  JOB-15), line 1865 (RouteDecisionWorkflow on rwb-valuation).
- `Recovery Workbench Temporal and Drools Design Text Extract v1.md`: slide 13 (the stage child
  workflows, including RouteDecisionWorkflow); it names no reconciliation workflow, which is
  consistent with JOB-04 being an event-started workflow in rwb-source-data.
- `Recovery Workbench Microservice Ownership Map v1.xlsx`: sheets `Services` (19 rows) and
  `Tables` (93 rows); `reconciliation_result` under P1, `decision_log_entry` under P7, `notice`
  under P6, `treatment` under S2, `proceeds` under P8, `write_off` under S7, `asset_sale` under S5;
  no S1 row.
- `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 011 Reconciliation
  and data quality report v1.md`: line 47 (REC-05 is the business-key check) and line 155 (BR5).
- `04 User stories/.../RWB-ITG-W1 Wave 1 integration/RWB ITG E1011 ITG ... v1.md` (section 4 step 7
  and AC12: REC-03 and REC-04 NOT_RUN until S2 and P8 land; section 19: REC-06 to REC-09), the P6
  and S5 E1011 slices (the REC-05 and REC-09 collision), and the P1 E1011 slice (P1 owns REC-01,
  REC-02 and the business-key check over its own tables only).
- `_work/msr/plan/split_plan.json`: `stats` (1034 slices, 358 legacy keys) and `legacy` for
  RWB-E1-011 (slices P1, P3, S5, P6, P1 OPS, P1 CON and ITG; no S2 and no P8), RWB-E1-011
  (split, primary P1, wave 1) and the retired RWB-E1-014.
- `_work/msr/plan/ids.json`: the realignment decision is D-RCV-60; ADR-014 and ADR-018 are cited
  here, and no new ADR or DL ID is allocated by this WP.

## Verification

`verify_v4.py` compares the three source sheets with v4 cell by cell and checks every owner. Result:
PASS, 0 problems, in `verify_v4.json`.

- 3 changed source cells, all declared (Reconciliations!B12, C12; Quality measures!B7); no other
  difference and no row or column lost.
- Header lines 1 and 2 and the change-log row present on `Read me`, which is the first sheet; sheet
  order Read me, Load checks, Reconciliations, Per-service reconciliation, Quality measures.
- 19 per-service rows, one per service of the map; each name and schema equal to sheet `Services`;
  each table listed equal to the tables sheet `Tables` gives that owner; S1 carries the R9
  placeholder.
- Every placeholder carries a `CG-B-DATA-25-n; ASM-B-DATA-25-n` citation, and every cited candidate
  row has a row in its register file (18 IDs cited, 18 rows present).

## Counts

- Load checks: 98 rows, 992 populated source cells, 0 changed; 2 notes added below the table.
- Reconciliations: 9 rows; 2 appended columns (2 headers, 18 values); 2 changed cells (B12, C12);
  2 notes.
- Quality measures: 6 rows; 1 appended column (1 header, 6 values); 1 changed cell (B7); 1 note.
- Per-service reconciliation: 19 service rows, 9 split rows, 6 numbering rows, 1 closing note.
- Changed source cells: 3 of 1087 populated source cells across the three sheets.
- Candidate gap rows: 9, CG-B-DATA-25-1 to CG-B-DATA-25-9.
- Candidate assumption rows: 9, ASM-B-DATA-25-1 to ASM-B-DATA-25-9.
