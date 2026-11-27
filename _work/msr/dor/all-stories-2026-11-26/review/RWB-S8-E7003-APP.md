# Build-readiness review (script) — RWB-S8-E7003-APP Run X3 deceased customer end to end

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7003-APP (RWB S8 E7003 APP Run X3 deceased customer end to end v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 23 (9 P1). AC review rows: 0. Missing criteria: 15.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'hardship and vulnerability specialist' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E7-003-05', not by a criterion; exception X3 is covered by 'TC-E7-003-02', not by a criterion; exception X4 is covered by 'TC-E7-003-02', not by a criterion; exception X5 is covered by 'TC-E7-003-02', not by a criterion; exception X6 is covered by 'TC-E7-003-02', not by a criterion; exception X7 is covered by 'TC-E7-003-03', not by a criterion; exception X8 is covered by 'TC-E7-003-03', not by a criterion; exception X9 is covered by 'TC-E7-003-02', not by a criterion; exception X10 is covered by 's17, BR8, BR10', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S8-012-1' has no BR ID; rule row 'R-DEV-03' has no BR ID; rule row 'R-DEV-06' has no BR ID; rule row 'BR-S8-012' has no BR ID; rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-UNI-38' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; 10 of 19 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 19 rules | — |
| 5 | State transitions | Pass | §9 has 15 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11457, CG-ALL-11476 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1 (+11 more) | CG-ALL-11458, CG-ALL-11459, CG-ALL-11460, CG-ALL-11461, CG-ALL-11462, CG-ALL-11463, CG-ALL-11464, CG-ALL-11465, CG-ALL-11466, CG-ALL-11467, CG-ALL-11468, CG-ALL-11469 (+3) |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11473 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11477, CG-ALL-11478 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11475 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-003-01, TC-E7-003-02, TC-E7-003-03, TC-E7-003-04, TC-E7-003-05, TC-E7-003-06, TC-S8-E7003-APP-01 | CG-ALL-11474 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7003-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11458 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-11459 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-11460 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-11461 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-11462 | rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-11463 | rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data | X5 | Conflict | Solution architect |
| CG-ALL-11464 | rwb-deviation.yaml holds raisedBy as a closed enum while the story reads LOV-RAISED-BY as data | X5 | Conflict | Solution architect |
| CG-ALL-11465 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11466 | Workflow DeviationWorkflow task queue rwb-deviation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11457 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11467 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11468 | Activity raiseDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11469 | Activity routeToOwner is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11470 | Activity applyContactStop is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11471 | Activity openEstatePath is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11472 | Activity recordOutcome is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11474 | Test cases not in Test Cases v8: TC-E7-003-01, TC-E7-003-02, TC-E7-003-03, TC-E7-003-04, TC-E7-003-05, TC-E7-003-06, TC-S8-E7003-APP-01 | X9 | Missing | QA |
| CG-ALL-11475 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11473 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11476 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11477 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11478 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11479 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: The role does not hold the Case record right of the operation (covered by 'TC-E7-003-05' only) | Not specified in the source documents | |
| AC6 | §5 X3: A required element of the request is absent or invalid, or the code is not in `LOV-DEVIATION` (covered by 'TC-E7-003-02' only) | Not specified in the source documents | |
| AC7 | §5 X4: The case is unknown, out of scope, or closed (covered by 'TC-E7-003-02' only) | Not specified in the source documents | |
| AC8 | §5 X5: The ACE data product behind the customer is stale after a late or failed batch (covered by 'TC-E7-003-02' only) | Not specified in the source documents | |
| AC9 | §5 X6: X3 is already open on the case (covered by 'TC-E7-003-02' only) | Not specified in the source documents | |
| AC10 | §5 X7: The outcome names no next step, or the code has no owner (covered by 'TC-E7-003-03' only) | Not specified in the source documents | |
| AC11 | §5 X8: The claim approval is refused or is not taken before filing (covered by 'TC-E7-003-03' only) | Not specified in the source documents | |
| AC12 | §5 X9: rwb-case, rwb-source-data or rwb-access does not answer inside 2 s, or its breaker is open (covered by 'TC-E7-003-02' only) | Not specified in the source documents | |
| AC13 | §5 X10: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 's17, BR8, BR10' only) | Not specified in the source documents | |
| AC14 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
