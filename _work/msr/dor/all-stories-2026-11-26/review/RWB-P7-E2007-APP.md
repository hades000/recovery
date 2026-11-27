# Build-readiness review (script) — RWB-P7-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2007-APP (RWB P7 E2007 APP Booking confirmation from the ALS load v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 22 (10 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT), a Credit Administration officer (RW-CREDITAD), a data steward (RW-DATASTEW) and the rwb-decision service that decides the match' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 1 of 12 rules are covered by no criterion and no test case: BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-ACC-009, DF-ACC-030, DF-ACC-031; §11 has 24 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /admin/jobs/{jobId}/rerun is not in rwb-decision.yaml; P1 GET /booking-decisions is not in rwb-decision.yaml; P1 GET /api/recovery/integration/v1/batches/{source}/{businessDate} is not published by rwb-integration; P1 GET /api/recovery/integration/v1/cases/{caseId}/accounts?businessDate= is not published by rwb-integration (+7 more) | CG-ALL-7093, CG-ALL-7094, CG-ALL-7095, CG-ALL-7096, CG-ALL-7097, CG-ALL-7098, CG-ALL-7099, CG-ALL-7101, CG-ALL-7102, CG-ALL-7103, CG-ALL-7104 |
| 9 | Messages | Partial | §14 lists 9 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4; P3 MSG-P2-006 text differs from the Error and Message Standard v4; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-7105, CG-ALL-7106, CG-ALL-7107, CG-ALL-7108 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-7112, CG-ALL-7113, CG-ALL-7114 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7111 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-007-11; P3 §18 test lists differ from RTM v7 | CG-ALL-7109, CG-ALL-7110 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7100 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7093 | POST /admin/jobs/{jobId}/rerun is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7094 | GET /booking-decisions is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7095 | GET /api/recovery/integration/v1/batches/{source}/{businessDate} is not published by rwb-integration | X5 | Missing | Solution architect |
| CG-ALL-7096 | GET /api/recovery/integration/v1/cases/{caseId}/accounts?businessDate= is not published by rwb-integration | X5 | Missing | Solution architect |
| CG-ALL-7097 | GET /api/recovery/treatment/v1/treatments?type=&state=APPROVED&booked=false is not published by rwb-treatment | X5 | Missing | Solution architect |
| CG-ALL-7098 | POST /api/recovery/treatment/v1/treatments/{treatmentId}/booking is not published by rwb-treatment | X5 | Missing | Solution architect |
| CG-ALL-7099 | POST /api/recovery/case/v1/cases/{caseId}/tasks is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7100 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7101 | Event type rwb.decision.BookingDecisionMade.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7102 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7103 | rwb-decision is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7104 | rwb-decision is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7106 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7108 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7109 | Test cases not in Test Cases v8: TC-E2-007-11 | X9 | Missing | QA |
| CG-ALL-7111 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7105 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7107 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7110 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7112 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7113 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7114 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
