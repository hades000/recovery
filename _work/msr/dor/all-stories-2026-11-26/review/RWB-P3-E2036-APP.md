# Build-readiness review (script) — RWB-P3-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2036-APP (RWB P3 E2036 APP Queue write interface for models and agents v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-036 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 21 (8 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 14 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 2 of 14 rules are covered by no criterion and no test case: BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 Status 'Assigned, In progress, Waiting customer, Waiting partner, Waiting approval' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Closed, refused (MSG-P3-005)' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'On hold, refused (MSG-P2-021)' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-4334, CG-ALL-4335, CG-ALL-4336, CG-ALL-4337 |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 22 data rows; detcheck: P2 Name `uk_assignment_open_case` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `permission_matrix` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_catalogue` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-4338, CG-ALL-4339, CG-ALL-4340 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 401 no valid session; P2 Payload of rwb.case.CaseAllocated.v1 differs from Kafka Catalog v1; P2 Payload of rwb.case.CaseTransferred.v1 differs from Kafka Catalog v1 (+1 more) | CG-ALL-4341, CG-ALL-4342, CG-ALL-4343, CG-ALL-4344, CG-ALL-4345 |
| 9 | Messages | Pass | §14 lists 11 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-4351, CG-ALL-4352, CG-ALL-4353 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4347 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-4346 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E2036-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4334 | Status 'Assigned, In progress, Waiting customer, Waiting partner, Waiting approval' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4335 | Status 'Closed, refused (MSG-P3-005)' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4336 | Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4337 | Status 'On hold, refused (MSG-P2-021)' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-4341 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4345 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4348 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4349 | Java package th.co.scb.ace.workbench.recovery.case.placement uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4338 | Name `uk_assignment_open_case` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4339 | Name `permission_matrix` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4340 | Name `interface_catalogue` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4342 | HTTP errors with no message ID: 401 no valid session | X5 | Missing | Business analyst |
| CG-ALL-4343 | Payload of rwb.case.CaseAllocated.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4344 | Payload of rwb.case.CaseTransferred.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4347 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4346 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4350 | Flyway file V2036_1__placement_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4351 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4352 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4353 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4354 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
