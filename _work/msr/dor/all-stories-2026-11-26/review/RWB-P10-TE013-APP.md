# Build-readiness review (script) — RWB-P10-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P10-TE013-APP (RWB P10 TE013 APP Agent runtime client with fallback v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-agent |
| Legacy key | RWB-TE-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 12 (2 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-TE-013-09', not by a criterion; exception X8 is covered by 'TC-P10-TE013-CON-01', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 7 of 12 rules are covered by no criterion and no test case: BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 11 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-2916 |
| 8 | Contract | Fail | detcheck: P1 POST /agent-steps is not in rwb-agent.yaml; P1 PUT /agent-runs/{runId}/decision-record is not in rwb-agent.yaml; P2 HTTP errors with no message ID: 401 no session or no service identity; 409 a repeated step key whose first run is RUNNING or a run holding another record; 503 the store, the workflow or a consumed contract unavailable. The two operations and the answer member names are fixed by RWB-P10-TE013-CON; P2 Activity ResolveAutonomyMode is not in Temporal Catalog v1 (+2 more) | CG-ALL-2907, CG-ALL-2908, CG-ALL-2909, CG-ALL-2910, CG-ALL-2911, CG-ALL-2912 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-2917 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2913 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1058-APP, RWB-P10-TE013-OPS); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P10-TE013-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-decision; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P10-E1058-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2907 | POST /agent-steps is not in rwb-agent.yaml | X5 | Missing | Solution architect |
| CG-ALL-2908 | PUT /agent-runs/{runId}/decision-record is not in rwb-agent.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2909 | HTTP errors with no message ID: 401 no session or no service identity; 409 a repeated step key whose first run is RUNNING or a run holding another record; 503 the store, the workflow or a consumed contract unavailable. The two operations and the answer member names are fixed by RWB-P10-TE013-CON | X5 | Missing | Business analyst |
| CG-ALL-2910 | Activity ResolveAutonomyMode is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2911 | Activity ApplyAutonomyMode is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2912 | Activity LinkDecisionRecord is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2913 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2914 | Flyway file V10_001__agent_runtime.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2915 | Flyway file V10_002__agent_run_decision_link.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-2916 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2917 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2918 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X7: A role without the right reads agent runs (covered by 'TC-TE-013-09' only) | Not specified in the source documents | |
| AC10 | §5 X8: The step operation is called with no step key or no rule result (covered by 'TC-P10-TE013-CON-01' only) | Not specified in the source documents | |
| AC11 | §8 BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
