# RWB-ITG-E1067-ITG Every Workbench action into the interaction ledger — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1067-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-067 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1067-APP, RWB-P3-E1067-APP, RWB-P5-E1067-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-ILG-005, REQ-ILG-002, REQ-ILG-007) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-067 for RWB-ITG-W1. The one in-process outbox and one listener for six `EV-nn` events become the per-service topics `rwb.case.events.v1` (P3 rwb-case: CaseCreated, CaseAllocated, CaseTransferred, TimerBreached), `rwb.document.events.v1` (P5 rwb-document: DocumentStored) and the shared `rwb.decision-record.v1` (DecisionRecorded), all in the CloudEvents 1.0 envelope (DP-09); the ledger stays with P1 rwb-source-data under DP-18, which runs one consumer group, rejects a repeat in `rwb_source_data.processed_event` and appends to `rwb_source_data.interaction`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the path from a real Workbench action to its entry in the interaction ledger proved end to end on the real wave 1 services and the three real topics — the six actions of the legacy story producing exactly one entry each on the topic of the service that owns them, a repeat of any event writing no second entry and adding exactly one hit, the entries of one case reading in occurred-time order with a `case_seq` that is gap-free from 1 to n even when the three topics deliver out of order, and a poison event dead-lettered with its retry count and incident `LEDGER_WRITE_FAILED` while the entries already written stay intact**, so that **the case history a case owner reads is complete, ordered and duplicate-free across three topic streams, and not only on the one outbox and one listener of the monolith**.

### 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. If these actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them. Each action already publishes an application event in the same transaction as the change, and a listener turns each event into one entry with its source and actor; events are delivered at least once, so a repeat is rejected by its idempotency key and counted (R-UNI-40). The story serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007, and its measure is unchanged from RWB-E1-067: every Workbench action on a case is in the ledger when it is taken.

In the monolith one in-process outbox and one listener carried all six events, so one order and one duplicate rule held for the whole set. In the 19-service target the same six events arrive from three producers on three topics in the CloudEvents 1.0 envelope (DP-09): `rwb.case.events.v1` carries CaseCreated, CaseAllocated, CaseTransferred and TimerBreached from P3 rwb-case; `rwb.document.events.v1` carries DocumentStored from P5 rwb-document; and the shared `rwb.decision-record.v1` carries DecisionRecorded, whose type and topic P7 rwb-decision owns (DP-03). The ledger does not move: DP-18 and the Ownership Map default ruling keep it with P1 rwb-source-data, which owns `interaction` and its writer in schema `rwb_source_data`, runs one consumer group, rejects a repeat in `processed_event` in the same transaction as the append, and migrates the schema on its own Flyway sequence (DP-01, DP-15). No behaviour is added: what changes is that the six events now travel on three independent streams, and the ledger is written by the service that owns it rather than by the module that changed.

That change is exactly what no single service story can prove. A producer that commits a change without its outbox row, an event that lands on the wrong topic, a second entry after a redelivery on another topic, entries out of occurred-time order because two streams interleaved differently, and a message of a newer schema version that is written instead of dead-lettered are all failures that appear only when the three real producers, the three real topics and the real consumer run together. Reference data comes through the rwb-case contract (DP-07), every call is one hop with a 2 s budget (DP-11), the entries reach the case record through the gateway-bff route (DP-19), and the local decision record of the deciding service is what feeds the central ledger (DP-03), so the suite can assert the ledger without any service reading another service's table (DP-01). This story builds and runs that harness; it publishes no operation of its own and owns no schema.

The measure is the legacy one: reads of the case history complete, with a hit count on every repeat and no lost entry, at the retry limit of 3 and the retry cadence of 1 min, 10 min and 1 h before the dead-letter topic (NFR-026). Where the sources do not state the event-to-ledger map after the split into per-service topics, the cross-topic ordering rule, the field that carries the duplicate key across three topics, the registration of rwb-source-data as a consumer of the case and document topics, or the incident raised for a dead-lettered ledger event, the suite reads the value as configuration and the open point is recorded as Not specified in the source documents (GAP-0376; ASM-0540).

### 3. Preconditions

- RWB-P1-E1067-APP is done: one consumer group on the three topics, the inbox dedupe in `rwb_source_data.processed_event`, the append to `rwb_source_data.interaction` with its `case_seq`, the read operation of section 12.2 and the dead-letter handling of each topic are in SIT.
- RWB-P3-E1067-APP is done: CaseCreated, CaseAllocated, CaseTransferred and TimerBreached are published from rwb-case's own outbox to `rwb.case.events.v1` in the same transaction as the change.
- RWB-P5-E1067-APP is done: DocumentStored is published from rwb-document's own outbox to `rwb.document.events.v1`.
- The shared topic `rwb.decision-record.v1` carries DecisionRecorded from the service that takes the decision — in these fixtures P3 rwb-case, through its local decision record and its outbox; the event type and the topic are owned by P7 rwb-decision, whose contract story carries the build (DP-03), so this story takes no P7 dependency.
- The three topics exist with 12 partitions, replication factor 3 and 7-day retention, key caseId, with their retry topics at 1 min, 10 min and 1 h and their `.dlt` topics (Arch v5 slides 11 and 22); the topic and event names come from the naming library (DP-14).
- Schema `rwb_source_data` holds `interaction` with its unique `idempotency_key`, `processed_event` and the outbox and inbox library objects, created by the P1 Flyway sequence (DP-15); the serving identity holds INSERT and SELECT and no UPDATE or DELETE grant on `interaction`.
- The gateway-bff composite route for SCR-03 Case record is deployed in SIT (DP-19, RWB-PLT-N001-CON), so the entries of a case are read the way the case owner reads them.
- The synthetic fixtures of the legacy story are loaded: case "RW-2026-000301" with no ledger entries, queue "MTG-BKK-CO", user "u-teammgr-03", document "DOC-SYN-3011", timer "SLA-ASSIGNED", decision log entry "DLE-SYN-3012" and the idempotency key "EV-02-RW-2026-000301-20261201".
- The harness RWB-ITG-W1J01-ITG is available with its SIT endpoints, its topic probes and its report writer.
- The event-to-ledger map after the split into per-service topics, the cross-topic ordering rule and the field that carries the duplicate key across the three topics are Not specified in the source documents (GAP-0376; ASM-0540); the suite reads them as configuration and invents none of them.
- No production data is used and no production connection is opened. The environment is SIT or DEV, and the suite refuses any other.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1 (Template and Rules §R5.7). The harness is written on Day 1 and run when the three services are in SIT; a fake is never used in their place.

### 4. Flow

1. QA integration engineer: seeds the synthetic fixtures of the harness RWB-ITG-W1J01-ITG — case "RW-2026-000301" with no ledger entries and the six legacy values of the actions; no production data is used.
2. SuiteRunner: reads the run configuration — the three topics with their retry and `.dlt` topics, the consumer group of rwb-source-data, the event map, the retry limit 3, the case and its identifiers, and the owner of the dead-letter items — and runs the preflight: the topics and their retry and `.dlt` topics exist, the ledger listener runs in one consumer group, the P3 and P5 producers and the decision-record relay answer, and `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` answers for the case. A missing topic, listener, producer or read stops the run before any test.
3. ActionDriver: drives the six real actions of the legacy story through the owners' own write paths on case "RW-2026-000301" — creation at 2026-12-01T06:10+07:00 by SY-CASEWF, allocation to "MTG-BKK-CO" at 06:40 by SY-RULES, transfer by "u-teammgr-03" at 2026-12-03T14:05+07:00, document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR, timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00 and decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00. The harness calls no service's tables and writes none of them.
4. Producer: commits the change and its outbox row in one transaction in its own schema; the relay publishes one CloudEvents 1.0 event in binary mode on the producer's topic, key caseId, carrying IDs and references only (DP-09).
5. rwb-source-data, one consumer group on the three topics: records the CloudEvents id in `processed_event` in the same transaction as the append to `interaction`, sets the event code from the event map, takes the next `case_seq` of the case, and sets source system WORKBENCH, the source reference `<owning service>, <event ID> <event name>` and the actor from the event header.
6. rwb-source-data: on a key it has already seen, writes no entry and adds one hit on `processed_event` (R-UNI-40).
7. LedgerProbe: reads the entries through the operation of section 12.2 and asserts six entries, the six event codes, the source reference of each owning service, the actor, the occurred time and `case_seq` 1 to 6 in occurred-time order.
8. OrderDriver: replays the same six events on their three topics in an order that differs from the occurred times and re-reads the ledger; the entries still read in occurred-time order with a gap-free `case_seq`, and an inversion the ledger cannot resolve is named in the report and fails the run.
9. DuplicateDriver: redelivers one event on each of the three topics with the same CloudEvents id and the same event idempotency key, and confirms one hit for each key and no second entry.
10. PoisonPublisher: publishes one event of an unsupported schema version on each of the three topics — CaseTransferred at schema version 3 on `rwb.case.events.v1`, DocumentStored at schema version 3 on `rwb.document.events.v1` and DecisionRecorded at schema version 3 on `rwb.decision-record.v1` — lets the four deliveries of the retry cadence run out, and confirms the dead-letter item, the incident and the entries already written.
11. ReportWriter: writes the evidence report with one row per test case, removes the synthetic fixtures, restores the fixture state and asserts that the run opened no production connection.
12. The run reads the event map, the ordering rule and the duplicate key from configuration; those three values are Not specified in the source documents (GAP-0376; ASM-0540) and the harness invents none of them.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same CloudEvents id and idempotency key | One entry; the repeat is counted on `processed_event` | None | AC3, AC7 |
| X2 | An event with a schema version that is neither current nor previous | Not written; it goes to the `.dlt` topic of its own topic with owner RW-PLATADM and an incident is raised | MSG-P1-022 (incident detail) | AC9 |
| X3 | The ledger append fails | Tried 4 times in all through the retry topics at 1 min, 10 min and 1 h, then the `.dlt` topic with owner RW-PLATADM and incident "LEDGER_WRITE_FAILED"; the event is not discarded | MSG-P1-022 (incident detail) | AC5, AC9 |
| X4 | Events of one case arrive on the three topics in an order other than their occurred times | Entries read in occurred-time order with a gap-free `case_seq`; an inversion the ledger cannot resolve is named in the run report and fails the run | None | AC8 |
| X5 | The same event reaches two consumer threads at once | One entry; one hit counted | None | AC7 |
| X6 | A topic name, the consumer group or the fixture set does not match what the harness expects | The suite fails as a harness fault and names the element; no service defect is raised | None | AC6 |
| X7 | A consumed call exceeds the 2 s budget or answers a server error | The call is retried once under the suite policy and the report records it; no assertion is made on data that was not read | None | AC6, AC8 |

X1 to X5 are the exception paths of RWB-E1-067 read on the three topics, with the legacy exception queue replaced by the `.dlt` topic of the owning topic (DP-09), and the legacy schema-version path now asserted as the poison case of AC9. X6 and X7 are the suite's own failure modes, so that a fixture fault is reported as a harness fault and a timeout never becomes a pass.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a test project of its own next to harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the three published topics, not their source code, and owns no schema, no table and no field |
| Negotiable | The wait windows, the probe settings, the fixture reset and the report layout are configuration; the six event codes, the six event IDs, the retry limit and the case values are fixed by the legacy story |
| Valuable | Proves across three topics what no single service story can prove: six actions, six entries naming their owners, one hit per redelivery, an occurred-time order with a gap-free sequence and a poison event that never reaches the ledger |
| Estimable | One suite module, four test classes, four fixtures, one order replay and one report |
| Small | Fits one sprint with the report; no service code and no schema change |
| Testable | Every criterion is asserted on an observable: an entry read through the owner's contract, an event on a topic, a dead-letter item, an incident, or a count |

### 7. Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger, proved across the three wave 1 topics

  Background:
    Given the environment is SIT with synthetic data and the harness RWB-ITG-W1J01-ITG is available
    Given rwb-source-data, rwb-case, rwb-document and rwb-decision are deployed with their published contracts behind gateway-bff
    Given rwb.case.events.v1, rwb.document.events.v1 and rwb.decision-record.v1 exist with their retry and .dlt topics
    Given the ledger listener of rwb-source-data runs in one consumer group
    Given case "RW-2026-000301" exists with no ledger entries

  Scenario: AC1 Workbench events are captured (legacy RWB-E1-067 AC1)
    Given the case is created at 2026-12-01T06:10+07:00 by SY-CASEWF
    Given allocated to queue "MTG-BKK-CO" at 06:40 by SY-RULES
    Given transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00
    Given has document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR
    Given has timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00
    Given has decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00
    When each action completes
    Then the ledger holds 6 entries for the case with events CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN
    Then each entry carries the case identifier, the event, the timestamp and the actor

  Scenario: AC3 Nothing is written twice (legacy RWB-E1-067 AC3)
    Given CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201" was written to the ledger
    When the same event arrives again with the same key
    Then one CASE_ALLOCATED entry exists
    Then the hit count for key "EV-02-RW-2026-000301-20261201" is 1

  Scenario: AC5 The ledger write fails for an event (legacy RWB-E1-067 AC5)
    Given every ledger insert fails
    When DocumentStored for case "RW-2026-000301" is delivered
    Then the delivery is tried 4 times in all
    Then the event is in the exception queue with owner RW-PLATADM
    Then the system raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301"

  Scenario: AC6 Each of the six events arrives on its own owner's topic and makes exactly one entry naming that owner (new, D-RCV-60)
    Given case "RW-2026-000301" has no ledger entries
    When the case is created at 2026-12-01T06:10+07:00, allocated to queue "MTG-BKK-CO" at 06:40, transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00, given document "DOC-SYN-3011" at 2026-12-04T09:30+07:00, given timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00 and given decision log entry "DLE-SYN-3012" at 2026-12-05T11:20+07:00 through the owners' own write paths
    Then rwb.case.events.v1 carries rwb.case.CaseCreated.v1, rwb.case.CaseAllocated.v1, rwb.case.CaseTransferred.v1 and rwb.case.TimerBreached.v1 for the case
    Then rwb.document.events.v1 carries rwb.document.DocumentStored.v1 for the case
    Then rwb.decision-record.v1 carries rwb.decision.DecisionRecorded.v1 for the case
    Then each event is a CloudEvents 1.0 event in binary mode with key "RW-2026-000301"
    When GET /api/recovery/source-data/v1/cases/{caseId}/interactions is read for the case
    Then it returns exactly 6 entries with the event codes CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN
    Then each entry carries source system "WORKBENCH" and a source reference that names its own owning service and its event: "P3 rwb-case, EV-01 CaseCreated", "P3 rwb-case, EV-02 CaseAllocated", "P3 rwb-case, EV-04 CaseTransferred", "P3 rwb-case, EV-19 TimerBreached", "P5 rwb-document, EV-16 DocumentStored" and "P3 rwb-case, EV-08 DecisionRecorded", whose type and topic P7 rwb-decision owns
    Then no entry was written from a fourth topic and no service read another service's table

  Scenario: AC7 A redelivery on any of the three topics adds one hit and no entry (new, D-RCV-60)
    Given the ledger holds the 6 entries of case "RW-2026-000301"
    When the CaseAllocated event with idempotency key "EV-02-RW-2026-000301-20261201" is redelivered on rwb.case.events.v1
    And the DocumentStored event of "DOC-SYN-3011" is redelivered on rwb.document.events.v1
    And the DecisionRecorded event of "DLE-SYN-3012" is redelivered on rwb.decision-record.v1
    Then the ledger still holds 6 entries for the case
    Then the hit count for key "EV-02-RW-2026-000301-20261201" is 1
    Then each redelivery adds exactly one hit on rwb_source_data.processed_event for its own CloudEvents id
    Then no case_seq is reused and no entry is updated or removed

  Scenario: AC8 Entries read in occurred-time order with a gap-free sequence across three topics (new, D-RCV-60)
    Given the 6 events of case "RW-2026-000301" carry their occurred times from 2026-12-01T06:10+07:00 to 2026-12-05T11:20+07:00
    When rwb.case.events.v1, rwb.document.events.v1 and rwb.decision-record.v1 deliver them out of order, so the DocumentStored event arrives before CaseCreated
    Then GET /api/recovery/source-data/v1/cases/{caseId}/interactions returns the 6 entries in occurred-time order from the earliest to the latest
    Then case_seq reads 1, 2, 3, 4, 5, 6 with no gap and no repeat
    Then each entry keeps the event code its own event carries
    Then the run report names every inversion it had to resolve
    Then an inversion the ledger cannot resolve is named in the report and fails the run

  Scenario: AC9 A poison event goes to its owner's .dlt with the retry count and raises LEDGER_WRITE_FAILED (new, D-RCV-60)
    Given CaseTransferred is at schema version 2 and the ledger holds the entries already written for case "RW-2026-000301"
    When a CaseTransferred event with schema version 3 is published on rwb.case.events.v1 for case "RW-2026-000301"
    Then the delivery is tried 4 times in all through the retry topics at 1 min, 10 min and 1 h
    Then the system writes no entry for it and the entries already written stay unchanged
    Then the event is on rwb.case.events.v1.dlt with owner RW-PLATADM and reason "schema version 3 not accepted"
    Then the system raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301" and MSG-P1-022 carries the detail
    Then a replay of the .dlt topic after the contract version is registered adds its entry and leaves the earlier entries intact
```

AC1, AC3 and AC5 are the legacy proof of RWB-E1-067 and are carried unchanged, including the words "exception queue"; in the target that queue is the `.dlt` topic of the owning topic (DP-09), the retry limit of 3 gives the four delivery attempts of AC5, and AC9 proves the same retry count on the dead-letter path with incident `LEDGER_WRITE_FAILED`. No scenario uses a contract mock: every step runs against the real services, the real topics and the real relay. AC6 to AC9 use only the synthetic values already present in the legacy story. The legacy AC2, AC4, AC6, AC7 and AC8 belong to RWB-P1-E1067-APP, not to this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen | REQ-ILG-005; EV-01, EV-02, EV-04, EV-19, EV-16, EV-08 (events.txt) |
| BR2 | Every entry names the system or person that produced it | REQ-ILG-002 |
| BR3 | The same event with the same key produces one entry, and the repeat is counted | R-UNI-40; REQ-ILG-007 |
| BR4 | Events are keyed caseId, so one topic keeps the order of one case; across the three topics the ledger orders the entries by the event's occurred time and assigns `case_seq` with no gap | Arch v5 slide 11 (key caseId, order per case); DP-09; ASM-0540 |
| BR5 | A consumer failure is retried through the retry topics at 1 min, 10 min and 1 h, then goes to the `.dlt` topic of the owning topic with owner RW-PLATADM and an incident | Events rule "Failure" (events.txt); R-UNI-36; Arch v5 slides 11 and 22 |
| BR6 | A consumer accepts the current and the previous schema version; any other version is not written and goes to the `.dlt` topic | Events rule "Versioning" (events.txt); Arch v5 slide 11 |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt); Arch v5 slides 42 and 43 |
| BR8 | One consumer group reads the three topics, and the dedupe in `processed_event` commits in the same transaction as the append to `interaction` | DP-09; Arch v5 slide 11 (inbox in each consumer) |
| BR9 | The ledger is owned by P1 rwb-source-data in `rwb_source_data`; no other service reads its tables and the suite owns no schema | DP-01; DP-18; DP-15 |
| BR10 | Every cross-service read is one hop on the owner's contract with a 2 s budget | DP-11; ADR-020 |
| BR11 | Each producer publishes its own event type on its own topic in the CloudEvents 1.0 envelope, key caseId, with IDs and references only; the ledger listener of rwb-source-data is an additional consumer group on the case, document and decision-record topics | DP-09; DP-03; Arch v5 slides 11, 42 and 43; ASM-0541 |
| BR12 | A dead-lettered ledger event raises `LEDGER_WRITE_FAILED` for its case and is replayed only after the contract version is registered | RWB-E1-067 BR5; ASM-0542 |

### 9. State transitions

None for a case status. This story changes no case status of its own; it drives the owners' write paths and observes the ledger, the inbox and the delivery states.

| Object | State | Meaning |
|---|---|---|
| `interaction` entry | Appended once | Written in the transaction that records the inbox row; never updated and never deleted |
| `processed_event` row | Deduplicated | One row per CloudEvents id and consumer group; `hit_count` rises by one on each redelivery and `last_hit_at` moves |
| Inbox delivery | Received, retried or dead-lettered | Received on the owner's topic, moved to a retry topic at 1 min, 10 min or 1 h, or dead-lettered on the `.dlt` topic of that topic |
| Poison message | Dead-lettered | Not written; on the `.dlt` topic with owner RW-PLATADM; replayed only after its contract version is registered |
| Harness run | Not started, running, passed or failed | A failing step stops the run and the report names the criterion, the topic and the evidence |

The suite reads these states through the owners' contracts and the topics; it changes none of them directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| P1 rwb-source-data owner (RWB-P1-E1067-APP) | Owns the listener, the inbox dedupe, the append, the `case_seq`, the read operation and the dead-letter handling |
| P3 rwb-case owner (RWB-P3-E1067-APP) | Owns the producer of CaseCreated, CaseAllocated, CaseTransferred and TimerBreached |
| P5 rwb-document owner (RWB-P5-E1067-APP) | Owns the producer of DocumentStored |
| P7 rwb-decision owner | Owns the event type and the topic `rwb.decision-record.v1`; takes no build dependency from this story |
| SY-CASEWF, SY-RULES and SY-OCR | Appear as actors on entries; do not call the ledger writer |
| RW-CASEOWN Case owner | Reads the entries of a case through the read operation on SCR-03 Case record |
| RW-PLATADM Platform administrator | Owns the dead-letter items and the incident; replays a dead-letter topic after a contract version is registered |
| No role | May update or delete an entry |

No approval level from the delegation of authority applies: the story takes no business decision.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-020 | `interaction` (schema `rwb_source_data`) | all fields | Write, by P1 rwb-source-data; read through the P1 contract |
| DF-INT-014 | `interaction` | event_code | Write; read for the six event codes |
| DF-INT-015 | `interaction` | actor_type | Write, read |
| DF-INT-016 | `interaction` | actor_ref | Write, read |
| DF-INT-017 | `interaction` | source_ref | Write, read (the owning service and the event) |
| DF-INT-018 | `interaction` | idempotency_key | Write; unique; the duplicate rule |
| DF-INT-019 | `interaction` | case_seq | Write, read (1 to 6 with no gap) |
| DF-INT-020 | `interaction` | decision_log_id | Write for the decision entry |
| DF-OPS-178 to DF-OPS-183 | `processed_event` (schema `rwb_source_data`) | all fields | Write, by P1 rwb-source-data; the hit count is read for the run by the P1 owner |

The four record IDs the entries carry — `recovery_case.id` (DF-CAS-001), `assignment.id` (DF-WRK-009), `document.id` (DF-DOC-001) and `decision_log_entry.id` (DF-DEC-001) — are read from the event payload and never queried, so no service's table is read by the suite (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-067. The hit count of DF-OPS-178 to DF-OPS-183 is not a REST response: it is read in SIT by the rwb-source-data owner from `processed_event` and attached to the run evidence, because the harness owns no schema and no table. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Confirms the entries of one case: the six event codes, the source reference, the actor, the occurred time and `case_seq`; the assertion surface of AC1, AC6, AC7 and AC8 |

The call is one hop to the owning service on its own base with the 2 s client budget (DP-11, DP-13); the harness calls no service through another service. The hit count of a repeated key is not carried by the read response: the P1 owner reads `processed_event` for the run and signs the evidence line (section 11). The browser reaches the same entries through the gateway-bff route for SCR-03 (DP-19); the suite calls the owner's base directly and adds no hop.

#### 12.3 Events published

None. The suite publishes no event. The test fixture publishes synthetic events only as the owning services would — through each producer's own outbox test fixture — and the suite itself puts nothing on a topic.

#### 12.4 Events consumed

| Event | Topic | Producer | CloudEvents type | Dedupe and retry |
|---|---|---|---|---|
| CaseCreated (EV-01) | `rwb.case.events.v1` | P3 rwb-case | `rwb.case.CaseCreated.v1` | Key caseId; inbox dedupe on the CloudEvents id in `processed_event` of rwb-source-data; retry 1 min, 10 min, 1 h, then `rwb.case.events.v1.dlt` |
| CaseAllocated (EV-02) | `rwb.case.events.v1` | P3 rwb-case | `rwb.case.CaseAllocated.v1` | Key caseId; the same dedupe and retry; then `rwb.case.events.v1.dlt` |
| CaseTransferred (EV-04) | `rwb.case.events.v1` | P3 rwb-case | `rwb.case.CaseTransferred.v1` | Key caseId; the same dedupe and retry; then `rwb.case.events.v1.dlt` |
| TimerBreached (EV-19) | `rwb.case.events.v1` | P3 rwb-case | `rwb.case.TimerBreached.v1` | Key caseId; the same dedupe and retry; then `rwb.case.events.v1.dlt` |
| DocumentStored (EV-16) | `rwb.document.events.v1` | P5 rwb-document | `rwb.document.DocumentStored.v1` | Key caseId; the same dedupe and retry; then `rwb.document.events.v1.dlt` |
| DecisionRecorded (EV-08) | `rwb.decision-record.v1` | the service that takes the decision (in these fixtures P3 rwb-case, through its local decision record); type and topic owned by P7 rwb-decision | `rwb.decision.DecisionRecorded.v1` | Key caseId; the same dedupe and retry; then `rwb.decision-record.v1.dlt` |

All six are consumed in the CloudEvents 1.0 envelope in binary mode by one consumer group of rwb-source-data across the three topics, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic of each topic with owner RW-PLATADM (ADR-015; Arch v5 slides 11, 22 and 42). Arch v5 slide 42 lists the catalogue consumers of the case and document topics and does not name rwb-source-data among them, so the ledger consumer is read as an additional consumer group on those two topics and on `rwb.decision-record.v1`, with no change to the catalogue's existing consumers (ASM-0541).

The event-to-ledger map after the split into per-service topics, the cross-topic ordering rule and the field that carries the duplicate key across the three topics are Not specified in the source documents (GAP-0376; ASM-0540). Under that assumption the run reads the three as configuration without inventing them: the map keeps the legacy pairs EV-01 CASE_CREATED, EV-02 CASE_ALLOCATED, EV-04 CASE_TRANSFERRED, EV-19 CASE_ESCALATED, EV-16 DOCUMENT_ATTACHED and EV-08 DECISION_TAKEN; the order across topics is the event's occurred time, with `case_seq` assigned in that order; and the duplicate key is the CloudEvents id with the event's idempotency key as the unique key of `interaction`.

#### 12.5 Workflows and activities

None. No workflow and no activity is registered, started or awaited by this story; the listener, the relay and the producers run as the services' own consumers and relays, outside Temporal.

#### 12.6 Schedules

None. No Temporal Schedule takes part; the outbox relay runs every minute in each producer as part of that service's own release (Arch v5 slide 44) and is not a Schedule of this story.

#### 12.7 Tables owned

None. The harness owns no table and reads no service's schema (DP-01). The tables it exercises — `interaction` and `processed_event` — belong to P1 rwb-source-data in schema `rwb_source_data` and are listed in section 11 with their owner.

#### 12.8 Contract fakes

None. No service contract is faked at this level: the real services, the real topics and the real relay replace the fakes of the app stories. The synthetic events are produced through each owner's outbox test fixture, in the producer's own transaction in its own schema, and consumed from the real topic by the real listener of rwb-source-data. A fake endpoint, a stub base or a mocked consumer fails the topology check before any test runs.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 1 |
| Kafka | 0 | 6 event types on 3 topics |
| Temporal | 0 | 0 |
| File | 0 | 0 |

The six consumed event types are `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.TimerBreached.v1`, `rwb.document.DocumentStored.v1` and `rwb.decision.DecisionRecorded.v1`, key caseId. No file, workflow or Schedule is in this story.

### 13. Solution plan

**Package and deliverables.** One suite module `integration/recovery/wave1/interaction-ledger` in the ACE repository, package `<ACE base package>.recovery.itg.wave1.ledger`, next to harness RWB-ITG-W1J01-ITG and not part of a deployed service.

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Runner | Preflight, run order, report, exit code; refuses an environment that is not SIT or DEV |
| Wave1Topology fixture | Configuration | Names the real SIT endpoints, the consumer group and the three topics with their retry and `.dlt` topics; fails the run when a fake endpoint is configured |
| ActionDriver | Test service | Drives the six real actions of case "RW-2026-000301" through the owners' own write paths |
| TopicProbe | Test service | Consumes the three topics and their retry and `.dlt` topics and asserts the count, the CloudEvents type, the key and the absence of personal data |
| LedgerProbe | Test service | Reads the interaction operation and asserts the six entries, the codes, the source reference, the actor and `case_seq` 1 to 6 in occurred-time order |
| DuplicateDriver | Test service | Redelivers one event on each topic with the same CloudEvents id and idempotency key and collects the hit evidence |
| OrderDriver | Test service | Replays the six events out of occurred-time order and re-reads the ledger |
| PoisonPublisher | Test service | Publishes one event of an unsupported schema version on each topic and watches the retry count, the dead-letter item and the incident |
| ReportWriter | Service | One row per test case with the evidence and the elapsed times |

**Database.** None of its own. The harness writes no table and no schema: every action goes through the owner's own write path and every assertion is a contract response or a topic observation (DP-01, DP-18).

**Configuration and reference data.**

- The three topics with their retry and `.dlt` topics, the consumer group, the read base and the wait windows, all as configuration.
- The event map EV-01 CASE_CREATED, EV-02 CASE_ALLOCATED, EV-04 CASE_TRANSFERRED, EV-19 CASE_ESCALATED, EV-16 DOCUMENT_ATTACHED and EV-08 DECISION_TAKEN, read from configuration and never written in code (legacy `rwb.dataengine.ledger.event-map`).
- The source-reference format `<owning service>, <event ID> <event name>`, which is the legacy format with the module replaced by the owning service.
- The retry limit 3 with the retry topics at 1 min, 10 min and 1 h (NFR-026; DL11).
- The synthetic case "RW-2026-000301" with "u-teammgr-03", "MTG-BKK-CO", "DOC-SYN-3011", "SLA-ASSIGNED", "DLE-SYN-3012" and "EV-02-RW-2026-000301-20261201".
- The dead-letter owner RW-PLATADM, who owns the dead-letter item of any of the three topics, and the incident `LEDGER_WRITE_FAILED`.
- The 2 s client budget and the agreed precision of the occurred-time comparison.

**Pattern application** (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story, not of this suite: the eight patterns sit on RWB-P1-E1067-APP, RWB-P3-E1067-APP and RWB-P5-E1067-APP and on the platform contract stories. This story's H, C and X lists are empty and its I list is exactly RWB-P1-E1067-APP, RWB-P3-E1067-APP and RWB-P5-E1067-APP; an ITG story builds against published contracts and blocks no build of its own (Template and Rules §R5.4 and §R5.7).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Six-action fixture | Case "RW-2026-000301" with no ledger entries; the six legacy values and their occurred times | AC1, AC6, TC-E1-067-01-ITG, TC-ITG-E1067-01 |
| Redelivery fixture | One event per topic republished with the same CloudEvents id and the same idempotency key | AC3, AC7, TC-E1-067-03-ITG, TC-ITG-E1067-02 |
| Out-of-order fixture | The same six events with the same occurred times, published so DocumentStored arrives before CaseCreated | AC8, TC-ITG-E1067-03 |
| Poison fixture | CaseTransferred at schema version 3, DocumentStored at schema version 3 and DecisionRecorded at schema version 3 | AC9, TC-ITG-E1067-04 |
| Failure fixture | Every insert failing for the DocumentStored delivery, with the retry limit 3 | AC5, TC-E1-067-05-ITG |

Every fixture value is the legacy value carried unchanged; no new business value is invented.

**Build steps.**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT topics and the rwb-source-data base.
2. Add the topology preflight: the three topics with their retry and `.dlt` topics, one consumer group, the three producers and the read operation.
3. Implement AC1 and AC6: the six actions through the owners' write paths, the six events on their own topics and the six entries with their source references.
4. Implement AC3, AC7 and AC8: the redelivery on each topic, the hit count, the out-of-order replay and the gap-free `case_seq`.
5. Implement AC5 and AC9: the failing insert with the four deliveries, the poison message with its retry count, the `.dlt` item, incident `LEDGER_WRITE_FAILED` and the replay after the version is registered.
6. Write the evidence report, reset the fixtures and run the suite in SIT against the wave 1 release candidate.

**Done when.** The seven test cases of section 16 pass in SIT against the published wave 1 contracts of the P3 and P5 producers and the P1 ledger, the six real actions produce exactly six entries each naming its own owning service, a redelivery on any of the three topics adds one hit and no entry, the entries of one case read in occurred-time order with `case_seq` 1 to 6, a poison event reaches `rwb.case.events.v1.dlt` with owner RW-PLATADM and incident `LEDGER_WRITE_FAILED` while the earlier entries stay intact, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | Ledger write failed, carried on the incident and on the dead-letter item | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without Case record C calls the ledger writer or reads the entries | You cannot {action} here. Your role does not include it. |

The two texts are copied unchanged from RWB-E1-067; this story adds no message text and no message ID. The refusal of MSG-P4-002 belongs to the writer's identity check of RWB-P1-E1067-APP and is carried here as the message the case record shows. A dead-letter item is platform text with its own fields — the topic, the partition, the offset, the CloudEvents id and the reason — and carries no message ID; the incident raised with it carries `LEDGER_WRITE_FAILED` and MSG-P1-022 for the case (ASM-0542). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built or tested by this story. The platform administrator sees a dead-letter item on SCR-09 Exception queue (Epic 1, state List), and the case owner reads the entries on SCR-03 Case record (Read only) through the gateway-bff composite route on the rwb-source-data base, one hop with a 2 s timeout (DP-19). The suite reads the same entries through the owner's contract; both screens are referenced and neither is changed here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01-ITG | AC1, BR1 | Integration | Six synthetic events for case RW-2026-000301 on the three real topics; no numeric business values added |
| TC-E1-067-03-ITG | AC3, BR3 | Integration | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201; one hit |
| TC-E1-067-05-ITG | AC5, BR5 | Integration | Ledger insert forced to fail for DocumentStored; retry limit 3; four deliveries; owner RW-PLATADM; incident LEDGER_WRITE_FAILED |
| TC-ITG-E1067-01 | AC6, BR1, BR11 | Integration | Six real actions on the three topics for case RW-2026-000301; each entry names its owning service and event |
| TC-ITG-E1067-02 | AC7, BR3, BR8 | Integration | One redelivery on each of the three topics with the same CloudEvents id and idempotency key |
| TC-ITG-E1067-03 | AC8, BR4 | Integration | The six events delivered out of occurred-time order across the three topics; gap-free case_seq 1 to 6 |
| TC-ITG-E1067-04 | AC9, BR5, BR6, BR12 | NFR | CaseTransferred at schema version 3; the four deliveries; the .dlt item; incident LEDGER_WRITE_FAILED; the earlier entries unchanged |

The three legacy criteria this story owns carry their legacy test case ID with the suffix `-ITG`; the four new criteria carry `TC-ITG-E1067-01` to `-04`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID. The legacy test cases of AC2, AC4, AC6, AC7 and AC8 stay with RWB-P1-E1067-APP.

### 17. Guardrails

- No business value in code: the event map, the retry limit, the topics, the consumer group and the synthetic case are configuration; the six event codes and the six event IDs are the legacy ones.
- No personal data in events, fixtures, logs or the report: the entries carry codes, IDs and references only (events rule "Payload"; Arch v5 slides 42 and 43), and the report holds counts, ids and timings.
- No cross-service table read and no schema of its own: every action goes through the owner's write path and every assertion is a contract response or a topic observation (DP-01, DP-18); the only read of `processed_event` is made by its owner and attached to the evidence.
- One hop and a 2 s timeout on every call (ADR-020, DP-11), and a timeout is never retried into a pass.
- One event type per producer topic and one consumer group for the ledger (BR8, BR11); a service that publishes another service's event, or a second consumer group, fails the run.
- The ledger entry is never updated and never deleted; the harness asserts the refusal instead of relying on the review.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG and reset after a run, with no production access of any kind; the suite refuses an environment that is not SIT or DEV.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | The three topics and the six event types of 12.4; `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`; the event map of section 13 | TC-E1-067-01-ITG, TC-E1-067-05-ITG, TC-ITG-E1067-01, TC-ITG-E1067-04 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The `interaction` field set DF-INT-001 to DF-INT-020, the source reference and the read response of 12.2 | TC-E1-067-01-ITG, TC-ITG-E1067-01 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | `processed_event`, the CloudEvents id and `interaction.idempotency_key` | TC-E1-067-03-ITG, TC-ITG-E1067-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three topics, the six CloudEvents types, the retry and `.dlt` topics | TC-ITG-E1067-01, TC-ITG-E1067-04 |
| DP-01 / DP-18 | Owner's schema, never another service's tables; the ledger is P1's | One writer for `rwb_source_data`; the suite asserts through the owner's contract | All |
| ASM-0540 | The map, the ordering rule and the duplicate key are configuration after the split | The event map, the occurred-time order and the idempotency key of 12.4 | TC-ITG-E1067-01, TC-ITG-E1067-02, TC-ITG-E1067-03 |
| ASM-0541 | The ledger listener is an additional consumer group on the case and document topics | One consumer group of rwb-source-data across the three topics | TC-ITG-E1067-01 |
| ASM-0542 | A dead-lettered ledger event raises LEDGER_WRITE_FAILED | The `.dlt` item of AC9 and the incident line of section 14 | TC-ITG-E1067-04 |

The legacy AC1 to AC8 at component level belong to RWB-P1-E1067-APP, RWB-P3-E1067-APP and RWB-P5-E1067-APP, not to this story; this list carries only the three criteria the story owns and the four it adds.

### 19. Out of scope

- The listener, the inbox dedupe, the append, the `case_seq`, the read operation and the dead-letter handling of the ledger (RWB-P1-E1067-APP), with its CON, DB and OPS stories.
- The producers of `rwb.case.events.v1` and `rwb.document.events.v1` (RWB-P3-E1067-APP, RWB-P5-E1067-APP) and the event type and topic contract of `rwb.decision-record.v1` with the local decision record that publishes DecisionRecorded (DP-03, RWB-PLT-E1027-CON).
- The ledger store and writer of RWB-E1-066 and the read interface of RWB-E1-068, which are taken over by the P1 stories of those legacy keys.
- The legacy AC2, AC4, AC6, AC7 and AC8 at component level, which RWB-P1-E1067-APP owns.
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).
- Retention periods, the retention run, and the daily seal of the central decision ledger to immutable storage.
- The build of the harness RWB-ITG-W1J01-ITG, which is a precondition here and not a deliverable, and the load and performance testing of RWB-ITG-NFR.
