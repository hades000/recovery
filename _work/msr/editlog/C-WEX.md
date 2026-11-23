# Edit log C-WEX — Worked Example next version

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date: 22 November 2026.

## Files written

- 04 User stories/Recovery Workbench User Story Worked Example v7.md
- _work/msr/gaps/C-WEX.jsonl
- _work/msr/assumptions/C-WEX.jsonl
- _work/msr/editlog/C-WEX.md

## What changed

The worked example of legacy story RWB-E1-020 (allocation and assignment engine) moves from the monolith template to the microservice story template of Template and Rules §R7, as the reference example of the run.

- Header of §R8.1 in the first two lines, the title line, the metadata table of §R7.1 with its 20 rows in order directly under the title, then the change-log row with D-RCV-60 and the tool line.
- As a worked example it adds, before section 1, the note that explains what the reader is looking at, the table of the seven stories of RWB-E1-020 with their lane and their Day-1 status, and one italic paragraph at the end of each section that says where the values came from in the §R7.3 order. Nothing is removed from the legacy content.
- The title line is `# <Story key> <Title>` with story key RWB-P3-E1020-APP, the app slice of the legacy key in rwb-case (wave 1, EP01, lane L-P3-F).
- All 19 sections are kept in their order and their content is kept: the story line, the business rationale, the 9 legacy flow steps, the legacy exception rows X1–X10, the INVEST check, the 13 acceptance criteria (12 scenarios in the block; AC10 is named as owned by RWB-P3-E1018-APP), business rules BR1–BR12, the state table, the authority table, the 29 data rows, the messages, the screens paragraph, the 15 test cases, the guardrails, the traceability table and the out-of-scope list.
- Every legacy identifier, number, date and message ID is copied character for character: RWB-E1-020, REQ-CWC-007/008/009/016, FEAT-CWC-07/08/09, DF-* and TC-E1-020-* IDs, MSG-P3-011/012/013, the queue codes, the rule IDs, the package versions, the cap 150 and the business date 2026-12-01. The release date is marked "(tentative)".
- Realignment changes only (§R7.3): Quartz JOB-03 becomes DailyCaseRun on the rwb-case Temporal queue; RuleEvaluator becomes local evaluation of packages ALLOCATION and ASSIGNMENT through the embedded Drools kit with a fetched, checksum-verified model (DP-04); the cross-module decision log writer becomes the local decision record plus `rwb.decision-record.v1` (DP-03); the recovery schema becomes `rwb_case` (DP-01); `/api/recovery/v1` becomes `/api/recovery/case/v1` (DP-13); the topic becomes `rwb.case.events.v1` with `rwb.case.<Event>.v1` names (DP-14); the Flyway sequence is per service (DP-15); screens are reached through gateway-bff (DP-19).
- Section 7: every `Scenario:` line carries its origin tag `(legacy RWB-E1-020 ACn)`, and each APP scenario adds a contract-mock Given for the rwb-decision dependency (class C).
- Section 12: the nine tables 12.1–12.9 replace the legacy prose contract blocks, with "None" where empty.
- Section 16: the Level column uses the fixed vocabulary; the 15 legacy TC IDs are kept.
- Section 18: the legacy criterion-to-story division and the seven-story slice family are added so the trace of a split story is readable from one place.
- Owners everywhere come from the Ownership Map v1: rwb-case (P3) owns the case, queue, queue_member, assignment and the parameter and reference tables; rwb-decision (P7) owns rule_row and the decision ledger; the outbox is a PLT library object in the service schema.
- New decisions use the IDs of `_work/msr/plan/ids.json` only; no new ADR or DL number is coined in this document.

## Gaps and assumptions

- Gap rows: 4 (GAP-3206 to GAP-3209).
- Assumption rows: 4 (ASM-5609 to ASM-5612).
- Confidences: ASM-5609 High, ASM-5610 Medium, ASM-5611 Medium, ASM-5612 High.
- The work package heading names "(E1-018)"; the source file and all its identifiers belong to RWB-E1-020, so the document keeps RWB-E1-020 (GAP-3206; ASM-5609).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-WEX --quick` — all pass, no findings:

| Check | Result | Findings |
|---|---|---|
| C02 story ID line and metadata rows | PASS | 0 |
| C03 the 19 section headings | PASS | 0 |
| C05 acceptance-criterion origin tags | PASS | 0 |
| C12 person names and emails | PASS | 0 |
| C13 issue-tracker references | PASS | 0 |
| C18 write scope and legacy files unchanged | PASS | 0 |

Run outside the quick set on the same four files: C14 (header lines) PASS 0, C15 (release dates) PASS 0, C17 (gap and assumption rows) PASS 0, C20 (tool attribution) PASS 0. C19 (planned outputs of every work package) has 77 findings, all of them missing edit logs or outputs of other work packages; none of them is C-WEX, and both planned outputs of this work package exist.

Document size: 54.8 KB, 598 lines, 19 sections, 12 tagged scenarios, 4 gap citations and 4 assumption citations. The scratch folder `_work/msr/docs/C-WEX/` was not needed, because the output is a Markdown file written directly.
