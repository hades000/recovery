# RWB-P1-E1067-APP Every Workbench action into the interaction ledger

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1067-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-067 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified; pending squad refinement |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); intake map version 1 |
| Screens and states | None; no screen is served here (DP-19); SCR-09 states are not owned by this story |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P1-P |
| Ready to start | After E1067-CON and the E1066 writer are ready; the consumer-group deployment of RWB-P1-E1066-OPS is a later step (RD-P1-074) |
| Depends on (build) | RWB-P1-E1067-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1066-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1066-OPS (declares the intake consumer groups; later deployment step, no build dependency) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-008, RD-P1-009 (X-03), RD-P1-072, RD-P1-074 |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- Intake of six facts on three owner topics with the final map, envelope attributes, inbox dedupe, in-process writer, retry topics and `.dlt` parking (RD-P1-007, RD-P1-008, RD-P1-009; consumer groups by RWB-P1-E1066-OPS, X-03).
- Acceptance criteria rewritten on read order and `.dlt`; AC16 to AC19 added; the exception-queue wording removed.
- Findings RWB-P1-E1067-APP#1 to #22 fixed or carried as pending with a gap ID (NEW-GAP-S8-11, NEW-GAP-F09-4).
- Batch D: a read is not a decision, so row 06 needs no filter (RD-P1-072; NEW-GAP-F09-4 closed, superseding the open item of the last bullet above); the build cycle with RWB-P1-E1066-OPS is cut (RD-P1-074). Test case IDs TC-P1-E1067-APP-05 to -08 cited.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register); applied RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-008 and RD-P1-009 (X-03); findings RWB-P1-E1067-APP#1 to #22.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-067 for rwb-source-data. The outbox listener of the monolith becomes the ledger listener of rwb-source-data, a Kafka consumer on the service's own worker that reads the owner topics of six facts; the event-to-entry map moves to configuration and to the contract of RWB-P1-E1067-CON; the in-process `InteractionLedgerWriter` becomes the in-process `InteractionLedgerWriter` of RWB-P1-E1066-APP in the intake transaction (RD-P1-007); the case-existence check is the writer's, not the listener's; the inbox `processed_event` and the idempotency table are PLT library objects created in `rwb_source_data` (DP-09); the ledger table is P1's (DP-01, DP-18); LOV-LEDGER-EVENT comes from rwb-case (DP-07); the append writes no decision record; the acting service records its own decision (RD-P1-007); the schema migration is on the per-service sequence (DP-15); no screen is served here (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1067-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

This is the listener slice of legacy RWB-E1-067 in rwb-source-data. It owns:

- `LedgerEventListener`, the consumer of the six owner topics on the service's own worker, in the consumer group of the service; its inbox rows, retry topics and dead-letter topic are the platform ones (DP-09; Architecture v5 slides 11 and 41);
- the event-to-entry map as configuration and as the contract of RWB-P1-E1067-CON, which turns EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-19 TimerBreached, EV-16 DocumentStored and EV-08 DecisionRecorded into the entry codes CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED and DECISION_TAKEN;
- the schema-version acceptance of the legacy listener (current and previous), the duplicate rule and the arrival-order rule, applied around the append;
- the in-process call of `InteractionLedgerWriter` of RWB-P1-E1066-APP in the intake transaction (RD-P1-007), which holds the case-existence check and the write of the entry;
- the incident `LEDGER_WRITE_FAILED` and the parking of a failed or unknown event in the matching `<topic>.dlt` topic with the RD-P1-009 headers.

It does not own the ledger table `interaction`, the writer, the case sequence or the list LOV-LEDGER-EVENT: those are RWB-P1-E1066-APP and RWB-P1-E1066-CON. It does not own the inbox and idempotency tables: `processed_event` and `idempotency_key` are PLT library objects created in `rwb_source_data` (DP-09; Ownership Map). It creates no table of its own and reads no table of another service (DP-01). It serves no screen (DP-19).

### 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. Each owner service writes its state change and its outbox row in one transaction, and its relay publishes the event to its own topic keyed by the case ID (DP-09; Architecture v5 slides 11 and 42). rwb-source-data consumes those six facts and appends one entry per fact, so the case owner sees the customer contacts and what the Workbench did between them, with the source and the actor of each action.

In the target the ledger is a capability of one service instead of a table of the monolith: the ledger and its intake rule are rwb-source-data's (DP-18; Template and Rules §R3 default ruling), the table `interaction` sits in `rwb_source_data` (DP-01), and the other eighteen services reach it through this service's contract and never through its table. Delivery is at least once, so the listener accepts the current and the previous schema version, records `caseSeq` in arrival order (the read orders by `occurredAt` then `caseSeq`), and uses `ce_id` only for inbox dedupe and passes `ce_idempotencykey` as the ledger business key, so a repeat increments the hit count of the inbox row instead of writing a second entry (R-UNI-40; DP-09). A failed or unreadable event is never acknowledged and never discarded: it is parked with its reason and its owner (R-UNI-36; NFR-026).

Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007; applies DP-01, DP-03, DP-07, DP-09, DP-11, DP-15, DP-18 and DP-19. The measure is one ledger entry per published fact; no event-to-entry lag target is given by any source, and NFR-070 applies to the read of RWB-P1-E1068-APP.

### 3. Preconditions

- RWB-P1-E1066-APP is done: the ledger table `interaction`, the case sequence, the append operation, the duplicate rule on `idempotency_key` and LOV-LEDGER-EVENT are in place (DP-01, DP-07, DP-18).
- RWB-P1-E1067-CON is published: the intake map, the six event fixtures and the writer stub of section 12.8, so the listener is written against a fixed contract from Day 1 (DP-11).
- RWB-PLT-TE006-CON is on the classpath: the outbox and inbox library with `processed_event` and `idempotency_key` created in `rwb_source_data`, the CloudEvents 1.0 envelope, the retry topics and the `.dlt` topic (DP-09; Architecture v5 slide 11).
- RWB-PLT-E1027-CON is on the classpath: the local decision-record library that publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, the sixth consumed type (DP-03).
- RWB-PLT-E1043-CON is on the classpath and RWB-P3-E1043-CON is published with its fake, so the entry codes are read as LOV-LEDGER-EVENT from the reference-data contract and never written in code (DP-07).
- RWB-PLT-E1044-CON is in place: the per-service Flyway sequence of rwb-source-data, on which the library migrations of the inbox arrive (DP-15).
- RWB-PLT-N001-CON exists for the gateway-bff composite route; this story serves no screen and adds no route to it (DP-19).
- The six producers publish their facts with the header and the payload of events.txt: event ID, idempotency key, schema version, occurred time and actor in the envelope, and IDs and codes only in the payload (legacy RWB-E1-067 §3; Architecture v5 slides 42 and 43 notes).
- The event type names the intake consumes are fixed by the Arch v5 event catalogue: `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1` and `rwb.case.TimerBreached.v1` on `rwb.case.events.v1` (P3), `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` (P5) and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (P7).
- The Kafka Topic and Event Catalog lists rwb-source-data as consumer of EV-01, EV-02, EV-04, EV-19, EV-16 and EV-08 with read access to the three topics and their retry topics (RD-P1-003 rule 5), and rwb-case, rwb-document and the decision-record library publish `ce_idempotencykey` and `ce_actor` (RD-P1-009 rule 1). EV-16 and EV-19 are read as `rwb.document.DocumentStored.v1` and `rwb.case.TimerBreached.v1` (GAP-0507, resolved).

### 4. Flow

1. Each owner publishes a CloudEvents message to its owner topic with the case UUID as the Kafka key.
2. One consumer group per topic delivers records to `LedgerEventListener`. Group IDs use the working pattern `rwb-source-data.<topic>` (NEW-ASM-A2); no group is created for `rwb.source-data.events.v1`.
3. The listener reads `ce_type`. The version is its `.vN` suffix and the registry subject; the current and previous registered versions are accepted. All six mapped types are `.v1` only; an unregistered synthetic type such as `rwb.case.CaseTransferred.v9` is parked.
4. The listener requires `ce_idempotencykey` (business key, at most 120) and `ce_actor` (`USER:<userId>`, `SERVICE:<service name>` or `PARTNER:<partnerCode>`, at most 74). `actorType` is the prefix before the first colon; `actorRef` is the remainder, at most 64. `occurredAt=ce_time`, `sourceSystem=WORKBENCH`, and `caseId=data.caseId`.
5. The mapper applies the six rows of E1067-CON. It sets `decisionLogId=data.entryId` for DecisionRecorded; it does not read `approver`, personal fields or `ce_source` for routing. Other event types on the three topics are committed and ignored. DecisionRecorded without `data.caseId` is committed and ignored.
6. In one transaction, the listener checks `processed_event` by `ce_id`. If present, it increments `hit_count` and updates `last_seen_at`, commits, and adds no entry. Otherwise it inserts the inbox row with `hit_count=1` and calls `InteractionLedgerWriter` in process. The request business key is `ce_idempotencykey`; if that key already exists in `interaction`, no entry or new `caseSeq` is created.
7. The inbox insert and writer append commit atomically. The append does not write a decision record. The listener does not wait behind a failed event. `caseSeq` is arrival order; ledger reads sort by `occurredAt`, then `caseSeq`.
8. Transient failures (database, case read timeout) are published to the next retry topic (1 min, 10 min, 1 h) and the offset is committed only after that publish; after the third retry the record goes to `<topic>.dlt`. Missing `ce_actor` or `ce_idempotencykey`, unsupported version, payload failing the registry schema and missing `data.caseId` on rows 01 to 05 go directly to `.dlt`. The record and its `ce_*` headers are preserved; added headers are `rwb-dlt-reason`, `rwb-dlt-consumer=rwb-source-data` and `rwb-dlt-owner=P1 squad`. The handling of a writer refusal that is not transient (case not found, validation refusal, decision-log reference check) is pending (NEW-GAP-S8-11).
9. One alert is raised per `.dlt` record. `LEDGER_WRITE_FAILED` with MSG-P1-022 is raised only by the intake for `RETRIES_EXHAUSTED`; the REST writer never raises this incident for intake calls. The platform replay tool replays parked records without changing earlier entries.
10. At first start, groups use `auto.offset.reset=earliest`. When the intake feature flag is off, they pause and resume from the committed offset when enabled. Records older than the 7-day topic retention are recovered only from `.dlt` through the replay tool.
11. The writer applies its rules of RWB-P1-E1066-APP to an intake call, but its REST idempotency header and rights checks do not apply: no user token and no HTTP call exist. Every decision record that carries `data.caseId` becomes a DECISION_TAKEN entry (row 06). Reads (case record, data product, customer and authorise checks) are written to the access log only and publish no DecisionRecorded, so only decisions under DP-03 reach row 06 (RD-P1-072).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice | One entry; the inbox row counts the repeat | None | AC7, AC16 |
| X2 | A schema version that is neither current nor previous | Not written; `<topic>.dlt` with `rwb-dlt-reason=UNSUPPORTED_VERSION` | None | AC4 |
| X3 | The write fails with a transient error on every attempt | Retry topics 1 min, 10 min, 1 h, then `.dlt` with `RETRIES_EXHAUSTED`; incident `LEDGER_WRITE_FAILED`; nothing discarded | MSG-P1-022 (incident detail) | AC9 |
| X4 | Events for one case arrive late or out of order | `caseSeq` follows arrival; the read orders by `occurredAt` then `caseSeq` | None | AC6 |
| X5 | The same event reaches two consumer threads at once | One entry; hit count 2 | None | AC7 |
| X6 | An event names a case that does not exist | No entry; handling of the parked or retried record pending (NEW-GAP-S8-11) | Pending | AC8 |
| X7 | The case read does not answer inside 2 s | Next retry topic, then commit; no entry counted | MSG-P1-022 on exhaustion | AC10 |
| X8 | `ce_actor` or `ce_idempotencykey`, or `data.caseId` on rows 01 to 05, is missing, or the payload fails its schema | Direct to `.dlt` with `MISSING_ATTRIBUTE` or `SCHEMA_INVALID` | None | AC13 |
| X9 | Another event type, or a decision record without a case | Committed and ignored | None | AC14, AC15 |
| X10 | `rwb.dataengine.ledger-events` is off | Consumers paused; no append; processed after the flag is on | None | AC19 |

X1, X2, X4, X5 and X6 are the exception paths of RWB-E1-067 carried onto the split.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published RWB-P1-E1067-CON baseline and the writer of RWB-P1-E1066-APP from Day 1, and against the platform libraries it holds in H; it needs no other service to be built |
| Negotiable | The map is configuration and the contract of RWB-P1-E1067-CON; the story fixes the listener, the duplicate rule, the order and the failure path |
| Valuable | The case owner sees every Workbench action in the case history, with its source and its actor |
| Estimable | One listener, one mapper, one configuration table, one incident and the fixtures of the six events |
| Small | Fits one sprint with its tests |
| Testable | Each criterion publishes a synthetic event to a fixture and reads the ledger through the writer's read path |

### 7. Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger

  Background:
    Given case "RW-2026-000301" exists with no ledger entries
    Given the ledger listener runs as the service identity of rwb-source-data

  Scenario: AC2 The entry names its source (legacy RWB-E1-067 AC2)
    Given a CaseAllocated fixture with `ce_actor=SERVICE:rwb-case` and a CaseTransferred fixture with `ce_actor=USER:u-teammgr-03` for the case
    When both are processed
    Then the CASE_ALLOCATED entry has `sourceSystem` WORKBENCH, `sourceRef` "EV-02 CaseAllocated", `actorType` SERVICE and `actorRef` "rwb-case"
    Then the CASE_TRANSFERRED entry has `sourceRef` "EV-04 CaseTransferred", `actorType` USER and `actorRef` "u-teammgr-03"
    Then each entry's `idempotencyKey` equals the message's `ce_idempotencykey` and `occurredAt` equals `ce_time`

  Scenario: AC4 An event with an unknown schema version (legacy RWB-E1-067 AC4)
    Given CaseTransferred is registered at version 1 only
    When the synthetic unregistered type `rwb.case.CaseTransferred.v9` arrives for case "RW-2026-000301"
    Then no entry and no inbox row are written and the writer is not called
    Then the record is on `rwb.case.events.v1.dlt` with `rwb-dlt-reason=UNSUPPORTED_VERSION`, `rwb-dlt-consumer=rwb-source-data` and `rwb-dlt-owner=P1 squad`
    Then no retry topic is used and the offset is committed

  Scenario: AC6 Entries follow the order the events were written (legacy RWB-E1-067 AC6)
    Given CaseCreated with `ce_time` 06:10 and CaseAllocated with `ce_time` 06:40 (+07:00) for the case
    When the first append of CaseCreated fails once and CaseAllocated is processed before its retry
    Then both entries exist, CASE_ALLOCATED has case_seq 1 and CASE_CREATED has case_seq 2
    Then the ledger read returns CASE_CREATED before CASE_ALLOCATED, ordered by `occurredAt` then `caseSeq`

  Scenario: AC7 The same event on two threads at once (legacy RWB-E1-067 AC7)
    Given CaseCreated for case "RW-2026-000301" is delivered to two consumer threads at the same moment
    When both threads process it
    Then one CASE_CREATED entry exists
    Then the `processed_event` row for `ce_id` has `hit_count=2` and an updated `last_seen_at`

  Scenario: AC8 An event for a case that does not exist (legacy RWB-E1-067 AC8)
    Given the case contract answers 404 for case ID "00000000-0000-0000-0000-000000000998"
    When DocumentStored arrives for that case ID
    Then no ledger entry is written
    Then the event is not discarded and the processing is visible in the consumer log with the case ID and no payload value
    # Pending: parked reason value, and whether it is retried or parked at once; owner solution architect; NEW-GAP-S8-11.

  Scenario: AC9 The ledger write is refused on every attempt and the event is parked (new, D-RCV-60)
    Given every ledger insert of the CaseCreated entry of case "RW-2026-000301" fails with a database error
    When the event is delivered and retried through the 1 min, 10 min and 1 h topics
    Then 4 attempts are made and the event goes to `rwb.case.events.v1.dlt` with `rwb-dlt-reason=RETRIES_EXHAUSTED`, `rwb-dlt-consumer=rwb-source-data` and `rwb-dlt-owner=P1 squad`
    Then one dead-letter alert and one `LEDGER_WRITE_FAILED` incident with MSG-P1-022 in its detail are raised
    Then no entry and no decision record are written

  Scenario: AC10 A case read timeout moves the event to the retry topic (new, D-RCV-60)
    Given the case contract does not answer within 2 s for the CaseCreated event of case "RW-2026-000301"
    When the listener processes the event
    Then the event is published to the 1 min retry topic and only then is the offset of the owner topic committed
    Then no entry and no inbox row remain from the failed attempt

  Scenario: AC11 An event payload carries references and codes only (new, D-RCV-60)
    Given a CaseAllocated fixture of case "RW-2026-000301" with an extra synthetic property "customerName"
    When the listener processes it
    Then the writer request carries no value of that property
    Then logs, retry and dead-letter headers and incident detail contain neither the property name nor its value

  Scenario: AC12 The six rows map the registered events (new, RD-P1-009)
    Given one fixture for each row in section 12.4
    When the listener maps each fixture
    Then the six `eventCode` values match the map rows
    Then row 06 uses `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and maps `data.entryId` to `decisionLogId`
    Then only DECISION_TAKEN carries `decisionLogId`, and `approver`, `summary`, `channel` and `direction` stay empty
    Then `sourceRef` values are the six literals in section 12.4
    # TC-P1-E1067-APP-01

  Scenario: AC13 Required envelope fields are parked when absent (new, RD-P1-009)
    Given an event without `ce_actor` or `ce_idempotencykey`
    When the listener receives it
    Then no append is made and the event is sent directly to `<topic>.dlt` with `rwb-dlt-reason=MISSING_ATTRIBUTE`
    # TC-P1-E1067-APP-02

  Scenario: AC14 Other event types are committed and ignored (new, RD-P1-009)
    Given `CaseStateChanged` on `rwb.case.events.v1`
    When the listener receives it
    Then the offset is committed with no inbox row, append or parked record
    # TC-P1-E1067-APP-03

  Scenario: AC15 Decision records without a case are committed and ignored (new, RD-P1-009)
    Given a `rwb.decision.DecisionRecorded.v1` event without `data.caseId`
    When the listener receives it
    Then the offset is committed with no inbox row, append or parked record
    # TC-P1-E1067-APP-04

  Scenario: AC16 A redelivery after a committed append adds no entry (new, RD-P1-009)
    Given CaseAllocated was appended and its offset was not committed before the consumer stopped
    When the same message is delivered again
    Then one CASE_ALLOCATED entry exists and the `processed_event` row of its `ce_id` has `hit_count` 2

  Scenario: AC17 A business key already in the ledger adds no entry (new, RD-P1-009)
    Given rwb-case appended over REST with business key K
    When an event with `ce_id` new and `ce_idempotencykey` K is processed
    Then no new entry and no new caseSeq are created and the inbox row of the event is committed

  Scenario: AC18 A parked event is replayed once (new, RD-P1-009)
    Given an event parked with `RETRIES_EXHAUSTED` whose cause is removed
    When the platform replay tool replays it
    Then exactly one entry is added and earlier entries are unchanged

  Scenario: AC19 The intake flag pauses consumption (new, RD-P1-009)
    Given `rwb.dataengine.ledger-events` is off
    When CaseCreated is published
    Then no append is made and the consumer group does not advance
    When the flag is switched on
    Then the event is processed and one entry exists
```

**Target reading.** The legacy assertions keep their meaning; what changes is where they run. The outbox listener of the monolith becomes the Kafka consumer `LedgerEventListener` on the owner topics of section 12.4 (DP-09). The map is configuration and the contract of RWB-P1-E1067-CON, and the entry codes are LOV-LEDGER-EVENT (DP-07). The writer is `InteractionLedgerWriter` of RWB-P1-E1066-APP, called in process in the intake transaction (RD-P1-007), so no HTTP hop and no rights check of a user exist between listener and writer. Access: the listener provides no operation; the legacy access case (SY-AGENT calls the append, MSG-P4-002) is proved on the append in RWB-P1-E1066-APP AC10 and is not a criterion here. AC1, AC3 and AC5 are the intake contract criteria of RWB-P1-E1067-CON. The hit counts are held by `processed_event` (DP-09) and this story creates no table. An append writes no decision record, so the intake cannot loop. DL10 and DL11 are confirmed by the directive of 26 November 2026 (ASM-2250, ASM-2357, ASM-2377, ASM-2863, ASM-0553, ASM-0703, ASM-1051, ASM-1104).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen | REQ-ILG-005; EV-01, EV-02, EV-04, EV-19, EV-16, EV-08 (events.txt) |
| BR2 | Every entry names the system or person that produced it | REQ-ILG-002 |
| BR3 | The same event with the same key produces one entry, and the repeat is counted | R-UNI-40; REQ-ILG-007 |
| BR4 | `caseSeq` follows arrival; the ledger is read by `occurredAt` then `caseSeq`; the intake does not wait behind a failed event; no order across topics is promised | Events rule "Ordering" (events.txt); RD-P1-009 rule 7 |
| BR5 | A transient consumer failure retries, then parks to the `<topic>.dlt` with its owner; a non-retryable record parks at once | Events rule "Failure" (events.txt); R-UNI-36; RD-P1-009 |
| BR6 | A consumer accepts the current and the previous schema version | Events rule "Versioning" (events.txt) |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt) |

**Where each rule lives in the target.** BR1 is the six-row intake map in E1067-CON. BR2 uses required `ce_actor`; its prefix before the first colon determines `actorType`, and the remainder is `actorRef`. BR3 uses `ce_id` to identify inbox deliveries; a repeat increments `processed_event.hit_count` and `last_seen_at`. The listener passes `ce_idempotencykey` as the permanent business key to the in-process writer. BR4 uses arrival order for `caseSeq`; the read interface orders by `occurredAt`, then `caseSeq`. The listener does not block later events behind a failed record and does not claim cross-topic ordering. BR5 retries transient failures after 1 min, 10 min and 1 h, then parks to `<topic>.dlt`; non-retryable envelope, version, schema and case-key failures go directly to the DLT. `LEDGER_WRITE_FAILED` with MSG-P1-022 is raised only by this intake after `RETRIES_EXHAUSTED`. BR6 accepts current and previous registered versions; the six current types are `.v1` only. BR7 reads only the properties listed in each map row and no personal fields.

### 9. State transitions

None. This story does not change a case status. It adds ledger entries and moves a failed or unreadable event to the `<topic>.dlt` topic with RD-P1-009 headers for the platform team (R-UNI-36).

| From | Event | Condition | To |
|---|---|---|---|
| an event on the topic, unprocessed | the consumer delivers it to `LedgerEventListener` | The version is current or previous and the attributes are present | The inbox row and the entry are committed together, then the offset |
| an event with an unknown schema version | the version check | The version is neither current nor previous | The event is parked in the matching `<topic>.dlt` topic with the RD-P1-009 headers |
| an event of a case that does not exist | the append | The writer finds no case | No entry; handling pending (NEW-GAP-S8-11) |
| an event whose write fails transiently | the retry topics | The third retry fails | The event is on `<topic>.dlt` with `RETRIES_EXHAUSTED`; `LEDGER_WRITE_FAILED` is raised |
| a parked event | the platform administrator replays it | The cause is removed | The event is delivered again and the duplicate rule keeps one entry |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Service identity of rwb-source-data | Runs the ledger listener on the service worker and calls the writer in process (DP-09; RD-P1-007) |
| Producer identities of rwb-case, rwb-document and the decision-record library | Appear as actors on the entries; they never call the append |
| rwb-agent (P10) | May not append (legacy Case record R) |
| RW-PLATADM, platform administrator | Receives the dead-letter alert and the incident and runs the replay tool; the P1 squad, named in `rwb-dlt-owner`, fixes the cause (Observability and Monitoring Design v6) |
| RW-CASEOWN, case owner | Reads the entries through the case timeline of rwb-case, which reads the ledger through this service's contract |
| No approval level from the delegation of authority applies | The story takes no business decision |

The login behind the write is the `rwb_source_data` login of the target (DP-02; Architecture v5 slide 29), and the grants it holds are delivered by the DB story of this service. This story writes no grant statement and holds no credential of its own.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, through `InteractionLedgerWriter` of RWB-P1-E1066-APP |
| DF-INT-014 | interaction | `eventCode` | Write |
| DF-INT-015 | interaction | `actorType` | Write |
| DF-INT-016 | interaction | `actorRef` | Write |
| DF-INT-017 | interaction | `sourceRef` | Write |
| DF-INT-018 | interaction | `idempotencyKey` | Write |
| DF-INT-019 | interaction | `caseSeq` | Write, assigned by the writer |
| DF-INT-020 | interaction | `decisionLogId` | Write, for DECISION_TAKEN only |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write, by the inbox of RWB-PLT-TE006-CON |

The field names used here and in section 12 are those of the `Interaction` schema of rwb-source-data.yaml 5.1.0 (API Specification v7); the physical column names of the table are RWB-P1-E1066-CON's. Record IDs of assignments, documents and decisions are read from the event payload, not from their tables: this story reads no row of `recovery_case`, `assignment`, `document` or `decision_log_entry`, and the case-existence check is the writer's. `documentId` (row 05) has no column in Physical Schema v9 (NEW-GAP-S8-12). The listener sets no `correctsEntryId`, because none of the six consumed types is a correction; that field belongs to the correction path of the writer's contract. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation: it is the consumer side of the intake, and the read and append operations of the ledger are RWB-P1-E1066-APP's.

#### 12.2 REST operations consumed

None across a service boundary by the listener. It calls `InteractionLedgerWriter` of RWB-P1-E1066-APP in process, in the same transaction as the inbox row. The values it sets are `caseId`, `eventCode`, `occurredAt`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey` and the row-specific holder, document and decision references; the writer assigns `caseSeq` and `sourceSystem` WORKBENCH. The writer's own case read of rwb-case runs inside that call (2 s).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON (RD-P1-022). This story publishes no event and writes no outbox row of its own: it is a consumer only.

#### 12.4 Events consumed

| Row | `ce_type` | Topic | `eventCode` | `sourceRef` | Payload fields read / extra mapping |
|---|---|---|---|---|---|
| 01 | `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | CASE_CREATED | `EV-01 CaseCreated` | `data.caseId` required |
| 02 | `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | CASE_ALLOCATED | `EV-02 CaseAllocated` | `data.caseId`; `toHolderRef` = `USER:` + `data.ownerId` |
| 03 | `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | CASE_TRANSFERRED | `EV-04 CaseTransferred` | `data.caseId`; `fromHolderRef` = `USER:` + `data.fromOwner`; `toHolderRef` = `USER:` + `data.toOwner` |
| 04 | `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | CASE_ESCALATED | `EV-19 TimerBreached` | `data.caseId` required |
| 05 | `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | DOCUMENT_ATTACHED | `EV-16 DocumentStored` | `data.caseId`; `documentId` = `data.documentId` |
| 06 | `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | DECISION_TAKEN | `EV-08 DecisionRecorded` | `data.caseId`; `decisionLogId` = `data.entryId`; `approver` not read |

Row 06 turns every decision record with `data.caseId` into an entry. Reads (case record, data product, customer and authorise checks) are written to the access log only and publish no DecisionRecorded, so only decisions under DP-03 reach row 06 (RD-P1-072). For every row: `sourceSystem=WORKBENCH`, `occurredAt=ce_time`, `caseId=data.caseId`, `idempotencyKey=ce_idempotencykey`; `actorType` is the prefix of `ce_actor` before the first colon and `actorRef` is the remainder. `ce_idempotencykey` is the business key (at most 120); `ce_actor` is `USER:<userId>` | `SERVICE:<service name>` | `PARTNER:<partnerCode>` (at most 74), and `actorRef` is at most 64. The document producer and decision-record library add both required headers. No personal field is read; `summary`, `channel` and `direction` stay empty. There is no routing on `ce_source`.

Any other `ce_type` on these topics is committed and ignored, with no inbox row or entry. A row-06 event without `data.caseId` is committed and ignored. Missing `data.caseId` on rows 01 to 05 goes directly to `<topic>.dlt`.

The version is the `.vN` suffix of `ce_type` and registry subject. The intake accepts the current and previous registered versions; all six types currently use `.v1` only. Refusal fixtures use an unregistered synthetic type such as `rwb.case.CaseTransferred.v9`. One consumer group per owner topic uses the working ID `rwb-source-data.<topic>` (NEW-ASM-A2) and is deployed by RWB-P1-E1066-OPS. No group consumes `rwb.source-data.events.v1`.

Transient database and case-read-timeout failures retry after 1 min, 10 min and 1 h, then park to `<topic>.dlt`. Missing `ce_actor` or `ce_idempotencykey`, unsupported version, missing `data.caseId` on rows 01 to 05 and schema-invalid payloads go directly to `.dlt`. Each parked record preserves the original message and `ce_*` headers and adds `rwb-dlt-reason` (`MISSING_ATTRIBUTE` | `UNSUPPORTED_VERSION` | `SCHEMA_INVALID` | `RETRIES_EXHAUSTED`), `rwb-dlt-consumer=rwb-source-data`, and `rwb-dlt-owner=P1 squad`. One alert is raised per parked record. `LEDGER_WRITE_FAILED` with MSG-P1-022 is raised only for `RETRIES_EXHAUSTED`; the REST writer never raises it for intake calls. Replay uses the platform replay tool.

#### 12.5 Workflows and activities

None. The listener is a Kafka consumer on the service worker, not a Temporal workflow or activity, and it starts none. The task queue `rwb-source-data` in namespace `rwb-recovery` is the service's queue; the workflows `AceIngestCheck` and `reconciliation` and the activities `listEligibleAccounts` and `snapshot(page)` of Architecture v5 slide 15 belong to other P1 stories.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the listener is driven by the topic, and the outbox relay of the producers is JOB-11 of the owning service (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data (DP-01, DP-18) | Written through the append of RWB-P1-E1066-APP; this story creates no column and no index of it |
| `processed_event` | `rwb_source_data` | PLT library object created in this service's schema (DP-09; Ownership Map) | Read and written by the inbox of RWB-PLT-TE006-CON for the hit count; created on the per-service Flyway sequence (DP-15) |

**This story adds no table.** The legacy story created `processed_event` in its own Flyway migration; in the target that table is the PLT inbox, created in `rwb_source_data` by the library migration on the service's own sequence, and the hit count is read from it. No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| `rwb-case` event fixtures (four) | `rwb.case.events.v1` | CaseCreated, CaseAllocated, CaseTransferred and TimerBreached at `.v1`, with `ce_idempotencykey` and `ce_actor`, a synthetic unregistered `CaseTransferred.v9`, and fixtures without a required attribute |
| `rwb-document` event fixture | `rwb.document.events.v1` | DocumentStored for case "RW-2026-000301" and for an unknown case ID, with `data.documentId` and both envelope attributes |
| `rwb-decision-record` event fixture | `rwb.decision-record.v1` | `rwb.decision.DecisionRecorded.v1` with `data.entryId`, with and without `data.caseId`, and both envelope attributes |
| Writer stub | `InteractionLedgerWriter` of RWB-P1-E1066-APP | Appended; business key already stored (no entry); case not found; database failure; case read timeout |
| Inbox fixture | `processed_event` in `rwb_source_data` | A first row with `hit_count` 1 and a redelivery with `hit_count` 2 and `last_seen_at` set |

The six event fixtures are the fixtures of RWB-P1-E1067-CON, and a fixture that drifts from the map fails the contract test. Every fixture is synthetic, and no production payload is copied into one.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None across a service boundary by the listener | The writer's case read is made inside `InteractionLedgerWriter` (2 s, DP-11) |
| Kafka | None | 6 event types on 3 topics | CloudEvents 1.0, key caseId, inbox dedupe, retry topics and `.dlt` (DP-09) |
| Temporal | None | None | The consumer is not a workflow or an activity |
| File | None | None | No file in this story |
| SQL | None | `interaction` and `processed_event`, both in `rwb_source_data` | Written through the writer and the inbox library; no read of another service's table (DP-01) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `ledger`, with the configuration reader and the consumer in `...sourcedata.ledger` and the published types taken from the writer's contract in `...sourcedata.ledger.api`. Service base `/api/recovery/source-data/v1` (not provided here), schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | In-process writer call; the writer's one hop to rwb-case, 2 s timeout | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 and DP-18 are this story's own patterns: the ledger is P1's and the listener writes it in P1's schema. DP-03 is used, not delivered: the DECISION_TAKEN entry takes `data.entryId` as `decisionLogId` from the shared decision-record event, and this story writes no decision record. DP-07 is used for the entry codes, read as LOV-LEDGER-EVENT. DP-09 is the consumer side of the platform library: the inbox, the envelope, the retry topics and the `.dlt`. DP-11 applies to the writer's case read; the writer itself is called in process (RD-P1-007). DP-15 is the per-service sequence the inbox objects arrive on, and this story adds no migration. DP-19 applies to the case timeline that shows the entries, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LedgerEventListener` | Consumer | Subscribes to the three owner topics, filters the six types, checks the version and attributes, runs the inbox and writer transaction, then commits the offset |
| `LedgerEventMapper` | Service | Event to interaction request per the map row, read from configuration and cross-checked against LOV-LEDGER-EVENT; sets the actor, the source reference and the idempotency key |
| `LedgerMapRepository` | Repository | Reads the versioned map of RWB-P1-E1067-CON; one row per event type |
| `LedgerIntakeService` | Service | One transaction: inbox row by `ce_id` and the in-process `InteractionLedgerWriter` call; no retry of its own (the retry topics retry) |
| `LedgerFailureHandler` | Service | Publishes to the retry topics or `<topic>.dlt` with the three `rwb-dlt-*` headers; raises `LEDGER_WRITE_FAILED` for `RETRIES_EXHAUSTED` only; writes no entry for a parked event |
| `LedgerIntakeContractTest` | Test | Compares the six fixtures with the map and fails on drift |

**Migrations and sequence (DP-15).** This story adds no table and no version of its own. The inbox `processed_event` and the idempotency table arrive as the PLT library objects created in `rwb_source_data` on the service's per-service Flyway sequence, and the ledger table `interaction` arrives with RWB-P1-E1066-APP. An applied version is never edited; a correction is a new version.

**Configuration and reference data**

- The event-to-entry map is configuration, one row per event type: the event type, the topic, the entry event code, the actor source, the payload fields read, the accepted schema versions and the source-reference form. It is the contract of RWB-P1-E1067-CON.
- The entry codes are read as LOV-LEDGER-EVENT from the reference-data contract of rwb-case (DP-07); a code that the list does not carry fails the contract test. LOV-LEDGER-EVENT is a closed list (Reference Data and Lists of Values), matched by the `eventCode` enum of rwb-source-data.yaml; a new code is a change to the list and to that contract, not a data row alone.
- The retry topics are 1 min, 10 min and 1 h from the outbox and inbox settings of the platform library, then `.dlt` (NFR-026; DL11; RD-P1-009).
- The DLT consumer and owner headers are `rwb-source-data` and `P1 squad`.
- No business value is written in code: the map, the retry limit, the owner and the accepted versions are configuration and reference data.

**Build steps**

1. `LedgerMapRepository` and the versioned map, with the six rows of section 12.4 and the cross-check against LOV-LEDGER-EVENT (AC2).
2. `LedgerEventMapper` with the actor, the source reference form and the idempotency key of the envelope (AC2).
3. `LedgerEventListener` on the three owner topics, with the type filter, version and attribute checks of the flow (AC4, AC13 to AC15).
4. `LedgerIntakeService` against the writer stub and the inbox, with the redelivery, two-thread and business-key cases (AC7, AC16, AC17).
5. The order path: arrival `caseSeq` and the read order of AC6.
6. `LedgerFailureHandler`: retry topics, `.dlt` headers, alert and incident, replay (AC8 to AC10, AC18); the flag pause (AC19).
7. `LedgerIntakeContractTest` over the six fixtures and the map; a drift fails the build (AC4, AC6).
8. Tests for AC2, AC4 and AC6 to AC19 with the fixtures of 12.8, and the regression rows of section 16.

**Feature flag.** `rwb.dataengine.ledger-events`, kept as the legacy key and held by the platform flag library. Off, the three consumer groups are paused; on, they resume from the committed offset. First start uses `auto.offset.reset=earliest`; events older than the 7-day topic retention are recovered only from `.dlt` (RD-P1-009 rule 8).

**Done when.** The tests of section 16 pass, each of the six event types is consumed in SIT, a redelivered event leaves one entry and a hit count of 2, and no offset is committed before the entry is written or the event is on a retry or dead-letter topic.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | Detail of the `LEDGER_WRITE_FAILED` incident after `RETRIES_EXHAUSTED` | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| `rwb-dlt-reason` values | Header of a parked record | `MISSING_ATTRIBUTE`, `UNSUPPORTED_VERSION`, `SCHEMA_INVALID`, `RETRIES_EXHAUSTED`; a value for case not found is pending (NEW-GAP-S8-11) |
| `LEDGER_WRITE_FAILED` | Retries exhausted | Incident code |

The reason values and the incident code are operational metadata, not API message fields. The intake shows no user message.

### 15. Screens and states

No screen in this story (DP-19). A parked event is a record on `<topic>.dlt`, not an item of the exception queue screen; the platform administrator sees the dead-letter alert and the service dashboard and runs the replay tool (Observability and Monitoring Design v6). The case owner reads the entries through the case timeline of rwb-case (`GET /cases/{caseId}/interactions`), whose screen and route are the screen owner's (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-02 | AC2, BR2 | End to end | CASE_ALLOCATED and CASE_TRANSFERRED fixtures |
| TC-E1-067-04 | AC4, BR6 | End to end | Unregistered synthetic `rwb.case.CaseTransferred.v9` |
| TC-E1-067-06 | AC6, BR4 | End to end | Ledger read by `occurredAt` then `caseSeq` after one retry |
| TC-E1-067-07 | AC7, BR3 | End to end | One event on two consumer threads; hit count 2 |
| TC-E1-067-08 | AC8 | End to end | DocumentStored for an unknown case ID |
| TC-E1-067-11 | AC9, BR5 | End to end | Database failure through the three retry topics to `.dlt` |
| TC-E1-067-12 | AC10, BR5 | End to end | Case read timeout; retry topic before commit |
| TC-E1-067-13 | AC11, BR7 | End to end | Extra synthetic property is not copied |
| TC-P1-E1067-APP-01 | AC12 | Component | The six map rows |
| TC-P1-E1067-APP-02 | AC13 | Component | Missing envelope attributes |
| TC-P1-E1067-APP-03 | AC14 | Component | Other event types ignored |
| TC-P1-E1067-APP-04 | AC15 | Component | Decision record without a case |
| TC-P1-E1067-APP-05 to TC-P1-E1067-APP-08 | AC16 to AC19 | Component | Redelivery, business-key duplicate, replay, flag pause |
| TC-E1-067-10 | ASM-3438 | Component | Tables of section 12.7; no column or index added |

TC-E1-067-01, -03 and -05 are the intake contract cases of RWB-P1-E1067-CON (its AC1, AC3, AC5); TC-E1-067-09 is the access check of the append and belongs with RWB-P1-E1066-APP AC10. The retry limit of the JOB-11 outbox relay is not used by the intake.

### 17. Guardrails

- No business value in code: the map, the entry codes, the retry intervals, the accepted versions and the `.dlt` owner are configuration and reference data (DP-07).
- No personal data in logs, tests, events or prompts: the six consumed types carry IDs and codes only, the map reads no personal field, and every fixture is synthetic (BR7).
- No read of another service's tables: the case reference, the document reference and the decision reference come from the payload, and the case-existence check is the writer's (DP-01).
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all (DP-05 is not used here).
- The listener never commits an offset for an event it has not written, ignored by rule, or published to a retry or dead-letter topic.
- The writer's case read is one hop of 2 s; a slow or failed read sends the event to the next retry topic and never half-writes an entry (DP-11).
- The tables it relies on are library objects or the writer's; this story creates none, and an applied migration is never edited (DP-15).
- No screen is served here; the timeline is the gateway-bff composite route and the screen owner's (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-36 | TC-P1-E1067-APP-01, TC-E1-067-04, TC-E1-067-06, TC-E1-067-08, TC-E1-067-11 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-067-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-04 | All recovery processes | R-UNI-40 | TC-E1-067-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1067-CON | Contract | H build dependency: the intake map, the six event fixtures and the writer stub of section 12.8 |
| RWB-P1-E1066-APP | App development | H build dependency: the ledger table, the case sequence and `InteractionLedgerWriter` this listener calls |
| RWB-P1-E1066-OPS | DevOps | External: declares the three intake consumer groups |
| RWB-P1-E1066-CON | Contract | Sibling of the same legacy key: the append contract whose request this listener fills and whose path is not restated here |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library that publishes `DecisionRecorded` (DP-03) |
| RWB-PLT-E1043-CON | Contract | H: the reference-data library that carries LOV-LEDGER-EVENT (DP-07) |
| RWB-PLT-TE006-CON | Contract | H: the outbox and inbox library, the CloudEvents envelope, the retry topics and the `.dlt` (DP-09) |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence on which the inbox objects arrive (DP-15) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route; this story serves no screen behind it (DP-19) |
| RWB-P3-E1043-CON | Contract | C: the rwb-case reference-data contract the entry codes are read from |
| The rwb-case producer stories for case creation, allocation, transfer and timers | App development | Producers of four of the six consumed types; no build dependency, their fixtures stand in for them |
| The rwb-document producer story for document storage, and the rwb-decision decision-record library | App development, Contract | Producers of the remaining two consumed types; the fixtures stand in for them |

### 19. Out of scope

- The ledger store, the writer, the case sequence, LOV-LEDGER-EVENT and the append operation: RWB-P1-E1066-APP and RWB-P1-E1066-CON.
- The inbox, the idempotency table and the retry and dead-letter topics of the platform: RWB-PLT-TE006-CON (DP-09).
- The contract of the intake, the versioned map and the six event fixtures: RWB-P1-E1067-CON.
- The six producers and their event payloads: their own service stories; this story consumes them and changes none of them.
- The read path of the ledger, the case timeline and its screen: rwb-case and the screen owner through the gateway-bff composite route (DP-19).
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).
- Any table of this story: it creates none, and the two tables it uses are another story's or the library's.

### Remaining delivery steps

- Size the story at refinement; owner: squad.
- Obtain epic design sign-off; owner: product owner.
- Publish the contract and matching fake; owner: contract owner.
- Rule the intake handling of non-transient writer refusals; owner solution architect; NEW-GAP-S8-11.
- Obtain the document and decision-record header additions from their producers; owner contract owner.
- Add or update story tests in Test Cases v9 (W2-tests); owner: test writer.
- Run the required test data in DEV after implementation; owner: delivery team.
