# Build-readiness review (script) — RWB-ITG-E1073-ITG Rule authoring, validation, test scenarios, approval and rollback in Drools — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1073-ITG (RWB ITG E1073 ITG Rule authoring, validation, test scenarios, approval and rollback in Drools - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-073 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 17 (7 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'TC-E1-073-12-ITG', not by a criterion; exception X11 is covered by 'TC-E1-073-16-ITG', not by a criterion; exception X13 is covered by 'TC-E1-073-14-ITG', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 15 exception paths | — |
| 4 | Business rules | Partial | §8 has 15 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source; P2 Rule ID ALLOC-032 used in the criteria exists in no current source; P2 Rule ID ALLOC-041 used in the criteria exists in no current source | CG-ALL-456, CG-ALL-457, CG-ALL-458 |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Pass | §10 has 14 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; §11 has 27 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/admin/rule-versions is not published by rwb-decision; P1 POST /api/recovery/decision/v1/admin/rule-versions is not published by rwb-decision; P1 POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve is not published by rwb-decision; P1 POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback is not published by rwb-decision (+2 more) | CG-ALL-449, CG-ALL-450, CG-ALL-451, CG-ALL-452, CG-ALL-453, CG-ALL-454 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-459 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-463 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 25 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1073-01, TC-ITG-E1073-02, TC-ITG-E1073-03, TC-ITG-E1073-04, TC-ITG-E1073-05; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-460, CG-ALL-461, CG-ALL-462 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 4 build dependencies are not done yet (RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P6-E1073-APP, RWB-P7-E1073-APP); 4 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-455 |
| 18 | Open decisions | Partial | open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-465 |
| 19 | Test data | Pass | every test case in §16 names its data (25) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1073-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-access, rwb-decision, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-449 | GET /api/recovery/decision/v1/admin/rule-versions is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-450 | POST /api/recovery/decision/v1/admin/rule-versions is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-451 | POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-452 | POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-453 | GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-454 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-455 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-456 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-457 | Rule ID ALLOC-032 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-458 | Rule ID ALLOC-041 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-459 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-460 | Test cases not in Test Cases v8: TC-ITG-E1073-01, TC-ITG-E1073-02, TC-ITG-E1073-03, TC-ITG-E1073-04, TC-ITG-E1073-05 | X9 | Missing | QA |
| CG-ALL-465 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-461 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-462 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-463 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-464 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X10: An empty file (covered by 'TC-E1-073-12-ITG' only) | Not specified in the source documents | |
| AC17 | §5 X11: A role without Rules and parameters C loads a file (covered by 'TC-E1-073-16-ITG' only) | Not specified in the source documents | |
| AC18 | §5 X13: A scenario of an in-force package fails in the pipeline (covered by 'TC-E1-073-14-ITG' only) | Not specified in the source documents | |
| AC19 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
