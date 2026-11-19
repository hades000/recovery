<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB TE 006 Outbox and retry for outbound work v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB TE 006 Outbox and retry for outbound work v1.md`  
> **Converted from:** Markdown (copied)

# RWB-TE-006 Outbox and retry for outbound work

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-006 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Program, section 5.2 and section 6.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry**, so that **no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit**.

## 2. Business rationale

The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it. The outbox stores each event with the change, a sender delivers it to every consumer at least once in case order, retries on a schedule held as data, and moves a delivery that keeps failing to the exception queue with a task. It meets REQ-DRI-007 (retry on a defined schedule; exception queue with a task for a named owner) and NFR-025 and NFR-026. The measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1).

## 3. Preconditions

- RWB-E1-044 (versioned migrations), RWB-E1-027 (decision log writer) and RWB-E1-007 (integration adapters, IdempotencyGuard and the outbound file sender) are done.
- The consumer list is loaded in the configuration service (RWB-E1-042) under rwb.integration.outbox.consumers: consumer name, the event types it takes, its owner role, and whether it holds a case step (for example the consumer "win-dispatch" of the work request WIN_DISPATCH holds the case step, owner role RW-PLATADM; assumed).
- The retry settings are loaded under rwb.integration.outbox.retry: 3 retries at 1, 5 and 15 minutes after the previous attempt (assumed; NFR-026, DL11).
- Quartz runs clustered in the ACE service; JOB-11 Outbox sender runs every minute.
- Feature flag `rwb.integration.outbox` is on.

## 4. Flow

1. Business service (for example notice approval): calls OutboxWriter.publish inside its own transaction with the event type (an event from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH), schema version, case ID, payload references, actor and idempotency key.
2. OutboxWriter: writes one outbox_event row with the next case sequence, and one outbox_delivery row per consumer listed for the event type.
3. Database: commits the change, the event and its deliveries together, or none of them.
4. JOB-11 Outbox sender (event step): every minute selects due deliveries with a row lock that skips rows another instance holds, oldest case sequence first, taking only the lowest open sequence per case and consumer.
5. OutboxSender: calls the consumer with the event header (event ID, idempotency key, schema version, occurred time, actor) and payload; each consumer checks the key through IdempotencyGuard (RWB-E1-007) before it acts.
6. OutboxSender: on success marks the delivery DELIVERED; when the delivery had failed before and the consumer holds a case step, raises RETRY_SUCCEEDED for the case (R-UNI-35).
7. OutboxSender: on a failure adds 1 to the attempt count and sets the next attempt from the retry settings; on the first failure of a consumer that holds a case step, raises SYSTEM_UNAVAILABLE for the case (R-UNI-33).
8. OutboxSender: when the retries are used, sets the delivery to EXCEPTION, raises task RESOLVE_OUTBOX_DELIVERY for the consumer's owner role on the case and, for a consumer that holds a case step, raises RETRY_LIMIT_REACHED (R-UNI-36), which writes the decision log entry; all in one transaction.
9. Platform administrator: reads exception deliveries (GET /admin/outbox/deliveries) and, once the consumer is fixed, sends one again (POST /admin/outbox/deliveries/{deliveryId}/resend).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist | None | AC3 |
| X2 | A consumer fails once and then succeeds | Delivery DELIVERED on the retry; the case resumes when the consumer holds a case step (R-UNI-35) | None | AC4 |
| X3 | The same idempotency key is published twice | One event exists | None | AC5 |
| X4 | Two service instances run the sender at once | Each delivery is made once | None | AC6 |
| X5 | An earlier event for the same case and consumer is failing | Later events for that case and consumer wait | None | AC7 |
| X6 | One consumer fails and another succeeds on the same event | Each consumer's delivery has its own state | None | AC8 |
| X7 | A platform administrator sends a delivery that is not in EXCEPTION | Refused with 409 | MSG-P2-022 | AC9 |
| X8 | An event with no case fails past its limit | EXCEPTION and an alert to the platform administrator; no task, no case event | MSG-P2-001 | AC10 |
| X9 | The retry settings are changed | The next attempt uses the new delays | None | AC11 |
| X10 | The decision log cannot be written when the limit is reached | Nothing changes; the delivery stays RETRYING and is tried at the next run; incident raised (R-UNI-39) | MSG-P7-003 | Principle 5 test TC-TE-006-13 |
| X11 | A role without Platform administration U sends a delivery again | Refused with 403 | MSG-P4-002 | Access test TC-TE-006-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the migration tool, the decision log writer and the IdempotencyGuard of Epic 1; consumers are listed in configuration |
| Negotiable | Consumers, owners, retry counts and delays are configuration |
| Valuable | No event or outbound request is lost or sent for a change that rolled back |
| Estimable | Two tables, one writer, one sender step, two admin endpoints |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses a stub consumer that fails on demand |

## 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work

  Background:
    Given consumer "win-dispatch" takes work request WIN_DISPATCH, holds the case step and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged, do not hold the case step and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 Sent after commit
    Given a notice approved
    When the transaction commits at 14 December 2026 10:00:00
    Then the outbox holds one WIN_DISPATCH request for case "RW-2026-000601" with one delivery for "win-dispatch"
    Then the header holds the event ID, idempotency key "WIN_DISPATCH:NT-SYN-0601", schema version 1, occurred time and actor
    Then the payload holds notice and case references only, with no name, address or identifier
    Then at the 10:01 run the sender delivers it and "win-dispatch" passes the notice to OutboundFiles.enqueue for the day's WIN file
    Then the delivery has status DELIVERED

  Scenario: AC2 Retry limit
    Given a target down for longer than the retry limit
    When "win-dispatch" fails at 10:01, 10:02, 10:07 and 10:22
    Then the system makes no fifth attempt
    Then the item moves to the exception queue: the "win-dispatch" delivery has status EXCEPTION and attempt count 4
    Then the system raises task RESOLVE_OUTBOX_DELIVERY on case "RW-2026-000601" for role RW-PLATADM
    Then event RETRY_LIMIT_REACHED moves the case to EXCEPTION_QUEUE by R-UNI-36 with one decision log entry

  Scenario: AC3 Nothing is sent for a change that did not commit
    Given the notice approval fails after OutboxWriter.publish and the transaction rolls back
    When the sender runs
    Then no event and no delivery exist for "NT-SYN-0601"

  Scenario: AC4 A retry that succeeds
    Given "win-dispatch" fails at 10:01 and the case moves to RETRY_QUEUE by R-UNI-33
    When the attempt at 10:02 succeeds
    Then the system delivers the delivery status with attempt count 2
    Then event RETRY_SUCCEEDED returns the case to the state it paused in by R-UNI-35

  Scenario: AC5 The same event is written once
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the outbox holds one event with that key
    Then the second transaction receives DuplicateOutboxKeyException and changes nothing

  Scenario: AC6 Two sender instances
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then the system makes each delivery once
    Then the delivery log holds 200 calls

  Scenario: AC7 Order per case and consumer
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the sender runs
    Then the system does not deliver sequence 12 to "ledger" until sequence 11 is DELIVERED

  Scenario: AC8 Consumers are independent
    Given event CaseAllocated for case "RW-2026-000601"
    When "ledger" fails and "reporting-feed" succeeds at 10:01
    Then the system delivers the "reporting-feed" delivery and the "ledger" delivery is RETRYING with next attempt 10:02
    Then the case route state does not change, because "ledger" does not hold the case step

  Scenario: AC9 Sending an exception delivery again
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator sends it again
    Then the response is 200 with message MSG-GEN-005
    Then the delivery status is PENDING with attempt count 0 and due at the next run
    When the platform administrator sends delivery "OBD-SYN-0002" with status DELIVERED again
    Then the response is 409 with message MSG-P2-022

  Scenario: AC10 An event with no case
    Given an event with no case whose only consumer fails 4 times
    When the retries are used
    Then the delivery status is EXCEPTION
    Then the system sends an alert to the platform administrator within 15 minutes
    Then no task and no case event are raised

  Scenario: AC11 Retry settings come from configuration
    Given the retry delays are changed in the configuration service to 2, 10 and 30 minutes at 09:00
    When "ledger" fails at 10:01
    Then the next attempt is due at 10:03
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction as the change: no event without the change and no change without the event | events.txt Rules, Transactions |
| BR2 | Each event carries an event ID and an idempotency key unique in the outbox; consumers drop a repeat through IdempotencyGuard | events.txt Rules, Duplicates; R-UNI-40 |
| BR3 | Delivery is at least once; each consumer has its own delivery state | events.txt Rules, Delivery |
| BR4 | Events for one case reach each consumer in the order they were written | events.txt Rules, Ordering |
| BR5 | A failed delivery is retried on the schedule; after the last retry it moves to the exception queue with a task for the consumer's owner role | events.txt Rules, Failure; NFR-026; REQ-DRI-007 |
| BR6 | For a consumer that holds a case step, the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED, and the limit RETRY_LIMIT_REACHED | R-UNI-33; R-UNI-35; R-UNI-36 |
| BR7 | Payloads hold references and codes, never personal data; the event carries its schema version | events.txt Rules, Payload and Versioning |
| BR8 | The move to the exception queue for a case does not happen unless its decision log entry is written | R-UNI-39; Principle 5; CTL-06 |
| BR9 | Consumers, owners, retry counts and delays are read from configuration | Principle 1; DL11 |

## 9. State transitions

Case status does not change. For a consumer that holds a case step, the route state changes through the universal rules; each delivery has its own status.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a consumer that holds the case step | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds | RESUME_STATE (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Retries used | EXCEPTION_QUEUE (R-UNI-36) |
| Delivery PENDING or RETRYING | Consumer succeeds | None | Delivery DELIVERED |
| Delivery PENDING | Consumer fails | Retries left | Delivery RETRYING |
| Delivery RETRYING | Consumer fails | No retries left | Delivery EXCEPTION |
| Delivery EXCEPTION | Sent again by the platform administrator | None | Delivery PENDING |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the sender step, applies R-UNI-33, R-UNI-35 and R-UNI-36 and raises the task |
| SY-DECLOG, decision log writer | Writes the entry for the move to the exception queue |
| RW-PLATADM, platform administrator | Reads deliveries and sends an exception delivery again (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM, security administrator | Reads deliveries (Platform administration CRUDA) |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

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
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write, through the P3 published interface |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P3 rule step that calls the P7 writer |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 rule step |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Published interfaces**

```java
// recovery.integration.api; joins the caller's transaction
UUID OutboxWriter.publish(OutboxEvent event);
//   OutboxEvent: eventType (EV-01 to EV-28 names, or a work request type such as WIN_DISPATCH), schemaVersion, caseId (nullable), payload (references only), actorRef, idempotencyKey
//   throws DuplicateOutboxKeyException when the key exists
// Implemented by each consumer and listed under its consumer name
ConsumeResult OutboxConsumer.consume(EventHeader header, JsonNode payload);   // OK or FAILED(code)
// P3 interfaces used on failure and recovery
void CaseEvents.raise(UUID caseId, String eventCode, String reference);  // SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED
UUID TaskApi.raiseTask(UUID caseId, String taskCode, String ownerRole);
// RWB-E1-007, called by each consumer before it acts
boolean IdempotencyGuard.firstTime(String consumer, String idempotencyKey);
```

**Job**

| Item | Value |
|---|---|
| Trigger | JOB-11 Outbox sender, every minute; this story adds the event step beside the outbound file step of RWB-E1-007 |
| Input | outbox_delivery rows with status PENDING or RETRYING and next_attempt_at at or before now |
| Output | Deliveries DELIVERED, RETRYING or EXCEPTION; case events; tasks; alerts |
| Events published | None of its own; it delivers EV-01 to EV-28 to their consumers |
| Idempotency key | outbox_event.idempotency_key, passed to each consumer in the header |
| Restart | Rows are locked per delivery with skip-locked selection; a delivery in flight when an instance stops is retried at its next attempt time and the consumer drops the repeat by its key |

**GET /api/recovery/v1/admin/outbox/deliveries** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Query | status, consumer, eventType, from, to, page, size |
| Response 200 | OutboxDeliveryPage: items of OutboxDelivery (id, eventId, eventType, caseId, consumer, status, attemptCount, nextAttemptAt, lastErrorCode, deliveredAt, createdAt), page, size, total. The payload is not returned |
| 403 | Role lacks Platform administration R (MSG-P4-002) |
| Authorization | Platform administration, right R |
| Idempotency | Read only |

**POST /api/recovery/v1/admin/outbox/deliveries/{deliveryId}/resend** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Request | None |
| Response 200 | OutboxDelivery with status PENDING and attempt count 0; message MSG-GEN-005 |
| 403 | Role lacks Platform administration U (MSG-P4-002) |
| 404 | Delivery not found (MSG-P4-003) |
| 409 | Delivery not in EXCEPTION (MSG-P2-022) |
| Authorization | Platform administration, right U; written to the ACE audit log with the user and the time |
| Idempotency | A second call finds the delivery PENDING and returns 409 |

## 13. Solution plan

**Package.** Folder `recovery/integration/outbox`, Java package `<ACE base package>.recovery.integration.outbox`; OutboxWriter and OutboxConsumer in `recovery.integration.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OutboxWriter | Published interface | Writes the event and one delivery per listed consumer in the caller's transaction (BR1, BR2, BR7) |
| OutboxEventEntity, OutboxDeliveryEntity | Entity | The two new rows |
| OutboxRepository | Repository | Skip-locked selection of due deliveries in case order per consumer (BR4) |
| OutboxSender | Service | Delivery, retry scheduling, case events and exception move (BR3, BR5, BR6, BR8) |
| ConsumerCatalog | Service | Reads the consumer list and the retry settings (BR9) |
| OutboxSenderEventStep | Job | The event step of JOB-11 |
| OutboxAdminController | Controller | GET /admin/outbox/deliveries and the retry endpoint |

**Database.** Flyway migration `V<next>__create_outbox_event.sql` in the P2 migration folder creates:
- outbox_event (id uuid primary key, event_type varchar(40) not null, schema_version integer not null, case_id uuid, case_seq bigint, idempotency_key varchar(120) not null, payload jsonb not null, actor_ref varchar(64), occurred_at timestamptz not null, plus the standard columns), with `UNIQUE (idempotency_key)` and `UNIQUE (case_id, case_seq)`.
- outbox_delivery (id uuid primary key, event_id uuid not null references outbox_event, consumer varchar(60) not null, status varchar(12) not null default 'PENDING', attempt_count integer not null default 0, next_attempt_at timestamptz not null, last_error_code varchar(40), delivered_at timestamptz, task_id uuid, plus the standard columns), with `UNIQUE (event_id, consumer)`, `CHECK (status IN ('PENDING','RETRYING','DELIVERED','EXCEPTION'))` and index `ix_outbox_delivery_due ON outbox_delivery (next_attempt_at) WHERE status IN ('PENDING','RETRYING')`.
case_seq is the case's highest sequence plus 1, taken under a lock on the case's latest outbox row.

**Configuration and reference data.** rwb.integration.outbox.consumers and rwb.integration.outbox.retry (assumed values in section 3; DL11), batch size 200 per run (assumed), loaded by RW-REFADM through the configuration service; the alert route to the operations channel from RWB-E1-056.

**Build steps**

1. Write the migration and the two entities; test the unique keys (AC5).
2. Write OutboxWriter joining the caller's transaction; test commit and rollback (AC1, AC3).
3. Write OutboxRepository with skip-locked selection and order per case and consumer; test two instances (AC6), order (AC7) and independent consumers (AC8).
4. Write OutboxSender with ConsumerCatalog and a stub consumer; test retry and success (AC2, AC4, AC11).
5. Add the case events, the task and the exception move through the P3 interfaces; test the forced decision log failure.
6. Add the alert for events with no case (AC10).
7. Add OutboxSenderEventStep to JOB-11.
8. Write OutboxAdminController with the access check and the audit write (AC9 and the access test).

**Feature flag.** `rwb.integration.outbox`. Off: the event step does not run and deliveries stay PENDING; the writer still records events so nothing is lost when it is switched on.

**Done when.** The tests in section 16 pass and the JOB-11 event step shows its runs on the job monitoring of RWB-E1-056.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Task text when a delivery enters the exception queue (new) | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Sending again a delivery that is not in EXCEPTION (new) | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | Decision log write failed at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Delivery not found | This case is not in your scope. |

In MSG-P2-001, {interface} is the consumer name and {item} the event type and case number. Thai text for each message follows decision DL10.

## 15. Screens and states

No screen of its own in Epic 1. The task RESOLVE_OUTBOX_DELIVERY appears on SCR-09 Exception queue (states Loading and List) for the owner role, with MSG-P2-001. The platform administrator uses the two admin endpoints; SCR-44 Interface and job monitor shows the deliveries from Epic 2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-01 | AC1, BR1, BR3, BR7 | System | Notice NT-SYN-0601 approved at 10:00; win-dispatch stub succeeds |
| TC-TE-006-02 | AC2, BR5, BR6, BR8 | System | win-dispatch stub fails 4 times |
| TC-TE-006-03 | AC3, BR1 | System | Approval rolled back after publish |
| TC-TE-006-04 | AC4, BR6 | System | win-dispatch stub fails once, then succeeds |
| TC-TE-006-05 | AC5, BR2 | System | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06 | AC6 | System | 200 due deliveries, two instances |
| TC-TE-006-07 | AC7, BR4 | System | Sequences 11 and 12, ledger stub failing on 11 |
| TC-TE-006-08 | AC8, BR3 | System | ledger fails and reporting-feed succeeds on one CaseAllocated event |
| TC-TE-006-09 | AC9 | System | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 DELIVERED |
| TC-TE-006-10 | AC10 | System | Event with no case, consumer failing 4 times |
| TC-TE-006-11 | AC11, BR9 | System | Retry delays changed to 2, 10 and 30 minutes before the run |
| TC-TE-006-12 | Access | Access | RW-DATASTEW sends a delivery again; refused with MSG-P4-002 |
| TC-TE-006-13 | Principle 5 | Resilience | Decision log write forced to fail at the exception move; delivery stays RETRYING; MSG-P7-003 in the job log; incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: consumers, owners, retry counts, delays and batch size are configuration.
- No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload.
- No read of another module's tables: case events and tasks go through the P3 interfaces; the decision log through P7.
- No event or delivery is deleted; a delivery leaves the exception queue only by being sent again.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-TE-006-01 to TC-TE-006-13 |

## 19. Out of scope

- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-E1-007.
- The consumers themselves, for example the ledger listener: RWB-E1-067 and RWB-E2-034.
- The interface and job monitor screen: SCR-44 in Epic 2 and Epic 8.
- Retry values: DL11.
