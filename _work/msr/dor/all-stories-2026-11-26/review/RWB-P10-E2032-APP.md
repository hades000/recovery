# Build-readiness review (script) — RWB-P10-E2032-APP TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2032-APP (RWB P10 E2032 APP TDR offer-suggestion model through the model gateway [E3e] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-032 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 14 (2 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 15 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR7, BR11; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-ACC-009; §11 has 8 data rows; detcheck: P2 Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-2817, CG-ALL-2828 |
| 8 | Contract | Fail | POST `/api/recovery/agent/v1/<suggestion path>` — Not specified in the source documents (GAP-0633; ASM-0977) has no idempotency key; detcheck: P1 POST /api/recovery/agent/v1/<suggestion path>` — Not specified in the source documents (GAP-0633; ASM-0977) is not in rwb-agent.yaml; P2 Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Workflow ID form and start rule of AgentRunWorkflow are not stated (+3 more) | CG-ALL-2818, CG-ALL-2819, CG-ALL-2820, CG-ALL-2821, CG-ALL-2822, CG-ALL-2823, CG-ALL-2824 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-2829 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2827 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-032-11, TC-E2-032-12, TC-E2-032-13, TC-E2-032-14, TC-E2-032-15, TC-E2-032-16, TC-E2-032-17; P3 §18 test lists differ from RTM v7 | CG-ALL-2825, CG-ALL-2826 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1058-APP, RWB-P10-E2032-INF); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E2032-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1058-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2818 | POST /api/recovery/agent/v1/<suggestion path>` — Not specified in the source documents (GAP-0633; ASM-0977) is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2820 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2817 | Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2819 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2821 | Workflow ID form and start rule of AgentRunWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-2822 | Activity BuildTdrInputs is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2823 | Activity CallModelGateway is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2824 | Activity CheckGuardrail is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2825 | Test cases not in Test Cases v8: TC-E2-032-11, TC-E2-032-12, TC-E2-032-13, TC-E2-032-14, TC-E2-032-15, TC-E2-032-16, TC-E2-032-17 | X9 | Missing | QA |
| CG-ALL-2827 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2826 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2828 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2829 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2830 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §8 BR7, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
