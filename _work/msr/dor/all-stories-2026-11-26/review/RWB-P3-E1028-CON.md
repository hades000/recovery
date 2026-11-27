# Build-readiness review (script) — RWB-P3-E1028-CON Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1028-CON (RWB P3 E1028 CON Service levels, timers, escalation and prescription dates - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-028 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 19 (7 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | 4 row(s) of §11 have no BR Field ID; §11 has 4 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3638 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/accounts/{accountId} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/calendar/holidays?from={from}&to={to} is not published by rwb-source-data; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 rwb-case.yaml holds timerType as a closed enum while the story reads LOV-TIMER as data (+7 more) | CG-ALL-3622, CG-ALL-3623, CG-ALL-3624, CG-ALL-3625, CG-ALL-3626, CG-ALL-3627, CG-ALL-3628, CG-ALL-3629, CG-ALL-3630, CG-ALL-3631, CG-ALL-3632 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P2 MSG-P3-030 is used with another meaning than the standard's; P2 MSG-P4-001 is used with another meaning than the standard's | CG-ALL-3633, CG-ALL-3634 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-3639, CG-ALL-3640 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P3-E1028-CON-01, TC-P3-E1028-CON-02, TC-P3-E1028-CON-03, TC-P3-E1028-CON-04, TC-P3-E1028-CON-05, TC-P3-E1028-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-3635, CG-ALL-3636 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3622 | GET /api/recovery/source-data/v1/accounts/{accountId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3623 | GET /api/recovery/source-data/v1/calendar/holidays?from={from}&to={to} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3624 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3625 | rwb-case.yaml holds timerType as a closed enum while the story reads LOV-TIMER as data | X5 | Conflict | Solution architect |
| CG-ALL-3626 | rwb-case.yaml holds status as a closed enum while the story reads LOV-TIMER-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3627 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3637 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3628 | rwb-case is not a consumer of rwb.case.CaseCreated.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3629 | rwb-case is not a consumer of rwb.case.CaseAllocated.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3630 | rwb-case is not a consumer of rwb.case.CaseTransferred.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3631 | rwb-case is not a consumer of rwb.case.CaseStateChanged.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3632 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3633 | MSG-P3-030 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3634 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3635 | Test cases not in Test Cases v8: TC-P3-E1028-CON-01, TC-P3-E1028-CON-02, TC-P3-E1028-CON-03, TC-P3-E1028-CON-04, TC-P3-E1028-CON-05, TC-P3-E1028-CON-06 | X9 | Missing | QA |
| CG-ALL-3636 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3638 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3639 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3640 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
