# Edit log D2-CTL — Recovery Workbench Document Control Sheet v13

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.
Work package: D2-CTL (Recovery Workbench Document Control Sheet, next version). Fanout: 0.
Source: `12 Project communication/Recovery Workbench Document Control Sheet v12.xlsx` (read only, not edited).

## Files written

- `12 Project communication/Recovery Workbench Document Control Sheet v13.xlsx`
- `_work/msr/gaps/D2-CTL.jsonl`
- `_work/msr/assumptions/D2-CTL.jsonl`
- `_work/msr/editlog/D2-CTL.md`

Scratch, not deliverables: `_work/msr/docs/D2-CTL/` (probe.py, build_rows.py, rows.jsonl, rows_report.json, src_rows.json, finish.py) and `_work/msr/extract/D2-CTL/` (the converted text of the v10, v11 and v12 workbooks).

## What v13 is

The workbook is the v12 file copied and extended, never edited in place. The three source sheets are kept: `Control sheet`, `Summary` and `Key`. A fourth sheet, `Change log`, is added as the first sheet.

- **Change log sheet.** Lines 1 and 2 are the two header lines of Template and Rules §R8.1. Line 4 is the title, and cell A6 holds the change-log row exactly as the work package asks: `v13, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Below it, the sheet lists what v13 changes and the six gap rows that describe it.
- **Control sheet.** The 134 source rows (rows 5 to 138) are copied character for character: every number, document, file, reviewer, sign-off role, review status and comment. 161 rows are appended, numbered 135 to 295. The note in A2 keeps the source sentence and adds one sentence: 161 rows, 135 to 295, the realignment documents of D-RCV-60, each marked 'Document set v15' in the comments column, 295 documents in total, and the change log on its own sheet. The filter now reaches row 299.
- **Summary sheet.** Every formula range moves from rows 5 to 136 to rows 5 to 299, so the 134 source documents, the two documents that v12 left outside the range and the 161 added documents are all counted. No other cell changes.
- **Key sheet.** Copied unchanged.

## What the 161 added rows are

Each added row carries the label `Document set v15` in the comments column, the review status `Not started`, and a blank `Uploaded on` and `Signed off on`, as every source row does. Nothing is dated.

- **85 rows continue an existing family.** They take the priority band, the layer, the document name, the reviewed-by roles and the signed-off-by role of the source row for that document, as §R8.2 and the source sheet's own convention ask, and they hold the next version's file names. Examples: Engineering Practices v6.docx, the Architecture Decision Records v4.md with ADR-013 to ADR-023, the Physical Schema v7 folder, the Requirements Traceability Matrix v7.xlsx, the risks, assumptions, issues and dependencies file v5.xlsx.
- **76 rows are documents that are new in v15.** The BRD for Epics 3 to 8, the 20 PRDs, the service story catalog, the service epics file, 31 epic story-file rows, the service catalog, the service template specification, the service contract catalog, the Kafka topic and event catalog, the Temporal workflow and activity catalog, the integration test plan, the Day-1 work allocation, the service epic diagrams, twelve rows of run material in folder 22 and the two registers in folder 23. Their band, layer and roles come from the nearest family and are recorded as CG-D2-CTL-6 with ASM-D2-CTL-6.
- **Folder families are one row each**, with the file count and the file pattern in the Files cell: Functional Specifications by Module v7 (38 files), Technical Specifications by Module v6 (39 files), API Specification v5 (41 files), Physical Schema v7 (21 files) and Service Epic Diagrams v1 (62 files). The 1065 story files of the realignment are 31 rows, one per epic folder, with the count in the Files cell; this reading of "one row per new file" is recorded as CG-D2-CTL-3 with ASM-D2-CTL-3.
- **The owner.** Every row whose document belongs to one service names that service in the comments column, in the form `Owner: P3 rwb-case (Ownership Map)`. The owning service is taken from the Services sheet of the Ownership Map for the 19 services, and for platform documents the row names PLT. Service-specific PRDs, the FSD and TSD module rows and the physical schema row follow the same rule. The sheet keeps its eleven source columns and adds no twelfth, which is recorded as CG-D2-CTL-2 with ASM-D2-CTL-2.
- **Files present and files pending.** Every file named in an added row was checked against the tree. The document index v14 was not in the tree when this sheet was written, so its row says so and cites CG-D2-CTL-4; the project hub v15, the team start pack v3 and the CTO presentation v4 were issued by their own work packages during this run and are named as they are. The hub row also records the version collision with the v17 hub in folder 14 (CG-D2-CTL-1).

## Numbers copied unchanged

- 134 source documents, rows 5 to 138, and every number, date and comment they carry. The controlling rows stay as they are: D-RCV-35 (U1 to U5) signed 15 November 2026, and from 16 November 2026 D-RCV-36 (T1 to T10), ADR-011 and ADR-012.
- 1034 stories and 31 epics, the figures the story catalog and the Service Epics v1 file carry.
- 1065 story files in 31 epic folders; 38 files in Functional Specifications v7, 39 in Technical Specifications v6, 41 in API Specification v5, 21 in Physical Schema v7, 62 in Service Epic Diagrams v1, 20 PRDs.
- No release date and no other date was changed, so no `(tentative)` marker was needed on any row. `Uploaded on` and `Signed off on` stay blank, as in the source.

## Candidate registers

- Gaps: `_work/msr/gaps/D2-CTL.jsonl` — 6 rows, CG-D2-CTL-1 to CG-D2-CTL-6. CG-1 Conflict, P2, the project hub at v15 against the v17 hub in folder 14. CG-2 Missing, P3, no owner column. CG-3 Ambiguous, P3, "one row per new file" against the sheet's document granularity. CG-4 Missing, P3, the document index v14 not yet in the tree. CG-5 Outdated, P3, the Summary range stops at row 136 in v12. CG-6 Ambiguous, P3, no source states the band, layer or reviewer of a brand-new document.
- Assumptions: `_work/msr/assumptions/D2-CTL.jsonl` — 6 rows, ASM-D2-CTL-1 to ASM-D2-CTL-6, one per gap. Confidence Medium for ASM-1, ASM-3 and ASM-6, High for ASM-2, ASM-4 and ASM-5.
- Counts: CG rows 6, ASM rows 6. Only step D1 numbers rows as GAP-nnnn and ASM-nnnn; every citation in the workbook uses the CG-D2-CTL-n form.
- Citations in the workbook: CG-D2-CTL-1, -2, -3, -4, -5 and -6 all resolve to a gap row, and each has its assumption row.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-CTL --quick` — C02, C03, C05, C12, C13 and C18 all PASS; see the report under `22 Microservice Realignment/checks/reports/wp-D2-CTL-*.md`.
- C14 (header), C15 (release dates), C16 (service names), C17 (gap and assumption citations), C19 (planned output present with the D-RCV-60 row) and C20 (tool line) were run directly on the same artefacts: C14, C15, C16, C17 and C20 PASS. C19 still reports the document index v14 and the edit logs of D2-IDX, D2-HUB and D2-TSP; those files belong to the other communication work packages and are not in this work package's write list.
- The source rows were diffed against the output: 0 cells differ in rows 1 to 138 apart from the A2 note, and the Key sheet is identical. The Summary sheet differs in the nine formula cells that carry the range only.
- No person name and no e-mail address appears in any file written here; the ownership and reviewer values are roles and services. No issue-tracker, Confluence, GitLab, Figma or web call was made, and no git commit was made. No legacy master was changed.

## Notes for the assembler

- The workbook is one of the six documents of the communication family of the set; the project hub v15, the team start pack v3, the CTO presentation v4 and the project overview v5 were written by their own work packages during the same run, and the document index v14 was still to come (CG-D2-CTL-4).
- The 161 rows are appended after row 138 and are grouped by folder: 01, 02, 03 (BRDs, the non-functional specification, the functional specifications v7 and the 20 PRDs), 04 (masters, catalogs and the 31 epic folders), 05, 06, 08, 09, 10, 11, 12, 16, 22 and 23. A later version may sort them into the priority bands; this version does not reorder the source.
- The label `Document set v15` is the label the plan gives this set. The implementation plan calls the pre-realignment set `Document set v14`; no source document defines either label beyond that use.
