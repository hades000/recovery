# Edit log - WP B-TECH-16 (Recovery Workbench System Disposition and Integration Inventory next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench System Disposition and Integration Inventory v3.xlsx`
(converted text, all four sheets and every row: 25 systems and 36 interfaces), the same family at v2 (sheet By route
only, read to check whether the counts were ever filled), `22 Microservice Realignment/Recovery Workbench Microservice
Story Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9), `_work/msr/plan/ownership.json` and `22 Microservice
Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Read me, Services, Tables, FK cuts, Endpoints and
the event and job sheets), `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 2,
6 to 9, 13 to 20, 23, 29, 30, 37, 41, 44 and 45), `22 Microservice Realignment/Recovery Workbench Temporal and Drools
Design Text Extract v1.md` (one transaction, decision record, points of no return), `_work/msr/plan/split_plan.json`
("stats" and "legacy" only) and `_work/msr/plan/ids.json`. Nothing read was edited; the v3 workbook was opened
read-only and the v4 file was copied from it, never the source.

## Files written

- 05 Technical architecture/Recovery Workbench System Disposition and Integration Inventory v4.xlsx
- _work/msr/docs/B-TECH-16/build.py
- _work/msr/docs/B-TECH-16/verify.py
- _work/msr/docs/B-TECH-16/rows.py
- _work/msr/docs/B-TECH-16/roundtrip/Recovery Workbench System Disposition and Integration Inventory v4.md
- _work/msr/gaps/B-TECH-16.jsonl
- _work/msr/assumptions/B-TECH-16.jsonl
- _work/msr/editlog/B-TECH-16.md

Scratch only under `_work/msr/docs/B-TECH-16/`: `build.py` (changes the copy sheet by sheet), `verify.py` (source diff,
counts, header, change log and properties), `rows.py` (the candidate register rows) and the round-trip extract used to
check the workbook. The converted source text sits in the run extract folder, `_work/msr/extract/B-TECH-16`, with the v2
extract in its `v2` subfolder.

## 1. How the next version was produced

The source was never edited. It was copied to v4 with `compat/office_write.py copy`, and only the copy was changed:

1. **Read me sheet added first.** Rows 1 and 2 are the header of Template and Rules §R8.1. Row 4 names the version and
   the decision, rows 5 to 8 the scope, the tool line, the status (Draft, no approval recorded) and the release line,
   rows 10 to 12 the change log, rows 14 to 21 what the version holds, rows 23 to 26 the counts, rows 28 to 34 the
   sources and rows 36 to 41 the open points. Row 11 is the change-log row
   `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`; row 12 records
   the source version, v3 of 15 November 2026.
2. **Disposition sheet: one Service column.** Inserted after Owner (column F) and filled on 25 of 25 rows from the
   Microservice Ownership Map v1. Every other cell of the 25 rows is the v3 value character for character, and the
   title, the description row and the header row keep their text.
3. **Interfaces sheet: one Service column.** Inserted after Owner (column K) and filled on 36 of 36 rows. Every other
   cell of the 36 rows is the v3 value character for character, header and description rows included.
4. **By route sheet: the counts calculated.** The six rows of v3 (COLLINS, File, Direct through ACE, Through partners,
   Not at all today and Total) now carry In, Out, Both and Total, recounted from the Interfaces sheet in `build.py`:
   COLLINS 8/0/0/8, File 8/4/0/12, Direct through ACE 1/3/3/7, Through partners 1/0/0/1, Not at all today 2/5/1/8,
   Total 20/12/4/36. The route vocabulary, the row order and the sheet title are unchanged.
5. **Key sheet: six rows appended.** The 23 key rows of v3 (rows 5 to 27) are untouched; rows 28 to 33 add Service, the
   three readings of the Owner column (Workbench per service, ACE team as the ingest path, Bank platform as the
   endpoint), the two interface IDs that Architecture v5 removes, and the pointer to the Service rules.
6. **By service sheet (new).** The 36 interfaces counted per owning service with the interfaces of each service named:
   P1 17, P6 3, S5 3, P2 2, P9 2, and P4, P8, P10, PLT (RWB-PLT-OBS), S3, S4, S6, S8 and S9 one each, with a Total row
   of 36. Calculated from the Service column in `build.py`, not typed.
7. **Service rules sheet (new, SR-01 to SR-19).** One rule per path group, with the service it gives, the rows it
   covers and the slide, ADR or Ownership Map ruling behind it, so every Service cell can be traced.
8. **Realignment changes sheet (new, R-01 to R-14).** Every change of this version with the v3 value, the v4 value, the
   decision, the pattern and the basis.
9. **Workbook properties.** The v3 file carries a person name in `creator` and `lastModifiedBy`. The v4 file is set to
   `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `… Inventory v4`, revision 4, modified
   22 November 2026 (root rule 4; ASM-3399).

**Columns and widths.** The two Service columns carry the body style of their sheet (Aptos 10, wrapped, top aligned) and
a width of 22 and 20; the widths and the autofilters of the shifted columns were reset (`A4:J29` and `A4:N40`), because
`insert_cols` does not move column widths.

## 2. Fidelity to version 3

`verify.py` diffed the v4 file against the untouched v3 file, cell by cell:

| Item | Result |
|---|---|
| Disposition rows 5 to 29, all 9 source columns | 0 differences (225 cells) |
| Interfaces rows 5 to 40, all 13 source columns | 0 differences (468 cells) |
| Key rows 1 to 27, all 3 columns | 0 differences (81 cells) |
| Titles, description rows and header rows of all four source sheets | Unchanged |
| Service cells filled | 25 of 25 and 36 of 36 |
| Header lines 1 and 2 of the Read me sheet | Present, as the first two rows |
| Change-log row with D-RCV-60 and the tool line | Present (row 11) |
| By route counts | Equal to a recount of the 36 interfaces |
| By service counts | Equal to a recount of the Service column |
| Person name or email address anywhere in the workbook | None; properties are the organisation and the tool |
| v3 file on disk | Byte-for-byte unchanged (sha256 `d78cb10f14f63d6c…`) |

Every ID (25 systems, INT-01 to INT-36, DP01 to DP14, DL03 to DL40, DT06 to DT12, D-RCV-35, RWB-ACE-001, E1 to E8), every
number (36 interfaces, 32 systems, 25 systems and tools, the interface counts, the frequency and data product values) and
the one date reference of the source are kept. The workbook carries no release date, so no `(tentative)` mark was
needed; the release line of the Read me states that any date written later is tentative (U7, DL48;
ASM-3400). No date is raised as a gap.

## 3. What version 4 changes, and why

The change set is the realignment only:

1. **One owning service per path.** The source gives an Owner of "ACE team", "Workbench" or "Bank platform" and names no
   service. The new Service column names one service per row from the Microservice Ownership Map v1 and the scope of the
   19 services in Architecture v5: the inbound ACE path goes to P1 rwb-source-data because only it reads the 30
   `recovery.v_ace_*` views (ADR-010; slides 7, 9, 15 and 29); the outbound file path to P2 rwb-integration unless a
   route service owns the content (slides 16 and 17); the route or platform service for the rest. The derivation is
   written per group on the Service rules sheet, so no cell is an assertion without a basis.
2. **The source Owner column is kept and read per service.** The Key sheet gains a row for each of the three source
   readings, so a reader of the source wording and a reader of the target see the same path.
3. **The data lake.** The row "Data lake and Power BI" and INT-19 and INT-20 stay with the IDs and the wording of v3 and
   carry P9 rwb-reporting, while Architecture v5 removes the data lake (slides 2, 7, 9 and 37) under DP-17 and ADR-018.
   The conflict is recorded rather than resolved by deletion, because the work package keeps every ID
   (GAP-2109; ASM-3388).
4. **The blank counts.** The By route sheet says it is calculated from the Interfaces tab but every count cell is empty
   in v2 and v3; v4 calculates them from the 36 rows and records the rule (GAP-2108; ASM-3386).
5. **Two new sheets for the target.** By service answers "how many interfaces does each service own", which the story
   split needs; Service rules carries the basis of every assignment.
6. **Decisions.** The workbook cites D-RCV-60 with the IDs of `_work/msr/plan/ids.json`: ADR-013, ADR-014, ADR-018,
   ADR-019, ADR-023, DL44, DL46 and DL48. No new ADR or DL ID was allocated by this work package.

## 4. Owners

Every Service cell is a code and short name of the Microservice Ownership Map v1 (P1 to P10, S1 to S9) or the platform
observability set `RWB-PLT-OBS` for PLT (ASM-3387, ASM-3396). No owner is a team type, a person or a story
master value. The 36 interfaces are owned by 13 services and PLT; the 25 systems are led by P1 on 15 rows and name one
service per interface on 9 rows. Four services (P3 rwb-case, S1 rwb-valuation, S2 rwb-treatment and S7 rwb-writeoff) own
no row because they consume the paths through P1 and P2 rather than owning one (GAP-2110; ASM-3397).

## 5. Registers

- Gap rows written: **8** candidate rows, `GAP-2108` to `GAP-2115`, in `_work/msr/gaps/B-TECH-16.jsonl`
  (2 Outdated, 2 Conflict, 2 Ambiguous, 2 Missing; 2 of severity P2 and 6 of P3; areas: interfaces 5, ownership 1, data
  1, documentation 1).
- Assumption rows written: **16** candidate rows, `ASM-3385` to `ASM-3400`, in
  `_work/msr/assumptions/B-TECH-16.jsonl` (11 High, 5 Medium).
- Every gap row names its assumption, every assumption that rests on a gap names it, and every citation in the workbook
  resolves to a row: the workbook cites GAP-2108 to -8 and ASM-3385 to -16, and no citation is unresolved.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as root rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-16 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

C02, C03 and C05 are the story-file checks and there is no story file in this work package. C12 finds no person name and
no email address in the files of this WP (the workbook properties carry the organisation and the tool). C13 finds no
issue-tracker reference. C18 finds no write outside the "Write only" list and no change to a story master.

`verify.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row present, 0 changed source cells in
the 225 disposition, 468 interface and 81 key cells, 25 and 36 Service cells filled, the By route and By service counts
equal to a recount, 29 Key data rows (23 of v3 plus 6), the three new sheets present in order, no person name and no
email address, and properties set to the organisation and the tool. The v3 workbook is byte-for-byte unchanged on disk.

## 7. Status and boundaries

The workbook is issued in **Draft**: no approval is recorded for this run (ASM-3385). No later lifecycle stage was
started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the family was touched, and the v2 and v3 workbooks were read only.
