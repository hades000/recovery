# Build-readiness review (script) — RWB-PLT-E1037-APP Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1037-APP (RWB PLT E1037 APP Role to permission matrix as data and PDPA field masking by role v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-037 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 11 (1 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'service developer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has 15 traceability rows; detcheck: P2 FR-PLT-008 has 2 meanings in the PRD; P2 FR-PLT-019 has 2 meanings in the PRD; P2 FR-PLT-026 has 2 meanings in the PRD; P2 FR-PLT-033 has 2 meanings in the PRD | CG-ALL-1309, CG-ALL-1310, CG-ALL-1311, CG-ALL-1312 |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 3 of 14 rules are covered by no criterion and no test case: BR10, BR12, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Pass | §11 has 13 data rows | — |
| 8 | Contract | Fail | detcheck: P2 platform is not a consumer of rwb.access.AccessPolicyChanged.v1 in Kafka Catalog v1; P1 Event type rwb.access.DoALimitChanged.v1 is not in Kafka Catalog v1 | CG-ALL-1304, CG-ALL-1305 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P1-002; §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story; P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-1313, CG-ALL-1314 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1308 |
| 12 | Test cases | Partial | §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-PLT-E1037-APP-01, TC-PLT-E1037-APP-02, TC-PLT-E1037-APP-03, TC-PLT-E1037-APP-04, TC-PLT-E1037-APP-05, TC-PLT-E1037-APP-06, TC-PLT-E1037-APP-07; P3 §18 test lists differ from RTM v7 | CG-ALL-1306, CG-ALL-1307 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL38 (assumptions: ASM-0245, ASM-1413, ASM-1424, ASM-1508) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1037-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1305 | Event type rwb.access.DoALimitChanged.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1304 | platform is not a consumer of rwb.access.AccessPolicyChanged.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-1306 | Test cases not in Test Cases v8: TC-PLT-E1037-APP-01, TC-PLT-E1037-APP-02, TC-PLT-E1037-APP-03, TC-PLT-E1037-APP-04, TC-PLT-E1037-APP-05, TC-PLT-E1037-APP-06, TC-PLT-E1037-APP-07 | X9 | Missing | QA |
| CG-ALL-1308 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-1309 | FR-PLT-008 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1310 | FR-PLT-019 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1311 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1312 | FR-PLT-033 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1307 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1313 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1314 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC7 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §8 BR10, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
