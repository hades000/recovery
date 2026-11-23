# RWB-P1-E1066-APP Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1066-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P1-P |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1066-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1066-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The in-process `InteractionLedgerWriter.append()` of the monolith becomes a REST operation of this service, `POST /api/recovery/source-data/v1/interactions` on base `/api/recovery/source-data/v1` (DP-11, DP-13), and the `interaction` table becomes P1's own table in schema `rwb_source_data` (DP-01, DP-18; ownership ruling of R-PREC, the Ledger owned by rwb-source-data); the per-service Flyway sequence carries the column migration and the append-only trigger (DP-15), the case check of the monolith becomes a call to the rwb-case case contract and the decision-log reference a read of the rwb-decision contract (DP-11), and the Workbench events written from the outbox stay with RWB-P1-E1067-APP, the read interface with RWB-P1-E1068-APP and the case timeline with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the append of one ledger entry on a case to be a REST operation of rwb-source-data that refuses a missing value, orders two appends that arrive at the same moment without a gap or a repeat, and answers 404 for a case that does not exist**, so that **the history of a case is written once, in order, and is never assembled after the fact**.

This is the application slice of legacy RWB-E1-066. It owns exactly three legacy criteria:

- **AC5** — a required value is missing: the append is refused, nothing is written and the missing field is named;
- **AC6** — two entries for one case at the same moment: both are written with consecutive `case_seq`, and no `case_seq` is missing or repeated;
- **AC7** — a case that does not exist: the append is refused with 404 and nothing is written.

It also delivers the writer behind them: the REST append operation on `/api/recovery/source-data/v1`, the local `interaction` table in `rwb_source_data` with its `case_seq` allocator, its two unique keys and its append-only trigger, the read of one entry that lets the writer answer 201 with what it stored, and the two contract hops the append takes (the case check and the decision-log reference).

It does **not** claim legacy AC1, AC2, AC3, AC4 or AC8. AC1 (the ledger exists and is written to), AC2 (it is ordered and complete), AC3 (it is distinct from the decision log), AC4 (a write failure is visible) and AC8 (an entry cannot be changed) are owned by the rwb-case and rwb-integration slices of this legacy key — the recording screens and event paths that call this writer and the outbox intake that rebuilds an entry from an event — and by the cross-service proof of RWB-ITG-E1066-ITG. This story builds the writer those slices call and tests only the three paths above.

### 2. Business rationale

Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

In the target the writer is a service of its own, so three things that were one method call in the monolith become three separate facts. The ledger is P1's table in `rwb_source_data` and no other service reads or writes it (DP-01, DP-18; Architecture v5 slides 29 and 41; R-PREC default ruling). The append is a REST contract with one hop and a 2 s timeout, called by the screens through gateway-bff and by the event paths of rwb-integration (DP-11, DP-13, DP-19; Architecture v5 slide 11). The scope of the case is no longer a local join: it is answered by rwb-case over the case contract, and a case outside the caller's scope and a case that does not exist are the same 404 to this writer, because the case service does not disclose which of the two it is (MSG-P4-003).

The ordering rule is the part that has to survive the move. In one transaction the monolith took an advisory lock on the case ID and read the highest `case_seq`; over REST two appends for the same case may arrive on two pods at once, so the allocation stays inside one database transaction on this service's own table, and the unique key `(case_id, case_seq)` is what makes a gap or a repeat impossible rather than unlikely. That is the whole of AC6, and it is why the ledger cannot be split across two schemas.

### 3. Preconditions

- RWB-P1-E1001-APP is done: schema `rwb_source_data` exists with the base `interaction` table, its standard record columns and the dictionary rows of P1 (legacy RWB-E1-001 in the target).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- RWB-P1-E1066-CON is published: the OpenAPI 3.1 document of the interaction-ledger resource, the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, the error envelope, the Idempotency-Key rule and the contract fakes. This story builds against that contract and never against a second draft of it.
- RWB-P3-E1018-CON is published with its fake, so the case check of the append runs from Day 1 against `GET /api/recovery/case/v1/cases/{caseId}` and a 404 is answerable without rwb-case being built (DP-11).
- RWB-P7-E1027-CON is published with its fake, so a `DECISION_TAKEN` entry is written against `GET /api/recovery/decision/v1/decision-log/{entryId}` and a missing decision entry is answerable from Day 1 (DP-03, DP-11).
- RWB-PLT-E1027-CON (the local decision-record library) is on the classpath, RWB-PLT-E1043-CON is the client library of the reference data, RWB-PLT-TE006-CON is the outbox, inbox and idempotency library, and RWB-PLT-N001-CON is the gateway-bff composite route the recording screens arrive through (DP-03, DP-07, DP-09, DP-19).
- RWB-P3-E1043-CON is published with its fake, and the list **LOV-LEDGER-EVENT** is served as data through it: CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN, CORRECTION, loaded by the reference data administrator (DP-07; legacy RWB-E1-066 §13).
- The caller holds Case record C on the case: a person through the recording screens and gateway-bff, or a service identity of rwb-case or rwb-integration (SY-CASEWF, SY-DATALOAD) with a workload identity token.
- The roles `rwb_source_data` and the login of this service exist in DEV and SIT, and the credential is held by the platform and never appears in code, a test or a runbook (DP-02; Architecture v5 slides 11 and 29).
- The append operation path, its authorisation header handling and the 404 semantics are a target choice and not a legacy value, because the legacy writer was an in-process Java interface with no path and no status code; the scope check is now a cross-service call and not a local join (GAP-0504; ASM-0696).

### 4. Flow

1. A recording screen or an event path of rwb-integration calls `POST /api/recovery/source-data/v1/interactions` with an `InteractionRequest` and an `Idempotency-Key`, and the caller's token from gateway-bff (DP-11, DP-13, DP-19).
2. `InteractionWriteController` reads the body against the published `InteractionRequest` schema and refuses a body that does not validate (12.1).
3. `CaseScopeClient` calls `GET /api/recovery/case/v1/cases/{caseId}` once, one hop, 2 s timeout, to confirm the case exists and that the caller holds Case record C and the case scope; a 404 from rwb-case and a case outside the scope are the same 404 to the caller (DP-11; MSG-P4-003).
4. `ReferenceDataClient` reads **LOV-LEDGER-EVENT** through the rwb-case reference-data contract, so an event code is data and never a constant in the code (DP-07).
5. For a `DECISION_TAKEN` entry, `DecisionLogClient` calls `GET /api/recovery/decision/v1/decision-log/{entryId}` once to confirm the reference, and stores the identifier only: rule, version and inputs stay in rwb-decision (DP-03, DP-11).
6. `LedgerWriteService` validates the command: the case, the event code against the list, the occurred time, the actor and the source, plus the idempotency key; a missing value is refused with MSG-GEN-001 and the field name, and nothing is written (AC5).
7. `LedgerWriteService` opens one transaction, takes a transaction-level advisory lock on the case ID, reads the highest `case_seq` of the case and allocates the next one; the unique key `(case_id, case_seq)` decides the race, and a clash is retried once (AC6).
8. `InteractionRepository` inserts the entry with the event code, the actor type and reference, the source system and source reference, the channel and direction where they apply, the decision-log entry ID for a decision and the entry it corrects for a correction; no update and no delete method exists on the repository (AC6, 12.7).
9. The transaction commits, the local decision-record library records the ledger event in this service's own record, and the response is 201 with the stored `Interaction`, read back through `GET /interactions/{entryId}` inside the same call so that what is returned is what was stored (DP-03).
10. A repeat of the same `Idempotency-Key` with the same body returns the stored entry and the same `caseSeq` with no second insert; the stored response of the idempotency library is the authority, not a second read of the ledger (DP-09).
11. A database failure rolls the transaction back, the caller receives 503 with MSG-P1-022, and the writer raises the incident `LEDGER_WRITE_FAILED` with the case ID and the error class and no personal data (legacy X1, owned by the rwb-case and rwb-integration slices and by RWB-ITG-E1066-ITG).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ledger cannot be written | Action and entry roll back; 503 to the caller; incident raised; nothing discarded silently | MSG-P1-022 | AC4 (the rwb-case and rwb-integration slices of this key and RWB-ITG-E1066-ITG; this story ships the rollback and the incident hook) |
| X2 | A required value is missing (event code, occurred time, actor) | 422; nothing written | MSG-GEN-001 | AC5 |
| X3 | Two entries for one case at the same moment | Both written with consecutive case_seq; no gap and no repeat | None | AC6 |
| X4 | The case does not exist or is out of scope | 404; nothing written | MSG-P4-003 | AC7 |
| X5 | Any change or delete of an entry | Refused by the append-only trigger; a correction is a new entry naming the original | None | AC8 (the trigger is applied by this key's migration and tested in RWB-P1-E1066-OPS; the behaviour is RWB-ITG-E1066-ITG) |
| X6 | The rwb-case case contract does not answer inside 2 s, or answers 503 | The append is refused with 503 and MSG-P1-022; no entry is written and no scope answer is guessed from a cache | MSG-P1-022 | Section 12.2 |

X2, X3 and X4 are the legacy exception paths of RWB-E1-066 that this slice owns, carried unchanged; X1 and X5 are kept because the writer ships the rollback and the migration ships the trigger, and their criteria are proved in the slices that own AC4 and AC8. X6 is the path the cross-service scope check adds: in the monolith the scope was a local join that could not time out.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published interaction-ledger contract of this key and the rwb-case and rwb-decision contracts and their fakes from Day 1; needs the `rwb_source_data` baseline and its own sequence |
| Negotiable | The internal class split, the allocator's retry count and the read-back call are the squad's choice behind the contract; the table, its keys and its trigger are fixed |
| Valuable | One writer for every recording path, one ordered history per case and a refused write that names the missing field |
| Estimable | One migration, one controller, one service, one repository, three clients and one incident hook |
| Small | Fits one sprint with its tests, as the writer slice of the legacy key |
| Testable | Every criterion in section 7 is one API call, one concurrent pair of calls or one refused call, on synthetic cases |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer

  Background:
    Given case "RW-2026-000201" exists with 6 ledger entries, case_seq 1 to 6
    Given user "u-owner-02" holds RW-CASEOWN and owns case "RW-2026-000201"

  Scenario: AC5 A required value is missing (legacy RWB-E1-066 AC5)
    When a service calls append() for case "RW-2026-000201" with no event code
    Then the system refuses the call with MSG-GEN-001 for field "event code"
    Then the system writes no entry

  Scenario: AC6 Two entries for one case at the same moment (legacy RWB-E1-066 AC6)
    Given two transactions append to case "RW-2026-000201" at the same moment
    When both commit
    Then the entries carry case_seq 7 and 8
    Then no case_seq is missing or repeated

  Scenario: AC7 A case that does not exist (legacy RWB-E1-066 AC7)
    Given the rwb-case contract mock returns 404 for case ID "00000000-0000-0000-0000-000000000999"
    When the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999"
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system writes no entry
```

**Target reading.** Every assertion above keeps its legacy wording; what changes is where it runs. `append()` is no longer an in-process method of the monolith but `POST /api/recovery/source-data/v1/interactions` on this service, with `GET /api/recovery/source-data/v1/interactions/{entryId}` as the read that lets the writer answer 201 with the stored entry (DP-11, DP-13). The `interaction` table is P1's own table in schema `rwb_source_data` and holds the ledger for the whole Workbench (DP-01, DP-18; Architecture v5 slides 29 and 41; the R-PREC default ruling that the ledger belongs to rwb-source-data). The column migration and the append-only trigger `tr_interaction_append_only` sit on this service's per-service Flyway sequence, so the writer and the table version move together (DP-15; RWB-PLT-E1044-CON). `processed_event`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_source_data`, not tables this story designs (DP-09; RWB-PLT-TE006-CON). The event codes are reference data read through the rwb-case reference-data contract and are never constants (DP-07; RWB-P3-E1043-CON). Each append records its own ledger fact locally through the decision-record library (DP-03; RWB-PLT-E1027-CON). The screens that record an interaction arrive through gateway-bff and never call this service directly (DP-19; RWB-PLT-N001-CON). The case of AC7 is no longer looked up in a local table: the rwb-case case contract answers it, and the added Given line is the fake that answers 404 for the case ID (C RWB-P3-E1018-CON). Legacy AC1, AC2, AC3, AC4 and AC8 are owned by the rwb-case and rwb-integration slices of this key and by the cross-service proof, and this story claims none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ledger holds every interaction on a case; no other record is the authoritative history | REQ-ILG-001; case file item "Interaction ledger" (casemodel.txt) |
| BR2 | Every entry carries case, event, time, actor and source | REQ-ILG-002 |
| BR3 | An offer, promise, payment or hand-over is recorded on the interaction it was made in | REQ-ILG-004; interaction.promise_amount |
| BR4 | Entries are append only; a correction is a new entry naming the original | tr_interaction_append_only (Recovery Workbench Physical Schema v6.sql); R-UNI-24 |
| BR5 | A ledger write that fails stops the action and raises an incident; no entry is discarded | REQ-ILG-008; CTL-06 |
| BR6 | The ledger records what happened; the decision log records why; a decision entry links the two | FEAT-ILG-02; ADR-009 |
| BR7 | Entries of one case carry a gap-free sequence | REQ-ILG-001; interaction.case_seq |

**Where each rule lives in the target.** BR1 is now a schema rule as well as a business rule: the `interaction` table exists once, in `rwb_source_data`, and no other service's schema holds a copy, so "one ledger" is enforced by the schema boundary and not only by convention (DP-01, DP-18). BR2 and BR3 are the append's validation and its insert: the required values are checked against the published `InteractionRequest` schema and the LOV-LEDGER-EVENT list (DP-07), and the promise fields are written on the entry they belong to. BR4 is the append-only trigger on the service's own migration plus the absence of any update or delete method on the repository; a correction is a second insert with `corrects_entry_id`, and the schema still has no update path for application code (DP-15). BR5 keeps its shape but crosses a boundary: the database failure is translated into a 503 with MSG-P1-022 at this service, while the incident `LEDGER_WRITE_FAILED` is raised by the rwb-case and rwb-integration slices that own the action being rolled back, because only they know which action was stopped; this story ships the rollback and the hook. BR6 becomes the split between P1's ledger entry and rwb-decision's decision-log entry, joined by `decision_log_id`: the entry carries the reference and never the rule, the version or the inputs, which are read through the rwb-decision decision-log contract (DP-03, DP-11; RWB-P7-E1027-CON). BR7 is the allocator and the unique key `(case_id, case_seq)` inside one database transaction per case.

### 9. State transitions

None in the business sense. This story does not change a case status. It adds ledger entries; an entry has no status and is never changed.

| From | Event | Condition | To |
|---|---|---|---|
| a case at case_seq n | a valid append | The case check answers and the body validates | The case is at case_seq n+1 and one entry exists |
| a case at case_seq n | a refused append | A required value is missing, or the case is unknown | The case is still at case_seq n and no entry exists |
| an applied migration version | a correction | The ledger columns or the trigger need a fix | A new Flyway version is merged; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) through the recording screens and gateway-bff |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries only in this story (Case record R) |
| SY-CASEWF, case workflow module | Appends entries for case actions (Case record C) over the writer contract |
| SY-DATALOAD, data load | Appends entries from the EFS and ALS loads (Case record C) over the writer contract |
| RW-AUDIT, internal audit | Reads only; may not record (Case record R) |
| RW-PLATADM, platform administrator | Receives the LEDGER_WRITE_FAILED incident and reads the append series of the deployment |
| rwb-case (P3) | Owns the case, its scope and the case timeline; answers the case check this writer takes (C RWB-P3-E1018-CON) |
| rwb-decision (P7) | Owns the central decision ledger; answers the decision-log reference this writer confirms (C RWB-P7-E1027-CON) |

The append runs as the service identity of rwb-source-data (DP-02; Architecture v5 slides 11 and 29), and the caller's identity travels in the token so that the case check is made for the caller and not for the service.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-015 | interaction | actor_type | Write |
| DF-INT-016 | interaction | actor_ref | Write |
| DF-INT-017 | interaction | source_ref | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-019 | interaction | case_seq | Write |
| DF-INT-020 | interaction | decision_log_id | Write |
| DF-INT-021 | interaction | corrects_entry_id | Write |
| DF-CAS-001 | recovery_case | id | Read (through the rwb-case case contract, not from the table) |
| DF-DEC-001 | decision_log_entry | id | Read (as a reference through the rwb-decision contract) |
| DF-DEC-003 | decision_log_entry | decision_code | Read (reference only) |
| DF-DEC-004 | decision_log_entry | rule_id | Read (reference only) |
| DF-DEC-005 | decision_log_entry | rule_version | Read (reference only) |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read (reference only) |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read (reference only) |

Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** `DF-INT-001` to `DF-INT-021` are this story's: the migration adds the eight ledger columns `event_code`, `actor_type`, `actor_ref`, `source_ref`, `idempotency_key`, `case_seq`, `decision_log_id` and `corrects_entry_id`, it drops `NOT NULL` on `channel` and `direction` so that a Workbench event such as `CASE_CREATED` needs neither, and the writer fills them. `DF-DEC-001` to `DF-DEC-010` are rwb-decision's own rows in `rwb_decision`: this story reads the six references above through the decision-log contract and never from the table (DP-01, DP-03). `DF-CAS-001` is rwb-case's own key, read through the case contract and never joined locally.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). The append and the read of one entry, on the interaction-ledger resource of RWB-P1-E1066-CON.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/interactions` | Appends one ledger entry to a case and returns 201 with the stored entry | Any authenticated caller with Case record C on the case; a service identity of rwb-case or rwb-integration for an event path | `Idempotency-Key` required; the same key with the same body returns the stored entry and the same `caseSeq`; the same key with a different body is refused |
| GET | `/interactions/{entryId}` | Reads one entry of this service's ledger, so the writer answers 201 with what it stored and a correction can name the entry it corrects | Case record R on the entry's case | Idempotent by entry ID |

The request body is `InteractionRequest` of the API specification — `channel`, `direction`, `result`, `summary`, plus the ledger fields the append needs — and the response is the `Interaction` schema of the API specification, which carries `eventCode`, `caseSeq`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `decisionLogId`, `correctsEntryId` and `retentionClass` among the fields of the resource. Errors are 400 for a body that fails schema validation, 401 without a session, 403 without Case record C, 404 for a case that does not exist or is out of scope (MSG-P4-003), 409 for an `Idempotency-Key` already used with a different body, 422 for a missing or invalid field (MSG-GEN-001), and 503 when the ledger cannot be written (MSG-P1-022) or the case contract does not answer inside 2 s. The exact error status for the idempotency conflict, the authorisation of the append and the 404 semantics are Not specified in the source documents (GAP-0504; ASM-0696); this story fixes them as above and RWB-P1-E1066-CON publishes them.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Once per append: the case exists, and the caller holds Case record C and the case scope; a 404 is passed on unchanged as 404 with MSG-P4-003 | DP-11; C RWB-P3-E1018-CON; faked |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Only for a `DECISION_TAKEN` entry: confirms the reference and returns nothing that is stored except the identifier | DP-03, DP-11; C RWB-P7-E1027-CON; faked |

Both calls are one hop with a 2 s timeout and a breaker per downstream (DP-11; Architecture v5 slide 11). The reference list **LOV-LEDGER-EVENT** reaches this service through the rwb-case reference-data client library and not as a run-time call of its own (DP-07; C RWB-P3-E1043-CON). No other service is called, and no table of another service is read (DP-01).

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 41). The decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` when a decision entry is appended, through the outbox (DP-03, DP-09); that is the library's event and not a business event of this story, and this story adds no message schema of its own.

#### 12.4 Events consumed

None. The recording screens arrive over REST and the event paths of rwb-integration call the append over REST as well; Architecture v5 slide 15 gives this service no consumed event. The outbox rebuild of an entry from a business event is RWB-P1-E1067-APP.

#### 12.5 Workflows and activities

None. The append is a synchronous REST step and writes one row in one transaction. The Temporal activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are other P1 stories; the task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data | The ledger table: the migration adds the eight ledger columns, drops `NOT NULL` on `channel` and `direction`, adds the unique keys `(case_id, case_seq)` and `(idempotency_key)`, keeps and re-creates the append-only trigger `tr_interaction_append_only`, and keeps the index `ix_interaction_case_time` on `(case_id, occurred_at)`; the writer inserts and reads it and never updates or deletes |
| `processed_event` | `rwb_source_data` | PLT library, created in this service's schema | The inbox of DP-09; read and written by the library, not by this story's code |
| `idempotency_key` | `rwb_source_data` | PLT library, created in this service's schema | The stored response of the append; read and written by the library |
| `outbox_event` | `rwb_source_data` | PLT library, created in this service's schema | The outbox the decision-record library writes through; this story adds no row of its own |

No table of another service is read and no foreign key crosses a schema (DP-01). The decision-log table `decision_log_entry` stays in `rwb_decision` and the case table `recovery_case` stays in `rwb_case`; both are reached over their contracts only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P3-E1018-CON fake | `GET /api/recovery/case/v1/cases/{caseId}` | A case in scope with Case record C, a case out of scope, a 404 for the synthetic case ID of AC7, and a timeout |
| RWB-P7-E1027-CON fake | `GET /api/recovery/decision/v1/decision-log/{entryId}` | A decision entry with code, rule, version and inputs reference, and a missing entry |
| RWB-P3-E1043-CON fake | The reference-data contract | The twelve values of LOV-LEDGER-EVENT, a value outside the list, and the Thai labels |
| Ledger fixture | `rwb_source_data` | A container at the baseline plus this story's migration, with the interaction table, its two unique keys and its trigger, so the concurrency test of AC6 runs on the real keys |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | 2 operations (`GET /api/recovery/case/v1/cases/{caseId}`, `GET /api/recovery/decision/v1/decision-log/{entryId}`) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | The topic belongs to RWB-P1-E1013-APP; `DecisionRecorded` is published by the local library (DP-03) |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `ledger`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data only through rwb-source-data's own contract or views; this story reads no ACE data | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case and the client library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox, inbox and idempotency library in this service's schema; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-18 is this story's own pattern: the ledger that the monolith held in the shared `recovery` schema becomes P1's table in `rwb_source_data`, and every consumer reads it through a contract. DP-11 is used twice, once for the append itself and once for the case check that replaces the local join. DP-03 applies as one decision record per appended entry, recorded locally and published to `rwb.decision-record.v1` by the library. DP-19 applies to the recording screens, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<next>__rwb_e1_066_interaction_ledger.sql` (legacy migration; the next version on the service sequence) | Migration | The eight ledger columns, the nullable channel and direction, the two unique keys, the append-only trigger and the case-time index |
| `InteractionWriteController` | Controller | The two operations of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; `Idempotency-Key` handling |
| `LedgerWriteService` | Service | Validation against LOV-LEDGER-EVENT, the allocator, the insert, the read-back and the incident hook |
| `InteractionRepository` | Repository | Inserts and reads interaction rows; no update and no delete method exists |
| `Interaction` | Entity | Immutable mapping of the interaction table |
| `CaseScopeClient` | Client | The rwb-case case contract: one hop, 2 s timeout, 404 passed on unchanged (DP-11) |
| `DecisionLogClient` | Client | The rwb-decision decision-log contract, for the reference of a `DECISION_TAKEN` entry (DP-03) |
| `ReferenceDataClient` | Client library use | Reads LOV-LEDGER-EVENT as data; no event code in code (DP-07) |
| `LedgerIncidentHook` | Hook | Raises `LEDGER_WRITE_FAILED` with the case ID and the error class, and never the summary or a contact point |

**Migrations and sequence (DP-15).** The migration sits on rwb-source-data's own Flyway sequence, after the baseline, and creates the ledger columns, the two unique keys, the trigger and the index in schema `rwb_source_data`. The legacy column and key definitions are kept as written in RWB-E1-066 §13; the exact version number is assigned by the sequence owner at build time, and no monolith version number is reused. An applied version is never edited.

**Database.** This story owns one table's shape: the `interaction` table in `rwb_source_data`. It creates no table of another service, adds no foreign key across a schema, and reads `decision_log_entry` and `recovery_case` over their contracts only (DP-01).

**Configuration and reference data**

- The list LOV-LEDGER-EVENT with its twelve values and its Thai labels is reference data of rwb-case, read through the client library and never written in the code (DP-07).
- The 2 s budget of the two consumed calls, the breaker and the bulkhead are configuration of the clients (DP-11).
- The flag `rwb.dataengine.ledger-writer` gates the writer at deployment (RWB-P1-E1066-OPS).
- The case-scope answer is never cached across calls: a stale answer would be a scope leak, and a call that does not answer inside 2 s refuses the append (X6).

**Build steps**

1. The migration for the eight columns, the nullable channel and direction, the two unique keys, the trigger and the index, with a repeated run that changes nothing.
2. `LedgerWriteService` validation against LOV-LEDGER-EVENT and the required fields, with MSG-GEN-001 naming the field and no insert on a refusal (AC5).
3. The `case_seq` allocator: a transaction-level advisory lock on the case ID and `max(case_seq)` plus one, with one retry on a unique-key clash, and a concurrency test on two connections (AC6).
4. The insert and the read-back through `GET /interactions/{entryId}`, so 201 carries the stored entry and the stored `caseSeq`.
5. The case check and the decision-log reference as the two clients of 12.2, each with its 2 s budget and its fake (AC7, X6).
6. The `Idempotency-Key` handling through the platform library: same key and same body returns the stored entry; same key and a different body is refused on the contract of RWB-P1-E1066-CON.
7. The failure path: the database error becomes a 503 with MSG-P1-022 and the `LEDGER_WRITE_FAILED` hook fires with the case ID and the error class.
8. An architecture test that no class outside the `ledger` module uses `InteractionRepository`, and that the repository has no update and no delete method.
9. Tests for AC5, AC6 and AC7 with the fakes of 12.8, and the regression rows of section 16 where the fixture of the owning slice is available.

**Feature flag.** `rwb.dataengine.ledger-writer`. Off, the append is refused at the edge of this service and no entry is written; the recording screens see the refusal as an error and no action is saved.

**Done when.** The tests in section 16 pass, the migration is applied on the service sequence with the trigger and the two unique keys in place, the append answers 201 with the stored entry against the two fakes, two concurrent appends for one case yield case_seq n+1 and n+2 with no gap, and a missing event code and an unknown case are both refused with nothing written.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed (new, see additions) | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing | Enter {field}. |
| MSG-P4-002 | Role without Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope | This case is not in your scope. |

Thai text for each message follows decision DL10. MSG-P4-002 and MSG-P4-003 are raised by the case check and passed on unchanged; the field name of MSG-GEN-001 is filled from the validation failure and is never a data value.

### 15. Screens and states

No screen in this story. In Epic 1 a contact is recorded through the recording screens of the rwb-case slice, which arrive through gateway-bff (DP-19; RWB-PLT-N001-CON) and call this writer; the case record view SCR-03 (Read only) shows ledger entries through the read interface of RWB-P1-E1068-APP. On a refused or failed append the caller sees MSG-GEN-001, MSG-P4-003 or MSG-P1-022 in the Error state of the recording screen; this story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-066-01 | AC1, BR2, BR3 — regression evidence: AC1 is owned by the rwb-case and rwb-integration slices of this key and the cross-service proof | End to end | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 |
| TC-E1-066-02 | AC2, BR1, BR7 — regression evidence: AC2 is owned by the recovery slices and the cross-service proof | End to end | 4 EFS entries, CASE_CREATED and CASE_ALLOCATED |
| TC-E1-066-03 | AC3, BR6 — regression evidence: AC3 is owned by the rwb-case slice and the rwb-decision contract | End to end | Reassignment under R-UNI-18 version 2026.11 |
| TC-E1-066-04 | AC4, BR5 — regression evidence: AC4 is owned by the rwb-integration slice and the cross-service proof | End to end | Insert forced to fail |
| TC-E1-066-05 | AC5 | End to end | append() with no event code |
| TC-E1-066-06 | AC6, BR7 | End to end | Two concurrent appends on one case |
| TC-E1-066-07 | AC7 | End to end | Unknown case ID |
| TC-E1-066-08 | AC8, BR4 — regression evidence: AC8 is owned by the migration trigger of this key and the cross-service proof | End to end | UPDATE and DELETE on entry case_seq 3; CORRECTION entry |
| TC-E1-066-09 | Access — regression evidence: the access path of the recording screen belongs to the rwb-case slice | Component | RW-AUDIT posts an interaction; refused with MSG-P4-002 |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. TC-E1-066-05, TC-E1-066-06 and TC-E1-066-07 are the three criteria this story owns and run here against the fakes and the ledger fixture; the other six rows are kept as regression evidence for the slices of this legacy key that own those criteria, and they run again in RWB-ITG-E1066-ITG against the live contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: event codes are list values of LOV-LEDGER-EVENT read through the reference-data contract; channels, directions and results come from their lists; the case-scope answer and the 2 s budget are configuration.
- No personal data in logs, tests, events or prompts: the incident detail names the case ID and the error class only; the summary is never logged; test summaries are synthetic, and the entry's `summary` is the one personal-data field and is masked by role at the read.
- No read of another service's tables: the case is read through the rwb-case case contract, the decision entry through the rwb-decision contract, and the `interaction` table is written only through this story's service and read only through its contract and the read interface (DP-01, DP-03, DP-11).
- No entry is ever updated or deleted by application code: the trigger refuses the statement and the repository has no such method.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).
- The append is one hop, 2 s, with a breaker per downstream; a slow case answer refuses the append and writes nothing (DP-11).
- The platform library objects stay the library's: `processed_event`, `idempotency_key` and `outbox_event` are created in this schema and are never redefined by this story (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-02 | All recovery processes | R-UNI-24 | TC-E1-066-02, TC-E1-066-06, TC-E1-066-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01, TC-E1-066-03, TC-E1-066-05, TC-E1-066-07 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry discarded | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-05 | All recovery processes | CTL-06 | TC-E1-066-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-CON | Contract | H build dependency: the interaction-ledger contract this story implements, its schemas, its error envelope and its fakes |
| RWB-P1-E1066-OPS | DevOps | X external dependency: the chart, the migration step, the flag, the five series and the three alerts of the writer |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the outbox path that turns a Workbench event into an append, and the duplicate rule |
| RWB-P1-E1068-APP | App development | Sibling of the same legacy key: the read interface and its filters |
| RWB-P3-E1018-APP | App development | Sibling: the rwb-case recording screens that call this writer, and the case timeline that reads the ledger through this contract |
| RWB-ITG-E1066-ITG | Integration | Proves AC1, AC2, AC3, AC4 and AC8 against the live contracts and the live ledger |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the reference-data client library, the outbox and inbox library, the per-service Flyway sequence and the gateway-bff composite route |
| RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON | Contract | C: the reference-data contract, the case contract and the decision-log contract, each with its fake |

### 19. Out of scope

- Writing the Workbench events from the outbox to the ledger and duplicate rejection across event paths (RWB-P1-E1067-APP).
- The ledger read interface, its filters and its paging (RWB-P1-E1068-APP).
- The case timeline, the case record view and the recording screens of rwb-case (RWB-P3-E1018-APP); this story serves them and builds none of them.
- The append-only behaviour as a business proof and the second row of a correction (RWB-ITG-E1066-ITG); this story ships the trigger and the insert. The database deployment of the trigger, of the two unique keys and of the index is RWB-P1-E1066-OPS.
- The central decision ledger of rwb-decision, its entries, its rules and its versions (RWB-P7-E1027-CON and the P7 stories); this story reads a reference and stores the identifier.
- The decision-record library, the outbox relay and the idempotency store as platform components (RWB-PLT-E1027-CON, RWB-PLT-TE006-CON).
- The reference data itself, its values and its Thai labels (rwb-case, RWB-P3-E1043-CON).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034 in the legacy set and the integration slices of this key).
- The retention class resolution for ledger entries (FEAT-ILG-10, RWB-E2-034); this story writes the column it is given and resolves nothing.
- The gateway-bff composite route and the screen rendering of a masked summary (RWB-PLT-N001-CON and the screen owners).
