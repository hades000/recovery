# Build-readiness review (script) — RWB-P2-E2007-OPS Booking confirmation from the ALS load - deployment

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2007-OPS (RWB P2 E2007 OPS Booking confirmation from the ALS load - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 21 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'platform engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 12 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3159, CG-ALL-3176 |
| 8 | Contract | Fail | detcheck: P2 rwb-integration is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P2 rwb-integration is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1; P1 Workflow BookingMatchWorkflow is not in Temporal Catalog v1; P2 Activity readBookedTerms is not in Temporal Catalog v1 (+5 more) | CG-ALL-3160, CG-ALL-3161, CG-ALL-3162, CG-ALL-3163, CG-ALL-3164, CG-ALL-3165, CG-ALL-3166, CG-ALL-3167, CG-ALL-3168 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3169, CG-ALL-3170, CG-ALL-3171 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-3177, CG-ALL-3178, CG-ALL-3179 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3174 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P2-E2007-OPS-01, TC-P2-E2007-OPS-02, TC-P2-E2007-OPS-03, TC-P2-E2007-OPS-04, TC-P2-E2007-OPS-05, TC-P2-E2007-OPS-06; P3 §18 test lists differ from RTM v7 | CG-ALL-3172, CG-ALL-3173 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E2007-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3162 | Workflow BookingMatchWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3159 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3160 | rwb-integration is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3161 | rwb-integration is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3163 | Activity readBookedTerms is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3164 | Activity listApprovedTreatments is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3165 | Activity evaluateBookingMatch is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3166 | Activity applyBookingOutcome is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3167 | Activity raiseBookingTasks is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3168 | Activity writeRunSummary is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3171 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3174 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3169 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3170 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3172 | Test cases not in Test Cases v8: TC-P2-E2007-OPS-01, TC-P2-E2007-OPS-02, TC-P2-E2007-OPS-03, TC-P2-E2007-OPS-04, TC-P2-E2007-OPS-05, TC-P2-E2007-OPS-06 | X9 | Missing | QA |
| CG-ALL-3173 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3175 | Flyway file V2007_1__booking_match.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3176 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3177 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3178 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3179 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
