# Edit log - WP C-ACG (Recovery Workbench Acceptance Criteria Glossary next version)

Work package: WP C-ACG. Decision: D-RCV-60 microservice realignment. Agent: aisdlc-msr-worker. Fanout: 0, so no subagent was started.
Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash. Date: 22 November 2026.

## Files written

- `04 User stories/Recovery Workbench Acceptance Criteria Glossary v2.xlsx` - the next version of the workbook, 6 sheets
- `_work/msr/gaps/C-ACG.jsonl` - 4 gap rows, `GAP-3150` to `GAP-3153`
- `_work/msr/assumptions/C-ACG.jsonl` - 4 assumption rows, `ASM-5540` to `ASM-5543`
- `_work/msr/editlog/C-ACG.md` - this file

Scratch only, under `_work/msr/docs/C-ACG/`:

- `src_dump.json` - every cell of the version 1 workbook, read with openpyxl, sheet by sheet
- `build_rows.py` - builds the four row JSONs
- `rows_readme.json`, `rows_frames.json`, `rows_prefixes.json`, `rows_additions.json` - the row JSON passed to `compat/office_write.py xlsx-append`
- `finalize.py` - sheet order, core properties, column widths, and the cell-by-cell comparison of the source sheets
- `write_jsonl.py` - writes the two registers
- `v2_dump.txt` - the new workbook read back, cell by cell, for review

No file that already existed was edited. `Recovery Workbench Acceptance Criteria Glossary v1.xlsx` is unchanged (same SHA-256, `25f3c8fe2b18bc54`).

## What was done

1. **Copy, then append.** `compat/office_write.py copy` made the version 2 file from the version 1 workbook; `xlsx-append` then added the two new sheets and the four new rows. The four source sheets were never touched: a cell-by-cell comparison of `Keywords`, `Sentence frames`, `Words` and `Code prefixes` between v1 and v2 reports 973 cells compared and 0 differences. So all 4 keyword rows, 55 sentence frames, 168 word rows and 15 code prefixes are kept as they stand, with their Thai text, their kinds, their examples and their order.

2. **Header and change log.** The new `Read me` sheet is first and its cells A1 and A2 are the two header lines of Template and Rules section R8.1. Below them: the document, version, date, decision, tool, status, source and audience; the change log with the version 1 source row and the version 2 row; the literal change-log line `v2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` (cell A21); a note on dates; what version 2 changes; and a sheet index.

3. **The three realignment additions only.** Three changes, all of them named by the work package and all of them taken from Template and Rules:
   - **Origin tag** (section R7.2 section 7). One row added to `Code prefixes` for `(legacy RWB-…-nnn ACn) / (new, D-RCV-60)` and one sentence frame for the tag at the end of a Scenario line.
   - **Contract mock Given** (section R5.4 class C, section R5.5 DP-11, section R7.2 section 12.8). One sentence frame, `the {service} contract fake is published`, with the example `Given the rwb-case contract fake is published`.
   - **-ITG** (section R7.2 section 16). One row added to `Code prefixes` for the integration test case suffix, with the example `TC-E1-001-01-ITG`.
   Nothing else was added, removed, renumbered or reworded.

4. **New sheet `Realignment additions`.** Three blocks. Block 1 gives the three additions with where each appears in a story, the rule with its source section, an example and the owner. Block 2 gives the contract fake of each of the 19 services: code, service, wave and REST base from the Ownership Map v1 `Services` sheet, the contract story pattern of section R5.2, and the contract group of that story. The contract group is deliberately not pinned to the service wave: 136 of the 288 CON slices in `split_plan.json` carry a wave earlier than their service wave, because section R5.6 keeps the business-epic wave, so the cell states the rule rather than a number. Block 3 lists the four questions this work package leaves open with their gap and assumption ids.

5. **Owners.** Every service owner in the workbook is read from the Ownership Map v1 `Services` sheet, which is the same 19 rows as section R4 of Template and Rules. The rwb-case fake is attributed to P3, the rwb-decision fake to P7, the rwb-source-data fake to P1, the rwb-access fake to P4 and the rwb-agent fake to P10, which is the map's reading of the section R3 default rulings on parameters and reference data, the case list API, the rule package registry, the interaction ledger and feature flags. The two documentation rows carry the fixed team-type phrases of section R5.3, because the map has no team-type owner.

6. **No names, no invented values.** The core properties of version 1 held a person name in `creator` and `lastModifiedBy`; version 2 sets both to the organisation and the tool line, and sets title, subject, description, category, keywords and revision 2. A scan of every cell finds no person name, no e-mail address and no issue-tracker reference. Every value that no source holds is the section R9 placeholder with its CG and ASM pair: three Thai cells, all pointing at `GAP-3150` and `ASM-5540`. No release date is invented, changed or raised as a gap; the workbook states that the source carries no version, date or change log rather than inventing one.

7. **Sheet order** of version 2: `Read me`, `Keywords`, `Sentence frames`, `Words`, `Code prefixes`, `Realignment additions`.

## Counts

- Gap rows: 4 (`GAP-3150` to `GAP-3153`). Severity: P1 0, P2 1, P3 3. Type: Missing 2, Ambiguous 2. Area: documentation 2, contract 1, testing 1.
- Assumption rows: 4 (`ASM-5540` to `ASM-5543`). Confidence: High 2, Medium 2, Low 0.
- Each gap is paired with one assumption and the pairing is one to one in both directions.
- New decision IDs: none beyond D-RCV-60. This document states no ADR or DL id of its own and cites no id outside `_work/msr/plan/ids.json`.
- Rows numbered GAP-nnnn and ASM-nnnn: none; step D1 numbers them.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-ACG --quick` at the end of the work package: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings. The report is under `22 Microservice Realignment/checks/reports/`.

Checked by hand as well, because the quick checks read the markdown and JSON files and not the workbook:

- the four source sheets compare equal cell by cell (973 cells, 0 differences), including the Thai column and the row order;
- the first two cells of the workbook are the section R8.1 header lines and the change-log line is present word for word in `Read me` cell A21;
- 8 register rows, 8 citations in the workbook, no citation without a row and no row without a citation;
- no person name, no e-mail address and no issue-tracker reference anywhere in the workbook or in the scratch files;
- the core properties name the organisation and the tool, not a person;
- 19 service rows in the contract fake table, matching the 19 rows of the Ownership Map v1 `Services` sheet one for one.
