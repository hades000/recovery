# RWB-P1-E1067-CON Every Workbench action into the interaction ledger - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1067-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-067 |
| Legacy disposition | Split (rework) |
| Size | Not specified in the source documents (DOR-RWB-P1-E1067-CON-16); the squad sizes it at refinement |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-067 for rwb-source-data. The legacy listener's six events, its event-to-entry map, its schema-version rule, its duplicate rule and its failure path become the published contract baseline of the ledger intake: a versioned map with one row per event type, the six event fixtures and the writer stub, on Day 1, before the app story of this legacy key is built. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1067-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 9 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the ledger intake: a versioned map of the six consumed event types with their topics, their entry event codes, their actor source, the payload fields they read and the schema versions they accept, the source-reference form, the dedupe contract, the ordering and failure contract, the nine contract tables of section 12 and the six event fixtures with the writer stub**, so that **the listener of RWB-P1-E1067-APP, the producers of the six facts and the test stories build against a fixed, testable intake contract on Day 1 without waiting for rwb-source-data to be built**.

This is the contract slice of legacy RWB-E1-067. It fixes what the intake consumes and how an event becomes an entry; it builds no consumer and writes no entry.

### 2. Business rationale

The ledger is P1's (DP-18; Template and Rules §R3 default ruling) and rwb-source-data is the one consumer of the six facts the ledger records (DP-01, DP-09). Contract-first is the decoupling decision (DP-11, ADR-020): if the map, the accepted schema versions, the idempotency key, the order and the failure path are agreed once and faked, the listener of RWB-P1-E1067-APP builds in parallel with the three producing services, and a change in a producer's payload is caught in a contract test rather than in an integration window.

The baseline also fixes the naming that the checks require: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata`. The intake consumes on three topics owned by other services and publishes nothing of its own.

Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007; applies DP-01, DP-03, DP-07, DP-09, DP-11, DP-15, DP-18 and DP-19.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the topic, the event names and the queue follow the platform rule rather than a local choice (DP-14).
- The outbox and inbox library is published with its CloudEvents 1.0 envelope, its `processed_event` columns and its retry and `.dlt` topics, as the reference of the dedupe and failure sections (RWB-PLT-TE006-CON, DP-09).
- The decision-record library and the shared topic are published, because `DecisionRecorded` is one of the six consumed types (RWB-PLT-E1027-CON, DP-03).
- The reference-data contract of rwb-case is published with LOV-LEDGER-EVENT, because every entry event code is a list value and not a constant (DP-07).
- The ledger table and its append contract are the writer's, and the field names of the request are taken from the `Interaction` schema of the API Specification v5 and from RWB-P1-E1066-CON (DP-01, DP-11).
- The owners of the six events are taken from the Ownership Map and the Architecture v5 event catalogue only; this baseline documents no event owned by rwb-source-data except its own two, which it does not consume.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the versioned map with one row per consumed event type: the event type, its topic, its owner, the entry event code, the source system, the source-reference form, the actor source, the payload fields read and the accepted schema versions.
2. Agree the entry event code of each row against LOV-LEDGER-EVENT and the decision entry rule of `DecisionRecorded`.
3. Agree the two payload rules: the actor comes from the CloudEvents envelope and the fields read are IDs and codes only.
4. State the schema-version rule: current and previous accepted, anything else to the exception queue with its reason text and owner RW-PLATADM.
5. State the dedupe contract: the idempotency key is the CloudEvents id, unique on `interaction.idempotency_key`, and a repeat increments the inbox hit count.
6. State the ordering and failure contract: per-case ordering on the case key, the retry limit, the retry topics, the `.dlt` topic, and the rule that no offset is acknowledged before the entry is written or the event is parked.
7. Publish the nine contract tables of section 12 and the six event fixtures with the writer stub.
8. Add the contract tests: map validation, row completeness, fixture against map, duplicate replay and version refusal; tag the baseline and hand it to RWB-P1-E1067-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A map row is missing a required field, or the map does not validate | The contract test fails and the merge is blocked; the app story cannot start | None | AC1 |
| X2 | A row names a field that carries personal data | The data-steward check fails the row and the merge is blocked | None | AC2 |
| X3 | A fixture carries a schema version that the row does not accept | The contract test fails; the fixture is corrected, not the rule | None | AC3 |
| X4 | A fixture repeats a CloudEvents id without a hit count in the inbox fixture | The contract test fails; a repeat is one entry and one hit | None | AC4 |
| X5 | A fixture arrives out of order for its case, or without the case key | The contract test fails; the row is not orderable | None | AC5 |
| X6 | A table of section 12 is missing, or a fixture drifts from its map row | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A field-level detail is missing from the source material | The item is marked with the placeholder and one gap row is carried | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published library contracts only |
| Negotiable | Field-level detail is settled with the producing teams; the names, the six types, the envelope and the rules are fixed by the target architecture |
| Valuable | Unblocks the listener of RWB-P1-E1067-APP and the tests of this legacy key on Day 1, and gives the three producers one agreed intake |
| Estimable | One versioned map, nine contract tables, six event fixtures and one writer stub, with six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Ledger intake contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the ledger intake consumes six event types on three owner topics

  Scenario: AC1 The intake contract document validates and names the six consumed types (new, D-RCV-60)
    Given the intake contract document of the ledger is published as a versioned YAML map
    When it is validated against its own schema
    Then it validates with no error and carries one row per event type
    Then it names rwb.case.CaseCreated.v1, rwb.case.CaseAllocated.v1, rwb.case.CaseTransferred.v1 and rwb.case.TimerBreached.v1 on rwb.case.events.v1
    Then it names rwb.document.DocumentStored.v1 on rwb.document.events.v1 and rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1
    Then each row names its entry event code, the source system "WORKBENCH" and the source-reference form "<owning module>, <event ID> <event name>"
    Then an event type that the map does not carry is refused by the contract test

  Scenario: AC2 The map states the actor source and the payload fields it reads (new, D-RCV-60)
    Given a row of the map
    When its actor and payload sections are read
    Then the actor is taken from the CloudEvents envelope, actorType USER for a user ID and SERVICE for a service identity code, with actorRef the identifier
    Then the idempotency key and the actor are read from the CloudEvents envelope, and their attribute names are Not specified in the source documents (GAP-1056, GAP-2257); each key keeps the legacy shape of event code, case number and action date
    Then the payload fields read are named per row and are IDs, codes, dates and amounts only
    Then no row names a name, an address, an identity number, a contact point or a free-text field
    Then no row reads a field the event does not carry

  Scenario: AC3 Schema-version acceptance is stated (new, D-RCV-60)
    Given an event of a type the map carries
    When it arrives at the current schema version
    Then it is accepted and one entry is appended
    When it arrives at the previous schema version
    Then it is accepted and one entry is appended
    When a CaseTransferred event arrives at schema version 3 while the row accepts versions 2 and 1
    Then no entry is written
    Then the event is in the exception queue with owner RW-PLATADM and reason "schema version 3 not accepted"

  Scenario: AC4 The dedupe contract is stated (new, D-RCV-60)
    Given an event of case "RW-2026-000301" with CloudEvents id "EV-02-RW-2026-000301-20261201"
    When it is appended and the same id is delivered again
    Then the idempotency key of the entry is the CloudEvents id and it is unique on interaction.idempotency_key
    Then one entry exists and the hit count of the inbox row for that key is 1
    Then a second delivery never overwrites the first entry
    Then the CloudEvents id is recorded in processed_event, with the event idempotency key as the business key

  Scenario: AC5 Ordering and failure are stated (new, D-RCV-60)
    Given two events of one case on the same owner topic
    When they are consumed
    Then the map states per-case ordering on the case key and that the writer assigns caseSeq in that order
    Then one consumer group reads the three owner topics, the ledger read orders by occurredAt and then caseSeq, and a cross-topic inversion that occurredAt cannot resolve is reported and not reordered
    Then the retry limit is three, the retry topics are 1 min, 10 min and 1 h, and the fourth attempt parks the event in the exception queue with owner RW-PLATADM
    Then no offset is acknowledged before the entry is written or the event is parked
    Then an event of an unknown case is parked with reason "case not found" and no entry

  Scenario: AC6 The nine contract tables are complete and the six fixtures match the map (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then each of the six event fixtures is a CloudEvents 1.0 message that validates against the schema of its row
    Then the envelope is asserted in the relay contract test against the AsyncAPI fragment of section 12.3
    Then each fixture produces the entry event code of its row and no other
    Then the contract tests fail on drift between a fixture and the map

  Scenario: AC7 The table ownership of section 12.7 is bounded (new, D-RCV-60)
    Given the tables owned by the contract of this story
    When section 12.7 is read
    Then only the tables interaction and processed_event are named as owned
    Then no table of another service is named as read or written

  Scenario: AC8 A field-level detail missing from the source material is marked with the placeholder (new, D-RCV-60)
    Given a field-level detail is missing from the source material
    When section 11 is written
    Then the item is marked with the placeholder and one gap row is carried
    Then no value is invented for the item

  Scenario: AC9 The intake publishes nothing and writes only through the writer (new, D-RCV-60)
    Given the intake of the ledger is running
    When it consumes an event
    Then it publishes no event and provides no REST operation
    Then it writes ledger entries only through the writer
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One intake map, one row per consumed event type; the entry event code of a row is a value of LOV-LEDGER-EVENT and never a constant in code | REQ-ILG-002; DP-07; legacy RWB-E1-067 §13 |
| BR2 | The entry names the system or person that produced it, taken from the CloudEvents envelope | REQ-ILG-002 |
| BR3 | The same event with the same key produces one entry, and the repeat is counted in the inbox | R-UNI-40; REQ-ILG-007; DP-09 |
| BR4 | Events for one case are consumed in the order they were written, on the case key, and the writer assigns `caseSeq` | Events rule "Ordering" (events.txt) |
| BR5 | A consumer failure retries, then goes to the exception queue with its owner, and no offset is acknowledged before the entry is written or the event is parked | Events rule "Failure" (events.txt); R-UNI-36; NFR-026 |
| BR6 | A consumer accepts the current and the previous schema version only | Events rule "Versioning" (events.txt) |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt); covered by AC2, TC-P1-E1067-CON-02 |
| BR8 | The intake publishes nothing: it consumes on the owners' topics and writes only the ledger's entries through the writer | DP-09, DP-14, DP-18; covered by AC9, TC-P1-E1067-CON-09 |

**Where each rule lives in the target.** BR1 is the versioned map (one row per consumed event type, six rows of section 12.4; its file name and version label are Not specified in the source documents (GAP-0508)) and the reference-data cross-check; a new fact is a map row and a new LOV value, not a code change. BR2 is the envelope, read once per event. BR3 is the inbox row of `rwb_source_data` and the unique key on `interaction.idempotency_key`; the library owns the first and the writer owns the second. BR4 is the case ID as the Kafka key plus the writer's gap-free `caseSeq`. BR5 is the retry topics, the `.dlt` topic, the parking with its reason and owner, and the acknowledgement rule. The JOB-11 outbox relay limit is read from the platform relay configuration as a parameter with no value fixed in code; the test covers the pending-to-published loop, not the count. The value of the limit is Not specified in the source documents (GAP-1057). BR6 is the registry with BACKWARD compatibility and the version check of the consumer. The JSON Schema registry subject of DocumentStored and the AsyncAPI document location for rwb.document.events.v1 are held in configuration; their values are Not specified in the source documents (GAP-1058). BR7 is the payload section of every row. BR8 is the direction of the intake: it provides no REST operation and publishes no event, and the topic of the service carries only its own two facts, which belong to RWB-P1-E1013-APP.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The six rows, the actor and payload sections and the six fixtures are described | In review |
| In review | Producer and consumer sign-off | The listener and the three producing teams accept the map and the fixtures | Baselined |
| Baselined | Additive change | A field is added within major version 1, or a seventh row is added | Baselined |
| Baselined | Breaking change | A row is removed, the entry event code of a row changes, or a payload field is retyped | New major version drafted |
| Baselined | Drift between a fixture and its row | The contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the map, the fixtures and the writer stub; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a seventh consumed type |
| Producing teams of rwb-case, rwb-document and rwb-decision | Review and sign off the rows of the events they publish |
| Reference-data owner of rwb-case | Confirms that every entry event code of the map is a value of LOV-LEDGER-EVENT |
| Data steward | Confirms that no row reads a personal data field |
| Platform library owner | Owns the CloudEvents envelope, the inbox table shape and the retry and dead-letter rule this baseline reuses |

The per-service login behind the intake is the `rwb_source_data` login (DP-02; Architecture v5 slides 11 and 29); the intake holds no credential of its own and this baseline writes no grant statement.

### 11. Data

The baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Map row | `eventType`, `topic`, `owner`, `entryEventCode`, `sourceSystem`, `sourceRefForm`, `actorSource`, `payloadFields`, `acceptedVersions` | Not specified in the source documents (DOR-RWB-P1-E1067-CON-7) |
| Actor | `actorType` as USER, SERVICE or PARTNER and `actorRef` as the user ID or the service identity code, both from the envelope | Not specified in the source documents (DOR-RWB-P1-E1067-CON-7) |
| Entry fields the intake sets | `eventCode`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `decisionLogId` for DECISION_TAKEN only; `caseSeq` is the writer's | Not specified in the source documents (DOR-RWB-P1-E1067-CON-7) |
| Payload fields read | References and codes only: the case reference, the document reference, the decision log reference, the timer reference, the queue code and the rule identifier where the event carries one | Not specified in the source documents (DOR-RWB-P1-E1067-CON-7) |
| Personal data | None: no name, address, identity number, contact point or free-text field is read by any row | Not specified in the source documents (DOR-RWB-P1-E1067-CON-7) |

The format of the map document itself (its schema, its version label and where it is published) and the exact target event names that carry the document fact and the timer fact are Not specified in the source documents (GAP-0508; ASM-0700); this baseline fixes the row content of the table above, the version label as a field of the document, and the six rows of section 12.4, and leaves the file format to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

None. This baseline documents an event intake, not a REST operation. The append the listener calls is the same service's operation of RWB-P1-E1066-CON and is named as consumed in 12.2; the read operations of the ledger are RWB-P1-E1066-CON's as well.

#### 12.2 REST operations consumed

None across a service boundary. The one operation the intake calls is the append of RWB-P1-E1066-CON in the same service, one call per event with a 2 s budget, documented there and stubbed in 12.8; this baseline does not restate its path, its payload type or its answer, and it consumes no other service's REST operation.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 41). The intake publishes no event and writes no outbox row.

#### 12.4 Events consumed

| Event type | Topic | Owner | Map row | Entry event code | Accepted versions |
|---|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | 01 · EV-01 CaseCreated | CASE_CREATED | Current and previous |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | 02 · EV-02 CaseAllocated | CASE_ALLOCATED | Current and previous |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | 03 · EV-04 CaseTransferred | CASE_TRANSFERRED | Current and previous (2 and 1 in the legacy state) |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 rwb-case | 04 · EV-19 TimerBreached | CASE_ESCALATED | Current and previous |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | 05 · EV-16 DocumentStored | DOCUMENT_ATTACHED | Current and previous |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | 06 · EV-08 DecisionRecorded | DECISION_TAKEN | Current and previous |

The row labels keep the legacy event ID so that the legacy criteria and the target map can be read side by side: EV-01, EV-02, EV-04, EV-19, EV-16 and EV-08 are the six events of the legacy listener, and `CaseTransferred` at schema version 2 accepting version 1 is the state AC3 and legacy AC4 describe. The source-reference form of every row is `<owning module>, <event ID> <event name>`, as AC2 shows with `P3 case and workflow, EV-02 CaseAllocated`. The actor of every row is the CloudEvents envelope. Each row fixes the payload fields it reads, and no row reads a personal field.

#### 12.5 Workflows and activities

None. The intake is a consumer on the service worker; it starts no workflow, calls no activity and publishes no contract jar. The task queue `rwb-source-data` in namespace `rwb-recovery` is the service's queue, and the workflows of Architecture v5 slide 15 belong to other P1 stories.

#### 12.6 Schedules

None. The intake is driven by the topic. No Temporal Schedule and no Quartz job is part of this baseline, and the outbox relay of a producer is JOB-11 of the owning service (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `interaction` | P1 rwb-source-data, schema `rwb_source_data` (DP-01, DP-18) | The entry the intake appends through the writer; `idempotencyKey` is unique on it and `caseSeq` is gap-free within its case |
| `processed_event` | PLT library object created in `rwb_source_data` (DP-09; Ownership Map) | The inbox row per consumed event, with the hit count of a repeated key; one row per consumer group |

No other table is named in the contract, and no table of another service is read (DP-01). The intake creates no table of its own.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb.case.events.v1` fixture set (four messages) | CaseCreated, CaseAllocated, CaseTransferred and TimerBreached, each a CloudEvents 1.0 message with `id`, `source`, `type`, `specversion`, `time`, `subject` and a payload of IDs and codes; CaseTransferred is supplied at version 2 and at version 3 | The listener, the contract tests |
| `rwb.document.events.v1` fixture | DocumentStored for case "RW-2026-000301" and for an unknown case ID, with the document reference only | The listener, the contract tests |
| `rwb.decision-record.v1` fixture | DecisionRecorded with the decision log reference that becomes `decisionLogId` | The listener, the contract tests |
| Writer stub | An accepted append, a duplicate key with its hit count, a case-not-found refusal and a failed insert | The listener, the contract tests |
| Inbox fixture | `processed_event` rows with a hit count per key | The contract tests of AC4 |

The six event fixtures are the fixtures of this baseline, and the contract tests compare every one of them with its map row and fail on drift.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed across a service boundary | The append is the same service's operation of RWB-P1-E1066-CON, one call per event, 2 s budget (DP-11) |
| Kafka | None published, 6 consumed | Three owner topics, CloudEvents 1.0, key caseId, inbox dedupe, retry topics and `.dlt` (DP-09) |
| Temporal | None | No workflow, activity or Schedule in this baseline |
| File | None | No file in this baseline; the fixtures are test artefacts |

### 13. Solution plan

**Deliverables.** `contract/ledger-intake-map-v1.yaml` (the versioned map, one row per consumed event type), `contract/ledger-intake-rules.md` (the version, dedupe, order and failure rules of sections 12.4 and 8), the six event fixtures under `contract/fixtures/`, the writer stub mapping and the six contract tests. The file format and the version label of the map are Not specified in the source documents (GAP-0508; ASM-0700).

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

The patterns are used, not delivered here: the dependency column is the one the app story of this legacy key carries, and this baseline has no build dependency of its own (§R5.7). DP-18 fixes the owner of the ledger and DP-01 the schema the entries live in; DP-09 and DP-03 fix the two platform envelopes the intake reads; DP-07 fixes the list the entry codes come from; DP-11 is the same-service append; DP-15 is the sequence the inbox objects arrive on; DP-19 is the route of the screen that shows the entries, which this baseline does not touch.

**Build steps**

1. The map skeleton with its version label, its row schema and the six rows of section 12.4; schema lint in the pipeline.
2. The actor and payload sections per row, with the no-personal-data check (AC2).
3. The version rule per row, with the CaseTransferred version 2 and version 3 fixtures (AC3).
4. The dedupe rule and the inbox hit count, with the repeated-id fixture (AC4).
5. The order and failure rule, with the case key, the retry limit, the retry topics, the `.dlt` and the parking reasons (AC5).
6. The six event fixtures and the writer stub, each fixture validated against its row (AC6).
7. The six contract tests; a drift between a fixture and its row fails the build.
8. Baseline tag and the sign-off note of the listener story and the three producing teams.

**Done when.** The map validates in the pipeline, the six contract tests pass, the six fixtures produce exactly the entry event codes of their rows, and RWB-P1-E1067-APP has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The append fails on the last attempt, carried on the incident and the exception queue item | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without the right on the ledger calls the append | You cannot {action} here. Your role does not include it. |
| Exception queue reason | A schema version the row does not accept | schema version 3 not accepted |
| Exception queue reason | The append answers that the case does not exist | case not found |

The two message texts are the legacy texts of RWB-E1-067, unchanged, and Thai text for each message follows decision DL10. DL10 (owner: Business lead with Legal and Compliance) is worked on the recommended option A of the decision log: the business lead drafts per module one epic ahead, and Legal and Compliance approve. The decision log gives this position while the Thai names are outstanding: screens go to UAT with English labels and the standard Thai message only. The two reason texts are contract elements of the intake: they are the words the exception queue item carries, and the listener writes no other reason of its own.

### 15. Screens and states

No screen in this baseline (DP-19). The entries the intake writes are read by the case owner through the case timeline of rwb-case (`GET /cases/{caseId}/interactions`), whose screen is the screen owner's and whose route is the gateway-bff composite route; the platform administrator reads a parked event on the exception queue screen (SCR-09, Platform administration R). SCR-09 states named here: loading, as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-2320). This baseline adds no route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1067-CON-01 | AC1 | Contract | The map validates; six rows; the topics and the owners of section 12.4; a seventh type refused |
| TC-P1-E1067-CON-02 | AC2 | Contract | The actor section and the payload section of each row; the no-personal-data check |
| TC-P1-E1067-CON-03 | AC3 | Component | CaseTransferred at version 2 and version 1 accepted; version 3 parked with its reason |
| TC-P1-E1067-CON-04 | AC4 | Contract | The same CloudEvents id delivered twice; one entry, one hit |
| TC-P1-E1067-CON-05 | AC5 | Component | Two events of one case; the retry limit and the parking; an unknown case |
| TC-P1-E1067-CON-06 | AC6 | Contract | The nine sub-tables, the six fixtures and the writer stub; a drift fails |
| TC-P1-E1067-CON-07 | AC7 | Contract | Section 12.7 names only interaction and processed_event as owned; no other table is named |
| TC-P1-E1067-CON-08 | AC8 | Contract | A field missing from the source is marked with the placeholder and one gap row is carried |
| TC-P1-E1067-CON-09 | AC9 | Component | The intake publishes no event, exposes no REST operation and writes only through the writer |
| TC-E1-067-01 | AC1, BR1 | End to end | Six synthetic events for case RW-2026-000301 |
| TC-E1-067-02 | AC2, BR2 | End to end | CASE_ALLOCATED and CASE_TRANSFERRED entries |
| TC-E1-067-03 | AC3, BR3 | End to end | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201 |
| TC-E1-067-04 | AC4, BR6 | End to end | CaseTransferred at schema version 3 |
| TC-E1-067-05 | AC5, BR5 | End to end | Ledger insert forced to fail; outbox retry limit 3 |
| TC-E1-067-06 | AC6, BR4 | End to end | CaseCreated then CaseAllocated in the outbox |
| TC-E1-067-07 | AC7, BR3 | End to end | One event on two consumer threads |
| TC-E1-067-08 | AC8 | End to end | DocumentStored for an unknown case ID |
| TC-E1-067-09 | Access | Component | SY-AGENT calls append(); refused with MSG-P4-002 |

The nine legacy rows are kept in order and character for character as regression evidence: their criteria are owned by RWB-P1-E1067-APP, which this baseline enables, and the legacy level "System" maps to "End to end" and "Access" to "Component". The nine new cases test the artefact of this story and nothing else. TC-E1-067-07 and TC-E1-067-08 are run by RWB-P1-E1067-APP, which owns their criteria. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the entry event code of a row is a LOV value, the retry limit and the accepted versions are configuration, and no threshold or reason is written in code (DP-07).
- No personal data in the map, a fixture or an example: IDs, codes, dates and amounts only; a row that names a personal field fails the data-steward check (BR7).
- The baseline names only rwb-source-data's tables and only events owned by other services; it documents no event of its own as consumed (DP-01, DP-09).
- One intake map and one row per consumed type: a second map, or a row without an owner, fails the review.
- Every fixture is synthetic; no production payload is copied into a fixture or a stub.
- The CloudEvents envelope, the inbox shape and the retry rule come from the platform library; this baseline narrows them but never redefines them.
- The map is forward only: a corrective change is a new version of the map, never an edit of a baselined one (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | The six rows of 12.4 and their entry event codes | TC-P1-E1067-CON-01, TC-P1-E1067-CON-06 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The actor section and the source-reference form of every row | TC-P1-E1067-CON-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | The dedupe contract of 12.4 and 12.7 | TC-P1-E1067-CON-04, TC-E1-067-03, TC-E1-067-07 |
| NFR-026 | A consumer retries, then parks the event with its owner | The retry limit, the topics, the `.dlt` and the parking reasons | TC-P1-E1067-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The single append of 12.2 with its 2 s budget | TC-P1-E1067-CON-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1067-APP | App development | Consumer of this baseline: the listener reads the map and the fixtures |
| RWB-P1-E1066-CON | Contract | Sibling of the same legacy key: the append this intake calls and the field names it sets |
| RWB-P1-E1066-APP | App development | Sibling: the ledger table, the case sequence and the writer behind the stub |
| RWB-PLT-TE006-CON | Contract | The CloudEvents envelope, the inbox shape and the retry and dead-letter rule this baseline reuses (DP-09) |
| RWB-PLT-E1027-CON | Contract | The decision-record library and the shared topic of row 06 (DP-03) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | The reference-data library and the rwb-case contract the entry codes come from (DP-07) |
| RWB-PLT-E1044-CON | Contract | The per-service sequence the inbox objects arrive on (DP-15) |
| RWB-PLT-N001-CON | Contract | The gateway-bff composite route of the screen that shows the entries (DP-19) |
| The producing stories of rwb-case, rwb-document and rwb-decision | App development | Publishers of the six consumed types; they sign off the rows of their events |

### 19. Out of scope

- The listener, the mapper, the append client and the failure handler: RWB-P1-E1067-APP.
- The ledger table, the case sequence, the append operation and its answer: RWB-P1-E1066-APP and RWB-P1-E1066-CON.
- The platform inbox, the idempotency table and the retry and dead-letter topics: RWB-PLT-TE006-CON (DP-09).
- The six producers and their payloads: their own service stories; this baseline documents what the intake reads and changes none of it.
- The case timeline and its screen, and the exception queue screen: rwb-case, the platform administration screens and the gateway-bff composite route (DP-19).
- Any table, migration or deployment asset: this story publishes documents and fixtures only.
- The file format of the map beyond the row content of section 11 (GAP-0508).
