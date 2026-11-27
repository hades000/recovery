# Build-readiness review (script) — RWB-P7-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2013-APP (RWB P7 E2013 APP Approval routing with the delegation of authority table v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 20 (7 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'approver, for example a product head (RW-PRODHEAD)' is in the roles table | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 14 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 7 of 18 rules are covered by no criterion and no test case: BR12, BR13, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 Status 'In progress, at the state the rule names' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Returned, with a task for the preparer' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Waiting approval, with the next approver' in the state table is not a value of LOV-CASE-STATUS; P1 The story adds ESCALATED to the closed list LOV-APPROVAL-STATUS | CG-ALL-7149, CG-ALL-7150, CG-ALL-7151, CG-ALL-7152 |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Partial | §11 has 26 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7165 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; P1 rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data; P1 rwb-decision.yaml holds status as a closed enum while the story reads LOV-APPROVAL-STATUS as data; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 (+5 more) | CG-ALL-7154, CG-ALL-7155, CG-ALL-7156, CG-ALL-7157, CG-ALL-7158, CG-ALL-7159, CG-ALL-7160, CG-ALL-7161, CG-ALL-7162 |
| 9 | Messages | Pass | §14 lists 12 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-10 has no empty, loading, error, no access state in the story; P3 SCR-11 has no empty, loading, error, no access state in the story | CG-ALL-7166, CG-ALL-7167 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7163 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P7-E2013-OPS); 15 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-OVERRIDE-REASON is not in Reference Data v5 | CG-ALL-7153 |
| 21 | Contract published | Fail | the contract story RWB-P7-E2013-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7149 | Status 'In progress, at the state the rule names' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-7150 | Status 'Returned, with a task for the preparer' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-7151 | Status 'Waiting approval, with the next approver' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-7152 | The story adds ESCALATED to the closed list LOV-APPROVAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-7155 | rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data | X5 | Conflict | Solution architect |
| CG-ALL-7156 | rwb-decision.yaml holds status as a closed enum while the story reads LOV-APPROVAL-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-7157 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7153 | List LOV-OVERRIDE-REASON is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-7154 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-7158 | rwb-decision is not a consumer of rwb.access.DoaLimitChanged.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7159 | Activity readDelegation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7160 | Activity routeApproval is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7161 | Activity recordOutcome is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7162 | Activity escalateApproval is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7163 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7164 | Flyway file V2013_1__approval.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7165 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7166 | SCR-10 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7167 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7168 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR12, BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC19 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
