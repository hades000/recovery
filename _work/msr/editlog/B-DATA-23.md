# Edit log B-DATA-23 — Recovery Workbench Reporting and Analytics Data Model next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source was converted once to text under the run scratch area with `compat/convert_sources.py`, read
  sheet by sheet, and never edited. It was copied to v4 with `compat/office_write.py copy`, and only the
  copy was changed: `06 Data/Recovery Workbench Reporting and Analytics Data Model v4.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9
  is the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
  DeepSeek v4.1 Flash`. Rows 11 to 17 list what changed, rows 19 to 20 what did not, rows 22 to 23 the
  counts and rows 25 to 26 the open register rows.
- `Facts`: ten v3 cells change and no other v3 cell moves. Note A2 no longer places the star schema in a
  data lake; it is the read model in `rwb_reporting` (P9) built from the business events, with ACE rows
  through the `rwb-source-data` contract on the `snapshot(page)` activity and never a direct
  `recovery.v_ace_*` read (GAP-0251, GAP-0252; ASM-0341, ASM-0342). The nine
  refresh cells F5 to F13 no longer read `v_ace_*` from the reporting layer and no longer say "Nightly from
  the Workbench": each reads event-fed projections or a named event, with the 01:30 publish (JOB-15) and,
  for the five ACE-fed facts, the P1 contract (GAP-0253; ASM-0343).
- `Facts`: three columns are appended at the end — `Owner (D-RCV-60)` gives `P9 rwb-reporting` on all nine
  rows, `Values from (D-RCV-60)` names the owning service and table of each input, `Pattern (D-RCV-60)`
  cites DP-09, DP-05 and DP-17. Columns A to F keep their letters, positions and values except A2 and
  F5 to F13.
- `Dimensions`: two columns are appended — `Owner (D-RCV-60)` gives `P9 rwb-reporting` on all eight rows and
  `Values from (D-RCV-60)` gives P1 for the two ACE-fed dimensions, P3 for route, stage and org, P7 for rule
  and decision and S9 for partner, row by row from the Ownership Map sheet `Tables`. Columns A and B are
  unchanged, cell for cell.
- `Measures`: two columns are appended — `Owner (D-RCV-60)` gives `P9 rwb-reporting` on all ten measures and
  `Served through (D-RCV-60)` gives `GET /dashboards/{id}` and `GET /reports/{id}` behind gateway-bff, which
  is what replaces the lake and Power BI feed (GAP-0258; ASM-0348). Columns A to C are
  unchanged.
- `Read model` is a new last sheet. It maps each of the nine fact tables to the topic it is built from, the
  events, the producer, the late-arrival rule and the rebuild without a lake (GAP-0253,
  GAP-0256; ASM-0343, ASM-0346). Below it, `Read-model controls` names
  `measure_definition`, `measure_snapshot` and `measure_publish` under P9 with the reconcile-to-case-list gate
  (GAP-0255; ASM-0345), and `Retired or moved in v4` records the five items the realignment
  changed: the lake landing place, INT-19 and INT-20, the direct ACE read path, the nightly Workbench load
  and the JOB-13 lake copy.
- Nothing else moved. `verify_v4.py` compares the three v3 sheets with v4 cell by cell: 10 changed cells in
  total (`Facts!A2` and `Facts!F5` to `F13`), no other difference, no row or column lost, no v3 sheet
  renamed, the header and change-log row present, the new sheet blocks in place, and every owner cell equal
  to the Ownership Map.
- The source holds no version number, no release date and no named person, so no release date is marked
  "(tentative)" and no date is changed. All nine fact names, eight dimension names, ten measure names, the
  LOV-ROUTE and LOV-STAGE codes and every grain, dimension, measure and source entity are copied character
  for character.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web
  call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Reporting and Analytics Data Model v4.xlsx`
- `_work/msr/gaps/B-DATA-23.jsonl`
- `_work/msr/assumptions/B-DATA-23.jsonl`
- `_work/msr/editlog/B-DATA-23.md`
- `_work/msr/docs/B-DATA-23/build_notes.md`
- `_work/msr/docs/B-DATA-23/v3_dump.json`
- `_work/msr/docs/B-DATA-23/verify_v4.json`

Scratch scripts in `_work/msr/docs/B-DATA-23/`: `dump_v3.py`, `build_v4.py`, `verify_v4.py`.

## Rows

- Candidate gap rows: 8, `GAP-0251` to `GAP-0258`, in `_work/msr/gaps/B-DATA-23.jsonl`, with
  every key of Template and Rules §R9. Types: 4 Conflict, 3 Missing and 1 Outdated. Severity: 4 at P2
  (GAP-0251, -2, -5, -7) and 4 at P3 (-3, -4, -6, -8). All carry `needed_by_wave` 1; the legacy keys
  they reference are RWB-E1-013, RWB-E2-009 and the retired RWB-E1-014.
- Candidate assumption rows: 8, `ASM-0341` to `ASM-0348`, in
  `_work/msr/assumptions/B-DATA-23.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence
  High on 5 and Medium on 3.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9
  require.

## Counts

- Facts: 9 fact tables; 3 appended columns and 27 appended values; 10 changed cells (A2 and F5 to F13).
- Dimensions: 8 dimensions; 2 appended columns and 16 appended values.
- Measures: 10 measures; 2 appended columns and 20 appended values.
- Read model: 9 build rows, 3 control rows and 5 retired or moved rows.
- Cells: 10 changed v3 cells out of 117 populated v3 cells (Facts 62, Dimensions 20, Measures 35); 70
  appended cells over the three sheets.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-23 --quick`: C02, C03, C05, C12,
  C13 and C18 PASS, 0 findings, both before and after this log was written.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md`,
  in this log and in the workbook has a row in its register file, and no other candidate row is cited.
- `verify_v4.py`: 10 changed v3 cells, all declared; 0 problems; every owner cell equal to the Ownership
  Map.

## Failures

None.
