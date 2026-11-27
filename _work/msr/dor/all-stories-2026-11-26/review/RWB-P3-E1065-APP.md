# Build-readiness review (script) — RWB-P3-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1065-APP (RWB P3 E1065 APP Sandbox database with synthetic recovery data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-065 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 6, Fail 8. Detcheck rows: 17 (6 P1). AC review rows: 2. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'tribe lead and squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 names no feature; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 9 rules are covered by no criterion and no test case: BR6, BR7; §8 has 9 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source | CG-ALL-3879 |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Pass | §11 has 14 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data; P1 rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data; P1 rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data | CG-ALL-3876, CG-ALL-3877, CG-ALL-3878 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-3887, CG-ALL-3888, CG-ALL-3889, CG-ALL-3890 |
| 11 | Guardrails | Partial | §17 does not state the personal data rule | — |
| 12 | Test cases | Fail | AC3 has no test case in §16; AC6 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-P3-E1065-01; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC3, AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-3880, CG-ALL-3881, CG-ALL-3882, CG-ALL-3883 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3875 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL15 (assumptions: ASM-5264); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL39 (assumptions: ASM-1617, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E1065-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_sandbox_read | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3875 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3876 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3877 | rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data | X5 | Conflict | Solution architect |
| CG-ALL-3878 | rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data | X5 | Conflict | Solution architect |
| CG-ALL-3884 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3885 | Java package th.co.scb.ace.workbench.recovery.case.sandboxseed uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3879 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3880 | Test cases not in Test Cases v8: TC-P3-E1065-01 | X9 | Missing | QA |
| CG-ALL-3882 | Criteria with no test case: AC3, AC6 | X9 | Missing | QA |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3881 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3883 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3886 | Flyway file V1065_1__case_estate_seed.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3887 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3888 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3889 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3890 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3891 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | no test case in §16 |  |
| AC6 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
