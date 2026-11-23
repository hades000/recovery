# RWB-P3-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP11, DP15, DP19 |
| Parallel lane | L-P3-AA |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-033, FR-P3-034) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-006 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the credit approval pack for an approved restructure plan assembled at the case from the case record in `rwb_case`, the plan terms read through rwb-treatment, the account, collateral and valuation facts read through rwb-source-data, the checklist documents read through rwb-document and the required approval level read through the rwb-access delegation contract, and the NLEADS credit result recorded on the case in one transaction with its decision record, its route state and its queue**, so that **the credit outcome is on the case without re-keying the case facts and the case moves on that outcome**.

The legacy story put the pack and the result on two P2 Integration endpoints and the four NLEADS columns on the treatment. Under D-RCV-60 the case side belongs to rwb-case: FSD P3 v4 A2.33 carries FEAT-CHO-07 in module P3, and its change note reads NLEADS credit results from `v_ace_credit_decision`, so the decision is ACE data read through the rwb-source-data contract (DP-05, DP-11) and rwb-case is the only writer of `recovery_case.route_state` (DP-01). The pack and result resources of the integration base stay with rwb-integration and the four treatment columns stay with rwb-treatment, and both are carried by the P2 and S2 stories of this legacy key. This story owns the case-side pack facts, the result record, the route state, the queue move and the decision record.

### 2. Business rationale

A restructure outside the approved range, or one with a deviation flag, goes to credit approval (R-RES-10; about 44% of TDR cases deviate today). The bank decides it in NLEADS, which has no interface to the Workbench (INT-26), so officers re-key the case facts and the plan terms into NLEADS and the result never reaches the case record: the case either waits or is moved by hand. Control CTL-04 answers this audit finding for the approval level, and CTL-06 for the decision record.

In the target ACE ingests NLEADS overnight and the decision is available in `v_ace_credit_decision` (FSD P3 v4 change note); only rwb-source-data reads the thirty `recovery.v_ace_*` views, and every other service reads ACE facts through its contract (DP-05). rwb-case owns the case, the CMMN state, the queues, the tasks, the allocation and the timers (Arch v5 slide 41), so this story reads no ACE view and no foreign table (DP-01): the case number, the product group, the route state and the account links come from `rwb_case`, the balances and the appraisal from the rwb-source-data contract, the plan terms from the rwb-treatment contract, the documents from the rwb-document contract and the required level from the rwb-access delegation contract. The NLEADS pack checklist is reference data of rwb-case (DP-07, DL19).

Two legacy in-process calls disappear because the case owner is now this service. `CaseEvents.raise(caseId, "CREDIT_APPROVED" | "CREDIT_DECLINED", facts)` becomes a state change inside rwb-case (DP-11, DP-01), and the P7 `DecisionLogWriter` becomes the local decision-record library that writes in the same transaction as the state change and publishes on `rwb.decision-record.v1` for the central ledger in rwb-decision (DP-03, T1 of the Temporal and Drools design). A decision that cannot be recorded does not proceed (R-UNI-39).

The story meets REQ-CHO-008 (a plan submitted for credit approval is recorded on the case) and REQ-CHO-006 (the treatment holds its type, terms, approval and outcome), and it applies REQ-RDF-009: every input of the pack carries its age and every credit result records the freshness of the data it used.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The library writes the record and publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on the service's behalf.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, which carries the NLEADS pack checklist rows and the route-state list with the version in force (DP-07). The rwb-case CON story is a same-service contract story and is therefore listed as a build dependency.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and the migration conventions of `rwb_case` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 (DP-19).
- The `rwb_case` tables `recovery_case`, `case_account`, `queue`, `assignment` and `task` exist from the rwb_case baseline, and `recovery_case.route_state` holds the value `AWAITING_CREDIT_APPROVAL` for the case (DF-CAS-007).
- The case is in route state AWAITING_CREDIT_APPROVAL with an open RESTRUCTURE treatment, and its ACE plan status is APPROVED (RWB-E2-002).
- The NLEADS pack checklist is loaded as reference data (DL19; the items CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF are the ones the legacy story assumes).
- The delegation rows for item 2.1.1 are loaded in rwb-access (DL18) and are read through its `GET /doa-limits` contract, never from a rwb-case table.
- The input age limit for balances in a credit pack is 1 business day (assumed in the legacy story under DL22).
- The person holds RW-RESTRUCT, or RW-CASEOWN, with the case in scope.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0729; ASM-1281).

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record through gateway-bff and selects the credit approval pack.
2. gateway-bff: calls `GET /api/recovery/case/v1/cases/{caseId}/credit-approval` on rwb-case, and in parallel the plan-terms read on rwb-treatment and the account, collateral and freshness reads on rwb-source-data, then merges the answers into the screen model (DP-19).
3. rwb-case: checks the case scope and the Treatment and offer right through the rwb-access authorise contract, cached per session.
4. rwb-case: reads `recovery_case` for the case number, product group, route state and status, and `case_account` for the `account_key` and `is_primary` of the linked accounts, inside `rwb_case` only (DP-01).
5. rwb-case: reads the balance, arrears and `data_as_of` of each account, and the collateral and its latest appraisal, from the rwb-source-data contract by `account_key` (DP-05, DP-11).
6. rwb-case: reads the plan terms of the open RESTRUCTURE treatment (offer amount, haircut amount, installments, valid until, state) from the rwb-treatment contract.
7. rwb-case: reads the NLEADS pack checklist rows from the reference-data contract with the version in force, and the documents on the case from the rwb-document contract; each row is returned as present with its link, or as missing (DP-07).
8. rwb-case: reads the required approval level for decision D5, product group and amount for item 2.1.1 from the rwb-access delegation contract, with the version in force.
9. rwb-case: attaches the age of every input from the freshness of the ACE business date and the pack rules; an input past its limit is returned with its age and MSG-P7-006 (REQ-RDF-009).
10. rwb-case: returns the case-side pack: case number, product group, route state, the accounts with balances as of the ACE business date, the collateral with its latest appraisal, the plan terms, the checklist rows with links, the required level and the messages; no field needs to be typed by the officer.
11. Restructuring officer: submits the plan in NLEADS and receives the reference, and later the result.
12. ACE: ingests the NLEADS decision overnight, and `v_ace_credit_decision` carries the reference, result, approval level, result date and reason for the plan (FSD P3 v4 change note; INT-26 has no interface).
13. Restructuring officer: records the result through `POST /api/recovery/case/v1/cases/{caseId}/credit-result` with the NLEADS reference, the result, the approval level, the result date and, for a refusal, the reason, under `If-Match` and an `Idempotency-Key`.
14. rwb-case: validates the case state (AWAITING_CREDIT_APPROVAL with an open RESTRUCTURE treatment), that no result is recorded yet, that the recorded level is at or above the required level of item 2.1.1, the reference and reason rules, the result date and the version; a failure returns the problem and nothing changes.
15. rwb-case: reads the NLEADS decision behind the recorded values through the rwb-source-data contract, so the record cites the ACE row and not a re-keyed value.
16. RecordAndApply: in one `rwb_case` transaction the service writes the new `recovery_case` route state, the placement of the case in the case owner's queue with its task, and the decision record with decision "D5", the final call "approved" or "rejected", the NLEADS reference in the actions and the freshness of the data used; the library publishes DecisionRecorded on `rwb.decision-record.v1`. A failed record write rolls the whole transaction back.
17. An approval moves the route state to OFFER_WITH_CUSTOMER by R-RES-11 and releases the offer to the customer with its 14-day validity; a refusal moves it to DECLINED_BY_CREDIT by R-RES-12 with the reason recorded, then to BACK_TO_ROUTE_DECISION by R-RES-14, with the case in the case owner's queue.
18. rwb-case: signals the running CaseWorkflow with the new route state and the decision record reference, so the parent resumes on the credit outcome; the treatment state change (SUBMITTED to APPROVED or REFUSED) and the four treatment columns are written by rwb-treatment through its own contract in the S2 story of this legacy key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A checklist document is not on the case | The pack shows the item as missing, with the other items present | MSG-P2-009 | AC4, carried by the P2 story of this legacy key |
| X2 | A balance in the pack is older than its age limit | The pack shows the input age in days | MSG-P7-006 | AC5, carried by the P2 story of this legacy key; the age itself is shown here |
| X3 | The reference is empty, or a refusal has no reason | The result is refused; nothing changes | MSG-GEN-001 | AC6, carried by the P2 story |
| X4 | The result date is after today | The result is refused; nothing changes | MSG-GEN-002 | AC6, carried by the P2 story |
| X5 | The NLEADS approval level is below the level the plan needs | The result is refused; nothing changes | MSG-P2-018 | AC7, carried by the P2 story |
| X6 | A result is already recorded on the case | The result is refused and no second decision record is written | MSG-P2-010 | AC8, carried by the P2 and S2 stories |
| X7 | The case is not in AWAITING_CREDIT_APPROVAL, or its treatment is not a restructure | The result is refused; nothing changes | MSG-P3-005 | AC9 |
| X8 | The case changed between read and write | The result is refused; nothing changes | MSG-GEN-004 | AC10, carried by the P2 story |
| X9 | The decision record cannot be written | Nothing changes; an incident is raised | MSG-P7-003 | AC11 |
| X10 | A role without the Treatment and offer right opens the pack or records a result | Refused before any read or write | MSG-P4-002 | TC-E2-006-12, carried by the P2 story |
| X11 | rwb-source-data, rwb-treatment, rwb-document or rwb-access does not answer inside the REST budget | One hop, 2 s timeout; the pack returns the source message for that section, and the result is refused with nothing written | MSG-GEN-006 | AC1, AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts: the decision-record library, the reference-data contract, the migration conventions and the edge route. The rwb-source-data, rwb-treatment, rwb-document and rwb-access answers come from their contract fakes |
| Negotiable | The checklist rows, the age limit, the route-state list and the delegation levels are data values in the reference tables and the rwb-access tables; the story fixes only the behaviour |
| Valuable | Puts the NLEADS credit outcome and its approval level on the case, so the case moves by R-RES-11 or R-RES-12/R-RES-14 without re-keying |
| Estimable | Two endpoints, one query service, one transactional record path, one library integration, one screen panel |
| Small | Fits two weeks with its tests |
| Testable | Each owned criterion has a test case in section 16; every cross-service answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL"
    Given treatment "TRT-SYN-0610" of type "RESTRUCTURE" has offer amount 2,400,000.00 baht, haircut 0.00 baht and 84 installments
    Given the ACE plan status of the case is "APPROVED"
    Given the plan needs approval at level "L6" or higher under item 2.1.1

  Scenario: AC1 Pack prepared (legacy RWB-E2-006 AC1)
    Given an approved restructure plan on treatment "TRT-SYN-0610"
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments and valid until 2026-12-29
    Given the rwb-source-data contract mock returns 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal
    Given the rwb-access contract mock returns required approval level "L6" for item 2.1.1
    Given the rwb-document contract mock returns a link for each of the 5 checklist documents
    When the officer opens the credit approval pack on 2026-12-15
    Then the pack holds case number "RW-2026-000610", product group "MORTGAGE", 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal
    Then the pack holds the plan terms: offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments, valid until 2026-12-29
    Then the pack lists the 5 checklist documents with a link to each one on the case
    Then the system shows the required approval level "L6"
    Then no field in the pack needs to be typed by the officer

  Scenario: AC2 Result recorded (legacy RWB-E2-006 AC2)
    Given the officer has submitted the pack in NLEADS
    Given the rwb-source-data contract mock returns NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with reference "NL-SYN-000610" and state "APPROVED"
    When the officer records NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    Then the treatment carries the reference "NL-SYN-000610" and its state is "APPROVED"
    Then a decision log entry with decision "D5" and final call "approved" holds the NLEADS reference
    Then the route state moves to "OFFER_WITH_CUSTOMER" by R-RES-11

  Scenario: AC3 Refused (legacy RWB-E2-006 AC3)
    Given NLEADS refuses the plan with reason "Income does not cover 84 installments"
    Given the rwb-source-data contract mock returns NLEADS reference "NL-SYN-000611", result "REFUSED" and reason "Income does not cover 84 installments"
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with state "REFUSED" and the reason
    When the officer records reference "NL-SYN-000611", result "REFUSED" and the reason
    Then the treatment state is "REFUSED" and the treatment shows the reason
    Then the route state moves to "DECLINED_BY_CREDIT" by R-RES-12 and then to "BACK_TO_ROUTE_DECISION" by R-RES-14
    Then the case is in the case owner's queue

  Scenario: AC9 Case not awaiting credit approval (legacy RWB-E2-006 AC9)
    Given case "RW-2026-000620" is in route state "PLAN_RUNNING"
    Given the rwb-treatment contract mock returns a "RESTRUCTURE" treatment for case "RW-2026-000620"
    When the officer records a result for its treatment
    Then the response is 409 with message MSG-P3-005

  Scenario: AC11 Decision log write fails (legacy RWB-E2-006 AC11)
    Given the decision log store is unavailable
    When the officer records result "APPROVED" with reference "NL-SYN-000613" and approval level "L5"
    Then the response is 503 with message MSG-P7-003
    Then the treatment and the route state do not change
    Then the system raises an incident
```

AC1, AC2, AC3, AC9 and AC11 are the criteria this story owns; the values are copied unchanged from the legacy story, including the level "L5" that AC2 records against a plan the Background puts at "L6" or higher. The treatment statements in AC2 and AC3 are written by rwb-treatment and proved in the S2 story of this legacy key; here the rwb-treatment contract fake returns the recorded result. AC4 to AC8 and AC10, and the access case of TC-E2-006-12, are carried by the P2 story of this legacy key, which owns the pack and result resources of the integration base; the approval routing of the level is the P7 story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A restructure outside the approved range, or with a deviation, goes to credit approval and the case sits in AWAITING_CREDIT_APPROVAL | R-RES-10; legacy BR1 |
| BR2 | A credit approval releases the offer to the customer with a 14-day validity and moves the route state to OFFER_WITH_CUSTOMER | R-RES-11; legacy BR2 |
| BR3 | A credit refusal records the reason, moves the case to DECLINED_BY_CREDIT and then returns it to the route decision in the case owner's queue | R-RES-12, R-RES-14; legacy BR3 |
| BR4 | NLEADS has no interface: ACE ingests the NLEADS decision, and rwb-case reads it only through the rwb-source-data contract over `v_ace_credit_decision`; no service reads the view directly except rwb-source-data | INT-26; DL12; FSD P3 v4 change note; DP-05; ADR-010 |
| BR5 | The recorded approval level must be at or above the level the delegation of authority sets for the decision, the product and the amount, read from the rwb-access delegation contract with the version in force and recorded with the decision | doa.txt item 2.1.1; CTL-04; DL18; ownership map (`delegation_limit` is P4) |
| BR6 | The pack documents are the rows of the NLEADS pack checklist held as reference data of rwb-case, with the version in force; a row with no document on the case is shown as missing | Document types reference table; DL19; DP-07 |
| BR7 | Every input of the pack carries its age against its limit, and the credit result records the freshness of the data it used | MSG-P7-006; REQ-RDF-009 |
| BR8 | A decision that cannot be written to the decision record does not proceed: the record, the route state and the queue move commit together or not at all, and an incident is raised | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR9 | A restructure covers every account of the customer in the case, so the pack carries every linked account and no account is added or removed by the pack | CTL-26 |
| BR10 | One credit result per case: a second result is refused and writes no second decision record | Legacy RWB-E2-006 AC8 and X6; DF-CAS-007 |
| BR11 | The case links to ACE and to the treatment by business key only (`account_key`, `treatmentId`), with no foreign key and no copy of an ACE or treatment row in `rwb_case` | DP-01; D-RCV-35 U4; ADR-010 |
| BR12 | The route state, the queue and the owner are case facts of rwb-case, written only through its own interface; no other service writes them | Arch v5 slide 41; DF-CAS-007 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | OFFER_WITH_CUSTOMER |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | DECLINED_BY_CREDIT |
| DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | BACK_TO_ROUTE_DECISION |

The case status moves from "Waiting approval" to "In progress" when the approver accepts or rejects. The treatment state moves from SUBMITTED to APPROVED or REFUSED in rwb-treatment, not here. Both route-state moves are writes of `recovery_case.route_state` inside `rwb_case`, and each one names its rule (R-RES-11, R-RES-12, R-RES-14) in the decision record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Opens the pack and records the result (Treatment and offer, CRUA) |
| RW-CASEOWN, case owner | Opens the pack and records the result on cases in scope (Treatment and offer, CRU), and receives the case in the queue after a refusal |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack and the result (Treatment and offer, RA); they approve in NLEADS, not in this story |
| SY-CASEWF, the rwb-case service identity | Applies R-RES-11, R-RES-12 and R-RES-14, moves the route state, places the case in the case owner's queue and signals CaseWorkflow |
| Decision-record library identity | Writes the local decision record and publishes DecisionRecorded on `rwb.decision-record.v1` (Decision log, C) |
| rwb-access delegation contract | Supplies the required approval level for item 2.1.1 with the version in force; levels L1 to L6 are recorded from NLEADS |
| rwb-source-data contract | Supplies the account, collateral, valuation and NLEADS credit-decision facts; it is the only reader of the ACE views |

The service runs as the rwb-case login (DP-02). The login name is Not specified in the source documents (GAP-0729; ASM-1281).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case (rwb_case) | case header fields, including case_no (DF-CAS-002), product_group (DF-CAS-003) and route_state (DF-CAS-007) | Read; route_state and status written |
| DF-CAS-024 to DF-CAS-029 | case_account (rwb_case) | account_key, is_primary | Read |
| DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 | queue (rwb_case) | queue_code, capacity_cap and the round-robin cursor of the queue the case returns to | Read; the queue itself is written by the other rwb-case stories |
| DF-WRK-009 to DF-WRK-016, DF-WRK-039, DF-WRK-040 | assignment (rwb_case) | assignee, queue, assigned_at and the reason of the placement | Write |
| DF-WRK-017 to DF-WRK-026 | task (rwb_case) | task_code, status, owner_role and due_at of the task the result raises | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in rwb_case) | all fields, including rule version, final call, actions and freshness | Write |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case) | The NLEADS pack checklist rows and the route-state list, with the version in force | Read |
| DF-ACE-002, DF-ACC-009, DF-ACC-010 | ACE account facts through the rwb-source-data contract | account_code, principal_outstanding, interest_outstanding | Read |
| DF-ACE-020, DF-ACE-018, DF-ACE-036 | ACE account facts through the rwb-source-data contract | total_balance, days_past_due, data_as_of | Read |
| DF-ACE-091, DF-ACE-097, DF-ACE-191, DF-ACE-193 | ACE collateral and valuation facts through the rwb-source-data contract | collateral_no, collateral_type, appraised_value, appraisal_date | Read |
| DF-DOC-001, DF-DOC-004 | document through the rwb-document contract | id, document_type | Read |
| DF-TRT-001, DF-TRT-004, DF-TRT-007, DF-TRT-008, DF-TRT-009, DF-TRT-010 | treatment through the rwb-treatment contract | id, treatment_type, offer_amount, haircut_amount, installments, valid_until | Read |
| DF-TRT-003, DF-TRT-011, DF-TRT-023, DF-TRT-024, DF-TRT-025, DF-TRT-026 | treatment through the rwb-treatment contract | decision_log_id, approval_level, nleads_ref, credit_result, credit_result_reason, credit_result_at | Read here; written by rwb-treatment (S2 story) |
| Standard column | treatment through the rwb-treatment contract | state | Read here; written by rwb-treatment (S2 story) |

Field IDs are those in the Logical Data Model and Data Dictionary v8. No ACE row and no treatment row is copied into `rwb_case`: the case links to them by `account_key` and `treatmentId` with no foreign key (DP-01, BR11). The NLEADS credit-decision facts of `v_ace_credit_decision` are read through the rwb-source-data contract and are not stored in `rwb_case`; the reference that the decision record carries is the one ACE ingested.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/credit-approval` | The case-side credit approval pack: case number, product group, route state, the accounts with balances and business date, the collateral with its latest appraisal, the plan terms, the checklist rows with links or as missing, the required approval level and the input ages | Case record R and Treatment and offer R, scope applied | Not applicable |
| POST | `/cases/{caseId}/credit-result` | Records the NLEADS credit result on the case: the route state, the placement in the case owner's queue and the decision record, in one transaction | Treatment and offer U, scope applied | `Idempotency-Key` on the POST; one result per case, a repeat returns 409 and writes nothing |

Response fields follow the rwb-case contract conventions of RWB-P3-E1043-CON and the legacy CreditPack and CreditResult shapes: case `id`, `caseNo`, `productGroup`, `routeState`, `status`; account `accountKey`, `isPrimary`, `principal`, `interest`, `totalBalance`, `daysPastDue`, `dataAsOf`, `ageDays`; collateral `collateralNo`, `type`, `appraisedValue`, `appraisalDate`; terms `offerAmount`, `haircutAmount`, `installments`, `validUntil`; `requiredLevel`; documents `type`, `documentId` or `missing`; `messages`; and on the POST the recorded `routeState`, `decisionRecordRef` and `queueCode`. Errors: 401 no session (MSG-P4-001), 403 no Treatment and offer right (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 409 state (MSG-P3-005), already recorded (MSG-P2-010), level too low (MSG-P2-018) or version (MSG-GEN-004), 422 (MSG-GEN-001, MSG-GEN-002), 503 source interface unavailable (MSG-GEN-006) or decision record (MSG-P7-003). The JSON field names of the response are Not specified in the source documents (GAP-0729; ASM-1284).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{id}` | rwb-source-data (P1) | Balance, arrears and `data_as_of` of each linked account | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/collateral/{id}` | rwb-source-data (P1) | The collateral and its latest appraisal (Arch v5 slide 15, P1) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/freshness` | rwb-source-data (P1) | The ACE business date and batch state behind each input (REQ-RDF-009) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | The plan terms and the treatment state (ownership map: GET /treatments/{treatmentId}) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | rwb-document (P5) | The checklist documents and their links | One hop, 2 s (DP-11) |
| GET | `/api/recovery/access/v1/doa-limits` | rwb-access (P4) | The required approval level for decision D5, product group and amount under item 2.1.1, with the version in force | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, scope and right check before a read or a write | One hop, 2 s (DP-11) |
| The NLEADS credit-decision read of the rwb-source-data contract | rwb-source-data (P1) | The reference, result, approval level, result date and reason behind the recorded result | One hop, 2 s (DP-11) |

The NLEADS credit-decision operation name and field shape are Not specified in the source documents (GAP-0729; ASM-1283). The treatment contract returns the plan terms and the credit result fields of the legacy treatment record (`nleads_ref`, `credit_result`, `credit_result_reason`, `credit_result_at`); the JSON field names of that contract are Not specified in the source documents (GAP-0729; ASM-1284).

#### 12.3 Events published

None by this story's own topic. The decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction, with the decision code "D5", the final call, the NLEADS reference in the actions and the freshness of the data used (DP-03, H RWB-PLT-E1027-CON).

The case state-change event on `rwb.case.events.v1` (EV-05, CaseStateChanged) is not published by this slice: the outbox and topic library of DP-09 is not a build dependency of this story, and the legacy `CaseEvents.raise` in-process call is now an internal state change of the service that owns the case (DP-01, DP-11). The route state is served by the case reads and carried into the decision record.

#### 12.4 Events consumed

None. The NLEADS decision arrives as ACE data and is read through the rwb-source-data contract at the request of the officer; this story subscribes to no topic, and it consumes no case event.

#### 12.5 Workflows and activities

None new. This story starts no workflow and adds no activity. After the transaction commits, the service signals the running CaseWorkflow (parent, one per case, workflow ID = case ID, task queue `rwb-case`) with the new route state and the decision record reference, so the parent resumes on the credit outcome. CaseWorkflow is built and owned by RWB-P3-E1018-APP; this story only signals it.

#### 12.6 Schedules

None. The credit approval is officer-driven; no Schedule and no timer is created by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| recovery_case | rwb_case | P3 | route_state (DF-CAS-007), status and the case header the pack reads |
| case_account | rwb_case | P3 | The `account_key` and `is_primary` of the accounts the pack reads |
| queue | rwb_case | P3 | The queue code of the case owner the refusal returns the case to |
| assignment | rwb_case | P3 | The owner and the assignment written on the queue move |
| task | rwb_case | P3 | The task raised for the officer on a result and for the case owner after a refusal |
| decision_record | rwb_case | PLT library, created in rwb_case | The local decision record written in the same transaction as the state change (DP-03) |

rwb-case reads no table of another service and holds no foreign key across services (DP-01). The treatment, document and ACE facts are read through their owners' contracts, never through a table.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | `GET /accounts/{id}`, `GET /collateral/{id}`, `GET /freshness` and the NLEADS credit-decision read, with the fixtures of AC1, AC2 and AC3 |
| rwb-treatment WireMock | The S2 contract | `GET /treatments/{treatmentId}` for the plan terms of TRT-SYN-0610 and for the recorded result states of AC2 and AC3, and the RESTRUCTURE treatment of AC9 |
| rwb-document WireMock | The P5 contract | `GET /cases/{caseId}/documents` presenting the five checklist documents with links |
| rwb-access WireMock | The P4 contract | `GET /doa-limits` returning level "L6" for item 2.1.1, and `POST /authorise` granting and refusing the Treatment and offer right |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-14 credit approval panel route (AC1) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 7 named paths plus the NLEADS credit-decision read consumed | Case-scoped pack and result provided; source data, treatment, document, delegation and authorise consumed; one hop, 2 s timeout, GET retried once with jitter |
| Kafka | None published by this service, 1 published by the decision-record library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf (DP-03); `rwb.case.events.v1` is not used by this slice |
| Temporal | None new, 1 signal to an existing workflow | The POST signals the running CaseWorkflow after commit |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `creditapproval`, Java package `th.co.scb.ace.workbench.recovery.case.creditapproval`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

RWB-P3-E1043-CON is the same-service reference-data contract story, so it is carried in the build dependency row of the metadata as well as in this table (Template and Rules §R5.7 rule 3).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CreditApprovalController | Controller | `GET /cases/{caseId}/credit-approval` and `POST /cases/{caseId}/credit-result`; validation; problem responses |
| CreditApprovalQueryService | Service | Composes the case-side pack from `rwb_case` and the rwb-source-data, rwb-treatment, rwb-document and rwb-access contracts; checklist and input age |
| CreditResultService | Service | Validates the result, the case state, the level and the version; writes the decision record first, then the route state and the queue, and signals CaseWorkflow |
| CreditResultRepository | Repository | `recovery_case`, `case_account`, `queue`, `assignment` and `task` inside `rwb_case`; no other schema |
| DecisionRecordWriter | Library client | Calls the local decision-record library with decision "D5", the final call, the actions and the freshness; a failure fails the transaction (DP-03) |
| SourceDataClient | Client | Calls the rwb-source-data contract for accounts, collateral, freshness and the NLEADS credit-decision read (DP-05) |
| TreatmentClient | Client | Calls the rwb-treatment contract for the plan terms and the treatment state |
| DocumentClient | Client | Calls the rwb-document contract for the checklist documents; a failure marks the section, not the pack |
| DoaLimitClient | Client | Calls the rwb-access delegation contract for the required level of item 2.1.1 with the version in force |
| AccessCheckClient | Client | Calls the rwb-access authorise contract (cached) before a read or a write |
| ChecklistCatalog | Service | Reads the NLEADS pack checklist rows through the reference-data contract; no document type in code (DP-07) |
| CreditApprovalPanel, CreditResultForm | Screen component | Read-only pack with a copy action per field, missing items and input ages; reference, result, level, date and reason with field errors |

**Database and migrations**

- Writes `recovery_case`, `case_account`, `queue`, `assignment`, `task` and the library table `decision_record` in schema `rwb_case`, through the rwb-case login (DP-02). The login name is Not specified in the source documents (GAP-0729; ASM-1281).
- No new column and no new table: the route state, the queue, the owner and the task columns exist in the `rwb_case` baseline, and the four NLEADS columns are on the treatment, not here.
- One migration in the rwb-case sequence: `V2006_1__credit_approval_read.sql` adds the partial index on `recovery_case (route_state, queue_id)` for the route states AWAITING_CREDIT_APPROVAL and DECLINED_BY_CREDIT, which the case-side queue read uses (DP-15).
- One credit result per case is enforced by the route state and by the decision record check inside the service transaction; no unique table is added (BR10).

**Configuration and reference data**

- The NLEADS pack checklist rows in the rwb-case reference tables, with the version in force (business lead with Legal, DL19); the five items the legacy story assumes are CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF.
- The route-state list values AWAITING_CREDIT_APPROVAL, OFFER_WITH_CUSTOMER, DECLINED_BY_CREDIT and BACK_TO_ROUTE_DECISION through the reference-data contract; no state name in code (DP-07).
- The balance age limit of 1 business day (assumed in the legacy story under DL22), read as a reference row.
- The delegation rows for item 2.1.1 stay in rwb-access (DL18) and are read through its contract; rwb-case holds no copy.

**Build steps**

1. CreditApprovalQueryService against the `rwb_case` tables and the contract stubs, with a test per pack section; AC1.
2. SourceDataClient over the rwb-source-data contract for accounts, collateral, freshness and the NLEADS credit-decision read; AC1, AC2, AC3.
3. TreatmentClient and DocumentClient over their contracts, with the per-section degradation and the missing-row message; AC1.
4. ChecklistCatalog over the reference-data contract, with the missing-item path and the input age; AC1.
5. DoaLimitClient over the rwb-access delegation contract, with the version in force; AC1.
6. CreditResultService validation: case state, one result, level, reference, reason, date and version; AC9 and the refusal paths of the P2 story.
7. DecisionRecordWriter before the state change, with the rollback path and the incident; AC11.
8. The transactional write of the route state, the queue placement, the task and the record, then the signal to CaseWorkflow; AC2, AC3.
9. CreditApprovalPanel and CreditResultForm on SCR-14 against the gateway-bff stub, with the states of section 15.
10. Contract-fake run of every cross-service answer in isolation, so the story builds before the other services exist.

**Feature switch.** The legacy flag name `rwb.integration.nleads-pack` is kept as the legacy reference for the switch. In the target the switch is a feature flag of the platform flag library (Template and Rules §R3 default ruling); off hides the credit approval panel and refuses the POST with MSG-GEN-006 while nothing is written.

**Done when.** The tests in section 16 pass, every credit result names decision "D5" and the freshness of the data it used, the route state and the queue match the rule that fired, and the contract tests of RWB-P3-E1043-CON and RWB-PLT-E1027-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-009 | A checklist document is missing from the pack | The credit approval pack is missing {item}. Add it to the case before you submit in NLEADS. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-GEN-001 | Reference or refusal reason empty | Enter {field}. |
| MSG-GEN-002 | Result date after today | {field} must be between {min} and {max}. |
| MSG-P2-018 | NLEADS approval level below the required level | The NLEADS approval is at level {level}. This plan needs level {required} or higher. |
| MSG-P2-010 | Result already recorded | The NLEADS result for this treatment was recorded on {date}. |
| MSG-P3-005 | Case not awaiting credit approval | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | Case or treatment changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

MSG-P3-005 names the target route state and the current one only. MSG-P7-003 is raised after the transaction has rolled back, and the incident carries the case number, the decision code and the failure class, never a personal value.

### 15. Screens and states

SCR-14 Treatment record, credit approval panel. In state submitted the officer opens the pack, copies each field into NLEADS and opens each document link; a missing item and a stale input show their own message. The officer records the result in the result form; the panel moves to state approved, or shows the refusal reason while the case leaves the officer's view for the case owner's queue.

The screen is served by the gateway-bff composite route, which calls rwb-case for the case-side pack and, in parallel, rwb-treatment for the plan terms and rwb-source-data for the account and collateral facts, one hop each, and merges the answers into the screen model (DP-19). The screen fields, their field-level masking and the composite route specification are Not specified in the source documents (GAP-0729; ASM-1282), and the whole read-only treatment view is the S2 story of this legacy key.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-12 | Access | Component | RW-PHONECOL calls the result operation; refused with MSG-P4-002 |
| TC-E2-006-01 | AC1, BR6, BR9 | End to end | Synthetic case with 2 accounts, 1 collateral and 5 checklist documents |
| TC-E2-006-02 | AC2, BR2 | End to end | Result APPROVED at level L5 |
| TC-E2-006-03 | AC3, BR3 | End to end | Result REFUSED with a reason |
| TC-E2-006-04 | AC4, BR6 | End to end | No INCOME_PROOF document |
| TC-E2-006-05 | AC5, BR7 | End to end | Account load of 2026-12-12 |
| TC-E2-006-06 | AC6 | End to end | Empty reason; result date in the future |
| TC-E2-006-07 | AC7, BR5 | End to end | Level L6 for a plan that needs L5 |
| TC-E2-006-08 | AC8 | End to end | Result recorded twice |
| TC-E2-006-09 | AC9, BR1 | End to end | Case in PLAN_RUNNING |
| TC-E2-006-10 | AC10 | End to end | Two results with If-Match version 3 |
| TC-E2-006-11 | AC11, BR8 | End to end | Decision log store stopped during a result |
| TC-E2-006-13 | Principle 5 | NFR | Decision log write forced to fail; treatment and route state unchanged; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-006-01, -02, -03, -09, -11 and -13 are the ones this story runs against its own endpoints; the others are cited for the legacy key and are carried by the P2 and S2 stories.

### 17. Guardrails

- No business value in code: the checklist rows, the age limit, the route-state list and the delegation levels are data in the reference tables and in rwb-access; the story fixes only the behaviour.
- No personal data in logs, tests, workflow history or prompts. The pack reads `account_key`, `person_key` and amounts only; the refusal reason is free text and is written to the decision record, never to application logs.
- No read of another service's tables and no ACE view: account, collateral, valuation, freshness and NLEADS credit-decision facts come only through the rwb-source-data contract; plan terms only through the rwb-treatment contract; documents only through the rwb-document contract; the required level only through the rwb-access contract (DP-01, DP-05).
- The rwb_case schema holds no foreign key into another schema; the case links to ACE and to the treatment by business key only.
- The decision record is written in the same transaction as the route state and the queue move; a failure blocks the action and raises an incident (R-UNI-39).
- No call to NLEADS from the Workbench: the bank submits in NLEADS and ACE ingests the decision.
- The route state, the queue and the owner are written only by this service; no other service writes `recovery_case`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval is recorded on the case | Epic 2, 3.2; Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-09, TC-E2-006-11, TC-E2-006-13 |
| REQ-CHO-006 | The treatment holds its type, terms, approval and outcome | Epic 2, 3.2; Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05 |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used | Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-006-01, TC-E2-006-05, TC-E2-006-11 |

### 19. Out of scope

- The pack and result resources of the integration base and the NLEADS submission record: carried by the P2 story of this legacy key (ownership map: `GET /treatments/{treatmentId}/credit-pack`, `POST /treatments/{treatmentId}/credit-result`).
- The four NLEADS columns on the treatment, its APPROVED or REFUSED state and the treatment record screen: carried by the S2 story of this legacy key.
- The delegation table itself, its versions and the approval workflow in rwb-decision: the P4 and P7 stories; this story only reads the level through their contracts.
- The missing-document and stale-input refusal paths, the empty-reference and level refusals, the double-record refusal and the version conflict (AC4 to AC8, AC10): carried by the P2 and S2 stories.
- Generating a credit application document from a template (RWB-E2-026).
- Booking the plan in NLEADS and ALS and its confirmation (RWB-E2-007 and Epic 3, R-RES-21, R-RES-22).
- Approval inside the Workbench for decisions within the delegation (RWB-E2-013).
- Publishing the case state-change event on `rwb.case.events.v1` and the outbox and topic library of DP-09, which is not a dependency of this slice.
