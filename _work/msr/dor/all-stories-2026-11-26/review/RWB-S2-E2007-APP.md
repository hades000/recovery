# Build-readiness review (script) — RWB-S2-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2007-APP (RWB S2 E2007 APP Booking confirmation from the ALS load v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 24 (6 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)** working the restructure and settlement routes of the case' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'BR9', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Pass | §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-ACC-009, DF-ACC-030, DF-ACC-031; §11 has 17 data rows; detcheck: P2 Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_booked_date` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_booked_amount` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-8293, CG-ALL-8294, CG-ALL-8295, CG-ALL-8296, CG-ALL-8311, CG-ALL-8312 |
| 8 | Contract | Fail | detcheck: P1 GET The approved-not-booked list of a treatment type set and a business date; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml; P1 POST The mark-booked write: treatment ID, business date, booking reference, the account facts of the business date, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml; P1 POST The booking-difference write: treatment ID, business date, the differing terms with their approved and booked value, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 (+3 more) | CG-ALL-8297, CG-ALL-8298, CG-ALL-8299, CG-ALL-8301, CG-ALL-8302, CG-ALL-8303, CG-ALL-8304 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-009; §14 lists 8 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4; P3 MSG-P2-006 text differs from the Error and Message Standard v4 | CG-ALL-8305, CG-ALL-8306, CG-ALL-8307 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-8313, CG-ALL-8314, CG-ALL-8315 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8310 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 20 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-007-11, TC-S2-E2007-APP-01, TC-S2-E2007-APP-02, TC-S2-E2007-APP-03, TC-S2-E2007-APP-04, TC-S2-E2007-APP-05, TC-S2-E2007-APP-06, TC-S2-E2007-APP-07, TC-S2-E2007-APP-08, TC-S2-E2007-APP-09; P3 §18 test lists differ from RTM v7 | CG-ALL-8308, CG-ALL-8309 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-8300 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (20) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8297 | GET The approved-not-booked list of a treatment type set and a business date; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8298 | POST The mark-booked write: treatment ID, business date, booking reference, the account facts of the business date, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8299 | POST The booking-difference write: treatment ID, business date, the differing terms with their approved and booked value, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8300 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-8301 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-8302 | Workflow TreatmentWorkflow` (booking branch) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8293 | Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8294 | Name `settlement_booked_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8295 | Name `settlement_booked_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8296 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8303 | Activity evaluateBookingMatch is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8304 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8306 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8308 | Test cases not in Test Cases v8: TC-E2-007-11, TC-S2-E2007-APP-01, TC-S2-E2007-APP-02, TC-S2-E2007-APP-03, TC-S2-E2007-APP-04, TC-S2-E2007-APP-05, TC-S2-E2007-APP-06, TC-S2-E2007-APP-07, TC-S2-E2007-APP-08, TC-S2-E2007-APP-09 | X9 | Missing | QA |
| CG-ALL-8310 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-8311 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8305 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8307 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8309 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8312 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8313 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8314 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8315 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8316 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X9: A component, a statement or a test reaches a case, task, account or rule table, or an ACE view (covered by 'BR9' only) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
