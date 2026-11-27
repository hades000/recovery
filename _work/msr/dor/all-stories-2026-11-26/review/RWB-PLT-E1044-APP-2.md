# Build-readiness review (script) — RWB-PLT-E1044-APP-2 Database migrations versioned with parameterized schema names

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1044-APP-2 (RWB PLT E1044 APP-2 Database migrations versioned with parameterized schema names v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-044 |

## R1. Verdict

**NOT READY.** Checklist: Pass 15, Partial 5, Fail 5. Detcheck rows: 9 (0 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 3 traceability rows; detcheck: P2 FR-PLT-005 has 2 meanings in the PRD; P2 FR-PLT-006 has 2 meanings in the PRD; P2 FR-PLT-007 has 2 meanings in the PRD | CG-ALL-1498, CG-ALL-1499, CG-ALL-1500 |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | §11 has no data table; detcheck: P2 Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `flyway_schema_history_recovery` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `information_schema` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1493, CG-ALL-1494, CG-ALL-1495 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 2 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1501 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-02, TC-PLT-E1044-APP2-03, TC-PLT-E1044-APP2-04, TC-PLT-E1044-APP2-05, TC-PLT-E1044-APP2-06; P3 §18 test lists differ from RTM v7 | CG-ALL-1496, CG-ALL-1497 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1044-CON exists; its build status is 'In build', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1493 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1494 | Name `flyway_schema_history_recovery` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1495 | Name `information_schema` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1496 | Test cases not in Test Cases v8: TC-PLT-E1044-APP2-01, TC-PLT-E1044-APP2-02, TC-PLT-E1044-APP2-03, TC-PLT-E1044-APP2-04, TC-PLT-E1044-APP2-05, TC-PLT-E1044-APP2-06 | X9 | Missing | QA |
| CG-ALL-1498 | FR-PLT-005 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1499 | FR-PLT-006 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1500 | FR-PLT-007 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1497 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1501 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
