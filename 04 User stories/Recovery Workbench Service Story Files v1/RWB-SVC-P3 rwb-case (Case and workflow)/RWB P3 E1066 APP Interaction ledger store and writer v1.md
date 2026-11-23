# RWB-P3-E1066-APP Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1066-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P3-U |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1066-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-case. The in-process `InteractionLedgerWriter.append()` of the monolith becomes the append of `rwb-source-data` (`POST /api/recovery/source-data/v1/interactions`, DP-11, DP-13), the `interaction` table becomes that service's own table in `rwb_source_data` (DP-01, DP-18; R-PREC default ruling), and this service keeps the case side of the same act: one link row per case action naming the entry that action wrote, the refusal that stops the action, the incident that names it, and no ledger row, no copy and no sequence of its own. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner and the case workflow (RW-CASEOWN; SY-CASEWF)**, I want **every case action of rwb-case — the case created, allocated, transferred or escalated, a contact or promise recorded, a decision taken — written into the one interaction ledger of rwb-source-data through its published append in the same act that takes the action, with one link row in `rwb_case` naming the entry the action wrote, and a refusal that stops the action and raises `LEDGER_WRITE_FAILED`**, so that **the history of a case is never assembled after the fact, while rwb-case holds no ledger entry, no ledger column and no case sequence of its own**.

- **Delivers, in `rwb-case`:** the case-side writer that every P3 case action calls — the append client (one hop, 2 s, breaker), the command it builds from the action, the event-code check against LOV-LEDGER-EVENT, the link table `interaction_link` in schema `rwb_case` with its PENDING, COMMITTED and REFUSED states, the incident hook, the correction path, and one Temporal activity for the case actions `CaseWorkflow` takes.
- **Consumes:** `RWB-P1-E1066-CON` — the append `POST /api/recovery/source-data/v1/interactions` and the entry it returns.
- **Not this slice:** the ledger table, its append-only trigger, its `case_seq` allocator, its columns and its read interface (rwb-source-data, this legacy key, DP-18); the recording screens and the timeline item (RWB-P3-E2034-APP, RWB-P3-E1018-APP); the cross-service proof (RWB-ITG-E1066-ITG). `interaction` is not a table of `rwb_case`.

### 2. Business rationale

Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

The realignment moves one seam and keeps four promises. The seam is the transaction: the action and its ledger entry are now owned by two services, so "written in the same transaction as the action" becomes a write order inside one act — the append is asked first and the case action commits only when the append has answered with an entry — and the one row this service keeps is the link that says which entry belongs to which action. The four promises are unchanged and each one now has a named owner: the entry is written once and ordered by the ledger's owner (DP-18); the case action is refused when the entry cannot be written (BR5); the act that was refused is named in the incident, which only the owner of the action can say (this slice); and the entry for a decision carries the decision log reference only, never the rule, the version or the inputs (BR6).

Two consequences are in this story rather than in a later one. An entry can exist for an action that never committed, and the writer reconciles it by appending one `CORRECTION` entry that names the original, which is the correction rule the ledger already has (BR4). And a retry must not write a second entry, so the action fixes one `Idempotency-Key` and the ledger answers the replay with the entry it stored (BR9).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| `RWB-P1-E1066-CON` is baselined | The append as consumed: `InteractionRequest` in, 201 with `Interaction` and its `caseSeq`, create-only, idempotent on `Idempotency-Key`, 409 for a replayed key with a different body, 422 for a missing value, 503 when the store is down, and the fake. The exact resource path and the per-service login name are carried as an open assumption of that contract (GAP-0505; ASM-0697) |
| The `rwb-case` baseline is applied | Schema `rwb_case` with `recovery_case`, its own Flyway sequence and history table, and the `rwb_case` login (DP-02, DP-15; RWB-PLT-E1044-CON) |
| The case facts and the case actions exist | `recovery_case` with case numbers RW-YYYY-NNNNNN, and the allocation, transfer and escalation actions this writer serves (RWB-P3-E1018-APP and the case action stories of this service) |
| The reference data of this service is loaded | The list **LOV-LEDGER-EVENT** with its values and Thai labels as rows of `rwb_case` reference data, loaded by the reference data administrator (DP-07; TSD P3 v3 T5.1). The sources disagree on its length — 14 values in TSD P3 v3, 12 in the legacy story §13 (GAP-2253; ASM-3711) |
| The event path exists | `CaseWorkflow` on task queue `rwb-case` in namespace `rwb-recovery`, so the case actions it takes can call the append activity (Architecture v5 slides 8 and 15) |
| The caller holds the case | Case record C with the case in scope: a person through the screens and gateway-bff, or the service identity of rwb-case with a workload identity token (DP-19) |

The legacy preconditions RWB-E1-018 and RWB-E1-027 are kept as the case record and the incident path of the target: the case record is this service's own, and the incident path is the `LEDGER_WRITE_FAILED` record and operations alert of this story's hook. The interaction table and its append-only trigger are no longer a precondition of this service, because they are not its table (DP-01, DP-18).

### 4. Flow

1. A case action is taken: the case is created, allocated, transferred or escalated by a P3 story, a contact or promise is recorded, or a case decision is taken (BR1).
2. `CaseActionLedgerWriter` derives the event code — `CASE_CREATED`, `CASE_ALLOCATED`, `CASE_TRANSFERRED`, `CASE_ESCALATED`, `CONTACT`, `PROMISE`, `DECISION_TAKEN` — and checks it against **LOV-LEDGER-EVENT** in this service's own reference rows; a code outside the list is refused with MSG-GEN-001 and nothing is appended (AC5, DP-07).
3. The writer inserts one `interaction_link` row in state `PENDING` — case ID, action reference, event code and one `Idempotency-Key` derived from the action reference — in the same local transaction as the case action, before that action is visible (AC1, DP-15).
4. `InteractionLedgerClient` calls `POST /api/recovery/source-data/v1/interactions` once, one hop, 2 s timeout, with the case and party, the event code, the occurred time, the actor and its reference, the source system `WORKBENCH` and its reference, the channel and direction where they apply, the action code, the contact result, the promise amount and date, the summary, the decision log entry ID for a decision, the entry it corrects for a correction, and the key (DP-11, DP-13, DP-18).
5. For a decision, the local decision-record library records it in this service's own record and its identifier travels as `decisionLogId`; the rule, the version and the inputs stay in `rwb-decision` and in the record (BR6, DP-03).
6. The ledger answers 201 with the entry and its `caseSeq`; the link row moves to `COMMITTED` with the entry identifier and the `caseSeq` it was given, and the case action commits and becomes visible (AC1, AC2, AC6).
7. A replay of the same action with the same key is answered with the stored entry and the same `caseSeq`, and no second entry is written (AC1, AC6).
8. A refusal: 422 becomes MSG-GEN-001, 404 becomes MSG-P4-003, 503 or a timeout becomes MSG-P1-022; the local transaction does not apply the action, the link row is `REFUSED`, and the hook raises `LEDGER_WRITE_FAILED` with the case ID and the error class only (AC4, X1 to X3).
9. A reconciliation: an entry was answered but the local commit then failed, so the writer appends one `CORRECTION` entry naming the entry it replaces and leaves the link row `REFUSED`; nothing is updated and nothing is deleted (AC8, BR4).
10. The actions `CaseWorkflow` takes use the same path as one activity `appendLedgerEntry` on queue `rwb-case`, with the action reference as the key, so a Temporal retry never writes a second entry (12.5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ledger cannot be written (503 or a database failure at the owner) | The case action is not applied; the link row is `REFUSED`; 503 to the caller; the incident is raised; nothing is discarded silently | MSG-P1-022 | AC4 |
| X2 | A required value is missing or the event code is not in LOV-LEDGER-EVENT | Refused before the append, naming the field; the link row is not written | MSG-GEN-001 | AC5 |
| X3 | The append does not answer inside 2 s, or the breaker is open | The action is refused with 503 and MSG-P1-022; the link row is `REFUSED`; no entry is assumed | MSG-P1-022 | AC4 |
| X4 | The case does not exist, or is outside the caller's scope | Refused with 404 before the append; nothing written | MSG-P4-003 | AC7 |
| X5 | The caller holds no Case record C | Refused with 403 before the append; nothing written | MSG-P4-002 | AC9 |
| X6 | The same action is retried after a timeout, and the first call had in fact committed at the owner | The replay with the same key returns the stored entry and its `caseSeq`; one entry exists and the action commits once | None | AC1, AC6 |
| X7 | The append answered, then the local commit failed | One `CORRECTION` entry naming the original is appended; the link row stays `REFUSED`; no entry is updated or deleted | None | AC8 |
| X8 | The ledger answers 409 for a replayed key with a different body | Treated as a defect of the derived key, refused with MSG-P1-022 and raised as an incident; no second entry | MSG-P1-022 | Section 12.2 |

X1 to X5 are the legacy exception paths of RWB-E1-066, carried unchanged in meaning; the write failure, the missing value, the unknown case and the read-only role keep their messages and their status codes. X6 to X8 are the paths the move to two services adds, and each is the reason for one line of section 13.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds from Day 1 against `RWB-P1-E1066-CON` and its fake; the case facts, the reference list and the migration sequence are this service's own |
| Negotiable | The link table's shape, the state names, the key derivation and the reconciliation step are the squad's choice behind the contract; the write order, the refusal and the incident are fixed |
| Valuable | Every case action lands in one ordered history, one act refuses instead of half-writing, and the incident names the action that stopped |
| Estimable | One migration, one writer, one client, one repository, one hook and one activity |
| Small | Fits one sprint with its tests, as the case-side slice of the legacy key |
| Testable | Every criterion of section 7 is one call against the P1 fake, one concurrent pair, one refusal or one reconciliation, on synthetic cases |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer

  Background:
    Given case "RW-2026-000201" exists with 6 ledger entries, case_seq 1 to 6
    Given user "u-owner-02" holds RW-CASEOWN and owns case "RW-2026-000201"

  Scenario: AC1 One case action appends one entry and records its link (new, D-RCV-60)
    Given the rwb-source-data contract mock returns one entry reference with case_seq 7 for event "CONTACT"
    When the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15
    Then the case action appends once to the rwb-source-data contract with case "RW-2026-000201", event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL", direction "OUTBOUND", promise 25,000.00 for 2026-12-15 and source system "WORKBENCH"
    Then the link row of the action holds event "CONTACT", case_seq 7 and the entry reference the contract returned, and it holds no summary, no contact result and no promise amount
    Then the case action is committed and the caller receives 201 with case_seq 7
    Then a repeat of the same action with the same Idempotency-Key appends no second entry

  Scenario: AC2 It is ordered and complete, and the order is the ledger's (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the 6 entries of "RW-2026-000201": 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01
    When the history of the case is read
    Then the 6 entries read in one sequence ordered by occurred time
    Then case_seq runs 1 to 6 with no gap
    Then rwb_case holds no sequence of its own: the link rows carry only the case_seq the contract returned, and no column and no table of rwb_case allocates one

  Scenario: AC3 The entry is distinct from the decision log (new, D-RCV-60)
    Given owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01"
    Given the rwb-source-data contract mock returns one entry reference with case_seq 7 for event "DECISION_TAKEN"
    When the reassignment is taken on the case
    Then the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver
    Then the append carries event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, no version and no inputs
    Then the link row holds the decision log entry ID only

  Scenario: AC4 A write failure is visible and stops the action (new, D-RCV-60)
    Given the rwb-source-data contract mock returns 503 for the append
    When the case owner records a call on case "RW-2026-000201"
    Then the system refuses the call with status 503 and MSG-P1-022
    Then the case action is not applied, the link row of the action is "REFUSED", and rwb_case holds no committed action and no entry reference
    Then the system raises an incident "LEDGER_WRITE_FAILED" with case "RW-2026-000201" and the error class only
    Then the ledger still holds 6 entries

  Scenario: AC5 A required value is missing (new, D-RCV-60)
    Given the case action builds the event code "CONTACT_TRIED" which is not in LOV-LEDGER-EVENT
    When the case owner takes the action on case "RW-2026-000201"
    Then the system refuses the action with MSG-GEN-001 for field "event code"
    Then the system appends nothing and writes no link row

  Scenario: AC6 Two actions for one case at the same moment (new, D-RCV-60)
    Given the rwb-source-data contract mock returns case_seq 7 for the first append and case_seq 8 for the second
    When two case actions on case "RW-2026-000201" append at the same moment
    Then the two link rows carry case_seq 7 and 8
    Then no case_seq is missing or repeated
    Then rwb_case allocates no sequence and makes no second append for either action

  Scenario: AC7 A case that does not exist (new, D-RCV-60)
    Given no case row exists for case ID "00000000-0000-0000-0000-000000000999"
    When the case owner takes an action for case ID "00000000-0000-0000-0000-000000000999"
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system appends nothing and writes no link row

  Scenario: AC8 An entry cannot be changed, only corrected (new, D-RCV-60)
    Given the append of a case action on "RW-2026-000201" answered with the entry of case_seq 3 and the local commit then failed
    When the writer reconciles the action
    Then the system appends one new entry with event "CORRECTION" naming entry case_seq 3
    Then no entry is updated and none is deleted, and the link row of the failed action stays "REFUSED"

  Scenario: AC9 A role that may read only cannot record (new, D-RCV-60)
    Given user "u-audit-01" holds RW-AUDIT and reads only
    When "u-audit-01" records a contact on case "RW-2026-000201"
    Then the system refuses the call with status 403 and MSG-P4-002
    Then no append is made and no link row is written
```

**Target reading.** `RWB-E1-066` is a secondary slice of this service: its legacy criteria are carried by rwb-source-data's own stories of this key (the ledger, its writer, its read interface), by the recording and timeline stories of rwb-case (RWB-P3-E2034-APP, RWB-P3-E1018-APP) and by RWB-ITG-E1066-ITG; the nine criteria above are therefore written `(new, D-RCV-60)` and assert only what this slice delivers, with every legacy value kept character for character — the case numbers, the times, the amount 25,000.00, the promise date 2026-12-15, the rule `R-UNI-18` version `2026.11`, decision code `D6`, the users and the unknown case ID. `append()` is no longer an in-process method: it is `POST /api/recovery/source-data/v1/interactions` on `RWB-P1-E1066-CON`, and each criterion that needs it carries the contract mock. AC1 to AC8 keep their legacy numbers, AC9 is the access criterion of `TC-E1-066-09`, and no legacy criterion is claimed twice by two services: the row that this service owns is the link, the refusal and the incident.

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
| BR8 | A case side holds no ledger row, no ledger column and no sequence: the entry and its order belong to the ledger's owner | DP-01; DP-18; R-PREC default ruling |
| BR9 | A case action commits only when its entry has been written, and a retried action writes no second entry | Legacy BR5; REQ-ILG-007; DP-18 |

**Where each rule lives in the target.** BR1 and BR8 are one rule seen from two sides: the ledger exists once in `rwb_source_data`, so `rwb_case` keeps only the link (DP-01, DP-18). BR2 and BR3 are the command built from the action, with the five required values checked before the append. BR4 becomes the trigger at the owner plus the absence of any update, delete or rewrite path here; the only repair is a `CORRECTION` append. BR5 crosses the seam and is expressed as an order: the append is asked first and the action is not applied when it refuses. BR6 is the `decisionLogId` field, and the rule, the version and the inputs are never sent. BR7 leaves this service entirely: no allocator and no sequence column exists in `rwb_case`. BR9 is the write order and the key derivation.

### 9. State transitions

None in the case. This story changes no case status; it moves no case and closes none. The only states it owns are the states of its own link row, and an entry of the ledger has no status at all.

| From | Event | Condition | To |
|---|---|---|---|
| (no link row) | a case action is taken | The event code is in LOV-LEDGER-EVENT and the caller holds Case record C | `PENDING`, with one key derived from the action reference |
| `PENDING` | the append answers 201 | The entry and its `caseSeq` are returned | `COMMITTED`; the case action commits and the entry identifier is kept |
| `PENDING` | the append answers 422, 404, 503 or does not answer inside 2 s | No entry is returned | `REFUSED`; the action is not applied; the incident is raised on a 5xx or a timeout |
| `PENDING` | the append answers but the local commit fails | The entry exists without its action | `REFUSED`, and one `CORRECTION` entry is appended naming the original |
| `COMMITTED` | a repeat of the same action | The key is the same and the entry is the stored one | `COMMITTED`, unchanged; no second entry |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Takes the actions of a case they hold (Case record C, scope Own); the entry is written by the ledger's owner on this writer's request |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Take the actions their role allows on a case in scope (Case record C); read entries through the read interface of rwb-source-data |
| SY-CASEWF, the case workflow | Takes the case actions of `CaseWorkflow` and calls the append activity with the action reference as its key (Case record C) |
| SY-DATALOAD, data load | Takes the load actions that raise an entry, with the source system of the load (Case record C) |
| RW-AUDIT, internal audit | Reads only; may not record, and the refusal is MSG-P4-002 (Case record R) |
| RW-PLATADM, platform administrator | Receives the `LEDGER_WRITE_FAILED` incident and reads the append series and the breaker state of the deployment |
| rwb-source-data (P1) | Owns the ledger, the entry, its `case_seq`, its trigger and its read; answers the append of this story (C `RWB-P1-E1066-CON`) |

The check is Case record C with the scope applied, from the cached permission data of rwb-access, evaluated by the service that owns the case (OWASP API1, object-level authorisation; Architecture v5 slide 10). No role name and no scope value sits in code, and the service runs as the `rwb_case` login (DP-02).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002 | recovery_case | id, case_no | Read (own schema) |
| DF-CAS-009 | recovery_case | owner_user_id | Read (own schema) |
| DF-INT-002 | interaction | case_id | Write: sent in the append command |
| DF-INT-014 | interaction | event_code | Write: sent, and kept on the link row |
| DF-INT-015, DF-INT-016 | interaction | actor_type, actor_ref | Write: sent in the append command |
| DF-INT-017 | interaction | source_ref | Write: sent in the append command |
| DF-INT-018 | interaction | idempotency_key | Write: one key per action, kept on the link row |
| DF-INT-019 | interaction | case_seq | Write: kept on the link row as returned by the owner |
| DF-INT-020 | interaction | decision_log_id | Write: sent for a decision, kept on the link row |
| DF-INT-021 | interaction | corrects_entry_id | Write: sent for a correction |
| DF-INT-001, DF-INT-003 to DF-INT-013 | interaction | id, party_id, occurred_at, channel, direction, action_code, contact_result, promise_amount, promise_date, summary, conduct_check, source_system | Write at the owner only: sent in the command, never stored in `rwb_case` |

Field IDs are those in the Logical Data Model and Data Dictionary. Every `interaction` row belongs to rwb-source-data (DP-18): this service sends fields and stores five of them — the event code, the key, the case sequence, the entry identifier and the decision log reference — on `interaction_link`, a technical table of the target with no BR Field ID of its own. The summary, the contact result and the promise amount are personal or commercial values and are not copied into `rwb_case`; the table's exact column names, lengths and state values are a target choice and are Not specified in the source documents (GAP-2255; ASM-3713).

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no resource and no operation to `/api/recovery/case/v1` (DP-13): the append of the legacy key is provided by rwb-source-data on `/api/recovery/source-data/v1`, and this service is one of its callers. The legacy operation **API-P3-015 `POST /cases/{caseId}/interactions`** of TSD P3 v3 therefore has no counterpart here — the case-side record path becomes the append of `RWB-P1-E1066-CON`, and the case-scoped read **API-P3-014** becomes the ledger read of that contract with `caseId` as its filter (GAP-2256; ASM-3714). The recording screens and the timeline item that show the result stay with RWB-P3-E2034-APP and RWB-P3-E1018-APP and call this writer; they are not served by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/interactions` | P1 rwb-source-data | The append of one case action: `InteractionRequest` in, 201 with `Interaction` and its `caseSeq`, the stored entry on a replay of the same key, 409 on a replay with a different body, 422 for a missing value, 503 when the store is down | DP-11, DP-18; C `RWB-P1-E1066-CON`; faked |

One row, one hop, 2 s timeout and a breaker per downstream; no retry on a 4xx and no retry at all with a new key. The list **LOV-LEDGER-EVENT** is not a call: it is read from this service's own reference rows (DP-07). The right and the scope come from the cached permission data of rwb-access, not from a call per action (DP-08 is not applied by this story). No other service is called and no table of another service is read (DP-01).

#### 12.3 Events published

None of its own. The topic of this service is `rwb.case.events.v1` with names `rwb.case.<Event>.v1` (DP-14), and its events belong to the stories that raise them; this writer adds no message schema. The local decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` when a case decision is recorded (DP-03); that is the library's event, not this story's business event, and the append itself is synchronous over REST, so this story writes no outbox row of its own.

#### 12.4 Events consumed

None. No case action is started by a consumed event in this story; the events that start case actions (`PaymentMissed` and the other signals of Architecture v5 slides 15 and 41) are consumed by the stories that own those actions, and each of them calls this writer in its own request.

#### 12.5 Workflows and activities

| Item | Queue | Namespace | Use |
|---|---|---|---|
| Activity `appendLedgerEntry` | `rwb-case` | `rwb-recovery` | The same append as one activity for the case actions `CaseWorkflow` takes: the case ID, the action reference, the event code and the command; the action reference is the `Idempotency-Key`, so a workflow retry never writes a second entry (AC1, AC6) |

One activity and no workflow: `CaseWorkflow` is the parent workflow of RWB-P3-E2043-APP and is not changed here. The activity's retry policy is Temporal's and is bounded; a refusal from the owner is a non-retryable application failure that the workflow sees as a failed action (AC4).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: every append is started by a case action, never by a clock.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction_link` | `rwb_case` | P3 rwb-case | New: one row per case action — case ID, action reference, event code, entry identifier, `case_seq`, decision log reference, key, state and timestamps; unique on the action reference and on the key; written, moved between its three states, never deleted |
| `recovery_case` | `rwb_case` | P3 rwb-case | Read: the case and its owner, and the object of the authority check |
| `lov_value`, `reference_row`, `reference_version` | `rwb_case` | P3 rwb-case | Read: LOV-LEDGER-EVENT and its labels with the version in force (DP-07) |
| `idempotency_key`, `outbox_event`, `processed_event` | `rwb_case` | PLT library, created in this schema | Present; this story writes none of them, because the replay is answered by the ledger's owner under the key this story sends |

`interaction` is **not** a table of this contract: rwb-source-data owns it, its trigger, its indexes and its `case_seq` (DP-01, DP-18), and it is reached only through 12.2. Its column shapes are the owner's too: the legacy migration makes the ledger columns required while TSD P3 v3 lists them optional, which is decided with that table and not here (GAP-2254; ASM-3712). No foreign key crosses a schema and no statement of this service names `rwb_source_data.interaction`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| `RWB-P1-E1066-CON` fake | `POST /api/recovery/source-data/v1/interactions` | 201 with an entry and `caseSeq` 7, then 8; the stored entry and the same `caseSeq` on a replay of one key; 409 for a replay with a different body; 422 for a missing event code; 404 for the unknown case; 503 and a delayed answer beyond 2 s |
| `rwb_case` fixture | This service's own test data | Case `RW-2026-000201` with its owner `u-owner-02`, the case of the 6-entry background, the unknown case ID of AC7, and one case whose local commit is forced to fail |
| Reference fixture | `rwb_case` reference rows | The values of LOV-LEDGER-EVENT with their Thai labels, and one value outside the list for AC5 |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | 1 operation (`POST /api/recovery/source-data/v1/interactions`) | One hop, 2 s, breaker, no retry with a new key (DP-11, DP-18) |
| Kafka | None | None | No event of its own; the decision record is published by the library (DP-03) |
| Temporal | 1 activity (`appendLedgerEntry`) | None | Queue `rwb-case`, namespace `rwb-recovery`, bounded retries, one key per action |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `ledger`, Java package `th.co.scb.ace.workbench.recovery.case.ledger`. Base `/api/recovery/case/v1` (no new operation), schema `rwb_case`, topic `rwb.case.events.v1` (not published here), task queue `rwb-case` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; the ledger stays in `rwb_source_data` and this service reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library; the entry carries `decisionLogId` and the record is published on `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data only through rwb-source-data; this story reads no ACE data | none |
| DP-07 | Reference data, LOV | Reference rows of rwb-case read in its own schema; no event code in code | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library present; this story publishes no event and writes no outbox row | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` for the service, `/api/recovery/source-data/v1` for the append | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_case` | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the screens arrive there | H RWB-PLT-N001-CON |

**Metadata build list.** The H rows of the table above are platform CON stories. The metadata row is `None` because those contracts are pulled by the `rwb-case` baseline stories and this story is Day 1 against `RWB-P1-E1066-CON` and its fake; no build dependency of this lane is missing.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CaseActionLedgerWriter` | Service | Event code, command, write order, link states, correction path |
| `InteractionLedgerClient` | Client | The append of 12.2: one hop, 2 s, breaker, four answers mapped to their messages |
| `LedgerEventCodeValidator` | Service | Reads LOV-LEDGER-EVENT from this service's reference rows (AC5) |
| `InteractionLinkRepository`, `InteractionLink` | Repository, entity | Inserts and moves the link row; no delete method and no rewrite of a `COMMITTED` entry reference |
| `LedgerIncidentHook` | Hook | Raises `LEDGER_WRITE_FAILED` with the case ID and the error class, never the summary |
| `CorrectionWriter` | Service | Appends one `CORRECTION` entry naming the original when the local commit fails after a 201 (AC8) |
| `AppendLedgerEntryActivity` | Temporal activity | The same path for the actions `CaseWorkflow` takes, keyed on the action reference (12.5) |

**Migration (DP-15).** One migration on this service's own sequence, after the baseline, creates `interaction_link` with its two unique keys and the index on `(case_id, created_at)`. The eight ledger columns of the legacy migration stay with the owner; nothing of `interaction` is created, altered or indexed here (DP-01, DP-18). An applied version is never edited.

**Configuration and reference data**

- **LOV-LEDGER-EVENT** as reference rows of `rwb_case`, with the version in force; no code holds a value (DP-07).
- The 2 s budget, the breaker and the bulkhead are client configuration; the activity's retry bounds are workflow configuration.
- The flag `rwb.case.ledger-write-through`: off, a case action that would raise an entry is refused rather than written without one, because a history with a gap is worse than a refused action (BR5).

**Build steps**

1. The migration for `interaction_link`, its keys and its index, with a repeated run that changes nothing.
2. `LedgerEventCodeValidator`, with MSG-GEN-001 naming the field and no link row on a refusal (AC5).
3. `CaseActionLedgerWriter` with one key per action reference and no second key on a retry (AC1, AC6).
4. `InteractionLedgerClient` against the fake: 201, the replay, 409, 422, 404, 503 and the delayed answer (AC1, AC4, AC7, X6 to X8).
5. The link states and the commit order, with the local commit forced to fail after the 201 (AC8).
6. `LedgerIncidentHook`, with a test that the detail carries the case ID and the error class and never the summary (AC4).
7. `AppendLedgerEntryActivity` on queue `rwb-case`, with a workflow test that a retry writes one entry (AC6).
8. An architecture test that no class outside `ledger` calls `InteractionLedgerClient`, and that nothing names `rwb_source_data` or `interaction`.

**Feature flag.** `rwb.case.ledger-write-through`, default on in SIT and off in PROD until the first wave is signed off; the legacy flag `rwb.dataengine.ledger-writer` is the ledger owner's and is not read here.

**Done when.** The tests of section 16 pass; a case action writes one entry and one `COMMITTED` link; a second action on the same case takes the next `caseSeq` from the owner and allocates nothing; a 503, a 422, a 404 and a read-only role each refuse the action and write nothing; a failed local commit after a 201 leaves one `CORRECTION` entry and no update; and no statement of the service reads or writes `interaction`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed, timed out or answered 409 for a replayed key | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing, or the event code is not in LOV-LEDGER-EVENT | Enter {field}. |
| MSG-P4-002 | Role without Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope | This case is not in your scope. |

Thai text for each message follows decision DL10. Every text is copied unchanged from the legacy story and the message catalogue; the field name of MSG-GEN-001 is filled from the validation failure and is never a data value, and {action} is the case action that was refused.

### 15. Screens and states

No screen in this story. A contact is recorded through the recording screens of RWB-P3-E2034-APP and the case record page of RWB-P3-E1018-APP, which arrive through gateway-bff (DP-19) and call this writer; the ledger entries are read through the read interface of rwb-source-data.

| Screen | State | What the user sees |
|---|---|---|
| Recording panel of the case record (RWB-P3-E2034-APP) | Saving | The action is held while the append answers inside 2 s |
| Recording panel of the case record (RWB-P3-E2034-APP) | Saved | The action is committed and its entry exists; the screen shows the entry on the next read |
| Recording panel of the case record (RWB-P3-E2034-APP) | Error | MSG-P1-022, MSG-GEN-001, MSG-P4-002 or MSG-P4-003, with the action not saved |

This story renders none of these states; it decides which of them is reachable.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-066-01 | AC1, BR2, BR3 | Contract | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 |
| TC-E1-066-02 | AC2, BR1, BR7 | Contract | 4 EFS entries, CASE_CREATED and CASE_ALLOCATED |
| TC-E1-066-03 | AC3, BR6 | Contract | Reassignment under R-UNI-18 version 2026.11 |
| TC-E1-066-04 | AC4, BR5 | End to end | Append forced to fail with 503 |
| TC-E1-066-05 | AC5 | Component | An event code outside LOV-LEDGER-EVENT |
| TC-E1-066-06 | AC6, BR7 | Contract | Two concurrent case actions on one case |
| TC-E1-066-07 | AC7 | Component | Unknown case ID |
| TC-E1-066-08 | AC8, BR4 | Contract | 201 answered, local commit forced to fail, CORRECTION entry naming case_seq 3 |
| TC-E1-066-09 | AC9 | Component | RW-AUDIT takes a case action; refused with MSG-P4-002 |

The legacy test case IDs, Covers and Data are kept in order and character for character; the legacy level "System" is realised as Contract where the assertion runs against the P1 fake, as Component where it runs inside `rwb_case`, and as End to end for the refused action of AC4, and "Access" maps to Component. No `-ITG` copy is minted here: `RWB-ITG-E1066-ITG` proves the same facts against the live contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: event codes, channels, directions, results, actor types and source values are list rows read from this service's reference data, and the append budget and the retry bounds are configuration (BR2, DP-07).
- No personal data in logs, events, prompts or the link table: the link carries codes, identifiers and a case sequence only; the summary, the contact result and the promise amount are sent to the ledger and never logged, never copied and never put in an incident detail, which names the case ID and the error class (BR1, BR3).
- No read of another service's tables and no second history: `interaction` and its trigger belong to `rwb_source_data`; this service writes only `interaction_link` in `rwb_case`, and no ACE view is read here (BR8, DP-01, DP-18).
- No entry is ever updated, deleted or rewritten by application code: the only repair is a `CORRECTION` append naming the original, and the repository has no delete method (BR4).
- One hop, 2 s, breaker per downstream, no chaining and no retry with a new key: a retry keeps the action's key so the ledger answers with the stored entry (BR9, DP-11).
- The append is asked before the case action commits; a refusal leaves no half-written action and no orphan link in `COMMITTED` (BR5).
- One schema, one login and one sequence: the release migrates `rwb_case` only, and an applied migration version is never edited (DP-02, DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-02 | All recovery processes | R-UNI-24 | TC-E1-066-02, TC-E1-066-06, TC-E1-066-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01, TC-E1-066-03, TC-E1-066-05, TC-E1-066-07 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry discarded | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-05 | All recovery processes | CTL-06 | TC-E1-066-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-CON | Contract | C contract dependency: the append this story consumes, its `InteractionRequest` and `Interaction` schemas, its four answers and its fake |
| RWB-P1-E1066-APP | App development | Owning slice of this legacy key: the writer, the ledger table, its allocator and its trigger in `rwb_source_data` (DP-18) |
| RWB-P1-E1067-APP, RWB-P1-E1068-APP | App development | Siblings: the outbox path into the ledger and the read interface; neither is built here |
| RWB-P3-E2034-APP, RWB-P3-E1018-APP | App development | Consumers: the recording panel and the case record that call this writer, and the timeline item that shows the entry |
| RWB-ITG-E1066-ITG | Integration | Proves the same nine facts against the live ledger and the live case service |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | The platform rows of the DP table, pulled by the `rwb-case` baseline: the decision-record library, the reference-data rows, the outbox and inbox library, the Flyway sequence and the gateway-bff route |

The BRD, FSD and TSD baselines read for this story are used as the current set with no approval record available in the read set, so the story stays Draft (realignment v1) (ASM-3715).

### 19. Out of scope

- The interaction ledger, its table, its eight ledger columns, its append-only trigger, its `case_seq` allocator and its indexes (RWB-P1-E1066-APP, RWB-P1-E1066-OPS; DP-01, DP-18).
- The append contract itself, its schemas, its error envelope and the exact resource path (RWB-P1-E1066-CON; GAP-0505; ASM-0697).
- The event paths that turn a Workbench event into an entry, and the duplicate rule across them (RWB-P1-E1067-APP).
- The ledger read interface, its filters and its paging (RWB-P1-E1068-APP), and the timeline item that composes it (RWB-P3-E2034-APP).
- The recording screens, their states and their field-level behaviour (RWB-P3-E2034-APP, RWB-P3-E1018-APP); this story decides only which state is reachable.
- The case actions themselves — creation, allocation, transfer, escalation, the decision and its authority (RWB-P3-E1018-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E2043-APP); this story serves them.
- The decision log, its entries, its rules and its versions (rwb-decision; RWB-P7-E1027-CON).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034 in the legacy set and RWB-P3-E2034-APP).
- The retention class of an entry (FEAT-ILG-10); this story writes no class and resolves none.
- The cross-service proof of the nine facts and the live-ledger run (RWB-ITG-E1066-ITG).
