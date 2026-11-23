# RWB-P7-E1027-CON Decision log writer v1 - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-027 for rwb-decision. The write interface, the record shape, the chain rule, the failure and retry rule, the idempotency key and the `DecisionRecorded` envelope are published on Day 1; the implementation is RWB-P7-E1027-APP and the store is RWB-P7-E1008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-002, FR-P7-007, FR-P7-008, FR-P7-009) |
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-decision**, I want **the published contract baseline of the decision log writer — the append interface the ledger of this service accepts, the record shape with the decision code, the rule and its version, the case, the subject, the data date, the inputs digest, the previous hash, the entry hash, the actor role and the timestamps, the hash-chain rule, the failure, incident and retry rule, the idempotency key, the `DecisionRecorded` envelope on the shared topic, the owned tables and the fakes — instead of the monolith's one published interface over one `decision_log_entry` table in the shared `recovery` schema**, so that **the writer of this service and every caller of it build on Day 1 against one frozen shape, and a field, a hash input, a message identifier or an event type can never drift between rwb-decision, its callers and the central ledger without a failing build**.

### 2. Business rationale

In the monolith the decision log was one table, `decision_log_entry`, in the single `recovery` schema, and the writer was one published interface inside the same process, documented in legacy section 12 in a page of Java and one sentence per rule. Architecture v5 changes three facts in one move: each service writes its own record in its own schema and publishes `DecisionRecorded` (slide 20), the record is written with the change in one transaction and hash-linked to the one before it (slide 28), and the central ledger in rwb-decision collects the records from the topic within five minutes (slide 28; ADR-022). The contract has to exist before the code does for three reasons.

The first is the chain. A hash chain is only verifiable if every writer computes the same input the same way: the field order, the encoding, the previous hash and the first link, which the module specification fixes as 64 zeros (FSD P7 A2.1 AC-ALT-P7-001-01). A record shape that leaves the canonical form to the implementer makes the nightly chain check of `JOB-14` meaningless after the second service goes live. The second is the transaction: a writer that opened its own transaction would let an action commit without its record, which is exactly what REQ-DRI-005 forbids, so `MANDATORY` is part of the contract and not a coding convention. The third is the envelope: the record leaves on the shared topic `rwb.decision-record.v1` where the ledger and the reporting read model both listen, so the type, the key and the payload are the only thing that keeps the ingest simple and the ordering per case intact.

The contract also fixes what the writer does not do. It writes no approval row (RWB-P7-E2013-APP), declares no rule model and no rule version of its own (RWB-P7-E1073-CON), reads no ACE view, writes no data-lake copy (the legacy stream is retired, DP-17), owns no Schedule (the `JOB-13` copy at 01:00 has no target and `JOB-14` is the store's) and provides no REST operation of its own: the two reads under `/api/recovery/decision/v1` are P7-owned and delivered by RWB-P7-E2005-APP.

**One element of the baseline is missing from the Ownership Map.** The map gives P7 the two reads and no write path, because in the target a decision record is written in process inside the caller's transaction and not over REST (DP-03, DP-11). The contract therefore describes the write surface as the local decision-record library of RWB-PLT-E1027-CON plus the service-local append operation of RWB-P7-E1008-APP, and it records the missing owned operation, with its assumption, rather than inventing a path: Not specified in the source documents as an operation of the Ownership Map (GAP-1235; ASM-2199).

The fake is the Day-1 unblocker: the app story, the store story and every caller can build and test the accepted record, the refusal, the repeat, the absent event and the broken chain before the ledger ingest exists, and the ingest can be built against the same envelope.

### 3. Preconditions

- The local record is the caller's: Architecture v5 slides 20 and 28 fix that the record is written with the change in one transaction, hash-linked to the one before, and collected centrally; ADR-022 records it.
- The store of this service is RWB-P7-E1008-APP: `decision_log_entry` in `rwb_decision` with the chain columns, the append-only trigger, the unique keys and the chain verifier behind `JOB-14` at 02:00. The contract names that store and never creates it.
- The platform library RWB-PLT-E1027-CON publishes the interfaces, the record type and the envelope family this baseline implements; where the two documents could differ, this baseline is the rwb-decision instance and says so.
- The shared topic name is fixed as `rwb.decision-record.v1` (Template and Rules §R4; Architecture v5 slides 20 and 42). The event type on it is fixed by this run as `rwb.decision-record.DecisionRecorded.v1`; the platform library contract writes the same event as `rwb.decision.DecisionRecorded.v1`, and that difference is recorded as a conflict (GAP-1238; ASM-2202).
- The record fields are the ones the Temporal and Drools Design slide 16 names — `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash`, `entry_hash` — with the case, the decision code, the actor and the idempotency key of the legacy story.
- The decision codes and the approval levels are values in force in the data of rwb-case, read through the parameters and reference-data contracts (RWB-P3-E1042-CON, RWB-P3-E1043-CON); this baseline holds no list of its own.
- The message identifiers `MSG-P7-009` and `MSG-P7-003` are kept unchanged from the legacy build; no published message catalogue defines their entry format, so that entry is Not specified in the source documents (GAP-1236; ASM-2200).
- The full column set, the data-date column, the canonical form of the entry hash and the exact payload schema beyond the fields of section 12.3 have no published specification and are published here as the working read (GAP-1236; ASM-2200; GAP-1237; ASM-2201).
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the write surface: the append interface this service accepts, its `MANDATORY` rule, the entry reference it returns and the two exceptions, together with the note that the Ownership Map carries no write operation (AC1).
2. The author fixes the record shape as the field groups of AC2, with the access-event exception for the subject, one worked example that uses the legacy values only, and the data date and inputs digest carried on every record.
3. The author fixes the hash-chain rule: the input of the entry hash, the encoding, the digest and its length, the first `prev_hash` and the rule that an entry is never rewritten (AC3).
4. The author fixes the failure rule: what is refused, what rolls back, what raises an incident with which message identifier, and what the caller retries and what it never retries (AC4).
5. The author fixes the idempotency rule: the key, its scope, the stored answer and the repeat counter (AC5).
6. The author fixes the `DecisionRecorded` envelope: mode, attribute set, type, source, subject, key rule, payload fields and the rule that no personal value travels (AC6).
7. The author fixes the owned and not-owned tables, the schema, the base, the topic, the queue, the package and the migration, and lists the fakes (AC7).
8. The lint and schema steps run: the interface compared with the legacy published interface, the record example scanned for personal data, the envelope validated against one accepted and one refused schema, and the chain fixture recomputed independently.
9. The fake set is generated and the drift test runs on the build of RWB-P7-E1027-APP and on the build of every caller.
10. The baseline is tagged at v1 and the store, the app, the read, the approval and the harness stories pin it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The published interface opens its own transaction, or writes when no transaction is open | The contract lint fails the build; the `MANDATORY` rule and the throw-before-write rule are fixed | None | AC1 |
| X2 | A record is published without the version group, without the data date or without the inputs digest | The schema validation fails the build; the groups are all required except for an access event | None | AC2 |
| X3 | The chain input is published without an order, an encoding or a first link | The chain fixture cannot reproduce the digests and the build fails | None | AC3 |
| X4 | A failure is published without its rollback behaviour, its identifier or its incident route | The failure matrix is incomplete and the build fails | None | AC4 |
| X5 | A record with the same key yields a second entry, or the repeat is not counted | The idempotency test fails the build | None | AC5 |
| X6 | The envelope is published with a type other than the fixed one, or with no key | The envelope validation fails the build | None | AC6 |
| X7 | A table, a path, a topic or a queue is claimed that the ownership map gives to another service | The boundary review fails and the row is corrected | None | AC7 |
| X8 | A value the consumers need is named by no source — the column set, the data-date column, the canonical form, the payload schema or the incident route | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1236; ASM-2200) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, an interface and a fake set; builds against no code and starts on Day 1 |
| Negotiable | Column widths, the canonical encoding and the fixture set are open until v1 is frozen; the interface, the field groups, the chain rule, the failure rule, the key rule and the envelope are fixed |
| Valuable | Unblocks the writer, the store ingest, the read path and every caller on Day 1 and keeps one record shape for the whole programme |
| Estimable | One interface, one record shape, one chain rule, one failure matrix, one key rule, one envelope, one table list and seven fakes |
| Small | One sprint for the document, the fixtures and the drift test |
| Testable | Each criterion below is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: decision log writer contract of rwb-decision

  Background:
    Given the contract document is published with major version 1
    Given the service owns one schema, one login, one topic and one task queue
    Given no production data is used in any example, schema or fake

  Scenario: AC1 The append interface the ledger accepts is published (new, D-RCV-60)
    Given the interface section of the contract document
    When it is validated and linted
    Then it publishes DecisionLogWriter.write(DecisionRecord) returning DecisionLogEntryRef, annotated with propagation MANDATORY and message identifiers MSG-P7-009 and MSG-P7-003 on its two exceptions
    Then DecisionLogEntryRef carries entryId, chainSeq, entryHash and repeated
    Then the write declares DecisionLogRecordInvalidException with messageId MSG-P7-009 and field, and DecisionLogUnavailableException with messageId MSG-P7-003, and no other thrown type
    Then a call with no open transaction throws IllegalTransactionStateException before any read or write
    Then the interface is declared as the local decision-record library of RWB-PLT-E1027-CON plus the service-local append of RWB-P7-E1008-APP, in process on task queue rwb-decision
    Then the document records that the Ownership Map names no write path for this service, and it declares no invented REST operation for the append

  Scenario: AC2 The record shape is fixed (new, D-RCV-60)
    Given the record-shape section of the document and its worked example
    When the schema is validated
    Then the shape carries the decision code, the rule ID with its rule version or the model or agent version, the case, the subject, the data date, the inputs reference with its digest, the previous hash, the entry hash, the actor role, the decided-at time and the created-at time
    Then it also carries the recommendation, the final call, the approver with an approval level, the actions and the outcome, as the legacy record does
    Then the version group requires at least one of rule version, model version and agent version, and a rule ID requires its rule version
    Then an access event carries no case and requires no subject group, and every other group stays required
    Then a record without the data date or without the inputs digest is refused, because a decision taken on stale data must be visible
    Then the example uses only the legacy values, with decision code D6, final call OWNER_ASSIGNED, rule ALLOC-MTG-BKK-01 of ALLOC-2026.11, case RW-2026-000123, actor SY-CASEWF and the inputs reference inputs/2026-12-03/7f3a

  Scenario: AC3 The hash-chain rule is fixed (new, D-RCV-60)
    Given the chain section of the document and the chain fixture
    When a first entry and a second entry are appended and the digests are recomputed independently
    Then the entry hash is the SHA-256 digest of the canonical form of the entry, rendered as 64 lowercase hexadecimal characters
    Then the canonical form fixes the field order, the null handling, the encoding and the separators, and no implementation may add a field to it
    Then the first entry carries 64 zeros as its previous hash, and every later entry carries the entry hash of the entry before it in chain sequence order
    Then the chain sequence is assigned by the store and never by the caller, and an entry is never updated and never deleted
    Then a recomputation that differs in any field fails the chain check and names the entry id and the field
    Then the document states that the nightly check of JOB-14 at 02:00 reads this rule and belongs to the store story

  Scenario: AC4 The failure, incident and retry rule is fixed (new, D-RCV-60)
    Given the failure section of the document and the failure matrix
    When each condition is compared with the legacy behaviour and the design
    Then a refused record writes nothing, raises with MSG-P7-009 and the field name, and leaves the caller's transaction to roll back
    Then a store, entry or outbox failure writes nothing, raises with MSG-P7-003, rolls the caller's action back and raises an incident to the platform administrator queue
    Then the writer itself never retries and never opens, commits or rolls back a transaction
    Then the caller retries with the kit policy of 1 s initial interval, back-off 2 and 10 attempts, and a refusal with MSG-P7-009 is declared non-retryable
    Then the central ledger being late never blocks a record: the outbox holds the event and only the points of no return wait for the ledger
    Then the document states that no condition writes a record for an action that did not take place

  Scenario: AC5 The idempotency key rule is fixed (new, D-RCV-60)
    Given the idempotency section of the document
    When a key is written twice
    Then the key is required on every record, and a record without it is refused with MSG-P7-009 naming "idempotencyKey"
    Then the key is scoped to the calling module, the event identifier and the decision code, and a unique key on the entry holds it
    Then a second record with the same key returns the first entry reference with repeated true, writes no second entry and adds one to the repeat counter of R-UNI-40
    Then the repeat counter is published as the metric decision_log_repeats_total and is named in the document
    Then the legacy value EV-7f3a-0001 is the example key

  Scenario: AC6 The DecisionRecorded envelope is fixed (new, D-RCV-60)
    Given the envelope section of the document
    When one record is validated against it
    Then the event is rwb.decision-record.DecisionRecorded.v1 published on the shared topic rwb.decision-record.v1 in CloudEvents 1.0 binary mode with ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header
    Then the record key is the caseId where the record has a case and the entry id where it does not
    Then the payload carries the entry id, the case where there is one, the decision code, the final call, the rule ID, the rule version, the chain sequence, the entry hash and the actor reference, and nothing else
    Then the payload carries no personal data, no free text and no rule payload
    Then the document states that the type differs from the platform library contract, which writes rwb.decision.DecisionRecorded.v1, and that the run convention fixes this type
    Then the document declares nothing on rwb.decision.events.v1 for this story, because the approval and rule events belong to other stories of this service

  Scenario: AC7 The owned tables, the naming and the fakes are fixed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the service owns decision_log_entry in rwb_decision plus the library tables outbox_event, processed_event and idempotency_key created in that schema
    Then delegation_limit is named as P4 rwb-access's, parameter_catalog, parameter_value, reference_row, reference_version and lov_value as P3 rwb-case's, and approval, rule_package, rule_package_version, rule_row and rule_test_case as other P7 stories', and none of them is declared as owned here
    Then the schema is rwb_decision, the base is /api/recovery/decision/v1, the topic is rwb.decision.events.v1 beside the shared rwb.decision-record.v1, the queue is rwb-decision and the package is th.co.scb.ace.workbench.recovery.decision
    Then the fakes answer an accepted record, a refusal with its field, a repeat, an append failure, the two data contracts, the rule version and the outbox
    Then the drift test of the app story and of every caller fails on any difference from sections 11, 12 and 13
```

These seven criteria are new for the contract baseline and test the artefact only; they restate no business outcome and copy no legacy criterion — **AC1 to AC7 of RWB-E1-027 stay with RWB-P7-E1027-APP**. Every identifier is taken character for character from the legacy story, the module specification or the Temporal and Drools Design.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract publishes one write surface, in process, declared `MANDATORY`, returning an entry reference and throwing only the two legacy exceptions | RWB-E1-027 section 12; DP-03; ADR-022 |
| BR2 | The record carries the legacy field groups, the data date and the inputs digest; the subject and the version group are not required for an access event | RWB-E1-027 BR2, BR3, BR4; DF-DEC-002 to DF-DEC-016; FEAT-DRI-12 |
| BR3 | An entry is linked to the one before it by `prev_hash` and carries its own `entry_hash`; the rule fixes the canonical form, the digest and the first link | Architecture v5 slide 28; Temporal and Drools Design slide 16; FSD P7 A2.1 AC-ALT-P7-001-01 |
| BR4 | A refused record writes nothing and names the field; a failed write rolls the caller's action back and raises an incident; the writer never retries | R-UNI-39; REQ-DRI-005; RWB-E1-027 sections 4 and 5 |
| BR5 | The same idempotency key gives one entry, the first reference and a counted repeat | R-UNI-40; RWB-E1-027 BR6 |
| BR6 | The record is announced on the shared topic in CloudEvents 1.0 binary mode with the type and the key rule of AC6, in the caller's transaction | DP-09; ADR-015; Architecture v5 slides 20, 22 and 42 |
| BR7 | The service owns `decision_log_entry` and the library objects in `rwb_decision` and declares no other service's table | DP-01; Ownership Map row `decision_log_entry`; Architecture v5 slide 41 |
| BR8 | No write path exists in the Ownership Map, so the contract declares no REST operation for the append and records the missing operation with its assumption | Ownership Map; Template and Rules §R9; DP-11 |
| BR9 | The contract writes no data-lake copy and no reporting copy; the legacy stream RWB-E1-014 is retired | DP-17; ADR-018; Template and Rules §R6 |
| BR10 | No Schedule, no Quartz row and no JOB element is declared: `JOB-13` has no target and `JOB-14` is the store story's | DP-10; Architecture v5 slide 44 |
| BR11 | The two read operations under the base are P7-owned and delivered by another story; this contract names them and never declares them | Ownership Map rows `GET /decision-log` and `GET /decision-log/{entryId}`; DP-13 |

### 9. State transitions

None at run time in this story: a document has no state. The record states it fixes are the ones the app story implements, and the version states are its own.

| Object | State | Meaning in the contract |
|---|---|---|
| Decision record | Unwritten | The caller has opened the transaction and not yet called the writer |
| Decision record | Validated | The field groups passed and the key is new |
| Decision record | Appended | The row exists with its chain link, visible inside the caller's transaction |
| Decision record | Committed | The caller committed; the entry, the change and the outbox row are stored together |
| Decision record | Refused | A field group failed; nothing is stored and the field is named |
| Decision record | Repeated | The key existed; the first reference is returned and the repeat is counted |
| DecisionRecorded | Published | The relay published it on the shared topic |
| DecisionRecorded | Absent | The transaction rolled back; no event exists |
| Contract version | v1 | The published version the app, the store, the read and every caller pin |
| Contract version | v2 | Raised by a breaking change, with a new `ce_type`; v1 stays readable and is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author of rwb-decision | Writes and versions the document, the interface section, the chain rule and the fakes |
| The service owner of rwb-decision | Approves a breaking change and freezes a version |
| The rwb-decision store owner | Confirms the append, the chain columns and the nightly check that read this rule |
| The rwb-access owner | Confirms the incident route to the platform administrator queue |
| The rwb-case owners of the parameters and the lists | Confirm the two data rows the record's codes and levels are read from |
| The platform library owner | Confirms the library interfaces, the record type and the envelope family this baseline implements |
| The callers (the app story, the approval story, the read story, the harness) | Review the parts they consume, pin the version and raise a change request rather than a private variant |
| RW-AUDIT, RW-COE | Audit the entries through the read operations, not through this contract |
| RW-PLATADM | Receives the incident of a failed write |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no e-mail address and no credential appears in the document, an example or a fake. Where an actor must be named, the story uses a role code or a user identifier only.

### 11. Data

| Item | Content |
|---|---|
| Record shape published | The legacy field groups DF-DEC-001 to DF-DEC-018, DF-DEC-030 and DF-DEC-031, the data date, the inputs digest, the previous hash and the entry hash |
| Personal data | None. The actor is a reference such as `SY-CASEWF` or a user identifier; the subject is a case or document identifier; no account number, national identifier or document content appears |
| Tables published | `decision_log_entry` in `rwb_decision`, plus the library objects `outbox_event`, `processed_event` and `idempotency_key` created in that schema; every other table is named as another owner's and never declared |
| Field identifiers | The record fields carry the legacy identifiers; the list values carry DF-REF-028 and DF-REF-029 and are read through the rwb-case contract |
| Data date | Carried on every record so that a decision taken on stale data is visible; the column name and the exact form are Not specified in the source documents (GAP-1236; ASM-2200) |
| Inputs digest | The reference and the digest of the snapshot the caller read; the digest algorithm is Not specified in the source documents (GAP-1236; ASM-2200) |
| Retention | The entry is append-only and kept; the retention period of the record and of the local store is Not specified in the source documents (GAP-1236; ASM-2200) |

The record shape is the one place where a rule value could leak into the contract, so the document fixes that a record carries codes and identifiers, the rule ID and the version label, and never the DRL, the payload of a rule evaluation or a personal field.

### 12. Contract

#### 12.1 REST operations provided

None. The base of the service is `/api/recovery/decision/v1` (DP-13), and the two operations the Ownership Map gives P7 under it are reads — `GET /decision-log` and `GET /decision-log/{entryId}` — owned by P7 and delivered by **RWB-P7-E2005-APP**. This baseline names them and declares neither, because a read of the ledger is not the write surface of the writer.

The write surface the baseline publishes is local:

| Element | Kind | Shape | Owner |
|---|---|---|---|
| `DecisionLogWriter.write` | Published interface, `MANDATORY` | `DecisionRecord` in, `DecisionLogEntryRef` out | P7, staged against RWB-PLT-E1027-CON |
| `DecisionLogStore.append` | Service-local append | Validated record plus chain link in, entry reference out | P7 store, RWB-P7-E1008-APP |
| `RecordAndApply` | Temporal activity on queue `rwb-decision` | Typed activity contract in the service's activity jar | P7, RWB-P7-E1027-APP |

A write operation over REST is absent from the Ownership Map and is Not specified in the source documents as an owned operation (GAP-1235; ASM-2199). The baseline therefore declares no path for the append, and a consumer that needs one raises it as a change request to the Ownership Map owner rather than adding a private path.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline | Contract |
|---|---|---|---|
| GET `/api/recovery/case/v1/admin/parameters/{code}` | P3 rwb-case | The decision code per event, so the contract refers to a value and holds no list | RWB-P3-E1042-CON |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION and LOV-APPROVAL-LEVEL, referred to and never copied | RWB-P3-E1043-CON |

Both rows are one hop with a 2 s timeout and are consumed by the implementation, not by the contract; the contract only fixes that the codes and levels are values in force and never constants. The field names behind the two operations are Not specified in the source documents beyond the list codes and the parameter keys (GAP-1236; ASM-2200).

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` (shared topic of DP-03) | `caseId` where the record has a case; the entry id where it does not | entry id, case ID where there is one, decision code, final call, rule ID, rule version, chain sequence, entry hash, actor reference | Announces every record to the central ledger and to the reporting read model; written to the outbox of `rwb_decision` in the caller's transaction |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | `rwb.decision-record.DecisionRecorded.v1` |
| ce_source | `/rwb-decision` |
| ce_subject | The case ID where there is one, the entry id where there is not |
| ce_id and traceparent | The event identifier and the W3C trace context of the caller |
| Payload | Identifiers, codes and dates only; no personal data and no free text |

The service's own topic is `rwb.decision.events.v1` and carries `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` from RWB-P7-E2013-APP and RWB-P7-E1073-CON; this baseline declares nothing on it. The type published here is the run convention for the shared topic; the platform library contract of RWB-PLT-E1027-CON writes the same event as `rwb.decision.DecisionRecorded.v1`, and the difference is recorded as a conflict of the two contract documents (GAP-1238; ASM-2202). The key rule for a record with no case, the exact payload schema beyond the fields listed and the `ce_subject` format are Not specified in the source documents (GAP-1236; ASM-2200).

#### 12.4 Events consumed

None. The writer is called in process and subscribes to nothing; the ingest of `DecisionRecorded` into the central ledger and the reporting projection belong to other stories and are not subscriptions of this contract.

#### 12.5 Workflows and activities

One activity and no workflow.

| Element | Queue | Input | Output | Note |
|---|---|---|---|---|
| `RecordAndApply` | `rwb-decision` in namespace `rwb-recovery` | The record, the decision code and the business date | Entry reference, chain sequence, entry hash | Declared as a typed activity contract; the retry policy of AC4 applies to it and not to the writer |

The writer is never called from workflow code: rules and I/O live in activities, so a replay reuses the recorded answer (DP-10). `ApprovalWorkflow` is the kit template of RWB-P7-E2013-APP and is not declared here.

#### 12.6 Schedules

None, and the contract says why. The legacy `JOB-13` decision log copy at 01:00 has no target: the ingest is continuous from the topic and the data lake is removed (Architecture v5 slide 44; DP-17). The nightly chain check `JOB-14` at 02:00 belongs to the store story RWB-P7-E1008-APP. The ACE shared Quartz tables and every JOB element are retired for this service (Template and Rules §R6, DP-10), so the baseline declares no cron entry, no job name and no shared scheduler row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| decision_log_entry | P7, in `rwb_decision` | The entry of every decision: the legacy field identifiers, the chain columns `chain_seq`, `prev_hash` and `entry_hash`, the data date, the final call and the decided-at time. Appended only |
| outbox_event | PLT library, created in `rwb_decision` | The `DecisionRecorded` row of AC6, written in the caller's transaction |
| processed_event | PLT library, created in `rwb_decision` | The inbox of this service; created with the schema and not used by the writer |
| idempotency_key | PLT library, created in `rwb_decision` | The stored key answer where an operation of this service carries one |

`delegation_limit` is P4 rwb-access's; `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case's; `approval` is P7's but belongs to RWB-P7-E2013-APP; `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's but belong to RWB-P7-E1073-CON and its app story. None of them is declared as owned here (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Writer fake | `DecisionLogWriter`, `DecisionRecord` and `DecisionLogEntryRef` | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field name; a repeated key with `repeated` true; a call with no transaction throwing IllegalTransactionStateException |
| Chain fixture | The chain rule of AC3 | A first entry with 64 zeros as its previous hash and chain sequence one; a second entry linked to the first; the recomputed digests; a refused update and a refused delete |
| Store fake | `DecisionLogStore.append` of RWB-P7-E1008-APP | An append that answers the entry reference; an append refused because the store is unavailable, raising `DecisionLogUnavailableException` with MSG-P7-003 |
| Outbox fake | `OutboxWriter` of RWB-PLT-TE006-CON | The event recorded in the caller's transaction, and absent after a rollback |
| Registry fake | The schema registry | BACKWARD mode, with one accepted and one refused `DecisionRecorded` body |
| rwb-case parameters fake | The parameters row of 12.2 | The four `rwb.decision.code.*` values with their version labels; an absent key |
| rwb-case reference-data fake | The lists row of 12.2 | LOV-DECISION with D6 and without D99; LOV-APPROVAL-LEVEL with L6 |
| Rule-registry fake | The rule package version label | Rule `R-UNI-14` with version `UNI-2026.11`, and the same rule with no version in force |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in the app story or in a caller rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the append is in process | 2: the parameters and the lists of rwb-case | One hop, 2 s; the two reads under the base belong to another P7 story and are named, not declared |
| Kafka | 1 event type fixed by the contract, published by the caller's outbox | 0 | AsyncAPI 3.0, CloudEvents 1.0 binary mode, key caseId or entry id on the shared topic |
| Temporal | 1 activity fixed by the contract | 0 | `RecordAndApply` on queue `rwb-decision`; no workflow and no Schedule |
| File | None | None | No file crosses the contract; the daily seal in write-once storage is the store story's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`: the interface, the record type, the entry reference and the failure matrix in `decision.api`; the chain rule and the envelope as contract resources of the service; the fake set as a test artefact. The implementation is RWB-P7-E1027-APP and the store is RWB-P7-E1008-APP.

**Interface surface**

| Interface | Signature | Returns or throws |
|---|---|---|
| `DecisionLogWriter` | `DecisionLogEntryRef write(DecisionRecord record)` annotated `@Transactional(propagation = Propagation.MANDATORY)` | The entry reference; throws `DecisionLogRecordInvalidException` (MSG-P7-009, field) and `DecisionLogUnavailableException` (MSG-P7-003) |
| `DecisionRecord` | decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, caseId, subjectType, subjectId, dataDate, inputsRef, inputsDigest, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, actorUserRef, decidedAt, idempotencyKey | The record the caller assembles from values it already holds |
| `DecisionLogEntryRef` | entryId, chainSeq, entryHash, repeated | The first entry reference of a key |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies are carried by the app story, because a CON story has none (Template and Rules §R5.7). No pattern is claimed for DP-02, DP-04, DP-05, DP-08, DP-12, DP-14, DP-16, DP-18 or DP-20: the contract adds no login, evaluates no rule package, reads no ACE view, declares no authorise call, runs no per-case workflow, renames no topic, calls no adapter, writes no ledger entry and calls no agent.

**Hardware and software change.** The contract moves the writer from one published interface over one table in the shared `recovery` schema to a service-local interface over `rwb_decision.decision_log_entry` with a fixed canonical chain form and one envelope on one shared topic. No new hardware is implied: the table is applied by this service's own Flyway run in the existing ACE PostgreSQL server and the event uses the Kafka platform ACE already runs.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLogWriter` and the two types | Published interface and types | The one write method, its `MANDATORY` rule and its two exceptions (AC1, AC2) |
| ChainRule | Contract resource | The canonical form, the digest, the first link and the no-rewrite rule (AC3) |
| FailureMatrix | Contract resource | One row per condition with its rollback, its identifier, its incident route and its retry verdict (AC4) |
| IdempotencyRule | Contract resource | The key, its scope, the stored answer and the repeat counter (AC5) |
| EnvelopeSpecification | Contract resource | The CloudEvents attribute set, the type, the key rule and the payload fields (AC6) |
| Fake set and fixtures | Test asset | The eight fakes of 12.8, used by the app story and every caller (AC7) |

**Build steps**

1. Write the interface and the two types, taken from the legacy published interface; lint the `MANDATORY` rule and the throw-before-write rule (AC1).
2. Write the record shape with the field groups, the access-event exception and the legacy example (AC2).
3. Freeze the canonical form and the digest rule, and publish the chain fixture; recompute the fixture independently and assert the first link (AC3).
4. Write the failure matrix with one row per condition and assert that no condition writes a record of an action that did not happen (AC4).
5. Write the idempotency rule and the metric name; test the repeat and the counter (AC5).
6. Write the envelope section and validate one accepted and one refused body against the registry fake (AC6).
7. Publish the table lists, the naming block and the fakes; add the drift test to the build of the app story and of every caller (AC7).
8. Tag v1 and record the pinned versions of the store, the app, the read and the harness.

**Done when.** The document, the interface and the fixture validate, the chain fixture recomputes, the eight fakes answer every criterion including the refusal, the repeat, the absent event and the broken chain, the drift test is green on the app story and on one caller, and v1 is tagged with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException`, messageId MSG-P7-009, with `field` |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException`, messageId MSG-P7-003 |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary of the caller) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. | Named only; the caller owns the display |
| MSG-P4-002 | The role lacks the right of the capability area | You cannot {action} here. Your role does not include it. | The service guard, before the writer is reached |

The texts are copied unchanged from RWB-E1-027 section 14 and this contract adds no message ID. The field names of the three refusals are `versions`, `ruleVersion` and `decisionCode`, with `approvalLevel` for the group of BR4 and `idempotencyKey` for AC5. The published catalogue entry format of MSG-P7-009 and MSG-P7-003 is Not specified in the source documents (GAP-1236; ASM-2200). Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: the writer has no user interface and answers inside the caller's transaction. The two read operations and the screens built on them belong to RWB-P7-E2005-APP and are reached through the gateway-bff composite route (DP-19, RWB-PLT-N001-CON); a refused record appears as an incident of RWB-PLT-E1056-OPS, not as a screen error.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E1027-CON-01 | AC1 | Contract | The interface section linted against the legacy published interface; the `MANDATORY` annotation; the two exceptions and their identifiers; the no-transaction call refused before any read; the missing owned operation recorded |
| TC-P7-E1027-CON-02 | AC2 | Contract | The record shape validated against the field groups; the access-event exception; the data date and the inputs digest required; the legacy example with D6, OWNER_ASSIGNED, ALLOC-MTG-BKK-01 of ALLOC-2026.11, RW-2026-000123 and SY-CASEWF; a personal-data scan |
| TC-P7-E1027-CON-03 | AC3 | Component | A first entry with 64 zeros and chain sequence one; a second linked to the first; the digests recomputed independently; a one-field difference refused; an update and a delete refused |
| TC-P7-E1027-CON-04 | AC4 | Contract | The failure matrix asserted row by row: refusal, store failure, outbox failure, no retry in the writer, the kit policy, the late ledger, and the incident route |
| TC-P7-E1027-CON-05 | AC5 | Contract | The key `EV-7f3a-0001` written twice; the first reference returned with repeated true; one entry; the counter incremented; a record without a key refused |
| TC-P7-E1027-CON-06 | AC6 | Contract | One record validated against the envelope: the attribute set, the type, the key with a case and the key without one, the payload fields; one accepted and one refused body; the type conflict recorded |
| TC-P7-E1027-CON-07 | AC7 | Component | The eight fakes answering every example; the owned and not-owned table lists; the naming block; the drift test on the app story and on a caller |

The legacy test case set of RWB-E1-027 is carried by RWB-P7-E1027-APP and RWB-ITG-E1027-ITG; these seven are the contract's own tests and no legacy identifier is renumbered.

### 17. Guardrails

- No business value in the contract: the decision codes and approval levels are values in force in the owner's data, and the only values this document fixes are the legacy example values.
- No personal data in a schema, an example, a fake or a log: the actor is a reference, the subject is a case or document identifier, and the scan fails the build otherwise.
- No cross-schema reference and no foreign key across services; the boundary test fails the build.
- No write path to `decision_log_entry` other than the writer, no update path at all, and the architecture test is part of the contract test of every caller.
- No REST surface invented for the append: the missing owned operation is carried as a gap and an assumption, never as a path.
- No second event type and no second topic for one record: the shared topic and one type per major version.
- No Schedule, no Quartz row and no JOB element is declared; the retired elements stay retired.
- A published version is never edited in place: a breaking change raises major version 2 with a new `ce_type` and a migration note.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Contract element | Test cases |
|---|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | Epic 1, 3.7; Program, 5.7 | The record shape, the chain rule, the envelope and the owned tables | TC-P7-E1027-CON-02, TC-P7-E1027-CON-03, TC-P7-E1027-CON-06 |
| REQ-DRI-005 | No action proceeds if its entry cannot be written | Epic 1, 3.7; Program, 5.7 | The `MANDATORY` rule, the failure matrix and the idempotency rule | TC-P7-E1027-CON-01, TC-P7-E1027-CON-04, TC-P7-E1027-CON-05 |
| RWB-E1-027 | The legacy key whose contract this baseline fixes | Epic 1, 3.7 | The seven criteria of section 7 | TC-P7-E1027-CON-01 to TC-P7-E1027-CON-07 |

| Element | Where it is fixed | Test cases |
|---|---|---|
| DP-03, DP-09, ADR-015, ADR-022 | The envelope of AC6, the outbox rule and the chain rule of AC3 | TC-P7-E1027-CON-03, TC-P7-E1027-CON-06 |
| DP-01, DP-13, DP-15, ADR-014, ADR-021 | The owned and not-owned lists and the naming block of AC7 | TC-P7-E1027-CON-07 |
| DP-06, DP-07 | The two data rows of 12.2 | TC-P7-E1027-CON-02 |
| DP-10 | 12.5 and 12.6 | TC-P7-E1027-CON-04 |
| DP-17, ADR-018 | The retirement of the lake stream, BR9 | TC-P7-E1027-CON-07 |
| DP-11, ADR-020 | The one-hop rule and the fetch timeout behind the two data rows | TC-P7-E1027-CON-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1027-APP | App development | H consumer: implements the interface, the validator, the chain and the publisher against this baseline and its fakes |
| RWB-P7-E1008-APP | App development | H consumer: the store, the append, the chain columns and the nightly check that read this rule |
| RWB-PLT-E1027-CON | Contract | The library interfaces and the envelope family this baseline implements; the source of the type conflict of AC6 |
| RWB-P7-E2005-APP | App development | The two read operations under the base, named and not declared here |
| RWB-P7-E2013-APP | App development | Calls the writer for approval decisions; its `approval` table and its workflow are not declared here |
| RWB-P7-E1073-CON | Contract | The rule package version label the record carries |
| RWB-PLT-TE006-CON | Contract | The outbox writer and the envelope family of the published event |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | The parameters and reference-data clients behind the two data rows |
| RWB-PLT-E1071-CON | Contract | The activity contract and the kit retry policy |
| RWB-PLT-E1044-CON | Contract | The per-service Flyway sequence of `rwb_decision` |
| RWB-PLT-N001-CON | Contract | The gateway route of the reads and of the incident view |
| RWB-ITG-E1027-ITG | Integration | The end-to-end proof of the writer and the ledger on real services |
| RWB-PLT-E1056-OPS | DevOps | X: the incident route and the dashboards of a failed write |

### 19. Out of scope

- The implementation — the validator, the chain, the idempotency path, the append and the publisher: RWB-P7-E1027-APP.
- The store, the append-only rule, the chain columns and the nightly check at 02:00: RWB-P7-E1008-APP.
- The two read operations under `/api/recovery/decision/v1` and the screens: RWB-P7-E2005-APP.
- The approval records, the `ApprovalWorkflow` and the delegation limit: RWB-P7-E2013-APP and P4 rwb-access.
- The rule registry, the rule package versions and their promotion: RWB-P7-E1073-CON and its app story.
- The parameters and the lists, owned by P3 rwb-case and consumed here.
- The platform library interfaces and the record type: RWB-PLT-E1027-CON.
- The outbox and inbox DDL, the retry topics and the dead-letter topic: RWB-PLT-TE006-CON and RWB-PLT-EVT.
- The retired data-lake copy of the decision log: RWB-E1-014, no target path (DP-17).
- The access-event records: P4 rwb-access, RWB-E1-039.
- The recommendation with the reasons for the route decision: Epic 4.
- The deployment, the consumer groups, the dashboards and the runbook of the service: RWB-PLT-E1056-OPS.
