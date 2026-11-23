# Edit log B-DATA-26 — Recovery Workbench Volume and Scale Forecast next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx` was read once, sheet by sheet and
  cell by cell, through the dump in the scratch area, and never edited. It was copied to v4 with
  `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Volume and Scale
  Forecast v4.xlsx`.
- `Service volumes` is a new sheet: 19 rows, one per owning service (P1 to P10, S1 to S9). Each row gives the
  volume driver, the 2027 volume as a formula on the existing sheets, the unit, the basis cell, the Kafka topic,
  the Temporal task queue and the consumers of its events. No driver is shared, so Inputs, Monthly, Five years and
  Route activity keep every value and every total (GAP-0277; ASM-0367). The topic, the queue and the
  wave of every row are the Ownership Map v1 sheet `Services`, row by row; the consumers are the event catalogue
  on Arch v5 slides 42 and 43.
- Below that table, eight cross-check rows restate the four headline volumes, the peak request rate, the event
  rate, the queue count and the topic count, and name the Arch v5 slide 48 figure beside each computed one
  (GAP-0282; ASM-0372).
- `Topics and queues` is a new sheet: the 19 service topics plus the shared `rwb.decision-record.v1`, each with
  12 partitions, replication factor 3, seven-day retention, key caseId, its consumer groups, the retry ladder
  (1 min, 10 min, 1 h) and its `.dlt` topic; then the 19 task queues with the workflows, activities, Schedules and
  a scale note; then 11 platform settings (namespace `rwb-recovery`, shared cluster, CloudEvents 1.0 binary,
  outbox and inbox, capacity, shared topic) (GAP-0280; ASM-0370).
- Five v3 cells change, wording only, no figure: `Read path!A2` and `C16`, `Inputs!G7` and `Key!C10` name
  rwb-source-data as the one reader of the 30 `recovery.v_ace_*` views (GAP-0278; ASM-0368);
  `Read path!C15` replaces the retired lake refresh with three jobs that exist in the target (GAP-0279,
  GAP-0283; ASM-0369, ASM-0373). `Read path!B15` stays 3, as the number of Workbench-side
  jobs.
- Two drivers have no figure in the source and carry the §R9 placeholder instead of an invented number: payment
  matching (P8) and guarantee claims (S3). Four basis notes state the cadence the architecture does give
  (GAP-0281; ASM-0371).
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the
  change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
  Flash`. It then lists what changed, what did not, the sheet order, the open register rows and the counts.
- Sheet order is `Read me`, `Inputs`, `Monthly`, `Five years`, `Users and load`, `Read path`, `Service volumes`,
  `Topics and queues`, `ACE growth`, `Route activity`, `Key`: the eight source sheets keep their relative order and
  the two new sheets sit after the read path they qualify.
- Nothing else moved. `verify_v4.py` compares the eight v3 sheets with v4 cell by cell, value, number format and
  style: 803 cells compared, 5 changed (all declared), 0 restyled, no row or column lost, no sheet renamed, the
  header and change-log rows present, every topic, queue, wave and service equal to the Ownership Map.
- The source carries no release date, so no date is marked "(tentative)" and no date is changed. The dates it does
  carry (30 June 2026, 6 July 2026, the July 2025 to June 2026 averages, the month labels Nov 2026 to Dec 2027) are
  bank data dates and are copied unchanged. No date is raised as a gap.
- The document properties of the copy carried a person's name in `creator`. It is replaced with "Recovery Workbench
  programme" and `lastModifiedBy` with the tool line, so no person name survives (root rule 4). No content cell was
  touched for this.
- All figures, IDs, units and labels of the source are copied character for character: I01 to I34, JOB-02 to
  JOB-22, the 14 ACE table names, the 30 view names and every month and year label.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was
  made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx`
- `_work/msr/gaps/B-DATA-26.jsonl`
- `_work/msr/assumptions/B-DATA-26.jsonl`
- `_work/msr/editlog/B-DATA-26.md`
- `_work/msr/docs/B-DATA-26/build_notes.md`
- `_work/msr/docs/B-DATA-26/gen_rows.py`
- `_work/msr/docs/B-DATA-26/gen_registers.py`
- `_work/msr/docs/B-DATA-26/dump_v3.py`
- `_work/msr/docs/B-DATA-26/v3_dump.json`
- `_work/msr/docs/B-DATA-26/rows_service_volumes.json`
- `_work/msr/docs/B-DATA-26/rows_topics_queues.json`
- `_work/msr/docs/B-DATA-26/rows_read_me.json`
- `_work/msr/docs/B-DATA-26/build_v4.py`
- `_work/msr/docs/B-DATA-26/verify_v4.py`
- `_work/msr/docs/B-DATA-26/verify_v4.json`

## Rows

- Candidate gap rows: 7, `GAP-0277` to `GAP-0283`, in `_work/msr/gaps/B-DATA-26.jsonl`, with every
  key of Template and Rules §R9. Types: 3 Conflict (GAP-0277, -2, -6), 2 Missing (-4, -5), 1 Outdated (-3)
  and 1 Ambiguous (-7). Severity: 4 at P2 (-1, -2, -4, -5) and 3 at P3 (-3, -6, -7). `needed_by_wave` is 1 on six
  rows and 2 on GAP-0281. The legacy keys they reference are NF-03, NF-08 and RWB-TE-009.
- Candidate assumption rows: 7, `ASM-0367` to `ASM-0373`, in
  `_work/msr/assumptions/B-DATA-26.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on
  four (ASM-0367 to -4) and Medium on three (-5 to -7).
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Service volumes: 19 service rows (10 platform, 9 route) over 10 columns; 8 cross-check rows.
- Topics and queues: 20 topic rows (19 service topics plus the shared decision-record topic), 19 queue rows and 11
  platform rows.
- Changed v3 cells: 5 of 803 compared, all on the read path, Inputs and Key; 0 restyled cells.
- New sheets: 3 (`Read me`, `Service volumes`, `Topics and queues`); v3 sheets kept: 8.
- Gaps: 7 rows; assumptions: 7 rows.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-26 --quick`: C02, C03, C05, C12, C13 and
  C18 PASS, 0 findings.
- `verify_v4.py`: 803 cells compared, 5 changed and all declared, 0 problems, every topic, queue and wave equal to
  the Ownership Map, the placeholder only on P8 and S3, the creator name scrubbed. Result PASS,
  `verify_v4.json`.
- C17 by hand over the same write set: `GAP-0277` to `-7` and `ASM-0367` to `-7` are cited in the
  workbook, in `build_notes.md` and in this log, each has a row in its register file, and no other candidate id is
  cited.

## Failures

None.
