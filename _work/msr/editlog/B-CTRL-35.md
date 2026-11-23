# Edit log - WP B-CTRL-35 (Recovery Workbench Regulatory Requirements Map next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-CTRL-35. Fanout: 0.

## Files written

- `10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx`
- `_work/msr/docs/B-CTRL-35/build_v3.py`
- `_work/msr/docs/B-CTRL-35/verify_v3.py`
- `_work/msr/docs/B-CTRL-35/verify_readme.py`
- `_work/msr/docs/B-CTRL-35/controls_dump.json`
- `_work/msr/gaps/B-CTRL-35.jsonl`
- `_work/msr/assumptions/B-CTRL-35.jsonl`
- `_work/msr/editlog/B-CTRL-35.md`

Scratch only under `_work/msr/docs/B-CTRL-35/`: the builder, the two verification scripts and the dump of the 44 control rows (control, L2, first release, owner service) read from the Controls Catalog v4 so every owner could be traced to a control. The source workbook was never edited. Its text for reading came from the sanctioned conversion command into `_work/msr/extract/B-CTRL-35/`; that folder is read-only for this work pack and no source file is touched.

## What was done

`10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v2.xlsx` was copied to the next version with `compat/office_write.py copy`, so the v2 file is untouched, and the copy was changed in place with `openpyxl` in `build_v3.py`.

1. **Header and change log.** A new first sheet, Read me, opens with the two header lines of Template and Rules R8.1 and carries the document control block (document, version 3, date 22 November 2026, supersedes v2, decision D-RCV-60, tool, status Draft, scope, owner-service convention, sources read, dates, approval, notes) plus the change log. The change-log row reads `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`; the version 2 row states the R9 placeholder for its date because no sheet states one.
2. **Obligations sheet.** Rows 1 and 2 (title and the 32-obligation description) are kept, row 3 (blank in v2) now carries the version line, and columns A to H of rows 1 to 36 are unchanged cell for cell: ID, Source, Obligation, Process, Rule, Controls, Owner, Status. Two columns are added at the right: I Owner service and J Service basis. The basis names the control, table, endpoint, workflow or job that fixes each owner, with the delivery wave. The autofilter is widened from A4:H36 to A4:J36; the freeze stays at C5; rows are raised only where the new basis text needs the space.
3. **By source and By process.** Unchanged, cell for cell: 18 sources and 34 L2 processes.
4. **By service (new).** The 15 services that satisfy at least one obligation, with the service name, the delivery wave of the Ownership Map v1, the number of obligations that name the service, the obligation IDs, the number of obligations where it is the primary owner, and those IDs; 44 service pairs, 32 primary. A note records that P2 rwb-integration, P8 rwb-payment and P10 rwb-agent own no obligation, that P8 owns CTL-40 and CTL-41 which answer no obligation here, that P2 owns the outbound credit-bureau item REG-27 reports through, and that S1 rwb-valuation owns the valuation record CTL-27 checks.
5. **Realignment changes (new).** Eleven rows, each change with its where, the v2 state, the v3 state, the decision D-RCV-60 and the basis.
6. **Key.** The four rows of v2 are kept and two rows are added: Owner service and Wave. The autofilter moves from A4:C8 to A4:C10.
7. **Sheet order and properties.** Read me, Obligations, By source, By process, By service, Realignment changes, Key. Creator and last modified by were a person label in v2; both are now Henka Group, and title, subject and description carry version 3, D-RCV-60 and the tool line. A scan of every cell finds no person name and no email address.

## Owner service

Every owner is derived from the controls the Controls cell names, through the Controls Catalog v4 owner service and the Ownership Map v1: P1 2 obligations, P3 3, P4 4, P5 1, P6 9, P7 5, P9 3, S2 3, S3 2, S4 1, S5 5, S6 1, S7 1, S8 1, S9 3. Primary owners: P1 2, P3 3, P4 2, P6 8, P7 3, P9 1, S2 2, S3 2, S5 4, S6 1, S7 1, S8 1, S9 2. No obligation, control, ID, number, date or business owner is added, retired, renumbered or reworded; no date is added or changed.

## Gaps and assumptions

- Gap rows written: 8 (`GAP-0194` to `GAP-0201`).
- Assumption rows written: 8 (`ASM-0284` to `ASM-0291`).
- Subjects: no version date or approval in the source; the map names no service owner; the reporting and outbound leg of REG-15 and REG-27 is covered by no control; the REG-25 breach notification has no owning object; the map and the Controls Catalog name different controls for four obligations; two obligations rest on the conduct sample whose owner is itself an assumption; an obligation states no release or wave; the Owner column and the new Owner service column can be read as one owner.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-CTRL-35 --quick` was run after the files were written.

Also checked directly with `verify_v3.py` and `verify_readme.py`: a cell-by-cell comparison shows no difference against v2 in Obligations columns A to H (row 3 excepted, blank in v2), in By source, in By process, or in Key rows 1 to 8; the 32 REG ids, 56 control references, 18 sources and 34 L2 processes are unchanged; the By service counts sum to 44 pairs and 32 primaries; the workbook opens on Read me with the R8.1 header lines in rows 1 and 2.

## Notes

- The workbook states no release date, so nothing is marked (tentative). The policy effective date 1 July 2026 in REG-29, REG-31 and the Key is copied unchanged and is not a release date.
- The Thai regulation codes in REG-30, the 'Retention classes (DL26)' reference in REG-24 and every regulation label are copied character for character.
- Version 3 is Draft because no approval is recorded (ASM-0284).

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash
