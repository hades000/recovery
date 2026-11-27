# Build-readiness review (script) — RWB-P1-E1011-CON Reconciliation and data quality report

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1011-CON (RWB P1 E1011 CON Reconciliation and data quality report - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 11 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 5 row(s) of §11 have no BR Field ID; §11 has 5 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /admin/reconciliation/results is not in rwb-source-data.yaml; P1 GET /admin/reconciliation/results/{resultId} is not in rwb-source-data.yaml; P2 rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P1 Workflow ReconciliationWorkflow is not in Temporal Catalog v1 (+1 more) | CG-ALL-2063, CG-ALL-2064, CG-ALL-2065, CG-ALL-2066, CG-ALL-2067 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2068, CG-ALL-2069 |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-2070, CG-ALL-2071, CG-ALL-2072 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2063 | GET /admin/reconciliation/results is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2064 | GET /admin/reconciliation/results/{resultId} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2066 | Workflow ReconciliationWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2065 | rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2067 | Activity reconciliation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2068 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2069 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2070 | Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09 | X9 | Missing | QA |
| CG-ALL-2071 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2072 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2073 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
