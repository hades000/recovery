# Edit log — B-REQ-SPEC-28

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Work package: B-REQ-SPEC-28, Recovery Workbench Non Functional Specification, next version.
Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.
Agent: aisdlc-msr-worker. Fanout 0, no subagents used.

## Files written

- `03 Requirements and specifications/Recovery Workbench Non Functional Specification v4.docx`
- `_work/msr/docs/B-REQ-SPEC-28/Recovery Workbench Non Functional Specification v4.md`
- `_work/msr/docs/B-REQ-SPEC-28/template_v4.docx`
- `_work/msr/docs/B-REQ-SPEC-28/build_v4.py`
- `_work/msr/docs/B-REQ-SPEC-28/fix_template.py`
- `_work/msr/docs/B-REQ-SPEC-28/verify.py`
- `_work/msr/gaps/B-REQ-SPEC-28.jsonl`
- `_work/msr/assumptions/B-REQ-SPEC-28.jsonl`
- `_work/msr/editlog/B-REQ-SPEC-28.md`

No source file was edited. `03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx`
was read only; the built-in style names of a scratch copy were lower-cased so `compat/office_write.py md-docx` can resolve
them, and the v3 docx was then used as the template.

## What was done

1. Read Template and Rules sections R1, R3, R5, R8 and R9, the converted text of the v3 docx
   (`_work/msr/extract/Recovery Workbench Non Functional Specification v3.md`), `plan/ownership.json` and the
   Microservice Ownership Map v1, the Architecture v5 text extract (slides 8 to 11, 16, 20, 37 and 48), the Temporal and
   Drools Design text extract (slide 13), `plan/split_plan.json` (stats and legacy only) and `plan/ids.json`.
2. Built the full version 4 text in `_work/msr/docs/B-REQ-SPEC-28/… v4.md` with `build_v4.py`, which appends one owning
   service cell to every table row and inserts the realignment notes; every other line is the source line, unchanged.
   No new decision ID was needed: D-RCV-60, ADR-019, ADR-020 and DL44 to DL49 already cover the change.
3. The first two lines are the Template and Rules §R8.1 header. The change-log row is
   `4 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
4. Changes, all additive:
   - document control: Version 4, `Requirements | 80 (78 in version 3, plus NFR-079 and NFR-080)`, and rows for the
     decision, the owner of record (Microservice Ownership Map v1), the Draft status and the tool;
   - section 1: an owning service column for the ten areas and a new `Calls` row (one hop, 2 s call timeout);
   - section 2: an owning service column and the note on the three concurrency figures (GAP-1867);
   - section 3.1 to 3.12: an owning service column on every requirement table, from the Ownership Map v1;
   - section 3.2: the one-hop REST rule, the 2 s call timeout, the GET retry with jitter and the breaker and bulkhead
     (Architecture v5 slides 10 and 11; DP-11; ADR-020), plus NFR-079 and NFR-080;
   - section 3.3: only P1 rwb-source-data reads the 30 `recovery.v_ace_*` views;
   - section 3.4: the recovery point and recovery time objectives are not stated for 19 services
     (GAP-1863, GAP-1864);
   - section 3.5: the "weeks" versus "28 days" wording (GAP-1865);
   - section 3.7: the data lake copy of NFR-042 against Architecture v5 (GAP-1866);
   - section 4: the partner gateway of ADR-019 and the owning service, as two new rows;
   - section 5: an owning service column;
   - section 6: the realignment record (what changed, the realigned targets, the requirement index by owning service,
     the gap rows, the assumption rows and the sources read).
5. `verify.py` compares the new text with the v3 extract: every source paragraph and heading appears verbatim, and every
   source table row appears with its cells character for character before the appended owning service cell. Result:
   78 of 78 source requirements kept, 80 in version 4, no source line lost.
6. Nothing was invented: the 2 s timeout, the one-hop rule, the screen budget, the 30 views and the partner gateway are
   quoted from the Architecture v5 extract; every owner comes from the Ownership Map v1 through `plan/ownership.json`;
   the one requirement whose owner the map does not name carries the §R9 placeholder and GAP-1868.
7. Dates: the v3 date of 15 November 2026 is kept unchanged, the new change-log date is 22 November 2026, no release date
   is named by the document and no date is raised as a gap (ASM-3060).

## Registers

- Gap rows written: 6 (`GAP-1863` to `GAP-1868`).
- Assumption rows written: 9 (`ASM-3053` to `ASM-3061`).
- Numbering is left to step D1, as Template and Rules §R9 requires.
- Gaps cited in the document: `GAP-1863` and `-2` (sections 3.4 and 5, and the NFR-022/NFR-023 owning
  service cells), `-3` (section 3.5), `-4` (section 3.7), `-5` (section 2), `-6` (NFR-032). Assumptions cited:
  `ASM-3053` (Status row), `-2` and `-3` (NFR-022 and NFR-023), `-4` to `-9` in the section notes and 6.5.

## Notes and limits

- The lifecycle gate "requirements approval by the Product Owner" is not met in this run; the status stays Draft and
  `ASM-3053` records it.
- The docx is regenerated from the md; the v3 docx supplied page setup, fonts and section properties only. Its own body
  paragraphs were removed by `md-docx`, as the helper does for every template.

## Check result

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-SPEC-28 --quick` — C02 PASS, C03 PASS, C05 PASS,
C12 PASS, C13 PASS, C18 PASS.
