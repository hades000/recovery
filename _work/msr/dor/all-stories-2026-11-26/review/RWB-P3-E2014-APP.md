# Build-readiness review (script) — RWB-P3-E2014-APP Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2014-APP (RWB P3 E2014 APP Approval screen for D7.1 demand and recall notices v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-014 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 21 (12 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'litigation officer, legal counsel and head of litigation who decide a D7.1 demand or recall notice, and the case owner who must act on the outcome' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 3 of 11 rules are covered by no criterion and no test case: BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Fail | §11 has 22 data rows; detcheck: P1 Index column task.notice_ref is not a field of task in LDM v9 | CG-ALL-4183 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/case/v1/cases/{caseId} is not in rwb-case.yaml; P1 GET /api/recovery/case/v1/cases/{caseId}/timeline is not in rwb-case.yaml; P1 rwb-case.yaml holds reason as a closed enum while the story reads LOV-ASSIGN-REASON as data; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data (+5 more) | CG-ALL-4184, CG-ALL-4185, CG-ALL-4186, CG-ALL-4187, CG-ALL-4188, CG-ALL-4189, CG-ALL-4190, CG-ALL-4191, CG-ALL-4192 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-11 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story | CG-ALL-4199, CG-ALL-4200, CG-ALL-4201, CG-ALL-4202 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4195 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-4193, CG-ALL-4194 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E2014-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4183 | Index column task.notice_ref is not a field of task in LDM v9 | X3 | Conflict | Data |
| CG-ALL-4184 | GET /api/recovery/case/v1/cases/{caseId} is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-4185 | GET /api/recovery/case/v1/cases/{caseId}/timeline is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-4186 | rwb-case.yaml holds reason as a closed enum while the story reads LOV-ASSIGN-REASON as data | X5 | Conflict | Solution architect |
| CG-ALL-4187 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4188 | rwb-case.yaml holds elementType as a closed enum while the story reads LOV-ELEMENT as data | X5 | Conflict | Solution architect |
| CG-ALL-4189 | rwb-case.yaml holds status as a closed enum while the story reads LOV-TASK-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4190 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4191 | Event type rwb.decision.ApprovalRefused.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4192 | Event type rwb.decision.ApprovalReturned.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4196 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4197 | Java package th.co.scb.ace.workbench.recovery.case.noticefacts uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4195 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4193 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4194 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4198 | Flyway file V2014_1__case_notice_redress_task.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4199 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4200 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4201 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4202 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4203 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
