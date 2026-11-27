# Build-readiness review (script) — RWB-S9-E6035-APP Match a recovery and calculate the agency fee

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E6035-APP (RWB S9 E6035 APP Match a recovery and calculate the agency fee v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E6-035 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 10, Fail 8. Detcheck rows: 22 (11 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner and agency manager' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-035-03', not by a criterion; exception X8 is covered by 'Section 17, BR5, BR6', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S9-007-1' has no BR ID; rule row 'BR-S9-007' has no BR ID; rule row 'R-WO-37' has no BR ID; rule row 'R-WO-33' has no BR ID; 10 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 8 transitions; detcheck: P1 The story adds PLACED_WITH_AGENCY to the closed list LOV-INSTR-STATUS; P1 The story adds PAYMENT_MATCHED to the closed list LOV-INSTR-STATUS | CG-ALL-11914, CG-ALL-11915 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11916, CG-ALL-11932 |
| 8 | Contract | Fail | detcheck: P1 GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml; P1 GET /partners` (API-S9-001) is not in rwb-partner.yaml; P1 No API Specification v5 yaml has the base of /api/recovery/payment/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1 (+6 more) | CG-ALL-11917, CG-ALL-11918, CG-ALL-11919, CG-ALL-11920, CG-ALL-11921, CG-ALL-11922, CG-ALL-11924, CG-ALL-11925, CG-ALL-11926, CG-ALL-11927, CG-ALL-11928 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11929 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-11933, CG-ALL-11934 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11931 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-035-01, TC-E6-035-02, TC-E6-035-03, TC-E6-035-04 | CG-ALL-11930 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 3 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11923 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S9-E6035-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_payment | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11914 | The story adds PLACED_WITH_AGENCY to the closed list LOV-INSTR-STATUS | X1 | Conflict | Product owner |
| CG-ALL-11915 | The story adds PAYMENT_MATCHED to the closed list LOV-INSTR-STATUS | X1 | Conflict | Product owner |
| CG-ALL-11917 | GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11918 | GET /partners` (API-S9-001) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11919 | No API Specification v5 yaml has the base of /api/recovery/payment/v1 | X5 | Missing | Solution architect |
| CG-ALL-11920 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-11921 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-11922 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-11923 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11924 | rwb-partner.yaml holds status as a closed enum while the story reads LOV-INSTR-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-11925 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11916 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11926 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11927 | Activity matchAgencyRecovery is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11928 | Activity calculateAgencyFee is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11930 | Test cases not in Test Cases v8: TC-E6-035-01, TC-E6-035-02, TC-E6-035-03, TC-E6-035-04 | X9 | Missing | QA |
| CG-ALL-11931 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11929 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11932 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11933 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11934 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11935 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the Partner portal right R (covered by 'TC-E6-035-03' only) | Not specified in the source documents | |
| AC4 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `payment` row or another service's (covered by 'Section 17, BR5, BR6' only) | Not specified in the source documents | |
| AC5 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
