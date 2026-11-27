# Build-readiness review (script) — RWB-S8-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E2036-APP (RWB S8 E2036 APP Queue write interface for models and agents v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E2-036 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 14 (2 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)** and the **deviation handler of a case' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR2, BR7', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-02' has no BR ID; rule row 'R-DEV-03' has no BR ID; rule row 'R-DEV-08' has no BR ID; rule row 'R-DEV-09' has no BR ID; rule row 'R-DEV-18' has no BR ID; 8 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-11398 |
| 8 | Contract | Fail | detcheck: P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P1 rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt; P2 Workflow ID form and start rule of DeviationWorkflow are not stated; P2 Activity recordAndApplyDeviation is not in Temporal Catalog v1 (+1 more) | CG-ALL-11399, CG-ALL-11400, CG-ALL-11401, CG-ALL-11402, CG-ALL-11403 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-11404 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-11408, CG-ALL-11409, CG-ALL-11410 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-11405, CG-ALL-11406, CG-ALL-11407 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E2036-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11399 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11400 | rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11398 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11401 | Workflow ID form and start rule of DeviationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11402 | Activity recordAndApplyDeviation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11403 | Activity releaseDeviationHold is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11404 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11405 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11406 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-11407 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11408 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11409 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11410 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11411 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X8: A statement, a component or a test reaches `rwb_case`, `rwb_queue` or another service's schema (covered by 'Section 17, BR2, BR7' only) | Not specified in the source documents | |
| AC14 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
