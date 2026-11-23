# WP B-BIZ-36 — Recovery Workbench Feature List v5

Decision D-RCV-60 microservice realignment. Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- 02 Business architecture and process/Recovery Workbench Feature List v5.xlsx
- _work/msr/docs/B-BIZ-36/readme.md
- _work/msr/docs/B-BIZ-36/build_v5.py
- _work/msr/gaps/B-BIZ-36.jsonl
- _work/msr/assumptions/B-BIZ-36.jsonl
- _work/msr/editlog/B-BIZ-36.md

## What was read

1. 02 Business architecture and process/Recovery Workbench Feature List v4.xlsx (source, never edited), converted to text under _work/msr/extract/B-BIZ-36/
2. 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (§R1, §R3, §R5, §R8, §R9)
3. 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (Read me, Services, Tables, Rulings)
4. 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (slides 18, 37, 41 and 44; lines 18, 707, 2043, 2296, 2701-2713, 2881, 2920, 2974)
5. 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
6. _work/msr/plan/ownership.json (services, tables and rulings)
7. _work/msr/plan/split_plan.json ("stats" and "legacy" only)
8. _work/msr/plan/ids.json

## How the workbook was built

1. `python -I "22 Microservice Realignment/compat/office_write.py" copy` of the v4 workbook to v5. The source was never opened for writing.
2. `python -I "_work/msr/docs/B-BIZ-36/build_v5.py"` on the copy: a "Read me" sheet is created first from _work/msr/docs/B-BIZ-36/readme.md, two columns are appended to Features (O and P) and to By module (H and I), "(tentative)" is added to every release date on Features and By epic, and two Column rows are inserted in Key.
3. `xlsx-append` was not used: it can only append rows at the end of a sheet, and this WP needs two appended columns and a new first sheet. The builder script does the same job on the same copy with openpyxl and writes nothing else.

## What changed

- New first sheet "Read me": R8.1 header on rows 1 and 2, document title, next-version note, tool line, change log with the row "v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", what changed, what did not change, counts and open points.
- Features: columns O "Service (D-RCV-60)" and P "Service epic (D-RCV-60)" on all 378 rows, from the Ownership Map ("P1 rwb-source-data", "RWB-SVC-P1"); autofilter widened to A4:P382.
- Features: release dates keep every character and add "(tentative)".
- By module: columns H and I, the same two columns, on the 19 module rows; the Total row stays empty; autofilter widened to A4:I23.
- By epic: release dates keep every character and add "(tentative)".
- Key: two Column rows for the two new columns, after the "Column | L1 processes" row.

## What did not change

- All 378 feature rows (368 live and 10 retired): Feature ID, module, module name, class, feature, what it does, primary role, other roles, L1 processes, systems, epic, story keys and depends on.
- The note rows of all four source sheets, the sheet order, the freeze points and the live COUNTIFS formulas on By module and By epic. The appended columns sit outside every formula range.
- No feature is added, retired, renamed or re-scoped in this version. The realignment findings are carried as gap and assumption rows and named in the "Open points" note.

## Placeholder policy

Every value in the two new columns comes from the Ownership Map v1 Services sheet; no value was invented and no placeholder was needed inside the workbook. The eight open points are cited from the Read me sheet as GAP-0149 to GAP-0156 and ASM-0233 to ASM-0240.

## Gap and assumption counts

- Gap rows: 8 (GAP-0149 to GAP-0156), one per finding: module-to-service mapping and 13 differing names; the single recovery schema of FEAT-RDF-01; the ten ledger features in P7; three features on the retired story A14; seven features naming the data lake and Power BI; nine features naming Quartz; the missing wave column and 141 features in 17 differing pairs; two feature-flag features in P3.
- Assumption rows: 8 (ASM-0233 to ASM-0240), one for each gap row, with read, confidence, confirm and impact.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-BIZ-36 --quick` — C02, C03, C05, C12, C13 and C18 all PASS.
