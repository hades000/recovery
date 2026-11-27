# Build-readiness review (script) — RWB-ITG-E2004-ITG Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2004-ITG (RWB ITG E2004 ITG Treatment entity and plan timers data model - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 11 (3 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and test team (QA)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC9 has no When; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 4 of 16 rules are covered by no criterion and no test case: BR13, BR14, BR15, BR16; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Pass | §11 has 16 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/data-products/DP04/records is not published by rwb-source-data; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-553, CG-ALL-555 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-556 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-559, CG-ALL-560, CG-ALL-561, CG-ALL-562 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-004-15-ITG, TC-E2-004-16-ITG; P3 §18 test lists differ from RTM v7 | CG-ALL-557, CG-ALL-558 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 4 build dependencies are not done yet (RWB-P3-E2004-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP); 4 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-554 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2004-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_treatment | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-553 | GET /api/recovery/source-data/v1/data-products/DP04/records is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-554 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-555 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-556 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-557 | Test cases not in Test Cases v8: TC-E2-004-15-ITG, TC-E2-004-16-ITG | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-558 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-559 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-560 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-561 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-562 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-563 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC9 | no When: the trigger is not stated |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR13, BR14, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
