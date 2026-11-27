# RWB-S2-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S2 rwb-treatment slice of legacy RWB-E2-006 is issued as its own story. The pack, the two integration-base operations, the NLEADS submission step and the input ages stay with rwb-integration (`RWB-P2-E2006-APP`); the route state AWAITING_CREDIT_APPROVAL, its move by R-RES-11, R-RES-12 and R-RES-14, the case owner's queue and the case-side record stay with rwb-case (`RWB-P3-E2006-APP`); the delegation of authority and the required level stay with rwb-access and its contract; the central ledger stays with rwb-decision. This story delivers the treatment-side consequence only: the four NLEADS columns on `treatment` in `rwb_treatment` (DF-TRT-023 to DF-TRT-026), the treatment state SUBMITTED to APPROVED or REFUSED, the recording write on the treatment resource on base `/api/recovery/treatment/v1`, the read that carries the recorded outcome, and the local decision record with decision D5 written in the same transaction as the row (DP-01, DP-03, DP-07, DP-11, DP-15, DP-19). The thirteen legacy test case identifiers are kept in the order the work package states. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E2006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP11, DP15, DP19 |
| Parallel lane | L-S2-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-CHO-008, REQ-CHO-006, REQ-RDF-009) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT) recording what NLEADS decided on a plan, and the case owner reading it back afterwards**, I want **the NLEADS reference, the result, the approved level, the result date and, for a refusal, the reason held on the treatment in `rwb_treatment`, with the treatment state moving from SUBMITTED to APPROVED or REFUSED and written only after the decision has been recorded by the local decision-record library**, so that **the plan carries its own credit outcome on the record that owns it, no result exists on a plan that cannot be explained from a record, and no other service writes this service's state**.

This is the `rwb-treatment` slice of legacy RWB-E2-006 and it owns no legacy criterion: `acs` is empty, and the nine criteria of section 7 are new and test only what this service delivers. Every legacy criterion AC1 to AC11, every legacy test case and every legacy value is owned by `RWB-P2-E2006-APP` for the pack, the result operation and the NLEADS submission, by `RWB-P3-E2006-APP` for the route state, the case-side record and the queue, or by the rwb-access delegation slice for the level; none of them is restated here.

What this story owns:

- the row: the four columns the legacy story put on the treatment — `nleads_ref` varchar(30), `credit_result` varchar(10), `credit_result_reason` varchar(1000) and `credit_result_at` timestamptz (DF-TRT-023 to DF-TRT-026 of TSD S2 T3.1) — in `rwb_treatment`, with the check that a reason is present when the result is REFUSED (DP-01, DP-15; TSD S2 T3.1);
- the state: SUBMITTED to APPROVED, or to REFUSED with its reason, on the treatment record, which is the state pair the legacy story fixes in its section 9;
- the write: the credit-result variant of `PATCH /treatments/{treatmentId}` on base `/api/recovery/treatment/v1`, guarded by `If-Match` on the treatment version and by the rule that one result exists per treatment (DP-11; TSD S2 T-A.2 API-S2-003);
- the read: `GET /treatments/{treatmentId}` answering the four recorded fields with the state and the version, which the pack and SCR-14 read (TSD S2 T-A.2 API-S2-002);
- the record: one local decision record with decision code D5, the final call, the level recorded, the NLEADS reference and the result date in its actions, written through the RWB-PLT-E1027-CON library in the same `rwb_treatment` transaction as the row, and announced on `rwb.decision-record.v1` (DP-03);
- the parameters of the write: LOV-CREDIT-RESULT with APPROVED and REFUSED and LOV-APPROVAL-LEVEL with L1 to L6, read through the reference-data contract of rwb-case at their version, and the length and format rules of the reference and the reason (DP-07; TSD S2 T3.2).

It does not own: the pack composition, the checklist, the input ages, the NLEADS reference and result capture, the integration-base resource and the two outcomes of the level check (`RWB-P2-E2006-APP`); the case route state `AWAITING_CREDIT_APPROVAL`, its move by R-RES-11, R-RES-12 and R-RES-14, the case owner's queue, the task and the case-side decision record (`RWB-P3-E2006-APP`); the delegation of authority of item 2.1.1, the required level and its version (rwb-access, P4, and its contract); the sealing of the record in the central ledger (rwb-decision, P7, and `RWB-P7-E2006-APP`); the account, collateral and valuation facts (rwb-source-data, P1, and its contract); the checklist documents (rwb-document, P5, and its contract).

### 2. Business rationale

A restructure outside the approved range goes to credit approval (R-RES-10), the bank decides it in NLEADS, and NLEADS has no interface to the Workbench (INT-26; legacy BR4). The plan is therefore carried in two places at once: the Workbench holds the terms, and the officer holds the decision in an inbox. When the decision is not written back, the case either waits or is moved by hand, and control CTL-04 for the approval level and CTL-06 for the decision record both fail.

The monolith wrote the four columns from the P2 Integration module into the one shared `recovery.treatment` table. Under D-RCV-60 that is neither possible nor allowed: `treatment` is one of the objects Architecture v5 gives `rwb-treatment`, in schema `rwb_treatment` with its own login, and no other service reads or writes it (DP-01; ADR-014). The pack and the submission step are the integration slice's, the route state and the queue are the case slice's, and the required level is rwb-access's. What only this service can do is make the treatment carry its own credit outcome: the reference and the result on the row, the state pair, and the record that proves the result was taken before anything moved (DP-03; R-UNI-39; Principle 5).

Three legacy mechanisms are replaced rather than ported. `TreatmentCommands.recordCreditResult` was an in-process call and becomes the REST write of 12.1, one hop with a 2 s budget and a fake (DP-11). The `DecisionLogWriter` of P7 becomes the local decision-record library, so the entry is committed with the row and never after it (DP-03). The result members and the level members become reference data of rwb-case read at the version in force, so no member is a constant in code (DP-07). The ACE facts stay in ACE: this story holds no `v_ace_*` grant and receives no account, collateral or valuation field (DP-05; ADR-010).

It serves REQ-CHO-006 on the treatment side — the type, the terms, the approval and the outcome on one record — and REQ-CHO-008 on the record side, and it applies REQ-RDF-009 by writing the result date beside the reference so the pack can show the age of what it carries.

### 3. Preconditions

- The `rwb_treatment` baseline is in place from `RWB-S2-E3001-APP`: the schema and its login, the `treatment` table with the columns of TSD S2 T3.1 and the standard record columns of T3.0, and the service's own Flyway sequence at the version that carries the library tables (DP-01, DP-02, DP-15).
- The local decision-record library RWB-PLT-E1027-CON is published with its fake: it writes the entry, seals the chain, answers the idempotency key and refuses an append when the store is down with MSG-P7-003 (DP-03).
- The reference-data contract of rwb-case is published with its fake, carrying LOV-CREDIT-RESULT with APPROVED and REFUSED and LOV-APPROVAL-LEVEL with L1 to L6, each with the version in force (RWB-PLT-E1043-CON, RWB-P3-E1043-CON; DP-07; TSD S2 T3.2).
- The treatment resource and its two operations are declared by this service's contract baselines (RWB-S2-E3001-CON for the resource, RWB-S2-E3002-CON for the `PATCH`), and this story adds the credit-result variant and its `If-Match` guard; the element names of that variant are Not specified in the source documents (GAP-2689; ASM-4437).
- A `treatment` row exists for synthetic treatment TRT-SYN-0610, of type RESTRUCTURE, in state SUBMITTED at version 3 and linked to case RW-2026-000610, carrying offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments and valid until 2026-12-29, with no credit result yet (legacy Background and section 11; ASM-4436).
- The case is in route state AWAITING_CREDIT_APPROVAL with an ACE plan status APPROVED. This service does not read the case to prove it; the caller slice holds that check and its message (GAP-2690; ASM-4440).
- The gateway-bff composite route is published with its fake, so SCR-14 can be read as the merged answer of the case read and the treatment read, one hop each (DP-19; RWB-PLT-N001-CON).
- No approval blocks this story: the BRDs and PRDs that would approve it are in review or pending, and the story is carried as Draft (realignment v1) under the run's no-approval rule (§R5.7 rule 2; ASM-4442).

### 4. Flow

1. The officer records the NLEADS outcome in the result form on SCR-14; the browser sends the credit-result variant of `PATCH /treatments/{treatmentId}` with the reference, the result, the level, the result date, the reason when the result is REFUSED, and `If-Match` with the version it read (DP-11, DP-19).
2. The API handler asks the guard library for the Treatment and offer right of right U and the case scope of the treatment, and refuses with MSG-P4-002 or MSG-P4-003 before any read of the row.
3. `CreditResultValidator` checks the request against the rules of section 14: the reference present and 1 to 30 letters, digits and dashes; the result a member of LOV-CREDIT-RESULT; the level a member of LOV-APPROVAL-LEVEL; the result date not after today; the reason 1 to 1,000 characters and required when the result is REFUSED. Each failure is 422 with the legacy message of that field, and nothing is read or written.
4. `CreditResultGuard` reads the treatment row from `rwb_treatment` and refuses when the row is not in state SUBMITTED, when a credit result is already held, or when the `If-Match` version differs from the row's version: 409 with MSG-P3-005, MSG-P2-010 or MSG-GEN-004 as section 14 maps them (legacy X6, X8).
5. `recordAndApply` opens one `rwb_treatment` transaction and writes the four columns (`nleads_ref`, `credit_result`, `credit_result_reason` — set to null on an approval — and `credit_result_at`), the state APPROVED or REFUSED, and the standard `updated_at` and `updated_by` columns.
6. In the same transaction it writes the local decision record through `DecisionRecordWriter.record`: decision code D5, final call `approved` or `rejected`, the level recorded, the NLEADS reference, the result date and the treatment ID in the actions, and the versions of the two lists in force. The outbox row of the record publication is written by the library, not by this service.
7. The transaction commits. A failure of the record write rolls the whole transaction back: no column changes, no state changes, no outbox row, and the caller reads 503 with MSG-P7-003 (legacy X9; BR8).
8. The handler answers 200 with the treatment element of the service contract — the four fields, the state and the new version — and the decision-record reference.
9. The caller slice reads that answer and raises CREDIT_APPROVED or CREDIT_DECLINED to rwb-case, which moves the route state by R-RES-11 or R-RES-12 and then by R-RES-14 on a refusal and puts the case in the case owner's queue. This service writes no case, queue, task or route row (GAP-2690; ASM-4440).
10. A repeat of the same write for a treatment that already holds a result finds the guard and answers 409 with MSG-P2-010: no second state change, no second record and no second outbox row.
11. The read of the treatment answers the four recorded fields with the state and the version to the pack and to SCR-14; the list members it shows come from the reference-data contract at their version and never from a constant (DP-07).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The reference is empty or longer than 30 characters, or a refusal carries no reason, or the reason exceeds 1,000 characters | Refused before any read or write, nothing changes | MSG-GEN-001 | AC3 |
| X2 | The result date is after today | Refused before any read or write, nothing changes | MSG-GEN-002 | AC3 |
| X3 | The result or the level is not a member of its list in force | Refused with 422 for the field; nothing changes and the list is not narrowed to a default | MSG-GEN-001 | AC3 |
| X4 | The treatment is not in state SUBMITTED | Refused with 409, nothing changes | MSG-P3-005 | AC4 |
| X5 | A result is already recorded on the treatment | Refused with 409 for the recorded date; no second record and no second outbox row | MSG-P2-010 | AC4 |
| X6 | The treatment changed between the read and the write | Refused with 409 on the version; nothing changes | MSG-GEN-004 | AC5 |
| X7 | The local decision record cannot be written | The transaction rolls back: no column, no state change and no outbox row; the caller retries and an incident is raised | MSG-P7-003 | AC6 |
| X8 | The identity has no Treatment and offer right, or the case is outside its scope | Refused with 403 or 404 before any read of the row | MSG-P4-002, MSG-P4-003 | AC9 |
| X9 | A statement or a test reaches a case, queue, account, rule or document table, or an ACE view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR10, AC9 |

X1 to X7 are the legacy refusal, result, record-failure and concurrency paths of RWB-E2-006 seen from the treatment row; X8 and X9 are the paths the split adds, where the right is checked at this service's door and the schema boundary is enforced by the login's grants. A refusal under X1, X2, X3, X4, X5, X6 or X8 writes nothing at all, because every check runs before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the reference-data fake, the record-writer fake and the composite-route fake; needs no live rwb-integration, rwb-case, rwb-access or rwb-decision |
| Negotiable | The component names, the payload element names, the feature-switch name and the index are this story's choice; the columns, the states, the list members, the messages and the values are fixed |
| Valuable | The plan carries its own credit outcome on the record that owns it, and no result exists without the decision record beside it |
| Estimable | One controller, one validator, one guard, one transactional write, one repository, one migration and one library adapter |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the nine criteria of section 7 is one automated test; the caller and the lists are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS — the treatment-side record

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL"
    Given treatment "TRT-SYN-0610" of type "RESTRUCTURE" is in state "SUBMITTED" at version 3, with offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments and valid until 2026-12-29
    Given the plan needs approval at level "L6" or higher under item 2.1.1
    Given the reference-data contract carries LOV-CREDIT-RESULT with "APPROVED" and "REFUSED" and LOV-APPROVAL-LEVEL with "L1" to "L6"

  Scenario: AC1 The NLEADS result is written on the treatment and the state moves to APPROVED (new, D-RCV-60)
    Given the rwb-integration contract mock returns the recording write for treatment "TRT-SYN-0610" with reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    And the request carries If-Match version 3
    When the credit-result write is served on base "/api/recovery/treatment/v1"
    Then treatment "TRT-SYN-0610" holds nleads_ref "NL-SYN-000610", credit_result "APPROVED", approval_level "L5" and credit_result_at 2026-12-17, and its state is "APPROVED" at version 4
    Then one local decision record names decision "D5", final call "approved", the reference "NL-SYN-000610", the level "L5" and the result date, and it is written in the same rwb_treatment transaction as the row
    Then the answer carries the four fields, the state "APPROVED" and the decision-record reference, and no case, queue, task or route row is written by this service

  Scenario: AC2 A refusal is recorded with its reason and the state moves to REFUSED (new, D-RCV-60)
    Given the rwb-integration contract mock returns the recording write for treatment "TRT-SYN-0610" with reference "NL-SYN-000611", result "REFUSED", approval level "L5", result date 2026-12-17 and reason "Income does not cover 84 installments"
    When the credit-result write is served with If-Match version 3
    Then treatment "TRT-SYN-0610" holds credit_result "REFUSED" and credit_result_reason "Income does not cover 84 installments", and its state is "REFUSED" at version 4
    Then one local decision record names decision "D5" with final call "rejected" and the reason in its actions, written in the same transaction
    Then this service writes no route or queue row and raises no case event

  Scenario: AC3 The write is refused when a value is missing, malformed or out of range (new, D-RCV-60)
    Given three writes for "TRT-SYN-0610": result "REFUSED" with reference "NL-SYN-000612" and an empty reason; result "APPROVED" with result date 2026-12-31 while today is 2026-12-17; and result "APPROVED" with approval level "L7"
    When each write is served with If-Match version 3
    Then each answers 422, with MSG-GEN-001 for field "reason", MSG-GEN-002 for field "resultDate" and MSG-GEN-001 for field "approvalLevel"
    Then the treatment is unchanged at version 3 and no decision record and no outbox row exists for any of the three

  Scenario: AC4 A treatment that already carries a result, or is not submitted, is refused (new, D-RCV-60)
    Given treatment "TRT-SYN-0610" holds result "APPROVED" with reference "NL-SYN-000610" recorded at 2026-12-17 in state "APPROVED"
    And treatment "TRT-SYN-0620" is in state "DRAFT" with no result
    When a result is recorded for each of them
    Then "TRT-SYN-0610" answers 409 with MSG-P2-010 for 2026-12-17 and "TRT-SYN-0620" answers 409 with MSG-P3-005
    Then neither row changes and no second record and no outbox row exists

  Scenario: AC5 Two officers record at once (new, D-RCV-60)
    Given two callers read treatment "TRT-SYN-0610" at version 3
    When both send the credit-result write with If-Match version 3
    Then one result is saved and the row moves to version 4
    Then the other answers 409 with MSG-GEN-004 and nothing of it is written

  Scenario: AC6 A failed record write leaves the treatment unchanged (new, D-RCV-60)
    Given the decision-record writer mock reports the store unavailable with MSG-P7-003
    When the write of AC1 is served with If-Match version 3
    Then the answer is 503 with MSG-P7-003
    Then no credit field and no state change is written, the row stays at version 3, no outbox row exists and an incident is raised

  Scenario: AC7 The read carries the recorded outcome to the pack and to SCR-14 (new, D-RCV-60)
    Given treatment "TRT-SYN-0610" holds the result of AC1 and treatment "TRT-SYN-0620" holds none
    When GET "/treatments/{treatmentId}" is served for each on base "/api/recovery/treatment/v1"
    Then the first answer carries nleads_ref "NL-SYN-000610", credit_result "APPROVED", approval_level "L5", credit_result_at 2026-12-17 and the state "APPROVED", and the second carries empty members with the state it holds
    Then the members offered for the result and the level are the LOV-CREDIT-RESULT and LOV-APPROVAL-LEVEL members read through the reference-data contract at their version, with no member in code

  Scenario: AC8 The recorded level is stored as given and the required level is not judged here (new, D-RCV-60)
    Given the rwb-integration contract mock records result "APPROVED" with approval level "L5" for a plan whose required level is "L6"
    When the credit-result write is served with If-Match version 3
    Then the write is accepted and approval_level holds "L5" character for character
    Then the comparison with the required level and its refusal MSG-P2-018 are answered by the caller's slice, and this service computes no required level

  Scenario: AC9 No personal data, no ACE view and no cross-schema read (new, D-RCV-60)
    Given a write and a read carry the treatment ID, the case ID, the reference, the result, the level, the result date and the reason
    When the treatment row, the local decision record and the log lines of the two operations are written
    Then they carry identifiers, codes, dates and the recorded reason only, and no name, address, telephone number, national identity number, account number or account holder name
    Then no statement of this service reaches a case, queue, account, rule or document table and no `v_ace_*` view, and a role without the Treatment and offer right reads 403 with MSG-P4-002
```

The nine criteria are new under D-RCV-60 and test only the S2 deliverable: the approved row with its state, the refused row with its reason, the validation refusals, the once-only and state guard, the version conflict, the failed record, the read the pack and SCR-14 consume, the level stored as given, and the boundary with no personal data. No criterion claims a legacy AC: AC1 to AC11 of RWB-E2-006 belong to `RWB-P2-E2006-APP` and `RWB-P3-E2006-APP`, where the pack, the checklist, the input ages, the NLEADS submission, the route state, the queue and the level comparison are written with their origin tags. Two readings are stated rather than hidden in the code: the values SUBMITTED, APPROVED and REFUSED are carried on the standard `state` column, which no list fixes, and the check that a REFUSED row holds a reason is added by this story's own Flyway version (GAP-2689; ASM-4436).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A restructure outside the approved range or with a deviation goes to credit approval; the case route state is the case's, and this service only records the outcome on the treatment | legacy BR1; R-RES-10 |
| BR2 | An approval releases the offer to the customer with a 14-day validity; this service records the approval and the caller moves the route | legacy BR2; R-RES-11 |
| BR3 | A refusal records the reason, and the case then returns to the route decision for the case owner; the reason is stored here and the move is the caller's | legacy BR3; R-RES-12, R-RES-14 |
| BR4 | NLEADS has no interface; the officer submits there and records the reference and the result here as given, and this service calls NLEADS never | legacy BR4; INT-26; DL12 |
| BR5 | The level the delegation of authority sets for the decision, the product and the amount is compared with the recorded level by the caller; this service stores the level as given and judges no level | legacy BR5; doa.txt item 2.1.1; CTL-04; DL18 |
| BR6 | The pack documents are those of the NLEADS pack checklist, which the caller assembles; no document field is held on the treatment | legacy BR6; DL19 |
| BR7 | An input past its age limit is shown with its age; the pack computes the age from the business date and this service stores the result date beside the reference | legacy BR7; MSG-P7-006; REQ-RDF-009 |
| BR8 | A decision that cannot be recorded does not proceed: the row, the state and the decision record are one transaction | legacy BR8; Principle 5; R-UNI-39; CTL-06 |
| BR9 | A restructure covers every account of the customer in the case; the treatment holds one case reference and no account key | legacy BR9; CTL-26 |
| BR10 | The treatment is this service's own record: this story writes no case, queue, task, account, rule or document table, holds no cross-schema foreign key and reads no ACE view | DP-01, DP-05; ownership of `treatment` only |

**Where each rule lives in the target.** BR1, BR2, BR3, BR4, BR5, BR6 and BR7 are statements of the boundary: each names the fact this story stores and the fact the caller owns, so neither service repeats the other's check. BR8 is the single transaction of step 5 and 6 and the MSG-P7-003 rollback. BR9 is why the row carries `case_id` and never an account. BR10 is the schema boundary of sections 11 and 17.

### 9. State transitions

None of the route states of the legacy table is this story's: AWAITING_CREDIT_APPROVAL to OFFER_WITH_CUSTOMER by R-RES-11, to DECLINED_BY_CREDIT by R-RES-12 and then to BACK_TO_ROUTE_DECISION by R-RES-14 are the case states of rwb-case (`RWB-P3-E2006-APP`). The rows below are the states of this service's own `treatment` row.

| From (treatment state) | Event | Condition | To |
|---|---|---|---|
| SUBMITTED | CREDIT_RESULT_RECORDED | result APPROVED and the record committed | APPROVED, with `nleads_ref`, `credit_result`, `approval_level` and `credit_result_at` |
| SUBMITTED | CREDIT_RESULT_RECORDED | result REFUSED with its reason and the record committed | REFUSED, with the four fields and the reason |
| SUBMITTED | CREDIT_RESULT_REFUSED | any validation failure, a version conflict or a failed record | SUBMITTED, unchanged |
| APPROVED or REFUSED | CREDIT_RESULT_RECORDED | a repeat of the write for the same treatment | Unchanged, 409 with MSG-P2-010 |

The state names are carried on the standard `state` column of TSD S2 T3.0, which no list fixes; LOV-TRT-OUTCOME of TSD S2 T3.2 is the `outcome` column's list and is not used for this state (GAP-2689; ASM-4436). The case status moves from "Waiting approval" to "In progress" in the case's own record, and the treatment state pair SUBMITTED to APPROVED or REFUSED is the one the legacy section 9 states.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-treatment service identity (the `rwb_treatment` login) | Serves the two operations, writes the treatment row, the state and the local decision record, and applies the guards of section 5 |
| rwb-integration (P2) | Owns the pack, the NLEADS submission step, the integration-base resource and the level check; calls the two operations of this story and never writes `rwb_treatment` |
| rwb-case (P3) | Owns the case route state, its move by R-RES-11, R-RES-12 and R-RES-14, the queue, the task and the case-side record |
| rwb-access (P4) | Owns the roles, the capability area "Treatment and offer", the rights and the scope data, and the delegation of authority of item 2.1.1 |
| rwb-decision (P7) | Owns the central ledger that seals the record this service writes; not called synchronously |
| RW-RESTRUCT, restructuring officer | Records the NLEADS result on the cases in scope (Treatment and offer CRUA) |
| RW-CASEOWN, case owner | Records the result on cases in scope (Treatment and offer CRU) and receives the case back after a refusal |
| RW-CREDCOMM, RW-PRODHEAD | Read the recorded result (Treatment and offer RA); they approve in NLEADS, not in this story |
| RW-AUDIT, internal audit | Reads the record and the version of the two lists it was taken under (R) |

No credential and no personal name appears in the request, the row, the record, the workflow input or the logs. Where a person must be identified the row carries the user identifier, never a name.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read, as the treatment the write names |
| DF-TRT-003 | treatment (S2, `rwb_treatment`) | decision_log_id | Write, the ID of the local decision record written with this change |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read, to refuse a treatment that is not a restructure or a settlement of this kind |
| DF-TRT-007, DF-TRT-008, DF-TRT-009, DF-TRT-010 | treatment (S2, `rwb_treatment`) | offer_amount, haircut_amount, installments, valid_until | Read only, returned with the outcome so the caller and SCR-14 need no second read |
| DF-TRT-011 | treatment (S2, `rwb_treatment`) | approval_level | Write, the level recorded from NLEADS as given |
| DF-TRT-023 | treatment (S2, `rwb_treatment`) | nleads_ref | Write, 1 to 30 letters, digits and dashes (DL12) |
| DF-TRT-024 | treatment (S2, `rwb_treatment`) | credit_result | Write, APPROVED or REFUSED (LOV-CREDIT-RESULT) |
| DF-TRT-025 | treatment (S2, `rwb_treatment`) | credit_result_reason | Write, 1 to 1,000 characters, required when REFUSED |
| DF-TRT-026 | treatment (S2, `rwb_treatment`) | credit_result_at | Write, the result date the officer records |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, created_at, created_by, updated_at, updated_by | Write `state` as section 9 defines it and `version` on every write; the rest as TSD S2 T3.0 defines them |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, `rwb_treatment`) | all fields, through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-CAS-002, DF-CAS-007, DF-ACE-* | recovery_case (P3), `v_ace_account`, `v_ace_collateral`, `v_ace_valuation` (P1) | case number, route state, balances, collateral, appraisal | Not read and no grant: the pack is the caller's and the case check is the case owner's (DP-05) |
| DF-DOC-001, DF-DOC-004 | document (P5, `rwb_document`) | id, document_type | Not read: the checklist is the pack's |
| DF-REF-002, DF-REF-003 | reference_row (P3, `rwb_case`) | list code, list value | Read through the reference-data contract only, never as a table (DP-07) |

`treatment` is the only table this story writes, and it writes the five credit columns (`nleads_ref`, `credit_result`, `credit_result_reason`, `credit_result_at` and `approval_level`) plus the standard `state` and `version`. Field identifiers are those of TSD S2 T3.1 and the Logical Data Model and Data Dictionary.

**No new table.** This story's Flyway version adds the credit rule on `treatment` in `rwb_treatment`: the check that `credit_result_reason` is not null when `credit_result` is REFUSED and is null otherwise, the check constraint of the state values of section 9, the check that `credit_result_at` is set only with `credit_result`, and the length checks the legacy story states for the reference and the reason (GAP-2689; ASM-4436). The table itself arrives with `RWB-S2-E3001-APP`, and no applied migration is edited (DP-15).

**No personal data.** The request, the row, the record and the logs carry the treatment ID, the case ID, the reference, the result, the level, the result date and the reason the officer recorded. No name, address, telephone number, national identity number, account number or account holder name is written, logged or put on a message.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1`; the resource and its read are declared by RWB-S2-E3001-CON and the `PATCH` by RWB-S2-E3002-CON, and this story adds the credit-result variant and its guard. The element names of that variant are Not specified in the source documents (GAP-2689; ASM-4437).

| Method | Path | Request | Response | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` | None | 200 with the treatment element: `nleadsRef`, `creditResult`, `approvalLevel`, `creditResultAt`, the state, the version and the plan terms of DF-TRT-007 to DF-TRT-010 | Treatment and offer R, scope applied, through the guard library | Not applicable |
| PATCH | `/treatments/{treatmentId}` | The credit-result variant: `nleadsRef` (1 to 30 letters, digits and dashes), `result` (APPROVED or REFUSED), `approvalLevel` (L1 to L6), `resultDate`, `reason` (1 to 1,000 characters, required when REFUSED), with the header `If-Match` | 200 with the treatment element of the row after the write, the decision-record reference and the new version | Treatment and offer U, scope applied, through the guard library | One result per treatment: `If-Match` required, a repeat on a recorded treatment returns 409 with MSG-P2-010 and writes nothing |

Errors: 401 no session (MSG-P4-001); 403 no Treatment and offer right (MSG-P4-002); 404 the treatment does not exist or lies outside the scope (MSG-P4-003); 409 the state (MSG-P3-005), a result already recorded (MSG-P2-010) or the version (MSG-GEN-004); 422 the field refusals of section 14 (MSG-GEN-001, MSG-GEN-002); 503 the decision record (MSG-P7-003). Each error is an RFC 9457 problem body with `messageId`, `detail` and `instance`.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use in this story |
|---|---|---|---|
| The reference-data read of LOV-CREDIT-RESULT and LOV-APPROVAL-LEVEL; name Not specified (GAP-2689; ASM-4437) | `/api/recovery/case/v1` | P3 rwb-case (RWB-P3-E1043-CON) | The list members the write accepts and the read offers, at their version; no member in code (DP-07) |

One hop with a 2 s timeout behind a breaker; the answer is cached for the life of the version in force. The authorise check is made through the guard library of the platform (RWB-PLT-E1037-CON) and is not a call of its own here. The H row of DP-07 and the C row it adds stand in no build row of this story's plan (GAP-2690; ASM-4438).

#### 12.3 Events published

| Event | Topic | Trigger | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` (DP-03) | Every recorded result, written by the record library in the same transaction as the row | `caseId` | The case ID, the treatment ID, the entity, the decision code D5, the final call, the level, the reference, the result date and the list versions; no personal data |

This story adds no event type on `rwb.treatment.events.v1`: `TreatmentApproved` (EV-10) is published by the treatment and offer stories on their own transitions, and this story writes only the record publication of the library. No outbox row is written by this service's own code; the library writes it in the same transaction.

#### 12.4 Events consumed

None. The NLEADS outcome arrives in the officer's write and never as an event; this story subscribes to no topic, and the reference-data answer it needs is a contract call.

#### 12.5 Workflows and activities

None started by this story. The write is a synchronous officer operation, one hop from the composite route, and this story adds no workflow, no activity and no signal. The child stage `TreatmentWorkflow` on queue `rwb-treatment` in namespace `rwb-recovery` is the plan and timer stage of `RWB-S2-E3004-APP` to `RWB-S2-E3007-APP` and is not entered here; the route state move runs in the case owner's `CaseWorkflow` (GAP-2690; ASM-4440).

#### 12.6 Schedules

None. The credit approval is officer-driven and no Schedule, no timer and no Quartz job is created by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Writes `nleads_ref`, `credit_result`, `credit_result_reason`, `credit_result_at`, `approval_level`, `state` and `version`; the table arrives with `RWB-S2-E3001-APP` and this story's Flyway version adds the credit rule (DP-01, DP-15) |
| `decision_record` | `rwb_treatment` | PLT library, applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched (DP-03) |

Not owned and never read as a table: `recovery_case`, `queue`, `task` (P3, `rwb_case`), `reference_row` (P3, reached through the contract only), `decision_log_entry` (P7, `rwb_decision`), `document` (P5, `rwb_document`), and every `v_ace_*` view (P1). No foreign key leaves the schema and no cross-schema join exists.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-integration caller fake | The credit-result write for `TRT-SYN-0610` with `NL-SYN-000610` approved at `L5`, the refusal `NL-SYN-000611` with its reason, the version-3 pair of AC5 and the repeated write of AC4 | AC1, AC2, AC4, AC5, AC8 |
| RWB-PLT-E1027-CON writer fake | An accepted record with chain sequence and entry hash; an unavailable store raising MSG-P7-003 | AC1, AC6 |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | LOV-CREDIT-RESULT with two members and LOV-APPROVAL-LEVEL with six, at their version, and a delayed answer beyond 2 s | AC3, AC7, X3 |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The merged SCR-14 answer for case `RW-2026-000610` with the case read of rwb-case and the treatment read of this service, one hop each | AC7 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of the contract story that owns it.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The treatment read and the credit-result write on `/api/recovery/treatment/v1`; the reference-data read of rwb-case, one hop and 2 s |
| Kafka | 1 published by the library | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` (DP-03); this service publishes no type of its own |
| Temporal | None | No workflow, no activity, no signal, no Schedule |
| File | None | No file is read, built or delivered |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `creditapproval`, Java package `th.co.scb.ace.workbench.recovery.treatment.creditapproval`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, queue `rwb-treatment`.

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

DP-01 is the schema rule of sections 11 and 17 and the reason a second service's write is impossible rather than discouraged. DP-03 is the transaction the story is built on: the entry is committed with the row, so a result cannot exist without its record (BR8). DP-05 is a prohibition here: no account, collateral, valuation or case fact is read, so the module holds no `v_ace_*` grant and the login has none. DP-07 is the two lists of 12.2, read at their version so no member is a constant. DP-11 is what the legacy in-process `TreatmentCommands.recordCreditResult` and `TreatmentQuery.get` become: a REST pair, one hop, a 2 s budget, a fake, no call chain. DP-15 is the new Flyway version of this service's own sequence. DP-19 is SCR-14 through the composite route, read only on this story's side.

**Dependencies the table adds and the plan does not hold.** The table adds the H rows `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON` and `RWB-PLT-N001-CON` and the C row `RWB-P3-E1043-CON`, while the plan's lists hold `Depends on (build)` None, `Contract dependencies` None and no integration or external dependency. The metadata keeps the plan's lists because every added row is a platform library the service template already carries, or a contract the story builds against with a fake from Day 1; the difference is recorded as GAP-2690 with ASM-4438.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CreditResultController` | REST controller | The credit-result write and the treatment read of 12.1; the problem mapping and the `If-Match` header |
| `CreditResultValidator` | Service | The length, format, list-membership and date rules of section 14, run before any read of the row |
| `CreditResultGuard` | Service | The state, once-only and version guards of section 5 |
| `CreditResultService` | Service | Builds the command, opens the transaction, calls the repository and the record adapter, and assembles the answer |
| `recordAndApply` | Transactional method | One transaction: the six columns and the state, the decision record, the version bump |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with D5, the final call, the level, the reference, the result date and the list versions (DP-03) |
| `TreatmentRepository` | Repository | Reads and writes `treatment` in `rwb_treatment` only, with the version predicate on every write |
| `ReferenceDataClient` | Contract client | The two lists of 12.2 at their version, cached, with the breaker and the 2 s budget (DP-07) |
| `Migrations` | Migration | The credit rule on `treatment` on this service's Flyway sequence (DP-15) |

**Database.** No table is added: `treatment` arrives with `RWB-S2-E3001-APP`. This story's Flyway version adds the credit rule — the four columns typed as TSD S2 T3.1 types them, the reason rule, the state check of section 9, the rule that `credit_result_at` is set only with `credit_result`, and the length checks — and never edits an applied migration (DP-15).

**Configuration and reference data.** The two list codes are read through the reference-data contract at their version; no member is written in code (DP-07; BR10). The feature switch `rwb.treatment.credit-result` is a flag of the platform library: off means the write is refused with 404 and the read answers the four fields as they stand.

**Build steps**

1. The Flyway version with the credit rule on `treatment`, and the migration test against the TSD types.
2. `ReferenceDataClient` and the two lists, with the delayed answer and the breaker path.
3. `CreditResultValidator` with each field refusal of section 14; test AC3.
4. `CreditResultGuard` with the state, once-only and version refusals; test AC4, AC5.
5. `recordAndApply` in one transaction, with the rollback path; test AC1, AC2, AC6.
6. `CreditResultController` with the access and scope refusals; test AC9.
7. The treatment read with the four fields and the version; test AC7.
8. The level stored as given with the caller's comparison left out; test AC8.
9. The boundary and no-PII tests: no statement outside `rwb_treatment`, no `v_ace_*` read, no personal field in the request, the record or the logs.

**Done when.** The tests of section 16 pass, a synthetic approved plan and a synthetic refused plan each hold their four fields, their state and exactly one decision record with D5, a forced record failure leaves the row and the state untouched, a second write is refused with MSG-P2-010, and SCR-14 shows the recorded outcome through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | The reference is empty or too long, the reason is empty on a refusal or too long, or a value is not a member of its list (X1, X3) | Enter {field}. |
| MSG-GEN-002 | The result date is after today (X2) | {field} must be between {min} and {max}. |
| MSG-P3-005 | The treatment is not in state SUBMITTED (X4) | This case cannot move to {state} from {current}. |
| MSG-P2-010 | A result is already recorded on the treatment (X5) | The NLEADS result for this treatment was recorded on {date}. |
| MSG-GEN-004 | The treatment changed between the read and the write (X6) | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The local decision record cannot be written (X7) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The identity has no Treatment and offer right (X8) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The treatment does not exist or lies outside the scope (X8) | This case is not in your scope. |

The eight texts are the legacy texts of RWB-E2-006 section 14, carried unchanged. MSG-P3-005 is the legacy state-refusal text and is used here on the treatment state, with {state} the state the write would set and {current} the state held; the case-side use of the same text remains `RWB-P3-E2006-APP`'s. For MSG-GEN-001 in X3, {field} names `approvalLevel` or `result` and the refusal states that the value is not in the list in force, never a default member. The status mapping is 403 for MSG-P4-002, 404 for MSG-P4-003, 409 for MSG-P3-005, MSG-P2-010 and MSG-GEN-004, 422 for MSG-GEN-001 and MSG-GEN-002, and 503 for MSG-P7-003. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-14 Treatment record | Submitted, awaiting the credit result | The plan terms and the state, read only, with the result form available to a right U holder |
| SCR-14 Treatment record | Form error | The field-level message of section 14 beside the field, nothing written |
| SCR-14 Treatment record | Approved | The reference, the result, the level and the result date, read only |
| SCR-14 Treatment record | Refused | The reference, the result, the level, the result date and the reason, read only |
| SCR-14 Treatment record | Refused or out of scope | A role without Treatment and offer R reads MSG-P4-002; a case outside the scope reads MSG-P4-003 |

SCR-14 is served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each (DP-19). The field list, the route specification and the layout are the platform edge contract's; this story fixes only the service side of the answer. The pack panel, the copy action per field and the input ages are `RWB-P2-E2006-APP`'s and are not shown here (GAP-2690; ASM-4441).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-12 | Access | Component | RW-PHONECOL calls POST /treatments/{treatmentId}/credit-result; refused with MSG-P4-002 |
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
| TC-E2-006-13 | Principle 5 | Component | Decision log write forced to fail; treatment and route state unchanged; MSG-P7-003 |
| TC-S2-E2006-APP-01 | AC1, BR8 | Component | The write for "TRT-SYN-0610" with "NL-SYN-000610" at "L5"; four fields, state APPROVED at version 4, one record naming D5 |
| TC-S2-E2006-APP-02 | AC2, BR3 | Component | The refusal "NL-SYN-000611" with "Income does not cover 84 installments"; state REFUSED, reason stored, one record |
| TC-S2-E2006-APP-03 | AC3 | Component | Empty reason, result date 2026-12-31 and level "L7"; three 422 answers, row unchanged at version 3 |
| TC-S2-E2006-APP-04 | AC4, BR8 | Component | A recorded treatment and a treatment in state DRAFT; 409 with MSG-P2-010 and MSG-P3-005, no second record |
| TC-S2-E2006-APP-05 | AC5 | Component | Two writes with If-Match version 3; one saved at version 4, the other 409 with MSG-GEN-004 |
| TC-S2-E2006-APP-06 | AC6, BR8 | Component | The record writer forced to fail; no field, no state change, no outbox row, 503 with MSG-P7-003 |
| TC-S2-E2006-APP-07 | AC7, BR7 | Contract | The treatment read with a recorded result and with none; the two lists from the reference-data fake at their version |
| TC-S2-E2006-APP-08 | AC8 | Component | Level "L5" recorded for a plan whose required level is "L6"; stored as given, no comparison here |
| TC-S2-E2006-APP-09 | AC9, BR10 | Contract | A property check over a synthetic party name and an account number, and a grant check over every statement; no personal field, no `v_ace_*` read |

The thirteen identifiers TC-E2-006-12 and TC-E2-006-01 to TC-E2-006-13 are legacy-carried, kept in the order the work package states, with their Covers and Data character for character. Their Covers name the eleven legacy criteria, which `RWB-P2-E2006-APP` and `RWB-P3-E2006-APP` own and answer, so this slice proves the treatment-side half of each row at the level the row's kind allows: the legacy level "System" maps to "End to end", and "Access", "Resilience" and "Principle 5" to "Component", as the sibling stories of this run do. The nine cases TC-S2-E2006-APP-01 to TC-S2-E2006-APP-09 are new for the criteria of this story that no legacy row exercises. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies of these rows belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the result members, the level members and the length limits are rows of the contracts and of this story's Flyway checks read at their version; a build check fails on any of them in the Java source or the module configuration (BR10).
- No personal data in logs, tests, events or records: the request, the row, the record and the span attributes carry the treatment ID, the case ID, the reference, the result, the level and dates only, and the reason the officer recorded is held on the row and never in the application log (legacy guardrail; AC9).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view and holds no grant on one, and no account, collateral or valuation field reaches this module (DP-05; ADR-010).
- No read of another service's tables and no cross-schema join: `recovery_case`, `queue`, `task` and `reference_row` (P3), `decision_log_entry` (P7) and `document` (P5) are reached only through their owners, and the boundary test fails the build on any statement outside `rwb_treatment`.
- The decision record is written in the same transaction as the state change, and a failed write rolls the whole transaction back with MSG-P7-003; no result exists without its record (DP-03; BR8; R-UNI-39).
- One hop and a 2 s budget on every contract call, with a breaker and no call chain; the write is never retried by this service, the caller retries under the same key.
- One result per treatment: the once-only guard and the `If-Match` version refuse a second write, and no second record and no second outbox row exists (X5, X6).
- The case route state, its move by R-RES-11, R-RES-12 and R-RES-14, the queue, the task and the case-side record are not written here (DP-01; ASM-4440).
- No Quartz job, no Schedule and no timer row: the write is synchronous.
- An applied migration is never edited: the credit rule is a new version on this service's own Flyway sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Plan submitted for credit approval recorded on the case, which this story answers on the treatment side by holding the reference, the result, the level, the result date and the reason on the row with its record | Business Requirements Program 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-06 to TC-E2-006-11, TC-E2-006-13, TC-S2-E2006-APP-01 to TC-S2-E2006-APP-06 |
| REQ-CHO-006 | Treatment holds type, terms, approval and outcome, which this story completes with the approval level and the credit outcome on the record that carries the terms | Business Requirements Program 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05, TC-S2-E2006-APP-07, TC-S2-E2006-APP-08 |
| REQ-RDF-009 | An input past its age limit is shown with its age, which this story applies by writing the result date beside the reference and offering both on the read | Business Requirements Program 5.4 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-UNI-41 | TC-E2-006-05, TC-S2-E2006-APP-07 |

The three requirement identifiers, the BRD sections, FEAT-CHO-07 and L3 process 7.3 are the legacy traceability rows' and are kept unchanged; the pack, the checklist, the input ages and the NLEADS submission measured by the legacy story stay with `RWB-P2-E2006-APP`, and no criterion of this story claims them.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E2-006 | The treatment-side deliverable: the four columns, the SUBMITTED to APPROVED or REFUSED state, the recording write, the read, the local decision record with D5 and the list reads |
| RWB-P2-E2006-APP | The pack, the checklist, the input ages, the NLEADS submission, the integration-base resource, the level comparison and the messages of the pack |
| RWB-P3-E2006-APP | The route state AWAITING_CREDIT_APPROVAL, its move by R-RES-11, R-RES-12 and R-RES-14, the queue, the task and the case-side record |
| rwb-access (P4) and its contract | The roles, the rights, the scope, the delegation of authority of item 2.1.1 and the required level |
| RWB-P7-E2006-APP and rwb-decision (P7) | The central ledger that seals the record, the rule registry and the reference registry |
| RWB-S2-E3001-APP, RWB-S2-E3004-APP to RWB-S2-E3011-APP | The treatment record, the plan offer, the timers and the payment matching this story does not build |
| RWB-S2-E3001-CON, RWB-S2-E3002-CON | The treatment resource, its read and the `PATCH` this story's write variant sits on |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON | The library and contract rows the pattern table adds, which stand in no build row of this story (GAP-2690; ASM-4438) |
| DP-01, DP-03, DP-07, DP-15 | The owner's schema, the local record in the same transaction, the lists at their version and the per-service Flyway sequence |
| DP-05, DP-11, DP-19 | No ACE view is read, one hop with a 2 s timeout on the contract pair, and SCR-14 behind the composite route |
| ADR-013, ADR-014, ADR-015, ADR-020, ADR-021, ADR-022 | 19 services inside ACE, a schema and a login per service, Kafka with outbox and inbox, contract-first REST with one hop, per-service migration ownership, and the local decision record |

### 19. Out of scope

- The credit approval pack, the checklist rows, the input ages, the copy action per field and the NLEADS submission step: `RWB-P2-E2006-APP` and INT-26.
- The two integration-base operations `GET /treatments/{treatmentId}/credit-pack` and `POST /treatments/{treatmentId}/credit-result`, their element names and their fakes: `RWB-P2-E2006-APP` (GAP-2690; ASM-4437).
- The comparison of the recorded level with the required level and MSG-P2-018: the caller's slice and rwb-access, since this story stores the level as given (BR5; ASM-4439).
- The case route states AWAITING_CREDIT_APPROVAL, OFFER_WITH_CUSTOMER, DECLINED_BY_CREDIT and BACK_TO_ROUTE_DECISION, their move, the case owner's queue and the case-side decision record: `RWB-P3-E2006-APP`.
- The roles, the rights, the scope data and the delegation of authority of item 2.1.1: rwb-access (P4) and its contract.
- The sealing of the record in the central ledger and the rule and reference registries: rwb-decision (P7).
- The account, collateral and valuation reads through `recovery.v_ace_*` and the Section B columns of RWB-ACE-001: rwb-source-data (P1) and its contract (DP-05).
- The checklist documents and their links: rwb-document (P5) and its contract.
- The treatment record, the plan offer, the validity timer, the booking, the payment matching and the broken plan of the plan: `RWB-S2-E3001-APP` and `RWB-S2-E3004-APP` to `RWB-S2-E3011-APP`.
- The query and result operation that records a credit result through an in-process interface (`TreatmentCommands.recordCreditResult` of the legacy): replaced by the REST write of 12.1 (DP-11).
- The gateway-bff composite route, the SCR-14 field list and the layout: `RWB-PLT-N001-CON` and the screen owners (DP-19).
- The real cross-service proof against the live rwb-integration, rwb-case, rwb-access and rwb-decision: the wave 2 integration harness.
- The deployment of this build: chart values, the schema and login provisioning, the switch, the dashboards and the runbook.
