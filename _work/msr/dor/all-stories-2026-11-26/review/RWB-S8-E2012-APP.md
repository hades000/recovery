# Build-readiness review (script) — RWB-S8-E2012-APP Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E2012-APP (RWB S8 E2012 APP Manual transfer and reassignment screen with reason v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E2-012 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 20 (6 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'Section 17', not by a criterion; exception X10 is covered by 'Section 17', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DEV-01' has no BR ID; rule row 'R-DEV-02' has no BR ID; rule row 'R-DEV-03' has no BR ID; rule row 'R-DEV-18' has no BR ID; 11 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 7 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-11336, CG-ALL-11337 |
| 8 | Contract | Fail | PATCH `/deviations/{deviationId}` has no idempotency key; detcheck: P1 GET /cases/{caseId}/deviations is not in rwb-deviation.yaml; P1 rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data; P1 rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data; P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt (+5 more) | CG-ALL-11338, CG-ALL-11340, CG-ALL-11341, CG-ALL-11342, CG-ALL-11343, CG-ALL-11344, CG-ALL-11345, CG-ALL-11346, CG-ALL-11347 |
| 9 | Messages | Partial | §14 lists 10 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-11348 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-05 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-11351, CG-ALL-11352, CG-ALL-11353, CG-ALL-11354 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-012-15; P3 Test cases cover other criteria in Test Cases v8 | CG-ALL-11349, CG-ALL-11350 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-11339 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E2012-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11338 | GET /cases/{caseId}/deviations is not in rwb-deviation.yaml | X5 | Missing | Solution architect |
| CG-ALL-11339 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-11340 | rwb-deviation.yaml holds outcome as a closed enum while the story reads LOV-DEV-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-11341 | rwb-deviation.yaml holds deviationCode as a closed enum while the story reads LOV-DEVIATION as data | X5 | Conflict | Solution architect |
| CG-ALL-11342 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-11343 | rwb.deviation.DeviationCleared.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11336 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11337 | Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11344 | rwb-deviation is not a consumer of rwb.case.CaseTransferred.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-11345 | Activity readOpenDeviations is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11346 | Activity applyCaseTransfer is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11347 | Activity recordDeviationMove is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11348 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11349 | Test cases not in Test Cases v8: TC-E2-012-15 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11350 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11351 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11352 | SCR-05 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11353 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11354 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11355 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X9: The case read, or the reference-data read, does not answer inside 2 s (covered by 'Section 17' only) | Not specified in the source documents | |
| AC15 | §5 X10: A statement, a test or a component reaches a `rwb_case` row or a `v_ace_*` view (covered by 'Section 17' only) | Not specified in the source documents | |
| AC16 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC19 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC20 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
