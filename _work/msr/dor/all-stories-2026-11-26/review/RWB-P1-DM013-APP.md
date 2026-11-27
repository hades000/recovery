# Build-readiness review (script) — RWB-P1-DM013-APP Migrate money and closure

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-DM013-APP (RWB P1 DM013 APP Migrate money and closure v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-DM-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 11, Fail 5. Detcheck rows: 7 (0 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 21 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 2 owned criteria in Gherkin | — |
| 4 | Business rules | Pass | §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1980 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-GEN-006 text differs from the Error and Message Standard v4 | CG-ALL-1981, CG-ALL-1982, CG-ALL-1983 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-1986 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1985 |
| 12 | Test cases | Partial | §16 has 3 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-013-01, TC-DM-013-03, TC-DM-013-04 | CG-ALL-1984 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1069-APP); 4 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (3) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1001-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1980 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1984 | Test cases not in Test Cases v8: TC-DM-013-01, TC-DM-013-03, TC-DM-013-04 | X9 | Missing | QA |
| CG-ALL-1985 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1981 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1982 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1983 | MSG-GEN-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1986 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
