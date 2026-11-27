# RWB-ITG-E1027-ITG Decision log writer v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-027 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1027-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1027-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-E1027-CON, RWB-P7-E1027-CON |
| Contract version | v1: the /v1 path of the two ledger reads, with the contract baselines RWB-P7-E1027-CON and RWB-PLT-E1027-CON at v1 |
| Integration dependencies | RWB-PLT-E1027-APP, RWB-P7-E1027-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-027 decision log writer across the platform decision-record library (PLT) and the central decision ledger of rwb-decision (P7)**, so that **the four Epic 1 records, the refusals, the transactional stop and the ledger read are proved on real services before wave 1 exits**.

### 2. Business rationale

The legacy story gives every module one published writer, `DecisionLogWriter`, that validates a record against the seven field groups, writes it in the caller's transaction, ignores a repeated event and publishes `DecisionRecorded`. In the target that writer is not application code inside one module: it is the **platform decision-record library** delivered by RWB-PLT-E1027-APP, and the place an auditor searches is the **central ledger** `rwb_decision` of P7 rwb-decision, fed from the shared topic `rwb.decision-record.v1` (DP-03, ADR-022). The caller still owns the action and the transaction, the library writes the record inside that same transaction, and the ledger collects the record asynchronously — which is why the local write stops an action and the ledger does not.

The target split for the legacy key is therefore: **RWB-PLT-E1027-APP owns the writer library** — the record contract, the validator, the transaction rule, the idempotency rule and the DecisionRecorded publication; **RWB-P7-E1027-APP owns the central ledger** — the `rwb_decision` store, the continuous Kafka ingest (JOB-13), the hash-chain check (JOB-14) and the two read operations `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}`. The legacy acceptance criteria **AC1 to AC7 stay with RWB-P7-E1027-APP**, and the writer library is proved at component level by **RWB-PLT-E1027-APP**; this story owns no legacy AC and adds fourteen new ones that only exist when the library and the ledger are exercised together.

Three target facts cannot be proved inside one service. **First**, the record is written in the caller's transaction and leaves only through the shared topic: a test that reads a local table would pass while the publication was broken, so the suite asserts the record in the P7 ledger and on `rwb.decision-record.v1` for the same commit. **Second**, decision codes are parameters and list values in the target owner's data (DP-06, DP-07): the suite never hard-codes a code, it asserts the values in force, and the P3 ownership of the parameter and reference-data stores is recorded in GAP-0352 and ASM-0446. **Third**, the legacy data-lake copy of the decision log (RWB-E1-014) is retired and no lake copy exists (DP-17, ADR-018); the absence is a cross-service fact that the suite must assert, because a leftover copy would be invisible from any one service.

No service contract is faked in this story. The PLT decision-record library conformance caller is the real library delivered by RWB-PLT-E1027-APP, exercised in a real transaction, and every ledger read goes to the real P7 service in SIT; the four records are produced by the wave 1 callers rwb-case and rwb-document through the same library, so those services are the run environment and the declared integration dependencies stay the library and the ledger that own the behaviour under test. The only stubs are the external ones named in section 12.8.

### 3. Preconditions

- RWB-PLT-E1027-APP is done: the decision-record library, its record contract, its validator, the mandatory-transaction rule, the idempotency rule and the DecisionRecorded publication are released to every consuming service.
- The library coordinates (group, artefact name and publication channel) are those of the platform library baseline: Not specified in the source documents (GAP-1402). A record with no case is keyed on the entry id, each service schema holds one chain with the hash algorithm shared with P7 rwb-decision, and a failed write is routed as an incident through the service's own alerting.
- The record schema, the DDL template and the CloudEvents envelope are the working read of the record contract at major version 1; they are frozen when the consuming stories pass their contract tests, and the ledger side is confirmed with P7 rwb-decision in the verification loop.
- RWB-P7-E1027-APP is done: the central ledger `rwb_decision` is in place with the continuous ingest, the chain columns, the two decision-log read operations and the Decision log R check.
- The audit search reads the central ledger only and shows an entry as not yet sealed until JOB-13 has collected it. The local record is reached through the owning service's contract, and strict mode waits for the ledger acknowledgement of its own record.
- The published contracts of P7 rwb-decision are deployed under `/api/recovery/decision/v1`, and the shared topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics and the schema-registry entry of `rwb.decision.DecisionRecorded.v1`.
- The wave 1 producers that write the four Epic 1 records are deployed in SIT with the library bound: rwb-case for case created, owner assigned and case transferred, and rwb-document with the OCR intake for document attached.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic case, document and event fixtures.
- The environment is SIT with the Temporal namespace rwb-recovery and the JOB-14 Schedule registered by the rwb-decision release.
- No production data is used and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. QA integration engineer: seeds the synthetic case, document and event fixtures of the harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: reads the decision codes and list values in force for the four Epic 1 final calls through the owner's published contract, so the expected codes are values in force and not constants in the test code.
3. Harness: creates case RW-2026-000123 and has JOB-03 give it an owner by row ALLOC-MTG-BKK-01 of ALLOC-2026.11, then transfers it under TRF-2026.11 and attaches document DOC-2026-0009981; each caller writes its record through the library as the last step before commit.
4. Harness: consumes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for each of the four records and asserts the CloudEvents envelope, the key caseId, the decision code, the final call, the rule ID and the rule version.
5. Harness: polls `GET /api/recovery/decision/v1/decision-log` for the case and `GET /api/recovery/decision/v1/decision-log/{entryId}` for one entry, and asserts that the ledger holds each record within 5 minutes of the commit, with the decision code, the final call, the rule ID, the package version and the chain sequence.
6. Harness: posts the negative records through the conformance caller — no version group, a rule ID with an empty rule version, a decision code outside the list and a call with no open transaction — and asserts the exact message and field name, and that no record and no event exist afterwards.
7. Harness: forces the library write to fail during JOB-03 for case RW-2026-000124 and asserts that the allocation rolls back, that the case owner stays empty, that the status stays "New" and that an incident reaches the platform administrator queue.
8. Harness: sends event EV-7f3a-0001 twice with the same idempotency key and asserts one record, the first entry ID returned and the repeat counted, then asserts one ledger entry for the event.
9. Harness: asserts the absence of any data-lake copy of the decision log and of any reporting copy written by the writer, and records that the legacy lake copy RWB-E1-014 is retired.
10. Harness: reads the ledger with a role that lacks Decision log R, records the 403 and MSG-P4-002, writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record misses the version group, the inputs reference, the final call or the case | The library refuses the record and names the missing field; the caller's action rolls back and nothing is published | MSG-P7-009 | AC2 |
| X2 | A record carries a rule ID with no rule version | Refused as X1, with the field named as the rule version | MSG-P7-009 | AC3 |
| X3 | The record cannot be written and the transaction cannot commit | The caller's action rolls back; an incident is raised to the platform administrator queue | MSG-P7-003 | AC4 |
| X4 | The same event arrives twice with the same idempotency key | One record; the first entry ID is returned and the repeat is counted | None | AC5 |
| X5 | The library is called outside a transaction | Refused with IllegalTransactionStateException; nothing is written and nothing is published | None | AC6 |
| X6 | A record carries a decision code not in the list in force | Refused as X1, with the field named as the decision code | MSG-P7-009 | AC7 |
| X7 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning story and no fake is put in its place | None | Preflight, AC1, AC8 |
| X8 | The PLT conformance caller or its fixture set does not match the library release | The suite fails as a harness fault and names the mismatched element; no service defect is raised and no production value is substituted | None | AC1, AC6 |
| X9 | A record is not in the central ledger within 5 minutes of the commit | The suite fails AC8 and names the entry and the elapsed time; the gap alert of P7 is read as evidence, and the point-of-no-return wait is reported as an observation, not as a pass | None | AC8 |
| X10 | The same DecisionRecorded event is delivered to P7 twice | The ledger inbox ignores the second delivery, one ledger entry remains and the record count is unchanged | None | AC5, AC8 |
| X11 | A suite step tries to read a service schema directly | The step does not exist: the suite ships with no client for a service schema, and the pipeline scan fails any change that adds one | None | AC11 |

X1 to X6 are the legacy exception paths carried onto the real library and the real ledger; X7 to X11 are the cross-service failures that only appear when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the two integration dependencies and the published contracts of P7, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval and the 5-minute observation window are configuration; the messages, the field names, the final calls and the rule versions are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one library for all writers, the record in the caller's transaction, the record in the central ledger, the counted repeat and the absence of a lake copy |
| Estimable | One suite module, one conformance caller driver, two ledger reads, one event probe, one failure switch and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a library response, a REST response, a Kafka event, a ledger entry or a message |

### 7. Acceptance criteria

```gherkin
Feature: Decision log writer v1, proven across the platform library and the P7 central ledger

  Background:
    Given the wave 1 services rwb-case, rwb-document and rwb-decision are deployed in SIT with their published contracts
    Given the platform decision-record library RWB-PLT-E1027-APP is bound in the calling services
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used
    Given allocation table version "ALLOC-2026.11" and transfer rule version "TRF-2026.11" are in force

  Scenario: AC1 Four Epic 1 records are written through the library (new, D-RCV-60)
    Given case "RW-2026-000123" is created, given an owner by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11", transferred under "TRF-2026.11" and given document "DOC-2026-0009981"
    When the four records are written through the library in the caller's transaction
    Then four records exist for the case with final calls "CASE_CREATED", "OWNER_ASSIGNED", "CASE_TRANSFERRED" and "DOCUMENT_ATTACHED"
    Then the second record carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11" and actor "SY-CASEWF"
    Then each record carries an inputs reference and the version group in force
    Then each record leaves as one rwb.decision.DecisionRecorded.v1 event on rwb.decision-record.v1

  Scenario: AC2 A record with no version group is refused (new, D-RCV-60)
    Given a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version
    When it is written through the library
    Then the library refuses it with message MSG-P7-009 naming "versions"
    Then the writer logs the error with the case ID and the missing field only
    Then the transfer in the same transaction is rolled back and no record and no event exist

  Scenario: AC3 A rule ID with an empty rule version is refused (new, D-RCV-60)
    Given a record with rule ID "R-UNI-14" and an empty rule version
    When it is written through the library
    Then the library refuses it with message MSG-P7-009 naming "ruleVersion"
    Then no record and no event are written

  Scenario: AC4 A failed write stops the action (new, D-RCV-60)
    Given the decision-record write of the library fails and cannot be committed
    When JOB-03 gives case "RW-2026-000124" to owner "U-7102"
    Then the write raises DecisionLogUnavailableException
    Then the case owner stays empty and the case status stays "New"
    Then an incident is raised to the platform administrator queue
    Then no record and no DecisionRecorded event exist for the case

  Scenario: AC5 The same event gives one entry and a counted repeat (new, D-RCV-60)
    Given event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written
    When the same event with idempotency key "EV-7f3a-0001" arrives again
    Then one record exists for the event
    Then the library returns the first record's entry ID and adds 1 to the repeat count for R-UNI-40
    Then the central ledger holds one entry for the event

  Scenario: AC6 A write outside a transaction is refused (new, D-RCV-60)
    Given a caller without an open transaction
    When it calls the library write
    Then the library refuses the call with IllegalTransactionStateException
    Then nothing is written and no event is published

  Scenario: AC7 An unknown decision code is refused (new, D-RCV-60)
    Given a record with decision code "D99"
    When it is written through the library
    Then the library refuses it with message MSG-P7-009 naming "decisionCode"
    Then no record and no event are written

  Scenario: AC8 The record reaches the central ledger within 5 minutes (new, D-RCV-60)
    Given a record was written and committed for case "RW-2026-000123"
    When the entry is read by entry ID through GET /api/recovery/decision/v1/decision-log/{entryId}
    And the case is read through GET /api/recovery/decision/v1/decision-log
    Then the ledger holds the record within 5 minutes of the commit
    Then the entry shows the decision code, the final call, the rule ID, the package version and the chain sequence
    Then the same entry is the one announced by rwb.decision.DecisionRecorded.v1

  Scenario: AC9 No data-lake copy of the decision log exists (new, D-RCV-60)
    Given the legacy decision-log copy to the data lake, RWB-E1-014, is retired
    When a record is written and collected into the P7 central ledger
    Then no data-lake copy of the decision log exists
    Then the writer writes no reporting copy and publishes no reporting event of its own
    Then the only copy outside the caller's schema is the central ledger entry of rwb-decision

  Scenario: AC10 A role without Decision log R is refused by the ledger (new, D-RCV-60)
    Given a user holds a role without Decision log R
    When the user reads the decision log through GET /api/recovery/decision/v1/decision-log
    Then the P7 service refuses the call with status 403 and MSG-P4-002
    Then no entry content is returned

  Scenario: AC11 A suite step cannot read a service schema directly (new, D-RCV-60)
    Given a change adds a client for a service schema to the suite
    When the pipeline scan runs over the change
    Then the scan fails the change
    Then the suite holds no client for a service schema

  Scenario: AC12 An approver without an approval level is refused (new, D-RCV-60)
    Given a record for case "RW-2026-000123" carries an approver and no approval level
    When it is written through the library
    Then the library refuses it with message MSG-P7-009 naming "approvalLevel"
    Then no record and no event are written

  Scenario: AC13 Decision codes are asserted as the values in force (new, D-RCV-60)
    Given the decision codes and list values in force are read through the owner's published contract
    When the suite asserts the four Epic 1 records
    Then each decision code is compared with the values in force
    Then the suite holds no decision code constant of its own as an expected value

  Scenario: AC14 Every call of the suite is one hop with a 2 s timeout (new, D-RCV-60)
    Given the suite is configured with its client budget
    When it calls a service
    Then the call goes to the owning service in one hop with a 2 s timeout
    Then nothing is called through another service
```

**Target reading.** The writer is the platform decision-record library of RWB-PLT-E1027-APP and the record is written in the caller's transaction (DP-03, ADR-022); the ledger is `rwb_decision` behind the two P7 read operations (DP-01, DP-13). The record leaves on the shared topic `rwb.decision-record.v1` in the CloudEvents envelope with key caseId (DP-09, ADR-015), and the decision codes, list values and rule versions are read as values in force from the target owners (DP-06, DP-07) rather than pasted into the test code; the P3 ownership of those stores is recorded in GAP-0352 and ASM-0446. No service table is read and no value is invented. Stored documents are asserted through the P5 contract of rwb-document, cases through the P3 contract and party keys through the P1 customer contract, and the decision record is read on `rwb.decision-record.v1`; the central ledger is proved in this story. Each service creates its local decision-record table in its own schema through the decision-record library, with the case reference and the trace ID carried in inputsRef; the table name and DDL are settled in the DB story of each service. Each service chains its own records in chain_seq order, the central ledger chains its entries on ingest, the daily WORM fingerprint covers the ledger chain, and the chain of record is the ledger, with the local chain kept for replay. The canonical form of the entry hash is that of RWB-E1-008 BR4: `entry_hash` is the SHA-256, in lower-case hexadecimal, of the entry's fields except `entry_hash` and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings and empty fields as null; the first `prev_hash` is 64 zeros.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Epic 1 writes records for case created, owner assigned, case transferred and document attached | REQ-DRI-004; RWB-E1-027 BR1 | AC1 |
| BR2 | Required on every record: a decision code from the decision list, an inputs reference, a final call, the decided-at time and the actor; the case unless the decision code is an access event | RWB-E1-027 BR2; DF-DEC-002, DF-DEC-003, DF-DEC-008, DF-DEC-012, DF-DEC-016 | AC1, AC7 |
| BR3 | The version group needs at least one of rule version, model version and agent version, except for access events; a rule ID needs its rule version | RWB-E1-027 BR3; DF-DEC-004 to DF-DEC-007; NFR-034 | AC2, AC3 |
| BR4 | An approver needs an approval level from the approval-level list on the same record | RWB-E1-027 BR4; DF-DEC-010, DF-DEC-011; FEAT-DRI-04 | AC12 |
| BR5 | The record is written in the caller's transaction; if it cannot be written, the action does not proceed | RWB-E1-027 BR5; R-UNI-39; CTL-06; REQ-DRI-005 | AC4 |
| BR6 | The same event with the same idempotency key gives one record, and the repeat is counted | RWB-E1-027 BR6; R-UNI-40 | AC5 |
| BR7 | Decision codes for the Epic 1 events are parameters and list values, not code | RWB-E1-027 BR7; DP-06; DP-07 | AC1, AC7 |
| BR8 | One writer for all nineteen services: the platform decision-record library of RWB-PLT-E1027-APP, with no service building its own writer or writing a ledger table | DP-03; ADR-022; Architecture v5 slide 20 | AC1 |
| BR9 | The record leaves the caller as one `rwb.decision.DecisionRecorded.v1` event on `rwb.decision-record.v1`, CloudEvents 1.0, key caseId, written to the outbox in the same transaction | DP-03; DP-09; ADR-015; Architecture v5 slides 20, 28 and 42 | AC1 |
| BR10 | The central ledger is `rwb_decision` of P7 rwb-decision, read only through `GET /api/recovery/decision/v1/decision-log` and `.../{entryId}`; no other service reads or writes it | DP-01; Architecture v5 slides 14 and 41 | AC8, AC10 |
| BR11 | Decision codes are P3 parameters and list values in the target, and list values are P3 reference data; the suite asserts the values in force and never a constant of its own | DP-06; DP-07; ASM-0446 | AC13 |
| BR12 | The ledger collects the record asynchronously and is complete within 5 minutes; only points of no return wait for the ledger confirmation, so an ordinary action is never blocked by ledger lag | Architecture v5 slide 28; Temporal and Drools design slide 28 | AC8 |
| BR13 | No data-lake copy of the decision log exists; the legacy copy RWB-E1-014 is retired and the writer writes no reporting copy of its own | DP-17; ADR-018; Template and Rules v1 §R6 | AC9 |
| BR14 | Every call of the suite is one hop with a 2 s timeout; nothing is called through another service, and the ledger view for a screen goes through gateway-bff | ADR-020; DP-11; DP-19 | AC14 |
| BR15 | No personal data in records, events, logs or fixtures beyond the actor reference and the case and document identifiers; a refused record is logged with its case ID and field name only | RWB-E1-027 section 17; ADR-015 | AC2 |

### 9. State transitions

None. This story does not change a case status. It makes a status change made by another service depend on its record: when the write fails, the case stays in the status it had, for example "New" in AC4.

| Object | State | Meaning |
|---|---|---|
| Decision record | Unwritten | The caller has opened the transaction and not yet written the record |
| Decision record | Written in the transaction | The library has validated the record and appended it inside the caller's transaction |
| Decision record | Committed | The caller committed; the action, the record and the outbox row are stored together |
| Decision record | Refused | The library refused the record and named the field; nothing is stored and nothing is published |
| Decision record | Repeated | The same idempotency key returned the first entry ID and the repeat count was incremented |
| DecisionRecorded | Published | The outbox relay published the event on `rwb.decision-record.v1` |
| Central ledger entry | Ingested | P7 consumed the event into `rwb_decision` within 5 minutes of the commit |
| Central ledger entry | Collected late | The event is not yet in the ledger; the gap alert is raised and only points of no return wait |
| Case | New | Unchanged by this story; the status the case keeps when its action rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the failure switch and the evidence report |
| Service owner of the platform decision-record library | Owns the record contract, the validator, the transaction rule, the idempotency rule and the publication |
| Service owner of rwb-decision | Owns the central ledger, the continuous ingest, the chain check and the two decision-log read operations |
| Service owner of rwb-case | Owns case created, owner assigned and case transferred, and calls the library for each |
| Service owner of rwb-document | Owns document attached and calls the library for it |
| Platform administrator | Receives the incident when a record cannot be written and the gap alert when the ledger lags |
| Every role holding Decision log R | Reads the ledger through the P7 contract inside its scope |
| No role | Writes a ledger table directly, or reads a service schema from the suite |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 rwb-decision central ledger; written by the library in the caller's schema) | all fields | Write through the library, read through the P7 contract |
| DF-DEC-030 | decision_log_entry (P7 rwb-decision central ledger) | actor_user_id | Write through the library, read through the P7 contract |
| DF-DEC-031 | decision_log_entry (P7 rwb-decision central ledger) | idempotency_key | Write, read through the library and the P7 contract |
| DF-REF-028 | lov_value (P3 rwb-case reference data in the target) | lov_code | Read through the owner's contract |
| DF-REF-029 | lov_value (P3 rwb-case reference data in the target) | value_code | Read through the owner's contract |
| Cross-service row | Decision codes and list values in force, and the conformance caller fixtures | Values and fixture set used by the suite | Not specified in the source documents (GAP-0352; ASM-0446) |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-027 unchanged. The legacy story writes `decision_log_entry` in the recovery schema and reads `lov_value` through the P4 list service; in the target the ledger lives in `rwb_decision` of P7, the decision codes are P3 parameters and the list values are P3 reference data (DP-01, DP-06, DP-07), so every row is written through the library and read through an owner's contract. The suite owns no field and no table. Every value in the run is synthetic.

The physical column list and widths of `decision_log_entry` are those of `06 Data/Recovery Workbench Physical Schema v7/rwb_decision.sql`. The data-date column, the inputs digest algorithm, the retention of a local record and the catalogue entry format of MSG-P7-009 and MSG-P7-003 are Not specified in the source documents (GAP-1236).

### 12. Contract

#### 12.1 REST operations provided

None. The decision-record write is a local operation, not a REST operation: the platform decision-record library appends in process in the caller's transaction (DP-03), with the service-local append, and no REST append is declared; the Ownership Map does not yet list this operation (GAP-1235). The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Read the records of a case; assert the four Epic 1 records and the ledger completeness of AC8 |
| GET /api/recovery/decision/v1/decision-log/{entryId} | P7 rwb-decision | Read one entry; assert decision code, final call, rule ID, package version and chain sequence of AC8, and the 403 of AC10 |

Every call is one hop with a 2 s timeout (ADR-020, DP-11, DP-13).

#### 12.3 Events published

None. The suite publishes no event; the records are written by the calling services through the library and the events are theirs.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | all 19 services; collected by P7 rwb-decision | Assert one event per record, the CloudEvents envelope, key caseId, the decision code, the final call, the rule ID and the rule version; assert the dedupe of AC5 |

The payload is the published schema of the producer; the same event is what the ledger ingests into `rwb_decision` (DP-03, DP-09).

#### 12.5 Workflows and activities

None of its own. The P7 ledger ingest is continuous Kafka consumption (JOB-13) with no workflow, and `ApprovalWorkflow` — the kit template that P7 runs for approvals — is out of scope for this story. The suite starts no workflow.

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| JOB-13 | Decision log copy | Continuous Kafka ingest, no schedule | rwb-decision | The ingestion path the suite observes; the legacy 01:00 batch is retired |
| JOB-14 | Hash-chain check | 02:00 | rwb-decision | Observed: the chain check reads the same entries and reports a break as an alert |

The suite registers no Schedule and triggers none.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01).

#### 12.8 Contract fakes

No service contract is faked, and no contract fake of rwb-decision is named or published, so no fake library version applies. The PLT decision-record library conformance caller is the **real library** delivered by RWB-PLT-E1027-APP, invoked in a real transaction, and every P7 call goes to the real service in SIT. External stubs only:

| Stub | Use |
|---|---|
| RWB-ITG-W1J01-ITG synthetic fixture set | The synthetic cases, documents and event identifiers used by the run |
| Mock Entra sign-in | Synthetic test identities, including the role without Decision log R of AC10 |

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 2 (the decision-log reads of section 12.2) |
| Kafka | 0 | 1 event type (`rwb.decision.DecisionRecorded.v1`) |
| Temporal | 0 | 1 Schedule observed (JOB-14) and 1 continuous ingest (JOB-13) |
| File | 0 | None |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a conformance caller driver for the real PLT library, a fixture builder, an event probe, two ledger probes, a failure switch and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts and the library release, run order, report and exit code |
| LibraryCallerDriver | Test harness | Drives the real PLT conformance caller inside a real transaction; builds the four Epic 1 records, the negative records and the no-transaction call |
| FixtureBuilder | Test harness | Seeds the synthetic case RW-2026-000123, case RW-2026-000124, document DOC-2026-0009981 and event EV-7f3a-0001 of the W1J01 set |
| ValueReader | Test harness | Reads the decision codes, list values and rule versions in force through the owner's contract; the suite holds no constant for them |
| EventProbe | Test harness | Consumes `rwb.decision.DecisionRecorded.v1`, asserts the envelope, the key, the count per record and the absence of a personal data field |
| LedgerProbe | Test harness | Polls the two P7 reads within the 5-minute window and asserts decision code, final call, rule ID, package version and chain sequence; holds the 403 path of AC10 |
| FailureSwitch | Test harness | Makes the library write fail for case RW-2026-000124 and proves the rollback, the unchanged owner and status and the incident |
| LakeAbsenceProbe | Test harness | Asserts that no data-lake copy of the decision log exists and that the writer writes no reporting copy |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, plus the cleanup record |

**Configuration**

- The SIT endpoint of P7 rwb-decision, the topic `rwb.decision-record.v1`, the schema-registry address and the namespace `rwb-recovery`, all as configuration.
- The synthetic case, document and event identifiers of the W1J01 set and the poll interval, with the 5-minute observation window of AC8 as a property.
- The decision codes, list values and rule versions read through the owner's contract (DP-06, DP-07); the versions "ALLOC-2026.11" and "TRF-2026.11" are the ones in force for the run.
- The 2 s client budget and the test identity of the role without Decision log R.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Synthetic case and document set | Case RW-2026-000123, its owner assignment by ALLOC-MTG-BKK-01, its transfer under TRF-2026.11 and document DOC-2026-0009981 | AC1, AC5, AC8, AC9 |
| Allocation failure case | Case RW-2026-000124 with no owner and status "New" | AC4 |
| Duplicate event | Event EV-7f3a-0001 with its idempotency key, sent twice | AC5 |
| Negative records | No version group, rule ID R-UNI-14 with an empty version, decision code D99, and a call with no transaction | AC2, AC3, AC6, AC7 |
| Role fixture | A test identity without Decision log R | AC10 |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The ledger is `rwb_decision`, owned by P7 rwb-decision; the suite reads it only through the P7 contract |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | On RWB-PLT-E1027-APP and RWB-P7-E1027-APP; the suite exercises the delivered library |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the calling services; the suite reads the decision codes in force through the owner's contract |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the calling services; the suite reads the list values in force through the owner's contract |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On every producer and on P7; the suite consumes the shared topic |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | On RWB-P7-E1027-APP for JOB-14; the suite observes it |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The two consumed ledger reads of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P7-E1027-APP; the suite changes no schema |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data | AC9: the legacy lake copy of the decision log is retired and absent |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The ledger view for a screen goes through gateway-bff; the suite calls P7 directly |

The dependency-added column records the build dependency of the owning story. This story carries **no H dependency, no C dependency and no X dependency**: an integration story waits on no build of its own, and its two **I dependencies** are RWB-PLT-E1027-APP and RWB-P7-E1027-APP (Template and Rules v1 §R5.4, §R5.7).

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the P7 endpoint, the shared topic and the schema registry, with the contract preflight that fails on any drift.
2. Build LibraryCallerDriver against the real conformance caller and prove the four Epic 1 records of AC1 in a real transaction.
3. Build ValueReader so the decision codes, list values and rule versions come from the owner's contract; fail the run if a code is not in force rather than defaulting.
4. Build EventProbe for `rwb.decision.DecisionRecorded.v1`, with the envelope, key, count and no-personal-data assertions and the duplicate of AC5.
5. Build LedgerProbe for the two P7 reads, the 5-minute window and the entry fields of AC8, plus the 403 path of AC10.
6. Build FailureSwitch for AC4 and the negative records of AC2, AC3, AC6 and AC7, asserting the exact message and field name and the absence of a record and an event afterwards.
7. Add LakeAbsenceProbe for AC9 and the evidence that the writer writes no reporting copy.
8. Build ReportWriter, clean up the synthetic set, and run the whole suite twice to prove that a repeated run adds no record and no ledger entry.

**Done when.** The fourteen test cases of section 16 pass on the real library and the real ledger in SIT, the fourteen criteria of section 7 are signed off against the contracts and the events, no service table was read, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P4-002 | A user without Decision log R reads the decision log through the P7 ledger | Not specified in the source documents (DOR-RWB-ITG-E1027-ITG-9) |

The first three texts are copied unchanged from RWB-E1-027 and this story adds no message ID; MSG-P4-002, used by AC10, is listed in the table above with its text not specified in the source documents (DOR-RWB-ITG-E1027-ITG-9). The field names the suite asserts are "versions" for AC2, "ruleVersion" for AC3, "decisionCode" for AC7 and "approvalLevel" for AC12. Thai text for each message follows decision DL10 (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863).

### 15. Screens and states

No screen in this story. The **ledger** is read through the gateway-bff composite route (DP-19) by the roles holding Decision log R, and the suite asserts the same facts through the two P7 read operations rather than through a screen. **Failed writes appear as incidents** in the platform monitoring, and a ledger that lags shows as a gap alert, not as a screen error.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-027-01-ITG | AC1 | Integration | Synthetic case created and allocated by row ALLOC-MTG-BKK-01, transferred under TRF-2026.11, document DOC-2026-0009981 attached; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-02-ITG | AC2 | Integration | Transfer record with no version group; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-03-ITG | AC3 | Integration | Record with rule ID R-UNI-14 and no rule version; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-04-ITG | AC4 | Integration | Library write switched off during JOB-03 for case RW-2026-000124; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-05-ITG | AC5, AC8 | Integration | Document attached event EV-7f3a-0001 sent twice with the same idempotency key; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-06-ITG | AC6 | Integration | Writer called outside a transaction; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-07-ITG | AC7 | Integration | Record with decision code D99; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-08-ITG | AC10 | Integration | A role without Decision log R reads the decision log and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-09-ITG | AC4 | NFR | Decision-record write forced to fail for the calling action; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-10-ITG | AC9 | Integration | Record written and collected into the P7 central ledger; lake-absence probe asserts no data-lake copy of the decision log; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-11-ITG | AC11 | Integration | A change that adds a client for a service schema to the suite, run through the pipeline scan |
| TC-E1-027-12-ITG | AC12 | Integration | Record with an approver and no approval level; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-13-ITG | AC13 | Integration | The four Epic 1 records compared with the decision codes in force; end-to-end: real services on the wave 1 contracts |
| TC-E1-027-14-ITG | AC14 | Integration | Client configuration and observed calls of one run checked for one hop and the 2 s timeout; end-to-end: real services on the wave 1 contracts |

The first nine rows are the legacy test cases of RWB-E1-027 in their legacy order, each with its ITG copy. The Level column follows Template and Rules v1 §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration and the legacy Resilience level becomes NFR. AC9 has no legacy test case, because the legacy story treats the lake copy as out of scope; it is asserted by the suite's lake-absence probe and recorded in the evidence report and in section 18.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case, document and event identifier, and no production data is read, copied or connected to.
- No personal data in records, events, logs, workflow history, fixtures or the report: the actor reference, case numbers, document identifiers, decision codes, rule IDs and versions only.
- No business value in the test code: decision codes, list values, approval levels and rule versions are read as the values in force through the owner's contract (DP-06, DP-07).
- No cross-service table read: every fact is read through a contract or an event, the ledger stays behind the P7 contract, and the suite ships with no client for a service schema (DP-01).
- One writer only: the suite calls the real PLT library and never writes a ledger table, and no service builds a second writer (DP-03).
- One hop and a 2 s budget on every REST call, with no service called through another service (ADR-020).
- No production access and no production namespace: the run is pinned to SIT and refuses to start against any other environment.
- No data-lake copy is created, read or asserted as present: the legacy copy is retired and the run proves its absence (DP-17).
- Clean-up in the same run: the synthetic set, the started transactions and the failure switch are removed or reset, and the report records what was cleaned.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | The library write, `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, `GET /api/recovery/decision/v1/decision-log` | TC-E1-027-01-ITG, TC-E1-027-02-ITG, TC-E1-027-03-ITG, TC-E1-027-05-ITG, TC-E1-027-07-ITG |
| REQ-DRI-005 | No action proceeds if its record cannot be written | The mandatory-transaction rule and the refused and failed writes, MSG-P7-003 and MSG-P3-013 | TC-E1-027-04-ITG, TC-E1-027-06-ITG, TC-E1-027-09-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, CloudEvents 1.0, key caseId | TC-E1-027-01-ITG, TC-E1-027-05-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed P7 reads of section 12.2 and the preflight | TC-E1-027-04-ITG, TC-E1-027-08-ITG |
| ADR-022 | Local decision record plus central ledger | The library record in the caller's transaction and the `rwb_decision` ledger | TC-E1-027-01-ITG, TC-E1-027-05-ITG, TC-E1-027-09-ITG |
| DP-03 | Local decision-record library and the shared topic | The PLT conformance caller and `rwb.decision-record.v1` | TC-E1-027-01-ITG, TC-E1-027-05-ITG |
| DP-06 | Parameters contract of rwb-case | Decision codes read as the values in force | TC-E1-027-01-ITG, TC-E1-027-07-ITG |
| DP-07 | Reference-data contract of rwb-case | List values read as the values in force | TC-E1-027-01-ITG, TC-E1-027-07-ITG |
| DP-09 | Outbox and inbox library; CloudEvents | One `DecisionRecorded` per record and the dedupe of the repeated event | TC-E1-027-01-ITG, TC-E1-027-05-ITG |
| DP-17 | No data lake | The absence of the legacy decision-log copy RWB-E1-014 and of a reporting copy | The lake-absence probe of section 13, reported with TC-E1-027-01-ITG |
| RWB-E1-027 (legacy story) | Decision log writer v1: AC1 to AC7 | The library record contract and the ledger read | The nine ITG copies of section 16 |
| RWB-P7-E1027-APP (component copy) | The central ledger, the continuous ingest, the chain check and the two read operations; owns legacy AC1 to AC7 | `rwb_decision`, JOB-13, JOB-14, `GET /api/recovery/decision/v1/decision-log` and `.../{entryId}` | TC-E1-027-05-ITG, TC-E1-027-08-ITG |
| RWB-PLT-E1027-APP (component copy) | The writer library: record contract, validator, transaction rule, idempotency rule and publication; owns the writer build | The conformance caller and the library release assertions | TC-E1-027-01-ITG to TC-E1-027-07-ITG |

The legacy acceptance criteria **AC1 to AC7 stay with RWB-P7-E1027-APP**, and the writer library is built and signed off by **RWB-PLT-E1027-APP**; this story owns no legacy AC and adds the fourteen new criteria of section 7. The integration dependencies are RWB-PLT-E1027-APP and RWB-P7-E1027-APP.

### 19. Out of scope

- The two application builds this run depends on: RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The legacy acceptance criteria AC1 to AC7 at component level, which RWB-P7-E1027-APP owns.
- The contract, database, operations and infrastructure stories of the legacy key.
- Approval records with the limit applied (RWB-E2-013).
- Access events (RWB-E1-039).
- The legacy copy to the data lake (RWB-E1-014), which is retired and has no target path.
- The recommendation service with reasons for the route decision (Epic 4).
- The `ApprovalWorkflow` template and the P7 approval screens.
- The build of the harness RWB-ITG-W1J01-ITG itself.
- The non-functional epic RWB-ITG-NFR, including load, resilience and performance testing.
