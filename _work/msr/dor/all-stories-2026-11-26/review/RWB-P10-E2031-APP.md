# Build-readiness review (script) — RWB-P10-E2031-APP Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-E2031-APP (RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-E2-031 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (1 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'TC-E2-031-08', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 6 of 12 rules are covered by no criterion and no test case: BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 32 data rows; detcheck: P2 Name `agent_run_daily` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `drift_points` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `window_days` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `min_feedback` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-2777, CG-ALL-2778, CG-ALL-2779, CG-ALL-2780, CG-ALL-2789 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; 503 the store or a consumed contract unavailable. The shape of the v2 element, its member types, its paging and its held-date status are fixed by RWB-P10-E2031-CON and its contract tests (ASM-0964); P1 Workflow AgentRunDailyRollupWorkflow is not in Temporal Catalog v1; P2 Activity aggregateAgentRuns (the legacy `agentRunDaily` step) is not in Temporal Catalog v1; P2 Activity agentDrift (the legacy `agentDrift` step) is not in Temporal Catalog v1 (+1 more) | CG-ALL-2781, CG-ALL-2782, CG-ALL-2783, CG-ALL-2784, CG-ALL-2785 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2790 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2786 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1063-APP, RWB-P10-E2031-OPS); 10 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-E2031-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1063-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2782 | Workflow AgentRunDailyRollupWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2777 | Name `agent_run_daily` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2778 | Name `drift_points` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2779 | Name `window_days` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2780 | Name `min_feedback` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2781 | HTTP errors with no message ID: 401 no session; 503 the store or a consumed contract unavailable. The shape of the v2 element, its member types, its paging and its held-date status are fixed by RWB-P10-E2031-CON and its contract tests (ASM-0964) | X5 | Missing | Business analyst |
| CG-ALL-2783 | Activity aggregateAgentRuns (the legacy `agentRunDaily` step) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2784 | Activity agentDrift (the legacy `agentDrift` step) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2785 | Activity dispatchAgentAlerts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2786 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2787 | Flyway file V10_007__agent_monitor_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2788 | Flyway file V10_006__agent_alert.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2789 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2790 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2791 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X6: A role without Platform administration R opens SCR-46 (covered by 'TC-E2-031-08' only) | Not specified in the source documents | |
| AC9 | §8 BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
