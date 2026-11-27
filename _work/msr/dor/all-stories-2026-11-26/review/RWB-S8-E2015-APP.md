# Build-readiness review (script) — RWB-S8-E2015-APP Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E2015-APP (RWB S8 E2015 APP Timers, escalation and the deviation flag on the case record view v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E2-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 14 (1 P1). AC review rows: 2. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'Section 14', not by a criterion; exception X7 is covered by 'Section 14', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-08' has no BR ID; rule row 'R-DEV-18' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-UNI-04, R-UNI-05, R-UNI-06' has no BR ID; rule row 'R-UNI-43' has no BR ID; 7 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR6, BR7, BR8; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `v_case_deviation` is not a field or entity in LDM v9 or Data Classification v5; P2 Field IDs DF-WRK-027 to DF-WRK-044 are not all fields of timer in LDM v9 | CG-ALL-11356, CG-ALL-11357 |
| 8 | Contract | Fail | detcheck: P1 GET /cases/{caseId}/deviations is not in rwb-deviation.yaml; P2 HTTP errors with no message ID: 401 no Workbench identity | CG-ALL-11358, CG-ALL-11359 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P7-003 is used with another meaning than the standard's | CG-ALL-11360 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11366, CG-ALL-11367, CG-ALL-11368 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11364 |
| 12 | Test cases | Fail | AC5 has no test case in §16; AC6 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5, AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-11361, CG-ALL-11362, CG-ALL-11363 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E2015-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11358 | GET /cases/{caseId}/deviations is not in rwb-deviation.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11356 | Name `v_case_deviation` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11357 | Field IDs DF-WRK-027 to DF-WRK-044 are not all fields of timer in LDM v9 | X3 | Conflict | Data |
| CG-ALL-11359 | HTTP errors with no message ID: 401 no Workbench identity | X5 | Missing | Business analyst |
| CG-ALL-11360 | MSG-P7-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-11362 | Criteria with no test case: AC5, AC6 | X9 | Missing | QA |
| CG-ALL-11364 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11361 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11363 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11365 | Flyway file V2015_1__case_deviation_read.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11366 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11367 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11368 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11369 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |
| AC6 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X2: The `caseId` is absent or is not a case reference (covered by 'Section 14' only) | Not specified in the source documents | |
| AC12 | §5 X7: An open row has no service-level row in force, or no label in the version of LOV-DEVIATION in force (covered by 'Section 14' only) | Not specified in the source documents | |
| AC13 | §8 BR1, BR2, BR3, BR4, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
