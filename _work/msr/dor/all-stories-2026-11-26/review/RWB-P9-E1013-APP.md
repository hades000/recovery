# Build-readiness review (script) — RWB-P9-E1013-APP Baseline measures

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P9-E1013-APP (RWB P9 E1013 APP Baseline measures v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-reporting |
| Legacy key | RWB-E1-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 11 (5 P1). AC review rows: 0. Missing criteria: 9.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by AC6, which this story neither owns nor names as owned by another story; exception X6 is covered by 'BR3, TC-E1-013-05', not by a criterion; exception X7 is covered by '§12.2, TC-E1-013-02', not by a criterion; exception X8 is covered by '§17, BR5', not by a criterion; exception X9 is covered by '§17, BR1', not by a criterion; exception X10 is covered by 'BR6, TC-E1-013-05', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 8 of 13 rules are covered by no criterion and no test case: BR3, BR4, BR6, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 10 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7806 |
| 8 | Contract | Fail | detcheck: P1 GET /measure-definitions is not in rwb-reporting.yaml; P1 GET /api/recovery/case/v1/cases/facts is not published by rwb-case; P1 GET /api/recovery/case/v1/cases/{caseId}` family is not published by rwb-case; P1 GET /api/recovery/source-data/v1/payments?accountId={accountId} is not published by rwb-source-data (+2 more) | CG-ALL-7799, CG-ALL-7800, CG-ALL-7801, CG-ALL-7802, CG-ALL-7803, CG-ALL-7804 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7807, CG-ALL-7808 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7805 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P9-E1013-OPS); 9 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P9-E1013-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7799 | GET /measure-definitions is not in rwb-reporting.yaml | X5 | Missing | Solution architect |
| CG-ALL-7800 | GET /api/recovery/case/v1/cases/facts is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7801 | GET /api/recovery/case/v1/cases/{caseId}` family is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7802 | GET /api/recovery/source-data/v1/payments?accountId={accountId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-7803 | Workflow MeasureRunWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7804 | Activity measureRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7805 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7806 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7807 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7808 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7809 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X3: The gate answer for the baseline date is HOLD (covered by AC6, which exist nowhere in this story) | Not specified in the source documents | |
| AC10 | §5 X6: The decision record cannot be written (covered by 'BR3, TC-E1-013-05' only) | Not specified in the source documents | |
| AC11 | §5 X7: The rwb-case or rwb-source-data read does not answer inside 2 s, or its breaker is open (covered by '§12.2, TC-E1-013-02' only) | Not specified in the source documents | |
| AC12 | §5 X8: A statement or a test reaches `recovery_case`, a `v_ace_*` view or another service's schema (covered by '§17, BR5' only) | Not specified in the source documents | |
| AC13 | §5 X9: A measure code, formula, unit or band value appears in Java (covered by '§17, BR1' only) | Not specified in the source documents | |
| AC14 | §5 X10: A frozen row is updated or deleted, by the service, a script or a person (covered by 'BR6, TC-E1-013-05' only) | Not specified in the source documents | |
| AC15 | §8 BR3, BR4, BR6, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
