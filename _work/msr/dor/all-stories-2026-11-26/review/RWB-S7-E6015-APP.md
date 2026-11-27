# Build-readiness review (script) — RWB-S7-E6015-APP Prepare the write-off pack

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S7-E6015-APP (RWB S7 E6015 APP Prepare the write-off pack v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-writeoff |
| Legacy key | RWB-E6-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 19 (8 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'write-off team member (RW-WRITEOFF)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-015-04', not by a criterion; exception X8 is covered by 'Section 17, BR3, BR4, BR5', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-WO-05' has no BR ID; 11 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 19 data rows; detcheck: P2 Name `provision_carried` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `pack_document_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly (+1 more) | CG-ALL-10879, CG-ALL-10880, CG-ALL-10881, CG-ALL-10894, CG-ALL-10895 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/document/v1; P1 No API Specification v5 yaml has the base of /api/recovery/agent/v1 (+4 more) | CG-ALL-10882, CG-ALL-10883, CG-ALL-10884, CG-ALL-10885, CG-ALL-10886, CG-ALL-10887, CG-ALL-10889, CG-ALL-10890, CG-ALL-10891 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-27 has no empty, loading, error, no access state in the story | CG-ALL-10896 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10893 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-015-01, TC-E6-015-02, TC-E6-015-03, TC-E6-015-04, TC-E6-015-05 | CG-ALL-10892 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 3 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-10888 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S7-E6015-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_agent, rwb_case, rwb_decision, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10882 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10883 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-10884 | No API Specification v5 yaml has the base of /api/recovery/document/v1 | X5 | Missing | Solution architect |
| CG-ALL-10885 | No API Specification v5 yaml has the base of /api/recovery/document/v1 | X5 | Missing | Solution architect |
| CG-ALL-10886 | No API Specification v5 yaml has the base of /api/recovery/agent/v1 | X5 | Missing | Solution architect |
| CG-ALL-10887 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10888 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-10889 | Workflow WriteOffWorkflow task queue rwb-writeoff` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10879 | Name `provision_carried` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10880 | Name `pack_document_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10881 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10890 | Workflow ID form and start rule of WriteOffWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10891 | Activity prepareWriteOffPack is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10892 | Test cases not in Test Cases v8: TC-E6-015-01, TC-E6-015-02, TC-E6-015-03, TC-E6-015-04, TC-E6-015-05 | X9 | Missing | QA |
| CG-ALL-10893 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-10894 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10895 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10896 | SCR-27 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10897 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X2: The role does not hold the Write-off and posting right of the action (covered by 'TC-E6-015-04' only) | Not specified in the source documents | |
| AC5 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `document` row or another service' (covered by 'Section 17, BR3, BR4, BR5' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
