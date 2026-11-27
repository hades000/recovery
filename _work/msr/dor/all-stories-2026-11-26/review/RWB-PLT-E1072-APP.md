# Build-readiness review (script) — RWB-PLT-E1072-APP Drools runtime and rule package store

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1072-APP (RWB PLT E1072 APP Drools runtime and rule package store v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-072 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 12 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'service team building the EvaluateRules activity of its own service' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 16 traceability rows; detcheck: P2 FR-PLT-014 has 2 meanings in the PRD; P2 FR-PLT-015 has 2 meanings in the PRD; P2 FR-PLT-016 has 2 meanings in the PRD; P2 FR-PLT-017 has 2 meanings in the PRD (+2 more) | CG-ALL-1396, CG-ALL-1397, CG-ALL-1398, CG-ALL-1399, CG-ALL-1400, CG-ALL-1401 |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'Guardrail, section 17', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 4 of 12 rules are covered by no criterion and no test case: BR4, BR10, BR11, BR12; §8 has 12 rules; detcheck: P2 Rule ID ALLOC-032 used in the criteria exists in no current source | CG-ALL-1393 |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows; detcheck: P2 Name `drools_kiebase_builds_total` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1391 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 1 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-1394 |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 8 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1395 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 10 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-1392 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1072-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1392 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1391 | Name `drools_kiebase_builds_total` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1393 | Rule ID ALLOC-032 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-1394 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1396 | FR-PLT-014 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1397 | FR-PLT-015 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1398 | FR-PLT-016 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1399 | FR-PLT-017 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1400 | FR-PLT-018 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1401 | FR-PLT-020 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1395 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1402 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X7: A workflow class calls `RuleEvaluator` directly (covered by 'Guardrail, section 17' only) | Not specified in the source documents | |
| AC9 | §8 BR4, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
