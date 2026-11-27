# Build-readiness review (script) — RWB-PLT-TE002-OPS Code owners for the recovery module

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-TE002-OPS (RWB PLT TE002 OPS Code owners for the recovery module - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-TE-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 6, Fail 5. Detcheck rows: 11 (0 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'DevOps engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has 5 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-002 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+3 more) | CG-ALL-1553, CG-ALL-1554, CG-ALL-1555, CG-ALL-1556, CG-ALL-1557, CG-ALL-1558, CG-ALL-1559 |
| 3 | Acceptance criteria | Pass | §7 holds 5 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 10 row(s) of §11 have no BR Field ID; §11 has 10 data rows | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 0 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 5 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-03, TC-PLT-TE002-OPS-04, TC-PLT-TE002-OPS-05; P3 §18 test lists differ from RTM v7 | CG-ALL-1551, CG-ALL-1552 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL32 (assumptions: none); open decision DL37 (assumptions: ASM-0189, ASM-0425, ASM-2516, ASM-3199); detcheck: P2 Open decision DL32 has no assumption | CG-ALL-1561 |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-PLT-TE002-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1553 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1554 | FR-PLT-002 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1555 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1556 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1557 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1558 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1559 | FR-PLT-027 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1561 | Open decision DL32 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1551 | Test cases not in Test Cases v8: TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-03, TC-PLT-TE002-OPS-04, TC-PLT-TE002-OPS-05 | X9 | Missing | QA |
| CG-ALL-1552 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1560 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
