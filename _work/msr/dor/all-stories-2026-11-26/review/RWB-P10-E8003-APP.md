# Build-readiness review (script) — RWB-P10-E8003-APP Run a champion and challenger test

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E8003-APP (RWB P10 E8003 APP Run a champion and challenger test v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E8-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 11 (3 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'centre of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'TC-E8-003-03', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR10; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 4 transitions; detcheck: P1 The story adds EVALUATION to the closed list LOV-AGENT-RUN | CG-ALL-2866 |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-2874 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 404 unknown evaluation run; 409 the pair is already running; 422 a required label missing or a label that resolves to no policy row of the agent; 503 store down. The request and response field names of the two version labels and of the comparison on `proposal` are Not specified in the source documents (GAP-0645; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Activity VersionPairRunner is not in Temporal Catalog v1 (+2 more) | CG-ALL-2867, CG-ALL-2868, CG-ALL-2869, CG-ALL-2870, CG-ALL-2871, CG-ALL-2872 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2875 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E8-003-01, TC-E8-003-02, TC-E8-003-03, TC-E8-003-04, TC-E8-003-05, TC-E8-003-06, TC-E8-003-07, TC-E8-003-08, TC-E8-003-09, TC-E8-003-10, TC-E8-003-11, TC-E8-003-12 | CG-ALL-2873 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 2 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Pass | — | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2866 | The story adds EVALUATION to the closed list LOV-AGENT-RUN | X1 | Conflict | Product owner |
| CG-ALL-2867 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2869 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2868 | HTTP errors with no message ID: 404 unknown evaluation run; 409 the pair is already running; 422 a required label missing or a label that resolves to no policy row of the agent; 503 store down. The request and response field names of the two version labels and of the comparison on `proposal` are Not specified in the source documents (GAP-0645 | X5 | Missing | Business analyst |
| CG-ALL-2870 | Activity VersionPairRunner is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2871 | Activity OutcomeComparator is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2872 | Activity ComparisonWriter is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2873 | Test cases not in Test Cases v8: TC-E8-003-01, TC-E8-003-02, TC-E8-003-03, TC-E8-003-04, TC-E8-003-05, TC-E8-003-06, TC-E8-003-07, TC-E8-003-08, TC-E8-003-09, TC-E8-003-10, TC-E8-003-11, TC-E8-003-12 | X9 | Missing | QA |
| CG-ALL-2874 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2875 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2876 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X9: A role without the Rules and parameters right calls a run or a read (covered by 'TC-E8-003-03' only) | Not specified in the source documents | |
| AC13 | §8 BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
