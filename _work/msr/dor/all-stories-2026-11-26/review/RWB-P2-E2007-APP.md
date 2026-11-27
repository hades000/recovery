# Build-readiness review (script) — RWB-P2-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2007-APP (RWB P2 E2007 APP Booking confirmation from the ALS load v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 31 (3 P1). AC review rows: 3. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)' is in the roles table | — |
| 2 | Links | Pass | §18 has 1 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Cross-slice: RWB-P4-E2007-APP (TC-E2-007-10)', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 5 of 16 rules are covered by no criterion and no test case: BR12, BR13, BR14, BR15, BR16; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-ACC-009, DF-ACC-030, DF-ACC-031; §11 has 30 data rows; detcheck: P2 Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_booked_date` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_booked_amount` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-3107, CG-ALL-3108, CG-ALL-3109, CG-ALL-3110, CG-ALL-3132, CG-ALL-3133 |
| 8 | Contract | Fail | detcheck: P1 POST /admin/jobs/{jobId}/rerun is not in rwb-integration.yaml; P2 rwb-integration is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P2 rwb-integration is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1; P1 Workflow BookingMatchWorkflow is not in Temporal Catalog v1 (+6 more) | CG-ALL-3111, CG-ALL-3113, CG-ALL-3114, CG-ALL-3115, CG-ALL-3116, CG-ALL-3117, CG-ALL-3118, CG-ALL-3119, CG-ALL-3120, CG-ALL-3121 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-003; §14 lists 9 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4; P3 MSG-P2-006 text differs from the Error and Message Standard v4 (+1 more) | CG-ALL-3122, CG-ALL-3123, CG-ALL-3124, CG-ALL-3125, CG-ALL-3126 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-3134, CG-ALL-3135, CG-ALL-3136 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3130 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-007-11; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3127, CG-ALL-3128, CG-ALL-3129 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 2 build dependencies are not done yet (RWB-P2-E1007-APP, RWB-P2-E2007-OPS); 14 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3112 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E2007-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P2-E1007-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3111 | POST /admin/jobs/{jobId}/rerun is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3112 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3115 | Workflow BookingMatchWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 17 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3107 | Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3108 | Name `settlement_booked_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3109 | Name `settlement_booked_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3110 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3113 | rwb-integration is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3114 | rwb-integration is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3116 | Activity readBookedTerms is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3117 | Activity listApprovedTreatments is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3118 | Activity evaluateBookingMatch is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3119 | Activity applyBookingOutcome is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3120 | Activity raiseBookingTasks is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3121 | Activity writeRunSummary is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3124 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3126 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3127 | Test cases not in Test Cases v8: TC-E2-007-11 | X9 | Missing | QA |
| CG-ALL-3130 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3132 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3122 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3123 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3125 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3128 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3129 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3131 | Flyway file V2007_1__booking_match.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3133 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3134 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3135 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3136 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3137 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC3 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X8: A role without Platform administration U asks for a rerun (covered by 'Cross-slice: RWB-P4-E2007-APP (TC-E2-007-10)' only) | Not specified in the source documents | |
| AC11 | §8 BR12, BR13, BR14, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
