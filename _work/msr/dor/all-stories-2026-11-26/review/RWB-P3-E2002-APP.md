# Build-readiness review (script) — RWB-P3-E2002-APP ACE plan status on the case v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2002-APP (RWB P3 E2002 APP ACE plan status on the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 6, Fail 8. Detcheck rows: 25 (7 P1). AC review rows: 2. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 1 of 14 rules are covered by no criterion and no test case: BR12; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `break_count` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `prior_route` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-3963, CG-ALL-3964 |
| 8 | Contract | Fail | detcheck: P1 GET /cases/{caseId}/plan-status is not in rwb-case.yaml; P1 GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} is not published by rwb-decision; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 503 store down. The timer started by a route move is read with the existing `GET /cases/{caseId}/timers` operation of rwb-case (+5 more) | CG-ALL-3965, CG-ALL-3966, CG-ALL-3967, CG-ALL-3968, CG-ALL-3970, CG-ALL-3971, CG-ALL-3972, CG-ALL-3973, CG-ALL-3974 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 6 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3975 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-3984, CG-ALL-3985 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3980 |
| 12 | Test cases | Fail | AC9 has no test case in §16; AC10 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-002-11; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC9, AC10; P3 §18 test lists differ from RTM v7 | CG-ALL-3976, CG-ALL-3977, CG-ALL-3978, CG-ALL-3979 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3969 |
| 18 | Open decisions | Partial | open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL14 (assumptions: ASM-0189, ASM-5687); open decision DL21 (assumptions: none); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560); detcheck: P2 Open decision DL21 has no assumption | CG-ALL-3987 |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E2002-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3965 | GET /cases/{caseId}/plan-status is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3966 | GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-3967 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3969 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3971 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3981 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3982 | Java package th.co.scb.ace.workbench.recovery.case.planstatus uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3963 | Name `break_count` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3964 | Name `prior_route` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3968 | HTTP errors with no message ID: 503 store down. The timer started by a route move is read with the existing `GET /cases/{caseId}/timers` operation of rwb-case | X5 | Missing | Business analyst |
| CG-ALL-3970 | Payload of rwb.case.CaseStateChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3972 | Workflow ID form and start rule of DailyCaseRun are not stated | X6 | Missing | Solution architect |
| CG-ALL-3973 | Activity readPlanStatus is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3974 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3975 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3976 | Test cases not in Test Cases v8: TC-E2-002-11 | X9 | Missing | QA |
| CG-ALL-3978 | Criteria with no test case: AC9, AC10 | X9 | Missing | QA |
| CG-ALL-3980 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3987 | Open decision DL21 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3977 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3979 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3983 | Flyway file V2002_1__plan_status.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3984 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3985 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3986 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC9 | no test case in §16 |  |
| AC10 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
