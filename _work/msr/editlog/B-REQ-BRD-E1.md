# Edit log — B-REQ-BRD-E1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Work package: B-REQ-BRD-E1, Recovery Workbench Business Requirements Epic 1, next version (BRD Builder).
Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.
Agent: aisdlc-brd-builder. Fanout 0, no subagents used.

## Files written

- `03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.md`
- `03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.docx`
- `_work/msr/docs/B-REQ-BRD-E1/Recovery Workbench Business Requirements Epic 1 v5.md`
- `_work/msr/docs/B-REQ-BRD-E1/template_v5.docx`
- `_work/msr/docs/B-REQ-BRD-E1/build_brd.py`
- `_work/msr/docs/B-REQ-BRD-E1/fix_template.py`
- `_work/msr/gaps/B-REQ-BRD-E1.jsonl`
- `_work/msr/assumptions/B-REQ-BRD-E1.jsonl`
- `_work/msr/editlog/B-REQ-BRD-E1.md`

No source file was edited. `03 Requirements and specifications/Recovery Workbench Business Requirements
Epic 1 v4.docx` was read only, and copied into the scratch folder as the docx template.

## What was done

1. Converted the source docx to text with `compat/convert_sources.py` into
   `_work/msr/extract/B-REQ-BRD-E1/` and confirmed it is byte-identical to the extract already in
   `_work/msr/extract/`. Sections 1 to 7 of version 5 are that text, copied line for line.
2. Read Template and Rules sections R1, R3, R5, R8 and R9, the Architecture v5 and Temporal and Drools
   text extracts, `plan/ownership.json`, the Ownership Map v1 workbook (9 sheets), `plan/split_plan.json`
   (`stats`, `legacy` and the slices needed for the epic of each key) and `plan/ids.json`. No new
   decision ID was needed: D-RCV-60, ADR-013 to ADR-023 and DL44 to DL49 already cover the realignment.
3. Wrote the next version in both formats. Header lines from R8.1 are the first two lines, and the
   change-log row is `5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
   DeepSeek v4.1 Flash`.
4. Document control: Version 5, Date 22 November 2026, Release `30 November 2026 (tentative)`, a
   two-row change log that keeps the version 4 row and its 15 November 2026 date.
5. New section 8 Delivery model: 19 service epics with service, scope and wave from the Ownership Map v1,
   the seven platform and five integration epics, waves 0 to 4 with every release date kept and marked
   tentative, contract-first delivery with ADR-013 to ADR-022, the six work types with soft team
   ownership, the five positions for Epic 1 requirements (kept, must change, retired, cancelled,
   removed), and the date rule.
6. New section 9: business requirement to service epic to business epic trace, one row per requirement
   key, 69 rows covering the 61 live and 8 removed keys, with the primary service epic, the service, the
   wave, the business epic and the delivery position.
7. Sections 1 to 7 keep every requirement key, priority, count, role and date. The only edits inside
   them are: the section 1 release sentence gains `(tentative)`, and the four section 7 owner cells that
   named people carry the R9 placeholder.

Checked mechanically: the 310 source lines of sections 1 to 7 reappear in version 5 in the same order;
the only differences are the `(tentative)` marker on the release sentence, the four owner cells and one
trailing blank line. The 69 requirement rows and the 77 program requirement rows are character for
character identical, and the counts of section 1 and section 2 were re-derived from the tables and agree
(61 at development detail, 51 Must, 75 program requirements met, 77 rows in section 4 of which 2 are
Removed).

## Registers

- Gap rows written: 6 (`GAP-1453` to `GAP-1458`).
  - 1 to 3: RWB-E1-014 retired by D-RCV-60, RWB-E1-029 and RWB-E1-048 already cancelled before this
    run, each still live in the source text (Conflict, P2).
  - 4: Epic 1 stories in P8, S5 and S8, whose Architecture v5 wave is 2 (Conflict, P2).
  - 5: section 3 headings name the ten P modules only, while three keys also carry S5, S8 and S9 stories
    (Outdated, P3).
  - 6: four section 7 owner cells named people and no role (Missing, P3).
- Assumption rows written: 12 (`ASM-2548` to `ASM-2559`).
- Numbering is left to step D1, as Template and Rules section R9 requires.

## Notes and limits

- The docx was produced with `compat/office_write.py md-docx` against the version 4 docx as template.
  That template stores its built-in styles under display names (`Heading 1`), which python-docx cannot
  resolve, so `fix_template.py` first made a scratch copy with the built-in style names lower-cased.
  Page setup, fonts and section properties are the source's; the source file is untouched.
- The lifecycle gate "requirements approval by the Product Owner" is not met in this run. The document
  stays Draft and `ASM-2548` records it.
- `requirement/Traceability_Matrix.md` is not written, because this work package does not list it under
  "Write only". The BR to service epic to business epic trace is section 9 of the document instead.
- The BR IDs of this epic are the existing RWB-E1-nnn and RWB-ACE-001 keys, so no BR-001 style series is
  introduced (`ASM-2549`).
- Story counts in section 9 come from the plan, not from the business, and are marked as such
  (`ASM-2553`).
- No issue-tracker, wiki, source-control, design-tool or web call was made, and no git command was run.
