# RWB-PLT-E1027-APP Decision log writer v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split (rework) of RWB-E1-027 for the platform library RWB-PLT-LIB. The local decision-record library that every service calls inside its own transaction is delivered here; the central ledger stays with RWB-P7-E1027-APP and the end-to-end proof with RWB-ITG-E1027-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-PLT-LIB-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

### 1. Story

As the **case workflow module's developer**, I want **one library that validates a decision record against the seven field groups, refuses an incomplete record, writes it to the caller's own `decision_record` table in the caller's transaction, hash-links it to the previous record of that service, ignores a repeated idempotency key and publishes `DecisionRecorded` through the caller's outbox in the same transaction**, so that **no action proceeds without its record and every service keeps its records in its own schema instead of one shared table**.

### 2. Business rationale

The legacy story gives every module one published writer, `DecisionLogWriter`, that validates a record against the seven field groups, writes it in the caller's transaction and publishes `DecisionRecorded` (legacy sections 1, 4 and 12). In the target the writer is not application code inside one module and its table is not one table in the `recovery` schema. Architecture v5 slide 20 says what every service does from the service template and the shared libraries: it writes its own decision records locally — "Own schema: business tables + outbox + inbox + decision_record" — and publishes `DecisionRecorded` to `rwb.decision-record.v1`; slide 28 adds that the record is saved with the change in one transaction, chained to the one before, and collected centrally by rwb-decision within 5 minutes, with strict mode only for points of no return. ADR-022 turns that into one decision: a local decision record plus a central ledger.

**The division of the legacy key is fixed.** This WP delivers the **local decision-record library** that every service calls inside its own transaction. The **central ledger** — the `rwb_decision` store, the continuous Kafka ingest (JOB-13), the hash-chain check (JOB-14) at 02:00 and the two read operations `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}` — is **RWB-P7-E1027-APP**, and the **end-to-end proof** across the library and the ledger is **RWB-ITG-E1027-ITG**. The legacy acceptance criteria **AC1 to AC7 stay with RWB-P7-E1027-APP** and are not copied into this story: every criterion in section 7 is new (D-RCV-60) and tests only the library deliverable in this title. The contract of the library is RWB-PLT-E1027-CON, the P7 contract behind the ledger is RWB-P7-E1027-CON, and this story carries no legacy AC.

What the library adds over the legacy writer is exactly what the split requires. The table it writes is created in the caller's own schema by the caller's own Flyway sequence under the caller's own login, because a service never reads or writes another service's tables (DP-01, DP-15, Architecture v5 slide 29). It keeps the hash chain inside each service: `chain_seq`, `prev_hash` and `entry_hash` are per service schema, append-only, so a gap or an edit shows locally and the ledger can be checked against the producers (Temporal and Drools Design slide 16; Architecture v5 slide 28). It publishes through the caller's outbox in the same transaction, so nothing is lost if Kafka is down and nothing is published for a transaction that rolls back (DP-09, Architecture v5 slide 22). It writes no data-lake copy: the legacy RWB-E1-014 copy is retired and the library publishes to the topic only (DP-17, ADR-018).

The guarantees the legacy story measured are unchanged: a decision without its record does not happen, an incomplete record is refused with the missing field named, a repeated event gives one record, and a refused or failed write stops the caller's action and raises an incident (REQ-DRI-004, REQ-DRI-005, CTL-06, R-UNI-39, R-UNI-40, NFR-034). The measure stays decisions with a record: target 100 percent and no action without one.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the interfaces, the record shape, the DDL template of `decision_record`, the `DecisionRecorded` envelope, the transaction and idempotency rules, the versioning rule and the fakes (section 12).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library (DP-06, DP-07); RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the rwb-case contracts behind them, and the decision code list and the approval-level list are values in force there, never constants in the library.
- RWB-PLT-TE006-CON is published: the `OutboxWriter` whose `publish` the library calls in the caller's transaction (DP-09).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit, so that the caller's activity runs on its own queue and a workflow class never calls the library (DP-10).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions that apply the DDL template in each service's own schema (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19); no screen is in scope here.
- RWB-P7-E1027-CON is published and consumed at a pinned version: the central ledger contract behind `rwb.decision-record.v1` and the two ledger reads this story names and does not implement.
- Each consuming service has its own schema and login, and its own `decision_record` exists before its first write; which per-service database story applies each copy is Not specified in the source documents (GAP-1402; ASM-2440).
- The shared topic `rwb.decision-record.v1` exists with its retry and dead-letter topics and the schema-registry entry of `rwb.decision.DecisionRecorded.v1`; the topic itself belongs to RWB-PLT-EVT.
- The library artefact coordinates — the group, the artefact name and the publication channel it is released under — are Not specified in the source documents (GAP-1402; ASM-2440); the library keeps the legacy interface shapes and the Java package family of the platform baseline.
- No approval stop is required for a Draft story: the release date 30 November 2026 is tentative, and the build starts on Day 1 against the contract and its fakes.

### 4. Flow

1. A calling service — rwb-case for case created, owner assigned and case transferred, rwb-document for document attached, and the sixteen other services for their own decisions — assembles a `DecisionRecord` from the values it already holds: idempotency key, case ID where there is one, decision code, the version group, inputs reference, recommendation, approver and approval level, final call, actions, outcome, actor reference and decided-at, inside its own transaction.
2. The caller calls `DecisionRecordWriter.record(record)` as the last step before commit, from its own activity on its own task queue.
3. The library checks that a transaction is open. The method is declared `@Transactional(propagation = MANDATORY)`; called with no open transaction it throws `IllegalTransactionStateException` and writes nothing (legacy AC6 behaviour).
4. The library checks the idempotency key in the caller's own `decision_record`, under the unique key on that column. A key already present returns the first entry reference with `repeated` true, increments the metric `decision_log_repeats_total` and writes nothing.
5. `DecisionRecordValidator` checks the seven field groups of section 8: the decision code against the list in force read through the reference-data client, the subject, the version group, the inputs reference, the recommendation and final call, the approver with an approval level, and the actor with the decided-at time. A missing or invalid value refuses the record with `MSG-P7-009` naming the field.
6. The library appends one row to `decision_record` in the caller's own schema: `chain_seq` is the highest `chain_seq` of that schema plus one, `prev_hash` is the `entry_hash` of that previous record, and `entry_hash` is computed over the row content and `prev_hash`. The table is append-only; the library exposes no update and no delete.
7. The library writes `rwb.decision.DecisionRecorded.v1` into the caller's outbox through `OutboxWriter.publish`, in the same transaction, with the record key `caseId` where the record has a case and the entry id where it does not.
8. The caller commits: the action, the record and the outbox row are stored together, or none of them. The outbox relay publishes the event later; the library itself publishes nothing.
9. A refused record raises `DecisionLogRecordInvalidException` with `MSG-P7-009`; a failed append raises `DecisionLogUnavailableException` with `MSG-P7-003`; in both cases the caller's transaction rolls back and an incident reaches the platform administrator queue through the service's own alerting.
10. The record is collected into the P7 central ledger from the shared topic asynchronously, within the 5-minute completeness target; only a point of no return waits for the ledger confirmation in strict mode, and that wait is the caller's business, not the library's.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record misses the version group, the inputs reference, the final call, the decided-at time, the actor or the decision code | Refused; the library logs the case ID and the missing field only; the caller's action rolls back | MSG-P7-009 | AC2 |
| X2 | A record carries a rule ID with an empty rule version | Refused as X1, with the field named as `ruleVersion` | MSG-P7-009 | AC3 |
| X3 | A record carries a decision code not in the list in force | Refused as X1, with the field named as `decisionCode` | MSG-P7-009 | AC1, AC2 |
| X4 | The append fails, for example the table is unavailable or the chain link cannot be read | The caller's action rolls back; an incident reaches the platform administrator queue | MSG-P7-003 | AC6 |
| X5 | The library is called with no open transaction | Refused with `IllegalTransactionStateException`; nothing is written and nothing is published | None | AC4 |
| X6 | The same idempotency key arrives twice | One record; the first entry reference is returned and the repeat counted | None | AC5 |
| X7 | The caller's transaction rolls back after the record was written | The record and the outbox row disappear with the transaction; no event is published | None | AC7 |
| X8 | A class outside the library tries to write `decision_record` | The architecture test fails the build; no second write path is accepted | None | AC8 |

An access event carries no case, so its record has no subject group; the actor, the decision code, the version group where one applies, the inputs reference, the final call and the decided-at time are still required (legacy BR2). The incident queue name and its routing key are Not specified in the source documents (GAP-1402; ASM-2441); the library raises the incident through the calling service's own alerting rather than opening an alert channel of its own.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the seven platform contract stories and the P7 ledger contract; the callers are other services and are reached only through the published contract and its fake |
| Negotiable | The artefact coordinates and the incident route are open until the library baseline is published; the record shape, the transaction rule, the idempotency rule and the envelope are fixed by RWB-PLT-E1027-CON |
| Valuable | Gives all 19 services one validated, chained, transaction-bound record writer from Day 1 and removes a shared decision table from every service plan |
| Estimable | One published interface, one validator, one append with the chain, one outbox call and the architecture test |
| Small | Fits one sprint with its tests |
| Testable | Each criterion is one component, contract or NFR test on an observable: a committed row, a refusal message, an outbox row or a build failure |

### 7. Acceptance criteria

```gherkin
Feature: Local decision-record library

  Background:
    Given the environment is DEV with synthetic data
    Given the decision code list and the approval-level list in force are read through the parameters and reference-data clients
    Given the platform library contract is published with major version 1

  Scenario: AC1 A complete record is written in the caller's transaction (new, D-RCV-60)
    Given a caller inside an open transaction with case "RW-2026-000123" and a complete record
    When it calls DecisionRecordWriter.record as the last step before commit
    Then one decision_record row exists in the caller's own schema with decision code "D6", final call "OWNER_ASSIGNED", rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11" and an inputs reference
    Then the row is visible to the caller inside the transaction and is visible to every reader after the commit
    Then no other schema holds a copy of the row

  Scenario: AC2 A record with no version group is refused (new, D-RCV-60)
    Given a decision record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version
    When it is written
    Then DecisionRecordValidator refuses it with message MSG-P7-009 naming "versions"
    Then the library logs the case ID and the missing field only, never the record body
    Then the caller's transaction can only roll back and no row exists

  Scenario: AC3 A rule ID with an empty rule version is refused (new, D-RCV-60)
    Given a decision record with rule ID "R-UNI-14" and an empty rule version
    When it is written
    Then the library refuses it with message MSG-P7-009 naming "ruleVersion"
    Then no row is written and no event reaches the outbox

  Scenario: AC4 A call with no open transaction is refused (new, D-RCV-60)
    Given a caller with no open transaction
    When it calls DecisionRecordWriter.record
    Then the call is refused with IllegalTransactionStateException
    Then nothing is written in any schema and no outbox row exists

  Scenario: AC5 A repeated idempotency key gives one record and a counted repeat (new, D-RCV-60)
    Given a decision record for event "EV-7f3a-0001" on document "DOC-2026-0009981" was written and committed
    When the same idempotency key "EV-7f3a-0001" arrives again
    Then one decision_record row exists for the key
    Then the library returns the first entry reference with chain sequence and entry hash, and the repeat flag is true
    Then decision_log_repeats_total is one higher

  Scenario: AC6 A failed append rolls the caller's action back and raises the incident (new, D-RCV-60)
    Given the append of the record fails inside the caller's transaction
    When the caller attempts to commit its action for case "RW-2026-000124"
    Then the write raises DecisionLogUnavailableException with message MSG-P7-003
    Then the caller's action is rolled back and the case keeps the state it had
    Then an incident reaches the platform administrator queue through the caller's own alerting

  Scenario: AC7 DecisionRecorded is in the outbox of the same transaction (new, D-RCV-60)
    Given a complete record written in the caller's transaction
    When the transaction commits
    Then one rwb.decision.DecisionRecorded.v1 outbox row exists in the caller's own schema with the record key "caseId"
    And when another transaction writes the record and then rolls back
    Then no outbox row exists for that record and no event is published

  Scenario: AC8 The chain columns are written and only the library writes them (new, D-RCV-60)
    Given the DDL template of decision_record applied in a service's own schema
    When a second record is written in the same schema
    Then the second row carries chain_seq two, prev_hash equal to the first row's entry_hash and its own entry_hash
    Then the table refuses an update and a delete
    Then the architecture test fails the build when a class outside the library writes decision_record
```

These criteria are new: no legacy acceptance criterion is copied here. **AC1 to AC7 of RWB-E1-027 stay with RWB-P7-E1027-APP**, the central ledger, and the cross-service run of the same records is RWB-ITG-E1027-ITG. Every value used above is the legacy story's own — case `RW-2026-000123`, case `RW-2026-000124`, event `EV-7f3a-0001`, document `DOC-2026-0009981`, rule `ALLOC-MTG-BKK-01` with version `ALLOC-2026.11`, rule `R-UNI-14`, decision code `D6`, final calls `OWNER_ASSIGNED` and `CASE_TRANSFERRED` — and no value was invented.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The record is written in the caller's transaction and the caller's schema, under the caller's own login; there is no record without the change and no change without the record | Principle 5; R-UNI-39; CTL-06; REQ-DRI-005; DP-01 |
| BR2 | The seven field groups are all required except the subject of an access event: the decision code from the list in force, the subject case, the version group, the inputs reference, the recommendation and final call, the approver with an approval level, and the actor with the decided-at time | DF-DEC-002, DF-DEC-003, DF-DEC-008, DF-DEC-010, DF-DEC-011, DF-DEC-012, DF-DEC-016; legacy BR2, BR4 |
| BR3 | The version group needs at least one of rule version, model version and agent version, except for access events, which carry no case; a rule ID needs its rule version, and the version written is the package version label | DF-DEC-004 to DF-DEC-007; NFR-034; D-RCV-36; Temporal and Drools Design slide 16 |
| BR4 | The decision code is checked against the list in force read through the reference-data client and the parameters client, never against a constant in the library | Principle 1; REQ-DRI-004; DP-06; DP-07; legacy BR7 |
| BR5 | A refused record and a failed append both stop the action: the library raises, the caller's transaction rolls back and an incident reaches the platform administrator queue | REQ-DRI-005; R-UNI-39; MSG-P7-009; MSG-P7-003 |
| BR6 | The same idempotency key gives one record; the first entry reference is returned and the repeat is counted in `decision_log_repeats_total` | R-UNI-40; legacy BR6 |
| BR7 | The record is hash-chained inside its own schema: `chain_seq`, `prev_hash` and `entry_hash`, append-only, no update path other than the chain check of P7 | Architecture v5 slide 28; Temporal and Drools Design slide 16 |
| BR8 | `DecisionRecorded` is written to the caller's outbox in the same transaction, on the shared topic, with the record key `caseId` where the record has a case and the entry id where it does not | DP-09; ADR-015; Architecture v5 slides 20 and 42; GAP-1402; ASM-2442 |
| BR9 | No data-lake copy and no reporting copy is written: the legacy copy RWB-E1-014 is retired and the only copy outside the caller's schema is the P7 ledger entry | DP-17; ADR-018; Template and Rules §R6 |

### 9. State transitions

None for a case: the library changes no case status. It makes a status change made by another service depend on its record — when the write fails, the case keeps the status it had. The record itself has the states below, and they are the vocabulary the tests and the incident report use.

| Object | State | Meaning |
|---|---|---|
| Decision record | Unwritten | The caller has opened the transaction and not yet called the library |
| Decision record | Validated | The seven field groups passed and the idempotency key is new |
| Decision record | Written in the transaction | The row is appended with its chain link and is visible inside the caller's transaction |
| Decision record | Committed | The caller committed; the action, the row and the outbox row are stored together |
| Decision record | Refused | A field group failed; nothing is stored and the field is named |
| Decision record | Repeated | The key already existed; the first entry reference is returned and the repeat counted |
| Decision record | Chained | The row carries `chain_seq`, `prev_hash` and `entry_hash` of its own schema |
| DecisionRecorded | Published | The caller's outbox relay published the event on the shared topic |
| DecisionRecorded | Absent | The caller's transaction rolled back; no outbox row and no event exist |
| Central ledger entry | Ingested | P7 consumed the event into `rwb_decision`; not this story's state, named for the boundary |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform library team, owning the template | Owns the interface, the validator, the chain rule and the architecture test; changes them only through the library contract story |
| The owning service of each caller — rwb-case, rwb-document and the sixteen other services | Builds the record from its own values and calls the library as the last step before commit; owns the action that the record guards |
| RW-PLATADM, platform administrator | Receives the incident when a record is refused or cannot be written |
| RW-AUDIT, RW-COE, RW-COMPLY and every role holding Decision log R | Read the records through the P7 contract and the central ledger; no read path through this library |
| RW-DATASTEW | Owns the decision code list and the approval-level list values that the library reads as values in force |
| No role | Writes `decision_record` outside the library, or writes another service's `decision_record` |
| No approval level from the delegation of authority applies | The library records the decision; it takes none |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_record (local library object in each service's own schema) | the record fields of the seven field groups | Write |
| DF-DEC-030 | decision_record | actor_user_id | Write |
| DF-DEC-031 | decision_record | idempotency_key | Write, read |
| DF-DEC-004 to DF-DEC-007 | decision_record | rule version, model version, agent version and rule ID | Write |
| DF-REF-028 | lov_value (P3 rwb-case reference data in the target) | lov_code | Read through the reference-data client |
| DF-REF-029 | lov_value (P3 rwb-case reference data in the target) | value_code | Read through the reference-data client |
| Chain columns | decision_record | chain_seq, prev_hash, entry_hash | Write |
| Case subject | decision_record | case_id | Write, null for an access event |
| Outbox row | outbox_event (RWB-PLT-TE006-CON) | event_type, case_id, payload, idempotency_key | Write through the outbox library, in the caller's own schema |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-027 unchanged. The record columns named on the Temporal and Drools Design slide 16 are `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash` and `entry_hash`; the legacy story adds `decisionCode`, the case, `actorUserRef` and `idempotencyKey`. `decision_log_entry` is **not** this story's table: it is the P7 central ledger in `rwb_decision` and is written only by P7. The column widths and the rest of the local table shape are published by RWB-PLT-E1027-CON and are Not specified in the source documents (GAP-1402; ASM-2441). No personal data is held: the actor is a reference, and the record holds codes and identifiers.

### 12. Contract

#### 12.1 REST operations provided

None — the library is in process and publishes no REST surface. The two ledger reads belong to P7 rwb-decision under `/api/recovery/decision/v1` and are named in section 19, not provided here.

#### 12.2 REST operations consumed

None directly — the library is in process. It reads the decision code list and the approval-level list through the parameters and reference-data client libraries, whose REST consumption and timeout budget belong to RWB-PLT-E1042-CON and RWB-PLT-E1043-CON.

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 (shared topic) | `caseId` where the record has a case; the entry id where it does not | entry id, case ID where there is one, decision code, final call, rule ID, rule version, chain sequence, entry hash, actor reference | Announces the record to the P7 central ledger and to rwb-reporting, written to the caller's outbox in the same transaction |

The envelope is CloudEvents 1.0 in binary mode with `ce_specversion` 1.0, `ce_id`, `ce_type` `rwb.decision.DecisionRecorded.v1`, `ce_source` as the producing service, `ce_subject`, `ce_time` and the W3C trace header; the payload carries identifiers and facts only. The record key for a record with no case is Not specified in the source documents (GAP-1402; ASM-2442); the library publishes it under the entry id so that the ledger can correlate the announcement with the record, and the P7 ingest accepts both keys.

#### 12.4 Events consumed

None — the library consumes no event. The records it writes are read by the P7 chain check through its own contract, which is not a subscription of this story.

#### 12.5 Workflows and activities

None — the library is called from inside the caller's own activity, on the caller's own task queue, and it starts no workflow and no activity. A workflow class never calls the library, so replays reuse the recorded decision (DP-10).

#### 12.6 Schedules

None — the legacy JOB-14 chain check runs as a P7 Schedule at 02:00 and is not this story's (RWB-P7-E1027-APP).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT | Library object created in each service's own schema by the library DDL template; append-only; `chain_seq`, `prev_hash` and `entry_hash` per schema; unique key on `idempotency_key`; `case_id` null for an access event |
| outbox_event | PLT | The caller's outbox row, written through RWB-PLT-TE006-CON in the same transaction and the same schema |

`decision_record` is a platform library object created in each service's own schema under the Ownership Map ruling, not one table in a shared schema; a service applies the template through its own Flyway sequence, under its own login, and no key crosses a schema boundary (DP-01, DP-15). `decision_log_entry` stays P7's: it is the central ledger table in `rwb_decision`, named here and neither created nor written by this library.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Caller fakes of rwb-case and rwb-document | The calling services of the four Epic 1 records | A caller that writes case created, owner assigned, case transferred and document attached in its own transaction, and a caller that rolls back after the write (AC1, AC6, AC7) |
| Reference-data and parameters fakes | `DecisionRecordValidator` behind the two clients | The decision code list with `D6` and without `D99`, the approval-level list, and a read that fails (AC1, AC2) |
| Outbox fake | `OutboxWriter` of RWB-PLT-TE006-CON | A publish that records the row in the caller's transaction and a publish that throws (AC7) |
| Ledger fake | The P7 contract of RWB-P7-E1027-CON | One ledger entry per event, for the correlation assertion of AC7 (AC7) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The library is in process; the two client libraries consume the rwb-case operations |
| Kafka | One event type published through the caller's outbox | `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, key `caseId` or entry id |
| Temporal | None | Called inside the caller's activity; starts no workflow and owns no queue |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Shared library artefact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.decisionrecord`; the published interfaces sit in `th.co.scb.ace.workbench.recovery.platform.api`; the DDL template is a resource applied by each service's own Flyway sequence. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1402; ASM-2440).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The record is written into the caller's own schema and no service reads another's | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. This story is that library | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the decision code per event is a parameter read as a value in force | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the decision code and approval-level lists are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. `DecisionRecorded` leaves through the caller's outbox in the same transaction | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the library is called in the caller's activity and the chain check stays a P7 Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the callers and the ledger are reached through published contracts, never in process across a service boundary | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the library adds no path and the ledger reads stay under the decision base | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the `decision_record` template is applied by each service's own sequence | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The legacy copy of the decision log is retired, so the library publishes to the topic only | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the ledger view for a screen is out of scope | H RWB-PLT-N001-CON |

**Hardware and software change.** The decision record moves from one `decision_log_entry` table in the monolith's `recovery` schema to a library object created in each of the 19 service schemas, written inside the caller's transaction, chained inside that schema and announced on the shared topic through the caller's outbox. The legacy writer became a library instead of a module service; the central log became the P7 ledger in `rwb_decision`; the data-lake copy and its job are removed. No new hardware is implied: the library runs in each service's own pods on the existing AKS cluster, the rows sit in the existing ACE PostgreSQL server under each service's own login, and the events use the Kafka platform ACE already runs.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionRecordWriter` | Published interface | `record(DecisionRecord)` declared `@Transactional(propagation = MANDATORY)`, returning `DecisionRecordEntryRef` and throwing the two exceptions (BR1, BR5, BR6) |
| DecisionRecordWriterService | Service | Transaction check, idempotency check, validation, chain append, outbox write (BR1, BR5, BR6, BR7, BR8) |
| `DecisionRecordValidator` | Service | The seven field groups of BR2 to BR4, with the lists read through the two clients |
| DecisionRecordChain | Service | `chain_seq`, `prev_hash` and `entry_hash` of the caller's schema; append-only append with the row lock of BR7 |
| DecisionRecordedPublisher | Service | Builds the envelope and calls `OutboxWriter.publish` in the same transaction (BR8) |
| DecisionRecordRepository | Repository | Idempotency key lookup, previous hash read and append in the caller's schema |
| DecisionRecordDdlTemplate | Resource | The DDL of `decision_record`, the unique key, the index and the append-only trigger (DP-15) |
| ArchitectureTest | Test asset | Fails the build when a class outside the library writes `decision_record` (BR7) |

**Database.** The DDL template creates, in whichever schema applies it:
- `decision_record` (id uuid primary key, entry_id uuid not null, case_id uuid null, decision_code varchar(40) not null, rule_id varchar(60), rule_version varchar(40), model_version varchar(40), agent_version varchar(40), inputs_ref varchar(200) not null, recommendation text, approver_user_id varchar(64), approval_level varchar(40), final_call varchar(40) not null, actions jsonb, outcome jsonb, actor_user_ref varchar(64) not null, decided_at timestamptz not null, idempotency_key varchar(120) not null, chain_seq bigint not null, prev_hash varchar(64), entry_hash varchar(64) not null, plus the standard columns), with `UNIQUE (idempotency_key)`, `UNIQUE (chain_seq)` and an index on `(case_id, decided_at)`.
- The append-only rule in one trigger that refuses `UPDATE` and `DELETE` on `decision_record`, and no update method in the repository.

`chain_seq` starts at one in each schema and is taken under a lock on the schema's highest chain row, so the chain is per service and a gap is visible locally; whether the chain is one per schema or one per service instance is Not specified in the source documents (GAP-1402; ASM-2440). `entry_hash` is computed over the record content and `prev_hash`; the algorithm and its salt are fixed by the CON story and shared with P7 so that the chain check can recompute it.

**Configuration and reference data.** The decision code per event, the approval-level list and the list version are read through the parameters and reference-data clients, never held in code (DP-06, DP-07). The legacy parameters `rwb.decision.code.*` and the LOV-DECISION values are the same data in the target owner's store. The repeat counter is exported as the metric `decision_log_repeats_total`. The incident route is the calling service's own alerting; its queue name and routing key are Not specified in the source documents (GAP-1402; ASM-2441).

**Build steps**

1. Publish the interface, the record type and the two exceptions from RWB-PLT-E1027-CON; test the compile and drift check of a sample caller (AC1).
2. Write the DDL template and the append-only trigger; apply it twice in two throwaway schemas and assert the unique keys and the refused update (AC8).
3. Build `DecisionRecordValidator` against the two client fakes; test the version group, the empty rule version and an unknown decision code (AC2, AC3, AC1).
4. Build the transaction check and prove the call with no open transaction (AC4).
5. Build the idempotency path with the unique key and the repeat metric (AC5).
6. Build `DecisionRecordChain` and prove two records link and the table refuses an update (AC8).
7. Add `DecisionRecordedPublisher` through `OutboxWriter` and prove the event exists with the commit and is absent after a rollback (AC7).
8. Add the failure path and prove the caller's action rolls back and the incident is raised (AC6).
9. Add the architecture test, wire the library into the service template and hand it to the wave 1 callers (AC8).

**Feature flag.** One flag per service, read as a parameter; while the flag is off the library still writes the record and the outbox row, and only the outbox relay holds the event, so nothing is lost when it is switched on.

**Done when.** The tests of section 16 pass, the contract tests of RWB-PLT-E1027-CON pass against the fakes, rwb-case and rwb-document write their Epic 1 records through the library, and the architecture test fails any writer outside the library.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary of the caller) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| decision_log_repeats_total | A repeated idempotency key is counted (metric, not a message) | No text; one increment per repeat, tagged by service and decision code |

The three texts are copied unchanged from RWB-E1-027 and this story adds no message ID. The field names the library produces are `versions` for AC2, `ruleVersion` for AC3 and `decisionCode` for an unknown code; a refused record is logged with the case ID and the field name only. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen of its own, and the library adds no route. A refused or failed record appears as an incident in the platform monitoring of the calling service, for RW-PLATADM. The records themselves are read through the P7 decision-log operations and the gateway-bff composite route (DP-19) by the roles holding Decision log R; that read path belongs to RWB-P7-E1027-APP and is out of scope here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1027-APP-01 | AC1, BR1, BR4 | Component | A caller in its own transaction with case RW-2026-000123, rule ALLOC-MTG-BKK-01 of ALLOC-2026.11, decision code D6 and final call OWNER_ASSIGNED; the row asserted in the caller's schema and absent from every other |
| TC-PLT-E1027-APP-02 | AC2, AC3, BR2, BR3 | Component | A transfer record with no version group and a record with rule ID R-UNI-14 and an empty rule version; MSG-P7-009 with the field "versions" and then "ruleVersion" |
| TC-PLT-E1027-APP-03 | AC4, BR1, BR5 | Component | The library called with no open transaction; IllegalTransactionStateException and no row and no outbox row |
| TC-PLT-E1027-APP-04 | AC5, BR6 | Component | Event EV-7f3a-0001 on document DOC-2026-0009981 written twice with the same idempotency key; one row, the first entry reference and decision_log_repeats_total raised by one |
| TC-PLT-E1027-APP-05 | AC6, BR5 | NFR | The append forced to fail for case RW-2026-000124; the caller's action rolled back, the case state unchanged, MSG-P7-003 in the log and one incident |
| TC-PLT-E1027-APP-06 | AC7, AC8, BR7, BR8, BR9 | Contract | The outbox row of the committed transaction and its absence after a rollback; two chained rows with chain_seq 1 and 2 and prev_hash of the first; a refused update; the architecture test on a writer outside the library |

The legacy test case set of RWB-E1-027 is carried by RWB-P7-E1027-APP and RWB-ITG-E1027-ITG; these six are the library's own tests and no legacy id is renumbered. The full test, with its Given, When and Then, goes into the next Test Cases version under the same id.

### 17. Guardrails

- No business value in code: the decision codes, the approval levels and the lists in force are parameters and reference rows read through the clients.
- No personal data in a record, an event, a log, a test or a prompt: the actor is a reference, the subject is a case ID, and a refused record is logged with the case ID and the field name only.
- No read or write of another service's tables: the record and the outbox row are written in the caller's own schema, and `decision_log_entry` is read only through the P7 contract.
- No write path to `decision_record` other than the library, checked by the architecture test; no update and no delete path at all.
- No retry inside the library: the caller's job or request retries, and an incident is raised instead of a silent second attempt.
- No data-lake copy and no reporting copy: the legacy copy is retired and the only copy outside the caller's schema is the P7 ledger entry.
- A published contract version is never edited in place; a breaking change is a new major version of RWB-PLT-E1027-CON.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-02, FEAT-DRI-03, FEAT-DRI-08 | 17 Run the decision center | BR1, BR2, BR3, BR4, BR6, BR7, BR8 | TC-PLT-E1027-APP-01, TC-PLT-E1027-APP-02, TC-PLT-E1027-APP-04, TC-PLT-E1027-APP-06 |
| REQ-DRI-005 | No action proceeds if its record cannot be written | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-04, FEAT-DRI-05 | 17 Run the decision center | BR1, BR5, BR9 | TC-PLT-E1027-APP-03, TC-PLT-E1027-APP-05, TC-PLT-E1027-APP-06 |
| Legacy test set RWB-E1-027 | TC-E1-027-01, TC-E1-027-02, TC-E1-027-03, TC-E1-027-04, TC-E1-027-05, TC-E1-027-06, TC-E1-027-07, TC-E1-027-08, TC-E1-027-09 | Epic 1, 3.7 | The legacy story's own features | 17 Run the decision center | The legacy rules R-UNI-39 and R-UNI-40 | Executed by RWB-P7-E1027-APP and RWB-ITG-E1027-ITG; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1027-CON | Contract | H: publishes the interface, the record shape, the DDL template, the envelope, the transaction and idempotency rules and the fakes this story implements |
| RWB-P7-E1027-CON | Contract | C: the central ledger contract behind the shared topic and the two ledger reads; owns legacy AC1 to AC7 together with RWB-P7-E1027-APP |
| RWB-P7-E1027-APP | App development | The central ledger, the ingest, the chain check and the read operations; the owner of the legacy acceptance criteria |
| RWB-ITG-E1027-ITG | Integration | The end-to-end proof of this library with the P7 ledger on real services |
| RWB-PLT-TE006-CON | Contract | H: the outbox writer and the envelope this library publishes through |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data clients the validator reads through |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit that runs the caller's activity |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence that applies the DDL template |
| RWB-PLT-N001-CON | Contract | H: the gateway route the ledger view will use |
| RWB-PLT-DB, the per-service DB stories | Database | X: create each service's schema, login and grants and apply the template |

### 19. Out of scope

- The central ledger, the continuous ingest (JOB-13), the hash-chain check (JOB-14) and the two read operations `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}`: RWB-P7-E1027-APP and RWB-P7-E1027-CON.
- The producer callers and their values — rwb-case for case created, owner assigned and case transferred, rwb-document for document attached, and the sixteen other services for their own decisions: their own APP stories.
- The `decision_record` store in each service's schema, the login and the grants: the per-service database stories and RWB-PLT-DB.
- The copy of the decision log to the data lake: retired with RWB-E1-014, no target path (DP-17).
- The access-event writer and its record content: P4 rwb-access, RWB-E1-039.
- Approval records with the limit applied: RWB-E2-013.
- The recommendation service with the reasons for the route decision: Epic 4.
- The outbox relay, the retry topics and the dead-letter topic themselves: RWB-PLT-TE006-APP and RWB-PLT-EVT.
