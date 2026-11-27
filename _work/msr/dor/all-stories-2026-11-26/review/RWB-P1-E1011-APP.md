# Build-readiness review (script) — RWB-P1-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1011-APP (RWB P1 E1011 APP Reconciliation and data quality report v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 15 (4 P1). AC review rows: 0. Missing criteria: 9.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Partial | §18 has no L3 process column; §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by AC2, which this story neither owns nor names as owned by another story; exception X2 is covered by 'BR6', not by a criterion; exception X3 is covered by 'BR9', not by a criterion; exception X6 is covered by 'BR13', not by a criterion; exception X8 is covered by 'TC-E1-011-07', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR3, BR4; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 37 data rows; detcheck: P2 Name `dq_exception` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `dq_rule` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2048, CG-ALL-2049 |
| 8 | Contract | Fail | detcheck: P1 GET /admin/reconciliation/results is not in rwb-source-data.yaml; P1 GET /admin/reconciliation/results/{resultId} is not in rwb-source-data.yaml; P1 rwb-source-data.yaml holds result as a closed enum while the story reads LOV-REC-RESULT as data; P2 rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 (+2 more) | CG-ALL-2050, CG-ALL-2051, CG-ALL-2052, CG-ALL-2053, CG-ALL-2054, CG-ALL-2055 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2056, CG-ALL-2057 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-2061 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-2058, CG-ALL-2059, CG-ALL-2060 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1011-OPS, RWB-P1-E1015-APP, RWB-P1-E1069-APP); 13 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P1-E1011-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1015-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2050 | GET /admin/reconciliation/results is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2051 | GET /admin/reconciliation/results/{resultId} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2052 | rwb-source-data.yaml holds result as a closed enum while the story reads LOV-REC-RESULT as data | X5 | Conflict | Solution architect |
| CG-ALL-2054 | Workflow ReconciliationWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2048 | Name `dq_exception` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2049 | Name `dq_rule` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2053 | rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2055 | Activity reconciliation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2058 | Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2056 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2057 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2059 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2060 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2061 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2062 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X1: A product's variance is above the tolerance (covered by AC2, which exist nowhere in this story) | Not specified in the source documents | |
| AC10 | §5 X2: The variance equals the tolerance (covered by 'BR6' only) | Not specified in the source documents | |
| AC11 | §5 X3: The ACE batch for the business date is not COMPLETE (covered by 'BR9' only) | Not specified in the source documents | |
| AC12 | §5 X6: A business key has no ACE row (covered by 'BR13' only) | Not specified in the source documents | |
| AC13 | §5 X8: A role without Platform administration R reads the results (covered by 'TC-E1-011-07' only) | Not specified in the source documents | |
| AC14 | §8 BR3, BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
