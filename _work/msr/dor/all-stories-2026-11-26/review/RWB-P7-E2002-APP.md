# Build-readiness review (script) — RWB-P7-E2002-APP ACE plan status on the case

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2002-APP (RWB P7 E2002 APP ACE plan status on the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 10 (2 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN), a team manager (RW-TEAMMGR) and an internal auditor (RW-AUDIT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Pass | §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Pass | §11 has 17 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | CG-ALL-7043 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-006, MSG-P2-008; §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-7044 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-7049, CG-ALL-7050, CG-ALL-7051 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7047 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-002-11; P3 §18 test lists differ from RTM v7 | CG-ALL-7045, CG-ALL-7046 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7042 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2002-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7042 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7043 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7044 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7045 | Test cases not in Test Cases v8: TC-E2-002-11 | X9 | Missing | QA |
| CG-ALL-7047 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7046 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7048 | Flyway file V2002_1__plan_status_record.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7049 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7050 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7051 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
