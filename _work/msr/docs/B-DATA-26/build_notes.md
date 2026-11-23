# Build note B-DATA-26 — Recovery Workbench Volume and Scale Forecast v4

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What the source says

`06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx` has eight sheets, no version number, no release
date, no service name and no owner anywhere.

- `Inputs` (A1:G38): 34 drivers, I01 to I34, each with value, unit, kind (Fact or Assumption), source and the
  effect if it moves.
- `Monthly` (A1:I18): 14 months from Nov 2026, all formulas off `Inputs`.
- `Five years` (A1:J9): 2027 to 2031, all formulas off `Inputs` and `ACE growth`.
- `Users and load` (A1:E8): three user groups, concurrent users and requests a second.
- `Read path` (A1:D16): the read path, then three Workbench facts (inbound load window, scheduled jobs, source
  freshness).
- `ACE growth` (A1:E23): the 14 tables and 12 columns that RWB-ACE-001 adds, rows and size a year, five-year
  totals and the share of a 2 TB database.
- `Route activity` (A1:C9): five route activities a month and a year.
- `Key` (A1:C13): kind and term definitions.

## What the realignment changed

Five v3 cells change and no other v3 cell moves.

| Cell | v3 | v4 | Why |
|---|---|---|---|
| Read path!A2 | The Workbench reads ACE through recovery.v_ace_* views | rwb-source-data (P1) reads the 30 views; every other service asks P1 | CG-B-DATA-26-2 |
| Read path!C15 | Outbound queue dispatch, lake refresh and case list reconciliation | Case creation and allocation (JOB-02, JOB-03), reconciliation (JOB-04), WIN notice file (JOB-10) | CG-B-DATA-26-3, CG-B-DATA-26-7 |
| Read path!C16 | read through v_ace_batch_status | read by rwb-source-data through v_ace_batch_status; GET /freshness; AceDataReady | CG-B-DATA-26-2 |
| Inputs!G7 | read through v_ace_account | read by rwb-source-data through v_ace_account | CG-B-DATA-26-2 |
| Key!C10 | a SELECT by a screen or by the lake refresh | a SELECT by rwb-source-data on behalf of a screen or a workflow | CG-B-DATA-26-2 |

Two sheets are added.

- `Service volumes` — 19 rows, one per owning service. `Volume, 2027` is a formula on the existing sheets
  (`Inputs`, `Five years`, `Users and load`, `Route activity`), so the forecast totals do not move and no driver
  is shared. `Basis` names the cell; `Kafka topic`, `Task queue` and the wave come from the Ownership Map v1
  sheet `Services`; `Consumers of its events` is the event catalogue on slides 42 and 43. Below it, eight
  cross-check rows restate the four headline volumes, the peak request rate, the event rate, the queue count and
  the topic count.
- `Topics and queues` — the 19 service topics plus the shared `rwb.decision-record.v1` (partitions 12,
  replication 3, retention 7 days, key caseId, consumer groups, retry 1 min / 10 min / 1 h, `.dlt`), then the 19
  task queues with workflows, activities and Schedules, then 11 platform settings (namespace `rwb-recovery`,
  shared cluster, envelope, outbox and inbox, capacity).
- `Read me` is a new first sheet. Rows 1 and 2 are the header lines of Template and Rules §R8.1, row 9 is the
  change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
  Flash`.

## What did not change

The 34 drivers and every value, unit, kind, source and effect; the 14 monthly formulas; the five annual columns;
the three user groups and their concurrency; the 14 ACE tables, 12 columns, rows and GB a year, the five-year
rows and size and the share of the 2 TB database; the five route activities; the key definitions. Every
identifier is copied character for character, including I01 to I34, JOB-02 to JOB-22, the 14 ACE table names and
the 30 view names. The source carries no release date, so no date is marked "(tentative)": the dates it
does carry (30 June 2026, 6 July 2026, the July 2025 to June 2026 averages) are bank data dates and are copied
unchanged.

The document properties of the copy carried a person's name in `creator`. It is replaced with "Recovery Workbench
programme" and `lastModifiedBy` with the tool line, so no person name survives in the workbook (root rule 4).

## Per-service volumes and where each one comes from

| Code | Service | Volume, 2027 | Source cell |
|---|---|---|---|
| P1 | rwb-source-data | accounts listed a day | Inputs!C5+C6+C8 |
| P2 | rwb-integration | registered letters a month | Inputs!C26 |
| P3 | rwb-case | cases a month | Five years!C5/12 |
| P4 | rwb-access | requests a second at peak | Users and load!E8 |
| P5 | rwb-document | documents a month | Five years!E5/12 |
| P6 | rwb-comms | registered letters a month | Inputs!C26 |
| P7 | rwb-decision | decision-log entries a month | Five years!H5/12 |
| P8 | rwb-payment | payments a month | placeholder (CG-B-DATA-26-5) |
| P9 | rwb-reporting | measure publish a day | 1, JOB-15 |
| P10 | rwb-agent | agent runs a month | (Five years!C5+E5)/12 |
| S1 | rwb-valuation | valuations a month | Five years!C5*0.5/12 |
| S2 | rwb-treatment | accounts under restructure | Inputs!C30 |
| S3 | rwb-guarantee | claims a month | placeholder (CG-B-DATA-26-5) |
| S4 | rwb-litigation | lawsuits a month | Inputs!C24 |
| S5 | rwb-asset | assets a month | Inputs!C25 |
| S6 | rwb-debtsale | accounts a month | Route activity!B9 |
| S7 | rwb-writeoff | write-offs a month | Five years!C5*0.3/12 |
| S8 | rwb-deviation | screenings a month | Five years!C5/12 |
| S9 | rwb-partner | partner users | Inputs!C33 |

## Open points and where each one lands

| Row | Point | Sheet it touches |
|---|---|---|
| CG-B-DATA-26-1 / ASM-B-DATA-26-1 | Per-service volumes are new | Service volumes |
| CG-B-DATA-26-2 / ASM-B-DATA-26-2 | One service reads the ACE views | Read path!A2, C16; Inputs!G7; Key!C10 |
| CG-B-DATA-26-3 / ASM-B-DATA-26-3 | Lake refresh retired, jobs re-owned | Read path!C15 |
| CG-B-DATA-26-4 / ASM-B-DATA-26-4 | No messaging content in the source | Topics and queues |
| CG-B-DATA-26-5 / ASM-B-DATA-26-5 | No demand figure for five drivers | Service volumes (P8, S3, and the notes on P9, S6, S8, S9) |
| CG-B-DATA-26-6 / ASM-B-DATA-26-6 | 3,110 cases a month against the source formula | Service volumes cross-checks |
| CG-B-DATA-26-7 / ASM-B-DATA-26-7 | 3 jobs against the 21-job map | Read path!C15 |

## Evidence used

- `Recovery Workbench Architecture v5 Text Extract v1.md`: line 45 and 69 (own schema, topic and queue per
  service), lines 245 to 246 (topic and queue naming), line 703 (12 partitions, RF 3, 7 days, caseId, retry,
  .dlt), line 707 (only rwb-source-data reads the 30 views), lines 1113 to 1115 (P1 contract), lines 2296 and
  2978 to 3002 (Temporal Schedules and the job map), lines 2433 and 3127 to 3179 (volumes), lines 2880 to 2898
  (slide 41 service catalogue), lines 2911 to 2963 (event catalogue), line 1544 (tens of thousands of events a
  day).
- `Recovery Workbench Temporal and Drools Design Text Extract v1.md`: lines 444 to 483 (one worker and one queue
  per service, 19 queues) and line 520 (namespace rwb-recovery, KEDA on backlog).
- `_work/msr/plan/ownership.json` and `Recovery Workbench Microservice Ownership Map v1.xlsx` (sheet `Services`):
  code, service, wave, schema, REST base, topic and queue for all 19 services.
- `_work/msr/plan/split_plan.json`: NF-03, NF-08 (platform technical enablers) and RWB-TE-009 (performance test
  harness) are the legacy keys this document feeds.
- `_work/msr/plan/ids.json`: ADR-013 to ADR-023 and DL44 to DL49; ADR-013 (19 services), ADR-014 (schema and login
  per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (Temporal, Schedules replace Quartz)
  and ADR-018 (no data lake) are the ones cited.

## Verification

`verify_v4.py` reads v3 and v4 cell by cell: 803 cells on the eight v3 sheets, 5 changed (all declared), 0
restyled, no sheet renamed or lost, the sheet order kept, the two header lines and the change-log row present,
the 19 service rows and the 20 topic and 19 queue rows equal to the Ownership Map, the placeholder only on P8
and S3, and the creator name scrubbed. Result: PASS, 0 problems. Output in `verify_v4.json`.

## Counts

- Service volumes: 19 service rows, 8 cross-check rows, 10 columns.
- Topics and queues: 20 topic rows, 19 queue rows, 11 platform rows.
- Changed v3 cells: 5 of 803 compared cells.
- Candidate gap rows: 7, CG-B-DATA-26-1 to CG-B-DATA-26-7 (3 Conflict, 2 Missing, 1 Outdated, 1 Ambiguous).
- Candidate assumption rows: 7, ASM-B-DATA-26-1 to ASM-B-DATA-26-7.
