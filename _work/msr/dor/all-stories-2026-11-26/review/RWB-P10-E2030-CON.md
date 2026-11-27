# Build-readiness review (script) — RWB-P10-E2030-CON Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2030-CON (RWB P10 E2030 CON Legal document agent in shadow on Epic 1 data [E3c] - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-030 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 8, Fail 4. Detcheck rows: 19 (9 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | 12 row(s) of §11 have no BR Field ID; §11 has 12 data rows | — |
| 8 | Contract | Fail | POST `/api/recovery/agent/v1/agent-runs` has no idempotency key; POST `/api/recovery/agent/v1/admin/agent-samples` has no idempotency key; POST `/api/recovery/agent/v1/admin/agent-evaluations` has no idempotency key; POST `/api/recovery/agent/v1/admin/agent-configs` and `/admin/agent-configs/{versionId}/approve` has no idempotency key; detcheck: P1 POST /api/recovery/agent/v1/agent-runs is not in rwb-agent.yaml; P1 GET /api/recovery/agent/v1/agent-runs/{runId} is not in rwb-agent.yaml; P1 POST /api/recovery/agent/v1/admin/agent-samples is not in rwb-agent.yaml; P1 POST /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml (+10 more) | CG-ALL-2758, CG-ALL-2759, CG-ALL-2760, CG-ALL-2761, CG-ALL-2762, CG-ALL-2763, CG-ALL-2764, CG-ALL-2765, CG-ALL-2766, CG-ALL-2767, CG-ALL-2768, CG-ALL-2769 (+2) |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P10-008 text differs from the Error and Message Standard v4 | CG-ALL-2772 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2776 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2775 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P10-E2030-CON-01, TC-P10-E2030-CON-02, TC-P10-E2030-CON-03, TC-P10-E2030-CON-04, TC-P10-E2030-CON-05, TC-P10-E2030-CON-06, TC-P10-E2030-CON-07; P3 §18 test lists differ from RTM v7 | CG-ALL-2773, CG-ALL-2774 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2758 | POST /api/recovery/agent/v1/agent-runs is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2759 | GET /api/recovery/agent/v1/agent-runs/{runId} is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2760 | POST /api/recovery/agent/v1/admin/agent-samples is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2761 | POST /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2762 | GET /api/recovery/agent/v1/admin/agent-evaluations is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2763 | GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2764 | POST /api/recovery/agent/v1/admin/agent-configs` and `/admin/agent-configs/{versionId}/approve is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2765 | GET /api/recovery/document/v1/documents/{documentId}/fields is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2767 | rwb.agent.AgentRunCompleted.v1 is on topic rwb.agent.events.v1 in the catalog, not rwb.agent.events.v1` with the retry topic and the `.dlt` topic | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2766 | HTTP errors with no message ID: 401 no session; 404 an unknown run, version or evaluation; 409 a self-approval or a second evaluation; 422 a failed check or an empty sample; 503 a store or a consumed contract unavailable | X5 | Missing | Business analyst |
| CG-ALL-2768 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2769 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2770 | Activity AssembleLegalPackInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2771 | Activity ScoreLegalPack is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2775 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2772 | MSG-P10-008 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2773 | Test cases not in Test Cases v8: TC-P10-E2030-CON-01, TC-P10-E2030-CON-02, TC-P10-E2030-CON-03, TC-P10-E2030-CON-04, TC-P10-E2030-CON-05, TC-P10-E2030-CON-06, TC-P10-E2030-CON-07 | X9 | Missing | QA |
| CG-ALL-2774 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2776 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
