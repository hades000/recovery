# Build-readiness review (script) — RWB-S5-E4033-APP Rent a held asset to a third party

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E4033-APP (RWB S5 E4033 APP Rent a held asset to a third party v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E4-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 18 (6 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer (RW-SALEOFF)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-033-04', not by a criterion; exception X8 is covered by 'Section 17', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DIS-25' has no BR ID; 9 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 10 transitions; detcheck: P1 The story adds RENTAL_ACTIVE to the closed list LOV-HOLDING | CG-ALL-10246 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-COL-028, DF-COL-029, DF-COL-031, DF-COL-033, DF-COL-041; §11 has 12 data rows; detcheck: P2 Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly (+1 more) | CG-ALL-10247, CG-ALL-10248, CG-ALL-10249, CG-ALL-10259, CG-ALL-10260 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/payment/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/comms/v1; P1 Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog (+2 more) | CG-ALL-10250, CG-ALL-10251, CG-ALL-10252, CG-ALL-10253, CG-ALL-10254, CG-ALL-10255, CG-ALL-10256 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-10261, CG-ALL-10262 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10258 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-033-01, TC-E4-033-02, TC-E4-033-03, TC-E4-033-04, TC-E4-033-05 | CG-ALL-10257 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E4033-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10246 | The story adds RENTAL_ACTIVE to the closed list LOV-HOLDING | X1 | Conflict | Product owner |
| CG-ALL-10250 | No API Specification v5 yaml has the base of /api/recovery/payment/v1 | X5 | Missing | Solution architect |
| CG-ALL-10251 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10252 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10253 | No API Specification v5 yaml has the base of /api/recovery/comms/v1 | X5 | Missing | Solution architect |
| CG-ALL-10254 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10247 | Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10248 | Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10249 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10255 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10256 | Activity rentHeldAsset is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10257 | Test cases not in Test Cases v8: TC-E4-033-01, TC-E4-033-02, TC-E4-033-03, TC-E4-033-04, TC-E4-033-05 | X9 | Missing | QA |
| CG-ALL-10258 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-10259 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10260 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10261 | SCR-21 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10262 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10263 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X2: The role does not hold the Asset and disposal right (covered by 'TC-E4-033-04' only) | Not specified in the source documents | |
| AC5 | §5 X8: A statement, a component or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 'Section 17' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
