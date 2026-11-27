# Build-readiness review (script) — RWB-S8-E7006-APP Run X6 lost contact and skip trace end to end

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E7006-APP (RWB S8 E7006 APP Run X6 lost contact and skip trace end to end v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E7-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 6, Partial 12, Fail 7. Detcheck rows: 18 (4 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'case owner** — and as the step the FSD gives no primary person, because it runs unattended and the agent works the trace under policy —' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR3, BR5', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-06' has no BR ID; rule row 'R-DEV-16' has no BR ID; rule row 'R-DEV-17' has no BR ID; rule row 'R-DEV-18' has no BR ID; rule row 'R-DEV-19' has no BR ID; rule row 'R-DEV-20' has no BR ID; rule row 'R-UNI-12' has no BR ID; 10 of 18 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 18 rules | — |
| 5 | State transitions | Fail | §9 has 14 transitions; detcheck: P1 The story adds DEV_WITH_OWNER to the closed list LOV-DEVIATION; P1 The story adds DEV_WITH_OWNER to the closed list LOV-RAISED-BY | CG-ALL-11560, CG-ALL-11561 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11562, CG-ALL-11574 |
| 8 | Contract | Fail | PATCH `/deviations/{deviationId}` has no idempotency key; detcheck: P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P1 rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P2 Workflow ID form and start rule of DeviationWorkflow are not stated; P2 Activity evaluateDeviationRules is not in Temporal Catalog v1 (+4 more) | CG-ALL-11563, CG-ALL-11564, CG-ALL-11565, CG-ALL-11566, CG-ALL-11567, CG-ALL-11568, CG-ALL-11569, CG-ALL-11570 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11571 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story | CG-ALL-11575, CG-ALL-11576 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-006-01, TC-E7-006-02, TC-E7-006-03, TC-E7-006-04; P3 Test cases listed for criteria this story does not own | CG-ALL-11572, CG-ALL-11573 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S8-E7006-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-partner; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11560 | The story adds DEV_WITH_OWNER to the closed list LOV-DEVIATION | X1 | Conflict | Product owner |
| CG-ALL-11561 | The story adds DEV_WITH_OWNER to the closed list LOV-RAISED-BY | X1 | Conflict | Product owner |
| CG-ALL-11563 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11564 | rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11562 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11565 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11566 | Activity evaluateDeviationRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11567 | Activity recordAndApplyDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11568 | Activity runSkipTrace is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11569 | Activity readContactData is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11570 | Activity resolveDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11572 | Test cases not in Test Cases v8: TC-E7-006-01, TC-E7-006-02, TC-E7-006-03, TC-E7-006-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11571 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11573 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-11574 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11575 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11576 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11577 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row, a `partner` row or another service's sche (covered by 'Section 17, BR3, BR5' only) | Not specified in the source documents | |
| AC4 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC6 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC7 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
