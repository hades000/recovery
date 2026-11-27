# RWB-ITG-E1066-ITG Interaction ledger store and writer — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1066-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized; the squad sizes it at refinement (DOR-RWB-ITG-E1066-ITG-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None (the three integration dependencies RWB-P3-E1018-APP, RWB-P1-E1066-APP and RWB-P3-E1066-APP are not build blockers; Template and Rules §R5.4) |
| Contract dependencies | RWB-P1-E1066-CON |
| Contract version | v1 (base paths /api/recovery/source-data/v1 and /api/recovery/case/v1); exact contract version Not specified in the source documents (DOR-RWB-ITG-E1066-ITG-23) |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P1-E1066-APP, RWB-P3-E1066-APP |
| External dependencies | None |
| Open decisions | DL10 is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-066 is split and reworked as the wave-1 integration story RWB-ITG-E1066-ITG. In the monolith the ledger, the `InteractionLedgerWriter` and the `POST /cases/{caseId}/interactions` endpoint sat in one deployable, with the P3 handler calling a published interface in the caller's transaction. Under the R-PREC default ruling and DP-18 the ledger and both interaction operations belong to P1 rwb-source-data in schema `rwb_source_data`, and P3 rwb-case keeps the case record, the case scope and the timeline and reads the ledger through P1's contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-ITG-E1066-ITG-L176, X20 RWB-ITG-E1066-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the interaction ledger proved end to end on the real wave-1 services — P3 rwb-case committing the case action and serving the case timeline `GET /api/recovery/case/v1/cases/{caseId}/timeline`, P1 rwb-source-data appending the entry through `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` and reading it back through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`, and P7 rwb-decision holding the central decision log entry that a decision entry links to**, so that **the history of a case is written where it is owned and read by every other service through a contract, and the crossing between the two services is proved before wave 1 exits rather than assumed**.

### 2. Business rationale

Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

The target moves the store and the writer out of the monolith. The interaction ledger and both interaction operations belong to P1 rwb-source-data (R-PREC default ruling, DP-18; the Ownership Map ruling on `interaction` and on `POST` and `GET /cases/{caseId}/interactions`), in schema `rwb_source_data`, on base `/api/recovery/source-data/v1` (DP-01, DP-13). The write is one hop from gateway-bff to P1 with a 2 s timeout (DP-11, DP-19); the schema arrives through P1's own Flyway sequence (DP-15); the local decision record and the outbox and inbox library carry the decision link to the central ledger in P7 rwb-decision (DP-03, DP-09); the LOV-LEDGER-EVENT values are read through the reference-data contract of rwb-case (DP-07); and no service but P1 reads an ACE view, so the EFS history entries on the ledger come through P1 alone (DP-05).

P3 rwb-case keeps the case record, the case scope and the case timeline. The timeline `GET /api/recovery/case/v1/cases/{caseId}/timeline` is composed from P1's interaction contract and P3's own case fields; schema `rwb_case` holds no interaction table and no copy of an entry. That leaves one behaviour that no single service story can prove: a P3 case action and a P1 ledger entry form one business transaction, and a P1 failure must not leave the P3 action committed. The sources do not name the mechanism that closes the gap, so this story asserts the outcome — the action is rolled back or compensated and the case shows its previous state — and records the open point as Not specified in the source documents (GAP-0375; ASM-0539).

The measure is unchanged from the legacy story: every contact, letter, promise, payment and hand-over on a case is on the ledger when it is recorded, and a failed write stops the action and raises incident LEDGER_WRITE_FAILED (REQ-ILG-008; CTL-06). The story meets REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008 and supports NFR-070 and NFR-077. It ends the history that is assembled after the fact, because the ledger of a case is one owned, ordered and append-only sequence that every other service reads through its owner.

### 3. Preconditions

- RWB-P3-E1018-APP is done: `recovery_case` exists in schema `rwb_case` with case numbers RW-YYYY-NNNNNN, the case scope is applied, and `GET /api/recovery/case/v1/cases/{caseId}` answers from it.
- RWB-P1-E1066-APP is done: `interaction` is written and read in schema `rwb_source_data`, `POST` and `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` are published on base `/api/recovery/source-data/v1`, the case lock and the case_seq assignment work, the required-value validation answers MSG-GEN-001, and a failed write raises incident LEDGER_WRITE_FAILED with MSG-P1-022.
- RWB-P3-E1066-APP is done: `GET /api/recovery/case/v1/cases/{caseId}/timeline` composes the case timeline from P1's interaction contract and P3's case fields, and schema `rwb_case` holds no interaction table and no stored copy of an entry.
- Schema `rwb_source_data` is migrated by the P1 Flyway sequence (DP-15) with the columns of DF-INT-001 to DF-INT-021, the unique keys on (case_id, case_seq) and on (idempotency_key), the append-only trigger `tr_interaction_append_only` (a database trigger recorded in Recovery Workbench Physical Schema v7.sql, not an LDM field), and the P1 login holding INSERT and SELECT with no UPDATE or DELETE grant (DP-01, DP-02).
- The DP-03 and DP-09 library objects `decision_record` (a DP-03 library table, not an LDM field or entity), `outbox_event` and `processed_event` exist in schema `rwb_source_data`, and the outbox relay publishes `DecisionRecorded` on the shared topic `rwb.decision-record.v1` (RWB-PLT-E1027-CON, RWB-PLT-TE006-CON).
- P7 rwb-decision holds `decision_log_entry`, ingests the shared topic idempotently through its inbox, and answers `GET /api/recovery/decision/v1/decision-log/{entryId}` (RWB-P7-E1008-APP).
- The list LOV-LEDGER-EVENT is in force with the values CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN and CORRECTION, read as data rows through the reference-data contract of rwb-case (DP-07).
- The gateway-bff route for the case screens is deployed in SIT, with the 2 s per-call budget and no call chain deeper than one (DP-19, RWB-PLT-N001-CON).
- The harness RWB-ITG-W1J01-ITG is available with its synthetic data set: case "RW-2026-000201" with its six ledger entries, user "u-owner-02" as its owner, approver "u-teammgr-01", rule "R-UNI-18" version "2026.11", and the four EFS history entries, the CASE_CREATED and the CASE_ALLOCATED entry.
- The mechanism that keeps the P3 case action and the P1 ledger entry in one business transaction — and the record of a compensated action — is Not specified in the source documents (GAP-0375; ASM-0539). The suite therefore asserts the committed or compensated state of the case, not the mechanism.
- Every service called by the suite is the real SIT service behind its own login; no contract fake stands in for a service.
- No production data is used and no production connection is opened. The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1 (Template and Rules §R5.7).

### 4. Flow

1. QA integration engineer: runs the preflight of section 13 — the two P1 interaction operations on base `/api/recovery/source-data/v1`, the P3 case read and timeline path, the P3 statement log, the append-only trigger, the local record objects, the shared topic and the P7 decision-log read. A missing element stops the run before any test.
2. Harness: seeds the synthetic data set of RWB-ITG-W1J01-ITG — case "RW-2026-000201" with its six entries, "u-owner-02" as the owner, "u-teammgr-01" as the approver, and the LOV-LEDGER-EVENT values read as data rows through the reference-data contract of rwb-case (DP-07).
3. Case owner: records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15, through `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` on the gateway-bff route, with an Idempotency-Key, channel CALL, direction OUTBOUND and source system WORKBENCH.
4. P3 rwb-case: commits the case action the call belongs to — the promise and the last contact of case "RW-2026-000201" — as the case side of the same business transaction, and calls no table of schema `rwb_source_data` (DP-01, DP-18).
5. P1 rwb-source-data: validates the command against LOV-LEDGER-EVENT, takes the transaction-level advisory lock on the case ID, assigns case_seq 7 as the case's highest case_seq plus 1, and inserts the entry with event code, actor "u-owner-02", source system "WORKBENCH", channel "CALL", direction "OUTBOUND" and the promise fields, and answers 201 with the entry.
6. P1 rwb-source-data: writes one local `decision_record` row naming the entry and one `outbox_event` row in the same transaction (DP-03, DP-09); the relay publishes `DecisionRecorded` on `rwb.decision-record.v1`, and P7 rwb-decision records the event id in its inbox and appends one `decision_log_entry`.
7. Harness: reads `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` and asserts the sequence of case_seq 1 to 7 with no gap and the fields of the call; reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case action is committed on the case.
8. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}/timeline` and compares the timeline entry with the ledger entry on entry ID, case_seq 7, occurred time 2026-12-02T10:15+07:00, event "CONTACT" and actor "u-owner-02"; then reads the P3 statement log and asserts no statement of the timeline read touches schema `rwb_source_data`.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log/{entryId}` and asserts that the decision entry of the reassignment holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver "u-teammgr-01", while the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID with no rule, version or inputs.
10. Harness: asserts the ordered history — the four EFS history entries from 2026-08-03 to 2026-11-28, the CASE_CREATED entry and the CASE_ALLOCATED entry of 2026-12-01 — read through P1 only, in one sequence by occurred time with case_seq 1 to 6 (DP-05).
11. Harness: forces the ledger insert to fail with a database error through the agreed test-only fault hook, repeats a call with an Idempotency-Key, records the 503 with MSG-P1-022, the unchanged entries, the absent contact in P1 and the absent timeline entry, the incident LEDGER_WRITE_FAILED, and the compensated case action of that call read through `GET /api/recovery/case/v1/cases/{caseId}`; it restores the hook and sends the same call again with the same key, and asserts exactly one entry.
12. Harness: issues an UPDATE and a DELETE on entry case_seq 3 and asserts both are refused, then writes a correction as a new entry with event "CORRECTION" naming entry case_seq 3.
13. Harness: writes the evidence report — per scenario the entry ID, the case_seq, the timeline entry, the statuses, the messages, the incident and the call latencies — restores every fixture, and confirms the fault hook and the append-only trigger are back in place.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ledger cannot be written inside P1's transaction | The P1 transaction rolls back, no entry and no contact are saved, the caller receives 503, incident LEDGER_WRITE_FAILED is raised, and the P3 timeline holds no entry for the call | MSG-P1-022 | AC4, AC9 |
| X2 | A required value is missing (event code, occurred time, actor) | 422; nothing written | MSG-GEN-001 | AC13 |
| X3 | Two entries for one case at the same moment | Both written with consecutive case_seq under the case lock; no gap and no repeat | None | AC14 |
| X4 | A call names a case that does not exist or is out of scope, for example case ID "00000000-0000-0000-0000-000000000999" | 404; nothing written | MSG-P4-003 | AC15 |
| X5 | Any change or delete of an entry | Refused by the append-only trigger; a correction is a new entry naming the original | None | AC8 |
| X6 | P1 answers 503 after P3 has prepared the case action of the call | P3 rolls the action back or compensates it, the case read shows the state before the call, and no timeline entry appears | MSG-P1-022 | AC9 |
| X7 | The timeline disagrees with the ledger, or P3 reads schema `rwb_source_data` directly | The run fails and names the entry ID, the two values and the offending statement | None | AC10 |
| X8 | A call is a chain rather than one hop, or exceeds the 2 s budget | The run fails and names the call, the services on the path and the latency | None | AC1, AC4, AC10 |
| X9 | The fixture set does not match the harness expectations, or the fault hook cannot be reached | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC2 |

X1 and X5 are the legacy exception paths carried onto the real services; X2 to X4 are carried with their owners; X6 to X9 are the cross-service paths that appear only once the ledger lives in P1 and the timeline reads it through the contract.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P1, P3 and P7, not their source code |
| Negotiable | The fixture size, the retry count, the wait intervals and the report layout are configuration; the case, the users, the rule, the values and the messages are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one owned entry, one order, one timeline agreement, one entry after a retry and no committed action without its entry |
| Estimable | One suite module, one fixture pack, one fault hook, one statement-log assertion and one evidence report |
| Small | Can be finished in two weeks or less: thirteen scenarios over three services and one shared topic; no service code and no schema change |
| Testable | Every criterion asserts a row, a response, a timeline entry, a status, a message, an incident or a recorded statement |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer, end-to-end across the wave 1 services

  Background:
    Given case "RW-2026-000201" exists with 6 ledger entries, case_seq 1 to 6
    Given user "u-owner-02" holds RW-CASEOWN and owns case "RW-2026-000201"
    Given the wave 1 services rwb-source-data, rwb-case and rwb-decision are deployed in SIT with their published contracts behind gateway-bff and no production data is used

  Scenario: AC1 The ledger exists and is written to (legacy RWB-E1-066 AC1)
    Given the case owner records an outbound call through POST /api/recovery/source-data/v1/cases/{caseId}/interactions on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15
    When the action completes
    Then the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND"
    Then the entry carries promise amount 25,000.00 and promise date 2026-12-15
    Then the entry names source system "WORKBENCH"

  Scenario: AC2 It is ordered and complete (legacy RWB-E1-066 AC2)
    Given case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01
    When the ledger is read
    Then the 6 entries are in one sequence ordered by occurred time
    Then case_seq runs 1 to 6 with no gap

  Scenario: AC3 It is distinct from the decision log (legacy RWB-E1-066 AC3)
    Given owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01"
    When both are read
    Then the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver
    Then the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs

  Scenario: AC4 A write failure is visible (legacy RWB-E1-066 AC4)
    Given the ledger insert fails with a database error
    When the case owner records a call on case "RW-2026-000201"
    Then the system refuses the call with status 503 and MSG-P1-022
    Then the ledger still holds 6 entries and no contact is saved
    Then the system raises an incident "LEDGER_WRITE_FAILED" with case "RW-2026-000201"

  Scenario: AC8 An entry cannot be changed (legacy RWB-E1-066 AC8)
    Given ledger entry case_seq 3 of case "RW-2026-000201"
    When any process issues an UPDATE or DELETE on it
    Then the database refuses the statement
    Then the system writes a correction as a new entry with event "CORRECTION" naming entry case_seq 3

  Scenario: AC9 The P3 case action and the P1 ledger entry are one business transaction, and a P1 failure leaves no committed action (new, D-RCV-60)
    Given case "RW-2026-000201" is owned by "u-owner-02" and holds 6 ledger entries, case_seq 1 to 6
    Given P3 rwb-case commits the case action of a call as the case side of the same business transaction as the ledger entry
    When the case owner records an outbound call through POST /api/recovery/source-data/v1/cases/{caseId}/interactions and P1 rwb-source-data answers 201
    Then the ledger holds entry case_seq 7 for the call
    Then GET /api/recovery/case/v1/cases/{caseId} shows the promise of 25,000.00 for 2026-12-15 on case "RW-2026-000201"
    When the ledger insert of a second call fails with a database error and P1 answers 503 with MSG-P1-022
    Then the ledger still holds 7 entries and no contact of the second call is saved
    Then the case action of the second call is rolled back or compensated, and GET /api/recovery/case/v1/cases/{caseId} shows the case as it stood after the first call, with no promise of the second
    Then the timeline of case "RW-2026-000201" holds no entry for the second call
    Then the system raises an incident "LEDGER_WRITE_FAILED" with case "RW-2026-000201"

  Scenario: AC10 The P3 timeline shows the same entry through the P1 contract and rwb-case holds no copy (new, D-RCV-60)
    Given case "RW-2026-000201" holds entry case_seq 7 appended by P1 rwb-source-data for the outbound call of 2026-12-02 at 10:15
    When the case owner reads GET /api/recovery/case/v1/cases/{caseId}/timeline through gateway-bff
    Then the timeline shows the entry with the same entry ID and case_seq 7, occurred 2026-12-02T10:15+07:00, event "CONTACT" and actor "u-owner-02"
    Then P3 answers the timeline through GET /api/recovery/source-data/v1/cases/{caseId}/interactions, one hop with a 2 s timeout
    Then the statement log of the timeline read holds no statement on schema rwb_source_data
    Then schema rwb_case holds no interaction table and no column that stores a copy of an entry

  Scenario: AC11 Each append writes one local decision record and one outbox row in the same transaction, and the central effect is one entry (new, D-RCV-60)
    When the case owner records an outbound call on case "RW-2026-000201" through POST /api/recovery/source-data/v1/cases/{caseId}/interactions
    Then P1 rwb-source-data writes one local decision record naming the new entry and one outbox row in the same transaction in schema rwb_source_data
    Then the relay publishes DecisionRecorded once on topic rwb.decision-record.v1
    Then rwb-decision holds exactly one decision log entry for the event ID of that call

  Scenario: AC12 Event and LOV values come through the rwb-case reference-data contract, and only P1 reads the EFS history (new, D-RCV-60)
    When P1 rwb-source-data reads the LOV-LEDGER-EVENT values for case "RW-2026-000201"
    Then the event and LOV values are read through the reference-data contract of rwb-case and no ACE view is read
    Then no service other than P1 rwb-source-data reads an ACE view, and the 4 EFS history entries of case "RW-2026-000201" reach the ledger through P1 alone

  Scenario: AC13 A call with a required value missing is refused with 422 and nothing is written (new, D-RCV-60)
    Given case "RW-2026-000201" holds 6 ledger entries, case_seq 1 to 6
    When the case owner records an outbound call on case "RW-2026-000201" through POST /api/recovery/source-data/v1/cases/{caseId}/interactions with one required value missing (event code, occurred time or actor)
    Then the system refuses the call with status 422 and MSG-GEN-001
    Then nothing is written to the ledger and the ledger still holds 6 entries

  Scenario: AC14 Two entries for one case at the same moment are both written with consecutive case_seq (new, D-RCV-60)
    Given case "RW-2026-000201" holds 6 ledger entries, case_seq 1 to 6
    When two calls are recorded on case "RW-2026-000201" at the same occurred time
    Then both entries are written under the case lock
    Then the two entries carry consecutive case_seq values with no gap and no repeat

  Scenario: AC15 A call that names a case that does not exist or is out of scope is refused with 404 (new, D-RCV-60)
    Given case "RW-2026-000201" holds 6 ledger entries, case_seq 1 to 6
    When the case owner records an outbound call through POST /api/recovery/source-data/v1/cases/00000000-0000-0000-0000-000000000999/interactions
    Then the system refuses the call with status 404 and MSG-P4-003
    Then nothing is written to the ledger

  Scenario: AC16 A status change the model does not allow is refused and writes no entry (new, D-RCV-60)
    Given ledger entry case_seq 3 of case "RW-2026-000201" exists
    When a status change that the model does not allow is requested for case "RW-2026-000201"
    Then the system refuses the change with the message Not specified in the source documents (NEWAC-RWB-ITG-E1066-ITG-AC15) and writes no entry
```

AC9 to AC16 are new. AC9 and AC10 carry the cross-service part the monolith never had: the one business transaction across P3 and P1 with its compensation, and the timeline that reads the ledger through the owner's contract without holding a copy. AC11 and AC12 cover BR11 and BR12, AC13 to AC15 cover exception paths X2 to X4, and AC16 covers a disallowed status change. The five legacy criteria are carried verbatim in substance, with only the monolith names adapted to the target operation, schema and owner. AC5, AC6 and AC7 are owned by RWB-P1-E1066-APP and are not written in this story's Gherkin; their behaviour is re-exercised here as exception paths X2 to X4 through AC13, AC14 and AC15.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ledger holds every interaction on a case; no other record is the authoritative history | REQ-ILG-001; case file item "Interaction ledger" (casemodel.txt) |
| BR2 | Every entry carries case, event, time, actor and source | REQ-ILG-002 |
| BR3 | An offer, promise, payment or hand-over is recorded on the interaction it was made in | REQ-ILG-004; interaction.promise_amount |
| BR4 | Entries are append only; a correction is a new entry naming the original | tr_interaction_append_only (Recovery Workbench Physical Schema v7.sql); R-UNI-24 |
| BR5 | A ledger write that fails stops the action and raises an incident; no entry is discarded | REQ-ILG-008; CTL-06 |
| BR6 | The ledger records what happened; the decision log records why; a decision entry links the two | FEAT-ILG-02; ADR-009 |
| BR7 | Entries of one case carry a gap-free sequence | REQ-ILG-001; interaction.case_seq |
| BR8 | The ledger and both interaction operations belong to P1 rwb-source-data in schema `rwb_source_data`; P3 rwb-case keeps the case record, the case scope and the timeline and holds no copy of an entry | DP-18; DP-01; R-PREC default ruling; Ownership Map v1 |
| BR9 | The P3 case action and the P1 ledger entry are one business transaction: a P1 503 never leaves the P3 action committed, and no distributed transaction is used to achieve it | RWB-E1-066 AC4; Arch v5 slide 11 (Idempotency-Key on every POST); ASM-0539 |
| BR10 | The write is one REST hop from gateway-bff to the owner within a 2 s budget, every POST carries an Idempotency-Key, and a repeat returns the first entry | ADR-020; DP-11; DP-19; Arch v5 slide 11 |
| BR11 | Each append writes one local decision record and one outbox row in the same transaction in `rwb_source_data`, and the consumer inbox makes the central effect exactly one entry | DP-03; DP-09; Arch v5 slides 20 and 28 |
| BR12 | The event and LOV values are reference data read through the contract of rwb-case; no service but P1 reads an ACE view, and the EFS history entries reach the ledger through P1 alone | DP-07; DP-05; R-PREC default ruling |

### 9. State transitions

None for a case status: the story changes no case status of its own and asserts the states below.

| Object | State | Meaning |
|---|---|---|
| `interaction` entry in `rwb_source_data` | Appended | Written by P1 in the caller's transaction; it has no status, is never updated and is never deleted |
| Correction | Correction of an entry | A new entry with `corrects_entry_id` naming the corrected entry; the corrected entry keeps its own record |
| P3 case action | Committed | The case side of the business transaction is on the case record, for example the promise and the last contact of the call |
| P3 case action | Rolled back or compensated | The P1 append answered 503; the case read shows the state before the call and no timeline entry exists |
| Local decision record | Committed with the entry | Present only with the entry, chained to the previous record, never alone |
| Central `decision_log_entry` | Ingested once | Appended to the central chain in P7, deduplicated by the P7 inbox |
| P3 timeline | Derived | Composed by P3 from its own case fields and P1's interaction contract; it holds no state of its own in `rwb_case` |
| Suite run | Not started, running, passed, failed | A failed run names the criterion, the service, the entry ID and the evidence |

The compensation state of the case action is read through `GET /api/recovery/case/v1/cases/{caseId}`; the suite changes none of these states directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| rwb-source-data service identity (the P1 login, DP-02) | Validates and appends entries, assigns case_seq, writes the local decision record and the outbox row, owns schema `rwb_source_data` |
| rwb-case service identity (the P3 login, DP-02) | Commits or compensates the case action, serves the case read and the timeline, calls P1's interaction contract, holds no copy of an entry |
| rwb-decision service identity (the P7 login, DP-02) | Ingests `DecisionRecorded` into the central ledger and serves the decision-log read |
| gateway-bff, platform edge | Owns the route, the 2 s per-call budget and the session check |
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) and reads the timeline of own cases |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries and the timeline in this story (Case record R); they record nothing here |
| RW-AUDIT Internal audit | Reads entries and the timeline only; may not record |
| RW-PLATADM Platform administrator | Receives the LEDGER_WRITE_FAILED incident |
| No role | May update or delete an entry; no role may read schema `rwb_source_data` through another service |

No approval level from the delegation of authority applies: the story takes no business decision of its own.

### 11. Data

| BR Field ID | Entity | Field | Read or write | Where it lives |
|---|---|---|---|---|
| DF-INT-001 to DF-INT-013 | `interaction` | all fields | Write by P1; read through P1 | rwb_source_data |
| DF-INT-014 | `interaction` | event_code | Write by P1; read through P1 | rwb_source_data |
| DF-INT-015, DF-INT-016 | `interaction` | actor_type, actor_ref | Write by P1; read through P1 | rwb_source_data |
| DF-INT-017 | `interaction` | source_ref | Write by P1; read through P1 | rwb_source_data |
| DF-INT-018 | `interaction` | idempotency_key | Write by P1; read through P1 | rwb_source_data |
| DF-INT-019 | `interaction` | case_seq | Write by P1; read through P1 | rwb_source_data |
| DF-INT-020 | `interaction` | decision_log_id | Write by P1; read through P7 | rwb_source_data |
| DF-INT-021 | `interaction` | corrects_entry_id | Write by P1; read through P1 | rwb_source_data |
| DF-CAS-001 | `recovery_case` | id | Read through P3 | rwb_case |
| DF-CAS-009 | `recovery_case` | owner_user_id | Read through P3 (the committed or compensated case action) | rwb_case |
| DF-DEC-001 | `decision_log_entry` | id | Read through P7 | rwb_decision |
| DF-DEC-003 | `decision_log_entry` | decision_code | Read through P7 | rwb_decision |
| DF-DEC-004 | `decision_log_entry` | rule_id | Read through P7 | rwb_decision |
| DF-DEC-005 | `decision_log_entry` | rule_version | Read through P7 | rwb_decision |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Read through P7 | rwb_decision |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Read through P7 | rwb_decision |
| Compensation record of the P3 case action | `interaction_link` | state `REFUSED` of the action's link row (GAP-2255; ASM-0539) | Written by P3; the suite reads the outcome through the P3 case read | rwb_case |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-066. The append-only trigger `tr_interaction_append_only` (recorded in Recovery Workbench Physical Schema v7.sql) and the library table `decision_record` (DP-03) are not LDM fields or entities and have no row in this table. The legacy story writes `interaction` in the monolith and reads `decision_log_entry` in process; in the target the entry is written and read by P1 in schema `rwb_source_data`, the case state is P3's, and the central entry is P7's. The suite owns no schema, no table and no field: it writes only through P1's contract and reads the three owners through their contracts.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Base | Use in the suite |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | `/api/recovery/source-data/v1` | The one-hop ledger write of the call, with an Idempotency-Key (AC1, AC4, AC9) |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | `/api/recovery/source-data/v1` | The entries of one case in case_seq order (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | `/api/recovery/case/v1` | The case record and the committed or compensated case action (AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | `/api/recovery/case/v1` | The timeline that shows the entry without holding a copy (AC10) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | `/api/recovery/decision/v1` | The central decision entry the ledger entry links to (AC3, AC9) |

Every call is one hop to the owning service on its own base with a 2 s budget (DP-11, DP-13); the browser reaches the services only through gateway-bff (DP-19). The interaction write follows the contract RWB-P1-E1066-CON (GAP-0375, GAP-0504, GAP-0505; ASM-0538). The append path is `/cases/{caseId}/interactions` on the rwb-source-data base, called under the `rwb_source_data` login (DP-02), with `InteractionRequest` in, `Interaction` out, property names from the API specification and a required `Idempotency-Key` header. P1 writes the entry, its local decision record and its outbox row in one transaction in `rwb_source_data` and answers 201 with the entry identifier and caseSeq. A repeat with the same key and body returns the stored entry with the same caseSeq and writes no second row; the same key with a different body answers 409; a missing key answers 400 with MSG-GEN-004. A missing required value answers 422 with MSG-GEN-001, a missing Case record C right 403 with MSG-P4-002, an unknown or out-of-scope case 404 with MSG-P4-003, and a failed write 503 with MSG-P1-022. The required flags of the ledger values are those of the contract, settled at its baseline review. The caller treats any non-2xx answer as a failed action and never keeps an action without its entry. rwb-case records each case action in its link table `interaction_link` (RWB-P3-E1066-APP): `PENDING` before the append, `COMMITTED` after 201, and `REFUSED` when the action is not applied.

#### 12.3 Events published

None. The suite publishes no business event. The `DecisionRecorded` event asserted in AC9 and AC3 is produced by P1 rwb-source-data through its outbox relay and is named in 12.4.

#### 12.4 Events consumed

None by the suite. DP-09, the outbox and inbox library, sits on the owning APP stories — RWB-P1-E1066-APP produces `DecisionRecorded` on `rwb.decision-record.v1`, and RWB-P7-E1008-APP consumes it into the central ledger; this story asserts the effect through the decision-log read of 12.2 and consumes no event itself.

#### 12.5 Workflows and activities

None. No workflow, activity or Nexus operation is started or awaited by this story; the write and the reads are synchronous REST calls (Arch v5 slide 12, question 1).

#### 12.6 Schedules

None. No Schedule is started, moved or waited for. The outbox relay of P1 is the every-minute sender JOB-11 of the owning service (Arch v5 slide 44), and this story only observes its effect.

#### 12.7 Tables owned

None. The suite owns no table and writes no schema of its own (DP-01). The tables it exercises are `interaction`, `decision_record`, `outbox_event` and `processed_event` in schema `rwb_source_data` (P1); `recovery_case` and `interaction_link` in schema `rwb_case` (P3; `interaction_link` holds one row per case action with case ID, action reference, event code, entry identifier, `case_seq`, decision log reference, key, state and timestamps, unique on the action reference and on the key, with one key derived per action reference and the append made before the local commit of the action); and `decision_log_entry` with its inbox in schema `rwb_decision` (P7). It reads and writes them only through their owners.

#### 12.8 Contract fakes

None. The suite runs against the deployed SIT services and their published contracts. The bank systems behind the ACE views are outside the bank's service contracts and are read by P1 alone through the `recovery.v_ace_*` views (DP-05); no service contract is faked, because the point of the story is that the real cross-service behaviour is proved (Template and Rules §R5.4 class I), so no published fake of rwb-case, rwb-decision or rwb-source-data is needed (DOR-RWB-ITG-E1066-ITG-22). The only intervention in a running service is the agreed test-only fault hook of AC4 and AC9 on the P1 insert, and it is switched off in UAT and production.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 5: the two P1 interaction operations, the P3 case read, the P3 timeline read and the P7 decision-log read, each one hop with a 2 s budget |
| Kafka | 0 | 0; the `DecisionRecorded` effect is asserted through the decision-log read |
| Temporal | 0 | 0 |
| File | 0 | 0 |

### 13. Solution plan

**Deliverables.** One suite module `integration/recovery-w1/interaction-ledger`, next to the harness RWB-ITG-W1J01-ITG, with the test classes `LedgerWriteIT`, `LedgerOrderIT`, `DecisionDistinctionIT`, `TimelineAgreementIT` and `CaseTransactionIT`, the fixture files and the evidence report writer. The module holds no service code and is not part of a deployed service. It owns no schema: `rwb_source_data` belongs to P1 rwb-source-data, `rwb_case` to P3 rwb-case and `rwb_decision` to P7 rwb-decision.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Runner | Preflight, run order, evidence report and exit code |
| PreflightProbe | Service | Checks the two P1 interaction operations, the P3 case read and timeline path, the P3 statement log, the append-only trigger, the local record objects, the shared topic and the P7 decision-log read before any test |
| LedgerWriter | Service | Calls the P1 write with an Idempotency-Key, channel CALL, direction OUTBOUND, result RIGHT_PARTY and the promise of 25,000.00 for 2026-12-15, and asserts 201 and the entry |
| LedgerReader | Service | Reads the case entries through P1 and asserts the order, case_seq 1 to 7 and the gap-free sequence |
| CaseReader | Service | Reads the case through P3 and asserts the committed or the compensated case action (AC9) |
| TimelineReader | Service | Reads the P3 timeline and compares entry ID, case_seq, occurred time, event code and actor with the ledger |
| SchemaBoundaryProbe | Service | Reads the P3 statement log and asserts no statement on schema `rwb_source_data`, and no interaction table or copy column in `rwb_case` |
| DecisionReader | Service | Reads the central entry through P7 and asserts decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver |
| FailureInjector | Service | Forces the P1 insert to fail through the agreed test-only fault hook, restores it in the same run, and repeats the call with the same Idempotency-Key |
| AppendOnlyProbe | Service | Issues the UPDATE and the DELETE on entry case_seq 3 and writes the CORRECTION entry naming it |
| EvidenceReport | Report | Per scenario the entry ID, the case_seq, the timeline entry, the statuses, the messages, the incident and the call latencies |

**Decoupling patterns applied (Template and Rules v1 §R5.5)**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | `interaction` and the library objects in `rwb_source_data`; the suite asserts through contracts only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | On RWB-P1-E1066-APP and RWB-P3-E1066-APP; the suite only reads the central entry through P7 |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | The four EFS history entries of AC2 come from the ACE EFS action view and are read by P1 alone; the suite asserts them through P1's contract |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | LOV-LEDGER-EVENT rows read as data through the P3 contract by P1 and by the fixtures |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On RWB-P1-E1066-APP for the local record and the outbox row; the suite asserts the central effect, not the envelope |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The interaction write and read and the timeline read of section 12.2; the legacy `append()` in the caller's transaction becomes a one-hop command |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path of section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P1-E1066-APP for `rwb_source_data` and its append-only trigger; the suite owns no schema |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none | The ledger and both interaction operations in P1; the P3 timeline reads them through P1's contract (AC9, AC10) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The browser reaches the interaction write and the case and timeline screens through gateway-bff only |

The dependency-added column records the build dependency of the owning story, exactly as §R5.5 states it. The H, C and X lists of this story are empty — the H dependencies of DP-03, DP-07, DP-09, DP-15 and DP-19 sit on the APP and platform stories that implement them, and the C dependency of DP-07 is published by P3 rwb-case. The three integration dependencies RWB-P3-E1018-APP, RWB-P1-E1066-APP and RWB-P3-E1066-APP are the only dependencies of this story, they are of class I, and an integration dependency never blocks a build (Template and Rules §R5.4).

**Build steps**

1. Create the suite module next to the harness RWB-ITG-W1J01-ITG and wire it to the SIT bases of P1, P3 and P7 through gateway-bff; the preflight fails the run when a fake endpoint is configured.
2. Build the fixture pack from the legacy values: case "RW-2026-000201", "u-owner-02", "u-teammgr-01", rule "R-UNI-18" version "2026.11", the promise of 25,000.00 for 2026-12-15, the four EFS entries, CASE_CREATED and CASE_ALLOCATED, and the LOV values read as data rows.
3. Implement AC1 and AC2: the one-hop write on `POST /api/recovery/source-data/v1/cases/{caseId}/interactions`, the entry of case_seq 7, and the ordered sequence 1 to 6 read through P1.
4. Implement AC3: the decision entry through `GET /api/recovery/decision/v1/decision-log/{entryId}` against the ledger entry of event "DECISION_TAKEN".
5. Implement AC8: the refused UPDATE and DELETE on entry case_seq 3 and the CORRECTION entry naming it.
6. Implement AC4 and AC9: the forced insert failure, the 503 with MSG-P1-022, the incident LEDGER_WRITE_FAILED, the compensated case action read through P3, and the retry with the same Idempotency-Key.
7. Implement AC10: the timeline read, the comparison with the ledger entry, and the statement-log and `rwb_case` boundary assertions.
8. Run the suite in SIT against the wave 1 release candidate, write the evidence report, and restore the fixtures, the fault hook and the trigger.

**Done when.** The seven test cases of section 16 pass in SIT against the published wave 1 contracts of P1, P3 and P7; a P1 503 leaves no committed case action and no timeline entry; the timeline agrees with the ledger and `rwb_case` holds no copy; and no service code or schema was changed by this story apart from the agreed test-only fault hook.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing, for example the field "event code" | Enter {field}. |
| MSG-P4-002 | Role without Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope, for example 404 for case ID "00000000-0000-0000-0000-000000000999" | This case is not in your scope. |

The four message IDs and their texts are copied unchanged from RWB-E1-066, and this story adds no message ID. Thai text for each message follows decision DL10. The suite's own report lines — the entry ID, the case_seq, the timeline values and the latencies — are for the integration record and are not part of the message standard.

### 15. Screens and states

No screen is built in this story. The screen the behaviour serves is the case record view SCR-03 with its ledger and timeline part, and it is not in scope here: the suite calls the interaction write, the case read, the timeline read and the decision-log read directly, and the browser reaches them through gateway-bff with the 2 s budget (DP-19). A failed write shows MSG-P1-022 in the error state of the screen; the timeline shows an entry only after P1 has appended it, and after a compensated action it shows nothing of the failed call. The screen build and its states belong to RWB-P3-E1066-APP and RWB-E1-068 (the ledger read view). SCR-03 states: empty, a case with no ledger entry shows the Empty state of the history panel (RWB-P1-E1068-APP) and no message; loading, as defined in Screen Specifications v1 SCR-03; error, a failed write shows MSG-P1-022 and the action is not saved; no access, MSG-P4-002 for a role without the Case record right and MSG-P4-003 for a case that is missing or out of scope (RWB-P1-E1066-CON).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-066-01-ITG | AC1, BR2, BR3 | Integration | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 for 2026-12-15 |
| TC-E1-066-02-ITG | AC2, BR1, BR7 | Integration | 4 EFS entries 2026-08-03 to 2026-11-28, CASE_CREATED and CASE_ALLOCATED on 2026-12-01 |
| TC-E1-066-03-ITG | AC3, BR6 | Integration | Reassignment under R-UNI-18 version 2026.11 by approver u-teammgr-01; decision code D6 |
| TC-E1-066-04-ITG | AC4, BR5 | Integration | The P1 ledger insert forced to fail with a database error |
| TC-E1-066-08-ITG | AC8, BR4 | Integration | UPDATE and DELETE on entry case_seq 3; the CORRECTION entry naming it |
| TC-ITG-E1066-01 | AC9, BR8, BR9 | Integration | The case action and the entry in one business transaction; the second call fails with 503 and its case action is compensated |
| TC-ITG-E1066-02 | AC10, BR8, BR10 | Integration | Entry case_seq 7 read through P1 and through the P3 timeline; the P3 statement log and rwb_case scanned for a copy |
| TC-ITG-E1066-03 | AC11, BR11 | Integration | Outbound call on case RW-2026-000201; one local decision record and one outbox row per append; one central decision log entry |
| TC-ITG-E1066-04 | AC12, BR12 | Integration | LOV-LEDGER-EVENT values read through the rwb-case contract; the 4 EFS history entries read through P1 alone |
| TC-ITG-E1066-05 | AC13 | Integration | Outbound call on case RW-2026-000201 with one required value missing (event code, occurred time or actor) |
| TC-ITG-E1066-06 | AC14 | Integration | Two calls recorded on case RW-2026-000201 at the same occurred time |
| TC-ITG-E1066-07 | AC15 | Integration | Call naming case 00000000-0000-0000-0000-000000000999 |
| TC-ITG-E1066-08 | AC16 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1066-ITG-AC15) |

The five legacy test cases are kept as ITG copies with the suffix `-ITG`, and the two new criteria carry `TC-ITG-E1066-01` and `TC-ITG-E1066-02`. The legacy criteria not owned here — AC5, AC6 and AC7 — and the access test TC-E1-066-09 are owned by RWB-P1-E1066-APP and are re-exercised only inside the end-to-end run where they appear as exception paths X2 to X4. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- No business value in code: the case, the users, the rule, the promise and the dates are fixture configuration; the event codes are LOV-LEDGER-EVENT values read through the rwb-case reference-data contract (DP-07).
- No personal data in logs, events, evidence or fixtures: IDs, codes and case_seq values only; the summary of a call is never logged and every fixture is synthetic.
- No cross-service table read: the case is read through P3, the entries through P1 and the decision entry through P7, and the suite owns no table (DP-01, DP-05, DP-18).
- One hop and one timeout: every call is a contract call with a 2 s budget and no chain deeper than one; the browser reaches nothing directly (DP-11, DP-19).
- No update and no delete path: no repository method, no grant and no endpoint exists for either, and AC8 asserts the refusal instead of relying on review.
- The ledger is owned by P1 and P3 holds no copy (DP-18); a timeline that answers from its own interaction table fails AC10, and it fails the statement-log assertion the same way.
- A P1 failure leaves no committed case action: the suite asserts the compensated state of AC9 and not only the error status.
- The forced insert failure runs only in DEV and SIT through the agreed test-only fault hook, is refused in UAT and production, and is restored in the same run with the append-only trigger.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | `interaction` in `rwb_source_data`; the P1 interaction write and read; the P3 timeline read | TC-E1-066-02-ITG, TC-E1-066-08-ITG, TC-ITG-E1066-02 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The P1 interaction write and read; the P3 timeline entry | TC-E1-066-01-ITG, TC-E1-066-03-ITG, TC-ITG-E1066-01 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | The promise amount 25,000.00 and promise date 2026-12-15 of the entry and of the case action | TC-E1-066-01-ITG, TC-ITG-E1066-01 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry discarded | The 503 with MSG-P1-022, the incident LEDGER_WRITE_FAILED and the compensated case action | TC-E1-066-04-ITG, TC-ITG-E1066-01 |
| DP-18 | Interaction ledger owned by rwb-source-data | The ledger and both interaction operations in P1; the P3 timeline reading P1's contract | TC-ITG-E1066-01, TC-ITG-E1066-02 |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the statement-log and `rwb_case` assertions | TC-ITG-E1066-02 |
| DP-11 | One hop and a 2 s timeout | The five consumed REST calls of section 12.2 | TC-E1-066-01-ITG, TC-ITG-E1066-02 |
| ASM-0538 | The ledger and both interaction operations belong to P1; P3 serves the timeline | The P1 and P3 rows of section 12.2 | TC-E1-066-01-ITG, TC-ITG-E1066-02 |
| ASM-0539 | The case action and the entry are one business transaction with compensation | AC9 and the compensated case read of section 12.2 | TC-ITG-E1066-01 |

The legacy AC1 to AC8 at component level belong to RWB-P1-E1066-APP and RWB-P3-E1066-APP, not to this story; the record of the compensation is the `REFUSED` state of the `interaction_link` row in rwb-case (GAP-2255).

### 19. Out of scope

- The P1 store, the writer, both interaction operations and the outbox relay (RWB-P1-E1066-APP).
- The `interaction` schema design, its columns, the two unique keys, the append-only trigger and the grants (RWB-P1-E1066-DB).
- The P1 deployment, the topic wiring and the test-only fault hook as a product feature (RWB-P1-E1066-OPS).
- The P3 case record, the case scope and the timeline read with its one-hop call to P1 (RWB-P3-E1066-APP); this story exercises them and owns none of them.
- The P7 central ledger, its ingest and its chain verification (RWB-P7-E1008-APP).
- The ledger read API, its filters and the SCR-03 ledger view (RWB-E1-068).
- The Workbench events written from the outbox and the duplicate rejection of that path (RWB-P1-E1067-APP).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline business view (RWB-E2-034).
- The retention class and the retention run for ledger entries (FEAT-ILG-10).
- The build of the harness RWB-ITG-W1J01-ITG, and NFR load and performance testing.
