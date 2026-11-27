# Build-readiness review (script) — RWB-S8-E7004-APP Run X4 fraud end to end

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7004-APP (RWB S8 E7004 APP Run X4 fraud end to end v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 6, Partial 11, Fail 8. Detcheck rows: 21 (8 P1). AC review rows: 0. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'fraud investigator (RW-FRAUD)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E7-004-03', not by a criterion; exception X6 is covered by 'X6', not by a criterion; exception X7 is covered by 'X7', not by a criterion; exception X8 is covered by 'X8', not by a criterion; exception X9 is covered by 'Section 17, BR4, BR5', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-UNI-08' has no BR ID; rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-04' has no BR ID; rule row 'R-DEV-13' has no BR ID; rule row 'R-DEV-14' has no BR ID; rule row 'R-DEV-19' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-DEV-21' has no BR ID; 11 of 19 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 19 rules | — |
| 5 | State transitions | Fail | §9 has 10 transitions; detcheck: P1 The story adds DEV_REROUTE to the closed list LOV-DEV-OUTCOME | CG-ALL-11498 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11499, CG-ALL-11500, CG-ALL-11515 |
| 8 | Contract | Fail | detcheck: P1 rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data; P1 rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data; P1 rwb-deviation.yaml holds raisedBy as a closed enum while the story reads LOV-RAISED-BY as data; P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1` with its retry and `.dlt` topics (+5 more) | CG-ALL-11502, CG-ALL-11503, CG-ALL-11504, CG-ALL-11505, CG-ALL-11506, CG-ALL-11507, CG-ALL-11508, CG-ALL-11509, CG-ALL-11510 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11516, CG-ALL-11517 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11514 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-004-01, TC-E7-004-02, TC-E7-004-03, TC-E7-004-04; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-11511, CG-ALL-11512, CG-ALL-11513 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 3 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11501 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7004-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11498 | The story adds DEV_REROUTE to the closed list LOV-DEV-OUTCOME | X1 | Conflict | Product owner |
| CG-ALL-11501 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11502 | rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-11503 | rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data | X5 | Conflict | Solution architect |
| CG-ALL-11504 | rwb-deviation.yaml holds raisedBy as a closed enum while the story reads LOV-RAISED-BY as data | X5 | Conflict | Solution architect |
| CG-ALL-11505 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1` with its retry and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-11506 | rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1` with its retry and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-11507 | Workflow DeviationWorkflow task queue rwb-deviation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11499 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11500 | Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11508 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11509 | Activity EvaluateDeviationRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11510 | Activity RecordAndApplyDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11511 | Test cases not in Test Cases v8: TC-E7-004-01, TC-E7-004-02, TC-E7-004-03, TC-E7-004-04 | X9 | Missing | QA |
| CG-ALL-11514 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11512 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-11513 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11515 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11516 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11517 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11518 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §5 X2: The caller does not hold Case record U of the operation (covered by 'TC-E7-004-03' only) | Not specified in the source documents | |
| AC7 | §5 X6: The deviation sits with its owner past the service level of R-DEV-20 (covered by 'X6' only) | Not specified in the source documents | |
| AC8 | §5 X7: A code outside X1 to X7, or a code with no owner (covered by 'X7' only) | Not specified in the source documents | |
| AC9 | §5 X8: A repeated raise with the same `Idempotency-Key`, or a second outcome on one deviation (covered by 'X8' only) | Not specified in the source documents | |
| AC10 | §5 X9: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's s (covered by 'Section 17, BR4, BR5' only) | Not specified in the source documents | |
| AC11 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC16 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
