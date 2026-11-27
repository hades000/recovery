# RWB-P6-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1055-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1052-APP |
| Depends on (build) | RWB-P6-E1055-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P6-E1052-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P5-E1054-CON, RWB-P3-E1028-CON, RWB-P1-E1066-CON |
| Integration dependencies | None |
| External dependencies | RWB-P6-E1055-INF, RWB-P6-E1055-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-comms (APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E1055-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the notices that rwb-comms holds written to the daily WIN file through rwb-integration, the WIN acknowledgment written back onto the notice as the sent date, the barcode and the sent type, and the proof of delivery that ACE ingests read back from rwb-source-data onto the notice as the delivery status and the callback date, with `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` published on `rwb.comms.events.v1`**, so that **the case shows what was sent and when it arrived, and a notice period is counted from the delivery date rather than from a print date or a phone call**.

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. The legacy story fixed one loop for that: a daily 16:00 file to WIN, an acknowledgment that sets the notice Sent, the weekly proof of delivery that ACE ingests and the Workbench reads back, a delivery fact on the notice, a ledger entry, and a notice period that starts on the delivery date (CTL-15). This story keeps the whole loop and rebuilds it inside one service: rwb-comms owns the notice and its dispatch and delivery fields in schema `rwb_comms`, runs the dispatch as `NoticeDispatchWorkflow` on task queue `rwb-comms`, and publishes the dispatch and delivery facts on `rwb.comms.events.v1`.

Three edges of the loop are no longer this service's to reach. The file moves only through rwb-integration, which owns `outbound_item` and executes `deliverFile` (DP-16 boundary, REQ-DRI-006). The proof-of-delivery rows, the freshness stamp and the interaction ledger are rwb-source-data's, the single reader of the `recovery.v_ace_*` views under the published contract `RWB-P1-E1066-CON`, so P6 holds no grant on `v_ace_pod`, `v_ace_batch_status` or `v_ace_account` and never reads another service's table (DP-01, DP-05, DP-18). The letter behind `notice.document_id` is rwb-document's, and the `NOTICE_PERIOD` timer is rwb-case's, started when it consumes `rwb.comms.NoticeDelivered.v1` (DP-09). Reference data such as the notice type, the template version, LOV-DELIVERY and LOV-SENT-TYPE is read through the rwb-case reference-data contract (DP-07). The 16:00 run is the bank Airflow file window plus the Temporal Schedule and workers of this service (DP-10), and the job and data-quality surfaces are reached through the gateway-bff composite route (DP-19).

This document is the rwb-comms app slice of legacy RWB-E1-055. It owns the legacy criteria AC2 to AC8 and AC10 to AC11: the proof of delivery, the agreed WIN interface contract, the unacknowledged file, the failed batch, the unknown reference, the repeated read, the repeated dispatch run, the repeated delivery record and the late batch. **AC1 (dispatched) and AC9 (barcode missing after three days) are owned by `RWB-ITG-E1055-ITG`** and are not restated here. The other slices of the same key are rwb-source-data (RWB-P1-E1055-APP), rwb-case (RWB-P3-E1055-APP) and rwb-document (RWB-P5-E1055-APP); the contract baseline is RWB-P6-E1055-CON, and the infrastructure and deployment work is RWB-P6-E1055-INF and RWB-P6-E1055-OPS.

It serves REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006, and it holds the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- RWB-P6-E1052-APP is done: notices are generated in state Generated with a stored PDF and a `document_id`.
- RWB-P6-E1055-CON is published: the `GET /notices/{noticeId}` shape with the dispatch and proof fields, the internal digest write, the two event envelopes, the delivery-status list and the four contract fakes (12.8).
- The platform contract libraries are live: the reference-data client (RWB-PLT-E1043-CON, DP-07), the outbox, inbox and idempotency library with CloudEvents (RWB-PLT-TE006-CON, DP-09), the workflow kit with Schedules (RWB-PLT-E1071-CON, DP-10), the per-service Flyway baseline (RWB-PLT-E1044-CON, DP-15) and the gateway-bff composite route (RWB-PLT-N001-CON, DP-19).
- RWB-P3-E1043-CON is published for LOV-NOTICE, LOV-DELIVERY and LOV-SENT-TYPE, so no list value is written in code.
- RWB-P5-E1054-CON is published; the operation that returns the stored letter of a notice is not named in the source documents (GAP-1099; ASM-2047).
- RWB-P3-E1028-CON is published for the `NOTICE_PERIOD` timer type; the timer itself is started by rwb-case, and this story neither writes nor owns it.
- RWB-P1-E1066-CON is published for the pod, freshness and ledger facts; the exact `v_ace_pod` and `v_ace_batch_status` element names behind it are not named in the source documents (GAP-1097; ASM-2045).
- The four operational values are loaded as reference data through the rwb-case reference-data contract: the dispatch-eligible state `GENERATED`, the attempt limit 3, the barcode break at 3 days and the stale period of 1 business day. Their owner is the platform administrator (RW-PLATADM).
- The WIN edge in SIT is the stub of 12.8: an SFTP folder and an acknowledgment record, with no real WIN connection and no production data.
- The login is the rwb-comms login (DP-02); no other service's credential is held, and no `v_ace_*` view is granted to it.

### 4. Flow

1. The Temporal Schedule of this service starts `NoticeDispatchWorkflow` at 16:00 Asia/Bangkok for the business date, in namespace `rwb-recovery` on task queue `rwb-comms`; the bank Airflow file window opens the cross-system edge in the same window (JOB-10).
2. The workflow asks the generate-letter activity for the letter of each dispatch-eligible notice, and the document hub returns the stored PDF behind `notice.document_id` (P5).
3. Where a rule decides, the workflow asks the decision-approval child in rwb-decision and records the outcome through the local decision-record library, which relays `rwb.decision-record.DecisionRecorded.v1` (DP-03 through the library; DP-09).
4. rwb-comms selects the notices in state Generated with no `sent_date`, builds the INT-14 record set for the notice type and template version read as data, sets `dispatch_file_id` and increments `dispatch_attempts` on each notice.
5. The `deliverFile` activity hands the file to rwb-integration, which owns the `outbound_item` row for the business date and delivers the file to the WIN folder.
6. The WIN acknowledgment arrives through rwb-integration and is applied by the acknowledgment handler: state Sent, `sent_date`, `barcode` and `sent_type` on each notice of the file.
7. rwb-comms writes the outbound LETTER entry through the interaction operation of rwb-source-data (DP-18) and writes `rwb.comms.NoticeDispatched.v1` to its outbox in the same transaction as the state change; the outbox relay publishes it with case ID as the key.
8. The pod read runs after the batch: rwb-comms reads the DP07 records of the business date through rwb-source-data, only when the freshness answer for the date is COMPLETE, and matches each row to a notice by `barcode` and then by `notice_ref`.
9. For each match rwb-comms sets `callback_date`, `delivery_status` and state Delivered, writes the delivery to the ledger through the same operation, and writes `rwb.comms.NoticeDelivered.v1` to the outbox with the delivered date.
10. rwb-case consumes `rwb.comms.NoticeDelivered.v1` through its inbox and starts the `NOTICE_PERIOD` timer from the delivered date the event carries; this service never starts, stops or writes that timer.
11. The daily reconciliation compares the notices sent to WIN with the barcodes returned (REC-05) and lists any notice without a barcode three days after sending for the platform administrator on SCR-45.
12. Any read of the notice through `GET /notices/{noticeId}` answers the dispatch and proof fields from `rwb_comms`; the composite route assembles the screen from this answer, the document hub and the case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN does not acknowledge the file | Notices stay Generated with the file sent; the next run sends them again; after the third failure a task goes to the owning team | MSG-GEN-006 | AC4 |
| X2 | The ACE batch for source WIN is not COMPLETE for the business date | No DP07 record of that date is read through rwb-source-data; earlier delivery data stays; the notice data product shows stale | MSG-P1-001 | AC5 |
| X3 | A proof-of-delivery row names an unknown barcode and notice_ref | The row is held on the exception list of rwb-source-data with check `References`; the rest are read | None | AC6 |
| X4 | The same proof-of-delivery row is read twice | One delivery is recorded on the notice and the repeat is counted | None | AC7 |
| X5 | The dispatch run runs twice on one day | No notice is written to a second file; `dispatch_file_id` and `dispatch_attempts` move once | None | AC8 |
| X6 | No barcode three days after sending | The REC-05 break is listed for the platform administrator | None | TC-E1-055-09 |
| X7 | A later row repeats a delivery already recorded | The notice is unchanged, no second event is written, and the repeat is counted | None | AC10 |
| X8 | The WIN batch is one business day late | The freshness answer carries the stale marker and the notice section shows it | MSG-P1-001 | AC11 |
| X9 | A caller or a job reads a path outside `/api/recovery/comms/v1`, or a cross-schema read appears | The build fails the boundary test; nothing is released | None | BR11 |
| X10 | The decision record cannot be written where a rule decided | Nothing changes on the notice or the file; the run stops and an incident is raised | MSG-P7-003 | BR10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses generated notices (RWB-P6-E1052-APP) and builds against RWB-P6-E1055-CON and its four fakes; the pod, freshness, ledger, document and timer answers are contract fakes |
| Negotiable | The file layout is the WIN contract, and the eligible state, the attempt limit, the break days and the stale period are reference data, not code |
| Valuable | The case shows sent and delivered dates from WIN, not from a phone call, and the notice period starts on the delivery date |
| Estimable | One dispatch run inside a workflow, one acknowledgment handler, one pod read, one daily reconciliation and one read operation |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each owned criterion runs against synthetic WIN files and the four contract fakes, with no real WIN connection |

### 7. Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN, in rwb-comms

  Background:
    Given the dispatch-eligible notice states are "GENERATED"
    Given notice "N-0001" for case "RC-2026-000123" is in state "Generated" with notice type "DEMAND" and primary account contract "CT-77001"

  Scenario: AC2 Proof of delivery (legacy RWB-E1-055 AC2)
    Given the rwb-source-data contract mock returns the DP07 record for 2026-11-30 with barcode "RR123456789TH" and callback_date 2026-11-28
    Given the rwb-case contract mock returns a running "NOTICE_PERIOD" timer started on 2026-11-28 for case "RC-2026-000123"
    Given notice "N-0001" is "Sent" with barcode "RR123456789TH"
    When v_ace_pod holds a row for 2026-11-30 with barcode "RR123456789TH" and callback_date 2026-11-28
    Then notice "N-0001" has state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28
    Then the system writes noticeDelivered to the outbox with delivered date 2026-11-28
    Then case "RC-2026-000123" has a running "NOTICE_PERIOD" timer started on 2026-11-28

  Scenario: AC3 Interface contract agreed with WIN (legacy RWB-E1-055 AC3)
    Given the rwb-source-data contract mock returns 25 of 25 DP07 records and 0 refused for 2026-11-30, and the batch status COMPLETE with feed_version "WIN-POD-SAMPLE-v1"
    Given the sample INT-15 file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner
    When ACE ingests it and the Workbench reads v_ace_pod
    Then all 25 rows are present in v_ace_pod with 0 refused
    Then v_ace_batch_status holds source "WIN" with feed_version "WIN-POD-SAMPLE-v1" for the business date

  Scenario: AC4 File not acknowledged (legacy RWB-E1-055 AC4)
    Given the rwb-integration contract mock returns no acknowledgment for the file of 2026-11-25 and one FileFailed on each of the three attempts
    Given the rwb-case contract mock returns one open task for the litigation officer team with MSG-GEN-006 naming "WIN"
    Given the WIN file of 2026-11-25 holding "N-0001" is not acknowledged
    When JOB-10 runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged
    Then the system sends "N-0001" in each of the three files and stays "Generated"
    Then after the third failure a task is raised to the litigation officer team with MSG-GEN-006 naming "WIN"

  Scenario: AC5 The WIN batch fails its check in ACE (legacy RWB-E1-055 AC5)
    Given the rwb-source-data contract mock returns no DP07 record for 2026-11-30 and the stale marker with MSG-P1-001 naming "DP07 Legal" and 2026-11-23
    Given the ACE batch for source "WIN" of 2026-11-30 has status "FAILED" at its record count check
    When the proof of delivery for 2026-11-30 is read
    Then the system reads no v_ace_pod row for that date and no notice changes state
    Then the notice data product shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23

  Scenario: AC6 Unknown reference held (legacy RWB-E1-055 AC6)
    Given the rwb-source-data contract mock returns 29 matchable DP07 records for 2026-11-30 and 1 held row with check "References"
    Given v_ace_pod holds 30 rows for 2026-11-30 and 1 row has barcode "RR000000000TH" and notice_ref "WIN-99999" matching no notice
    When the proof of delivery is read
    Then 29 notices update their delivery fields
    Then the system holds 1 row on the exception list with check "References"

  Scenario: AC7 The same proof of delivery read twice (legacy RWB-E1-055 AC7)
    Given the rwb-source-data contract mock returns the same DP07 records for business date 2026-11-30 on both reads
    Given the v_ace_pod rows for business date 2026-11-30 have been read
    When the same rows are read again
    Then one delivery is recorded per notice and the repeat is counted under rule R-UNI-40
    Then no notice changes state a second time

  Scenario: AC8 Repeated dispatch run (legacy RWB-E1-055 AC8)
    Given the rwb-integration contract mock returns one outbound item for the file of 2026-11-25
    Given JOB-10 has written notice "N-0001" in the file of 2026-11-25
    When JOB-10 is rerun on 2026-11-25 from the job monitor
    Then the second file does not hold "N-0001"

  Scenario: AC10 Repeated delivery record (legacy RWB-E1-055 AC10)
    Given the rwb-source-data contract mock returns the second DP07 record of 2026-11-28 with barcode "RR123456789TH" and callback_date 2026-11-28
    Given notice "N-0001" is "Delivered" with callback date 2026-11-28
    When v_ace_pod holds a second row with barcode "RR123456789TH" and callback_date 2026-11-28
    Then the notice is unchanged
    Then the system writes no second NoticeDelivered
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC11 Proof of delivery batch late (legacy RWB-E1-055 AC11)
    Given the rwb-source-data contract mock returns the stale marker for "DP07 Legal" on 2026-12-01
    Given the WIN batch due on 2026-11-30 is not COMPLETE on 2026-12-01
    When a litigation officer opens case "RC-2026-000123" on 2026-12-01
    Then the notice section shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23
```

The nine criteria above are the legacy criteria this slice owns, copied word for word from RWB-E1-055 section 7 with the origin tag added and one `Given` line per cross-service answer, so the story builds before rwb-source-data, rwb-document and rwb-case are live. **AC1 and AC9 of RWB-E1-055 are not here: they belong to `RWB-ITG-E1055-ITG`**, which proves the file, the acknowledgment, the ledger call and the reconciliation break end to end on the real wave-1 services.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only notices in a dispatch-eligible state are written to the WIN file; Generated in Epic 1, Approved from RWB-E2-014. The eligible state is reference data, never a constant | INT-14; JOB-10; legacy BR1 |
| BR2 | A notice period starts only from the delivery date on the proof of delivery, and the date travels on `rwb.comms.NoticeDelivered.v1` | CTL-15; R-LIT-07; legacy BR2 |
| BR3 | An unacknowledged file is sent again; after the third failure a task goes to the owning team | INT-14 error handling; R-UNI-33, R-UNI-34; legacy BR3 |
| BR4 | A proof-of-delivery row is read only when the ACE batch for source WIN is COMPLETE for its business date; a row with an unknown reference is held; the read is made by rwb-source-data and never by rwb-comms | ACE batch record; INT-15 error handling; legacy BR4; DP-05 |
| BR5 | A notice sent with no barcode after three days is a reconciliation break, and the break days are reference data | REC-05; legacy BR5 |
| BR6 | The same event twice, and the same proof-of-delivery row twice, produce one effect and the repeat is counted | R-UNI-40; legacy BR6 |
| BR7 | The notice data product is stale one business day after the WIN batch was due, and MSG-P1-001 names the product and the last load date | `v_ace_batch_status`; MSG-P1-001; legacy BR7 |
| R-LIT-07 | The notice period runs from the delivery date: the proof of delivery is read, the delivery is written on the notice and the timer starts on the event, never on the print date | Temporal and Drools design slide 20 notes (EV-15, R-LIT-07) |
| R-LIT-08 | The proof window is 7 days from dispatch: a notice still without proof inside the window is chased by the owning team, and the window itself is RWB-E2-021 | Temporal and Drools design slide 20 notes; RWB-E2-021 |
| R-LIT-09 | A delivered-refused or undeliverable letter moves the notice to Unserved and the case to its owner's queue; the rule is evaluated in RWB-E2-021, and this story only records the delivery status the row carries | FSD P6 A2.2 AC-ALT-P6-002-02; RWB-E2-021 |
| R-UNI-33 | A downstream system that fails is retried, and the state of the record is not advanced until the retry succeeds | INT-14 error handling; legacy BR3 |
| R-UNI-34 | A retried call that passes its limit leaves the record in the exception queue with the reason, and the queue is reviewed by the owning team | INT-14 error handling; legacy BR3 |
| R-UNI-40 | The same event or the same source row twice produces one effect, and the repeat is counted | legacy BR6; FSD P6 A2.2 AC7 |

### 9. State transitions

This story changes the notice state, not a case status. The notice moves on a standard lifecycle column, with the states the legacy story and FSD P6 A2.2 name:

| From | Event | Condition | To |
|---|---|---|---|
| Generated | The dispatch run writes the notice to the file | The notice is in the dispatch-eligible state and has no `sent_date` | Generated, with `dispatch_file_id` set and `dispatch_attempts` incremented |
| Generated | WIN acknowledgment | A barcode returns for the ContractNO of the notice | Sent |
| Generated | The third attempt fails | The attempt limit is passed | Generated, with the task raised; the notice is not dispatched |
| Sent | `PROOF_OF_DELIVERY_RECEIVED` | A call-back date is present on the row | Delivered |
| Sent | A row carries a refusal or an undeliverable result | The delivery status is the row's, and the queue transfer is RWB-E2-021 | Unserved |
| Generated or Sent | A template is withdrawn before dispatch | `hold_reason` is set by the holding rule | Held, with the hold reason on the notice |
| Held | The holding condition is cleared | The template is approved again or the hold is released | The state the notice held before, and it becomes eligible again |

The hold reasons are rows on `notice.hold_reason` (DF-LEG-032); the only value the sources name is `TEMPLATE_WITHDRAWN` (FSD P6 A2.2 AC-EXC-P6-002-02), and the rest of the list is not specified in the source documents (GAP-1105; ASM-2053). The move to Delivered writes `callback_date` and `delivery_status` on the same row in the same transaction as the outbox row.

The `NOTICE_PERIOD` timer is **rwb-case's state, not this service's**: rwb-comms publishes the delivered date, and rwb-case consumes the event through its inbox and starts the timer from that date. This story names the call and asserts the effect; it never writes, stops or reads the timer row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD P6 T6.1 matrix: reads the notice, its sent date, barcode, delivery status and callback date, and receives the task after the third failure |
| RW-LEGAL, legal counsel | Litigation RA: reads and approves, and the approval before dispatch is RWB-E2-014 |
| RW-CASEOWN, case owner | Documents CRU and Litigation R: reads the notice state and the delivery facts on the case record |
| RW-PLATADM, platform administrator | Documents R and Litigation absent: reruns the dispatch run and reads the REC-05 breaks on SCR-44 and SCR-45 |
| rwb-comms service identity | Writes the notice, runs the workflow, writes the outbox rows and calls the owners' operations; it holds no grant on another schema and no grant on `recovery.v_ace_*` |
| rwb-source-data, rwb-document and rwb-case owner identities | Serve the pod records, the freshness stamp, the ledger operation, the stored letter and the timer; they take no decision in this story |

The rights above are the rows of TSD P6 T6.1 and nothing wider. DP-08 is **not** in the patterns applied to this story: the declared capability area and right on `GET /notices/{noticeId}` are enforced at gateway-bff for the screen path, and where a local guard is required on the operation itself the guard and its story are not named in the sources (GAP-1098; ASM-2046). A refusal keeps its message MSG-P4-002 and writes no notice change.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-017 | notice | document_id | Read, into the letter request only |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Write |
| DF-LEG-020 | notice | barcode | Write |
| DF-LEG-021 | notice | callback_date | Write |
| DF-LEG-022 | notice | delivery_status | Write |
| DF-LEG-023 | notice | sent_type | Write |
| Standard column | notice | state | Write |
| DF-LEG-032 | notice | hold_reason | Write, where the holding rule applies |
| DF-LEG-033 | notice | dispatch_file_id | Write |
| DF-LEG-034 | notice | dispatch_attempts | Write |
| DF-REF-047 | template | template_version | Read, as the version in force through the reference-data contract |
| DF-CAS-027 | case_account (P3) | is_primary | Read, through the rwb-case contract |
| DF-ACE-006 | v_ace_account (P1) | contract_no | Read, through the rwb-source-data contract |
| DF-ACE-253 to DF-ACE-258 | pod record (P1) | notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type | Read, through the rwb-source-data contract |
| DF-INT-002 to DF-INT-011 | interaction (P1) | case_id, occurred_at, channel, direction, summary | Written through the ledger operation of rwb-source-data |

**Indexes and migration.** The dispatch and proof columns arrive in the service's per-service Flyway sequence (DP-15), as `V1055_1__notice_dispatch.sql` by the convention of the service, after the `notice` table of RWB-P6-E1052-APP: it adds `dispatch_file_id` and `dispatch_attempts` (default 0), a unique index on `barcode` where `barcode` is not null, an index on `case_id`, and an index on `sent_date` for the daily reconciliation and the age of an undispatched notice.

**The dispatch file link.** `notice.dispatch_file_id` is a cross-reference to `outbound_item` of rwb-integration (P2), many to 0 or 1 in the TSD P6 T3.3 relationship list. It is stored as an identifier and never as a foreign key across schemas (DP-01), and the file itself is read through the rwb-integration and document contracts, never from a table of this service.

**No personal data.** The notice row of this story carries identifiers, dates, a barcode, two list values and a counter. The addressee, the address and the contact value never enter `rwb_comms`: they are read by rwb-source-data and leave through its contract into the outbound file stream, and they are not logged and not put on an event. The delivery proof carries the barcode and the dates only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/notices/{noticeId}` | Read a notice with its dispatch and proof-of-delivery fields: state, `sent_date`, `barcode`, `sent_type`, `callback_date`, `delivery_status`, `dispatch_file_id`, `dispatch_attempts`, `hold_reason`, `notice_type` and `template_version` | Litigation R, scope applied (TSD P6 T-A API-P6-002) | Not applicable |
| POST | `/internal/pod-digests` | The internal digest and pod write: the run posts the business date, the feed version, the row count and the digest of the batch it has consumed, under the service identity, and the answer records that the batch was digested once | Service identity only; no Workbench role | Idempotency-Key required; a repeated key returns the first answer and counts the repeat |

The internal operation is not part of the Workbench API surface: it is the service's own write path for the batch it has read, and its path and field names are this story's design, because no source names them. The record fields it touches are DF-LEG-019 to DF-LEG-023 and DF-LEG-033 to DF-LEG-034 only. `GET /notices/{noticeId}` answers 401, 403, 404 and 503 with the platform error envelope and takes no Idempotency-Key.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/DP07/records` | P1 rwb-source-data (RWB-P1-E1066-CON) | The proof-of-delivery records of the business date, as rwb-source-data serves them; the exact element names are not in the source documents (GAP-1097; ASM-2045) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1066-CON) | The batch completeness of source WIN and the stale marker of DP07 Legal (AC3, AC5, AC11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (DP-18) | The outbound LETTER entry on dispatch and the delivery entry on delivery |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document (RWB-P5-E1054-CON) | The stored letter behind `notice.document_id`; the element that returns it is not named in the source documents (GAP-1099; ASM-2047) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case (RWB-P3-E1028-CON) | Observed only, to assert that the `NOTICE_PERIOD` timer started on the delivered date (AC2) |
| The LOV read of the rwb-case reference-data contract | P3 rwb-case (RWB-P3-E1043-CON) | LOV-NOTICE, LOV-DELIVERY and LOV-SENT-TYPE by version, so no list value is in code |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). No row is composed into another: this service never calls a service that calls a third one.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | caseId | notice ID, case ID, sent date, barcode, sent type. No addressee, no address, no contact value |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | caseId | notice ID, case ID, delivered date, callback date, delivery status |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | caseId | decision record reference, rule code, rule version, final call, decided at; written through the local decision-record library where a rule decides |

All three are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; the delivery proof carries the barcode and the dates only.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler use |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | A case that moves out of a state in which a notice may be dispatched holds the pending notices before the next run |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | A contact stop holds the notices of the case; the stop itself is S8's fact |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | The hold is released and the notices become eligible again |

Each event is deduped through the inbox of schema `rwb_comms` on its event ID; a repeat produces no second effect and is counted (R-UNI-40).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow from the kit template; one per business date and dispatch run | `rwb-comms` in namespace `rwb-recovery` | Owns the dispatch run: the eligible set, the file request, the acknowledgment wait and the two events |
| `generateLetter` | Activity, calls rwb-document (P5) | `rwb-comms` | Ensures the letter of each eligible notice exists behind its document ID before the file is built |
| `approveNotice` | Child workflow in rwb-decision (P7) | `rwb-decision` | The approval where a rule decides; its outcome is recorded through the decision-record library before any state change |
| `deliverFile` | Activity, calls rwb-integration (P2) | `rwb-integration` | Delivers the INT-14 file for the business date and returns the `FileDelivered` or `FileFailed` fact |

The workflow is idempotent by business date and notice ID: a retried run does not write a notice into a second file and does not re-send an acknowledged notice.

#### 12.6 Schedules

One Schedule, for the in-service part of JOB-10.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The dispatch Schedule of rwb-comms (RWB-PLT-E1071-CON) | 16:00 Asia/Bangkok, daily | SKIP | Catch-up window of the workflow kit | `NoticeDispatchWorkflow` for the business date |

The cross-system edge of JOB-10 is the bank Airflow file window, owned by the platform and by rwb-integration (Architecture v5 slide 44, "Airflow file window + workers"); this story registers the in-service Schedule only and no Quartz row, no job table entry and no Control-M job.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice, its dispatch fields and its proof-of-delivery fields |
| template | P6 (rwb_comms) | The template version the letter of a notice was generated from, read only |
| merge_field | P6 (rwb_comms) | The merge codes of the template catalog, read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox, inbox and idempotency objects of the three published events and the internal write (DP-09) |

Not owned and never read as a table: `document` and `signature_request` (P5), `interaction` (P1, DP-18), `recovery_case`, `timer` and `case_account` (P3), `decision_log_entry` (P7), `outbound_item` (P2). No `v_ace_*` view is read here: the ACE facts arrive through RWB-P1-E1066-CON (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data pod batch fake (RWB-P1-E1066-CON) | 25 of 25 records with 0 refused and feed version `WIN-POD-SAMPLE-v1` for 2026-11-30; the 30-row batch of 2026-11-30 with 29 matchable rows and 1 held row with check `References`; the second record of 2026-11-28 for barcode `RR123456789TH`; batch states COMPLETE, FAILED and not COMPLETE; the stale marker with MSG-P1-001 naming "DP07 Legal" and 2026-11-23 | AC3, AC5, AC6, AC7, AC10, AC11 |
| rwb-document PDF fake (RWB-P5-E1054-CON) | The stored letter of notice `N-0001` behind its document ID, and a stored letter per notice of the fixture set | AC2, AC4, AC8 |
| rwb-case timer fake (RWB-P3-E1028-CON) | A running `NOTICE_PERIOD` timer on case `RC-2026-000123` started on 2026-11-28, and no timer on 2026-11-26 | AC2 |
| rwb-integration WIN file fake | One `outbound_item` for the file of 2026-11-25 in state ACKNOWLEDGED, one unacknowledged file per run of 2026-11-26 to 2026-11-28, and one `FileFailed` on each failed attempt; the acknowledgment record carries sent date 26112026, barcode `RR123456789TH` and sent type `NPL` for contract `CT-77001` | AC4, AC8 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the baseline is a build failure (RWB-P6-E1055-CON).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | The notice read and the internal digest write; pod records, freshness, ledger, document, timers and the reference read; one hop and 2 s each |
| Kafka | 3 published, 3 consumed | NoticeDispatched, NoticeDelivered and DecisionRecorded on `rwb.comms.events.v1` and `rwb.decision-record.v1`; CaseStateChanged, DeviationRaised and DeviationCleared |
| Temporal | 1 workflow, 3 activities | `NoticeDispatchWorkflow` on `rwb-comms`, with `generateLetter`, the decision-approval child and `deliverFile` |
| File | 1 | The INT-14 outbound WIN letters file, built here and delivered by rwb-integration; the INT-15 proof file is read back through rwb-source-data |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `dispatch`, Java package `th.co.scb.ace.workbench.recovery.comms.dispatch`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service reads no ACE view, and the primary account contract number, the address and the pod arrive through RWB-P1-E1066-CON. DP-18 applies as "the LETTER entry is written through the interaction operation of rwb-source-data", never through a table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeDispatchController | Controller | `GET /notices/{noticeId}` with the problem mapping for 401, 403, 404 and 503 |
| PodDigestController | Controller | `POST /internal/pod-digests`; service identity only, Idempotency-Key required |
| NoticeReader | Service | Builds the notice answer with the dispatch and proof fields from `rwb_comms` only |
| NoticeDispatchWorkflow | Workflow | The dispatch run of section 4: eligible set, file request, acknowledgment wait, events |
| WinNoticeFileWriter | Service | Builds the INT-14 record set and its trailer from the notice rows and the template version in force |
| WinAcknowledgmentHandler | Service | Applies the acknowledgment: state Sent, `sent_date`, `barcode`, `sent_type`, the ledger entry and `NoticeDispatched` |
| ProofOfDeliveryReader | Service | Reads DP07 through rwb-source-data for the business date after the completeness gate, and matches by barcode and then by `notice_ref` |
| DeliveryMatcher | Service | Matches a row to one notice, writes the delivery fields, the ledger entry and `NoticeDelivered`, and counts the repeat |
| PodDigestWriter | Service | Writes the digest of a batch once, under the idempotency key, and refuses a second digest of the same batch |
| BarcodeReconciliation | Job inside the service | The daily REC-05 check after the batch is complete, with the break days read as data |
| NoticeEventPublisher | Service | Writes the outbox rows of the three events |

**Database and migrations.** The `notice`, `template`, `merge_field` and library objects live in `rwb_comms` (RWB-P6-E1052-APP and RWB-P6-E1046-APP own their baseline); this story adds `V1055_1__notice_dispatch.sql` with `dispatch_file_id`, `dispatch_attempts` and the three indexes of section 11. No column is added for another service's data.

**Configuration and reference data.** `rwb.comms.dispatch.eligible-states` = `GENERATED`; `rwb.comms.dispatch.max-attempts` = 3; `rwb.comms.dispatch.barcode-break-days` = 3; `rwb.comms.pod.stale-after-business-days` = 1. All four are reference data read with their version through the rwb-case reference-data contract (DP-07), owned by the platform administrator, and none is compiled into the service.

**Build steps**

1. Write the migration and test the unique index on `barcode` and the two query indexes.
2. Build `WinNoticeFileWriter` against the INT-14 record set and the trailer, with three synthetic notices.
3. Build `NoticeDispatchWorkflow` with the Schedule hook, the idempotency rule by business date and notice ID, and the attempt count; test AC4 and AC8.
4. Build `WinAcknowledgmentHandler` with the ledger call and `NoticeDispatched`; test the Sent fields against the fake.
5. Build `ProofOfDeliveryReader` and `DeliveryMatcher` over the rwb-source-data contract, with the completeness gate, the held row, the repeat count and `NoticeDelivered`; test AC2, AC3, AC5, AC6, AC7 and AC10.
6. Build `PodDigestWriter` and the internal operation, with the repeated-batch test.
7. Build `BarcodeReconciliation` and the stale marker read; test the break list and the late batch of AC11.
8. Build `NoticeReader` and the notice answer over the contract fake, then the contract test against the real service in SIT.

**Feature flag.** `rwb.comms.win-dispatch-v1`, read as a flag of the platform library; off means no notice is written to a file and the pod read does not change a notice.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E1055-CON stay green, and a SIT week shows one file per business date, one dispatch event per acknowledged notice, one delivery per row, no notice in a second file of the same date and no notice whose delivery came from a table of this service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the Litigation right reads the notice | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written where a rule decided | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The texts are the legacy wording of RWB-E1-055 and are copied unchanged; the values of section 7 are the ones the tests assert — "DEMAND was sent for registered mail on 26 November 2026." for MSG-P6-004, "{system} is not available. Your request is queued and will be retried." with WIN named for MSG-GEN-006, and "DP07 Legal is from 2026-11-23. Today's load has not arrived." for MSG-P1-001.

### 15. Screens and states

No screen is built in this story. Three existing surfaces show what it writes, through the gateway-bff composite route (DP-19):

| Surface | What it shows |
|---|---|
| SCR-03 Case record, notice panel (state read only) | Notice state, sent date, barcode, callback date and the delivery status read from this service |
| SCR-30 Case documents | The stored letter behind the document ID and its link to the notice |
| SCR-44 Interface and job monitor | The dispatch run and the pod read in the states Running; failed; complete, with the file ID and the attempt count |
| SCR-45 Data quality | The held row with check `References` and the REC-05 break, in state breaks |

The route merges the answer of this service with rwb-document and rwb-case; the screen field lists and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | End to end | v_ace_pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-E1-055-05 | AC5, BR4 | End to end | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | End to end | 30 rows, 1 unknown |
| TC-E1-055-07 | AC7 | End to end | v_ace_pod rows of 2026-11-30 read twice |
| TC-E1-055-08 | AC8 | End to end | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | AC9, BR5 | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6 | End to end | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7 | End to end | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |

TC-E1-055-01 and TC-E1-055-09 exercise legacy AC1 and AC9, whose owning story is `RWB-ITG-E1055-ITG`; they stay in this table because it is the legacy test set of the key and the suite runs them on the same fixtures. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the eligible state, the attempt limit, the break days, the stale period, the hold reasons and the list values are reference data read with their version; no role, list value, state name or number appears in Java.
- No personal data in events, logs, workflow inputs or tests: the notice row carries identifiers, dates, a barcode and list values only; the addressee, the address and the contact value never enter `rwb_comms`, are never logged and are not put on an event.
- ACE data only through the owner's contract: the pod, the batch status, the account contract number and the contact value arrive through RWB-P1-E1066-CON, and this service holds no grant on any `v_ace_*` view (DP-05).
- No read of another service's tables and no cross-schema join: the letter is read on the document contract, the ledger is written through the rwb-source-data operation, the timer is rwb-case's and the file is rwb-integration's (DP-01, DP-18).
- Files move only through rwb-integration: no component calls WIN, and the `deliverFile` activity is the only path to the edge (REQ-DRI-006).
- One hop and a 2 s budget per consumed call, with one GET retry with jitter and a breaker per downstream; no call chain.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only; a consumer dedupes through its inbox (DP-09).
- The decision is never recorded after the effect: where a rule decides, the record is written first through the library, and a failed write stops the run (MSG-P7-003).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-02 to TC-E1-055-08, TC-E1-055-10, TC-E1-055-11 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-02, TC-E1-055-12 |
| REQ-DRI-006 | No direct call to a system of record; ACE data is read through the owner's contract and files move only through rwb-integration | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; ADR-020; DP-05 | TC-E1-055-03, TC-E1-055-05, TC-E1-055-06, TC-E1-055-07 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-055 | The dispatch and proof-of-delivery loop of the notice; AC2 to AC8 and AC10 to AC11 owned here, AC1 and AC9 owned by RWB-ITG-E1055-ITG |
| DP-01 | The notice lives in `rwb_comms`; the letter, the ledger, the timer and the file item are read through their owners |
| DP-05 | The pod, the batch status and the account facts arrive through RWB-P1-E1066-CON, and no ACE view is read here |
| DP-07 | The notice type, the template version and the two lists are reference data with a version |
| DP-09 | Three events published from the outbox and three consumed through the inbox, with CloudEvents |
| DP-10 | JOB-10 runs as the dispatch Schedule plus the workflow, not as a Quartz row |
| DP-11 | Six consumed operations, one hop and 2 s each |
| DP-15 | The dispatch columns and their three indexes in the per-service Flyway sequence |
| DP-18 | The LETTER and delivery entries are written through the rwb-source-data ledger operation |
| DP-19 | SCR-03, SCR-30, SCR-44 and SCR-45 are reached through the gateway-bff composite route |
| ADR-013 | 19 services inside ACE: this loop runs in rwb-comms, not in one monolith |
| ADR-014 | Schema and login per service: `rwb_comms` and the rwb-comms login |
| ADR-015 | Kafka with outbox, inbox and CloudEvents for the two dispatch facts |
| ADR-016 | The reusable Temporal layer, with a Schedule in place of a Quartz job |
| ADR-020 | Contract-first REST, one hop, 2 s timeout on every consumed row |
| ADR-021 | Per-service Flyway and migration ownership of the dispatch columns |

### 19. Out of scope

- **Legacy AC1 (dispatched) and AC9 (barcode missing after three days), and the end-to-end proof of the whole loop: `RWB-ITG-E1055-ITG`.**
- Notice generation, the template and merge-field catalog and the notice read baseline as a contract: RWB-P6-E1052-APP, RWB-P6-E1046-APP and RWB-P6-E1055-CON.
- The WIN acknowledgment loop of Epic 2, the refused and undeliverable letters, the 7-day proof window and the transfer to the owner's queue: RWB-E2-021 and RWB-P6-E2021-APP (R-LIT-08, R-LIT-09).
- SMS and LINE dispatch through NSS and LINE OA: RWB-P6-E2022-APP and its slices.
- The ACE ingestion of INT-15, the pod records, the freshness stamp and the interaction ledger: rwb-source-data (RWB-P1-E1055-APP, RWB-P1-E1066-CON).
- The `NOTICE_PERIOD` timer and its start: rwb-case (RWB-P3-E1055-APP, RWB-P3-E1028-CON).
- The stored letter, its content and its retention: rwb-document (RWB-P5-E1054-CON, RWB-P5-E1055-APP).
- The WIN file edge, the outbound item and the file transport: rwb-integration (RWB-P2-E1007-CON); the network, certificate and storage of the edge: RWB-P6-E1055-INF.
- The deployment, the Schedule registration, the dashboards, the alerts and the runbook: RWB-P6-E1055-OPS.
