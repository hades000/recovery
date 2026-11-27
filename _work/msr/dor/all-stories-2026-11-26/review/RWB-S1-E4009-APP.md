# Build-readiness review (script) — RWB-S1-E4009-APP Approve a route above the limit at committee

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S1-E4009-APP (RWB S1 E4009 APP Approve a route above the limit at committee v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-valuation |
| Legacy key | RWB-E4-009 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 15 (5 P1). AC review rows: 0. Missing criteria: 15.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-009-03', not by a criterion; exception X3 is covered by 'TC-E4-009-01', not by a criterion; exception X4 is covered by 'TC-E4-009-01, TC-S1-E4009-APP-02', not by a criterion; exception X5 is covered by 'TC-E4-009-01', not by a criterion; exception X6 is covered by 'TC-E4-009-01', not by a criterion; exception X7 is covered by 'TC-E4-009-01', not by a criterion; exception X8 is covered by 'TC-S1-E4009-APP-02', not by a criterion; exception X9 is covered by 'TC-S1-E4009-APP-02', not by a criterion; exception X10 is covered by 's17, BR8, BR10, TC-S1-E4009-APP-01', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S1-009-1' has no BR ID; rule row 'BR-S1-009' has no BR ID; rule row 'R-UNI-14' has no BR ID; rule row 'R-UNI-15' has no BR ID; rule row 'R-UNI-38' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; rule row 'R-UNI-41' has no BR ID; 11 of 19 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 19 rules | — |
| 5 | State transitions | Pass | §9 has 13 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8148, CG-ALL-8160 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1; P1 Workflow RouteDecisionWorkflow task queue rwb-valuation` in namespace `rwb-recovery differs from the catalog (+4 more) | CG-ALL-8149, CG-ALL-8150, CG-ALL-8151, CG-ALL-8152, CG-ALL-8153, CG-ALL-8154, CG-ALL-8155, CG-ALL-8156, CG-ALL-8157 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-13 has no empty, loading, error, no access state in the story | CG-ALL-8161 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8159 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-009-01, TC-E4-009-02, TC-E4-009-03, TC-E4-009-04, TC-S1-E4009-APP-01, TC-S1-E4009-APP-02 | CG-ALL-8158 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S1-E4009-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8149 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-8150 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-8151 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-8152 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-8153 | Workflow RouteDecisionWorkflow task queue rwb-valuation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8148 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8154 | Workflow ID form and start rule of RouteDecisionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8155 | Activity checkDelegation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8156 | Activity escalateToCommittee is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8157 | Activity recordCommitteeAnswer is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8158 | Test cases not in Test Cases v8: TC-E4-009-01, TC-E4-009-02, TC-E4-009-03, TC-E4-009-04, TC-S1-E4009-APP-01, TC-S1-E4009-APP-02 | X9 | Missing | QA |
| CG-ALL-8159 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8160 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8161 | SCR-13 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8162 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the right of the operation (U to submit, RA to answer) (covered by 'TC-E4-009-03' only) | Not specified in the source documents | |
| AC4 | §5 X3: The case is not at `ROUTE_D6`, or the amount or the recommended route is absent (covered by 'TC-E4-009-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: No delegation row covers the product, the decision and the amount, or the row is stale (covered by 'TC-E4-009-01, TC-S1-E4009-APP-02' only) | Not specified in the source documents | |
| AC6 | §5 X5: rwb-decision, rwb-case or rwb-access does not answer inside 2 s, or its breaker is open (covered by 'TC-E4-009-01' only) | Not specified in the source documents | |
| AC7 | §5 X6: The amount is at or below the limit (covered by 'TC-E4-009-01' only) | Not specified in the source documents | |
| AC8 | §5 X7: The committee refuses (covered by 'TC-E4-009-01' only) | Not specified in the source documents | |
| AC9 | §5 X8: The item or the submission is repeated with the same `Idempotency-Key` (covered by 'TC-S1-E4009-APP-02' only) | Not specified in the source documents | |
| AC10 | §5 X9: The recommendation changes while the item is open (covered by 'TC-S1-E4009-APP-02' only) | Not specified in the source documents | |
| AC11 | §5 X10: A component, a statement or a test reaches `recovery_case`, `delegation_limit`, another service's schema or a `v_ace_*`  (covered by 's17, BR8, BR10, TC-S1-E4009-APP-01' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
