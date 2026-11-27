# Build-readiness review (script) — RWB-P3-E2016-APP Full case record view with the history timeline

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2016-APP (RWB P3 E2016 APP Full case record view with the history timeline v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-016 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 15 (8 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 4 of 15 rules are covered by no criterion and no test case: BR6, BR11, BR12, BR14; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Fail | §11 has 34 data rows; detcheck: P1 Index column assignment.assigned_at DESC is not a field of assignment in LDM v9; P1 Index column timer.started_at DESC is not a field of timer in LDM v9 | CG-ALL-4234, CG-ALL-4235 |
| 8 | Contract | Fail | detcheck: P1 GET /cases/{caseId}/timeline` with `type=ASSIGNMENT,TRANSFER is not in rwb-case.yaml; P1 GET /api/recovery/comms/v1/cases/{caseId}/notices is not published by rwb-comms; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/access/v1/masking-policies is not published by rwb-access (+1 more) | CG-ALL-4236, CG-ALL-4237, CG-ALL-4238, CG-ALL-4239, CG-ALL-4240 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-04 has no empty, loading, error, no access state in the story | CG-ALL-4246, CG-ALL-4247 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4242 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-4241 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P3-E2012-APP, RWB-P3-E2015-APP); 11 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E2016-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E2015-APP, RWB-P3-E2012-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4234 | Index column assignment.assigned_at DESC is not a field of assignment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-4235 | Index column timer.started_at DESC is not a field of timer in LDM v9 | X3 | Conflict | Data |
| CG-ALL-4236 | GET /cases/{caseId}/timeline` with `type=ASSIGNMENT,TRANSFER is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-4237 | GET /api/recovery/comms/v1/cases/{caseId}/notices is not published by rwb-comms | X5 | Missing | Solution architect |
| CG-ALL-4238 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4239 | GET /api/recovery/access/v1/masking-policies is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-4243 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4244 | Java package th.co.scb.ace.workbench.recovery.case.timeline uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4240 | HTTP errors with no message ID: 503 the case store is down. A downstream that is down is not a 5xx of this operation: it is an `unavailableSources[]` entry with 200 (BR10) | X5 | Missing | Business analyst |
| CG-ALL-4242 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4241 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4245 | Flyway file V2016_1__timeline_indexes.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4246 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4247 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4248 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR6, BR11, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
