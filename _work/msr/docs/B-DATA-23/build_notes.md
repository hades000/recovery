# Build note B-DATA-23 — Recovery Workbench Reporting and Analytics Data Model v4

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What the source says

`06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx` has three sheets and no
version number, no release date and no owner anywhere.

- `Facts` (A1:F13): note A2 reads "Star schema in the data lake for Power BI. ACE source rows are
  read through recovery.v_ace_* views; Workbench rows come from the recovery tables. No source
  system is loaded directly." Nine fact tables follow, each with grain, dimensions, measures,
  source entities and refresh.
- `Dimensions` (A1:B12): eight dimensions and what each holds.
- `Measures` (A1:C14): ten management measures, the formula of each and the fact table it reads.

## What the realignment changed

Ten v3 cells change and no other v3 cell moves.

| Cell | v3 | v4 | Why |
|---|---|---|---|
| Facts!A2 | Star schema in the data lake for Power BI; ACE read through recovery.v_ace_* | Star schema in rwb_reporting (P9) for the dashboard and the reports, built from the events; ACE rows through the P1 contract and snapshot(page); no lake | CG-B-DATA-23-1, CG-B-DATA-23-2 |
| Facts!F5, F7, F8, F9, F11 | Read through v_ace_*; nightly | Event-fed projections; publish 01:30 (JOB-15); ACE rows through the P1 contract | CG-B-DATA-23-3 |
| Facts!F6, F10, F12 | Nightly from the Workbench | Event-fed from the named events; publish 01:30 (JOB-15) | CG-B-DATA-23-3 |
| Facts!F13 | Read through v_ace_bucket_log; monthly | Monthly from the P1 contract (P1 reads v_ace_bucket_log); publish 01:30 | CG-B-DATA-23-2, CG-B-DATA-23-3 |

Three columns are appended to `Facts` (G Owner, H Values from, I Pattern) on all nine rows, two to
`Dimensions` (C Owner, D Values from) on all eight rows and two to `Measures` (D Owner, E Served
through) on all ten rows. Every owner value comes from `Recovery Workbench Microservice Ownership
Map v1.xlsx`, sheet `Services` for the service code and sheet `Tables` for the table owner: P9
rwb-reporting owns measure_definition, measure_snapshot and measure_publish; P1 the ACE rows through
the view contract; P3 the case, queue, assignment and timer rows; P7 the decision ledger and the rule
registry; P8 proceeds; S2 treatment; S4 legal action and hearing; S5 asset sale and listing; S6 the
lots; S7 write-off; S9 partner instructions (ASM-B-DATA-23-4).

Two new sheets are added.

- `Read model` — how each of the nine facts is built from its topic, the events that feed it, the
  producer, the late-arrival rule and the rebuild (CG-B-DATA-23-3, CG-B-DATA-23-6). Below it the
  three P9 control tables with the publish gate (CG-B-DATA-23-5) and the five items the realignment
  retired or moved: the lake landing place, INT-19 and INT-20, the direct ACE read path, the nightly
  Workbench load and the JOB-13 lake copy (CG-B-DATA-23-1, CG-B-DATA-23-2).
- `Read me` — first sheet. Row 1 and row 2 are the two header lines of Template and Rules section
  R8.1; row 9 is the change-log row
  `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.

## What did not change

The nine fact tables keep their names, grains, dimensions, measures and source entities. The eight
dimensions keep their names and what they hold. The ten measure definitions keep their names,
formulas and the fact table each reads. Every identifier is copied character for character, including
fact_case_daily, fact_decision, fact_treatment, fact_legal, fact_asset, fact_lot, fact_recovery,
fact_partner, fact_flow, dim_date, dim_product, dim_route, dim_stage, dim_org, dim_partner, dim_rule,
dim_decision, LOV-ROUTE and LOV-STAGE. The source carries no date, so no release date is marked
"(tentative)" and none is changed.

## Open points and where each one lands

| Row | Point | Sheet it touches |
|---|---|---|
| CG-B-DATA-23-1 / ASM-B-DATA-23-1 | Lake premise replaced by the rwb_reporting read model | Facts!A2, Read model |
| CG-B-DATA-23-2 / ASM-B-DATA-23-2 | ACE views read only by rwb-source-data | Facts!F5 to F13, Dimensions!D5 to D12 |
| CG-B-DATA-23-3 / ASM-B-DATA-23-3 | Refresh wording and the 01:30 publish | Facts!F5 to F13, Read model |
| CG-B-DATA-23-4 / ASM-B-DATA-23-4 | No owner or schema in the source | Facts!G to I, Dimensions!C to D, Measures!D to E |
| CG-B-DATA-23-5 / ASM-B-DATA-23-5 | Control tables and queue measures absent | Read model, Read-model controls |
| CG-B-DATA-23-6 / ASM-B-DATA-23-6 | No late-arrival, freeze or replay rule | Read model |
| CG-B-DATA-23-7 / ASM-B-DATA-23-7 | dim_org owner against the no-personal-data rule | Dimensions!D9, Read model |
| CG-B-DATA-23-8 / ASM-B-DATA-23-8 | Power BI wording in LDM v8 and FSD P3 | Measures!E4 to E14, Read model |

## Evidence used

- `Recovery Workbench Architecture v5 Text Extract v1.md`: line 37 and line 67 (no lake, INT-19/20),
  lines 664 to 665 (slide 37), lines 1096 to 1119 (slide 41 P9 contract), line 2296 and lines 2327 to
  2330 (JOB-15 at 01:30), lines 2899 to 2968 (service catalogue and event catalogue), lines 2988 to
  2990 (slide 44 job map).
- `Recovery Workbench Temporal and Drools Design Text Extract v1.md`: no reporting workflow; the P9
  work is the Schedule and the buildRegulatoryExtract activity named on slide 41.
- `_work/msr/plan/ownership.json` and `Recovery Workbench Microservice Ownership Map v1.xlsx`: P9
  owns the three measure tables; the input tables carry P1, P3, P7, P8, S2, S4, S5, S6, S7 and S9.
- `Recovery Workbench Logical Data Model and Data Dictionary v8.md`: measure_definition,
  measure_snapshot, measure_publish and queue_measure with fields DF-RPT-020 to DF-RPT-058.
- `_work/msr/plan/split_plan.json`: the five P9 legacy keys are RWB-E1-013 (Baseline measures),
  RWB-E2-009 (Steering dashboard v1 data set), RWB-E6-037, RWB-E8-001 and RWB-E8-002; RWB-E1-014 is
  the retired decision-log lake copy.
- `_work/msr/plan/ids.json`: ADR-013 to ADR-023 and DL44 to DL49; ADR-018 is the one cited here.

## Verification

`verify_v4.py` reads v3 and v4 cell by cell. It reports 10 changed cells, all declared, no row or
column lost, no sheet renamed, the header and change-log row present, the three new sheet blocks in
place, and every owner cell equal to the Ownership Map. Result: PASS, 0 problems. Output in
`verify_v4.json`.

## Counts

- Facts: 9 tables; 3 appended columns; 27 appended values.
- Dimensions: 8 tables; 2 appended columns; 16 appended values.
- Measures: 10 measures; 2 appended columns; 20 appended values.
- Read model: 9 build rows, 3 control rows, 5 retired or moved rows.
- Changed v3 cells: 10 of 117 populated cells across the three v3 sheets (Facts 62, Dimensions 20,
  Measures 35); all 10 changed cells are on Facts.
- Candidate gap rows: 8, CG-B-DATA-23-1 to CG-B-DATA-23-8.
- Candidate assumption rows: 8, ASM-B-DATA-23-1 to ASM-B-DATA-23-8.
