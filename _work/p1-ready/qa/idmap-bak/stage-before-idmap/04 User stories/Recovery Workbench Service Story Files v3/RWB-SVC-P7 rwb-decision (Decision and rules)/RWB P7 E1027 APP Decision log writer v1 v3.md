# RWB-P7-E1027-APP Decision log writer v1

**Version 3 changes.**

- AC13 specifies the existing-snapshot behavior when the freshness read fails (RWB-P1-E1015-APP#23); its test case is pending (NEW-GAP-G7-3).

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: realigned from RWB-E1-027 for rwb-decision. The writer is reworked so that the append goes to this service's own store in `rwb_decision`, the record leaves on the shared topic `rwb.decision-record.v1`, and the central ledger, the chain check and the two reads stay in the other stories of this legacy key; the seven legacy criteria are kept word for word. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1027-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 13 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1027-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P7-B |
| Ready to start | After RWB-P7-E1008-APP and RWB-PLT-E1056-OPS; both are not yet done |
| Depends on (build) | RWB-P7-E1027-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P7-E1008-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON; published contract of the P4 authorise call: Not specified in the source documents (GAP-2404) |
| Size | Small: fits within two weeks; not further sized in the source documents (DOR-RWB-P7-E1027-APP-16); the squad sizes it at refinement |
| Contract version | v1 (the /v1 path of the reads; contract baseline RWB-P7-E1027-CON) |
| Integration dependencies | None |
| External dependencies | RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-002, FR-P7-007, FR-P7-008, FR-P7-009) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **calling service identity of rwb-case, rwb-document and rwb-decision, and as the rwb-decision service identity that owns the writer, the reference implementation of the shared library**, I want **one writer, deployed in rwb-decision, that validates a record against the seven field groups, refuses an incomplete one with the field named, appends it hash-chained in the caller's transaction, returns the first entry for a repeated idempotency key and publishes `DecisionRecorded` to the shared topic in the same transaction**, so that **every action carries a validated record or does not happen, and the record is written once, in one shape, by one piece of code**.

### 2. Business rationale

Without one writer, every module builds its own record and some actions go unrecorded. The legacy story gave every module one published interface inside the monolith's one process; in the target that interface has to survive four changes at once. The store is no longer one `decision_log_entry` table in the single `recovery` schema: each service writes its own record in its own schema and publishes `DecisionRecorded`, and rwb-decision collects the records into the central ledger (Architecture v5 slides 20 and 28; ADR-022). The transaction rule is unchanged and is the whole point: the record is written with the change, in the caller's transaction, so a failed write stops the action (R-UNI-39, REQ-DRI-005). The event is no longer EV-08 in an application outbox with no broker: it is a CloudEvents 1.0 message on the shared topic `rwb.decision-record.v1` through the outbox library (DP-03, DP-09). And the data-lake copy of the log is gone: reporting reads the events, not a lake partition (DP-17).

The division of the legacy key is fixed by this run and this story is one slice of it. **This story** is the writer: the record builders, the validator over the seven field groups, the mandatory transaction, the idempotency path, the append into `decision_log_entry` in `rwb_decision`, the chain link and the `DecisionRecorded` outbox write. The **store contract of this service** — the append-only rule, the chain columns, the unique keys and the chain verifier — is RWB-P7-E1008-APP. The **contract baseline** the writer and its fakes are built against is RWB-P7-E1027-CON. The **reads** `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}` are P7-owned and delivered by RWB-P7-E2005-APP. The **rule version labels** the writer stamps on a record come from the rule registry of RWB-P7-E1073-CON. What the writer takes from the platform is the local decision-record library of RWB-PLT-E1027-CON — the interfaces, the record shape and the envelope — and it implements them against this service's own store rather than inventing a second record type.

The seven legacy criteria are kept word for word because they are the behavioural specification of the writer and nothing in the target changes the behaviour they test: a record per decision, the version group enforced, a rule ID without a rule version refused, a failed write stopping the action, one entry for a repeated key, a call outside a transaction refused, and an unknown decision code refused. Where a criterion names a fact another owner now holds, one mock line states the answer of that owner and every legacy value — the case number, the owner identifier, the allocation row, the rule version, the event identifier, the document number, the message identifiers and the refusal field names — is carried unchanged. The end-to-end proof of those journeys across services is RWB-ITG-E1027-ITG.

The writer serves REQ-DRI-004 and REQ-DRI-005, carries control CTL-06, and gives the measure "decisions with a log entry, 100 percent" (NFR-034) its service-side evidence: the FSD P7 measure of decisions within the delegation of authority is measured against these entries.

### 3. Preconditions

- RWB-P7-E1008-APP is done: `decision_log_entry` exists in `rwb_decision` with the chain columns `chain_seq`, `prev_hash` and `entry_hash`, the append-only trigger, the unique key on `idempotency_key`, the unique key on `chain_seq` and the chain verifier behind JOB-14 at 02:00.
- RWB-P7-E1027-CON is published: the append interface, the seven field groups, the refusal and failure identifiers, the `Idempotency-Key` rule, the `DecisionRecorded` envelope on the shared topic and the fakes, so this story builds against a fixed contract on Day 1.
- RWB-PLT-E1027-CON is published: the local decision-record library interfaces, the record type, the entry reference and the `MANDATORY` transaction rule, which this story implements rather than redefines. Its artefact coordinates are taken from the platform library baseline and are Not specified in the source documents (GAP-1402); a record with no case is keyed on its entry identifier, the chain is one per service schema, and a failed write routes to the service's own alerting.
- RWB-PLT-TE006-CON is published: the outbox writer, the inbox and the CloudEvents envelope family, so the `DecisionRecorded` row is written in the caller's transaction and relayed by the outbox relay.
- RWB-PLT-E1071-CON is published: the workflow kit, the `rwb-recovery` namespace and the typed activity contract on task queue `rwb-decision`, so `RecordAndApply` is an activity and never workflow code.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence of `rwb_decision`, so the migration of section 11 runs in this service's own pipeline.
- RWB-PLT-N001-CON is published: the gateway-bff composite route, so a failed write surfaces as an incident and a read reaches the entries through the gateway and not through this story.
- The parameters and reference data are in force: `rwb.decision.code.CASE_CREATED=D6`, `rwb.decision.code.OWNER_ASSIGNED=D6`, `rwb.decision.code.CASE_TRANSFERRED=D6` and `rwb.decision.code.DOCUMENT_ATTACHED=D6` (the values are the legacy assumption, kept as parameters of rwb-case under DP-06), LOV-DECISION with the decision codes, and LOV-APPROVAL-LEVEL (DP-07; contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON as fakes from the first run). The decision codes are asserted as values in force; no P3 store is read and no data-lake copy of the log is asserted (DP-17).
- The rule version stamped on a record is the rule package version label in force, read from the rule registry (D-RCV-36; RWB-P7-E1073-CON); the writer never derives a label of its own.
- The message identifiers `MSG-P7-009` and `MSG-P7-003` are kept unchanged from the legacy build; no published message catalogue defines their entry format, so that entry is Not specified in the source documents (GAP-1236; ASM-2200).
- The full column set beyond the legacy field identifiers, the data-date column, the entry-hash canonical form and the exact payload schema beyond the fields of section 12.3 have no published specification and are used here as the working read of the assumption (GAP-1236; ASM-2200; GAP-1237; ASM-2201). The record schema, the DDL template and the envelope are the working read at major version 1, frozen when the consuming stories pass their contract tests; the ledger side is confirmed with P7 in the verification loop (GAP-1403).
- The build dependencies are the writer contract, the platform contracts and the store story; the two rwb-case contracts are C rows and never block the build (Template and Rules §R5.7). No production data is used in any example, test or fake.
- Open decision DL10 is still open and applies to this story; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 4. Flow

1. A calling module inside rwb-decision — the Epic 1 record builders for the four legacy events, the approval path of RWB-P7-E2013-APP and the decision centre — assembles a `DecisionRecord` with the case, the decision code, the rule ID and version, the inputs reference, the actor, the final call and an idempotency key, inside its own transaction.
2. The caller calls `DecisionLogWriter.write` as the last step before commit; the record is handed in process, one hop, and no REST call is made to reach the writer.
3. `DecisionLogWriterService` checks that a transaction is open and refuses the call with `IllegalTransactionStateException` if not, before any row is read or written.
4. `DecisionLogWriterService` reads the idempotency key; for a key already written it returns the first entry reference with `repeated` true and adds one to the repeat counter of R-UNI-40.
5. `DecisionLogRecordValidator` applies the seven field groups of BR2 to BR4: the decision code from LOV-DECISION, the inputs reference, the final call, the decided-at time and the actor; the case unless the decision code is an access event; at least one of rule version, model version and agent version; a rule ID with its rule version; and an approver with an approval level. A refusal names the field with `MSG-P7-009` and nothing is written.
6. `DecisionLogStore.append` of RWB-P7-E1008-APP appends the row with the next `chain_seq`, the previous `entry_hash` as `prev_hash` and the new `entry_hash`, in the caller's transaction, under the append-only rule.
7. The writer writes the `DecisionRecorded` row to the outbox of `rwb_decision` in the same transaction, on the shared topic `rwb.decision-record.v1`, keyed by caseId where the record has a case and by the entry id where it does not.
8. The caller commits; the action, the entry and the outbox row are stored together, and the outbox relay publishes the event.
9. On a refused record the writer raises `DecisionLogRecordInvalidException` with `MSG-P7-009` and the field name, the caller's transaction rolls back and the caller shows its own message or `MSG-P7-003`.
10. On a failed append the writer raises `DecisionLogUnavailableException` with `MSG-P7-003`; the caller's transaction rolls back, nothing moves, and an incident is raised to the platform administrator queue.
11. The writer never retries: the calling job, request or activity applies its own retry policy, and the `RecordAndApply` activity uses the kit policy of 1 s initial interval, back-off 2 and 10 attempts (DP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record misses the version group, the inputs reference, the final call or the case | Refused; the writer logs the error with the missing field; the caller's action rolls back | MSG-P7-009 | AC2 |
| X2 | A record carries a rule ID with no rule version | Refused as X1 | MSG-P7-009 | AC3 |
| X3 | The store cannot be written | The caller's action rolls back; an incident is raised | MSG-P7-003 | AC4 |
| X4 | The same event arrives twice with the same idempotency key | One entry; the repeat is counted | None | AC5 |
| X5 | The writer is called outside a transaction | Refused with IllegalTransactionStateException; nothing is written | None | AC6 |
| X6 | A record carries a decision code not in LOV-DECISION | Refused as X1 | MSG-P7-009 | AC7 |
| X7 | The record passes validation but the outbox row cannot be written | Refused as X3: the entry, the change and the event are one transaction, so none of them is stored | MSG-P7-003 | AC1, AC4 |
| X8 | A record carries an approver without an approval level | Refused with the field `approvalLevel` named | MSG-P7-009 | AC8, BR4, TC-E1-027-12 |
| X9 | A caller outside the right of the capability area calls the writer through an operation | Refused by the gateway and the service guard before the writer is reached | MSG-P4-002 | AC9, TC-E1-027-08 |

X7 to X9 are the paths the target adds: the outbox row is part of the same transaction, the approval level is a field group the legacy story states in BR4 and no legacy criterion exercises, and the access refusal is the guard every operation of the service carries.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P7-E1027-CON, the store of RWB-P7-E1008-APP, the platform library contracts and two rwb-case contracts read as fakes from the first run |
| Negotiable | The decision code per event, the approval levels and the repeat counter are parameters and reference data; the record shape, the transaction rule and the refusal behaviour are fixed |
| Valuable | Every decision of this service has a validated record or does not happen, and the same code is the reference the other services build their writer from |
| Estimable | One interface, one validator, one idempotency path, one append, one outbox write, one activity and one migration |
| Small | Fits in one week with its tests, as the app slice of the legacy key |
| Testable | Each criterion below is one automated test in section 16, run against the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Decision log writer v1

  Background:
    Given the environment is DEV with synthetic data
    Given allocation table version "ALLOC-2026.11" and transfer rule version "TRF-2026.11" are in force

  Scenario: AC1 Record per event (legacy RWB-E1-027 AC1)
    Given the rwb-case contract mock returns case "RW-2026-000123" created by JOB-02 and owner "U-7101" given by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03
    Given case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03
    When the two events are written
    Then two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED"
    Then the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference
    Then both entries pass the schema check and two DecisionRecorded events are in the outbox

  Scenario: AC2 Schema enforced (legacy RWB-E1-027 AC2)
    Given the rwb-case contract mock returns the transfer of case "RW-2026-000123" in the same transaction as the record write
    Given a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "versions"
    Then the writer logs the error with the case ID and the missing field
    Then the system rolls the transfer in the same transaction back

  Scenario: AC3 A rule ID with no rule version is refused (legacy RWB-E1-027 AC3)
    Given a record with rule ID "R-UNI-14" and an empty rule version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "ruleVersion"

  Scenario: AC4 A failed write stops the action (legacy RWB-E1-027 AC4)
    Given the rwb-case contract mock returns case "RW-2026-000124" with no owner and status "New"
    Given the decision log store is unavailable
    When JOB-03 gives case "RW-2026-000124" to owner "U-7102"
    Then the write raises DecisionLogUnavailableException
    Then the case owner stays empty and the case status stays "New"
    Then the system raises an incident to the platform administrator queue

  Scenario: AC5 A repeated event gives one entry (legacy RWB-E1-027 AC5)
    Given the rwb-document contract mock returns document "DOC-2026-0009981" attached to case "RW-2026-000123" with event identifier "EV-7f3a-0001"
    Given event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written
    When the same event with idempotency key "EV-7f3a-0001" arrives again
    Then one entry exists for the event
    Then the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40

  Scenario: AC6 A write outside a transaction is refused (legacy RWB-E1-027 AC6)
    Given a caller without an open transaction
    When it calls the writer
    Then the system refuses the call with IllegalTransactionStateException and nothing is written

  Scenario: AC7 An unknown decision code is refused (legacy RWB-E1-027 AC7)
    Given a record with decision code "D99"
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "decisionCode"

  Scenario: AC8 An approver without an approval level is refused (exception X8) (new, D-RCV-60)
    Given a record with approver "U-7101" and no approval level
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "approvalLevel"

  Scenario: AC9 A caller outside the right is refused (exception X9) (new, D-RCV-60)
    Given a caller without the right of the capability area
    When it calls the writer through an operation
    Then the gateway and the service guard refuse the call with message MSG-P4-002 before the writer is reached

  Scenario: AC10 Rules BR4 and BR8 to BR13 hold on each write (no legacy origin tag) (new, D-RCV-60)
    Given a record for case "RW-2026-000123" with an approver "U-7101" and an approval level from LOV-APPROVAL-LEVEL
    When it is written in the caller's transaction
    Then the approval level is stored on the same record as the approver
    Then the entry, the change and the outbox row are stored in one transaction
    Then the entry is chained in chain_seq order through prev_hash and entry_hash
    Then DecisionRecorded leaves on topic "rwb.decision-record.v1" in CloudEvents 1.0 binary mode, keyed by caseId and carrying no personal data
    Then the writer does not retry and does not open a transaction
    Then the record shape, the append and the envelope are those of RWB-P7-E1027-CON and RWB-PLT-E1027-CON, with no second record type or event
    Then no data-lake copy is written

  Scenario: AC11 Error answers 401, 403 and 404 of the provided operations (no legacy origin tag) (new, D-RCV-60)
    Given a caller without a credential
    When it calls a provided operation under the /v1 path
    Then the operation answers with status 401
    Given a caller with a credential but without the right of the capability area
    When it calls the writer through an operation
    Then the operation answers with status 403 and message MSG-P4-002
    Given a read request for an entry ID that does not exist under the /v1 path
    When it is sent
    Then the read answers with status 404

  Scenario: AC12 A retried or timed-out activity leaves at most one entry per event (no legacy origin tag) (new, D-RCV-60)
    Given an activity that calls the writer for case "RW-2026-000123" and the write fails
    When the activity is retried under its own retry policy
    Then the writer does not retry itself and a rolled-back attempt stores no entry
    Then the retried event with the same idempotency key leaves one entry
    Given an activity that calls the writer and runs past its timeout
    When the activity times out
    Then the transaction of that attempt is rolled back and nothing is stored for it

  Scenario: AC13 A freshness read failure preserves the stored decision inputs
    Given a decision and its inputs snapshot have already been written
    When the source-data freshness call returns 503 or exceeds the 2 s budget
    Then the screen shows the stored inputs snapshot unchanged and recomputes no value

```

These seven criteria are the legacy criteria of RWB-E1-027, copied line for line with the origin tag on each scenario. AC8 and AC9 are this story's own criteria for exceptions X8 and X9, AC10 is its own criterion for the rules BR4 and BR8 to BR13, and AC11 and AC12 are its own criteria for error answers and for retried or timed-out activities; they carry no legacy origin tag. One line is added to AC1, AC2, AC4 and AC5 where the criterion names a fact that another service now owns — the case and its owner, the transfer in the same transaction, the absent owner and status, the attached document — and that line states only the answer of the owner's contract mock; every legacy value is unchanged. In the target the case-created, owner-assigned and case-transferred records are written by rwb-case in `rwb_case` and the document-attached record by rwb-document, through the same library; this story proves the writer as deployed in rwb-decision, with the entries landing in `rwb_decision`, and the cross-service journeys are proven by RWB-ITG-E1027-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The decisions of this service write an entry for case created, owner assigned, case transferred and document attached, and for every other decision the service takes | REQ-DRI-004; FEAT-DRI-02; FEAT-DRI-08 |
| BR2 | Required on every record: decision code from LOV-DECISION, inputs reference, final call, decided at and the actor; the case unless the decision code is an access event | DF-DEC-002, DF-DEC-003, DF-DEC-008, DF-DEC-012, DF-DEC-016; LOV-DECISION |
| BR3 | The version group needs at least one of rule version, model version and agent version, except for access events; a rule ID needs its rule version | DF-DEC-004 to DF-DEC-007; NFR-034 |
| BR4 | An approver needs an approval level from LOV-APPROVAL-LEVEL on the same record | DF-DEC-010, DF-DEC-011; FEAT-DRI-04 |
| BR5 | The record is written in the caller's transaction; if it cannot be written, the action does not proceed | Principle 5; R-UNI-39; CTL-06; REQ-DRI-005 |
| BR6 | The same event with the same idempotency key gives one entry, and the repeat is counted | R-UNI-40; FSD P7 A2.2 AC-EXC-P7-002-03 |
| BR7 | Decision codes for the events are parameters, not code | Principle 1; parameters `rwb.decision.code.*` |
| BR8 | The entry, the change and the outbox row are one transaction: a failure of any of the three stores none of them | Architecture v5 slide 28; Temporal and Drools Design slide 14; DP-09 |
| BR9 | Each service chains its entries in `chain_seq` order through `prev_hash` and `entry_hash`; for the first record of a service, `prev_hash` holds Not specified in the source documents (GAP-2074); the central ledger chains its entries on ingest and is the chain of record, anchored daily to WORM storage, and the local chain serves replay; the chain is verified by the store story at 02:00; an entry the central ledger has not yet acknowledged is shown as not yet sealed by the audit search, which reads the ledger only; the ledger completeness target is five minutes, the ingest lag is a metric of RWB-PLT-OBS with the threshold as a parameter, and the gap alert owner is Not specified in the source documents (GAP-2465); this story writes the sealed entry and no alert; strict mode waits for the ledger acknowledgement of its own record | Architecture v5 slide 28; Temporal and Drools Design slide 16; RWB-P7-E1008-APP; GAP-2075; GAP-2465 |
| BR10 | `DecisionRecorded` leaves on the shared topic `rwb.decision-record.v1` in CloudEvents 1.0 binary mode, keyed by caseId where there is a case and by the entry id where there is not, and carries no personal data | Architecture v5 slides 20, 22, 42; DP-03; DP-09 |
| BR11 | The writer does not retry and does not open a transaction; the caller's job, request or activity retries | RWB-E1-027 section 17; DP-10; RWB-E1-027 section 5 X5 |
| BR12 | The record shape, the append and the envelope are those of RWB-P7-E1027-CON and RWB-PLT-E1027-CON; this story adds no second record type and no second event | DP-03; ADR-022 |
| BR13 | No data-lake copy is written: the legacy lake stream of the decision log is retired and reporting reads the events | DP-17; ADR-018; Template and Rules §R6 |

### 9. State transitions

None in the case. This story does not change a case status: it makes a status change made by another module depend on its entry, so that when the write fails the case stays in the status it had (for example "New" in AC4). The record itself has the states below.

| Object | State | Meaning in this story |
|---|---|---|
| Decision record | Unwritten | The caller has opened the transaction and not yet called the writer |
| Decision record | Validated | The seven field groups passed and the idempotency key is new |
| Decision record | Appended | The row exists with its `chain_seq`, `prev_hash` and `entry_hash`, visible inside the caller's transaction |
| Decision record | Committed | The caller committed; the action, the entry and the outbox row are stored together |
| Decision record | Refused | A field group failed; nothing is stored and the field is named |
| Decision record | Repeated | The key existed; the first entry reference is returned with `repeated` true and the repeat is counted |
| DecisionRecorded | Written to the outbox | The row is in `outbox_event` in the caller's transaction |
| DecisionRecorded | Published | The outbox relay published it on `rwb.decision-record.v1` |
| DecisionRecorded | Absent | The caller's transaction rolled back; no event exists |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-decision service identity | Calls the writer for its own decisions, appends to `decision_log_entry` in `rwb_decision` and writes the outbox row (DP-02) |
| The calling service identities of rwb-case, rwb-document and rwb-decision | Hand a record in their own transaction through the library; they never read or write `decision_log_entry` (DP-01) |
| SY-CASEWF, the case workflow system actor | The actor value the legacy criteria carry on the owner-assigned entry; the value is unchanged |
| RW-AUDIT, RW-COE and every role holding the Decision log right | Read the entries through the read operations of RWB-P7-E2005-APP, never through a table of this service |
| RW-PLATADM, platform administrator | Receives the incident when a write fails; operates the run through the Schedules of the store story |
| The rule registry owner (P7) | Publishes the rule package version label the writer stamps on a record (RWB-P7-E1073-CON) |
| The rwb-case owners of the parameters and the lists | Keep the decision code per event and the approval levels as data (RWB-P3-E1042-CON, RWB-P3-E1043-CON) |
| No delegation of authority level applies | A record write is a technical step, not a credit decision; the approval level on the record is copied from the decision that was taken |

No personal name, no e-mail address and no credential appears in this story, its examples or its fixtures. Where an actor must be named, the story uses a role code or a user identifier only.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |
| DF-REF-028 | lov_value, through the rwb-case contract | lov_code | Read |
| DF-REF-029 | lov_value, through the rwb-case contract | value_code | Read |
| Standard column | decision_log_entry | chain_seq, prev_hash, entry_hash | Write, through the store of RWB-P7-E1008-APP |
| Standard column | decision_log_entry | decided_at, created_at | Write |
| Standard column | outbox_event | event payload, key, headers | Write, through the outbox library |
| Placeholder | decision_log_entry | data date carried on the record | Write; the column name and the exact form are Not specified in the source documents (GAP-1236; ASM-2200) |

Field IDs are those in the Logical Data Model and Data Dictionary. The migration is one per-service Flyway step in the `rwb_decision` sequence (DP-15, RWB-PLT-E1044-CON): `V_E1027__declog_idempotency.sql` adds `idempotency_key varchar(80)` with a unique index on the field `idempotency_key` (DF-DEC-031; the index carries no separate name) where the store story has not already created it, and it creates no table. The chain columns, the append-only trigger and the unique key on `chain_seq` belong to RWB-P7-E1008-APP and are not created twice.

Personal data is a column of `decision_log_entry` only as the user identifier in `actor_user_id` (DF-DEC-030), the P2 field that Data Classification v5 classes as personal data; the actor is otherwise a role code, the subject is a case, document or entry identifier, and the inputs reference is a pointer to a snapshot the caller holds. The indexes this story relies on are the unique key on `idempotency_key` for the repeat path and the primary key on the entry id for the reference it returns; the chain index belongs to the store story.

### 12. Contract

#### 12.1 REST operations provided

None. The base of this service is `/api/recovery/decision/v1` (DP-13), and the only operations the Ownership Map gives P7 under that base are reads: `GET /decision-log` and `GET /decision-log/{entryId}`, owned by P7 and delivered by **RWB-P7-E2005-APP**; they are named here and not declared as provided, because a read of the ledger is not the write surface of this story.

The surface this story provides is three local elements, in process, one hop and with no REST call:

| Element | Kind | Shape | Note |
|---|---|---|---|
| `DecisionLogWriter.write` | Published interface, implementing `DecisionRecordWriter` of RWB-PLT-E1027-CON, annotated `MANDATORY` | `DecisionRecord` in, `DecisionRecordEntryRef` out | The only path to `decision_log_entry`; refuses outside a transaction |
| `DecisionLogStore.append` | Service-local append, provided to this writer by RWB-P7-E1008-APP | Validated record plus chain link in, entry reference out | Appends only; no update and no delete |
| `RecordAndApply` | Temporal activity on task queue `rwb-decision` | Typed activity contract in the service's activity jar | Wraps the write in one activity so a replay reuses the recorded result |

A write path on REST — for example `POST /api/recovery/decision/v1/decision-log` — is not in the Ownership Map. This story therefore declares no such operation and records the missing owned operation as Not specified in the source documents (GAP-1235; ASM-2199).

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story | Contract |
|---|---|---|---|
| GET `/api/recovery/case/v1/admin/parameters/{code}` | P3 rwb-case | The decision code per event: `rwb.decision.code.CASE_CREATED`, `.OWNER_ASSIGNED`, `.CASE_TRANSFERRED`, `.DOCUMENT_ATTACHED` | RWB-P3-E1042-CON (C) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION for the decision-code check and LOV-APPROVAL-LEVEL for the approval-level check | RWB-P3-E1043-CON (C) |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its status and its owner, used by the AC1 and AC4 mocks; read as a contract fake only | The P3 case contract, consumed as a fake and not a dependency row of this story |
| GET `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The attached document and its event identifier, used by the AC5 mock; read as a contract fake only | The P5 document contract, consumed as a fake and not a dependency row of this story |
| The local decision-record library `DecisionRecordWriter` | Platform library | The append interface and the record type this story implements | RWB-PLT-E1027-CON (H) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A missing parameter or list answer is never treated as a value: the writer refuses with `MSG-P7-009` and names the field, because no default decision code may be invented (BR7). The field names behind the two rwb-case operations are Not specified in the source documents beyond the list codes and the parameter keys of the legacy story (GAP-1236; ASM-2200).

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` (shared topic of DP-03) | `caseId` where the record has a case; the entry id where it does not | entry id, case ID where there is one, decision code, final call, rule ID, rule version, chain sequence, entry hash and the actor reference | Announces every record to the central ledger and to the reporting read model; written to the outbox of `rwb_decision` in the same transaction as the entry |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | `rwb.decision.DecisionRecorded.v1` |
| ce_source | `/rwb-decision` |
| ce_subject | The case ID where there is one, the entry id where there is not |
| ce_id and traceparent | The event identifier and the W3C trace context of the caller |
| Retry | Retry topics at 1 min, 10 min and 1 h, then `.dlt` with an alert (DP-09, RWB-PLT-TE006-CON) |
| Payload | Identifiers, codes and dates only; no personal data and no free text beyond the legacy fields |

This story publishes nothing on the service's own topic `rwb.decision.events.v1`: `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` are the events of RWB-P7-E2013-APP and RWB-P7-E1073-CON. The type of the shared event is `rwb.decision.DecisionRecorded.v1` as fixed by the Kafka Topic and Event Catalog v1 (EV-08); the platform library contract of RWB-PLT-E1027-CON writes the same type (GAP-1238). The key rule for a record with no case and the exact payload schema beyond the fields listed above are Not specified in the source documents (GAP-1236; ASM-2200).

#### 12.4 Events consumed

None. The writer is called in process inside the caller's transaction and subscribes to nothing: the facts it needs arrive in the record and, where a value is data, through the two rwb-case operations of 12.2. The consumption of `DecisionRecorded` into the central ledger is the ingest of RWB-P7-E1008-APP, and the reporting projection is rwb-reporting's; neither is a subscription of this story.

#### 12.5 Workflows and activities

One activity and no workflow.

| Element | Queue | Input | Output | Note |
|---|---|---|---|---|
| `RecordAndApply` | `rwb-decision` in namespace `rwb-recovery` | The validated record, the decision code and the business date | The entry reference, the chain sequence and the entry hash | Writes the entry, the change and the outbox row in one transaction (Temporal and Drools Design slides 13 and 14); retry policy 1 s initial interval, back-off 2, 10 attempts; a refusal with `MSG-P7-009` is non-retryable |

The writer is never called from workflow code: rules and I/O live in activities, so a replay reuses the recorded answer (DP-10, Temporal and Drools Design slide 27). `ApprovalWorkflow` is the workflow kit template of the approval story RWB-P7-E2013-APP and is not declared here.

#### 12.6 Schedules

None. The legacy `JOB-13` decision log copy at 01:00 has no target: the data lake is removed and the ingest of the records is continuous from the topic (DP-17, DP-10; Architecture v5 slide 44 keeps JOB-13 as "ingest is continuous (Kafka)"). The nightly chain check `JOB-14` at 02:00 is the Schedule of the store story RWB-P7-E1008-APP. The ACE shared Quartz tables and every JOB element are retired for this service (Template and Rules §R6, DP-10), so this story declares no cron entry, no job name and no shared scheduler row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| decision_log_entry | P7, in `rwb_decision` | The entry of every decision: the legacy field identifiers DF-DEC-001 to DF-DEC-018, DF-DEC-030 and DF-DEC-031, the chain columns, the final call and the decided-at time. Appended only; the table name and DDL are settled in the DB story of each service (GAP-2068) |
| outbox_event | PLT library, created in `rwb_decision` | The `DecisionRecorded` row, written in the caller's transaction and relayed to `rwb.decision-record.v1` |
| processed_event | PLT library, created in `rwb_decision` | The inbox of this service; not used by the writer, created with the schema |
| idempotency_key | PLT library, created in `rwb_decision` | The stored `Idempotency-Key` answer, where an operation of this service carries one |

`delegation_limit` is P4 rwb-access's, `parameter_catalog` and `parameter_value` are P3 rwb-case's, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case's, `approval` is P7's but belongs to RWB-P7-E2013-APP, and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's but belong to RWB-P7-E1073-CON and its app story. None of them is declared as owned here and none is read directly (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | Case "RW-2026-000123" with owner "U-7101" and status "In progress", allocated by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11"; case "RW-2026-000124" with no owner and status "New"; a transfer that is refused when the record write fails; a delayed answer beyond 2 s | App story, contract tests, harness |
| rwb-case parameters fake | `rwb.decision.code.CASE_CREATED` = D6, `rwb.decision.code.OWNER_ASSIGNED` = D6, `rwb.decision.code.CASE_TRANSFERRED` = D6, `rwb.decision.code.DOCUMENT_ATTACHED` = D6, with their version labels; an absent key; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case reference-data fake | LOV-DECISION with D6 and the access event codes, and without D99; LOV-APPROVAL-LEVEL with L6; a delayed answer beyond 2 s | App story, contract tests |
| rwb-document fake | Document "DOC-2026-0009981" attached to case "RW-2026-000123" with event identifier "EV-7f3a-0001"; a delayed answer beyond 2 s | App story, contract tests |
| Rule-registry fake | Rule "R-UNI-14" with version "UNI-2026.11", and the same rule with no version in force | App story, contract tests |
| Store fake | An append that answers chain sequence and entry hash; an append refused because the store is unavailable, raising `DecisionLogUnavailableException` with MSG-P7-003 | App story, contract tests |
| Outbox fake | The `DecisionRecorded` row recorded in the caller's transaction, and absent after a rollback | App story, contract tests |

The values are the legacy values of RWB-E1-027 section 7, kept unchanged so that the component, contract and integration assertions read the same fixtures; the fixtures carry no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed as contract dependencies, 2 consumed as fakes | The append is in process; the two rwb-case operations of RWB-P3-E1042-CON and RWB-P3-E1043-CON are consumed; the case and document reads are fakes only; one hop, 2 s |
| Kafka | 1 published by this story | `DecisionRecorded` on `rwb.decision-record.v1`; nothing on `rwb.decision.events.v1` from this story |
| Temporal | 1 activity, 0 workflows | `RecordAndApply` on queue `rwb-decision`; the writer is called inside the caller's activity |
| File | None | No file element in this story; the daily ledger seal in write-once storage is the store story's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, packages `decision.writer`, `decision.record` and `decision.activity`; the artefact is the `rwb-decision` api and worker deployment of the service template. The writer implements the library interfaces of RWB-PLT-E1027-CON and is published as the service's own contract through RWB-P7-E1027-CON.

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

No pattern is claimed for DP-02, DP-04, DP-05, DP-08, DP-12, DP-14, DP-16, DP-18 or DP-20: this story adds no login of its own (the DB story creates it), evaluates no Drools package, reads no ACE view, declares no authorise call of its own (the guard is the gateway's and the service's), runs no per-case parent workflow, renames no topic beyond the shared one it uses, calls no rwb-integration adapter, writes no interaction ledger entry and calls no agent.

**Hardware and software change.** The writer moves from the monolith's one published interface over one table in the shared `recovery` schema to a service-local writer over `rwb_decision.decision_log_entry`, built from the platform library, called in the caller's transaction and publishing on a shared Kafka topic. No new hardware is implied: the table lives in the ACE PostgreSQL server under the `rwb_decision` schema and login, and the event uses the Kafka platform ACE already runs.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLogWriter` | Published interface | The one write method, its `MANDATORY` rule and its two exceptions (BR5, BR8, BR11) |
| `DecisionLogWriterService` | Service | Transaction check, idempotency check, validation, append, outbox write (BR2 to BR8) |
| `DecisionLogRecordValidator` | Service | The seven field groups with the decision codes from LOV-DECISION and the approvals from LOV-APPROVAL-LEVEL (BR2 to BR4) |
| `Epic1DecisionRecords` | Service | The builders for the four legacy events, with the decision code read from the parameter catalogue of rwb-case (BR1, BR7) |
| `DecisionRecordedPublisher` | Service | Writes `DecisionRecorded` to the outbox in the caller's transaction (BR10) |
| `DecisionLogEntryRepository` | Repository | The idempotency lookup and the append through `DecisionLogStore` of RWB-P7-E1008-APP |
| `RecordAndApplyActivity` | Activity | The activity wrapper on queue `rwb-decision` with the kit retry policy (BR11, DP-10) |

**Build steps**

1. Run the migration of section 11 in the `rwb_decision` sequence and assert that the unique key on `idempotency_key` exists once.
2. Build `DecisionLogRecordValidator` with the tests of AC2, AC3 and AC7 and one test for the missing approval level.
3. Build `DecisionLogWriterService` with the mandatory transaction, the idempotency path and the append; test AC5 and AC6.
4. Add the `DecisionRecorded` outbox write and test that a rollback leaves no event (X7).
5. Build the four Epic 1 record builders with the decision codes from the parameter fake; test AC1.
6. Wire the writer into the approval path of RWB-P7-E2013-APP and into the decision centre through the interface; a caller outside the package is refused by the architecture test.
7. Build `RecordAndApply` on queue `rwb-decision` with the typed activity contract and the retry policy; test that a refusal is non-retryable and that a store failure is retried.
8. Test AC4 with the store switched off: the caller's change rolls back and the incident is raised.
9. Add the chain assertions: a second entry carries the first entry's `entry_hash` as `prev_hash` and its own `entry_hash` matches the canonical form.

**Done when.** The tests of section 16 pass against the contract fakes, the append-only and boundary tests are green, an architecture test fails the build if any class outside `decision.writer` writes to `decision_log_entry`, and no data-lake sink, Quartz row or second record type exists in the build.

### 14. Validation and messages

| ID | When | Message | Raised as |
|---|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException`, with `field` |
| MSG-P7-003 | The store, the entry or the outbox cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException` |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary of the caller) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. | Named only; the caller owns the display |
| MSG-P4-002 | The role lacks the right of the capability area | You cannot {action} here. Your role does not include it. | The service guard, before the writer is reached |

The three texts are copied unchanged from RWB-E1-027 section 14 and this story adds no message ID. The field names are `versions`, `ruleVersion` and `decisionCode` for the three refusals of the legacy criteria, and `approvalLevel` for the group of BR4 that no legacy criterion exercises. The published catalogue entry format of MSG-P7-009 and MSG-P7-003 is Not specified in the source documents (GAP-1236; ASM-2200). Thai text follows decision DL10.

### 15. Screens and states

No screen in this story. Entries are read through the two read operations of RWB-P7-E2005-APP under `/api/recovery/decision/v1`, reached through the gateway-bff composite route (DP-19, RWB-PLT-N001-CON); a failed write appears as an incident in the job and service monitoring of RWB-PLT-E1056-OPS, not as a screen error.

| Screen | What it shows from this story | State |
|---|---|---|
| SCR-DEC-LOG, the decision log of a case | The entries this writer appended, with the rule ID, the rule version, the approver and the hash | Committed |
| SCR-DEC-ENTRY, one entry | The chain sequence and the entry hash, for an audit read | Committed, refused, repeated |
| The incident queue of the platform administrator | The refusal or the failure with the message identifier and the field, never a customer value | Refused, failed |

The composite route, its field list, its masking and its timeout budget belong to RWB-PLT-N001-CON and are not fixed here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-027-01 | AC1, BR1, BR7 | End to end | Synthetic case created and allocated by row ALLOC-MTG-BKK-01 |
| TC-E1-027-02 | AC2, BR3 | End to end | Transfer record with no version |
| TC-E1-027-03 | AC3, BR3 | End to end | Record with rule ID R-UNI-14 and no rule version |
| TC-E1-027-04 | AC4, BR5 | End to end | Store switched off during JOB-03 |
| TC-E1-027-05 | AC5, BR6 | End to end | Document attached event sent twice |
| TC-E1-027-06 | AC6, BR5 | End to end | Writer called outside a transaction |
| TC-E1-027-07 | AC7, BR2 | End to end | Record with decision code D99 |
| TC-E1-027-08 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E1-027-09 | Principle 5 | NFR | The decision log write forced to fail; the calling action rolls back |
| TC-E1-027-10 | §12, BR10, BR12 | Component | The operations, events and activities of section 12 against the contract fakes of 12.8 |
| TC-E1-027-11 | §12.7 | Component | Each table of 12.7 checked against its owner's declared use |
| TC-E1-027-12 | AC8, BR4 | End to end | Record with an approver and no approval level |
| TC-E1-027-13 | AC9, Access | Component | A caller without the right calls the writer through an operation |
| TC-E1-027-14 | BR8 | Component | Entry, change or outbox row fails; none of the three is stored |
| TC-E1-027-15 | BR9 | Component | Chain of records checked by the store story's verification |
| TC-E1-027-16 | BR11 | Component | Writer call fails; the writer neither retries nor opens a transaction |
| TC-E1-027-17 | BR13 | Component | Reporting reads the events; no data-lake copy is written |
| TC-E1-027-18 | AC10, BR4, BR8, BR9, BR10, BR11, BR12, BR13 | Component | Record with approver and approval level written in a transaction; entry, change, outbox row and event checked |
| TC-E1-027-19 | AC11 | Component | Caller without a credential, caller without the right, and a read of an entry ID that does not exist |
| TC-E1-027-20 | AC12, BR5, BR6, BR11 | Component | Writer call fails and the activity is retried; the activity runs past its timeout |

AC13 has no test case in Test Cases v9. Pending: the test case of AC13, owner QA lead, tracked as NEW-GAP-G7-3.

The nine cases are the legacy cases of this key, kept in the legacy order with their covers and data unchanged; legacy level System maps to End to end, Access to Component and Resilience to NFR. TC-E1-027-10 to TC-E1-027-20 are added by this story for the section 12 contract, the 12.7 tables, the criteria AC8 to AC12, and the rules BR8 to BR13 that no legacy case covers. They run against the contract fakes of 12.8 and the store of RWB-P7-E1008-APP, and the cross-service journeys are repeated by RWB-ITG-E1027-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code per event is a parameter, the decision codes and approval levels are list values, and the rule version is the label in force.
- No personal data in logs, tests, prompts or events: a refused record is logged with its case ID and field name only, and the actor is a role code or a user identifier.
- No read of another service's tables: callers hand the values in the record, the lists and parameters arrive through the rwb-case contract, and the boundary test fails a cross-schema reference.
- No write path to `decision_log_entry` other than this writer, checked by an architecture test; no update and no delete exist at all, and the append-only rule is the store story's.
- No retry inside the writer: the caller's job, request or activity retries, with the kit policy of 1 s, back-off 2 and 10 attempts.
- The event is written to the outbox in the same transaction as the entry; a build that writes the event after the commit fails the transaction test.
- No data-lake sink and no reporting copy: the legacy lake stream is retired, and reporting follows the events (DP-17).
- One record type and one event: a second record shape or a second `DecisionRecorded` type fails the contract drift test of RWB-P7-E1027-CON.
- Every example and fixture is synthetic; no production payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-02, FEAT-DRI-03, FEAT-DRI-08 | 17 Run the decision center | BR1, BR2, BR3, BR4, BR6, BR7, BR8, BR10 | TC-E1-027-01, TC-E1-027-02, TC-E1-027-03, TC-E1-027-05, TC-E1-027-07 |
| REQ-DRI-005 | No action proceeds if its entry cannot be written | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-04, FEAT-DRI-05 | 17 Run the decision center | BR5, BR8, BR9, BR11 | TC-E1-027-04, TC-E1-027-06, TC-E1-027-09 |

| Element | Where it is fixed | Test cases |
|---|---|---|
| DP-01, DP-13 | The owned and not-owned lists of 12.7 and the base of 12.1 | TC-E1-027-01, TC-E1-027-08 |
| DP-03, DP-09 | The `DecisionRecorded` row of 12.3, BR8 and BR10 | TC-E1-027-01, TC-E1-027-05 |
| DP-06, DP-07 | The two admin rows of 12.2, BR2, BR4 and BR7 | TC-E1-027-01, TC-E1-027-07 |
| DP-10 | 12.5 and 12.6, BR11 | TC-E1-027-04, TC-E1-027-06 |
| DP-15, DP-17 | The migration of section 11 and BR13 | TC-E1-027-01 |
| ADR-014, ADR-020, ADR-022 | The schema and login, the one-hop budget and the local-record model | TC-E1-027-01, TC-E1-027-04, TC-E1-027-08 |
| Section 12 | The contract of 12 and the tables of 12.7 | TC-E1-027-10, TC-E1-027-11 |
| AC8, AC9, X8, X9, BR4, BR8, BR9, BR11, BR13 | The added criteria and the exception paths they cover | TC-E1-027-12, TC-E1-027-13, TC-E1-027-14, TC-E1-027-15, TC-E1-027-16, TC-E1-027-17 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1027-CON | Contract | H: the baseline this story implements and its fakes |
| RWB-P7-E1008-APP | App development | H: the store, the append, the chain and the append-only rule |
| RWB-PLT-E1027-CON | Contract | H: the library interfaces, the record type and the transaction rule |
| RWB-PLT-TE006-CON | Contract | H: the outbox writer and the envelope family |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data clients |
| RWB-PLT-E1071-CON | Contract | H: the activity contract and the kit retry policy |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence |
| RWB-PLT-N001-CON | Contract | H: the gateway route the read and the incident view use |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the parameters and lists, read as fakes and never blocking the build |
| RWB-P7-E2005-APP | App development | The two read operations under the base; not this story's |
| RWB-P7-E2013-APP | App development | The approval path that calls this writer for its own decisions |
| RWB-P7-E1073-CON | Contract | The rule package version label stamped on a record |
| RWB-ITG-E1027-ITG | Integration | The end-to-end proof of the seven journeys across services |
| RWB-PLT-E1056-OPS | DevOps | X: the monitoring and the incident route of a failed write |

### 19. Out of scope

- The store, the append-only rule, the chain columns, the chain verifier and the `JOB-14` chain check at 02:00 (RWB-P7-E1008-APP).
- The contract baseline, its fakes and its drift test (RWB-P7-E1027-CON).
- The two reads under `/api/recovery/decision/v1` and the screens that show the entries (RWB-P7-E2005-APP).
- Approval records with the limit applied and the `ApprovalWorkflow` of the kit (RWB-P7-E2013-APP).
- The rule registry, the rule package versions and their promotion (RWB-P7-E1073-CON and its app story).
- Access events and their records (P4 rwb-access, RWB-E1-039).
- The data-lake copy of the decision log and its retention (RWB-E1-014, retired, DP-17).
- The central ledger ingest, the completeness alert and the daily seal in write-once storage (RWB-P7-E1008-APP; Architecture v5 slide 28).
- The recommendation service with the reasons for the route decision (Epic 4, API-P7-001).
- The monitoring, dashboards and runbook of the service (RWB-PLT-E1056-OPS).
- The gateway-bff composite route, its masking and its timeout budget (RWB-PLT-N001-CON).
