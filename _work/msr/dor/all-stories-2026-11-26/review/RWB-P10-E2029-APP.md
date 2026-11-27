# Build-readiness review (script) — RWB-P10-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2029-APP (RWB P10 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-029 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 13 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'conduct and QA officer (RW-CONDUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'TC-E2-029-11', not by a criterion; §7 holds 10 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 6 of 13 rules are covered by no criterion and no test case: BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 10 transitions; detcheck: P1 Status 'ANY_STATE' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, Assigned, In progress, any Waiting' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-2714, CG-ALL-2715 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 12 roles | — |
| 7 | Data | Partial | §11 has 35 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-2722 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/deviation/v1/deviations?caseId= is not published by rwb-deviation; P2 HTTP errors with no message ID: 401 no session; P2 Workflow ID form and start rule of AgentRunWorkflow are not stated; P2 Activity ResolveScreeningMode is not in Temporal Catalog v1 | CG-ALL-2716, CG-ALL-2717, CG-ALL-2718, CG-ALL-2719 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-2720 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story; P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2723, CG-ALL-2724, CG-ALL-2725 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2721 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P10-E1062-APP); 12 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E2029-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1062-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2714 | Status 'ANY_STATE' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-2715 | Status 'New, Assigned, In progress, any Waiting' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-2716 | GET /api/recovery/deviation/v1/deviations?caseId= is not published by rwb-deviation | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2717 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-2718 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2719 | Activity ResolveScreeningMode is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2720 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2721 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2722 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2723 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2724 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2725 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2726 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X8: A role without Case record U confirms or rejects (covered by 'TC-E2-029-11' only) | Not specified in the source documents | |
| AC12 | §8 BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
