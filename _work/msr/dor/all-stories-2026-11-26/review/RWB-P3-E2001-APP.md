# Build-readiness review (script) — RWB-P3-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2001-APP (RWB P3 E2001 APP EFS hand-over with full history v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 5, Fail 8. Detcheck rows: 27 (6 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 10 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 4 of 12 rules are covered by no criterion and no test case: BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Fail | §9 has 2 transitions; detcheck: P1 Status 'New, Assigned, In progress or any Waiting' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'No case' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-3936, CG-ALL-3937 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 16 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 503 ledger or case store down. `GET /cases/{caseId}` and `GET /cases` exist from RWB-P3-E1018-APP and RWB-P3-E1002-APP and are unchanged; P2 Payload of rwb.case.CaseCreated.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 (+7 more) | CG-ALL-3938, CG-ALL-3939, CG-ALL-3940, CG-ALL-3941, CG-ALL-3942, CG-ALL-3943, CG-ALL-3944, CG-ALL-3945, CG-ALL-3946, CG-ALL-3947, CG-ALL-3948 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages; detcheck: P3 MSG-P2-006 text differs from the Error and Message Standard v4 | CG-ALL-3949 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, error, no access state in the story; P3 SCR-04 has no empty, error, no access state in the story; P3 SCR-45 has no empty, error, no access state in the story | CG-ALL-3957, CG-ALL-3958, CG-ALL-3959 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3953 |
| 12 | Test cases | Fail | AC10 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC10; P3 §18 test lists differ from RTM v7 | CG-ALL-3950, CG-ALL-3951, CG-ALL-3952 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption; P2 Open decision DL29 has no assumption | CG-ALL-3961, CG-ALL-3962 |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E2001-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3936 | Status 'New, Assigned, In progress or any Waiting' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3937 | Status 'No case' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3938 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3941 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3954 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3955 | Java package th.co.scb.ace.workbench.recovery.case.handover uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 13 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3939 | HTTP errors with no message ID: 503 ledger or case store down. `GET /cases/{caseId}` and `GET /cases` exist from RWB-P3-E1018-APP and RWB-P3-E1002-APP and are unchanged | X5 | Missing | Business analyst |
| CG-ALL-3940 | Payload of rwb.case.CaseCreated.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3942 | rwb-case is not a consumer of rwb.source-data.AceDataLate.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3943 | Two workflow ID forms for DailyCaseRun in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3944 | Activity readCandidates is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3945 | Activity readEfsHistory is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3946 | Activity CreateOrLinkCase is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3947 | Activity AppendEfsHistory is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3948 | Activity recordRunSummary is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3951 | Criteria with no test case: AC10 | X9 | Missing | QA |
| CG-ALL-3953 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3961 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |
| CG-ALL-3962 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3949 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3950 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3952 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3956 | Flyway file V2001_1__handover_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3957 | SCR-02 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3958 | SCR-04 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3959 | SCR-45 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3960 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC10 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
