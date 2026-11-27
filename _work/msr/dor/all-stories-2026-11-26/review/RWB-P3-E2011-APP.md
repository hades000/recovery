# Build-readiness review (script) — RWB-P3-E2011-APP Queue view screens: my queue, team queues, filters and ageing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2011-APP (RWB P3 E2011 APP Queue view screens  my queue, team queues, filters and ageing v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 12 (5 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Pass | §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E2-011-13', not by a criterion; §7 holds 12 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 2 of 10 rules are covered by no criterion and no test case: BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 25 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data; P1 rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data; P1 rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data (+1 more) | CG-ALL-4091, CG-ALL-4092, CG-ALL-4093, CG-ALL-4094, CG-ALL-4095 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-05 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story | CG-ALL-4098, CG-ALL-4099, CG-ALL-4100, CG-ALL-4101 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-4096 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P3-E1020-APP); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E2011-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E1020-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4091 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4092 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4093 | rwb-case.yaml holds routeCode as a closed enum while the story reads LOV-ROUTE as data | X5 | Conflict | Solution architect |
| CG-ALL-4094 | rwb-case.yaml holds stageCode as a closed enum while the story reads LOV-STAGE as data | X5 | Conflict | Solution architect |
| CG-ALL-4097 | Java package th.co.scb.ace.workbench.recovery.case.queueview uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4095 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4096 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4098 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4099 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4100 | SCR-05 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4101 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4102 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X7: A role without Case record R or without Queue and allocation R opens either view (covered by 'TC-E2-011-13' only) | Not specified in the source documents | |
| AC14 | §8 BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC18 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
