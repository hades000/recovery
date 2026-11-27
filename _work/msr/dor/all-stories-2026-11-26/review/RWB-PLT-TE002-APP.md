# Build-readiness review (script) — RWB-PLT-TE002-APP Code owners for the recovery module

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-TE002-APP (RWB PLT TE002 APP Code owners for the recovery module v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-TE-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 8, Fail 5. Detcheck rows: 10 (0 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 names no feature; §18 has 1 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-002 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+3 more) | CG-ALL-1542, CG-ALL-1543, CG-ALL-1544, CG-ALL-1545, CG-ALL-1546, CG-ALL-1547, CG-ALL-1548 |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'Access test TC-TE-002-08', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 2 of 7 rules are covered by no criterion and no test case: BR4, BR5; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 4 roles | — |
| 7 | Data | Partial | §11 has no data table | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 0 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 8 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1541 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-PLT-TE001-APP, RWB-PLT-TE002-OPS); 6 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL04 (assumptions: ASM-0189, ASM-3199); open decision DL07 (assumptions: ASM-0189, ASM-3199); open decision DL32 (assumptions: none); open decision DL36 (assumptions: ASM-5584); open decision DL37 (assumptions: ASM-0189, ASM-0425, ASM-2516, ASM-3199); detcheck: P2 Open decision DL32 has no assumption | CG-ALL-1550 |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
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
| CG-ALL-1542 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1543 | FR-PLT-002 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1544 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1545 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1546 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1547 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1548 | FR-PLT-027 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1550 | Open decision DL32 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1541 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1549 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X7: A squad member who is not a code owner tries to satisfy the review (covered by 'Access test TC-TE-002-08' only) | Not specified in the source documents | |
| AC9 | §8 BR4, BR5 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
