# Build-readiness review (script) — RWB-P10-E1058-CON Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1058-CON (RWB P10 E1058 CON Agent platform set-up [E1a] - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-058 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 7, Fail 5. Detcheck rows: 21 (6 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead of rwb-agent' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR8; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds ECHO to the closed list LOV-AGENT-RUN | CG-ALL-2510 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows; detcheck: P2 Name `agent_run_daily` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2511 |
| 8 | Contract | Fail | POST `/admin/agent-configs` has no idempotency key; POST `/admin/agent-configs/{versionId}/approve` has no idempotency key; POST `/admin/agent-samples` has no idempotency key; POST `/admin/agent-evaluations` has no idempotency key; POST `/agent-runs/{runId}/feedback` has no idempotency key; detcheck: P1 GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case; P1 GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/access/v1/masking-policies is not published by rwb-access (+10 more) | CG-ALL-2512, CG-ALL-2513, CG-ALL-2514, CG-ALL-2515, CG-ALL-2516, CG-ALL-2517, CG-ALL-2518, CG-ALL-2519, CG-ALL-2520, CG-ALL-2521, CG-ALL-2522, CG-ALL-2523 (+2) |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2530 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2528 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P10-E1058-CON-01, TC-P10-E1058-CON-02, TC-P10-E1058-CON-03, TC-P10-E1058-CON-04, TC-P10-E1058-CON-05, TC-P10-E1058-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-2526, CG-ALL-2527 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2510 | The story adds ECHO to the closed list LOV-AGENT-RUN | X1 | Conflict | Product owner |
| CG-ALL-2512 | GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2513 | GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2514 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2515 | GET /api/recovery/access/v1/masking-policies is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2518 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2511 | Name `agent_run_daily` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2516 | HTTP errors with no message ID: 401 no session; 404 an unknown version, evaluation, run or case; 503 the store or a consumed contract unavailable. Idempotency: the two loads and the approve carry an Idempotency-Key header | X5 | Missing | Business analyst |
| CG-ALL-2517 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2519 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2520 | Activity ResolveAgentConfig is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2521 | Activity GatherInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2522 | Activity MaskInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2523 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2524 | Activity CheckGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2525 | Activity RecordAgentRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2528 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2526 | Test cases not in Test Cases v8: TC-P10-E1058-CON-01, TC-P10-E1058-CON-02, TC-P10-E1058-CON-03, TC-P10-E1058-CON-04, TC-P10-E1058-CON-05, TC-P10-E1058-CON-06 | X9 | Missing | QA |
| CG-ALL-2527 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2529 | Flyway file V10_001__agent_runtime.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2530 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
