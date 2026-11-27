# Build-readiness review (script) — RWB-P7-E2012-APP Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2012-APP (RWB P7 E2012 APP Manual transfer and reassignment screen with reason v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-012 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 16 (2 P1). AC review rows: 4. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'internal audit officer (RW-AUDIT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 3 of 11 rules are covered by no criterion and no test case: BR8, BR9, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 14 data rows; detcheck: P2 Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7133 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 404 an unknown package code or entry; P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | CG-ALL-7134, CG-ALL-7136 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-7137, CG-ALL-7138 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-05 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-7145, CG-ALL-7146, CG-ALL-7147 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7143 |
| 12 | Test cases | Fail | AC4 has no test case in §16; AC7 has no test case in §16; AC8 has no test case in §16; AC9 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-012-15; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC4, AC7, AC8, AC9; P3 §18 test lists differ from RTM v7 | CG-ALL-7139, CG-ALL-7140, CG-ALL-7141, CG-ALL-7142 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7135 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2012-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7135 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7136 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7133 | Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7134 | HTTP errors with no message ID: 404 an unknown package code or entry | X5 | Missing | Business analyst |
| CG-ALL-7137 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7138 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7139 | Test cases not in Test Cases v8: TC-E2-012-15 | X9 | Missing | QA |
| CG-ALL-7141 | Criteria with no test case: AC4, AC7, AC8, AC9 | X9 | Missing | QA |
| CG-ALL-7143 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7140 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7142 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7144 | Flyway file V2027_3__decision_transfer_ledger.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7145 | SCR-05 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7146 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7147 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7148 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | no test case in §16 |  |
| AC7 | no test case in §16 |  |
| AC8 | no test case in §16 |  |
| AC9 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR8, BR9, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
