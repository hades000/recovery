# RWB-ITG-E1067-ITG Every Workbench action into the interaction ledger — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The event map, `sourceRef` literals, `ce_idempotencykey`, `ce_actor` and the business key form are the ruled values (RD-P1-007, RD-P1-009; findings #1, #2).
- A redelivery leaves one entry and `hit_count` 2; the ledger reads by `occurredAt` then `caseSeq`, and `caseSeq` is arrival order (RD-P1-009; findings #3, #4).
- Non-retryable events go straight to `.dlt` with the `rwb-dlt-*` headers; `LEDGER_WRITE_FAILED` is raised only for exhausted retries; one consumer group per topic (RD-P1-003, RD-P1-009; findings #5, #6).
- Events are keyed by the case uuid, the decision event type is `rwb.decision.DecisionRecorded.v1` and AC13 to AC15 are added (RD-P1-008, RD-P1-023; findings #7, #8, #9).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

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
| Size | Not specified in the source documents (DOR-RWB-ITG-E1067-ITG-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) for the ledger read; the six event types at `.v1` |
| Event contract (rwb.document.events.v1) | Message `rwb.document.DocumentStored.v1`; AsyncAPI document location and JSON Schema registry subject name not specified in the source documents (GAP-1058); both held in configuration, never in code |
| Integration dependencies | RWB-P1-E1067-APP, RWB-P3-E1067-APP, RWB-P5-E1067-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-ILG-005, REQ-ILG-002, REQ-ILG-007) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-023 |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-067 for RWB-ITG-W1. The one in-process outbox and one listener for six `EV-nn` events become the per-service topics `rwb.case.events.v1` (P3 rwb-case: CaseCreated, CaseAllocated, CaseTransferred, TimerBreached), `rwb.document.events.v1` (P5 rwb-document: DocumentStored) and the shared `rwb.decision-record.v1` (DecisionRecorded), all in the CloudEvents 1.0 envelope (DP-09); the ledger stays with P1 rwb-source-data under DP-18, which runs one consumer group, rejects a repeat in `rwb_source_data.processed_event` and appends to `rwb_source_data.interaction`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1067-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 11 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register): version 3, ledger intake assertions aligned with RD-P1-001, 003, 007, 008, 009 and 023.

### 1. Story

As a **QA integration engineer**, I want **the path from a real Workbench action to its entry in the interaction ledger proved end to end on the real wave 1 services and the three real topics — the six actions of the legacy story producing exactly one entry each on the topic of the service that owns them, a repeat of any event writing no second entry and adding exactly one hit, the entries of one case reading in occurred-time order with a `case_seq` that is gap-free from 1 to n even when the three topics deliver out of order, a non-retryable event parked on `.dlt` with its reason, and a failed write parked after its retries with incident `LEDGER_WRITE_FAILED` while the entries already written stay intact**, so that **the case history a case owner reads is complete, ordered and duplicate-free across three topic streams, and not only on the one outbox and one listener of the monolith**.

### 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. If these actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them. Each action already publishes an application event in the same transaction as the change, and a listener turns each event into one entry with its source and actor; events are delivered at least once, so a repeat is rejected by its idempotency key and counted (R-UNI-40). The story serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007, and its measure is unchanged from RWB-E1-067: every Workbench action on a case is in the ledger when it is taken.

In the monolith one in-process outbox and one listener carried all six events, so one order and one duplicate rule held for the whole set. In the 19-service target the same six events arrive from three producers on three topics in the CloudEvents 1.0 envelope (DP-09): `rwb.case.events.v1` carries CaseCreated, CaseAllocated, CaseTransferred and TimerBreached from P3 rwb-case; `rwb.document.events.v1` carries DocumentStored from P5 rwb-document; and the shared `rwb.decision-record.v1` carries DecisionRecorded, whose type and topic P7 rwb-decision owns (DP-03). The ledger does not move: DP-18 and the Ownership Map default ruling keep it with P1 rwb-source-data, which owns `interaction` and its writer in schema `rwb_source_data`, runs one consumer group per topic, rejects a repeat in `processed_event` in the same transaction as the append, and migrates the schema on its own Flyway sequence (DP-01, DP-15). No behaviour is added: what changes is that the six events now travel on three independent streams, and the ledger is written by the service that owns it rather than by the module that changed.

That change is exactly what no single service story can prove. A producer that commits a change without its outbox row, an event that lands on the wrong topic, a second entry after a redelivery on another topic, entries out of occurred-time order because two streams interleaved differently, and a message of an unregistered schema version that is written instead of dead-lettered are all failures that appear only when the three real producers, the three real topics and the real consumer run together. Reference data comes through the rwb-case contract (DP-07), every call is one hop with a 2 s budget (DP-11), the entries reach the case record through the gateway-bff route (DP-19), and the local decision record of the deciding service is what feeds the central ledger (DP-03), so the suite can assert the ledger without any service reading another service's table (DP-01). This story builds and runs that harness; it publishes no operation of its own and owns no schema.

The measure is the legacy one: reads of the case history complete, with a hit count on every repeat and no lost entry, at the retry limit of 3 and the retry cadence of 1 min, 10 min and 1 h before the dead-letter topic (NFR-026). The event-to-ledger map, the read order, the duplicate key, the consumer registrations and the parking of failed events are ruled by RD-P1-003 and RD-P1-009 (GAP-0376 closed; ASM-0540 changed).

### 3. Preconditions

- RWB-P1-E1067-APP is done: the ledger intake runs one consumer group per topic (working group ID `rwb-source-data.<topic>`), dedupes on `ce_id` in `rwb_source_data.processed_event`, appends to `rwb_source_data.interaction` with its `case_seq`, serves the read of section 12.2 and parks to `<topic>.dlt`.
- RWB-P3-E1067-APP is done: CaseCreated, CaseAllocated, CaseTransferred and TimerBreached are published from rwb-case's own outbox to `rwb.case.events.v1` in the same transaction as the change, each with `ce_idempotencykey` and `ce_actor`.
- RWB-P5-E1067-APP is done: DocumentStored is published from rwb-document's own outbox to `rwb.document.events.v1` with `ce_idempotencykey` and `ce_actor`; the decision-record library adds the same two attributes to DecisionRecorded.
- The shared topic `rwb.decision-record.v1` carries DecisionRecorded from the service that takes the decision — in these fixtures P3 rwb-case, through its local decision record and its outbox; the event type and the topic are owned by P7 rwb-decision, whose contract story carries the build (DP-03), so this story takes no P7 dependency.
- The three topics exist with 12 partitions, replication factor 3 and 7-day retention, key caseId, with their retry topics at 1 min, 10 min and 1 h and their `.dlt` topics (Arch v5 slides 11 and 22); the topic and event names come from the naming library (DP-14).
- Schema `rwb_source_data` holds `interaction` with its unique `idempotency_key`, `processed_event` and the outbox and inbox library objects, created by the P1 Flyway sequence (DP-15); the serving identity holds INSERT and SELECT and no UPDATE or DELETE grant on `interaction`.
- The gateway-bff composite route for SCR-03 Case record is deployed in SIT (DP-19, RWB-PLT-N001-CON), so the entries of a case are read the way the case owner reads them.
- The synthetic fixtures of the legacy story are loaded: case "RW-2026-000301" with no ledger entries, queue "MTG-BKK-CO", user "u-teammgr-03", document "DOC-SYN-3011", timer "SLA-ASSIGNED", decision log entry "DLE-SYN-3012" and the idempotency key "EV-02-RW-2026-000301-20261201-<actionId>" (`<actionId>` is the fixture uuid of the action). Every `caseId` is the synthetic uuid of the case; "RW-2026-000301" is display data and part of the business key only.
- The harness RWB-ITG-W1J01-ITG is available with its SIT endpoints, its topic probes and its report writer.
- The event-to-ledger map is that of section 12.4 (RD-P1-009); the suite holds it as configuration and invents no value.
- No production data is used and no production connection is opened. The environment is SIT or DEV, and the suite refuses any other.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1 (Template and Rules §R5.7). The harness is written on Day 1 and run when the three services are in SIT; a fake is never used in their place.
- The design of epic EP01 is signed before build starts on the epic (Definition of Ready and Done v4, item 14); the signed epic design record is Not specified in the source documents (DOR-RWB-ITG-E1067-ITG-14).
- This integration story has no contract story of its own. The ledger contract it asserts against is that of the owning service rwb-source-data, RWB-P1-E1067-CON, which is to be Done and listed with its version in Service Contract Catalog v1 (Definition of Ready and Done v4, item 21); the contract dependency list of this story stays empty.
- This suite builds against no contract fake (section 12.8), so it consumes no version of the contract fake library (Definition of Ready and Done v4, item 22); the fakes of RWB-P1-E1067-CON serve the component stories.
- The story is built on the recommended answers of two open decisions: DL10, "The business lead drafts per module one epic ahead; Legal and Compliance approve."; and DL11, "Use the ACE values where ACE has them; the solution architect proposes the rest; Risk agrees." (Business Requirements Program v5, decision log).

### 4. Flow

1. QA integration engineer: seeds the synthetic fixtures of the harness RWB-ITG-W1J01-ITG — case "RW-2026-000301" with no ledger entries and the six legacy values of the actions; no production data is used.
2. SuiteRunner: reads the run configuration — the three topics with their retry and `.dlt` topics, the three consumer groups of rwb-source-data, the event map, the retry limit 3, the case and its identifiers, and the owner of the dead-letter items — and runs the preflight: the topics and their retry and `.dlt` topics exist, the ledger listener runs in one consumer group per topic, the P3 and P5 producers and the decision-record relay answer, and `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` answers for the case. A missing topic, listener, producer or read stops the run before any test.
3. ActionDriver: drives the six real actions of the legacy story through the owners' own write paths on case "RW-2026-000301" — creation at 2026-12-01T06:10+07:00 by SY-CASEWF, allocation to "MTG-BKK-CO" at 06:40 by SY-RULES, transfer by "u-teammgr-03" at 2026-12-03T14:05+07:00, document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR, timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00 and decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00. The harness calls no service's tables and writes none of them.
4. Producer: commits the change and its outbox row in one transaction in its own schema; the relay publishes one CloudEvents 1.0 event in binary mode on the producer's topic, key the case uuid, carrying IDs and references only, with `ce_idempotencykey` and `ce_actor` (DP-09).
5. rwb-source-data, one consumer group per topic: records `ce_id` in `processed_event` in the same transaction as the append to `interaction`, sets the event code and the `sourceRef` literal from the map of section 12.4, takes the next `case_seq` of the case, and sets source system WORKBENCH, `occurredAt` from `ce_time`, the business key from `ce_idempotencykey` and the actor from `ce_actor`.
6. rwb-source-data: on a `ce_id` it has already seen, writes no entry and raises `hit_count` by one on that `processed_event` row; on a new `ce_id` whose business key already exists in `interaction`, writes no second entry (R-UNI-40).
7. LedgerProbe: reads the entries through the operation of section 12.2 and asserts six entries ordered by `occurredAt` then `caseSeq`, the six event codes, the `sourceRef` literals, the actor, the occurred time and the `case_seq` values 1 to 6 with no gap.
8. OrderDriver: delivers the same six events on their three topics in an order that differs from the occurred times and re-reads the ledger; the entries read in occurred-time order and their `case_seq` values follow the order of arrival with no gap.
9. DuplicateDriver: redelivers one event on each of the three topics with the same CloudEvents id and the same business key, and confirms `hit_count` 2 on each of the three `processed_event` rows and no second entry.
10. PoisonPublisher: publishes one event of an unregistered version (`rwb.case.CaseTransferred.v9`) and one event without `ce_actor`, and confirms each goes straight to `<topic>.dlt` with the `rwb-dlt-*` headers, no retry and no entry; with every ledger insert failing it confirms the retries, the `.dlt` record with `RETRIES_EXHAUSTED`, incident `LEDGER_WRITE_FAILED` and, after the fault is removed, the replay that adds one entry.
11. ReportWriter: writes the evidence report with one row per test case, removes the synthetic fixtures, restores the fixture state and asserts that the run opened no production connection.
12. The run holds the event map, the read order and the duplicate key of RD-P1-009 as configuration and invents no value.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same CloudEvents id | One entry; `hit_count` of its `processed_event` row becomes 2 | None | AC3, AC7 |
| X2 | A non-retryable event: unregistered version, missing `ce_actor` or `ce_idempotencykey`, missing `data.caseId` on the case and document events, or a payload failing the registry schema | Not written; straight to `<topic>.dlt` with `rwb-dlt-reason`, `rwb-dlt-consumer` and `rwb-dlt-owner`; one alert; no `LEDGER_WRITE_FAILED` | None | AC9, AC14 |
| X3 | The ledger append fails | Tried 4 times in all through the retry topics at 1 min, 10 min and 1 h, then `<topic>.dlt` with `rwb-dlt-reason` RETRIES_EXHAUSTED and incident "LEDGER_WRITE_FAILED"; the event is not discarded | MSG-P1-022 (incident detail) | AC5, AC13 |
| X4 | Events of one case arrive on the three topics in an order other than their occurred times | Entries read in occurred-time order; `case_seq` is arrival order with no gap | None | AC8 |
| X5 | The same event reaches two consumer threads at once | One entry; one hit counted | None | AC7 |
| X6 | A topic name, a consumer group or the fixture set does not match what the harness expects | The suite fails as a harness fault and names the element; no service defect is raised | None | AC6 |
| X7 | A consumed call exceeds the 2 s budget or answers a server error | The call is retried once under the suite policy and the report records it; no assertion is made on data that was not read | None | AC6, AC8 |

X1 to X5 are the exception paths of RWB-E1-067 read on the three topics, with the legacy exception queue replaced by the `.dlt` topic of the owning topic (DP-09), and the legacy schema-version path now asserted as the unregistered-version case of AC9. X6 and X7 are the suite's own failure modes, so that a fixture fault is reported as a harness fault and a timeout never becomes a pass.

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
    Given the ledger listener of rwb-source-data runs in one consumer group per topic
    Given the outbox relay of each producer reads its publish retry limit from platform relay configuration with no value fixed in code
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
    Given CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201-<actionId>" was written to the ledger
    When the same event arrives again with the same CloudEvents id and key
    Then one CASE_ALLOCATED entry exists
    Then hit_count of the processed_event row of that CloudEvents id is 2

  Scenario: AC5 The ledger write fails for an event (legacy RWB-E1-067 AC5)
    Given every ledger insert fails
    When DocumentStored for case "RW-2026-000301" is delivered
    Then the delivery is tried 4 times in all
    Then the event is in the exception queue with owner RW-PLATADM
    Then the system raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301"

  Scenario: AC6 Each of the six events arrives on its own owner's topic and makes exactly one entry with the ruled source reference (new, D-RCV-60)
    Given case "RW-2026-000301" has no ledger entries
    When the case is created at 2026-12-01T06:10+07:00, allocated to queue "MTG-BKK-CO" at 06:40, transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00, given document "DOC-SYN-3011" at 2026-12-04T09:30+07:00, given timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00 and given decision log entry "DLE-SYN-3012" at 2026-12-05T11:20+07:00 through the owners' own write paths
    Then rwb.case.events.v1 carries rwb.case.CaseCreated.v1, rwb.case.CaseAllocated.v1, rwb.case.CaseTransferred.v1 and rwb.case.TimerBreached.v1 for the case
    Then rwb.document.events.v1 carries rwb.document.DocumentStored.v1 for the case
    Then rwb.decision-record.v1 carries rwb.decision.DecisionRecorded.v1 for the case
    Then each event is a CloudEvents 1.0 event in binary mode whose key and data.caseId are the case uuid, with attributes ce_idempotencykey and ce_actor
    When GET /api/recovery/source-data/v1/cases/{caseId}/interactions is read for the case
    Then it returns exactly 6 entries with the event codes CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN
    Then each entry carries source system "WORKBENCH" and the sourceRef "EV-01 CaseCreated", "EV-02 CaseAllocated", "EV-04 CaseTransferred", "EV-19 TimerBreached", "EV-16 DocumentStored" or "EV-08 DecisionRecorded" of its event, with actorType and actorRef taken from ce_actor and occurredAt from ce_time
    Then the DOCUMENT_ATTACHED entry holds documentId from data.documentId and the DECISION_TAKEN entry holds decisionLogId from data.entryId
    Then no entry was written from a fourth topic and no service read another service's table

  Scenario: AC7 A redelivery on any of the three topics adds one hit and no entry (new, D-RCV-60)
    Given the ledger holds the 6 entries of case "RW-2026-000301"
    When the CaseAllocated event with idempotency key "EV-02-RW-2026-000301-20261201-<actionId>" is redelivered on rwb.case.events.v1
    And the DocumentStored event of "DOC-SYN-3011" is redelivered on rwb.document.events.v1
    And the DecisionRecorded event of "DLE-SYN-3012" is redelivered on rwb.decision-record.v1
    Then the ledger still holds 6 entries for the case
    Then each redelivery raises hit_count from 1 to 2 on the rwb_source_data.processed_event row of its own CloudEvents id
    Then no case_seq is reused and no entry is updated or removed

  Scenario: AC8 Entries read in occurred-time order with a gap-free sequence across three topics (new, D-RCV-60)
    Given the 6 events of case "RW-2026-000301" carry their occurred times from 2026-12-01T06:10+07:00 to 2026-12-05T11:20+07:00
    When rwb.case.events.v1, rwb.document.events.v1 and rwb.decision-record.v1 deliver them out of order, so the DocumentStored event arrives before CaseCreated
    Then GET /api/recovery/source-data/v1/cases/{caseId}/interactions returns the 6 entries ordered by occurredAt then caseSeq, from the earliest to the latest
    Then the case_seq values are 1 to 6 with no gap and no repeat, in the order of arrival, so the DOCUMENT_ATTACHED entry holds a lower case_seq than the CASE_CREATED entry
    Then each entry keeps the event code its own event carries

  Scenario: AC9 An unregistered event version goes straight to .dlt (new, D-RCV-60; changed by RD-P1-009)
    Given CaseTransferred is registered at version v1 only and the ledger holds the entries already written for case "RW-2026-000301"
    When an event of type rwb.case.CaseTransferred.v9 is published on rwb.case.events.v1 for the case
    Then no retry topic receives it
    Then the system writes no entry for it and the entries already written stay unchanged
    Then the record is on rwb.case.events.v1.dlt with its original ce_ headers and rwb-dlt-reason "UNSUPPORTED_VERSION", rwb-dlt-consumer "rwb-source-data" and rwb-dlt-owner "P1 squad"
    Then one alert is raised and no incident LEDGER_WRITE_FAILED is raised

  Scenario: AC10 Each entry names its producer, its event carries no personal data and it is read only through the owner's contract within 2 s (new, D-RCV-60)
    Given the ledger holds the 6 entries of case "RW-2026-000301"
    When GET /api/recovery/source-data/v1/cases/{caseId}/interactions is read for the case
    Then each entry names the system or person that produced it
    Then the payload of each event carries references and codes and no personal data
    Then the read is one hop on the owner's contract and returns within 2 s
    Then no service other than rwb-source-data reads the ledger tables

  Scenario: AC11 A consumed call fails or does not answer within its 2 s budget (new, D-RCV-60)
    Given the ledger holds the 6 entries of case "RW-2026-000301"
    When the owner's contract fails or does not answer the read of GET /api/recovery/source-data/v1/cases/{caseId}/interactions within 2 s
    Then the caller receives a failure and no partial list of entries
    Then the entries already in the ledger stay unchanged

  Scenario: AC12 A status change the model does not allow is refused (new, D-RCV-60)
    Given the ledger holds the 6 entries of case "RW-2026-000301"
    When a status change that the case status model does not allow is requested through the owner's write path for case "RW-2026-000301"
    Then the change is refused, no event is published for it and no entry is written for it
    Then the entries already in the ledger stay unchanged

  Scenario: AC13 Exhausted retries park the event and a replay adds it once (new, RD-P1-009)
    Given every ledger insert fails and DocumentStored of "DOC-SYN-3011" has been tried 4 times
    When the record is read on rwb.document.events.v1.dlt
    Then it holds rwb-dlt-reason "RETRIES_EXHAUSTED", rwb-dlt-consumer "rwb-source-data" and rwb-dlt-owner "P1 squad"
    Then one incident LEDGER_WRITE_FAILED with MSG-P1-022 in its detail is raised by the intake
    When the insert fault is removed and the record is replayed with the platform replay tool
    Then one DOCUMENT_ATTACHED entry is added and the earlier entries are unchanged

  Scenario: AC14 An event without ce_actor goes straight to .dlt (new, RD-P1-009)
    Given a CaseAllocated event for case "RW-2026-000301" has no ce_actor attribute
    When it is delivered
    Then no retry topic receives it and no entry is written
    Then the record is on rwb.case.events.v1.dlt with rwb-dlt-reason "MISSING_ATTRIBUTE"

  Scenario: AC15 A type outside the map is committed and ignored (new, RD-P1-009)
    Given a synthetic event of a ce_type outside the six rows of the map is published on rwb.case.events.v1
    When the intake reads it
    Then its offset is committed, no processed_event row and no entry are written, and nothing is parked
```

AC1, AC3 and AC5 are the legacy proof of RWB-E1-067; AC1 and AC5 are carried unchanged, including the words "exception queue", and AC3 takes the ruled key form and hit count; in the target that queue is the `.dlt` topic of the owning topic (DP-09), the retry limit of 3 gives the four delivery attempts of AC5, AC13 proves the parked record, the incident `LEDGER_WRITE_FAILED` and the replay, and AC9 and AC14 prove the non-retryable path. No scenario uses a contract mock: every step runs against the real services, the real topics and the real relay. AC6 to AC9 and AC13 to AC15 use the synthetic values of the legacy story and the ruled fixture values. The legacy AC2, AC4, AC6, AC7 and AC8 belong to RWB-P1-E1067-APP, not to this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen | REQ-ILG-005; EV-01, EV-02, EV-04, EV-19, EV-16, EV-08 (events.txt); EV-16 maps to rwb.document.DocumentStored.v1 and EV-19 to rwb.case.TimerBreached.v1 (Arch v5 slide 15 rows 16 and 19) |
| BR2 | Every entry names the system or person that produced it | REQ-ILG-002 |
| BR3 | The same event produces one entry and the repeat is counted: a redelivery is deduplicated on `ce_id` in `processed_event` (`hit_count` plus one), and the business key from `ce_idempotencykey` (`<code>-<caseNo>-<yyyyMMdd>-<actionId>`) is unique on `interaction` | R-UNI-40; REQ-ILG-007; RD-P1-007; RD-P1-009 |
| BR4 | `caseSeq` is arrival order, assigned under the case lock with no gap; the ledger is read ordered by `occurredAt` then `caseSeq`; the intake does not wait behind a failed event | RD-P1-009 rule 7 |
| BR5 | A transient consumer failure is retried through the retry topics at 1 min, 10 min and 1 h, then parked on `<topic>.dlt` with an alert; a non-retryable failure goes straight to `.dlt` | R-UNI-36; Arch v5 slides 11 and 22; RD-P1-009 |
| BR6 | A consumer accepts the current and the previous registered version (the `.vN` suffix of `ce_type`); all six types are `.v1` only; any other version is not written and goes straight to `.dlt` | Events rule "Versioning"; RD-P1-009 rule 4 |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt); Arch v5 slides 42 and 43 |
| BR8 | One consumer group per topic reads the three topics, and the dedupe in `processed_event` commits in the same transaction as the append to `interaction` | DP-09; RD-P1-003; RD-P1-009 |
| BR9 | The ledger is owned by P1 rwb-source-data in `rwb_source_data`; no other service reads its tables and the suite owns no schema | DP-01; DP-18; DP-15 |
| BR10 | Every cross-service read is one hop on the owner's contract with a 2 s budget | DP-11; ADR-020 |
| BR11 | Each producer publishes its own event type on its own topic in the CloudEvents 1.0 envelope, key caseId, with IDs and references only, the business key in `ce_idempotencykey` and the actor in `ce_actor` (RD-P1-009); the registry subjects of rwb.case.events.v1 and rwb.document.events.v1 and the AsyncAPI document location are held in configuration, values Not specified in the source documents (GAP-2257, GAP-1058); the ledger listener of rwb-source-data has one consumer group on each of the case, document and decision-record topics | DP-09; DP-03; Arch v5 slides 11, 42 and 43; ASM-0541 |
| BR12 | Only an event parked as RETRIES_EXHAUSTED raises `LEDGER_WRITE_FAILED` for its case; a parked event is replayed with the platform replay tool after its cause is removed | RD-P1-009 rule 6; ASM-0542 |

### 9. State transitions

None for a case status. This story changes no case status of its own; it drives the owners' write paths and observes the ledger, the inbox and the delivery states.

| Object | State | Meaning |
|---|---|---|
| `interaction` entry | Appended once | Written in the transaction that records the inbox row; never updated and never deleted |
| `processed_event` row | Deduplicated | One row per CloudEvents id; `hit_count` is 1 on first delivery and rises by one on each redelivery |
| Inbox delivery | Received, retried or parked | Received on the owner's topic; a transient failure moves to a retry topic at 1 min, 10 min or 1 h, then `<topic>.dlt`; a non-retryable failure moves straight to `.dlt` |
| Poison message | Parked | Not written; on `<topic>.dlt` with the `rwb-dlt-*` headers; replayed only after its cause is removed |
| Harness run | Not started, running, passed or failed | A failing step stops the run and the report names the criterion, the topic and the evidence |

The suite reads these states through the owners' contracts and the topics; it changes none of them directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| P1 rwb-source-data owner (RWB-P1-E1067-APP) | Owns the listener, the inbox dedupe, the append, the `case_seq`, the read operation and the dead-letter handling; `rwb-dlt-owner` is the P1 squad |
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
| DF-INT-018 | `interaction` | idempotency_key | Write; unique; the business key from `ce_idempotencykey` |
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
| GET `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Confirms the entries of one case: the six event codes, the source reference, the actor, the occurred time and `case_seq`, ordered by `occurredAt` then `caseSeq`; the assertion surface of AC1, AC6, AC7 and AC8 |

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

All six are consumed in the CloudEvents 1.0 envelope in binary mode, with the required extension attributes `ce_idempotencykey` and `ce_actor` (`USER:<userId>`, `SERVICE:<service name>` or `PARTNER:<partnerCode>`), by one consumer group of rwb-source-data per topic (working IDs `rwb-source-data.<topic>`), with `auto.offset.reset=earliest` at first start. Transient failures use the retry topics at 1 min, 10 min and 1 h and then `<topic>.dlt`; non-retryable failures go straight to `.dlt`. Each parked record keeps the original record and `ce_` headers and adds `rwb-dlt-reason`, `rwb-dlt-consumer` and `rwb-dlt-owner`. rwb-source-data is an added consumer of these topics, with no change to their existing consumers (ASM-0541; RD-P1-003; RD-P1-009).

The event-to-ledger map (RD-P1-009 rule 2), with `sourceSystem` WORKBENCH, `occurredAt` from `ce_time`, `caseId` from `data.caseId` and the business key from `ce_idempotencykey`: CaseCreated to CASE_CREATED (`sourceRef` `EV-01 CaseCreated`); CaseAllocated to CASE_ALLOCATED (`EV-02 CaseAllocated`, `toHolderRef` `USER:` + `data.ownerId`); CaseTransferred to CASE_TRANSFERRED (`EV-04 CaseTransferred`, `fromHolderRef` and `toHolderRef` from `data.fromOwner` and `data.toOwner`); TimerBreached to CASE_ESCALATED (`EV-19 TimerBreached`); DocumentStored to DOCUMENT_ATTACHED (`EV-16 DocumentStored`, `documentId`); DecisionRecorded to DECISION_TAKEN (`EV-08 DecisionRecorded`, `decisionLogId` from `data.entryId`). Any other `ce_type`, and a DecisionRecorded event with no `data.caseId`, is committed and ignored.

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
| Wave1Topology fixture | Configuration | Names the real SIT endpoints, the three consumer groups and the three topics with their retry and `.dlt` topics; fails the run when a fake endpoint is configured |
| ActionDriver | Test service | Drives the six real actions of case "RW-2026-000301" through the owners' own write paths |
| TopicProbe | Test service | Consumes the three topics and their retry and `.dlt` topics and asserts the count, the CloudEvents type, the key and the absence of personal data |
| LedgerProbe | Test service | Reads the interaction operation and asserts the six entries in occurred-time order, the codes, the source reference, the actor and the `case_seq` values 1 to 6 |
| DuplicateDriver | Test service | Redelivers one event on each topic with the same CloudEvents id and idempotency key and collects the hit evidence |
| OrderDriver | Test service | Replays the six events out of occurred-time order and re-reads the ledger |
| PoisonPublisher | Test service | Publishes the unregistered-version event, the event without `ce_actor` and the unlisted type, drives the failing insert, reads the `.dlt` headers and the incident and replays the parked record |
| ReportWriter | Service | One row per test case with the evidence and the elapsed times |

**Database.** None of its own. The harness writes no table and no schema: every action goes through the owner's own write path and every assertion is a contract response or a topic observation (DP-01, DP-18).

**Configuration and reference data.**

- The three topics with their retry and `.dlt` topics, the three consumer groups, the read base and the wait windows, all as configuration.
- The event map EV-01 CASE_CREATED, EV-02 CASE_ALLOCATED, EV-04 CASE_TRANSFERRED, EV-19 CASE_ESCALATED, EV-16 DOCUMENT_ATTACHED and EV-08 DECISION_TAKEN, read from configuration and never written in code (legacy `rwb.dataengine.ledger.event-map`).
- The source-reference literals `<event ID> <event name>` of the map of section 12.4.
- The retry limit 3 with the retry topics at 1 min, 10 min and 1 h (NFR-026; DL11).
- The synthetic case "RW-2026-000301" with "u-teammgr-03", "MTG-BKK-CO", "DOC-SYN-3011", "SLA-ASSIGNED", "DLE-SYN-3012" and "EV-02-RW-2026-000301-20261201-<actionId>".
- RW-PLATADM, who owns the dead-letter records and alerts, the header value `rwb-dlt-owner` = `P1 squad`, and the incident `LEDGER_WRITE_FAILED`.
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
| Redelivery fixture | One event per topic republished with the same CloudEvents id and the same business key | AC3, AC7, TC-E1-067-03-ITG, TC-ITG-E1067-02 |
| Out-of-order fixture | The same six events with the same occurred times, published so DocumentStored arrives before CaseCreated | AC8, TC-ITG-E1067-03 |
| Poison fixture | `rwb.case.CaseTransferred.v9`, a CaseAllocated event without `ce_actor` and a synthetic unlisted type | AC9, AC14, AC15, TC-ITG-E1067-04 |
| Failure fixture | Every insert failing for the DocumentStored delivery, with the retry limit 3 | AC5, TC-E1-067-05-ITG |

Every fixture value is the legacy value carried unchanged; no new business value is invented.

**Build steps.**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT topics and the rwb-source-data base.
2. Add the topology preflight: the three topics with their retry and `.dlt` topics, one consumer group per topic, the three producers and the read operation.
3. Implement AC1 and AC6: the six actions through the owners' write paths, the six events on their own topics and the six entries with their source references.
4. Implement AC3, AC7 and AC8: the redelivery on each topic, the hit count, the out-of-order delivery, the read order and the gap-free `case_seq`.
5. Implement AC5, AC9 and AC13 to AC15: the failing insert with the four deliveries, the `.dlt` headers, incident `LEDGER_WRITE_FAILED` and the replay, the non-retryable events and the unlisted type.
6. Write the evidence report, reset the fixtures and run the suite in SIT against the wave 1 release candidate.

**Done when.** The test cases of section 16 pass in SIT against the published wave 1 contracts of the P3 and P5 producers and the P1 ledger, the six real actions produce exactly six entries each with its ruled source reference, a redelivery on any of the three topics adds one hit and no entry, the entries of one case read in occurred-time order with a gap-free `case_seq`, a non-retryable event is parked on `.dlt` without retries, a failed write raises `LEDGER_WRITE_FAILED` after its retries, the earlier entries stay intact, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | Ledger write failed after its retries, carried in the incident detail | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without Case record C calls the ledger writer or reads the entries | You cannot {action} here. Your role does not include it. |

The two texts are copied unchanged from RWB-E1-067; this story adds no message text and no message ID. The refusal of MSG-P4-002 belongs to the writer's identity check of RWB-P1-E1067-APP and is carried here as the message the case record shows. A parked record carries no message ID; it holds the original record, its `ce_` headers and the three `rwb-dlt-*` headers, and only a RETRIES_EXHAUSTED record has the incident `LEDGER_WRITE_FAILED` with MSG-P1-022 (RD-P1-009; ASM-0542). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built or tested by this story. The platform administrator sees a dead-letter item on SCR-09 Exception queue (Epic 1, state List; loading as in Screen Specifications v1; empty, error and no access Not specified in the source documents (CG-ALL-434)), and the case owner reads the entries on SCR-03 Case record (Read only; loading as in Screen Specifications v1; empty, error and no access Not specified in the source documents (CG-ALL-433)) through the gateway-bff composite route on the rwb-source-data base, one hop with a 2 s timeout (DP-19). The suite reads the same entries through the owner's contract; both screens are referenced and neither is changed here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01-ITG | AC1, BR1 | Integration | Six synthetic events for case RW-2026-000301 on the three real topics; no numeric business values added |
| TC-E1-067-03-ITG | AC3, BR3 | Integration | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201-<actionId>; one entry, `hit_count` 2 (row to be updated in Test Cases v9, W2-tests) |
| TC-E1-067-05-ITG | AC5, BR5 | Integration | Ledger insert forced to fail for DocumentStored; retry limit 3; four deliveries; owner RW-PLATADM; incident LEDGER_WRITE_FAILED |
| TC-ITG-E1067-01 | AC6, BR1, BR11 | Integration | Six real actions on the three topics for case RW-2026-000301; each entry names its owning service and event |
| TC-ITG-E1067-02 | AC7, BR3, BR8 | Integration | One redelivery on each of the three topics with the same CloudEvents id and idempotency key |
| TC-ITG-E1067-03 | AC8, BR4 | Integration | The six events delivered out of occurred-time order across the three topics; read in occurred-time order; `case_seq` 1 to 6 in arrival order (row to be updated in Test Cases v9, W2-tests) |
| TC-ITG-E1067-04 | AC9, BR5, BR6 | NFR | `rwb.case.CaseTransferred.v9`; straight to `.dlt` with UNSUPPORTED_VERSION; no retry, no incident; earlier entries unchanged (row to be updated in Test Cases v9, W2-tests) |
| TC-ITG-E1067-05 | AC10, BR2, BR7, BR9, BR10 | Integration | Six entries of case RW-2026-000301 read through the owner's contract; producer named on each entry; payload checked for personal data; 2 s budget |
| TC-ITG-E1067-06 | AC11 | Integration | Owner's contract forced to fail or not answer within 2 s on the interactions read; failure returned; no partial list; ledger entries unchanged |
| TC-ITG-E1067-07 | AC12 | Integration | Status change the model does not allow requested through the owner's write path for case RW-2026-000301; refused; no event published; no entry written; ledger entries unchanged |
| TC-E1-067-06-ITG | AC13, BR5, BR12 | Integration | Exhausted retries, headers, incident and replay |
| TC-E1-067-07-ITG | AC14, BR5 | Integration | CaseAllocated without `ce_actor`; MISSING_ATTRIBUTE |
| TC-E1-067-08-ITG | AC15 | Integration | Unlisted type committed and ignored |

The three legacy criteria this story owns carry their legacy test case ID with the suffix `-ITG`; the new criteria carry `TC-ITG-E1067-01` to `-07`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID. The legacy test cases of AC2, AC4, AC6, AC7 and AC8 stay with RWB-P1-E1067-APP.

### 17. Guardrails

- No business value in code: the event map, the retry limit, the topics, the consumer group and the synthetic case are configuration; the six event codes and the six event IDs are the legacy ones.
- No personal data in event payloads: they carry codes, IDs and references only (events rule "Payload"; Arch v5 slides 42 and 43). No personal data in logs or the report, and no real personal data in fixtures; the report holds counts, ids and timings.
- Personal data fields touched (Data Classification and Personal Data Inventory v5): the ledger entries read by the suite hold DF-INT-003 (`person_key`, indirect identifier), DF-INT-011 (`summary`, direct identifier, Restricted) and DF-INT-004 to DF-INT-010 and DF-INT-012 to DF-INT-019 (customer data, Confidential). They are shown only within the role's scope, DF-INT-011 is masked unless the role may see it, and the suite holds synthetic values only. DF-INT-001, DF-INT-002, DF-INT-020 and DF-OPS-178 to DF-OPS-183 are classed Not personal.
- No cross-service table read and no schema of its own: every action goes through the owner's write path and every assertion is a contract response or a topic observation (DP-01, DP-18); the only read of `processed_event` is made by its owner and attached to the evidence.
- One hop and a 2 s timeout on every call (ADR-020, DP-11), and a timeout is never retried into a pass.
- One event type per producer topic and one ledger consumer group per topic (BR8, BR11); a service that publishes another service's event, or a second ledger group on a topic, fails the run.
- The ledger entry is never updated and never deleted; the harness asserts the refusal instead of relying on the review.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG and reset after a run, with no production access of any kind; the suite refuses an environment that is not SIT or DEV.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | The three topics and the six event types of 12.4; `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`; the event map of section 13 | TC-E1-067-01-ITG, TC-E1-067-05-ITG, TC-ITG-E1067-01, TC-ITG-E1067-04 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The `interaction` field set DF-INT-001 to DF-INT-020, the source reference and the read response of 12.2 | TC-E1-067-01-ITG, TC-ITG-E1067-01 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | `processed_event`, the CloudEvents id and `interaction.idempotency_key` | TC-E1-067-03-ITG, TC-ITG-E1067-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three topics, the six CloudEvents types, the retry and `.dlt` topics and the `rwb-dlt-*` headers | TC-ITG-E1067-01, TC-ITG-E1067-04 |
| DP-01 / DP-18 | Owner's schema, never another service's tables; the ledger is P1's | One writer for `rwb_source_data`; the suite asserts through the owner's contract | All |
| ASM-0540 (changed by RD-P1-009) | One consumer group per topic; the ledger reads by occurred time then `case_seq`; the map and the duplicate key are ruled | The map and attributes of 12.4 | TC-ITG-E1067-01, TC-ITG-E1067-02, TC-ITG-E1067-03 |
| ASM-0541 | The ledger listener is an added consumer on the case and document topics | One consumer group of rwb-source-data per topic | TC-ITG-E1067-01 |
| ASM-0542 | A dead-lettered ledger event raises LEDGER_WRITE_FAILED | The `.dlt` item of AC9 and the incident line of section 14 | TC-ITG-E1067-04 |

The legacy AC1 to AC8 at component level belong to RWB-P1-E1067-APP, RWB-P3-E1067-APP and RWB-P5-E1067-APP, not to this story; this list carries only the three criteria the story owns and the seven it adds.

### 19. Out of scope

- The listener, the inbox dedupe, the append, the `case_seq`, the read operation and the dead-letter handling of the ledger (RWB-P1-E1067-APP), with its CON, DB and OPS stories.
- The producers of `rwb.case.events.v1` and `rwb.document.events.v1` (RWB-P3-E1067-APP, RWB-P5-E1067-APP) and the event type and topic contract of `rwb.decision-record.v1` with the local decision record that publishes DecisionRecorded (DP-03, RWB-PLT-E1027-CON).
- The ledger store and writer of RWB-E1-066 and the read interface of RWB-E1-068, which are taken over by the P1 stories of those legacy keys.
- The legacy AC2, AC4, AC6, AC7 and AC8 at component level, which RWB-P1-E1067-APP owns.
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).
- Retention periods, the retention run, and the daily seal of the central decision ledger to immutable storage.
- The build of the harness RWB-ITG-W1J01-ITG, which is a precondition here and not a deliverable, and the load and performance testing of RWB-ITG-NFR.

### 20. Remaining delivery steps

- Size and epic design sign-off: Pending (owner: squad and solution architect).
- RWB-P1-E1067-CON Done with `ce_idempotencykey` and `ce_actor` published in the rwb-document and decision-record AsyncAPI files: Pending (owner: contract owners).
- Consumer group ID scheme fixed (RWB-PLT-E1047-CON): Pending (owner: platform event owner).
- Update TC-E1-067-03-ITG, TC-ITG-E1067-03 and -04 and add the AC13 to AC15 rows in Test Cases v9: Pending (owner: QA).
- Fixtures and fault controls in SIT: Pending (owner: QA).
