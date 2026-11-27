# Build-readiness review (script) — RWB-P5-E2030-APP Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E2030-APP (RWB P5 E2030 APP Legal document agent in shadow on Epic 1 data [E3c] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E2-030 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 4, Fail 7. Detcheck rows: 11 (4 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 7 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 5 of 7 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR5, BR7; §8 has 7 rules | — |
| 5 | State transitions | Fail | §9 has 3 transitions; detcheck: P1 The story adds MORTGAGE_CIVIL to the closed list LOV-ROUTE; P1 The story adds MORTGAGE_CIVIL to the closed list LOV-STAGE; P1 The story adds MORTGAGE_CIVIL to the closed list LOV-REVIEW | CG-ALL-6270, CG-ALL-6271, CG-ALL-6272 |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 5 data rows | — |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no Workbench identity; 404 no such case; P1 rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data | CG-ALL-6273, CG-ALL-6274 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-6278, CG-ALL-6279 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-P5-E2030-01, TC-P5-E2030-02; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-6275, CG-ALL-6276, CG-ALL-6277 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P5-E2030-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.2 has no owner or service column; §13 names other schemas: rwb_case, rwb_litigation | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6270 | The story adds MORTGAGE_CIVIL to the closed list LOV-ROUTE | X1 | Conflict | Product owner |
| CG-ALL-6271 | The story adds MORTGAGE_CIVIL to the closed list LOV-STAGE | X1 | Conflict | Product owner |
| CG-ALL-6272 | The story adds MORTGAGE_CIVIL to the closed list LOV-REVIEW | X1 | Conflict | Product owner |
| CG-ALL-6274 | rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6273 | HTTP errors with no message ID: 401 no Workbench identity; 404 no such case | X5 | Missing | Business analyst |
| CG-ALL-6275 | Test cases not in Test Cases v8: TC-P5-E2030-01, TC-P5-E2030-02 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6276 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6277 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6278 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6279 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6280 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR4, BR5, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
