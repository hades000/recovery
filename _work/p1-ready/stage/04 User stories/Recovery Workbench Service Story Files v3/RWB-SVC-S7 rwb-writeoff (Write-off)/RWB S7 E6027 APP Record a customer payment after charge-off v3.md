# RWB-S7-E6027-APP Record a customer payment after charge-off

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6027-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-S7-O |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6027-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S7-E6027-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version built against | `v1` (the version in the path, `/v1`); a numeric contract version is Not specified in the source documents (DOR-RWB-S7-E6027-APP-23) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: the post charge-off recovery slice of legacy RWB-E6-027 reworked for rwb-writeoff. The four legacy acceptance criteria are kept word for word with their origin tag; a payment received after charge-off now arrives as a consumed rwb-payment event, is matched to the `write_off` row of `rwb_writeoff` and to the placement, and is evaluated by R-WO-37 or R-WO-49 of the WO package, recorded through the local decision-record library before the row changes (DP-03), written as `recovered_after`, `posted_date`, `state` and `decision_log_id` (DP-01), read for its ACE payment, account and customer facts through rwb-source-data's contract (DP-05), and answered to rwb-case as the stage move `PAYMENT_MATCHED` over the gateway-bff composite route for SCR-27 (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6027-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 15 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **the Workbench to take a payment on a charged-off balance, apply it and record the recovery**, so that **write-offs follow the criteria and the committee's decision**.

This is the post charge-off recovery slice of legacy RWB-E6-027. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screen they depend on;
- the recovery branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (context pack workflow row `WriteOffWorkflow`; Temporal and Drools Design slide 13, "Write-off · rwb-writeoff · WO 51");
- the consumption of rwb-payment's payment event for a charged-off account, matched to the case, the account and the placement (context pack connection matrix, row S7, "T E" into P8);
- the evaluation of R-WO-37 for a case in `PLACED_WITH_AGENCY` and of R-WO-49 for a case in `CASE_CLOSED`, with the WO package version in force (Business Rules and Routing Logic v4; TSD S7 T4, "51 rules over 27 states");
- the income posting instruction for ALS and the general ledger raised as the `postProceeds` activity on rwb-payment's queue, and the agency fee reference the rule asks for;
- the decision record of the match, the rule ID with its version, the recovery amount, the fee reference and the outcome, written before the row changes (DP-03);
- the write of `recovered_after` (DF-FIN-020), `posted_date` (DF-FIN-016), `state`, `decision_log_id` and the standard columns on the `write_off` row in `rwb_writeoff`;
- the answer to rwb-case that moves the case to `PAYMENT_MATCHED`, with the rule ID and its version;
- the element of SCR-27 that shows the recovery on the approved write-off through the gateway-bff composite route (DP-19).

It does not own: the published shapes of the `write_off` element, of the consumed event, of the fee reference and of the case move, the state vocabulary, the error set and the fakes, which are RWB-S7-E6027-CON; the monthly scan, the tax criteria and JOB-16, which are RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack, the removal and the routing, which are RWB-S7-E6015-APP, RWB-S7-E6016-APP and RWB-S7-E6017-APP; the approve, reject and defer, which are RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP; the posting of an approved write-off, the provision inputs, the reconciliation and the exception loop, which are RWB-S7-E6021-APP to RWB-S7-E6024-APP; the post charge-off sale and the case closure after retention, which are RWB-S7-E6028-APP and RWB-S7-E6025-APP; the agency placement and the agency fee calculation, which are RWB-S9-E6034-APP and RWB-S9-E6035-APP; the case of record and its route states, which are rwb-case's (P3); the payment match and the money, which are rwb-payment's (P8); the ACE facts, which are rwb-source-data's (P1); the ledger entry, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-027 gave the Workbench one step that took a payment on a charged-off balance, applied it and recorded the recovery. The FSD keeps the objective unchanged — "Takes a payment on a charged-off balance, applies it and records the recovery" (FSD S7 A2.15.1) — against the module metric "write-off packs accepted first time, rising each month", measured on the decision log and the Workbench records and reviewed monthly. The problem is unchanged as well: write-off populations are assembled by hand each month.

What D-RCV-60 changes is where the money, the facts, the record and the case live:

- **the recovery is this service's.** `recovered_after` (DF-FIN-020) is the post charge-off recovery column of `write_off`, the only table of S7 in `rwb_writeoff` (TSD S7 T3.1; context pack ownership row), so the recovery amount, its posting date and the record reference are written here and nowhere else.
- **the payment is not this service's.** The receipt, its match to the case and the account, and the posting of the proceeds are rwb-payment's (P8, FEAT-PAY-01); S7 listens to the payment event and calls the `postProceeds` activity on the P8 queue (context pack connection matrix, row S7, "T E").
- **the ACE facts are not this service's.** `v_ace_payment`, `v_ace_account` and `v_ace_customer` are read only by rwb-source-data (P1); this service reads them through P1's contract and holds no `v_ace_*` grant, which is DP-05.
- **the case and its route states are not this service's.** `recovery_case`, `PLACED_WITH_AGENCY`, `CASE_CLOSED` and `PAYMENT_MATCHED` as case states are rwb-case's (P3); the step answers the move and writes the WRITEOFF state of its own row.
- **the fee is reference data.** The agency fee schedule and the placement facts are reference data, which the default ruling places with rwb-case (Template and Rules §R3); R-WO-37's fee calculation is also the subject of rwb-partner's FEAT-PRM-07, so this story consumes the fee and records the reference (GAP-3048; ASM-5117, ASM-5118).
- **the record is this service's, the ledger is not.** The decision record of the match is written through the local library of DP-03 before the row changes; the central ledger entry stays with rwb-decision.

The binding values are unchanged and are not written in code: the WO rule rows and the package version, the agency fee schedule, the retention and posting parameters and the state list are package rows, reference data and parameters read with their version.

The delivery is the plan's: this key is EP06 and therefore wave 4, and rwb-writeoff is created in wave 4 (Architecture v5), so the two agree and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5123).

### 3. Preconditions

- RWB-S7-E6027-CON is published: the `write_off` recovery element, the consumed payment event element, the fee reference, the case-move answer, the state vocabulary, the error set and the fakes are baselined and handed to this story.
- The rwb-payment event is available for the fake: one payment received after charge-off, matched to the case and to the placement (context pack connection matrix, row S7). The event name and its payload are Not specified in the source documents (GAP-3046; ASM-5115).
- The rwb-source-data read is available for the fake: the payment, the account and the customer facts of the charged-off case. The operation name is Not specified in the source documents (GAP-3046; ASM-5116).
- The rwb-case reference-data read is available for the fake: the agency fee schedule row and the placement facts at their version. The operation name is Not specified in the source documents (GAP-3046; ASM-5117).
- The rwb-payment `postProceeds` activity is available for the stub on the P8 queue: the income posting to ALS and the general ledger, and the posted date it confirms (ASM-5120).
- The WO package copy in force carries R-WO-37 and R-WO-49 with the version to record; the package is governed in rwb-decision and delivered to this service (DP-04 row, recorded, not claimed: ASM-5119).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service, rwb-case and rwb-payment through the gateway-bff composite route, one hop each (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case.recovery_case`, `rwb_payment.proceeds` or a `v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-02, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6027-CON when its tests pass.

### 4. Flow

1. rwb-payment publishes the payment event of a receipt matched to a charged-off account; this service's consumer group on `rwb.payment.events.v1` writes one inbox row and signals the recovery branch of `WriteOffWorkflow` on queue `rwb-writeoff` (ASM-5115).
2. The branch loads the `write_off` row of `rwb_writeoff` by the case reference, with `state`, `amount`, `tax_criteria_met`, `recovered_after` and the record reference.
3. `PostChargeOffMatcher` reads the payment, the account and the customer facts on rwb-source-data's contract and checks that the payment matches the case and, where the case carries one, the placement (DP-05; ASM-5116).
4. `PostChargeOffEvaluator` reads the WO package version in force and applies R-WO-37 where the `write_off` state is `PLACED_WITH_AGENCY` and the payment matches the placement, and R-WO-49 where the state is `CASE_CLOSED` and the payment matches a closed case with no placement.
5. Where R-WO-37 fires, `AgencyFeeClient` reads the fee schedule row of the placement and the panel facts on the reference-data contract at their version and returns the fee reference the rule asks for (GAP-3048; ASM-5117, ASM-5118).
6. `WriteOffRecoveryRecordWriter` writes one decision record through the local library, **before any change**, with the case reference, the write-off reference, the payment reference, the recovery amount, the rule ID and its version, the package version, the fee reference and the outcome. A failed write stops the act with nothing changed (DP-03; legacy AC1, AC2, AC3 and AC4).
7. `PaymentPostingClient` starts the `postProceeds` activity on rwb-payment's queue with the case, the account, the recovery amount and the income code of the rule, and waits for the posting confirmation and the posted date (ASM-5120).
8. `WriteOffRecoveryWriter` updates the `write_off` row in one `rwb_writeoff` transaction with the inbox row, the record, the idempotency row and the optimistic lock of `version`: `state` becomes `PAYMENT_MATCHED`, `recovered_after` holds the recovery amount (DF-FIN-020), `posted_date` holds the confirmed posting date (DF-FIN-016) and `decision_log_id` holds the identifier the library returns (DF-FIN-012).
9. `CaseMoveAnswer` answers rwb-case with the move `PAYMENT_MATCHED`, the rule ID, the version and the decided-at time; rwb-case writes the case of record and the parent `CaseWorkflow` applies the move (ASM-5121).
10. The step publishes no event of its own; the write-off event `WriteOffApproved` (`EV-24`) is the approval path's and is not raised here (ASM-5122).
11. SCR-27 in its approved state shows the recovery, the posting date and the fee reference of the write-off through the composite route, next to the case route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no state, no recovery amount, no posting date, no record reference, no posting and no case move | MSG-P7-003 | AC4, TC-E6-027-04, TC-E6-027-06 |
| X2 | The payment does not match the case, the account or the placement the `write_off` row names | The rule does not fire, nothing is written and the event is raised to the reconciliation of the key, never applied by default | None | AC2, AC3 |
| X3 | The `write_off` row is in a state neither R-WO-37 nor R-WO-49 names | The event is parked in the inbox and reported; nothing is written and no state changes | None | AC1, AC2, AC3 |
| X4 | The posting activity on the P8 queue does not confirm | The step retries on the workflow's own schedule; the row keeps its state and its recovery amount is not committed | None | AC2, AC3 |
| X5 | The fee schedule row of the placement is absent or its version is stale | R-WO-37 does not fire and nothing is written; the gap is raised to the reference-data owner, never defaulted to a local fee | MSG-GEN-001 | AC2 |
| X6 | A data product is stale after a late or failed ACE batch | The step does not evaluate on stale facts and answers the caller with the product and its date | MSG-P1-001 | AC1, AC3 |
| X7 | The rwb-source-data or reference-data contract does not answer inside 2 s, or its breaker is open | The event is retried on the workflow's schedule; nothing is written and the inbox row holds the attempt | None | AC1, AC2, AC3 |
| X8 | The same payment event is delivered twice | One inbox row, one record, one row update and one case-move answer; the repeat is counted and dropped | None | AC2 |
| X9 | A component, a statement or a test reaches another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E6-027-09, Section 17, BR6 |

X1 and X2 are the exception paths of RWB-E6-027 carried onto the split (AC4 and the "matches" conditions of R-WO-37 and R-WO-49), X3 to X8 are the paths the event trigger, the posting call, the reference data and the idempotency add, and X9 is the DP-01, DP-02 and DP-05 boundary. The fee schedule, the income code and the state list are values in force in reference data and in the package, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6027-CON, the rwb-payment event and posting stub, the rwb-source-data read fake, the reference-data fake and the decision-record stub, on its own schema, and needs no live P1, P3 or P8 |
| Negotiable | The activity and component names, the consumer group name and the shape of the stage outcome are this story's choice; the rules, the messages, the state values, the `write_off` columns and the naming are fixed |
| Valuable | A payment after charge-off is posted as income, the recovery is recorded once on the write-off, the fee is referenced, and the case moves with the rule version provable from the record |
| Estimable | One event consumer, one workflow branch, one matcher, one evaluator, three clients, one record write, one row update and one case-move answer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic payments, placements and package versions through the contract fakes, plus the component cases of the failed record write and the stale data product |

### 7. Acceptance criteria

```gherkin
Feature: Record a customer payment after charge-off

  Background:
    Given write-off "WO-2027-000221" carries case "RC-2027-000712" in schema rwb_writeoff
    Given the WO rule package is in force at its version and carries R-WO-37 and R-WO-49
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record a customer payment after charge-off (legacy RWB-E6-027 AC1)
    Given the rwb-payment contract mock returns a payment received after charge-off matched to case "RC-2027-000712"
    Given the rwb-source-data contract mock returns the payment, the account and the customer facts of "RC-2027-000712"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes a payment on a charged-off balance, applies it and records the recovery
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-WO-37 (legacy RWB-E6-027 AC2)
    Given the rwb-payment contract mock returns a payment matched to case "RC-2027-000712" and to its agency placement
    Given the rwb-case contract mock returns the fee schedule row of that placement with its version
    Given a case in state PLACED_WITH_AGENCY
    When payment received after chargeoff
    Then post the recovery as post charge-off income and calculate the agency fee
    Then the case moves to PAYMENT_MATCHED

  Scenario: AC3 Rule R-WO-49 (legacy RWB-E6-027 AC3)
    Given the rwb-payment contract mock returns a payment matched to closed case "RC-2027-000744" with no placement
    Given a case in state CASE_CLOSED
    When payment received after chargeoff
    Then post the recovery as post charge-off income against the closed case
    Then the case moves to PAYMENT_MATCHED

  Scenario: AC4 Not recorded (legacy RWB-E6-027 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 A component, a statement or a test reaches another service's schema or a `v_ace_*` view is refused (new, D-RCV-60)
    Given a component, a statement or a test names another service's schema or a `v_ace_*` view
    When the boundary test runs in the build
    Then the grant refuses the statement and the boundary test fails the build; nothing is released

  Scenario: AC6 The business rules BR1 to BR11 are each covered by a criterion or a guardrail (new, D-RCV-60)
    Given the business rules of section 8 are in force
    When the build runs its checks
    Then each rule BR1 to BR11 is covered by a criterion, a guardrail or a boundary test

  Scenario: AC7 A posting activity that does not confirm leaves the row unchanged (new, D-RCV-60)
    Given the postProceeds activity on rwb-payment's queue does not confirm
    When the step retries on the workflow's own schedule
    Then the write_off row keeps its state and its recovery amount is not committed

  Scenario: AC8 A consumed call that fails or does not answer writes nothing (new, D-RCV-60)
    Given the rwb-source-data contract does not answer inside 2 s, or its breaker is open
    When the event is processed
    Then the event is retried on the workflow's schedule and nothing is written

  Scenario: AC9 A state change the model does not allow is refused (new, D-RCV-60)
    Given the write_off row is in a state neither R-WO-37 nor R-WO-49 names
    When the payment event arrives
    Then the event is parked in the inbox and reported; nothing is written and no state changes
```

The four criteria are the legacy criteria of RWB-E6-027 word for word, with their origin tag added and the decision log wording changed to decision record (CG-ALL-11215), and nothing else changed: the repetition of `Then`, the legacy wording of `payment received after chargeoff`, `the action is taken` and `the data and the rule version this feature needs are in place` all stand. The cross-service parts are mocked, so AC1 carries two and AC2 and AC3 carry two `Given the <service> contract mock returns <x>` lines each; those added `Given` lines and the feature Background are the only additions. What the legacy lines describe now happens in three places: rwb-payment owns the receipt, its match and the posting of the proceeds, rwb-source-data owns the ACE facts, and this story evaluates R-WO-37 or R-WO-49, records the match, writes the recovery on the `write_off` row and answers the case move. Legacy AC2 and AC3 say "the case moves to PAYMENT_MATCHED": the case route state is rwb-case's and is answered, while `PAYMENT_MATCHED` is also the WRITEOFF state this service writes on `write_off.state` (ASM-5121). The decision record of AC1 and AC4 is the local decision record of DP-03 written before the row changes, plus the ledger entry rwb-decision writes.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-37 | Write-off | D9 | PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | Post the recovery as post charge-off income and calculate the agency fee | PAYMENT_MATCHED | Workbench | ALS core and GL, Agent Runtime | next working day |
| R-WO-49 | Write-off | D9 | CASE_CLOSED | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches a closed case with no placement | Post the recovery as post charge-off income against the closed case | PAYMENT_MATCHED | Workbench | ALS core and GL | next working day |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character, and they are rows of the WRITEOFF machine of TSD S7 T4. Their owner column is a role of the business and not a service: the money is rwb-payment's, the field facts are rwb-source-data's, the case move is answered to rwb-case, and the ledger entry is rwb-decision's. R-WO-50, the post charge-off sale, is RWB-S7-E6028-APP's; R-WO-01 to R-WO-25, the scan, the pack, the committee and the posting, are the stories of this key named in section 19.

| ID | Rule | Source |
|---|---|---|
| BR1 | The recovery, its posting date and the record reference are this service's: `recovered_after`, `posted_date` and `decision_log_id` are columns of `write_off` in `rwb_writeoff`, and no other service writes them | Context pack ownership row `write_off`; TSD S7 T3.1 (DF-FIN-012, DF-FIN-016, DF-FIN-020); DP-01 |
| BR2 | The decision is recorded before the `write_off` row changes, with the rule ID, the package version in force, the payment reference and the recovery amount; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy RWB-E6-027 AC1 to AC4 |
| BR3 | The payment, its match and the posting of the proceeds stay with rwb-payment: this service consumes ProceedsMatched (EV-25) as the match, records the recovery, the income and the agency fee here, holds a payment that matches nothing in the exception list this module shows, and starts the `postProceeds` activity; the ownership of the initial match is an open question with the P8 owner | FEAT-PAY-01; context pack connection matrix, row S7; FSD S7 A2.15.2 |
| BR4 | The ACE payment, account and customer facts are read only through rwb-source-data's contract; this service holds no `v_ace_*` grant and copies no ACE row | DP-05; context pack naming rules; ASM-5116 |
| BR5 | The agency fee is a value of the fee-schedule reference row at its version, read as reference data; the fee calculation belongs to rwb-partner (FEAT-PRM-07), this service records the fee reference in the decision record only, and the fee ownership question is open with the solution architect before the baseline tag; no fee is a constant, a default or a branch of the build | R-WO-37 action; GAP-3048; ASM-5117, ASM-5118, ASM-5124; Epics 3 to 8 Specification v3 FEAT-PRM-07 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; the case, the payment and the placement are identifiers of other services' facts | DP-01, DP-02; TSD S7 T3.3 |
| BR7 | R-WO-37 requires the `write_off` state `PLACED_WITH_AGENCY` and a payment that matches the placement; R-WO-49 requires `CASE_CLOSED` and a payment that matches a closed case with no placement; in both cases the state becomes `PAYMENT_MATCHED` | Business Rules and Routing Logic v4 rows R-WO-37 and R-WO-49; TSD S7 T4 |
| BR8 | The case and its route states stay with rwb-case: this service reads the case reference from its own row, writes no `recovery_case` row and answers the move | ASM-5121 |
| BR9 | No value a business person may change is written in code: the income code, the fee schedule, the posting parameters and the state list are read from reference data and the package at their version | FSD S7 A2.15.3.1 BR-S7-015; Template and Rules §R7.2 (s17) |
| BR10 | A stale data product stops the evaluation: the step does not apply a rule to facts a late or failed batch left behind | FSD S7 A2.15.3.1 VR-S7-015-1; MSG-P1-001 |
| BR11 | No person name, contact value or identity number enters `rwb_writeoff`, the decision record, an event, a log or a workflow input | Template and Rules §R7.2 (s17); context pack naming rule on PII |

BR1 to BR11 are each checked by AC6 and test case TC-E6-027-10 (NEWAC-RWB-S7-E6027-APP-AC6).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR8). What this story writes is the WRITEOFF state of the `write_off` row.

| From (WRITEOFF, `write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `PLACED_WITH_AGENCY` | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` under R-WO-37 | the payment matches the case and the placement | `PAYMENT_MATCHED`, with the recovery, the posting date, the record reference and the fee reference written, the proceeds posted and the case move answered |
| `CASE_CLOSED` | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` under R-WO-49 | the payment matches a closed case with no placement | `PAYMENT_MATCHED`, with the recovery, the posting date and the record reference written, the proceeds posted and the case move answered |
| Any state the rule does not name | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` | X3 | Unchanged, the event is parked in the inbox and reported |
| `PLACED_WITH_AGENCY` | `PAYMENT_RECEIVED_AFTER_CHARGEOFF` where no fee-schedule row matches | X5 | Unchanged, the rule does not fire and the gap is raised |
| `PAYMENT_MATCHED` | A second delivery of the same payment | X8 | Unchanged, the repeat is dropped |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The payment event arrives on `rwb.payment.events.v1` | The inbox row is written and the branch is signalled | Matching |
| Matching | The payment matches the case and the placement | R-WO-37 or R-WO-49 fires | Recording |
| Recording | The record, the posting and the row are written | The posting confirms and the transaction commits | Waiting for the next event |
| Recording | The record write, the posting or the transaction fails | X1, X4 | Waiting, nothing changed |

`PLACED_WITH_AGENCY`, `CASE_CLOSED` and `PAYMENT_MATCHED` are WRITEOFF states of TSD S7 T4 and of the rule table; the states the other stories of this key read or write — `SCAN_DUE`, `POPULATION_PROPOSED`, `WITH_COMMITTEE`, `APPROVED`, `POSTED` — are untouched here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-writeoff service identity | Consumes the payment event, evaluates R-WO-37 and R-WO-49, writes the record and the row and answers the case move; TSD S7 T6.2 gives service identities the same checks as people, and the FSD names the act "None; runs unattended" |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA in TSD S7 T6.1: reads the recovery, the posting date and the fee reference on SCR-27 and works the exception the failed record write raises; the FSD names this role the other user of the feature |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the recovery of the case |
| RW-PRODHEAD, RW-WOCOMM, RW-FINANCE | Write-off and posting RA: read the recovery and the fee reference of the write-offs they approved |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-DATALOAD, SY-AGENT, SY-RULES | Write-off and posting U and R as TSD S7 T6.1 gives them: no act of this story and no right to change the recovery |

The act itself belongs to no role: it is the service identity's, triggered by rwb-payment's event, and the legacy permission table's A and C rights belong to the committee decision and to the scan, which are RWB-S7-E6018-APP's and RWB-S7-E6013-APP's. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and built by the platform (ASM-5119).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the event, the record and the case move |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case the payment is matched to |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision-record library returns |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the balance written off, never changed by a recovery |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the tax criteria result behind the posted write-off |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Write, the posting date the `postProceeds` activity confirms (ASM-5120) |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Write, the post charge-off recovery amount of this story |
| DF-FIN-017, DF-FIN-018, DF-FIN-019 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product | Not written here: the posting parameters of the write-off, read as they stand |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `state`, `updated_at`, `updated_by` and the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, payment reference, recovery amount, fee reference, outcome, decided at | Write through the local library, before the `write_off` row changes |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment (P1) | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Not read as a table: the payment facts arrive on the rwb-source-data read and on the payment event (ASM-5116) |
| DF-ACE-001 to DF-ACE-042 | v_ace_account (P1) | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Not read as a table: the account facts arrive on the rwb-source-data read |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer (P1) | person_key, cif_no, customer_status and the rest | Not read as a table, and no personal field is copied here |
| DF-PRT-001 to DF-PRT-007 | partner (S9) | partner_code, partner_type, panel_status, contract_end and the rest | Not read as a table: the placement and fee-schedule facts arrive on the reference-data contract (ASM-5117) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, status, stage_code and the rest | Not read as a table: the case reference is on the `write_off` row and the move is answered |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | id, case_id, decision_code, rule_id, rule_version and the rest | Not written here: rwb-decision writes the ledger entry |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes four of its existing columns, and `decision_record`, `inbox_event` and `idempotency_key` are platform library objects created in `rwb_writeoff` by the library's own migration (DP-03). `decision_record` and `inbox_event` are not entities or fields of the Logical Data Model v9 or Data Classification v5; the library defines them under DP-03. The legacy Data table lists six entities; five are other services' and are consumed on their contracts as the rows above state. The agency fee has no column, so it is carried in the decision record only (ASM-5124).

**No personal data.** The rows this story writes carry identifiers, an amount, a date, a code and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The act is triggered by rwb-payment's event, and no source publishes a recovery operation for rwb-writeoff: the module's two operations, `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A), belong to RWB-S7-E6013-APP and RWB-S7-E6018-APP, and the legacy Endpoints table repeats those same two rows for this story (GAP-3046; ASM-5114). The read the officer makes on SCR-27 is the composite route's, not an operation of this service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The payment, account and customer read (operation name Not specified in the source documents (GAP-3046; ASM-5116)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The payment, the account and the customer facts that prove the match; faked |
| The reference-data read of the fee schedule and the placement (operation name Not specified in the source documents (GAP-3046; ASM-5117)) | `/api/recovery/case/v1` | P3 rwb-case, reference data under the default ruling | The fee schedule row of the placement, the panel facts and their version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). Both rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3046, GAP-3048).

#### 12.3 Events published

None. No source gives this step an event of its own: `WriteOffApproved` (`EV-24`) is the service's only published event and it is the approval path's (RWB-S7-E6018-APP), so a recovery published under that name would be a false approval. The recovery reaches rwb-reporting only through the write-off events of the key, which is a reporting gap and is raised with the proposal to allocate one event on `rwb.writeoff.events.v1` (GAP-3046; ASM-5122). The step holds no outbox row and the check of this story fails a build that publishes here.

#### 12.4 Events consumed

| Event | Topic | Owner | Payload | Use |
|---|---|---|---|---|
| The payment received after charge-off event (event name and payload Not specified in the source documents (GAP-3046; ASM-5115)) | `rwb.payment.events.v1`, with its retry and `.dlt` topics | P8 rwb-payment | The matched payment and its case, account and placement references, with no personal data | The trigger of the step: writes one inbox row and signals the recovery branch |

The consumer group is this service's and the inbox row is written in the same `rwb_writeoff` transaction as the recovery (DP-09 as a platform object, recorded as an absent plan row: ASM-5115). A repeated delivery is dropped by the inbox key (X8).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the stage child of `CaseWorkflow` | `rwb-writeoff` | Input: the case, the write-off and the package in force; signals: the payment event and the case state |
| Recovery step of `WriteOffWorkflow` (not a separate catalogued workflow) | Step within `WriteOffWorkflow`, the step from the payment event to `PAYMENT_MATCHED` | `rwb-writeoff` | Matches, applies R-WO-37 or R-WO-49, posts the proceeds, writes the record and the row and answers the case move |
| `applyPostChargeOffRecovery` | Activity, the one step of this story | `rwb-writeoff` | The payment, the `write_off` row, the fee schedule and the package answer in; the rule ID with its version, the recovery amount, the posted date, the state, the record reference and the case move out |
| `postProceeds` | Activity, consumed on rwb-payment's queue | `rwb-payment` (P8) | The case, the account, the recovery amount and the income code in; the posting reference and the posted date out; declared as another service's and not registered here |

The activity names are target design choices of this story and are fixed by no source document; `postProceeds` is the payment activity the Temporal and Drools Design slide 12 names in the L4 activity contracts of the platform.

Workflow ID form and start rule of `WriteOffWorkflow`: Not specified in the source documents (CG-ALL-11209). The catalog row gives the trigger only: JOB-16 on the third working day after AceDataReady (R-WO-01) (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040).

#### 12.6 Schedules

None. The step is event-driven and owns no Temporal Schedule, no Quartz row and no shared job table. `JOB-16`, the monthly write-off scan, becomes the Schedule of R-WO-01 in RWB-S7-E6013-APP and is named here only as another story's (GAP-3046).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story writes `recovered_after`, `posted_date`, `state` and `decision_log_id` |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the match, the recovery amount and the fee reference (DP-03) |
| inbox_event | PLT library, created in `rwb_writeoff` | The row of the consumed payment event and its idempotency key |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated delivery and the answer it holds |

Not owned and never read as a table: `recovery_case` and `queue` (P3), `proceeds` and `payment` (P8), `partner` (S9), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and every `v_ace_*` view (P1). No foreign key leaves the schema and `write_off.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment event fake | A payment received after charge-off matched to case `RC-2027-000712` and its placement, a payment matched to closed case `RC-2027-000744` with no placement, a payment that matches nothing, and the same event delivered twice | AC1, AC2, AC3, X2, X8 |
| rwb-payment posting stub | A confirmed posting with its reference and posted date, a timeout, and a refusal | AC2, AC3, X4 |
| rwb-source-data read fake | The payment, the account and the customer facts of the two cases, a fact set that contradicts the case, and no answer beyond 2 s | AC1, AC2, AC3, X7 |
| rwb-case reference-data fake | A fee schedule row with its version for the placement of `RC-2027-000712`, no row for the placement, and a stale version | AC2, X5 |
| rwb-case case-move fake | The move `PAYMENT_MATCHED` accepted with the rule version, and a move refused because the case has already moved | AC2, AC3 |
| WO package fixture | The package at its version in force with R-WO-37 and R-WO-49 among its 51 rules over 27 states | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2027-000221` in its approved state, with the recovery and the fee reference | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the payment event, the payment read, the reference-data read and the posting activity are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3046; ASM-5115, ASM-5116, ASM-5117, ASM-5120).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The rwb-source-data payment read and the rwb-case reference-data read of the fee schedule; one hop, 2 s |
| Kafka | 0 published, 1 consumed | The payment received after charge-off event on `rwb.payment.events.v1` through the inbox; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity registered, 1 consumed | `WriteOffWorkflow` and its recovery branch on `rwb-writeoff`, with `applyPostChargeOffRecovery`; `postProceeds` on the P8 queue; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the pack documents are rwb-document's (P5) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.writeoff`, module `recovery`, Java package `th.co.scb.ace.workbench.recovery.writeoff.recovery`; front end `src/modules/recovery/writeoff/WriteOffRecovery.tsx`, the fragment SCR-27 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record of the match, the recovery amount and the fee reference commits with the `write_off` update or not at all, and the failed write is MSG-P7-003. DP-05 is read as rwb-source-data's contract, because the views are read only by P1 and this service holds no `v_ace_*` grant; the row adds no dependency (ASM-5116). DP-13 moves the base of the module's two operations, which this story does not declare. DP-19 is how SCR-27 reaches this service and rwb-case, one hop through the gateway. DP-04, DP-07, DP-09 and DP-16 appear in the sources and are recorded rather than claimed: the package is a governed copy, the fee schedule is reference data, the inbox is a platform object and the posting is P8's activity (GAP-3048; ASM-5115, ASM-5117, ASM-5120).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. The two consumed rows and the consumed payment event are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 (GAP-3048). The act is event-driven: it exposes no operation and publishes no event of its own. The consumed payment event's topic, name and payload are Not specified in the source documents (GAP-3047); the payment read on rwb-source-data, the reference-data read on rwb-case and the posting activity names are Not specified in the source documents (GAP-3047) until their owners publish them. The reporting gap is raised (GAP-3046), and one recovery event is proposed to its owner, with its topic and name Not specified in the source documents (GAP-3046). R-WO-30, R-WO-33, R-WO-34 and R-WO-35 (agency placement, result and recall through the S9 partner portal) are carried as product behaviour only: no placement decision is made until the partner contract is published in the same wave, and the placement slice is sequenced last inside wave 4.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` recovery branch | Workflow | Waits for the payment event, loads the row, applies R-WO-37 or R-WO-49 and answers the case move |
| `applyPostChargeOffRecovery` | Activity | The one step: match, evaluate, post, record, write and answer, in one transaction |
| `WriteOffRecoveryConsumer` | Consumer | The consumer group of `rwb.payment.events.v1`, the inbox row and the signal to the branch |
| `PostChargeOffMatcher` | Service | The match of the payment to the case, the account and the placement |
| `PostChargeOffEvaluator` | Service | The rule evaluation against the WO package version in force and the WRITEOFF state |
| `SourceDataClient` | Client | The payment, account and customer read of rwb-source-data; one hop, 2 s, breaker |
| `AgencyFeeClient` | Client | The fee schedule and panel read of the reference-data contract, consumed as a reference-data row of the fee schedule with the fee reference carried on the decision record only; one hop, 2 s, breaker |
| `PaymentPostingClient` | Client | The `postProceeds` activity on the P8 queue and the posting confirmation |
| `WriteOffRecoveryRecordWriter` | Library adapter | Writes the decision record before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `WriteOffRecoveryWriter` | Repository | Updates `state`, `recovered_after`, `posted_date` and `decision_log_id` in one `rwb_writeoff` transaction, with the inbox row and the optimistic lock |
| `CaseMoveAnswer` | Client | The child workflow's outcome, answered to rwb-case as the case boundary, with the rule ID and its version |
| `WriteOffRecovery` | React component | Shows the recovery, the posting date and the fee reference on SCR-27, with the not-recorded and the posting-pending states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the decision record, the inbox and the idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03, ASM-5115). No column is added: `recovered_after` (DF-FIN-020), `posted_date` (DF-FIN-016) and `decision_log_id` (DF-FIN-012) exist, and `state` is the standard record column of TSD S7 T3.0. The other schemas named in this section are owned by their services: `rwb_case` by rwb-case, `rwb_partner` by rwb-partner (S9) and `rwb_payment` by rwb-payment. This service writes none of them and reaches each only on its contract (BR3, BR6, BR8).

**Configuration and reference data.**

- The WO package and its rows R-WO-37 and R-WO-49 with the income code and the state list, read as package values at their version, never as constants.
- The agency fee schedule and the placement facts, read as reference data at their version; a missing or stale row is X5 and never a local fee (ASM-5117, ASM-5118).
- The posting parameters the write-off carries — responsibility centre, cost centre and GL product — read as they stand and never recomputed here.
- The stale-product rule of VR-S7-015-1 and the 2 s budget and single hop of ADR-020.
- The feature flag of the step, read from the platform library, never a build constant.

**Build steps**

1. `WriteOffRecoveryConsumer` and the inbox row on `rwb.payment.events.v1` against the event fake, with the repeated delivery (AC1, X8).
2. The recovery branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow` (AC1).
3. `SourceDataClient` against its fake, with the match and the no-answer path (AC1, AC2, AC3, X2, X7).
4. `AgencyFeeClient` and `PostChargeOffEvaluator` over R-WO-37, R-WO-49 and the WRITEOFF state, with the no-row and stale-version paths (AC2, AC3, X3, X5).
5. `WriteOffRecoveryRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `PaymentPostingClient` and the `postProceeds` stub, with the posting-pending path (AC2, AC3, X4).
7. `WriteOffRecoveryWriter` with the one transaction, the four columns, the inbox row and the optimistic lock (AC2, AC3).
8. `CaseMoveAnswer` and the parent signal, with the move `PAYMENT_MATCHED` (AC2, AC3).
9. The stale-product guard and MSG-P1-001 (AC1, X6).
10. The `WriteOffRecovery` fragment and the composite route fake (AC1).
11. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_payment` or `rwb_partner` (X9, BR6).

**Feature flag.** `rwb.writeoff.post-chargeoff-recovery-v1`, read as a flag of the platform library; off means the consumer stops at the inbox and the branch holds the event, writing nothing and publishing nothing, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic payment event in SIT, R-WO-37 and R-WO-49 each produce their record, their recovery, their posting date and their case move, a repeated event writes once, a forced record failure changes nothing, the stale-product path answers MSG-P1-001, no `recovery_case`, `proceeds`, `partner`, `rule_row` or `decision_log_entry` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product this step reads is stale after a late or failed ACE batch (X6) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A fee-schedule field is absent or invalid, or no fee row matches the placement (X5) | Enter {field}. |
| MSG-P4-002 | A role reads or changes the recovery without the Write-off and posting right of the capability area (section 10) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the `write_off` row changes (X1), and the officer sees it on SCR-27 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan gate R-WO-03 and RWB-S7-E6013-APP's path, so no path of this story raises it | The scan is on hold until Finance publishes the tax criteria. |

The five message IDs are those of the legacy message set of this key and of the FSD, and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001 whose text is copied from the Error and Message Standard v4 (CG-ALL-11212); MSG-P1-001 is the stale-product message of FSD S7 A2.15.3.1. No message is reworded or added.

### 15. Screens and states

SCR-27 Write-off proposal — "the monthly population, the pack per case and removals with reasons", first in E6 (FSD S7 Screens) — is the nearest screen of this step, in its approved state: it shows the posted write-off with its recovery, its posting date and its fee reference. It is served through the gateway-bff composite route (DP-19): the route calls this service for the `write_off` row and its recovery, rwb-case for the case and its route state, and rwb-payment for the receipt and the posting. The step itself is unattended, and no screen of this key shows a post charge-off recovery at the population level; the officer reaches the case on SCR-27 and on the case view of rwb-case (GAP-3046).

The states this story produces are the write-off's `PAYMENT_MATCHED` with its recovery and its posting date, the posting-pending state while the P8 activity runs, the not-recorded state with MSG-P7-003, the stale-product state with MSG-P1-001 and the parked state of an event whose state no rule names. The scan, proposed, in-committee, rejected and deferred states belong to other stories of this key. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-11216).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-027-01 | AC1 | Component | The payment event on `RC-2027-000712`; the match, the record, the recovery, the posting and the case move asserted on the fakes |
| TC-E6-027-02 | AC2 | Integration | R-WO-37 on a `PLACED_WITH_AGENCY` write-off with the fee schedule above and a payment that matches the placement; the `PAYMENT_MATCHED` state, the recovery, the posted date, the fee reference and the case move asserted across the rwb-payment, rwb-source-data and rwb-case fakes |
| TC-E6-027-03 | AC3 | Integration | R-WO-49 on a `CASE_CLOSED` write-off with no placement; the same assertions without a fee reference, across the same fakes |
| TC-E6-027-04 | AC4 | Component | The decision-record stub stopped; nothing written, no recovery, no posting, no move answered and MSG-P7-003 shown |
| TC-E6-027-05 | Access | Component | A role without the Write-off and posting right on the read path; MSG-P4-002 and no write |
| TC-E6-027-06 | Principle 5 | Component | A forced decision record write failure at the moment of the row update; no column changed, no posting confirmed and no move answered |
| TC-E6-027-07 | Contract (section 12) | Integration | Each operation, event and activity named in section 12 checked against its catalogued or yaml contract; no other operation, event or activity called |
| TC-E6-027-08 | Boundary (section 12.7, ASM-3438) | Component | Each table of section 12.7 read and written only as section 12.7 states; the tables it names as not owned are not read |
| TC-E6-027-09 | AC5 | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC5) | A statement naming another service's schema and a `v_ace_*` view; the grant refuses it, the boundary test fails the build and nothing is released |
| TC-E6-027-10 | AC6 | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC6) | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC6) |
| TC-E6-027-11 | AC7 | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC7) | The postProceeds activity on the rwb-payment fake not confirming; retried on the workflow's schedule; the row state and the recovery amount asserted unchanged |
| TC-E6-027-12 | AC8 | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC8) | The rwb-source-data fake not answering inside 2 s; nothing written, the inbox row holds the attempt and the call is retried on the workflow's schedule |
| TC-E6-027-13 | AC9 | Not specified in the source documents (NEWAC-RWB-S7-E6027-APP-AC9) | A write_off row in a state neither R-WO-37 nor R-WO-49 names; the event parked and reported, no state changed |

The six legacy cases are the legacy cases of RWB-E6-027 in their legacy order, with the Level column added: TC-E6-027-01, -04, -05 and -06 map to `Component` because the step is tested on its fakes, and -02 and -03 map to `Integration` because they cross the rwb-payment, rwb-source-data and rwb-case boundaries. The full test, with its Given, When and Then, is to be added to the next Recovery Workbench Test Cases version, tab Story test cases, under the same test case ID (CG-ALL-11213); no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the income code, the fee schedule, the posting parameters, the state list and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates and a rule version only, and every fixture is synthetic. `v_ace_customer` is never copied here.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-01, DP-02, DP-05).
- The money stays with rwb-payment and the ledger with rwb-decision: no receipt, no proceeds and no ledger entry is created here (BR3).
- The case and its route states stay with rwb-case: no `recovery_case` row is read or written (BR8).
- The fee is never derived locally: where the fee-schedule row is missing or stale, R-WO-37 does not fire and the gap is raised (BR5, X5).
- The decision is recorded before the change and the record, the posting and the row update commit together; a build that writes the row first fails the review (DP-03).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second topic and no event of this step on `rwb.writeoff.events.v1`.
- A stale data product stops the evaluation; a build that applies a rule to stale facts fails the test of X6.

### 18. Traceability

| Requirement ID | Feature | L3 process | Requirement (short) | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S7-007 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Recoveries after charge-off are matched to the account, with income and agency fees recorded (Must, E6) | The consumer, the matcher, the income posting, the fee reference and the recovery column | TC-E6-027-01, TC-E6-027-02, TC-E6-027-03 |
| REQ-S7-006 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Post charge-off treatment is set by rule, including placement with an agency (Must, E6); this story applies the rule to a placement that exists, and the placement itself is RWB-S9-E6034-APP's | R-WO-37 and R-WO-49 | TC-E6-027-02, TC-E6-027-03 |
| ADR-013 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | 19 services inside ACE | rwb-writeoff as the owner of the write-off row and its recovery | TC-E6-027-01 |
| ADR-014 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-027-06 |
| ADR-015 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Kafka with outbox, inbox and CloudEvents | The inbox row of the consumed payment event | TC-E6-027-01 |
| ADR-020 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget | TC-E6-027-02, TC-E6-027-03 |
| ADR-022 | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Not specified in the source documents (DOR-RWB-S7-E6027-APP-2) | Local decision record plus central ledger | The record of the match, the recovery and the fee reference, with the ledger entry in P7 | TC-E6-027-04, TC-E6-027-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-027, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-027-01 to TC-E6-027-06 |
| Feature and screens | FEAT-WOF-15, SCR-27 Write-off proposal |
| Rules | R-WO-37 and R-WO-49, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the `write_off` recovery element, the consumed payment event, the fee reference, the case-move answer, the state vocabulary, the error set and the fakes: RWB-S7-E6027-CON.
- The receipt, its match and the posting of the proceeds to ALS and the general ledger: rwb-payment (P8) and FEAT-PAY-01, whose `postProceeds` activity this story consumes (ASM-5120).
- The ACE payment, account and customer facts: rwb-source-data (P1), read on its contract and never as a view (DP-05).
- The agency placement and the agency fee calculation: RWB-S9-E6034-APP and RWB-S9-E6035-APP (FEAT-PRM-06 and FEAT-PRM-07), whose fee this story references only (GAP-3048).
- The case of record, its route states and the case-move operation name: rwb-case (P3), whose move this story answers and fakes (ASM-5121).
- The fee schedule, its owner, its versions and the reference-data contract: carried as consumed with the placeholder (GAP-3046; ASM-5117).
- The WO package, its version, the income code and the ledger: rwb-decision (P7) (ASM-5119).
- The monthly scan, the tax criteria and JOB-16: RWB-S7-E6013-APP and RWB-S7-E6014-APP. The pack, the removal and the routing: RWB-S7-E6015-APP to RWB-S7-E6017-APP. The approve, reject and defer: RWB-S7-E6018-APP to RWB-S7-E6020-APP.
- The posting of an approved write-off, the provision inputs, the reconciliation, the exception loop and the case closure after retention: RWB-S7-E6021-APP to RWB-S7-E6025-APP.
- The post charge-off sale and R-WO-50: RWB-S7-E6028-APP.
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- A published recovery event and the reporting read model that would need it: carried as a gap and not built here (GAP-3046; ASM-5122).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
