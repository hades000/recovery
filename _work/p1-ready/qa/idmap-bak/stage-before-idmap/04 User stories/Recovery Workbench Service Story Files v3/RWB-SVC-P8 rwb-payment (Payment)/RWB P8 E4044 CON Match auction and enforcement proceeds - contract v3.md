# RWB-P8-E4044-CON Match auction and enforcement proceeds

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-061, RD-P1-066: Declare the shared ACE event subscription and the source-data payment and batch-status reads.
- EV-26 is cited with its published record key and payload, and the start rule is `source_system` ALS with status COMPLETED (RD-P1-003, RD-P1-040).


| Item | Value |
|---|---|
| Story key | RWB-P8-E4044-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-044 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P8-E4044-CON-16); the squad sizes it at refinement |
| Contract version | v1 (the /v1 base paths in section 1 and the .v1 event names in section 12.3) ; consumes rwb-source-data.yaml 5.1.0 and the P1 AsyncAPI |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-061, RD-P1-066 |
| Depends on (build) | None |
| Contract dependencies | rwb-source-data payment data product; rwb-case reference-data and case-state reads; rwb-decision rule package (payment match rules read as governed rule rows; payment_match_rule is not declared as a table of this service); rwb-integration posting file (class C) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Requirement trace | FEAT-PAY-04, VR-P8-004-1 and BR-P8-004 (placeholder until a requirement id is allocated, GAP-1375) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **TechX contract owner of rwb-payment**, I want **the contract of the proceeds match published before the build starts**, so that **the application story, the case router and the reporting read model can be built against one stable shape**.

This baseline publishes, for legacy RWB-E4-044 (FEAT-PAY-04):

- the two operations of the proceeds match on base `/api/recovery/payment/v1`: `GET /proceeds` (API-P8-001) and `POST /proceeds/{proceedsId}/match` (API-P8-002), with their shapes, rights, errors and idempotency rule;
- the `proceeds` element list of TSD P8 T3.1 (DF-FIN-001 to DF-FIN-009) and its two lists of values, `LOV-MATCH` and `LOV-PROCEEDS-SRC`;
- the three event schemas of the service on `rwb.payment.events.v1` — `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) — with the CloudEvents envelope, the retry and `.dlt` topics and the case key;
- the consumed rows of the slice — the rwb-case case read, the rwb-decision rule-package read and the ACE batch status of source ALS — and one fake for each;
- the JOB-07 workflow and its matching activity as a contract element, with their input and output and no Schedule;
- the table baseline of `rwb_payment` and the call-type summary of the slice.

It does not own the behaviour behind the operations, which is RWB-P8-E4044-APP, and it publishes no shape of another service: the case, the treatment, the asset, the lot, the write-off, the rule rows and the ledger stay with their owners (P3, S2, S5, S6, S7, P7).

### 2. Business rationale

A contract story is what lets two teams build at once. The application story of this key cannot write a row that the case router, the reporting read model and the reconciliation job will read unless the row, the event and the operation are fixed first, and the wave 3 harness cannot fake what is not published. The legacy key had no published contract at all: the endpoints were module endpoints of one monolith, the events were in-process, and the match rules were read from module tables.

The realignment changes exactly that boundary. The service owns `rwb_payment` and `rwb.payment.events.v1`, publishes its two operations on its own base, and consumes the other owners' facts on their contracts (DP-01, DP-05, DP-13, DP-14). This baseline is the piece of that change that can be tagged on Day 1, before any behaviour is built, which is why it carries every shape the other stories need and no behaviour of its own.

### 3. Preconditions

- The template and naming rules of the run are in force, and the service row of the context pack fixes the base, the topic, the queue and the schema (Template and Rules §R4).
- TSD P8 T3.1, T3.2, T-A.1 and T-A.2 are readable; they are the source of every element and every operation of this baseline.
- The event rows EV-11, EV-12 and EV-25 of the Event and Messaging Design v5 are readable, and so is EV-26 for the trigger.
- The platform libraries of DP-03 and DP-19 exist as contracts: RWB-PLT-E1027-CON for the local decision record and RWB-PLT-N001-CON for the composite route; this CON story holds no H row to them, but their shapes are referenced and not redefined.
- The two consumed operation names that no source publishes are carried as placeholders, and their fakes are built from the documents (GAP-2518; ASM-4168).

### 4. Flow

1. The baseline is written from the module documents: the two operations, the `proceeds` elements and the two lists from TSD P8; the three events from the Event and Messaging Design; the trigger from EV-26 and the ACE batch-status contract fake in §12.8.
2. Each element is checked against its owner: no element of the case, the treatment, the asset, the lot, the write-off or the rule rows is declared, and each of those is referenced by identifier only. No column is added to legal_action; the round result, the percentage of official value and the proceeds source code are facts of the RWB-P8-E4044-CON answer only, and the operation names and element keys that no source gives carry the placeholder Not specified in the source documents (GAP-1896).
3. The two consumed rows are written with the placeholder where no name is published, and one fake is written for each row from the document.
4. The document is published as OpenAPI 3.1 for the two operations and AsyncAPI for the three events, with `additionalProperties: false` on the closed objects. Each of the three event payloads carries the CloudEvents 1.0 envelope with its event id and the case key caseId; each further element is the placeholder Not specified in the source documents (GAP-1376) until the event owner publishes the AsyncAPI document.
5. The compatibility check runs on the previous tag, the new draft and a corpus of recorded fake answers; a removal, a rename, a type change or a new required element fails it.
6. The application story builds against the tag; the wave 3 harness builds its fakes from it; the case router consumes the published event shape.
7. A change after the tag is a new minor version under BACKWARD compatibility, or a new major version when the check fails.

### 5. Exception paths

| Condition | What happens | Reference | Covered by |
|---|---|---|---|
| An element of another owner is declared in the schema | The review refuses the document; the element is referenced by identifier instead | DP-01 | AC3 |
| A business value appears as a default, a constant or an example | The review refuses the document; the value stays a rule row or a reference-data row | BR-P8-004 | AC3 |
| The match package read has no published operation name | The row carries the placeholder and the fake is built from the document | GAP-2518; ASM-4168 | AC5 |
| A consumed contract is not yet built | The fake is published first; no build waits for another service | ADR-020 | AC5 |
| The compatibility check fails on a removal or a type change | A new major version is required, and the consumers are told | AC7 | Not specified in the source documents (DOR-RWB-P8-E4044-CON-3) |
| The `Idempotency-Key` rule is declared twice, in the document and in the service | The platform library owns the rule; the document cites it | DP-09 | AC2 |
| A second topic, base, queue or schema name appears | The review refuses the document | DP-13, DP-14 | AC7 |

### 6. INVEST check

| Letter | Result |
|---|---|
| Independent | Yes. It has no build dependency, and it references the two platform contracts without needing them tagged. |
| Negotiable | The element names of the consumed operations are open until their owners publish them; every documented element is fixed. |
| Valuable | Yes. Three other stories and the wave 3 harness can start on Day 1. |
| Estimable | Yes. Two operations, one schema, three events, three consumed rows, one table. |
| Small | Yes. It is a document and its examples, with no behaviour and no migration. |
| Testable | Yes. Seven criteria, all contract level, all decided by schema validation and the compatibility check. |

### 7. Acceptance criteria

```gherkin
Feature: Match auction and enforcement proceeds — contract

  Scenario: AC1 The two proceeds operations are published on the service base (new, D-RCV-60)
    Given the OpenAPI document of rwb-payment
    When the proceeds paths are read
    Then GET /api/recovery/payment/v1/proceeds returns a ProceedsPage filtered by matched, from, to, page and size (API-P8-001)
    And POST /api/recovery/payment/v1/proceeds/{proceedsId}/match takes a MatchRequest and returns a Proceeds (API-P8-002)
    And no other base and no other path of the proceeds match is declared

  Scenario: AC2 The right and the idempotency rule are fixed (new, D-RCV-60)
    Given the two proceeds operations
    When their access and idempotency are read
    Then both declare the capability area Write-off and posting with R for the read and U for the match, and the caller's scope applied
    And the match requires an Idempotency-Key header and stores its answer, and a repeat with the same key returns the stored answer
    And the access check of both operations is the rwb-access authorise call (DP-08)

  Scenario: AC3 The proceeds schema and its lists are published (new, D-RCV-60)
    Given the Proceeds, ProceedsPage and MatchRequest schemas
    When their properties are read
    Then Proceeds carries DF-FIN-001 to DF-FIN-009, with source from LOV-PROCEEDS-SRC and matched_to from LOV-MATCH
    And the closed objects declare additionalProperties false and carry the seven standard record columns
    And no tolerance, window, grace, priority or rule ID appears as a default or an enumeration member

  Scenario: AC4 The three event schemas are published on the service topic (new, D-RCV-60)
    Given the AsyncAPI document of rwb-payment
    When the channel is read
    Then TreatmentBooked, PaymentMissed and ProceedsMatched are declared on rwb.payment.events.v1 with its retry and .dlt topics
    And each uses the CloudEvents 1.0 envelope, the case as its key, and the payload of its EV row with no personal data

  Scenario: AC5 The consumed rows and their fakes are declared (new, D-RCV-60)
    Given the consumed rows of this slice
    When they are read
    Then the rwb-case case read, the rwb-decision rule-package read and the ACE batch status of source ALS are declared as consumed with a one-hop, 2 s contract
    And one fake is declared per row, and a name that no source publishes carries the placeholder

  Scenario: AC6 The error set is one problem document (new, D-RCV-60)
    Given the two proceeds operations
    When their answers are read
    Then 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 are declared
    And each answer is one problem document with a code, a message ID and a correlation reference

  Scenario: AC7 The slice declares one base, one topic, one queue and no Schedule (new, D-RCV-60)
    Given the document as a whole
    When the call types are summarised
    Then it names REST, Kafka and Temporal only, with two provided and four consumed REST rows, three published events, one consumed event on the shared source-data group and no Schedule
    And it declares no Schedule, no Quartz row, no foreign table and no second topic or base

  Scenario: AC8 A duplicate delivery of a consumed event is applied once (new, D-RCV-60)
    Given a consumed event of this slice is delivered again with the same identifier
    When the repeat is processed
    Then its effect is applied once and the repeat leaves no second record

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the model does not allow
    When the change is requested
    Then the change is refused and no status is written
```

### 8. Business rules

| ID | Rule | Effect on the contract |
|---|---|---|
| BR-P8-004 | No value a business person may change is written in code; it is read from reference data or the rule package with its version | No threshold, amount, percentage or rule ID becomes a schema default, a constant or an enumeration member |
| VR-P8-004-1 | A stale data product is declared with its date | The stale answer is a documented error, MSG-P1-001, not a silent partial page |
| R-UNI-39 | No action proceeds unlogged | The 503 answer of the match covers the decision library being unavailable |
| R-UNI-40 | A duplicate is ignored and counted | The inbox and idempotency objects are cited, not redefined |
| DP-13, DP-14 | One base and one topic per service | `/api/recovery/payment/v1` and `rwb.payment.events.v1` only |
| DP-01 | No service reads another's tables | Every foreign fact is a reference or a consumed contract |

### 9. State transitions

| From | Trigger | To | Where it is fixed |
|---|---|---|---|
| Draft contract | The internal review of the two operations passes | Tagged minor version | AC1, AC6 |
| Tagged contract | An additive change inside BACKWARD compatibility | Next minor version | AC7 |
| Tagged contract | A removal, a rename or a type change | New major version, consumers notified | AC7 |
| Tagged contract | A consumed owner publishes the operation name that was a placeholder | The placeholder is replaced; no behaviour changes | GAP-2518 |

The contract has no runtime state. The lifecycle of a `proceeds` row itself is RWB-P8-E4044-APP's section 9 and is not restated here.

### 10. Authority

| Artefact | Who approves it |
|---|---|
| The two operations, their errors and their idempotency rule | The solution architect of P8 and the service owner of rwb-payment |
| The three event schemas | The event platform owner (RWB-PLT-EVT) and the consumers' owners: rwb-case for `ProceedsMatched` and `PaymentMissed`, rwb-case for `TreatmentBooked` |
| The `proceeds` element list and the two lists of values | The data owner of `rwb_payment` and the reference-data owner of rwb-case (P3) |
| The consumed rows and the fakes | The owner of each consumed contract: rwb-case (P3), rwb-decision (P7) and rwb-source-data (P1) |
| The table baseline | The ACE DB owner (RWB-PLT-DB) |

No name of a person appears in this document; the approval is by role, and the tag waits for every role above.

### 11. Data

| Element | Type | Required | Source | Field ID |
|---|---|---|---|---|
| `id` | uuid | Yes | Workbench | DF-FIN-001 |
| `case_id` | uuid | Yes | rwb-case reference | DF-FIN-002 |
| `treatment_id` | uuid | No | rwb-treatment reference | DF-FIN-003 |
| `account_payment_id` | uuid | No | ACE payment reference | DF-FIN-004 |
| `source` | `LOV-PROCEEDS-SRC` | Yes | Workbench | DF-FIN-005 |
| `amount` | numeric(18,2) | Yes | ACE payment fact | DF-FIN-006 |
| `received_date` | date | Yes | ACE payment fact | DF-FIN-007 |
| `matched_to` | `LOV-MATCH` | Yes | Workbench | DF-FIN-008 |
| `posting_ref` | varchar(40) | No | ACE payment fact | DF-FIN-009 |

Lists: `LOV-MATCH` = INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED; `LOV-PROCEEDS-SRC` = CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR (TSD P8 T3.2). The schema also carries `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by` (TSD P8 T3.0). The relationship of `account_payment_id` to an `account_payment` object is declared in TSD P8 T3.3 but no owner of that object appears in the ownership map, so the element is published as a reference to the ACE payment code and nothing else (GAP-2521; ASM-4171).

Reference data: the parameters this slice reads are the two lists above and the rule-package version, read on the reference-data contract of rwb-case (DP-06, DP-07) and the rule package of rwb-decision; no value is written in code (BR-P8-004).

MatchRequest: the request carries case_id (DF-FIN-002) as the case reference and matched_to (DF-FIN-008) with a value of LOV-MATCH, plus the Idempotency-Key header (AC2); every further element is Not specified in the source documents (GAP-1371).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, query `matched`, `from`, `to`, `page`, `size` (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out, status 200 (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored and returned on a repeat; a second key on an already matched receipt answers 409 |

The error envelope of the two operations is one problem document with a code, a message ID and a correlation reference: 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope proceeds reference, 409 on a repeat, 422 with MSG-GEN-001 for an invalid element, 503 when the decision library or a consumed contract does not answer. The elements of `MatchRequest` that no source names are those of the match and no other (GAP-2518; ASM-4168).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2518; ASM-4168)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and its stage for a receipt; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2518; ASM-4168)) | `/api/recovery/decision/v1` | P7 rwb-decision | The proceeds arm at the version in force, with its rule IDs; faked |
| GET `/payments?businessDate={date}` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Date-form PaymentsAnswer, one row per paymentCode ordered by paymentCode, interim unpaged. 409 MSG-P1-001 when gated. Builder RWB-P1-E1013-APP, contract RWB-P1-E1015-CON. |
| GET `/batch-status` | `/api/recovery/source-data/v1` | P1 rwb-source-data | BatchStatusAnswer for the source and business date, using the rwb-payment workload identity. |

Each REST row is one hop, 2 s, one retry on a GET and a breaker per downstream (ADR-020). The plan gives this slice no C dependency; the absence of the two names is GAP-2518 with ASM-4168.

#### 12.3 Events published

| Event | Topic | Envelope | Key |
|---|---|---|---|
| `TreatmentBooked` (`rwb.payment.TreatmentBooked.v1`, EV-11) — `treatmentId`, `bookingRef`, `businessDate` | `rwb.payment.events.v1` | CloudEvents 1.0, event id, subject | The case reference |
| `PaymentMissed` (`rwb.payment.PaymentMissed.v1`, EV-12) — `treatmentId`, `dueDate`, `amountDue` | `rwb.payment.events.v1` | CloudEvents 1.0, event id, subject | The case reference |
| `ProceedsMatched` (`rwb.payment.ProceedsMatched.v1`, EV-25) — `proceedsId`, `caseId`, `amount` | `rwb.payment.events.v1` | CloudEvents 1.0, event id, subject | The case reference |

The three payloads are the EV rows of the Event and Messaging Design v5 and nothing beyond them. The schemas are registered once for the service with BACKWARD compatibility, carry no personal data, and are written to the outbox in the same transaction as the change they describe (Event and Messaging Design, Transactions and Payload rules). `TreatmentBooked` and `PaymentMissed` are published by the sibling stories of this service; the baseline fixes their shape and publishes none of them.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When | Owner service |
|---|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.rwb.source-data.events.v1` | Payload: `sourceSystem`, `businessDate`, `status`, `completedAt`. Record key: `{sourceSystem}:{businessDate}`. | Starts the auction and enforcement matching workflow on ALS/COMPLETED only | P1 rwb-source-data |

The rwb-payment listener consumes EV-26 from `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. Only `sourceSystem=ALS` and `status=COMPLETED` invoke Temporal signal-with-start on the auction and enforcement matching run's workflow ID for the event business date. The listener dedupes the CloudEvent ID in the shared inbox and the workflow guards the source and date. AceDataLate reports lateness and starts no matching. Receipt facts come from the payments operation in section 12.2.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The JOB-07 payment-matching workflow (name Not specified in the source documents (GAP-2520; ASM-4170)) | Workflow, one execution per business date | `rwb-payment` in namespace `rwb-recovery` | Input: the business date and the source `ALS`. No signal in this slice |
| The matching activity, name Not specified in the source documents (GAP-2520; ASM-4170) | Activity | `rwb-payment` | In: business date. Out: the rule IDs with their version, the rows written, the record references and the outbox row, in one transaction |

The activity calls Drools only inside itself, so a replay reuses the recorded answer, and it writes the record, the row and the outbox row in one transaction (the slide 14 pattern of the Temporal and Drools design; DP-03). Retry: 1 s initial, back-off 2, 10 attempts.

#### 12.6 Schedules

None. The run starts on the ACE batch completion of source ALS for a business date (EV-26; FSD P8 A2.4 AC-BG-P8-004-01), so this baseline declares no Temporal Schedule and no legacy Quartz row (DP-10 is not applied).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | The table baseline of TSD P8 T3.1 with the standard record columns; the elements are declared, no migration is |
| `decision_record` | Platform library, created in `rwb_payment` | The local decision record of DP-03 |
| `outbox_event` | Platform library, created in `rwb_payment` | The rows of the three published events (DP-09) |
| `inbox_event` | Platform library, created in `rwb_payment` | The (source, business date) replay guard (DP-09) |
| `idempotency_key` | Platform library, created in `rwb_payment` | The `Idempotency-Key` of the manual match and its stored answer |

No table of another owner is declared: `recovery_case` (P3), `treatment` (S2), `asset` and `sale` (S5), `debt_sale_lot` (S6), `write_off` (S7), `rule_row`, `rule_package_version` and `decision_log_entry` (P7) and every `v_ace_*` view (P1) are named by their owners only. The match rule table of TSD P8 T3.1 (`payment_match_rule`, DF-REF-261 to DF-REF-273) is declared by no owner of the ownership map, and the service holds no copy of it; the rule rows it needs are read from rwb-decision (GAP-2519; ASM-4169).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read | The open case `RC-2026-000611` of account `A-0611`; no case for `A-0998`; no answer inside 2 s | AC7, TC-P8-E4044-CON-05 |
| rwb-decision rule-package read | The proceeds arm at version `PM-2026.12` with its rule IDs; a replaced version | AC7, TC-P8-E4044-CON-05 |
| ACE batch-status fake | COMPLETED for source `ALS` on `2026-11-22`; a late and a failed batch | AC6, TC-P8-E4044-CON-04 |
| Published-event fake of `rwb.payment.events.v1` | One `ProceedsMatched` for one committed row; the same event twice | AC4, TC-P8-E4044-CON-03 |
| Decision-record stub (RWB-PLT-E1027-CON) | A healthy chain and a stopped chain | AC6, TC-P8-E4044-CON-06 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case and the unmatched list, with its empty, error and no-access states | AC1, TC-P8-E4044-CON-01 |

A fake that answers more than its owner's document fails the review. The two consumed operations without a published name are stubbed from the documents and keep the placeholder until their owners confirm them (GAP-2518; ASM-4168).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1`; the rwb-case case read and the rwb-decision rule-package read, date-form payments and batch status; one hop, 2 s |
| Kafka | 3 published, 1 consumed | `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` on `rwb.payment.events.v1` with `.retry` and `.dlt` ; EV-26 through the shared source-data group |
| Temporal | 1 workflow, 1 activity | The JOB-07 payment-matching workflow and its matching activity on `rwb-payment`; no Schedule |
| File | None | No file is produced or consumed by this slice |

### 13. Solution plan

| Artefact | What it fixes | Review owner |
|---|---|---|
| OpenAPI 3.1, one file | The base, the two operations, the query, the answers, the error set and the idempotency rule | P8 solution architect |
| Schemas in the same file | `Proceeds`, `ProceedsPage`, `MatchRequest`, the two lists and the standard columns | P8 data owner |
| AsyncAPI, one file | The topic, the three events, the envelope, the key and the payload | Event platform owner |
| Examples | One synthetic answer per operation and one event per schema, with no personal data | P8 solution architect |
| Table baseline | The `proceeds` elements and the standard columns, no migration | ACE DB owner |
| Fake set | One fake per consumed row and one per published event | The owner of each consumed contract |

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON (referenced, not held by this CON story) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data.yaml 5.1.0 with the rwb-payment workload identity | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON (referenced, not held) |

The compatibility check runs on three inputs — the previous tag, the new draft and a corpus of recorded fake answers — and a removal, a rename, a type change or a new required element forces a new major version (AC7). Because a CON story has no build dependency, this baseline is tagged on Day 1 and every consumer builds against the tag and its fakes.

### 14. Validation and messages

| ID | Type | Message | Declared on |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | The 422 answer of the match |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The 403 answer of both operations |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The 503 answer when the decision library does not answer |
| MSG-P1-001 | Error | {product} is from {date}. Today's load has not arrived. | The stale-data answer of the read (VR-P8-004-1) |

The identifiers are the module's own; the wording belongs to the Error and Message Standard and is cited, not restated in code. A message ID is the only text a client may switch on.

### 15. Screens and states

| Screen | State | Contract element it reads |
|---|---|---|
| SCR-28 Proceeds matching | Loading | `GET /proceeds` in flight; the composite route shows a skeleton |
| SCR-28 Proceeds matching | Matched | `Proceeds` rows with SALE_PROCEEDS or another matched value, with `posting_ref` when known |
| SCR-28 Proceeds matching | Unmatched | `Proceeds` rows with `matched_to` UNMATCHED; the match action is offered only with right U |
| SCR-28 Proceeds matching | Empty | Not specified in the source documents (CG-ALL-7666) |
| SCR-28 Proceeds matching | Error | Not specified in the source documents (CG-ALL-7666) |
| SCR-28 Proceeds matching | No access | Not specified in the source documents (CG-ALL-7666) |

The screen itself and its field layout are RWB-PLT-N001-CON and the edge stories; the contract fixes only the two answers the route merges (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E4044-CON-01 | AC1 | Contract | The OpenAPI document validates; the base, the two paths, the query parameters, the answers and the rights are present, and no other base is declared |
| TC-P8-E4044-CON-02 | AC2 | Contract | The `Idempotency-Key` rule is declared on the match only, the stored answer is described, and a repeat with a second key is a 409 |
| TC-P8-E4044-CON-03 | AC3 | Contract | `Proceeds`, `ProceedsPage` and `MatchRequest` validate against DF-FIN-001 to DF-FIN-009, `LOV-MATCH` and `LOV-PROCEEDS-SRC`, with `additionalProperties` false and no default or constant of a business value |
| TC-P8-E4044-CON-04 | AC4 | Contract | The three event schemas validate with the CloudEvents envelope, the topic with `.retry` and `.dlt`, the case key, the payload of the EV row and no personal data; a removed field is refused in BACKWARD mode |
| TC-P8-E4044-CON-05 | AC5 | Contract | The three consumed rows and the six fakes answer what their owners document; a fake that answers more, and a placeholder that loses its gap row, both fail |
| TC-P8-E4044-CON-06 | AC6, AC7 | Contract | The seven error answers are one problem document each with a code, a message ID and a correlation reference; a Schedule, a Quartz row, a foreign table, a second topic or a second base fails the absence test |
| TC-P8-E4044-CON-07 | AC7 | Contract | Each of the five tables of §12.7 is declared once with its owner; a sixth table, a copy of a foreign table or a missing owned table fails the boundary test |
| TC-P8-E4044-CON-08 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4044-CON-AC8) |
| TC-P8-E4044-CON-09 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4044-CON-AC9) |

The four legacy test cases TC-E4-044-01 to TC-E4-044-04 are owned by RWB-P8-E4044-APP; the six above are new contract cases, and a wave 3 harness copy takes the `-ITG` suffix.

### 17. Guardrails

- No business value in the contract: the tolerance, the window, the grace, the priority, the amounts and the rule IDs stay rule rows or reference data, never a schema default, an example constant or an enumeration member (BR-P8-004).
- No personal data in a schema, an example, an event payload or a fake: identifiers, amounts, dates, list values and a rule version only, and every example is synthetic.
- ACE receipt and batch facts come through rwb-source-data.yaml 5.1.0 using the rwb-payment workload identity (DP-05).
- No read of another service's table: the case, the treatment, the asset, the lot, the write-off and the rule rows are referenced by identifier and reached on their owners' contracts (DP-01).
- One base, one topic, one queue and one login: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment`, `rwb_payment`; a document that names another service's base or topic as its own fails review (DP-13, DP-14).
- The error envelope, the idempotency rule, the naming rule and the decision-record library come from the platform library; this story narrows them and never redefines them.
- The document lists only operations owned by rwb-payment; a consumed operation is described as consumed and faked, never as provided (DP-11).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-044 Match auction and enforcement proceeds, feature FEAT-PAY-04, module P8 (E4) | 1, 2 |
| FSD P8 v3 | A2.4 intent, steps and roles; VR-P8-004-1, BR-P8-004; AC-P8-004-01, AC-EXC-P8-004-01 and -02, AC-BG-P8-004-01; SCR-28 | 3, 8, 12.6, 15 |
| TSD P8 v2 | T3.0 standard columns; T3.1 `proceeds`; T3.2 lists; T3.3 relationships; T5.3 events; T6.1 rights; T-A.1 and T-A.2 | 11, 12.1, 12.3 |
| Event and Messaging Design v5 | EV-11, EV-12, EV-25 payloads; EV-26; the envelope, duplicate, transaction and payload rules | 12.3, 12.4 |
| Jobs and context | JOB-07 payment matching; service row of the P8 context pack | 12.5, 12.6 |
| Template and Rules v1 | §R4 naming; §R5.5 DP table; §R7.1 and §R7.2 template; §R7.3 fill order | all |
| Gaps and assumptions | GAP-2518, -3, -4, -5; ASM-4168, -3, -4, -5 | 3, 5, 11, 12 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The behaviour behind the two operations, the matching activity, the record-then-change transaction and the screen: RWB-P8-E4044-APP.
- The shapes of the other stories of this service: the settlement payment (RWB-E4-043), the rental auto-debit (RWB-E4-048), the fees, the ALS booking, the general-ledger posting and the daily reconciliation.
- The case, its states and its router: rwb-case (P3). The treatment: rwb-treatment (S2). The asset and its sale: rwb-asset (S5). The lot and the award: rwb-debtsale (S6). The write-off: rwb-writeoff (S7).
- The ACE payment, account and batch facts and the freshness of the data product: rwb-source-data (P1).
- The match package, the rule rows, their version and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the two rights: rwb-access (P4) and the guard of the service template.
- The composite route, the layout of SCR-28 and its field list: RWB-PLT-N001-CON and the edge stories.
- The migration of the schema and the DE role grants: the DB story of this service. The build pipeline, the tag and the release: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E4044-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
