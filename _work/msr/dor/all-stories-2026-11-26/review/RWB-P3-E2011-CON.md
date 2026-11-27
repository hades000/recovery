# Build-readiness review (script) — RWB-P3-E2011-CON Queue view screens: my queue, team queues, filters and ageing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2011-CON (RWB P3 E2011 CON Queue view screens  my queue, team queues, filters and ageing - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 6, Fail 4. Detcheck rows: 11 (5 P1). AC review rows: 2. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-4111 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data; P1 rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data; P1 rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data (+1 more) | CG-ALL-4103, CG-ALL-4104, CG-ALL-4105, CG-ALL-4106, CG-ALL-4107 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no error, no access state in the story; P3 SCR-07 has no empty, error, no access state in the story | CG-ALL-4112, CG-ALL-4113 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P3-E2011-CON-01, TC-P3-E2011-CON-02, TC-P3-E2011-CON-03, TC-P3-E2011-CON-04, TC-P3-E2011-CON-05, TC-P3-E2011-CON-06, TC-P3-E2011-CON-07, TC-P3-E2011-CON-08, TC-P3-E2011-CON-09; P3 §18 test lists differ from RTM v7 | CG-ALL-4108, CG-ALL-4109 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4103 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4104 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4105 | rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data | X5 | Conflict | Solution architect |
| CG-ALL-4106 | rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data | X5 | Conflict | Solution architect |
| CG-ALL-4110 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4107 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4108 | Test cases not in Test Cases v8: TC-P3-E2011-CON-01, TC-P3-E2011-CON-02, TC-P3-E2011-CON-03, TC-P3-E2011-CON-04, TC-P3-E2011-CON-05, TC-P3-E2011-CON-06, TC-P3-E2011-CON-07, TC-P3-E2011-CON-08, TC-P3-E2011-CON-09 | X9 | Missing | QA |
| CG-ALL-4109 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4111 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-4112 | SCR-02 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4113 | SCR-07 has no empty, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | message MSG-P4-001 is not in §14 |  |
| AC7 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
