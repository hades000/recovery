# Edit log - WP C3-TC (Test Cases next version and Regression Suite next version)

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Run date: 22 November 2026.
WP: `_work/msr/wp/C3-TC.md`. Agent: AI-SDLC QA Test Case Generator. Fanout: 0, so no subagent was used.

## Files written

- `09 Testing and quality/Recovery Workbench Test Cases v8.xlsx`
- `09 Testing and quality/Recovery Workbench Regression Suite v7.xlsx`
- `_work/msr/gaps/C3-TC.jsonl`
- `_work/msr/assumptions/C3-TC.jsonl`
- `_work/msr/editlog/C3-TC.md`

Scratch, inside `_work/msr/docs/C3-TC/`: `build.py` (the two builders), `write_registers.py` (the CG and ASM rows), `verify.py` (the source-cell comparison and the row audit), `extra_checks.py` (the wider check run) and `patch.py` (a one-off edit to `build.py`). No Markdown document was written, because both outputs are spreadsheets.

Every path above is inside the WP `Write only` block and nothing outside it was touched. The two sources were read only: `Recovery Workbench Test Cases v7.xlsx` and `Recovery Workbench Regression Suite v6.xlsx` are byte-identical to what they were before the run, and neither was edited. The new files were made by `compat/office_write.py copy`, and the columns, the Read me sheet and the added rows were then written into the copies by `build.py` with `openpyxl`, because the WP helper appends rows only and this WP also adds columns to an existing sheet.

## What the realignment changed

Only four things, in both workbooks:

1. **Owner column.** `Service`, the owning service of a case, on every row. It is the owning service of the case's legacy story from the Microservice Ownership Map v1 and the plan's primary owner (P1 to P10 and S1 to S9 to `rwb-<short>`), with `platform` for the RWB-PLT stories and `integration` for the RWB-ITG stories. A legacy story that was split lists every story that owns it in `Story key (new)`. No team name and no person is written.
2. **Story column.** `Story key (new)` gives every story of the target that owns the case. The source `Story` column (the legacy key) is untouched beside it, so both the old and the new identity of a case are on the row.
3. **Level column.** The source vocabularies (System, Access, Resilience, Operational, Schema, Rule table) are not the Template and Rules R7.2 vocabularies (Unit, Component, Contract, Integration, End to end, NFR). The source `Level` column is kept exactly as it is and a `Test level` column gives the R7.2 value: System, Schema and Access to Component, Resilience and Operational to NFR, Rule table to Component (GAP-3219, ASM-5622).
4. **`Origin`.** `legacy <story or rule set> (kept)` on a source row, `new, D-RCV-60` on an added row, so the source content and the realignment content are never confused.

Arrays of change:

| Sheet | Source rows | Rows added | New columns |
|---|---|---|---|
| Test Cases, Story test cases | 1,457 | 987 `-ITG` copies + 206 draft cases = 1,193 | O Service, P Story key (new), Q Test level, R Origin |
| Test Cases, Rule test cases | 448 | 0 | K Service, L Test level, M Origin |
| Regression Suite, Suite | 679 | 150 `-ITG` copies | K Service, L Story key (new), M Test level, N Origin |

**`-ITG` copies.** The 147 integration stories already hold the integration case of a case in section 16 of their story file, with the ID of the base case plus `-ITG` (Template and Rules R7.2). 987 of them copy a case that Test Cases v7 already holds, so those 987 rows were added to the case workbook, and the 150 of them whose base case the regression suite runs were added to the suite. The level and the data are the story's section 16 values; test name, given, when and expected result are the base row's own text, because the copy is the same assertion at integration level.

**Draft cases.** 30 stories hold no legacy case at all: 23 platform keys (N001, N001-CON, N002 to N012, NF01 to NF08) and 7 integration keys (W1J01, W1J02, W2J01, W3J01, W4J01, TE009, TE010). Their 206 section 16 rows were added, tagged `new, D-RCV-60`, with test name, given, when and then read from section 7 of the same story (or from the exception table of section 5 for an X path). No case was invented: every added row has an ID, a cover, a level and data that already exist in the story file.

**What was not added.** The WP says draft cases only for slices with no legacy case, so the 429 further section 16 rows of integration stories whose base case is outside the case workbook were not added; the workbook keeps its own 147-story scope (GAP-3220). The regression suite adds only the `-ITG` copy of a case it already runs, because its Growth sheet states that each release adds its cases; the 206 new platform and integration cases join it when their release ships (GAP-3225, ASM-5627).

**Retired and cancelled.** The 98 parked cases of the nine cancelled stories and the 20 live cases of the two stories retired under D-RCV-60 keep their text and their status, and carry `None` with the reason in the Service column instead of an invented owner (GAP-3223, ASM-5628, ASM-5629). Nothing was deleted and nothing was renumbered.

## Dates, header and change log

Neither workbook carries a release date, so no date was added and no release date was changed; the story release dates stay in the story files, unchanged and marked tentative (ASM-5633). The two source dates (16 November 2026 for Test Cases v7 and 15 November 2026 for Regression Suite v6) stay where they are, and the new change-log row carries 22 November 2026.

The two header lines of Template and Rules R8.1 and the change-log row sit on a new first sheet named `Read me` in both workbooks (`A1` and `A2`, then the metadata, then the change-log row `8, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` for the cases and `7, 22 November 2026, ...` for the suite). A spreadsheet cannot carry two free lines above its table without moving the source rows, and rule 1 forbids moving or editing a source row, so the header goes on its own first sheet (ASM-5631). Both workbooks are Draft, because no approval of this version is recorded in this run (ASM-5632).

## Verification

- **Source cells.** Every cell of every source sheet was compared with the same cell of the new workbook: Story test cases 1,461 rows and 14 columns, Rule test cases 452 rows and 10 columns, Suite 683 rows and 10 columns. **0 differences.** The source title lines (row 1 and row 2 of each sheet) and the source header row (row 4) are unchanged, including the sentence that counts the cases of the old version.
- **Columns.** Story test cases 18 columns wide with `Service`, `Story key (new)`, `Test level`, `Origin` in O to R; Rule test cases 13 wide with the three new columns in K to M; Suite 14 wide with the four new columns in K to N. No blank cell in any new column on any of the 3,927 data rows.
- **Identifiers.** 2,650 story-case IDs, all unique (1,457 source + 1,193 added). 829 suite rows, all unique. No added ID collides with a source ID.
- **Added rows.** No added row has a blank test name, expected result, data, service, story key or level. Every added row's level is one of Unit, Component, Contract, Integration, End to end, NFR: Integration 902, Component 136, NFR 73, Contract 43, End to end 35, Unit 4.
- **Owners.** Every one of the 1,457 source stories resolves to an owner: 1,339 to one of the 19 services, 98 to `None (cancelled)`, 20 to `None (retired)`. Every one of the 448 rule cases resolves through Architecture v5 slide 3: rwb-treatment 101, rwb-litigation 79, rwb-asset 72, rwb-decision 50, rwb-writeoff 51, rwb-debtsale 41, rwb-guarantee 32, rwb-deviation 22.

## Register counts

- Candidate gaps: **9 rows** in `_work/msr/gaps/C3-TC.jsonl`, `GAP-3218` to `GAP-3226`. By type: Missing 4, Conflict 2, Outdated 2, Ambiguous 1. By severity: P3 nine. No gap raises a date and none is P1 or P2. Every row carries the 15 keys of Template and Rules R9.
- Candidate assumptions: **14 rows** in `_work/msr/assumptions/C3-TC.jsonl`, `ASM-5621` to `ASM-5634`. By confidence: High 10, Medium 4. Nine rows answer a gap row (ASM-2 to CG-2, ASM-3 to CG-7, ASM-4 to CG-9, ASM-5 to CG-5, ASM-7 to CG-8, ASM-9 to CG-6, ASM-10 to CG-4, ASM-14 to CG-1, and ASM-6 to CG-2 as the companion); five are readings with no gap (ownership of a case, the parked and retired rows, the header sheet, Draft status, dates). Every row carries the ten keys of R9.
- **Count of CG rows: 9. Count of ASM rows: 14.** Only step D1 numbers them as GAP-nnnn and ASM-nnnn.
- The two citations in the workbooks (`GAP-3222` and `ASM-5625` on the owner column, `GAP-3218` to `GAP-3226` in the Read me sheet) all exist as register rows.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C3-TC --quick` was run and every quick check passes:

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

C02, C03 and C05 filter to story files and find none in this work package's file set, as expected: the outputs are spreadsheets and the story files belong to another work package. C12 (person names and e-mail addresses), C13 (issue-tracker references) and C18 (write-only compliance and the legacy master hashes) read the five files written here and all pass. C14, C17 and C20 were also run on the same file set and pass: every CG and ASM identifier cited anywhere in the file set has a register row, and both workbooks carry the header lines and the change-log row. C01 passes: no baseline document changed. C19 reports 67 findings, every one of them a planned output of another, not yet written work package; no finding names this WP, and both of its planned outputs exist with the D-RCV-60 change-log row present. No step failed three times.

## Not done, by rule

- No approval was sought and none is recorded; both workbooks are Draft.
- No issue tracker, Confluence, repository or web call was made, and no commit was created.
- No master file, no register numbering and no other document was written; the story files, the plan and the Ownership Map were read only.
