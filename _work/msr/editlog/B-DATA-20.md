# Edit log B-DATA-20 — Recovery Workbench Data Ownership and Stewardship next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx` was read once, cell by cell, and never edited. It was copied to `v4` with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 18 list what changed, rows 20 to 23 what did not, rows 25 to 28 the counts and rows 30 to 31 the open register rows.
- `Ownership`: three columns are appended at the end, `Owning service (D-RCV-60)`, `Owning schema (D-RCV-60)` and `Basis (D-RCV-60)`. Columns A to K keep their letters, positions and values. The 14 data products get one owner each, all from the Ownership Map sheet `Tables` and Architecture v5 slide 41: P1 rwb-source-data on DP01, DP02 and DP05; P3 rwb-case on DP03 and DP14; P5 rwb-document on DP10; P7 rwb-decision on DP12; P8 rwb-payment on DP13; S1 rwb-valuation on DP11; S2 rwb-treatment on DP04; S4 rwb-litigation on DP07; S5 rwb-asset on DP06; S6 rwb-debtsale on DP09; S9 rwb-partner on DP08.
- `Ownership split`: the same three columns are appended. Tier 1, Tier 2 and Tier 3 fall to P1 rwb-source-data (22 ACE tables and 14 new ACE tables read through the ACE view contract; 4 extension tables owned by P1). Tier 4 is split across 18 services and the platform library: P1 13, P2 3, P3 15, P4 5, P5 12, P6 3, P7 6, P8 1, P9 3, P10 8, S2 1, S3 1, S4 2, S5 2, S6 2, S7 1, S8 1, S9 3 and the platform library 6, which is 88 tables.
- `Ownership split`: two cells change in the `Workbench access` column, F7 and F8, from `Read and write by the recovery module` to the owning service and its own `rwb_<name>` schema (GAP-0234; ASM-0324).
- `Roles` gets one row (row 13, service data steward) and `Change process` one step (step 8, owner service); `Quality measures` gets one measure (row 12, schema isolation) and one changed cell, B10, so the view conformance check reads `no rwb_<name> table reads public.*` (GAP-0233, GAP-0234; ASM-0323, ASM-0324).
- Nothing else moved. `verify_v4.py` compares all five v3 sheets with v4 cell by cell: 3 changed cells in total (`Ownership split!F7`, `Ownership split!F8`, `Quality measures!B10`), no other difference, no row or column lost, no v3 sheet renamed, header and change log present, and all 14 data products carry an owner service and a schema.
- The source holds no date in any of its five sheets, so no release date is marked "(tentative)" and no date is changed. All DP01 to DP14 identifiers, the four tiers, the table counts and the 12 v3 roles are copied character for character.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx`
- `_work/msr/gaps/B-DATA-20.jsonl`
- `_work/msr/assumptions/B-DATA-20.jsonl`
- `_work/msr/editlog/B-DATA-20.md`
- `_work/msr/docs/B-DATA-20/build_notes.md`
- `_work/msr/docs/B-DATA-20/v3_dump.json`

Scratch scripts in `_work/msr/docs/B-DATA-20/`: `dump_v3.py`, `dump_ownmap.py`, `map_tables.py`, `probe_styles.py`, `build_v4.py`, `verify_v4.py`, `verify_v4.json`, `gen_rows.py`, `show_v4.py`.

## Rows

- Candidate gap rows: 11, `GAP-0224` to `GAP-0234`, in `_work/msr/gaps/B-DATA-20.jsonl`, with every key of Template and Rules §R9. Severity: 3 at P2 (GAP-0224, GAP-0225, GAP-0228) and 8 at P3. Types: 6 Ambiguous, 3 Missing, 2 Outdated. All 11 carry legacy_ref RWB-E1-001, the Epic 1 data story that built the single recovery schema and the 14 data products.
- Candidate assumption rows: 11, `ASM-0314` to `ASM-0324`, in `_work/msr/assumptions/B-DATA-20.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on 5 and Medium on 6.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Ownership: 14 data products and 14 owning services, over 11 owner codes (P1 3, P3 2, P5 1, P7 1, P8 1, S1 1, S2 1, S4 1, S5 1, S6 1, S9 1).
- Ownership split: 4 tiers; Tier 1 22 ACE tables through 16 views, Tier 2 14 new tables and 12 new columns through 14 views, Tier 3 4 extension tables, Tier 4 88 tables over 19 owners (18 services plus the platform library). S1 rwb-valuation owns no table row (GAP-0228).
- Roles 12 plus 1, Change process 7 plus 1, Quality measures 7 plus 1.
- Cells: 3 v3 cells changed out of the five sheets' full cell grid; 42 appended cells on `Ownership` (14 rows by 3 columns), 12 on `Ownership split` (4 tiers by 3 columns), 2 on `Roles`, 3 on `Change process`, 4 on `Quality measures` (3 appended plus the changed B10), plus the 31 lines of `Read me`.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-20 --quick`: C02, C03, C05, C12, C13, C18 and C20 are satisfied for this write set; the run is recorded in the console output of this task and in `22 Microservice Realignment/checks/reports/`.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md`, `editlog/B-DATA-20.md` and the workbook has a row in its register file, and no other candidate row is cited.
- `verify_v4.py`: 3 changed v3 cells, 0 problems, all 14 data products carry an owning service and a schema, all 4 tier rows carry both.

## Failures

None.
