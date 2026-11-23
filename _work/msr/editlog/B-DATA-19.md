# Edit log B-DATA-19 — Recovery Workbench Reference Data and Lists of Values next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Reference Data and Lists of Values v4.xlsx` was read once, sheet by sheet, and never edited. It was copied to `v5` with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 18 list what changed, rows 20 to 23 what did not, rows 25 to 28 the counts and rows 30 to 31 the open register rows.
- `Lists` (138 rows): four columns are appended at the end, `Owning service (D-RCV-60)`, `Owning schema (D-RCV-60)`, `Shared-list route (D-RCV-60)` and `Basis (D-RCV-60)`. Columns A to F keep their letters, positions and values. Owners come from `Ownership Map v1` sheet `Tables`: 126 lists are held by P3 rwb-case in `rwb_case`, 7 are ACE data read through P1 `rwb_source_data`, 2 are held in `rwb_document` (P5), 2 in `rwb_decision` (P7) and 1 in `rwb_access` (P4).
- `Lists`: the shared lists are read through the rwb-case list read `RWB-P3-E1043-CON` (DP-07), 124 rows; LOV-EXPOSURE, held in `parameter_catalog`, through the rwb-case parameters contract `RWB-P3-E1042-CON` (DP-06); LOV-TEAM through the rwb-case queue resource (DP-13); the 7 ACE lists through the P1 contract and never loaded (DP-05); the 2 P5 lists through the rwb-document contract; the 2 P7 lists through the rwb-decision rule packages `RWB-P7-E1073-CON` (DP-04); the P4 list through the rwb-access contract `RWB-P4-E1037-CON` (DP-08).
- `Reference tables` (14 rows): the same four columns are appended (F to I). `delegation_limit`, `role`, `permission` and `masking_rule` go to P4 (ASM-0070; Ownership Map), `rule_row` to P7 (ASM-0069), `document_type` and `retention_rule` to P5 (ASM-0076), `template` to P6, `partner` to S9, `queue`, `timer` and `reference_row` to P3, and the feature flags to the platform library (R-PREC default ruling).
- `Reference data starter` is a new sheet after `Reference tables`: 179 rows, one per service and starter item, 171 Load and 8 Read, over 18 service codes (all ten P services, S2 to S6, S8, S9 and the platform library). Four definition rows sit above the table and a count row below it. A row exists when the service owns a table whose column the list's `Used by` cell names, owns the ACE view the column is read from, or owns a reference table (GAP-0220; ASM-0310).
- `Reference data starter`: the 11 closed lists with no live field after D-RCV-35 give no row, and S1 rwb-valuation and S7 rwb-writeoff give no row because no list names a table they own, which is recorded as an open point (GAP-0219; ASM-0309).
- `Change process` gets one row (row 13, step 9, `Shared list`): a list is held and loaded once in its owning service, and every other service reads it through that owner's contract with the `asOf` business date; no service loads a second copy (DP-07).
- `Key` gets four rows (13 to 16): `Owning service (D-RCV-60)`, `Shared-list route (D-RCV-60)`, `Starter mode` and `Reference data starter`.
- `Values` is unchanged: 598 values with their Thai label `Pending (DL10)`, their order and their valid from date of 30 Nov 2026. No date is changed. The 598 dates are in-force dates of the values, not a document release date; the Read me says so, and the programme release of 30 November 2026 stays tentative in the programme documents, so no date is raised as a gap.
- Nothing else moved. `verify_v5.py` compares the five source sheets with v5 cell by cell, with value, number format, font and fill: 0 differences, no row or column lost, no sheet renamed. Only the new sheet, the 8 appended columns, the one Change process row, the four Key rows and the read-me sheet are new.
- Document properties were reset: the v4 creator was a person name, v5 sets the creator to `SCB Collections and Recovery, Henka Group`, `lastModifiedBy` to the tool line and the title to the v5 title. No person name, no e-mail address and no issue-tracker reference is written anywhere.
- No repository, wiki or web call was made; no commit was created; no human approval was requested.

## Files written

- `06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx`
- `_work/msr/gaps/B-DATA-19.jsonl`
- `_work/msr/assumptions/B-DATA-19.jsonl`
- `_work/msr/editlog/B-DATA-19.md`
- `_work/msr/docs/B-DATA-19/build_notes.md`

Scratch scripts and dumps in `_work/msr/docs/B-DATA-19/`: `derive.py`, `derive.json`, `build_v5.py`, `verify_v5.py`, `verify_v5.json`, `probe_lists.py`, `tables_owner.json`.

## Rows

- Candidate gap rows: 7, `GAP-0217` to `GAP-0223`, in `_work/msr/gaps/B-DATA-19.jsonl`, with every key of Template and Rules §R9. Severity: 3 at P2 (GAP-0217, GAP-0219, GAP-0220) and 4 at P3. Types: 1 Conflict, 1 Outdated, 2 Missing, 3 Ambiguous. Legacy refs: 6 carry RWB-E1-043 and 1 carries RWB-E2-027.
- Candidate assumption rows: 7, `ASM-0307` to `ASM-0313`, in `_work/msr/assumptions/B-DATA-19.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on 3 and Medium on 4.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Lists: 138 rows (124 closed, 14 source); 552 appended cells; owning service P3 126, P1 7, P5 2, P7 2, P4 1; route rwb-case list read 124, rwb-case parameters contract 1, rwb-case queue resource 1, ACE read through P1 7, rwb-decision 2, rwb-document 2, rwb-access 1.
- Reference data starter: 179 rows over 18 codes; 171 Load and 8 Read; wave 0 3, wave 1 147, wave 2 13, wave 3 10, wave 4 6.
- Reference tables: 14 rows, 56 appended cells; P4 4, P3 3, P7 2, P5 2, P6 1, S9 1, PLT 1.
- Values: 598 rows, 0 changed cells. Change process: 8 rows plus 1. Key: 12 rows plus 4. Read me: 31 lines.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-19 --quick`: C02, C03, C05, C12, C13 and C18 PASS with 0 findings, run after the edit log was written.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md`, `editlog/B-DATA-19.md` and the workbook has a row in its register file, and no other candidate row is cited.
- `verify_v5.py`: 0 differences over the five source sheets, shapes and auto-filters as expected, starter 179 rows, header and change-log row present, properties reset.

## Failures

None. No check failed after three attempts; no safety, credential or production-data issue was met.
