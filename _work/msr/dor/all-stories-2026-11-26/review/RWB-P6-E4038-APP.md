# Build-readiness review (script) — RWB-P6-E4038-APP Raise a dispute in self-service

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E4038-APP (RWB P6 E4038 APP Raise a dispute in self-service v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E4-038 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 11 (3 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'customer (borrower) on LINE OA or HOME.SCB' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'TC-E4-038-03', not by a criterion; exception X8 is covered by 'TC-E4-038-03', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 10 of 14 rules are covered by no criterion and no test case: BR4, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 15 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `notice_dispute` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6702, CG-ALL-6703 |
| 8 | Contract | Fail | detcheck: P1 POST /notices/{noticeId}/disputes is not in rwb-comms.yaml; P1 GET /notices/{noticeId}/disputes is not in rwb-comms.yaml; P2 HTTP errors with no message ID: 401 no session; 404 the notice is absent or out of scope, or the data contract does not return the party; 409 the notice is not a sent notice of the case, or a dispute is already open against it; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-6704, CG-ALL-6705, CG-ALL-6706, CG-ALL-6707 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-33 has no empty, loading, error, no access state in the story | CG-ALL-6711 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6709 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-038-01, TC-E4-038-02, TC-E4-038-03, TC-E4-038-04 | CG-ALL-6708 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-P6-E4038-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_deviation | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6704 | POST /notices/{noticeId}/disputes is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6705 | GET /notices/{noticeId}/disputes is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6707 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6702 | Name `notice_dispute` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6703 | Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6706 | HTTP errors with no message ID: 401 no session; 404 the notice is absent or out of scope, or the data contract does not return the party; 409 the notice is not a sent notice of the case, or a dispute is already open against it | X5 | Missing | Business analyst |
| CG-ALL-6708 | Test cases not in Test Cases v8: TC-E4-038-01, TC-E4-038-02, TC-E4-038-03, TC-E4-038-04 | X9 | Missing | QA |
| CG-ALL-6709 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6710 | Flyway file V4038_1__notice_dispute.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6711 | SCR-33 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6712 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X1: The notice is outside the caller's scope or does not exist (covered by 'TC-E4-038-03' only) | Not specified in the source documents | |
| AC4 | §5 X8: A role without the Documents right (covered by 'TC-E4-038-03' only) | Not specified in the source documents | |
| AC5 | §8 BR4, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
