# RWB-E1-007 Integration adapters for file loads and outbound files

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-007 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | FEAT-RDF-21 Run the integration adapters for file loads and outbound files; FEAT-RDF-23 Queue and retry a failed interface call; FEAT-RDF-24 Raise an interface failure to the exception queue; FEAT-DRI-09 Run the file adapters for sources outside COLLINS; FEAT-DRI-10 Run file and SFTP adapters; FEAT-DRI-11 Route every outbound file through the integration adapters; FEAT-DRI-13 Detect and ignore a duplicate event |
| Requirement IDs | REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one adapter pattern for every file load and outbound file, with file checks, a run log, retry and an exception queue**, so that **every later interface follows one pattern and a failed file is found on the day it fails**.

## 2. Business rationale

Each source outside COLLINS is reached today by hand or by a one-off file, and failures are found late. This story builds the one path every file takes in and out: checked, logged, retried on a schedule held as data, and moved to the exception queue with a task for a named owner after the retry limit. It meets REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008 and serves the FSD P2 measure "outbound items in the exception queue over one day: zero".

## 3. Preconditions

- RWB-E1-001 (recovery schema) is done.
- The interface configuration rows for INT-10, INT-11, INT-14 and INT-15 are loaded by the reference data administrator (RW-REFADM), version "IF-2026.11".
- The load check rows DQ-057 to DQ-063 (INT-10 CCMS) and DQ-085 to DQ-091 (INT-15 WIN) are in force.
- The SFTP inbound and outbound folders exist in DEV and SIT, with credentials in the key store (NFR-052).
- The service identity SY-DATALOAD holds its Entra ID managed identity in each environment.
- The Quartz scheduler of the ACE service runs JOB-09 (file loads), JOB-10 (WIN outbound notices) and JOB-11 (outbox sender).

## 4. Flow

1. Scheduler: JOB-09 starts the file load for an inbound interface, for example INT-10 CCMS, at its time.
2. SY-DATALOAD: the FileLoadAdapter reads the interface configuration row in force and lists the inbound folder for the file pattern and business date.
3. SY-DATALOAD: the adapter writes an interface_run row with status RECEIVED, the file name, the file hash and the business date.
4. SY-DATALOAD: the adapter runs the file checks held as data (business date, structure, control total, keys) against the header and trailer.
5. SY-DATALOAD: when every file check passes, the adapter hands the records to the owning module's loader through its published interface and sets the run to LOADED with the record count.
6. Owning module: writes an outbound file request through OutboundFiles.enqueue, for example JOB-10 for the daily WIN notice file (INT-14).
7. SY-DATALOAD: the adapter writes one outbound_item with an idempotency key, in the same transaction as the request.
8. Scheduler: JOB-11 runs every minute; the OutboundSender sends each due item over SFTP and marks it SENT, then ACKNOWLEDGED when the acknowledgment file arrives.
9. SY-DATALOAD: on a transfer failure, the sender raises SYSTEM_UNAVAILABLE for each case in the file and schedules the next attempt from the retry intervals.
10. SY-DATALOAD: after the last allowed attempt fails, the sender sets the item to EXCEPTION, raises OUTBOUND_FAILED for each case and a task for the owner role, and logs MSG-P2-001.
11. SY-DATALOAD: every consumer of an application event checks the idempotency key through IdempotencyGuard before it acts.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A file check fails (control total, business date, structure or keys) | The file is refused in full; no record is passed on; the previous load stays in use; the data product is marked stale; the data steward is alerted | MSG-P1-002 | AC2, AC4 |
| X2 | The outbound transfer fails | The item waits for the next attempt; the cases move to RETRY_QUEUE | MSG-GEN-006 | AC3 |
| X3 | The retry limit is reached | The item moves to the exception queue; a task goes to the owner role; the cases move to EXCEPTION_QUEUE | MSG-P2-001 | AC3 |
| X4 | No file is in the inbound folder by the cut-off | The run is written as MISSING; the data product is marked stale one business day after the file was due | MSG-P1-001 | AC5 |
| X5 | The same file (same hash and business date) arrives again | The repeat is logged as DUPLICATE; nothing is loaded | None | AC6 |
| X6 | The same application event arrives twice with the same key | The second event is ignored and the hit is counted (R-UNI-40) | None | AC7 |
| X7 | Two sender instances pick the same item | Only one holds the row lock; the other skips it | None | AC8 |
| X8 | A platform administrator resends an item from the exception queue | The item returns to PENDING with attempt count 0 | MSG-GEN-005 | AC9 |
| X9 | A role without the right lists or resends exception items | Refused; nothing changes | MSG-P4-002 | TC-E1-007-10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the schema (RWB-E1-001); the EFS load (RWB-E1-004) and later file loads and outbound files reuse it |
| Negotiable | Retry counts, intervals, folders and owners are interface configuration rows; the story fixes the behavior |
| Valuable | Every file in and out is logged, retried and raised to a named owner from Epic 1 |
| Estimable | Four tables, two adapters, one sender job, one guard, two endpoints |
| Small | One squad, within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Integration adapters for file loads and outbound files

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"

  Scenario: AC1 Pattern described
    Given a developer adds the file load "INT-15" WIN proof of delivery
    When the build pipeline runs
    Then the system declares the load as an interface configuration row and uses FileLoadAdapter
    Then the contract test "INT-15" parses the synthetic sample file of 120 records and passes
    Then the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter

  Scenario: AC2 File load checked
    Given a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201
    When the adapter loads it
    Then the system refuses the file in full with failed check "DQ-059 Control total"
    Then the system passes no collateral record to the loader
    Then the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale
    Then the system alerts the data steward with message MSG-P1-002

  Scenario: AC3 Retry and exception queue
    Given the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases
    Given the SFTP transfer fails on attempts 1, 2 and 3
    When the outbox sender runs
    Then attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2
    Then each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33)
    Then after attempt 3 the item status is "EXCEPTION"
    Then each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34)
    Then the item shows in the exception queue with message MSG-P2-001

  Scenario: AC4 Every file check runs before any record is used
    Given a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected
    When the adapter loads it
    Then the system refuses the file with failed check "DQ-057 Business date"
    Then the run row shows status "REFUSED" and record count 0

  Scenario: AC5 File missing at the cut-off
    Given no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00
    When JOB-09 runs
    Then the run row for "INT-11" shows status "MISSING"
    Then the system marks on 2026-11-10 the SVAF data product stale with message MSG-P1-001

  Scenario: AC6 Same file delivered twice
    Given the CCMS file for business date 2026-11-09 with hash "9f2c" was loaded at 04:05
    When the same file arrives again at 04:40
    Then the system writes a run row with status "DUPLICATE"
    Then the system passes no record to the loader

  Scenario: AC7 Duplicate application event ignored
    Given consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1"
    When the same event arrives again with the same key
    Then the consumer does not act
    Then the hit count for that key becomes 2 (R-UNI-40)

  Scenario: AC8 Two senders pick the same item
    Given outbound item "OB-0001" is due
    When two sender threads run at 10:00:00
    Then the system sends the file once
    Then the attempt count is 1

  Scenario: AC9 Resend from the exception queue
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    When a platform administrator resends it
    Then the item status is "PENDING" with attempt count 0
    Then the system writes the resend to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No component calls a system of record directly; files move only through the adapters | ADR-005; DT12; REQ-DRI-006 |
| BR2 | A file that fails a business date, structure, control total or key check is refused in full and the previous load stays in use | DQ-057 to DQ-060; CTL-02; ifspec INT-10 error handling |
| BR3 | A data product is marked stale one business day after its file was due | ifspec INT-10 to INT-16, Retry column |
| BR4 | An outbound file is sent again on the intervals in its configuration row; after the third failure a task goes to the owning team | ifspec INT-14; interface_config.max_attempts (new) |
| BR5 | A system that is unavailable queues the action and retries | R-UNI-33, R-UNI-35, R-UNI-36 |
| BR6 | An item that fails after the retry limit moves to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007 |
| BR7 | An event with a key already processed by the consumer is ignored and the hit is counted | R-UNI-40; events.txt Rules sheet, Duplicates |
| BR8 | Retry counts, intervals, folders, patterns and owners are data rows, never code | Principle 1; DT02 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE (route state) | SYSTEM_UNAVAILABLE | First failed attempt of an outbound file for the case | RETRY_QUEUE |
| RETRY_QUEUE | RETRY_SUCCEEDED | A later attempt is sent | RESUME_STATE |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Attempt count equals max attempts | EXCEPTION_QUEUE |
| ANY_ACTIVE (route state) | DUPLICATE_EVENT | Key already processed | RESUME_STATE |

The case status (recovery_case.status) does not change. P3 moves the route state when the adapter raises the event. The story also changes interface_run.status (RECEIVED, LOADED, REFUSED, MISSING, DUPLICATE) and outbound_item.status (PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Reads files, runs the file checks, writes run rows and outbound items, sends files |
| SY-CASEWF, case workflow module | Moves the route state on SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED and raises the task |
| RW-PLATADM, platform administrator | Lists exception items and resends one (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the refused load alert; reads run rows (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run rows and exception items (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-137 | interface_config | interface_id | Read |
| DF-OPS-138 | interface_config | direction | Read |
| DF-OPS-139 | interface_config | transport | Read |
| DF-OPS-140 | interface_config | inbound_path | Read |
| DF-OPS-141 | interface_config | file_pattern | Read |
| DF-OPS-142 | interface_config | data_product | Read |
| DF-OPS-143 | interface_config | max_attempts | Read |
| DF-OPS-144 | interface_config | retry_intervals_min | Read |
| DF-OPS-145 | interface_config | owner_role | Read |
| DF-OPS-146 | interface_config | alert_role | Read |
| DF-OPS-147 | interface_config | valid_from | Read |
| DF-OPS-148 | interface_config | valid_to | Read |
| DF-OPS-149 to DF-OPS-160 | interface_run | all fields | Write |
| DF-OPS-168 to DF-OPS-177 | outbound_item | all fields | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 interface |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-022 | task | status | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-09 File loads.** Trigger: Quartz, weekly Monday 04:00 for CCMS, SVAF, RPS and WIN; monthly on the 2nd working day for AMIS and GL. Input: the file matching interface_config.file_pattern in inbound_path. Output: one interface_run row per file; records passed to the owning loader. Events: none from P2; the P1 loader publishes LoadCompleted (EV-26) or LoadRefused (EV-27). Idempotency key: interface_id + business_date + file hash. Restart: a rerun for the same key writes DUPLICATE and loads nothing; a run that stopped before LOADED is rerun from the start.

**Job JOB-10 WIN outbound notices.** Trigger: Quartz, daily 16:00. Input: approved notices from P6 through OutboundFiles.enqueue. Output: one outbound_item for the day's file. Idempotency key: "INT-14:" + business date. Restart: a second run for the same date finds the key and adds nothing.

**Job JOB-11 Outbox sender.** Trigger: Quartz, every minute. Input: outbound_item rows with status PENDING or RETRY and next_attempt_at at or before now, read with `FOR UPDATE SKIP LOCKED`. Output: SFTP transfer; item status. Restart: an item in SENT without acknowledgment after 30 minutes (assumed; DL11) is retried.

**Published interfaces (package recovery.integration.adapter.api).**

```java
public interface FileLoadAdapter {
    InterfaceRunResult run(String interfaceId, LocalDate businessDate);
}
public interface OutboundFiles {
    UUID enqueue(OutboundFileRequest request); // request: interfaceId, idempotencyKey, payloadRef, caseIds
}
public interface IdempotencyGuard {
    boolean firstTime(String consumer, String idempotencyKey); // false means already processed; hit counted
}
public interface RecordLoader<T> { // implemented by the owning module, for example P1 CollateralLoader
    LoadOutcome load(String interfaceId, LocalDate businessDate, Stream<T> records);
}
```

**Endpoints (new, recorded in additions).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/outbound-items?status=EXCEPTION&interfaceId=INT-14 | Query: status, interfaceId, from, to | Array of OutboundItem: id, interfaceId, status, attemptCount, lastError, caseCount, ownerRole, updatedAt | 401 no session (MSG-P4-001); 403 no right (MSG-P4-002); 503 store unavailable (MSG-GEN-006) | Platform administration, R | Read only |
| POST /admin/outbound-items/{itemId}/resend | None; header If-Match with the item version | OutboundItem | 401; 403 (MSG-P4-002); 404 unknown item (MSG-P4-003); 409 item not in EXCEPTION or version changed (MSG-GEN-004); 503 | Platform administration, U | A second resend of an item already PENDING returns 409 and changes nothing |

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/adapter`, Java package `recovery.integration.adapter`, with `api`, `inbound`, `outbound` and `idempotency` sub-packages.

| Component | Type | Responsibility |
|---|---|---|
| IntegrationController | Controller | The two exception queue endpoints; maps errors to problem responses |
| FileLoadAdapterImpl | Service | Lists the inbound folder, writes the run row, runs the file checks, passes records to the RecordLoader |
| FileCheckRunner | Service | Runs the business date, structure, control total and key checks from the DQ rows for the interface |
| OutboundFilesImpl | Service | Writes outbound_item in the caller's transaction |
| OutboundSender | Job | JOB-11; sends due items, applies retry intervals, moves items to EXCEPTION, raises case events through P3 |
| SftpTransport | Service | The only class that opens SFTP sessions; credentials from the key store |
| IdempotencyGuardImpl | Service | Inserts into processed_event; on conflict increments hit_count and returns false |
| InterfaceConfigRepository, InterfaceRunRepository, OutboundItemRepository, ProcessedEventRepository | Repository | The four P2 tables only |
| InterfaceRun, OutboundItem, ProcessedEvent, InterfaceConfig | Entity | JPA entities with the standard columns |
| FileLoadJob | Job | JOB-09 entry point per interface |
| AdapterBoundaryTest | Test | ArchUnit rule: no SFTP, file system or HTTP client use outside recovery.integration.adapter |

- **Database:** Flyway migration `V2026_11_07__p2_adapter_tables.sql` creates interface_config, interface_run, outbound_item and processed_event in schema recovery, each with the standard columns. Constraints: unique (interface_id, business_date, file_hash) on interface_run; unique (idempotency_key) on outbound_item; primary key (consumer, idempotency_key) on processed_event; index (status, next_attempt_at) on outbound_item.
- **Configuration and reference data:** interface_config rows for INT-10 to INT-16 and INT-25, loaded by RW-REFADM through the reference data load; DQ-057 to DQ-098 load check rows (P1 reference data); property `rwb.integration.sftp.host` per environment; SFTP key in the key store.
- **Build steps:**
  1. Write the migration and the four entities and repositories with repository tests.
  2. Build FileCheckRunner with one test per check type on synthetic header and trailer files.
  3. Build FileLoadAdapterImpl with the run row, refusal path (calls P1 DataProductStatus.markStale) and duplicate path.
  4. Build OutboundFilesImpl and OutboundSender with SKIP LOCKED, retry intervals from the row and the EXCEPTION move.
  5. Wire the P3 calls: CaseEvents.raise for SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED; TaskApi.raiseTask for the owner task.
  6. Build IdempotencyGuardImpl and use it in every event listener of the recovery module through a shared base listener.
  7. Build the two endpoints with the access check and the ACE audit write on resend.
  8. Add the contract test template and the AdapterBoundaryTest to the pipeline.
- **Feature flag:** `rwb.integration.file-adapters`.
- **Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A file check refuses a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-001 | A data product is stale after a missing or refused file | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | An outbound transfer fails and is queued for retry | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-001 | An outbound item moves to the exception queue | The {interface} file {file} was not sent after {count} attempts. It is in the exception queue. |
| MSG-GEN-004 | A resend on an item whose version changed | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Saved. |
| MSG-P4-002 | A role without the right calls an endpoint | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-09 Exception queue (E1), states Loading and list: the platform administrator sees failed outbound items with the interface, attempt count, last error and case count, and resends an item. The data steward receives the refused load alert by email from the Log Analytics alert rule on event `rwb.integration.load.refused`.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-01 | AC1, BR1, BR8 | System | Synthetic INT-15 sample file, 120 records |
| TC-E1-007-02 | AC2, BR2 | System | Synthetic CCMS file, 4,200 records, trailer total 4,201 |
| TC-E1-007-03 | AC3, BR4, BR5, BR6 | System | Synthetic WIN file for 85 cases; SFTP stub failing three times |
| TC-E1-007-04 | AC4, BR2 | System | CCMS header business date 2026-11-02 |
| TC-E1-007-05 | AC5, BR3 | System | Empty SVAF inbound folder |
| TC-E1-007-06 | AC6, BR2 | System | Same CCMS file delivered twice |
| TC-E1-007-07 | AC7, BR7 | System | Event key EV-10:TRT-0001:v1 sent twice |
| TC-E1-007-08 | AC8 | System | One due item, two sender threads |
| TC-E1-007-09 | AC9 | System | Item in EXCEPTION after 3 attempts |
| TC-E1-007-10 | Access | Access | RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: retry counts, intervals, folders, patterns, owners and check tolerances are read from tables.
- No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results.
- No read of another module's tables; records reach the owning module only through its RecordLoader.
- Only SftpTransport opens a connection to another system; the boundary test fails the build on any other call.
- Outbound items carry case IDs, never addresses or names.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record | Program 5.2; Epic 1 3.2 | FEAT-DRI-09, FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | None | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Log every file, retry, exception queue with an owner task | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40 | TC-E1-007-03, TC-E1-007-06, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09 |
| REQ-DRI-008 | Data moves by COLLINS or a file load | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | None | TC-E1-007-04, TC-E1-007-05 |

## 19. Out of scope

- The record-level checks (references, lists of values, movement) and the stale marker: P1 loaders, RWB-E1-015 and RWB-E1-016.
- The run books and job monitoring: RWB-E1-056.
- The Control-M and ADF schedules of the source extracts: RWB-E1-051.
- The full SCR-44 interface and job monitor: Epic 2 and Epic 8.
- The WIN notice content and template: RWB-E2-021.

