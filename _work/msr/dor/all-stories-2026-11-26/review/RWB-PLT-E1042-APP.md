# Build-readiness review (script) — RWB-PLT-E1042-APP Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1042-APP (RWB PLT E1042 APP Central configuration service and parameter catalog v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-042 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 10 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'squad member' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has 12 traceability rows; detcheck: P2 FR-PLT-008 has 2 meanings in the PRD; P2 FR-PLT-016 has 2 meanings in the PRD; P2 FR-PLT-017 has 2 meanings in the PRD; P2 FR-PLT-018 has 2 meanings in the PRD (+1 more) | CG-ALL-1328, CG-ALL-1329, CG-ALL-1330, CG-ALL-1331, CG-ALL-1332 |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Pass | §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 3 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.case.ParameterVersionApproved.v1 is not in Kafka Catalog v1 | CG-ALL-1325 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1333, CG-ALL-1334 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-PLT-E1042-APP-01, TC-PLT-E1042-APP-02, TC-PLT-E1042-APP-03, TC-PLT-E1042-APP-04, TC-PLT-E1042-APP-05, TC-PLT-E1042-APP-06, TC-PLT-E1042-APP-07; P3 §18 test lists differ from RTM v7 | CG-ALL-1326, CG-ALL-1327 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 9 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1042-CON exists; its build status is 'In build', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1325 | Event type rwb.case.ParameterVersionApproved.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1326 | Test cases not in Test Cases v8: TC-PLT-E1042-APP-01, TC-PLT-E1042-APP-02, TC-PLT-E1042-APP-03, TC-PLT-E1042-APP-04, TC-PLT-E1042-APP-05, TC-PLT-E1042-APP-06, TC-PLT-E1042-APP-07 | X9 | Missing | QA |
| CG-ALL-1328 | FR-PLT-008 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1329 | FR-PLT-016 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1330 | FR-PLT-017 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1331 | FR-PLT-018 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1332 | FR-PLT-019 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1327 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1333 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1334 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
