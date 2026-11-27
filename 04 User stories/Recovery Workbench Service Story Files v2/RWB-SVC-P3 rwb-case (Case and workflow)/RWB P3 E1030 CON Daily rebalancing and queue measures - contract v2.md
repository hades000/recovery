# RWB-P3-E1030-CON Daily rebalancing and queue measures - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1030-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Squad sizes at refinement; not yet sized |
| Contract version | 1 (/api/recovery/case/v1; rwb.case.events.v1) |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-017, FR-P3-018) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-030 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 18 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the case service (any service or the gateway-bff)**, I want **one published, versioned contract for the queue measures of a business date, the case read used to reconcile them, the `CaseTransferred` message and the run that produces them, with its error envelope and its fake**, so that **every reader and every consumer builds against a fixed shape on Day 1, before the rebalancing run is built**.

This story is the contract baseline of the rebalancing and measure capability of `rwb-case`:

- REST base `/api/recovery/case/v1`, OpenAPI 3.1.
- Topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, AsyncAPI 3.0, CloudEvents 1.0.
- Temporal task queue `rwb-case` in namespace `rwb-recovery`; the Schedule and the activities are declared as the run artifact of the document.
- Java package `th.co.scb.ace.workbench.recovery.case`, copied from the Service Template Specification v1 (CG-ALL-3665); no non-reserved package segment is Not specified in the source documents (CG-ALL-3665).
- Schema `rwb_case`, owned by P3; the document names tables only as sources of fields (DP-01).

It carries no business logic. It fixes the three read operations, the measure schema taken from the legacy `QueueMeasureView`, the `CaseTransferred` message, the error envelope, the versioning rule and the declarations of the run, and it publishes the fake that the build story and the reporting consumer use.

### 2. Business rationale

The monolith published the Java interface `QueueMeasureService` and left the measure fields in a record inside the module; nothing outside the module could read a queue's numbers without the module. In the target the queue measures are read over REST by the case-side screens through the gateway, and the reporting projection is built from events. Without a published contract on Day 1, the screens, the reporting consumer and the reconciliation test of REQ-CWC-015 and REQ-RDF-012 would each guess a field list, a status value and a reconciliation rule, and the numbers a team manager sees would drift from the case list.

The contract also fixes the two things that changed under D-RCV-60: the measure publication has no data-lake copy (DP-17), and the run's record is the workflow's own record rather than a job monitor (DP-10). Both are declared in the document, so a consumer can see what it can and cannot read.

### 3. Preconditions

- The Template and Rules v1 service facts are in force: base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, queue `rwb-case`, package `th.co.scb.ace.workbench.recovery.case`.
- The ownership map confirms P3 owns `GET /cases`, `GET /queues` and `GET /queues/{queueId}/cases`, and the tables `queue`, `queue_member`, `recovery_case`, `assignment`, `timer` and `queue_measure`.
- The legacy measure field list of `QueueMeasureView` is the baseline and does not change: queue code, team code, as-of time, depth, unassigned, average age in days, maximum age in days, owner minimum, owner maximum and breaches.
- No build dependency: this story is Day 1 and sits in contract group `CG-W1` (Template and Rules §R5.7 rule 1).

### 4. Flow

1. Write the OpenAPI 3.1 document with the three read operations and the schemas `QueueMeasure`, `QueueMeasurePage`, `Case`, `CasePage`, `Assignment` and the error envelope.
2. Take the `QueueMeasure` field list from the legacy record, field for field, and add the snapshot status from LOV-SNAPSHOT-STATUS.
3. Write the AsyncAPI 3.0 document for `rwb.case.events.v1` with `CaseTransferred`, the CloudEvents envelope, the key `caseId` and the headers.
4. Declare the run artifact in the document: the Schedule `rwb-case-rebalance-daily`, the `DailyCaseRun` workflow and its `rebalance` and `takeQueueMeasures` activities, and their inputs and outputs.
5. State what the run publishes and what it does not: `CaseTransferred` per move and the decision record on `rwb.decision-record.v1`; no measure feed and no file (DP-17).
6. Publish the error envelope: RFC 9457 problem response with `messageId`, `detail`, `instance` and `traceId`.
7. State the versioning rule: path version `v1` at the base, additive change only inside `v1`, a breaking change is a new path version.
8. Publish the fake: a contract server generated from the document with deterministic examples for 200, 400, 401, 403 and 503, and a Kafka stub that emits one `CaseTransferred`.
9. Run the contract tests of section 16 and publish the document in the service contract catalogue.

### 5. Exception paths

| ID | Situation | What the contract does | Covered by |
|---|---|---|---|
| C1 | A caller sends an unknown query parameter on the case read | The schema sets `additionalProperties: false` on the parameter set; the request is refused with the error envelope and the 400 example | AC1 |
| C2 | A consumer sends an event without the CloudEvents envelope | The AsyncAPI document marks the envelope required and the schema refuses a bare payload | AC3 |
| C3 | A producer adds a field to `CaseTransferred` | Allowed as an additive change inside `v1`; the consumer schema keeps `additionalProperties: true` and ignores unknown fields | AC3 |
| C4 | A breaking change is needed | A new path version is published; `v1` stays served until its announced retirement date; the change is never made in place | AC6 |
| C5 | A reader asks for a snapshot that is `TAKEN` or `HELD` | The document states that only a `PUBLISHED` snapshot is returned, and the 404 example names the queue and the business date | AC2 |
| C6 | A consumer expects a measure feed or a file | The document states that the run publishes events only, that the lake copy is removed (DP-17) and that reporting projects from events | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1; no build dependency, no service code |
| Negotiable | Field names follow the legacy record; descriptions and examples are reviewable |
| Valuable | The screens, the reporting consumer and the reconciliation test build against one shape |
| Estimable | Two documents, six schemas, one fake, five contract tests |
| Small | One sprint-week for one pair |
| Testable | Every artifact has a contract test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures - contract baseline

  Background:
    Given the contract baseline of rwb-case version 1 is published
    Given the service facts of Template and Rules v1: base /api/recovery/case/v1 and topic rwb.case.events.v1

  Scenario: AC1 The three read operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case version 1
    When the paths /queues, /queues/{queueId}/cases and /cases are read
    Then GET /queues answers QueueMeasurePage and GET /queues/{queueId}/cases answers CasePage
    Then GET /cases declares the queue, status, page and size parameters and answers CasePage
    Then every operation declares 401, 403 and 503 with the error envelope and a named messageId for each
    Then a document validator reports no error against OpenAPI 3.1

  Scenario: AC2 The measure schema (new, D-RCV-60)
    Given the named schema QueueMeasure
    When its fields are read
    Then it carries queueCode, teamCode, asOf, depth, unassigned, avgAgeDays, maxAgeDays, ownerMin, ownerMax and breached
    Then it carries status with the three values TAKEN, PUBLISHED and HELD, and only a PUBLISHED row is returned by the operation
    Then it carries no case identifier, no party attribute, no amount and no personal data
    Then each field names its source table in rwb_case and no table of another service
    Then a depth is published only when it equals the case list count at the same time

  Scenario: AC3 The CaseTransferred message (new, D-RCV-60)
    Given the AsyncAPI 3.0 document of rwb.case.events.v1
    When the message CaseTransferred is read
    Then its name follows rwb.case.<Event>.v1 and the topic is rwb.case.events.v1
    Then the envelope is CloudEvents 1.0 with the key caseId and the source rwb-case
    Then the payload carries caseId, fromOwner, toOwner and reasonCode, and the reason value REBALANCE is given as an example
    Then no payload carries a party name, a national identifier, a contact detail or an amount

  Scenario: AC4 Error envelope, idempotency and the run declaration (new, D-RCV-60)
    Given the document components Error and Problem and the run artifact section
    When a 403 response example is read
    Then it is an RFC 9457 problem response with type, title, status, detail, instance, messageId and traceId
    Then messageId holds one of MSG-P3-011, MSG-P3-028, MSG-P3-029, MSG-P7-003 and MSG-P4-002 and never free text
    When the run artifact section is read
    Then it declares the Schedule rwb-case-rebalance-daily, the workflow DailyCaseRun and the activities rebalance and takeQueueMeasures
    Then it states that a case is moved once per business date and that a balanced queue selects nothing on a repeat
    Then it states that the run publishes CaseTransferred and the decision record and no measure feed and no file

  Scenario: AC5 The nine contract tables of section 12 (new, D-RCV-60)
    Given the contract story of RWB-E1-030
    When section 12 is read
    Then each of the nine sub-tables is present and either carries rows or states None
    Then every operation and table owner named in it is the owner recorded in the ownership map
    Then the fake described in 12.8 is published with the document in the same release
    Then the document states that the legacy rerun call has no published operation and that the run record is the workflow record (GAP-2206; ASM-3622)

  Scenario: AC6 A breaking change is a new path version and v1 is not changed in place (new, D-RCV-60)
    Given the contract baseline of rwb-case version 1 is published
    When a breaking change to a published operation or event is needed
    Then it is published as a new path version and v1 stays served until its announced retirement date
    Then the change is not made to v1 in place

  Scenario: AC7 Each business rule of section 8 is covered by a criterion and a test (new, D-RCV-60)
    Given the business rule table of section 8 with the rules BR1 to BR8
    When each rule and its Covered by entry are read
    Then every rule BR1 to BR8 names at least one criterion of section 7 and one test case of section 16
    Then each criterion and test case named in the table exists in this document

  Scenario: AC8 Each provided operation declares a 404 response with the error envelope (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case version 1
    When the provided operations are read
    Then every provided operation declares 404 with the error envelope

  Scenario: AC9 A retried or timed-out activity moves no case twice (new, D-RCV-60)
    Given the workflow DailyCaseRun with the activities rebalance and takeQueueMeasures
    When the activity rebalance is retried or times out
    Then no case is moved twice
    Then the run still publishes CaseTransferred and the decision record and no measure feed and no file

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the snapshot status values TAKEN, PUBLISHED and HELD of AC2
    When a status change that the status model does not allow is requested
    Then the change is refused and is not published
    Then the refusal uses the error envelope
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The measure field list is the legacy `QueueMeasureView` list, unchanged, plus the snapshot status | RWB-E1-030 section 12; REQ-RDF-012 | AC2, TC-P3-E1030-CON-02 |
| BR2 | Only a `PUBLISHED` snapshot is served; a `TAKEN` or `HELD` row is not | RWB-E1-030 BR6; DL25 (open; assumptions: Not specified in the source documents (DOR-RWB-P3-E1030-CON-18)); REC-01 | AC2, TC-P3-E1030-CON-02 |
| BR3 | A depth is published only when it equals the case list count at the same time | RWB-E1-030 BR6 | AC2, TC-P3-E1030-CON-02 |
| BR4 | `CaseTransferred` carries caseId, fromOwner, toOwner and reasonCode, and no personal data | EV-04; section 12.3 | AC3, TC-P3-E1030-CON-03 |
| BR5 | The path version sits in the base; a breaking change is a new version and never an in-place change | DP-13; Template and Rules §R5.5 | AC6, TC-P3-E1030-CON-07 |
| BR6 | The document names no table of another service; the measure row is `rwb_case.queue_measure` | DP-01 | AC2, TC-P3-E1030-CON-02 |
| BR7 | The run publishes events only: no measure feed and no file (no data lake) | DP-17 | AC4, TC-P3-E1030-CON-04 |
| BR8 | The topic and event names come from the naming rule and are not typed by a consumer | DP-14 | AC3, TC-P3-E1030-CON-03 |

### 9. State transitions

| From | Event | To |
|---|---|---|
| Document in draft | review comments closed | Document in review |
| Document in review | the contract tests of section 16 pass | Document published as version 1 |
| Document published as version 1 | additive change agreed | Version 1 revised; the change is recorded in the change log |
| Document published as version 1 | breaking change agreed | Version 2 published; version 1 served until its announced retirement date |

The document has no case state. The snapshot states it describes are those of section 9 of RWB-P3-E1030-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX contract owner | Authors, versions and publishes the document and the fake |
| Solution architect | Approves the shape and the versioning rule |
| Consumer teams of the case screens, the reporting projection and the wave-1 harness | Read the document and build against the fake; they do not change it |
| RW-TEAMMGR, RW-BIANAL, RW-DATASTEW | Named as the roles the operations authorise; they take no action in this story |
| SY-CASEWF, SY-DECLOG | Named as the system actors of the capability, not of the document |

### 11. Data

The contract names fields; it stores nothing.

| Schema | Fields that come from an owned table | Owning table in rwb_case | BR Field ID |
|---|---|---|---|
| `QueueMeasure` | queueCode, teamCode | `queue` | Not specified in the source documents (DOR-RWB-P3-E1030-CON-7) |
| `QueueMeasure` | asOf, depth, unassigned, avgAgeDays, maxAgeDays, ownerMin, ownerMax, breached, status | `queue_measure` | Not specified in the source documents (DOR-RWB-P3-E1030-CON-7) |
| `CasePage`, `Case` | caseId, caseNo, status, queueCode, ownerUserId, entryDate, deviationOpen, legalHold | `recovery_case`, `queue` | Not specified in the source documents (DOR-RWB-P3-E1030-CON-7) |
| `Assignment` | assigneeUserId, assignedAt, reason, queueId | `assignment` | Not specified in the source documents (DOR-RWB-P3-E1030-CON-7) |
| Event `CaseTransferred` | caseId, fromOwner, toOwner, reasonCode | `recovery_case`, `assignment` | Not specified in the source documents (DOR-RWB-P3-E1030-CON-7) |

The run record of a business date has no published read of its own: the legacy job record is retired with the Quartz job, and the moves of a date are read through `GET /cases` and the snapshot through `GET /queues`. The shape of a published run record and the operation of the legacy rerun call are Not specified in the source documents (GAP-2206; ASM-3622).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Document |
|---|---|---|---|
| GET | `/api/recovery/case/v1/queues` | P3 | Query team, page, size; `QueueMeasurePage` out, `PUBLISHED` snapshots only |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 | The case list count of a queue at one time; `CasePage` out |
| GET | `/api/recovery/case/v1/cases` | P3 | Query queue, status, page, size; `CasePage` out; the reconciliation read |

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

| Event | Topic | Owner | Payload |
|---|---|---|---|
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | caseId, fromOwner, toOwner, reasonCode |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | the hash-chained decision record |

#### 12.4 Events consumed

| Event | Topic | Owner |
|---|---|---|
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 |

The document declares `TimerBreached` as the input of the breach alert; it declares no other subscription for the run, because the run is started by a Schedule.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Declared input and output |
|---|---|---|---|
| `DailyCaseRun` | Workflow | `rwb-case` | Input: businessDate. Steps: allocation, then rebalance. Output: the run result |
| `rebalance` | Activity | `rwb-case` | Input: businessDate. Output: the moves, the resulting assignment views and the cases that stayed with MSG-P7-003 |
| `takeQueueMeasures` | Activity | `rwb-case` | Input: businessDate and as-of time. Output: one measure view per queue with its status |

#### 12.6 Schedules

| Schedule | Workflow | Cron | Zone | Declared by |
|---|---|---|---|---|
| `rwb-case-rebalance-daily` | `DailyCaseRun` | 06:30 daily | the business time zone of the values file, Not specified in the source documents (GAP-2207; ASM-3623) | RWB-P3-E1030-OPS |

#### 12.7 Tables owned

| Table | Owner | Named in the document as |
|---|---|---|
| `queue` | P3 | the queue reference of a measure row and of the case read |
| `queue_measure` | P3 | the measure row and its status |
| `recovery_case` | P3 | the case fields of the case read |
| `assignment` | P3 | the assignment view returned by the run |
| `queue_member` | P3 | the capacity behind the cap, not exposed |
| `timer` | P3 | the breach count, aggregated, not exposed per row |

#### 12.8 Contract fakes

| Fake | Story | Contents |
|---|---|---|
| Queue and case read contract server | RWB-P3-E1030-CON (this story) | Generated from the document; deterministic examples for 200, 400, 401, 403 and 503 |
| Event stub | RWB-P3-E1030-CON (this story) | One `CaseTransferred` with reasonCode REBALANCE on a local topic with the CloudEvents envelope |
| Decision-record fake | RWB-PLT-E1027-CON | The record write and the topic publish |
| Decision contract fake | RWB-P7-E1027-CON | The central ledger's collection of the record |
| Reference-data fake | RWB-P3-E1043-CON | The queue and member rows in force |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 0 | The measure read, the queue case read and the case read |
| Kafka | Published 1 event and 1 decision record; consumed 1 event declared | `rwb.case.events.v1`, `rwb.decision-record.v1` |
| Temporal | 1 workflow, 2 activities and 1 Schedule declared | `DailyCaseRun`, `rebalance`, `takeQueueMeasures` |
| File | None | No file declared; the lake copy is removed (DP-17) |

### 13. Solution plan

**Artifacts**

| Artifact | Path | Format |
|---|---|---|
| OpenAPI document | `contracts/rwb-case/openapi-queues-v1.yaml` | OpenAPI 3.1 |
| AsyncAPI document | `contracts/rwb-case/asyncapi-queues-v1.yaml` | AsyncAPI 3.0 |
| Schemas | inside the two documents, named components | JSON Schema 2020-12 |
| Fake server | `contracts/rwb-case/fake-queues/` | Generated server plus the hand-written examples |
| Contract test suite | `contracts/rwb-case/tests-queues/` | Schemathesis or equivalent, run in the pipeline |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the run record and rerun surface are Not specified in the source documents (GAP-2206; ASM-3622) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

As a contract story this one has no build dependency (§R5.7 rule 1). The rows above are the patterns the capability applies; the dependencies they add are carried by RWB-P3-E1030-APP and by the platform contract stories themselves.

**Build steps**

1. Draft `QueueMeasure` from the legacy record, field for field, and add `status` from LOV-SNAPSHOT-STATUS.
2. Add the three read operations and the `Case`, `CasePage` and `Assignment` schemas.
3. Add the error envelope and the five message examples.
4. Write the AsyncAPI document with the CloudEvents envelope and `CaseTransferred`.
5. Declare the run artifact: the Schedule, the workflow and the two activities, with their inputs and outputs.
6. Generate the fake and the contract test suite; run the five tests of section 16.

**Done when.** Both documents validate, the fake serves every example, the five contract tests pass, the run artifact section names the Schedule and the two activities, and the document is published in the service contract catalogue as version 1.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Cases left without an owner | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-028 | Service level breach alert | {count} cases in {queue} are past their service level. |
| MSG-P3-029 | Snapshot does not reconcile | The queue measures for {date} were not published: {check}. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Each identifier is bound to one status in the document: MSG-P4-002 to 403, MSG-P7-003 to 503, and MSG-P3-011, MSG-P3-028 and MSG-P3-029 to the body of the run result and of the alert, never to a read response.

### 15. Screens and states

No screen. The document is the input to the gateway-bff composite route (DP-19) that serves the case list and the queue reads, and to the reporting consumer's client. It states, for the screen's benefit, that only a `PUBLISHED` snapshot is returned and that a queue with no cap is reported with zero moves.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1030-CON-01 | AC1 | Contract | OpenAPI 3.1 validation of the three read operations and their error statuses |
| TC-P3-E1030-CON-02 | AC2 | Contract | `QueueMeasure` field list, the three status values, the depth-to-case-count rule, the personal-data scan and the source-table names |
| TC-P3-E1030-CON-03 | AC3 | Contract | AsyncAPI validation; the message name, the envelope, the key and the payload scan |
| TC-P3-E1030-CON-04 | AC4 | Component | The problem envelope on all five examples; the run declaration: Schedule, workflow, activities and the once-per-date statement |
| TC-P3-E1030-CON-05 | AC5 | Component | The nine sub-tables present, each owner matched against the ownership map, the fake published with the document |
| TC-P3-E1030-CON-06 | AC5 | Component | The six owned tables of 12.7: each owner P3, each named in `rwb_case`, no table of another service |
| TC-P3-E1030-CON-07 | AC6 | Contract | Versioning: a breaking change is a new path version and v1 is not changed in place |
| TC-P3-E1030-CON-08 | AC7 | Contract | Section 8 rule table: each rule BR1 to BR8 names a criterion and a test case that exist in this document |
| TC-P3-E1030-CON-09 | AC8 | Contract | Every provided operation declares 404 with the error envelope |
| TC-P3-E1030-CON-10 | AC9 | Component | Retry and timeout of rebalance: no case moved twice; events only, no measure feed and no file |
| TC-P3-E1030-CON-11 | AC10 | Component | A disallowed status change is refused and not published; the refusal uses the error envelope |

The legacy test cases TC-E1-030-01 to TC-E1-030-12 stay with the build story (section 16 of RWB-P3-E1030-APP); they are recorded in this key's fragment for traceability and are not renumbered here.

### 17. Guardrails

- No business value in the document that belongs to data: the cap, the method and the measure definitions are rows, and the document references the status list by name.
- No personal data in any example, event payload or response: examples use case numbers, user identifiers and codes only.
- No table of another service is named as a source (DP-01).
- No measure feed and no file is declared (DP-17); the document states that reporting projects from events.
- The document is versioned and never edited in place; a breaking change is a new path version.
- The fake is generated from the document, so a drift between document and fake fails the pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-17, FEAT-CWC-18, FEAT-WKM-11 | All recovery processes | R-UNI-19, R-UNI-30 | TC-P3-E1030-CON-01, TC-P3-E1030-CON-03, TC-P3-E1030-CON-04 |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | Epic 1, 3.3; Program, 5.1 | FEAT-RPT-02 | 15 Manage performance, data and AI | None | TC-P3-E1030-CON-02, TC-P3-E1030-CON-05 |

| Legacy reference | Where it is kept |
|---|---|
| `QueueMeasureView` field list | Sections 1, 4, 11, 12.1, 16 |
| Event CaseTransferred (EV-04) | Sections 4, 12.3, 16 |
| MSG-P3-011, MSG-P3-028, MSG-P3-029, MSG-P7-003, MSG-P4-002 | Section 14 |
| `GET monolith-base/cases` used for the reconciliation | Sections 11, 12.1 |
| JOB-06 trigger 06:30 and the legacy rerun call | Sections 4, 5, 11, 12.6 |
| Legacy key RWB-E1-030, story RWB-P3-E1030-APP, contract RWB-P3-E1030-CON, deployment RWB-P3-E1030-OPS | Metadata, section 12 |

### 19. Out of scope

- The rebalancing capability itself, its tests and its feature flag (RWB-P3-E1030-APP).
- The chart, the Schedule creation, the migration, the metrics, the alerts and the runbook (RWB-P3-E1030-OPS).
- The assignment engine and the timer capability (RWB-P3-E1020-APP, RWB-P3-E1028-APP).
- The gateway-bff composite route itself and the Epic 2 team queues screen (RWB-E2-011).
- The reporting projection and the Power BI report (rwb-reporting, RW-BIANAL).
- The central decision ledger and its own contract (rwb-decision).
