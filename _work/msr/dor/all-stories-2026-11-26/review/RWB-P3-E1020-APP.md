# Build-readiness review (script) — RWB-P3-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1020-APP (RWB P3 E1020 APP Allocation and assignment engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 19 (9 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Access test TC-E1-020-14', not by a criterion; §7 holds 12 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 4 of 12 rules are covered by no criterion and no test case: BR7, BR10, BR11, BR12; §8 has 12 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source | CG-ALL-3519 |
| 5 | State transitions | Fail | §9 has 4 transitions; detcheck: P1 Status 'New, in the deviation handler queue' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, in the exception queue' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-3512, CG-ALL-3513, CG-ALL-3514 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Pass | §11 has 29 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds assignmentMethod as a closed enum while the story reads LOV-ASSIGN as data; P1 rwb-case.yaml holds reason as a closed enum while the story reads LOV-ASSIGN-REASON as data; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | CG-ALL-3516, CG-ALL-3517, CG-ALL-3518 |
| 9 | Messages | Partial | event name 'rwb.case.DecisionRecorded' does not follow rwb.<short>.<Event>.v1 (DP-14); §14 lists 6 messages; detcheck: P3 MSG-P3-012 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3520, CG-ALL-3521 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, error, no access state in the story | CG-ALL-3527, CG-ALL-3528, CG-ALL-3529 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3522, CG-ALL-3523 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 5 build dependencies are not done yet (RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1020-OPS, RWB-P3-E1073-APP, RWB-PLT-E1056-OPS); 18 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3515 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL15 (assumptions: ASM-5264); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E1020-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3512 | Status 'New, in the deviation handler queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3513 | Status 'New, in the exception queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3514 | Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3515 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3516 | rwb-case.yaml holds assignmentMethod as a closed enum while the story reads LOV-ASSIGN as data | X5 | Conflict | Solution architect |
| CG-ALL-3517 | rwb-case.yaml holds reason as a closed enum while the story reads LOV-ASSIGN-REASON as data | X5 | Conflict | Solution architect |
| CG-ALL-3518 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3524 | Java package th.co.scb.ace.workbench.recovery.case.allocation uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3525 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3519 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3521 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3520 | MSG-P3-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3522 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3523 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3526 | Flyway file V020_1__allocation_columns.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3527 | SCR-02 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3528 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3529 | SCR-09 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3530 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X10: A user without the right starts DailyCaseRun from the run monitor (covered by 'Access test TC-E1-020-14' only) | Not specified in the source documents | |
| AC15 | §8 BR7, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
