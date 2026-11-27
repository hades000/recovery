# Build-readiness review (script) — RWB-P10-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1062-APP (RWB P10 E1062 APP Deviation screening agent in shadow [E2b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-062 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 21 (8 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E1-062-10', not by a criterion; exception X8 is covered by 'TC-P10-E1062-CON-05', not by a criterion; exception X9 is covered by 'TC-P10-E1062-CON-05', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 9 transitions; detcheck: P1 The story adds PR1 to the closed list LOV-DEVIATION | CG-ALL-2605 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 10 roles | — |
| 7 | Data | Pass | §11 has 54 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /agent-runs is not in rwb-agent.yaml; P1 GET /agent-runs/{runId} is not in rwb-agent.yaml; P1 GET /api/recovery/deviation/v1/deviations is not published by rwb-deviation; P1 GET /api/recovery/document/v1/cases/{caseId}/documents` and `/api/recovery/document/v1/documents/{documentId} is not published by rwb-document (+12 more) | CG-ALL-2606, CG-ALL-2607, CG-ALL-2608, CG-ALL-2609, CG-ALL-2610, CG-ALL-2611, CG-ALL-2612, CG-ALL-2613, CG-ALL-2614, CG-ALL-2615, CG-ALL-2616, CG-ALL-2617 (+4) |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2623 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2622 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1058-APP, RWB-P10-TE013-APP); 12 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E1062-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1058-APP, RWB-P10-TE013-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2605 | The story adds PR1 to the closed list LOV-DEVIATION | X1 | Conflict | Product owner |
| CG-ALL-2606 | POST /agent-runs is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2607 | GET /agent-runs/{runId} is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2608 | GET /api/recovery/deviation/v1/deviations is not published by rwb-deviation | X5 | Missing | Solution architect |
| CG-ALL-2609 | GET /api/recovery/document/v1/cases/{caseId}/documents` and `/api/recovery/document/v1/documents/{documentId} is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2610 | GET /api/recovery/decision/v1/rule-models/{n}/{v} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-2612 | Event type rwb.agent.AgentRunStarted.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2614 | Event type rwb.agent.ScreeningProposalRaised.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2611 | HTTP errors with no message ID: 401 no session; 404 an unknown run; 409 a repeat that returns the stored run; 422 a request member missing or a trigger event outside the two of this story; 503 the store or a consumed contract unavailable | X5 | Missing | Business analyst |
| CG-ALL-2613 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2615 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2616 | Activity AssembleScreeningInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2617 | Activity ResolveOwnerRole is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2618 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2619 | Activity CheckScreeningGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2620 | Activity RecordScreeningRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2621 | Activity PublishScreeningEvents is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2623 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2622 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2624 | Flyway file V10_005__evaluation_review_count.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2625 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X7: A role without the right (covered by 'TC-E1-062-10' only) | Not specified in the source documents | |
| AC11 | §5 X8: A consumed contract of section 12.2 does not answer inside its 2 s budget (covered by 'TC-P10-E1062-CON-05' only) | Not specified in the source documents | |
| AC12 | §5 X9: The rwb-decision registry answers no rule package version for R-DEV-02 to R-DEV-06, or the checksum of the fetched packa (covered by 'TC-P10-E1062-CON-05' only) | Not specified in the source documents | |
| AC13 | §8 BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
