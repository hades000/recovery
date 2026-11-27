# RWB-P1-E1067-APP Every Workbench action into the interaction ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P1-P |
| Ready to start | After RWB-P1-E1066-APP |
| Depends on (build) | RWB-P1-E1067-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1066-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-067 for rwb-source-data. The outbox listener of the monolith becomes the ledger listener of rwb-source-data, a Kafka consumer on the service's own worker that reads the owner topics of six facts; the event-to-entry map moves to configuration and to the contract of RWB-P1-E1067-CON; the in-process `InteractionLedgerWriter` becomes the append of RWB-P1-E1066-APP over its REST contract (DP-11); the case-existence check is the writer's, not the listener's; the inbox `processed_event` and the idempotency table are PLT library objects created in `rwb_source_data` (DP-09); the ledger table is P1's (DP-01, DP-18); LOV-LEDGER-EVENT comes from rwb-case (DP-07); the decision record is written locally through the decision-record library (DP-03); the schema migration is on the per-service sequence (DP-15); no screen is served here (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1067-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

This is the listener slice of legacy RWB-E1-067 in rwb-source-data. It owns:

- `LedgerEventListener`, the consumer of the six owner topics on the service's own worker, in the consumer group of the service; its inbox rows, retry topics and dead-letter topic are the platform ones (DP-09; Architecture v5 slides 11 and 41);
- the event-to-entry map as configuration and as the contract of RWB-P1-E1067-CON, which turns EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-19 TimerBreached, EV-16 DocumentStored and EV-08 DecisionRecorded into the entry codes CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED and DECISION_TAKEN;
- the schema-version acceptance of the legacy listener (current and previous), the duplicate rule and the per-case order, applied around the append;
- the call to the append operation of the interaction ledger writer of RWB-P1-E1066-APP, which is now a REST append in the same service (DP-11) and holds the case-existence check and the write of the entry;
- the incident `LEDGER_WRITE_FAILED` and the parking of a failed or unknown event in the exception queue with owner RW-PLATADM.

It does not own the ledger table `interaction`, the writer, the case sequence or the list LOV-LEDGER-EVENT: those are RWB-P1-E1066-APP and RWB-P1-E1066-CON. It does not own the inbox and idempotency tables: `processed_event` and `idempotency_key` are PLT library objects created in `rwb_source_data` (DP-09; Ownership Map). It creates no table of its own and reads no table of another service (DP-01). It serves no screen (DP-19).

### 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. Each owner service writes its state change and its outbox row in one transaction, and its relay publishes the event to its own topic keyed by the case ID (DP-09; Architecture v5 slides 11 and 42). rwb-source-data consumes those six facts and appends one entry per fact, so the case owner sees the customer contacts and what the Workbench did between them, with the source and the actor of each action.

In the target the ledger is a capability of one service instead of a table of the monolith: the ledger and its intake rule are rwb-source-data's (DP-18; Template and Rules §R3 default ruling), the table `interaction` sits in `rwb_source_data` (DP-01), and the other eighteen services reach it through this service's contract and never through its table. Delivery is at least once, so the listener accepts the current and the previous schema version, keeps the order of one case on the case key, and passes the CloudEvents id as the idempotency key, so a repeat increments the hit count of the inbox row instead of writing a second entry (R-UNI-40; DP-09). A failed or unreadable event is never acknowledged and never discarded: it is parked with its reason and its owner (R-UNI-36; NFR-026).

Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007; applies DP-01, DP-03, DP-07, DP-09, DP-11, DP-15, DP-18 and DP-19. The measure is one ledger entry per published fact, read back inside the user wait (NFR-070).

### 3. Preconditions

- RWB-P1-E1066-APP is done: the ledger table `interaction`, the case sequence, the append operation, the duplicate rule on `idempotency_key` and LOV-LEDGER-EVENT are in place (DP-01, DP-07, DP-18).
- RWB-P1-E1067-CON is published: the intake map, the six event fixtures and the writer stub of section 12.8, so the listener is written against a fixed contract from Day 1 (DP-11).
- RWB-PLT-TE006-CON is on the classpath: the outbox and inbox library with `processed_event` and `idempotency_key` created in `rwb_source_data`, the CloudEvents 1.0 envelope, the retry topics and the `.dlt` topic (DP-09; Architecture v5 slide 11).
- RWB-PLT-E1027-CON is on the classpath: the local decision-record library that publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, the sixth consumed type (DP-03).
- RWB-PLT-E1043-CON is on the classpath and RWB-P3-E1043-CON is published with its fake, so the entry codes are read as LOV-LEDGER-EVENT from the reference-data contract and never written in code (DP-07).
- RWB-PLT-E1044-CON is in place: the per-service Flyway sequence of rwb-source-data, on which the library migrations of the inbox arrive (DP-15).
- RWB-PLT-N001-CON exists for the gateway-bff composite route; this story serves no screen and adds no route to it (DP-19).
- The six producers publish their facts with the header and the payload of events.txt: event ID, idempotency key, schema version, occurred time and actor in the envelope, and IDs and codes only in the payload (legacy RWB-E1-067 §3; Architecture v5 slides 42 and 43 notes).
- The event type names the intake consumes are fixed by the Arch v5 event catalogue: `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1` and `rwb.case.TimerBreached.v1` on `rwb.case.events.v1` (P3), `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` (P5) and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` (P7).
- The catalogue does not name rwb-source-data as a consumer of the document fact or of the timer fact, and the legacy names EV-16 DocumentStored and EV-19 TimerBreached are not the two CloudEvents types the intake reads: the mapping of those two facts onto `rwb.document.DocumentStored.v1` and `rwb.case.TimerBreached.v1` is Not specified in the source documents (GAP-0507; ASM-0699). This story reads them that way, as rows 16 and 19 of the Architecture v5 event catalogue, and RWB-P1-E1067-CON fixes both in the map.

### 4. Flow

1. Owner service: commits its change and its outbox row in one transaction; its relay publishes the event to the owner topic with the case ID as the key (DP-09; Architecture v5 slide 11).
2. rwb-source-data: the consumer group of the service delivers the event to `LedgerEventListener`; deliveries of one case keep the order they were written in, because the key is the case ID (BR4).
3. `LedgerEventListener`: checks the schema version of the event against the map; the current and the previous version are accepted, anything else is parked (BR6; X2).
4. `LedgerEventMapper`: maps the event type to the entry event code from the map of RWB-P1-E1067-CON, read as configuration and cross-checked against LOV-LEDGER-EVENT of rwb-case (DP-07): CaseCreated to CASE_CREATED, CaseAllocated to CASE_ALLOCATED, CaseTransferred to CASE_TRANSFERRED, TimerBreached to CASE_ESCALATED, DocumentStored to DOCUMENT_ATTACHED and DecisionRecorded to DECISION_TAKEN with `decisionLogId` (BR1).
5. `LedgerEventMapper`: sets `actorType` and `actorRef` from the CloudEvents envelope (a user ID or a service identity code), `sourceRef` as the owning module and the event type in the legacy form, and `idempotencyKey` as the CloudEvents id (BR2, BR3).
6. `LedgerEventListener`: calls the append of RWB-P1-E1066-APP once with the interaction request; the writer checks that the case exists and assigns the next `caseSeq` (DP-11; legacy X6).
7. rwb-source-data: when the idempotency key already exists, no entry is written and the inbox row `processed_event` of `rwb_source_data` adds 1 to the hit count of that key (R-UNI-40; DP-09).
8. `LedgerEventListener`: acknowledges the offset only after the entry is written or the event is parked, so a crash redelivers the event and the duplicate rule keeps one entry (BR5).
9. On failure: the broker retries through the retry topics of 1 min, 10 min and 1 h; after the retry limit of three the event goes to the `.dlt` topic and to the exception queue with owner RW-PLATADM, and incident `LEDGER_WRITE_FAILED` is raised with MSG-P1-022 (NFR-026; legacy X3).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same key | One entry; the repeat is counted in the inbox hit count | None | AC7 |
| X2 | An event with a schema version that is neither current nor previous | Not written; moved to the exception queue with owner RW-PLATADM | None (exception queue item) | AC4 |
| X3 | The ledger write fails | Retried three times, then the `.dlt` topic and an incident; the event is not discarded | MSG-P1-022 (incident detail) | Section 12.9 |
| X4 | Events for one case arrive in written order | Entries follow that order in `caseSeq` | None | AC6 |
| X5 | The same event reaches two consumer threads at once | One entry; one hit counted | None | AC7 |
| X6 | An event names a case that does not exist | Not written; moved to the exception queue with reason "case not found" | None (exception queue item) | AC8 |
| X7 | The append does not answer, or answers a failure | The offset is not acknowledged and the entry is not counted as written; the delivery is retried | MSG-P1-022 on the last attempt | Section 12.7 |

X1, X2, X4, X5 and X6 are the exception paths of RWB-E1-067 carried onto the split. X3 and X7 are the same path seen from the two sides of the append: the writer's refusal and the listener's acknowledgement rule.

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
    Given the CASE_ALLOCATED entry of case "RW-2026-000301"
    When it is read
    Then it names source system "WORKBENCH", source reference "P3 case and workflow, EV-02 CaseAllocated" and actor "SY-RULES"
    Then the CASE_TRANSFERRED entry names actor type "USER" and actor "u-teammgr-03"

  Scenario: AC4 An event with an unknown schema version (legacy RWB-E1-067 AC4)
    Given CaseTransferred is at schema version 2 and accepts version 1
    When a CaseTransferred event with schema version 3 arrives for case "RW-2026-000301"
    Then the system writes no entry
    Then the event is in the exception queue with owner RW-PLATADM and reason "schema version 3 not accepted"

  Scenario: AC6 Entries follow the order the events were written (legacy RWB-E1-067 AC6)
    Given CaseCreated and CaseAllocated for case "RW-2026-000301" are written to the outbox in that order
    When both are processed
    Then CASE_CREATED has case_seq 1 and CASE_ALLOCATED has case_seq 2

  Scenario: AC7 The same event on two threads at once (legacy RWB-E1-067 AC7)
    Given CaseCreated for case "RW-2026-000301" is delivered to two consumer threads at the same moment
    When both threads process it
    Then one CASE_CREATED entry exists
    Then the hit count for its key is 1

  Scenario: AC8 An event for a case that does not exist (legacy RWB-E1-067 AC8)
    When DocumentStored arrives for case ID "00000000-0000-0000-0000-000000000998"
    Then the system writes no entry
    Then the event is in the exception queue with reason "case not found"
```

**Target reading.** Every assertion above keeps its legacy wording; what changes is where it runs. The outbox listener of the monolith becomes a Kafka consumer of rwb-source-data on the service's own worker, `LedgerEventListener`, subscribing to the owner topics of section 12.4 instead of to the internal outbox (DP-09). The event-to-entry map of the legacy flow becomes configuration and the contract of RWB-P1-E1067-CON, and the entry codes are read as LOV-LEDGER-EVENT from rwb-case (DP-07). The in-process `InteractionLedgerWriter` of RWB-E1-066 becomes the REST append of RWB-P1-E1066-APP (DP-11, DP-18), so the case-existence check behind AC8 is the writer's and the listener adds no mock and no second query: the `Given` of a case that exists is the writer's own answer. The hit counts of AC7 are held by the PLT inbox row `processed_event` created in `rwb_source_data` (DP-09), and no table is created by this story. The ledger table stays P1's (DP-01), the decision entry behind `decisionLogId` is written locally through the decision-record library (DP-03), and the sequence of the schema objects that make this work is the per-service one (DP-15). No criterion here adds, drops or rewords a line, and no contract-mock `Given` is needed, because the one call the listener makes is the same service's writer.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen | REQ-ILG-005; EV-01, EV-02, EV-04, EV-19, EV-16, EV-08 (events.txt) |
| BR2 | Every entry names the system or person that produced it | REQ-ILG-002 |
| BR3 | The same event with the same key produces one entry, and the repeat is counted | R-UNI-40; REQ-ILG-007 |
| BR4 | Events for one case are processed in the order they were written | Events rule "Ordering" (events.txt) |
| BR5 | A consumer failure retries, then goes to the exception queue with its owner | Events rule "Failure" (events.txt); R-UNI-36 |
| BR6 | A consumer accepts the current and the previous schema version | Events rule "Versioning" (events.txt) |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt) |

**Where each rule lives in the target.** BR1 is the map of RWB-P1-E1067-CON over the six owner topics: the facts are published by rwb-case, rwb-document and the decision-record library, and this service only consumes them, so a seventh fact is a map row and a contract change, not a code change. BR2 is the actor of the CloudEvents envelope, carried into `actorType` and `actorRef`; the listener never guesses an actor and never reads a user record. BR3 is the inbox row `processed_event` of `rwb_source_data` and the unique key on `interaction.idempotency_key`: the library owns the first (DP-09) and the writer of RWB-P1-E1066-APP owns the second. BR4 is the case ID as the Kafka key, one partition per case, plus the writer's gap-free `caseSeq`. BR5 is the retry topics and the `.dlt` topic of the platform, the exception queue with owner RW-PLATADM and the incident `LEDGER_WRITE_FAILED`; the listener never acknowledges an event it has not written or parked. BR6 is the schema registry with BACKWARD compatibility and the version check of step 3. BR7 is enforced twice: by the producers, which publish IDs and codes only, and by the map, which reads no field that carries personal data.

### 9. State transitions

None. This story does not change a case status. It adds ledger entries and moves a failed or unreadable event to the exception queue state EXCEPTION_QUEUE for the platform team (R-UNI-36).

| From | Event | Condition | To |
|---|---|---|---|
| an event on the topic, unprocessed | the consumer delivers it to `LedgerEventListener` | The schema version is current or previous and the case exists | The entry is appended and the offset of the inbox row is committed |
| an event with an unknown schema version | the version check | The version is neither current nor previous | The event is parked in the exception queue with owner RW-PLATADM |
| an event of a case that does not exist | the append | The writer answers "case not found" | The event is parked in the exception queue with its reason |
| an event whose append fails | the retry topics | The retry limit of three is reached | The event is on the `.dlt` topic and in the exception queue; incident `LEDGER_WRITE_FAILED` |
| a parked event | the platform administrator replays it | The cause is removed | The event is delivered again and the duplicate rule keeps one entry |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Service identity of rwb-source-data | Runs the ledger listener on the service worker and calls the append (DP-09, DP-11) |
| Producer identities of rwb-case, rwb-document and the decision-record library | Appear as actors on the entries; they never call the append |
| rwb-agent (P10) | May not append (legacy Case record R) |
| RW-PLATADM, platform administrator | Owns the exception queue items and the dead-letter alerts of the listener; receives the incident |
| RW-CASEOWN, case owner | Reads the entries through the case timeline of rwb-case, which reads the ledger through this service's contract |
| No approval level from the delegation of authority applies | The story takes no business decision |

The login behind the append is the `rwb_source_data` login of the target (DP-02; Architecture v5 slide 29), and the grants it holds are delivered by the DB story of this service. This story writes no grant statement and holds no credential of its own.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, through the append of RWB-P1-E1066-APP |
| DF-INT-014 | interaction | `eventCode` | Write |
| DF-INT-015 | interaction | `actorType` | Write |
| DF-INT-016 | interaction | `actorRef` | Write |
| DF-INT-017 | interaction | `sourceRef` | Write |
| DF-INT-018 | interaction | `idempotencyKey` | Write |
| DF-INT-019 | interaction | `caseSeq` | Write, assigned by the writer |
| DF-INT-020 | interaction | `decisionLogId` | Write, for DECISION_TAKEN only |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write, by the inbox of RWB-PLT-TE006-CON |

The field names used here and in section 12 are those of the `Interaction` schema of the API Specification v5; the physical column names of the table are RWB-P1-E1066-CON's. Record IDs of assignments, documents and decisions are read from the event payload, not from their tables: this story reads no row of `recovery_case`, `assignment`, `document` or `decision_log_entry`, and the case-existence check is the writer's. The listener sets no `correctsEntryId`, because none of the six consumed types is a correction; that field belongs to the correction path of the writer's contract. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation: it is the consumer side of the intake, and the read and append operations of the ledger are RWB-P1-E1066-APP's.

#### 12.2 REST operations consumed

None across a service boundary. The one call the listener makes is the append of RWB-P1-E1066-APP in the same service, documented by RWB-P1-E1066-CON: it carries the `Interaction` request of the writer's contract (`eventCode`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `caseSeq`, `decisionLogId`) and answers a reference to the written entry, a duplicate answer with the current hit count, or a refusal for a case that does not exist. The path, the payload type and the answer of that operation are fixed by RWB-P1-E1066-CON and are not restated here, so no other service's contract is consumed and nothing is faked in this section.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 41). This story publishes no event and writes no outbox row of its own: it is a consumer only.

#### 12.4 Events consumed

| Event type | Topic | Owner | Entry event code | Actor source |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_CREATED | Envelope: service identity code |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_ALLOCATED | Envelope: service identity code |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_TRANSFERRED | Envelope: user ID |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_ESCALATED | Envelope: service identity code |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | DOCUMENT_ATTACHED | Envelope: service identity code |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | DECISION_TAKEN | Envelope: user ID or service identity code |

The map is read as configuration, one row per event type, and it is the contract of RWB-P1-E1067-CON. The `sourceRef` of each entry is the owning module and the event type in the legacy form `<owning module>, <event ID> <event name>`, as AC2 shows with `P3 case and workflow, EV-02 CaseAllocated`; the value per row is the map row, not a constant in the listener. Each consumer group of the service has its own inbox rows, its own retry topics (1 min, 10 min, 1 h) and its own `.dlt` topic with an alert (Architecture v5 slide 11). No other event type is consumed by this story, and the two events of the service's own topic are not consumed by it.

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
| `rwb-case` event fixtures (four) | `rwb.case.events.v1` | CaseCreated, CaseAllocated, CaseTransferred and TimerBreached, each a CloudEvents 1.0 message with `id`, `source`, `type`, `specversion`, `time`, `subject` and a payload of IDs and codes, in the current version and in the previous one |
| `rwb-document` event fixture | `rwb.document.events.v1` | DocumentStored for case "RW-2026-000301" and for an unknown case ID, with the document reference only |
| `rwb-decision-record` event fixture | `rwb.decision-record.v1` | DecisionRecorded with the decision log reference that becomes `decisionLogId` |
| Writer stub | The append of RWB-P1-E1066-APP | An accepted append, a duplicate key with its hit count, a case-not-found refusal and a failed insert, so AC6, AC7 and AC8 run without the writer's database |
| Inbox fixture | `processed_event` in `rwb_source_data` | Rows with a hit count per key, so AC7 reads the count the inbox holds |

The six event fixtures are the fixtures of RWB-P1-E1067-CON, and a fixture that drifts from the map fails the contract test. Every fixture is synthetic, and no production payload is copied into one.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None across a service boundary | The append of RWB-P1-E1066-APP is the same service's operation, one call per event, 2 s budget (DP-11) |
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
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 and DP-18 are this story's own patterns: the ledger is P1's and the listener writes it in P1's schema. DP-03 is used, not delivered: the DECISION_TAKEN entry takes its `decisionLogId` from the event the local decision-record library publishes, and this story writes no decision record. DP-07 is used for the entry codes, read as LOV-LEDGER-EVENT. DP-09 is the consumer side of the platform library: the inbox, the envelope, the retry topics and the `.dlt`. DP-11 is the one call to the same service's writer, with its 2 s budget. DP-15 is the per-service sequence the inbox objects arrive on, and this story adds no migration. DP-19 applies to the case timeline that shows the entries, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LedgerEventListener` | Consumer | Subscribes to the six event types on their owner topics, checks the schema version, calls the mapper and the writer, commits the offset after the entry is written or the event is parked |
| `LedgerEventMapper` | Service | Event to interaction request per the map row, read from configuration and cross-checked against LOV-LEDGER-EVENT; sets the actor, the source reference and the idempotency key |
| `LedgerMapRepository` | Repository | Reads the versioned map of RWB-P1-E1067-CON; one row per event type |
| `LedgerAppendClient` | Client | The append of RWB-P1-E1066-APP, one call, 2 s timeout, no retry of its own (the broker retries) |
| `LedgerFailureHandler` | Service | Parks an event with its reason and owner, raises `LEDGER_WRITE_FAILED`, writes no entry for a parked event |
| `LedgerIntakeContractTest` | Test | Compares the six fixtures with the map and fails on drift |

**Migrations and sequence (DP-15).** This story adds no table and no version of its own. The inbox `processed_event` and the idempotency table arrive as the PLT library objects created in `rwb_source_data` on the service's per-service Flyway sequence, and the ledger table `interaction` arrives with RWB-P1-E1066-APP. An applied version is never edited; a correction is a new version.

**Configuration and reference data**

- The event-to-entry map is configuration, one row per event type: the event type, the topic, the entry event code, the actor source, the payload fields read, the accepted schema versions and the source-reference form. It is the contract of RWB-P1-E1067-CON.
- The entry codes are read as LOV-LEDGER-EVENT from the reference-data contract of rwb-case (DP-07); a code that the list does not carry fails the contract test.
- The retry limit is three and the retry topics are 1 min, 10 min and 1 h, from the outbox and inbox settings of the platform library (NFR-026; DL11).
- The exception queue owner is RW-PLATADM, as data and not as a constant.
- No business value is written in code: the map, the retry limit, the owner and the accepted versions are configuration and reference data.

**Build steps**

1. `LedgerMapRepository` and the versioned map, with the six rows of section 12.4 and the cross-check against LOV-LEDGER-EVENT (AC2).
2. `LedgerEventMapper` with the actor, the source reference form and the idempotency key of the envelope (AC2).
3. `LedgerEventListener` on the six topics, with the version check of step 3 of the flow (AC4).
4. `LedgerAppendClient` against the writer stub, and the duplicate answer read from the inbox row (AC7).
5. The order path: the case key of the topic and the `caseSeq` of the writer, with the two events of AC6 (AC6).
6. `LedgerFailureHandler`: the case-not-found refusal, the retry limit and the parking with its reason, the `.dlt` topic and the incident (AC8, X3).
7. `LedgerIntakeContractTest` over the six fixtures and the map; a drift fails the build (AC4, AC6).
8. Tests for AC2, AC4, AC6, AC7 and AC8, and the four regression rows of section 16.

**Feature flag.** `rwb.dataengine.ledger-events`, kept as the legacy key and held by the platform flag library (Template and Rules §R3 default ruling), so the consumer can be switched off without a deployment.

**Done when.** The tests in section 16 pass, each of the six event types has the ledger as a consumer in SIT, a redelivered event leaves one entry and one hit, and no event is acknowledged before it is written or parked.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | Ledger write failed, carried on the incident and the exception queue item | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without the right on the ledger calls the append | You cannot {action} here. Your role does not include it. |
| Exception queue reason | A schema version that is neither current nor previous | schema version 3 not accepted |
| Exception queue reason | The append answers that the case does not exist | case not found |
| Incident | The retry limit is reached | LEDGER_WRITE_FAILED |

The two message texts are the legacy texts, unchanged, and Thai text for each message follows decision DL10. The exception queue reason and the incident name are for the platform administrator and are not part of the message standard.

### 15. Screens and states

No screen in this story (DP-19). The platform administrator sees a parked event on the exception queue screen (SCR-09, Platform administration R) with its reason and its owner, and the dead-letter alert on the service dashboard. The case owner reads the entries through the case timeline of rwb-case (`GET /cases/{caseId}/interactions`), whose screen is owned by the screen owner and whose route is the gateway-bff composite route (DP-19); this story serves the data behind that route and builds none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01 | AC1, BR1 | End to end | Six synthetic events for case RW-2026-000301 |
| TC-E1-067-02 | AC2, BR2 | End to end | CASE_ALLOCATED and CASE_TRANSFERRED entries |
| TC-E1-067-03 | AC3, BR3 | End to end | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201 |
| TC-E1-067-04 | AC4, BR6 | End to end | CaseTransferred at schema version 3 |
| TC-E1-067-05 | AC5, BR5 | End to end | Ledger insert forced to fail; outbox retry limit 3 |
| TC-E1-067-06 | AC6, BR4 | End to end | CaseCreated then CaseAllocated in the outbox |
| TC-E1-067-07 | AC7, BR3 | End to end | One event on two consumer threads |
| TC-E1-067-08 | AC8 | End to end | DocumentStored for an unknown case ID |
| TC-E1-067-09 | Access | Component | SY-AGENT calls append(); refused with MSG-P4-002 |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-E1-067-02, TC-E1-067-04, TC-E1-067-06, TC-E1-067-07 and TC-E1-067-08 are the evidence of the five criteria this story owns. TC-E1-067-01, TC-E1-067-03 and TC-E1-067-05 are kept as regression rows: AC1, AC3 and AC5 are the criteria of RWB-P1-E1066-APP, the writer and its duplicate rule, and the listener must not break them. TC-E1-067-09 is the access regression of the same legacy key.

### 17. Guardrails

- No business value in code: the map, the entry codes, the retry limit, the accepted versions and the exception queue owner are configuration and reference data (DP-07).
- No personal data in logs, tests, events or prompts: the six consumed types carry IDs and codes only, the map reads no personal field, and every fixture is synthetic (BR7).
- No read of another service's tables: the case reference, the document reference and the decision reference come from the payload, and the case-existence check is the writer's (DP-01).
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all (DP-05 is not used here).
- The listener never acknowledges an event it has not written or moved to the exception queue.
- One hop and 2 s on the append; a slow or failed answer parks the event and never half-writes an entry (DP-11).
- The tables it relies on are library objects or the writer's; this story creates none, and an applied migration is never edited (DP-15).
- No screen is served here; the timeline is the gateway-bff composite route and the screen owner's (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-36 | TC-E1-067-01, TC-E1-067-04, TC-E1-067-05, TC-E1-067-06, TC-E1-067-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-067-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-04 | All recovery processes | R-UNI-40 | TC-E1-067-03, TC-E1-067-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1067-CON | Contract | H build dependency: the intake map, the six event fixtures and the writer stub of section 12.8 |
| RWB-P1-E1066-APP | App development | H build dependency: the ledger table, the case sequence and the append this listener calls |
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
