# Build-readiness review (script) — RWB-PLT-TE003-APP-2 Types and contract tests from the API specification

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-TE003-APP-2 (RWB PLT TE003 APP-2 Types and contract tests from the API specification v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-TE-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 15, Partial 5, Fail 5. Detcheck rows: 18 (0 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 11 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-009 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+11 more) | CG-ALL-1581, CG-ALL-1582, CG-ALL-1583, CG-ALL-1584, CG-ALL-1585, CG-ALL-1586, CG-ALL-1587, CG-ALL-1588, CG-ALL-1589, CG-ALL-1590, CG-ALL-1591, CG-ALL-1592 (+3) |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | §11 has no data table | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 1 messages | — |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-03, TC-PLT-TE003-APP2-04, TC-PLT-TE003-APP2-05, TC-PLT-TE003-APP2-06; P3 §18 test lists differ from RTM v7 | CG-ALL-1579, CG-ALL-1580 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-PLT-TE003-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 16 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1579 | Test cases not in Test Cases v8: TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-03, TC-PLT-TE003-APP2-04, TC-PLT-TE003-APP2-05, TC-PLT-TE003-APP2-06 | X9 | Missing | QA |
| CG-ALL-1581 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1582 | FR-PLT-009 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1583 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1584 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1585 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1586 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1587 | FR-PLT-019 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1588 | FR-PLT-021 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1589 | FR-PLT-022 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1590 | FR-PLT-023 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1591 | FR-PLT-024 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1592 | FR-PLT-025 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1593 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1594 | FR-PLT-028 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1595 | FR-PLT-029 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1580 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1596 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
