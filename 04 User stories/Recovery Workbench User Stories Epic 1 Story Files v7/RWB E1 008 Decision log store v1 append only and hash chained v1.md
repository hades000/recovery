# RWB-E1-008 Decision log store v1, append only and hash chained

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-008 |
| Epic | E1, release 30 November 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-DRI-01 Store decision log entries append-only and hash-chained |
| Requirement IDs | REQ-DRI-001, REQ-DRI-002, REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an append-only decision log store holding the seven field groups of every decision, with each entry hashed to the one before it**, so that **every decision from Epic 1 is recorded once, cannot be changed or deleted, and any change to a stored entry is found by recomputing the chain**.

## 2. Business rationale

Documentation and audit trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. This story builds the store that every later decision writes to: one record per decision with inputs, versions, recommendation, approver, final call, actions and outcome; refusal of every update and delete in the database; a single hash chain; and a verifier that finds a break. It meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003 and implements ADR-009. The measure is every decision reproducible from the log (NFR-033).

## 3. Preconditions

- RWB-E1-001 is done: table decision_log_entry exists with the trigger tr_declog_append_only and the function refuse_change from Recovery Workbench Physical Schema v6.sql.
- The database role of the ACE service holds INSERT and SELECT on decision_log_entry and no UPDATE or DELETE grant.
- The ACE notification path can send to the Compliance and PDPA officer group, and the ACE incident path is available.

## 4. Flow

1. Writer (SY-DECLOG, built in RWB-E1-027): calls DecisionLogStore.append with a validated record inside the caller's transaction, as its last statement.
2. Store (DecisionLogStore): takes the chain lock (a PostgreSQL transaction advisory lock on the key "decision_log_chain").
3. Store: reads the chain_seq and entry_hash of the last entry; sets chain_seq to last plus 1 and prev_hash to the last entry_hash, or 64 zeros for the first entry.
4. Store: builds the canonical form of the entry and sets entry_hash to its SHA-256 in lower-case hexadecimal.
5. Store: inserts the row; the caller's transaction commits the action and the entry together and releases the lock.
6. Store: on any failure, raises DecisionLogUnavailableException; the caller's transaction rolls back and the action does not happen.
7. Database: refuses any UPDATE or DELETE on decision_log_entry through tr_declog_append_only; the ACE service writes the refused attempt to the ACE audit and SOC log.
8. Verifier (HashChainVerifier): reads entries in chain_seq order over a range, recomputes each entry_hash and checks each prev_hash against the entry before it.
9. Verifier: returns the result with the count checked, the last chain_seq and its entry_hash; on a break, it names the first entry that fails, raises an incident and sends MSG-P7-008 to Compliance within 15 minutes.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An UPDATE or DELETE is attempted on a stored entry | The database refuses it; the attempt is written to the ACE audit and SOC log | None (database error, logged) | AC1 |
| X2 | A stored entry was changed outside the service, for example in a test environment | The verifier names the first entry whose hash does not match; an incident is raised; Compliance is told within 15 minutes | MSG-P7-008 | AC4 |
| X3 | Two writers append at the same moment | The chain lock orders them; chain_seq values are consecutive and each prev_hash names the entry before | None | AC5 |
| X4 | A decided entry is wrong | A new entry is written that names the corrected entry; the original stays | None | AC6 |
| X5 | The store cannot be written | The append fails, the caller's action rolls back and the caller shows its message | MSG-P7-003 | AC7 |
| X6 | A role without Decision log R reads an entry | Refused with 403 | MSG-P4-002 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the table from RWB-E1-001; every later writer depends on it |
| Negotiable | The canonical form and the hash algorithm are fixed by this story; retention follows DL26 |
| Valuable | Every decision from Epic 1 is recorded once and any change to it is found |
| Estimable | One store, one migration, one verifier, two read endpoints |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Decision log store v1, append only and hash chained

  Background:
    Given the environment is DEV with synthetic data
    Given the decision log store is empty

  Scenario: AC1 Append only
    Given an entry with chain_seq 1 and final call "OWNER_ASSIGNED" is stored for case "RW-2026-000123"
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the ACE service's database role and again through the schema owner role
    Then the system refuses all four statements : by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged
    Then the system writes the refused attempts to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC2 Hash chain
    Given 100 entries are appended
    When the chain verifier runs from chain_seq 1 to 100
    Then every entry_hash equals the SHA-256 of the entry's canonical form
    Then every prev_hash equals the entry_hash of the entry before it, and the first prev_hash is 64 zeros
    Then the result holds count 100, last chain_seq 100 and that entry's entry_hash

  Scenario: AC3 Seven field groups
    Given an entry is appended for decision "D6" on case "RW-2026-000123" with rule "R-UNI-14", rule version "UNI-2026.11", inputs reference "inputs/2026-12-03/7f3a", recommendation, approver "U-6101", approval level "L6", final call "APPROVED", actions and outcome
    When it is read with GET /decision-log/{entryId}
    Then the response holds inputsRef, ruleId and ruleVersion, recommendation, approverUserId and approvalLevel, finalCall, actions and outcome
    Then decidedAt, prevHash and entryHash are present

  Scenario: AC4 Hash chain verified daily
    Given the store holds 10,000 entries
    Given the actions of the entry with chain_seq 7,412 were changed in the DEV database with the trigger disabled
    When the chain verifier runs from chain_seq 1 to 10,000
    Then the result names chain_seq 7,412 and its entry ID as the first break
    Then the system raises an incident and MSG-P7-008 is sent to the Compliance group within 15 minutes of the run start

  Scenario: AC5 Two appends at the same moment form one chain
    Given entries up to chain_seq 50 are stored
    When two writers append one entry each in parallel transactions
    Then the entries get chain_seq 51 and 52
    Then the prev_hash of 52 equals the entry_hash of 51, and the prev_hash of 51 equals the entry_hash of 50

  Scenario: AC6 A correction is a new entry
    Given entry "E-1" records owner "U-6102" by mistake
    When a correction entry is appended with corrects_entry_id "E-1" and the right owner "U-6103"
    Then entry "E-1" is unchanged
    Then GET /decision-log for case "RW-2026-000123" returns both entries in chain order with the correction naming "E-1"

  Scenario: AC7 A failed append leaves nothing behind
    Given the database connection for the store is closed in the test double
    When a writer appends an entry inside a transaction that also changes the case owner
    Then the system raises decisionLogUnavailableException
    Then the system stores no entry , the case owner is unchanged and chain_seq is not used

  Scenario: AC8 Reading an entry needs the Decision log right
    Given test user "U-6104" holds only RW-PHONECOL, whose Decision log letter is "-"
    When the user calls GET /decision-log/{entryId}
    Then the system refuses the call with status 403 and message MSG-P4-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision writes one entry holding the seven field groups: inputs, versions, recommendation, approver, final call, actions and outcome | REQ-DRI-001; DF-DEC-004 to DF-DEC-015 |
| BR2 | A stored entry is never updated or deleted; a correction is a new entry naming the entry it corrects | REQ-DRI-002; R-UNI-24; tr_declog_append_only in Recovery Workbench Physical Schema v6.sql; ADR-009 |
| BR3 | Entries form one chain in chain_seq order; prev_hash is the entry_hash of the entry before, and 64 zeros for the first | REQ-DRI-003; DF-DEC-017, DF-DEC-018 |
| BR4 | entry_hash is the SHA-256, in lower-case hexadecimal, of the canonical form: the entry's fields except entry_hash and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings and empty fields as null | This story; ADR-009 |
| BR5 | The append is the last statement of the caller's transaction, so the action and its entry commit or roll back together | Principle 5; R-UNI-39; CTL-06 |
| BR6 | A break found by the verifier is reported to Compliance within 15 minutes and raises an incident | NFR-035; REQ-DRI-003 |
| BR7 | Retention of entries follows the bank retention schedule | DL26 |

## 9. State transitions

None. This story does not change a case status. A stored entry has no states; it exists from its append onward.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | Appends entries (Decision log C) |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR, SY-AGENT | Write through the writer only (Decision log C) |
| RW-AUDIT Internal audit | Reads entries (Decision log R) |
| RW-COMPLY Compliance and PDPA officer | Reads entries; receives break reports |
| RW-COE Center of excellence analyst | Reads entries |
| Every bank role holding Decision log R | Reads entries inside its scope |
| RW-PLATADM Platform administrator | Receives the incident on a break or a failed append |
| No role | May update or delete an entry |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (append), read |
| DF-DEC-028 | decision_log_entry | chain_seq | Write, read |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Write, read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/decision-log/{entryId}** (API-P7-007)

| Item | Value |
|---|---|
| Request | Path: entryId (uuid) |
| Response | DecisionLogEntry: id, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, overrideReason, actions, outcome, decidedAt, prevHash, entryHash |
| Errors | 401; 403 no Decision log R (MSG-P4-002); 404 no entry or case out of scope (MSG-P4-003); 503 store unavailable (MSG-GEN-006) |
| Authorization | Decision log, right R, scope applied through the entry's case |
| Idempotency | Not applicable, read only |

**GET /api/recovery/v1/decision-log** (API-P7-006), in this story by caseId only, ordered by chain_seq; page and size; response DecisionLogPage; Decision log R; errors 401, 403, 503. The other filters come in RWB-E2-005.

**Interfaces inside P7** (package recovery.decision.log):

```java
DecisionLogEntryRef append(DecisionLogRecord record) throws DecisionLogUnavailableException; // called only by the writer
ChainCheckResult verify(long fromSeq, long toSeq); // count, lastSeq, lastHash, breakSeq, breakEntryId
```

## 13. Solution plan

- Package: folder `recovery/decision/log` in the recovery module; Java package `recovery.decision.log`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionCenterAndLogController | Controller | GET /decision-log/{entryId} and GET /decision-log by case |
| DecisionLogStore | Service | Chain lock, chain_seq and prev_hash, canonical form, hash, insert |
| CanonicalEntryForm | Service | Builds the canonical JSON per BR4; one implementation used by the store and the verifier |
| HashChainVerifier | Service | Recomputes a range in chain_seq order in batches of 1,000 and reports the first break |
| ChainBreakNotifier | Service | Raises the incident and sends MSG-P7-008 to the Compliance group |
| DecisionCenterAndLogRepository | Repository | Inserts and reads decision_log_entry; no update or delete method exists |
| DecisionLogEntry | Entity | Maps decision_log_entry with the new columns; immutable |

- Database: Flyway migration V_E1_008__declog_chain.sql adds chain_seq bigint not null unique, corrects_entry_id uuid references decision_log_entry (id), actor_user_id uuid; makes case_id nullable with check constraint ck_declog_case (case_id IS NOT NULL OR decision_code LIKE 'AC-%'); adds index ix_declog_actor_time on (actor_user_id, decided_at) and ix_declog_rule on (rule_id, rule_version); revokes UPDATE and DELETE on decision_log_entry from the service role. The trigger tr_declog_append_only stays.
- Configuration and reference data: property rwb.decision.chain.genesis-hash (64 zeros); notification group for Compliance in the ACE notification path; retention class per DL26.
- Build steps:
  1. Write the migration and confirm the trigger refuses UPDATE and DELETE; test AC1.
  2. Build CanonicalEntryForm with golden test vectors (fixed entry to fixed hash) checked into the test resources.
  3. Build DecisionLogStore with the advisory lock and the insert; tests for AC2, AC5 and AC7.
  4. Build the correction path (corrects_entry_id) and its read order; test AC6.
  5. Build HashChainVerifier in batches with the break report; test AC4 on 10,000 synthetic entries.
  6. Build ChainBreakNotifier on the ACE incident and notification paths.
  7. Build the two read endpoints with scope through the case; tests for AC3 and AC8.
- Feature flag: `rwb.decision.log-store`.
- Done when: the tests in section 16 pass and the golden hash vectors give the same result on the build server and on a developer machine.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | A caller's action fails because the append failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-008 | The verifier finds a break (new) | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P4-002 | Read without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Entry of a case outside the caller's scope | This case is not in your scope. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-008 is in the additions file.

## 15. Screens and states

No screen in this story. Entries are read through the two endpoints. The Decision log query screen SCR-38 comes in RWB-E2-005.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-008-01 | AC1, BR2 | System | One synthetic entry; update and delete statements |
| TC-E1-008-02 | AC2, BR3, BR4 | System | 100 synthetic entries |
| TC-E1-008-03 | AC3, BR1 | System | One entry with all seven field groups filled |
| TC-E1-008-04 | AC4, BR6 | System | 10,000 synthetic entries with one changed in DEV |
| TC-E1-008-05 | AC5, BR3 | System | Two parallel appends after chain_seq 50 |
| TC-E1-008-06 | AC6, BR2 | System | Entry and its correction |
| TC-E1-008-07 | AC7, BR5 | System | Closed connection in the test double |
| TC-E1-008-08 | AC8 | System | RW-PHONECOL test user |
| TC-E1-008-09 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E1-008-10 | Principle 5 | Resilience | The decision log write forced to fail; the caller's change rolls back |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code; the genesis hash and the notification group are configuration.
- No personal data in logs, tests or prompts. Entries hold references (inputs_ref, case ID, user references), not customer names or identity numbers.
- No read of another module's tables; other modules write only through the P7 writer.
- No update or delete method in the repository, and no database grant for either.
- One canonical form implementation for writing and verifying.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | Epic 1, 3.7 | FEAT-DRI-01 | 17 Run the decision center | BR1 | TC-E1-008-03 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Epic 1, 3.7 | FEAT-DRI-01 | 17 Run the decision center | BR2, BR5 | TC-E1-008-01, TC-E1-008-06, TC-E1-008-07, TC-E1-008-10 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | Epic 1, 3.7 | FEAT-DRI-01 | 17 Run the decision center | BR3, BR4, BR6 | TC-E1-008-02, TC-E1-008-04, TC-E1-008-05 |

## 19. Out of scope

- Validation of entries and the publish of DecisionRecorded (RWB-E1-027).
- The nightly schedule of the chain check and its daily report (RWB-TE-008, JOB-14).
- The copy of the log to the data lake (RWB-E1-014, JOB-13).
- Audit queries by approver, rule version and date, and the query screen (RWB-E2-005).
- Retention periods (DL26).
