# RWB-P6-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Proof-of-delivery rows are read on `GET /proof-of-delivery?businessDate=`, which writes nothing; rwb-comms is the only writer-caller of delivery entries (RD-P1-007 rule 7, RD-P1-021; findings #1, #2).
- Both ledger appends are specified: case uuid, `Idempotency-Key`, InteractionRequest 5.1.0, business key, answers and retry, and rwb-comms' own decision record (RD-P1-001, RD-P1-007; findings #3, #8).
- Freshness is `LOADED` or `STALE`, the ACE batch literal is `COMPLETED`, the stale period of this service is withdrawn and message texts follow Error and Message Standard v6 (RD-P1-005, RD-P1-041; findings #5, #6, #11).
- The barcode break is REC-09 (GAP-1169) (finding #10).
- Pending: feed version (NEW-GAP-F14-3), pod read trigger (NEW-GAP-F14-4), decision point (NEW-GAP-F14-5), account contract number for the file (NEW-GAP-F14-6), held rows (NEW-GAP-F14-7), second pod rows (NEW-GAP-F14-8), a row with no callback date (NEW-GAP-F14-9), WIN delivery status mapping (NEW-GAP-D3). The dispatch `conductCheck`, the delivery reference and the key length are ruled (RD-P1-064; NEW-GAP-F14-1, NEW-GAP-F14-2 and NEW-GAP-S10-16 closed).
- Finishing pass: dispatch and delivery entries follow RD-P1-064 (reference, keys, `conductCheck` `PASSED`, sole appender), the flag-closed answer follows the published read, and the address read is `getCustomer` (RD-P1-060); test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

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
| Readiness decisions | RD-P1-001; RD-P1-005; RD-P1-007; RD-P1-009; RD-P1-021; RD-P1-041, RD-P1-060, RD-P1-064 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1052-APP |
| Depends on (build) | RWB-P6-E1055-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P6-E1052-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P5-E1054-CON, RWB-P3-E1028-CON, RWB-P1-E1066-CON, RWB-P1-E1055-APP, RWB-P1-E1015-CON, RWB-P4-E1037-CON; rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| Contract version | Path version /v1; consumed P1 contract rwb-source-data.yaml 5.1.0 (API Specification v7); version of the rwb-comms contract Not specified in the source documents (DOR-RWB-P6-E1055-APP-23) |
| External dependencies | RWB-P6-E1055-INF, RWB-P6-E1055-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-023) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-P6-E1055-APP-16); size is set at refinement |
| Dependency status | RWB-P6-E1052-APP, RWB-P6-E1055-INF and RWB-P6-E1055-OPS are not done yet; the build starts after them |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-comms (APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E1055-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (43 resolved, 22 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, proof-of-delivery read, ledger append, freshness, repeat and message statements aligned with RD-P1-001, 005, 007, 009, 021 and 041. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the notices that rwb-comms holds written to the daily WIN file through rwb-integration, the WIN acknowledgment written back onto the notice as the sent date, the barcode and the sent type, and the proof of delivery that ACE ingests read back from rwb-source-data onto the notice as the delivery status and the callback date, with `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` published on `rwb.comms.events.v1`**, so that **the case shows what was sent and when it arrived, and a notice period is counted from the delivery date rather than from a print date or a phone call**.

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. The legacy story fixed one loop for that: a daily 16:00 file to WIN, an acknowledgment that sets the notice Sent, the weekly proof of delivery that ACE ingests and the Workbench reads back, a delivery fact on the notice, a ledger entry, and a notice period that starts on the delivery date (CTL-15). This story keeps the whole loop and rebuilds it inside one service: rwb-comms owns the notice and its dispatch and delivery fields in schema `rwb_comms`, runs the dispatch as `NoticeDispatchWorkflow` on task queue `rwb-comms`, and publishes the dispatch and delivery facts on `rwb.comms.events.v1`.

Three edges of the loop are no longer this service's to reach. The file moves only through rwb-integration, which owns `outbound_item` and executes `deliverFile` (DP-16 boundary, REQ-DRI-006). The proof-of-delivery rows, the freshness stamp and the interaction ledger are rwb-source-data's, the single reader of the `recovery.v_ace_*` views under the published contract `rwb-source-data.yaml` 5.1.0 (ledger: RWB-P1-E1066-CON; proof-of-delivery read: RWB-P1-E1055-APP; freshness: RWB-P1-E1015-CON), so P6 holds no grant on `v_ace_pod`, `v_ace_batch_status` or `v_ace_account` and never reads another service's table (DP-01, DP-05, DP-18). The letter behind `notice.document_id` is rwb-document's, and the `NOTICE_PERIOD` timer is rwb-case's, started when it consumes `rwb.comms.NoticeDelivered.v1` (DP-09). This story is a secondary slice of the notice-period clock and owns no legacy criterion of RWB-E1-055; both facts keep the one clock, the unique running index and the idempotency key of notice and delivered date, so a second fact is a repeat counted under R-UNI-40. Revisit at the wave 3 refinement of RWB-P3-E5002-APP. Reference data such as the notice type, the template version, LOV-DELIVERY and LOV-SENT-TYPE is read through the rwb-case reference-data contract (DP-07). The 16:00 run is the bank Airflow file window plus the Temporal Schedule and workers of this service (DP-10), and the job and data-quality surfaces are reached through the gateway-bff composite route (DP-19).

This document is the rwb-comms app slice of legacy RWB-E1-055. It owns the legacy criteria AC2 to AC8 and AC10 to AC11: the proof of delivery, the agreed WIN interface contract, the unacknowledged file, the failed batch, the unknown reference, the repeated read, the repeated dispatch run, the repeated delivery record and the late batch. **AC1 (dispatched) and AC9 (barcode missing after three days) are owned by `RWB-ITG-E1055-ITG`** and are not restated here. The other slices of the same key are rwb-source-data (RWB-P1-E1055-APP), rwb-case (RWB-P3-E1055-APP) and rwb-document (RWB-P5-E1055-APP); the contract baseline is RWB-P6-E1055-CON, and the infrastructure and deployment work is RWB-P6-E1055-INF and RWB-P6-E1055-OPS.

It serves REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006, and it holds the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- RWB-P6-E1052-APP is done: notices are generated in state Generated with a stored PDF and a `document_id`.
- RWB-P6-E1055-CON is published: the `GET /notices/{noticeId}` shape with the dispatch and proof fields, the internal digest write, the two event envelopes, the delivery-status list and the four contract fakes (12.8).
- The element names of the NoticeDelivered event and of the notice read are fixed at contract review of RWB-P6-E1055-CON (GAP-2243); no value or rule depends on them.
- The platform contract libraries are live: the reference-data client (RWB-PLT-E1043-CON, DP-07), the outbox, inbox and idempotency library with CloudEvents (RWB-PLT-TE006-CON, DP-09), the workflow kit with Schedules (RWB-PLT-E1071-CON, DP-10), the per-service Flyway baseline (RWB-PLT-E1044-CON, DP-15) and the gateway-bff composite route (RWB-PLT-N001-CON, DP-19).
- RWB-P3-E1043-CON is published for LOV-NOTICE, LOV-DELIVERY and LOV-SENT-TYPE, so no list value is written in code.
- RWB-P5-E1054-CON is published; the operation that returns the stored letter of a notice is not named in the source documents (GAP-1099; ASM-2047).
- RWB-P3-E1028-CON is published for the `NOTICE_PERIOD` timer type; the timer itself is started by rwb-case, and this story neither writes nor owns it.
- `rwb-source-data.yaml` 5.1.0 (API Specification v7) publishes the proof-of-delivery read (`ProofOfDeliveryAnswer`, `ProofOfDeliveryRow`), the freshness read (`DataProductFreshness`) and the ledger append (`InteractionRequest`). This settles the paths and element names left open by GAP-1097 and replaces the records path of ASM-2045; page parameters of the proof-of-delivery read stay Pending (GAP-0577).
- The rwb-comms workload identity holds the proof-of-delivery read right and Case record C on the ledger append; the case number used in the ledger business key is read from `GET /api/recovery/case/v1/cases/{caseId}`.
- The three operational values are loaded as reference data through the rwb-case reference-data contract: the dispatch-eligible state `GENERATED`, the attempt limit 3 and the barcode break at 3 days. Their owner is the platform administrator (RW-PLATADM). Staleness of DP07 is not a value of this service: it is the status rwb-source-data answers (RD-P1-041).
- The WIN edge in SIT is the stub of 12.8: an SFTP folder and an acknowledgment record, with no real WIN connection and no production data.
- The login is the rwb-comms login (DP-02); no other service's credential is held, and no `v_ace_*` view is granted to it.
- Ownership (GAP-1101): rwb-comms computes the barcode break on its own notice rows and publishes it; rwb-source-data owns the References exception list and the data-quality read. Pending: rwb-source-data.yaml 5.1.0 publishes no operation that records or reads a held References row, owner solution architect, tracked as NEW-GAP-F14-7 and NEW-GAP-F03-1.

### 4. Flow

1. The Temporal Schedule of this service starts `NoticeDispatchWorkflow` at 16:00 Asia/Bangkok for the business date, in namespace `rwb-recovery` on task queue `rwb-comms`; the bank Airflow file window opens the cross-system edge in the same window (JOB-10).
2. The workflow asks the generate-letter activity for the letter of each dispatch-eligible notice, and the document hub returns the stored PDF behind `notice.document_id` (P5).
3. Where a rule decides, the workflow asks the decision-approval child in rwb-decision and records the outcome through the local decision-record library, which relays `rwb.decision.DecisionRecorded.v1` (DP-03 through the library; DP-09).
4. rwb-comms selects the notices in state Generated with no `sent_date`, builds the INT-14 record set for the notice type and template version read as data, sets `dispatch_file_id` and increments `dispatch_attempts` on each notice.
5. The `deliverFile` activity hands the file to rwb-integration, which owns the `outbound_item` row for the business date and delivers the file to the WIN folder.
6. The WIN acknowledgment arrives through rwb-integration and is applied by the acknowledgment handler: state Sent, `sent_date`, `barcode` and `sent_type` on each notice of the file.
7. rwb-comms appends the outbound LETTER entry on `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` (section 12.2), records its own decision for the dispatch, and after the 201 or 200 answer commits the state change with `rwb.comms.NoticeDispatched.v1` in its outbox in one transaction; the outbox relay publishes it with case ID as the key.
8. The pod read runs after the WIN file window: rwb-comms calls `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=`. rwb-source-data serves rows only when the WIN row of the ACE batch record for the date is `COMPLETED` and answers the DP07 freshness stamp with them; the read writes nothing. rwb-comms matches each row to a notice by `barcode` and then by `noticeRef`. Pending: what starts the read and which business date it asks for, owner solution architect, tracked as NEW-GAP-F14-4.
9. For each matched `podKey` whose row holds a `barcode` or a `noticeRef` rwb-comms appends one delivery entry on the ledger operation (a row with neither is not matched, gets no entry and is logged as unmatched; RD-P1-064 rule 4), records its own decision for the delivery, and after the 201 or 200 answer sets `callback_date`, `delivery_status` and state Delivered and writes `rwb.comms.NoticeDelivered.v1` to the outbox with the delivered date.
10. rwb-case consumes `rwb.comms.NoticeDelivered.v1` through its inbox and starts the `NOTICE_PERIOD` timer from the delivered date the event carries; this service never starts, stops or writes that timer.
11. The daily reconciliation compares the notices sent to WIN with the barcodes returned (REC-09; GAP-1169) and lists any notice without a barcode three days after sending for the platform administrator on SCR-45.
12. Any read of the notice through `GET /notices/{noticeId}` answers the dispatch and proof fields from `rwb_comms`; the composite route assembles the screen from this answer, the document hub and the case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN does not acknowledge the file | Notices stay Generated with the file sent; the next run sends them again; after the third failure a task goes to the owning team | MSG-GEN-006 | AC4 |
| X2 | The ACE batch for source WIN is not `COMPLETED` for the business date | The proof-of-delivery read answers no row of that date and the DP07 status `STALE`; no append is made and earlier delivery data stays | MSG-P1-001 | AC5 |
| X3 | A proof-of-delivery row names an unknown barcode and noticeRef | The row changes no notice and gets no ledger append; it is held on the exception list of rwb-source-data with check `References` (operation Pending: NEW-GAP-F14-7); the rest are processed | None | AC6 |
| X4 | The same proof-of-delivery row is read twice | One delivery is recorded on the notice and the repeat is counted | None | AC7 |
| X5 | The dispatch run runs twice on one day | No notice is written to a second file; `dispatch_file_id` and `dispatch_attempts` move once | None | AC8 |
| X6 | No barcode three days after sending | The REC-09 break is listed for the platform administrator | None | AC12 |
| X7 | A later row repeats a delivery already recorded | The notice is unchanged, no second event is written, and the repeat is counted | None | AC10 |
| X8 | The WIN batch is one business day late | The freshness answer carries DP07 with status `STALE` and the notice section shows it | MSG-P1-001 | AC11 |
| X9 | A caller or a job reads a path outside `/api/recovery/comms/v1`, or a cross-schema read appears | The build fails the boundary test; nothing is released | None | AC13 |
| X10 | The decision record cannot be written where a rule decided | Nothing changes on the notice or the file; the run stops and an incident is raised | MSG-P7-003 | AC14 |
| X11 | The ledger append fails, is refused or does not answer | The notice state is not advanced and no event is written; a failed call is retried with the same keys; a refusal is recorded by the run | MSG-GEN-006 on 503 | AC19, AC21 |
| X12 | The Section B views are not deployed, the pod-read flag is closed, or the read is refused or unavailable | No notice changes and no append is made | MSG-GEN-006 on 503 | AC22, AC23 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses generated notices (RWB-P6-E1052-APP) and builds against RWB-P6-E1055-CON and its four fakes; the pod, freshness, ledger, document and timer answers are contract fakes |
| Negotiable | The file layout is the WIN contract, and the eligible state, the attempt limit and the break days are reference data, not code |
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
    Given the rwb-source-data provider fake answers GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30 with 200, productCode "DP07", freshness status "LOADED" and one row with podKey {pod_key}, noticeRef "N-0001", barcode "RR123456789TH" and callbackDate 2026-11-28
    Given notice "N-0001" is "Sent" with barcode "RR123456789TH" and {caseId} is the synthetic uuid of case "RC-2026-000123"
    Given the rwb-case contract mock returns a running "NOTICE_PERIOD" timer started on 2026-11-28 for case "RC-2026-000123"
    When rwb-comms reads the proof of delivery of 2026-11-30
    Then rwb-comms calls POST /api/recovery/source-data/v1/cases/{caseId}/interactions once for {pod_key} with header Idempotency-Key (a UUID), eventCode "LETTER", occurredAt on 2026-11-28, actorType "SERVICE", actorRef "rwb-comms", sourceRef "N-0001", idempotencyKey "LETTER-RC-2026-000123-20261128-{u}" where {u} is the UUID version 5 of {pod_key} in the RFC 9562 URL namespace, channel "LETTER", direction "OUTBOUND", deliveryStatus "DELIVERED" and externalRef "RR123456789TH", and is answered 201
    Then notice "N-0001" has state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28
    Then one "rwb.comms.NoticeDelivered.v1" with delivered date 2026-11-28 is written to the outbox with ce_idempotencykey equal to the idempotencyKey of the append
    Then rwb-comms writes its own decision record for the delivery (decision point and rule code Pending: NEW-GAP-F14-5)
    Then case "RC-2026-000123" has a running "NOTICE_PERIOD" timer started on 2026-11-28

  Scenario: AC3 Interface contract agreed with WIN (legacy RWB-E1-055 AC3)
    Given the sample INT-15 file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner is ingested by ACE and the WIN row of the ACE batch record for 2026-11-30 is "COMPLETED" with is_complete true
    Given the rwb-source-data provider fake answers the proof-of-delivery read of 2026-11-30 with 200, freshness status "LOADED" and 25 rows
    When rwb-comms reads the proof of delivery of 2026-11-30
    Then all 25 rows are received in ascending podKey order with 0 refused, each with the ten fields of ProofOfDeliveryRow
    # Pending: how rwb-comms learns the feed version "WIN-POD-SAMPLE-v1"; the published answer carries none (NEW-GAP-F14-3). Page parameters: Pending (GAP-0577)

  Scenario: AC4 File not acknowledged (legacy RWB-E1-055 AC4)
    Given the rwb-integration contract mock returns no acknowledgment for the file of 2026-11-25 and one FileFailed on each of the three attempts
    Given the rwb-case contract mock returns one open task for the litigation officer team with MSG-GEN-006 naming "WIN"
    Given the WIN file of 2026-11-25 holding "N-0001" is not acknowledged
    When the dispatch run runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged
    Then the system sends "N-0001" in each of the three files and stays "Generated"
    Then after the third failure a task is raised to the litigation officer team with MSG-GEN-006 naming "WIN"
    Then no ledger append is made for "N-0001"

  Scenario: AC5 The WIN batch fails its check in ACE (legacy RWB-E1-055 AC5)
    Given the ACE batch for source "WIN" of 2026-11-30 has status "FAILED" at its record count check
    Given the rwb-source-data provider fake answers the proof-of-delivery read of 2026-11-30 with 200, no row and a DP07 freshness stamp with status "STALE" and business date 2026-11-23
    When the proof of delivery for 2026-11-30 is read
    Then no notice changes state, no ledger append is made and no NoticeDelivered is written
    Then the notice section shows MSG-P1-001 naming DP07 and 2026-11-23

  Scenario: AC6 Unknown reference held (legacy RWB-E1-055 AC6)
    Given the rwb-source-data provider fake answers the proof-of-delivery read of 2026-11-30 with 30 rows, of which 29 match a "Sent" notice and 1 with barcode "RR000000000TH" and noticeRef "WIN-99999" matches none
    When the proof of delivery is read
    Then 29 notices update their delivery fields and 29 ledger appends are made, one per matched podKey
    Then the unmatched row changes no notice and gets no ledger append
    Then the system holds 1 row on the exception list with check "References"
    # Pending: the published rwb-source-data operation that records and answers the held row (NEW-GAP-F14-7; NEW-GAP-F03-1)

  Scenario: AC7 The same proof of delivery read twice (legacy RWB-E1-055 AC7)
    Given AC2 has run and notice "N-0001" is "Delivered" from the row with podKey {pod_key}
    When the proof of delivery of 2026-11-30 is read again and the same row is returned
    Then no notice changes state a second time, no second NoticeDelivered is written and no second append is sent
    Then the case ledger holds one delivery entry for {pod_key}
    Then the repeat is counted under rule R-UNI-40 (counter of this service Pending: GAP-0580)

  Scenario: AC8 Repeated dispatch run (legacy RWB-E1-055 AC8)
    Given the rwb-integration contract mock returns one outbound item for the file of 2026-11-25
    Given the dispatch run has written notice "N-0001" in the file of 2026-11-25
    When the dispatch run is rerun on 2026-11-25 from the workflow monitor
    Then the second file does not hold "N-0001"

  Scenario: AC10 Repeated delivery record (legacy RWB-E1-055 AC10)
    Given notice "N-0001" is "Delivered" with callback date 2026-11-28 from the row with podKey {pod_key}
    When a later proof-of-delivery read returns the row {pod_key} with barcode "RR123456789TH" and callbackDate 2026-11-28 again
    Then the notice is unchanged, no ledger append is sent and no second NoticeDelivered is written
    Then the system counts the repeat under rule R-UNI-40 (counter of this service Pending: GAP-0580)
    # Pending: a second row with a different podKey for an already delivered barcode (NEW-GAP-F14-8)

  Scenario: AC11 Proof of delivery batch late (legacy RWB-E1-055 AC11)
    Given the WIN batch due on 2026-11-30 is not "COMPLETED" on 2026-12-01 and GET /api/recovery/source-data/v1/data-products/freshness answers DP07 with status "STALE" and business date 2026-11-23
    When a litigation officer opens case "RC-2026-000123" on 2026-12-01
    Then the notice section shows MSG-P1-001 naming DP07 and 2026-11-23

  Scenario: AC12 No barcode three days after sending (exception X6, added in this story) (new, D-RCV-60)
    Given notice "N-0002" is "Sent" with no barcode and sent_date 2026-11-28
    When the daily reconciliation runs on 2026-12-01
    Then the barcode break for notice "N-0002" is listed for the platform administrator

  Scenario: AC13 Read outside the service path (exception X9, added in this story) (new, D-RCV-60)
    Given a caller or a job reads a path outside /api/recovery/comms/v1, or a cross-schema read appears
    When the boundary test runs in the build
    Then the build fails the boundary test and nothing is released

  Scenario: AC14 Decision record cannot be written (exception X10, added in this story) (new, D-RCV-60)
    Given notice "N-0001" is "Generated" and the decision record of the rule cannot be written
    When the dispatch run decides the notice
    Then nothing changes on the notice or the file, the run stops and an incident is raised with MSG-P7-003

  Scenario: AC15 Error answers of the provided operations (added in this story) (new, D-RCV-60)
    When a caller sends a request without valid credentials to a provided operation of /api/recovery/comms/v1
    Then the answer is 401
    When a caller sends a request without the role the operation needs to a provided operation of /api/recovery/comms/v1
    Then the answer is 403
    When a caller sends a request for a notice that does not exist to a provided operation of /api/recovery/comms/v1
    Then the answer is 404

  Scenario: AC16 Activity retry and timeout (added in this story) (new, D-RCV-60)
    Given an activity of the dispatch run fails and is retried under the retry and timeout policy Not specified in the source documents (NEWAC-RWB-P6-E1055-APP-AC16)
    When the retried activity times out
    Then the retry and the timeout follow the policy Not specified in the source documents (NEWAC-RWB-P6-E1055-APP-AC16) and the notice keeps its state until one attempt succeeds

  Scenario: AC17 Consumed call fails or does not answer (added in this story) (new, D-RCV-60)
    Given a consumed call of the dispatch run fails or does not answer
    When the dispatch run makes the call
    Then the notice keeps its state, no outbox event is written for it, and the run records the failed call

  Scenario: AC18 The dispatch entry is appended on the published ledger contract (new, RD-P1-007)
    Given WIN has acknowledged "N-0001" with sent date 26112026 and barcode "RR123456789TH", and {caseId} is the synthetic uuid of case "RC-2026-000123"
    When rwb-comms appends the dispatch entry
    Then POST /api/recovery/source-data/v1/cases/{caseId}/interactions carries header Idempotency-Key (a UUID), eventCode "LETTER", occurredAt on 2026-11-26, actorType "SERVICE", actorRef "rwb-comms", sourceRef "INT-14 WIN", idempotencyKey "LETTER-RC-2026-000123-20261126-{notice record uuid}", channel "LETTER", direction "OUTBOUND", deliveryStatus "SENT", externalRef "RR123456789TH" and conductCheck "PASSED"
    Then the answer is 201, one entry exists, and "rwb.comms.NoticeDispatched.v1" carries ce_idempotencykey equal to that idempotencyKey
    Then rwb-comms writes its own decision record for the dispatch (decision point and rule code Pending: NEW-GAP-F14-5); rwb-source-data writes none for the append

  Scenario: AC19 The ledger append fails and is retried (new, RD-P1-001, RD-P1-007)
    Given the rwb-source-data provider fake answers 503 to the first delivery append for {pod_key} and 201 to the next
    When the delivery matcher processes the row
    Then notice "N-0001" stays "Sent" and no NoticeDelivered is written until an append is answered 201 or 200
    Then the retry sends the same Idempotency-Key header, the same idempotencyKey and the same body, and the ledger holds one entry

  Scenario: AC20 A repeated business key returns the stored entry (new, RD-P1-007)
    Given the delivery entry for {pod_key} is stored and the notice change was not committed
    When rwb-comms sends the same body and idempotencyKey with a new Idempotency-Key header
    Then the answer is 200 with the existing entry, and the notice moves to "Delivered" with one NoticeDelivered

  Scenario: AC21 The ledger refuses the append (new, RD-P1-007)
    Given the rwb-source-data provider fake answers 422 MSG-GEN-002 with a named field to the delivery append for {pod_key}
    When the delivery matcher processes the row
    Then notice "N-0001" keeps state "Sent", no NoticeDelivered is written, no value of the append is truncated and the run records the failed call

  Scenario: AC22 The Section B views are not available (new, RD-P1-007; GAP-0579; ASM-0821)
    Given the flag rwb.dataengine.pod-read is closed and the read answers 200 with rows empty and DP07 freshness "STALE" with a null business date (the reason member is Pending: GAP-0579)
    When rwb-comms reads the proof of delivery
    Then no notice changes state, no ledger append is made, no event is written and no earlier date is read in its place

  Scenario: AC23 The proof-of-delivery read is refused or unavailable (new, RD-P1-007)
    Given the rwb-source-data provider fake answers the proof-of-delivery read with 401, 403, 422 MSG-GEN-001 or 503 MSG-GEN-006
    When the proof of delivery is read
    Then no notice changes state, no append and no event is written, and the run records the status of the failed call
```

The nine criteria AC2 to AC8, AC10 and AC11 are the legacy criteria this slice owns, restated in version 3 on the published rwb-source-data contract (RD-P1-005, RD-P1-007, RD-P1-041); AC12 to AC14 cover exception paths X6, X9 and X10, and AC18 to AC23 the ledger and read paths. Cross-service answers are contract fakes, so the story builds before rwb-source-data, rwb-document and rwb-case are live. **AC1 and AC9 of RWB-E1-055 are not here: they belong to `RWB-ITG-E1055-ITG`**, which proves the file, the acknowledgment, the ledger call and the reconciliation break end to end on the real wave-1 services. TC: AC2, AC3, AC5, AC6, AC7, AC10, AC11 and AC18 to AC23: to be added in Test Cases v9 (W2-tests).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only notices in a dispatch-eligible state are written to the WIN file; Generated in Epic 1, Approved from RWB-E2-014. The eligible state is reference data, never a constant | INT-14; JOB-10; legacy BR1 |
| BR2 | A notice period starts only from the delivery date on the proof of delivery, and the date travels on `rwb.comms.NoticeDelivered.v1` | CTL-15; R-LIT-07; legacy BR2 |
| BR3 | An unacknowledged file is sent again; after the third failure a task goes to the owning team | INT-14 error handling; R-UNI-33, R-UNI-34; legacy BR3 |
| BR4 | A proof-of-delivery row is read only when the ACE batch for source WIN is `COMPLETED` for its business date; a row with an unknown reference is held; the read is made by rwb-source-data and never by rwb-comms | ACE batch record; INT-15 error handling; legacy BR4; DP-05 |
| BR5 | A notice sent with no barcode after three days is a reconciliation break, and the break days are reference data | REC-09 (GAP-1169); legacy BR5 |
| BR6 | The same event twice, and the same proof-of-delivery row twice, produce one effect and the repeat is counted | R-UNI-40; legacy BR6 |
| BR7 | The notice data product is stale when rwb-source-data answers DP07 with status `STALE` (no `LOADED` stamp for the expected business date at its expected-by time, or a failed source), and MSG-P1-001 names the product and the last load date; this service computes no stale period of its own | RD-P1-041; MSG-P1-001; legacy BR7 |
| BR8 (R-LIT-07) | The notice period runs from the delivery date: the proof of delivery is read, the delivery is written on the notice and the timer starts on the event, never on the print date | Temporal and Drools design slide 20 notes (EV-15, R-LIT-07) |
| BR9 (R-LIT-08) | The proof window is 7 days from dispatch: a notice still without proof inside the window is chased by the owning team, and the window itself is RWB-E2-021 | Temporal and Drools design slide 20 notes; RWB-E2-021 |
| BR10 (R-LIT-09) | A delivered-refused or undeliverable letter moves the notice to Unserved and the case to its owner's queue; the rule is evaluated in RWB-E2-021, and this story only records the delivery status the row carries | FSD P6 A2.2 AC-ALT-P6-002-02; RWB-E2-021 |
| BR11 (R-UNI-33) | A downstream system that fails is retried, and the state of the record is not advanced until the retry succeeds | INT-14 error handling; legacy BR3 |
| BR12 (R-UNI-34) | A retried call that passes its limit leaves the record in the exception queue with the reason, and the queue is reviewed by the owning team | INT-14 error handling; legacy BR3 |
| BR13 (R-UNI-40) | The same event or the same source row twice produces one effect, and the repeat is counted | legacy BR6; FSD P6 A2.2 AC7 |
| BR14 | Each dispatch entry and each matched `podKey` is appended once by rwb-comms with a permanent business key; the same value is the `ce_idempotencykey` of the event of that action; rwb-comms records its own decision for the action | RD-P1-007 rules 4, 6 and 7; RD-P1-009 |

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
| RW-PLATADM, platform administrator | Documents R and Litigation absent: reruns the dispatch run and reads the REC-09 breaks on SCR-44 and SCR-45 |
| rwb-comms service identity | Writes the notice, runs the workflow, writes the outbox rows and calls the owners' operations, including the proof-of-delivery read and the ledger append (Case record C); it holds no grant on another schema and no grant on `recovery.v_ace_*` |
| rwb-source-data, rwb-document and rwb-case owner identities | Serve the pod records, the freshness stamp, the ledger operation, the stored letter and the timer; they take no decision in this story |

The rights above are the rows of TSD P6 T6.1 and nothing wider. DP-08 is **not** in the patterns applied to this story: the declared capability area and right on `GET /notices/{noticeId}` are enforced at gateway-bff for the screen path, and where a local guard is required on the operation itself the guard and its story are not named in the sources (GAP-1098; ASM-2046), and the rwb-access authorise check on the operation is Not specified in the source documents (DOR-RWB-P6-E1055-APP-6). A refusal keeps its message MSG-P4-002 and writes no notice change.

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
| DF-ACE-251 to DF-ACE-260 | `ProofOfDeliveryRow` (P1) | podKey, accountKey, noticeRef, sentDate, barcode, callbackDate, deliveryStatus, sentType, sourceSystem, dataAsOf | Read, through `GET /proof-of-delivery` |
| `InteractionRequest` 5.1.0 | interaction (P1) | eventCode, occurredAt, actorType, actorRef, sourceRef, idempotencyKey, channel, direction, conductCheck (dispatch), deliveryStatus, externalRef | Written through the ledger operation of rwb-source-data; no summary and no personal data is sent |

**Indexes and migration.** The dispatch and proof columns arrive in the service's per-service Flyway sequence (DP-15), as `V1055_1__notice_dispatch.sql` by the convention of the service, after the `notice` table of RWB-P6-E1052-APP: it adds `dispatch_file_id` and `dispatch_attempts` (default 0), a unique index on `barcode` where `barcode` is not null, an index on `case_id`, and an index on `sent_date` for the daily reconciliation and the age of an undispatched notice.

**The dispatch file link.** `notice.dispatch_file_id` is a cross-reference to `outbound_item` of rwb-integration (P2), many to 0 or 1 in the TSD P6 T3.3 relationship list. It is stored as an identifier and never as a foreign key across schemas (DP-01), and the file itself is read through the rwb-integration and document contracts, never from a table of this service.

**Personal data.** The fields classed as personal data in this story are Not specified in the source documents (DOR-RWB-P6-E1055-APP-11). The notice row of this story carries identifiers, dates, a barcode, two list values and a counter. The addressee, the address and the contact value never enter `rwb_comms`: they are read by rwb-source-data and leave through its contract into the outbound file stream, and they are not logged and not put on an event. The delivery proof carries the barcode and the dates only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/notices/{noticeId}` | Read a notice with its dispatch and proof-of-delivery fields: state, `sent_date`, `barcode`, `sent_type`, `callback_date`, `delivery_status`, `dispatch_file_id`, `dispatch_attempts`, `hold_reason`, `notice_type` and `template_version` | Litigation R, scope applied (TSD P6 T-A API-P6-002) | Not applicable |
| POST | `/internal/pod-digests` | The internal digest and pod write: the run posts the business date, the feed version (source Pending: NEW-GAP-F14-3), the row count and the digest of the batch it has consumed, under the service identity, and the answer records that the batch was digested once | Service identity only; no Workbench role | Idempotency-Key required; a repeated key returns the first answer and counts the repeat |

The internal operation is not part of the Workbench API surface: it is the service's own write path for the batch it has read, and its path and field names are this story's design, because no source names them. The record fields it touches are DF-LEG-019 to DF-LEG-023 and DF-LEG-033 to DF-LEG-034 only. `GET /notices/{noticeId}` answers 401, 403, 404 and 503 with the platform error envelope and takes no Idempotency-Key.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/proof-of-delivery?businessDate=` | P1 rwb-source-data (RWB-P1-E1055-APP) | `ProofOfDeliveryAnswer`: businessDate, productCode `DP07`, freshness and rows in ascending podKey order; writes nothing and takes no caseId; 400, 401, 403, 422 MSG-GEN-001, 503 MSG-GEN-006, no 404; while the pod-read flag is closed 200 with rows empty and DP07 `STALE` with a null `businessDate`; page parameters Pending (GAP-0577) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1015-CON) | `DataProductFreshness` of DP07: productCode, businessDate (nullable), status `LOADED` or `STALE` (AC5, AC11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (RWB-P1-E1066-CON) | The dispatch entry and one delivery entry per matched podKey; `{caseId}` is the case uuid; header `Idempotency-Key` (UUID, reused on retry); body `InteractionRequest` 5.1.0; 201 new entry, 200 repeated business key, 409 MSG-PLT-N009-05 (key reused with a different body), 422 MSG-GEN-001 or MSG-GEN-002 with the field, 503 |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number of the ledger business key |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document (RWB-P5-E1054-CON) | The stored letter behind `notice.document_id`; the element that returns it is not named in the source documents (GAP-1099; ASM-2047) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case (RWB-P3-E1028-CON) | Observed only, to assert that the `NOTICE_PERIOD` timer started on the delivered date (AC2) |
| The LOV read of the rwb-case reference-data contract | P3 rwb-case (RWB-P3-E1043-CON) | LOV-NOTICE, LOV-DELIVERY and LOV-SENT-TYPE by version, so no list value is in code |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). No row is composed into another: this service never calls a service that calls a third one.

**Ledger entries (RD-P1-007; RD-P1-064).** rwb-comms is the one appender of the dispatch and delivery entries. Both carry eventCode `LETTER`, channel `LETTER`, direction `OUTBOUND`, actorType `SERVICE`, actorRef `rwb-comms` and an idempotencyKey of at most 120 characters. Dispatch, when the WIN file is sent: deliveryStatus `SENT`, externalRef the WIN `barcode` of the notice, conductCheck `PASSED` (a letter is dispatched only after the conduct check passed), sourceRef `INT-14 WIN`, occurredAt the sent date, idempotencyKey `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>`. A letter refused by the conduct check appends conductCheck `BLOCKED` with no deliveryStatus and no externalRef. Delivery, one entry per matched row of `GET /proof-of-delivery`: deliveryStatus from the row, externalRef the row `barcode`, else its `noticeRef` when `barcode` is null (a row with neither is not matched, gets no entry and is logged as unmatched), sourceRef the notice reference (at most 60), occurredAt the `callbackDate` at 00:00 Asia/Bangkok, idempotencyKey `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>` where `<u>` is the UUID version 5 of `podKey` in the RFC 9562 URL namespace (36 characters; the same on every re-read), so no `podKey` length matters. On 503 MSG-P1-022 rwb-comms does not commit its action, or retries with the same header key and business key (rule 13). Pending: the mapping of WIN `delivery_status` to `SENT`, `DELIVERED`, `READ`, `FAILED`, owner rwb-comms owner with the WIN interface owner, tracked as NEW-GAP-D3 (interim: the values of this story's fixture); the occurredAt of a row with no callback date, owner P1 contract owner with the rwb-comms contract owner, tracked as NEW-GAP-F14-9; what a second pod row with a different `podKey` for a delivered barcode does, owner solution architect, tracked as NEW-GAP-F14-8.

**Other rwb-source-data facts.** The postal address and contact value for the INT-14 file are read through `GET /api/recovery/source-data/v1/customers/{personKey}` (`getCustomer`, rwb-source-data.yaml 5.1.0; RD-P1-060), clear only for the rwb-comms notice identity where the masking rule unmasks them (unmask rows Pending, NEW-GAP-D1, owner data protection officer with the rwb-access owner). Pending: the published read that supplies the primary account contract number to rwb-comms, owner solution architect, tracked as NEW-GAP-F14-6.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | caseId | barcode, notice ID, sent date. No addressee, no address, no contact value |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | caseId | notice ID, delivered date, delivery status |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | caseId | decision record reference, rule code, rule version, final call, decided at; written through the local decision-record library where a rule decides |

All three are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; the delivery proof carries the barcode and the dates only.

`NoticeDispatched` and `NoticeDelivered` carry `ce_idempotencykey` equal to the ledger business key of the same action (RD-P1-007 rule 4). rwb-source-data writes no decision record for an append; the decision record of the dispatch and of each delivery is this service's own, and its decision point and rule code are Pending: owner solution architect, tracked as NEW-GAP-F14-5.

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
| `NoticeDispatchWorkflow` | Workflow from the kit template; one per business date and dispatch run | `rwb-comms` | Owns the dispatch run: the eligible set, the file request, the acknowledgment wait and the two events |
| `generateLetter` | Activity, calls rwb-document (P5) | `rwb-comms` | Ensures the letter of each eligible notice exists behind its document ID before the file is built |
| `approveNotice` | Child workflow in rwb-decision (P7) | `rwb-decision` | The approval where a rule decides; its outcome is recorded through the decision-record library before any state change |
| `deliverFile` | Activity, calls rwb-integration (P2) | `rwb-integration` | Delivers the INT-14 file for the business date and returns the `FileDelivered` or `FileFailed` fact |

The workflow is idempotent by business date and notice ID: a retried run does not write a notice into a second file and does not re-send an acknowledged notice.

Workflow ID form: Not specified in the source documents (CG-ALL-6412). Start: a notice request (POST /notices), or a stage workflow that needs a letter (Temporal Catalog v1). Duplicate-start policy: Not specified in the source documents (CG-ALL-6412).

#### 12.6 Schedules

One Schedule, for the in-service part of JOB-10.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The dispatch Schedule of rwb-comms (RWB-PLT-E1071-CON) | 16:00 Asia/Bangkok, daily | SKIP | Catch-up window of the workflow kit | `NoticeDispatchWorkflow` for the business date |

The cross-system edge of JOB-10 is the bank Airflow file window, owned by the platform and by rwb-integration (Architecture v5 slide 44, "Airflow file window + workers"); this story registers the in-service Schedule only and no Quartz row, no job table entry and no Control-M job.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice, its dispatch fields and its proof-of-delivery fields: barcode, callback date and delivery status sit on the notice row; no separate proof table |
| template | P6 (rwb_comms) | The template version the letter of a notice was generated from, read only |
| merge_field | P6 (rwb_comms) | The merge codes of the template catalog, read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox, inbox and idempotency objects of the three published events and the internal write (DP-09) |

Not owned and never read as a table: `document` and `signature_request` (P5), `interaction` (P1, DP-18), `recovery_case`, `timer` and `case_account` (P3), `decision_log_entry` (P7), `outbound_item` (P2). No `v_ace_*` view is read here: the ACE facts arrive through `rwb-source-data.yaml` 5.1.0 (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data provider fake (`rwb-source-data.yaml` 5.1.0) | Proof-of-delivery read: 25 rows with 0 refused for 2026-11-30; the 30-row answer with 29 matchable and 1 unmatched row; the repeated row of 2026-11-28 for barcode `RR123456789TH`; the no-row answer with DP07 `STALE` of 2026-11-23; the Section B unavailable answer; 401, 403, 422, 503. Freshness: `LOADED` and `STALE`. Ledger: 201, 200, 409, 422 and 503 | AC2, AC3, AC5, AC6, AC7, AC10, AC11, AC18 to AC23 |
| rwb-document PDF fake (RWB-P5-E1054-CON) | The stored letter of notice `N-0001` behind its document ID, and a stored letter per notice of the fixture set | AC2, AC4, AC8 |
| rwb-case timer fake (RWB-P3-E1028-CON) | A running `NOTICE_PERIOD` timer on case `RC-2026-000123` started on 2026-11-28, and no timer on 2026-11-26 | AC2 |
| rwb-integration WIN file fake | One `outbound_item` for the file of 2026-11-25 in state ACKNOWLEDGED, one unacknowledged file per run of 2026-11-26 to 2026-11-28, and one `FileFailed` on each failed attempt; the acknowledgment record carries sent date 26112026, barcode `RR123456789TH` and sent type `NPL` for contract `CT-77001` | AC4, AC8 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the baseline is a build failure (RWB-P6-E1055-CON).

Proof of delivery is held behind the rwb-source-data flag `rwb.dataengine.pod-read` until RWB-ACE-001 lands and `v_ace_pod` is available; the fallback (proof entered by hand against the barcode) is agreed with the litigation business owner before wave 2 (GAP-1608). While the flag is closed or the views are not deployed, the read answers 200 with rows empty and DP07 `STALE` with a null `businessDate`; the answer has no member for the reason, which is Pending (RD-P1-043; GAP-0579; ASM-0821). It never returns a guessed date and never falls back to data_as_of.

The proof-of-delivery read writes nothing and takes no caseId. rwb-comms matches each row to a notice and appends the delivery entry itself; it is the only writer-caller of delivery entries (RD-P1-007 rule 7; RD-P1-021). rwb-source-data counts DP07 repeats in its metric `rwb_source_data_win_delivery_repeat_total`; where rwb-comms records its own idempotency hit is Pending (GAP-0580).

On a match the delivery date is set on the notice and EV-15 NoticeDelivered is published from rwb-comms. No new event and no new job is introduced.

The WIN file layout is not stated in any source. The dispatch is built against the rwb-integration WIN file fake until the INT-14 file layout is held as a versioned interface definition and agreed with the WIN owner before wave 2 (GAP-1602).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 7 consumed | The notice read and the internal digest write; proof-of-delivery read, freshness, ledger append, case read, document, timers and the reference read; one hop and 2 s each |
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

DP-05 applies only as a prohibition: this service reads no ACE view, and the primary account contract number, the address and the pod arrive through `rwb-source-data.yaml` 5.1.0. DP-18 applies as "the LETTER entry is written through the interaction operation of rwb-source-data", never through a table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeDispatchController | Controller | `GET /notices/{noticeId}` with the problem mapping for 401, 403, 404 and 503 |
| PodDigestController | Controller | `POST /internal/pod-digests`; service identity only, Idempotency-Key required |
| NoticeReader | Service | Builds the notice answer with the dispatch and proof fields from `rwb_comms` only |
| NoticeDispatchWorkflow | Workflow | The dispatch run of section 4: eligible set, file request, acknowledgment wait, events |
| WinNoticeFileWriter | Service | Builds the INT-14 record set and its trailer from the notice rows and the template version in force |
| WinAcknowledgmentHandler | Service | Applies the acknowledgment: state Sent, `sent_date`, `barcode`, `sent_type`, the ledger entry and `NoticeDispatched` |
| ProofOfDeliveryReader | Service | Calls the proof-of-delivery read for the business date (the completeness gate is inside that read) and matches by barcode and then by `noticeRef` |
| DeliveryMatcher | Service | Matches a row to one notice, appends the delivery entry, then writes the delivery fields and `NoticeDelivered`, and counts the repeat |
| PodDigestWriter | Service | Writes the digest of a batch once, under the idempotency key, and refuses a second digest of the same batch |
| BarcodeReconciliation | Job inside the service | The daily REC-09 check after the batch is complete, with the break days read as data |
| NoticeEventPublisher | Service | Writes the outbox rows of the three events |

**Database and migrations.** The `notice`, `template`, `merge_field` and library objects live in `rwb_comms` (RWB-P6-E1052-APP and RWB-P6-E1046-APP own their baseline); this story adds `V1055_1__notice_dispatch.sql` with `dispatch_file_id`, `dispatch_attempts` and the three indexes of section 11. No column is added for another service's data.

**Configuration and reference data.** `rwb.comms.dispatch.eligible-states` = `GENERATED`; `rwb.comms.dispatch.max-attempts` = 3; `rwb.comms.dispatch.barcode-break-days` = 3. All three are reference data read with their version through the rwb-case reference-data contract (DP-07), owned by the platform administrator, and none is compiled into the service. The former `rwb.comms.pod.stale-after-business-days` is not built: staleness is the status rwb-source-data answers.

**Build steps**

1. Write the migration and test the unique index on `barcode` and the two query indexes.
2. Build `WinNoticeFileWriter` against the INT-14 record set and the trailer, with three synthetic notices.
3. Build `NoticeDispatchWorkflow` with the Schedule hook, the idempotency rule by business date and notice ID, and the attempt count; test AC4 and AC8.
4. Build `WinAcknowledgmentHandler` with the ledger call and `NoticeDispatched`; test the Sent fields against the fake.
5. Build `ProofOfDeliveryReader` and `DeliveryMatcher` over the rwb-source-data contract, with the ledger append, the held row, the repeat count and `NoticeDelivered`; test AC2, AC3, AC5, AC6, AC7 and AC10.
6. Build `PodDigestWriter` and the internal operation, with the repeated-batch test.
7. Build `BarcodeReconciliation` and the DP07 STALE status read; test the break list and the late batch of AC11.
8. Build `NoticeReader` and the notice answer over the contract fake, then the contract test against the real service in SIT.

**Feature flag.** `rwb.comms.win-dispatch-v1`, read as a flag of the platform library; off means no notice is written to a file and the pod read does not change a notice.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E1055-CON stay green, and a SIT week shows one file per business date, one dispatch event per acknowledged notice, one delivery per row, no notice in a second file of the same date and no notice whose delivery came from a table of this service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt, or a consumed system cannot complete a call | {system} is not available. Try again in a few minutes. |
| MSG-P1-001 | DP07 is `STALE` | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the Litigation right reads the notice | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written where a rule decided | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The texts are those of Error and Message Standard v6. The values the tests assert are "DEMAND was sent for registered mail on 26 November 2026." for MSG-P6-004, "{system} is not available. Try again in a few minutes." with WIN named for MSG-GEN-006, and MSG-P1-001 with the catalogue product name of DP07 and 2026-11-23 (the legacy fixture 'DP07 Legal' stays test data; rendering GAP-0581).

### 15. Screens and states

No screen is built in this story. Three existing surfaces show what it writes, through the gateway-bff composite route (DP-19):

| Surface | What it shows |
|---|---|
| SCR-03 Case record, notice panel (state read only) | Notice state, sent date, barcode, callback date and the delivery status read from this service |
| SCR-30 Case documents | The stored letter behind the document ID and its link to the notice |
| SCR-44 Interface and job monitor | The dispatch run and the pod read in the states Running; failed; complete, with the file ID and the attempt count |
| SCR-45 Data quality | The held row with check `References` and the REC-09 break, in state breaks |

The route merges the answer of this service with rwb-document and rwb-case; the screen field lists and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories, not here.

States of each screen (Screen Specifications v1): SCR-03 is read only, with loading; empty, error and no access are Not specified in the source documents (CG-ALL-6420). SCR-30 has loading; empty, error and no access are Not specified in the source documents (CG-ALL-6421). SCR-44 has the states Running, failed and complete above; empty, loading, error and no access are Not specified in the source documents (CG-ALL-6422). SCR-45 is in state breaks, with loading; empty, error and no access are Not specified in the source documents (CG-ALL-6423).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | BR1 (AC1; run by RWB-ITG-E1055-ITG) | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | End to end | pod record for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-P6-E1055-APP-03 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-P6-E1055-APP-04 | AC5, BR4 | End to end | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | End to end | 30 rows, 1 unknown |
| TC-P6-E1055-APP-06 | AC7 | End to end | pod records of 2026-11-30 read twice |
| TC-E1-055-08 | AC8 | End to end | Dispatch run rerun on 2026-11-25 |
| TC-E1-055-09 | BR5 (AC9; run by RWB-ITG-E1055-ITG) | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-P6-E1055-APP-07 | AC10, BR6 | End to end | Repeat of RR123456789TH on 2026-12-07 |
| TC-P6-E1055-APP-08 | AC11, BR7 | End to end | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |
| TC-E1-055-13 | AC12 (X6) | End to end | N-0002 with no barcode sent on 2026-11-28, read on 2026-12-01 |
| TC-E1-055-14 | AC13 (X9) | Component | Caller reads a path outside /api/recovery/comms/v1 |
| TC-E1-055-15 | AC14 (X10) | Component | Decision record cannot be written for N-0001 in state Generated |
| TC-E1-055-16 | Contract test of section 12 | Contract | Every operation, event and activity of section 12 against its consumer and producer contract |
| TC-E1-055-17 | Boundary test of section 12.7 (ASM-3438) | Boundary | Each table of section 12.7 read or written only by its owner |
| TC-E1-055-18 | AC15 | Component | Not specified in the source documents (NEWAC-RWB-P6-E1055-APP-AC15) |
| TC-E1-055-19 | AC16 | Component | Not specified in the source documents (NEWAC-RWB-P6-E1055-APP-AC16) |
| TC-E1-055-20 | AC17 | Component | Not specified in the source documents (NEWAC-RWB-P6-E1055-APP-AC17) |

TC-E1-055-01 and TC-E1-055-09 exercise legacy AC1 and AC9, which are run by `RWB-ITG-E1055-ITG`; they are marked run by that story and are not owned here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

Version 3 changes AC2, AC3, AC5, AC6, AC7, AC10 and AC11 and adds AC18 to AC23: TC: TC-P6-E1055-APP-09, TC-P6-E1055-APP-10, TC-P6-E1055-APP-11, TC-P6-E1055-APP-12, TC-P6-E1055-APP-13, TC-P6-E1055-APP-14, TC-P6-E1055-APP-01, TC-E1-055-02, TC-P6-E1055-APP-02, TC-E1-055-03, TC-P6-E1055-APP-04, TC-P6-E1055-APP-05, TC-E1-055-06, TC-P6-E1055-APP-06, TC-P6-E1055-APP-07, TC-P6-E1055-APP-08 (Test Cases v9). The v8 text of TC-E1-055-02, 03, 05, 06, 07, 10 and 11 is superseded where it differs from section 7.

Version 3: rows that cite `TC-P6-E1055-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in code: the eligible state, the attempt limit, the break days, the hold reasons and the list values are reference data read with their version; no role, list value, state name or number appears in Java.
- No personal data in events, logs, workflow inputs or tests: the notice row carries identifiers, dates, a barcode and list values only; the addressee, the address and the contact value never enter `rwb_comms`, are never logged and are not put on an event.
- ACE data only through the owner's contract: the pod, the batch status, the account contract number and the contact value arrive through `rwb-source-data.yaml` 5.1.0, and this service holds no grant on any `v_ace_*` view (DP-05).
- No read of another service's tables and no cross-schema join: the letter is read on the document contract, the ledger is written through the rwb-source-data operation, the timer is rwb-case's and the file is rwb-integration's (DP-01, DP-18).
- Files move only through rwb-integration: no component calls WIN, and the `deliverFile` activity is the only path to the edge (REQ-DRI-006).
- One hop and a 2 s budget per consumed call, with one GET retry with jitter and a breaker per downstream; no call chain.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only; a consumer dedupes through its inbox (DP-09).
- The decision is never recorded after the effect: where a rule decides, the record is written first through the library, and a failed write stops the run (MSG-P7-003).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-02 to TC-E1-055-08, TC-P6-E1055-APP-07, TC-P6-E1055-APP-08, TC-E1-055-13, TC-E1-055-15 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-02, TC-E1-055-12 |
| REQ-DRI-006 | No direct call to a system of record; ACE data is read through the owner's contract and files move only through rwb-integration | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; ADR-020; DP-05 | TC-E1-055-03, TC-P6-E1055-APP-04, TC-E1-055-06, TC-P6-E1055-APP-06, TC-E1-055-14, TC-E1-055-16, TC-E1-055-17 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-055 | The dispatch and proof-of-delivery loop of the notice; AC2 to AC8 and AC10 to AC11 owned here, AC1 and AC9 owned by RWB-ITG-E1055-ITG |
| DP-01 | The notice lives in `rwb_comms`; the letter, the ledger, the timer and the file item are read through their owners |
| DP-05 | The pod, the batch status and the account facts arrive through `rwb-source-data.yaml` 5.1.0, and no ACE view is read here |
| DP-07 | The notice type, the template version and the two lists are reference data with a version |
| DP-09 | Three events published from the outbox and three consumed through the inbox, with CloudEvents |
| DP-10 | JOB-10 runs as the dispatch Schedule plus the workflow, not as a Quartz row |
| DP-11 | Seven consumed operations, one hop and 2 s each |
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

### 20. Remaining delivery steps

- Size, epic design sign-off: Not specified / Pending. Owner: squad and solution architect.
- CON story RWB-P6-E1055-CON Done and its version published: Pending. Owner: contract owner.
- rwb-source-data.yaml 5.1.0 provider fake published with the proof-of-delivery, freshness and ledger answers of section 12.8: Pending. Owner: P1 contract owner.
- Proof-of-delivery read right and Case record C for the rwb-comms workload identity granted: Pending. Owner: platform administrator.
- Close NEW-GAP-F14-3 to NEW-GAP-F14-9, NEW-GAP-D1 and NEW-GAP-D3 before build of the affected paths; update the AC2, AC18 and AC21 data in Test Cases v9 to RD-P1-064: Pending. Owner: solution architect and QA.
- Test case rows in Test Cases v9 and synthetic fixture data in DEV: Pending. Owner: QA.
