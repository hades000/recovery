# RWB-ITG-TE006-ITG Outbox and retry for outbound work — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-006 for the wave-1 integration epic. The monolith outbox with one in-process consumer call becomes the outbox and inbox library of the platform, one owner topic per service, CloudEvents 1.0 on Kafka with retry topics and a `.dlt`, the case effects as Temporal signals on `rwb-case`, the move to the exception queue as a decision record on `rwb.decision-record.v1`, and the WIN dispatch as the `deliverFile` step of rwb-integration; this story builds and runs the harness that proves that path across services and topics. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P2-E1007-APP, RWB-PLT-TE006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

### 1. Story

As a **tech lead**, I want **the outbox and inbox library of the platform exercised end to end across the wave-1 services: every service writing its event and one delivery per consumer in its own schema inside the caller's transaction, the relay of each service publishing CloudEvents 1.0 to that service's own topic keyed caseId, every consumer deduping through its inbox, a failing consumer walking the retry topics to the `.dlt` with an alert, and the case effects and the exception task arriving in rwb-case and the decision record in rwb-decision**, so that **no outbound action is lost or sent twice when a system or a consumer is down, and the retry, ordering, dedupe and exception behaviour is proven on the services and topics that will run it rather than on one service's in-process stand-in**.

### 2. Business rationale

The legacy story protects the Workbench with one transactional outbox in the integration module, a sender that calls each consumer directly in process, and case events raised through a published P3 interface (RWB-TE-006 sections 4 and 12). If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it; the measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1). REQ-DRI-007 asks for retry on a defined schedule and an exception queue with a task for a named owner.

In the target nothing of that path stays inside one process. Every service is built from the template with its own schema, its own relay and its own topic (Arch v5 slides 20 and 41), so the tables `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are library objects created in each service schema (DP-09, ASM-0074), and rwb-integration owns no table of another service. Delivery is a Kafka publish in CloudEvents 1.0 binary mode with the case ID as the key, retry topics at 1 minute, 10 minutes and 1 hour, and a `.dlt` with an alert (Arch v5 slide 11); the consumers dedupe through their own inbox. The case effects that the legacy story raised in process become signals and activities on `rwb-case` through CaseWorkflow, one hop on the owner's queue and never a REST call chain (DP-11, DP-12; Temporal design slides 11 and 14), and the move of a case to the exception queue writes its decision record through `rwb.decision-record.v1` owned by rwb-decision (DP-03). The outbound work request WIN_DISPATCH is no longer an internal adapter: it is the daily WIN file that rwb-comms opens at 16:00 and rwb-integration delivers with its `deliverFile` activity (Arch v5 slides 16 and 44, JOB-10). A local outbox that commits alone, an event without a subscriber, a duplicate acted on twice, a poison message with no dead letter, a case left in the retry queue and a decision that moves a case without its record are all failures that only appear across services; this story builds and runs the harness that proves them together, and it publishes no operation, owns no table and adds no business rule of its own.

### 3. Preconditions

- The nine wave-1 services are deployed in DEV and SIT, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- Every wave-1 schema holds the library objects of DP-09 created by its own DB story: `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`, with the unique key on `outbox_event.idempotency_key` and the unique key on `(event_id, consumer)` in `outbox_delivery` (ASM-0074; RWB-PLT-TE006-APP and the DB story of each service).
- The topic of each service exists with its retry topics and `.dlt` topic — `rwb.comms.events.v1`, `rwb.case.events.v1`, `rwb.integration.events.v1`, `rwb.decision-record.v1` and the topics of the other wave-1 services in the fixture path — with the JSON Schema registry in BACKWARD mode (Arch v5 slide 11; RWB-PLT-EVT).
- The relay JOB-11 runs in every service every minute and is part of the service template (Arch v5 slides 20 and 44; ownership ruling ASM-0063, so it is not a Temporal Schedule).
- Queue `rwb-case` is registered in namespace `rwb-recovery`, and CaseWorkflow is deployed with its signals on `rwb-case` (RWB-P3-E1018-APP, RWB-PLT-E1071-CON).
- rwb-integration is deployed with the `deliverFile` activity and the 16:00 WIN window of JOB-10 (Arch v5 slides 16 and 44; RWB-P2-E1007-APP; ownership ruling ASM-0062).
- rwb-decision consumes `rwb.decision-record.v1` and holds the central ledger; the decision-record library is available to every service (DP-03; RWB-PLT-E1027-CON).
- rwb-access answers `POST /api/recovery/access/v1/authorise` and holds the test roles RW-PLATADM, RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY and RW-SECADM with their Platform administration letters (RWB-P4-E1008-APP; Arch v5 slide 14).
- The consumer list per event type and the retry settings are read as parameters through the rwb-case parameters contract, and the event types and delivery statuses as reference data through the rwb-case reference-data contract; no value is written in harness code (DP-06, DP-07).
- The mapping from the legacy case events to the signals and activities of `rwb-case`, the service that raises RESOLVE_OUTBOX_DELIVERY, the retry delays, the `.dlt` alert route and the consumer list per event type are Not specified in the source documents (GAP-0382; ASM-0553; ASM-0554).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the platform library and rwb-integration and is run when they are in DEV; a fake is never used in their place.

### 4. Flow

1. Harness: reads the service list, the topic list, the consumer list, the retry settings and the queue names from configuration, and runs the preflight of section 13; a missing library table in a service schema, a missing topic, retry topic or `.dlt`, a missing relay or a missing queue stops the run before any test.
2. Harness: drives one real state change in rwb-comms on synthetic case "RW-2026-000601" with notice "NT-SYN-0601" approved, through the service's own write path, and reads the case back through `GET /api/recovery/case/v1/cases/{caseId}` (DP-11, DP-13).
3. Service: writes the state change, the `outbox_event` row and one `outbox_delivery` row per configured consumer in one transaction in its own schema; a failed transaction leaves none of the three (BR1).
4. Relay: JOB-11 in that service selects the due deliveries in case order with a skip-locked read, publishes one CloudEvents 1.0 event in binary mode on the owner topic with key "RW-2026-000601" and `acks=all`, and marks the delivery DELIVERED on the broker acknowledgement (BR3, BR4, BR9).
5. Harness: reads the topic with its own consumer group and asserts one event per change, the envelope (`ce_id`, `ce_source`, `ce_type`, `ce_schemaurl`, `ce_time`, `ce_idempotencykey`) and a payload of case and notice references only (BR7).
6. rwb-integration: the `win-dispatch` consumer of work request WIN_DISPATCH resolves to the `deliverFile` activity on queue `rwb-integration`; the file run opens in the 16:00 WIN window of JOB-10 and publishes `rwb.integration.FileDelivered.v1` on `rwb.integration.events.v1` (BR9, BR10).
7. Consumers: each consumer records the CloudEvents id in its own `processed_event` before it acts, so a repeated delivery changes nothing (BR2, BR6).
8. Harness: makes one consumer fail on demand and reads the delivery back through `GET /api/recovery/integration/v1/admin/outbox/deliveries`; the retry chain of the topic and the relay schedule advance the delivery RETRYING, then DELIVERED, or to EXCEPTION with the attempt count of the legacy fixtures (BR5).
9. rwb-case: on the first failure of a consumer that holds a case step CaseWorkflow receives SYSTEM_UNAVAILABLE, on a later success RETRY_SUCCEEDED, and at the limit RETRY_LIMIT_REACHED; rwb-decision receives the record of the move to the exception queue on `rwb.decision-record.v1`, and `RESOLVE_OUTBOX_DELIVERY` appears in the task list of the consumer's owner role (BR6, BR8, BR10).
10. Harness: as RW-PLATADM, resends an EXCEPTION delivery through `POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend`, and repeats the call as a role without Platform administration U through the rwb-access check (BR5).
11. Harness: reconciles the counts — one change, one event, one delivery per consumer, one effect per consumer, one record per move to the exception queue — and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist in the service schema | None | AC1 |
| X2 | The same idempotency key is published twice | One event exists; the second transaction receives DuplicateOutboxKeyException and changes nothing | None | AC4 |
| X3 | The same event is delivered twice to a consumer | The consumer inbox `processed_event` ignores the second delivery; one effect exists | None | AC4 |
| X4 | A consumer fails once and then succeeds | The delivery is DELIVERED on the retry and the case resumes by R-UNI-35 | None | AC3 |
| X5 | The retries are used | The delivery is EXCEPTION; RESOLVE_OUTBOX_DELIVERY is raised for the consumer's owner role; RETRY_LIMIT_REACHED moves the case by R-UNI-36; MSG-P2-001 is the task text | MSG-P2-001 | AC3 |
| X6 | The decision record cannot be written at the exception move | Nothing changes; the delivery stays RETRYING and is tried at the next run; an incident is raised (R-UNI-39) and the caller sees MSG-P7-003 | MSG-P7-003 | AC3 |
| X7 | An earlier event for the same case and consumer is failing | Later events for that case and consumer wait on the topic and on the relay | None | AC5 |
| X8 | Two relay instances run at once | Each delivery is published once; the consumer drops a repeat by its key | None | AC5 |
| X9 | An event with no case reaches the `.dlt` | EXCEPTION and an alert to the platform administrator; no task and no case event | MSG-P2-001 | AC6 |
| X10 | A delivery that is not in EXCEPTION is resent | Refused with 409 | MSG-P2-022 | AC6 |
| X11 | A role without Platform administration U resends a delivery | Refused with 403 after the rwb-access check | MSG-P4-002 | AC6 |
| X12 | The delivery ID does not exist | The read answers 404 | MSG-P4-003 | AC6 |

X1 to X8 are the exception paths of the legacy story carried onto the real services and topics; X9 to X12 are the dead-letter, resend and access paths the Kafka and platform shape adds. The alert route of X9 is Not specified in the source documents (GAP-0382; ASM-0553).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the platform library, the wave-1 services, the topics and the `rwb-case` and `rwb-integration` workers, and it owns no schema and no table |
| Negotiable | Fixture counts, wait intervals and report layout are configuration; consumer names, case, notice, deliveries, sequences, keys, messages and statuses are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one event per change, one delivery per consumer, one effect per consumer, order per case, a dead letter with an alert, a case effect and a record at the limit |
| Estimable | One harness project, six test classes, five fixtures, one forced failure per consumer and one resend pair |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row, an event, a delivery state, a signal outcome, a task, a record, a response |

### 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work, proven across the wave-1 services and topics

  Background:
    Given the environment is DEV with synthetic data
    Given the nine wave-1 services run with their own schemas, logins, topics and relays
    Given every service schema holds outbox_event, outbox_delivery, processed_event and idempotency_key from the platform library
    Given consumer "win-dispatch" takes work request WIN_DISPATCH and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 The event and its deliveries commit or roll back with the caller's transaction (new, D-RCV-60)
    Given the approval of "NT-SYN-0601" in rwb-comms writes work request WIN_DISPATCH for case "RW-2026-000601"
    When the transaction commits at 14 December 2026 10:00:00
    Then rwb_comms holds one outbox_event with event type WIN_DISPATCH, schema version 1, case ID, the next case sequence and idempotency key "WIN_DISPATCH:NT-SYN-0601"
    Then rwb_comms holds one outbox_delivery per configured consumer, each with status PENDING and attempt count 0
    Then no other service schema holds a row of that change and no service reads another service's outbox tables
    When a second approval writes the same event and its transaction rolls back after the write
    Then no outbox_event and no outbox_delivery exist for that attempt
    Then the harness finds no event for that attempt on any topic

  Scenario: AC2 One CloudEvents event per delivery on the owner's topic, and the WIN step is a file through rwb-integration (new, D-RCV-60)
    Given the relay of rwb-comms runs at 10:01
    When it publishes the due deliveries of case "RW-2026-000601"
    Then exactly one CloudEvents 1.0 event in binary mode is on rwb.comms.events.v1 with key "RW-2026-000601" and acks=all
    Then the harness consumer group reads ce_id, ce_source, ce_type, ce_schemaurl, ce_time and ce_idempotencykey "WIN_DISPATCH:NT-SYN-0601"
    Then the payload holds the case and notice references and codes only, with no name, address or identifier
    Then the delivery to "win-dispatch" is DELIVERED and the consumer resolves to the deliverFile activity on queue rwb-integration
    Then the file run opens inside the 16:00 WIN window of JOB-10 and rwb.integration.FileDelivered.v1 is on rwb.integration.events.v1
    Then no in-process adapter call exists between the producer and the consumer, and the harness fails the run if one is found

  Scenario: AC3 The case effects arrive as Temporal signals on rwb-case, and the limit writes the decision record (new, D-RCV-60)
    Given the consumer "win-dispatch" fails at 10:01
    Then CaseWorkflow receives SYSTEM_UNAVAILABLE by R-UNI-33 and the case moves to RETRY_QUEUE
    When the attempt at 10:02 succeeds
    Then the delivery is DELIVERED with attempt count 2 and CaseWorkflow receives RETRY_SUCCEEDED, which returns the case to the state it paused in by R-UNI-35
    Given the consumer fails at 10:02, 10:07 and 10:22 as well
    Then the relay makes no fifth attempt
    Then the delivery to "win-dispatch" is EXCEPTION with attempt count 4
    Then task RESOLVE_OUTBOX_DELIVERY is raised in rwb-case on case "RW-2026-000601" for the owner role named in the consumer configuration, with text MSG-P2-001
    Then CaseWorkflow receives RETRY_LIMIT_REACHED and the case moves to EXCEPTION_QUEUE by R-UNI-36
    Then rwb.decision-record.DecisionRecorded.v1 is on rwb.decision-record.v1 and rwb_decision holds one entry for the move, so the move and its record commit together (R-UNI-39)
    When the decision record cannot be written at the exception move
    Then nothing changes, the delivery stays RETRYING and is tried at the next run, the caller sees MSG-P7-003 and an incident is raised

  Scenario: AC4 One event per key and one effect per consumer, whatever the delivery count (new, D-RCV-60)
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the producer schema holds one outbox_event with that key and the second transaction changes nothing
    Given the same event is delivered to a consumer twice
    When the consumer handles both deliveries
    Then its processed_event holds the CloudEvents id once and the effect exists once
    Then the harness reads one event on the topic and one effect per consumer for the change (R-UNI-40)
    When the harness counts the messages on the retry topics for that event
    Then no message is duplicated by a second publish of the same outbox_event

  Scenario: AC5 Order per case and consumer, and one delivery each across two relay instances (new, D-RCV-60)
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the relay runs
    Then sequence 12 is not delivered to "ledger" until sequence 11 is DELIVERED
    Then the order holds per case and consumer only, so "reporting-feed" reads its own deliveries in its own order
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then each delivery is published once and the consumer group log holds 200 events for the 200 deliveries
    Then two deliveries of one event to two consumers keep their own state, so a failure of "ledger" leaves "reporting-feed" DELIVERED and "ledger" RETRYING with the next attempt at 10:02

  Scenario: AC6 The exception queue is worked through the P2 admin surface and the P4 right check (new, D-RCV-60)
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator resends it through POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend
    Then the response is 200 with message MSG-GEN-005
    Then its status is PENDING with attempt count 0 and it is due at the next run
    When the platform administrator resends delivery "OBD-SYN-0002" with status DELIVERED
    Then the response is 409 with message MSG-P2-022
    When a test user holding only RW-DATASTEW resends a delivery
    Then rwb-access refuses the Platform administration U check and the answer is 403 with MSG-P4-002
    When a delivery ID that does not exist is read
    Then the answer is 404 with MSG-P4-003
    Given an event with no case whose only consumer fails 4 times
    Then the delivery reaches the .dlt topic of the owner, its status is EXCEPTION and an alert reaches the platform administrator
    Then no task and no case event are raised for that event
```

The mapping from the legacy case events to the signals and activities of `rwb-case`, and the service that raises the `RESOLVE_OUTBOX_DELIVERY` task, are Not specified in the source documents (GAP-0382; ASM-0553); the retry delays and the `.dlt` alert route are Not specified in the source documents (GAP-0382; ASM-0553); the consumer list per event type across services is Not specified in the source documents (GAP-0382; ASM-0554). The legacy acceptance criteria that these scenarios re-exercise are owned by RWB-PLT-TE006-APP and are named in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction as the change, in the producer's own schema: no event without the change and no change without the event | RWB-TE-006 BR1; DP-01; DP-09; Arch v5 slide 11 |
| BR2 | Each event carries a CloudEvents id and an idempotency key unique in the producer's outbox; a consumer drops a repeat through its inbox `processed_event` | RWB-TE-006 BR2; R-UNI-40; Arch v5 slide 11 |
| BR3 | Delivery is at least once and each consumer has its own delivery state, advanced by the relay on the acknowledgement of an `acks=all` publish | RWB-TE-006 BR3; Arch v5 slide 11 |
| BR4 | Events for one case reach each consumer in the order they were written; the key is the case ID, the relay reads due deliveries in case order with a skip-locked selection, and a failing event holds later events for that case and consumer | RWB-TE-006 BR4; Arch v5 slide 11 (key caseId, order per case) |
| BR5 | A failed delivery is retried on the configured schedule and, when the retries are used, the delivery is EXCEPTION and the item is worked from the exception queue; the retry delays, the counts and the alert route are data, not code | RWB-TE-006 BR5; NFR-026; REQ-DRI-007; GAP-0382 |
| BR6 | For a consumer that holds a case step, the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED and the limit RETRY_LIMIT_REACHED, all as signals on CaseWorkflow in rwb-case; the exception task RESOLVE_OUTBOX_DELIVERY is raised in rwb-case for the owner role in the consumer configuration | RWB-TE-006 BR6; R-UNI-33; R-UNI-35; R-UNI-36; ASM-0553 |
| BR7 | Payloads hold references and codes, never personal data, and every event carries its schema version in the registry | RWB-TE-006 BR7; Arch v5 slide 11 |
| BR8 | A case does not move to the exception queue unless its decision record is written; a refused record leaves the delivery RETRYING and raises an incident | R-UNI-39; CTL-06; DP-03 |
| BR9 | Every event travels on the producer's own topic `rwb.<short>.events.v1` in the CloudEvents 1.0 envelope, binary mode, key caseId, with the retry topics at 1 minute, 10 minutes and 1 hour and a `.dlt` with an alert; no service publishes another service's topic | Arch v5 slides 11 and 20; DP-09; Template and Rules §R4 |
| BR10 | The outbound work request WIN_DISPATCH is delivered as the daily WIN file by the `deliverFile` activity of rwb-integration inside the 16:00 window of JOB-10, not by an in-process adapter | Arch v5 slides 16 and 44; ASM-0062; DP-16 |
| BR11 | The consumer list, the retry settings and the case-step flag of a consumer are parameters read through the rwb-case parameters contract, and the event types and delivery statuses are reference data read through its reference-data contract | RWB-TE-006 BR9; DP-06; DP-07 |

### 9. State transitions

No case status changes because of this story; it drives and asserts. The states it observes:

| Item | States |
|---|---|
| Delivery | PENDING (written, not yet published or not yet published successfully), RETRYING (a publish or a consumer failed with attempts left), DELIVERED (the broker acknowledged the publish with `acks=all`), EXCEPTION (the retries are used or the event reached the `.dlt`) |
| Delivery after a resend | EXCEPTION becomes PENDING with attempt count 0 and is due at the next relay run |
| Relay run | Idle, running (skip-locked selection of due deliveries), or stopped by the feature flag, in which case deliveries stay PENDING |
| Consumer | Received, deduplicated through `processed_event`, acted on once, retried through the retry topic, or dead-lettered |
| Case route state, observed through rwb-case | ANY_ACTIVE to RETRY_QUEUE on SYSTEM_UNAVAILABLE (R-UNI-33); RETRY_QUEUE to the state it paused in on RETRY_SUCCEEDED (R-UNI-35); RETRY_QUEUE to EXCEPTION_QUEUE on RETRY_LIMIT_REACHED (R-UNI-36) |
| Exception task | Raised for the consumer's owner role, open, then closed when the item is worked |
| Harness run | Not started, running, passed, failed with the failing criterion named |

| From | Event or cause | Condition | To |
|---|---|---|---|
| PENDING | Relay publishes | Broker acknowledges | DELIVERED |
| PENDING | Publish or consumer fails | Attempts left | RETRYING |
| RETRYING | Retry succeeds | None | DELIVERED |
| RETRYING | Retry fails | No attempts left | EXCEPTION |
| EXCEPTION | Platform administrator resends | None | PENDING (attempt count 0) |
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a consumer that holds the case step | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds | The state it paused in (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | The retries are used and the decision record is written | EXCEPTION_QUEUE (R-UNI-36) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the forced failures and the run report |
| Platform library owner (RWB-PLT-TE006-CON, RWB-PLT-TE006-APP) | Owns the outbox, inbox and idempotency objects, the delivery statuses, the retry scheduling and the relay |
| Wave-1 service teams | Own their schema, their topic, their relay instance and their consumers |
| rwb-integration owner (RWB-P2-E1007-APP) | Owns the `deliverFile` activity, the file run and the two admin endpoints of the Ownership Map |
| rwb-case owner | Owns CaseWorkflow, the three signals, the exception task and the case route state |
| rwb-decision owner | Owns the decision record, the shared topic and the ledger entry |
| rwb-access owner | Owns the Platform administration right check and the refusals |
| RW-PLATADM Platform administrator | Reads deliveries and resends an EXCEPTION delivery (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM Security administrator | Reads deliveries (Platform administration CRUDA) |
| No role | Updates or deletes an event or a delivery |

The harness acts only through the services' own write paths, the topics and the admin and access endpoints; it never writes a service schema directly. The forced failures of AC3, AC5 and AC6 run on the synthetic data set in DEV and SIT only and are switched off in UAT and production.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 to DF-OPS-197 | `outbox_event` (each service schema) | id, event_type, schema_version, case_id, case_seq, idempotency_key, payload, actor_ref, occurred_at | Write by the owner; read by the harness through the admin read |
| DF-OPS-198 to DF-OPS-206 | `outbox_delivery` (each service schema) | id, event_id, consumer, status, attempt_count, next_attempt_at, last_error_code, delivered_at, task_id | Write by the owner; read by the harness through the admin read |
| None | `processed_event` (each consumer schema) | event id, consumer group, processed at | Write by the consumer; read by the harness through the consumer's own probe |
| None | `idempotency_key` (each service schema) | key, stored response, created at | Write by the owner; asserted on the duplicate path of AC4 |
| DF-WRK-017 to DF-WRK-026 | `task` (rwb_case) | all fields | Write through the P3 contract; read as RW-PLATADM through `GET /api/recovery/case/v1/me/tasks` |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (the owner schema) and `decision_log_entry` (rwb_decision) | all fields | Write through the DP-03 library and the P7 ingest; read through the decision read |
| DF-CAS-001 | `recovery_case` (rwb_case) | id | Read |
| DF-CAS-007 | `recovery_case` (rwb_case) | route_state | Write through the P3 rule step; read through the case read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-006. The harness owns no schema, no table and no field: it reads the delivery rows through the P2 admin read, the case and task rows through the P3 contract, the decision record through the P7 read, and it observes the topics with its own consumer group.

The library tables are created in every service schema by that service's DB story under ASM-0074, not in `rwb_integration` alone; the delivery attempt count that reaches 4 in AC3 and the retry delays are Not specified in the source documents (GAP-0382; ASM-0553).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | Reads the delivery rows of the run by status, consumer, event type and date; the payload is not returned |
| POST | `/api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend` | P2 rwb-integration | Resends an EXCEPTION delivery as RW-PLATADM, and the refusals of AC6 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Platform administration R, U and CRUDA checks for every reader and for the resend |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | P3 rwb-case | The case command that a consumer's case step applies, used to drive the fixture change |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the route state RETRY_QUEUE, RESUME_STATE or EXCEPTION_QUEUE after a signal |
| GET | `/api/recovery/case/v1/me/tasks` | P3 rwb-case | Finds the open RESOLVE_OUTBOX_DELIVERY task and its owner role |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service. The admin read is P2's by the Ownership Map; that it serves the delivery rows of every service through the library admin contract is Not specified in the source documents (GAP-0382; ASM-0554).

#### 12.3 Events published

None. The harness publishes no business event of its own; every event asserted in this story is produced by a wave-1 service and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 rwb-comms | CloudEvents 1.0 binary mode, key caseId, exactly one event per approval; the harness group reads it to prove the producer side of AC1 and AC2 |
| `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The WIN file step of the `win-dispatch` consumer; a failed file publishes FileFailed and is retried inside the workflow |
| `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Order per case and consumer, key caseId; the "ledger" and "reporting-feed" fixtures read them for AC5 |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (produced by every service) | One event per append; the harness reads the record of the move to the exception queue |

The consumer list per event type across services is Not specified in the source documents (GAP-0382; ASM-0554); under that assumption "win-dispatch" resolves to the rwb-integration file step, "ledger" to rwb-source-data's interaction ledger and "reporting-feed" to the rwb-reporting projections, and each fixture subscribes with its own consumer group. Every consumer dedupes on the CloudEvents id through `processed_event` and walks the retry topics at 1 minute, 10 minutes and 1 hour before the `.dlt` (Arch v5 slide 11).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow | `rwb-case` | Workflow ID is the case ID; signals SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED and RETRY_LIMIT_REACHED with the case ID and the consumer reference; the harness reads the resulting route state through the case read |
| deliverFile | Activity | `rwb-integration` | Input the manifest of the WIN file (fileId, batchId, sha256, record count); output the file run; idempotent on fileId; runs inside the 16:00 window of JOB-10 |
| `outboxRelay` (JOB-11) | Relay, not a Temporal workflow | Every service | Publishes the due `outbox_event` rows to the owner topic and advances the delivery state; part of the service template |

The signal names and the task code are the legacy ones; that they are delivered as Temporal signals on `rwb-case` rather than through the legacy published interface is Not specified in the source documents (GAP-0382; ASM-0553).

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `winFileWindow` | Daily at 16:00, Airflow file window with the rwb-comms notice run and the `deliverFile` step of rwb-integration | JOB-10, owned by rwb-comms with rwb-integration performing the delivery (ASM-0062) | JOB-10 WIN notices |
| `outboxRelay` | Every minute in every service | JOB-11, part of the service template and not a Temporal Schedule (ASM-0063) | JOB-11 Outbox sender |

#### 12.7 Tables owned

None. The harness owns no table. The tables it exercises belong to each service schema and to rwb_case, rwb_decision and the platform library, and are listed in section 11 with their owners. The outbox, inbox and idempotency tables are library objects created in every service schema under ASM-0074, and the consumer list per event type is Not specified in the source documents (GAP-0382; ASM-0554).

#### 12.8 Contract fakes

None. This is the integration level: the real platform library, the real services, the real topics and the real `rwb-case` and `rwb-integration` workers replace the contract fakes of RWB-PLT-TE006-APP and RWB-P2-E1007-APP.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 | Two admin outbox calls, the authorise call, one case command, one case read and the task read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 7 event types on 4 topics | `rwb.comms.events.v1`, `rwb.integration.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`; key caseId, CloudEvents 1.0 binary, retry topics and `.dlt` |
| Temporal | None | 1 workflow, 1 activity, 3 signals | CaseWorkflow on `rwb-case` with SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED and RETRY_LIMIT_REACHED; `deliverFile` on `rwb-integration` |
| File | None | 1 file step | The daily WIN file inside the 16:00 window (JOB-10), claim-check manifest with fileId, batchId, sha256 and record count |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/outbox`, with the six test classes `TransactionalOutboxIT`, `RelayAndTopicIT`, `CaseEffectIT`, `DedupeIT`, `OrderAndConcurrencyIT` and `ExceptionQueueIT`, the fixture files, the forced-failure double and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| TopicProbe | Service | Consumes each topic with its own consumer group and asserts one event per change, the key, the envelope, the payload and the schema version |
| DeliveryProbe | Service | Reads the delivery rows through the P2 admin read and asserts status, attempt count and next attempt |
| ConsumerDouble | Service | A configurable consumer that fails on demand, holds or does not hold the case step, and counts the deliveries it sees |
| CaseEffectProbe | Service | Reads the case route state and the task list and asserts the three signals and the open exception task |
| DecisionProbe | Service | Reads `rwb.decision-record.v1` and the decision read and asserts one record per move to the exception queue |
| FileStepProbe | Service | Asserts that the `win-dispatch` consumer produced a `deliverFile` run inside the 16:00 window and a FileDelivered event |
| ResidualAdapterScanner | Service | Reads the service interfaces, the module list and the deployment descriptors and fails on an in-process consumer call or a copied adapter |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The library tables are created by each service's DB story in its own schema; the harness reads them only through the P2 admin read and the P3 and P7 contracts.

**Configuration and reference data**

- The service list, the topic list with the retry and `.dlt` topics, the consumer group names, the queue names and the namespace.
- The consumer list per event type with the owner role and the case-step flag, read as parameters through the rwb-case parameters contract (DP-06).
- The retry settings (3 retries at 1, 5 and 15 minutes in DEV, a data value), the batch size of 200 and the wait intervals.
- The event types and the delivery statuses PENDING, RETRYING, DELIVERED and EXCEPTION, read as reference data through the rwb-case reference-data contract (DP-07).
- The synthetic case "RW-2026-000601", the notice "NT-SYN-0601", the deliveries "OBD-SYN-0001" and "OBD-SYN-0002" and the sequences 11 and 12.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies the DPs name — DP-09 with H RWB-PLT-TE006-CON, DP-06 and DP-07 with their C entries, DP-10, DP-15 and DP-19 with their platform H entries — stay with the platform and service stories this harness proves; this story carries no H, C or X dependency, and its I list names the two stories whose behaviour it exercises, RWB-P2-E1007-APP for the file step and RWB-PLT-TE006-APP for the library (Template and Rules §R5.4 and §R5.5).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Notice approval | Case "RW-2026-000601" with notice "NT-SYN-0601" approved in rwb-comms, one WIN_DISPATCH event, one delivery per consumer | AC1, AC2, TC-TE-006-01-ITG |
| Failing consumer | "win-dispatch" failing at 10:01, 10:02, 10:07 and 10:22, and a second variant failing once then succeeding | AC3, TC-TE-006-02-ITG, TC-TE-006-04-ITG |
| Rolled-back approval | The same approval with the transaction rolled back after the outbox write | AC1, TC-TE-006-03-ITG |
| Duplicate key and duplicate delivery | Two approvals with key "WIN_DISPATCH:NT-SYN-0601" and one event delivered twice to one consumer | AC4, TC-TE-006-05-ITG |
| 200 due deliveries | 200 due deliveries and two relay instances over one producer schema | AC5, TC-TE-006-06-ITG |
| Sequences 11 and 12 | CaseTransferred at sequence 11 and CaseStateChanged at sequence 12 with "ledger" failing on 11 | AC5, TC-TE-006-07-ITG, TC-TE-006-08-ITG |
| Resend pair | "OBD-SYN-0001" in EXCEPTION and "OBD-SYN-0002" in DELIVERED, plus a delivery ID that does not exist | AC6, TC-TE-006-09-ITG |
| Event with no case | An event without a case ID whose only consumer fails 4 times | AC6, TC-TE-006-10-ITG |
| Retry change | The retry delays changed to 2, 10 and 30 minutes before the run | AC3, TC-TE-006-11-ITG |
| Role set | RW-PLATADM, RW-DATASTEW and RW-COE with their Platform administration letters | AC6, TC-TE-006-12-ITG |
| Forced decision failure | The decision record refused at the exception move | AC3, TC-TE-006-13-ITG |

**Run order.** Preflight; one approval and its deliveries (AC1); the relay, the topic read and the file step (AC2); the forced failures, the three signals, the task and the decision record (AC3); the duplicate key and the duplicate delivery (AC4); order and the 200 deliveries (AC5); the resend pair, the `.dlt`, the role refusals and the 404 (AC6); the residual-adapter scan; cleanup of the DEV fixtures. A failing step stops the run and the report names the criterion, the service, the topic and the evidence.

**Done when.** The 19 test cases of section 16 pass on the real services in DEV and SIT, every change yields one event and one delivery per consumer, the order holds per case and consumer on the 200-delivery and two-sequence fixtures, the `.dlt` and its alert appear, the three signals change the case route state as R-UNI-33, R-UNI-35 and R-UNI-36 require, RESOLVE_OUTBOX_DELIVERY is open for the configured owner role, one decision record exists per move to the exception queue, and the residual-adapter scan finds no in-process consumer call.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Task text when a delivery enters the exception queue | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | The decision record cannot be written at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The delivery or the case is not in the caller's scope | This case is not in your scope. |

The six texts are copied unchanged from RWB-TE-006 and section 14 of that story; this story adds no message text. Report lines of the harness are for developers and are not part of the message standard. In MSG-P2-001, {interface} is the consumer name and {item} the event type and case number.

### 15. Screens and states

No screen in this story, and the harness renders nothing: it calls the admin, case, task and access endpoints and reads the topics directly. The task RESOLVE_OUTBOX_DELIVERY appears on SCR-09 Exception queue with MSG-P2-001 for the owner role when the case is in the exception queue, and the deliveries appear on SCR-44 Interface and job monitor; both screens belong to their own stories and are out of scope here. The states the harness observes are the delivery, relay, consumer, case route and run states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-01-ITG | legacy AC1, BR1, BR3, BR7 | Integration | Notice NT-SYN-0601 approved at 10:00; the real `deliverFile` step replaces the stub |
| TC-TE-006-02-ITG | legacy AC2, BR5, BR6, BR8 | Integration | "win-dispatch" failing four times; the task, the record and RETRY_LIMIT_REACHED |
| TC-TE-006-03-ITG | legacy AC3, BR1 | Integration | The approval rolled back after the publish |
| TC-TE-006-04-ITG | legacy AC4, BR6 | Integration | "win-dispatch" failing once, then succeeding |
| TC-TE-006-05-ITG | legacy AC5, BR2 | Integration | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06-ITG | legacy AC6 | Integration | 200 due deliveries, two relay instances |
| TC-TE-006-07-ITG | legacy AC7, BR4 | Integration | Sequences 11 and 12, "ledger" failing on 11 |
| TC-TE-006-08-ITG | legacy AC8, BR3 | Integration | "ledger" fails and "reporting-feed" succeeds on one CaseAllocated event |
| TC-TE-006-09-ITG | legacy AC9 | Integration | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 in DELIVERED |
| TC-TE-006-10-ITG | legacy AC10 | Integration | An event with no case and a consumer failing four times; the alert |
| TC-TE-006-11-ITG | legacy AC11, BR11 | Integration | Retry delays changed to 2, 10 and 30 minutes before the run, read from the parameters contract |
| TC-TE-006-12-ITG | Access | Integration | RW-DATASTEW resends a delivery and is refused with MSG-P4-002 after the rwb-access check |
| TC-TE-006-13-ITG | Principle 5 | Integration | The decision record forced to fail at the exception move; the delivery stays RETRYING; MSG-P7-003 in the log; the incident |
| TC-ITG-TE006-01 | AC1, BR1 | Integration | One approval and one rolled-back approval in rwb_comms; two consumers |
| TC-ITG-TE006-02 | AC2, BR7, BR9, BR10 | End to end | One event on the owner topic and the `deliverFile` run inside the 16:00 window |
| TC-ITG-TE006-03 | AC3, BR5, BR6, BR8 | End to end | One consumer failing four times, one failing once; the three signals, the task and the record |
| TC-ITG-TE006-04 | AC4, BR2 | Integration | A duplicate idempotency key and a duplicate delivery to one consumer |
| TC-ITG-TE006-05 | AC5, BR4 | Integration | Sequences 11 and 12; 200 due deliveries on two relay instances |
| TC-ITG-TE006-06 | AC6, BR5 | Component | The resend pair, the missing delivery, the `.dlt` alert and the role refusal |

The legacy acceptance criteria of RWB-TE-006 are owned by RWB-PLT-TE006-APP, so the Covers cell of a legacy copy names those legacy AC numbers and not the criteria of this story; the legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC6 carry TC-ITG-TE006-01 to TC-ITG-TE006-06.

### 17. Guardrails

- No business value in code: the consumer list, the owner roles, the case-step flags, the retry counts and delays, the batch size and the alert route are parameters and reference data (DP-06, DP-07); the harness reads them through the rwb-case contracts.
- No personal data in events, workflow inputs, logs, fixtures or the report: case IDs, notice references, event IDs, delivery IDs, consumer names and codes only, and the admin read does not return the payload.
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness reads the deliveries through the P2 admin read and the case and task through the P3 contract, and it never joins two schemas.
- No event and no delivery is deleted; a delivery leaves the exception queue only by being resent, and a correction of an event is a new event.
- One topic per service and one event type per business fact (BR9): a service that publishes another service's topic, or a producer that skips its outbox, fails the run.
- The retry topics and the `.dlt` are part of every topic's contract (BR9); a topic without them, or a dead letter with no alert, fails the preflight.
- No in-process consumer call and no copied adapter survives (BR10, DP-16); the residual-adapter scan is a regression test, not a one-off check.
- The harness never uses production data and never points at a production namespace; its forced failures exist only in DEV and SIT.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | `outbox_event`, `outbox_delivery` and `processed_event` in every service schema; the owner topics with their retry topics and `.dlt`; the relay JOB-11; the CaseWorkflow signals of `rwb-case`; RESOLVE_OUTBOX_DELIVERY; the `rwb.decision-record.v1` record of the move; the P2 admin resend | TC-TE-006-01-ITG to TC-TE-006-13-ITG, TC-ITG-TE006-01 to TC-ITG-TE006-06 |

The rules of the requirement are R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39 and R-UNI-40, as in RWB-TE-006 section 18.

### 19. Out of scope

- The library itself: the contract of `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`, the statuses, the retry scheduling and the relay as code (RWB-PLT-TE006-CON, RWB-PLT-TE006-APP).
- The schema, the grants and the indexes of the four library tables in each service schema (each service's DB story; RWB-PLT-TE006-DB).
- The two admin endpoints in rwb-integration and their access checks (P2 by the Ownership Map; RWB-P2-E1007-APP).
- The consumers themselves — rwb-comms notices, the rwb-source-data ledger, the rwb-reporting projections, the rwb-case signals and the rwb-decision ingest — which this story exercises and owns none of.
- The topic provisioning, the retry and `.dlt` topics, the schema registry and the alert route (RWB-PLT-EVT and the operations stories).
- The `deliverFile` activity, the file run and the 16:00 WIN window (RWB-P2-E1007-APP, RWB-E2 outbound file stories).
- The SCR-09 exception queue and SCR-44 interface and job monitor screens (their own stories).
- The retry values, the alert routing and the consumer list as approved business data (DL11; GAP-0382).
