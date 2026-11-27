# Build-readiness review (script) — RWB-S8-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E1065-APP (RWB S8 E1065 APP Sandbox database with synthetic recovery data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E1-065 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 6, Fail 9. Detcheck rows: 12 (5 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'recovery developer (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 7 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | CG-ALL-11319 |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 14 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data; P1 rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data; P1 rwb-deviation.yaml holds raisedBy as a closed enum while the story reads LOV-RAISED-BY as data | CG-ALL-11322, CG-ALL-11323, CG-ALL-11324 |
| 9 | Messages | Pass | §14 lists 2 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11328, CG-ALL-11329 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC8 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-11325, CG-ALL-11326, CG-ALL-11327 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11321 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL15 (assumptions: ASM-5264); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL39 (assumptions: ASM-1617, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-DEV-BAND is not in Reference Data v5 | CG-ALL-11320 |
| 21 | Contract published | Fail | no contract story RWB-S8-E1065-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_sandbox, rwb_sandbox_next | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11319 | The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | X1 | Conflict | Product owner |
| CG-ALL-11321 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11322 | rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-11323 | rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data | X5 | Conflict | Solution architect |
| CG-ALL-11324 | rwb-deviation.yaml holds raisedBy as a closed enum while the story reads LOV-RAISED-BY as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11320 | List LOV-DEV-BAND is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-11326 | Criteria with no test case: AC8 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11325 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11327 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11328 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11329 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11330 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR3, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
