# Build-readiness review (script) — RWB-P8-E4050-APP Reconcile money movements daily

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E4050-APP (RWB P8 E4050 APP Reconcile money movements daily v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E4-050 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 12, Fail 6. Detcheck rows: 11 (0 P1). AC review rows: 0. Missing criteria: 13.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 22 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-050-01, TC-E4-050-02', not by a criterion; exception X3 is covered by 'TC-E4-050-01', not by a criterion; exception X4 is covered by 'TC-E4-050-01', not by a criterion; exception X5 is covered by 'TC-E4-050-01', not by a criterion; exception X6 is covered by 'TC-E4-050-01', not by a criterion; exception X7 is covered by 'TC-E4-050-01', not by a criterion; exception X8 is covered by 'TC-E4-050-03', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 16 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-7779, CG-ALL-7787 |
| 8 | Contract | Partial | detcheck: P2 HTTP errors with no message ID: 400; 401; 404 for an object outside scope; 503 when a consumed answer or the record library does not answer in time; P2 Activity proceedsReconciliation is not in Temporal Catalog v1; P2 Activity The rule-in-force read is not in Temporal Catalog v1 | CG-ALL-7780, CG-ALL-7781, CG-ALL-7782 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-7783 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story | CG-ALL-7788 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7786 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-050-01, TC-E4-050-02, TC-E4-050-03, TC-E4-050-04; P3 Test cases listed for criteria this story does not own | CG-ALL-7784, CG-ALL-7785 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 2 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7779 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7780 | HTTP errors with no message ID: 400; 401; 404 for an object outside scope; 503 when a consumed answer or the record library does not answer in time | X5 | Missing | Business analyst |
| CG-ALL-7781 | Activity proceedsReconciliation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7782 | Activity The rule-in-force read is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7784 | Test cases not in Test Cases v8: TC-E4-050-01, TC-E4-050-02, TC-E4-050-03, TC-E4-050-04 | X9 | Missing | QA |
| CG-ALL-7786 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-7787 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7783 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7785 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-7788 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7789 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The rule row of REC-04 or REC-05 is not readable, or no version is in force (covered by 'TC-E4-050-01, TC-E4-050-02' only) | Not specified in the source documents | |
| AC4 | §5 X3: The batch record of the source is absent for the business date, or `is_complete` is not set (covered by 'TC-E4-050-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: rwb-source-data does not answer the payment rows inside 2 s (covered by 'TC-E4-050-01' only) | Not specified in the source documents | |
| AC6 | §5 X5: The owner's `reconciliation_result` read is not available (covered by 'TC-E4-050-01' only) | Not specified in the source documents | |
| AC7 | §5 X6: The run is repeated for the same business date (covered by 'TC-E4-050-01' only) | Not specified in the source documents | |
| AC8 | §5 X7: A key does not resolve in the view (covered by 'TC-E4-050-01' only) | Not specified in the source documents | |
| AC9 | §5 X8: A caller without the right tries the read, or a case outside its scope (covered by 'TC-E4-050-03' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
