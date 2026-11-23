# Edit log B-DATA-25 — Recovery Workbench Data Quality and Reconciliation Rules next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source was converted once to text under the run scratch area with `compat/convert_sources.py`,
  read sheet by sheet, and never edited. It was copied to v4 with `compat/office_write.py copy`, and
  only the copy was changed: `06 Data/Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx`.
  The copy was then edited by the scratch script `build_v4.py`, because `xlsx-append` can only add rows
  to the end of a sheet and this version needs two appended columns, one changed meaning and a new
  first sheet; no other tool touched the file.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1.
  Row 9 is the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code /
  OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 17 say what changed, rows 19 to 21 what did not, row 24
  the counts and row 27 the open register rows.
- `Load checks` is unchanged, cell for cell: 98 retired checks, DQ-001 to DQ-098, interface INT-01 to
  INT-16, data product DP01 to DP13, owner and the status "Moved to ACE ingestion (RWB-ACE-001)". Two
  notes below the table record that ACE ingestion keeps the checks and that rwb-source-data is the
  only service that reads the 30 `recovery.v_ace_*` views (DP-05).
- `Reconciliations` keeps REC-01 to REC-09 with their source side, Workbench side, compared-on,
  tolerance, cadence and break route. Two columns are appended: `Owner (D-RCV-60)` names the service
  that holds the Workbench side (P3 and P1 for REC-01 and REC-02, S2, P8, P6 and P1, S7, S5, P7, and
  P1 with P3, P8, S5 and S6 for REC-09), and `Per-service reconciliation (D-RCV-60)` points at the row
  of the new sheet. Two notes below the table carry the split rule and the REC-08 change.
- `Reconciliations`, REC-08: two cells change. B12 (Source side) reads "Local decision record of each
  of the 19 services (rwb.decision-record.v1, via the rwb-decision contract)" and C12 (Workbench side)
  reads "Central decision ledger, rwb-decision (decision_log_entry), with its hash chain". The copy
  REC-08 compared is the copy to the data lake, retired with RWB-E1-014, and JOB-13 is now a continuous
  Kafka ingest (GAP-0270; ASM-0360).
- `Per-service reconciliation` is a new sheet with three blocks. Block 1 gives one row per service (19
  rows) with the schema, the tables of the Ownership Map sheet `Tables`, the part of each check the
  service runs over its own rows and what it reconciles against, the key, the tolerance, the cadence,
  the break and result route, the pattern and the basis. Block 2 splits the nine reconciliations by
  the service that holds each side. Block 3 records the REC numbering, because the source numbers the
  notice-barcode check REC-05 and the business-key check REC-09 while RWB-E1-011 and every realigned
  slice number them the other way round (GAP-0273; ASM-0363).
- Every tolerance, key, cadence and break route already in the source is copied unchanged. The ten
  services with no legacy reconciliation row (P2, P4, P5, P10, S1, S3, S4, S6, S8, S9) carry the §R9
  placeholder in the tolerance cell (GAP-0272; ASM-0362). The S1 tables cell carries the
  placeholder because the Ownership Map lists no S1 table (GAP-0274; ASM-0364).
- `Quality measures` keeps its six measures and targets. One column is appended, `Owner service
  (D-RCV-60)`, taken from the Ownership Map (P1, P3 and every service). B7 changes to "The ACE batch
  for the business date is complete when rwb-source-data reads it and publishes AceDataReady", because
  only rwb-source-data holds the 30 ACE views (GAP-0276; ASM-0366).
- No value was invented: every owner comes from the Ownership Map, every other value from the source,
  and every missing value is the §R9 placeholder with a candidate gap row and a candidate assumption
  row. The source holds no version number and no release date, so no date is changed and no release
  date is marked "(tentative)".
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or
  web call was made; no commit was created. No file outside the WP write list was created or changed.

## Files written

- `06 Data/Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx`
- `_work/msr/gaps/B-DATA-25.jsonl`
- `_work/msr/assumptions/B-DATA-25.jsonl`
- `_work/msr/editlog/B-DATA-25.md`
- `_work/msr/docs/B-DATA-25/build_notes.md`
- `_work/msr/docs/B-DATA-25/v3_dump.json`
- `_work/msr/docs/B-DATA-25/verify_v4.json`

Scratch scripts in `_work/msr/docs/B-DATA-25/`: `build_v4.py`, `verify_v4.py` and `check_editlog.py`
(the last one checks this log against the write list of the WP).

## Rows

- Candidate gap rows: 9, `GAP-0268` to `GAP-0276`, in `_work/msr/gaps/B-DATA-25.jsonl`,
  with every key of Template and Rules §R9. Types: 2 Conflict (-1, -8), 4 Missing (-2, -4, -5, -7),
  2 Outdated (-3, -9) and 1 ID collision (-6). Severity: 5 at P2 (-1, -2, -3, -6, -8) and 4 at P3 (-4,
  -5, -7, -9). `needed_by_wave` is 1 on six rows, 2 on two (-5, -8) and 3 on one (-7). The legacy keys
  they reference are RWB-E1-011, RWB-E1-014 and RWB-AD-019.
- Candidate assumption rows: 9, `ASM-0358` to `ASM-0366`, in
  `_work/msr/assumptions/B-DATA-25.jsonl`, one per gap, each with `gap` pointing at its CG row.
  Confidence High on 7 and Medium on 2 (-4, -7).
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9
  require.

## Counts

- Load checks: 98 rows, 992 populated source cells, 0 changed; 2 notes added below the table.
- Reconciliations: 9 rows; 2 appended columns (2 headers, 18 values); 2 changed cells (B12, C12);
  2 notes.
- Quality measures: 6 rows; 1 appended column (1 header, 6 values); 1 changed cell (B7); 1 note.
- Per-service reconciliation: 19 service rows, 9 reconciliation split rows, 6 numbering rows and 1
  closing note; 19 services, 93 tables in the Ownership Map.
- Changed source cells: 3 of 1087 populated source cells across the three source sheets.
- Candidate gap rows: 9. Candidate assumption rows: 9.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-25 --quick`: C02, C03, C05,
  C12, C13 and C18 PASS, 0 findings, both before and after this log was written.
- `verify_v4.py`: 3 changed source cells, all declared; 0 problems; every per-service name, schema and
  table equal to the Ownership Map; every placeholder carries a citation; every cited candidate row
  exists in its register file. Result PASS.
- C17 by hand over the same write set: the 18 cited candidate rows all have a row in their register
  file and no uncited row was created.

## Failures

None.
