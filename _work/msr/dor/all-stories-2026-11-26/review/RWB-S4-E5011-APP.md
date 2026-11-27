# Build-readiness review (script) — RWB-S4-E5011-APP Track hearings, deadlines and fees

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5011-APP (RWB S4 E5011 APP Track hearings, deadlines and fees v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (4 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'BR6', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `scheduled_for` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9242, CG-ALL-9253 |
| 8 | Contract | Fail | POST `/legal-actions/{legalActionId}/hearings` has no idempotency key; PATCH `/legal-actions/{legalActionId}` has no idempotency key; detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/payment/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog (+4 more) | CG-ALL-9243, CG-ALL-9244, CG-ALL-9245, CG-ALL-9246, CG-ALL-9247, CG-ALL-9248, CG-ALL-9249, CG-ALL-9250 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9251 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-19 has no empty, loading, error, no access state in the story; P3 SCR-20 has no empty, loading, error, no access state in the story | CG-ALL-9254, CG-ALL-9255 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-011-01, TC-E5-011-02, TC-E5-011-03, TC-E5-011-04 | CG-ALL-9252 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5011-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9243 | No API Specification v5 yaml has the base of /api/recovery/payment/v1 | X5 | Missing | Solution architect |
| CG-ALL-9244 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-9245 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-9246 | Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9242 | Name `scheduled_for` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9247 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9248 | Activity recordHearing is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9249 | Activity armHearingDeadline is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9250 | Activity recordSpendDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9252 | Test cases not in Test Cases v8: TC-E5-011-01, TC-E5-011-02, TC-E5-011-03, TC-E5-011-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9251 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9253 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9254 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9255 | SCR-20 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9256 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X9: A statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR6' only) | Not specified in the source documents | |
| AC4 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC6 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
