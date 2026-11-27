# Build-readiness review (script) — RWB-P3-E2042-APP Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E2042-APP (RWB P3 E2042 APP Epic 2 rule packages in Drools v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E2-042 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 13 (6 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 5 of 13 rules are covered by no criterion and no test case: BR6, BR8, BR10, BR11, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; §11 has 9 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-4395 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision; P1 GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision; P1 Workflow RuleModelSwap is not in Temporal Catalog v1; P2 Activity swapRuleModel is not in Temporal Catalog v1 | CG-ALL-4386, CG-ALL-4387, CG-ALL-4389, CG-ALL-4390 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-4391 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-4396 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-4392 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 3 build dependencies are not done yet (RWB-P3-E1073-APP, RWB-P3-E2042-INF, RWB-P3-E2042-OPS); 14 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-4388 |
| 18 | Open decisions | Partial | open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-4398 |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E2042-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E1073-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4386 | GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-4387 | GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-4388 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-4389 | Workflow RuleModelSwap is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4393 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-4394 | Java package th.co.scb.ace.workbench.recovery.case.rules.epic2 uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4390 | Activity swapRuleModel is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-4391 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-4398 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4392 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4395 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-4396 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4397 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR6, BR8, BR10, BR11, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
