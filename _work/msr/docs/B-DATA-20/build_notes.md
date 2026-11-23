SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Build notes B-DATA-20 — Recovery Workbench Data Ownership and Stewardship v4

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx` was read once, cell by cell, and never edited. It was copied to `v4` with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx`.
- The Ownership Map v1 was read cell by cell: sheet `Services` (19 rows) and sheet `Tables` (93 rows, table, owner, schema). Every owner in v4 comes from that sheet; nothing is invented.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 18 list what changed, rows 20 to 23 what did not, rows 25 to 28 the counts and rows 30 to 31 the open register rows.
- `Ownership`: three columns are appended at the end, `Owning service (D-RCV-60)`, `Owning schema (D-RCV-60)` and `Basis (D-RCV-60)`. Columns A to K keep their letters, positions and values. The 14 data products get one owner each: P1 rwb-source-data on DP01, DP02 and DP05; P3 rwb-case on DP03 and DP14; P5 rwb-document on DP10; P7 rwb-decision on DP12; P8 rwb-payment on DP13; S1 rwb-valuation on DP11; S2 rwb-treatment on DP04; S4 rwb-litigation on DP07; S5 rwb-asset on DP06; S6 rwb-debtsale on DP09; S9 rwb-partner on DP08.
- `Ownership split`: the same three columns are appended. Tier 1, Tier 2 and Tier 3 fall to P1 rwb-source-data, because the 22 ACE tables and the 14 new ACE tables are read through the ACE view contract and the 4 extension tables are P1 rows. Tier 4 is split across 18 services and the platform library: P1 13, P2 3, P3 15, P4 5, P5 12, P6 3, P7 6, P8 1, P9 3, P10 8, S2 1, S3 1, S4 2, S5 2, S6 2, S7 1, S8 1, S9 3 and the platform library 6, which is 88 tables.
- `Ownership split`: two cells change in the `Workbench access` column. Tier 3 (F7) and Tier 4 (F8) read `Read and write by the recovery module` in v3; they now read the owning service and its own schema, because the monolith module and the single recovery schema are replaced by 19 services and 19 `rwb_<name>` schemas (CG-B-DATA-20-11; ASM-B-DATA-20-11).
- `Roles`: one row is appended, row 13, `Service data steward (D-RCV-60)`, who holds one `rwb_<name>` schema (CG-B-DATA-20-10; ASM-B-DATA-20-10). The 12 v3 roles are unchanged.
- `Change process`: one step is appended, step 8, owner service, for a Tier 3 or Tier 4 change made by the owning service in its own schema with its own Flyway sequence (CG-B-DATA-20-10; ASM-B-DATA-20-10). The 7 v3 steps are unchanged.
- `Quality measures`: one measure is appended, schema isolation, and one cell changes: the view conformance measure (B10) now reads `no rwb_<name> table reads public.*` instead of `no recovery table reads public.*` (CG-B-DATA-20-11). The other 7 v3 measures are unchanged.
- Nothing else moved. `verify_v4.py` compares all five v3 sheets with v4 cell by cell: 3 changed cells in total (`Ownership split!F7`, `Ownership split!F8`, `Quality measures!B10`), no other difference, no row or column lost, no v3 sheet renamed, header and change log present.
- The source holds no date in any of its five sheets, so no release date is marked "(tentative)" and no date is changed. All DP01 to DP14 identifiers, the four tiers, the table counts (22 ACE tables through 16 views, 14 new tables and 12 new columns through 14 views, 4 extension tables, 88 Workbench tables) and the 12 v3 roles are copied character for character.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Where each open row is cited

- CG-B-DATA-20-1 and ASM-B-DATA-20-1: the missing owner column, seen on `Ownership` column L and `Ownership split` column G.
- CG-B-DATA-20-2 and ASM-B-DATA-20-2: DP04, `Ownership` row 8 basis cell.
- CG-B-DATA-20-3 and ASM-B-DATA-20-3: DP06, `Ownership` row 10 basis cell.
- CG-B-DATA-20-4 and ASM-B-DATA-20-4: DP07, `Ownership` row 11 basis cell.
- CG-B-DATA-20-5 and ASM-B-DATA-20-5: DP11, `Ownership` row 15 basis cell and `Ownership split` row 8 basis cell.
- CG-B-DATA-20-6 and ASM-B-DATA-20-6: DP13, `Ownership` row 17 basis cell.
- CG-B-DATA-20-7 and ASM-B-DATA-20-7: DP05, `Ownership` row 9 basis cell.
- CG-B-DATA-20-8 and ASM-B-DATA-20-8: DP14, `Ownership` row 18 basis cell.
- CG-B-DATA-20-9 and ASM-B-DATA-20-9: the 88 against 93 count, `Ownership split` row 8 basis cell and `Read me` `Counts`.
- CG-B-DATA-20-10 and ASM-B-DATA-20-10: the three governance rows, `Roles` row 13, `Change process` row 12 and `Quality measures` row 12.
- CG-B-DATA-20-11 and ASM-B-DATA-20-11: the `Application owner (DL02)` and `the recovery module` wording, `Ownership split` cells F7 and F8 and `Read me` `What did not change`.

## Files written

- `06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx`
- `_work/msr/gaps/B-DATA-20.jsonl`
- `_work/msr/assumptions/B-DATA-20.jsonl`
- `_work/msr/editlog/B-DATA-20.md`
- `_work/msr/docs/B-DATA-20/build_notes.md`
- `_work/msr/docs/B-DATA-20/v3_dump.json`

Scratch scripts in `_work/msr/docs/B-DATA-20/`: `dump_v3.py`, `dump_ownmap.py`, `map_tables.py`, `probe_styles.py`, `build_v4.py`, `verify_v4.py`, `verify_v4.json`, `gen_rows.py`, `show_v4.py`.
