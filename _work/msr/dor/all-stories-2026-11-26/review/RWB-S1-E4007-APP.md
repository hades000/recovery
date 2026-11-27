# Build-readiness review (script) — RWB-S1-E4007-APP Score the routes and recommend one with reasons

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S1-E4007-APP (RWB S1 E4007 APP Score the routes and recommend one with reasons v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-valuation |
| Legacy key | RWB-E4-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 16 (6 P1). AC review rows: 0. Missing criteria: 15.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-007-03', not by a criterion; exception X3 is covered by 'TC-E4-007-01', not by a criterion; exception X4 is covered by 'TC-E4-007-01', not by a criterion; exception X5 is covered by 'TC-E4-007-01', not by a criterion; exception X6 is covered by 'TC-E4-007-01', not by a criterion; exception X7 is covered by 'TC-E4-007-01', not by a criterion; exception X8 is covered by 'TC-E4-007-01', not by a criterion; exception X9 is covered by 'TC-E4-007-01', not by a criterion; exception X10 is covered by 's17, BR4, BR9', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S1-007-1' has no BR ID; rule row 'BR-S1-007' has no BR ID; rule row 'R-UNI-37' has no BR ID; rule row 'R-UNI-38' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; rule row 'R-UNI-41' has no BR ID; rule row 'R-RES-32' has no BR ID; 10 of 18 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 13 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-DEC-019, DF-DEC-027; §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8093, CG-ALL-8106 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/agent/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1 (+5 more) | CG-ALL-8094, CG-ALL-8095, CG-ALL-8096, CG-ALL-8097, CG-ALL-8098, CG-ALL-8099, CG-ALL-8100, CG-ALL-8101, CG-ALL-8102 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-8103 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-13 has no empty, loading, error, no access state in the story | CG-ALL-8107 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8105 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-007-01, TC-E4-007-02, TC-E4-007-03, TC-E4-007-04, TC-S1-E4007-APP-01, TC-S1-E4007-APP-02, TC-S1-E4007-APP-03 | CG-ALL-8104 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S1-E4007-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_agent, rwb_case, rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8094 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-8095 | No API Specification v5 yaml has the base of /api/recovery/agent/v1 | X5 | Missing | Solution architect |
| CG-ALL-8096 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-8097 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-8098 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-8099 | Workflow RouteDecisionWorkflow task queue rwb-valuation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8093 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8100 | Workflow ID form and start rule of RouteDecisionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8101 | Activity scoreRoutes is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8102 | Activity recommendRoute is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8104 | Test cases not in Test Cases v8: TC-E4-007-01, TC-E4-007-02, TC-E4-007-03, TC-E4-007-04, TC-S1-E4007-APP-01, TC-S1-E4007-APP-02, TC-S1-E4007-APP-03 | X9 | Missing | QA |
| CG-ALL-8105 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8103 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8106 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8107 | SCR-13 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8108 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the Treatment and offer right of the operation (covered by 'TC-E4-007-03' only) | Not specified in the source documents | |
| AC4 | §5 X3: The agent answer fails the allowed-action check, names a route outside the open set, or falls below the confidence thres (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: rwb-agent does not answer inside 2 s, or its breaker is open (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC6 | §5 X5: The ACE data product is stale after a late or failed batch (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC7 | §5 X6: A route of the open set has no COLLINS return, or the range is absent (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC8 | §5 X7: The case is not at the route decision, or a route of the recommendation is barred on the case (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC9 | §5 X8: The same assessment is submitted twice with the same `Idempotency-Key` (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC10 | §5 X9: rwb-source-data, rwb-agent, rwb-case or rwb-decision does not answer inside 2 s (covered by 'TC-E4-007-01' only) | Not specified in the source documents | |
| AC11 | §5 X10: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 's17, BR4, BR9' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
