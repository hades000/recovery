# Edit log — B-REQ-BRD-PROG

Work package: B-REQ-BRD-PROG, Recovery Workbench Business Requirements Program, next version (BRD Builder).
Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md`
- `03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx`
- `_work/msr/docs/B-REQ-BRD-PROG/Recovery Workbench Business Requirements Program v5.md`
- `_work/msr/docs/B-REQ-BRD-PROG/template_v5.docx`
- `_work/msr/docs/B-REQ-BRD-PROG/build_v5.py`
- `_work/msr/docs/B-REQ-BRD-PROG/fix_template.py`
- `_work/msr/gaps/B-REQ-BRD-PROG.jsonl`
- `_work/msr/assumptions/B-REQ-BRD-PROG.jsonl`
- `_work/msr/editlog/B-REQ-BRD-PROG.md`

No source file was edited. `03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx` was read only, and copied to the scratch folder as the docx template.

## What changed from version 4

1. Header lines from Template and Rules §R8.1 added as the first two lines, and a change-log row
   `5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
2. Document control: Version 5, Date 22 November 2026, a Tool row, a `Change (version 5)` row, and a
   two-row change log that keeps the version 4 row. The version 4 Change text is kept word for word.
3. Section 7: the rows `Built on ACE`, `Modular monolith` and `Programmatic workflow` restated as
   superseded by D-RCV-60 with ADR-013, ADR-014 and ADR-016. Every other constraint row is unchanged.
4. Section 8: each release date keeps its value and gains `(tentative)` (U7, DL48). The phrase
   `30 November release` in section 7 gains `(tentative)`.
5. Section 9: the four owner cells that named persons (DL06, DL12, DL13, DL20) replaced by the §R9
   value placeholder, citing the gap and assumption rows. The question and answer cells are unchanged.
6. New section 10 Delivery model: epic structure (7 platform, 19 service, 5 integration), the 19
   service epics with module, schema and wave from the Ownership Map, waves and releases, the
   contract-first build rules with ADR-013 to ADR-022, and the ownership of the shared items.
7. New section 11: business requirement to service epic to business epic trace table. 38 rows,
   231 requirements, total checked. Plus the non-functional position and the P8/P9/P10 note.
8. New section 12: the 8 gap rows and 14 assumption rows raised by this version.

Checked mechanically: the 231 requirement rows of section 5 and the 78 non-functional requirement rows
of section 6 are character-for-character identical to version 4, in the same order. The only 19 source
lines that do not reappear verbatim are the version and date rows, the three restated constraints, the
eight release-date rows, the ACE team dependency row and the four owner cells.

## Registers

- Gap rows written: 8 (`GAP-1491` to `GAP-1498`).
- Assumption rows written: 14 (`ASM-2603` to `ASM-2616`).
- Numbering is left to step D1, as Template and Rules §R9 requires.

## Notes and limits

- The docx was produced with `compat/office_write.py md-docx` against the version 4 docx as template.
  That template stores its built-in styles under display names (`Heading 1`), which python-docx cannot
  resolve, so `fix_template.py` first made a scratch copy with the built-in style names lower-cased.
  Page setup, fonts and section properties are the source's; the source file is untouched.
- The lifecycle gate "requirements approval by the Product Owner" is not met in this run. Status stays
  Draft and `ASM-2603` records it.
- `requirement/Traceability_Matrix.md` is not written, because this work package does not list it under
  "Write only". The BR to service epic to business epic trace is in section 11 of the document instead.
- Attachments are not made inline in this document: the epic BRDs (Epic 1, Epic 2, Epics 3 to 8) are
  separate families with their own work packages.
