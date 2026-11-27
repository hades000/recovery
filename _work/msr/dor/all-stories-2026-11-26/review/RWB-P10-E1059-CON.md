# Build-readiness review (script) — RWB-P10-E1059-CON Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E1059-CON (RWB P10 E1059 CON Case intake agent in shadow [E1b] - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E1-059 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 22 (4 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 8 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `read_case` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_documents` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_valuations` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-2562, CG-ALL-2563, CG-ALL-2564, CG-ALL-2565, CG-ALL-2566, CG-ALL-2582 |
| 8 | Contract | Fail | detcheck: P1 POST /agent-runs` - the path is fixed by this document; no source names it (GAP-0611; ASM-0862) is not in rwb-agent.yaml; P1 GET /agent-runs/{runId} is not in rwb-agent.yaml; P1 GET /api/recovery/case/v1/cases/{caseId}/accounts` and `/parties is not published by rwb-case; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access (+7 more) | CG-ALL-2567, CG-ALL-2568, CG-ALL-2569, CG-ALL-2570, CG-ALL-2571, CG-ALL-2572, CG-ALL-2573, CG-ALL-2574, CG-ALL-2575, CG-ALL-2576, CG-ALL-2577 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2578 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2583 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2581 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P10-E1059-CON-01, TC-P10-E1059-CON-02, TC-P10-E1059-CON-03, TC-P10-E1059-CON-04, TC-P10-E1059-CON-05, TC-P10-E1059-CON-06, TC-P10-E1059-CON-07, TC-P10-E1059-CON-08; P3 §18 test lists differ from RTM v7 | CG-ALL-2579, CG-ALL-2580 |
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

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2567 | POST /agent-runs` - the path is fixed by this document; no source names it (GAP-0611; ASM-0862) is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2568 | GET /agent-runs/{runId} is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2569 | GET /api/recovery/case/v1/cases/{caseId}/accounts` and `/parties is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2570 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 14 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2562 | Name `read_case` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2563 | Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2564 | Name `read_documents` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2565 | Name `read_valuations` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2566 | Name `read_contact_points` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2571 | HTTP errors with no message ID: 401 no session; 404 no run for the identifier; 409 a repeat of the run key (R-UNI-40); 503 the store or a consumed contract unavailable. The full run resource, the admin configuration and run reads and the evaluation operations are baselined in RWB-P10-E1058-CON and RWB-P10-TE013-CON | X5 | Missing | Business analyst |
| CG-ALL-2572 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2573 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2574 | Activity BuildIntakeInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2575 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2576 | Activity CheckGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2577 | Activity RecordShadowRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2581 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-2582 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2578 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2579 | Test cases not in Test Cases v8: TC-P10-E1059-CON-01, TC-P10-E1059-CON-02, TC-P10-E1059-CON-03, TC-P10-E1059-CON-04, TC-P10-E1059-CON-05, TC-P10-E1059-CON-06, TC-P10-E1059-CON-07, TC-P10-E1059-CON-08 | X9 | Missing | QA |
| CG-ALL-2580 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2583 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
