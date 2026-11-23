# Edit log B-DATA-17 — Conceptual Data Model next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Conceptual Data Model v6.xlsx` was read once, cell by cell, and never edited. It was copied to `v7` with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Conceptual Data Model v7.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 18 list what changed, rows 20 to 22 what did not, rows 24 to 28 the counts and rows 30 to 31 the open register rows.
- `Entities`: three columns were appended at the end, `Owning service` (`P1` to `S9`, or `PLT`), `Target schema` (`rwb_<name>`, the read-only `recovery` schema for a view, or the platform-library wording) and `Ownership basis` (the map row and its reason). Columns A to G keep their letters, positions, values and the field counts. All 122 entities carry an owner: 88 Workbench tables, the 4 extension tables and the 30 `recovery.v_ace_*` views.
- The owner of every entity comes from the Ownership Map v1 sheet `Tables`, row by row, per the WP instruction "Use the Ownership Map for every owner". 91 of the 92 Workbench entities resolve on the table name; `Rule` resolves to `rule_row` (P7) and `List value` to `lov_value` (P3) on the LDM v8 dictionary. `Payment match rule` has no map row because D-RCV-36 T10 dropped the table, so it is recorded as P7 with that basis (GAP-0203). The 30 views are not in the map; they are P1 because only rwb-source-data reads them and owns the view contract (Architecture v5 slides 15 and 41; GAP-0202).
- `Subject areas`: one column appended, `Owning services`. 10 of the 17 subject areas span more than one service.
- `Data products`: one column appended, `Owning service(s)`. Column J and its `COUNTIF` formula are untouched, so each data product still counts its entities.
- `Relationships`: three columns appended, `Owning service (entity)`, `Owning service (refers to)` and `Cross-service reference`. 59 of the 104 relationships cross a service boundary: 11 are already a business key into an ACE view and 48 are a table-to-table reference whose foreign key is cut to a business key (DP-01; GAP-0206).
- `Service ownership`: a new last sheet, 19 service rows, a `PLT` row and a Total row, with schema, entities owned, the table and view split and a note where the owner is unusual (P1 the views, PLT the library objects, P7 the rule registry, S1 no entity).
- `Key`: five `Term` rows appended at rows 22 to 26 (Owning service, Target schema, PLT, Cross-service reference, Service contract). The 16 v6 rows are unchanged.
- Nothing else moved. `verify_v7.py` compares all six v6 sheets with v7 cell by cell: 0 differences outside the appended cells, no row or column lost, no sheet renamed, the `COUNTIF` formulas intact.
- The workbook carries no release date, so no date is marked "(tentative)" and no date is changed. The one date in the source, the 21 November date in the Gaps note on DL43, is a decision date and is copied character for character.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Conceptual Data Model v7.xlsx`
- `_work/msr/gaps/B-DATA-17.jsonl`
- `_work/msr/assumptions/B-DATA-17.jsonl`
- `_work/msr/editlog/B-DATA-17.md`
- `_work/msr/docs/B-DATA-17/build_notes.md`
- `_work/msr/docs/B-DATA-17/owners.json`

Scratch scripts in `_work/msr/docs/B-DATA-17/`: `map_owners.py`, `probe_aggs.py`, `build_v7.py`, `gen_rows.py`, `verify_v7.py`. The converted source text is `_work/msr/extract/B-DATA-17/Recovery Workbench Conceptual Data Model v6.md`.

## Rows

- Candidate gap rows: 8, `GAP-0202` to `GAP-0209`, in `_work/msr/gaps/B-DATA-17.jsonl`, with every key of Template and Rules §R9. Severity: 2 at P2 (GAP-0204, GAP-0206) and 6 at P3. Types: 4 Missing, 2 Ambiguous, 1 Conflict and 1 Outdated.
- Candidate assumption rows: 8, `ASM-0292` to `ASM-0299`, in `_work/msr/assumptions/B-DATA-17.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on 5 and Medium on 3.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Entities: 122 rows, 10 columns; 92 Workbench entities (88 tables and 4 extension tables) and 30 ACE source views.
- Owned per service: P1 48, P3 15, P5 12, P10 8, PLT 6, P4 5, P7 5, P2 3, P6 3, P9 3, S9 3, S4 2, S5 2, S6 2, S2 1, S3 1, S7 1, S8 1, S1 0.
- Subject areas: 17 and a Total row, one new column. Data products: 14 and a Total row, one new column, 97 entities inside the 14.
- Relationships: 104 rows, 45 inside one service, 11 to an ACE view and 48 cut across two services.
- Service ownership: 19 service rows, 1 PLT row and 1 Total row. Key: 21 rows. Gaps: 43 rows unchanged.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-17 --quick`: C02, C03, C05, C12, C13 and C18 PASS, 0 findings.
- `verify_v7.py`: 0 problems, all 122 entity rows carry an owner and a schema, 30 rows marked as read-only ACE views, 104 complete relationship rows, both header lines and the change-log row present.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md` and in this log has a row in its register file, and no other candidate row is cited.

## Failures

None.
