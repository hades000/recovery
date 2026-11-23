# Edit log B-DATA-18 — Source to Target Mapping next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Source to Target Mapping v4.xlsx` was read once, cell by cell, and never edited. It was copied to `v5` with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Source to Target Mapping v5.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 11 to 16 list what changed, rows 18 to 20 what did not, rows 22 to 25 the counts and rows 27 to 28 the open register rows.
- `Mapping`: two columns were appended at the end, `Target schema` (`rwb_<name>`) and `Owning service` (`P1` to `S7`). Columns A to N keep their letters, positions and values. Every value comes from the Ownership Map sheet Tables, row by row, per the WP instruction "Use the Ownership Map for every owner". 85 rows land in `rwb_source_data` (P1): 81 fields of ACE-side entities read through the 30 `recovery.v_ace_*` views (ADR-010, DP-05) plus the `interaction` and `dp_treatment` tables. The remaining 48 rows are the 14 owned Workbench tables: `rwb_litigation` 12, `rwb_asset` 7, `rwb_case` 6, `rwb_treatment` 6, `rwb_comms` 5, `rwb_writeoff` 5, `rwb_payment` 3, `rwb_access` 1, `rwb_debtsale` 1, `rwb_decision` 1, `rwb_document` 1.
- `ACE gaps`: the same two columns were appended. All 80 rows are ACE additions read through rwb-source-data, so the target schema is `rwb_source_data` and the owner is `P1`.
- `By source`: exactly one cell changed, the ACE table(s) cell of the `Aric via COLLINS` row, from `recovery` to `rwb_source_data.party_ext`. The 1/0/0/1 counts and the Total row (133 fields, 52 ACE reuse, 80 ACE new, 1 extension) are unchanged.
- `Mapping rules`: eight rules were appended after the ten v4 rules, which are unchanged word for word: target schema, owning service, ACE reads, ACE-side entities, extension fields, cross-service links, migration and load, status after realignment.
- Nothing else moved. `verify_v5.py` compares all four v4 sheets with v5 cell by cell: 1 changed cell in total, no other difference, no row or column lost, and no v4 sheet renamed.
- The source holds no date in any of its four sheets, so no release date is marked "(tentative)" and no date is changed. All 133 Field IDs and all 80 ACE gap Field IDs are copied character for character.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Source to Target Mapping v5.xlsx`
- `_work/msr/gaps/B-DATA-18.jsonl`
- `_work/msr/assumptions/B-DATA-18.jsonl`
- `_work/msr/editlog/B-DATA-18.md`
- `_work/msr/docs/B-DATA-18/build_notes.md`
- `_work/msr/docs/B-DATA-18/v4_dump.json`

Scratch scripts in `_work/msr/docs/B-DATA-18/`: `dump_v4.py`, `build_v5.py`, `verify_v5.py`, `gen_notes.py`, `probe_entities.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe_ownmap.py`, `probe_svc.py`, `probe_props.py`, `check_cites.py`, `show_v5.py`, `show_v5b.py`.

## Rows

- Candidate gap rows: 7, `GAP-0210` to `GAP-0216`, in `_work/msr/gaps/B-DATA-18.jsonl`, with every key of Template and Rules §R9. Severity: 2 at P2 (GAP-0210 and GAP-0211) and 5 at P3. Types: 1 Ambiguous at P2, 1 Missing at P2, 2 Outdated, 2 Missing and 1 Ambiguous at P3.
- Candidate assumption rows: 7, `ASM-0300` to `ASM-0306`, in `_work/msr/assumptions/B-DATA-18.jsonl`, one per gap, each with `gap` pointing at its CG row. Confidence High on 5 and Medium on 2.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Mapping: 133 field rows, 25 entities, 17 source systems, 12 target schemas, one per owning service (`rwb_source_data` alone holds 85 rows).
- ACE gaps: 80 rows, all with target schema `rwb_source_data` and owner `P1`.
- By source: 17 source rows and the Total row; 133 fields, 52 ACE reuse, 80 ACE new, 1 extension.
- Mapping rules: 10 v4 rules unchanged plus 8 new rules.
- Cells: 1 v4 cell changed out of the 4 sheets' full cell grid (4 sheets, 134 + 81 + 19 + 11 rows).

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-18 --quick`: C02, C03, C05, C12, C13 and C18 PASS, 0 findings, both before and after this log was written.
- C17 by hand over the same write set: every candidate gap and assumption row cited in `build_notes.md` has a row in its register file, and no other candidate row is cited.
- `verify_v5.py`: 1 changed v4 cell, 0 problems, all 133 Mapping rows carry a target schema and an owner, all 80 ACE gap rows carry both.

## Failures

None.
