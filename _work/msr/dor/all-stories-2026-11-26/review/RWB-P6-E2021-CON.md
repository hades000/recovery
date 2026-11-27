# Build-readiness review (script) — RWB-P6-E2021-CON Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E2021-CON (RWB P6 E2021 CON Letter dispatch loop with proof of delivery from WIN - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 17 (2 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 4 of 14 rules are covered by no criterion and no test case: BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 6 row(s) of §11 have no BR Field ID; §11 has 6 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-6570 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/deviation/v1/deviations?caseId={caseId} is not published by rwb-deviation; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Workflow ID form and start rule of NoticeDispatchWorkflow are not stated; P2 Activity conductCheck is not in Temporal Catalog v1 (+2 more) | CG-ALL-6558, CG-ALL-6559, CG-ALL-6560, CG-ALL-6561, CG-ALL-6562, CG-ALL-6563 |
| 9 | Messages | Partial | §14 lists 13 messages; detcheck: P2 MSG-P3-030 is used with another meaning than the standard's; P2 MSG-P6-005 is used with another meaning than the standard's; P2 MSG-P3-005 is used with another meaning than the standard's | CG-ALL-6564, CG-ALL-6565, CG-ALL-6566 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-6571, CG-ALL-6572, CG-ALL-6573 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 22 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P6-E2021-CON-01, TC-P6-E2021-CON-02, TC-P6-E2021-CON-03, TC-P6-E2021-CON-04, TC-P6-E2021-CON-05, TC-P6-E2021-CON-06, TC-P6-E2021-CON-07, TC-P6-E2021-CON-08; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-6567, CG-ALL-6568, CG-ALL-6569 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (22) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6558 | GET /api/recovery/deviation/v1/deviations?caseId={caseId} is not published by rwb-deviation | X5 | Missing | Solution architect |
| CG-ALL-6559 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6560 | Workflow ID form and start rule of NoticeDispatchWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-6561 | Activity conductCheck is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6562 | Activity generateLetter is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6563 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6564 | MSG-P3-030 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6565 | MSG-P6-005 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6566 | MSG-P3-005 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6567 | Test cases not in Test Cases v8: TC-P6-E2021-CON-01, TC-P6-E2021-CON-02, TC-P6-E2021-CON-03, TC-P6-E2021-CON-04, TC-P6-E2021-CON-05, TC-P6-E2021-CON-06, TC-P6-E2021-CON-07, TC-P6-E2021-CON-08 | X9 | Missing | QA |
| CG-ALL-6568 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-6569 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6570 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-6571 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6572 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6573 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6574 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §8 BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
