# Edit log B-DATA-21 — Recovery Workbench Data Migration Approach next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Data Migration Approach v3.docx` was read once, converted to text with `compat/convert_sources.py` into `_work/msr/extract/B-DATA-21/`, and never edited. Version 4 is a new file next to it.
- Version 4 was written in full as markdown in the scratch folder, then rendered to docx with `compat/office_write.py md-docx` against a scratch copy of the source as the template. The template copy in `_work/msr/docs/B-DATA-21/` carries the same styles, fonts and section setup as the source; the only change made to the copy is that the six built-in heading style names are spelled in the lower-case form the docx library expects, so the headings render. Nothing of the source file was touched.
- Lines 1 and 2 are the two header lines of Template and Rules §R8.1. The document control table keeps its six source rows (Document, Version, Date, Prepared by, Structure, Decision) and adds one `Realignment` row carrying D-RCV-60, ADR-014, ADR-021, DP-15 and DL44. Version is 4 and the document date is 22 November 2026; the D-RCV-35 decision text is copied character for character.
- Sections 1 to 8 keep every section number, ID, number, table row and date of version 3. All 54 content lines of sections 1 to 8 of the converted source reappear in version 4 in the same order; the check found 0 not found. The only additions inside them are marked "Under D-RCV-60" notes: one after the section 1 table, one after the section 2 table, one after the section 4 table, one after the section 5 table, one after section 6, one after section 7 and one row in the section 8 open-decisions table. The three source decision rows DL12, DL29 and DL43 keep their text and their date unchanged.
- New section 9, migration by schema: the rules that apply to every schema (ADR-014 schema and login per service, ADR-021 and DP-15 per-service Flyway, DP-01 no cross-schema access, DP-05 one reader of the 30 views, P1 as the data engine), the 19 schemas with the tables that receive migrated rows, the 14 migration stories re-cut against the schema and owner of every table, the reference-data split of DP14 across its five owners, and the 8-step cutover order by schema.
- New section 10, cut-over, reconciliation and parallel run per schema: per-schema reconciliation rows in reconciliation_result (P1), the parallel run per schema with ten clean days, and the gate on every schema cutover. The global case-list check of section 7 stays the single gate and keeps case_list_row with P1 and the case list API with P3.
- New section 11, change log: the row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`, plus a two-row table that keeps the version 3 row and its 15 November 2026 date.
- Every owner in the document is the Ownership Map v1 owner of the table named: `_work/msr/plan/ownership.json` and the Ownership Map sheets `Services` and `Tables` were read row by row. 50 tables across 15 schemas receive migrated rows; four schemas carry none in this version (rwb_integration P2, rwb_agent P10, rwb_guarantee S3, and rwb_valuation S1 beyond the route-decision assumption). No owner is set by this document.
- Release dates in the new sections are copied from the plan and marked `(tentative)`: 30 November 2026 and 31 December 2026 for the 14 migration stories. No date was changed and no date is raised as a gap.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Data Migration Approach v4.docx`
- `_work/msr/docs/B-DATA-21/Recovery Workbench Data Migration Approach v4.md`
- `_work/msr/docs/B-DATA-21/template_v3_fixed.docx`
- `_work/msr/docs/B-DATA-21/write_rows.py`
- `_work/msr/docs/B-DATA-21/make_template.py`
- `_work/msr/docs/B-DATA-21/build_docx.py`
- `_work/msr/docs/B-DATA-21/fix_docx.py`
- `_work/msr/docs/B-DATA-21/postprocess.py`
- `_work/msr/docs/B-DATA-21/dump_v4.py`
- `_work/msr/docs/B-DATA-21/verify_docx.py`
- `_work/msr/docs/B-DATA-21/verify_src.py`
- `_work/msr/docs/B-DATA-21/probe_styles.py`
- `_work/msr/docs/B-DATA-21/patch_verify.py`
- `_work/msr/docs/B-DATA-21/patch_md.py`
- `_work/msr/docs/B-DATA-21/patch_log.py`
- `_work/msr/docs/B-DATA-21/final_check.py`
- `_work/msr/docs/B-DATA-21/patch_log2.py`
- `_work/msr/docs/B-DATA-21/patch_log3.py`
- `_work/msr/docs/B-DATA-21/v4_dump.txt`
- `_work/msr/gaps/B-DATA-21.jsonl`
- `_work/msr/assumptions/B-DATA-21.jsonl`
- `_work/msr/editlog/B-DATA-21.md`

The converted source text is `_work/msr/extract/B-DATA-21/Recovery Workbench Data Migration Approach v3.md`.

## Rows

- Candidate gap rows: 9, `GAP-0235` to `GAP-0243`, in `_work/msr/gaps/B-DATA-21.jsonl`, with every key of Template and Rules §R9. Types: 6 Missing, 3 Conflict. Severity: 5 at P2 and 4 at P3. Areas: data migration, reference data, delivery sequencing, retention.
- Candidate assumption rows: 9, `ASM-0325` to `ASM-0333`, in `_work/msr/assumptions/B-DATA-21.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on 5 and Medium on 4.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Source sections kept: 8 of 8, with 54 content lines checked and 0 not found. New sections: 3 (§9, §10, §11) with 8 subsections.
- Schemas: 19 named, with schema, service and wave from the Ownership Map `Services` sheet. Platform library tables: 6, created in every schema, no rows migrated.
- Tables receiving migrated rows: 50 in 15 schemas. P3 12, P7 6, P1 5, P4 5, P5 5, P6 3, S9 3, S4 2, S5 2, S6 2, P8 1, P9 1, S2 1, S7 1, S8 1; none in P2, P10, S3 and S1.
- Migration stories re-cut: 14 legacy keys, 14 rows, with 26 story IDs from the plan (DM-013 carries the P1, P8 and ITG stories).
- Reference data: 8 table groups across 6 schemas (P3, P7, P4, P6, P5, P1).
- Cutover order: 9 rows (step 0 plus steps 1 to 8).
- Document control: 7 rows, 1 change-log table with 2 rows and 1 change-log line.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-21 --quick`: C02, C03, C05, C12, C13 and C18 PASS, 0 findings.
- `verify_docx.py`: every line of the markdown version appears in the docx (paragraph or table row), 158 paragraph and table-row blocks, 0 missing, 0 backticks, 11 tables with borders and a repeating header row.
- `verify_src.py`: the 54 content lines of source sections 1 to 8 reappear in version 4, 0 not found.
- C17 by hand over the same write set: the 9 CG ids and 9 ASM ids cited in the document and in this log each have a row in their register file, and no other candidate row is cited.

## Failures

None. One tool note: the source docx spells the built-in heading styles in the capitalised form, which the docx library cannot resolve, so a scratch copy with the lower-case style names was made and given to `md-docx` as the template. The output keeps the source page setup, fonts and styles.
