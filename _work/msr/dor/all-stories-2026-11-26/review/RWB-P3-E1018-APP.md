# Build-readiness review (script) — RWB-P3-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1018-APP (RWB P3 E1018 APP Case ID issuance and case record v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-018 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 7, Fail 10. Detcheck rows: 32 (14 P1). AC review rows: 4. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 7 Data; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 20 Reference data; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'product owner' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 3 of 14 rules are covered by no criterion and no test case: BR9, BR10, BR14; §8 has 14 rules; detcheck: P2 Rule ID EXCL-004 used in the criteria exists in no current source; P2 Rule ID EXCL-006 used in the criteria exists in no current source | CG-ALL-3440, CG-ALL-3441 |
| 5 | State transitions | Fail | §9 has 3 transitions; detcheck: P1 Status 'Active' in the state table is not a value of LOV-CASE-STATUS; P1 The story adds WAITING_COURT to the closed list LOV-CASE-STATUS | CG-ALL-3425, CG-ALL-3426 |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Fail | §11 has 8 data rows; detcheck: P1 Index column recovery_case.primary_customer_id is not a field of recovery_case in LDM v9; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3427, CG-ALL-3451, CG-ALL-3452 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P1 GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision (+6 more) | CG-ALL-3429, CG-ALL-3430, CG-ALL-3431, CG-ALL-3432, CG-ALL-3433, CG-ALL-3434, CG-ALL-3436, CG-ALL-3437, CG-ALL-3438, CG-ALL-3439 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3442, CG-ALL-3443 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no error, no access state in the story; P3 SCR-03 has no empty, error, no access state in the story | CG-ALL-3453, CG-ALL-3454 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3447 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-018-15, TC-E1-018-16; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3444, CG-ALL-3445, CG-ALL-3446 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 2 build dependencies are not done yet (RWB-P3-E1018-OPS, RWB-P3-E1073-APP); 15 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3435 |
| 18 | Open decisions | Partial | open decision DL15 (assumptions: ASM-5264); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption | CG-ALL-3456 |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Fail | detcheck: P1 Parameter case.entry.dpd is also written as case.entry.dpd_threshold | CG-ALL-3428 |
| 21 | Contract published | Fail | the contract story RWB-P3-E1018-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E1073-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 14 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3425 | Status 'Active' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3426 | The story adds WAITING_COURT to the closed list LOV-CASE-STATUS | X1 | Conflict | Product owner |
| CG-ALL-3427 | Index column recovery_case.primary_customer_id is not a field of recovery_case in LDM v9 | X3 | Conflict | Data |
| CG-ALL-3428 | Parameter case.entry.dpd is also written as case.entry.dpd_threshold | X4 | ID collision | Business analyst |
| CG-ALL-3429 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3430 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3431 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3432 | GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-3433 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3435 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3436 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3437 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3448 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3449 | Java package th.co.scb.ace.workbench.recovery.case.casecreation uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3434 | HTTP errors with no message ID: 503 store down | X5 | Missing | Business analyst |
| CG-ALL-3438 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3439 | Workflow ID form and start rule of DailyCaseRun are not stated | X6 | Missing | Solution architect |
| CG-ALL-3440 | Rule ID EXCL-004 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3441 | Rule ID EXCL-006 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3443 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3444 | Test cases not in Test Cases v8: TC-E1-018-15, TC-E1-018-16 | X9 | Missing | QA |
| CG-ALL-3447 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3451 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-3456 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3442 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3445 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3446 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3450 | Flyway file V1018_1__case_creation.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3452 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3453 | SCR-02 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3454 | SCR-03 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3455 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC3 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC7 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC12 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §8 BR9, BR10, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
