# Build-readiness review (script) — RWB-P8-E4046-APP Post a settlement booking to ALS

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E4046-APP (RWB P8 E4046 APP Post a settlement booking to ALS v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E4-046 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 11, Fail 7. Detcheck rows: 19 (7 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'Credit Administration officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-046-01', not by a criterion; exception X3 is covered by 'TC-E4-046-01', not by a criterion; exception X4 is covered by 'TC-E4-046-01', not by a criterion; exception X5 is covered by 'TC-E4-046-01', not by a criterion; exception X6 is covered by 'TC-E4-046-01', not by a criterion; exception X7 is covered by 'TC-E4-046-01', not by a criterion; exception X8 is covered by 'Section 17, BR5, BR7', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-P8-006-1' has no BR ID; rule row 'BR-P8-006' has no BR ID; 11 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7685, CG-ALL-7700 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/treatment/v1; P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/integration/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1 (+5 more) | CG-ALL-7686, CG-ALL-7687, CG-ALL-7688, CG-ALL-7689, CG-ALL-7691, CG-ALL-7692, CG-ALL-7693, CG-ALL-7694, CG-ALL-7695 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P2-001; §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-7696 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-7701, CG-ALL-7702 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7699 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-046-01, TC-E4-046-02, TC-E4-046-03, TC-E4-046-04; P3 Test cases listed for criteria this story does not own | CG-ALL-7697, CG-ALL-7698 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 2 dependencies named; detcheck: P1 Story RWB-P8-E4046-CON named as a dependency does not exist | CG-ALL-7690 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column; §13 names other schemas: rwb_case, rwb_decision, rwb_integration, rwb_treatment | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7686 | No API Specification v5 yaml has the base of /api/recovery/treatment/v1 | X5 | Missing | Solution architect |
| CG-ALL-7687 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-7688 | No API Specification v5 yaml has the base of /api/recovery/integration/v1 | X5 | Missing | Solution architect |
| CG-ALL-7689 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-7690 | Story RWB-P8-E4046-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7691 | rwb.payment.TreatmentBooked.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, with its `.retry` and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-7692 | Workflow SettlementBookingWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7685 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7693 | Activity postBooking is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7694 | Activity readBackBooking is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7695 | Activity deliverFile(manifest) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7697 | Test cases not in Test Cases v8: TC-E4-046-01, TC-E4-046-02, TC-E4-046-03, TC-E4-046-04 | X9 | Missing | QA |
| CG-ALL-7699 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7696 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7698 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-7700 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7701 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7702 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7703 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The treatment is not an accepted settlement, or its state is not the one R-SET-10 allows (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC4 | §5 X3: The ACE data product is stale after a late or failed batch (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: The rwb-treatment, rwb-source-data, rwb-integration or rwb-case contract does not answer inside 2 s, or its breaker is o (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC6 | §5 X5: The outbound item reaches `EXCEPTION`, or the interface row is not in force (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC7 | §5 X6: The booked position or the settlement payment does not match the accepted terms (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC8 | §5 X7: The same `TreatmentApproved` or the same `Idempotency-Key` arrives twice (covered by 'TC-E4-046-01' only) | Not specified in the source documents | |
| AC9 | §5 X8: A component, a statement or a test reads a `v_ace_*` view, another `rwb_*` schema or a `recovery_*` table (covered by 'Section 17, BR5, BR7' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC12 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC13 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
