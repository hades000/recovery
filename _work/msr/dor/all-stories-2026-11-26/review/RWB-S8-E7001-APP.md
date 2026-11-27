# Build-readiness review (script) — RWB-S8-E7001-APP Run X1 dispute and complaint end to end

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7001-APP (RWB S8 E7001 APP Run X1 dispute and complaint end to end v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 11, Fail 6. Detcheck rows: 14 (2 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'complaint officer (RW-COMPLAIN)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR3, BR4', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-02' has no BR ID; rule row 'R-DEV-07' has no BR ID; rule row 'R-DEV-08' has no BR ID; rule row 'R-DEV-09' has no BR ID; rule row 'R-DEV-18' has no BR ID; rule row 'R-DEV-19' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-DEV-22' has no BR ID; 9 of 18 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 13 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11412, CG-ALL-11422 |
| 8 | Contract | Fail | PATCH `/deviations/{deviationId}` has no idempotency key; detcheck: P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P1 rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P2 Workflow ID form and start rule of DeviationWorkflow are not stated; P2 Activity evaluateDeviationRules is not in Temporal Catalog v1 (+2 more) | CG-ALL-11413, CG-ALL-11414, CG-ALL-11415, CG-ALL-11416, CG-ALL-11417, CG-ALL-11418 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11419 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11423, CG-ALL-11424 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-001-01, TC-E7-001-02, TC-E7-001-03, TC-E7-001-04; P3 Test cases listed for criteria this story does not own | CG-ALL-11420, CG-ALL-11421 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7001-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11413 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11414 | rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11412 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11415 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11416 | Activity evaluateDeviationRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11417 | Activity recordAndApplyDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11418 | Activity resolveDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11420 | Test cases not in Test Cases v8: TC-E7-001-01, TC-E7-001-02, TC-E7-001-03, TC-E7-001-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11419 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11421 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-11422 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11423 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11424 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11425 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema (covered by 'Section 17, BR3, BR4' only) | Not specified in the source documents | |
| AC4 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC6 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC7 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
