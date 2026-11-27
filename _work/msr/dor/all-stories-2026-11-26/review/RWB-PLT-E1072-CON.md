# Build-readiness review (script) — RWB-PLT-E1072-CON Drools runtime and rule package store - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1072-CON (RWB PLT E1072 CON Drools runtime and rule package store - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-072 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 10 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 14 Epic design; 16 Size; 17 Dependencies; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'consumer of the embedded rules kit' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has 14 traceability rows; detcheck: P2 FR-PLT-014 has 2 meanings in the PRD; P2 FR-PLT-015 has 2 meanings in the PRD; P2 FR-PLT-016 has 2 meanings in the PRD; P2 FR-PLT-017 has 2 meanings in the PRD (+2 more) | CG-ALL-1407, CG-ALL-1408, CG-ALL-1409, CG-ALL-1410, CG-ALL-1411, CG-ALL-1412 |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 6 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 11 of 11 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 1 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-1404 |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 5 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-PLT-E1072-CON-01, TC-PLT-E1072-CON-02, TC-PLT-E1072-CON-03, TC-PLT-E1072-CON-04, TC-PLT-E1072-CON-05; P3 §18 test lists differ from RTM v7 | CG-ALL-1405, CG-ALL-1406 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 0 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-1403 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1403 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1404 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1407 | FR-PLT-014 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1408 | FR-PLT-015 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1409 | FR-PLT-016 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1410 | FR-PLT-017 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1411 | FR-PLT-018 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1412 | FR-PLT-020 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1405 | Test cases not in Test Cases v8: TC-PLT-E1072-CON-01, TC-PLT-E1072-CON-02, TC-PLT-E1072-CON-03, TC-PLT-E1072-CON-04, TC-PLT-E1072-CON-05 | X9 | Missing | QA |
| CG-ALL-1406 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
