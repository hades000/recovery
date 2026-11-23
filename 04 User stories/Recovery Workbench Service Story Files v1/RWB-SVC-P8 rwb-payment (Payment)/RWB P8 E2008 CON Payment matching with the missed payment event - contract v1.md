# RWB-P8-E2008-CON Payment matching with the missed payment event — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E2008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-005, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E2-008 for rwb-payment — the two REST operations on `/api/recovery/payment/v1`, the three event schemas on `rwb.payment.events.v1`, the consumed-contract declarations and their fakes, the error model, the message map and the `rwb_payment` schema baseline — is published as one frozen baseline so that RWB-P8-E2008-APP and RWB-P8-E2008-OPS start on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of the payment service (TechX)**, I want **one published baseline for rwb-payment payment matching — the shapes of the two operations, the three event schemas, the consumed contracts with their fakes, the error model and the `rwb_payment` schema with its versioning rule — so that** the application story, the deployment story and every consumer build on Day 1 against a fake and no shape is decided twice.

The baseline fixes, and nothing else:

- the two operations of the service's ownership rows — `GET /proceeds` and `POST /proceeds/{proceedsId}/match` — on base `/api/recovery/payment/v1`, with their access rights and idempotency (DP-13, R4);
- three event schemas on `rwb.payment.events.v1` with `.retry` and `.dlt`: `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.payment.ProceedsMatched.v1` (EV-25), in a CloudEvents 1.0 envelope keyed on `caseId` (DP-09);
- the declarations of the nine operations the service consumes — three ACE reads on rwb-source-data, two rwb-case reads, two treatment-record calls, the parameters and lists reads and the package read — with the element names of the review baseline and a fake per declaration (DP-05, DP-06, DP-07, DP-11);
- the `rwb_payment` baseline: `proceeds` with the field set of TSD P8 T3.1, the standard record columns, the keys, the library tables and the per-service Flyway rule (DP-01, DP-15);
- the error model and the message map of the legacy messages, so a consumer reads one envelope (DP-11);
- the event and operation contracts the gateway-bff composite route of SCR-28 consumes (DP-19).

This story writes no business logic. The behaviour of the match, the record, the events and the read is RWB-P8-E2008-APP; the deployment of the build is RWB-P8-E2008-OPS. Where a legacy shape has no target counterpart, the baseline states the placeholder and the gap, and no value is invented (GAP-2504; ASM-4143).

### 2. Business rationale

A split story is only as good as the contract it builds against. RWB-E2-008 was written as one service call to six in-process interfaces and to two ACE views, so nothing in the legacy story can be built by a team that does not own the neighbour. Under D-RCV-60 each of those calls becomes one hop with a 2 s timeout and a fake, and the shapes have to be frozen before the application and the deployment stories open — otherwise the four services this key touches would each freeze a different shape of the same payment.

- **one baseline, four consumers.** RWB-P8-E2008-APP, RWB-P8-E2008-OPS, RWB-P8-E2027 and the Epic 4 stories of the service all read these shapes; freezing them once is what makes the lane CG-W2 work.
- **the contract is testable without a neighbour.** Every declaration carries a fake with a documented answer, so a contract test proves the shape on Day 1 and SIT only replaces the fake with the owner.
- **nothing of the business is frozen here.** The window, the tolerance, the grace days and the match types stay rows of package `PAYMENT_MATCH`; the baseline carries their shape, never their value.

### 3. Preconditions

- The Ownership Map rows for this service are taken as authoritative: table `proceeds` (P8), operations `GET /proceeds` and `POST /proceeds/{proceedsId}/match` (P8), events EV-11, EV-12 and EV-25 (P8), jobs JOB-07 and JOB-08 (P8), no workflow name (P8). The context pack is the only source used for them.
- The API Specification, the Event and Messaging document and the Physical Schema are at their next versions and read as the parents of this baseline; the baseline restates only what this key touches.
- The platform contracts the patterns name — RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — are published at their baseline versions; this story freezes the shapes against them and does not restate them.
- The four P3 contracts the plan names — RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2004-CON and RWB-P3-E2042-CON — are readable as drafts, so their response elements are declared from the published documents and the fakes are built from those declarations.
- Status is Draft (realignment v1): no approval is required to publish a baseline, and a consumer builds against the tagged version (GAP-2504; ASM-4144).
- The legacy message IDs and their texts stand in the message map; no new message text is written here.

### 4. Flow

1. Take the two operations of the service's ownership rows, place them on base `/api/recovery/payment/v1`, and write the request, the response, the errors, the access right and the idempotency of each into 12.1.
2. Take the three events of the service's ownership rows, name them `rwb.payment.<Event>.v1`, place them on `rwb.payment.events.v1` with `.retry` and `.dlt`, fix the key and the CloudEvents envelope, and write the payload element names into 12.3.
3. Take the nine consumed operations, declare each with its base, its owner, its request and its response elements, and record the placeholder where no published document fixes an element (12.2).
4. Take the `proceeds` field set of TSD P8 T3.1, add the standard record columns of T3.0, and fix the business key, the indexes, the retention and the no-cross-schema-key rule in 12.7.
5. Add the library tables the patterns create in `rwb_payment` — `decision_record`, `inbox_event`, `outbox_event`, `idempotency_key` — as inherited shapes, not as new design.
6. Fix the error model: the platform problem shape, the codes for the legacy messages of section 14, and the rule that a refused right answers MSG-P4-002 and changes nothing.
7. Publish one fake per declaration and per provider, each with the documented answer of 12.8, so the contract tests run without a neighbour.
8. Freeze the baseline as version `v1`, tag it, and hand the tag to RWB-P8-E2008-APP and RWB-P8-E2008-OPS; any later shape change is a new version and is recorded in the Change Register.
9. Run the contract tests of section 16 against the OpenAPI document, the three event schemas and the fakes, and publish the result with the tag.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer sends a shape the baseline does not declare | The request is refused with the problem envelope and no business change | MSG-P4-002 or the field code of section 14 | AC5 |
| X2 | A declared operation has no published document behind it and the owner has not confirmed the element names | The declaration carries the placeholder and the fake answers the baseline shape; the review row is open | None | AC3, GAP-2504 |
| X3 | A breaking change is proposed after the tag | The change opens a new version of the baseline; the tagged version stays buildable | None | AC7 |
| X4 | A fake returns an answer the baseline does not document | The contract test fails and the baseline is not tagged | None | AC6 |
| X5 | A schema statement of the baseline names another `rwb_*` schema or a foreign key out of `rwb_payment` | The schema lint fails and the baseline is not tagged | None (lint log) | AC4, section 17 |
| X6 | A request carries no `Idempotency-Key` on the manual match, or replays one | The operation answers the stored result or refuses the replay as declared; no second row | None | AC1 |

X2 is the only path that ends in an open review row; the rest are gates of the tag. No path invents a business value: the values behind the shapes are package rows or reference data of their owners.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no running neighbour: every declaration has a fake and every shape comes from a published document or the Ownership Map |
| Negotiable | The element names of an unpublished consumed operation are the review baseline and may be corrected by the owner without a behaviour change |
| Valuable | Four stories and every consumer of the payment contract build on Day 1 against one tag |
| Estimable | Two operations, three event schemas, nine consumed declarations, one schema baseline, nine fakes and one message map |
| Small | Fits in one sprint with its contract tests |
| Testable | Every criterion runs as a contract test at Level Contract against the documents and the fakes |

### 7. Acceptance criteria

```gherkin
Feature: The rwb-payment contract baseline for payment matching

  Background:
    Given service "rwb-payment" with schema "rwb_payment", base "/api/recovery/payment/v1", topic "rwb.payment.events.v1" and task queue "rwb-payment"
    Given the Ownership Map rows of the service: table "proceeds", operations "GET /proceeds" and "POST /proceeds/{proceedsId}/match", events EV-11, EV-12 and EV-25, jobs JOB-07 and JOB-08

  Scenario: AC1 The two operations are published with their shape, right and idempotency (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads the OpenAPI document of the service
    Then "GET /proceeds" is declared with the query parameters matched, from, to, page and size and a page of receipts
    Then "POST /proceeds/{proceedsId}/match" is declared with body "MatchRequest", response "Proceeds" and an "Idempotency-Key" header
    Then "GET /proceeds" requires the Write-off and posting right R and "POST /proceeds/{proceedsId}/match" requires right U
    Then no operation is declared outside the base "/api/recovery/payment/v1"

  Scenario: AC2 The three event schemas are published with their envelope and key (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads the event schemas of the service
    Then "rwb.payment.TreatmentBooked.v1", "rwb.payment.PaymentMissed.v1" and "rwb.payment.ProceedsMatched.v1" are declared on topic "rwb.payment.events.v1"
    Then each schema carries a CloudEvents 1.0 envelope with the source of the service and the key of its declared field
    Then each schema declares no personal data field
    Then the retry topic "rwb.payment.events.v1.retry" and the dead-letter topic "rwb.payment.events.v1.dlt" are declared once

  Scenario: AC3 The nine consumed operations are declared with a fake each (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads section 12.2 and section 12.8 of the baseline
    Then each consumed operation names its base, its owner service and its request and response elements
    Then each consumed operation has one fake with a documented answer
    Then an operation whose path or elements no published document fixes carries the placeholder and one review row

  Scenario: AC4 The rwb_payment baseline is published with its versioning rule (new, D-RCV-60)
    Given the baseline document version "v1"
    When the schema statement is read and linted
    Then "proceeds" is declared with DF-FIN-001 to DF-FIN-009 and the standard record columns of TSD P8 T3.0
    Then the business key, the indexes and the retention of "proceeds" are declared
    Then no foreign key leaves "rwb_payment" and no statement names another "rwb_*" schema
    Then the per-service Flyway sequence, its numbering and its drift gate are declared once

  Scenario: AC5 The error model and the message map are published (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads the error model and section 14
    Then the problem envelope is declared once with its fields and its trace identifier
    Then each legacy message ID of the key maps to one HTTP status and one envelope code
    Then a request without the declared right answers MSG-P4-002 and changes nothing

  Scenario: AC6 Every fake reproduces its documented answer and no business value is frozen (new, D-RCV-60)
    Given the baseline document version "v1"
    When the contract tests run at Level Contract
    Then each fake returns the answer documented in section 12.8 for its declared scenario
    Then no window, tolerance, grace day, partial floor or match type appears as a value in a schema, a fake or a test
    Then every such value is read from package "PAYMENT_MATCH" or from the reference-data contract

  Scenario: AC7 A breaking change opens a new version and the tag stays buildable (new, D-RCV-60)
    Given the baseline is tagged "v1"
    When a consumer proposes a change to a published element
    Then the change is published as "v2" with its own document and fake
    Then the tag "v1" remains readable and the stories that cite it still build
    Then the change is recorded in the Change Register
```

The seven criteria test the baseline only. They carry no payment, plan, case, amount or date of the legacy story except the operation, event and field names the Ownership Map and TSD P8 fix; the values behind the shapes stay rows of package `PAYMENT_MATCH` and of the reference-data contract (ASM-4144).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The baseline is one tagged version; a consumer builds against the tag and never against a draft element | R8.2; R5.7 rule 1 |
| BR2 | The operation set is the ownership rows of the service and nothing else; an operation the Ownership Map does not carry is not published | Ownership Map; GAP-2504 |
| BR3 | One base per service, `/api/recovery/payment/v1`, and no operation outside it | DP-13, R4 |
| BR4 | Event names follow `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, with a retry and a dead-letter topic | DP-09, DP-14 |
| BR5 | One schema and one login per service; no foreign key and no statement may leave `rwb_payment` | DP-01, DP-02 |
| BR6 | Every consumed operation is declared with a fake; a declaration without a fake is not publishable | DP-11 |
| BR7 | No business value is frozen: window, tolerance, grace days, partial floor, match types and the LOV values are read from their owners | Principle 1; D-RCV-36 T10 |
| BR8 | No personal data in a schema, an event, a fake or a test fixture | Section 17 |
| BR9 | The error envelope is the platform problem shape and every legacy message ID maps to one status and one code | R7.2 s14; section 14 |
| BR10 | A breaking change is a new version and a Change Register row; a correction of an element name by its owner is a patch to the same version | R8.2; AC7 |

### 9. State transitions

None of business data: this story changes no record. The states it owns are the states of the baseline itself.

| From | Event | Condition | To |
|---|---|---|---|
| Not existing | The baseline is written and its tests pass | The tag gate of section 16 is green | `v1` Draft, tagged and handed to the consumers |
| `v1` Draft | The owner confirms or corrects an element name of a consumed operation | The change is not breaking | `v1` patched, the review row closed |
| `v1` | A published element changes shape | A consumer cannot build against the old shape | `v2` opened; `v1` stays readable and buildable |
| `v1` | A consumer asks for an operation the Ownership Map does not carry | The row is absent | No change; the request answers the gap row |

The version states are `Draft`, `Tagged` and `Superseded`, and only a tagged version is citable by an APP or OPS story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract owner of rwb-payment (TechX) | Writes, tags and versions the baseline; owns the fakes and the contract tests; refuses a declaration without a published document |
| The owner of rwb-source-data (P1) | Confirms or corrects the three declarations and their fakes; owns the ACE read boundary |
| The owner of rwb-case (P3) | Confirms or corrects the open-case, plans, parameters, lists and package declarations and their fakes |
| The owner of rwb-treatment (S2) | Confirms the treatment entity behind RWB-P3-E2004-CON and its two declarations |
| The owner of rwb-decision (P7) | Confirms the package declaration and the shared topic `rwb.decision-record.v1` |
| The platform contract owners (PLT) | Own the library shapes the baseline inherits: the record, the outbox and inbox, the workflow kit, the Flyway gate and the composite route |
| RW-CREDITAD, RW-CASEOWN, SY-AGENT, RW-COE | Read the baseline as consumers; hold no write right on it |

The right of each published operation is the row of TSD P8 T6.1; the baseline declares it and grants nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Declared as |
|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | `proceeds` (P8) | id, case_id, treatment_id, account_payment_id, source, amount, received_date, matched_to, posting_ref | Required, optional and nullable per TSD P8 T3.1; `source` from LOV-PROCEEDS-SRC and `matched_to` from LOV-MATCH |
| DF-ACE-043 to DF-ACE-046, DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, data_as_of | Response elements of the payments declaration |
| DF-ACE-028 | `v_ace_account` (P1) | next_installment_date | Response element of the next-installment declaration |
| DF-ACE-178, DF-ACE-179, DF-ACE-182 | `v_ace_batch_status` (P1) | source_system, business_date, status | Response elements of the batch-status declaration |
| DF-CAS-025, DF-CAS-026 | `case_account` (P3) | case_id, account_key | Response elements of the open-case declaration |
| DF-TRT-001, DF-TRT-004, DF-TRT-009, DF-TRT-031, DF-TRT-032 | treatment record (contract RWB-P3-E2004-CON) | id, treatment_type, installments, installment_amount, installments_paid | Declared on the treatment contract; the plan scopes the owner as P3 while the entity is S2's |
| DF-REF-002, DF-REF-003, DF-REF-296, DF-REF-297, DF-REF-298 | `rule_row` (P7) | rule_id, rule_version, package_version_id, drools_rule_name, outputs | Read-only elements of the evaluation result; no `drl_source` and no workbook |
| DF-DEC-004, DF-DEC-005 | decision record (PLT library) | rule_id, rule_version | Inherited library shape |
| DF-OPS-118 to DF-OPS-129 | reconciliation result (REC-04) | all fields | Declared in the run summary shape of the workflow kit |

The `payment_code` of the legacy story has no column in the TSD field set, which carries `account_payment_id` (DF-FIN-004): where the payment code lives and how it is keyed is Not specified in the source documents (GAP-2504; ASM-4143). The field list of an event payload is the legacy list of section 12.3 extended by the envelope fields, and no other element is added here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13); document `openapi/rwb-payment-v1.yaml`.

| Method | Path | Request | Response | Errors | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/proceeds` | query `matched` (boolean), `from`, `to`, `page`, `size` | 200 `ProceedsPage` with `items` of `Proceeds`, `page`, `size`, `total` | 401, 403 (MSG-P4-002), 503 | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | path `proceedsId`; body `MatchRequest` with the case and the account to match | 200 `Proceeds` | 401, 403, 404, 409, 422, 503 | Write-off and posting, right U, scope applied | `Idempotency-Key` header, replayed answer on a repeat |

`Proceeds` carries DF-FIN-001 to DF-FIN-009, and `MatchRequest` carries the case and account reference of a manual match. Architecture v5 lists `GET /cases/{id}/payments` among the IN operations of this service and the Ownership Map has no row for it: the operation is not published, the case payment list is answered through `GET /proceeds` with the case scope applied, and the absence is recorded (GAP-2504; ASM-4143).

#### 12.2 REST operations consumed

| Operation | Base | Owner | Request | Response elements |
|---|---|---|---|---|
| Payments of a business date (name Not specified in the source documents (GAP-2504; ASM-4143)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | source, businessDate | payment_code, account_key, payment_date, payment_amount, data_as_of |
| Next installment date of an account (name as above) | `/api/recovery/source-data/v1` | P1 rwb-source-data | accountKey, businessDate | next_installment_date |
| Batch status of a source (name as above) | `/api/recovery/source-data/v1` | P1 rwb-source-data | source, businessDate | source_system, business_date, status |
| Open case of an account (name as above) | `/api/recovery/case/v1` | P3 rwb-case | accountKey | caseId, absent where the account is on no open case |
| Running plans of a case (name as above) | RWB-P3-E2004-CON | P3 as the plan scopes it; the entity is S2's | caseId | treatmentId, treatment_type, installments, installment_amount, installments_paid, nextDueDate |
| Record an installment paid (name as above) | RWB-P3-E2004-CON | as above | treatmentId, proceedsId, dueDate, amount | the updated installment position |
| Run parameters (name as above) | RWB-P3-E1042-CON | P3 rwb-case | key, businessDate | value, version |
| Lists of the run (name as above) | RWB-P3-E1043-CON | P3 rwb-case | listCode, businessDate | the active values of LOV-MATCH and LOV-PROCEEDS-SRC |
| Rule package in force (name as above) | RWB-P3-E2042-CON | P3 as the plan scopes it; the package is P7's | packageCode, onDate | package code, version, rows, checksum |

Every row is one hop with a 2 s timeout, a single GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The element names are the review baseline: each owner confirms or corrects them at review, and a correction is a patch to the same version.

#### 12.3 Events published

| Event | Topic | Key | Payload elements | Producer |
|---|---|---|---|---|
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | `caseId` | treatmentId, caseId, bookingRef, businessDate | rwb-payment, booking story (JOB-08) |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | `caseId` | treatmentId, dueDate, amountDue | rwb-payment, this key |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | `caseId` | proceedsId, caseId, amount | rwb-payment, this key |

Each schema is CloudEvents 1.0 with `id`, `source`, `type`, `subject`, `time` and `datacontenttype`, is registered on the topic with its subject and version, and carries no personal data. The retry topic `rwb.payment.events.v1.retry` and the dead-letter topic `rwb.payment.events.v1.dlt` are declared once for all three. `DecisionRecorded` is published by the local library on the shared topic `rwb.decision-record.v1`, whose owner is rwb-decision (DP-03), and its schema is inherited and not restated. The element lists beyond the legacy ones — the matched treatment and the business date of a match, and the case id of a missed payment — are Not specified in the source documents (GAP-2504; ASM-4143).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Envelope rule | Declaration |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.ace-data-ready.v1` | dedupe on the event id in `inbox_event`; no order assumed | source, businessDate, batchStatus |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.rule-package.v1` | dedupe on the checksum | packageCode, version, checksum |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | `rwb-payment.treatment-approved.v1` | dedupe on the event id | treatmentId, caseId, approvedDate |
| `rwb.debtsale.LotAwarded.v1` (EV-23) | `rwb.debtsale.events.v1` | `rwb-payment.lot-awarded.v1` | dedupe on the event id | lotId, caseIds, buyerRef |
| `rwb.asset.AssetTakenOn.v1` (EV-22) | `rwb.asset.events.v1` | `rwb-payment.asset-taken-on.v1` | dedupe on the event id | assetId, caseId |
| `rwb.asset.AssetSold.v1` | `rwb.asset.events.v1` | `rwb-payment.asset-sold.v1` | dedupe on the event id | assetId, caseId, salePrice |
| `rwb.writeoff.WriteOffApproved.v1` (EV-24) | `rwb.writeoff.events.v1` | `rwb-payment.write-off-approved.v1` | dedupe on the event id | writeOffId, caseId |

The seven rows are the service's subscriptions: EV-26 and EV-30 serve this key, and the other five serve the booking and Epic 4 stories. This story declares the consumer groups and the envelope rules once so that no later story invents a second group name. The subscriptions this key uses are EV-26 only.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `matchPayments` (JOB-07; name Not specified in the source documents (GAP-2504; ASM-4143)) | Workflow, event-started | `rwb-payment`, namespace `rwb-recovery` | input source, businessDate, eventId; execution id derived from source and date |
| `readFacts`, `evaluateMatch`, `recordAndApply`, `raiseMissedPayment` | Activities | `rwb-payment` | the input and output element names of 13; `NoPackageInForce` non-retryable |
| `confirmBookings` (JOB-08; name as above) | Workflow, event-started | `rwb-payment` | the booking story of the service |

The baseline fixes the registration contract — the queue, the namespace, the workflow type name, the input schema and the retry policy of the kit — and not the activity names a story chooses. `postProceeds`, the debt-sale saga step, is registered by that journey and not here.

#### 12.6 Schedules

None. No job of this key is a Temporal Schedule: JOB-07 and JOB-08 are event-started, and the daily cadence is the bank's Airflow edge. The baseline therefore declares no cron, no overlap policy and no catch-up window, and no Schedule row is created for this service.

#### 12.7 Tables owned

| Table | Owner | Key and indexes | Columns | Note |
|---|---|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | `id` primary key; business key on the payment reference where the environment grants it; index on (`matched_to`, `received_date`) | DF-FIN-001 to DF-FIN-009 plus the standard record columns of TSD P8 T3.0 | the receipt of a case and what it was matched to |
| `decision_record` | PLT library, created in `rwb_payment` | hash chain per record kind | inherited | DP-03 |
| `inbox_event` | PLT library, created in `rwb_payment` | (`consumer_group`, `event_id`) | inherited | DP-09 |
| `outbox_event` | PLT library, created in `rwb_payment` | (`status`, `created_at`) and the relay cursor | inherited | DP-09 |
| `idempotency_key` | PLT library, created in `rwb_payment` | (`scope`, `key`) | inherited | DP-09 |

The baseline declares no foreign key out of `rwb_payment`, no grant on another schema and no read of another owner's table; `case_id`, `treatment_id` and `account_payment_id` are identifiers (DP-01). The migration rule is one Flyway sequence per service, numbered in `rwb_payment` and gated by the lint and drift gate of RWB-PLT-E1044-CON (DP-15); the monolith's `V2_008__payment_matching.sql` is not reused and its target name is Not specified in the source documents (GAP-2504; ASM-4143). `payment_missed_event_key` is not created: the key is the idempotency row.

#### 12.8 Contract fakes

| Fake | Provider | Documented answer | Consumers |
|---|---|---|---|
| Payment OpenAPI fake | rwb-payment | a page of matched and unmatched receipts; a manual match accepted, refused with MSG-P4-002 and refused on a replayed key | APP, OPS, gateway-bff |
| Event schema fakes | rwb-payment | one valid `TreatmentBooked`, one `PaymentMissed` and one `ProceedsMatched` sample per schema, and one schema-invalid sample | APP, OPS, the three consumers |
| rwb-source-data fake | P1 | the payments, the next installment date and a COMPLETE, a FAILED and an absent batch status for the synthetic business dates | APP, OPS |
| rwb-case fake | P3 | the open case, the running plans and the absence of a case for a synthetic account | APP |
| Treatment-record fake | S2 as the plan scopes it | the running plan position and the answer of a recorded installment | APP |
| rwb-decision package fake | P7 | `PAYMENT_MATCH` with one version in force, a second version and no version in force | APP |
| Parameters and lists fake | P3 | one key with its version and the two LOV sets | APP |
| Library fakes | PLT | the record chain healthy and stopped, the outbox and inbox writers, the workflow kit with a deterministic clock | APP, OPS |
| gateway-bff route fake | PLT edge | the merged SCR-28 answer with the payment read once | APP, OPS |

Each fake is generated from its document under `contracts/fakes/`, is versioned with the baseline and is replaced by the owner in SIT without a change to a consumer.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 9 consumed | the two operations on `/api/recovery/payment/v1`; three rwb-source-data reads, two rwb-case reads, two treatment-record calls, the parameters and lists reads and the package read; one hop, 2 s |
| Kafka | 3 published, 7 subscribed | three schemas on `rwb.payment.events.v1` with retry and DLT; EV-26 and EV-30 for this key, EV-10, EV-22, EV-23, EV-24 and `AssetSold` for the other stories |
| Temporal | 2 workflows registered, 4 activities | `matchPayments` and `confirmBookings` on `rwb-payment`; no Schedule |
| File | None | no file shape is published by this key |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `contract`; artefacts under `contracts/rwb-payment/`: `openapi-v1.yaml`, `events/*.avsc`, `fakes/*.json`, `schema/rwb_payment.sql`, `messages.yaml`.

| Component | Type | Responsibility |
|---|---|---|
| `openapi-v1.yaml` | Document | the two operations, their parameters, their bodies, their errors and their examples |
| `events/*.avsc` | Document | the three event schemas and their envelope rules |
| `consumed.yaml` | Document | the nine declarations with their owners and their review state |
| `schema/rwb_payment.sql` | Document | the baseline of 12.7 with its keys, its retention and its no-cross-schema rule |
| `messages.yaml` | Document | the message map of section 14 |
| `fakes/` | Generator | one fake per declaration, generated from the document and versioned with it |
| `ContractTag` | Build step | tags the baseline and publishes the tag to the two consumer stories |

**Build steps.** (1) Write the OpenAPI document and lint it; test AC1 and AC5. (2) Write the three event schemas and validate the samples; test AC2. (3) Write the nine declarations and generate the fakes; test AC3. (4) Write the schema baseline and pass the schema lint; test AC4. (5) Run the nine contract tests, tag `v1` and publish the tag; test AC6 and AC7.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` | owner's schema `rwb_payment`; no foreign key leaves it | none |
| DP-03 | DecisionLogWriter | local record library and `rwb.decision-record.v1`, inherited shape | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | embedded kit; the package read from its owner | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*` | the three ACE reads declared on rwb-source-data's contract or the granted views | none |
| DP-06 | Parameters | the parameters contract declared | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | the two lists declared | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, outbox | three schemas, the outbox and inbox writers, the retry and DLT topics | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | the registration contract of the event-started workflow | H RWB-PLT-E1071-CON |
| DP-11 | In-process call | one hop, 2 s, a fake per declaration | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/payment/v1` | none |
| DP-15 | V0001 baseline | one Flyway sequence per service | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | the composite route the read is served through | H RWB-PLT-N001-CON |

### 14. Validation and messages

| ID | When | Status and code |
|---|---|---|
| MSG-P8-001 | A run summary carries unmatched payments | 200 with the summary text; no error code |
| MSG-P8-002 | No `PAYMENT_MATCH` version is in force | 409 on a manual match; the run alert text for the workflow |
| MSG-P3-027 | The rule version is refused | 422 with the detail of the refused package and date only |
| MSG-P1-001 | The ACE batch is late or not complete | 503 on a read of stale data; the text carries the product and the date |
| MSG-P4-002 | The role lacks the right | 403 on both operations; nothing changes |

The envelope of every error is the platform problem shape — `type`, `title`, `status`, `detail`, `instance` and `traceId` — and carries no personal data. The five texts are the legacy texts of RWB-E2-008 section 14 and are copied into the message map unchanged.

### 15. Screens and states

SCR-28 Proceeds matching is the only screen this key serves. The baseline declares the read that fills it — `GET /proceeds` filtered by matched or unmatched — and the composite route the screen calls through the gateway-bff (DP-19). SCR-14, SCR-04 and SCR-44 are served by other services and read this service only through the same operations.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E2008-CON-01 | AC1 | Contract | the OpenAPI document read against the ownership row of each operation |
| TC-P8-E2008-CON-02 | AC1, AC5 | Contract | a request without the declared right and a request with an undeclared field |
| TC-P8-E2008-CON-03 | AC2 | Contract | one valid and one invalid sample of each of the three schemas |
| TC-P8-E2008-CON-04 | AC3, AC6 | Contract | the nine declarations and their generated fakes |
| TC-P8-E2008-CON-05 | AC4 | Contract | the schema statement linted for keys, indexes and cross-schema names |
| TC-P8-E2008-CON-06 | AC5 | Contract | each of the five messages mapped to its status and code |
| TC-P8-E2008-CON-07 | AC6, AC7 | Contract | the tag `v1`, a proposed breaking change and the tag `v2` |
| TC-P8-E2008-CON-08 | AC1 | Contract | an `Idempotency-Key` replay of a manual match |

The eight are new with D-RCV-60 and test the baseline only. Integration copies end in `-ITG` and belong to RWB-ITG-E2008-ITG; the legacy test cases of RWB-E2-008 stay with the criteria the APP story owns.

### 17. Guardrails

- No business value in a document, a schema, a fake or a test: the window, the tolerance, the grace days, the partial floor, the match types and the LOV values are rows of their owners and appear here only as element names.
- No personal data in a schema, an event, a fixture or a log: a payment is identified by its payment reference and its account key, and an account number is never an element.
- No statement leaves `rwb_payment`: no foreign key, no cross-schema `select` and no name of another service's table in the baseline.
- No declaration without a fake, no fake without a documented answer, and no tag without the contract tests.
- The five message texts are copied, never reworded; a new text needs its owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-P8-E2008-CON-03, TC-P8-E2008-CON-04 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-P8-E2008-CON-01, TC-P8-E2008-CON-05, TC-P8-E2008-CON-08 |

The baseline is cited by RWB-P8-E2008-APP, RWB-P8-E2008-OPS, RWB-P8-E2027 and the Epic 4 stories of the service; each citation names the tag `v1`.

### 19. Out of scope

- The behaviour of the match, the record, the events and the read (RWB-P8-E2008-APP).
- The deployment, the topics, the worker pool, the alerts and the runbook (RWB-P8-E2008-OPS).
- The reference-data and rule-authoring behaviour of RWB-E2-027 (RWB-P8-E2027) and of the package stories of rwb-decision.
- The manual, settlement and enforcement matching of Epic 4 and their posting files.
- The platform shapes this baseline inherits — the record library, the outbox and inbox, the workflow kit, the Flyway gate and the composite route — which are owned by their PLT stories.
