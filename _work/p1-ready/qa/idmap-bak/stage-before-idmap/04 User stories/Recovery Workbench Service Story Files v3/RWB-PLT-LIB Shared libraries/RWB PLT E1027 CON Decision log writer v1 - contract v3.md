# RWB-PLT-E1027-CON Decision log writer v1 - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Specified the local rwb_source_data migration and the decision event’s business-key derivation. Backfilled 4 mapped v9 test case IDs. RD-P1-068.
- Envelope gains the required headers `ce_idempotencykey` and `ce_actor` (RD-P1-009; finding #1; BR11, AC11, AC12).
- Type `rwb.decision.DecisionRecorded.v1` was already stated; ASM-0209 noted as confirmed (RD-P1-008; #2). Payload wire names `entryId`, `caseId`, `decisionCode` and the rwb-source-data consumer added (#5).
- The business-key derivation and the rwb_source_data migration follow RD-P1-068. The shared DDL publication remains pending under NEW-GAP-F08-7.

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-027 for the platform library RWB-PLT-LIB. The local decision-record contract is published on Day 1; the central ledger stays P7's and the implementation is RWB-PLT-E1027-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 131 cross-document, 9 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not set; the squad sizes it at refinement |
| Contract version | v1 (/v1 path); envelope as `asyncapi/rwb.decision-record.v1.asyncapi.yaml` of API Specification v7, type `rwb.decision.DecisionRecorded.v1`, with the headers `ce_idempotencykey` and `ce_actor` |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None; built against fakes of RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1072-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON until published, then replaced in the same iteration; plan lists kept; RWB-P7-E1073-CON and RWB-P3-E1042-CON built against their fakes; rwb-access authorise contract (ID not specified in the source documents (GAP-1288)) built against its fake; the platform baseline RWB-PLT-E1044-CON, RWB-PLT-NF06-DB, RWB-PLT-E1042-CON, RWB-PLT-E1047-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON is the precondition and fake set; metadata H row stays None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-020, RD-P1-068 |

### 1. Story

As a **platform contract owner**, I want **the published contract of the local decision-record library — the interfaces and exceptions, the record shape, the DDL template of `decision_record` that every service applies in its own schema, the `DecisionRecorded` envelope on `rwb.decision-record.v1`, the transaction and idempotency rules, the versioning rule and the fakes — instead of the monolith's one `decision_log_entry` table in the shared `recovery` schema**, so that **all 19 services can write their records from Day 1 against one frozen contract while the central ledger stays P7's**.

### 2. Business rationale

In the monolith the decision log was one table, `decision_log_entry`, in the single `recovery` schema, and the writer was one published interface inside the same process (legacy sections 11 and 12). Architecture v5 changes both facts in one move. Slide 20 states what every service does from the service template and the shared libraries — it writes its own decision records locally, in "Own schema: business tables + outbox + inbox + decision_record", and publishes `DecisionRecorded` to `rwb.decision-record.v1` — and slide 28 adds that the record is written with the change in one transaction, chained to the one before, and collected centrally by rwb-decision within 5 minutes. ADR-022 records the decision: a local decision record plus a central ledger.

**The division of the legacy key is fixed.** This WP delivers the **local decision-record library** and its contract. The **central ledger** — the `rwb_decision` store, the continuous ingest (JOB-13), the chain check (JOB-14) at 02:00 and the reads `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}` — is **RWB-P7-E1027-APP**, and the **end-to-end proof** is **RWB-ITG-E1027-ITG**. The legacy acceptance criteria **AC1 to AC7 stay with RWB-P7-E1027-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title.

The contract has to exist before the code does, for three reasons. The record shape is the only thing that makes the chain check of P7 possible at all: if one service writes a different column set, the ledger cannot recompute an entry hash, and Audit cannot search one place for every decision. The transaction rule is the whole point of the local write: a library that opened its own transaction would let an action commit without its record, which is exactly what REQ-DRI-005 forbids, so `MANDATORY` is part of the contract and not a coding convention. And the envelope has to be fixed for a shared topic: all 19 services publish to `rwb.decision-record.v1`, so the type name, the key and the payload shape are the only thing that keeps the ingest simple and the ordering per case intact.

The contract also fixes what the library does not do. It does not write the central ledger, does not raise a case event or a task, does not copy to a data lake (the legacy RWB-E1-014 copy is retired, DP-17), and does not write another service's table. The table it declares is a library object owned by PLT and created in each service's own schema, and `decision_log_entry` is named only as the P7 ledger that is not this contract's.

The fake is the Day-1 unblocker: every service can build and test its record write, its refusal path and its outbox call before a single other service exists, and P7 can build its ingest against the same envelope (Template and Rules §R5.4 class C).

### 3. Preconditions

- The local record is the caller's: Architecture v5 slides 20 and 28 fix that each service writes its own record in its own schema and publishes `DecisionRecorded`, and that the central ledger is P7's.
- The shared topic name is fixed by Template and Rules §R4 as `rwb.decision-record.v1`; the event name follows the §R4 naming rule as `rwb.decision.DecisionRecorded.v1` and the topic keeps its shared name (ASM-2444, ASM-0209 confirmed by RD-P1-008).
- The envelope carries `ce_idempotencykey` and `ce_actor`, because the rwb-source-data ledger intake (RWB-P1-E1067-APP) consumes the event and parks a record without either of them (RD-P1-009).
- ce_idempotencykey is the record’s RD-P1-007 rule 4 business key (RD-P1-009, RD-P1-068). The actor prefixes remain USER:<userId>, SERVICE:<service name> and PARTNER:<partnerCode>.
- rwb_source_data applies the shared-library decision_record migration for DM012 and the sandbox. Pending: publish the migration DDL in the physical schema, owner platform lead (library owner), tracked as NEW-GAP-F08-7. The interim Testcontainers build runs the library migration (RD-P1-068 rule 8).
- The ledger owner is fixed: `decision_log_entry` is P7's under the Ownership Map ruling on `decision_log_entry` (owner P7) and Architecture v5 slide 41.
- The record columns are the ones the Temporal and Drools Design slide 16 names — `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash`, `entry_hash` — with the case, the decision code, the actor and the idempotency key of the legacy story.
- The decision codes and approval levels are values in force in the target owner's data, read through the parameters and reference-data contracts of rwb-case; the contract refers to them and holds no list of its own.
- The outbox contract of RWB-PLT-TE006-CON exists, so the contract can name the publisher it uses without redeclaring it.
- The per-service Flyway conventions of RWB-PLT-E1044-CON exist, so the DDL template is a template and not one shared migration.
- The message identifiers `MSG-P7-009` and `MSG-P7-003` are kept unchanged from the legacy build; no published message catalogue defines their entry format, so that entry is Not specified in the source documents (GAP-1403; ASM-2443).
- The full column set of the local table, the entry-hash algorithm and the exact payload schema beyond the fields named in section 12.3 have no published specification and are published here as the working read (GAP-1403; ASM-2443).
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the three interfaces — `DecisionRecordWriter`, `DecisionRecord` and `DecisionRecordEntryRef` — with their signatures, the two exceptions and the `MANDATORY` transaction rule.
2. The author fixes the record shape as the seven field groups of section 12.2, with the access-event exception for the subject and the version group, and one worked example that uses the legacy values only.
3. The author writes the DDL template of `decision_record`: the columns, the unique keys, the chain columns, the append-only trigger and the index, as one template each service applies in its own schema.
4. The author writes the `DecisionRecorded` envelope section: CloudEvents 1.0 binary mode, the attribute set, `ce_type` `rwb.decision.DecisionRecorded.v1`, the headers `ce_idempotencykey` and `ce_actor`, the key rule, the payload fields and the rule that the payload carries identifiers and facts only.
5. The author writes the transaction and idempotency rules: the call joins the caller's transaction, opens none, throws before any write, returns the first entry reference for a repeated key and counts the repeat.
6. The author writes the versioning rule: major version 1, a backward-compatible change versus a new major version with a new `ce_type`, and the pinning rule for consuming services.
7. The lint and schema steps run: the interfaces compared against the legacy published interface, the DDL applied twice in throwaway schemas, the example scanned for personal data, and the envelope validated against one accepted and one refused schema.
8. The fake set is generated: a writer fake, a chain fixture, an outbox fake, a registry fake and a P7 ledger fake, all answering from the same example set.
9. The contract test runs the fakes against the document on every change and fails the build on any drift.
10. The document and the fakes are published at v1; RWB-PLT-E1027-APP and every consuming service pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published signature opens its own transaction, or performs a write when no transaction is open | The contract lint fails the build; the `MANDATORY` rule and the throw-before-write rule are fixed | None | AC1 |
| X2 | A record shape published without the version group, or without the access-event exception | The schema validation fails the build; the seven field groups are all required and the exception is declared | None | AC2 |
| X3 | A service applies the DDL template in another service's schema, or hand-writes the table | The boundary and drift checks fail the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | The envelope is published with a type other than `rwb.decision.DecisionRecorded.v1`, or with no key | The envelope validation fails the build; the type and the key rule are fixed | None | AC4 |
| X5 | A breaking change is made to an interface, a column, the key rule or the envelope | The change raises major version 2 and a new `ce_type`; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming service ships without the drift test, or a schema change breaks a consumer | The registry refuses the change and the drift test fails the build | None | AC6 |
| X7 | A value the consumers need is named by no source — the full column set, the hash algorithm, the payload schema or the incident route | The value is published as the working read of the assumption, and the gap stays open | Not specified in the source documents (GAP-1403; ASM-2443) | AC7, AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a DDL template and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | Column widths, the hash algorithm and the fixture set are open until v1 is frozen; the interfaces, the seven field groups, the key rule and the versioning rule are fixed |
| Valuable | Unblocks all 19 services and the P7 ingest on Day 1 and keeps one shared decision table out of every service plan |
| Estimable | Three interfaces, one record shape, one DDL template, one envelope, two rules and five fakes |
| Small | One sprint for the document, the template, the fakes and the lint rules |
| Testable | Each criterion below is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: local decision-record library contract

  Background:
    Given the platform library contract document is published with major version 1
    Given the 19 services have one schema and one login each
    Given the contract declares no REST base, no topic and no queue of its own

  Scenario: AC1 The interfaces, the MANDATORY transaction rule and the exceptions are published (new, D-RCV-60)
    Given the interface section of the contract document
    When it is validated and linted
    Then it publishes DecisionRecordWriter.record(DecisionRecord) returning DecisionRecordEntryRef, annotated with propagation MANDATORY
    Then DecisionRecordEntryRef carries entryId, chainSeq, entryHash and repeated
    Then the write declares DecisionLogRecordInvalidException with messageId MSG-P7-009 and field, and DecisionLogUnavailableException with messageId MSG-P7-003, and no other thrown type
    Then a call with no open transaction throws IllegalTransactionStateException before any write
    Then no interface method opens, commits or rolls back a transaction and no method calls another service

  Scenario: AC2 The record shape carries the seven field groups with the access-event exception (new, D-RCV-60)
    Given the record-shape section of the document and its worked example
    When the schema is validated
    Then the shape carries the decision code, the subject case, the version group, the inputs reference, the recommendation and final call, the approver with an approval level, and the actor with the decided-at time
    Then the version group requires at least one of rule version, model version and agent version, and a rule ID requires its rule version
    Then an access event carries no case and requires no subject group, and every other group stays required
    Then the example uses only the legacy values, with decision code D6, final call OWNER_ASSIGNED, rule ALLOC-MTG-BKK-01 of ALLOC-2026.11 and case RW-2026-000123

  Scenario: AC3 The DDL template creates decision_record in each service's own schema (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through each service's own Flyway sequence
    Then it creates decision_record in the applying schema only, with the chain columns chain_seq, prev_hash and entry_hash
    Then it declares the unique key on idempotency_key and the unique key on chain_seq
    Then it installs the append-only rule that refuses an update and a delete
    Then it declares no foreign key and no reference to another service's schema
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The DecisionRecorded envelope is fixed (new, D-RCV-60)
    Given the envelope section of the document
    When one record is validated against it
    Then the event is rwb.decision.DecisionRecorded.v1 published on the shared topic rwb.decision-record.v1 in CloudEvents 1.0 binary mode with ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header
    Then the record key is caseId where the record has a case, and the entry id where it does not
    Then the payload carries the entry id as entryId, the case where there is one as caseId, the decision code as decisionCode, the final call, the rule ID, the rule version, the chain sequence, the entry hash and the actor reference
    Then the event also carries the headers ce_idempotencykey and ce_actor
    Then the payload carries no personal data and no free text beyond the legacy fields
    Then the registry holds one accepted schema version and refuses a body that does not match it
    Then the contract declares no data-lake copy and no reporting copy

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then a backward-compatible change keeps major version 1 and the ce_type version, and is accepted by the registry in BACKWARD mode
    Then a breaking change raises major version 2 and a new ce_type, and v1 is never edited in place
    Then a consuming service pins a published version and raises a change request rather than a private variant

  Scenario: AC6 The fake answers the document and every consuming service runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the writer fake, the chain fixture, the outbox fake, the registry fake and the P7 ledger fake
    Then the writer fake returns an entry reference with chain sequence and entry hash, refuses with MSG-P7-009 and the field name, and repeats a key with repeated true
    Then the chain fixture answers a first record and a second record linked to the first, and refuses an update
    Then the outbox fake records the event in the caller's transaction and answers absent after a rollback
    Then the drift test of every consuming service fails on any difference from section 12 and section 13

  Scenario: AC7 A value named by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value the consumers need is named by no source
    When the contract is published
    Then the value is published as the working read of the assumption
    Then the gap GAP-1403 stays open and the value cites ASM-2443

  Scenario: AC8 A consumer value named by no source is published as the working read with its gap open (new, D-RCV-60)
    Given a value the consumers need is named by no source: the full column set, the hash algorithm, the payload schema or the incident route
    When the contract is published
    Then each such value is published as the working read of the assumption and cites its gap
    Then no such value is presented as a settled published value

  Scenario: AC9 Every business rule of section 8 names a criterion and a test (new, D-RCV-60)
    Given the business rules table of section 8
    When its Covered by column is checked
    Then each rule BR1 to BR11 names at least one criterion and at least one test case of section 16

  Scenario: AC10 A disallowed change to a recorded entry is refused (new, D-RCV-60)
    Given a decision record entry already written to decision_record
    When an update or a delete of the entry is attempted
    Then the append-only rule refuses it and the entry is unchanged
    Then the chain fixture refuses an update of the entry

  Scenario: AC11 The event carries the business key and the actor the ledger intake needs (new, RD-P1-009)
    Given a record with idempotencyKey "EV-08-RW-2026-000123-20261201-7f3c2a10-0000-4000-8000-000000000123", a case and a system actor of service rwb-case
    When the writer fake records it and the outbox fake publishes it
    Then the event has ce_type rwb.decision.DecisionRecorded.v1, ce_idempotencykey equal to the decision record’s RD-P1-007 rule 4 business key and ce_actor "SERVICE:rwb-case"
    Then data.entryId and data.caseId are the entry id and the case id
    Given the same record made by a user
    Then ce_actor is "USER:" followed by the user identifier
    Then ce_idempotencykey is at most 120 characters and ce_actor at most 74 characters

  Scenario: AC12 A record that cannot give the two headers is refused before any write (new, RD-P1-009)
    Given a record whose idempotencyKey is 121 characters long, and a second record with no actor reference
    When each is passed to the writer fake
    Then each throws DecisionLogRecordInvalidException with MSG-P7-009 and field idempotencyKey or actorUserRef respectively
    Then no row and no outbox event are written
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — **AC1 to AC7 of RWB-E1-027 stay with RWB-P7-E1027-APP** — and every identifier comes from the legacy story, Architecture v5 or the Temporal and Drools Design, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The library publishes three interfaces and nothing else, and the write is declared with propagation MANDATORY so that it joins the caller's transaction and opens none | RWB-E1-027 section 12; ADR-022; Architecture v5 slide 28 | AC1; TC-PLT-E1027-CON-01 |
| BR2 | The record carries the seven field groups; the subject case and the version group are not required for an access event, and every other group is required for every record | RWB-E1-027 BR2, BR3, BR4; DF-DEC-002 to DF-DEC-016 | AC2; TC-PLT-E1027-CON-02 |
| BR3 | The table is a library object owned by PLT and created in each service's own schema by the DDL template, append-only, with the chain columns and the unique idempotency key | DP-01; DP-15; Architecture v5 slide 20; Ownership Map | AC3; TC-PLT-E1027-CON-03, TC-PLT-E1027-CON-06 |
| BR4 | `DecisionRecorded` is published on the shared topic in CloudEvents 1.0 binary mode with the type and the key rule of section 12.3 | DP-09; ADR-015; Architecture v5 slides 20, 22 and 42 | AC4; TC-PLT-E1027-CON-04 |
| BR5 | A refused record names the field with MSG-P7-009; a failed append raises with MSG-P7-003 and the caller's transaction rolls back | R-UNI-39; REQ-DRI-005; RWB-E1-027 sections 4 and 14 | AC1, AC6; TC-PLT-E1027-CON-01, TC-PLT-E1027-CON-05 |
| BR6 | The same idempotency key gives one record, the first entry reference and a counted repeat | R-UNI-40; RWB-E1-027 BR6 | AC6; TC-PLT-E1027-CON-05 |
| BR7 | A published version is never edited: a backward-compatible change stays in major version 1 and a breaking change raises major version 2 with a new `ce_type` | Template and Rules §R7.2; §R5.4 class C | AC5; TC-PLT-E1027-CON-04 |
| BR8 | The ledger stays P7's: `decision_log_entry` in `rwb_decision` is named only, and no consumer of this contract reads or writes it directly | DP-01; Ownership Map row `decision_log_entry`; Architecture v5 slide 41 | AC1, AC3; TC-PLT-E1027-CON-01, TC-PLT-E1027-CON-03 |
| BR9 | The contract writes no data-lake copy and no reporting copy; the legacy copy RWB-E1-014 is retired and its dependencies are dropped | DP-17; ADR-018; Template and Rules §R6 | AC4; TC-PLT-E1027-CON-04 |
| BR10 | The message identifiers MSG-P7-009 and MSG-P7-003 are kept unchanged although the store moved, so every record and report that cites them stays readable | ASM-2443 | AC1, AC6; TC-PLT-E1027-CON-01, TC-PLT-E1027-CON-05 |
| BR11 | Every `DecisionRecorded` carries `ce_idempotencykey` (the record's business key, at most 120 characters, form `<code>-<caseNo>-<yyyyMMdd>-<actionId>` with code `EV-08`, so it never equals the key of the same action's own event) and `ce_actor` (`USER:<userId>`, `SERVICE:<service name>` or `PARTNER:<partnerCode>`, at most 74 characters) | RD-P1-007 rule 4; RD-P1-009 rule 1 | AC11, AC12; TC-PLT-E1027-CON-11, TC-PLT-E1027-CON-12 |

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are fixed here and the implementation behind them is specified in RWB-PLT-E1027-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Decision record | Unwritten | The caller has opened the transaction and not yet called the library |
| Decision record | Validated | The seven field groups passed and the idempotency key is new |
| Decision record | Written in the transaction | The row is appended with its chain link and is visible inside the caller's transaction |
| Decision record | Committed | The caller committed; the action, the row and the outbox row are stored together |
| Decision record | Refused | A field group failed; nothing is stored and the field is named |
| Decision record | Repeated | The key already existed; the first entry reference is returned and the repeat counted |
| DecisionRecorded | Published | The caller's outbox relay published the event on the shared topic |
| DecisionRecorded | Absent | The caller's transaction rolled back; no event exists |
| Contract version | v1 | The published version every consuming service pins |
| Contract version | v2 | Raised by a breaking change, with a new `ce_type`; v1 stays readable and is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template, the envelope section and the fakes |
| The platform owner of the library | Approves a breaking change and freezes a version |
| The service teams of the 19 services | Consume the contract, pin the version, raise a change request rather than a private variant |
| The rwb-decision owner (P7) | Confirms the ledger side: the ingest, the chain check and the two read operations that this contract announces to |
| The rwb-case owner (P3) | Confirms the parameters and reference-data operations the decision code and approval-level lists are read from |
| RW-PLATADM | Receives the incident that the implementation raises when a record cannot be written |
| RW-AUDIT, RW-COE | Audit the records through the P7 ledger, not through this contract |
| No delegation of authority level applies | A library contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. Where a caller or an operator must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | BR Field ID | Value |
|---|---|---|
| Business data published | BR1 | None. The document publishes signatures, the record shape, codes, status values and message identifiers; no customer, account or case value appears |
| Record shape published | BR2 | The seven field groups of section 12.2 and the chain columns, with one worked example from the legacy story |
| Personal data | BR2 | None. The actor is a reference such as `SY-CASEWF` or a user identifier, never a name; no account number, national identifier or document content appears |
| Tables published | BR3 | `decision_record` only, as a DDL template applied in each service's own schema; the central `decision_log_entry` is P7's and is named only |
| Field identifiers | BR2 | The record fields carry the legacy identifiers DF-DEC-001 to DF-DEC-018, DF-DEC-030 and DF-DEC-031; the list values carry DF-REF-028 and DF-REF-029 |
| Retention | BR3 | The table is append-only in each service's schema and keeps every record; the retention period of a local record is Not specified in the source documents (GAP-1403; ASM-2443) |

The record shape is the one place where a rule value could leak into the contract, so the document fixes that a record carries codes and identifiers, the rule ID and the version label, and never the DRL, the payload of a rule evaluation or a personal field.

### 12. Contract

#### 12.1 REST operations provided

None — the library is in process and publishes Java interfaces, a DDL template and an envelope, not an OpenAPI document. The two ledger reads belong to P7 rwb-decision under `/api/recovery/decision/v1` and are named in section 19, not declared here.

#### 12.2 REST operations consumed

None — the library joins the caller's transaction and calls no service. The decision code and approval-level lists reach it through the parameters and reference-data client libraries, whose REST consumption belongs to RWB-PLT-E1042-CON and RWB-PLT-E1043-CON.

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | `caseId` where the record has a case; the entry id where it does not | `entryId`, `caseId` where there is one, `decisionCode`, final call, rule ID, rule version, chain sequence, entry hash, actor reference | Announces every record to the P7 central ledger, to rwb-reporting and to the rwb-source-data ledger intake (one `DECISION_TAKEN` entry per event with `data.caseId`; `decisionLogId` = `data.entryId`; `approver` not read); written to the caller's outbox in the same transaction |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.decision.DecisionRecorded.v1 |
| ce_source | The producing service |
| ce_idempotencykey | The record's business key, at most 120 characters; required |
| ce_actor | `USER:<userId>`, `SERVICE:<service name>` or `PARTNER:<partnerCode>`, at most 74 characters; required |
| ce_subject | The case ID where there is one, the entry id where there is not |
| ce_id and traceparent | The event identifier and the W3C trace context of the caller |
| Payload | Identifiers and facts only; no personal data and no free text beyond the legacy fields |

The `ce_` rows are CloudEvents 1.0 envelope attributes of the event, not LDM or Data Classification fields. The event name follows the §R4 naming rule while the topic keeps the shared name `rwb.decision-record.v1` (ASM-2444). The key rule for a record with no case, the exact payload schema beyond the fields listed and the `ce_subject` format are Not specified in the source documents (GAP-1403) and are published as the working read (ASM-2443).

#### 12.4 Events consumed

None — the library consumes no event. The chain check of P7 reads the table through its own contract and is not a subscription of this library.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. The library is called from inside the caller's own activity on the caller's own task queue, and a workflow class never calls it, so a replay reuses the recorded decision (DP-10).

#### 12.6 Schedules

None — the legacy JOB-14 chain check is a P7 Schedule at 02:00 and is named in section 19 as out of scope; this contract declares no Schedule (RWB-P7-E1027-APP).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT | Contract shape of the local record: the seven field groups, the chain columns `chain_seq`, `prev_hash` and `entry_hash`, the unique key on `idempotency_key` and the append-only rule. Each service applies the template in its own schema |

The table is a library object owned by PLT and created in each service's own schema through that service's own Flyway sequence and login; the contract does not create a schema, a login or a table in another service's schema and declares no foreign key across a service boundary (DP-01, DP-15). The central `decision_log_entry` is P7's, lives in `rwb_decision` and is named here only: this contract neither creates it nor writes it, and no consumer of the contract reads it directly (BR8). For rwb-source-data the application of this template is Pending (NEW-GAP-F08-7).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Writer fake | `DecisionRecordWriter`, `DecisionRecord` and `DecisionRecordEntryRef` | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field name; a repeated key with `repeated` true; a call with no transaction throwing IllegalTransactionStateException |
| Chain fixture | The chain columns and the append-only rule | A first record with chain sequence one and no `prev_hash`; a second linked to the first; a refused update and a refused delete |
| Outbox fake | `OutboxWriter` of RWB-PLT-TE006-CON | An event recorded in the caller's transaction with `ce_idempotencykey` and `ce_actor`, and absent after a rollback |
| Registry fake | The schema registry | BACKWARD mode with one accepted and one refused `DecisionRecorded` body |
| P7 ledger fake | The contract of RWB-P7-E1027-CON | One ledger entry per event, with the entry id, the chain sequence and the 5-minute completeness boundary |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming service rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract publishes interfaces, a template and an envelope | 0 | The two client libraries consume the rwb-case operations |
| Kafka | 1 event type fixed by the contract, published by the caller through its outbox | 0 | AsyncAPI 3.0, CloudEvents 1.0 binary mode, key `caseId` or entry id on the shared topic |
| Temporal | 0 | 0 | No workflow, no activity and no Schedule; the caller's activity calls the library |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Shared library contract artefact of the platform: the three interfaces in `th.co.scb.ace.workbench.recovery.platform.api`, the record type and the entry reference with them, the DDL template as a resource, and the envelope and versioning rules in the contract document. The implementation is RWB-PLT-E1027-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1403; ASM-2443).

**Interface surface**

| Interface | Signature | Returns or throws |
|---|---|---|
| `DecisionRecordWriter` | `DecisionRecordEntryRef record(DecisionRecord record)` annotated `@Transactional(propagation = Propagation.MANDATORY)` | The entry reference; throws `DecisionLogRecordInvalidException` (MSG-P7-009, field) and `DecisionLogUnavailableException` (MSG-P7-003) |
| `DecisionRecord` | The seven field groups: idempotencyKey, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, actorUserRef, decidedAt | The record the caller assembles from values it already holds |
| `DecisionRecordEntryRef` | `entryId`, `chainSeq`, `entryHash`, `repeated` | The first entry reference of an idempotency key |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract declares the table in the applying schema only | referred to; the consuming story carries the dependency |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. This story is the contract of that library | referred to; the consuming story carries the dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the decision code per event is a parameter read as a value in force | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the decision code and approval-level lists are reference rows | referred to; the consuming story carries the dependency |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The contract fixes the `DecisionRecorded` envelope the caller's outbox carries | referred to; the consuming story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the contract states the library is called in an activity and the chain check stays a P7 Schedule | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the record is handed in process inside the caller's transaction and the ledger is reached through its contract | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract adds no path and the ledger reads stay under the decision base | referred to; the consuming story carries the dependency |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the DDL template is applied by each service's own sequence | referred to; the consuming story carries the dependency |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The legacy lake copy of the decision log is retired and the contract declares no copy | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route; the ledger view for a screen is out of scope here | referred to; the consuming story carries the dependency |

**Hardware and software change.** The contract moves the decision record from one `decision_log_entry` table in the monolith's `recovery` schema to a template that every service applies in its own schema, fixes the record inside the caller's transaction with `MANDATORY`, fixes the chain columns per schema, and fixes one envelope on one shared topic for all 19 producers. Governance and the central log stay in rwb-decision. No new hardware is implied: the template is applied by each service's own Flyway run in the existing ACE PostgreSQL server, and the events use the Kafka platform ACE already runs.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionRecordWriter` | Published interface | The one write method, its `MANDATORY` rule and its two exceptions (BR1, BR5) |
| `DecisionRecord` and `DecisionRecordEntryRef` | Published types | The seven field groups and the entry reference (BR1, BR2) |
| DecisionRecordDdlTemplate | Resource | The `decision_record` DDL: columns, keys, chain columns and append-only rule (BR3) |
| EnvelopeSpecification | Document | The CloudEvents 1.0 binary-mode attribute set, the `ce_type`, the headers `ce_idempotencykey` and `ce_actor`, the key rule and the payload fields (BR4, BR11) |
| VersioningSpecification | Document | Major version 1, the compatible versus breaking rule and the pinning rule (BR7) |
| Fake set and fixtures | Test asset | The writer, chain, outbox, registry and ledger fakes used by every consuming service (AC6) |

**Build steps**

1. Write the three interfaces, the record type and the entry reference, taken from the legacy published interface; lint the `MANDATORY` rule and the throw-before-write rule (AC1).
2. Write the record-shape section with the seven field groups, the access-event exception and the legacy example (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the chain columns, the unique keys, the append-only rule and the absence of a cross-schema key (AC3).
4. Write the envelope section and validate one record against the registry fake; assert the type, the key and the payload fields (AC4).
5. Write the transaction and idempotency rules into the interface documentation; test the repeated key and the missing transaction on the writer fake (AC1, AC6).
6. Write the versioning section with the compatible and breaking examples (AC5).
7. Generate the fake set and write the drift test; wire it into the build of every consuming service (AC6).
8. Publish v1 and record the pinned version of RWB-PLT-E1027-APP and of each consuming service.

**Done when.** The document and the template validate, the two throwaway applications prove the reusability, the fake set answers every criterion including the refusal, the repeat and the absent event, the drift test is green on the build of this story and on the build of RWB-PLT-E1027-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException`, messageId MSG-P7-009, with `field` |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException`, messageId MSG-P7-003 |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary of the caller) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. | Named only; the caller owns the display |

The three texts are copied unchanged from RWB-E1-027 and this contract adds no message ID. The field names are `versions`, `ruleVersion` and `decisionCode` for the three refusals of the legacy criteria. The published catalogue entry format for MSG-P7-009 and MSG-P7-003 is Not specified in the source documents (GAP-1403; ASM-2443). Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: the library has no user interface and answers inside the caller's transaction. The ledger view and the decision-log screens are reached through the gateway-bff composite route (DP-19) and belong to RWB-P7-E1027-APP; a refused record appears as an incident, not as a screen error.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1027-CON-01 | AC1 | Contract | The interface section linted; the signature compared against the legacy published interface; the `MANDATORY` annotation; the two exceptions with their identifiers; a no-transaction call refused before any write |
| TC-PLT-E1027-CON-02 | AC2 | Contract | The record shape validated against the seven field groups; the access-event exception; the legacy example with D6, OWNER_ASSIGNED, ALLOC-MTG-BKK-01 of ALLOC-2026.11 and RW-2026-000123; a personal-data scan |
| TC-PLT-E1027-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the chain columns, the two unique keys, the append-only rule and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-PLT-E1027-CON-04 | AC4, AC5 | Contract | One record validated against the envelope: the CloudEvents attribute set, `ce_type`, the key with a case and the key without one, the payload fields; one accepted and one refused body; a compatible change and a breaking change; no data-lake or reporting copy. |
| TC-PLT-E1027-CON-05 | AC6 | Component | The five fakes answering every example, including the refused record with its field, the repeated key, the absent event after a rollback and the drift test on a consuming service |
| TC-PLT-E1027-CON-06 | AC3 | Component | The boundary of the section 12.7 table: decision_record created in the applying schema only, with no cross-schema key or reference |
| TC-PLT-E1027-CON-07 | AC7 | Contract | A value named by no source published as the working read of the assumption; GAP-1403 stays open |
| TC-PLT-E1027-CON-08 | AC8 | Contract | Each value named by no source (full column set, hash algorithm, payload schema, incident route) published as the working read; the gap stays open and the value cites its assumption |
| TC-PLT-E1027-CON-09 | AC9 | Contract | The section 8 table checked: each of BR1 to BR11 names a criterion and a test case in its Covered by column |
| TC-PLT-E1027-CON-10 | AC10 | Component | An update and a delete of a recorded entry asked of the append-only table and of the chain fixture; both refused and the entry unchanged |
| TC-PLT-E1027-CON-11 | AC11 | Contract | AC11 The event carries the business key and the actor the ledger intake needs (new, RD-P1-009) |
| TC-PLT-E1027-CON-12 | AC12 | Component | AC12 A record that cannot give the two headers is refused before any write (new, RD-P1-009) |

The legacy test case set of RWB-E1-027 is carried by RWB-P7-E1027-APP and RWB-ITG-E1027-ITG; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the decision codes and approval levels are values in force in the owner's data, and the only values this document fixes are the legacy example values.
- No personal data in a schema, an example, a fake or a log: the actor is a reference, the subject is a case or document identifier, and the scan fails the build otherwise.
- No cross-schema reference in the DDL template and no foreign key across services; the boundary test fails the build.
- No write path to `decision_record` other than the library, no update path at all, and the architecture test is part of the contract test of every consuming service.
- No REST surface and no topic of the library's own: the shared topic belongs to the event platform and the ledger reads to P7.
- The library writes no ledger row, raises no case event and no task, and writes no data-lake or reporting copy.
- A published version is never edited in place: a breaking change raises major version 2 with a new `ce_type` and a migration note.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-02, FEAT-DRI-03, FEAT-DRI-08 | 17 Run the decision center | BR1, BR2, BR3, BR4 | TC-PLT-E1027-CON-01, TC-PLT-E1027-CON-02, TC-PLT-E1027-CON-04, TC-PLT-E1027-CON-06 |
| REQ-DRI-005 | No action proceeds if its record cannot be written | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-04, FEAT-DRI-05 | 17 Run the decision center | BR1, BR5, BR6 | TC-PLT-E1027-CON-01, TC-PLT-E1027-CON-05 |
| Legacy test set RWB-E1-027 | TC-E1-027-01, TC-E1-027-02, TC-E1-027-03, TC-E1-027-04, TC-E1-027-05, TC-E1-027-06, TC-E1-027-07, TC-E1-027-08, TC-E1-027-09 | Epic 1, 3.7 | The legacy story's own features | 17 Run the decision center | The legacy rules R-UNI-39 and R-UNI-40 | Executed by RWB-P7-E1027-APP and RWB-ITG-E1027-ITG; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1027-APP | App development | H consumer: implements the interfaces, the validator, the chain and the publisher against this contract and its fake |
| RWB-P7-E1027-CON | Contract | Referred to: the central ledger contract the envelope announces to and the two ledger reads; also the C row of the legacy dependency. This contract adds no build dependency of its own |
| RWB-P7-E1027-APP | App development | The central ledger, the ingest, the chain check and the read operations; owner of the legacy acceptance criteria |
| RWB-ITG-E1027-ITG | Integration | The end-to-end proof of the library and the ledger on real services |
| RWB-PLT-TE006-CON | Contract | Referred to: the outbox writer and the envelope family this contract's event uses. This contract adds no build dependency of its own |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | Referred to: the parameters and reference-data clients that carry the decision code and approval-level lists |
| RWB-PLT-E1071-CON | Contract | Referred to: the activity in which the library is called |
| RWB-PLT-E1044-CON | Contract | Referred to: the per-service Flyway sequence that applies the DDL template |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway route the ledger view uses; no path is declared here |
| RWB-PLT-DB, the per-service DB stories | Database | X: create each service's schema, login and grants so the template can be applied |

### 19. Out of scope

- The implementation — the validator, the chain, the idempotency path and the publisher: RWB-PLT-E1027-APP.
- The central ledger, the continuous ingest (JOB-13), the chain check (JOB-14) and the two read operations under `/api/recovery/decision/v1`: RWB-P7-E1027-APP and RWB-P7-E1027-CON.
- The outbox DDL and relay, the retry topics and the dead-letter topic: RWB-PLT-TE006-CON, RWB-PLT-TE006-APP and RWB-PLT-EVT.
- The per-service schema and login and the grants that apply the template: RWB-PLT-DB and the per-service database stories.
- The rule package registry and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The retired data-lake copy of the decision log: RWB-E1-014, no target path (DP-17).
- The access-event writer and its records: P4 rwb-access, RWB-E1-039.
- Approval records with the limit applied: RWB-E2-013.
- The recommendation service with the reasons for the route decision: Epic 4.

### Remaining delivery steps

- Close NEW-GAP-F08-6 before the library implementation builds the two headers (platform library owner with the solution architect).
- Close NEW-GAP-F08-7 before the rwb-source-data migration set is frozen (solution architect).
- Update the shared asyncapi document and publish the fakes at v1 (platform library owner).
- Size the story at refinement (squad).
- Add the new TC-PLT-E1027-CON assertions to Test Cases v9 and the RTM (QA lead).
