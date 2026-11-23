# C4-DEP edit log - Recovery Workbench Dependency Map v5

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Run date 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx`
- `_work/msr/gaps/C4-DEP.jsonl`
- `_work/msr/assumptions/C4-DEP.jsonl`
- `_work/msr/docs/C4-DEP/build_v5.py`
- `_work/msr/docs/C4-DEP/verify_v5.py`
- `_work/msr/docs/C4-DEP/stats-v5.json`
- `_work/msr/docs/C4-DEP/src_depmap.json`
- `_work/msr/editlog/C4-DEP.md`

The two sources were also converted to text in the run extract folder the work package
names, `_work/msr/extract/C4-DEP/`, with `compat/convert_sources.py` (usual `read only`
place, not an output of the family).

## What was done

The source `Recovery Workbench Dependency Map v4.xlsx` was copied to v5 with
`compat/office_write.py copy`, and the copy was then extended by
`_work/msr/docs/C4-DEP/build_v5.py`. The source file was never edited: all 1,389
non-empty cells of its four sheets compare equal between v4 and v5, cell by cell and
sheet by sheet.

- `Read me` (new, sheet 1): the two R8.1 header lines, title, one-line scope, tool line,
  version and Status Draft with its assumption, the change log (v4 as the source row and
  the v5 row "22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
  DeepSeek v4.1 Flash"), the same change-log row as a sentence, nine "what changed"
  bullets and the graph in numbers.
- `Dependencies` (kept): DEP-01 to DEP-36 with every ID, party, epic, date, owner,
  decision, effect and status unchanged. Three columns added: `Class (R5.4)` = X for all
  36 rows, `Blocks the build?` = No; tracked, and `Business epic (v5)` = EP01 to EP06.
  Five note rows added below the table.
- `Dependency classes` (new): the four classes of R5.4 with what each one blocks and its
  2,534-row count and share; what each class means for the plan; the seven checks the
  graph was put through with their result; the 20 decoupling patterns of R5.5 with the
  number of v5 rows that point at each pattern's dependency; the service template
  baseline; and the six Wave 0 platform dependencies of Architecture v5 slide 39 with
  their owner roles and whether a v4 row covers them.
- `Story dependencies v5` (new): 2,534 rows over 622 stories - H 1,600, C 440, I 412,
  X 82 - rebuilt from the Dependencies sheet of the Service Story Catalog v1. Each row
  names both stories with their titles, epics, work types, services, service codes from
  the Ownership Map v1, waves, the class, what the class blocks, the wave order and the
  suggested owner by work type. Frozen header, autofilter over all 17 columns.
- `Story dependencies v4` (kept, renamed from `Story dependencies`): the 325 legacy rows
  unchanged, with three note rows below.
- `Legacy dependency trace` (new): all 325 version 4 story dependencies mapped to the v5
  rows that carry them - 312 carried, 2 carried by the R6 redirect to RWB-PLT-E1071-CON,
  6 dropped with a retired story (RWB-E1-014, RWB-TE-007) and 5 not carried, each with
  its gap citation.
- `By service and class` (new): rows each service consumes and provides by class (out
  and in), a wave and class table, and the 36 external rows by business epic. Both
  service totals reconcile to 2,534.
- `By team and epic` (kept): the 13-row count matrix unchanged, with two note rows.
- `How they are tracked` (kept): steps 1 to 5 unchanged; steps 6 to 9 added for the four
  classes, the non-blocking C row, the ITG-only I row, the tracked X row and the weekly
  review.
- `Owners` (new): the 19 services of the Ownership Map v1 with wave, schema, REST base,
  topic and queue; the suggested owner of each work type of R5.3; and the external owner
  roles of the 36 rows with their business epics and decisions.

No release date appears on any sheet of this document, so no date was marked tentative.
The `Needed by` dates of the 36 external rows are dependency dates, copied unchanged
(`ASM-5656`). No person is named: owners are service codes, team types and external
roles only, and the workbook creator and last-modified-by properties were set to
"SCB Collections and Recovery" and the tool line.

## Counts

- Gap rows: 5 - `GAP-3232` (catalog 2,534 rows against the 2,609 of the story files,
  P3), `GAP-3233` (5 legacy dependencies not carried, P3), `GAP-3234` (10 X rows to
  a platform APP enabler, P3), `GAP-3235` (five Wave 0 dependencies of Architecture v5
  slide 39 with no DEP row, P1) and `GAP-3236` (124 non-CON stories with no row, 31 of
  them APP, P3).
- Assumption rows: 10 - `ASM-5647` to `ASM-5656`. One per gap (1 to 5) and five
  more for the decisions the document rests on (Draft status, the kept v4 sheet, the
  E1-to-EP01 column, the wave rule, the dependency dates).
- Every `CG-C4-DEP-n` and `ASM-C4-DEP-n` cited anywhere in the workbook resolves to a row
  in these two registers, and every row of the two registers is cited in the workbook.
- Rows numbered GAP-nnnn and ASM-nnnn: none. Numbering is step D1's.
- New decisions: none beyond D-RCV-60 and DL48, which the plan already holds. No ADR, DL
  or D-RCV ID from `_work/msr/plan/ids.json` is used or issued here.

## Corrections made during the run

- A first pass treated any retired dependency target as "carried by redirect" when the
  new story happened to carry RWB-PLT-E1071-CON; RWB-E1-063 to RWB-E1-014 was miscounted
  that way. The redirect is now limited to RWB-TE-007, which is the case Template and
  Rules R6 names, and the counts became 312 carried, 2 by redirect, 6 dropped, 5 not
  carried.
- The service-and-wave totals originally counted the `All` row as well; the verification
  now sums the five wave rows only and reconciles 2,534 twice.
- Three notes cited the assumptions in short form (`ASM-8`, `ASM-9`, `ASM-10`); all three
  were rewritten to the full ids so every citation resolves.
- The service-and-wave table first gave the integration epics wave 0; the ITG epics are
  not a service, so the row now reads 1 to 4 and the note says an ITG story carries the
  wave of its integration epic.
- One note and the impact of `ASM-5655` first gave the same-wave total as 1,156 and
  omitted the 8 X rows that point at an earlier wave; both were corrected to the counted
  values (1,278 earlier, 1,216 same, 40 later).
- The work-type and external-owner tables on the Owners sheet first left empty bordered
  columns between their fields; both were rebuilt with the owner text merged across the
  trailing columns.

## Check run

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C4-DEP --quick` - C02,
C03, C05, C12, C13 and C18 all PASS with no findings; the report is under
`22 Microservice Realignment/checks/reports/`.

C01 (legacy masters unchanged), C14 (R8.1 header), C17 (register keys and every citation
resolved), C19 and C20 (tool line) were also run against the files of this work package:
C01, C14, C17 and C20 PASS. C19 reports only the planned outputs of other work packages
that have not run yet and carries no finding for C4-DEP.

`_work/msr/docs/C4-DEP/verify_v5.py` re-checks the workbook independently and PASSes:
1,389 source cells equal, 2,534 rows in the same story-and-target set as the catalog,
class counts H 1,600 / C 440 / I 412 / X 82, 36 external rows all class X, 325 trace rows,
service and wave totals of 2,534, the R8.1 header and the change-log row, no person name,
no e-mail address, no issue-tracker reference and no monolith API base anywhere in the
workbook text or its properties.

## Notes

- No FAILED step and nothing was retried three times.
- The work package asks for the `.xlsx` to be extended through `xlsx-append`. That command
  appends rows to a sheet and cannot add columns, merged note rows or a sheet at position
  1, so the copy was extended by one writer script with openpyxl, run only against the v5
  copy. The source workbook was read only, and its hash is checked by C01 and by the
  verification script.
