# Build-readiness review (script) — RWB-P1-DM012-APP Migrate decision log

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-DM012-APP (RWB P1 DM012 APP Migrate decision log v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-DM-012 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 12, Fail 5. Detcheck rows: 7 (0 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW)** and **an internal auditor (RW-AUDIT)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 24 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'TC-DM-012-05', not by a criterion; exception X10 is covered by 'TC-DM-012-04', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 1 of 11 rules are covered by no criterion and no test case: BR4; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1973 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-1974 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1978 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1976 |
| 12 | Test cases | Partial | §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-012-01, TC-DM-012-03, TC-DM-012-04, TC-DM-012-05 | CG-ALL-1975 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1069-APP); 5 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1001-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1973 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1975 | Test cases not in Test Cases v8: TC-DM-012-01, TC-DM-012-03, TC-DM-012-04, TC-DM-012-05 | X9 | Missing | QA |
| CG-ALL-1976 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1974 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1977 | Flyway file V000x__dm012_decision_log_cutover.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-1978 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1979 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X5: The local decision record or its outbox row cannot be written (covered by 'TC-DM-012-05' only) | Not specified in the source documents | |
| AC5 | §5 X10: A caller without the Platform administration right asks for the cutover result or starts the run (covered by 'TC-DM-012-04' only) | Not specified in the source documents | |
| AC6 | §8 BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
