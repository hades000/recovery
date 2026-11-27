# RWB-PLT-TE006-CON Outbox and retry for outbound work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-TE-006 for the platform library RWB-PLT-LIB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 91 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-PLT-TE006-CON-16) |
| Contract version | v1 (the /v1 path this story builds against) |
| Library object template version | Not specified in the source documents (GAP-1232) |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON; RWB-P3-E1042-CON; RWB-P3-E1043-CON |
| Shared platform baseline (wave 0, not H) | RWB-PLT-E1027-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1071-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON |
| Integration dependencies | None |
| Event and Schedule boundary | No outbox producer, no event consumer, no inbox row and no Schedule in this slice (GAP-1899) |
| Admin endpoint host | rwb-integration serves the outbox admin endpoints against the library (GAP-3193) |
| External dependencies | Kafka hosting on the bank platform not yet confirmed by ACE, Azure Event Hubs Premium fallback (GAP-0011) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract of the outbox and inbox library — the `OutboxWriter`, `OutboxConsumer` and `IdempotencyGuard` interfaces with their exceptions, the DDL contract of the four library tables that every service creates in its own schema, the CloudEvents 1.0 envelope and the caseId key, the inbox dedupe rule, the retry and dead-letter contract with its alert rule, the versioning and compatibility rule, and the fakes — instead of the monolith's single `recovery` schema outbox and its in-process consumer interface**, so that **all 19 services build their events against one published contract from Day 1, no service hand-writes an outbox, inbox or idempotency table, and every consumer can be built and tested before the producer exists** (Template and Rules §R6, DP-09).

### 2. Business rationale

In the monolith the outbox was two tables in the one `recovery` schema and the consumer was a Java interface implemented in the same process (legacy section 12). Under Arch v5 each of the 19 services writes its own schema and its own Flyway sequence, publishes to its own topic and consumes through its own consumer group (Arch v5 slides 11, 20, 22, 29). The library therefore becomes a contract before it becomes code: the three interfaces fix the transaction boundary and the failure shape, the DDL contract fixes the four table shapes each service applies in its own schema, and the envelope and dedupe rules fix what travels on the wire.

This contract is the DP-09 dependency of every service CON and APP story. Publishing it on Day 1 lets a service build its outbox row, its inbox and its consumer against a frozen interface and a fake, while the producer of the event it consumes may still be two waves away. It also carries the two rules that keep the split honest: the library joins the caller's transaction and never opens its own, and it raises no case event, no task and no decision record on another service's behalf.

The retry contract is the Kafka retry-topic ladder of 1 min, 10 min and 1 h and then the dead-letter topic with an alert and a replay tool (Arch v5 slides 11 and 22). The legacy 3 retries at 1, 5 and 15 minutes is the lower-ranked source and is kept only in the preserved criteria of the APP story and exercised through configuration; the conflict is recorded in GAP-1416 with its assumptions.

It supports REQ-DRI-007 and the two non-functional targets of the legacy story: no event is lost, and every delivery is retried on a defined schedule and ends in an exception path with an owner.

### 3. Preconditions

- The platform library has an artifact name, a version scheme and a publication channel in the service template; the channel itself is Not specified in the source documents (GAP-1416; ASM-2475).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions, so the DDL contract is applied by each service's own sequence in its own schema (DP-15).
- RWB-PLT-E1027-CON is published: the local decision-record library and topic `rwb.decision-record.v1`, which the contract refers to and does not duplicate (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters and reference-data clients that carry the recipient list and the retry windows (DP-06, DP-07).
- The Kafka platform of RWB-PLT-EVT provides one event topic per service, its three retry topics and its dead-letter topic, and the schema registry in BACKWARD mode; the contract refers to those names and does not provision them.
- The Ownership Map ruling stands: the four tables are owned by PLT and created in each service's own schema, not once in an rwb-integration schema. The per-service table list that a DB story applies is Not specified in the source documents (GAP-1416; ASM-2475).
- No build dependency: the contract is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Fix the three interfaces: `OutboxWriter.publish`, `OutboxConsumer.consume` and `IdempotencyGuard.firstTime`, with their input and output types and their exceptions.
2. Fix the transaction rule in the interface documentation: a call joins the caller's transaction, opens none, and throws before any write when the key exists.
3. Fix the DDL contract of the four tables, with the keys, the checks, the indexes and the standard columns, as one template that each service applies in its own schema.
4. Fix the envelope: CloudEvents 1.0 in binary mode, `ce_specversion` 1.0, `ce_id`, `ce_type` as the event name with its schema version, `ce_source` as the owning service, `ce_subject`, `ce_time`, the W3C trace header and the caseId record key.
5. Fix the inbox rule: the consumer records `ce_id` with its consumer group in `processed_event` in the same transaction as its own change, and a repeated `ce_id` has no second effect.
6. Fix the retry and dead-letter contract: the three retry windows, the dead-letter topic, exactly one alert per dead-letter record, the replay tool as the recovery path and the rule that the library raises no case event, no task and no decision record.
7. Fix the versioning rule: major version 1 of the interfaces and the envelope, backward-compatible event schemas in the registry, and a breaking change as a new major version and a new `ce_type`.
8. Publish the fake of the three interfaces and the fixture set, and wire the contract tests into the build of every service that depends on the library.
9. Publish the contract document with the nine tables of section 12 and hand it to every service CON story as the DP-09 dependency.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A service implements the writer outside its own transaction | The contract test fails and the build is refused; no partial publish is accepted | None | AC1 |
| X2 | A service creates the tables in another service's schema | The boundary test fails on the cross-schema reference and the build is refused | None | AC2 |
| X3 | An event body does not validate against the registry | The relay refuses to publish and the delivery keeps its state with the error code | None | AC3 |
| X4 | The same `ce_id` is delivered twice | The inbox drops the second delivery and the consumer answers OK | None | AC4 |
| X5 | A record fails the third retry | The record goes to the dead-letter topic and one alert is raised; the replay tool is the recovery path | None | AC5 |
| X6 | A schema change breaks a consumer | The registry refuses the change in BACKWARD mode and a new major version and `ce_type` are required | None | AC6 |
| X7 | A service hand-writes an outbox table instead of applying the template | The drift check against the DDL contract fails and the build is refused | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; the contract refers to the platform, the case and the decision contracts by name only |
| Negotiable | The artifact channel and the fixture set are agreed with the platform team; the interfaces, the table shapes, the envelope and the retry windows are fixed by the target architecture |
| Valuable | Unblocks every service CON and APP story that publishes or consumes an event, from Day 1 |
| Estimable | Three interfaces, one DDL template, one envelope rule, one dedupe rule, one retry contract and the fakes |
| Small | Fits two weeks with its contract tests |
| Testable | Every criterion below is a contract test that the build of a consuming service runs |

### 7. Acceptance criteria

```gherkin
Feature: Outbox and inbox library contract

  Background:
    Given the platform library contract document is published with major version 1
    Given the 19 services have one schema and one login each

  Scenario: AC1 The three interfaces are published and stable (new, D-RCV-60)
    Given the contract jar of the platform library is published
    When a service compiles against it
    Then OutboxWriter.publish(OutboxEvent event) returns a UUID and joins the caller's transaction
    Then OutboxEvent carries eventType, schemaVersion, caseId, payload, actorRef and idempotencyKey
    Then publish throws DuplicateOutboxKeyException when the idempotency key already exists
    Then OutboxConsumer.consume(EventHeader header, JsonNode payload) returns OK or FAILED with a code
    Then IdempotencyGuard.firstTime(String consumer, String idempotencyKey) returns a boolean
    Then no method opens its own transaction and no method calls another service

  Scenario: AC2 The DDL contract creates four tables in each service schema (new, D-RCV-60)
    Given the DDL template of the library
    When a service applies it through its own Flyway sequence
    Then it creates outbox_event, outbox_delivery, processed_event and idempotency_key in that service's own schema
    Then outbox_event carries the unique key on idempotency_key and the unique key on (case_id, case_seq)
    Then outbox_delivery carries the unique key on (event_id, consumer), the status check on PENDING, RETRYING, DELIVERED and EXCEPTION and the due index on next_attempt_at
    Then processed_event carries the unique key on ce_id and the consumer group
    Then idempotency_key carries the unique key on scope and key with the stored response
    Then no table names another service's schema and no key crosses a schema boundary

  Scenario: AC3 The envelope and the record key are fixed (new, D-RCV-60)
    Given a record the relay is about to publish
    When it is published to the owning service's topic rwb.<short>.events.v1
    Then the CloudEvents 1.0 binary-mode headers ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject and ce_time are set
    Then ce_type is the event name rwb.<short>.<Event>.v1
    Then ce_source is the owning service
    Then the record key is caseId and the traceparent header carries the W3C trace context
    Then the body is validated against the registry before publish and carries IDs and facts only
    Then the producer is idempotent with acks=all and the schema compatibility is BACKWARD

  Scenario: AC4 The inbox dedupe and the idempotency rule are fixed (new, D-RCV-60)
    Given a consumer that subscribes to an event of another service
    When the same ce_id arrives twice
    Then the consumer records it in processed_event in the same transaction as its own change
    Then the second delivery has no second effect and answers OK
    When a caller publishes with an idempotency key that already exists
    Then one event exists and the second call throws DuplicateOutboxKeyException

  Scenario: AC5 The retry and dead-letter contract is fixed (new, D-RCV-60)
    Given a consumer that fails
    When the first, the second and the third attempt fail
    Then the record moves through the retry topics at 1 min, 10 min and 1 h
    Then after the third retry the record goes to the dead-letter topic and exactly one alert is raised to the platform administrator
    Then the replay tool is the recovery path of a dead-letter record
    Then the library raises no case event, no task and no decision record of its own

  Scenario: AC6 Versioning, compatibility and the fake (new, D-RCV-60)
    Given the contract declares major version 1 of the interfaces and the envelope
    When an event schema changes
    Then a backward-compatible change is accepted by the registry and the ce_type version stays the same
    Then a breaking change needs a new major version and a new ce_type
    Then the library fake answers OutboxWriter, OutboxConsumer and IdempotencyGuard for the contract test of every service
    Then the contract test of each consuming service runs against the published jar and fails on any drift from section 12

  Scenario: AC7 The outbox row and its deliveries share the caller's transaction (BR1) (new, D-RCV-60)
    Given a service that changes a case and publishes one event in the same call
    When the transaction rolls back
    Then neither the change nor the outbox_event and outbox_delivery rows exist
    Then the outbox rows are written in the caller's schema and no other schema

  Scenario: AC8 The event carries a CloudEvents id and a repeat is dropped (BR2) (new, D-RCV-60)
    Given an event published with a CloudEvents id and an idempotency key
    When a consumer receives a repeat with the same ce_id
    Then processed_event or IdempotencyGuard drops the repeat and the consumer answers OK

  Scenario: AC9 Delivery is at least once with one consumer group and one delivery state per recipient (BR3) (new, D-RCV-60)
    Given an event with two recipients
    When the relay publishes it and one delivery is not acknowledged
    Then each recipient has its own consumer group and its own outbox_delivery row
    Then the unacknowledged delivery is delivered again

  Scenario: AC10 Events for one case reach each recipient in write order by caseId (BR4) (new, D-RCV-60)
    Given two events for the same case written in order
    When they are published
    Then both use the caseId record key
    Then each recipient receives them in the order they were written

  Scenario: AC11 A failed record climbs the retry topics and then reaches the dead-letter topic with one alert (BR5) (new, D-RCV-60)
    Given a consumer that fails
    When the record fails on every attempt
    Then the record climbs the retry topics at 1 min, 10 min and 1 h
    Then the record then goes to the dead-letter topic with one alert and the replay tool is its recovery path

  Scenario: AC12 The library raises no case event, no task and no decision record (BR6) (new, D-RCV-60)
    Given the library fake in a contract test of a consuming service
    When the library handles an event
    Then no case event, no task and no decision record is raised by the library
    Then the consumer's owning service raises them through its own contract

  Scenario: AC13 Payloads hold references and codes only and carry the schema version and trace context (BR7) (new, D-RCV-60)
    Given an outbox_event to publish
    When it is validated against the registry before publish
    Then the payload holds references and codes and no personal data
    Then the event carries its schema version and the envelope carries the W3C trace context

  Scenario: AC14 A contract change is backward compatible or a new major version with a migration note (BR8) (new, D-RCV-60)
    Given a change to an event schema
    When the change is submitted to the registry
    Then a backward-compatible change is accepted
    Then a breaking change is a new major version with a migration note

  Scenario: AC15 The recipient list, the owners and the retry windows are configuration (BR9) (new, D-RCV-60)
    Given the library code and its published interfaces
    When the recipient list, the owners and the retry windows are read
    Then they come from configuration behind the published interfaces
    Then no recipient, owner or retry window value is held in the library code

  Scenario: AC16 A disallowed status change is refused (new, D-RCV-60)
    Given an outbox delivery row in one of the statuses in the outbox_delivery status check of section 12.7
    When a status change the model does not allow is attempted
    Then the change is refused and the row keeps its status
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The outbox row and its deliveries are written in the caller's transaction and the caller's schema: no event without the change and no change without the event | events.txt Rules, Transactions; DP-01; DP-09 |
| BR2 | The event carries a CloudEvents id and an idempotency key unique in the caller's outbox; a consumer drops a repeat through its inbox `processed_event` or `IdempotencyGuard` | events.txt Rules, Duplicates; R-UNI-40; Arch v5 slides 11 and 22 |
| BR3 | Delivery is at least once; each recipient has its own consumer group and its own delivery state | events.txt Rules, Delivery; Arch v5 slide 21 |
| BR4 | Events for one case reach each recipient in the order they were written, through the caseId record key | events.txt Rules, Ordering; Arch v5 slide 21 |
| BR5 | A failed record climbs the retry topics at 1 min, 10 min and 1 h and then goes to the dead-letter topic with one alert and the replay tool. One retry table for the platform: three retries per outbound item and then the exception queue of P2 rwb-integration; for events, retry topics at 1, 10 and 60 min then the .dlt topic with an alert; for Temporal, 10 activity attempts with a 1 s initial interval doubling, and the non-retryable error list Not specified in the source documents (GAP-1666) | Arch v5 slides 11 and 22; NFR-026; REQ-DRI-007; Temporal and Drools Design slide 28 |
| BR6 | The library raises no case event, no task and no decision record; the consumer's owning service does that through its own contract | R-UNI-33; R-UNI-35; R-UNI-36; GAP-1416 |
| BR7 | Payloads hold references and codes and never personal data; the event carries its schema version and the envelope its trace context | events.txt Rules, Payload and Versioning |
| BR8 | A contract change is backward compatible in the registry, and a breaking change is a new major version with a migration note | Arch v5 slide 11 |
| BR9 | The recipient list, the owners and the retry windows are configuration behind the published interfaces, never values in the library code | Principle 1; DL11 |

### 9. State transitions

The contract fixes the delivery states and their legal moves; no case status is held by the library.

| From | Event | Condition | To |
|---|---|---|---|
| Contract version 1 | A backward-compatible change | The registry accepts the schema and the envelope is unchanged | Contract version 1, new schema minor version |
| Contract version 1 | A breaking change | An interface, a table shape or an envelope attribute changes | Contract version 2 with a migration note |
| Delivery PENDING | Publish acknowledged | None | Delivery DELIVERED |
| Delivery PENDING | Recipient or broker fails | Retries left | Delivery RETRYING in the retry topic of the window |
| Delivery RETRYING | Recipient fails | No retries left | Record in the dead-letter topic |
| Event in the dead-letter topic | Replay through the replay tool | None | Delivered again under the same `ce_id`, dropped where already processed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform library team, owning the template | Owns the interfaces, the DDL template, the envelope rule and the fakes; publishes version 1 and later versions |
| The owning service of each consumer | Implements `OutboxConsumer` and `IdempotencyGuard` under its own consumer name and raises its own case events, task and decision record |
| Platform team | Owns the retry-topic and dead-letter settings, the alert and the replay tool that the contract refers to |
| ACE data team | Owns the per-service schema, login and grants that the DDL contract assumes |
| No approval level from the delegation of authority applies | The contract takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 to DF-OPS-197 | outbox_event | all fields, fixed by the DDL contract | Write, in the caller's schema |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | all fields, fixed by the DDL contract | Write, in the caller's schema |
| DF-DEC-001 to DF-DEC-018 | decision_record (local library) | all fields | Not held by this contract; written by the owning service |
| DF-CAS-001 | recovery_case | id | Read only as the envelope subject and the record key, through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary. `processed_event` and `idempotency_key` have no field ID of their own in the source; they are library objects owned by PLT and created in each service's schema. The `outbox_event` and `outbox_delivery` columns are fixed by DF-OPS-189 to DF-OPS-206; the column set of `processed_event` and `idempotency_key` is Not specified in the source documents and is published as the working read (GAP-1416; ASM-2475).

The CloudEvents attributes ce_specversion, ce_id, ce_type, ce_source, ce_subject and ce_time are envelope headers of the CloudEvents 1.0 attribute set. They are not fields of the Logical Data Model or Data Classification and are not rows of this table (DOR-RWB-PLT-TE006-CON-7).

Contract shape (GAP-1416): the library is one published artifact with a major version. It exposes three interfaces, OutboxWriter.publish, OutboxConsumer.consume and IdempotencyGuard.firstTime, with the exceptions set out in the legacy RWB-TE-006 section 12. Its artifact name and publication channel are Not specified in the source documents (GAP-1416). Events carry CloudEvents 1.0 attributes and the caseId record key (BR2, BR4). The retry ladder is 1 min, 10 min and 1 h, then the dead-letter topic with one alert and the replay tool (BR5). Case-step events, tasks and decision records stay with the owning service (BR6).

### 12. Contract

#### 12.1 REST operations provided

None — the library has no REST surface. The admin read and resend operations belong to P2 rwb-integration in the Ownership Map.

#### 12.2 REST operations consumed

None — the library joins the caller's transaction and calls no service.

#### 12.3 Events published

None of its own — the contract fixes the envelope and the key for the records that the caller's schema relays to `rwb.<short>.events.v1`; the library publishes no event type of its own.

#### 12.4 Events consumed

None of its own — the contract fixes the inbox rule for the events each service subscribes to under its own consumer group in its own `processed_event` table.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity; the relay is a background worker in each service (plain code, no Temporal Schedule).

#### 12.6 Schedules

None — the contract states that the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay and not a Temporal Schedule (GAP-1416; ASM-2476).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| outbox_event | PLT | Contract shape of the published fact; unique key on `idempotency_key` and on `(case_id, case_seq)` |
| outbox_delivery | PLT | Contract shape of one event and recipient; unique key on `(event_id, consumer)`, status check and due index |
| processed_event | PLT | Contract shape of the inbox; unique key on `ce_id` and the consumer group |
| idempotency_key | PLT | Contract shape of the stored response per scope and key |

Each service applies the same template in its own schema under its own login, through its own Flyway sequence; the library does not create a schema, a login or a table in another service's schema (DP-01, DP-15). The `outbox_event` and `outbox_delivery` shapes carry DF-OPS-189 to DF-OPS-206; the column set of `processed_event` and `idempotency_key` is the working read of this contract, because no source defines it (GAP-1416; ASM-2475).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Library interface fake | `OutboxWriter`, `OutboxConsumer`, `IdempotencyGuard` | A writer that records the call and throws `DuplicateOutboxKeyException` on a repeated key; a consumer that answers OK or FAILED on demand; a guard that answers first time or not |
| Registry fake | The schema registry | BACKWARD mode with one accept and one refusal fixture |
| Kafka retry and dead-letter fake | The three retry topics and the dead-letter topic | A record that fails three times and lands in the dead-letter topic with one alert |
| rwb-case case-event and task fake | The P3 contract | Task code RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM; RETRY_LIMIT_REACHED and RETRY_SUCCEEDED accepted |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The contract adds no path and calls no service |
| Kafka | None published and none consumed by the library itself | The contract fixes the envelope, the caseId key, the three retry topics and the dead-letter topic for the records each service relays |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | No file is read or written; an outbound file is a claim-check call through the rwb-integration contract |

### 13. Solution plan

**Package.** Shared library contract artifact of the platform, the three interfaces in `th.co.scb.ace.workbench.recovery.platform.api`, the DDL template as a resource, the envelope and dedupe rules in the contract document; the implementation is the APP story of this legacy key.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract fixes that each service applies the four tables in its own schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the contract hands the record to the owning service and does not write it | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the recipient list and the retry windows are parameters behind the interface | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the recipient and event-type lists are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. This story is the contract of that library | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay, not a Temporal Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the recipient is reached through its published contract or its topic, never in process | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract states that the library adds no path and the admin path belongs to P2 | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the DDL contract is applied by each service's own sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route; the admin screen is out of scope | H RWB-PLT-N001-CON |

Dependencies and reporting (GAP-1161, GAP-3075, GAP-2448, GAP-2569): build against a fake of each contract on Day 1 and replace each fake with the published contract in the same iteration. Platform contracts added by the pattern table (wave 0 shared baseline): RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1042-CON (DP-06), RWB-PLT-E1043-CON (DP-07), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19). P3 C rows: RWB-P3-E1042-CON (DP-06) and RWB-P3-E1043-CON (DP-07). The pattern table also names the P4 authorise contract RWB-P4-E1037-CON. The DP-09 row names this story's own key and is no build dependency. Fake names for the reference-data and decision-record contracts are Not specified in the source documents (GAP-1161). This library declares no rwb-reporting event: rwb.reporting.ReportPublished.v1 on rwb.reporting.events.v1 is not declared here, and any freshness event is for the reporting read-model owner to raise as its own story (GAP-2569).

**Hardware and software change.** The contract moves the outbox, inbox and idempotency tables from one set in the monolith's `recovery` schema to a library template that every service applies in its own schema; it fixes the publish path as each owner's topic with CloudEvents 1.0 and an idempotent producer; it fixes retry as the Kafka retry-topic ladder and the dead-letter topic with an alert and a replay tool; and it fixes that the case-step and decision-record effects stay in the owning service's code through its contracts. No new hardware is implied: the relay runs in each service's own pods on the existing AKS cluster and the tables sit in the existing ACE PostgreSQL server.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `OutboxWriter` | Published interface | One method with its `OutboxEvent` input and its `DuplicateOutboxKeyException`; joins the caller's transaction |
| `OutboxConsumer` | Published interface | One method with the `EventHeader` and the payload, returning `ConsumeResult` OK or FAILED with a code |
| `IdempotencyGuard` | Published interface | One method answering whether a consumer has already acted on a key |
| OutboxDdlTemplate | Resource | The DDL contract of the four tables, keys, checks and indexes |
| EnvelopeSpecification | Document | The CloudEvents 1.0 binary-mode attribute set, the caseId key, the trace header and the `ce_type` shape |
| InboxSpecification | Document | The dedupe rule against `processed_event` in the consumer's own transaction |
| RetrySpecification | Document | The three retry windows, the dead-letter topic, the one-alert rule and the replay path |
| Library fake and fixtures | Test asset | The three interfaces and the fixture set used by every consuming service |

**Build steps**

1. Write the three interfaces and the exception types; run the compile and drift test of a sample service (AC1).
2. Write the DDL template and apply it twice, in two throwaway schemas, to prove the reusability and the absence of cross-schema references (AC2).
3. Write the envelope specification and the registry check; test the headers, the key and one accepted and one refused schema (AC3).
4. Write the inbox specification and the idempotency rule; test a repeated `ce_id` and a repeated key (AC4).
5. Write the retry and dead-letter specification with the one-alert rule and the replay path; test the three windows and the dead-letter landing (AC5).
6. Publish the fake and wire the contract test into the build of the dependent services; test the drift refusal (AC6).
7. Publish the contract document with the tables of section 12 and record the version and the compatibility rule.

**Done when.** The six criteria pass as contract tests, the tables of section 12 are complete and name their owner from the Ownership Map, and the APP story of this legacy key builds against the published jar.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-005 | A delivery is queued to send again through the P2 admin API | Saved. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION, through the P2 admin API | Only an item in the exception queue can be sent again. |
| MSG-P7-003 | The owning service cannot write its decision record at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Platform administration right calls the P2 admin API | You cannot {action} here. Your role does not include it. |

The library itself raises no user-facing message; these are the messages of the operations that the contract refers to, unchanged from the legacy story. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen of its own. The contract has no user interface: the admin read and resend screen and SCR-44 Interface and job monitor belong to P2 and Epic 2, and the library adds no route and no state to any screen (DP-19).

SCR-44 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-1460).

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE006-CON-01 | AC1 | Contract | A sample service compiles against the jar; a writer in its own transaction and a writer that opens its own transaction |
| TC-PLT-TE006-CON-02 | AC2 | Component | The template applied in two throwaway schemas; the unique keys, the status check and the due index asserted |
| TC-PLT-TE006-CON-03 | AC3, AC5 | Contract | One record published with the full CloudEvents header set, one schema accepted and one refused, three failed attempts and a dead-letter landing with one alert |
| TC-PLT-TE006-CON-04 | AC4 | Component | The same `ce_id` twice and the same idempotency key twice |
| TC-PLT-TE006-CON-05 | AC6 | Contract | A backward-compatible change accepted, a breaking change refused, and the drift test against the published jar |
| TC-PLT-TE006-CON-06 | AC7, BR1 | Component | A case change and its outbox rows written in one transaction and rolled back; rows checked in the caller's schema only |
| TC-PLT-TE006-CON-07 | AC8, BR2 | Component | The same ce_id delivered twice to a consumer |
| TC-PLT-TE006-CON-08 | AC9, BR3 | Contract | One event with two recipients and one unacknowledged delivery |
| TC-PLT-TE006-CON-09 | AC10, BR4 | Contract | Two ordered events for one caseId |
| TC-PLT-TE006-CON-10 | AC11, BR5 | Contract | A consumer failing on every attempt, a dead-letter landing and one alert |
| TC-PLT-TE006-CON-11 | AC12, BR6 | Contract | The library fake handling one event, with no case event, task or decision record raised |
| TC-PLT-TE006-CON-12 | AC13, BR7 | Contract | An outbox payload of references and codes only, and an envelope with trace context |
| TC-PLT-TE006-CON-13 | AC14, BR8 | Contract | A backward-compatible schema change accepted and a breaking change refused without a new major version |
| TC-PLT-TE006-CON-14 | AC15, BR9 | Contract | The recipient list and the retry windows read from configuration |
| TC-PLT-TE006-CON-15 | AC2 | Component | Boundary values for each table of §12.7 (ASM-3438): the unique keys, the status check values accepted and refused, and the due index |
| TC-PLT-TE006-CON-16 | AC16 | Component | Not specified in the source documents (NEWAC-RWB-PLT-TE006-CON-AC8) |
| TC-PLT-TE006-CON-17 | Event and Schedule boundary | Contract | No outbox producer, consumer, inbox row or Schedule is created by this slice |

### 17. Guardrails

- No business value in the contract: the recipient list, the owners and the retry windows are configuration behind the interfaces.
- No personal data in the envelope, in a fixture or in a log; the body carries references and codes only.
- No cross-schema reference in the DDL template and no foreign key across services; the boundary test fails the build.
- The contract states that the library raises no case event, no task and no decision record of its own.
- A published version is never edited in place; a breaking change is a new major version with a migration note.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-PLT-TE006-CON-01 to TC-PLT-TE006-CON-05 |

### 19. Out of scope

- The implementation of the writer, the consumer, the relay and the DDL template: the APP story of this legacy key.
- The Kafka topics, the retry topics, the dead-letter topic and the registry themselves: RWB-PLT-EVT.
- The admin read and resend API and its screen: P2 rwb-integration, SCR-44 and Epic 2.
- The decision-record library and the central ledger: RWB-PLT-E1027-CON and RWB-P7-E1027-CON.
- The per-service schema, login and grants: RWB-PLT-DB.
- The retry values as a business decision: DL11, and the conflict recorded in GAP-1416.

