# Build-readiness review (script) — RWB-S8-E7005-APP Run X5 bankruptcy and seizure end to end

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7005-APP (RWB S8 E7005 APP Run X5 bankruptcy and seizure end to end v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-005 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 11, Fail 6. Detcheck rows: 18 (1 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'Legal counsel (RW-LEGAL)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'BR5', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-05' has no BR ID; rule row 'R-DEV-15' has no BR ID; rule row 'R-DEV-19' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; 5 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR6, BR7; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 10 transitions; detcheck: P1 The story adds DEV_FLAGGED to the closed list LOV-DEVIATION | CG-ALL-11532 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 17 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11533, CG-ALL-11546 |
| 8 | Contract | Partial | PATCH `/deviations/{deviationId}` has no idempotency key; detcheck: P2 Payload of rwb.deviation.DeviationRaised.v1 differs from Kafka Catalog v1; P2 Payload of rwb.deviation.DeviationCleared.v1 differs from Kafka Catalog v1; P2 Workflow ID form and start rule of DeviationWorkflow are not stated; P2 Activity validateDeviation is not in Temporal Catalog v1 (+5 more) | CG-ALL-11535, CG-ALL-11536, CG-ALL-11537, CG-ALL-11538, CG-ALL-11539, CG-ALL-11540, CG-ALL-11541, CG-ALL-11542, CG-ALL-11543 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11547, CG-ALL-11548 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11545 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-005-02, TC-E7-005-03, TC-E7-005-04, TC-E7-005-05, TC-E7-005-06, TC-S8-E7005-APP-01, TC-S8-E7005-APP-02, TC-S8-E7005-APP-03 | CG-ALL-11544 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 dependencies named; detcheck: P2 HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a state that refuses the step or an X5 deviation already open; 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S8-E7005-CON`, which this story consumes as its first build dependency | CG-ALL-11534 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7005-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_document, rwb_litigation | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11532 | The story adds DEV_FLAGGED to the closed list LOV-DEVIATION | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 13 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11533 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11534 | HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a state that refuses the step or an X5 deviation already open; 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S8-E7005-CON`, which this story consumes as its first build dependency | X5 | Missing | Business analyst |
| CG-ALL-11535 | Payload of rwb.deviation.DeviationRaised.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-11536 | Payload of rwb.deviation.DeviationCleared.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-11537 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11538 | Activity validateDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11539 | Activity evaluateRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11540 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11541 | Activity applyDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11542 | Activity raiseClockSignal is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11543 | Activity publishDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11544 | Test cases not in Test Cases v8: TC-E7-005-02, TC-E7-005-03, TC-E7-005-04, TC-E7-005-05, TC-E7-005-06, TC-S8-E7005-APP-01, TC-S8-E7005-APP-02, TC-S8-E7005-APP-03 | X9 | Missing | QA |
| CG-ALL-11545 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11546 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11547 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11548 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11549 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X10: A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR5' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR4, BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
