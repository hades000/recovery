<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 027 Decision log writer v1 v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 027 Decision log writer v1 v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-027 Decision log writer v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-027 |
| Epic | E1, release 30 November 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-DRI-02 Write a decision log entry for every decision; FEAT-DRI-03 Record the rule ID, rule version and inputs on each entry; FEAT-DRI-04 Record the approver and the limit applied; FEAT-DRI-05 Block an action when the decision log write fails; FEAT-DRI-08 Expose the decision service to the workflow |
| Requirement IDs | REQ-DRI-004, REQ-DRI-005 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-E1-056 |
| Status | Ready for build |

## 1. Story

As the **case workflow module (SY-CASEWF)**, I want **one writer that validates and records case created, owner assigned, case transferred and document attached, with the rule ID and version used, in the same transaction as the action**, so that **the first decision records exist in Epic 1 and no action proceeds without its record**.

## 2. Business rationale

Without one writer, each module would build its own record and some actions would go unrecorded. This story gives every module one published interface that checks each record against the seven field groups, refuses an incomplete record, writes it in the caller's transaction so that a failed write stops the action, ignores a repeated event and publishes DecisionRecorded. It meets REQ-DRI-004 and REQ-DRI-005 and is the automated part of control CTL-06. The measure is decisions with a log entry: target 100 percent, and no action without one (NFR-034).

## 3. Preconditions

- RWB-E1-008 is done: the store appends hash-chained entries and holds the columns chain_seq, corrects_entry_id and actor_user_id.
- RWB-E1-056 is done: the writer's failure alert and run book are in the job and service monitoring.
- LOV-DECISION is loaded by RW-DATASTEW with the decision codes, including the access event codes for RWB-E1-039.
- Parameters in the catalog: rwb.decision.code.CASE_CREATED=D6, rwb.decision.code.OWNER_ASSIGNED=D6, rwb.decision.code.CASE_TRANSFERRED=D6, rwb.decision.code.DOCUMENT_ATTACHED=D6 (assumed; D6 is the entry and ownership decision; owner RW-DATASTEW).
- The ACE outbox (RWB-TE-006) is available in the same database transaction.

## 4. Flow

1. Calling module (for example SY-CASEWF in the morning allocation): builds a DecisionLogRecord with the case, the event, the rule ID and version, the inputs reference, the actor and an idempotency key, inside its own transaction.
2. Calling module: calls DecisionLogWriter.write as the last step before commit.
3. Writer (DecisionLogWriterService): checks that a transaction is open; refuses the call if not.
4. Writer: checks the idempotency key; for a key already written, returns the first entry reference and counts the repeat.
5. Writer (DecisionLogRecordValidator): checks the required fields and the version group; refuses an incomplete record with the missing field named.
6. Writer: calls DecisionLogStore.append (RWB-E1-008).
7. Writer: writes the DecisionRecorded event to the outbox in the same transaction.
8. Calling module: commits; the action, the entry and the event are stored together.
9. Writer: on a refused record or a failed append, raises the exception; the caller's transaction rolls back, an incident is raised and the caller shows MSG-P7-003 or its own message.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record misses the version group, the inputs reference, the final call or the case | Refused; the writer logs the error with the missing field; the caller's action rolls back | MSG-P7-009 | AC2 |
| X2 | A record carries a rule ID with no rule version | Refused as X1 | MSG-P7-009 | AC3 |
| X3 | The store cannot be written | The caller's action rolls back; an incident is raised | MSG-P7-003 | AC4 |
| X4 | The same event arrives twice with the same idempotency key | One entry; the repeat is counted | None | AC5 |
| X5 | The writer is called outside a transaction | Refused with IllegalTransactionStateException; nothing is written | None | AC6 |
| X6 | A record carries a decision code not in LOV-DECISION | Refused as X1 | MSG-P7-009 | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-E1-008) and the monitoring (RWB-E1-056) |
| Negotiable | Decision codes per event are parameters; the validation rules follow the seven field groups |
| Valuable | Every Epic 1 action has a validated record or does not happen |
| Estimable | One interface, one validator, one outbox write |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Decision log writer v1

  Background:
    Given the environment is DEV with synthetic data
    Given allocation table version "ALLOC-2026.11" and transfer rule version "TRF-2026.11" are in force

  Scenario: AC1 Record per event
    Given case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03
    When the two events are written
    Then two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED"
    Then the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference
    Then both entries pass the schema check and two DecisionRecorded events are in the outbox

  Scenario: AC2 Schema enforced
    Given a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "versions"
    Then the writer logs the error with the case ID and the missing field
    Then the system rolls the transfer in the same transaction back

  Scenario: AC3 A rule ID with no rule version is refused
    Given a record with rule ID "R-UNI-14" and an empty rule version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "ruleVersion"

  Scenario: AC4 A failed write stops the action
    Given the decision log store is unavailable
    When JOB-03 gives case "RW-2026-000124" to owner "U-7102"
    Then the write raises DecisionLogUnavailableException
    Then the case owner stays empty and the case status stays "New"
    Then the system raises an incident to the platform administrator queue

  Scenario: AC5 A repeated event gives one entry
    Given event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written
    When the same event with idempotency key "EV-7f3a-0001" arrives again
    Then one entry exists for the event
    Then the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40

  Scenario: AC6 A write outside a transaction is refused
    Given a caller without an open transaction
    When it calls the writer
    Then the system refuses the call with IllegalTransactionStateException and nothing is written

  Scenario: AC7 An unknown decision code is refused
    Given a record with decision code "D99"
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "decisionCode"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Epic 1 writes entries for case created, owner assigned, case transferred and document attached | REQ-DRI-004 |
| BR2 | Required on every record: decision code from LOV-DECISION, inputs reference, final call, decided at and the actor; the case unless the decision code is an access event | DF-DEC-002, DF-DEC-003, DF-DEC-008, DF-DEC-012, DF-DEC-016; LOV-DECISION |
| BR3 | The version group needs at least one of rule version, model version and agent version, except for access events; a rule ID needs its rule version | DF-DEC-004 to DF-DEC-007; NFR-034 |
| BR4 | An approver needs an approval level from LOV-APPROVAL-LEVEL on the same record | DF-DEC-010, DF-DEC-011; FEAT-DRI-04 |
| BR5 | The record is written in the caller's transaction; if it cannot be written, the action does not proceed | Principle 5; R-UNI-39; CTL-06; REQ-DRI-005 |
| BR6 | The same event with the same idempotency key gives one entry, and the repeat is counted | R-UNI-40; events.txt, Duplicates rule |
| BR7 | Decision codes for the Epic 1 events are parameters, not code | Principle 1; parameters rwb.decision.code.* |

## 9. State transitions

None. This story does not change a case status. It makes a status change made by another module depend on its entry: when the write fails, the case stays in the status it had (for example "New" in AC4).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | Writes entries (Decision log C) |
| SY-CASEWF Case workflow module | Calls the writer for case created, owner assigned and case transferred (Decision log C) |
| SY-OCR OCR and extraction pipeline | Calls the writer for document attached (Decision log C) |
| SY-RULES, SY-DATALOAD, SY-AGENT | Call the writer for their own decisions (Decision log C) |
| RW-AUDIT, RW-COE and every role holding Decision log R | Read the entries |
| RW-PLATADM Platform administrator | Receives the incident when a write fails |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Published interface DecisionLogWriter** (package recovery.decision.writer), the only way any module writes to the decision log:

```java
@Transactional(propagation = Propagation.MANDATORY)
DecisionLogEntryRef write(DecisionLogRecord record)
    throws DecisionLogRecordInvalidException,  // messageId MSG-P7-009, field
           DecisionLogUnavailableException;     // messageId MSG-P7-003
// DecisionLogRecord: idempotencyKey, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef,
//   recommendation, approverUserId, approvalLevel, finalCall, overrideReason, actions, outcome, decidedAt,
//   actorUserRef, correctsEntryId
// DecisionLogEntryRef: entryId, chainSeq, entryHash, repeated (boolean)
```

**Event published:** EV-08 DecisionRecorded, payload entryId, caseId, decisionCode, approver; written to the outbox in the same transaction; consumers ledger and reporting.

**GET /api/recovery/v1/decision-log/{entryId}** and **GET /api/recovery/v1/decision-log** (API-P7-007, API-P7-006): read the written entries; Decision log R; built in RWB-E1-008.

Idempotency: the record's idempotencyKey (the event ID from the calling module); unique index on decision_log_entry (idempotency_key).

## 13. Solution plan

- Package: folder `recovery/decision/writer` in the recovery module; Java package `recovery.decision.writer`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogWriter | Published interface | The write method above |
| DecisionLogWriterService | Service | Transaction check, idempotency check, validation, append, outbox event |
| DecisionLogRecordValidator | Service | BR2 to BR4 checks, with the decision codes read from LOV-DECISION |
| Epic1DecisionRecords | Service | Builders for the four Epic 1 events, with the decision code from the parameter catalog |
| DecisionRecordedPublisher | Service | Writes EV-08 to the ACE outbox |
| DecisionCenterAndLogRepository | Repository | Idempotency key lookup; append through DecisionLogStore |

- Database: Flyway migration V_E1_027__declog_idempotency.sql adds idempotency_key varchar(80) to decision_log_entry with unique index uk_declog_idempotency. No other table.
- Configuration and reference data: LOV-DECISION (RW-DATASTEW); parameters rwb.decision.code.* (RW-DATASTEW, values assumed); repeat counter exposed as metric decision_log_repeats_total in the job and service monitoring (RWB-E1-056).
- Build steps:
  1. Write the migration for idempotency_key.
  2. Build DecisionLogRecordValidator with tests for AC2, AC3 and AC7.
  3. Build DecisionLogWriterService with the mandatory transaction, the idempotency check and the append; tests for AC5 and AC6.
  4. Add the outbox write of DecisionRecorded; test that a rollback leaves no event.
  5. Build the Epic 1 record builders and wire them into JOB-02, JOB-03, the transfer engine (RWB-E1-021) and document attach (RWB-E1-032) through the interface; test AC1.
  6. Test AC4 with the store switched off: the caller's change rolls back and the incident is raised.
- Feature flag: `rwb.decision.log-writer`.
- Done when: the tests in section 16 pass and an architecture test fails the build if any class outside recovery.decision writes to decision_log_entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field (new; written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-003 | The store cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-013 | Allocation not made because the write failed (shown by the allocation summary) | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-009 is in the additions file.

## 15. Screens and states

No screen in this story. Entries are read through the decision log endpoints; failed writes appear as incidents in the job and service monitoring (RWB-E1-056).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-027-01 | AC1, BR1, BR7 | System | Synthetic case created and allocated by row ALLOC-MTG-BKK-01 |
| TC-E1-027-02 | AC2, BR3 | System | Transfer record with no version |
| TC-E1-027-03 | AC3, BR3 | System | Record with rule ID R-UNI-14 and no rule version |
| TC-E1-027-04 | AC4, BR5 | System | Store switched off during JOB-03 |
| TC-E1-027-05 | AC5, BR6 | System | Document attached event sent twice |
| TC-E1-027-06 | AC6, BR5 | System | Writer called outside a transaction |
| TC-E1-027-07 | AC7, BR2 | System | Record with decision code D99 |
| TC-E1-027-08 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E1-027-09 | Principle 5 | Resilience | The decision log write forced to fail; the calling action rolls back |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: decision codes per event are parameters and list values.
- No personal data in logs, tests or prompts; a refused record is logged with its case ID and field name only.
- No read of another module's tables; callers pass the values in the record.
- No write path to decision_log_entry other than this interface, checked by an architecture test.
- No retry inside the writer; the caller's job or request retries.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-004 | Records from Epic 1 for case creation, owner assignment, transfer and document attachment | Epic 1, 3.7 | FEAT-DRI-02, FEAT-DRI-03, FEAT-DRI-08 | 17 Run the decision center | BR1, BR2, BR3, BR4, BR6, BR7 | TC-E1-027-01, TC-E1-027-02, TC-E1-027-03, TC-E1-027-05, TC-E1-027-07 |
| REQ-DRI-005 | No action proceeds if its entry cannot be written | Epic 1, 3.7 | FEAT-DRI-04, FEAT-DRI-05 | 17 Run the decision center | BR5 | TC-E1-027-04, TC-E1-027-06, TC-E1-027-09 |

## 19. Out of scope

- The store, the hash chain and the verifier (RWB-E1-008).
- Approval records with the limit applied (RWB-E2-013).
- Access events (RWB-E1-039).
- The copy to the data lake (RWB-E1-014).
- The recommendation service with reasons for the route decision (Epic 4, API-P7-001).
