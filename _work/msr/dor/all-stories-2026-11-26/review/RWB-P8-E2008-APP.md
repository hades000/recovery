# Build-readiness review (script) — RWB-P8-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E2008-APP (RWB P8 E2008 APP Payment matching with the missed payment event v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E2-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 24 (4 P1). AC review rows: 2. Missing criteria: 10.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'BR4', not by a criterion; exception X3 is covered by 'BR5', not by a criterion; exception X8 is covered by 'BR9', not by a criterion; exception X9 is covered by 'Section 17', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 5 of 13 rules are covered by no criterion and no test case: BR3, BR4, BR5, BR8, BR11; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 10 data rows; detcheck: P2 Name `payment_missed_event_key` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 (+3 more) | CG-ALL-7506, CG-ALL-7507, CG-ALL-7508, CG-ALL-7509, CG-ALL-7510, CG-ALL-7523, CG-ALL-7524 |
| 8 | Contract | Fail | detcheck: P1 rwb.payment.ProceedsMatched.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, with `.retry` and `.dlt; P1 rwb.payment.PaymentMissed.v1 is on topic rwb.payment.events.v1 in the catalog, not the same topic and its retry and DLT topics; P1 Workflow matchPayments` (JOB-07; name Not specified in the source documents (GAP-2503; ASM-4139)) is not in Temporal Catalog v1; P2 Activity readFacts` (name as above) is not in Temporal Catalog v1 (+3 more) | CG-ALL-7512, CG-ALL-7513, CG-ALL-7514, CG-ALL-7515, CG-ALL-7516, CG-ALL-7517, CG-ALL-7518 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-003; §14 lists 5 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-7519 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-28 has no empty, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7525, CG-ALL-7526, CG-ALL-7527, CG-ALL-7528 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7521 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7520 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 build dependencies are not done yet (RWB-P8-E2008-OPS); 14 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7511 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P8-E2008-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-treatment; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7511 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7512 | rwb.payment.ProceedsMatched.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-7513 | rwb.payment.PaymentMissed.v1 is on topic rwb.payment.events.v1 in the catalog, not the same topic and its retry and DLT topics | X6 | Conflict | Solution architect |
| CG-ALL-7514 | Workflow matchPayments` (JOB-07; name Not specified in the source documents (GAP-2503; ASM-4139)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7506 | Name `payment_missed_event_key` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7507 | Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7508 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7509 | Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7510 | Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7515 | Activity readFacts` (name as above) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7516 | Activity evaluateMatch` (name as above) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7517 | Activity recordAndApply` (name as above) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7518 | Activity raiseMissedPayment` (name as above) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7519 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7521 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-7523 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7520 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7522 | Flyway file V2_008__payment_matching.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7524 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7525 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7526 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7527 | SCR-28 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7528 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7529 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC7 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X2: A payment is on an account with no open case (covered by 'BR4' only) | Not specified in the source documents | |
| AC11 | §5 X3: The ACE batch for ALS is not COMPLETE for the business date (covered by 'BR5' only) | Not specified in the source documents | |
| AC12 | §5 X8: A consumed contract does not answer inside 2 s, or its breaker is open (covered by 'BR9' only) | Not specified in the source documents | |
| AC13 | §5 X9: A component, a statement or a test reaches another service's schema or a view this login does not hold (covered by 'Section 17' only) | Not specified in the source documents | |
| AC14 | §8 BR3, BR4, BR5, BR8, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC17 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
