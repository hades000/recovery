# Build-readiness review (script) — RWB-P4-E2033-APP Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2033-APP (RWB P4 E2033 APP Case and queue list with status, owner and ageing v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 5, Fail 8. Detcheck rows: 12 (4 P1). AC review rows: 2. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR), a case owner or an internal auditor who reads the case and queue list' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'BR1', not by a criterion; exception X8 is covered by 'BR7', not by a criterion; exception X9 is covered by 'BR9', not by a criterion; §7 holds 12 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 9 rules are covered by no criterion and no test case: BR5, BR8; §8 has 9 rules | — |
| 5 | State transitions | Fail | §9 has no transition (no status change in this story); detcheck: P1 The story adds CAR to the closed list LOV-PRODUCT; P1 The story adds CAR to the closed list LOV-CAPABILITY; P1 The story adds CAR to the closed list LOV-SCOPE | CG-ALL-5351, CG-ALL-5352, CG-ALL-5353 |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 18 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | CG-ALL-5354 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-GEN-007 text differs from the Error and Message Standard v4; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-5355, CG-ALL-5356 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story | CG-ALL-5360 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC11 has no test case in §16; AC12 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC11, AC12; P3 §18 test lists differ from RTM v7 | CG-ALL-5357, CG-ALL-5358, CG-ALL-5359 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL31 (assumptions: none); detcheck: P2 Open decision DL31 has no assumption | CG-ALL-5362 |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2033-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5351 | The story adds CAR to the closed list LOV-PRODUCT | X1 | Conflict | Product owner |
| CG-ALL-5352 | The story adds CAR to the closed list LOV-CAPABILITY | X1 | Conflict | Product owner |
| CG-ALL-5353 | The story adds CAR to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-5354 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5356 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5358 | Criteria with no test case: AC11, AC12 | X9 | Missing | QA |
| CG-ALL-5362 | Open decision DL31 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5355 | MSG-GEN-007 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-5357 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5359 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5360 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5361 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC11 | no test case in §16 |  |
| AC12 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X1: No Recovery role in the session (covered by 'BR1' only) | Not specified in the source documents | |
| AC14 | §5 X8: The access record cannot be written (covered by 'BR7' only) | Not specified in the source documents | |
| AC15 | §5 X9: The parameters or reference contract does not answer inside its budget (covered by 'BR9' only) | Not specified in the source documents | |
| AC16 | §8 BR5, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
