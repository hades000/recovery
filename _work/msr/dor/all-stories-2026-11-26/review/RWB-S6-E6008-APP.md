# Build-readiness review (script) — RWB-S6-E6008-APP Derecognize and post to the general ledger

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S6-E6008-APP (RWB S6 E6008 APP Derecognize and post to the general ledger v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-debtsale |
| Legacy key | RWB-E6-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 16 (1 P1). AC review rows: 0. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-008-05', not by a criterion; exception X4 is covered by 'X5', not by a criterion; exception X5 is covered by 'X4', not by a criterion; exception X6 is covered by 'X7', not by a criterion; exception X7 is covered by 'X7', not by a criterion; exception X8 is covered by 'Section 17, BR5, BR8', not by a criterion; exception X9 is covered by 'X9', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DS-29' has no BR ID; rule row 'R-DS-30' has no BR ID; rule row 'R-DS-31' has no BR ID; rule row 'R-DS-32' has no BR ID; rule row 'R-DS-33' has no BR ID; 11 of 16 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `account_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10653, CG-ALL-10654, CG-ALL-10665 |
| 8 | Contract | Fail | detcheck: P1 Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of DebtSaleWorkflow are not stated; P2 Activity derecogniseAccounts is not in Temporal Catalog v1; P2 Activity postToLedger is not in Temporal Catalog v1 (+1 more) | CG-ALL-10655, CG-ALL-10656, CG-ALL-10657, CG-ALL-10658, CG-ALL-10659 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 is used with another meaning than the standard's | CG-ALL-10660, CG-ALL-10661 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-25 has no empty, loading, error, no access state in the story; P3 SCR-26 has no empty, loading, error, no access state in the story | CG-ALL-10666, CG-ALL-10667 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10664 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-008-01, TC-E6-008-02, TC-E6-008-03, TC-E6-008-04, TC-E6-008-05, TC-E6-008-06; P3 Test cases listed for criteria this story does not own | CG-ALL-10662, CG-ALL-10663 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S6-E6008-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10655 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10653 | Name `account_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10654 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10656 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10657 | Activity derecogniseAccounts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10658 | Activity postToLedger is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10659 | Activity The outbound item call (name Not specified in the source documents (GAP-3006; ASM-4960)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10661 | MSG-P2-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10662 | Test cases not in Test Cases v8: TC-E6-008-01, TC-E6-008-02, TC-E6-008-03, TC-E6-008-04, TC-E6-008-05, TC-E6-008-06 | X9 | Missing | QA |
| CG-ALL-10664 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10660 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-10663 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-10665 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10666 | SCR-25 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10667 | SCR-26 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10668 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: The role does not hold the Debt sale right of the surface (covered by 'TC-E6-008-05' only) | Not specified in the source documents | |
| AC6 | §5 X4: The account or balance product is stale after a late or failed ACE batch (covered by 'X5' only) | Not specified in the source documents | |
| AC7 | §5 X5: rwb-source-data, rwb-case or rwb-decision does not answer inside 2 s, or its breaker is open (covered by 'X4' only) | Not specified in the source documents | |
| AC8 | §5 X6: ALS or the general ledger rejects the posting (covered by 'X7' only) | Not specified in the source documents | |
| AC9 | §5 X7: The same lot, business date and package version arrive twice, or the same `Idempotency-Key` twice (covered by 'X7' only) | Not specified in the source documents | |
| AC10 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema (covered by 'Section 17, BR5, BR8' only) | Not specified in the source documents | |
| AC11 | §5 X9: The interface row has been changed since the last item, or no interface row is in force at the business date (covered by 'X9' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
