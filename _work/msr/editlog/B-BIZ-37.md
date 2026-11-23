# Edit log - B-BIZ-37

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
WP: B-BIZ-37 - Recovery Workbench Case and Workflow Model next version

## Files written

- `02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx`
- `_work/msr/docs/B-BIZ-37/source_dump.txt`
- `_work/msr/docs/B-BIZ-37/build_rows.py`
- `_work/msr/docs/B-BIZ-37/format_book.py`
- `_work/msr/docs/B-BIZ-37/write_jsonl.py`
- `_work/msr/docs/B-BIZ-37/readme.json`
- `_work/msr/docs/B-BIZ-37/workflow_model.json`
- `_work/msr/docs/B-BIZ-37/stage_ownership.json`
- `_work/msr/docs/B-BIZ-37/case_file_ownership.json`
- `_work/msr/docs/B-BIZ-37/change_log.json`
- `_work/msr/docs/B-BIZ-37/realignment_changes.json`
- `_work/msr/gaps/B-BIZ-37.jsonl`
- `_work/msr/assumptions/B-BIZ-37.jsonl`

## What was done

- Copied v5 to v6; every v5 sheet, ID, number and date is unchanged (verified cell for cell: Stages, Elements, Case status, Status transitions, Milestones, Tasks, Event listeners, Sentries, Case file).
- Added the sheets Read me, Workflow model (v5), Stage ownership (v5), Case file ownership (v5), Change log and Realignment changes.
- Workflow model: CaseWorkflow parent on P3 rwb-case with a child workflow per stage, all owners from the Microservice Ownership Map v1 (D-RCV-60).
- Read me carries the R8.1 header lines. Change log carries the row "v6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
- No release dates appear in the source, so no date needed "(tentative)".
- No person names, no email addresses and no issue-tracker references were written.

## Counts

- Gap rows (CG): 2 (GAP-0157, GAP-0158)
- Assumption rows (ASM): 2 (ASM-0241, ASM-0242)

## Check result

PASS - `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-BIZ-37 --quick`
C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
Report written by the check tool under `22 Microservice Realignment/checks/reports/`.
