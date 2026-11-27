# Build-readiness review (script) — RWB-S6-E6004-APP Take buyer bids

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S6-E6004-APP (RWB S6 E6004 APP Take buyer bids v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-debtsale |
| Legacy key | RWB-E6-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 19 (9 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'debt buyer and AMC' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Section 17, BR1, BR9', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DS-17' has no BR ID; rule row 'R-DS-18' has no BR ID; rule row 'R-DS-34' has no BR ID; rule row 'R-DS-35' has no BR ID; rule row 'R-DS-39' has no BR ID; 10 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 15 rules | — |
| 5 | State transitions | Fail | §9 has 11 transitions; detcheck: P1 The story adds BIDDING_OPEN to the closed list LOV-LOT-STATUS; P1 The story adds BIDS_RECEIVED to the closed list LOV-LOT-STATUS; P1 The story adds GL_POSTED to the closed list LOV-LOT-STATUS; P1 The story adds LOT_CLOSED to the closed list LOV-LOT-STATUS | CG-ALL-10518, CG-ALL-10519, CG-ALL-10520, CG-ALL-10521 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 18 data rows; detcheck: P2 Name `account_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10522, CG-ALL-10523, CG-ALL-10534 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/partner/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1 (+4 more) | CG-ALL-10524, CG-ALL-10525, CG-ALL-10526, CG-ALL-10527, CG-ALL-10528, CG-ALL-10529, CG-ALL-10530, CG-ALL-10531 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-26 has no empty, loading, error, no access state in the story | CG-ALL-10535 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10533 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-004-01, TC-E6-004-02, TC-E6-004-03, TC-E6-004-04, TC-E6-004-05 | CG-ALL-10532 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S6-E6004-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10518 | The story adds BIDDING_OPEN to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10519 | The story adds BIDS_RECEIVED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10520 | The story adds GL_POSTED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10521 | The story adds LOT_CLOSED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10524 | No API Specification v5 yaml has the base of /api/recovery/partner/v1 | X5 | Missing | Solution architect |
| CG-ALL-10525 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10526 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-10527 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10528 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10522 | Name `account_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10523 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10529 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10530 | Activity takeBid is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10531 | Activity closeLotAfterClaimWindow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10532 | Test cases not in Test Cases v8: TC-E6-004-01, TC-E6-004-02, TC-E6-004-03, TC-E6-004-04, TC-E6-004-05 | X9 | Missing | QA |
| CG-ALL-10533 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10534 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10535 | SCR-26 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10536 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X10: A component, a statement or a test reaches `rwb_case`, `rwb_partner`, `rwb_decision`, `rwb_access`, `rwb_reporting` or a (covered by 'Section 17, BR1, BR9' only) | Not specified in the source documents | |
| AC5 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
