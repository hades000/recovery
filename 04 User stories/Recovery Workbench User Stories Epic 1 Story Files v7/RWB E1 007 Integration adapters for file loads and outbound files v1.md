# RWB-E1-007 Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-007 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | FEAT-RDF-21 Run the integration adapters for outbound files; FEAT-RDF-23 Queue and retry a failed interface call; FEAT-RDF-24 Raise an interface failure to the exception queue; FEAT-DRI-10 Run outbound file and SFTP adapters; FEAT-DRI-11 Route every outbound file through the integration adapters; FEAT-DRI-13 Detect and ignore a duplicate event |
| Requirement IDs | REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U1, U4); ADR-010 |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-015 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one adapter pattern for every outbound file, with the data it reads taken from the ACE views, retry on a schedule held as data and an exception queue with a named owner**, so that **every later outbound file follows one pattern and a failed file is found on the day it fails**.

## 2. Business rationale

The Workbench loads no source data; ACE ingests every source and the Workbench only sends (D-RCV-35 U1). What remains in P2 is one outbound path for the WIN registered-mail notice file, the reporting extract to the data lake and Power BI, the decision and outcome feed to COLLINS through the lake, and the debt buyer data tape. Each outbound file is built from Workbench tables and the `recovery.v_ace_*` views, sent through the outbox, acknowledged, retried on the schedule held in its interface row, and moved to the exception queue with a task for a named owner after the retry limit. It meets REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008 and serves the FSD P2 measure "outbound items in the exception queue over one day: zero".

## 3. Preconditions

- RWB-E1-001 (recovery schema) is done: interface_config, outbound_item, processed_event, outbox_event and outbox_delivery exist.
- RWB-E1-069 is done: the Section A views exist, including `v_ace_contact` and `v_ace_account`, so an outbound file can read the addressee and the account. `v_ace_batch_status` is a Section B view; the readiness check stays behind its flag until RWB-ACE-001 lands (DL43).
- RWB-E1-015 is done: the ACE batch status and the late-batch event exist.
- The interface configuration rows for INT-14, INT-19, INT-20 and INT-25 are loaded by the reference data administrator (RW-REFADM), version "IF-2026.11", each with direction OUTBOUND.
- The SFTP outbound folders exist in DEV and SIT, with credentials in the key store (NFR-052).
- The recovery service identity (recovery_svc) holds its Entra ID managed identity in each environment and SELECT on `recovery.v_ace_*` only.
- The Quartz scheduler of the ACE service runs JOB-10 (WIN outbound notices), JOB-11 (outbox sender), JOB-13 (decision log copy) and JOB-15 (reporting extract).

## 4. Flow

1. Owning module: writes an outbound file request through `OutboundFiles.enqueue`, for example JOB-10 for the daily WIN notice file (INT-14).
2. System: reads the interface configuration row in force, which names the target, the transport, the attempts, the retry intervals and the owner role.
3. System: builds the file from Workbench tables and, where the file needs source data, from the `recovery.v_ace_*` views; the addressee and address come from `v_ace_contact` by `contact_key`.
4. System: checks `v_ace_batch_status` that the ACE batch for the file's business date is COMPLETE; if it is not, the item is held and no file is built.
5. recovery_svc: writes one outbound_item with an idempotency key, in the same transaction as the request, and stores the built file in the document store.
6. Scheduler: JOB-11 runs every minute; the OutboundSender sends each due item over SFTP and marks it SENT, then ACKNOWLEDGED when the acknowledgment file arrives.
7. System: on a transfer failure, the sender raises SYSTEM_UNAVAILABLE for each case in the file and schedules the next attempt from the retry intervals.
8. System: after the last allowed attempt fails, the sender sets the item to EXCEPTION, raises OUTBOUND_FAILED for each case and a task for the owner role, and logs MSG-P2-001.
9. System: every consumer of an application event checks the idempotency key through `IdempotencyGuard` before it acts, including EV-26 AceDataReady.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch for the file's business date is not COMPLETE | The file is not built and no outbound_item is written; the request waits for the next window after EV-26; the platform administrator and data steward are alerted | MSG-P1-001 | AC4 |
| X2 | The outbound transfer fails | The item waits for the next attempt; the cases move to RETRY_QUEUE | MSG-GEN-006 | AC3 |
| X3 | The retry limit is reached | The item moves to the exception queue; a task goes to the owner role; the cases move to EXCEPTION_QUEUE | MSG-P2-001 | AC3 |
| X4 | The same application event arrives twice with the same key | The second event is ignored and the hit is counted (R-UNI-40) | None | AC5 |
| X5 | Two sender instances pick the same item | Only one holds the row lock; the other skips it | None | AC6 |
| X6 | A platform administrator resends an item from the exception queue | The item returns to PENDING with attempt count 0 | MSG-GEN-005 | AC7 |
| X7 | A role without the right lists or resends exception items | Refused; nothing changes | MSG-P4-002 | TC-E1-007-10 |
| X8 | A build reads a public table instead of a view | The statement fails at the database and the boundary test fails the build | None (pipeline log) | AC1, AC2 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the schema (RWB-E1-001) and the views (RWB-E1-069); the outbound files of later epics reuse it |
| Negotiable | Retry counts, intervals, folders, patterns and owners are interface configuration rows; the story fixes the behaviour |
| Valuable | Every outbound file is built from one source of truth, logged, retried and raised to a named owner from Epic 1 |
| Estimable | Five tables, one outbound adapter, one readiness check, one sender job, one guard, two endpoints |
| Small | One squad, within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Integration adapters for outbound files

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has direction "OUTBOUND", max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"

  Scenario: AC1 One outbound pattern
    Given a developer adds the outbound file "INT-25" debt buyer data tape
    When the build pipeline runs
    Then the system declares the file as an interface configuration row with direction "OUTBOUND" and uses OutboundFileAdapter
    Then the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and v_ace_account and passes
    Then the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter
    Then no interface configuration row has direction "INBOUND"

  Scenario: AC2 Outbound file reads ACE only through the views
    Given 85 approved notices for business date 2026-11-10, each with person_key and contact_key
    When JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt"
    Then each addressee and address is read from v_ace_contact by contact_key
    Then no statement of the build reads a public table
    Then the outbound item records the ACE business date 2026-11-10 from v_ace_batch_status

  Scenario: AC3 Retry and exception queue
    Given the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases
    Given the SFTP transfer fails on attempts 1, 2 and 3
    When the outbox sender runs
    Then attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2
    Then each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33)
    Then after attempt 3 the item status is "EXCEPTION"
    Then each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34)
    Then the item shows in the exception queue with message MSG-P2-001

  Scenario: AC4 Outbound file held while the ACE batch is not complete
    Given v_ace_batch_status shows the ALS batch for 2026-11-10 with status "FAILED" at 05:20
    Given the WIN notice file for 2026-11-10 is due at 16:00
    When JOB-10 reaches its build step
    Then no file is built and no outbound_item is written
    Then the request is held with the reason "DP01 Account and arrears is from 2026-11-07"
    Then the platform administrator receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-07. Today's ACE batch has not arrived."
    Then the file is built by the next JOB-10 run after EV-26 for 2026-11-10

  Scenario: AC5 Duplicate application event ignored
    Given consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1"
    When the same event arrives again with the same key
    Then the consumer does not act
    Then the hit count for that key becomes 2 (R-UNI-40)

  Scenario: AC6 Two senders pick the same item
    Given outbound item "OB-0001" is due
    When two sender threads run at 10:00:00
    Then the system sends the file once
    Then the attempt count is 1

  Scenario: AC7 Resend from the exception queue
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    When a platform administrator resends it
    Then the item status is "PENDING" with attempt count 0
    Then the system writes the resend to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound file goes through the one adapter; no component calls a target system directly | ADR-010; REQ-DRI-006 |
| BR2 | An outbound file reads ACE only through `recovery.v_ace_*`, by business key, and never writes to ACE | D-RCV-35 U4; ADR-010; BR-P2-001-ACE |
| BR3 | An outbound file is built only when the ACE batch for its business date is COMPLETE in `v_ace_batch_status` | VR-P2-001-1; RWB-E1-015 |
| BR4 | An outbound file is sent again on the intervals in its configuration row; after the last failure a task goes to the owning team | ifspec INT-14; interface_config.max_attempts |
| BR5 | A system that is unavailable queues the action and retries | R-UNI-33, R-UNI-35, R-UNI-36 |
| BR6 | An item that fails after the retry limit moves to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007 |
| BR7 | An event with a key already processed by the consumer is ignored and the hit is counted | R-UNI-40; events.txt Rules sheet, Duplicates |
| BR8 | Retry counts, intervals, folders, patterns and owners are data rows, never code | Principle 1; DT02 |
| BR9 | P2 has no inbound adapter: no file is picked up, checked or signed off in the Workbench, and `interface_config` holds outbound rows only | D-RCV-35 U1; ADR-010 |
| BR10 | An outbound item carries case IDs and business keys, never an address, a name or an identity number; the file itself is held in the document store | CTL-11; Guardrails |
| BR11 | The GL write-off posting and the SOC log leave through ACE paths: the approved write-off is posted in GL and read back through `v_ace_write_off`, and access and security events go to the SOC log through ACE logging (INT-22) | D-RCV-35 U1; FSD P2 A1.5 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE (route state) | SYSTEM_UNAVAILABLE | First failed attempt of an outbound file for the case | RETRY_QUEUE |
| RETRY_QUEUE | RETRY_SUCCEEDED | A later attempt is sent | RESUME_STATE |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Attempt count equals max attempts | EXCEPTION_QUEUE |
| ANY_ACTIVE (route state) | DUPLICATE_EVENT | Key already processed | RESUME_STATE |

The case status (recovery_case.status) does not change. P3 moves the route state when the adapter raises the event. The story also changes outbound_item.status (PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED) and outbox_delivery.status. There is no interface_run row: the outbound run record is outbound_item plus outbox_delivery.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Builds files, reads the views, writes outbound items, sends files |
| SY-CASEWF, case workflow module | Moves the route state on SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED and raises the task |
| RW-PLATADM, platform administrator | Lists exception items and resends one (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the held-file alert; reads run state (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run state and exception items (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-137 | interface_config | interface_id | Read |
| DF-OPS-138 | interface_config | direction | Read |
| DF-OPS-139 | interface_config | transport | Read |
| DF-OPS-141 | interface_config | file_pattern | Read |
| DF-OPS-142 | interface_config | data_product | Read |
| DF-OPS-143 | interface_config | max_attempts | Read |
| DF-OPS-144 | interface_config | retry_intervals_min | Read |
| DF-OPS-145 | interface_config | owner_role | Read |
| DF-OPS-146 | interface_config | alert_role | Read |
| DF-OPS-147 | interface_config | valid_from | Read |
| DF-OPS-148 | interface_config | valid_to | Read |
| DF-OPS-168 to DF-OPS-177 | outbound_item | all 10 fields | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event | all 6 fields | Write |
| DF-OPS-189 to DF-OPS-197 | outbox_event | all 9 fields | Write |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | all 9 fields | Write |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read |
| DF-ACE-001 | v_ace_account | account_key | Read (INT-25) |
| DF-ACE-002 | v_ace_account | account_code | Read (INT-25) |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-LEG-019 | notice | sent_date | Read (INT-14) |
| DF-LEG-030 | notice | person_key | Read (INT-14) |
| DF-DOC-006 | document | storage_ref | Read (INT-14) |
| DF-SAL-033 | debt_sale_account | account_key | Read (INT-25) |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 interface |
| DF-WRK-018 | task | case_id | Write, through the P3 interface |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-022 | task | status | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. `interface_config.inbound_path` (DF-OPS-140) stays in the table but is empty on every outbound row and is not read by this story.

## 12. Contract

**Jobs**

| Job | Trigger | Input | Output | Idempotency and restart |
|---|---|---|---|---|
| JOB-10 WIN outbound notices | Quartz, daily 16:00, after the ACE batch is complete | Approved notices from P6 through `OutboundFiles.enqueue`; addressee from `v_ace_contact` | one outbound_item for the day's file; the file in the document store | key "INT-14:" + business date; a second run adds nothing |
| JOB-11 Outbox sender | Quartz, every minute | outbound_item rows with status PENDING or RETRY and next_attempt_at at or before now, read with `FOR UPDATE SKIP LOCKED` | SFTP transfer; item status; outbox_delivery rows | an item in SENT without acknowledgment after 30 minutes (assumed; DL11) is retried |
| JOB-13 Decision log copy | Quartz, nightly 01:00 | decision_log_entry and outcomes changed that day | file to the data lake (INT-20) | key INT-20 plus business date; the next night picks up the remainder |
| JOB-15 Reporting extract | Quartz, nightly 01:30 | case, queue, task, timer, decision log and outcome records changed that day | file to the data lake (INT-19) | key INT-19 plus business date; a failed run leaves the report on the previous day |

**Published interfaces (package recovery.integration.adapter.api).**

```java
public interface OutboundFiles {
    UUID enqueue(OutboundFileRequest request); // request: interfaceId, idempotencyKey, payloadRef, caseIds, businessDate
}
public interface OutboundFileAdapter {
    OutboundResult send(String interfaceId, LocalDate businessDate);
}
public interface IdempotencyGuard {
    boolean firstTime(String consumer, String idempotencyKey); // false means already processed; hit counted
}
```

There is no `FileLoadAdapter` and no `RecordLoader`: P2 receives no file and passes no record to another module. The inbound file checks of the previous version are gone with them.

**Endpoints**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/outbound-items?status=EXCEPTION&interfaceId=INT-14 | Query: status, interfaceId, from, to | Array of OutboundItem: id, interfaceId, status, attemptCount, lastError, caseCount, ownerRole, updatedAt | 401 no session (MSG-P4-001); 403 no right (MSG-P4-002); 503 store unavailable (MSG-GEN-006) | Platform administration, R | Read only |
| POST /admin/outbound-items/{itemId}/resend | None; header If-Match with the item version | OutboundItem | 401; 403 (MSG-P4-002); 404 unknown item (MSG-P4-003); 409 item not in EXCEPTION or version changed (MSG-GEN-004); 503 | Platform administration, U | A second resend of an item already PENDING returns 409 and changes nothing |

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/adapter`, Java package `recovery.integration.adapter`, with `api`, `outbound` and `idempotency` sub-packages.

| Component | Type | Responsibility |
|---|---|---|
| IntegrationController | Controller | The two exception queue endpoints; maps errors to problem responses |
| OutboundFileAdapterImpl | Service | Builds the file from Workbench tables and the ACE views, checks the ACE batch, sends it and records the result |
| AceBatchReadiness | Service | Reads `v_ace_batch_status` and returns COMPLETE or HOLD for an interface and business date |
| OutboundFilesImpl | Service | Writes outbound_item in the caller's transaction |
| OutboundSender | Job | JOB-11; sends due items, applies retry intervals, moves items to EXCEPTION, raises case events through P3 |
| SftpTransport | Service | The only class that opens SFTP sessions; credentials from the key store |
| IdempotencyGuardImpl | Service | Inserts into processed_event; on conflict increments hit_count and returns false |
| InterfaceConfigRepository, OutboundItemRepository, ProcessedEventRepository, OutboxEventRepository, OutboxDeliveryRepository | Repository | The five P2 tables only |
| OutboundItem, ProcessedEvent, InterfaceConfig, OutboxEvent, OutboxDelivery | Entity | JPA entities with the standard columns |
| AdapterBoundaryTest | Test | ArchUnit rule: no SFTP, file system or HTTP client use outside recovery.integration.adapter, and no read of schema public |

- **Removed in this version.** FileLoadAdapter, FileCheckRunner, RecordLoader, the inbound folder listing, the file checks DQ-057 and DQ-059, the missing-file run row, JOB-09 File loads, `interface_run` and `interface_signoff`. Their later home is ACE ingestion under RWB-ACE-001. Nothing in this story replaces them.
- **Database:** no new table. V0001 (RWB-E1-001) creates interface_config, outbound_item, processed_event, outbox_event and outbox_delivery with the standard columns. Constraints already in place: unique (interface_id, valid_from) on interface_config; unique (idempotency_key) on outbound_item; unique (consumer, idempotency_key) on processed_event; unique (event_id, consumer) on outbox_delivery; index (status, next_attempt_at) on outbound_item. The interface load validates direction = OUTBOUND; a row with INBOUND is refused because no inbound interface exists.
- **Configuration and reference data:** interface_config rows for INT-14, INT-19, INT-20 and INT-25 with direction OUTBOUND, loaded by RW-REFADM through the reference data load; property `rwb.integration.sftp.host` per environment; SFTP key in the key store; the document store container for built files (RWB-TE-012).
- **Build steps:**
  1. Write the five entities and repositories with repository tests.
  2. Build AceBatchReadiness on `v_ace_batch_status` and its HOLD path.
  3. Build OutboundFileAdapterImpl with the build, the business-key reads from the views, the send, the duplicate path and the stored file.
  4. Build OutboundFilesImpl and OutboundSender with SKIP LOCKED, retry intervals from the row and the EXCEPTION move.
  5. Wire the P3 calls: CaseEvents.raise for SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED; TaskApi.raiseTask for the owner task.
  6. Build IdempotencyGuardImpl and use it in every event listener of the recovery module through a shared base listener.
  7. Build the two endpoints with the access check and the ACE audit write on resend.
  8. Add the contract test template and the AdapterBoundaryTest to the pipeline.
- **Feature flag:** `rwb.integration.file-adapters`.
- **Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-14 and INT-25 contract tests pass in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | An outbound file is held because the ACE batch is not complete | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | An outbound transfer fails and is queued for retry | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-001 | An outbound item moves to the exception queue | The {interface} file {file} was not sent after {count} attempts. It is in the exception queue. |
| MSG-GEN-004 | A resend on an item whose version changed | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Saved. |
| MSG-P4-002 | A role without the right calls an endpoint | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A resend names an unknown item | This record was not found. |

## 15. Screens and states

SCR-09 Exception queue (E1), states Loading and list: the platform administrator sees failed outbound items with the interface, attempt count, last error and case count, and resends an item. The data steward receives the held-file and failed-file alert by email from the Log Analytics alert rule on events `rwb.integration.outbound.held` and `rwb.integration.outbound.failed`.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-01 | AC1, BR1, BR8, BR9 | System | Synthetic INT-25 tape, 120 accounts; interface load with an INBOUND row |
| TC-E1-007-02 | AC2, BR2, BR10 | System | 85 synthetic notices with person_key and contact_key; v_ace_contact rows |
| TC-E1-007-03 | AC3, BR4, BR5, BR6 | System | Synthetic WIN file for 85 cases; SFTP stub failing three times |
| TC-E1-007-04 | AC4, BR3 | System | ALS batch FAILED for 2026-11-10; WIN file due at 16:00 |
| TC-E1-007-07 | AC5, BR7 | System | Event key EV-10:TRT-0001:v1 sent twice |
| TC-E1-007-08 | AC6 | System | One due item, two sender threads |
| TC-E1-007-09 | AC7 | System | Item in EXCEPTION after 3 attempts |
| TC-E1-007-10 | Access | Access | RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend; refused with MSG-P4-002 |

TC-E1-007-05 (file missing at the cut-off) and TC-E1-007-06 (same file delivered twice) are retired with the inbound file load; their behaviour is ACE ingestion and EV-27 AceDataLate. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: retry counts, intervals, folders, patterns, owners and check tolerances are read from tables.
- No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results.
- No read of another module's tables; records reach the owning module only through its published interface.
- ACE data only through `recovery.v_ace_*` views; a direct `public.*` read is a defect and fails the boundary test.
- Only SftpTransport opens a connection to another system; the boundary test fails the build on any other call.
- Outbound items carry case IDs and business keys, never addresses, names or identity numbers.
- No inbound adapter, no inbound folder and no sign-off is built, and no interface row has direction INBOUND.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the views and leaves through ACE's paths | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Log every outbound file, retry, exception queue with an owner task | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40 | TC-E1-007-03, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06 | TC-E1-007-01, TC-E1-007-04 |

## 19. Out of scope

- The record-level checks and the stale marker: P1, RWB-E1-015 and RWB-E1-016.
- The run books and job monitoring: RWB-E1-056.
- Inbound source ingestion, its schedules, its checks and the ACE team sign-off: RWB-ACE-001.
- The full SCR-44 interface and job monitor: Epic 2 and Epic 8.
- The WIN notice content and template: RWB-E2-021.
- GL write-off posting (read back through `v_ace_write_off`) and the SOC log (ACE logging, INT-22).
