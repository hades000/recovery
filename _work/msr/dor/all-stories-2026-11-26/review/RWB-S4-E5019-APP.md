# Build-readiness review (script) — RWB-S4-E5019-APP Follow the LED auction ladder

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5019-APP (RWB S4 E5019 APP Follow the LED auction ladder v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 17 (1 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'enforcement owner (RW-ENFORCE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E5-019-04', not by a criterion; exception X9 is covered by 'Section 17, BR3, BR6', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-63' has no BR ID; rule row 'R-LIT-65' has no BR ID; rule row 'R-LIT-66' has no BR ID; rule row 'R-LIT-67' has no BR ID; 9 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 14 data rows; detcheck: P2 Name `auction_price_basis` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `official_value` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `round_result` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `bid_amount` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-9474, CG-ALL-9475, CG-ALL-9476, CG-ALL-9477, CG-ALL-9478, CG-ALL-9487 |
| 8 | Contract | Fail | PATCH `/legal-actions/{legalActionId}` has no idempotency key; detcheck: P1 Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of LitigationWorkflow are not stated; P2 Activity openLedAuction is not in Temporal Catalog v1; P2 Activity recordAuctionRound is not in Temporal Catalog v1 (+1 more) | CG-ALL-9479, CG-ALL-9480, CG-ALL-9481, CG-ALL-9482, CG-ALL-9483 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9484 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-19 has no empty, loading, error, no access state in the story; P3 SCR-20 has no empty, loading, error, no access state in the story | CG-ALL-9488, CG-ALL-9489 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-9486 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-019-01, TC-E5-019-02, TC-E5-019-03, TC-E5-019-04, TC-E5-019-05 | CG-ALL-9485 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5019-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_payment, rwb_reporting | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9479 | Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9474 | Name `auction_price_basis` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9475 | Name `official_value` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9476 | Name `round_result` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9477 | Name `bid_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9478 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9480 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9481 | Activity openLedAuction is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9482 | Activity recordAuctionRound is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9483 | Activity closeUnsoldLadder is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9485 | Test cases not in Test Cases v8: TC-E5-019-01, TC-E5-019-02, TC-E5-019-03, TC-E5-019-04, TC-E5-019-05 | X9 | Missing | QA |
| CG-ALL-9486 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9484 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9487 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9488 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9489 | SCR-20 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9490 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X2: The role does not hold the Litigation right of the operation (covered by 'TC-E5-019-04' only) | Not specified in the source documents | |
| AC5 | §5 X9: A component, a statement or a test reaches a `recovery_case` row, an `assignment` row, a `task` row, a `rule_row`, a `de (covered by 'Section 17, BR3, BR6' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
