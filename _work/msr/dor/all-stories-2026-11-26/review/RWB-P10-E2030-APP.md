# Build-readiness review (script) — RWB-P10-E2030-APP Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2030-APP (RWB P10 E2030 APP Legal document agent in shadow on Epic 1 data [E3c] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-030 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 18 (9 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E2-030-10', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 2 of 10 rules are covered by no criterion and no test case: BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 9 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/agent/v1/admin/agent-samples is not in rwb-agent.yaml; P1 POST /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml; P1 GET /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml; P1 GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report is not in rwb-agent.yaml (+10 more) | CG-ALL-2740, CG-ALL-2741, CG-ALL-2742, CG-ALL-2743, CG-ALL-2744, CG-ALL-2745, CG-ALL-2746, CG-ALL-2747, CG-ALL-2748, CG-ALL-2749, CG-ALL-2750, CG-ALL-2751 (+2) |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P10-008 text differs from the Error and Message Standard v4 | CG-ALL-2754 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2757 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2756 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2755 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P10-E1058-APP); 10 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E2030-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1058-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2740 | POST /api/recovery/agent/v1/admin/agent-samples is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2741 | POST /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2742 | GET /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2743 | GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2744 | POST /api/recovery/agent/v1/admin/agent-configs is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2745 | POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2746 | GET /api/recovery/agent/v1/admin/agent-configs is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2747 | GET /api/recovery/document/v1/documents/{documentId}/fields is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2749 | rwb.agent.AgentRunCompleted.v1 is on topic rwb.agent.events.v1 in the catalog, not rwb.agent.events.v1`, with the retry topic and the `.dlt` topic | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2748 | HTTP errors with no message ID: 401 no session; 404 an unknown version or evaluation; 503 the store or a consumed contract unavailable. No operation of this story returns the pack or the completeness list (BR1) | X5 | Missing | Business analyst |
| CG-ALL-2750 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2751 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2752 | Activity AssembleLegalPackInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2753 | Activity ScoreLegalPack is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2756 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2754 | MSG-P10-008 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2755 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2757 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X7: A role without the right (covered by 'TC-E2-030-10' only) | Not specified in the source documents | |
| AC11 | §8 BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
