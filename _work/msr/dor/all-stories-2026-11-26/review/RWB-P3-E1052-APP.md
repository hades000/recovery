# Build-readiness review (script) — RWB-P3-E1052-APP Notice generation v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1052-APP (RWB P3 E1052 APP Notice generation v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-052 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 32 (11 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)**, and as the **rwb-case service** behind the case task' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 1 of 8 rules are covered by no criterion and no test case: BR7; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Fail | §11 has 32 data rows; detcheck: P1 Index column recovery_case.notice_ref is not a field of recovery_case in LDM v9; P2 Name `notice_state` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `notice_hold_reason` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `notice_template_code` is not a field or entity in LDM v9 or Data Classification v5 (+5 more) | CG-ALL-3794, CG-ALL-3795, CG-ALL-3796, CG-ALL-3797, CG-ALL-3798, CG-ALL-3799, CG-ALL-3800, CG-ALL-3801, CG-ALL-3802 |
| 8 | Contract | Fail | PATCH `/tasks/{taskId}` (API-P3-009) has no idempotency key; detcheck: P1 GET /me/tasks` (API-P3-008) is not in rwb-case.yaml; P1 PATCH /tasks/{taskId}` (API-P3-009) is not in rwb-case.yaml; P1 GET /cases/{caseId}` (API-P3-002) is not in rwb-case.yaml; P1 GET /cases/{caseId}/next-action` (API-P3-016) is not in rwb-case.yaml (+7 more) | CG-ALL-3803, CG-ALL-3804, CG-ALL-3805, CG-ALL-3806, CG-ALL-3807, CG-ALL-3808, CG-ALL-3809, CG-ALL-3810, CG-ALL-3811, CG-ALL-3812, CG-ALL-3813 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-001, MSG-P4-001; §14 lists 8 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-3814 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story | CG-ALL-3821, CG-ALL-3822, CG-ALL-3823, CG-ALL-3824 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-052-11; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-3815, CG-ALL-3816, CG-ALL-3817 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E1052-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_comms | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3794 | Index column recovery_case.notice_ref is not a field of recovery_case in LDM v9 | X3 | Conflict | Data |
| CG-ALL-3803 | GET /me/tasks` (API-P3-008) is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3804 | PATCH /tasks/{taskId}` (API-P3-009) is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3805 | GET /cases/{caseId}` (API-P3-002) is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3806 | GET /cases/{caseId}/next-action` (API-P3-016) is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3807 | POST /api/recovery/comms/v1/cases/{caseId}/notices` (API-P6-001) is not published by rwb-comms | X5 | Missing | Solution architect |
| CG-ALL-3808 | GET /api/recovery/comms/v1/notices/{noticeId}` (API-P6-002) is not published by rwb-comms | X5 | Missing | Solution architect |
| CG-ALL-3810 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3812 | Workflow Notify (workflow kit template) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3818 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3819 | Java package th.co.scb.ace.workbench.recovery.case.noticerequest uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3795 | Name `notice_state` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3796 | Name `notice_hold_reason` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3797 | Name `notice_template_code` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3798 | Name `notice_template_version` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3799 | Name `notice_document_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3800 | Name `notice_delivered_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3801 | Field IDs DF-LEG-015 to DF-LEG-034 are not all fields of notice in LDM v9 | X3 | Conflict | Data |
| CG-ALL-3802 | Field IDs DF-REF-045 to DF-REF-069 are not all fields of template in LDM v9 | X3 | Conflict | Data |
| CG-ALL-3809 | HTTP errors with no message ID: 409 the task is not in a state that may be completed; 503 a store that does not answer | X5 | Missing | Business analyst |
| CG-ALL-3811 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3813 | Activity RequestNotice is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3815 | Test cases not in Test Cases v8: TC-E1-052-11 | X9 | Missing | QA |

### R3.3 Minor (P3) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3814 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3816 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3817 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3820 | Flyway file V1052_1__notice_reference.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3821 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3822 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3823 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3824 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3825 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
