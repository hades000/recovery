# RWB-S7-E6027-CON Record a customer payment after charge-off - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement (no size in this story) |
| Contract version | v1 (the /v1 base paths and the .v1 topic and event names) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the post charge-off recovery of rwb-writeoff, split from RWB-E6-027. It fixes the consumed payment event element on `rwb.payment.events.v1`, the `write_off` recovery element over the fields DF-FIN-010 to DF-FIN-020 with `recovered_after`, `posted_date` and `decision_log_id`, the fee reference read as reference data, the case-move answer on the child-workflow boundary, the two consumed REST rows with their placeholders, the decision-record element of DP-03, the rights of TSD S7 T6.1, the eight fakes and the absence tests for a published event, a second topic and a Schedule. No REST operation is declared, because no source publishes a recovery operation for the service; DP-04, DP-07, DP-09 and DP-16 are recorded and the plan's C row is None while two rows and one event are consumed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6027-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 12 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect**, I want **the published contract baseline of the post charge-off recovery of rwb-writeoff — the consumed payment event element, the write-off recovery element, the fee reference, the case-move answer, the consumed rows, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a state, a consumed row or an event shape can never drift between rwb-writeoff, rwb-payment, rwb-source-data and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the same discipline applies to a consumed event. The legacy post charge-off payment of RWB-E6-027 crossed four boundaries at once: the receipt, the ACE payment and account facts, the placement and its fee, and the case, and its Endpoints table named the scan and the committee decision with the monolith base and no element of its own. The target splits them: rwb-payment owns the receipt, its match and the posting of the proceeds, rwb-source-data owns the ACE facts, rwb-case owns the case, its route states and the reference data, rwb-partner owns the placement and the fee story, and rwb-writeoff owns the recovery column, the record and the case-move answer. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, event name `rwb.writeoff.WriteOffApproved.v1` for the approval path only, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_payment`, so DP-05 is declared as a read through the owner's contract.

Four points are carried as gaps and assumptions rather than decided quietly: the consumed payment event has no published name or payload (ASM-5115); the ACE read, the reference-data read and the posting activity have no published operation names (ASM-5116, ASM-5117, ASM-5120); the agency fee has no column and is also claimed by rwb-partner's FEAT-PRM-07 (GAP-3048; ASM-5118, ASM-5124); and no event carries the recovery to reporting (ASM-5122).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the idempotency rule and the CloudEvents envelope are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` is P3's, `write_off` is S7's, `payment` and `proceeds` are P8's, `partner` is S9's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's and `notice` is P6's.
- The rwb-payment event and its posting activity, the rwb-source-data read, the rwb-case move and the rwb-case reference data are published with their fakes, so every consumed element names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3048; ASM-5115, ASM-5116, ASM-5117, ASM-5120, ASM-5121).
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The WO package and its rows R-WO-37 and R-WO-49 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the element section of rwb-writeoff for this step: the consumed payment event, the recovery element, the fee reference, the case-move answer, the record element and the errors.
2. Fix the consumed event element: its name and topic derived from the naming rule, its payload placeholders, its CloudEvents envelope, its no-personal-data rule and its inbox treatment.
3. Fix the `write_off` recovery element over the columns of DF-FIN-010 to DF-FIN-020, with `recovered_after`, `posted_date`, `state` and `decision_log_id` as the four properties this step writes, and record that no column is added.
4. Fix the fee reference as a consumed reference-data row of the fee schedule, and the case-move answer as the stage outcome of the child workflow.
5. Fix the two consumed rows: the rwb-source-data read and the rwb-case reference-data read, and the consumed `postProceeds` activity on the P8 queue, marking with the placeholder what the sources do not give.
6. Record the decision-record element of DP-03, written before the case moves and before the column changes, and the rights of the capability area.
7. Record that the step publishes no event, that `WriteOffApproved` (`EV-24`) stays the approval path's, and that the recovery has no reporting event.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` or `proceeds` write, the drift between a fake and the document, and the absence of a published event and of a Schedule.
10. Tag the baseline and hand it to RWB-S7-E6027-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or element fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed element has a name or a payload the sources do not give | The element carries the placeholder and the fake is derived from the published document | None | AC1, AC3 |
| X5 | The recovery is declared as a new topic, its own event or a new table | The absence test fails the build | None | AC5, AC7 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a `payment` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC2, AC3 |
| X7 | The document declares a Schedule, a second topic or a published event of this step | The absence test fails the build | None | AC5, AC7 |
| X8 | The rights of the read path are not the ones TSD S7 T6.1 gives the capability area | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-payment, rwb-source-data and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the base, the topic, the schema, the rights and the state values are fixed by the architecture and the rule package |
| Valuable | Unblocks RWB-S7-E6027-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-payment, rwb-source-data and rwb-case teams on the same day |
| Estimable | One element document, nine contract tables, eight fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the post charge-off recovery of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of payment and proceeds is P8, of recovery_case is P3, of partner is S9 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The consumed payment event element is declared with its shape and its placeholders (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the topic naming rule, the payment ownership of P8 and the connection matrix row S7
    Then the element is declared as consumed from P8 rwb-payment on rwb.payment.events.v1, with its retry and .dlt topics
    Then the element declares the payment reference, the case reference, the account reference, the payment date, the amount and the placement reference, and no personal field
    Then the event name and the payload beyond those properties are Not specified in the source documents (GAP-3047; ASM-5115) and the element carries the placeholder
    Then the element is declared as written to the inbox in the same rwb_writeoff transaction as the recovery, with one consumer group of this service and the repeated delivery dropped by the inbox key
    Then the element declares no outbox row and no publication of its own

  Scenario: AC2 The recovery element is fixed over the write-off columns and no column is added (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1, T3.0 and the write_off field list
    Then the element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then the step's own properties are recovered_after, posted_date, decision_log_id and the standard state, and amount, tax_criteria_met, committee_date and the three posting parameters are declared as read only
    Then recovered_after is declared as the post charge-off recovery amount and posted_date as the date the posting activity confirms
    Then the element declares no new column, no new table and no migration, and no property for the agency fee
    Then an element test fails a build that adds a write_off property, renames one of the eleven or declares the fee as a column

  Scenario: AC3 The consumed rows and the case boundary are declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack and the connection matrix row S7
    Then the payment, account and customer read is declared as consumed from P1 rwb-source-data, with the fields DF-ACE-001 to DF-ACE-074 of v_ace_payment, v_ace_account and v_ace_customer
    Then the fee schedule and the placement read is declared as consumed from the reference-data contract of P3 rwb-case under the default ruling, with the partner fields DF-PRT-001 to DF-PRT-007 and the fee version
    Then the postProceeds activity is declared as consumed on the P8 queue with the case, the account, the recovery amount and the income code in and the posting reference and posted date out
    Then the case-move answer is declared as the stage outcome of the child workflow to P3 rwb-case, carrying PAYMENT_MATCHED with the rule ID and its version
    Then the operation names of the two rows and of the activity are Not specified in the source documents (GAP-3047; ASM-5116, ASM-5117, ASM-5120) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no payment or proceeds property, no partner property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T-A.1, T6.1, T6.2 and the legacy permission table
    Then the step is declared as run by the rwb-writeoff service identity with no user act, as the FSD names it None; runs unattended
    Then RW-CREDITAD is declared the other user, holding CRUA on Write-off and posting, and RW-WRITEOFF, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold the rights T6.1 gives them
    Then every other role and every SY-* service identity of TSD S7 T6.1 holds R or U as the matrix gives it
    Then the A and C rights of the capability area are declared as the committee decision's and the scan's, and not this step's
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition of MSG-P1-001, MSG-GEN-001, MSG-P4-002 and MSG-P7-003

  Scenario: AC5 The decision-record element and the fee reference are declared, and the step publishes no event (new, D-RCV-60)
    Given the record, fee and event sections of the baseline
    When they are compared with the library schema, the reference-data rule and the topic naming rule
    Then one decision record is declared per rule outcome with the case reference, the write-off reference, the payment reference, the recovery amount, the rule ID and its version, the package version in force, the fee reference and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the row changes, and a failed write leaves everything unchanged with MSG-P7-003
    Then the fee reference is declared as a property of the record only, read from the fee schedule at its version, with no write_off property and no fee value as a schema default
    Then the WriteOffApproved element of EV-24 is declared as the approval path's on rwb.writeoff.events.v1 and is not raised by this step
    Then no event, no outbox row and no second topic is declared for the recovery, and the reporting gap is recorded (GAP-3047; ASM-5122)
    Then the record carries no rule row, no state threshold as a literal and no person name

  Scenario: AC6 The eight fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation, the event or the element it serves
    Then the rwb-payment event fake answers a payment matched to case RC-2027-000712 and its placement, a payment matched to closed case RC-2027-000744 with no placement, a payment that matches nothing and the same event twice
    Then the rwb-payment posting stub answers a confirmed posting, a timeout and a refusal
    Then the rwb-source-data fake answers the facts of the two cases, a contradicting fact set and no answer beyond 2 s
    Then the rwb-case reference-data fake answers a fee schedule row with its version, no row and a stale version, and the case-move fake answers PAYMENT_MATCHED accepted and refused
    Then the package fixture answers R-WO-37 and R-WO-49 at their version, the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 approved state
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed, and no published event and no Schedule are declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, inbox_event and idempotency_key, and recovery_case, payment, proceeds, partner, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no REST operation of this step, no published event, no second topic and no Schedule, and it names JOB-16 as RWB-S7-E6013-APP's
    Then the absence test fails a build that adds an operation of the step, a published event, a second topic, a Schedule, a v_ace_* read or a write to another service's table
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6027-APP and copy no criterion of the legacy story, whose four criteria stay with the app story word for word. The baseline declares a consumed event and no operation and no published event of the step, which is what the sources give (GAP-3046; ASM-5114, ASM-5122).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The recovery is rwb-writeoff's, and the contract declares the properties and the required flags on the recovery element, the consumed event element and the case-move answer only | TSD S7 T3.1 and T3.0; context pack ownership row `write_off` |
| BR2 | The decision record is declared as an element written before the write-off row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy RWB-E6-027 AC1 to AC4 |
| BR3 | The payment, its match and the posting stay with rwb-payment: the contract declares `ProceedsMatched` (`EV-25`) as the consumed match and the `postProceeds` activity as consumed, holds an unmatched payment in the exception list this module shows, and declares no receipt and no proceeds property; the owner of the initial match is an open question with the P8 owner | FEAT-PAY-01; context pack connection matrix, row S7; FSD S7 A2.15; Architecture v5 slides 40 and 43 |
| BR4 | The ACE facts stay with rwb-source-data: the contract declares the read as consumed and declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read | DP-05; ASM-5116 |
| BR5 | The fee schedule stays with reference data: the contract declares the row as consumed with its version and declares the fee reference on the record only, because no source gives the fee a `write_off` column; the fee calculation is the rwb-partner feature FEAT-PRM-07 and is not declared here, and the fee ownership question is open with the solution architect | DF-PRT-001 to DF-PRT-007; ASM-5117, ASM-5124 |
| BR6 | The case stays with rwb-case: the contract declares the case-move answer as consumed and declares no `recovery_case` property and no case state write | ASM-5121; TSD S7 T4 |
| BR7 | The step publishes no event: `WriteOffApproved` (`EV-24`) is the approval path's on `rwb.writeoff.events.v1`, and the recovery's reporting gap is recorded rather than closed with a name the sources do not give | TSD S7 T5.3; DP-14; ASM-5122 |
| BR8 | A consumed event declares its topic, its retry and `.dlt` topics, its CloudEvents envelope, its consumer group and its inbox, and declares no outbox of its own | DP-09 as a platform object; ASM-5115 |
| BR9 | No personal data in a schema, an example, a payload or a fake: identifiers, amounts, dates, a code and a rule version only, and every example is synthetic; a property the data catalogue classes as personal data is removed before the tag | Template and Rules v1 §R7.2 (s17); TSD S7 T6.2 |
| BR10 | One base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists no operation of this step as provided, and a consumed operation or activity is described as consumed and faked, never as provided | DP-01, DP-11; ASM-5114 |
| BR13 | The act is the service identity's and no user right is declared for it; the read rights of the capability area stay the ones TSD S7 T6.1 gives them | TSD S7 T6.1, T6.2; FSD S7 A2.15.3.3 |
| BR14 | The states `PLACED_WITH_AGENCY`, `CASE_CLOSED` and `PAYMENT_MATCHED` are declared as the vocabulary of the answer and of the machine | TSD S7 T4; Business Rules and Routing Logic v4 rows R-WO-37 and R-WO-49 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The consumed event, the recovery element, the fee reference, the case boundary, the record element, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-payment, rwb-source-data and rwb-case accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional payment reference | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the fee becomes a schema default | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC5 and AC7 fail: a published event, a second topic, a Schedule, a `v_ace_*` view or another service's table | In review |

The state machine the document describes is the app story's: `PLACED_WITH_AGENCY` and `CASE_CLOSED` are the from states of R-WO-37 and R-WO-49, `PAYMENT_MATCHED` their to state, and the states before and after — `APPROVED`, `POSTED`, `SOLD_POST_CHARGEOFF` — follow from steps this baseline does not declare (TSD S7 T4). This document fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the element baseline and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the two consumed rows, the consumed event and the absent DP-04, DP-07, DP-09 and DP-16 rows |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-payment, rwb-source-data and rwb-case) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule, the decision-record library and the inbox and outbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an event, an element, an example or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Recovery element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` | BR1 |
| Consumed event element | The payment reference, the case reference, the account reference, the payment date, the amount and the placement reference; the name and the payload beyond these properties are Not specified in the source documents (GAP-3047; ASM-5115) | BR3, BR8 |
| Fee element | The fee schedule row of the placement: the partner code, the panel status, the contract end, the fee basis and the version; the fee reference only, with no fee property on `write_off` | BR5 |
| Case-move element | The stage outcome to rwb-case: the case reference, the move `PAYMENT_MATCHED`, the rule ID `R-WO-37` or `R-WO-49` with its version and the decided-at time | BR6, BR14 |
| Required flags | `id`, `case_id`, `amount` and `tax_criteria_met` required on the recovery element; the case reference, the payment reference and the rule ID required on the event element; the other properties optional | BR1, BR11 |
| Lists | None: TSD S7 T3.2 publishes no list of values, so the baseline declares no enumeration beyond the state vocabulary of the answer | BR14 |
| Event and record data | The inbox row of the consumed event and the decision record of DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) | BR2, BR8 |
| Case, payment and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, the payment and proceeds fields of P8, DF-PRT-001 to DF-PRT-007 of `partner` in S9, DF-ACE-001 to DF-ACE-074 of the three views in P1 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | BR3, BR4, BR5, BR6 |
| Not declared here | `recovery_case` and `queue` (P3), `payment` and `proceeds` (P8), `partner` (S9), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) | BR1, BR3, BR4, BR6 |
| Consumed fields with no source | The event name and payload, the two operation names, the posting activity name and the agency fee column: Not specified in the source documents (GAP-3047, GAP-3048; ASM-5115, ASM-5116, ASM-5117, ASM-5120, ASM-5124) | BR7 |

The field-level types, lengths and required flags of the consumed elements are settled in the baseline review; this story fixes the element names, the property rule of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story. The case boundary is the outcome of the rwb-case child workflow; the fee element is a consumed reference-data row; the event name, the payload and the three placeholder operation and activity names are confirmed with their owners before the tag.

### 12. Contract

#### 12.1 REST operations provided

None. No source publishes a recovery operation for rwb-writeoff: TSD S7 T-A.1 lists only `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A), which are RWB-S7-E6013-APP's and RWB-S7-E6018-APP's, and the legacy Endpoints table repeats those same two rows for this story. The base `/api/recovery/writeoff/v1` (DP-13) is nevertheless fixed here, because the module's operations and the composite route both sit on it, and the absence of an operation of this step is the finding of the baseline (GAP-3046; ASM-5114).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The payment, account and customer read (operation name Not specified in the source documents (GAP-3047; ASM-5116)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The fields of `v_ace_payment`, `v_ace_account` and `v_ace_customer` that prove the match; faked |
| The fee schedule and placement read (operation name Not specified in the source documents (GAP-3047; ASM-5117)) | `/api/recovery/case/v1` | P3 rwb-case, reference data under the default ruling | The `partner` fields DF-PRT-001 to DF-PRT-007, the fee basis and the version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3048).

#### 12.3 Events published

None. `WriteOffApproved` (`EV-24`) is the service's only published event, it is the approval path's on `rwb.writeoff.events.v1` as `rwb.writeoff.WriteOffApproved.v1`, and it is declared here as another story's. No source gives the recovery an event name or a payload, so the recovery is not published under a name the baseline would invent; the reporting gap is recorded with the proposal to allocate one event on the same topic (GAP-3047; ASM-5122).

#### 12.4 Events consumed

| Event | Topic | Owner | Payload element | Consumer |
|---|---|---|---|---|
| The payment received after charge-off event (event name Not specified in the source documents (GAP-3047; ASM-5115)) | `rwb.payment.events.v1`, with its retry and `.dlt` topics | P8 rwb-payment | The payment reference, the case reference, the account reference, the payment date, the amount and the placement reference, in a CloudEvents envelope, with no personal data | rwb-writeoff, one consumer group, one inbox row, the repeated delivery dropped |

The event is declared as written to the inbox in the same `rwb_writeoff` transaction as the recovery, and the step declares no outbox row and no publication (DP-09 as a platform object behind the inbox: ASM-5115).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | The stage that hosts the recovery branch; its signals and its outcome for the parent are declared, not built |
| `applyPostChargeOffRecovery` | Activity, the one recovery step | `rwb-writeoff` | The payment, the `write_off` row, the fee row and the package version in; the rule ID with its version, the recovery amount, the posted date, the state and the case move out |
| `postProceeds` | Activity, consumed on rwb-payment's queue | `rwb-payment` (P8) | The case, the account, the recovery amount and the income code in; the posting reference and the posted date out; declared as another service's and not registered here |

No child workflow for the case and none for the money exists in this service. The local activity name is a target design choice; `postProceeds` is the payment activity the Temporal and Drools Design slide 12 names in the L4 activity contracts. No activity is registered by this story.

Workflow ID form: Not specified in the source documents (CG-ALL-11221). Start rule: the Temporal Catalog v1 row reads 'JOB-16 on the third working day after AceDataReady (R-WO-01)' (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040). Duplicate-start policy: Not specified in the source documents (CG-ALL-11221).

#### 12.6 Schedules

None. The step is event-driven and this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. `JOB-16`, the write-off scan on the third working day, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP and is named here only as another story's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its fields and its dates; the table the recovery element is drawn from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the match, the recovery amount and the fee reference (DP-03) |
| inbox_event | PLT library, created in `rwb_writeoff` | The row of the consumed payment event and its idempotency key |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated delivery and the answer it holds |

`recovery_case` and `queue` (P3), `payment` and `proceeds` (P8), `partner` (S9), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `notice` (P6) are not owned by this baseline; it names them only as consumed rows, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment event fake | A payment matched to case RC-2027-000712 and its placement, a payment matched to closed case RC-2027-000744 with no placement, a payment that matches nothing, and the same event delivered twice | AC1, AC6 |
| rwb-payment posting stub | A confirmed posting with its reference and posted date, a timeout, and a refusal | AC3, AC6 |
| rwb-source-data read fake | The fields of the three views for the two cases, a contradicting fact set, and no answer beyond 2 s | AC3, AC6 |
| rwb-case reference-data fake | A fee schedule row with its version, no row for the placement, and a stale version | AC3, AC5, AC6 |
| rwb-case case-move fake | The move `PAYMENT_MATCHED` accepted with the rule version, and a move refused because the case has already moved | AC3, AC6 |
| WO package fixture | The package at its version in force with R-WO-37 and R-WO-49 among its 51 rules over 27 states | AC2, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off WO-2027-000221 in its approved state, with the recovery, the posting date and the fee reference | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The names of the consumed event, the two consumed operations and the posting activity carry the placeholder until their owners confirm them (GAP-3047; ASM-5115, ASM-5116, ASM-5117, ASM-5120).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The rwb-source-data payment read and the rwb-case reference-data read of the fee schedule; one hop, 2 s |
| Kafka | 0 published, 1 consumed | The payment received after charge-off event on `rwb.payment.events.v1` through the inbox; the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 2 workflows and 1 activity declared, 1 consumed, 0 registered | `WriteOffWorkflow`, `applyPostChargeOffRecovery` and the case child boundary on `rwb-writeoff`, and `postProceeds` on the P8 queue as another service's; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no amount, no fee and no rule package. What it publishes is one element baseline, nine contract tables and eight fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row changes. DP-05 is declared as the rwb-source-data read, because the views are read only by P1 and this service holds no `v_ace_*` grant. DP-13 fixes the base the module's operations and the composite route sit on, even though this step declares none of them. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-07, DP-09 and DP-16 are not in the pattern set: the package is a governed copy, the fee schedule a consumed reference-data row, the inbox a library object behind the consumed event, and the posting another service's activity (GAP-3048; ASM-5115, ASM-5117, ASM-5119, ASM-5120).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the inbox library that the consumed event needs and the Drools kit rows that an embedded evaluation would add. The two consumed rows and the consumed event are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the consumed event element of AC1 with its placeholder, its envelope, its consumer group and its inbox rule.
2. Write the recovery element, the required flags and the no-new-column rule of AC2, with the placeholder where a type or a length is unstated.
3. Record the two consumed rows, the posting activity and the case boundary of AC3 with their owner, their budget and their placeholders.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element, the fee reference and the no-published-event rule of AC5, and validate the record against the library schema.
6. Publish the eight fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are the element baseline of `rwb-writeoff-v1`, the four elements, the contract README rows for the two consumed rows and the consumed event with their placeholders, and the eight fakes of 12.8.

**Done when.** The element baseline validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27, the wave 4 harness and the owners of rwb-payment, rwb-source-data and rwb-case have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The contract describes the stale-product state of a data product behind the read (VR-S7-015-1) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required field of the event element or the read is absent or invalid, or an element fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the read path declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the write-off row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001, whose text is copied from the Error and Message Standard v4 section 4; MSG-P1-001 is the stale-product message of FSD S7 A2.15.3.1. No other message is reworded and no new one is added. Every error condition of the contract is bound to one of these IDs: MSG-GEN-001 for an absent or invalid field and a schema failure, MSG-P4-002 for a role without the right, MSG-P7-003 for a decision that cannot be recorded, and MSG-P1-001 for a stale product.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its approved state through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its recovery and its fee reference, rwb-case for the case and its route state, and rwb-payment for the receipt and the posting; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": this step's outcome is shown inside the approved state, the step itself is unattended, and no screen of this key shows a post charge-off recovery at the population level (GAP-3046). The refusal, invalid-element, stale-product and not-recorded states read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-11228).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-027-01 | AC1, AC2 | Contract | The payment event on RC-2027-000712; the event element, the recovery element, the record element and the case move are present with their placeholders |
| TC-E6-027-02 | AC2, AC3, AC5 | Contract | The fee schedule above and a payment that matches the placement; the recovery element, the fee reference and the record element answer the R-WO-37 shape |
| TC-E6-027-03 | AC2, AC3 | Contract | The closed case with no placement; the recovery element and the case move answer the R-WO-49 shape with no fee reference |
| TC-E6-027-04 | AC2, AC5 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence of a published event |
| TC-E6-027-05 | AC4 | Contract | A role without the right on the read path; the 403 with MSG-P4-002 and the envelope of a malformed event |
| TC-E6-027-06 | AC4, AC5 | Contract | RW-CREDITAD holds CRUA and RW-WRITEOFF holds CRU; the rights and the record element answer TSD S7 T6.1 |
| TC-S7-E6027-CON-01 | AC1 | Contract | The event element validates; the topic, the consumer group, the inbox rule and the placeholder are present |
| TC-S7-E6027-CON-02 | AC2, AC3 | Contract | The recovery element validates with its eleven properties and their required flags; the two consumed rows and the case boundary carry their placeholders |
| TC-S7-E6027-CON-03 | AC3, AC4 | Contract | The no-`v_ace_*`, no-`recovery_case`, no-`payment` and no-`partner` boundary; the rights and the error envelope |
| TC-S7-E6027-CON-04 | AC5, AC6 | Contract | The record element and the fee reference match their schemas; the eight fakes match the document and a drifted fake fails the build |
| TC-S7-E6027-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of a provided operation, a published event, a second topic and a Schedule |
| TC-S7-E6027-CON-06 | AC7 | Contract | Each table of §12.7 is read and written only through its owner; a write to a table §12.7 does not own fails the build (ASM-3438) |

The six legacy cases are those of RWB-E6-027 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6027-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The six cases `TC-S7-E6027-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the income code, the fee basis, the posting parameters, R-WO-37, R-WO-49, their states and the package version stay rule rows, reference data and parameters, never a schema default, an enumeration member or a constant of the code.
- No personal data in a schema, an example, a payload or a fake: identifiers, amounts, dates, a code and a rule version only, and every example is synthetic.
- The payment stays with rwb-payment: the document declares no receipt property, no proceeds property and no posting of its own (BR3).
- The ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read (BR4).
- The case stays with rwb-case: the document declares no `recovery_case` property and no case state write (BR6).
- The fee stays reference data: the fee reference is a record property and no fee value is a schema default (BR5).
- The record is declared before the change; a build that writes the row first fails the review (DP-03).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No retired element and no invented element is reintroduced: the absence tests fail a build that declares a provided operation of this step, a published event, a second topic, a Schedule or a Quartz row.
- The error envelope, the idempotency rule, the naming rule, the decision-record library and the inbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-007 | Recoveries after charge-off are matched to the account, with income and agency fees recorded (Must, E6); the baseline declares the event, the recovery element, the fee reference and the case move | The event element, the recovery element, the fee reference and the record element | TC-E6-027-01, TC-E6-027-02, TC-S7-E6027-CON-01, TC-S7-E6027-CON-02 |
| REQ-S7-006 | Post charge-off treatment is set by rule, including placement with an agency (Must, E6); the baseline declares the rule IDs and the placement reference and owns neither | The state vocabulary and the placement reference | TC-E6-027-02, TC-S7-E6027-CON-02 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6027-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The consumed event element and the inbox library | TC-E6-027-01, TC-S7-E6027-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S7-E6027-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the record identifier of the recovery element | TC-E6-027-06, TC-S7-E6027-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-027, disposition Split (rework); feature FEAT-WOF-15 |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S7-E6027-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-027; FSD S7 Write-off and recovery v3 A2.15, A2.15.2, A2.15.3, A2.15.4 and Screens; TSD S7 Write-off and recovery v2 T2, T3.0, T3.1, T3.2, T4, T5.3, T6.1, T6.2 and T-A.1; Business Rules and Routing Logic v4 rows R-WO-37 and R-WO-49 |
| Test cases | The six legacy cases as the contract half, and the five new contract cases TC-S7-E6027-CON-01 to -05 |
| Feature and screens | FEAT-WOF-15, SCR-27 Write-off proposal |
| Rules | R-WO-37 and R-WO-49, governed in rwb-decision; R-WO-50 named as RWB-S7-E6028-APP's |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of R-WO-37 and R-WO-49, the match, the record, the posting call and the case-move answer: RWB-S7-E6027-APP.
- The receipt, its match and the posting of the proceeds: rwb-payment (P8) and FEAT-PAY-01, whose event and activity this baseline declares as consumed and faked (ASM-5115, ASM-5120).
- The ACE payment, account and customer facts and the `v_ace_*` views: rwb-source-data (P1), whose read this baseline declares as consumed and faked (ASM-5116).
- The case of record, its route states, the parent `CaseWorkflow` and the case-move operation name: rwb-case (P3) (ASM-5121).
- The fee schedule, its owner, its versions and the reference-data contract: carried as consumed with the placeholder (ASM-5117).
- The agency placement and the agency fee calculation: RWB-S9-E6034-APP and RWB-S9-E6035-APP, whose overlap with R-WO-37's action is recorded (GAP-3048; ASM-5118).
- The authoring, testing, approval and versioning of the WO package, the income code and the ledger: rwb-decision (P7) (ASM-5119).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- A published recovery event and the reporting read model that would need it: carried as a gap and not declared (GAP-3047; ASM-5122).
- The monthly scan, the tax criteria, the pack, the removal, the routing, the committee decisions, the posting of an approved write-off, the provision inputs, the reconciliation, the exception loop, the case closure and the post charge-off sale: RWB-S7-E6013-APP to RWB-S7-E6028-APP.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
