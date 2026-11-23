# RWB-PLT-TE006-APP Outbox and retry for outbound work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-006 for the platform library RWB-PLT-LIB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-PLT-LIB-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-TE006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON, RWB-P2-E1007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

### 1. Story

As a **platform library engineer**, I want **the outbox, inbox and idempotency library that all 19 services use from the service template — an `OutboxWriter` that writes the event and one delivery row per listed recipient in the caller's own transaction, inside the caller's `rwb_<short>` schema under the caller's own login, an `OutboxConsumer` with an inbox that drops a repeated delivery, a continuous per-service outbox relay that publishes to the owning service's Kafka topic with the CloudEvents 1.0 envelope and an idempotent producer, and a retry path carried by the Kafka retry topics and the dead-letter topic with an alert and a replay tool — instead of the monolith's single `recovery` schema tables, its shared Quartz sender JOB-11 and its in-process consumer call**, so that **no outbound fact is lost when a service, Kafka or a recipient is down, nothing is sent for a change that did not commit, and every service's outbox, inbox and idempotency rows live in its own schema with its own owner** (Template and Rules §R6, DP-09, DP-01).

### 2. Business rationale

The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. In the monolith one outbox table sat in the single `recovery` schema, one clustered Quartz job, JOB-11, delivered the rows to consumers and one decision log writer recorded the move to the exception queue. Under Arch v5 the same guarantee has to hold when there are 19 services, 19 schemas and 19 logins: the outbox row must be written in the same transaction and in the same schema as the change it describes, because a service may not read or write another service's tables (DP-01), and the delivery has to cross a Kafka topic instead of an in-process call (DP-09, DP-11).

This story is that library, and it is the DP-09 dependency of every service CON and APP story in waves 1 to 4. It keeps the four properties the legacy story measured — written with the change, delivered at least once, ordered per case and per recipient, retried on a defined schedule and moved to an exception path with a task for a named owner (REQ-DRI-007) — and it adds the four that only a microservice shape needs: the event leaves through the owner's own topic with a CloudEvents 1.0 envelope and an idempotent producer; each consumer deduplicates through an inbox table in its own schema; a failed delivery climbs the Kafka retry-topic ladder and ends in the dead-letter topic with an alert and a replay tool; and the case-step events and the decision record stay in the code of the service that owns the case step, reached through its published contract, because the library may not raise a case event or write a decision record on another service's behalf.

The retry schedule is the one point where the two sources disagree. The legacy story holds the retry settings as configuration with 3 retries at 1, 5 and 15 minutes; Arch v5 slide 22 and slide 11 fix the Kafka retry topics at 1 min, 10 min and 1 h and then the dead-letter topic. §R3 R-PREC puts the Arch v5 catalogue slides first, so the Kafka ladder wins and the legacy values are kept only in the preserved criteria text and exercised through the configuration of section 13; the conflict is recorded in GAP-1415 with its assumptions.

The measure is unchanged: the count of outbox deliveries that reach the exception or dead-letter path over one day, with a target of zero.

### 3. Preconditions

- RWB-PLT-TE006-CON is published (this story's contract deliverable): the `OutboxWriter`, `OutboxConsumer` and `IdempotencyGuard` interfaces, the DDL contract of the four library tables, the CloudEvents 1.0 envelope and the caseId key, the inbox dedupe rule, the retry and dead-letter contract, the versioning rule and the fakes.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15), so the library DDL template is applied by each service in its own schema and not by one shared migration.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger contract behind it.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library (DP-06, DP-07); RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the rwb-case contracts behind them.
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, so a service can still choose an event-started workflow where one is warranted (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19); the admin screen itself is out of scope.
- RWB-P2-E1007-CON is published: the rwb-integration contract, so the outbound file path that a consumer such as "win-dispatch" calls is a published contract and not an in-process call.
- The ACE Kafka platform is provisioned with one event topic per service, its three retry topics and its dead-letter topic, and the schema registry is in BACKWARD mode (Arch v5 slides 11, 21, 22). The retention, partition and replication settings are the platform settings, not values of this story.
- The four table names `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are owned by the platform library and created in every service schema under the Ownership Map ruling; which per-service database story applies each copy is Not specified in the source documents (GAP-1415; ASM-2473).
- The exception path of a delivery that keeps failing has no single owner in the sources: the legacy story raises a task and a case event in the same step as the move, while in the target the case-step event and the task belong to the service that owns the case step and the dead-letter path belongs to Kafka and the platform team (GAP-1415; ASM-2474).

### 4. Flow

1. A business service (for example the notice approval in rwb-comms) calls `OutboxWriter.publish` inside its own transaction with the event type (an event of the EV catalogue such as CaseAllocated, or an outbound work request type such as WIN_DISPATCH), the schema version, the case ID where there is one, payload references, the actor reference and the idempotency key.
2. `OutboxWriter` writes one `outbox_event` row into the caller's own schema, under the caller's own login, with the next case sequence for that case, and one `outbox_delivery` row per recipient listed for the event type.
3. The caller's transaction commits the change, the event and its deliveries together, or none of them.
4. The per-service outbox relay (legacy JOB-11, now a continuous background worker in each service, not a Schedule) selects due deliveries with a skip-locked selection, oldest case sequence first, taking only the lowest open sequence per case and recipient.
5. The relay builds the CloudEvents 1.0 envelope in binary mode (`ce_specversion` 1.0, `ce_id`, `ce_type`, `ce_source`, `ce_subject`, `ce_time`), uses the case ID as the record key so one case's events stay in order on one partition, copies the W3C trace context and validates the body against the registry before it publishes.
6. The relay publishes with an idempotent producer and acks=all to the owning service's topic `rwb.<short>.events.v1` and marks the delivery DELIVERED on the broker acknowledgement; if Kafka is down the rows wait in the outbox and nothing is lost.
7. Each consumer records `ce_id` in `processed_event` in its own schema, in the same transaction as its own change, and drops a delivery it has already processed; `IdempotencyGuard.firstTime` answers the same question for a consumer that keeps its own key table.
8. A consumer that fails is redelivered by the Kafka retry topics at 1 min, 10 min and 1 h; a record that fails the third retry goes to the dead-letter topic and raises one alert to the platform administrator.
9. The owning service of the case step raises its own case events (SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED) and its own task through its own contract, and its own decision-record library writes the entry in the same transaction; the library itself raises no case event, no task and no decision record.
10. A record that is not in EXCEPTION is not resent: the resend operation belongs to the admin API of P2 rwb-integration, and a replay of the dead-letter topic is the recovery path of the platform team.
11. The relay records its runs and counts (due, delivered, retrying, dead-lettered) on the platform observability path so that the delivery count in the exception path can be measured daily.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist | None | AC3 |
| X2 | A recipient fails once and then succeeds | The delivery is DELIVERED on the retry; the owning service resumes the case when the recipient holds the case step (R-UNI-35) | None | AC4 |
| X3 | The same idempotency key is published twice | One event exists; the second call throws `DuplicateOutboxKeyException` and changes nothing | None | AC5 |
| X4 | Two relay instances run at once | The skip-locked selection makes each delivery once | None | AC6 |
| X5 | An earlier event for the same case and recipient is failing | Later events for that case and recipient wait behind it | None | AC7 |
| X6 | One recipient fails and another succeeds on the same event | Each recipient's delivery has its own state | None | AC8 |
| X7 | A delivery that is not in EXCEPTION is resent | Refused with 409 by the P2 admin API | MSG-P2-022 | AC9 |
| X8 | An event with no case fails past its retries | The record goes to the dead-letter topic and one alert goes to the platform administrator; the owning service raises no task and no case event | MSG-P2-001 | AC10 |
| X9 | The retry settings are changed | The next attempt uses the new windows; the Kafka ladder is applied through the configuration of section 13 | None | AC11 |
| X10 | The decision record cannot be written when the limit is reached | Nothing changes; the delivery stays RETRYING and is attempted at the next window; an incident is raised (R-UNI-39) | MSG-P7-003 | TC-TE-006-13 |
| X11 | A role without Platform administration U resends a delivery | Refused with 403 by the P2 admin API | MSG-P4-002 | TC-TE-006-12 |
| X12 | Kafka is down | The rows stay PENDING in the outbox of the caller's schema and are published when the broker returns; nothing is lost (Arch v5 slides 22 and 34) | None | AC1, AC6 |
| X13 | The relay instance stops with deliveries in flight | The rows keep their state; a delivery in flight is attempted again at its next window and the consumer drops the repeat through its inbox | None | AC6, AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the library CON story and the platform contract stories; the case step, the decision record and the admin API are reached through their contract fakes, so no other service has to be built first |
| Negotiable | Recipients, owners, retry windows and batch size are configuration; the four tables, the envelope and the key are the published contract and are not negotiated per service |
| Valuable | Gives all 19 services one outbox, inbox and idempotency implementation on Day 1 and removes the shared Quartz sender and the single-schema tables from every service plan |
| Estimable | Four tables, one writer, one consumer, one relay, one DDL template and the fakes |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below uses a stub consumer that fails on demand and the contract fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work

  Background:
    Given consumer "win-dispatch" takes work request WIN_DISPATCH, holds the case step and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged, do not hold the case step and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 Sent after commit (legacy RWB-TE-006 AC1)
    Given a notice approved
    When the transaction commits at 14 December 2026 10:00:00
    Then the outbox holds one WIN_DISPATCH request for case "RW-2026-000601" with one delivery for "win-dispatch"
    Then the header holds the event ID, idempotency key "WIN_DISPATCH:NT-SYN-0601", schema version 1, occurred time and actor
    Then the payload holds notice and case references only, with no name, address or identifier
    Then at the 10:01 run the sender delivers it and "win-dispatch" passes the notice to OutboundFiles.enqueue for the day's WIN file
    Then the delivery has status DELIVERED

  Scenario: AC2 Retry limit (legacy RWB-TE-006 AC2)
    Given the rwb-case contract mock returns task code "RESOLVE_OUTBOX_DELIVERY" with owner role "RW-PLATADM" for case "RW-2026-000601" and event RETRY_LIMIT_REACHED accepted for that case
    Given a target down for longer than the retry limit
    When "win-dispatch" fails at 10:01, 10:02, 10:07 and 10:22
    Then the system makes no fifth attempt
    Then the item moves to the exception queue: the "win-dispatch" delivery has status EXCEPTION and attempt count 4
    Then the system raises task RESOLVE_OUTBOX_DELIVERY on case "RW-2026-000601" for role RW-PLATADM
    Then event RETRY_LIMIT_REACHED moves the case to EXCEPTION_QUEUE by R-UNI-36 with one decision log entry

  Scenario: AC3 Nothing is sent for a change that did not commit (legacy RWB-TE-006 AC3)
    Given the notice approval fails after OutboxWriter.publish and the transaction rolls back
    When the sender runs
    Then no event and no delivery exist for "NT-SYN-0601"

  Scenario: AC4 A retry that succeeds (legacy RWB-TE-006 AC4)
    Given the rwb-case contract mock returns route state RESUME_STATE for case "RW-2026-000601" when RETRY_SUCCEEDED is raised
    Given "win-dispatch" fails at 10:01 and the case moves to RETRY_QUEUE by R-UNI-33
    When the attempt at 10:02 succeeds
    Then the system delivers the delivery status with attempt count 2
    Then event RETRY_SUCCEEDED returns the case to the state it paused in by R-UNI-35

  Scenario: AC5 The same event is written once (legacy RWB-TE-006 AC5)
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the outbox holds one event with that key
    Then the second transaction receives DuplicateOutboxKeyException and changes nothing

  Scenario: AC6 Two sender instances (legacy RWB-TE-006 AC6)
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then the system makes each delivery once
    Then the delivery log holds 200 calls

  Scenario: AC7 Order per case and consumer (legacy RWB-TE-006 AC7)
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the sender runs
    Then the system does not deliver sequence 12 to "ledger" until sequence 11 is DELIVERED

  Scenario: AC8 Consumers are independent (legacy RWB-TE-006 AC8)
    Given event CaseAllocated for case "RW-2026-000601"
    When "ledger" fails and "reporting-feed" succeeds at 10:01
    Then the system delivers the "reporting-feed" delivery and the "ledger" delivery is RETRYING with next attempt 10:02
    Then the case route state does not change, because "ledger" does not hold the case step

  Scenario: AC9 Sending an exception delivery again (legacy RWB-TE-006 AC9)
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator sends it again
    Then the response is 200 with message MSG-GEN-005
    Then the delivery status is PENDING with attempt count 0 and due at the next run
    When the platform administrator sends delivery "OBD-SYN-0002" with status DELIVERED again
    Then the response is 409 with message MSG-P2-022

  Scenario: AC10 An event with no case (legacy RWB-TE-006 AC10)
    Given an event with no case whose only consumer fails 4 times
    When the retries are used
    Then the delivery status is EXCEPTION
    Then the system sends an alert to the platform administrator within 15 minutes
    Then no task and no case event are raised

  Scenario: AC11 Retry settings come from configuration (legacy RWB-TE-006 AC11)
    Given the retry delays are changed in the configuration service to 2, 10 and 30 minutes at 09:00
    When "ledger" fails at 10:01
    Then the next attempt is due at 10:03
```

**Note on the retry times.** The retry times in AC2 and AC4 are the legacy values, copied unchanged. The target retry ladder is the Kafka retry topics 1 min / 10 min / 1 h and then the dead-letter topic (Architecture v5 slide 22); the conflict is recorded in the gap (GAP-1415), and the criteria are tested with those windows through the configuration of section 13. The only additions to the criteria are the origin tag on each Scenario line and one `Given the rwb-case contract mock returns ...` line in AC2 and AC4, where the case step is mocked; no legacy line was changed or dropped.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction and the same schema as the change, under that service's own login: no event without the change and no change without the event | events.txt Rules, Transactions; DP-01; DP-09 |
| BR2 | Each event carries a CloudEvents id and an idempotency key unique in the caller's outbox; a second publish with the same key throws `DuplicateOutboxKeyException`, and a repeated delivery is dropped in the consumer's inbox `processed_event` or by `IdempotencyGuard` | events.txt Rules, Duplicates; R-UNI-40; Arch v5 slides 11 and 22 |
| BR3 | Delivery is at least once; each recipient has its own delivery state and its own consumer group | events.txt Rules, Delivery; Arch v5 slide 21 |
| BR4 | Events for one case reach each recipient in the order they were written: the record key is the case ID, so one case's events share one partition | events.txt Rules, Ordering; Arch v5 slides 21 and 22 |
| BR5 | A failed delivery climbs the retry topics at 1 min, 10 min and 1 h; after the third retry it goes to the dead-letter topic with one alert and the replay tool as the recovery path | Arch v5 slides 11, 22 and 34; NFR-026; REQ-DRI-007 |
| BR6 | The case-step effects belong to the service that owns the case step: the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED and the limit RETRY_LIMIT_REACHED through that service's own contract, never from the library | R-UNI-33; R-UNI-35; R-UNI-36; GAP-1415 |
| BR7 | The envelope carries `ce_specversion` 1.0, the event type with its schema version, the source as the owning service, the subject and the trace context; payloads hold references and codes, never personal data | events.txt Rules, Payload and Versioning; Arch v5 slides 11 and 22 |
| BR8 | Nothing moves when the decision record cannot be written: the record, the state change and the outbox row are one transaction (R-UNI-39) | R-UNI-39; Arch v5 slide 28; Temporal and Drools Design slide 28 |
| BR9 | Recipients, owners, retry windows and the batch size are configuration, read through the parameters client, never values in the code | Principle 1; DL11; DP-06 |

### 9. State transitions

The case status does not change in this story. For a recipient that holds a case step, the route state changes through that service's universal rules, and each delivery has its own status inside the caller's schema.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a recipient that holds the case step, raised by the owning service | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds, raised by the owning service | RESUME_STATE (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Retries used, raised by the owning service | EXCEPTION_QUEUE (R-UNI-36) |
| Delivery PENDING or RETRYING | Broker acknowledgement | None | Delivery DELIVERED |
| Delivery PENDING | Recipient fails | Retries left | Delivery RETRYING in the retry topic of the window |
| Delivery RETRYING | Recipient fails | No retries left | Record in the dead-letter topic; delivery EXCEPTION where the consumer reports the failure back |
| Delivery EXCEPTION | Resent through the P2 admin API | None | Delivery PENDING |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform library team, owning the template | Publishes the interfaces, the DDL template, the envelope rule and the fakes; changes them only through the library contract story |
| The owning service of each consumer | Raises its own case events, its own task and its own decision record through its own contract |
| RW-PLATADM, platform administrator | Reads deliveries and resends an exception delivery through the admin API of P2, which this library does not provide |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries through the admin API of P2 |
| RW-SECADM, security administrator | Reads deliveries through the admin API of P2 |
| Platform team | Receives the dead-letter alert, holds the replay tool and owns the Kafka topic settings |
| No approval level from the delegation of authority applies | The library takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 | outbox_event | id | Write |
| DF-OPS-190 | outbox_event | event_type | Write |
| DF-OPS-191 | outbox_event | schema_version | Write |
| DF-OPS-192 | outbox_event | case_id | Write |
| DF-OPS-193 | outbox_event | case_seq | Write |
| DF-OPS-194 | outbox_event | idempotency_key | Write |
| DF-OPS-195 | outbox_event | payload | Write |
| DF-OPS-196 | outbox_event | actor_ref | Write |
| DF-OPS-197 | outbox_event | occurred_at | Write |
| DF-OPS-198 | outbox_delivery | id | Write |
| DF-OPS-199 | outbox_delivery | event_id | Write |
| DF-OPS-200 | outbox_delivery | consumer | Write |
| DF-OPS-201 | outbox_delivery | status | Write |
| DF-OPS-202 | outbox_delivery | attempt_count | Write |
| DF-OPS-203 | outbox_delivery | next_attempt_at | Write |
| DF-OPS-204 | outbox_delivery | last_error_code | Write |
| DF-OPS-205 | outbox_delivery | delivered_at | Write |
| DF-OPS-206 | outbox_delivery | task_id | Write |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write, through the owning service's contract |
| DF-DEC-001 to DF-DEC-018 | decision_record (local library) | all fields | Write, through the local record library of the owning service |
| DF-CAS-001 | recovery_case | id | Read, through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary. The four library tables and the `processed_event` and `idempotency_key` columns have no field ID of their own in the source; they are the same objects the Ownership Map assigns to PLT, created in each service's own schema (GAP-1415; ASM-2472). No copy of another service's row is written.

### 12. Contract

#### 12.1 REST operations provided

None — the admin read and resend API `GET /admin/outbox/deliveries` and `POST /admin/outbox/deliveries/{deliveryId}/resend` belongs to P2 rwb-integration in the Ownership Map, and the library publishes no REST surface of its own.

#### 12.2 REST operations consumed

None — the library joins the caller's transaction and calls no service.

#### 12.3 Events published

None — the caller's events are relayed to the owning service's `rwb.<short>.events.v1`; the library publishes no event of its own.

#### 12.4 Events consumed

None — the inbox receives the owning service's subscribed events, under that service's own consumer group and in that service's own `processed_event` table.

#### 12.5 Workflows and activities

None — the relay is a plain background worker in each service, not a workflow, and it starts no activity.

#### 12.6 Schedules

None — the relay is a continuous background worker, not a Schedule; the legacy Quartz JOB-11 trigger every minute does not become a Temporal Schedule (GAP-1415; ASM-2473).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| outbox_event | PLT | One row per published fact, in the caller's own schema; unique key on `idempotency_key` and on `(case_id, case_seq)` |
| outbox_delivery | PLT | One row per event and recipient, in the caller's own schema; unique key on `(event_id, consumer)` and a due index on `next_attempt_at` |
| processed_event | PLT | The inbox of each consumer, in the consumer's own schema; unique key on the CloudEvents id and the consumer group |
| idempotency_key | PLT | The stored response per scope and key for a repeated command, in the caller's own schema |

The four tables are library objects created by the library DDL template in each service's own schema, under the Ownership Map ruling; they are not created once in an rwb-integration schema. No table of another service is read and no key crosses a schema boundary (DP-01, DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case case-event and task fake | The P3 case-step contract behind `CaseEvents.raise` and `TaskApi.raiseTask` | Task code RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM on case RW-2026-000601; RETRY_LIMIT_REACHED accepted; route state RESUME_STATE on RETRY_SUCCEEDED (AC2, AC4) |
| rwb-decision decision-record fake | The P7 ledger contract behind the local record library | One decision log entry for the move to EXCEPTION_QUEUE (AC2, TC-TE-006-13) |
| Owning-service recipient fakes | The consumer side of each event type | A recipient stub that succeeds on demand and fails on demand, with the consumer names "win-dispatch", "ledger" and "reporting-feed" (AC1 to AC11) |
| rwb-integration admin API fake | The P2 contract behind the read and resend operations | An EXCEPTION delivery OBD-SYN-0001 and a DELIVERED delivery OBD-SYN-0002 (AC9) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The library adds no REST surface; the admin API is provided by P2 |
| Kafka | None published and none consumed by the library itself | The caller's records are relayed to the owning service's `rwb.<short>.events.v1` with the CloudEvents 1.0 envelope and the caseId key, through the three retry topics and the dead-letter topic |
| Temporal | None | The relay is a background worker; a service that needs a workflow for its own step uses the workflow kit |
| File | None | The library writes and reads no file; an outbound file is a claim-check call through the rwb-integration contract |

### 13. Solution plan

**Package.** Shared library artifact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.outbox`; the three published interfaces sit in `th.co.scb.ace.workbench.recovery.platform.api`; the DDL template is a resource of the library, applied by each service's own Flyway sequence.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The outbox, inbox and idempotency rows are written in the caller's own schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the record is written by the owning service in its own transaction, not by the relay | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the recipient list and the retry windows are parameters | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the recipient and event-type lists are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. This story is that library | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay, not a Temporal Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the recipient is reached through its published contract or its topic, never in process | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the library adds no path of its own and every admin path belongs to P2 | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the library DDL template is applied by each service's own sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route; the admin screen that reads and resends deliveries is out of scope | H RWB-PLT-N001-CON |

**Hardware and software change.** The outbox, inbox and idempotency tables are library objects created in every service schema, not one set of tables in a P2 schema; the relay publishes to each owner's topic with CloudEvents 1.0 and an idempotent producer; retry is the Kafka retry-topic ladder and the dead-letter topic with an alert and a replay tool; and the case-step and decision-record effects stay in the owning service's code through its contracts. No new hardware is added: the relay runs in each service's own pods on the existing AKS cluster and the tables sit in the existing ACE PostgreSQL server under each service's own login, replacing the shared Quartz sender and the single `recovery` schema tables.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `OutboxWriter` | Published interface | Writes the event and one delivery per listed recipient in the caller's transaction (BR1, BR2, BR7) |
| `OutboxConsumer` | Published interface | Consumes one delivery and returns OK or FAILED with a code; the caller implements it under its consumer name |
| `IdempotencyGuard` | Published interface | Answers whether a consumer has already acted on a key (BR2) |
| OutboxEventEntity, OutboxDeliveryEntity, ProcessedEventEntity, IdempotencyKeyEntity | Entity | The four rows, mapped into the caller's schema |
| OutboxRepository | Repository | Skip-locked selection of due deliveries in case order per recipient (BR4) |
| OutboxRelay | Service | Continuous per-service relay: selection, envelope, publish, mark delivered, retry topic and dead-letter path (BR3, BR5) |
| ConsumerCatalog | Service | Reads the recipient list, the event types per recipient and the retry windows through the parameters and reference contracts (BR9) |
| EnvelopeFactory | Service | Builds the CloudEvents 1.0 binary-mode envelope, the caseId key and the trace headers (BR7) |
| OutboxDdlTemplate | Resource | The DDL contract of the four tables, applied by each service's own Flyway sequence (DP-15) |

**Database.** The library DDL template creates, in whichever schema applies it:
- `outbox_event` (id uuid primary key, event_type varchar(40) not null, schema_version integer not null, case_id uuid, case_seq bigint, idempotency_key varchar(120) not null, payload jsonb not null, actor_ref varchar(64), occurred_at timestamptz not null, plus the standard columns), with `UNIQUE (idempotency_key)` and `UNIQUE (case_id, case_seq)`.
- `outbox_delivery` (id uuid primary key, event_id uuid not null references outbox_event, consumer varchar(60) not null, status varchar(12) not null default 'PENDING', attempt_count integer not null default 0, next_attempt_at timestamptz not null, last_error_code varchar(40), delivered_at timestamptz, task_id uuid, plus the standard columns), with `UNIQUE (event_id, consumer)`, `CHECK (status IN ('PENDING','RETRYING','DELIVERED','EXCEPTION'))` and index `ix_outbox_delivery_due ON outbox_delivery (next_attempt_at) WHERE status IN ('PENDING','RETRYING')`.
- `processed_event` (id uuid primary key, ce_id varchar(64) not null, consumer_group varchar(60) not null, processed_at timestamptz not null, plus the standard columns), with `UNIQUE (ce_id, consumer_group)`.
- `idempotency_key` (id uuid primary key, scope varchar(60) not null, key varchar(120) not null, stored_response jsonb, created_at timestamptz not null, plus the standard columns), with `UNIQUE (scope, key)`.

`case_seq` is the case's highest sequence plus 1, taken under a lock on the case's latest outbox row in the same schema. No table references a table of another service. The `outbox_event` and `outbox_delivery` columns above are the legacy DDL and its field identifiers DF-OPS-189 to DF-OPS-206; the `processed_event` and `idempotency_key` column sets are the working read of this run, because no source defines them (GAP-1415; ASM-2473).

**Configuration and reference data.** The recipient list and the retry windows are parameters read through the parameters client (DP-06) and the reference-data client (DP-07), held by rwb-case: recipient name, the event types it takes, its owner role and whether it holds a case step; the retry windows of the ladder (1 min, 10 min, 1 h) and the batch size. The legacy values 3 retries at 1, 5 and 15 minutes stay in the AC text only and are exercised through this configuration (GAP-1415; ASM-2472). The alert route to the platform team and the replay tool are the platform observability and Kafka runbook items.

**Build steps**

1. Publish the three interfaces and their exceptions from the CON story; test that no method opens its own transaction.
2. Write the DDL template and the four entities; test the unique keys and the due index in a throwaway schema (AC5, AC6).
3. Write `OutboxWriter` joining the caller's transaction; test commit and rollback (AC1, AC3).
4. Write `OutboxRepository` with the skip-locked selection and the order per case and recipient; test two relay instances (AC6), order (AC7) and independent recipients (AC8).
5. Write `EnvelopeFactory` and the idempotent producer; test the headers, the caseId key, the trace header and the registry validation (AC1).
6. Write `OutboxConsumer` and the inbox; test the duplicate drop and the `IdempotencyGuard` path (AC5, AC8).
7. Write `OutboxRelay` with `ConsumerCatalog`; test the retry windows, a success after a failure and a configuration change (AC2, AC4, AC11).
8. Add the dead-letter alert, the counts and the replay note (AC10).
9. Hand the case-step events, the task and the decision record to the owning services as a contract test, and prove the library raises none of them (AC2, AC4).
10. Run the contract tests of section 12.8 against the fakes and prove that the library adds no REST surface (AC9).

**Feature flag.** One flag per service, read as a parameter; off, the relay does not publish and the deliveries stay PENDING while the writer still records the events, so nothing is lost when it is switched on.

**Done when.** The tests in section 16 pass, the contract tests of the CON story pass against the fakes, and the relay counts of every service appear on the platform observability path.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Text when a delivery enters the exception path (new) | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION (new) | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | Decision record write failed at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Delivery not found | This case is not in your scope. |

In MSG-P2-001, {interface} is the recipient name and {item} the event type and case number. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen of its own. The task that an owning service raises on a failed case step appears on SCR-09 Exception queue (states Loading and List) for the owner role, with MSG-P2-001, and the owning service owns that display. The platform administrator reads and resends deliveries through the admin API that P2 rwb-integration provides; SCR-44 Interface and job monitor shows the deliveries from Epic 2. The library adds no screen and no route (DP-19).

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-13 | AC2, BR8 | NFR | Decision record write forced to fail at the exception move; the delivery stays RETRYING; MSG-P7-003 in the relay log; incident raised |
| TC-TE-006-12 | Access | Component | RW-DATASTEW resends a delivery through the P2 admin API; refused with MSG-P4-002 |
| TC-TE-006-01 | AC1, BR1, BR3, BR7 | Component | Notice NT-SYN-0601 approved at 10:00; win-dispatch stub succeeds; the envelope and the caseId key are asserted |
| TC-TE-006-02 | AC2, BR5, BR6 | Component | win-dispatch stub fails 4 times through the retry topics and the dead-letter topic |
| TC-TE-006-03 | AC3, BR1 | Component | Approval rolled back after publish |
| TC-TE-006-04 | AC4, BR6 | Component | win-dispatch stub fails once, then succeeds |
| TC-TE-006-05 | AC5, BR2 | Component | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06 | AC6, BR3 | Component | 200 due deliveries, two relay instances |
| TC-TE-006-07 | AC7, BR4 | Integration | Sequences 11 and 12, ledger stub failing on 11, one partition key caseId |
| TC-TE-006-08 | AC8, BR3 | Component | ledger fails and reporting-feed succeeds on one CaseAllocated event |
| TC-TE-006-09 | AC9 | Component | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 DELIVERED |
| TC-TE-006-10 | AC10 | Component | Event with no case, consumer failing 4 times, one dead-letter alert |
| TC-TE-006-11 | AC11, BR9 | Component | Retry windows changed in configuration before the run |

The legacy test case ids are kept with their level mapped to the target shape: Access becomes Component, Principle 5 and Resilience become NFR, and System becomes Component or Integration. The full test, with its Given, When and Then, is carried into the next Test Cases version under the same id.

### 17. Guardrails

- No business value in code: recipients, owners, retry windows and batch size are configuration read through the parameters and reference contracts.
- No personal data in logs, events, tests or prompts; payloads hold references and codes only, and the envelope carries IDs and facts.
- No read of another service's tables and no cross-schema key: the outbox, the inbox and the idempotency rows are written in the caller's own schema, and case events, tasks and decision records go through their owners' contracts.
- No event and no delivery is deleted; a record leaves the exception path only by a resend through the P2 admin API or a replay of the dead-letter topic.
- The library raises no case event, no task and no decision record of its own.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-TE-006-01 to TC-TE-006-13 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-TE006-CON | Contract | H: publishes the interfaces, the DDL template, the envelope, the dedupe and retry rules and the fakes this story implements |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the owning service writes through |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data clients for the recipient list and the retry windows |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit for a service that needs an event-started workflow |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence that applies the DDL template |
| RWB-PLT-N001-CON | Contract | H: the gateway route; the admin screen is out of scope |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON, RWB-P2-E1007-CON | Contract | C: the owner contracts behind the parameters, the reference data, the decision record and the outbound file path |
| RWB-PLT-EVT | Platform epic | X: the event platform stories provision the topics, the retry topics, the dead-letter topic and the registry |

### 19. Out of scope

- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-P2-E1007-CON and the P2 stories behind it.
- The recipients themselves, for example the ledger listener: the owning service stories of each consumer.
- The interface and job monitor screen and the admin read and resend screen: SCR-44 in Epic 2 and Epic 8, and the admin API of P2 rwb-integration.
- The Kafka topic settings, the ACLs, the retry topics and the dead-letter topic themselves: RWB-PLT-EVT.
- The decision-record library and the central ledger: RWB-PLT-E1027-CON and RWB-P7-E1027-CON.
- The retry values as a business decision: DL11, and the conflict recorded in GAP-1415.
