# Build-readiness review (script) — RWB-P10-E1062-CON Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1062-CON (RWB P10 E1062 CON Deviation screening agent in shadow [E2b] - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-062 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 6, Fail 4. Detcheck rows: 20 (7 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /agent-runs is not in rwb-agent.yaml; P1 GET /agent-runs/{runId} is not in rwb-agent.yaml; P1 GET /api/recovery/deviation/v1/deviations is not published by rwb-deviation; P1 GET /api/recovery/document/v1/cases/{caseId}/documents` and `/api/recovery/document/v1/documents/{documentId} is not published by rwb-document (+12 more) | CG-ALL-2626, CG-ALL-2627, CG-ALL-2628, CG-ALL-2629, CG-ALL-2630, CG-ALL-2631, CG-ALL-2632, CG-ALL-2633, CG-ALL-2634, CG-ALL-2635, CG-ALL-2636, CG-ALL-2637 (+4) |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2644 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P10-E1062-CON-01, TC-P10-E1062-CON-02, TC-P10-E1062-CON-03, TC-P10-E1062-CON-04, TC-P10-E1062-CON-05, TC-P10-E1062-CON-06, TC-P10-E1062-CON-07, TC-P10-E1062-CON-08; P3 §18 test lists differ from RTM v7 | CG-ALL-2642, CG-ALL-2643 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2626 | POST /agent-runs is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2627 | GET /agent-runs/{runId} is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2628 | GET /api/recovery/deviation/v1/deviations is not published by rwb-deviation | X5 | Missing | Solution architect |
| CG-ALL-2629 | GET /api/recovery/document/v1/cases/{caseId}/documents` and `/api/recovery/document/v1/documents/{documentId} is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2630 | GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-2632 | Event type rwb.agent.AgentRunStarted.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2634 | Event type rwb.agent.ScreeningProposalRaised.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2631 | HTTP errors with no message ID: 401 no session; 404 an unknown run; 409 a repeat that returns the stored run; 422 a request member missing or a trigger event outside the two of this key; 503 the store or a consumed contract unavailable | X5 | Missing | Business analyst |
| CG-ALL-2633 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2635 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2636 | Activity AssembleScreeningInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2637 | Activity ResolveOwnerRole is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2638 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2639 | Activity CheckScreeningGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2640 | Activity RecordScreeningRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2641 | Activity PublishScreeningEvents is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2644 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2642 | Test cases not in Test Cases v8: TC-P10-E1062-CON-01, TC-P10-E1062-CON-02, TC-P10-E1062-CON-03, TC-P10-E1062-CON-04, TC-P10-E1062-CON-05, TC-P10-E1062-CON-06, TC-P10-E1062-CON-07, TC-P10-E1062-CON-08 | X9 | Missing | QA |
| CG-ALL-2643 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2645 | Flyway file V10_005__evaluation_review_count.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
