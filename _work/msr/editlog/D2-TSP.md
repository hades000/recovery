# Edit log D2-TSP

Work package: WP D2-TSP, Recovery Workbench Team Start Pack next version.
Decision: D-RCV-60 microservice realignment. Agent: aisdlc-msr-worker. Fanout: 0, so no subagent was started.
Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Sources read

- `12 Project communication/Recovery Workbench Team Start Pack v2.pptx` (all 13 slides, every shape, table and cell).
- `_work/msr/editlog/` (the edit logs of the run, for the house style of a next-version deck).
- `_work/msr/extract/D2-TSP/Recovery Workbench Team Start Pack v2.md`, made with
  `python -I "22 Microservice Realignment/compat/convert_sources.py"` from the v2 deck.
- Template and Rules v1, `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md`,
  §R1, §R3, §R4, §R5, §R6, §R8 and §R9.
- `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`
  (Read me, Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Parameters and Rulings).
- `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md`.
- `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`.
- `_work/msr/plan/split_plan.json` ("stats" and "legacy" only) and `_work/msr/plan/ids.json`.
- `11 Delivery and operations/Recovery Workbench Day-1 Work Allocation v1.xlsx` (the assembled list of the 939 Day-1
  stories, sheet by team type), read only to take the counts and the first stories of each team type.

The v2 deck was never opened for writing. Nothing read was edited.

## Files written

- `12 Project communication/Recovery Workbench Team Start Pack v3.pptx` - the next version of the pack: 20 slides.
- `_work/msr/gaps/D2-TSP.jsonl` - 8 gap rows, `CG-D2-TSP-1` to `CG-D2-TSP-8`.
- `_work/msr/assumptions/D2-TSP.jsonl` - 10 assumption rows, `ASM-D2-TSP-1` to `ASM-D2-TSP-10`.
- `_work/msr/editlog/D2-TSP.md` - this log.

Scratch files under `_work/msr/docs/D2-TSP/` (build and verification only):

- `_work/msr/docs/D2-TSP/build.py` - the script that builds v3 from the copy.
- `_work/msr/docs/D2-TSP/verify.py` - the script that compares v2 and v3 and checks the header, the change log, the page numbers and the citations.
- `_work/msr/docs/D2-TSP/v2-slide-text.txt` - the text of the source deck, extracted for the comparison.
- `_work/msr/docs/D2-TSP/v3-slide-text.txt` - the text of the new deck, extracted for the comparison.
- `_work/msr/docs/D2-TSP/render/Recovery Workbench Team Start Pack v3.pdf` - a render of all 20 slides.
- `_work/msr/docs/D2-TSP/render/s02.png`, `s05.png`, `s15.png`, `s16.png`, `s17.png`, `s18.png`, `s19.png`, `s20.png` - page images read to confirm that no table touches its note and no shape leaves the slide.

No file that already existed was edited; the v2 deck is unchanged.

## 1. How the next version was produced

`compat/office_write.py copy` made `Recovery Workbench Team Start Pack v3.pptx` from the v2 deck, and `build.py` then
changed only the copy. `pptx-append` was not used because the new slides are tables, and its text-only placeholders
cannot hold a table; the deck grammar was rebuilt from the deck itself instead:

1. **The read-me slide at position 2.** Built from the deck's own shapes: the 24 pt bold Aptos title in `4E297F` with
   the hairline rule and the `595959` page-number box, copied from a numbered source slide, and a table with the deck's
   own style `{5940675A-B579-460E-94D1-54222C63F5DA}`, the `DCD3EB` header fill and white body cells.
2. **Page numbers follow the position.** Only the number in the page-number box of the twelve numbered source slides
   changed (2 to 13 became 3 to 14); the new slides are numbered 15 to 20, and the read-me slide is 2.
3. **Six new content slides, 15 to 20.** Each is a table with a note, in the same grammar as the source tables, sized so
   that no table reaches its note and no note reaches the page number.
4. **Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. The new file is set to
   `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Team Start Pack v3`,
   revision 3 and modified 22 November 2026 (rule 4).

**Header and change log.** The read-me slide (position 2) carries the two header lines of Template and Rules §R8.1 as
its first two body lines, then the change-log row
`3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`, the row it follows
(`2, 28 October 2026, the issued deck`), what is kept, what changes, the owner rule, the dates and the Draft status.

## 2. Fidelity to version 2

`verify.py` extracts every text line and every table cell of both decks and compares them.

| Item | Result |
|---|---|
| Non-empty lines of version 2, page numbers excluded | 355 |
| Lines of version 2 present in version 3 | 355 of 355 |
| Source slides kept slide for slide | 13, at positions 3 to 14 |
| Change to a source slide | the page number, and the release column marked `(tentative)` |
| Release dates | all eight kept character for character: 30 Nov 2026, 31 Dec 2026, 31 Jan 2027, 28 Feb 2027, 31 Mar 2027, 30 Apr 2027, 31 May 2027, 30 Jun 2027 |
| Title slide | kept, including `Henka Group, 28 October 2026` |
| Slides | 20: the 13 of version 2, the read-me at 2, the six new slides at 15 to 20 |
| Header lines 1 and 2 of §R8.1 | present as the first two body lines of slide 2 |
| Change-log row with D-RCV-60 and the tool line | present on slide 2 |
| Citations | 18 distinct CG/ASM citations, 0 unresolved |

Every ID, number, module code, week, forum, gate, role, dependency and date of version 2 is kept: the six modules and
their owners on slide 3, the eight releases and their themes on slide 4, the 67 stories and 374 points of E1 and the 32
stories and 199 points of E2 on slide 5, the five ways of working on slide 6, the eleven forums on slide 7, the six
gates on slide 8, the seven decision steps and three escalation lines on slide 9, the five roles and four weeks of the
first month on slides 10 and 11, the twelve first items with their modules, points and dependencies on slide 12, and the
twelve documents on slide 13.

**One source change beyond the page number.** Rule 10 of the run requires every release date to be marked tentative, so
the header cell of the release column on the release slide reads `Release (tentative)`. The eight dates themselves are
unchanged. No other source cell changed.

## 3. What version 3 adds (slides 15 to 20)

1. **Day-1 work by team type (15).** Five rows and a total: 846 TechX (CON 288, APP 418, ITG 140), 11 ACE team (DB),
   18 SCB IT infrastructure (INF), 57 DevOps team (OPS) and 7 QA team (ITG), 939 of the 1034 stories of the plan. The
   note gives the Day-1 rule and the suggested-only phrase (ASM-D2-TSP-4, ASM-D2-TSP-5).
2. **Contract first: 288 contract stories, all Day 1 (16).** The five contract groups with their counts and the service
   epics behind them, read from the same list: CG-W0 17, CG-W1 44, CG-W2 64, CG-W3 71 and CG-W4 92.
3. **The platform work that gives every team type a Day 1 (17).** Ten Day-1 platform and harness stories with title,
   work type, team type and epic: N001-CON, N009-CON, N010-CON, N011-DB, NF06-DB, N002-INF, N003-INF, N004-OPS,
   N005-OPS and W1J01-ITG.
4. **What each team type pulls first (18).** One row per team type with four or six named Day-1 stories and a short
   label for each, taken from the first rows of the same list.
5. **How a team uses this pack (19).** Six steps: find the team type, pull a contract story, build against the fake,
   wait only for an H dependency, keep I dependencies on integration stories, read Ready to start.
6. **What is still open (20).** One row per gap, with its CG and ASM row, the open point, the owner role and the
   proposed reading.

## 4. Owners

Every owner is a team type of Rules §R5.3 with the fixed phrase (`TechX`, `ACE team`, `SCB IT infrastructure`,
`DevOps team`, `QA team`; suggestion only, any team may pick up this story) and every service or platform owner is a
code of the Microservice Ownership Map v1 (`P1` to `P10`, `S1` to `S9`, `RWB-PLT-LIB`, `RWB-PLT-WF`, `RWB-PLT-TPL`,
`RWB-PLT-EDGE`, `RWB-PLT-EVT`, `RWB-PLT-DB`, `RWB-PLT-OBS`, `RWB-ITG-W1`). No owner is a person and no name appears
anywhere; the v2 person name in the document properties was replaced.

## 5. Registers

- Gap rows: **8**, `CG-D2-TSP-1` to `CG-D2-TSP-8`: 3 Conflict, 1 Ambiguous and 4 Missing; 2 of severity P2 and 6 of
  P3; needed by wave 0 (4 rows) and wave 1 (4 rows).
- Assumption rows: **10**, `ASM-D2-TSP-1` to `ASM-D2-TSP-10`: 8 High and 2 Medium.
- Eight of the ten assumptions answer a gap and each of the eight gaps names its assumption; ASM-9 (Draft status) and
  ASM-10 (tentative dates) carry no gap.
- Every CG and ASM citation in the deck resolves to a row: 18 distinct citations, none orphaned, and every row is cited.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-TSP --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

Also run by hand: C01 (no baseline file changed), C14 (header lines), C17 (every register row has its keys and no
citation is orphaned) and C20 (tool line in every edit log). `verify.py` reports PASS on its ten rules: 20 slides,
355 of 355 source lines kept, source slides identical at positions 3 to 14 apart from the page number and the
release-column mark, the release column marked tentative with the eight dates intact, the two header lines first on the
read-me slide, the D-RCV-60 change-log row, page number equal to position, no table touching its note and no shape
overlapping another, and 18 of 18 citations resolved. A PDF render of all 20 slides was read page by page.

## 7. Status and boundaries

The pack is issued in **Draft**: no approval is recorded for this run (ASM-D2-TSP-9). Release dates are unchanged and
tentative (ASM-D2-TSP-10, DL48). No later lifecycle stage was started. No issue tracker, wiki, repository, design tool
or web call was made, and no commit was created. The v2 deck and the other documents of folder 12 were not touched.

## 8. Failures

None after the fixes. Two build iterations were needed before the render was clean: the read-me slide was first placed
by moving the last slide rather than itself, and the first table heights were too small for the renderer, which pushed
two tables into their notes. Both were fixed in `build.py` and confirmed by `verify.py` and the PDF render.
