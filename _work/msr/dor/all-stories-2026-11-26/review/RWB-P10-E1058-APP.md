# Build-readiness review (script) — RWB-P10-E1058-APP Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1058-APP (RWB P10 E1058 APP Agent platform set-up [E1a] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-058 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 20 (5 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X11 is covered by 'TC-E1-058-16', not by a criterion; exception X12 is covered by 'Section 12.2', not by a criterion; exception X13 is covered by 'Section 12.2', not by a criterion; exception X14 is covered by 'Section 12.7', not by a criterion; §7 holds 15 owned criteria in Gherkin; §5 has 15 exception paths | — |
| 4 | Business rules | Partial | 7 of 17 rules are covered by no criterion and no test case: BR11, BR12, BR13, BR14, BR15, BR16, BR17; §8 has 17 rules | — |
| 5 | State transitions | Pass | §9 has 13 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 10 data rows; detcheck: P2 Name `read_case` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2490 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case; P1 GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/access/v1/masking-policies is not published by rwb-access (+10 more) | CG-ALL-2491, CG-ALL-2492, CG-ALL-2493, CG-ALL-2494, CG-ALL-2495, CG-ALL-2496, CG-ALL-2497, CG-ALL-2498, CG-ALL-2499, CG-ALL-2500, CG-ALL-2501, CG-ALL-2502 (+2) |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2508 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2506 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2505 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1058-INF, RWB-P10-E1058-OPS); 14 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E1058-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2491 | GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2492 | GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2493 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2494 | GET /api/recovery/access/v1/masking-policies is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2497 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2490 | Name `read_case` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2495 | HTTP errors with no message ID: 404 an unknown version, evaluation or case; 503 the store or a consumed contract unavailable. The case-output read is delivered here because a run's evidence is read through the owner by RWB-ITG-E1058-ITG | X5 | Missing | Business analyst |
| CG-ALL-2496 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2498 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2499 | Activity ResolveAgentConfig is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2500 | Activity GatherInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2501 | Activity MaskInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2502 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2503 | Activity CheckGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2504 | Activity RecordAgentRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2506 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2505 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2507 | Flyway file V10_001__agent_runtime.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2508 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2509 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X11: A role without the right calls an endpoint (covered by 'TC-E1-058-16' only) | Not specified in the source documents | |
| AC17 | §5 X12: A consumed contract does not answer inside the 2 s client budget, or answers outside its published shape (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC18 | §5 X13: The parameter key or the list version in force names a value the policy does not allow (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC19 | §5 X14: A migration of the service's Flyway sequence fails (covered by 'Section 12.7' only) | Not specified in the source documents | |
| AC20 | §8 BR11, BR12, BR13, BR14, BR15, BR16, BR17 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC21 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
