# RWB-S2-E3016-APP Set up a deed in lieu buy-back rental

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-016 for rwb-treatment. The buy-back rental leaves the monolith's S2 service in the one `recovery` schema and becomes the rental stage of `TreatmentWorkflow` on this service's own task queue, driving R-DIL-32 and the arrears rule R-DIL-34, with the rental carried as a `treatment` row of type RENTAL in schema `rwb_treatment`, the AMIS rental record and the ATS auto-debit mandate requested through their owners and returned as facts, the matched receipts and the missed instalments arriving from rwb-payment, the local decision record written in the same transaction as the rental change (DP-03), the customer and NPA-asset facts read as facts (DP-05), and the screens SCR-14 and SCR-16 reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-AA |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3016-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the rental stage of `TreatmentWorkflow` on task queue `rwb-treatment` — the opening of the rental record (R-DIL-32), the auto-debit mandate, the receipt loop that follows each instalment, the arrears test that hands the asset to disposal when the limit is passed (R-DIL-34), and the local decision record written in the same transaction — with the rental carried as a `treatment` row of type RENTAL, the case status and the arrears task carried by their owners, the customer and NPA-asset facts arriving as facts, the AMIS rental record and the ATS mandate requested through their owners and returned as facts, and the matched receipts reaching this stage from rwb-payment**, so that **a buy-back rental runs without a person for a standard arrangement, the rent, the mandate and every receipt are provable with the rule version that produced them, and this service opens no rental table and calls no external system**.

This is the application slice of legacy RWB-E3-016. It owns:

- the three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and data rows they depend on;
- the rental stage of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, with the five activities `openRentalRecord`, `setUpAutoDebit`, `followRentalReceipts`, `evaluateRentalArrears` and `recordAndApply`, plus `reportRentalOutcome`;
- the creation of the `treatment` row of type RENTAL in schema `rwb_treatment`, and the rental elements it carries: the agreed rent in `offer_amount` (DF-TRT-007), the first rental due date in `first_due_date` (DF-TRT-029), the instalments paid in `installments_paid` (DF-TRT-032), and `rentalRef`, `autoDebitRef` and `autoDebitStatus` (RWB-S2-E3016-CON);
- the local decision record written through RWB-PLT-E1027-CON in the same transaction as the rental change (DP-03);
- the request for the AMIS rental record and the ATS auto-debit mandate through their owners, and the facts that come back for the rental;
- the receipt loop: a matched instalment arrives as a fact and increments `installments_paid`, and a missed instalment arrives as `rwb.payment.PaymentMissed.v1` (EV-12) on this service's inbox;
- the entry of the stage and the screen path of SCR-14 and SCR-16 through the gateway-bff composite route (DP-19).

It does not own: the published rental element set, the no-new-table rule, the event position, the compatibility rule and the fakes, which are RWB-S2-E3016-CON; the treatment record and its creation operation, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the deed-in-lieu journey that brings the case to ASSET_ON_BOOKS, which is RWB-S2-E3012-APP; the settlement offer and its below-floor approval, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the asset record, the AMIS interface and the disposal route, which are rwb-asset and rwb-integration; the payment matching, the posting and the proceeds, which are rwb-payment; the case status, the case task and the case clock, which stay rwb-case's; and the deployment, the flag, the dashboards and the alerts, which are this legacy key's DevOps story.

### 2. Business rationale

REQ-S2-010 asks that a buyback rental, its auto-debit, its receipts and its arrears follow-up run without a person for a standard arrangement (Should, E3), and FEAT-TRT-16 opens the rental record, the auto-debit and the receipt loop where the customer buys back. The route matters because a deed in lieu ends with the bank owning the asset, and the cheapest exit for both sides is often that the former owner stays in the property and pays rent until the buy-back completes. Left manual, that rent is a spreadsheet: the debit is set by hand in ATS, each receipt is matched by hand, and arrears are noticed only when the asset should long since have gone to disposal.

The monolith answered it in one process: the S2 service inserted the rental into the shared `recovery` schema, set the debit in ATS in the same transaction boundary, wrote `decision_log_entry`, read `v_ace_customer` and `v_ace_npa_asset` directly, and matched proceeds in the same code. In the 19-service target each of those facts has a different owner. The case status is rwb-case's and reaches the stage on the case signal (ASM-4388). The record is the platform library's, written locally in this service's schema (DP-03). The customer and NPA-asset facts are rwb-source-data's and arrive as facts, because the connection matrix gives rwb-treatment no link to rwb-source-data (DP-05; ASM-4415). The AMIS rental record and the ATS mandate are rwb-asset's and rwb-integration's and return as facts (ASM-4416). The receipts are rwb-payment's and arrive as facts and as EV-12 (ASM-4417).

What the business keeps is the rule, not the code. R-DIL-32 creates the rental record and sets the auto-debit when the customer rents the asset back, and the case reaches RENTAL_RUNNING; R-DIL-34 hands the asset to the disposal route when the rental arrears exceed the limit. The rent, the limit, the state names and the reason codes are values in force of their owners, never constants (BR-S2-016).

Serves REQ-S2-010 and REQ-S2-008. No business value moves into code.

### 3. Preconditions

- RWB-S2-E3016-CON is published: the rental element set (the rent in `offer_amount`, the first due date in `first_due_date` and `rentalRef`, `autoDebitRef`, `autoDebitStatus`), the rule that the rental is a `treatment` row of type RENTAL and that no rental table is created, the event position, the compatibility rule and the fakes (H).
- RWB-PLT-E1027-CON is published (DP-03): `DecisionRecordWriter.record(DecisionRecord)` with propagation `MANDATORY`, the refusal `DecisionLogRecordInvalidException` with MSG-P7-009 and its field, and `DecisionLogUnavailableException` with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): the gateway-bff composite route that carries SCR-14 and SCR-16, one hop (H).
- RWB-S2-E3001-APP is done: `treatment` exists in schema `rwb_treatment` with DF-TRT-001 to DF-TRT-033, and its own migration sequence is the only place a column is added.
- RWB-S2-E3012-APP is done: the deed in lieu has reached ASSET_ON_BOOKS, so R-DIL-32 has an asset on books and a transfer reference to rent back (FEAT-TRT-12, the legacy story's dependency).
- `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed and the DEEDINLIEU package is in force with its version label, evaluated by the embedded Drools runtime (ASM-4418).
- The workflow kit and the outbox and inbox library are service-template capabilities (ASM-4418): the stage child, the timers, the signal handling, the outbox and the inbox are taken from the kit.
- The access guard is the platform guard library's; this story declares the capability area "Treatment and offer" and the rights the stage exercises — C and U for the officer — with the roles TSD S2 T6.1 lists.
- The customer and NPA-asset facts are on the case signal; no `v_ace_*` view is read here (DP-05; ASM-4415). The AMIS and ATS answers come back as facts from rwb-asset and rwb-integration (ASM-4416), and the receipts from rwb-payment (ASM-4417).
- The rent, the first due date, the arrears limit, the state names and the reason codes are values in force of their owners; this story holds no copy of any of them.
- No approval of this story is needed to build against a Draft contract baseline; RWB-S2-E3016-CON tags the version when its tests pass.

### 4. Flow

1. The parent `CaseWorkflow` on rwb-case forwards the case signal to the running `TreatmentWorkflow` child on `rwb-treatment`; the signal carries the case status, the product, the collateral and the customer and NPA-asset facts, and the status stays rwb-case's (ASM-4388; ASM-4415).
2. The stage holds a case at ASSET_ON_BOOKS with a completed transfer and the buy-back agreed arrives as a fact on the case signal — the condition "customer rents the asset back" of R-DIL-32.
3. `openRentalRecord` (R-DIL-32): inserts one `treatment` row on the case with `treatment_type` RENTAL of LOV-TREATMENT, `proposed_by` RULE, `proposed_at`, the agreed rent in `offer_amount` and the first rental due date in `first_due_date`. No rental table is opened (RWB-S2-E3016-CON; GAP-2681).
4. `setUpAutoDebit`: requests the ATS auto-debit mandate through rwb-integration and the rental record in AMIS through rwb-asset; the answers return as facts on the workflow and the treatment takes `rentalRef`, `autoDebitRef` and `autoDebitStatus` (ASM-4416).
5. `followRentalReceipts`: starts the rental due clock as a durable timer of the stage, so it survives a restart and a release. rwb-payment matches each instalment against the case; a matched receipt arrives as a fact and `installments_paid` increments, and the stage asks the parent for the next due date the rule in force sets (ASM-4417).
6. `evaluateRentalArrears` (R-DIL-34): a missed instalment arrives as `rwb.payment.PaymentMissed.v1` (EV-12) on this service's inbox; when the arrears pass the limit in force the stage reports HANDED_TO_DISPOSAL to the parent, which hands the asset to the disposal route on rwb-asset and raises the task of the owner in rwb-case.
7. `recordAndApply`, one transaction: the treatment row insert or update, the decision record through `DecisionRecordWriter.record` (decision code D6.4, the rule ID R-DIL-32 or R-DIL-34, the rule version of the package in force, the recommendation, the final call, the outcome and the time) and the outbox row.
8. `reportRentalOutcome`: the rule outcome — RENTAL_RUNNING from R-DIL-32 or the disposal hand-off of R-DIL-34 — goes to the parent, which moves the case status. This service publishes no business event on this path: the catalogue gives the service one event, EV-10, and it is published at the offer release of the deed in lieu by RWB-S2-E3012-APP (GAP-2680; ASM-4417).
9. A redelivered case signal, a repeated facts answer or a redelivered EV-12 answers the open step and opens no second rental row and no second child: the workflow ID of this stage, the treatment's own key and the cloud event id carry the idempotency.
10. The rental ends when the buy-back completes, the tenancy ends or the asset goes to disposal; the treatment takes its outcome of LOV-TRT-OUTCOME and the stage reports it to the parent.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right C or U on "Treatment and offer" acts on the rental | 403 from the guard; the refusal is logged and nothing changes | MSG-P4-002 | AC1, TC-E3-016-04 |
| X2 | The decision record cannot be written | The transaction rolls back: no rental row, no update, no outbox row and no report to the parent | MSG-P7-003 | AC3, TC-E3-016-03, TC-E3-016-05 |
| X3 | The record is refused for a missing or invalid field | The transaction rolls back and the field is named in the service log and the incident | MSG-P7-009 | AC3 |
| X4 | The data product behind the case or the asset is stale | The stage holds the rental and asks for the figure before it opens the row | MSG-P1-001 | AC1 |
| X5 | The ATS mandate is refused or AMIS does not answer inside the step | The stage retries on the kit's policy, then holds at ASSET_ON_BOOKS with `autoDebitStatus` as its owner reported it and a task for the owner; no partial rental fact is written | None | AC1 |
| X6 | A second rental is proposed for the same case and asset | The stage finds the open rental and answers the caller with it; no second row and no second mandate is opened | None | AC2 |
| X7 | An instalment is missed and the arrears pass the limit in force (R-DIL-34) | The stage reports HANDED_TO_DISPOSAL to the parent, which hands the asset to the disposal route and raises the owner's task | None | AC1 |
| X8 | The rent or the first due date is not in force when the row is opened | The stage holds the rental and asks the parent for the value in force; nothing is defaulted | MSG-GEN-001 | AC1 |

X1 to X3 are the exception paths of RWB-E3-016 carried onto the split; X4 to X8 are the paths of the target. The exception flows the FSD records for FEAT-TRT-16 — a role without the right and an unrecordable decision — are AC-EXC-S2-016-01 and AC-EXC-S2-016-02 and are X1 and X2 (FSD S2 A2.16.4.3).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published element set and fakes of RWB-S2-E3016-CON, the decision-record contract and the gateway route; no live rwb-case, rwb-asset, rwb-integration or rwb-payment is needed to start, and the case status, the ACE facts, the AMIS and ATS answers and the receipts arrive on mocks |
| Negotiable | The activity names, the three rental columns and the request bodies are this story's choice; the rent, the limit, the clocks and the state names are fixed by their owners' data |
| Valuable | A buy-back rental is opened, debited and receipted with no hand-carried step, and the arrears test is the rule's, not the officer's |
| Estimable | One stage, five activities, one row of type RENTAL, three columns, one event consumed and no event published |
| Small | Finished inside three weeks with its tests |
| Testable | Each criterion runs on synthetic cases, rentals and receipts through the contract fakes, plus one component test of the guard and the stage entry |

### 7. Acceptance criteria

```gherkin
Feature: Set up a deed in lieu buy-back rental

  Scenario: AC1 Set up a deed in lieu buy-back rental (legacy RWB-E3-016 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then opens the rental record, the auto-debit and the receipt loop where the customer buys back
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-32 (legacy RWB-E3-016 AC2)
    Given the rwb-case contract mock returns case status ASSET_ON_BOOKS
    Given a case in state ASSET_ON_BOOKS
    When buyback agreed
    Then create the rental record and set the auto-debit
    Then the case moves to RENTAL_RUNNING

  Scenario: AC3 Not recorded (legacy RWB-E3-016 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** All three criteria keep their wording and their values; what changes is where each step runs, who owns each fact and how the answer is proved. The journey is no longer a step of the monolith's S2 service in the one `recovery` schema: it is the rental stage of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, on task queue `rwb-treatment` in namespace `rwb-recovery` (ASM-4388). "Its trigger arrives" of AC1 is the buy-back agreed fact on the case signal, and "the rental record, the auto-debit and the receipt loop" are the stage's three activities: a `treatment` row of type RENTAL, the ATS mandate request, and the timer and inbox that follow the receipts (RWB-S2-E3016-CON; ASM-4416; ASM-4417). "The result written to the decision log with the rule version" is the local decision record written through RWB-PLT-E1027-CON in the same transaction as the rental change (DP-03); `decision_log_entry` is P7's ledger and is neither written nor read here. The case status of AC2 — ASSET_ON_BOOKS in, RENTAL_RUNNING out — stays rwb-case's, which is why the added Given line is answered by the rwb-case contract mock standing in for the case signal: the stage reports the rule outcome and the parent moves the status (ASM-4388). R-DIL-32 and R-DIL-34 are evaluated by the embedded Drools runtime against the package version in force announced by `rwb.decision.RulePackageInForce.v1`, and that version is written into each record (ASM-4418). AC3 is unchanged and is served by the `MANDATORY` propagation of the record: no rental row, no mandate request and no status report survives a failed append. The receipt and the arrears limit are values in force of rwb-payment and the package, never figures of this code (BR-S2-016).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A buy-back agreed on an asset on the books opens one rental record on the case and sets the auto-debit, and the case reaches RENTAL_RUNNING | R-DIL-32 |
| BR2 | The rental record is a `treatment` row of type RENTAL: the agreed rent in `offer_amount`, the first rental due date in `first_due_date`, the instalments paid in `installments_paid`, and `rentalRef`, `autoDebitRef` and `autoDebitStatus`; no rental table is opened | RWB-S2-E3016-CON; GAP-2681; ASM-4414 |
| BR3 | Each matched instalment increments `installments_paid` and the next due date is the one the rule in force sets; no receipt is matched, posted or reversed in this service | R-DIL-32; ASM-4417 |
| BR4 | A missed instalment arrives as EV-12 and the arrears test runs on the limit in force; when the arrears pass it the asset is handed to the disposal route | R-DIL-34; R-DIL-33 |
| BR5 | A stale data product holds the rental and asks for the figure before the row is opened | VR-S2-016-1; FSD S2 A2.16.3.1 |
| BR6 | No value a business person may change is written in code: the rent, the first due date, the arrears limit, the clocks, the state names and the reason codes are read as values in force with their version | BR-S2-016; FSD S2 A2.16.3.1 |
| BR7 | A step whose decision cannot be recorded does not take effect: the record joins the caller's transaction and a failed append rolls everything back | R-UNI-39; RWB-PLT-E1027-CON; Principle 5 |
| BR8 | The case status, the case task, the asset record, the AMIS interface, the ATS mandate, the receipts and the proceeds stay with their owners; this stage requests them and writes none of them | DP-01; ASM-4388; ASM-4416; ASM-4417 |
| BR9 | This service publishes no business event on the rental path; the rental start reaches rwb-payment through the case events of rwb-case, and the one event type of the service stays with the offer release of the deed in lieu | GAP-2680; ASM-4417 |

**Where each rule lives in the target.** BR1 and BR2 are `openRentalRecord`: the insert of the RENTAL row, the rent and the first due date as values in force (BR6). BR2 also fixes that no rental table is opened, which is the contract's rule and the reason the element names exist. BR3 is `followRentalReceipts`: the fact, the increment and the timer. BR4 is `evaluateRentalArrears`: the EV-12 subscription, the limit read from its owner, and the hand-off reported to the parent. BR5 is the stale-product check before the insert. BR6 is served by reading every value from its owner; the only fixed strings in this story are the element names of its contract. BR7 is `recordAndApply`: the rental change, the decision record and the outbox row sit in one transaction, and `DecisionLogUnavailableException` (MSG-P7-003) and `DecisionLogRecordInvalidException` (MSG-P7-009) roll it back. BR8 is the signal contract with the parent and the request contract with rwb-asset, rwb-integration and rwb-payment.

### 9. State transitions

None of the states below is this service's to change (ASM-4388). The stage evaluates the rule, records the outcome and reports it to the parent `CaseWorkflow`, and the parent moves the case status in rwb-case. The table lists the buy-back and rental steps of the DEEDINLIEU route as the stage asserts them, which is what AC2 names.

| From (case status, rwb-case's) | Event | Condition | To (case status, rwb-case's) | Rule |
|---|---|---|---|---|
| ASSET_ON_BOOKS | BUYBACK_AGREED | the customer rents the asset back | RENTAL_RUNNING | R-DIL-32 |
| ASSET_ON_BOOKS | DISPOSAL_REQUIRED | no buy-back agreed | HANDED_TO_DISPOSAL | R-DIL-33 |
| RENTAL_RUNNING | RENTAL_ARREARS | the rental arrears exceed the limit in force | HANDED_TO_DISPOSAL | R-DIL-34 |

Two states of the stage's own object are visible in the outcome: the treatment's `autoDebitStatus` is empty until the mandate has answered and carries its owner's answer after it, and the treatment's `outcome` carries the LOV-TRT-OUTCOME value the rental ends on. The stage holds no state machine of its own beyond those values.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the stage, the five activities, the rental row and the three rental columns |
| RW-CASEOWN, case owner | Records the buy-back agreement and the rental terms on SCR-14 and SCR-16; holds CRU in "Treatment and offer"; R-DIL-32 names the case owner as the owner of the step |
| RW-RESTRUCT, restructuring officer (FCR) | Holds CRUA in the capability area and may stand in for the case owner |
| RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL | Hold R in the capability area and read the rental; they change nothing |
| The sale officer of the FSD roles | Acts on the rental as the FSD names the primary role of FEAT-TRT-16 beside "runs unattended" |
| RW-AUDIT, RW-COE | Read the recorded decision and the rental outcome; they change nothing |
| rwb-case (P3) | Owns the case status, the case task and the clock the stage reads as a value |
| rwb-payment (P8) | Owns the payment matching, the posting, the receipt fact, the proceeds and EV-12 |
| rwb-asset (S5), rwb-integration (P2) | Own the asset record, the AMIS interface, the ATS mandate and the disposal route |
| rwb-decision (P7) | Owns the rule packages and their versions, and the approval record the stage never opens |
| No delegation of authority level applies to this story | The story builds the stage; the level that applies is a data value of the approver's row, never a decision of this code |

No credential, personal name or email address appears in the workflow input, the activity payloads, the event or the logs, which carry treatment and case identifiers, codes, amounts, versions and timestamps only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Write on the insert |
| DF-TRT-002 | treatment | case_id | Write on the insert |
| DF-TRT-004 | treatment | treatment_type | Write: RENTAL of LOV-TREATMENT |
| DF-TRT-005 | treatment | proposed_by | Write: RULE of LOV-PROPOSER |
| DF-TRT-006 | treatment | proposed_at | Write |
| DF-TRT-007 | treatment | offer_amount | Write; carries the agreed rent on this path |
| DF-TRT-013 | treatment | outcome | Write at the end of the rental |
| DF-TRT-014 | treatment | outcome_at | Write at the end of the rental |
| DF-TRT-029 | treatment | first_due_date | Write; the first rental due date |
| DF-TRT-032 | treatment | installments_paid | Write on each matched receipt |
| (no field ID) | treatment | rentalRef, autoDebitRef, autoDebitStatus | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (library object in `rwb_treatment`) | id, case_id, decision_code, rule_id, rule_version, model_version, idempotency_key, final_call, outcome, decided_at, chain_seq, entry_hash and the rest | Write through `DecisionRecordWriter` |
| DF-CAS-001 to DF-CAS-023 | recovery_case (`rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and the rest | Read as facts on the case signal, never from the table |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer (`rwb_source_data`'s read) | person_key, cif_no, first_name, last_name, date_of_birth and the rest | Read as facts on the case signal, never from the view |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (`rwb_source_data`'s read) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and the rest | Read as facts on the case signal, never from the view |
| DF-FIN-001 to DF-FIN-009 | proceeds (`rwb_payment`) | id, case_id, treatment_id, payment_code, source, amount and the rest | Read as a matched-receipt fact, never from the table |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`) | rule_id, rule_version, from_state, event_code, condition, target state | Read as the evaluated package, never from the table |

`treatment` is this service's table and the only one this story writes, together with the library's `decision_record` and the outbox in the same schema (DP-01; DP-03). The three rental columns carry no field ID and no column definition in the TSD, which lists DF-TRT-001 to DF-TRT-033 with no rental reference, no mandate reference and no mandate status: their names and types are the working read of the gap and the assumption (GAP-2681; ASM-4419). `recovery_case`, `proceeds` and the two `v_ace_*` views belong to rwb-case, rwb-payment and rwb-source-data: the case facts, the asset facts and the receipt arrive on the case signal, and no ACE view is named in a statement of this service (DP-05; ASM-4415; ASM-4417). Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story declares no operation of its own: the rental row is opened through the treatment creation operation `POST /cases/{caseId}/treatments` and read through `GET /treatments/{treatmentId}`, which are RWB-S2-E3001-CON's, and the officer's action that records the buy-back agreement is an update of the treatment through `PATCH /treatments/{treatmentId}`, which is RWB-S2-E3002-CON's. The `/submit` form of API Specification v4 and TSD S2 T-A.1 API-S2-004 is superseded on this service by the offer operation, under the source precedence of Template and Rules §R3. The stage itself writes the rental row in its own transaction and calls no operation.

| Element this story reads or writes | Source | Use |
|---|---|---|
| The treatment element of a read, and the creation of a treatment on a case | RWB-S2-E3001-CON | The stage entry: the treatment exists and belongs to the case |
| `rentalRef`, `autoDebitRef`, `autoDebitStatus`, and the rent and first due date carried in published fields | RWB-S2-E3016-CON | The rental facts the stage writes and the screens read |
| `PATCH /treatments/{treatmentId}` | RWB-S2-E3002-CON | The surface on which the officer records the buy-back agreement |

#### 12.2 REST operations consumed

None. The case status, the customer and asset facts and the matched receipt arrive on the case signal the parent `CaseWorkflow` forwards, which is the only way a case fact reaches this service (ASM-4388; ASM-4415; ASM-4417). The AMIS rental record, the ATS mandate and the disposal hand-off are reached through Temporal on their owners' queues, because route services reach shared capabilities through Temporal and never REST (Architecture v5 slide 13 note; ASM-4416). The Work Package lists no contract dependency for this story, and none is added.

#### 12.3 Events published

None of its own. The service publishes one event type, `rwb.treatment.TreatmentApproved.v1` (EV-10), and it is published at the offer release of the deed in lieu by RWB-S2-E3012-APP, not on this path; no source names an event for the rental (GAP-2680; ASM-4417). The decision record reaches the shared `rwb.decision-record.v1` topic through the library and the outbox relay of the service template, in the same transaction as the rental change (DP-03).

| Event | Topic | This path | Purpose |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | Not published: EV-10 belongs to the offer release of R-DIL-16 on RWB-S2-E3012-APP | EV-10 tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt |

The rental start is not silent for the consumer that needs it: the parent reports RENTAL_RUNNING to rwb-case, whose case events are what rwb-payment subscribes to, so the expected rent reaches the matching side without a new event of this service (ASM-4417). No payload is added, no field is added to the one envelope, and no outbox row is written on a refusal or a hold.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | EV-30: names the DEEDINLIEU package version in force, which the stage evaluates and writes into each record; a version is swapped in at the next event and no restart is needed |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 rwb-payment | EV-12: a rental instalment is missing, which starts the arrears test of R-DIL-34 |

Both are consumed through the inbox of the outbox library, so a redelivery is deduplicated by the cloud event id. `rwb.payment.TreatmentBooked.v1` (EV-11) and `rwb.deviation.DeviationRaised.v1` (EV-06) are consumed by other stages of `TreatmentWorkflow`, not by this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (rental stage) | Workflow, the stage child of `CaseWorkflow` (rwb-case), one execution per case and stage, continue-as-new at the stage end | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, case status, product, the asset and customer facts and the buy-back agreement; the stage outcome returned to the parent; search attributes CaseId and Stage |
| `openRentalRecord` | Activity | `rwb-treatment` | The insert of the RENTAL treatment row: rent, first due date, `proposed_by` RULE; idempotent by case and stage |
| `setUpAutoDebit` | Activity | `rwb-treatment` | The AMIS rental record and the ATS mandate requested on their owners' queues, and the facts that return: `rentalRef`, `autoDebitRef`, `autoDebitStatus` |
| `followRentalReceipts` | Activity | `rwb-treatment` | The matched-receipt fact, the `installments_paid` increment and the rental due timer |
| `evaluateRentalArrears` | Activity | `rwb-treatment` | The EV-12 fact, the arrears limit in force and the disposal hand-off reported to the parent |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the treatment change, the decision record through RWB-PLT-E1027-CON and the outbox row |
| `reportRentalOutcome` | Activity | `rwb-treatment` | The rule outcome RENTAL_RUNNING or HANDED_TO_DISPOSAL reported to the parent |

DP-03, DP-05, DP-13 and DP-19 are the patterns this story applies; the workflow and activity names are a target design choice fixed by no source document, and the stage model itself is the workflow kit's. The retry policy is the kit's, and the clocks of the route — the rental due and the arrears limit — are values in force that the stage reads and never sets.

#### 12.6 Schedules

None. The stage is signal-started inside `TreatmentWorkflow` and owns no Temporal Schedule and no legacy Quartz job; the rental due clock and the arrears window are durable timers of this stage, so they survive a worker restart and a release (ASM-4418).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Inserted as one row of type RENTAL with DF-TRT-001, -002, -004, -005, -006, -007 and -029; updated with `installments_paid`, `rentalRef`, `autoDebitRef`, `autoDebitStatus`, `outcome` and `outcome_at` |
| `decision_record` | `rwb_treatment` | PLT (library object, written through RWB-PLT-E1027-CON) | Written in the same transaction as the rental change (DP-03) |
| `outbox` | `rwb_treatment` | S2, from the service template | Written in the same transaction; the relay publishes the decision record to `rwb.decision-record.v1` |
| `asset` | `rwb_asset` | S5 | Not written and not read: the AMIS rental record is requested and its reference returns as a fact |
| `proceeds` | `rwb_payment` | P8 | Not written and not read: the matched receipt and the proceeds are the payment service's |
| `recovery_case`, `assignment` | `rwb_case` | P3 | Not written and not read: the status, the task and the facts arrive on the case signal |
| `v_ace_customer`, `v_ace_npa_asset` | ACE views, `rwb_source_data`'s read | P1 | Never named in a statement of this service (DP-05) |

No rental table is created, and no foreign key crosses a schema (DP-01; RWB-S2-E3016-CON). `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3016-CON rental fake | The rental elements and the no-new-table rule | A rental row at each rental state with its rent, its mandate status and its instalment count; a rental with no mandate answer and one with no rental reference |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| RWB-PLT-N001-CON gateway route fake | The composite route of SCR-14 and SCR-16 | A granted right C and U for the officer; a refused answer; a scope miss |
| rwb-case case-status mock | The added Given line of AC2 and the facts of the stage entry | Case status ASSET_ON_BOOKS and RENTAL_RUNNING on the signal, the product, the asset and the customer facts, and the status the parent reports back |
| rwb-asset and rwb-integration answer fake | The AMIS rental record, the ATS mandate and the disposal hand-off | A rental accepted with a reference; a mandate accepted; a mandate refused; a timeout |
| rwb-payment receipt and event fake | The matched receipt and EV-12 | A receipt matched for a rental instalment; a missed instalment on `rwb.payment.events.v1`; a duplicate cloud event id |
| Rental value fixture | The values in force | The arrears limit, the due clock and the reason codes of the disposal hand-off, of their owners |

The element, decision-record and gateway fakes are the published contracts of those stories; the case-status mock stands in for the signal, which is the only way a case fact reaches this service (ASM-4388); the asset, integration and payment fakes stand in for the Temporal and Kafka answers of their owners (ASM-4416; ASM-4417).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the stage declares no operation | 0 | The treatment resource is RWB-S2-E3001-CON's and the update surface RWB-S2-E3002-CON's, reached through gateway-bff (DP-19) |
| Kafka | 0 business events | 2 events (`rwb.decision.RulePackageInForce.v1`, `rwb.payment.PaymentMissed.v1`) | The decision record reaches `rwb.decision-record.v1` through the outbox of the template; inbox of the template for the two |
| Temporal | 1 stage workflow and 6 activities | Activities on rwb-asset, rwb-integration and rwb-payment | Namespace `rwb-recovery`; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `buyback-rental` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract or the service's own ACE views; here the facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of each step inside the same transaction; DP-05 is the customer and NPA-asset read that comes to this stage as facts, because the connection matrix gives rwb-treatment no call to rwb-source-data and the views are granted to rwb-source-data alone (ASM-4415); DP-13 fixes the service base on which the sibling operations answer; DP-19 is the route by which SCR-14 and SCR-16 reach this service. The ownership rule of DP-01 is applied in prose and in the SQL: `recovery_case`, `asset`, `proceeds` and the two views are never named in a statement of this service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (rental stage) | Workflow | The rental opening, the mandate, the receipt loop, the arrears test and the outcome report |
| `openRentalRecord` | Activity | The RENTAL treatment row: rent, first due date, `proposed_by` RULE |
| `setUpAutoDebit` | Activity | The AMIS rental record and the ATS mandate requests, and the facts that return |
| `followRentalReceipts` | Activity | The matched receipt, the instalment count and the due timer |
| `evaluateRentalArrears` | Activity | The EV-12 fact, the limit in force and the disposal hand-off |
| `recordAndApply` | Activity | The treatment change, the decision record and the outbox row in one transaction |
| `RentalStageHandler` | Handler | The stage entry from the case signal: the agreement, the state and the facts mapped onto the stage input |
| `TreatmentRepository` | Repository | The insert and update of `treatment`, with the optimistic-lock version of the row |

**Database.** `treatment` already holds DF-TRT-001 to DF-TRT-033. This story adds `rentalRef`, `autoDebitRef` and `autoDebitStatus` on the service's own migration sequence and creates no table: the rental has none of its own (GAP-2681; ASM-4414). `decision_record` is the library object of RWB-PLT-E1027-CON in the same schema.

**Configuration and reference data.** The rent, the first due date, the arrears limit, the due clock, the state names and the reason codes are values in force of their owners and are read, never set here (BR6). The package version arrives through `rwb.decision.RulePackageInForce.v1`. The capability area and the rights are the guard library's data.

**Build steps**

1. The migration that adds the three rental columns to `treatment` on the service sequence, with no new table.
2. `openRentalRecord` against the rental fakes, with the insert of the RENTAL row and the duplicate case (AC1, AC2).
3. `setUpAutoDebit` against the AMIS and ATS answers, with the accepted mandate, the refused mandate and the timeout (AC1).
4. `followRentalReceipts` against the receipt fake and its duplicate, with the increment and the timer (AC1).
5. `evaluateRentalArrears` against EV-12 and the limit fixture, with the pass and the disposal hand-off (AC1).
6. `recordAndApply` with the treatment change, the decision record through the fake and the outbox row, and the rollback on MSG-P7-003 and MSG-P7-009 (AC3).
7. The stage entry and the guard, with the case signal and a role without right C or U (AC1, TC-E3-016-04).
8. The outcome report to the parent and the two mocked case statuses (AC2).
9. Tests for AC1 to AC3 against the fakes and the fixtures.

**Feature flag.** `rwb.treatment.buyback-rental`.

**Done when.** The tests in section 16 pass, a synthetic buy-back rental walks from ASSET_ON_BOOKS to RENTAL_RUNNING and on to HANDED_TO_DISPOSAL in SIT with the rent, the mandate and the instalments recorded on the treatment, no second rental is opened on a redelivered signal, a forced record failure leaves the treatment unchanged with MSG-P7-003, and SCR-14 shows the rental row with its mandate status through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message | Source |
|---|---|---|---|
| MSG-S2-003 | The rental arrangement to the customer carries its end date | The offer to the customer ends on {date}. | RWB-E3-016 |
| MSG-S2-001 | A figure on the rental is below the floor of its case and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. | RWB-E3-016; VR-S2-016-1 |
| MSG-S2-002 | The payoff behind the rental figure is older than the freshness limit | The payoff is from {date}. A new figure has been requested. | RWB-E3-016 |
| MSG-P1-001 | The data product behind the case or the asset is from an earlier date | {product} is from {date}. Today's ACE batch has not arrived. | FSD S2 A2.16.3.1 (VR-S2-016-1) |
| MSG-GEN-001 | A required field of the rental — the rent, the first due date or the mandate — is missing | Enter {field}. | RWB-E3-016; FSD S2 A2.15.3.1 |
| MSG-P4-002 | The role does not hold the right the action needs in "Treatment and offer" | You cannot {action} here. Your role does not include it. | RWB-E3-016 |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | RWB-E3-016; RWB-PLT-E1027-CON |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to the customer) | The decision record was refused: {field} is missing or not valid. | RWB-PLT-E1027-CON |

The six legacy texts are carried unchanged, MSG-P1-001 comes from the FSD validation rule of this feature and MSG-P7-009 comes with the decision-record contract. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record (states Draft; submitted; approved; booked; broken) shows the rental as a treatment of type RENTAL beside the deed-in-lieu treatment of its case, with its rent, its first due date, its mandate status and its instalment count; SCR-16 Deed in lieu (states Checks; appraisal; approved; transferred) shows the deed-in-lieu facts that led to the rental. Both reach this service through the gateway-bff composite route (DP-19), which calls rwb-treatment and the screen's other owners in parallel, one hop each; the officer's action that records the buy-back agreement is an update of the treatment through the surface of RWB-S2-E3002-CON, and the stage learns it on the case signal. The screen field list and the composite route specification belong to the platform edge story and the screen owners; this story fixes the service side only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-016-01 | AC1 | End to end | An asset on the books with the buy-back agreed; the rental row opened, the mandate set in ATS, the receipts followed and the decision record carrying the rule version |
| TC-E3-016-02 | AC2 | End to end | Case status ASSET_ON_BOOKS on the case signal mock; the buy-back agreed; the rental record created, the auto-debit set and the case reaching RENTAL_RUNNING |
| TC-E3-016-03 | AC3 | End to end | The decision-record fake refuses the write; nothing changes and MSG-P7-003 is shown |
| TC-E3-016-04 | Access | Component | The case owner acts with right C and U and is granted; a role without the right is refused with MSG-P4-002 and nothing changes |
| TC-E3-016-05 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003; the rental row, the outbox and the parent report are unchanged |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The contract fakes of section 12.8 stand behind every case, and the asset, integration and payment fakes replace the calls and the events of their owners. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to the wave 2 integration harness, RWB-ITG-W2, and are not listed here.

### 17. Guardrails

- No business value in code: the rent, the first due date, the arrears limit, the clocks, the state names and the reason codes are values in force of their owners, read with their version, never constants (BR6).
- No personal data in logs, events, workflow inputs or the fixture: the stage carries treatment and case identifiers, codes, amounts, versions and timestamps; test data is synthetic and no customer field is copied.
- No read of another service's table and no read of an ACE view: the case, asset and receipt facts arrive on the case signal and the rental record and the mandate are requested from their owners (DP-01; DP-05; ASM-4415).
- No rental table and no second place where the rent lives: the `treatment` row and the local record are the only two, as RWB-S2-E3016-CON fixes (BR2).
- No write outside the transaction that records the change: the rental insert or update, the decision record and the outbox row commit together or not at all (DP-03; BR7).
- The decision is written before the change takes effect, and a refused or unavailable record leaves the case exactly as it was, which is what R-UNI-39 and Principle 5 require.
- The rule version is written with every answer, so an auditor can see why a rental was opened or an asset handed to disposal.
- No case status and no case task is written: the parent moves the status and raises the task on the stage outcome (ASM-4388).
- No business event is published on this path: the one event type of the service stays with the offer release of the deed in lieu (GAP-2680).
- No credential, no secret and no document content appears in code, configuration, a prompt or an event payload.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-010 | Buyback rental, auto-debit, receipts and arrears follow-up run without a person for a standard arrangement | Business Requirements Program, section 5.9 | FEAT-TRT-16 | 07 Route, settle and claim | R-DIL-32; R-DIL-34 | TC-E3-016-01, TC-E3-016-02 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program, section 5.9 | FEAT-TRT-16 | 07 Route, settle and claim | R-DIL-32 | TC-E3-016-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3016-CON | Contract | H: declares the rental element set, the no-new-table rule, the event position and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, its `MANDATORY` rule and its two exceptions (DP-03) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-16 (DP-19) |
| RWB-S2-E3001-APP | App development | Same lane, earlier: the treatment record the rental row is inserted into |
| RWB-S2-E3012-APP | App development | Same lane, earlier: the deed-in-lieu journey that brings the case to ASSET_ON_BOOKS (FEAT-TRT-12) |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the same legacy key against rwb-case, rwb-asset, rwb-integration and rwb-payment; not this story's |

### 19. Out of scope

- The published rental element set, the no-new-table rule, the event position, the compatibility rule and the fakes: RWB-S2-E3016-CON.
- The treatment record, its creation operation and its fields DF-TRT-001 to DF-TRT-033: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The deed in lieu from the offer to the asset on books, the field inspection and the unlock: RWB-S2-E3012-APP and RWB-S2-E3012-CON.
- The settlement offer, its range and the below-floor approval: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The asset record, the asset list, the AMIS interface, the ATS mandate interface and the disposal route: rwb-asset and rwb-integration, through their own contracts.
- The payment matching, the posting, the receipt, the proceeds and the arrears event: rwb-payment, RWB-P8 and its own contract.
- The case status, the case table, the case task and the case signal: rwb-case, RWB-P3-E1018 and its contract.
- The rule package registry, the version promotion and the approval record: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag, the dashboards and the alerts of this build: this legacy key's DevOps story.
- The real cross-service proof against the live rwb-case, rwb-asset, rwb-integration and rwb-payment: the wave 2 integration harness.
