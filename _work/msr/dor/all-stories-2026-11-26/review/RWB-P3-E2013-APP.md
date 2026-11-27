# Build-readiness review (script) — RWB-P3-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2013-APP (RWB P3 E2013 APP Approval routing with the delegation of authority table v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 26 (12 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'case owner, and the service that holds the case' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'BR14', not by a criterion; exception X11 is covered by 'BR12', not by a criterion; exception X12 is covered by 'BR12', not by a criterion; exception X13 is covered by 'TC-E2-013-15', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 3 of 14 rules are covered by no criterion and no test case: BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 14 transitions; detcheck: P1 Status 'Waiting approval, while the item still waits' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'In progress, at the state the rule names' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'On hold, with `status_before_hold` = WAITING_APPROVAL' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Waiting approval, with the next approver' in the state table is not a value of LOV-CASE-STATUS (+1 more) | CG-ALL-4157, CG-ALL-4158, CG-ALL-4159, CG-ALL-4160, CG-ALL-4161 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 15 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data; P1 rwb-case.yaml holds elementType as a closed enum while the story reads LOV-ELEMENT as data; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-TASK-STATUS as data; P1 rwb-case.yaml holds timerType as a closed enum while the story reads LOV-TIMER as data (+4 more) | CG-ALL-4163, CG-ALL-4164, CG-ALL-4165, CG-ALL-4166, CG-ALL-4167, CG-ALL-4168, CG-ALL-4169, CG-ALL-4170 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-003; §14 lists 11 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-10 has no empty, loading, error, no access state in the story (+1 more) | CG-ALL-4177, CG-ALL-4178, CG-ALL-4179, CG-ALL-4180, CG-ALL-4181 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4173 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-4171, CG-ALL-4172 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 11 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-OVERRIDE-REASON is not in Reference Data v5 | CG-ALL-4162 |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4157 | Status 'Waiting approval, while the item still waits' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4158 | Status 'In progress, at the state the rule names' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4159 | Status 'On hold, with `status_before_hold` = WAITING_APPROVAL' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4160 | Status 'Waiting approval, with the next approver' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4161 | The story adds DECLINED_BY_APPROVER_SET to the closed list LOV-CASE-STATUS | X1 | Conflict | Product owner |
| CG-ALL-4163 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4164 | rwb-case.yaml holds elementType as a closed enum while the story reads LOV-ELEMENT as data | X5 | Conflict | Solution architect |
| CG-ALL-4165 | rwb-case.yaml holds status as a closed enum while the story reads LOV-TASK-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4166 | rwb-case.yaml holds timerType as a closed enum while the story reads LOV-TIMER as data | X5 | Conflict | Solution architect |
| CG-ALL-4168 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4174 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4175 | Java package th.co.scb.ace.workbench.recovery.case.approval uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4162 | List LOV-OVERRIDE-REASON is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-4167 | Payload of rwb.case.CaseStateChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4169 | rwb-case is not a consumer of rwb.decision.ApprovalRequested.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4170 | rwb-case is not a consumer of rwb.decision.ApprovalDecided.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4173 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4171 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-4172 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4176 | Flyway file V2013_1__case_approval_task.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4177 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4178 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4179 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4180 | SCR-10 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4181 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4182 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §5 X10: A request arrives for a closed case (covered by 'BR14' only) | Not specified in the source documents | |
| AC16 | §5 X11: A decided event arrives for a case with no open decision task (covered by 'BR12' only) | Not specified in the source documents | |
| AC17 | §5 X12: The local decision record cannot be written (covered by 'BR12' only) | Not specified in the source documents | |
| AC18 | §5 X13: A role without Case record R reads the case or the task list (covered by 'TC-E2-013-15' only) | Not specified in the source documents | |
| AC19 | §8 BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC20 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC21 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
