# Build-readiness review (script) — RWB-S7-E6022-APP Send provision inputs to Finance

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S7-E6022-APP (RWB S7 E6022 APP Send provision inputs to Finance v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-writeoff |
| Legacy key | RWB-E6-022 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 11 (1 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-022-04', not by a criterion; exception X3 is covered by 'VR-S7-010-1, X8', not by a criterion; exception X4 is covered by 'X7', not by a criterion; exception X5 is covered by 'X4', not by a criterion; exception X6 is covered by 'X7, R-WO-27', not by a criterion; exception X7 is covered by 'X7', not by a criterion; exception X8 is covered by 'Section 17, BR5, BR8', not by a criterion; exception X9 is covered by 'X9', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-WO-25' has no BR ID; rule row 'R-WO-26' has no BR ID; rule row 'R-WO-27' has no BR ID; rule row 'R-WO-28' has no BR ID; 11 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `finance_feed_status` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11083, CG-ALL-11084, CG-ALL-11091 |
| 8 | Contract | Fail | detcheck: P1 Workflow WriteOffWorkflow task queue rwb-writeoff` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of WriteOffWorkflow are not stated; P2 Activity prepareFinanceFeed is not in Temporal Catalog v1; P2 Activity sendFinanceFeed is not in Temporal Catalog v1 | CG-ALL-11085, CG-ALL-11086, CG-ALL-11087, CG-ALL-11088 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-27 has no empty, loading, error, no access state in the story | CG-ALL-11092 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11090 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-022-01, TC-E6-022-02, TC-E6-022-03, TC-E6-022-04, TC-E6-022-05 | CG-ALL-11089 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S7-E6022-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11085 | Workflow WriteOffWorkflow task queue rwb-writeoff` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11083 | Name `finance_feed_status` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11084 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11086 | Workflow ID form and start rule of WriteOffWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11087 | Activity prepareFinanceFeed is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11088 | Activity sendFinanceFeed is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11089 | Test cases not in Test Cases v8: TC-E6-022-01, TC-E6-022-02, TC-E6-022-03, TC-E6-022-04, TC-E6-022-05 | X9 | Missing | QA |
| CG-ALL-11090 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11091 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11092 | SCR-27 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11093 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X2: A caller without the Write-off and posting right reads the feed outcome (covered by 'TC-E6-022-04' only) | Not specified in the source documents | |
| AC5 | §5 X3: No tax criteria version is in force (covered by 'VR-S7-010-1, X8' only) | Not specified in the source documents | |
| AC6 | §5 X4: The case is not at `PROVISION_RELEASED` when the run arrives, or has left the population since it was read (covered by 'X7' only) | Not specified in the source documents | |
| AC7 | §5 X5: rwb-case, rwb-decision or the reference-data read does not answer inside 2 s, or its breaker is open (covered by 'X4' only) | Not specified in the source documents | |
| AC8 | §5 X6: The Finance provision feed rejects the file (covered by 'X7, R-WO-27' only) | Not specified in the source documents | |
| AC9 | §5 X7: The same business date, population and package version arrive twice, or the same `Idempotency-Key` twice (covered by 'X7' only) | Not specified in the source documents | |
| AC10 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 'Section 17, BR5, BR8' only) | Not specified in the source documents | |
| AC11 | §5 X9: The Finance feed row has changed since the last run, or no row is in force at the business date (covered by 'X9' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
