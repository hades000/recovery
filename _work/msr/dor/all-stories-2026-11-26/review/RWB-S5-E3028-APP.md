# Build-readiness review (script) — RWB-S5-E3028-APP Set the start and floor price

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E3028-APP (RWB S5 E3028 APP Set the start and floor price v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E3-028 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 11, Fail 7. Detcheck rows: 21 (9 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E3-028-05', not by a criterion; exception X9 is covered by 'Section 17, BR4, BR5', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DIS-28' has no BR ID; rule row 'R-DIS-29' has no BR ID; rule row 'R-DIS-17' has no BR ID; 11 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 18 transitions; detcheck: P1 The story adds ROUTE_APPROVED_AUCTION to the closed list LOV-LISTING; P1 The story adds PRICE_PROPOSED to the closed list LOV-LISTING; P1 The story adds FLOOR_APPROVED to the closed list LOV-LISTING; P1 The story adds REAPPRAISAL_RECEIVED to the closed list LOV-LISTING (+1 more) | CG-ALL-9877, CG-ALL-9878, CG-ALL-9879, CG-ALL-9880, CG-ALL-9881 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-COL-028, DF-COL-042; §11 has 12 data rows; detcheck: P2 Name `asset_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `outlier_flag` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9882, CG-ALL-9883, CG-ALL-9884, CG-ALL-9893 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/valuation/v1; P1 Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog (+2 more) | CG-ALL-9885, CG-ALL-9886, CG-ALL-9887, CG-ALL-9888, CG-ALL-9889, CG-ALL-9890 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-23 has no empty, loading, error, no access state in the story; P3 SCR-24 has no empty, loading, error, no access state in the story | CG-ALL-9894, CG-ALL-9895, CG-ALL-9896 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-9892 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-028-01, TC-E3-028-02, TC-E3-028-03, TC-E3-028-04, TC-E3-028-05, TC-E3-028-06 | CG-ALL-9891 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'valuable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E3028-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_valuation | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9877 | The story adds ROUTE_APPROVED_AUCTION to the closed list LOV-LISTING | X1 | Conflict | Product owner |
| CG-ALL-9878 | The story adds PRICE_PROPOSED to the closed list LOV-LISTING | X1 | Conflict | Product owner |
| CG-ALL-9879 | The story adds FLOOR_APPROVED to the closed list LOV-LISTING | X1 | Conflict | Product owner |
| CG-ALL-9880 | The story adds REAPPRAISAL_RECEIVED to the closed list LOV-LISTING | X1 | Conflict | Product owner |
| CG-ALL-9881 | The story adds ASSET_HELD to the closed list LOV-LISTING | X1 | Conflict | Product owner |
| CG-ALL-9885 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-9886 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-9887 | No API Specification v5 yaml has the base of /api/recovery/valuation/v1 | X5 | Missing | Solution architect |
| CG-ALL-9888 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9882 | Name `asset_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9883 | Name `outlier_flag` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9884 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9889 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9890 | Activity setStartAndFloorPrice is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9891 | Test cases not in Test Cases v8: TC-E3-028-01, TC-E3-028-02, TC-E3-028-03, TC-E3-028-04, TC-E3-028-05, TC-E3-028-06 | X9 | Missing | QA |
| CG-ALL-9892 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9893 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9894 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9895 | SCR-23 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9896 | SCR-24 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9897 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: The role does not hold the Asset and disposal right of the operation (covered by 'TC-E3-028-05' only) | Not specified in the source documents | |
| AC6 | §5 X9: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 'Section 17, BR4, BR5' only) | Not specified in the source documents | |
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
