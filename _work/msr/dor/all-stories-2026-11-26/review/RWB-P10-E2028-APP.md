# Build-readiness review (script) — RWB-P10-E2028-APP Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2028-APP (RWB P10 E2028 APP Case intake agent live at L1 [E3a] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-028 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 14 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'TC-E2-028-10', not by a criterion; exception X9 is covered by 'TC-P10-E2028-CON-08', not by a criterion; exception X10 is covered by 'TC-P10-E2028-CON-03', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 7 of 13 rules are covered by no criterion and no test case: BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 30 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-2688 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P2 HTTP errors with no message ID: 401 no session; P1 rwb.agent.AgentRunCompleted.v1 is on topic rwb.agent.events.v1 in the catalog, not rwb.agent.events.v1` with the retry topic and the `.dlt` topic; P2 Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 (+3 more) | CG-ALL-2678, CG-ALL-2679, CG-ALL-2680, CG-ALL-2681, CG-ALL-2682, CG-ALL-2683, CG-ALL-2684 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2689, CG-ALL-2690 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2686 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2685 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E2028-OPS, RWB-P10-E2031-APP); 13 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E2028-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E2031-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2678 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2680 | rwb.agent.AgentRunCompleted.v1 is on topic rwb.agent.events.v1 in the catalog, not rwb.agent.events.v1` with the retry topic and the `.dlt` topic | X6 | Conflict | Solution architect |
| CG-ALL-2682 | Event type rwb.agent.AgentFeedbackRecorded.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2679 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-2681 | Payload of rwb.agent.AgentRunCompleted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2683 | Activity ResolveIntakeMode is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2684 | Activity RecordIntakeFeedback is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2686 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2685 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2687 | Flyway file V10_008__agent_feedback.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2688 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2689 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2690 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2691 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X8: A role without Case record U sends feedback (covered by 'TC-E2-028-10' only) | Not specified in the source documents | |
| AC11 | §5 X9: The rwb-case case record read, the reference-data read or the case-decision proposal does not answer inside the 2 s budg (covered by 'TC-P10-E2028-CON-08' only) | Not specified in the source documents | |
| AC12 | §5 X10: The approved policy row of the segment carries no confidence floor, no segment threshold or no mode (covered by 'TC-P10-E2028-CON-03' only) | Not specified in the source documents | |
| AC13 | §8 BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
