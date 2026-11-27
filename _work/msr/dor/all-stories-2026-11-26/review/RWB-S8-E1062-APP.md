# Build-readiness review (script) — RWB-S8-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E1062-APP (RWB S8 E1062 APP Deviation screening agent in shadow [E2b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E1-062 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 12 (2 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'Section 14', not by a criterion; exception X3 is covered by 'Section 14', not by a criterion; exception X6 is covered by 'Section 14', not by a criterion; exception X7 is covered by 'Section 17, BR1, BR6', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-02' has no BR ID; rule row 'R-DEV-03' has no BR ID; rule row 'R-DEV-04' has no BR ID; rule row 'R-DEV-05' has no BR ID; rule row 'R-DEV-06' has no BR ID; rule row 'R-DEV-01' has no BR ID; 7 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR5, BR6, BR7, BR8; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 16 data rows; detcheck: P2 Name `v_open_deviation` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-11307 |
| 8 | Contract | Fail | detcheck: P1 GET /deviations is not in rwb-deviation.yaml; P2 HTTP errors with no message ID: 401 no Workbench identity | CG-ALL-11308, CG-ALL-11309 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11316, CG-ALL-11317 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11314 |
| 12 | Test cases | Fail | AC2 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC2; P3 §18 test lists differ from RTM v7 | CG-ALL-11311, CG-ALL-11312, CG-ALL-11313 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11310 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E1062-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-agent; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11308 | GET /deviations is not in rwb-deviation.yaml | X5 | Missing | Solution architect |
| CG-ALL-11310 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11307 | Name `v_open_deviation` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11309 | HTTP errors with no message ID: 401 no Workbench identity | X5 | Missing | Business analyst |
| CG-ALL-11312 | Criteria with no test case: AC2 | X9 | Missing | QA |
| CG-ALL-11314 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11311 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11313 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11315 | Flyway file V1062_1__screening_deviation_read.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11316 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11317 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11318 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X2: The `caseId` query is absent or is not a case reference (covered by 'Section 14' only) | Not specified in the source documents | |
| AC11 | §5 X3: The reference-data or the package read does not answer inside the budget, or the registry has no package version in forc (covered by 'Section 14' only) | Not specified in the source documents | |
| AC12 | §5 X6: The rwb-agent policy read does not answer, so the mode in force is unknown (covered by 'Section 14' only) | Not specified in the source documents | |
| AC13 | §5 X7: A component, a statement or a test reaches a `recovery_case` row, a `rwb_case` table, a `v_ace_*` view or another servic (covered by 'Section 17, BR1, BR6' only) | Not specified in the source documents | |
| AC14 | §8 BR1, BR2, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
