# RWB-S6-E6001-CON Approve lots, reserve and tiered terms - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | API Specification v5 |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Size (INVEST Small) | Fits two weeks: Not specified in the source documents (DOR-RWB-S6-E6001-CON-15); the squad sizes this story at refinement (DOR-RWB-S6-E6001-CON-16) |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | rwb-decision (approval chain as the child ApprovalWorkflow of the kit, started and awaited by this story, which writes neither the approval row nor the ledger entry; and rule package); rwb-access (DoA row); rwb-case (case state read and case move) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the committee-approval slice of RWB-E6-001. It declares the lot read on base `/api/recovery/debtsale/v1` (DP-13), the element with its approval fields and closed lists, the consumed rwb-decision approval chain and rule package, the consumed rwb-access DoA row and the rwb-case read and answer, the rights and the error set, the naming baseline, the boundary and the fakes that let RWB-S6-E6001-APP start on Day 1 (DP-03, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 23 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a squad that owns rwb-debtsale, I want the contract of the lot approval read and of its consumed rows baselined with its fakes, so that the approval build starts on Day 1 without a live rwb-decision, rwb-access or rwb-case.

This contract story carries the interface of the legacy key's approval slice. It owns:

- the one REST operation this key provides, `GET /debt-sale-lots/{lotId}` on base `/api/recovery/debtsale/v1` (API-S6-002, DP-13), with its shape, its rights, its errors and its idempotency statement;
- the `DebtSaleLot` element: the lot fields, its accounts, its reserve, its bids and the approval fields `approval_authority`, `payment_terms` and `signing_date` (DF-SAL-020 to DF-SAL-030);
- the closed lists the element and its consumers read: `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-PUTBACK` (TSD S6 T3.2);
- the consumed rows: the rwb-decision approval chain, act and rule package; the rwb-access delegation limit; the rwb-case state read and the case-move answer (GAP-2980; ASM-4908);
- the error set and the problem envelope of the read, and the fakes every consumer and the build use;
- the naming baseline of the service (DP-13, DP-19) and the boundary that keeps `rwb_decision`, `rwb_access` and `rwb_case` out of this schema.

It does not own: the behaviour behind the read, the rule evaluation, the record write, the column update and the case answer, which are RWB-S6-E6001-APP; the award operation API-S6-003 and the lot-creation operation API-S6-001, which belong to other S6 keys; the approval chain and the decision log, which are rwb-decision's (P7); the DoA table, which is rwb-access's (P4); the case and its route states, which are rwb-case's (P3); and the deployment of the service.

### 2. Business rationale

A split service is only buildable in parallel when its interface is fixed before its behaviour: the APP story and every consumer start from this document and from its fakes, not from a running service. Three facts make the contract of this key worth its own story.

**The base changes.** The monolith served the Workbench from one base; the target serves each service from its own, `/api/recovery/debtsale/v1` (DP-13). The read that shows an approved lot on SCR-25 and SCR-26 is the same read, on a new base, and every consumer needs that base, that shape and that error set in writing.

**The approval is not a screen of this service.** The chain, the act, the DoA limit and the ledger entry belong to rwb-decision and rwb-access, and the case belongs to rwb-case. The contract must therefore declare what this service **consumes** as precisely as what it provides, so that the approval build can be tested with fakes and the real chain only arrives in integration (GAP-2980; ASM-4908).

**The approval facts must be named once.** `approval_authority`, `payment_terms` and `signing_date` are columns of `debt_sale_lot` (DF-SAL-027 to DF-SAL-029) and elements of the read; if the element and the table disagree, every consumer of the lot drifts. Naming them here fixes them for the approval, the award and the data-room keys alike.

The key is EP06 and therefore wave 4, while the service is created in wave 3; the date is copied unchanged and marked tentative. The contract is Day 1 work in contract group CG-W4, because a CON story has no build dependency and every later story of the key waits on it (R5.7 rules 1 and 8).

### 3. Preconditions

- The service row of the context pack is in force: code S6, service rwb-debtsale, schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1`, queue `rwb-debtsale`, package `th.co.scb.ace.workbench.recovery.debtsale`.
- The ownership rows of S6 are in force: the two tables, the five REST operations, the one event and the one workflow (context pack, ownership rows).
- The naming rules of R4 and the DP table of R5.5 are in force (DP-03, DP-13, DP-19 apply to this key).
- The TSD S6 API appendix (T-A.1 and T-A.2) is the source of the read: path, purpose, request, response, errors, authorization and idempotency.
- The element is taken from TSD S6 T3.1 and the closed lists from T3.2; the Logical Data Model v8 carries the field IDs.
- The consumed rows are described only as far as their owners publish them; where an operation name is not published the placeholder of §R9 is used and the row is recorded (GAP-2980; ASM-4909).
- No approval is needed to baseline a Draft contract; the contract tag is set when the contract tests of this story pass.

### 4. Flow

1. This story reads the service row, the ownership rows, the naming rules, the TSD appendix and the data model, and writes the contract of the read, the element, the lists, the consumed rows, the errors and the fakes.
2. It publishes the contract document and its machine-readable form (the operation, the element and the closed lists) in the service's contract repository, versioned with the contract group.
3. It publishes the fakes: the read answered from a fixture lot, the consumed approval chain, the DoA row, the case state and the case-move answer, each with its healthy and its failing answer.
4. RWB-S6-E6001-APP binds to the read and to the fakes on Day 1 and writes the behaviour behind them (the approval branch, the evaluator, the record, the columns and the answer).
5. The award, data-room and transfer stories of S6 bind to the same element and the same base for their own operations, so the element is declared once for all of them.
6. A consumer that needs a field not in the element raises a contract change against this story; the field is added here, never ad hoc in a consumer.
7. On integration, the fakes are replaced by the real rwb-decision, rwb-access and rwb-case services; the contract document does not change, only the endpoint behind it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer asks for a field or a list value that the element does not declare | The request fails the contract test and the field is raised as a contract change against this story | None | AC2, AC6 |
| X2 | A caller does not hold the Debt sale right of the read | The contract fixes 403 with MSG-P4-002 and changes nothing | MSG-P4-002 | AC5 |
| X3 | A lot is unknown or outside the caller's scope | The contract fixes 404, with no existence leak outside the scope | None | AC1, AC5 |
| X4 | A consumed owner changes an operation name or a shape | The fake is regenerated from the owner's document; the consumer build is unaffected because it binds to the fake | None | AC3, AC4, AC6 |
| X5 | A consumed owner has published no operation name | The contract carries the §R9 placeholder and the fake, and the row is recorded | None | AC3, AC4 |
| X6 | A statement reaches `rwb_decision`, `rwb_access`, `rwb_case` or another schema | The boundary test fails the contract build | None (pipeline log) | AC7 |

X1 and X6 protect the contract from silent drift; X4 and X5 are the reason the fakes exist.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 work: no build dependency, no live service, only published documents and its own repository |
| Negotiable | The document format, the fake technology and the test harness are this story's choice; the path, the element, the lists, the rights and the error codes are fixed |
| Valuable | The approval build and every consumer of the lot start on Day 1 against one element, one base and one error set |
| Estimable | One operation, one element, four lists, five consumed rows, one error set and six fakes |
| Small | Finished inside one week |
| Testable | Contract tests on the fakes, a schema check of the element and a boundary test of the schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract of approve lots, reserve and tiered terms

  Scenario: AC1 The lot read is declared on the debtsale base with its shape and its errors (new, D-RCV-60)
    Given the service row fixes rwb-debtsale and the base "/api/recovery/debtsale/v1"
    When the contract is published
    Then "GET /debt-sale-lots/{lotId}" is declared with status 200 and the DebtSaleLot element
    And the errors 400, 401, 403, 404 and 503 are declared with the problem envelope

  Scenario: AC2 The DebtSaleLot element carries the lot, the reserve and the approval fields (new, D-RCV-60)
    Given the element is taken from TSD S6 T3.1 and the data model
    When the contract is published
    Then the element carries DF-SAL-020 to DF-SAL-030
    And it carries approval_authority, payment_terms and signing_date, and the four closed lists of T3.2

  Scenario: AC3 The consumed rwb-decision approval chain and rule package are declared (new, D-RCV-60)
    Given rwb-decision owns the approval chain, the act, the ledger entry and the rule package
    When the contract is published
    Then the consumed rows are declared with their owner, their path and their use
    And a fake answers each row in its healthy and its failing form

  Scenario: AC4 The consumed rwb-access DoA row and the rwb-case rows are declared (new, D-RCV-60)
    Given rwb-access owns the delegation limit and rwb-case owns the case and its route states
    When the contract is published
    Then the DoA read, the case read and the case-move answer are declared as consumed rows
    And no row is declared as a table of this schema

  Scenario: AC5 The right, the scope and the partner path are fixed on the read (new, D-RCV-60)
    Given the RBAC rows of TSD S6 T6.1
    When the contract is published
    Then the read declares the Debt sale right R with scope applied
    And 403 carries MSG-P4-002 and 404 leaks no lot outside the scope

  Scenario: AC6 The fakes answer the document and the contract tests run against them (new, D-RCV-60)
    Given the six fakes of the contract
    When the contract tests run
    Then the read answers the fixture lot and each consumed row answers its fake
    And a document change fails the test until the fake and the element are updated

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming rules of R4 and the pattern table of R5.5
    When the contract is published
    Then the base, the queue and the package follow the service row
    And the service's one event is declared as the award story's and no event is declared in this key

  Scenario: AC8 A consumed activity that is retried or times out is answered with the declared errors (new, D-RCV-60)
    Given the rwb-decision approval chain fake is set to a retried or timed-out call
    When the contract tests run
    Then the read answers with an error of the set declared in AC1
    And the retry count and the timeout are Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC10)

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a lot whose state does not allow the requested change
    When the contract tests run
    Then the answer refuses the change with an error of the set declared in AC1
    And the allowed transitions of the lot are Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC11)

  Scenario: AC10 Each business rule of section 8 is checked by a test case (new, D-RCV-60)
    Given the rules BR1 to BR8 of section 8
    When the contract tests run
    Then each rule is checked by a test case of section 16 or by the boundary check of TC-S6-E6001-CON-06

  Scenario: AC11 A write replayed with the same idempotency key does not repeat its effect (new, D-RCV-60)
    Given a write request whose idempotency key was already used on this contract
    When the contract tests run
    Then the replay does not repeat the effect of the first request
    And its answer is Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC9)
```

All eleven criteria are new under D-RCV-60 and test the contract deliverable only. The legacy criteria of RWB-E6-001 belong to RWB-S6-E6001-APP, are copied there word for word, and are not restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one base: the read is served on `/api/recovery/debtsale/v1` and no consumer reaches the schema | DP-13; context pack service row |
| BR2 | The element is declared once for all S6 keys that read a lot: the approval, the award, the data room and the transfer bind to it | Context pack ownership rows; TSD S6 T3.1 |
| BR3 | The approval fields are the table's: `approval_authority`, `payment_terms` and `signing_date` are columns of `debt_sale_lot` and elements of the read | TSD S6 T3.1; DF-SAL-027 to DF-SAL-029 |
| BR4 | The approval chain, the act, the ledger entry, the rule package and the DoA limit are consumed as contracts; this service writes none of them | GAP-2980; ASM-4908 |
| BR5 | The case route states are read and the move is answered; no case row is read as a table | GAP-2980; ASM-4909 |
| BR6 | The contract declares no event for this key: the service's one event, EV-23 `LotAwarded`, is the award story's | GAP-2982; ASM-4910 |
| BR7 | No value a business person may change is in the contract as a constant: the four lists are declared as lists and read with their version as reference data under DP-06 and DP-07; the list names and parameters read are Not specified in the source documents (DOR-RWB-S6-E6001-CON-20) | TSD S6 T3.2; FSD S6 A2.5.3.1 BR-S6-005; DP-06; DP-07 |
| BR8 | The contract carries no personal data in its examples, its fixtures or its logs | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The contract has no business state machine of its own; it fixes the states the read and the answer expose. The states below are those the element and the consumed rows carry, and they are declared, not applied, here.

| Element | Values | Owner of the values |
|---|---|---|
| Case route state on the read | `LOT_BUILT`, `LOT_WITH_COMMITTEE`, `LOT_APPROVED`, `LOT_WITHDRAWN` | rwb-case (P3) |
| `debt_sale_lot.status` | BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED (`LOV-LOT-STATUS`) | rwb-debtsale (S6) |
| `debt_sale_account.put_back_status` | NONE, CLAIMED, ACCEPTED, REJECTED (`LOV-PUTBACK`) | rwb-debtsale (S6) |
| Contract baseline | Draft, then baselined when this story's contract tests pass | This story |

The business transitions of the case are in RWB-S6-E6001-APP and in the TSD T4 machine; this story declares the values and their owner and changes none of them.

### 10. Authority

| Who | What they may do with this contract |
|---|---|
| RW-DEBTSALE, debt sale officer | Consume the read with right R in scope; the A right belongs to the award story |
| RW-HEADASL, RW-PRODHEAD | Consume the read with right R in scope |
| The other TSD S6 T6.1 staff roles | Consume the read with right R in scope |
| PT-BUYER, PT-RAMC | Consume the partner view through the partner gateway and the gateway-bff route, never the approval authority |
| SY-CASEWF, SY-RULES, SY-AGENT | Consume the read as service identities under the same checks |
| rwb-debtsale squad | Own the contract, its fakes and its tests |
| rwb-decision, rwb-access, rwb-case squads | Own the consumed rows this contract binds to; a change is raised against them and reflected in the fake (GAP-2980; ASM-4909) |

The rights are the rows of TSD S6 T6.1; the contract adds no right and removes none.

Each read is authorised by an rwb-access check under DP-08 before it is served; the check's operation name is Not specified in the source documents (DOR-RWB-S6-E6001-CON-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | In the element |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6) | id | Yes, the lot reference |
| DF-SAL-021 | debt_sale_lot (S6) | lot_no | Yes |
| DF-SAL-022 | debt_sale_lot (S6) | cut_off_date | Yes |
| DF-SAL-023 | debt_sale_lot (S6) | segment | Yes, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6) | reserve_price | Yes |
| DF-SAL-025 | debt_sale_lot (S6) | buyer_partner_id | Yes, where the lot is awarded |
| DF-SAL-026 | debt_sale_lot (S6) | buyer_class | Yes, against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6) | signing_date | Yes, the approval field |
| DF-SAL-028 | debt_sale_lot (S6) | approval_authority | Yes, the approval field |
| DF-SAL-029 | debt_sale_lot (S6) | payment_terms | Yes, the approval field |
| DF-SAL-030 | debt_sale_lot (S6) | status | Yes, against `LOV-LOT-STATUS` |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Yes, as the accounts of the lot |
| Standard columns | both tables (S6) | `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_active` | `version` only, as the optimistic lock of the element |

The four closed lists are `LOV-SEGMENT` (RETAIL, SSME, CORPORATE), `LOV-BUYER-CLASS` (AMC, NON_AMC), `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED) and `LOV-PUTBACK` (NONE, CLAIMED, ACCEPTED, REJECTED) (TSD S6 T3.2). **No personal data**: `borrower_code` is a code and no name, address, contact value or identity number appears in the element, the examples or the fixtures (BR8). **No new table and no new column**: the element is a view of two existing tables.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/debt-sale-lots/{lotId}` | `DebtSaleLot` of status 200 out, with its accounts, reserve and bids (API-S6-002) | Debt sale, right R, scope applied | Not applicable |
| POST | `/debt-sale-lots` | `DebtSaleLot` of status 201 out from a `LotRequest` (API-S6-001) | Debt sale, right C, scope applied | `Idempotency-Key` header |
| POST | `/debt-sale-lots/{lotId}/award` | `DecisionLogEntry` of status 200 out from an `AwardRequest` (API-S6-003) | Debt sale, right A, scope applied | `Idempotency-Key` header |
| GET | `/partner/data-room/{lotId}` | `DataRoom` of status 200 out (API-S6-004) | Partner portal, right R, scope applied | Not applicable |
| POST | `/partner/data-room/{lotId}/bids` | `Bid` of status 201 out from a `BidRequest` (API-S6-005) | Partner portal, right C, scope applied | `Idempotency-Key` header |

This story baselines the five operations of the service because one element and one base are shared by them; the behaviour of each belongs to its own key, and the approval key builds only the read. The path, the request, the response, the errors, the authorization and the idempotency of each row are those of TSD S6 T-A.1 and T-A.2 and are not redefined here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The approval chain read and the approver's act (three act rows; the architecture names one `POST /approvals/{id}/decide`) | `/api/recovery/decision/v1` | P7 rwb-decision | The chain, the act and the DoA level tested; faked (GAP-2980; ASM-4909) |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2980; ASM-4909)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and its rule rows; faked |
| `GET /doa-limits` | `/api/recovery/access/v1` | P4 rwb-access | The `delegation_limit` row of the approver's level; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the reference and the stage; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2980; ASM-4909)) | rwb-case (P3) | P3 rwb-case | `LOT_WITH_COMMITTEE`, `LOT_APPROVED` or `LOT_WITHDRAWN` with the rule and its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream (ADR-020). The five rows are class C dependencies that the plan's C row does not carry, so the contract binds to their published documents and fakes (GAP-2981; ASM-4907).

#### 12.3 Events published

None in this key. The service owns one event, EV-23 `rwb.debtsale.LotAwarded.v1` on topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics (context pack, ownership rows; TSD S6 T5.3), and it is published by the award story. This key declares it by name for the topic baseline and publishes nothing (GAP-2982; ASM-4910).

#### 12.4 Events consumed

None. The approval answer arrives on the chain the approval story starts and on the rwb-case contract; this key declares no consumer group and no subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow` | `rwb-debtsale` in namespace `rwb-recovery` | Input: the case, the lot, the reserve, the tiered terms and the package in force; signals: the approval answer and the case state |
| `ApprovalWorkflow` | Child workflow, the kit's Approval template, owned and run by rwb-decision | `rwb-decision` (P7) | The maker-checker chain with the DoA lookup as a parameter; started by the approval story (GAP-2980) |
| `recordCommitteeApproval` | Activity of the approval story | `rwb-debtsale` | The case, the lot and the answer in; the record, the columns and the move out, in one transaction |

The workflow contract is declared here; its behaviour, its activities and their names are RWB-S6-E6001-APP's.

Start rule: the workflow starts when the monthly sale cycle opens or a residual arrives from disposal (R-DS-01). Workflow ID form: Not specified in the source documents (CG-ALL-10447). Duplicate-start policy: Not specified in the source documents (CG-ALL-10447).

#### 12.6 Schedules

None. The service owns no job (context pack, jobs: None) and this key registers no Temporal Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, the reserve and the three approval fields |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of a lot |
| decision_record | PLT library, in `rwb_debtsale` | The local record, created by the library (DP-03) |
| idempotency_key | PLT library, in `rwb_debtsale` | The key of a repeated write |
| outbox_event | PLT library, in `rwb_debtsale` | Created by the library; used by the stories that publish |

Not owned and never read as tables: `recovery_case` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `delegation_limit` (P4), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Lot read fake | The fixture lot `LOT-2027-000041` with two accounts, its reserve, its terms and its approval authority, status 200 | AC1, AC2, AC6 |
| Element and lists schema check | The element against DF-SAL-020 to DF-SAL-037 and the four closed lists against T3.2 | AC2, AC6 |
| rwb-decision approval-chain fake | Decided inside the delegation, decided outside it, returned for a raised reserve, refused, and no answer beyond 2 s | AC3, AC6 |
| rwb-decision rule-package fake | The DS package at its version with R-DS-04, R-DS-06, R-DS-07 and R-DS-08 | AC3, AC6 |
| rwb-access DoA fake | A limit above and a limit below the reserve; no answer beyond 2 s | AC4, AC6 |
| rwb-case state and move fake | The four route states, the three moves accepted and a move refused | AC4, AC6 |
| Error fake | 400, 401, 403 with MSG-P4-002, 404 and 503 in the problem envelope | AC1, AC5, AC6 |

The fakes are test-only and are replaced by the real services in integration. The unpublished names carry the placeholder until their owners publish them (GAP-2980; ASM-4909).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 5 consumed | The five service operations on `/api/recovery/debtsale/v1`; the approval chain, the rule package, the DoA read, the case read and the case-move answer; one hop, 2 s |
| Kafka | 1 declared, 0 in this key | EV-23 `rwb.debtsale.LotAwarded.v1`, published by the award story |
| Temporal | 1 workflow, 1 child workflow, 1 activity | `DebtSaleWorkflow` on `rwb-debtsale`, the P7 `ApprovalWorkflow` child, `recordCommitteeApproval`; no Schedule |
| File | None | No file is read, built or delivered by this key |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `contract`, package `th.co.scb.ace.workbench.recovery.debtsale.contract`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 fixes the record element the approval story writes; the pattern table adds the platform contract dependency, so the contract story declares it for the build that follows. DP-13 and DP-19 fix the base and the route the read is reached through. This contract story itself has no build dependency and sits in CG-W4, as a CON story must (R5.7 rule 1).

**Artefacts**

| Artefact | Content |
|---|---|
| `openapi/debtsale-v1.yaml` | The five operations, the element, the requests, the error set and the idempotency headers |
| `schema/DebtSaleLot.json` | The element of DF-SAL-020 to DF-SAL-037 with the closed lists as enumerations |
| `schema/lists.yaml` | `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-PUTBACK` at their version |
| `fakes/` | The seven fakes of 12.8, each with a healthy and a failing answer |
| `tests/contract/` | The contract tests of section 16, run on every change of the document or a fake |

**Database and migrations.** None. The contract declares an element over two existing tables and adds no DDL; the tables arrive with the DB story of the service.

**Configuration and reference data.** The base, the queue, the topic and the package name come from the service row and are not configurable per environment; the four lists are read with their version and are never inlined as constants in the element's consumers.

**Tests.** Contract tests on the fakes; a schema check of the element against the data model; a naming check of the base, the queue and the package; a boundary check that no consumed row is declared as a local table.

### 14. Validation and messages

| ID | HTTP | Message | When |
|---|---|---|---|
| MSG-P4-002 | 403 | You cannot {action} here. Your role does not include it. | The caller does not hold the Debt sale right of the read (X2) |
| MSG-P7-003 | 503 | The action was not taken because the decision could not be recorded. Try again in a few minutes. | A consumed decision contract does not answer and the step cannot proceed |
| None | 400 | A malformed request, in the platform problem envelope | The path or the query is malformed |
| None | 401 | Not authenticated | No session or an expired one |
| None | 404 | The lot is unknown or outside the scope | X3; the answer reveals nothing outside the scope |
| None | 409 | The case is not in the state the rule expects | A move is answered for a case in another state |

The two business messages are the legacy and FSD messages, copied unchanged; the four envelope answers carry no business text and are the platform's. The contract fixes the codes and the envelope, not the wording of the platform errors.

### 15. Screens and states

| Screen | States | Fields the contract exposes |
|---|---|---|
| SCR-25 Lot builder | Draft; priced; approved; empty, loading, error, no access: Not specified in the source documents (CG-ALL-10450) | Lot number, cut-off date, segment, reserve, terms, approval authority, accounts |
| SCR-26 Award | Open; closed; awarded; transferred; empty, loading, error, no access: Not specified in the source documents (CG-ALL-10451) | Lot number, reserve, terms, approval authority, buyer class, signing date |

Both screens read the element through the gateway-bff composite route (DP-19) and compose it with the approval rows of rwb-decision and the case route state of rwb-case; the contract of this service exposes only the lot facts, and the approval rows and the case state are their owners'.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S6-E6001-CON-01 | AC1; BR1 | Contract | The read on the fixture lot; the five error codes in the envelope |
| TC-S6-E6001-CON-02 | AC2; BR2, BR3, BR7 | Contract | The element against DF-SAL-020 to DF-SAL-037 and the four lists |
| TC-S6-E6001-CON-03 | AC3; BR4 | Contract | The rwb-decision chain and package fakes, healthy and failing |
| TC-S6-E6001-CON-04 | AC4; BR5 | Contract | The DoA fake and the case state and move fakes |
| TC-S6-E6001-CON-05 | AC5 | Contract | A caller with the right, a caller without it, and a lot outside the scope |
| TC-S6-E6001-CON-06 | AC6, AC7; BR6, BR8 | Contract | The seven fakes, the naming check and the boundary check |
| TC-S6-E6001-CON-07 | §12.7 (ASM-3438) | Contract | Each table of §12.7 and each v_ace_* view against its owner; no foreign key leaves the schema (DP-01) |
| TC-S6-E6001-CON-08 | AC8 | Contract | Retried and timed-out call on the approval chain fake; retry count and timeout Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC10) |
| TC-S6-E6001-CON-09 | AC9 | Contract | Status change the model does not allow; allowed transitions Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC11) |
| TC-S6-E6001-CON-10 | AC10; BR1 to BR8 | Contract | Each rule of section 8 against its test case or the boundary check |
| TC-S6-E6001-CON-11 | AC11 | Contract | Replay of a write with the same idempotency key; proposed test Not specified in the source documents (NEWAC-RWB-S6-E6001-CON-AC9) |

The eleven cases are the contract tests of this story and run on every change of the document or a fake. The legacy test cases TC-E6-001-01 to TC-E6-001-06 stay with RWB-S6-E6001-APP and are not copied here.

### 17. Guardrails

- No business value in the contract as a constant: the four lists and the thresholds are declared as lists and values read with their version.
- No personal data in the element, the examples, the fixtures or the logs; the fixture lot is synthetic.
- ACE data only through the owner's contract or `v_ace_*` views; this contract declares no ACE view and no cross-schema read.
- One hop per call, 2 s, a breaker per downstream; no consumer chains two services.
- No consumed row is declared as a local table; the boundary test fails the build on a cross-schema statement.
- Every consumed row names its owner; a row without an owner fails the naming check.
- The contract changes only by a new version, never in place; a consumer binds to a version.

### 18. Traceability

| Legacy | Legacy feature | New story | New AC | Requirement |
|---|---|---|---|---|
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC1, AC5 | REQ-S6-004 |
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC2 | REQ-S6-005 |
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC3 | REQ-S6-006 |
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC4 | REQ-S6-007 |
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC6 | REQ-S6-008 |
| RWB-E6-001 | FEAT-DBS-05 | RWB-S6-E6001-CON | AC7 | REQ-S6-009 |

Feature FEAT-DBS-05 of the FSD S6 (A2.5); epic E6 of the story master; business epic EP06; service epic RWB-SVC-S6; contract group CG-W4; PRD reference Pending (C1). The requirement IDs are the TSD S6 T8 rows that name FEAT-DBS-05. The legacy criteria and test cases are traced through RWB-S6-E6001-APP.

### 19. Out of scope

- The behaviour behind the read: the rule evaluation, the record write, the column update and the case answer; RWB-S6-E6001-APP owns them.
- The approval chain, the approver's act, the approval rows, the decision log and the rule package; rwb-decision owns them.
- The DoA table and the delegation limits; rwb-access owns them.
- The case, its route states and the parent workflow; rwb-case owns them.
- The award, data-room and transfer behaviour behind the other four operations; their own keys own it.
- The database schema, the migrations and the grants; the DB story of the service owns them.
- The gateway-bff route configuration; RWB-PLT-N001-CON owns it.
- The deployment and the environments; the operations story of the service owns them.
