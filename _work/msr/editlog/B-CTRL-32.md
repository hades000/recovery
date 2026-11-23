# Edit log - WP B-CTRL-32 (Recovery Workbench Controls Catalog next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-CTRL-32. Fanout: 0.

## Files written

- `10 Policy, controls and compliance/Recovery Workbench Controls Catalog v4.xlsx`
- `_work/msr/docs/B-CTRL-32/ownership_dump.json`
- `_work/msr/docs/B-CTRL-32/ownership_text.txt`
- `_work/msr/docs/B-CTRL-32/build_v4.py`
- `_work/msr/docs/B-CTRL-32/write_register_rows.py`
- `_work/msr/gaps/B-CTRL-32.jsonl`
- `_work/msr/assumptions/B-CTRL-32.jsonl`
- `_work/msr/editlog/B-CTRL-32.md`

Scratch only under `_work/msr/docs/B-CTRL-32/`: the Ownership Map dump used to read every owner, the
builder script and the register-row script. The source text of v3 used for reading came from the
sanctioned conversion command, written to `_work/msr/extract/B-CTRL-32/`; the source workbook was never
edited.

## What was done

`10 Policy, controls and compliance/Recovery Workbench Controls Catalog v3.xlsx` was copied to the next
version with `compat/office_write.py copy`, so the source is untouched, and the copy was then changed in
place with `openpyxl` in `build_v4.py`. Only the control owner service is new.

1. **Header and change log.** A new first sheet, Read me, opens with the two header lines of Template and
   Rules R8.1 and carries the metadata (document, version 4, date 22 November 2026, supersedes v3,
   decision D-RCV-60, tool, status Draft) plus the change-log row
   `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
2. **Controls sheet.** Rows 1 and 2 (title and the 44-control description) are kept. Row 3 was blank and
   now carries the version line. Rows 5 to 48 keep columns A to N character for character: ID, L2,
   process, check, type, how, performed by, evidence, how it is tested, frequency, rules, obligations,
   audit finding and first release. Two columns are added at the right: O Owner service (one primary
   owner per control) and P Owner basis (the table, endpoint, event, workflow or job that fixes the owner,
   and the second owner where the check spans two services).
3. **Summary sheets.** By type and By release are unchanged, cell for cell (44 controls; 13 detective and
   31 preventive; E1 10, E2 12, E3 7, E4 2, E5 4, E6 4, E7 3, E8 2). Key is unchanged.
4. **By owner service (new).** The 16 services that own at least one control, with the service name, the
   delivery wave of the Ownership Map v1, the control count and the control IDs; total 44. A note records
   that P2 rwb-integration, S1 rwb-valuation and P10 rwb-agent own no control, and that S1 owns the
   valuation record CTL-27 checks.
5. **Realignment changes (new).** Ten rows, each change with its where, the v3 state, the v4 state, the
   decision and the basis.
6. **Workbook properties.** Creator and last modified by were person labels in v3; both are set to
   Henka Group, and title/subject/description carry version 4, D-RCV-60 and the tool line. No person name
   remains in the workbook.

## Owner service

Every owner comes from the Ownership Map v1 and the Architecture v5 extract: P1 3 controls, P3 4, P4 4,
P5 2, P6 4, P7 4, P8 2, P9 1, S2 4, S3 1, S4 1, S5 5, S6 2, S7 2, S8 2, S9 3. No control is added,
retired, renumbered or reworded; no date is added or changed.

## Gaps and assumptions

- Gap rows written: 7 (`GAP-0170` to `GAP-0176`).
- Assumption rows written: 7 (`ASM-0254` to `ASM-0260`).
- Subjects: owner service not stated in v3; CTL-36 first release E5 against owner service S9 wave 4;
  five controls whose check spans two services; CTL-39 conduct sample with no ownership row; monolith
  component and message names kept in the control text; no approval recorded; no calendar release date.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-CTRL-32 --quick` was run after the
files were written: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS (0 failures).

Also checked directly: C01 PASS (no source file changed), C14 PASS (header lines), C17 PASS (every gap and
assumption row has its required keys and every citation resolves), C20 PASS (tool line). C19 reports only
the outputs of other work packs that have not run yet; both B-CTRL-32 expected outputs exist.

A cell-by-cell comparison of v4 against v3 shows no difference in sheets Controls columns A to N (except
the previously blank row 3), By type, By release and Key. Workbook creator and last modified by were
person labels in v3; both are now Henka Group, and a scan of every cell finds no person name and no email
address.

## Notes

- The catalog states no calendar date; the first release is a business epic (E1 to E8) and is kept
  unchanged, so no release date is marked (tentative) because none is written.
- The v3 workbook records no approval, so v4 is Draft (ASM-0259).
- Row heights were raised only where the new Owner basis column needs the space; no cell value of v3
  changes.

