# Build-readiness review (script) — RWB-S8-E7008-APP Review an override

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7008-APP (RWB S8 E7008 APP Review an override v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 10, Fail 8. Detcheck rows: 17 (7 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'risk and model risk officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E7-008-03', not by a criterion; exception X8 is covered by 'Section 17, BR5, BR8', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-09' has no BR ID; rule row 'R-DEV-10' has no BR ID; rule row 'R-DEV-22' has no BR ID; rule row 'R-DEV-11' has no BR ID; 10 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 12 transitions; detcheck: P1 The story adds DEV_WITH_OWNER to the closed list LOV-DEV-OUTCOME | CG-ALL-11623 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 16 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `recovery_log` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11624, CG-ALL-11625, CG-ALL-11636 |
| 8 | Contract | Fail | PATCH `/deviations/{deviationId}` (API-S8-002) has no idempotency key; detcheck: P1 PATCH /deviations/{deviationId}` (API-S8-002) is not in rwb-deviation.yaml; P1 POST /cases/{caseId}/deviations` (API-S8-001) is not in rwb-deviation.yaml; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data (+3 more) | CG-ALL-11626, CG-ALL-11627, CG-ALL-11628, CG-ALL-11630, CG-ALL-11631, CG-ALL-11632, CG-ALL-11633 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11637, CG-ALL-11638 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11635 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-008-01, TC-E7-008-02, TC-E7-008-03, TC-E7-008-04 | CG-ALL-11634 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 3 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11629 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7008-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11623 | The story adds DEV_WITH_OWNER to the closed list LOV-DEV-OUTCOME | X1 | Conflict | Product owner |
| CG-ALL-11626 | PATCH /deviations/{deviationId}` (API-S8-002) is not in rwb-deviation.yaml | X5 | Missing | Solution architect |
| CG-ALL-11627 | POST /cases/{caseId}/deviations` (API-S8-001) is not in rwb-deviation.yaml | X5 | Missing | Solution architect |
| CG-ALL-11628 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-11629 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11630 | rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-11631 | Workflow DeviationWorkflow task queue rwb-deviation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11624 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11625 | Name `recovery_log` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11632 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11633 | Activity recordDeviationReview is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11634 | Test cases not in Test Cases v8: TC-E7-008-01, TC-E7-008-02, TC-E7-008-03, TC-E7-008-04 | X9 | Missing | QA |
| CG-ALL-11635 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11636 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11637 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11638 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11639 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the case record right U (covered by 'TC-E7-008-03' only) | Not specified in the source documents | |
| AC4 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 'Section 17, BR5, BR8' only) | Not specified in the source documents | |
| AC5 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
