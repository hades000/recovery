# Build-readiness review (script) — RWB-P7-E2004-APP Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2004-APP (RWB P7 E2004 APP Treatment entity and plan timers data model v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 12 (3 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'centre of excellence analyst (RW-COE)** who owns the rule package, and as an **internal auditor (RW-AUDIT)** who reads the log' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Pass | §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 15 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /rule-catalog/{ruleId}` with the query `packageVersion is not in rwb-decision.yaml; P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | CG-ALL-7052, CG-ALL-7054 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4; P2 MSG-P7-009 is used with another meaning than the standard's | CG-ALL-7055, CG-ALL-7056 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story; P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-7061, CG-ALL-7062 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7060 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-004-15, TC-E2-004-16; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-7057, CG-ALL-7058, CG-ALL-7059 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7053 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2004-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7052 | GET /rule-catalog/{ruleId}` with the query `packageVersion is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7053 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7054 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7055 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7056 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7057 | Test cases not in Test Cases v8: TC-E2-004-15, TC-E2-004-16 | X9 | Missing | QA |
| CG-ALL-7060 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7058 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-7059 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7061 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7062 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7063 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
