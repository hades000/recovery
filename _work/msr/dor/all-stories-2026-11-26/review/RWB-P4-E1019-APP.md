# Build-readiness review (script) — RWB-P4-E1019-APP Roles, teams and queues as data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1019-APP (RWB P4 E1019 APP Roles, teams and queues as data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 6, Fail 8. Detcheck rows: 13 (5 P1). AC review rows: 5. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator (RW-SECADM) and a reference data administrator (RW-REFADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 8 of 13 rules are covered by no criterion and no test case: BR2, BR3, BR4, BR6, BR8, BR9, BR10, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds AUDIT_VIEW to the closed list LOV-CAPABILITY | CG-ALL-4901 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 10 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 20 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/access/v1/admin/roles is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/me/session is not in rwb-access.yaml; P2 HTTP errors with no message ID: 404 a path this service does not publish; P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data (+1 more) | CG-ALL-4902, CG-ALL-4903, CG-ALL-4904, CG-ALL-4905, CG-ALL-4906 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-006; §14 lists 6 messages; detcheck: P2 MSG-P4-006 is used with another meaning than the standard's | CG-ALL-4907 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-4912 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC2 has no test case in §16; AC3 has no test case in §16; AC4 has no test case in §16; AC6 has no test case in §16; AC8 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC2, AC3, AC4, AC6, AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-4908, CG-ALL-4909, CG-ALL-4910 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1019-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4901 | The story adds AUDIT_VIEW to the closed list LOV-CAPABILITY | X1 | Conflict | Product owner |
| CG-ALL-4902 | GET /api/recovery/access/v1/admin/roles is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4903 | GET /api/recovery/access/v1/me/session is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4905 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-4906 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4904 | HTTP errors with no message ID: 404 a path this service does not publish | X5 | Missing | Business analyst |
| CG-ALL-4907 | MSG-P4-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4909 | Criteria with no test case: AC2, AC3, AC4, AC6, AC8 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4908 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4910 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4911 | Flyway file V1019_1__role_matrix.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4912 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4913 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no test case in §16 |  |
| AC3 | no test case in §16; vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |
| AC4 | no test case in §16 |  |
| AC6 | no test case in §16 |  |
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR2, BR3, BR4, BR6, BR8, BR9, BR10, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
