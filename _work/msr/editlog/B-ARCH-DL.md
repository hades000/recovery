# Edit log — WP B-ARCH-DL (Decision Log v-next)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx

- _work/msr/gaps/B-ARCH-DL.jsonl

- _work/msr/assumptions/B-ARCH-DL.jsonl

- _work/msr/editlog/B-ARCH-DL.md

Scratch files under `_work/msr/docs/B-ARCH-DL/` (build and verification only, not an output of the run):
`build_xlsx.py`, `verify_xlsx.py`, `diff_xlsx.py`, `inspect.py`.

## What was done

The source `01 Decisions and governance/Recovery Workbench Decision Log v10.xlsx` was never edited. It was
copied to v11 with `compat/office_write.py copy`, and only the copy was changed:

1. **Read me sheet added first.** Rows 1 and 2 are the header of Template and Rules §R8.1. Row 8 is the
   change-log row `v11, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
   Rows 12 to 16 list what changed and the sheet counts.
2. **Decisions taken.** D-RCV-60 and DL44 to DL49 are appended as rows 28 to 34, dated 22 November 2026, with
   the decision, the taker role and what it means for the build. The sheet holds 29 decisions, and the
   description line in A2 is updated from 22 to 29 for that reason only. IDs are those in `_work/msr/plan/ids.json`
   (`D-RCV-60`, `DL44` to `DL49`).
3. **D-RCV-36 marked amended at T1 and T2.** The Decision cell keeps every word of v10 and gains
   ` (T1 and T2 amended by D-RCV-60)`; the "What it means for the build" cell keeps every word of v10 and gains
   the amendment text, which is grounded in Architecture v5 slides 41 and 44 and plan DP-10. No other cell of the
   row changed. Recorded as GAP-0118 / ASM-0190.
4. **Owner labels.** Fifteen open-decision owner cells and twelve `By owner` rows named an individual. Each now
   carries the §R9 placeholder `Not specified in the source documents (GAP-0117; ASM-0189)`, with the
   role or organisation the same cell already stated kept after it (for example `… with the architecture team`,
   `Solution architect with …`). Counts, earliest dates and decision IDs are unchanged, so the sheet still reads
   31 owners and 41 open decisions. A note in A4 of both sheets says so.
5. **Release dates.** Four release references carry `(tentative)`: Epic 5 litigation, March 2027 (DL03); the Epic 1
   release on 29 November (DL34); the 30 November release (DL43, question and if-late cells). Dates a decision is
   needed by are unchanged and unmarked.
6. **Document properties.** Creator and last-modified-by of the copy were set to "SCB Collections and Recovery",
   because the v10 property block held a personal name, which root rule 4 forbids.

Every other cell of v10 is byte-identical in v11; this was verified cell by cell against the source
(`diff_xlsx.py`): 15 owner cells, 3 release-date cells, the D-RCV-36 cells, the Decisions taken count and the two
A4 notes are the only differences, plus the 7 appended rows and the new Read me sheet.

Owners of services, tables, endpoints, events, workflows and jobs quoted by the new rows are those of the
Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`.

## Registers

- Gap rows written: 3 candidate rows (`GAP-0117` to `GAP-0119`) in `_work/msr/gaps/B-ARCH-DL.jsonl`.
- Assumption rows written: 8 candidate rows (`ASM-0188` to `ASM-0195`) in
  `_work/msr/assumptions/B-ARCH-DL.jsonl`.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-DL --quick` — C02, C03, C05, C12, C13 and
C18 all PASS, 0 findings. Run twice, second run identical.

## Not done, by design

- No ADR, story, catalogue or register master file was touched; this work package writes the Decision Log only.
- No issue tracker, wiki, repository or web call was made; no commit was created.
- The six new decisions are not renumbered or re-dated later in the run; D1 merges the candidate register rows.
