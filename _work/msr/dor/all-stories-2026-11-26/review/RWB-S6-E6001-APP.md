# Build-readiness review (script) — RWB-S6-E6001-APP Approve lots, reserve and tiered terms

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S6-E6001-APP (RWB S6 E6001 APP Approve lots, reserve and tiered terms v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-debtsale |
| Legacy key | RWB-E6-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 13 (6 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR7', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DS-06' has no BR ID; rule row 'R-DS-04' has no BR ID; rule row 'R-DS-07' has no BR ID; rule row 'R-DS-08' has no BR ID; 10 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 18 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10439 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog (+3 more) | CG-ALL-10429, CG-ALL-10430, CG-ALL-10431, CG-ALL-10432, CG-ALL-10433, CG-ALL-10434, CG-ALL-10435, CG-ALL-10436 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-25 has no empty, loading, error, no access state in the story; P3 SCR-26 has no empty, loading, error, no access state in the story | CG-ALL-10440, CG-ALL-10441 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10438 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-001-01, TC-E6-001-02, TC-E6-001-03, TC-E6-001-04, TC-E6-001-05, TC-E6-001-06 | CG-ALL-10437 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S6-E6001-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10429 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10430 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10431 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-10432 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10433 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |
| CG-ALL-10435 | Workflow The committee branch of `DebtSaleWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10434 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10436 | Activity recordCommitteeApproval is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10437 | Test cases not in Test Cases v8: TC-E6-001-01, TC-E6-001-02, TC-E6-001-03, TC-E6-001-04, TC-E6-001-05, TC-E6-001-06 | X9 | Missing | QA |
| CG-ALL-10438 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10439 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10440 | SCR-25 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10441 | SCR-26 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X8: A statement reaches `rwb_decision`, `rwb_access`, `rwb_case` or another service's schema (covered by 'Section 17, BR7' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
