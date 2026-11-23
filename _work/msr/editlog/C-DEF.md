# Edit log — WP C-DEF (Story Defects, next version)

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. fanout: 0, no subagents.

## Files written

| File | Note |
|---|---|
| `04 User stories/Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx` | Next version of the defect register. The copied `Defects` sheet is v4 unchanged (121 rows, 7 columns, verified cell for cell), and a new first sheet `Realignment v5` carries the R8.1 header, the change-log row and one mapping row per defect |
| `_work/msr/gaps/C-DEF.jsonl` | 4 gap rows (GAP-3194 to GAP-3197) |
| `_work/msr/assumptions/C-DEF.jsonl` | 11 assumption rows (ASM-5589 to ASM-5599) |
| `_work/msr/plan/defects.jsonl` | 121 lines, keys id, legacy, story, note, as the Work Package asks |
| `_work/msr/docs/C-DEF/build_defects.py` | Scratch builder: reads the v4 workbook, the catalog and the plan, writes the rows JSON and the three registers |
| `_work/msr/docs/C-DEF/finish_book.py` | Scratch finisher: puts `Realignment v5` first, sets its widths and confirms the `Defects` sheet still matches v4 |
| `_work/msr/docs/C-DEF/rows.json` | Scratch rows file handed to `office_write.py xlsx-append` |
| `_work/msr/editlog/C-DEF.md` | This log |

No source file was edited and no file outside the "Write only" list was touched, apart from the one extra register the Work Package asks for at the end (`_work/msr/plan/defects.jsonl`).

## Counts

- CG rows: 4.
- ASM rows: 11.
- Defect rows: 121 (100 Open, 16 Closed 15 Nov 2026, 2 Fixed 29 Oct, 3 Closed).
- Mapping rows with a new story: 108. Rows with no new story (cancelled, retired or a fixed set-wide row): 13.

## How the Work Package was applied

- The v4 workbook is copied, never edited: `office_write.py copy`, then `office_write.py xlsx-append` of the new sheet. The `Defects` sheet keeps its two title rows, its header row, all seven columns, every status, ruling, decision and date character for character.
- `Realignment v5` opens with the two §R8.1 lines, then the change log with the row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. The finisher moves the sheet to the first position so the document starts on those lines.
- One row per defect: `Defect` (DEF-001 to DEF-121, sheet order), the v4 story and step, the v4 status, the realigned story IDs, work types, owner service from the Ownership Map v1, the R5.3 suggested-owner phrase, the release (dates unchanged, marked tentative) and a one-line mapping note.
- Story IDs come from the split plan, the Service Story Catalog v1 and the legacy map only; the builder stops if a cited ID is not in the catalog, and every ID in the mapping column and in the notes was checked against the 1034 plan slices.
- Owner and service come from the Ownership Map v1: `Services` for the code to service and wave, `Tables` for the twelve table owners named in the DEF-05 note (`hearing` and `legal_action` S4, `notice` P6, `write_off` S7, `asset_sale` S5, `proceeds` P8, `dp_treatment` and `interaction` P1, `decision_log_entry` P7, `debt_sale_account` S6, `treatment` S2, `recovery_case` P3) and `Jobs` for JOB-02, JOB-07, JOB-08, JOB-10, JOB-12 and JOB-14 named in the notes.
- Mapping rule (ASM-5590): a defect about section 10, 12 or 14 goes to the CON story of the key; a defect about a step, an exception path, a criterion or a test case goes to the APP story; a schema or key defect goes to the DB story where the catalog has one; a job or schedule defect goes to the OPS story; a defect that only names a header goes to every story of the key (ASM-5591).
- No new ADR or DL ID was needed: the document cites D-RCV-60, DL47 for the Epic 1 preservation rule and ADR-014 and ADR-021 for the schema and migration positions, all of them allocated in `_work/msr/plan/ids.json`.
- Release dates are copied unchanged and marked `(tentative)`; RWB-PLT-NF06-DB has no release date in any source, so the cell carries the §R9 placeholder with ASM-5599 and no date is raised as a gap.
- No person name, no email, no issue-tracker reference and no external call. Roles only, as the notes and the gap rows show.

## Open seams (all in the registers)

- DEF-05 (row 121): the twelve owners are named, but only P1, P3, P4, P7 and the platform have an ACE DB story, so seven services have no story for the column drop (GAP-3194; ASM-5594).
- The 13 rows of cancelled or retired keys (RWB-E1-003, E1-005, E1-006, E1-010, E1-012, E1-014, E1-029, E1-048, TE-005, TE-007) keep their v4 status and close with the key (GAP-3195; ASM-5592).
- The v4 sheet has no ID column and two rows carry the narrative labels DEF-05 and DEF-06; this run numbers the rows DEF-001 to DEF-121 and keeps both labels word for word (GAP-3196; ASM-5589).
- Row 93 closes against a replacement that no source dates: the DailyCaseRun workflow window is not stated anywhere (GAP-3197; ASM-5597).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-DEF --quick` returns PASS on all six quick checks (C02, C03, C05, C12, C13, C18), 0 findings each, after the outputs were written.

Run separately on the same file set, C01, C14, C17 and C20 also return PASS. C19 lists the planned outputs of the other work packages of the run that are not started yet; none of the findings names a C-DEF output.

FAILED items: none.
