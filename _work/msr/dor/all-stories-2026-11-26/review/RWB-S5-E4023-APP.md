# Build-readiness review (script) — RWB-S5-E4023-APP Allocate the asset to an auction vendor by distance

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E4023-APP (RWB S5 E4023 APP Allocate the asset to an auction vendor by distance v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E4-023 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 16 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'Section 17, BR3, BR6', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DIS-30' has no BR ID; rule row 'R-DIS-31' has no BR ID; 11 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 10 data rows; detcheck: P2 Name `vendor_capacity` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9993, CG-ALL-9994, CG-ALL-10004, CG-ALL-10005 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of AssetDisposalWorkflow are not stated (+2 more) | CG-ALL-9995, CG-ALL-9996, CG-ALL-9997, CG-ALL-9998, CG-ALL-9999, CG-ALL-10000 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-10001 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-23 has no empty, loading, error, no access state in the story | CG-ALL-10006, CG-ALL-10007 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10003 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-023-01, TC-E4-023-02, TC-E4-023-03, TC-E4-023-04, TC-E4-023-05, TC-E4-023-06 | CG-ALL-10002 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E4023-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_partner | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9995 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-9996 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-9997 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9993 | Name `vendor_capacity` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9994 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9998 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9999 | Activity allocateVendor is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10000 | Activity The rwb-partner vendor-panel activity (name Not specified in the source documents (GAP-2901; ASM-4799)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10002 | Test cases not in Test Cases v8: TC-E4-023-01, TC-E4-023-02, TC-E4-023-03, TC-E4-023-04, TC-E4-023-05, TC-E4-023-06 | X9 | Missing | QA |
| CG-ALL-10003 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-10004 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10001 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-10005 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10006 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10007 | SCR-23 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10008 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X9: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, an `assignment` row or another servi (covered by 'Section 17, BR3, BR6' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
