<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 066 Interaction ledger store and writer v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 066 Interaction ledger store and writer v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-066 Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-066 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-ILG-01 Write every Workbench event to the ledger; FEAT-ILG-02 Hold the ledger beside the decision log; FEAT-ILG-05 Raise an incident when the ledger cannot be written |
| Requirement IDs | REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded**, so that **the history of the case is never assembled after the fact**.

## 2. Business rationale

Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

## 3. Preconditions

- RWB-E1-018 is done: recovery_case exists with case numbers RW-YYYY-NNNNNN.
- RWB-E1-027 is done: the decision log writer and its incident path (incident record and operations alert) exist.
- The interaction table from RWB-E1-001 exists with its append-only trigger tr_interaction_append_only.
- The list LOV-LEDGER-EVENT is loaded by the reference data administrator (values in section 13).
- The caller of the writer holds Case record C: a person through POST /cases/{caseId}/interactions, or a service identity (SY-CASEWF, SY-DATALOAD).

## 4. Flow

1. Case owner: records a call with POST /cases/{caseId}/interactions (channel CALL, direction OUTBOUND, result RIGHT_PARTY, summary, promise amount and date).
2. P3 interactions handler: checks Case record C and the case scope, opens a transaction and calls InteractionLedgerWriter.append().
3. InteractionLedgerWriter: validates the command (case, event code in LOV-LEDGER-EVENT, occurred time, actor, source, idempotency key).
4. InteractionLedgerWriter: takes a transaction-level advisory lock on the case ID and assigns case_seq as the case's highest case_seq plus 1.
5. InteractionLedgerWriter: inserts the entry with event code, actor type and reference, source system and source reference, channel and direction where they apply, and the decision log entry ID for a decision.
6. P3 handler: commits the action and the entry in one transaction and returns 201 with the Interaction.
7. Other recording paths (EFS history load, ALS payment load, notice dispatch): call append() in their own transactions with source system EFS or WORKBENCH.
8. On a write failure: the transaction rolls back, the caller receives MSG-P1-022, and the writer raises an incident with incident code LEDGER_WRITE_FAILED, the case ID and the cause.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ledger cannot be written | Action and entry roll back; 503 to the caller; incident raised; nothing discarded silently | MSG-P1-022 | AC4 |
| X2 | A required value is missing (event code, occurred time, actor) | 422; nothing written | MSG-GEN-001 | AC5 |
| X3 | Two entries for one case at the same moment | Both written with consecutive case_seq; no gap and no repeat | None | AC6 |
| X4 | The case does not exist or is out of scope | 404; nothing written | MSG-P4-003 | AC7 |
| X5 | Any change or delete of an entry | Refused by the append-only trigger; a correction is a new entry naming the original | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the case record (RWB-E1-018) and the decision log writer with its incident path (RWB-E1-027) |
| Negotiable | Event codes are list values; the story fixes the append-only write, the sequence and the failure behavior |
| Valuable | The case history exists as it happens and is never rebuilt by hand |
| Estimable | One table change, one writer, one published interface |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is a writer or API test on synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer

  Background:
    Given case "RW-2026-000201" exists with 6 ledger entries, case_seq 1 to 6
    Given user "u-owner-02" holds RW-CASEOWN and owns case "RW-2026-000201"

  Scenario: AC1 The ledger exists and is written to
    Given the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15
    When the action completes
    Then the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND"
    Then the entry carries promise amount 25,000.00 and promise date 2026-12-15
    Then the entry names source system "WORKBENCH"

  Scenario: AC2 It is ordered and complete
    Given case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01
    When the ledger is read
    Then the 6 entries are in one sequence ordered by occurred time
    Then case_seq runs 1 to 6 with no gap

  Scenario: AC3 It is distinct from the decision log
    Given owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01"
    When both are read
    Then the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver
    Then the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs

  Scenario: AC4 A write failure is visible
    Given the ledger insert fails with a database error
    When the case owner records a call on case "RW-2026-000201"
    Then the system refuses the call with status 503 and MSG-P1-022
    Then the ledger still holds 6 entries and no contact is saved
    Then the system raises an incident "LEDGER_WRITE_FAILED" with case "RW-2026-000201"

  Scenario: AC5 A required value is missing
    When a service calls append() for case "RW-2026-000201" with no event code
    Then the system refuses the call with MSG-GEN-001 for field "event code"
    Then the system writes no entry

  Scenario: AC6 Two entries for one case at the same moment
    Given two transactions append to case "RW-2026-000201" at the same moment
    When both commit
    Then the entries carry case_seq 7 and 8
    Then no case_seq is missing or repeated

  Scenario: AC7 A case that does not exist
    When the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999"
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system writes no entry

  Scenario: AC8 An entry cannot be changed
    Given ledger entry case_seq 3 of case "RW-2026-000201"
    When any process issues an UPDATE or DELETE on it
    Then the database refuses the statement
    Then the system writes a correction as a new entry with event "CORRECTION" naming entry case_seq 3
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ledger holds every interaction on a case; no other record is the authoritative history | REQ-ILG-001; case file item "Interaction ledger" (casemodel.txt) |
| BR2 | Every entry carries case, event, time, actor and source | REQ-ILG-002 |
| BR3 | An offer, promise, payment or hand-over is recorded on the interaction it was made in | REQ-ILG-004; interaction.promise_amount |
| BR4 | Entries are append only; a correction is a new entry naming the original | tr_interaction_append_only (Recovery Workbench Physical Schema v4.sql); R-UNI-24 |
| BR5 | A ledger write that fails stops the action and raises an incident; no entry is discarded | REQ-ILG-008; CTL-06 |
| BR6 | The ledger records what happened; the decision log records why; a decision entry links the two | FEAT-ILG-02; ADR-009 |
| BR7 | Entries of one case carry a gap-free sequence | REQ-ILG-001; interaction.case_seq |

## 9. State transitions

None. This story does not change a case status. It adds ledger entries; an entry has no status and is never changed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries only in this story (Case record R) |
| SY-CASEWF, case workflow module | Appends entries for case actions (Case record C) |
| SY-DATALOAD, data load | Appends entries from the EFS and ALS loads (Case record C) |
| RW-AUDIT, internal audit | Reads only; may not record (Case record R) |
| RW-PLATADM, platform administrator | Receives the LEDGER_WRITE_FAILED incident |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-DEC-001 | decision_log_entry | id | Read |
| DF-DEC-003 | decision_log_entry | decision_code | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-015 | interaction | actor_type | Write |
| DF-INT-016 | interaction | actor_ref | Write |
| DF-INT-017 | interaction | source_ref | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-019 | interaction | case_seq | Write |
| DF-INT-020 | interaction | decision_log_id | Write |
| DF-INT-021 | interaction | corrects_entry_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoint used (P3, API-P3-015)**

| Item | Value |
|---|---|
| Method and path | POST /api/recovery/v1/cases/{caseId}/interactions |
| Request | InteractionRequest: channel, direction, result, summary |
| Response | 201 Interaction: id, caseId, partyId, occurredAt, channel, direction, actionCode, contactResult, promiseAmount, promiseDate, summary, conductCheck, sourceSystem |
| Errors | 401 no session (MSG-P4-001); 403 no Case record C (MSG-P4-002); 404 case missing or out of scope (MSG-P4-003); 422 field invalid (MSG-GEN-001); 503 ledger write failed (MSG-P1-022) |
| Authorization | Case record, C, scope applied |
| Idempotency | The handler builds the idempotency key from the request ID header; a repeat returns the first entry (RWB-E1-067) |

**Published interface (P1)**

```java
package recovery.dataengine.ledger.api;

public interface InteractionLedgerWriter {
    /** Must run inside the caller's transaction (Propagation.MANDATORY). */
    LedgerEntryRef append(LedgerEntryCommand command);
}

public record LedgerEntryCommand(UUID caseId, UUID partyId, String eventCode,
        OffsetDateTime occurredAt, ActorType actorType, String actorRef,
        String sourceSystem, String sourceRef, String channel, String direction,
        String actionCode, String contactResult, BigDecimal promiseAmount,
        LocalDate promiseDate, String summary, UUID decisionLogEntryId,
        UUID correctsEntryId, String idempotencyKey) {}

public record LedgerEntryRef(UUID entryId, long caseSeq) {}
```

**Incident path (RWB-E1-027)**: `IncidentRecorder.raise(String incidentCode, UUID caseId, String detail)` with incident code LEDGER_WRITE_FAILED; detail holds the error class and no personal data.

## 13. Solution plan

- Package: folder `recovery/dataengine/ledger`, Java package `recovery.dataengine.ledger`.

| Component | Type | Responsibility |
|---|---|---|
| InteractionLedgerWriter | Published interface | append() for every recording path |
| LedgerWriteService | Service | Validation, advisory lock, case_seq, insert, incident on failure |
| InteractionRepository | Repository | Inserts and reads interaction rows; no update or delete method |
| Interaction | Entity | Immutable mapping of the interaction table |
| InteractionsHandler (P3, API-P3-015) | Controller | Existing P3 endpoint; delegates the write to InteractionLedgerWriter |

- Database: Flyway migration in this story adds to interaction the columns event_code varchar(40) not null, actor_type varchar(10) not null, actor_ref varchar(64) not null, source_ref varchar(60) not null, idempotency_key varchar(120), case_seq bigint not null, decision_log_id uuid, corrects_entry_id uuid; drops NOT NULL on channel and direction (Workbench events such as CASE_CREATED have no channel); adds unique (case_id, case_seq) and unique (idempotency_key). The append-only trigger stays. Index ix_interaction_case_time (case_id, occurred_at) from Recovery Workbench Physical Schema v4.sql serves the read.
- Configuration and reference data: list LOV-LEDGER-EVENT with values CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN, CORRECTION, loaded by the reference data administrator; Thai labels per DL10.
- Build steps:
  1. Flyway migration for the new columns, the nullable channel and direction, and the two unique keys.
  2. LedgerWriteService validation against LOV-LEDGER-EVENT and the required fields; MSG-GEN-001 on a missing value.
  3. Case sequence with pg_advisory_xact_lock on the case ID and max(case_seq) plus 1; retry once on a unique key clash.
  4. Insert with Propagation.MANDATORY so the entry commits with the action.
  5. Failure handling: translate the database error to LedgerWriteException, raise LEDGER_WRITE_FAILED, return MSG-P1-022 with 503 at the API.
  6. P3 InteractionsHandler delegation for POST /cases/{caseId}/interactions.
  7. Architecture test: no class outside `recovery.dataengine.ledger` uses InteractionRepository.
  8. Tests for AC1 to AC8 and the access test.
- Feature flag: `rwb.dataengine.ledger-writer`.
- Done when: the tests in section 16 pass and the EFS history load (RWB-E1-004) writes through append().

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed (new, see additions) | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing | Enter {field}. |
| MSG-P4-002 | Role without Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. In Epic 1 a contact is recorded through the API; the case record view SCR-03 (Read only) shows ledger entries through RWB-E1-068. On a failed write the caller sees MSG-P1-022 in the Error state.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-066-01 | AC1, BR2, BR3 | System | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 |
| TC-E1-066-02 | AC2, BR1, BR7 | System | 4 EFS entries, CASE_CREATED and CASE_ALLOCATED |
| TC-E1-066-03 | AC3, BR6 | System | Reassignment under R-UNI-18 version 2026.11 |
| TC-E1-066-04 | AC4, BR5 | System | Insert forced to fail |
| TC-E1-066-05 | AC5 | System | append() with no event code |
| TC-E1-066-06 | AC6, BR7 | System | Two concurrent appends on one case |
| TC-E1-066-07 | AC7 | System | Unknown case ID |
| TC-E1-066-08 | AC8, BR4 | System | UPDATE and DELETE on entry case_seq 3; CORRECTION entry |
| TC-E1-066-09 | Access | Access | RW-AUDIT posts an interaction; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: event codes are list values; channels, directions and results come from their lists.
- No personal data in logs, tests or prompts: the incident detail names the case ID and the error class only; the summary is never logged; test summaries are synthetic.
- No read of another module's tables: decision details come through the P7 interface; the interaction table is written only through InteractionLedgerWriter and read only through RWB-E1-068.
- No entry is ever updated or deleted by application code.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-02 | All recovery processes | R-UNI-24 | TC-E1-066-02, TC-E1-066-06, TC-E1-066-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01, TC-E1-066-03, TC-E1-066-05, TC-E1-066-07 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry discarded | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-05 | All recovery processes | CTL-06 | TC-E1-066-04 |

## 19. Out of scope

- Writing the Workbench events from the outbox to the ledger and duplicate rejection (RWB-E1-067).
- The ledger read interface and its filters (RWB-E1-068).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034).
- The retention class for ledger entries (FEAT-ILG-10, RWB-E2-034).
