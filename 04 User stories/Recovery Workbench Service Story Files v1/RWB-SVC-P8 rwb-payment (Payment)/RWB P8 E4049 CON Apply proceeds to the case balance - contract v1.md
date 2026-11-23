# RWB-P8-E4049-CON Apply proceeds to the case balance - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E4049-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **tech lead of rwb-payment**, I want **the published contract baseline of the proceeds application – the OpenAPI 3.1 document of `/api/recovery/payment/v1` with `GET /proceeds` and `POST /proceeds/{proceedsId}/match`, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements over DF-FIN-001 to DF-FIN-009 with the applied amounts in the answer, the lists `LOV-MATCH`, `LOV-MATCH-TYPE` and `LOV-PROCEEDS-SRC`, the `ProceedsMatched` schema on `rwb.payment.events.v1` with the CloudEvents envelope, the `proceeds` table of `rwb_payment` and its versioned baseline, the error envelope, the rights, the compatibility rule and the fakes**, so that **the app story, SCR-28 Proceeds matching and the wave 3 harness build against one fixed contract on Day 1, and a path, a field, a list value, an applied amount or an event name can never drift between rwb-payment, rwb-case, rwb-source-data and the screens without a failing build**.

This is the contract slice of legacy RWB-E4-049 (FEAT-PAY-10, module P8 Payments and posting). It owns the published surface only: the two operations, the elements and the applied-amount answer, the event schema, the table baseline, the error set, the rights, the compatibility rule and the fakes. It owns no behaviour and copies no legacy criterion: the two legacy acceptance criteria of the story stay word for word with RWB-P8-E4049-APP (GAP-2529; ASM-4182).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith, the application read `v_ace_account`, `v_ace_payment`, the `recovery_case` row, the `decision_log_entry` row and the `proceeds` row in one process on `/api/recovery/v1`, so no boundary existed that another team could build against; every reader of the application was also a reader of four other modules' tables. In the target each boundary is a contract: the receipt and balance facts are rwb-source-data's, the case and its balance are rwb-case's, the rule package is rwb-decision's and the money is rwb-payment's.

Three consumers depend on this baseline on Day 1. RWB-P8-E4049-APP builds the application step of JOB-07 and cannot start until the elements, the applied-amount answer, the event schema and the fakes are fixed. The rwb-case team consumes `ProceedsMatched` and answers the balance application on its own contract, so the shape of both sides has to be pinned while its stage is still being written. SCR-28 Proceeds matching reaches the two operations through the gateway-bff composite route (DP-19), so the screen contract, the error envelope and the pagination have to be settled before the screen work starts.

The baseline also fixes the naming the checks require: schema `rwb_payment`, base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with retry and `.dlt` topics, event names `rwb.payment.<Event>.v1`, task queue `rwb-payment` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.payment` (context pack; Template and Rules R4). It records that this service holds no `v_ace_*` grant and no grant on another `rwb_*` schema, so DP-05 is declared as a prohibition: the receipt and the balance of ACE arrive on rwb-source-data's contract and never through a view of this service.

Two points are carried as gaps rather than decided quietly. The TSD names `MatchRequest` and `ProceedsPage` without a field list, and the applied-amount answer the legacy criterion needs appears in no document, so the elements are derived from the nine columns of `proceeds`, the query parameters of API-P8-001 and the wording of the criterion (GAP-2532; ASM-4185). The application order – its components, its sequence and its caps – is named only as "the order the policy sets" and is published nowhere, so the contract fixes it as a rule-package value and never as a schema default, an enumeration or an example (GAP-2530; ASM-4183).

### 3. Preconditions

- The service naming rule of the platform library is in force: base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` with retry and `.dlt`, event names `rwb.<short>.<Event>.v1`, queue `rwb-<short>`, login and schema `rwb_<short>` (context pack; Template and Rules R4).
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `proceeds` and the two operations are P8's, `recovery_case` and the balance are P3's, the `v_ace_*` views are P1's, and `rule_row`, `rule_package_version` and `decision_log_entry` are P7's. This document never declares another service's operation or table as provided.
- The two operations and their shapes are the ones of TSD P8 T-A.1 and T-A.2: API-P8-001 `GET /proceeds` with `ProceedsPage` out and errors 401, 403 and 503, and API-P8-002 `POST /proceeds/{proceedsId}/match` with `MatchRequest` in, `Proceeds` out, errors 401, 403, 404, 409, 422 and 503, and the `Idempotency-Key` header.
- The columns and the lists are the ones of TSD P8 T3.1 and T3.2: DF-FIN-001 to DF-FIN-009, the values `INSTALLMENT`, `SETTLEMENT`, `FEE`, `SALE_PROCEEDS` and `UNMATCHED` of `LOV-MATCH`, the values `EXACT`, `WINDOW` and `PARTIAL` of `LOV-MATCH-TYPE`, and `CUSTOMER`, `LED`, `AUCTION`, `BUYER`, `AGENCY`, `INSURER` and `GUARANTOR` of `LOV-PROCEEDS-SRC`.
- The event is the one of Architecture v5 slides 42 and 43: `ProceedsMatched` (25), produced by rwb-payment and consumed by rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee; the envelope is CloudEvents 1.0 in binary mode with key `caseId`, 12 partitions, replication factor 3 and 7-day retention (slide 22).
- The schema registry is in BACKWARD mode and the AsyncAPI document per service is the contract, so the event is registered against it (Architecture v5 slide 42 notes).
- The `proceeds` table arrives with the DB story of this service; this baseline declares its name, its schema, its columns and its baseline version, and creates nothing.
- RWB-P8-E4049-APP, SCR-28 and the wave 3 harness are named as the consumers of this baseline but are not build dependencies: this story has none and is Day 1 by rule (Template and Rules R5.7).
- No approval is needed to publish a Draft baseline in this run, and no human verification stop is part of it.

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-payment for this surface: the two operations, the elements, the query parameters, the pagination, the rights and the seven error responses.
2. Fix the `Proceeds` element on DF-FIN-001 to DF-FIN-009 and the answer field that carries the amounts applied, with no new column and no new table.
3. Fix `ProceedsPage` on the pagination convention and `MatchRequest` on the fields the application needs, marking the fields no source gives with the placeholder.
4. Publish `LOV-MATCH`, `LOV-MATCH-TYPE` and `LOV-PROCEEDS-SRC` as enumerated values of the document, and fix the rule that no application order, percentage or cap is a schema default or an enumeration member.
5. Draft the AsyncAPI fragment and the JSON schema `ProceedsMatched` with the CloudEvents envelope, `ce_type` `rwb.payment.ProceedsMatched.v1`, `ce_source` `/rwb-payment`, `ce_subject` `case/<caseId>`, key `caseId` and no personal data.
6. Fix the `rwb_payment.proceeds` table baseline: the columns, the standard record columns, the baseline version and the rule that no foreign key leaves the schema.
7. Record the consumed surface as consumed and faked: the receipt and balance read of rwb-source-data, the case read and balance-application answer of rwb-case and the package read of rwb-decision.
8. Fix the error envelope and one message ID per condition, the rights of the capability area "Write-off and posting", and the `Idempotency-Key` rule with its stored answer.
9. Publish the six contract fakes and the drift test that compares each with the document.
10. Add the contract tests, tag the baseline and hand it to RWB-P8-E4049-APP, SCR-28 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A path, a property or a list value is renamed or removed within major version 1 | The contract test fails; the change needs a new major version and a new event type | None | AC7 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6, AC7 |
| X4 | A field of `MatchRequest`, of the applied-amount answer or of the event payload has no source value | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC4 |
| X5 | An application order, a percentage or a cap appears as a schema default, an example constant or an enumeration member | The vocabulary test fails the build | None | AC3 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, or a `recovery_case`, balance or `rule_row` property | The review fails the baseline and the boundary test fails the build | None | AC5, AC7 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC6 |
| X8 | The rights of an operation are not the ones TSD P8 T6.1 and T-A.2 declare | The access test fails the build | MSG-P4-002 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, TSD P8 and the published owner documents of rwb-case, rwb-source-data and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the paths, the columns, the lists, the base, the topic, the queue and the event names are fixed by the target architecture |
| Valuable | Unblocks RWB-P8-E4049-APP, SCR-28 and the wave 3 harness on Day 1, and pins the `ProceedsMatched` schema for its five consumers on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the proceeds application of rwb-payment

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of proceeds and of the two operations is P8, of recovery_case and its balance is P3, of the v_ace_* views is P1 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations are declared on the payment base and the application is their behaviour (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-payment is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /proceeds with the ProceedsPage answer of status 200 and POST /proceeds/{proceedsId}/match with the Proceeds answer of status 200, both under the base /api/recovery/payment/v1 and owned by rwb-payment
    Then GET /proceeds declares the query parameters matched, from, to, page and size, and answers ProceedsPage
    Then POST /proceeds/{proceedsId}/match declares the MatchRequest body and answers Proceeds with the amounts applied to the case balance
    Then the document declares no third operation for the application, no monolith API base and no operation of another service

  Scenario: AC2 The Proceeds element and the applied-amount answer are fixed on the contracted columns (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with TSD P8 T3.1
    Then Proceeds carries DF-FIN-001 to DF-FIN-009 and the TSD P8 T3.0 standard columns, with no additional column for the order, the components or the applied state
    Then the answer of POST /proceeds/{proceedsId}/match carries the amounts applied per balance component and the rule ID with its version, and every field the sources do not give carries the placeholder
    Then MatchRequest and ProceedsPage are published with their fields and the query parameters of API-P8-001
    Then no amount, percentage, cap or order appears in the document as a default or a constant

  Scenario: AC3 The application order is a rule-package value and never a contract value (new, D-RCV-60)
    Given the vocabulary and the schema defaults of the baseline
    When they are inspected for the order, the components, the percentages and the caps
    Then LOV-MATCH, LOV-MATCH-TYPE and LOV-PROCEEDS-SRC are published as the only enumerations of the surface
    Then no enumeration member names an application order or a balance component
    Then the document states that the order is read from the PAYMENT_MATCH package at its version in force through the rwb-decision contract
    Then a build that adds such a value to the document or to a fake fails the vocabulary test

  Scenario: AC4 The ProceedsMatched schema carries the application and no personal data (new, D-RCV-60)
    Given the AsyncAPI fragment and the JSON schema of ProceedsMatched
    When they are validated and the registry is checked
    Then the schema declares caseId, the proceeds reference, the treatment reference, the receipt amount, the amount applied, the value date, the match value and the rule ID with its version, and the remaining fields carry the placeholder
    Then each message declares the CloudEvents 1.0 binary envelope with ce_type rwb.payment.ProceedsMatched.v1, ce_source /rwb-payment, ce_subject case/<caseId> and a W3C traceparent header
    Then the schema registers in BACKWARD mode and a removed field is refused
    Then no name, address, contact value or identity number appears in the schema, an example or a fake

  Scenario: AC5 The consumed balance surface is consumed and faked, and no cross-schema key leaves rwb_payment (new, D-RCV-60)
    Given the consumed rows of the baseline and the table baseline
    When they are compared with the ownership rows and TSD P8 T3.3
    Then the case read and the balance-application answer of rwb-case, the receipt and balance read of rwb-source-data and the package read of rwb-decision are described as consumed and faked, never as provided
    Then the baseline declares no v_ace_* read, no balance table and no recovery_case, assignment, task or timer property
    Then rwb_payment.proceeds declares DF-FIN-001 to DF-FIN-009 and the standard columns, with no foreign key leaving the schema

  Scenario: AC6 The Idempotency-Key rule, the error set and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD P8 T-A.2 and T6.1
    Then POST /proceeds/{proceedsId}/match declares the Idempotency-Key header and its stored answer, and GET /proceeds declares none
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect
    Then a receipt that is already applied answers 409, an unknown proceedsId answers 404, and a missing or invalid field answers 422 with MSG-GEN-001
    Then both operations declare the capability area Write-off and posting with rights R and U, and a role without the right answers 403 with MSG-P4-002

  Scenario: AC7 Compatibility and boundary hold for the whole surface (new, D-RCV-60)
    Given the published baseline and its fakes
    When the drift, boundary and absence tests run
    Then every consumed path is answered by its fake and a drifted fake fails the build
    Then the document declares no data-lake copy, no Schedule, no Quartz row and no shared job table
    Then an added property is accepted within major version 1 and a renamed or removed one is refused until a new major version and a new event type are published
```

The seven criteria are new contract criteria: the legacy criteria of RWB-E4-049 are behavioural and stay word for word with RWB-P8-E4049-APP, and this baseline copies none of them (GAP-2529; ASM-4182). Each criterion tests the artefact this story publishes, not a business outcome.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR-P8-010 | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.10.3.1, copied character for character |
| CBR1 | The contract declares only operations and objects owned by rwb-payment; a consumed operation is described as consumed and faked | DP-11; context pack ownership rows |
| CBR2 | The application order, its components, its percentages and its caps are values of the PAYMENT_MATCH package at its version in force, never a schema default, an example constant or an enumeration member | DP-04; FSD P8 A2.10.1 and A2.10.3.1; GAP-2530 |
| CBR3 | `Proceeds` carries DF-FIN-001 to DF-FIN-009 and no additional column: the applied amounts travel in the answer, and the applied state value is the DB story's, not a contract member | TSD P8 T3.1 and T3.0; GAP-2532 |
| CBR4 | No foreign key leaves `rwb_payment`; `case_id`, `treatment_id` and `account_payment_id` are identifiers of other services' facts | DP-01; TSD P8 T3.3 |
| CBR5 | The event is registered in BACKWARD mode against the AsyncAPI document, and a removed field needs a new major version and a new event type | Architecture v5 slide 42 notes; ADR-015 |
| CBR6 | One base, one topic, one queue and one login per service, and the document names no other service's base or topic as its own | DP-13, DP-14; Template and Rules R4 |
| CBR7 | No personal data in a schema, an example, an event payload or a fake | Template and Rules s17; Architecture v5 slide 42 notes |
| CBR8 | The rights of the two operations are the rows of TSD P8 T6.1 and no wider, and the `Idempotency-Key` rule is the platform rule | TSD P8 T6.1 and T-A.2; Architecture v5 slide 11 |

BR-P8-010 is copied character for character from FSD P8 A2.10.3.1; the remaining rows are the rules the target contract fixes.

### 9. State transitions

This baseline declares no business state machine. The states it fixes are the contract lifecycle of the document and the declared answer of a repeated call.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Baseline review | The five contract tests pass and the consumers accept | Published, major version 1 |
| Published, major version 1 | An additive change | A new optional property or a new event field | Published, same major version, registered in BACKWARD mode |
| Published, major version 1 | A rename or a removal | The change is not additive | Refused; a new major version and a new event type are required |
| Published, major version 1 | A repeated POST with the same `Idempotency-Key` | The key and the answer are stored | Published, the stored answer returned, no second effect |
| Published, major version 1 | A receipt already applied | The contract answers 409 | Published, no schema change |

The behavioural states of the application — the receipt's applied state and the case balance — belong to RWB-P8-E4049-APP and rwb-case, and are not declared here.

### 10. Authority

| Who | What they may do in this baseline |
|---|---|
| Tech lead of rwb-payment | Publishes the baseline, tags the version and answers consumer questions |
| TechX and the P8 squad | Build against the document and the fakes |
| rwb-case, rwb-source-data and rwb-decision owners | Confirm the consumed rows and the placeholders of their operation names |
| rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee teams | Consume the `ProceedsMatched` schema and sign off its compatibility |
| RW-CREDITAD, RW-WRITEOFF, SY-DATALOAD | Write-off and posting U, as declared by the contract of the match and not built here |
| The read-only roles of TSD P8 T6.1 | Write-off and posting R, as declared by the contract of the list |
| QA lead and the wave 3 harness | Copy the contract cases into the harness with the `-ITG` suffix |

No approval is needed to publish a Draft baseline in this run, and no person is named: the owners are roles only.

### 11. Data

| BR Field ID | Entity (owner) | Field | Contracted use |
|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | proceeds (P8, `rwb_payment`) | `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to`, `posting_ref` | Declared in `Proceeds`, `ProceedsPage` and `MatchRequest`; the table baseline of 12.7 |
| TSD P8 T3.0 standard columns | proceeds (P8, `rwb_payment`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Declared in the table baseline; not exposed as contract properties beyond `version` for the optimistic lock |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and 17 more | Consumed only: the case reference and the balance-application answer; no property is declared as ours |
| DF-ACE-001 to DF-ACE-042 and DF-ACE-043 to DF-ACE-054 | `v_ace_account` and `v_ace_payment` (P1) | The balance and receipt facts of the ACE batch | Consumed only on the rwb-source-data contract; the document declares no view and no ACE table |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library) | rule id, rule version, inputs reference, outcome | Declared as a library object, not as a property of this surface |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | `id`, `rule_id`, `rule_version`, `route_set`, `from_state`, `event_code` and 9 more | Consumed as the package read; never declared as ours and never a list member |

The columns are those of TSD P8 T3.1 and of the legacy data table of RWB-E4-049, with their owners changed by the target. The applied-amount answer, the `MatchRequest` field list and the event payload beyond the published example are Not specified in the source documents (GAP-2532; ASM-4185) and are declared with the placeholder.

**No personal data.** Every example and every fake uses synthetic identifiers, amounts, dates and codes; no name, address, contact value or identity number appears.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, filtered by `matched`, `from` and `to`, paginated by `page` and `size` (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out with the amounts applied (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD P8 T-A.1 and T-A.2; the paths are those of the target base and not the monolith form. No third operation is declared for the application: the automatic application runs inside the JOB-07 step of RWB-P8-E4049-APP, and the manual one is the match of API-P8-002.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The receipt and balance read of the ACE batch (operation name Not specified in the source documents (GAP-2531; ASM-4184)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The receipts of the business date for source `ALS` and the account balance of the case, with the freshness stamp of the data product; faked |
| The case read and the balance-application answer (operation names Not specified in the source documents (GAP-2532; ASM-4185)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its product group and state, and the answer that records the amount applied to the case balance; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2530; ASM-4183)) | `/api/recovery/decision/v1` | P7 rwb-decision | The PAYMENT_MATCH package at the version in force and its application-order rule row; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row for this story does not carry, because it is None, so the app story builds against these documents and fakes on Day 1 (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

#### 12.3 Events published

Topic `rwb.payment.events.v1`, with the `.retry` and `.dlt` topics, 12 partitions, replication factor 3 and 7-day retention, key `caseId` (Architecture v5 slide 22).

| Event | Schema name | Consumers | Payload element |
|---|---|---|---|
| `ProceedsMatched` (EV-25) | `rwb.payment.ProceedsMatched.v1` | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | `caseId`, the proceeds reference, the treatment reference, the receipt amount, the amount applied, the value date, the match value and the rule ID with its version; the remaining field list is Not specified in the source documents (GAP-2532; ASM-4185) |

Each message declares the CloudEvents 1.0 binary envelope with `ce_specversion`, `ce_type`, `ce_source` `/rwb-payment`, `ce_id`, `ce_subject` `case/<caseId>` and a W3C `traceparent` header, and the body is validated against the registry in BACKWARD mode. This baseline declares the schema once for the whole service; the publishing step of this legacy key is RWB-P8-E4049-APP. `TreatmentBooked` (EV-11) and `PaymentMissed` (EV-12) are the booking and plan-matching stories' and are not declared here.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.apply-run.v1` | The business date and the source of the completed batch | Declared as consumed by the application story; starts the JOB-07 run |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.apply-run.v1` | The package code and the version in force | Declared as consumed by the application story |

`DecisionRecorded` (EV-08) is written by all nineteen services through the local library on the shared topic `rwb.decision-record.v1`, and its consumers are rwb-decision and rwb-reporting (Architecture v5 slide 42, row 08). rwb-payment is a **producer** of that topic and not a consumer: the baseline declares the record through the library of DP-03 and adds no consumer group or inbox row for it.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The JOB-07 event-started run (name Not specified in the source documents (GAP-2530; ASM-4183)) | Workflow, one execution per business date and source, started by `AceDataReady` | `rwb-payment` in namespace `rwb-recovery` | The boundary the baseline serves: the input record, the two signals and the outcome; not built here |
| The application step of JOB-07 (activity name Not specified in the source documents (GAP-2530; ASM-4183)) | Activity | `rwb-payment` | The activity contract the baseline serves: the receipts, the balance and the package in; the rule ID with its version, the amounts applied, the record, the row, the balance answer and the outbox event out |

No child workflow and no Nexus operation is declared here. `matchPayments` and `postProceeds` are the activities Architecture v5 slide 17 names on the same queue and belong to the matching and posting stories.

#### 12.6 Schedules

None. JOB-07 is an event-triggered run and not a Temporal Schedule (Architecture v5 slide 44), so the baseline declares no Schedule, no Quartz row and no shared job table. JOB-08 is the other job of this service and belongs to its batch stories.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| proceeds | P8 (`rwb_payment`) | The receipt, its match and the amounts applied; the table the two operations read and the match writes |
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked decision record of the rule outcome (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The `ProceedsMatched` row and the relay (DP-09) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The key of the repeated POST and the answer it holds |

The baseline declares the `proceeds` table and its versioned baseline in `rwb_payment`; the migration itself is the DB story of this service. `recovery_case` and the case balance (P3), the `v_ace_*` views (P1), and `rule_row`, `rule_package_version` and `decision_log_entry` (P7) are other owners' and are named only as answers, rule versions or a later story's table; no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data receipt and balance fake | A receipt of source `CUSTOMER` for case `RC-2026-000555` on its business date and the balance of the case; a stale product with its date; no answer beyond 2 s | AC1, AC5, AC7 |
| rwb-case case and balance fake | The case with its route state and an accepted and a refused balance-application answer | AC1, AC5, AC7 |
| rwb-decision package fake | The PAYMENT_MATCH package at its version in force with the application-order row | AC3, AC7 |
| rwb-source-data event fake | `AceDataReady` for business date D and source `ALS`, the same event twice, and an event for an empty batch | AC1, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain with MSG-P7-003 | AC6, AC7 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case, with the proceeds list of this service read once | AC1, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read, of the rwb-case balance answer and of the rwb-decision package read are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two operations on `/api/recovery/payment/v1`; the receipt and balance row, the case and balance-application row and the package row; one hop, 2 s |
| Kafka | 1 published, 2 consumed | `ProceedsMatched` on `rwb.payment.events.v1`; `AceDataReady` and `RulePackageInForce` in group `rwb-payment.apply-run.v1` |
| Temporal | 1 run boundary and 1 activity declared, 0 registered | JOB-07 on `rwb-payment` with its application step; no Schedule |
| File | None | No file is read, built or delivered here; the posting file is the posting story's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no receipt, no case and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-payment-v1.yaml` for this surface, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements with the applied-amount answer, `LOV-MATCH`, `LOV-MATCH-TYPE` and `LOV-PROCEEDS-SRC` as published enumerations, the `ProceedsMatched` JSON schema with the CloudEvents envelope, the contract README rows for the three consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: only rwb-source-data holds SELECT on the `recovery.v_ace_*` views (Architecture v5 slide 29), so the document declares no `v_ace_*` read and no grant on another `rwb_*` schema, and the legacy reads of `v_ace_account` and `v_ace_payment` are consumed on the owner's contract instead. DP-03 fixes the record element that is written before the row; DP-13 moves the base and nothing else; DP-19 is behind SCR-28 Proceeds matching, whose screen model is the edge contract's.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None, so the baseline builds against their fakes until those platform contract stories publish; the three consumed rows are class C dependencies in fact that the plan's C row does not carry, and they are built against their documents and fakes until their owners publish (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

**Build steps**

1. Write the two operations and validate the surface of AC1 in the pipeline.
2. Write the `Proceeds` element of AC2 from DF-FIN-001 to DF-FIN-009 and the applied-amount answer, with the placeholder on the fields the sources do not give.
3. Write `ProceedsPage` on the pagination convention and `MatchRequest` against the match the app story describes, with the placeholder on its unstated fields.
4. Publish the three lists as enumerations and add the vocabulary and no-order-default tests of AC3.
5. Write the AsyncAPI fragment and the `ProceedsMatched` schema of AC4 with the CloudEvents envelope and the no-personal-data rule.
6. Record the table baseline of AC5 and the versioned file naming, with the no-cross-schema-key test.
7. Record the error envelope, the rights and the `Idempotency-Key` rule of AC6.
8. Publish the six fakes of AC7 and the drift test.
9. Record the compatibility and boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the five contract tests pass, the six fakes answer every consumed path and the drift test is green, the event schema registers in BACKWARD mode, and the app story, SCR-28 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the `MatchRequest` is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the proceeds row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-P8-010-1 of the FSD | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and it is raised by the receipt read of the app story and not by this baseline.

### 15. Screens and states

The contract serves SCR-28 Proceeds matching in its loading, matched and unmatched states through the gateway-bff composite route (DP-19). The route calls rwb-payment for `GET /proceeds` and `POST /proceeds/{proceedsId}/match`, rwb-case for the case, its state and its balance and rwb-source-data for the receipt facts; this baseline fixes the rwb-payment answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and failure states the screen shows - refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001 - read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E4049-CON-01 | AC1, AC6 | Contract | The document validates; the two operations, the base, the query parameters, the answers, the errors, the `Idempotency-Key` rule and the rights are present, and no third operation and no monolith base is declared |
| TC-P8-E4049-CON-02 | AC2, AC3 | Contract | The `Proceeds`, `ProceedsPage` and `MatchRequest` elements validate against DF-FIN-001 to DF-FIN-009 and the three lists, the applied-amount answer is present, and no order, percentage or cap appears as a default or a constant |
| TC-P8-E4049-CON-03 | AC4 | Contract | The `ProceedsMatched` schema validates with the CloudEvents envelope, `ce_source` `/rwb-payment`, key `caseId`, the applied amount and no personal data; a removed field is refused in BACKWARD mode |
| TC-P8-E4049-CON-04 | AC5 | Contract | The `rwb_payment.proceeds` baseline declares DF-FIN-001 to DF-FIN-009 and the standard columns, no cross-schema key, no `v_ace_*` read, no balance table and no Schedule, and a forbidden element fails the absence test |
| TC-P8-E4049-CON-05 | AC6, AC7 | Contract | The six fakes answer every consumed path; a drifted fake fails the build; a repeated POST with the same `Idempotency-Key` returns the stored answer; an additive change passes and a removal is refused |

Legacy test cases TC-E4-049-01 to TC-E4-049-04 are owned by RWB-P8-E4049-APP. The five cases above are new contract cases; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the application order, the percentages, the caps, the amounts and the rule IDs stay data, reference data or the rule package, never a schema default, an example constant or an enumeration member of the code.
- No personal data in a schema, an example, an event payload or a fake: identifiers, amounts, dates, list values and a rule version only, and every example is synthetic.
- ACE data only through the owner's contract or a `v_ace_*` view the service holds: it holds none, so the document declares no ACE view and no ACE table and the receipt and the balance are consumed on rwb-source-data's contract (DP-05; Architecture v5 slide 29).
- The case and its balance stay with rwb-case, and the rule package with rwb-decision: the document declares no `recovery_case`, balance, `rule_row` or `rule_package_version` property and no write of their rows (DP-01).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-payment; a consumed operation is described as consumed and faked, never as provided (DP-11).
- No retired element is reintroduced: the absence test fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-PAY-10 | Every receipt is applied to the balance in the order the policy sets and the result is recorded with its rule version (FSD P8 A2.10 and AC-P8-010-01); the legacy story master carries no requirement id (GAP-2529; ASM-4182) | The two operations, the applied-amount answer, the `ProceedsMatched` schema and the record element | TC-P8-E4049-CON-01, TC-P8-E4049-CON-03 |
| BR-P8-010 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.10.3.1) | The three lists as published enumerations and the absence rule of any order or threshold in the schema | TC-P8-E4049-CON-02 |
| VR-P8-010-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.10.3.1) | The freshness row of the consumed receipt contract and the message of section 14 | TC-P8-E4049-CON-01 |
| ADR-014 | Schema and login per service | The `rwb_payment` table baseline and the no-cross-schema-key rule | TC-P8-E4049-CON-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `ProceedsMatched` schema with the CloudEvents envelope and the BACKWARD registry rule | TC-P8-E4049-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-P8-E4049-CON-01 |
| ADR-022 | Local decision record plus central ledger | The record element written before the row, through the library | TC-P8-E4049-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-049, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-P8-E4049-APP; this baseline copies none of them |
| Test cases | The five new contract cases TC-P8-E4049-CON-01 to -05; the four legacy cases belong to the app story |
| Feature and screens | FEAT-PAY-10 Apply proceeds to the case balance; SCR-28 Proceeds matching |
| Rules | The PAYMENT_MATCH package, named from the Temporal and Drools design and governed in rwb-decision, with no package code or rule ID fixed here; R-UNI-39 of the Business Rules and Routing Logic v4 behind the blocked action (GAP-2530; ASM-4183) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the application step of JOB-07, the evaluation of the order, the decision record, the proceeds row, the balance answer and the `ProceedsMatched` publication: RWB-P8-E4049-APP.
- The case of record, its route states, its balance and the move that follows an application: rwb-case (P3), whose read and answer this baseline declares as consumed and faked.
- The ACE receipt, account and batch-status facts and the freshness of the data product: rwb-source-data (P1).
- The PAYMENT_MATCH package, its application-order rule rows, its version and its approval: rwb-decision (P7).
- The settlement and the auction and enforcement arms of the match: RWB-P8-E4043-CON and RWB-P8-E4044-CON, which declare the same surface for their own slices.
- The posting of the applied amount to ALS and to the general ledger, the posting reference of DF-FIN-009 and the posting file: the posting stories of this service.
- The creation of the `proceeds` table and its migration: the DB story of this service, whose table this baseline declares.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
