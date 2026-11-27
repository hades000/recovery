# Build-readiness review (script) — RWB-ITG-E1013-ITG Baseline measures

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1013-ITG (RWB ITG E1013 ITG Baseline measures - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 9 (2 P1). AC review rows: 2. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 6 of 12 rules are covered by no criterion and no test case: BR6, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 5 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-198, CG-ALL-199 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/source-data/v1/business-days/{date}/ready is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/payments?accountId={accountId} is not published by rwb-source-data; P2 Activity snapshot(page) is not in Temporal Catalog v1 | CG-ALL-193, CG-ALL-194, CG-ALL-195 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-200, CG-ALL-201 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 9 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-196, CG-ALL-197 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E1018-APP, RWB-P9-E1013-APP); 4 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1013-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-reporting, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-193 | POST /api/recovery/source-data/v1/business-days/{date}/ready is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-194 | GET /api/recovery/source-data/v1/payments?accountId={accountId} is not published by rwb-source-data | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-195 | Activity snapshot(page) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-198 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-196 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-197 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-199 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-200 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-201 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC6 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR6, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC11 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
