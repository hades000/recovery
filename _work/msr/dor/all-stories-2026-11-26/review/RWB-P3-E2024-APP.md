# Build-readiness review (script) — RWB-P3-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2024-APP (RWB P3 E2024 APP Field app photos and bills into the document hub v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-024 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 17 (10 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'field collector who syncs a visit and the case owner who chases what the visit did not deliver' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 9 rules are covered by no criterion and no test case: BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 15 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/case/v1/cases/{caseId} is not in rwb-case.yaml; P1 GET /api/recovery/case/v1/cases/{caseId}/timeline is not in rwb-case.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 rwb-case.yaml holds discretion as a closed enum while the story reads LOV-DISCRETION as data (+4 more) | CG-ALL-4273, CG-ALL-4274, CG-ALL-4275, CG-ALL-4276, CG-ALL-4277, CG-ALL-4278, CG-ALL-4279, CG-ALL-4280 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-003; §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story | CG-ALL-4286, CG-ALL-4287, CG-ALL-4288 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-4281, CG-ALL-4282 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL03 (assumptions: ASM-0189, ASM-0193, ASM-0578, ASM-2567); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E2024-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4273 | GET /api/recovery/case/v1/cases/{caseId} is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-4274 | GET /api/recovery/case/v1/cases/{caseId}/timeline is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-4275 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4276 | rwb-case.yaml holds discretion as a closed enum while the story reads LOV-DISCRETION as data | X5 | Conflict | Solution architect |
| CG-ALL-4277 | rwb-case.yaml holds elementType as a closed enum while the story reads LOV-ELEMENT as data | X5 | Conflict | Solution architect |
| CG-ALL-4278 | rwb-case.yaml holds status as a closed enum while the story reads LOV-TASK-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4279 | rwb-case.yaml holds status as a closed enum while the story reads LOV-VERSION-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-4280 | rwb.document.DocumentStored.v1 is on topic rwb.document.events.v1 in the catalog, not rwb.document.events.v1`, through the inbox of DP-09 | X6 | Conflict | Solution architect |
| CG-ALL-4283 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4284 | Java package th.co.scb.ace.workbench.recovery.case.context uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4281 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4282 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4285 | Flyway file V2024_1__checklist_task.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4286 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4287 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4288 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4289 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | message MSG-GEN-003 is not in §14 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §8 BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
