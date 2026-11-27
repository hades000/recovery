# RWB-P1-E1067-CON Every Workbench action into the interaction ledger - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
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
| Size | Not specified; pending squad refinement |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | After the build dependencies and their fakes are published |
| Depends on (build) | RWB-P1-E1066-CON, RWB-PLT-TE006-CON, RWB-PLT-E1027-CON, RWB-P3-E1043-CON |
| Contract dependencies | producer AsyncAPI messages for rwb-case, rwb-document and rwb-decision; Kafka consumer registration for rwb-source-data |
| Integration dependencies | None |
| External dependencies | None |
| Contract version | Intake map version 1 (`contract/ledger-intake-map-v1.yaml`); rwb-source-data.yaml 5.1.0 and the producer AsyncAPI 5.1.0 documents (API Specification v7) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-008, RD-P1-009 (X-03), RD-P1-011, RD-P1-072, RD-P1-074 |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- Intake map fixed: six rows with payload fields, literal source references, envelope attributes, version rule, dedupe, ignore rules and `.dlt` parking; DecisionRecorded type corrected (RD-P1-007, RD-P1-008, RD-P1-009).
- Consumer registration of rwb-source-data on the three topics and the in-process writer stub (RD-P1-003, RD-P1-007; consumer groups by RWB-P1-E1066-OPS).
- Findings RWB-P1-E1067-CON#1 to #21 fixed or carried as pending with a gap ID (NEW-GAP-S8-11, NEW-GAP-F09-4).
- Batch D: a read is not a decision, so row 06 needs no filter (RD-P1-072; NEW-GAP-F09-4 closed, superseding the open item of the last bullet above); the consumer-group deployment is a later step with no build dependency (RD-P1-074).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register); applied RD-P1-001, RD-P1-003, RD-P1-007, RD-P1-008, RD-P1-009 (X-03) and RD-P1-011; findings RWB-P1-E1067-CON#1 to #21.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-067 for rwb-source-data. The legacy listener's six events, its event-to-entry map, its schema-version rule, its duplicate rule and its failure path become the published contract baseline of the ledger intake: a versioned map with one row per event type, the producer-versioned fixtures and the E1066 writer stub, on Day 1, before the app story of this legacy key is built. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

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
- The ledger table and its append contract are the writer's, and the field names of the request are those of `InteractionRequest` in rwb-source-data.yaml 5.1.0, published by RWB-P1-E1066-CON (DP-01, DP-11).
- The owners of the six events are taken from the Ownership Map and the Architecture v5 event catalogue only; this baseline documents no event owned by rwb-source-data except its own two, which it does not consume.
- The build dependencies of the header are published; this story is not a Day 1 story. The producer AsyncAPI documents list rwb-source-data in `x-consumers`, and the Kafka catalog gives it read access to the three topics and their retry topics (RD-P1-003 rule 5).

### 4. Flow

1. Draft the versioned map with one row per consumed event type: the event type, its topic, its owner, the entry event code, the source system, the source-reference form, the actor source, the payload fields read and the accepted schema versions.
2. Agree the entry event code of each row against LOV-LEDGER-EVENT and the decision entry rule of `DecisionRecorded`.
3. Agree the two payload rules: the actor comes from the CloudEvents envelope and the fields read are IDs and codes only.
4. State the version rule: current and previous registered versions accepted; unsupported versions go to `<topic>.dlt` with the RD-P1-009 headers.
5. State the dedupe contract: `ce_id` is the inbox identity; `ce_idempotencykey` is the business key, unique on `interaction.idempotency_key`, and a redelivery increments the inbox hit count.
6. State the ordering and failure contract: `caseSeq` in arrival order and reads by `occurredAt` then `caseSeq`, the retry topics, the `.dlt` topic, and the rule that no offset is committed before the event is written, ignored by rule, or published to a retry or dead-letter topic.
7. Publish the nine contract tables of section 12 and the six event fixtures with the writer stub.
8. Add the contract tests: map validation, row completeness, fixture against map, duplicate replay and version refusal; tag the baseline and hand it to RWB-P1-E1067-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A map row is missing a required field, or the map does not validate | The contract test fails and the merge is blocked; the app story cannot start | None | AC1 |
| X2 | A row names a field that carries personal data | The data-steward check fails the row and the merge is blocked | None | AC2 |
| X3 | A fixture carries a schema version that the row does not accept | The contract test fails; the fixture is corrected, not the rule | None | AC3 |
| X4 | A fixture repeats a `ce_id` without a hit count in the inbox fixture | The contract test fails; a repeat is one entry and one hit | None | AC4 |
| X5 | A fixture of rows 01 to 05 has no `data.caseId` | The intake contract sends it to `.dlt`; out-of-order delivery is accepted and read by `occurredAt` | None | AC5, AC12 |
| X6 | A table of section 12 is missing, or a fixture drifts from its map row | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A field-level detail is missing from the source material | The item is marked with the placeholder and one gap row is carried | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published library contracts only |
| Negotiable | Field-level detail is settled with the producing teams; the names, the six types, the envelope and the rules are fixed by the target architecture |
| Valuable | Unblocks the listener of RWB-P1-E1067-APP and the tests of this legacy key on Day 1, and gives the three producers one agreed intake |
| Estimable | One versioned map, nine contract tables, six event fixtures and one writer stub, with the contract tests of section 16 |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Ledger intake contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the ledger intake consumes six event types on three owner topics and one group per topic is registered

  Scenario: AC1 The intake contract document validates and names the six consumed types (new, D-RCV-60)
    Given the intake contract document of the ledger is published as a versioned YAML map
    When it is validated against the JSON Schema of the map published beside it
    Then it validates with no error, carries its version label 1 as a field of the document and one row per event type
    Then it names rwb.case.CaseCreated.v1, rwb.case.CaseAllocated.v1, rwb.case.CaseTransferred.v1 and rwb.case.TimerBreached.v1 on rwb.case.events.v1
    Then it names rwb.document.DocumentStored.v1 on rwb.document.events.v1 and rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1
    Then each row names its event code, `sourceSystem=WORKBENCH`, and the literal `sourceRef` from section 12.4
    Then `CaseStateChanged` is acknowledged and ignored with no inbox row, append or parked record

  Scenario: AC2 The map states the actor source and the payload fields it reads (new, D-RCV-60)
    Given a row of the map
    When its actor and payload sections are read
    Then `ce_actor` is `USER:<userId>`, `SERVICE:<service name>` or `PARTNER:<partnerCode>`; `actorType` is the prefix and `actorRef` the remainder
    Then `ce_idempotencykey` is the business key (at most 120) and `ce_actor` is the actor (at most 74); `ce_id` is used only for inbox deduplication
    Then the payload fields read per row are exactly those of section 12.4
    Then no row names a name, an address, an identity number, a contact point or a free-text field
    Then no row reads a field the event does not carry

  Scenario: AC3 Schema-version acceptance is stated (new, D-RCV-60)
    Given an event of a type the map carries
    When it arrives at the current schema version
    Then it is accepted and one entry is appended
    When it arrives at the previous schema version
    Then it is accepted and one entry is appended
    When the synthetic unregistered type `rwb.case.CaseTransferred.v9` arrives
    Then no entry is written
    Then it is sent to `<topic>.dlt` with `rwb-dlt-reason=UNSUPPORTED_VERSION`, `rwb-dlt-consumer=rwb-source-data` and `rwb-dlt-owner=P1 squad`
    Then the offset is committed and no retry topic is used

  Scenario: AC4 The dedupe contract is stated (new, D-RCV-60)
    Given an event of case "RW-2026-000301" with `ce_id` "7f0c2a4e-1111-4222-8333-000000000001" and `ce_idempotencykey` "EV-02-RW-2026-000301-20261201-9a1b3c5d-1111-4222-8333-000000000002"
    When it is appended and the same `ce_id` is delivered again
    Then one entry exists whose `idempotencyKey` is the `ce_idempotencykey` value
    Then the `processed_event` row for `ce_id` has `hit_count` 2 after the redelivery
    Then the second delivery changes no entry
    When another `ce_id` carries the same `ce_idempotencykey`
    Then no entry is added and its inbox row is committed

  Scenario: AC5 Ordering and failure are stated (new, D-RCV-60)
    Given two events of one case on the same owner topic
    When they are consumed
    Then the writer assigns `caseSeq` in arrival order and the intake does not wait behind a failed record
    Then one group per owner topic is deployed by RWB-P1-E1066-OPS; ledger reads order by `occurredAt`, then `caseSeq`; no cross-topic order is promised
    Then transient failures (database, case read timeout) are published to the 1 min, 10 min and 1 h retry topics and then to `<topic>.dlt` with `RETRIES_EXHAUSTED`
    Then one `LEDGER_WRITE_FAILED` incident with MSG-P1-022 and one dead-letter alert are raised
    Then no offset is committed before the entry is written or the record is on a retry or dead-letter topic
    # Pending: handling of a writer refusal that is not transient (case not found, validation refusal); owner solution architect; NEW-GAP-S8-11.

  Scenario: AC6 The nine contract tables are complete and the six fixtures match the map (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then each of the six event fixtures is a CloudEvents 1.0 message that validates against the schema of its row
    Then each fixture validates against the producer AsyncAPI message named in section 12.4; the intake has no relay
    Then each fixture produces the entry event code of its row and no other
    Then the contract tests fail on drift between a fixture and the map

  Scenario: AC7 The table ownership of section 12.7 is bounded (new, D-RCV-60)
    Given the intake runs with grants on the `rwb_source_data` schema only
    When it processes the six fixtures
    Then it writes only `interaction` (through the writer) and `processed_event`
    Then no table of another service is read or written

  Scenario: AC8 A field-level detail missing from the source material is marked with the placeholder (new, D-RCV-60)
    Given map version 1
    When each field of each row is inspected
    Then every field whose type or required flag no source gives carries the gap ID GAP-0096 in the map
    Then no row defines a type of its own for such a field

  Scenario: AC9 The intake publishes nothing and writes only through the writer (new, D-RCV-60)
    Given the six fixtures are consumed against the writer stub
    When processing ends
    Then exactly one writer call is made per mapped fixture
    Then no record is produced except to retry or dead-letter topics
    Then no REST operation is added to rwb-source-data.yaml

  Scenario: AC10 Producer messages match the map fixtures (new, RD-P1-009)
    Given the producer AsyncAPI messages named in section 12.4
    When the six fixtures are validated
    Then each fixture matches the producer message and a removed or retyped read field fails the contract check
    # TC-P1-E1067-CON-10

  Scenario: AC11 The writer stub matches the append contract (new, RD-P1-007)
    Given the `InteractionLedgerWriter` interface of RWB-P1-E1066-APP and `InteractionRequest` of RWB-P1-E1066-CON
    When the stub outcomes are checked
    Then the stub offers appended, business key already stored, case not found, validation refusal, database failure and case read timeout
    Then database failure and case read timeout are retried, a stored business key adds no entry, and the two refusals follow NEW-GAP-S8-11
    # TC-P1-E1067-CON-11

  Scenario: AC12 Missing envelope attributes are parked (new, RD-P1-009)
    Given a fixture without `ce_actor` or `ce_idempotencykey`, or a row 01 to 05 fixture without `data.caseId`
    When the intake processes it
    Then no append is called and the record goes directly to `.dlt` with `rwb-dlt-reason=MISSING_ATTRIBUTE` and `rwb-dlt-owner=P1 squad`
    # TC-P1-E1067-CON-12

  Scenario: AC13 DecisionRecorded without a case is ignored (new, RD-P1-009)
    Given `rwb.decision.DecisionRecorded.v1` without `data.caseId`
    When the intake receives it
    Then the offset is committed with no inbox row, append or parked record
    # TC-P1-E1067-CON-13

  Scenario: AC14 Other event types are ignored (new, RD-P1-009)
    Given `CaseStateChanged`, `CaseAllocationFailed` or `DocumentFieldsExtracted` on a consumed topic
    When the intake receives the event
    Then it is committed with no inbox row, append or parked record
    # TC-P1-E1067-CON-14

  Scenario: AC15 No unlisted property is copied into the map or parked record (new, RD-P1-009)
    Given the permitted envelope and payload properties in section 12.4
    When map rows, fixtures and parked-record headers are checked
    Then no other property is read or copied
    # TC-P1-E1067-CON-15
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One intake map, one row per consumed event type; the entry event code of a row is a value of LOV-LEDGER-EVENT and never a constant in code | REQ-ILG-002; DP-07; legacy RWB-E1-067 §13 |
| BR2 | The entry names the system or person that produced it, taken from the CloudEvents envelope | REQ-ILG-002 |
| BR3 | The writer business key is permanent and unique; redeliveries by the same `ce_id` increment inbox `hit_count` | R-UNI-40; REQ-ILG-007; DP-09 |
| BR4 | `caseSeq` is assigned in arrival order; ledger reads order by `occurredAt`, then `caseSeq`; the intake does not wait behind a failed event | Events rule "Ordering" (events.txt) |
| BR5 | A consumer failure retries, then goes to the `<topic>.dlt` topic with its RD-P1-009 headers, and no offset is acknowledged before the entry is written or the event is parked | Events rule "Failure" (events.txt); R-UNI-36; NFR-026 |
| BR6 | A consumer accepts the current and previous registered schema versions only | Events rule "Versioning" (events.txt) |
| BR7 | Event payloads carry references and codes, no personal data | Events rule "Payload" (events.txt); covered by AC2, TC-P1-E1067-CON-01 |
| BR8 | The intake publishes nothing: it consumes on the owners' topics and writes only the ledger's entries through the writer | DP-09, DP-14, DP-18; covered by AC9, TC-P1-E1067-CON-09 |

**Where each rule lives in the target.** BR1 is the versioned map `contract/ledger-intake-map-v1.yaml` (one row per consumed event type, six rows of section 12.4, version label as a field; GAP-0508 resolved, ASM-0700) and the reference-data cross-check; a new fact is a map row and a new LOV value, not a code change. BR2 is the envelope, read once per event. BR3 is the inbox row of `rwb_source_data` and the unique key on `interaction.idempotency_key`; the library owns the first and the writer owns the second. BR4 is the writer's gap-free `caseSeq` in arrival order and the read order by `occurredAt`. BR5 is the retry topics, the `.dlt` topic, the parking with its reason and owner, and the acknowledgement rule. BR6 is the registry with BACKWARD compatibility and the version check of the consumer. The producer AsyncAPI message and registry subject are read from the producer contract; the intake does not invent a subject or field type. BR7 is the payload section of every row. BR8 is the direction of the intake: it provides no REST operation and publishes no event, and the topic of the service carries only its own two facts, which belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON.

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

| Item | Content | BR Field ID |
|---|---|---|
| Map row | `ce_type`, topic, owner, `eventCode`, literal `sourceRef`, payload fields read and accepted registered versions | DF-INT-014, DF-INT-015, DF-INT-016, DF-INT-017, DF-INT-018, DF-INT-019, DF-INT-020 |
| Envelope | `ce_id` for inbox dedupe; required `ce_idempotencykey` (at most 120) for the business key; required `ce_actor` (at most 74); `ce_time` for `occurredAt`; `.vN` suffix in `ce_type` | DF-INT-015 to DF-INT-018; DF-OPS-178 to DF-OPS-183 |
| Entry fields the intake sets | `eventCode`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `decisionLogId` for DECISION_TAKEN only; `caseSeq` is assigned by the writer | DF-INT-014 to DF-INT-020 |
| Payload fields read | `data.caseId` (uuid); row 02 `data.ownerId`, row 03 `data.fromOwner`, `data.toOwner` (user IDs; the resulting holder reference is at most 60); row 05 `data.documentId` (uuid); row 06 `data.entryId` (uuid). `caseId` is required on rows 01 to 05; the producer AsyncAPI documents give no property types or required flags (GAP-0096; ASM-0160) | DF-CAS-001; DF-INT-020 |
| Inbox | `processed_event` keyed by `ce_id`; repeat increments `hit_count` and updates `last_seen_at` | DF-OPS-178 to DF-OPS-183 |
| Personal data | None; no name, address, identity number, contact point or free text is read | No personal field is selected by this map |

The registry schema of the producer is the schema a payload is validated against; a failure is `SCHEMA_INVALID`. No other payload field is read. The map artefact is `contract/ledger-intake-map-v1.yaml`; a breaking change publishes `contract/ledger-intake-map-v2.yaml` and version 1 stays published until its consumers have moved. `documentId` has no column in Physical Schema v9 (NEW-GAP-S8-12).

### 12. Contract

#### 12.1 REST operations provided

None. This baseline documents an event intake, not a REST operation. The write the listener makes is the in-process `InteractionLedgerWriter` of RWB-P1-E1066-APP, and the read operations of the ledger are RWB-P1-E1066-CON's.

#### 12.2 REST operations consumed

None across a service boundary. The intake calls `InteractionLedgerWriter` in process (RD-P1-007 rule 1), stubbed in 12.8; its request values are those of `InteractionRequest`, and no user token or case-record right applies to the in-process call.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON (RD-P1-022). The intake publishes no event and writes no outbox row.

#### 12.4 Events consumed

| Row | `ce_type` | Topic | Owner | `eventCode` | `sourceRef` | Payload fields read / extra mapping | Accepted versions |
|---|---|---|---|---|---|---|---|
| 01 | `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_CREATED | `EV-01 CaseCreated` | `data.caseId` required | Current and previous registered; currently `.v1` only |
| 02 | `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_ALLOCATED | `EV-02 CaseAllocated` | `data.caseId`; `data.ownerId` maps to `toHolderRef=USER:<ownerId>` | Current and previous registered; currently `.v1` only |
| 03 | `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_TRANSFERRED | `EV-04 CaseTransferred` | `data.caseId`; `data.fromOwner` maps to `fromHolderRef=USER:<fromOwner>`; `data.toOwner` maps to `toHolderRef=USER:<toOwner>` | Current and previous registered; currently `.v1` only |
| 04 | `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 rwb-case | CASE_ESCALATED | `EV-19 TimerBreached` | `data.caseId` required | Current and previous registered; currently `.v1` only |
| 05 | `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | DOCUMENT_ATTACHED | `EV-16 DocumentStored` | `data.caseId`; `data.documentId` maps to `documentId` | Current and previous registered; currently `.v1` only |
| 06 | `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | DECISION_TAKEN | `EV-08 DecisionRecorded` | `data.caseId`; `data.entryId` maps to `decisionLogId`; `approver` not read | Current and previous registered; currently `.v1` only |

For all six rows, `sourceSystem=WORKBENCH`, `occurredAt=ce_time`, `caseId=data.caseId` and `idempotencyKey=ce_idempotencykey`. `ce_actor` is required and has form `USER:<userId>` | `SERVICE:<service name>` | `PARTNER:<partnerCode>` (at most 74). `actorType` is its prefix before the first colon; `actorRef` is the remainder (at most 64). `ce_idempotencykey` is the RD-P1-007 rule 4 business key (at most 120); `ce_id` is used only to dedupe the inbox. rwb-document and the decision-record library add both required headers. No personal field is read; `summary`, `channel` and `direction` stay empty. No routing uses `ce_source`. Row 06 turns every decision record with `data.caseId` into an entry. Reads (case record, data product, customer and authorise checks) are written to the access log only and publish no DecisionRecorded, so only decisions under DP-03 reach row 06 (RD-P1-072). Rows 05 and 06 depend on the two headers that the AsyncAPI documents of rwb-document and the decision record already declare.

Any other `ce_type` on the three topics is committed and ignored without an inbox row or entry. Row 06 without `data.caseId` is committed and ignored. Missing `data.caseId` on rows 01 to 05 is non-retryable and sent directly to `<topic>.dlt`.

Version is the `.vN` suffix of `ce_type` and the registry subject. The intake accepts current and previous registered versions. All six current types are `.v1` only; use an unregistered synthetic type such as `rwb.case.CaseTransferred.v9` in a refusal fixture. One consumer group per topic uses working ID `rwb-source-data.<topic>` (NEW-ASM-A2); RWB-P1-E1066-OPS deploys the groups. This service does not consume `rwb.source-data.events.v1`. The difference from Architecture v5 slide 15 is recorded as NEW-ASM-X1.

Transient database and case-read-timeout failures retry after 1 min, 10 min and 1 h, then park to `<topic>.dlt`. Missing `ce_actor` or `ce_idempotencykey`, unsupported version, missing `data.caseId` on rows 01 to 05 and payload schema failures go directly to `.dlt`. Each parked record preserves the original message and `ce_*` headers and adds `rwb-dlt-reason` (`MISSING_ATTRIBUTE` | `UNSUPPORTED_VERSION` | `SCHEMA_INVALID` | `RETRIES_EXHAUSTED`), `rwb-dlt-consumer=rwb-source-data` and `rwb-dlt-owner=P1 squad`. One alert is raised per record. `LEDGER_WRITE_FAILED` with MSG-P1-022 is raised only for `RETRIES_EXHAUSTED`; the writer never raises it for an intake call. Replay through the platform tool adds one entry and leaves earlier entries intact.

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
| `rwb.case.events.v1` fixtures | CaseCreated, CaseAllocated, CaseTransferred and TimerBreached at current `.v1`; a synthetic unregistered `CaseTransferred.v9`; missing `ce_actor`, `ce_idempotencykey` and `data.caseId` cases | Listener and contract checks |
| `rwb.document.events.v1` fixtures | DocumentStored with `data.caseId` and `data.documentId`; missing required headers | Listener and contract checks |
| `rwb.decision-record.v1` fixtures | `rwb.decision.DecisionRecorded.v1` with `data.caseId` and `data.entryId`; one message without `data.caseId`; `approver` is not read | Listener and contract checks |
| Ignored event fixtures | `CaseStateChanged`, `CaseAllocationFailed` and `DocumentFieldsExtracted` on the consumed topics | Listener and contract checks |
| Writer stub | `InteractionLedgerWriter` interface fake: appended, business key already stored, case not found, validation refusal, database failure, case read timeout; retry for the last two, pending handling for the two refusals (NEW-GAP-S8-11) | Listener and contract checks |
| Inbox fixture | `processed_event` with `ce_id`, `hit_count=1`, and a redelivery result with `hit_count=2` plus updated `last_seen_at` | Dedupe contract checks |
| DLT fixture | Original event and `ce_*` headers plus `rwb-dlt-reason`, `rwb-dlt-consumer=rwb-source-data`, and `rwb-dlt-owner=P1 squad` | Parking and replay checks |

The fixtures are published at `fakes/rwb-source-data/5.1.0/` with the contract version 5.1.0 and map version 1 (RD-P1-011): for each of the six rows `contract/fixtures/<ce_type>.json`, plus one negative fixture per rule (`CaseTransferred.v9`, missing `ce_actor`, missing `ce_idempotencykey`, missing `data.caseId`, decision record without a case, three ignored types). Consumers (RWB-P1-E1067-APP, RWB-P3-E1067-APP, RWB-P5-E1067-APP) state these versions. Fixtures validate against the producer AsyncAPI message named in each map row; producer contract checks catch removed or retyped read fields.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed across a service boundary | The write is the in-process `InteractionLedgerWriter` (RD-P1-007) |
| Kafka | None published, 6 consumed | Three owner topics, CloudEvents 1.0, key caseId, inbox dedupe, retry topics and `.dlt` (DP-09) |
| Temporal | None | No workflow, activity or Schedule in this baseline |
| File | None | No file in this baseline; the fixtures are test artefacts |

### 13. Solution plan

**Deliverables.** `contract/ledger-intake-map-v1.yaml` (the versioned map, one row per consumed event type), `contract/ledger-intake-rules.md` (the version, dedupe, order and failure rules of sections 12.4 and 8), the event fixtures under `contract/fixtures/`, the writer stub and the contract tests of section 16. The map's JSON Schema is published beside it.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | In-process writer call; the writer's one hop to rwb-case | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The patterns are used, not delivered here: the dependency column is the one the app story of this legacy key carries, and this baseline has no build dependency of its own (§R5.7). DP-18 fixes the owner of the ledger and DP-01 the schema the entries live in; DP-09 and DP-03 fix the two platform envelopes the intake reads; DP-07 fixes the list the entry codes come from; DP-11 applies to the writer's case read; DP-15 is the sequence the inbox objects arrive on; DP-19 is the route of the screen that shows the entries, which this baseline does not touch.

**Build steps**

1. The map skeleton with its version label, its row schema and the six rows of section 12.4; schema lint in the pipeline.
2. The actor and payload sections per row, with the no-personal-data check (AC2).
3. The version rule per row, with current `.v1` and synthetic unregistered `.v9` fixtures (AC3).
4. The dedupe rule and the inbox hit count, with the repeated-id fixture (AC4).
5. The order and failure rule, with arrival order, the retry topics, the `.dlt` and the parking reasons (AC5).
6. The six event fixtures and the writer stub, each fixture validated against its row (AC6).
7. The contract tests of section 16; a drift between a fixture and its row fails the build.
8. Baseline tag and the sign-off note of the listener story and the three producing teams.

**Done when.** The map validates in the pipeline, the contract tests of section 16 pass, the six fixtures produce exactly the entry event codes of their rows, and RWB-P1-E1067-APP has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The append fails on the last attempt, carried on the incident and the `.dlt` record | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| `rwb-dlt-reason` | Missing attribute; unsupported version; schema failure; retries exhausted | `MISSING_ATTRIBUTE`, `UNSUPPORTED_VERSION`, `SCHEMA_INVALID`, `RETRIES_EXHAUSTED` |
| Pending | The writer finds no case | Reason value and routing pending (NEW-GAP-S8-11) |

The message text is the legacy text of RWB-E1-067, unchanged, and Thai text for each message follows decision DL10. DL10 (owner: Business lead with Legal and Compliance) is worked on the recommended option A of the decision log: the business lead drafts per module one epic ahead, and Legal and Compliance approve. The decision log gives this position while the Thai names are outstanding: screens go to UAT with English labels and the standard Thai message only. The reason values are contract elements of the intake: the `.dlt` record carries them in `rwb-dlt-reason`, with `rwb-dlt-consumer` and `rwb-dlt-owner`, and the listener writes no other reason. The access refusal of the append (MSG-P4-002) belongs to RWB-P1-E1066-APP.

### 15. Screens and states

No screen in this baseline (DP-19). The entries the intake writes are read by the case owner through the case timeline of rwb-case (`GET /cases/{caseId}/interactions`), whose screen is the screen owner's; a parked record is on `<topic>.dlt`, with the dead-letter alert to the platform administrator, and is not an exception queue screen item. This baseline adds no route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1067-CON-16 | AC1, BR1 | Contract | Map validates; six rows and topics; ignored type |
| TC-P1-E1067-CON-01 | AC2, BR2 | Contract | Actor, key and payload fields per row |
| TC-P1-E1067-CON-17 | AC3, BR6 | Component | Current `.v1` accepted; synthetic `.v9` parked |
| TC-P1-E1067-CON-02 | AC4, BR3 | Contract | Redelivered `ce_id`; shared business key |
| TC-P1-E1067-CON-18 | AC5, BR4, BR5 | Component | Arrival order; retry topics and `.dlt` |
| TC-P1-E1067-CON-03 | AC6 | Contract | Nine sub-tables, six fixtures and drift |
| TC-P1-E1067-CON-04, TC-P1-E1067-CON-07 | AC7 | Contract | Tables written by the intake |
| TC-P1-E1067-CON-05, TC-P1-E1067-CON-08 | AC8 | Contract | Unspecified fields carry the gap ID |
| TC-P1-E1067-CON-09 | AC9 | Component | One writer call per fixture; nothing published |
| TC-P1-E1067-CON-10 to TC-P1-E1067-CON-15 | AC10 to AC15 | Contract | Producer messages, writer stub, parked and ignored records |

The legacy cases TC-P1-E1067-APP-09 to TC-P1-E1067-APP-13 are run by RWB-P1-E1067-APP, which owns their criteria; TC-P1-E1067-APP-14 is the access check of the append (RWB-P1-E1066-APP).

### 17. Guardrails

- No business value in the contract: the entry event code of a row is a LOV value, the retry intervals and the accepted versions are configuration (DP-07).
- No personal data in the map, a fixture or an example: IDs, codes, dates and amounts only; a row that names a personal field fails the data-steward check (BR7).
- The baseline names only rwb-source-data's tables and only events owned by other services; it documents no event of its own as consumed (DP-01, DP-09).
- One intake map and one row per consumed type: a second map, or a row without an owner, fails the review.
- Every fixture is synthetic; no production payload is copied into a fixture or a stub.
- The CloudEvents envelope, the inbox shape and the retry rule come from the platform library; this baseline narrows them but never redefines them.
- The map is forward only: a corrective change is a new version of the map, never an edit of a baselined one (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | The six rows of 12.4 and their entry event codes | TC-P1-E1067-CON-16, TC-P1-E1067-CON-03 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The actor section and the source reference of every row | TC-P1-E1067-CON-01 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | The dedupe contract of 12.4 and 12.7 | TC-P1-E1067-CON-02 |
| NFR-026 | A consumer retries, then parks the event with its owner | The retry topics, the `.dlt` and the parking reasons | TC-P1-E1067-CON-18 |
| ADR-020 | Contract-first interfaces | The versioned map, the fixtures and the writer stub | TC-P1-E1067-CON-03 |

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
- The format of the map beyond its row content and version label, settled at the baseline review (ASM-0700).

### Remaining delivery steps

- Size the story at refinement; owner: squad.
- Obtain epic design sign-off; owner: product owner.
- Publish the map, its JSON Schema and the fixtures; owner contract owner.
- Rule the intake handling of non-transient writer refusals; owner solution architect; NEW-GAP-S8-11.
- Obtain the producer header additions on the document and decision-record events; owner contract owner.
- Add or update story tests in Test Cases v9 (W2-tests); owner: test writer.
- Run the required test data in DEV after implementation; owner: delivery team.
