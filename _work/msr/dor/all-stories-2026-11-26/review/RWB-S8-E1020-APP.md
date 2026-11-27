# Build-readiness review (script) — RWB-S8-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E1020-APP (RWB S8 E1020 APP Allocation and assignment engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E1-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 9, Fail 8. Detcheck rows: 18 (3 P1). AC review rows: 2. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR5, BR6', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-03' has no BR ID; rule row 'R-DEV-04' has no BR ID; rule row 'R-DEV-05' has no BR ID; rule row 'R-DEV-06' has no BR ID; rule row 'R-DEV-21' has no BR ID; 7 of 15 rules are covered by no criterion and no test case: BR1, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11260, CG-ALL-11274 |
| 8 | Contract | Fail | POST `/cases/{caseId}/deviations` has no idempotency key; PATCH `/deviations/{deviationId}` has no idempotency key; detcheck: P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Workflow ID form and start rule of DeviationWorkflow are not stated; P2 Activity evaluateHandlerRules is not in Temporal Catalog v1 (+1 more) | CG-ALL-11262, CG-ALL-11263, CG-ALL-11264, CG-ALL-11265, CG-ALL-11266 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11267, CG-ALL-11268 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11275, CG-ALL-11276 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11272 |
| 12 | Test cases | Fail | AC4 has no test case in §16; AC7 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC4, AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-11269, CG-ALL-11270, CG-ALL-11271 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11261 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E1020-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11261 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11262 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11263 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11260 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11264 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11265 | Activity evaluateHandlerRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11266 | Activity recordAndApplyPlacement is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11267 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11270 | Criteria with no test case: AC4, AC7 | X9 | Missing | QA |
| CG-ALL-11272 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11268 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11269 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11271 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11273 | Flyway file V1020_1__placement_indexes.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11274 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11275 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11276 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11277 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | no test case in §16 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema (covered by 'Section 17, BR5, BR6' only) | Not specified in the source documents | |
| AC9 | §8 BR1, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC12 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
