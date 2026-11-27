# Build-readiness review (script) — RWB-ITG-E2015-ITG Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2015-ITG (RWB ITG E2015 ITG Timers, escalation and the deviation flag on the case record view - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 5 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and QA team' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 4 owned criteria in Gherkin | — |
| 4 | Business rules | Pass | §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Pass | §11 has 27 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access | CG-ALL-662 |
| 9 | Messages | Pass | §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-665 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 11 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-663, CG-ALL-664 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P3-E2015-APP, RWB-P4-E2015-APP, RWB-S8-E2015-APP); 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2015-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-662 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-663 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-664 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-665 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-666 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
