# Build-readiness review (script) — RWB-P6-E2021-OPS Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E2021-OPS (RWB P6 E2021 OPS Letter dispatch loop with proof of delivery from WIN - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 7, Fail 5. Detcheck rows: 12 (0 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'platform engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 14 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-6582 |
| 8 | Contract | Partial | detcheck: P2 Workflow ID form and start rule of NoticeDispatchWorkflow are not stated; P2 Activity conductCheck is not in Temporal Catalog v1; P2 Activity recordDecision is not in Temporal Catalog v1; P2 Activity generateLetter is not in Temporal Catalog v1 | CG-ALL-6575, CG-ALL-6576, CG-ALL-6577, CG-ALL-6578 |
| 9 | Messages | Pass | §14 lists 9 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-6583, CG-ALL-6584, CG-ALL-6585 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 23 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P6-E2021-OPS-01, TC-P6-E2021-OPS-02, TC-P6-E2021-OPS-03, TC-P6-E2021-OPS-04, TC-P6-E2021-OPS-05, TC-P6-E2021-OPS-06, TC-P6-E2021-OPS-07, TC-P6-E2021-OPS-08, TC-P6-E2021-OPS-09; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-6579, CG-ALL-6580, CG-ALL-6581 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL35 (assumptions: ASM-0189, ASM-0377, ASM-2041, ASM-2051) | — |
| 19 | Test data | Pass | every test case in §16 names its data (23) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P6-E2021-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6575 | Workflow ID form and start rule of NoticeDispatchWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-6576 | Activity conductCheck is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6577 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6578 | Activity generateLetter is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6579 | Test cases not in Test Cases v8: TC-P6-E2021-OPS-01, TC-P6-E2021-OPS-02, TC-P6-E2021-OPS-03, TC-P6-E2021-OPS-04, TC-P6-E2021-OPS-05, TC-P6-E2021-OPS-06, TC-P6-E2021-OPS-07, TC-P6-E2021-OPS-08, TC-P6-E2021-OPS-09 | X9 | Missing | QA |
| CG-ALL-6580 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6581 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6582 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-6583 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6584 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6585 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6586 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
