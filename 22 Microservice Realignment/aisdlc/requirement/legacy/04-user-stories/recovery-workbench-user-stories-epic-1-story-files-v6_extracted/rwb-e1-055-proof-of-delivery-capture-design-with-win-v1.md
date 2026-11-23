<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 055 Proof of delivery capture design with WIN v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 055 Proof of delivery capture design with WIN v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-055 Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-055 |
| Epic | E1, release 30 November 2026 |
| Module | P6 Communications |
| Feature | FEAT-DRI-17 Capture proof of delivery from WIN |
| Requirement IDs | REQ-OCC-003, REQ-ILG-004 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4; Business Requirements Epic 2, section 4 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.1 |
| Priority | Should |
| Depends on | RWB-E1-052, RWB-E1-054, RWB-E1-028, RWB-E1-066 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **generated notices sent to WIN for print and registered mail, with the dispatch and the proof of delivery written back on the notice**, so that **the case shows what was sent and when it arrived**.

## 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. This story writes the daily WIN notice file (INT-14) and reads back the WIN barcode and the weekly proof of delivery that ACE ingests into `pod_receipt`, through `v_ace_pod` by `notice_ref`. It publishes the delivery so the notice period timer starts from the delivery date (CTL-15). It serves REQ-OCC-003 and REQ-ILG-004 and the FSD P6 measure "notices with proof of delivery, 100 percent", and fixes the interface contract with WIN that RWB-E2-021 completes. The Workbench writes no WIN delivery fact of its own: ACE holds the proof of delivery, as it holds every other source record (D-RCV-35 U1).

## 3. Preconditions

- RWB-E1-052 is done: notices are generated in state Generated with a stored PDF.
- RWB-E1-028 is done: P3 starts a NOTICE_PERIOD timer when it consumes NoticeDelivered.
- RWB-E1-066 is done: the interaction ledger accepts entries through its writer.
- RWB-E1-054 is done: held records reach a review list.
- The integration adapters (P2) send and receive WIN files on the SFTP path agreed with the WIN owner.
- The dispatch-eligible notice states are configured: Generated in Epic 1.
- JOB-10 is listed in the job monitor with its run book (RWB-E1-056).
- v_ace_pod is a Section B view over the ACE table pod_receipt, so the proof of delivery steps stay behind their flag until RWB-ACE-001 lands (DL43).

## 4. Flow

1. JOB-10 WIN outbound notices, daily 16:00: selects notices in a dispatch-eligible state with no sent date.
2. System: builds one INT-14 file: ContractNO of the case's primary account, addressee, address read from `v_ace_contact` by `person_key`, notice type, template version and document reference; writes the trailer with the record count.
3. System: hands the file to the integration adapters and marks each notice "file sent" with the file ID.
4. Integration adapters: deliver the WIN acknowledgment, which carries per ContractNO the sent date (DDMMYYYY), Barcode and Sent Type (s2t mapping of INT-14).
5. System: sets notice state Sent with sent_date, barcode and sent_type; writes a LETTER entry to the interaction ledger; publishes NoticeDispatched.
6. System: reads the WIN proof of delivery that ACE ingested into `pod_receipt`, through `v_ace_pod`, for the notice's business date.
7. System: matches each `v_ace_pod` row to a notice by barcode, then by `notice_ref`; sets callback_date and delivery_status from the row, and state Delivered.
8. System: writes the delivery to the interaction ledger and publishes NoticeDelivered with the delivery date; P3 starts the notice period timer from that date.
9. System: each day, compares notices sent to WIN with barcodes returned (REC-05) and lists any notice with no barcode three days after sending for the platform administrator.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN does not acknowledge the file | Notices stay Generated with file sent; the next JOB-10 run sends them again; after the third failure a task goes to the owning team | MSG-GEN-006 | AC4 |
| X2 | The ACE batch for source WIN is not COMPLETE for the business date | No `v_ace_pod` row of that date is read; earlier delivery data stays; the notice data product shows stale | MSG-P1-001 | AC5 |
| X3 | A `v_ace_pod` row names an unknown barcode and notice_ref | The row is held on the exception list; the rest are read | None | AC6 |
| X4 | The same `v_ace_pod` row is read twice | One delivery is recorded and the repeat is counted | None | AC7 |
| X5 | JOB-10 runs twice on one day | No notice is written to a second file | None | AC8 |
| X6 | No barcode three days after sending | REC-05 break listed for the platform administrator | None | AC9 |
| X7 | A later `v_ace_pod` row repeats a delivery already recorded | Ignored and counted | None | AC10 |
| X8 | The WIN batch is one business day late | The notice data product shows as stale | MSG-P1-001 | AC11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses generated notices (RWB-E1-052) and the P3 timer consumer (RWB-E1-028); refused and undeliverable results come in RWB-E2-021 |
| Negotiable | The file layouts are the WIN contract; schedule and eligible states are configuration |
| Valuable | The case shows sent and delivered dates from WIN, not from a phone call |
| Estimable | One outbound job step, two inbound handlers, one daily reconciliation |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against synthetic WIN files |

## 7. Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN

  Background:
    Given the dispatch-eligible notice states are "GENERATED"
    Given notice "N-0001" for case "RC-2026-000123" is in state "Generated" with notice type "DEMAND" and primary account contract "CT-77001"

  Scenario: AC1 Dispatched
    Given JOB-10 runs at 16:00 on 2026-11-25
    When WIN acknowledges the file with sent date 26112026, barcode "RR123456789TH" and sent type "NPL" for contract "CT-77001"
    Then notice "N-0001" has state "Sent", sent date 2026-11-26 and barcode "RR123456789TH"
    Then the interaction ledger has an outbound "LETTER" entry for case "RC-2026-000123" on 2026-11-26
    Then the system writes noticeDispatched to the outbox with notice "N-0001", barcode "RR123456789TH" and sent date 2026-11-26
    Then the case record shows MSG-P6-004 "DEMAND was sent for registered mail on 26 November 2026."

  Scenario: AC2 Proof of delivery
    Given notice "N-0001" is "Sent" with barcode "RR123456789TH"
    When v_ace_pod holds a row for 2026-11-30 with barcode "RR123456789TH" and callback_date 2026-11-28
    Then notice "N-0001" has state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28
    Then the system writes noticeDelivered to the outbox with delivered date 2026-11-28
    Then case "RC-2026-000123" has a running "NOTICE_PERIOD" timer started on 2026-11-28

  Scenario: AC3 Interface contract agreed with WIN
    Given the sample INT-15 file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner
    When ACE ingests it and the Workbench reads v_ace_pod
    Then all 25 rows are present in v_ace_pod with 0 refused
    Then v_ace_batch_status holds source "WIN" with feed_version "WIN-POD-SAMPLE-v1" for the business date

  Scenario: AC4 File not acknowledged
    Given the WIN file of 2026-11-25 holding "N-0001" is not acknowledged
    When JOB-10 runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged
    Then the system sends "N-0001" in each of the three files and stays "Generated"
    Then after the third failure a task is raised to the litigation officer team with MSG-GEN-006 naming "WIN"

  Scenario: AC5 The WIN batch fails its check in ACE
    Given the ACE batch for source "WIN" of 2026-11-30 has status "FAILED" at its record count check
    When the proof of delivery for 2026-11-30 is read
    Then the system reads no v_ace_pod row for that date and no notice changes state
    Then the notice data product shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23

  Scenario: AC6 Unknown reference held
    Given v_ace_pod holds 30 rows for 2026-11-30 and 1 row has barcode "RR000000000TH" and notice_ref "WIN-99999" matching no notice
    When the proof of delivery is read
    Then 29 notices update their delivery fields
    Then the system holds 1 row on the exception list with check "References"

  Scenario: AC7 The same proof of delivery read twice
    Given the v_ace_pod rows for business date 2026-11-30 have been read
    When the same rows are read again
    Then one delivery is recorded per notice and the repeat is counted under rule R-UNI-40
    Then no notice changes state a second time

  Scenario: AC8 Repeated dispatch run
    Given JOB-10 has written notice "N-0001" in the file of 2026-11-25
    When JOB-10 is rerun on 2026-11-25 from the job monitor
    Then the second file does not hold "N-0001"

  Scenario: AC9 Barcode missing after three days
    Given notice "N-0002" was in the file of 2026-11-25 and no barcode has returned
    When the daily reconciliation REC-05 runs on 2026-11-28
    Then the system lists "N-0002" as a break for the platform administrator on SCR-45

  Scenario: AC10 Repeated delivery record
    Given notice "N-0001" is "Delivered" with callback date 2026-11-28
    When v_ace_pod holds a second row with barcode "RR123456789TH" and callback_date 2026-11-28
    Then the notice is unchanged
    Then the system writes no second NoticeDelivered
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC11 Proof of delivery batch late
    Given the WIN batch due on 2026-11-30 is not COMPLETE on 2026-12-01
    When a litigation officer opens case "RC-2026-000123" on 2026-12-01
    Then the notice section shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only notices in a dispatch-eligible state are written to the WIN file; Generated in Epic 1, Approved from RWB-E2-014 | INT-14; JOB-10 |
| BR2 | A notice period starts only from the delivery date on the proof of delivery | CTL-15; R-LIT-07 |
| BR3 | An unacknowledged file is sent again; after the third failure a task goes to the owning team | INT-14 error handling; R-UNI-33, R-UNI-34 |
| BR4 | A `v_ace_pod` row is read only when the ACE batch for source WIN is COMPLETE for its business date; a row with an unknown reference is held | ACE batch record; INT-15 error handling |
| BR5 | A notice sent with no barcode after three days is a reconciliation break | REC-05 |
| BR6 | The same event twice produces one effect and the repeat is counted | R-UNI-40 |
| BR7 | The notice data product is stale one business day after the WIN batch was due | v_ace_batch_status; MSG-P1-001 |

## 9. State transitions

None. This story does not change a case status. It changes the notice state (standard column state):

| From | Event | Condition | To |
|---|---|---|---|
| Generated | WIN acknowledgment | Barcode returned for the ContractNO | Sent |
| Sent | PROOF_OF_DELIVERY_RECEIVED | Call-back date present | Delivered |

P3 starts the NOTICE_PERIOD timer when it consumes NoticeDelivered (EV-15).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs JOB-10 and the proof of delivery read and writes the outbound file (Litigation U) |
| SY-CASEWF, case workflow module | Consumes NoticeDelivered and starts the timer |
| RW-LITOFF, litigation officer | Reads notice state, dates and barcode (Litigation R); receives the task on repeated failure |
| RW-CASEOWN, case owner | Reads notice state (Litigation R) |
| RW-PLATADM, platform administrator | Reruns JOB-10 from SCR-44; reads REC-05 breaks |
| RW-DATASTEW, data steward | Reads refused files and held records on SCR-45 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-017 | notice | document_id | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Write |
| DF-LEG-020 | notice | barcode | Write |
| DF-LEG-021 | notice | callback_date | Write |
| DF-LEG-022 | notice | delivery_status | Write |
| DF-LEG-023 | notice | sent_type | Write |
| Standard column | notice | state | Write |
| DF-LEG-033 | notice | dispatch_file_id | Write |
| DF-LEG-034 | notice | dispatch_attempts | Write |
| DF-CAS-027 | case_account | is_primary | Read |
| DF-ACE-006 | v_ace_account | contract_no | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read |
| DF-ACE-253 | v_ace_pod | notice_ref | Read |
| DF-ACE-254 | v_ace_pod | sent_date | Read |
| DF-ACE-255 | v_ace_pod | barcode | Read |
| DF-ACE-256 | v_ace_pod | callback_date | Read |
| DF-ACE-257 | v_ace_pod | delivery_status | Read |
| DF-ACE-258 | v_ace_pod | sent_type | Read |
| DF-REF-047 | template | template_version | Read |
| DF-INT-002 | interaction | case_id | Write, through the ledger writer |
| DF-INT-004 | interaction | occurred_at | Write, through the ledger writer |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-006 | interaction | direction | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-10 WIN outbound notices**

| Item | Value |
|---|---|
| Trigger | Quartz, daily 16:00 Asia/Bangkok |
| Input | Notices in a dispatch-eligible state with no sent date |
| Output | INT-14 file: ContractNO, addressee, address, notice type, template version, document reference; trailer with record count |
| Events published | NoticeDispatched (EV-14) per acknowledged notice |
| Idempotency key | Notice ID and file date; a notice already in an unacknowledged file of the same date is skipped |
| Restart | A failed run is rerun from SCR-44; notices already in a file of that date are not written again |

**Read path: v_ace_pod (ACE ingestion of INT-15)**

| Item | Value |
|---|---|
| Trigger | A daily read at 06:00, after v_ace_batch_status shows source WIN COMPLETE for the business date |
| Input | v_ace_pod rows by notice_ref: barcode, sent_date, callback_date, delivery_status, sent_type, source_system and data_as_of |
| Checks | The ACE batch for source WIN is COMPLETE for the business date; each row matches one notice by barcode, then by notice_ref |
| Output | notice.callback_date, delivery_status and state; ledger entries; held rows on the exception list |
| Events published | NoticeDelivered (EV-15) per newly delivered notice |
| Idempotency key | pod_key and the notice with its callback_date; a repeat is counted under R-UNI-40 |
| Restart | Holds no state; the next read takes the rows of the business date again and changes nothing twice |

**Published interfaces called**

```java
void WinFileGateway.send(OutboundFile file);                                    // P2 integration adapters
void WinAcknowledgmentHandler.onAcknowledgment(WinAckFile ack);               // P6, called by P2 on arrival
UUID InteractionLedgerApi.record(InteractionRecord record);                     // ledger writer, RWB-E1-066
Stream<PodReceipt> RecoveryDataApi.proofOfDelivery(LocalDate businessDate);     // P1, from v_ace_pod by notice_ref
```

## 13. Solution plan

- Package: folder `recovery/comms/dispatch`, Java package `recovery.comms.dispatch`.

| Component | Type | Responsibility |
|---|---|---|
| WinNoticeFileJob | Job | JOB-10: selects eligible notices, builds and sends the INT-14 file |
| WinNoticeFileWriter | Service | Builds records and trailer to the file specification |
| WinAcknowledgmentHandler | Published interface | Applies the INT-14 acknowledgment: Sent, sent date, barcode, sent type |
| ProofOfDeliveryReader | Service | Reads v_ace_pod for the business date and matches each row to a notice by barcode, then notice_ref |
| DeliveryMatcher | Service | Matches a row by barcode, then notice_ref and sent date |
| NoticeEventPublisher | Service | Writes NoticeDispatched and NoticeDelivered to the outbox |
| BarcodeReconciliation | Job | Daily REC-05 check after the ACE batch is complete |

- Database: table notice gets dispatch_file_id uuid and dispatch_attempts integer default 0 in migration `V1_055__notice_dispatch.sql`; unique index ux_notice_barcode on (barcode) where barcode is not null; index ix_notice_state_sent on (state, sent_date).
- Configuration and reference data: `rwb.comms.dispatch.eligible-states` = GENERATED; `rwb.comms.dispatch.max-attempts` = 3 (INT-14); `rwb.comms.dispatch.barcode-break-days` = 3 (REC-05); `rwb.comms.pod.stale-after-business-days` = 1 (INT-15). Owner of the values: platform administrator through the configuration service.
- Build steps:
  1. Write the migration; test the barcode unique index.
  2. Build WinNoticeFileWriter against the INT-14 file specification; test layout and trailer with 3 synthetic notices.
  3. Build WinNoticeFileJob with the idempotency rule and the retry count; test AC4 and AC8.
  4. Build WinAcknowledgmentHandler with the ledger write and NoticeDispatched; test AC1.
  5. Build ProofOfDeliveryReader over v_ace_pod and DeliveryMatcher with the batch check and NoticeDelivered; test AC2, AC5, AC6, AC7, AC10.
  6. Run the WIN owner's sample file through ACE ingestion as a contract test in SIT; test AC3.
  7. Build BarcodeReconciliation and the stale marker; test AC9 and AC11.
- Feature flag: `rwb.comms.win-dispatch-v1`.
- Done when: the tests in section 16 pass, and the run book for JOB-10 and the proof of delivery read are in the job monitor (RWB-E1-056).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE | {product} is from {date}. Today's load has not arrived. |

## 15. Screens and states

No screen in this story. The litigation officer sees the notice state, sent date, barcode and callback date on SCR-03 Case record (state read only) and SCR-30 Case documents. The platform administrator sees JOB-10 and the proof of delivery read on SCR-44 Interface and job monitor (states Running; failed; complete); the data steward sees held rows and REC-05 breaks on SCR-45 Data quality (states Loading; breaks).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | System | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | System | v_ace_pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | System | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | System | No acknowledgment on three runs |
| TC-E1-055-05 | AC5, BR4 | System | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | System | 30 rows, 1 unknown |
| TC-E1-055-07 | AC7 | System | v_ace_pod rows of 2026-11-30 read twice |
| TC-E1-055-08 | AC8 | System | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | AC9, BR5 | System | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6 | System | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7 | System | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Access | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: schedule, eligible states, attempt limit, break days and stale period are configuration; file layouts follow the interface specification.
- No personal data in logs, tests or prompts. The address is read from `v_ace_contact` only into the outbound file stream and is never logged; the job log holds notice IDs and counts.
- No read of another module's tables. The primary account contract number and the address come through the P1 query; the timer is started by P3 on the event; the delivery is read from `v_ace_pod`.
- Files move only through the integration adapters (REQ-DRI-006); no direct call to WIN.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-01 to TC-E1-055-11 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-01, TC-E1-055-02, TC-E1-055-12 |

## 19. Out of scope

- Refused, returned and undeliverable letters, the proof window and the transfer to the owner's queue (RWB-E2-021, R-LIT-08, R-LIT-09).
- The conduct check before dispatch (RWB-E2-021).
- Notice approval before dispatch (RWB-E2-014).
- Statutory sale notices for repossessed assets (FEAT-AST-04, Epic 3).
