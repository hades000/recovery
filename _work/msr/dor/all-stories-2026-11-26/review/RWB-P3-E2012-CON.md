# Build-readiness review (script) — RWB-P3-E2012-CON Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2012-CON (RWB P3 E2012 CON Manual transfer and reassignment screen with reason - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-012 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Pass (not applicable) 2, Partial 9, Fail 5. Detcheck rows: 14 (8 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'consumer of the case service (the gateway-bff composite route, the transfer screen and the test stories of this key)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 12 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 12 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows | — |
| 8 | Contract | Fail | POST `/cases/{caseId}/transfer` has no idempotency key; detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/deviation/v1/cases/{caseId}/deviations is not published by rwb-deviation; P1 GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision; P1 GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision (+3 more) | CG-ALL-4132, CG-ALL-4133, CG-ALL-4134, CG-ALL-4135, CG-ALL-4137, CG-ALL-4138, CG-ALL-4139 |
| 9 | Messages | Partial | §14 lists 11 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-4140 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-05 has no empty, loading, error, no access state in the story | CG-ALL-4145 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4143 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P3-E2012-CON-01, TC-P3-E2012-CON-02, TC-P3-E2012-CON-03, TC-P3-E2012-CON-04, TC-P3-E2012-CON-05, TC-P3-E2012-CON-06, TC-P3-E2012-CON-07, TC-P3-E2012-CON-08, TC-P3-E2012-CON-09, TC-P3-E2012-CON-10, TC-P3-E2012-CON-11, TC-P3-E2012-CON-12; P3 §18 test lists differ from RTM v7 | CG-ALL-4141, CG-ALL-4142 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 0 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-4136 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4132 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4133 | GET /api/recovery/deviation/v1/cases/{caseId}/deviations is not published by rwb-deviation | X5 | Missing | Solution architect |
| CG-ALL-4134 | GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-4135 | GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-4136 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-4137 | rwb-case.yaml holds transferReasonCode as a closed enum while the story reads LOV-TRANSFER-REASON as data | X5 | Conflict | Solution architect |
| CG-ALL-4139 | Workflow ManualTransferWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4144 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4138 | Payload of rwb.case.CaseTransferred.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4140 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-4143 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4141 | Test cases not in Test Cases v8: TC-P3-E2012-CON-01, TC-P3-E2012-CON-02, TC-P3-E2012-CON-03, TC-P3-E2012-CON-04, TC-P3-E2012-CON-05, TC-P3-E2012-CON-06, TC-P3-E2012-CON-07, TC-P3-E2012-CON-08, TC-P3-E2012-CON-09, TC-P3-E2012-CON-10, TC-P3-E2012-CON-11, TC-P3-E2012-CON-12 | X9 | Missing | QA |
| CG-ALL-4142 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4145 | SCR-05 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
