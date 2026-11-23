# WP C2-RTM edit log (D-RCV-60)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Agent: aisdlc-traceability-manager
Run: C2-RTM, single agent, fanout 0

## Files written

- `09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx`
- `_work/msr/gaps/C2-RTM.jsonl`
- `_work/msr/assumptions/C2-RTM.jsonl`
- `_work/msr/docs/C2-RTM/RTM v7 realignment notes.md`

## Scratch files written (working area, not a deliverable)

- `_work/msr/docs/C2-RTM/build_rtm.py`
- `_work/msr/docs/C2-RTM/rtm_v6.json`
- `_work/msr/docs/C2-RTM/cov_v6.json`
- `_work/msr/docs/C2-RTM/req_story.json`
- `_work/msr/docs/C2-RTM/req_fr.json`

## What was done

1. The source matrix (v6) was copied to v7 with the compat office writer; no source file was edited.
2. RTM sheet: the section R8.1 header lines sit on rows 1 and 2; the v6 title, description and all 231 requirement rows are kept, and rows 7 and 8 carry the change-log row "v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash". Columns A to M keep the v6 values character for character (verified: 231 rows, 0 differences). Columns N to R are new: legacy keys, new story IDs, PRD FR IDs, the realigned owner, and the coverage and review flags.
3. Legacy keys come from the v6 Stories column; the new story IDs are the split_plan slices of those keys, and where no legacy key exists they are the stories whose section 18 names the requirement.
4. PRD FR IDs were read from the 20 PRD files (FR tables and the 11.2 requirement trace summary).
5. Owners were read for every row from the service whose PRD functional requirements carry the requirement, and from the Ownership Map primary of its legacy key where it has no FR (R3 default rulings).
6. Coverage sheet: the v6 block is kept unchanged and a realignment block is added below it, with the epic tally and 15 artifact checks.
7. Gap and assumption rows: candidate rows only, not numbered; step D1 numbers them.

## Counts

- Requirement rows: 231 (unchanged IDs, unchanged order)
- Rows with a legacy key: 134
- Rows with realigned story IDs: 220
- Orphaned requirements (no realigned story): 9
- Requirements with no PRD FR: 6, plus 1 retired by design and 2 withdrawn
- Owners that differ from the v6 Module value: 14
- Rows citing a retired legacy story: 5
- Gap rows (CG candidates): 8
- Assumption rows (ASM candidates): 8

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp C2-RTM --quick` : C02, C03, C05, C12, C13, C18 all PASS.
- No issue-tracker access, no external writes, no commits, no names of people.

## Not done, by design

- No PMO or approval workflow: every row is Draft (ASM-5620).
- No issue, branch, commit or pull request metadata: none exists in this run (GAP-3216; ASM-5619).
- The 9 orphaned requirements and the 6 requirements without a PRD FR are flagged, not invented into a story or an FR.
