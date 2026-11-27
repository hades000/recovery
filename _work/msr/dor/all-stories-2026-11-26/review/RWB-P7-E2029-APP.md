# Build-readiness review (script) — RWB-P7-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2029-APP (RWB P7 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-029 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 17 (8 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'risk and model risk officer (RW-RISK)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 5 of 15 rules are covered by no criterion and no test case: BR5, BR9, BR10, BR14, BR15; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 23 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-7362 |
| 8 | Contract | Fail | detcheck: P1 POST /decision-log is not in rwb-decision.yaml; P1 GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationRunId} is not published by rwb-agent; P1 GET /api/recovery/agent/v1/agent-runs/{runId} is not published by rwb-agent; P1 GET /api/recovery/case/v1/parameters/{parameterCode} is not published by rwb-case (+6 more) | CG-ALL-7348, CG-ALL-7349, CG-ALL-7350, CG-ALL-7351, CG-ALL-7352, CG-ALL-7353, CG-ALL-7354, CG-ALL-7355, CG-ALL-7356, CG-ALL-7357 |
| 9 | Messages | Partial | §14 lists 9 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's | CG-ALL-7358 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-7363 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC4 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC4; P3 §18 test lists differ from RTM v7 | CG-ALL-7359, CG-ALL-7360, CG-ALL-7361 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2029-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7348 | POST /decision-log is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7349 | GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationRunId} is not published by rwb-agent | X5 | Missing | Solution architect |
| CG-ALL-7350 | GET /api/recovery/agent/v1/agent-runs/{runId} is not published by rwb-agent | X5 | Missing | Solution architect |
| CG-ALL-7351 | GET /api/recovery/case/v1/parameters/{parameterCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7352 | GET /api/recovery/case/v1/reference-data/{listCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-7353 | GET /api/recovery/source-data/v1/... is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-7354 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-7356 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7355 | HTTP errors with no message ID: 401 no session; 404 the record, the item or the case is absent or out of scope | X5 | Missing | Business analyst |
| CG-ALL-7357 | Payload of rwb.decision.ApprovalRequested.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7358 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7360 | Criteria with no test case: AC4 | X9 | Missing | QA |
| CG-ALL-7362 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7359 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7361 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7363 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7364 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR5, BR9, BR10, BR14, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
