# RWB-P3-E1021-CON Transfer rules and engine v1 - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1021-CON-16) |
| Contract version | 1; the two retention reads are additive operations of rwb-case.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-047, RD-P1-048 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E1073-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-007, FR-P3-012, FR-P3-013, FR-P3-030, FR-P3-031) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: Test Cases v9 mappings.

- RD-P1-047 and RD-P1-048: rwb-case publishes `GET /cases/retention-exclusions` and `GET /cases/closure-dates` as in rwb-case.yaml 5.1.0, with a fake, schemas and AC11 to AC13 (finding #1).
- Open paging details recorded as GAP-3336 (finding #2); ACE read wording aligned (finding #3).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-021 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **consumer of the case service (any service or the gateway-bff)**, I want **one published, versioned contract for moving a case between queues, teams and owners, with its events, its reason and rule-result shapes and its error envelope**, so that **every caller and every consumer builds against a fixed shape on Day 1, before the transfer capability is built**.

This story is the contract baseline of the transfer capability of `rwb-case`:

- REST base `/api/recovery/case/v1`, OpenAPI 3.1.
- Topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, AsyncAPI 3.0, CloudEvents 1.0.
- Temporal task queue `rwb-case` in namespace `rwb-recovery`.
- Java package `th.co.scb.ace.workbench.recovery.case`.
- Schema `rwb_case`, owned by P3, with the per-service login of DP-02. The login name is Not specified in the source documents (GAP-0688; ASM-1235) and is referred to as "the rwb-case login (DP-02)".

It carries no business logic. It fixes the artifacts that RWB-P3-E1021-APP and RWB-P3-E1021-OPS build and deploy, and it publishes the fake that the other services build against.

### 2. Business rationale

The monolith published a Java interface (`TransferService`) and a shared decision log; nothing outside the module could be built against it without the module. In the target, the transfer is called over REST by the gateway and by nothing else, and observed over Kafka by `rwb-reporting`. Without a published contract on Day 1, the five sibling slices of this legacy key (rwb-access, rwb-decision, rwb-document, rwb-deviation and the wave-1 integration harness) and the gateway route would each guess a shape, and the transfer request, response, error codes and authorization that REQ-CWC-010 requires to stay unchanged would drift.

The contract also fixes the two things that changed under D-RCV-60: the reason list is read as reference data of `rwb-case` (DP-07) and the rule answer is the `RuleResult` shape of the embedded Drools kit (DP-04), not a local rule table. Both appear in the document as named components, so a consumer can see where a value comes from without reading a table (DP-01).

### 3. Preconditions

- The Template and Rules v1 service facts are in force: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, queue `rwb-case`, package `th.co.scb.ace.workbench.recovery.case`.
- The ownership map confirms P3 owns `POST /cases/{caseId}/transfer`, `POST /cases/{caseId}/legal-hold`, `GET /me/tasks` and `PATCH /tasks/{taskId}`, and the tables `recovery_case`, `assignment`, `queue`, `queue_member`, `task`.
- RD-P1-047 gives rwb-case, owner of the legal-hold operation, two further reads: `GET /cases/retention-exclusions` and `GET /cases/closure-dates`. Their consumer is the retention run of rwb-source-data (RWB-P1-E1017-CON).
- The legacy request, response, error codes and authorization of the manual transfer are the baseline and do not change (BR11 of RWB-E1-021).
- No build dependency: this story is Day 1 and sits in contract group `CG-W1` (Template and Rules §R5.7 rule 1).
- The epic design is signed off; the sign-off is confirmed by the programme directive.

### 4. Flow

1. Write the OpenAPI 3.1 document for the transfer operation and the two task operations, with the schemas `TransferRequest`, `Assignment`, `LegalHoldRequest`, `Case`, `Task`, `TaskPage` and the error envelope.
   The same document carries the two retention reads of section 12.1 with the schemas `RetentionExclusionsPage`, `RetentionExclusion`, `ClosureDatesPage` and `ClosureDate`, and the fake answers them.
2. Write the AsyncAPI 3.0 document for `rwb.case.events.v1` with `CaseTransferred` and `CaseStateChanged`, the CloudEvents 1.0 envelope, the key and the headers.
3. Write the named schemas `TransferReason`, `RuleResult` and `DecisionRecordRef`, and reference them from the operation and the events.
4. Publish the error envelope: RFC 9457 problem response with `messageId`, `detail`, `instance` and `traceId`.
5. State the versioning rule: path version `v1` at the base, additive change only inside `v1`, breaking change is a new path version, deprecation announced in the document.
6. Publish the fake: a contract server generated from the document, with deterministic examples for 200, 401, 403, 404, 409, 422 and 503, and a Kafka stub that emits one CaseTransferred and one CaseStateChanged.
7. Run the contract tests of section 16 against the fake and publish the document in the service contract catalogue.

### 5. Exception paths

| ID | Situation | What the contract does | Covered by |
|---|---|---|---|
| C1 | A caller sends an unknown field in `TransferRequest` | The schema sets `additionalProperties: false`; the request is refused with the error envelope and the 422 example | AC1 |
| C2 | A caller omits `Idempotency-Key` on the POST | The header is declared required; the 400 example names the missing header; the document states the behaviour | AC1, AC5 |
| C3 | A consumer sends an event without the CloudEvents envelope | The AsyncAPI document marks the envelope required and the schema refuses a bare payload | AC3 |
| C4 | A producer adds a field to CaseTransferred | Allowed as an additive change inside `v1`; the consumer schema keeps `additionalProperties: true` and ignores unknown fields | AC5 |
| C5 | A breaking change is needed | A new path version is published; `v1` stays served until its announced retirement date; the change is never made in place | AC5 |
| C6 | A caller sends a transfer reason that is not in the list | The enum is a reference to LOV-TRANSFER-REASON; the 422 example shows MSG-P3-001; the list itself is read at run time, not frozen into the client | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1; no build dependency, no service code |
| Negotiable | Field names follow the legacy request and response; the descriptions and examples are reviewable |
| Valuable | Five sibling slices and the gateway build against it without waiting for the capability |
| Estimable | Three documents, six schemas, one fake, six contract tests |
| Small | One sprint-week for one pair |
| Testable | Every artifact has a contract test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1 - contract baseline

  Background:
    Given the contract baseline of rwb-case version 1 is published
    Given the service facts of Template and Rules v1: base /api/recovery/case/v1 and topic rwb.case.events.v1

  Scenario: AC1 OpenAPI 3.1 document for the transfer operation (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case version 1
    When the path /cases/{caseId}/transfer is read
    Then it declares POST with the operation ID of the transfer, the request body TransferRequest and the response 200 Assignment
    Then it declares 401, 403, 404, 409, 422 and 503 with the error envelope and a named messageId for each
    Then it declares the Idempotency-Key header as required and the Authorization bearer scheme
    Then a document validator reports no error against OpenAPI 3.1

  Scenario: AC2 Task operations and the transfer context (new, D-RCV-60)
    Given the same OpenAPI 3.1 document
    When the paths /me/tasks and /tasks/{taskId} are read
    Then GET /me/tasks answers TaskPage and PATCH /tasks/{taskId} answers Task
    Then the Task schema carries the caseId, queueCode, ownerUserId and the transfer reason code of the case
    Then every operation declares its authorisation right (Case record R for the read, Case record U for the update)

  Scenario: AC3 AsyncAPI document for the two events (new, D-RCV-60)
    Given the AsyncAPI 3.0 document of rwb.case.events.v1
    When the messages CaseTransferred and CaseStateChanged are read
    Then each message name follows rwb.case.<Event>.v1
    Then the envelope is CloudEvents 1.0 with the key caseId and the source rwb-case
    Then the CaseTransferred payload carries caseId, fromOwner, toOwner, reasonCode and ruleId
    Then no payload carries a party name, a national identifier or a contact detail

  Scenario: AC4 Transfer reason and rule-result shapes (new, D-RCV-60)
    Given the named schemas of the document
    When TransferReason, RuleResult and DecisionRecordRef are read
    Then TransferReason is a string that references LOV-TRANSFER-REASON and its values come from the reference-data contract, not from the document
    Then RuleResult carries packageCode, packageVersion, ruleId and outputs and is marked as the answer of the embedded Drools kit
    Then DecisionRecordRef carries the decision record ID and the hash link, and never the inputs

  Scenario: AC5 Error envelope, idempotency and versioning (new, D-RCV-60)
    Given the document components Error and Problem
    When a 422 response example is read
    Then it is an RFC 9457 problem response with type, title, status, detail, instance, messageId and traceId
    Then messageId holds a MSG- identifier and never free text
    When the Idempotency-Key behaviour and the versioning rule are read
    Then a repeat with the same key returns the first response and creates no second assignment
    Then the versioning rule states v1 in the path, additive-only change inside v1 and a new path version for a breaking change

  Scenario: AC6 The nine contract tables of section 12 (new, D-RCV-60)
    Given the contract story of RWB-E1-021
    When section 12 is read
    Then each of the nine sub-tables is present and either carries rows or states None
    Then every operation and table owner named in it is the owner recorded in the ownership map
    Then the fake described in 12.8 is published with the document in the same release

  Scenario: AC7 Manual transfer keeps its contract (new, D-RCV-60)
    Given the manual transfer of RWB-E1-021 as the baseline
    When the POST operation of /cases/{caseId}/transfer is read
    Then its endpoint, request, response, errors and authorisation are those of the manual transfer, copied unchanged

  Scenario: AC8 Every business rule of section 8 names a criterion (new, D-RCV-60)
    Given the business rules table of section 8
    When the Covered by column is read
    Then BR1 to BR7 each name an AC of section 7 and each named AC exists

  Scenario: AC9 A retried or timed-out transfer activity is handled once (new, D-RCV-60)
    Given a transfer activity of the case workflow
    When the activity is retried after a timeout
    Then the transfer is not applied twice and the repeat rule of AC5 is kept
    Then the retry count and timeout values are Not specified in the source documents (NEWAC-RWB-P3-E1021-CON-AC8)

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case version 1
    When the responses of PATCH /tasks/{taskId} are read
    Then it declares 409 with the problem envelope of AC1
    Then a status change that the status model of the Task schema does not allow answers 409 and publishes no CaseStateChanged message

  Scenario: AC11 Retention exclusion set (new, D-RCV-60)
    Given the fake holds case A on legal hold and case B open, each with account and person keys, and case C closed and not held
    When the rwb-source-data identity reads GET /api/recovery/case/v1/cases/retention-exclusions with size 1000
    Then the answer is 200 with items, page, size and total, and holds case A with reason LEGAL_HOLD and case B with reason OPEN with closedAt null, each with caseId, caseNumber, accountKeys and personKeys
    Then case C is not in the answer
    Then when more items exist than the page holds, cursor is not null, following it returns every held and open case exactly once, and the last page has cursor null

  Scenario: AC12 Closure dates of closed, unheld cases (new, D-RCV-60)
    Given the fake holds case C closed before 2026-01-01T00:00:00+07:00 and not held, case D closed before it and on legal hold, and case E closed after it
    When the rwb-source-data identity reads GET /api/recovery/case/v1/cases/closure-dates with closedBefore 2026-01-01T00:00:00+07:00
    Then the answer is 200 and holds case C only, with caseId, closedAt, accountKeys and personKeys

  Scenario: AC13 Errors of the two retention reads (new, D-RCV-60)
    Given the published fake of rwb-case
    When closure-dates is read without closedBefore, or either read is made with size 1001
    Then the answer is 400 with the error envelope
    Then a call with no valid credential answers 401, a caller without Case record R answers 403 and an unavailable store answers 503, each with the error envelope
    Then no read writes a row or publishes an event
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The manual transfer keeps its endpoint, request, response, errors and authorization; the contract copies them unchanged | REQ-CWC-010; BR11 of RWB-E1-021 | AC7 |
| BR2 | The transfer reason is a coded value from LOV-TRANSFER-REASON, referenced and not frozen into the document | LOV-TRANSFER-REASON; REQ-WKM-003 | AC4 |
| BR3 | CaseTransferred carries caseId, fromOwner, toOwner, reasonCode, and no personal data | EV-04; section 12.3 | AC3 |
| BR4 | A repeat of the POST with the same Idempotency-Key returns the first response | Architecture v5 slide 11; TSD P3 API-P3-006 | AC5 |
| BR5 | The path version sits in the base; a breaking change is a new version and never an in-place change | DP-13; Template and Rules §R5.5 | AC5 |
| BR6 | The document names no table of another service and no rule table; the rule answer is a `RuleResult` | DP-01; DP-04; D-RCV-36 T5 | AC6 |
| BR7 | Topic and event names come from the naming rule and are not typed by a consumer | DP-14 | AC3 |

### 9. State transitions

| From | Event | To |
|---|---|---|
| Document in draft | review comments closed | Document in review |
| Document in review | contract tests of section 16 pass | Document published as version 1 |
| Document published as version 1 | additive change agreed | Version 1 revised; the minor change is recorded in the change log |
| Document published as version 1 | breaking change agreed | Version 2 published; version 1 served until its announced retirement date |

The document itself has no case state. The case states it describes are those of section 9 of RWB-P3-E1021-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX contract owner | Authors, versions and publishes the document and the fake |
| Solution architect | Approves the shape and the versioning rule |
| Consumer teams of rwb-access, rwb-decision, rwb-document, rwb-deviation and the integration harness | Read the document and build against the fake; they do not change it |
| RW-TEAMMGR, RW-CAPACITY, RW-LITOFF | Named as the roles the operations authorise; they take no action in this story |
| SY-RULES, SY-CASEWF, SY-DECLOG | Named as the system actors of the capability, not of the document |

### 11. Data

The contract names fields; it stores nothing.

| Schema | Fields that come from an owned table | Owning table in rwb_case | BR Field ID |
|---|---|---|---|
| `Assignment` | id, caseId, assigneeUserId, assignedAt, reason, ruleId, transferReasonCode, queueId | `assignment` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `RetentionExclusion` | caseId, caseNumber, reason (`LEGAL_HOLD` or `OPEN`), closedAt (nullable), accountKeys, personKeys | `recovery_case`, `case_account`, `case_party` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `ClosureDate` | caseId, closedAt, accountKeys, personKeys | `recovery_case`, `case_account`, `case_party` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `Case` (hold response) | caseId, status, legalHold, statusBeforeHold, queueCode, ownerUserId | `recovery_case`, `queue` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `Queue` fields inside `Assignment` | queueId, queueCode, teamCode | `queue` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `Task`, `TaskPage` | id, caseId, taskCode, status, ownerRole, dueAt | `task` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `TransferRequest` | toOwnerId, toQueueId, reasonCode, note, transferReasonCode | none; accepted as input | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `TransferReason` | code | `lov_value` through the reference-data contract of DP-07 | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `RuleResult` | packageCode, packageVersion, ruleId, outputs | none; the answer of the embedded Drools kit of DP-04 | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| `DecisionRecordRef` | decisionRecordId, entryHash | the decision-record library table of DP-03 | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |
| Event `CaseTransferred` | caseId, fromOwner, toOwner, reasonCode | `recovery_case`, `assignment` | Not specified in the source documents (DOR-RWB-P3-E1021-CON-7) |

The ownership of the transfer reason list itself, and who may add or retire a reason code, is Not specified in the source documents (GAP-0690; ASM-1237). The document therefore references the list by name and never enumerates it as a closed set in the client.

Open decision DL23 (REQ-WKM-003) is still open. Its assumptions ASM-1232, ASM-1237, ASM-1259 and ASM-1560 apply, as confirmed by the programme directive.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Document |
|---|---|---|---|
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 | TransferRequest in, Assignment out, Idempotency-Key required |
| POST | `/api/recovery/case/v1/cases/{caseId}/legal-hold` | P3 | LegalHoldRequest in, Case out, Idempotency-Key required |
| GET | `/api/recovery/case/v1/me/tasks` | P3 | Query due, type, page, size; TaskPage out |
| PATCH | `/api/recovery/case/v1/tasks/{taskId}` | P3 | TaskUpdate in, Task out; complete or reassign a transfer-related task |
| GET | `/api/recovery/case/v1/cases/retention-exclusions` | P3 | Query `page`, `size` (1 to 1,000), `cursor`; `RetentionExclusionsPage` out: every case on legal hold or open, with the account and person keys; Case record R |
| GET | `/api/recovery/case/v1/cases/closure-dates` | P3 | Query `closedBefore` (date-time, required), `page`, `size` (1 to 1,000), `cursor`; `ClosureDatesPage` out: closed, unheld cases; Case record R |

The two retention reads are published in rwb-case.yaml 5.1.0. Their errors are 400, 401, 403 and 503 with the error envelope. rwb-source-data calls them with a one-hop 2 s budget, at the start of a retention run and again before each delete unit, and fails the run when an exclusion answer cannot be read, so each answer states the cases as they are at the time of the call. Pending, owner rwb-case service owner: default page size, item order, how `page` and `cursor` combine, and the source column of `closedAt` (GAP-3336).

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

| Event | Topic | Owner | Payload |
|---|---|---|---|
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | caseId, fromOwner, toOwner, reasonCode |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | caseId, decisionLogEntryId, fromState, ruleId, toState |

#### 12.4 Events consumed

| Event | Topic | Owner |
|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 |
| `rwb.decision.ApprovalRequested.v1` | `rwb.decision.events.v1` | P7 |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 |
| `rwb.valuation.RouteDecided.v1` | `rwb.valuation.events.v1` | S1 |

The contract declares these as the triggers the capability observes; it does not declare `TimerDue` as a Kafka event, because the timer expiry is raised inside `CaseWorkflow` by its durable timer. For the route-decided trigger of TRF-002 the wave 1 contract asserts the route-decided fact that rwb-case commits as `rwb.case.CaseStateChanged.v1`; the S1 `RouteDecided` announcement is asserted separately when rwb-valuation lands in wave 3 (assumption recorded under GAP-0346).

#### 12.5 Workflows and activities

| Name | Kind | Queue | Declared input and output |
|---|---|---|---|
| `CaseWorkflow` | Parent workflow | `rwb-case` | Input: caseId. Signal: the trigger fact. Output: none |
| `transfer` | Activity | `rwb-case` | Input: caseId, trigger fact, or the manual request with caller and key. Output: the assignment view |

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Owner | Named in the document as |
|---|---|---|
| `recovery_case` | P3 | the case view behind the hold response |
| `case_account` | P3 | the account keys of the two retention reads |
| `case_party` | P3 | the person keys of the two retention reads |
| `assignment` | P3 | the transfer response |
| `queue` | P3 | the queue reference of the response and the request |
| `queue_member` | P3 | the member load, not exposed |
| `task` | P3 | Task and TaskPage |

#### 12.8 Contract fakes

| Fake | Story | Contents |
|---|---|---|
| Transfer and legal-hold contract server | RWB-P3-E1021-CON (this story) | Generated from the document; deterministic examples for 200, 401, 403, 404, 409, 422 and 503 |
| Retention reads fake | RWB-P3-E1021-CON (this story) | `retention-exclusions` and `closure-dates`: a held case, an open case, a closed unheld case, an empty set, two pages, a timeout and 503; consumed by RWB-P1-E1017-CON |
| Event stub | RWB-P3-E1021-CON (this story) | One CaseTransferred and one CaseStateChanged on a local topic with the CloudEvents envelope |
| Decision-record fake | RWB-PLT-E1027-CON | The record write and the topic publish |
| Drools kit stub | RWB-PLT-E1072-CON | Package TRANSFER, version "TRF-2026.11", rule "TRF-007" |
| Reference-data fake | RWB-P3-E1043-CON | LOV-TRANSFER-REASON R01 to R06 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 6, consumed 0 | Two transfer operations, two task operations and two retention reads |
| Kafka | Published 2 events; consumed 7 events declared | `rwb.case.events.v1` and the inbound topics |
| Temporal | 1 workflow, 1 activity declared | `CaseWorkflow` and `transfer` |
| File | None | None |

### 13. Solution plan

**Artifacts**

| Artifact | Path | Format |
|---|---|---|
| OpenAPI document | `contracts/rwb-case/openapi-v1.yaml` | OpenAPI 3.1 |
| AsyncAPI document | `contracts/rwb-case/asyncapi-v1.yaml` | AsyncAPI 3.0 |
| Schemas | inside the two documents, named components | JSON Schema 2020-12 |
| Fake server | `contracts/rwb-case/fake/` | Generated server plus the hand-written examples |
| Contract test suite | `contracts/rwb-case/tests/` | Schemathesis or equivalent, run in the pipeline |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract only | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

As a contract story this one has no build dependency (§R5.7 rule 1). The pattern rows above are the patterns the capability applies; the dependencies they add are carried by RWB-P3-E1021-APP, the build story, and by the platform contract stories themselves.

**Build steps**

1. Draft `TransferRequest`, `Assignment`, `LegalHoldRequest` and `Case` from the legacy request and response, field for field.
2. Add the two task operations and their schemas.
3. Add the error envelope and the seven error examples with their MSG identifiers.
4. Add `TransferReason`, `RuleResult` and `DecisionRecordRef`.
5. Write the AsyncAPI document with the CloudEvents envelope, the key and the two messages.
6. Generate the fake and the contract test suite; run the six tests of section 16.
7. Add the two retention reads, their four schemas, their fake and the tests of AC11 to AC13.

**Done when.** Both documents validate, the fake serves all seven error examples, the six contract tests pass, the two retention reads and their fake are published and consumed by the contract test of RWB-P1-E1017-CON, and the document is published in the service contract catalogue with version 1.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | Manual transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-027 | No TRANSFER version is in force for a rule trigger | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Each identifier is bound to one HTTP status in the document: MSG-P4-002 to 403, MSG-P3-005 and MSG-GEN-004 to 409, MSG-P3-001, MSG-P3-002 and MSG-P3-011 to 422, MSG-P7-003 to 503, and MSG-P3-027 to the non-retryable error of the activity, not to a caller response.

### 15. Screens and states

No screen. The document is the input to the gateway-bff composite route (DP-19) that serves the case record view, and to the client library that the Epic 2 transfer screen (RWB-E2-012) will use. The document states, for the screen's benefit, that a case in the overflow queue has no owner and that a case on hold shows the hold banner.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1021-CON-01 | AC1 | Contract | OpenAPI 3.1 validation of the document; the transfer path and its seven error responses |
| TC-P3-E1021-CON-02 | AC2 | Contract | The two task operations and the Task schema fields |
| TC-P3-E1021-CON-03 | AC3 | Contract | AsyncAPI validation; the two messages and the CloudEvents envelope; a payload scan for personal-data fields |
| TC-P3-E1021-CON-04 | AC4 | Component | TransferReason, RuleResult and DecisionRecordRef resolved and referenced from the operation and the events |
| TC-P3-E1021-CON-05 | AC5 | Contract | The problem envelope on all seven examples; a repeated request with the same Idempotency-Key; the versioning statement |
| TC-P3-E1021-CON-06 | AC6 | Component | The nine sub-tables present, each owner matched against the ownership map, the fake published with the document |
| TC-P3-E1021-CON-07 | AC6 | Component | Boundary of the seven tables of 12.7: each owned by P3, and no table outside 12.7 is named in the document |
| TC-P3-E1021-CON-08 | AC7 | Contract | The POST operation compared with the manual transfer baseline: endpoint, request, response, errors and authorisation |
| TC-P3-E1021-CON-09 | AC8 | Component | Traceability of the Covered by column of section 8 (BR1 to BR7) against the criteria of section 7 |
| TC-P3-E1021-CON-10 | AC9 | Component | A retried or timed-out transfer activity applies the transfer once and keeps the repeat rule of AC5; retry and timeout values are Not specified in the source documents (NEWAC-RWB-P3-E1021-CON-AC8) |
| TC-P3-E1021-CON-11 | AC10 | Contract | The 409 response of PATCH /tasks/{taskId}; a disallowed status change answers 409 and publishes no CaseStateChanged message |
| TC-P3-E1021-CON-12 | AC11 | Contract | Held, open and closed cases; two pages followed by cursor |
| TC-P3-E1021-CON-13 | AC12 | Contract | closedBefore with a closed unheld, a closed held and a later closed case |
| TC-P3-E1021-CON-14 | AC13 | Contract | Missing closedBefore, size 1001, 401, 403, 503 |

### 17. Guardrails

- No business value in the document that belongs to reference data: the reason list is referenced, not enumerated.
- No personal data in any example, in any event payload or in any response: examples use case numbers, user identifiers and codes only. The two retention reads are the exception ruled by RD-P1-047: they return account and person keys (synthetic in every example, never logged) and no name, address, contact value or identity number.
- No table of another service is named as a source; the rule answer is a `RuleResult`, never a rule table (DP-01, DP-04).
- The manual transfer keeps its request, response, errors and authorization (BR11 of RWB-E1-021).
- The document is versioned and never edited in place: a breaking change is a new path version.
- The fake is generated from the document, so a drift between document and fake fails the pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers and manual request with a reason | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-P3-E1021-CON-01, TC-P3-E1021-CON-02, TC-P3-E1021-CON-05 |
| REQ-CWC-016 | Every transfer logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-P3-E1021-CON-03, TC-P3-E1021-CON-04 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | Epic 2, work management | FEAT-CWC-10 | All recovery processes | VR-P3-010-1; DL23 | TC-P3-E1021-CON-04 |
| REQ-CWC-005 | A case is in one queue with one open assignment | Epic 1, 3.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20 | TC-P3-E1021-CON-01 |

| Legacy reference | Where it is kept |
|---|---|
| Package code TRANSFER, version "TRF-2026.11" | Sections 3, 12.8, 16 |
| Event CaseTransferred (EV-04) | Sections 1, 12.3, 16 |
| MSG-P3-001, MSG-P3-002, MSG-P3-005, MSG-P3-011, MSG-P3-027, MSG-GEN-004, MSG-P7-003, MSG-P4-002 | Section 14 |
| `POST /cases/{caseId}/transfer` | Sections 4, 12.1, 16 |
| Legacy key RWB-E1-021, story RWB-P3-E1021-APP, contract RWB-P3-E1021-CON, deployment RWB-P3-E1021-OPS | Metadata, section 12 |

### 19. Out of scope

- The transfer capability itself, its tests and its feature flag (RWB-P3-E1021-APP).
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics and the runbook (RWB-P3-E1021-OPS).
- The rule package authoring, approval and promotion (RWB-P3-E1073-APP).
- The gateway-bff composite route and the Epic 2 transfer screen (RWB-E2-012).
- The central decision ledger and its own contract (rwb-decision).
- Any change to the request, response, error codes or authorization of the manual transfer; this story records them, it does not change them.

### 20. Remaining delivery steps

- Size the story (delivery lead).
- Contract story Done and the fakes, including the retention reads fake, published (rwb-case service owner).
- Consumer acceptance by rwb-source-data (RWB-P1-E1017-CON; rwb-source-data service owner; ASM-5705).
- Test data loaded in DEV and Test Cases v9 rows confirmed (QA lead).
