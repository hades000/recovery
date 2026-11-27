# Build-readiness review (script) — RWB-P3-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2007-APP (RWB P3 E2007 APP Booking confirmation from the ALS load v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 24 (6 P1). AC review rows: 1. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'TC-E2-007-10', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 12 rules are covered by no criterion and no test case: BR10, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 2 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 11 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-4070, CG-ALL-4071 |
| 8 | Contract | Fail | PATCH `/tasks/{taskId}` has no idempotency key; detcheck: P1 GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 409 task already completed; 503 store down; P2 Payload of rwb.case.CaseStateChanged.v1 differs from Kafka Catalog v1 (+4 more) | CG-ALL-4052, CG-ALL-4053, CG-ALL-4054, CG-ALL-4056, CG-ALL-4057, CG-ALL-4058, CG-ALL-4059, CG-ALL-4060 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-4061, CG-ALL-4062 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no error, no access state in the story; P3 SCR-14 has no error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-4072, CG-ALL-4073, CG-ALL-4074 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4066 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-007-11; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-4063, CG-ALL-4064, CG-ALL-4065 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 10 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-4055 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4052 | GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-4053 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4055 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-4057 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4067 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4068 | Java package th.co.scb.ace.workbench.recovery.case.bookingconfirmation uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4054 | HTTP errors with no message ID: 409 task already completed; 503 store down | X5 | Missing | Business analyst |
| CG-ALL-4056 | Payload of rwb.case.CaseStateChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4058 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-4059 | Activity BookingConfirmation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4060 | Activity raiseTask is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4062 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-4063 | Test cases not in Test Cases v8: TC-E2-007-11 | X9 | Missing | QA |
| CG-ALL-4066 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-4070 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4061 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-4064 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-4065 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4069 | Flyway file V2007_1__booking_confirmation.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4071 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-4072 | SCR-01 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4073 | SCR-14 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4074 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4075 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X9: A role without Case record R reads the case or its tasks (covered by 'TC-E2-007-10' only) | Not specified in the source documents | |
| AC11 | §8 BR10, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
