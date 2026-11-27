# Build-readiness review (script) — RWB-P10-E1059-APP Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1059-APP (RWB P10 E1059 APP Case intake agent in shadow [E1b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-059 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 19 (2 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E1-059-09', not by a criterion; exception X8 is covered by 'BR9; section 13', not by a criterion; exception X9 is covered by 'BR8', not by a criterion; exception X10 is covered by 'BR7', not by a criterion; exception X11 is covered by 'BR10', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 6 of 11 rules are covered by no criterion and no test case: BR3, BR7, BR8, BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 11 data rows; detcheck: P2 Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_valuations` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_contact_points` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-2543, CG-ALL-2544, CG-ALL-2545, CG-ALL-2559 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/case/v1/cases/{caseId}/accounts` and `/parties is not published by rwb-case; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1; P2 Workflow ID form and start rule of AgentRunWorkflow are not stated (+4 more) | CG-ALL-2546, CG-ALL-2547, CG-ALL-2548, CG-ALL-2549, CG-ALL-2550, CG-ALL-2551, CG-ALL-2552, CG-ALL-2553 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2554 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2560 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2557 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-2555, CG-ALL-2556 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1058-APP, RWB-P10-TE013-APP); 13 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E1059-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1058-APP, RWB-P10-TE013-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2546 | GET /api/recovery/case/v1/cases/{caseId}/accounts` and `/parties is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2547 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2543 | Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2544 | Name `read_valuations` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2545 | Name `read_contact_points` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2548 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2549 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2550 | Activity BuildIntakeInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2551 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2552 | Activity CheckGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2553 | Activity RecordShadowRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2557 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2554 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2555 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-2556 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2558 | Flyway file V10_004__intake_run_key.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2559 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2560 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2561 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X7: A role without the right starts or reads evaluations (covered by 'TC-E1-059-09' only) | Not specified in the source documents | |
| AC10 | §5 X8: The rwb-source-data, rwb-case or rwb-document contract does not answer inside the 2 s budget (covered by 'BR9; section 13' only) | Not specified in the source documents | |
| AC11 | §5 X9: The policy version in force holds no value for the timeout, the floor or the allowed tools (covered by 'BR8' only) | Not specified in the source documents | |
| AC12 | §5 X10: The outbox relay cannot reach `rwb.agent.events.v1` (covered by 'BR7' only) | Not specified in the source documents | |
| AC13 | §5 X11: The migration `V10_004__intake_run_key.sql` fails in the service's Flyway sequence (covered by 'BR10' only) | Not specified in the source documents | |
| AC14 | §8 BR3, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
