# Build-readiness review (script) — RWB-P8-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E2027-APP (RWB P8 E2027 APP Payment matching rules with the data team v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E2-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 17 (5 P1). AC review rows: 0. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'Credit Administration officer (RW-CREDITAD)' is in the roles table | — |
| 2 | Links | Pass | §18 has 7 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by AC5, which this story neither owns nor names as owned by another story; exception X2 is covered by AC4, which this story neither owns nor names as owned by another story; exception X5 is covered by AC8, which this story neither owns nor names as owned by another story; exception X6 is covered by AC9, which this story neither owns nor names as owned by another story; exception X9 is covered by 'TC-E2-027-01', not by a criterion; exception X10 is covered by 'TC-E2-027-02', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 5 of 14 rules are covered by no criterion and no test case: BR10, BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-7564, CG-ALL-7576 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions is not published by rwb-decision; P1 GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision; P2 Payload of rwb.payment.ProceedsMatched.v1 differs from Kafka Catalog v1; P2 Payload of rwb.payment.PaymentMissed.v1 differs from Kafka Catalog v1 (+2 more) | CG-ALL-7565, CG-ALL-7566, CG-ALL-7568, CG-ALL-7569, CG-ALL-7570, CG-ALL-7571, CG-ALL-7572 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-7573 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story; P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-40 has no empty, loading, error, no access state in the story | CG-ALL-7577, CG-ALL-7578, CG-ALL-7579 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7574 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 2 build dependencies are not done yet (RWB-P8-E2008-APP, RWB-P8-E2027-OPS); 14 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7567 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P8-E2027-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P8-E2008-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7565 | GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-7566 | GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-7567 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7571 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7572 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7564 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7568 | Payload of rwb.payment.ProceedsMatched.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7569 | Payload of rwb.payment.PaymentMissed.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7570 | Payload of rwb.payment.TreatmentBooked.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7573 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7574 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-7576 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7575 | Flyway file V2027_2__payment_matching_rules.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7577 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7578 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7579 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7580 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X1: A partial payment below the partial floor (covered by AC5, which exist nowhere in this story) | Not specified in the source documents | |
| AC12 | §5 X2: A late payment one day past the window (covered by AC4, which exist nowhere in this story) | Not specified in the source documents | |
| AC13 | §5 X5: A payment above the installment by more than the tolerance (covered by AC8, which exist nowhere in this story) | Not specified in the source documents | |
| AC14 | §5 X6: Two rows would match (covered by AC9, which exist nowhere in this story) | Not specified in the source documents | |
| AC15 | §5 X9: The `AceDataReady` event of the business date is repeated (covered by 'TC-E2-027-01' only) | Not specified in the source documents | |
| AC16 | §5 X10: The rwb-treatment contract does not answer within 2 s (covered by 'TC-E2-027-02' only) | Not specified in the source documents | |
| AC17 | §8 BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC18 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC19 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC20 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC21 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
