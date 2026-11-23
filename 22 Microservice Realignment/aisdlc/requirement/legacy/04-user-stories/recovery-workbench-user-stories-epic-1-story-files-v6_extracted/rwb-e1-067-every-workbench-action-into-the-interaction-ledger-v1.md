<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 067 Every Workbench action into the interaction ledger v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 067 Every Workbench action into the interaction ledger v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-067 Every Workbench action into the interaction ledger

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-067 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-ILG-01 Write every Workbench event to the ledger; FEAT-ILG-04 Reject a duplicate ledger entry |
| Requirement IDs | REQ-ILG-005, REQ-ILG-002, REQ-ILG-007 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-002, REQ-ILG-005, REQ-ILG-007) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-066 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

## 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. If these actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them. Each action already publishes an application event to the outbox in the same transaction as the change (events.txt); a ledger listener turns each event into one entry with its source and actor. Events are delivered at least once, so the listener rejects a repeat by its idempotency key and counts it. Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007.

## 3. Preconditions

- RWB-E1-066 is done: InteractionLedgerWriter, the case sequence and LOV-LEDGER-EVENT exist.
- RWB-TE-006 is done: the outbox delivers events at least once, per case in written order, with event ID, idempotency key, schema version, occurred time and actor in the event header, and moves an event to the exception queue after the retry limit.
- The publishing stories exist for EV-01 CaseCreated and EV-02 CaseAllocated (RWB-E1-018, RWB-E1-020), EV-04 CaseTransferred (RWB-E1-021), EV-16 DocumentStored (RWB-E1-024), EV-08 DecisionRecorded (RWB-E1-027) and EV-19 TimerBreached.
- The listener runs as service identity SY-CASEWF (Case record C).

## 4. Flow

1. Publishing module: commits its change and writes the event to the outbox in the same transaction.
2. Outbox: delivers the event to LedgerEventListener, in order per case.
3. LedgerEventListener: checks the schema version is the current or the previous version for the event.
4. LedgerEventMapper: maps the event to a LedgerEntryCommand: EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED, EV-16 to DOCUMENT_ATTACHED, EV-08 to DECISION_TAKEN with the decision log entry ID.
5. LedgerEventMapper: sets actor from the event header (user ID or service identity), source system WORKBENCH, source reference as the owning module and event ID, and the event's idempotency key.
6. InteractionLedgerWriter: appends the entry with the next case_seq.
7. LedgerDuplicateService: when the idempotency key already exists, writes no entry and adds 1 to the hit count for that key (R-UNI-40).
8. Outbox: marks the event processed for the ledger consumer.
9. On failure: the outbox retries; after three retries the event goes to the exception queue with owner RW-PLATADM and incident LEDGER_WRITE_FAILED is raised.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same key | One entry; the repeat is counted | None | AC3 |
| X2 | An event with a schema version that is neither current nor previous | Not written; moved to the exception queue with owner RW-PLATADM | None (exception queue item) | AC4 |
| X3 | The ledger write fails | Retried three times, then the exception queue and an incident; the event is not discarded | MSG-P1-022 (incident detail) | AC5 |
| X4 | Events for one case arrive in written order | Entries follow that order in case_seq | None | AC6 |
| X5 | The same event reaches two consumer threads at once | One entry; one hit counted | None | AC7 |
| X6 | An event names a case that does not exist | Not written; moved to the exception queue | None (exception queue item) | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ledger writer (RWB-E1-066) and the outbox (RWB-TE-006); the events come from stories earlier in Epic 1 |
| Negotiable | The event to entry map is configuration; the story fixes the listener, the duplicate rule and the failure path |
| Valuable | The case owner sees every Workbench action in the case history |
| Estimable | One listener, one mapper, one duplicate table |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion publishes synthetic events and reads the ledger |

## 7. Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger

  Background:
    Given case "RW-2026-000301" exists with no ledger entries
    Given the ledger listener runs as SY-CASEWF

  Scenario: AC1 Workbench events are captured
    Given the case is created at 2026-12-01T06:10+07:00 by SY-CASEWF
    Given allocated to queue "MTG-BKK-CO" at 06:40 by SY-RULES
    Given transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00
    Given has document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR
    Given has timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00
    Given has decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00
    When each action completes
    Then the ledger holds 6 entries for the case with events CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN
    Then each entry carries the case identifier, the event, the timestamp and the actor

  Scenario: AC2 The entry names its source
    Given the CASE_ALLOCATED entry of case "RW-2026-000301"
    When it is read
    Then it names source system "WORKBENCH", source reference "P3 case and workflow, EV-02 CaseAllocated" and actor "SY-RULES"
    Then the CASE_TRANSFERRED entry names actor type "USER" and actor "u-teammgr-03"

  Scenario: AC3 Nothing is written twice
    Given CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201" was written to the ledger
    When the same event arrives again with the same key
    Then one CASE_ALLOCATED entry exists
    Then the hit count for key "EV-02-RW-2026-000301-20261201" is 1

  Scenario: AC4 An event with an unknown schema version
    Given CaseTransferred is at schema version 2 and accepts version 1
    When a CaseTransferred event with schema version 3 arrives for case "RW-2026-000301"
    Then the system writes no entry
    Then the event is in the exception queue with owner RW-PLATADM and reason "schema version 3 not accepted"

  Scenario: AC5 The ledger write fails for an event
    Given every ledger insert fails
    When DocumentStored for case "RW-2026-000301" is delivered
    Then the delivery is tried 4 times in all
    Then the event is in the exception queue with owner RW-PLATADM
    Then the system raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301"

  Scenario: AC6 Entries follow the order the events were written
    Given CaseCreated and CaseAllocated for case "RW-2026-000301" are written to the outbox in that order
    When both are processed
    Then CASE_CREATED has case_seq 1 and CASE_ALLOCATED has case_seq 2

  Scenario: AC7 The same event on two threads at once
    Given CaseCreated for case "RW-2026-000301" is delivered to two consumer threads at the same moment
    When both threads process it
    Then one CASE_CREATED entry exists
    Then the hit count for its key is 1

  Scenario: AC8 An event for a case that does not exist
    When DocumentStored arrives for case ID "00000000-0000-0000-0000-000000000998"
    Then the system writes no entry
    Then the event is in the exception queue with reason "case not found"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen | REQ-ILG-005; EV-01, EV-02, EV-04, EV-19, EV-16, EV-08 (events.txt) |
| BR2 | Every entry names the system or person that produced it | REQ-ILG-002 |
| BR3 | The same event with the same key produces one entry, and the repeat is counted | R-UNI-40; REQ-ILG-007 |
| BR4 | Events for one case are processed in the order they were written | Events rule "Ordering" (events.txt) |
| BR5 | A consumer failure retries, then goes to the exception queue with its owner | Events rule "Failure" (events.txt); R-UNI-36 |
| BR6 | A consumer accepts the current and the previous schema version | Events rule "Versioning" (events.txt) |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt) |

## 9. State transitions

None. This story does not change a case status. It adds ledger entries and moves failed events to the exception queue state EXCEPTION_QUEUE for the platform team (R-UNI-36).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the ledger listener and appends entries (Case record C) |
| SY-RULES, SY-OCR, SY-DECLOG | Appear as actors on entries; do not call the writer |
| SY-AGENT, agent platform | May not append (Case record R) |
| RW-PLATADM, platform administrator | Owns exception queue items from the listener; receives the incident |
| RW-CASEOWN, case owner | Reads the entries through RWB-E1-068 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-WRK-009 | assignment | id | Read |
| DF-DOC-001 | document | id | Read |
| DF-DEC-001 | decision_log_entry | id | Read |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-015 | interaction | actor_type | Write |
| DF-INT-016 | interaction | actor_ref | Write |
| DF-INT-017 | interaction | source_ref | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-019 | interaction | case_seq | Write |
| DF-INT-020 | interaction | decision_log_id | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write |

Record IDs of assignments, documents and decisions are read from the event payload, not from their tables. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Listener**

| Item | Value |
|---|---|
| Trigger | Outbox delivery of EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-08 DecisionRecorded, EV-16 DocumentStored, EV-19 TimerBreached |
| Job name | None in batch.txt; the outbox consumer runs in the service, not as a scheduled job |
| Input | Event header (event ID, idempotency key, schema version, occurred time, actor) and payload as in events.txt |
| Output | One interaction row per event, or one hit on processed_event |
| Events published | None |
| Idempotency key | The event's idempotency key, unique on interaction.idempotency_key |
| Restart behavior | At-least-once delivery; an unprocessed event is delivered again after a restart; three retries, then the exception queue (NFR-026) |

**Published interface used (P1, from RWB-E1-066)**

```java
LedgerEntryRef InteractionLedgerWriter.append(LedgerEntryCommand command);
```

The writer checks that the calling identity holds Case record C; a call from an identity without it throws AccessDeniedException mapped to MSG-P4-002.

## 13. Solution plan

- Package: folder `recovery/dataengine/ledger/events`, Java package `recovery.dataengine.ledger.events`.

| Component | Type | Responsibility |
|---|---|---|
| LedgerEventListener | Listener | Outbox consumer for the six events; version check; calls the mapper and the writer |
| LedgerEventMapper | Service | Event to LedgerEntryCommand per the map in the flow, read from configuration |
| LedgerDuplicateService | Service | Catches the unique key clash on idempotency_key and adds a hit |
| InteractionDuplicateRepository | Repository | Upserts processed_event |
| InteractionDuplicate | Entity | One row per repeated idempotency key |

- Database: table processed_event (new, Flyway migration in this story) with idempotency_key varchar(120) primary key, first_interaction_id uuid not null, hit_count integer not null, last_hit_at timestamptz not null, plus the standard columns. Uses the interaction columns added by RWB-E1-066.
- Configuration and reference data: event to ledger event map in `rwb.dataengine.ledger.event-map` (EV-01=CASE_CREATED, EV-02=CASE_ALLOCATED, EV-04=CASE_TRANSFERRED, EV-08=DECISION_TAKEN, EV-16=DOCUMENT_ATTACHED, EV-19=CASE_ESCALATED); retry limit 3 from the outbox settings (NFR-026; DL11).
- Build steps:
  1. Flyway migration for processed_event.
  2. LedgerEventMapper with the configured map and the source reference "<owning module>, <event ID> <event name>".
  3. LedgerEventListener subscribed to the six events with the schema version check.
  4. LedgerDuplicateService on the unique key clash, inside a new transaction so the hit is recorded.
  5. Identity check in InteractionLedgerWriter for Case record C.
  6. Failure path through the outbox retry and exception queue, with LEDGER_WRITE_FAILED.
  7. Tests for AC1 to AC8 and the access test, publishing synthetic events through the outbox test fixture.
- Feature flag: `rwb.dataengine.ledger-events`.
- Done when: the tests in section 16 pass and each of the six events has the ledger as a consumer in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | Ledger write failed, carried on the incident and the exception queue item | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without Case record C calls the writer | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator sees failed events on SCR-09 Exception queue (Epic 1, state List). The case owner reads the entries through RWB-E1-068 on SCR-03 Case record (Read only).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01 | AC1, BR1 | System | Six synthetic events for case RW-2026-000301 |
| TC-E1-067-02 | AC2, BR2 | System | CASE_ALLOCATED and CASE_TRANSFERRED entries |
| TC-E1-067-03 | AC3, BR3 | System | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201 |
| TC-E1-067-04 | AC4, BR6 | System | CaseTransferred at schema version 3 |
| TC-E1-067-05 | AC5, BR5 | System | Ledger insert forced to fail; outbox retry limit 3 |
| TC-E1-067-06 | AC6, BR4 | System | CaseCreated then CaseAllocated in the outbox |
| TC-E1-067-07 | AC7, BR3 | System | One event on two consumer threads |
| TC-E1-067-08 | AC8 | System | DocumentStored for an unknown case ID |
| TC-E1-067-09 | Access | Access | SY-AGENT calls append(); refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the event map and the retry limit are configuration.
- No personal data in logs, tests or prompts: entries from events carry codes and references only (events rule "Payload"); test events are synthetic.
- No read of another module's tables: everything the entry needs comes from the event; no query on assignment, document or decision_log_entry.
- The listener never acknowledges an event it has not written or moved to the exception queue.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-36 | TC-E1-067-01, TC-E1-067-04, TC-E1-067-05, TC-E1-067-06, TC-E1-067-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-067-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-04 | All recovery processes | R-UNI-40 | TC-E1-067-03, TC-E1-067-07 |

## 19. Out of scope

- The ledger store and writer (RWB-E1-066) and the read interface (RWB-E1-068).
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).
