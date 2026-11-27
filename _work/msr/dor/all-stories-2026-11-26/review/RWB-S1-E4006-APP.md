# Build-readiness review (script) — RWB-S1-E4006-APP Calculate the payoff and settlement range

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S1-E4006-APP (RWB S1 E4006 APP Calculate the payoff and settlement range v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-valuation |
| Legacy key | RWB-E4-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 19 (6 P1). AC review rows: 1. Missing criteria: 13.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'Section 10; TC-E4-006-03', not by a criterion; exception X2 is covered by 'TC-S1-E4006-APP-02', not by a criterion; exception X4 is covered by 'R-SET-25; TC-S1-E4006-APP-01', not by a criterion; exception X5 is covered by 'TC-S1-E4006-APP-02', not by a criterion; exception X6 is covered by 'TC-S1-E4006-APP-01', not by a criterion; exception X7 is covered by 'Section 12.1', not by a criterion; exception X8 is covered by 'Section 12.2', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 7 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `payoff_as_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_range_low` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_range_high` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-8057, CG-ALL-8058, CG-ALL-8059, CG-ALL-8060, CG-ALL-8072, CG-ALL-8073 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1 (+4 more) | CG-ALL-8061, CG-ALL-8062, CG-ALL-8063, CG-ALL-8064, CG-ALL-8065, CG-ALL-8066, CG-ALL-8067, CG-ALL-8068, CG-ALL-8069 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-8070 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-13 has no empty, loading, error, no access state in the story | CG-ALL-8074 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-006-01, TC-E4-006-02, TC-E4-006-03, TC-E4-006-04, TC-S1-E4006-APP-01, TC-S1-E4006-APP-02 | CG-ALL-8071 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S1-E4006-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8061 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-8062 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-8063 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-8064 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-8065 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-8066 | Workflow RouteDecisionWorkflow task queue rwb-valuation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8057 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8058 | Name `payoff_as_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8059 | Name `settlement_range_low` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8060 | Name `settlement_range_high` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8067 | Workflow ID form and start rule of RouteDecisionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8068 | Activity calculatePayoffAndRange is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8069 | Activity readAccountBalances is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8071 | Test cases not in Test Cases v8: TC-E4-006-01, TC-E4-006-02, TC-E4-006-03, TC-E4-006-04, TC-S1-E4006-APP-01, TC-S1-E4006-APP-02 | X9 | Missing | QA |
| CG-ALL-8072 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8070 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8073 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8074 | SCR-13 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8075 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X1: A role without right U in Treatment and offer, or a case outside the scope (covered by 'Section 10; TC-E4-006-03' only) | Not specified in the source documents | |
| AC4 | §5 X2: The account data product is stale for the business date (covered by 'TC-S1-E4006-APP-02' only) | Not specified in the source documents | |
| AC5 | §5 X4: The account of the case has no row in the ACE account product (covered by 'R-SET-25; TC-S1-E4006-APP-01' only) | Not specified in the source documents | |
| AC6 | §5 X5: `payoff_as_at` is older than the freshness limit (covered by 'TC-S1-E4006-APP-02' only) | Not specified in the source documents | |
| AC7 | §5 X6: The rule set in force carries no floor, or no range for the route set (covered by 'TC-S1-E4006-APP-01' only) | Not specified in the source documents | |
| AC8 | §5 X7: A required element of the request is absent or outside its list (covered by 'Section 12.1' only) | Not specified in the source documents | |
| AC9 | §5 X8: The rwb-source-data read or the rule read does not answer inside 2 s (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
