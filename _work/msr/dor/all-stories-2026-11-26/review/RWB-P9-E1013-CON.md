# Build-readiness review (script) — RWB-P9-E1013-CON Baseline measures - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P9-E1013-CON (RWB P9 E1013 CON Baseline measures - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-reporting |
| Legacy key | RWB-E1-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 6, Fail 4. Detcheck rows: 14 (6 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead of rwb-reporting' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 13 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 10 row(s) of §11 have no BR Field ID; §11 has 10 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7820 |
| 8 | Contract | Fail | detcheck: P1 GET /measure-definitions is not in rwb-reporting.yaml; P1 THE REFERENCE-LOAD ELEMENT OF THE DEFINITION TABLE (OPERATION NAME AND PATH NOT SPECIFIED IN THE SOURCE DOCUMENTS (GAP-2568; ASM-4234)) under the same base is not in rwb-reporting.yaml; P1 GET /api/recovery/case/v1/cases/facts is not published by rwb-case; P1 GET /api/recovery/case/v1/cases/{caseId}` family is not published by rwb-case (+3 more) | CG-ALL-7810, CG-ALL-7811, CG-ALL-7812, CG-ALL-7813, CG-ALL-7814, CG-ALL-7815, CG-ALL-7816 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7821, CG-ALL-7822 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P9-E1013-CON-01, TC-P9-E1013-CON-02, TC-P9-E1013-CON-03, TC-P9-E1013-CON-04, TC-P9-E1013-CON-05; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-7817, CG-ALL-7818, CG-ALL-7819 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7810 | GET /measure-definitions is not in rwb-reporting.yaml | X5 | Missing | Solution architect |
| CG-ALL-7811 | THE REFERENCE-LOAD ELEMENT OF THE DEFINITION TABLE (OPERATION NAME AND PATH NOT SPECIFIED IN THE SOURCE DOCUMENTS (GAP-2568; ASM-4234)) under the same base is not in rwb-reporting.yaml | X5 | Missing | Solution architect |
| CG-ALL-7812 | GET /api/recovery/case/v1/cases/facts is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7813 | GET /api/recovery/case/v1/cases/{caseId}` family is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7814 | GET /api/recovery/source-data/v1/payments?accountId={accountId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-7815 | Workflow MeasureRunWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7816 | Activity measureRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7817 | Test cases not in Test Cases v8: TC-P9-E1013-CON-01, TC-P9-E1013-CON-02, TC-P9-E1013-CON-03, TC-P9-E1013-CON-04, TC-P9-E1013-CON-05 | X9 | Missing | QA |
| CG-ALL-7818 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7819 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7820 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7821 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7822 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7823 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
