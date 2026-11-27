# RWB-ITG-E1055-ITG Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1055-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-16); the squad sizes at refinement |
| Contract version | /v1 (the path version of each operation in section 12.2) |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P5-E1054-APP, RWB-P3-E1028-APP, RWB-P1-E1066-APP, RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P1-E1055-APP |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E1054-APP, RWB-P3-E1028-APP, RWB-P1-E1066-APP, RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P1-E1055-APP |
| External dependencies | RWB-ACE-001 Section B view v_ace_pod (DL43 open); proof-of-delivery capture stays behind feature flag rwb.dataengine.pod-read until the view is available. Fallback (proof entered by hand against the barcode) to be agreed with the litigation business owner before wave 2 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-055 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1055-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 26 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer on the wave 1 release**, I want **JOB-10 WIN dispatch and the whole proof-of-delivery capture proved end to end on the real wave-1 SIT services before wave 1 exits — the 16:00 file through rwb-integration to the stubbed WIN edge, the acknowledgment that makes the notice Sent, the INT-15 proof file that ACE ingests and rwb-source-data serves, the Delivered notice and its ledger entry, and the NOTICE_PERIOD timer that rwb-case starts from the delivery date**, so that **a notice period is never counted from the print date, no notice is sent twice into a second file, and every freshness, held-row and reconciliation break of the loop is evidenced on the owners' published contracts rather than found in production**.

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. The legacy story fixed one loop for that: a daily 16:00 file to WIN, an acknowledgment that sets the notice Sent, a weekly proof file that ACE ingests and the Workbench reads back, a delivery fact on the notice, a ledger entry, and a notice period that starts on the delivery date. In the target that loop is no longer one process over one schema. rwb-comms owns the notice and the dispatch workflow, rwb-integration owns the file and executes `deliverFile` on queue `rwb-integration`, rwb-document holds the letter behind a document ID, rwb-source-data is the single reader of the `recovery.v_ace_*` views and the single owner of the pod, freshness and interaction facts, and rwb-case owns the NOTICE_PERIOD timer that starts on the event (DP-01, DP-05, DP-09, DP-10, DP-15, DP-18).

Every one of those edges fails in a way no single-service suite can see: a notice that stays Sent because the acknowledgment landed on the wrong base, a second file built for one rerun, a pod row read while the ACE batch for the date is not COMPLETE, two deliveries for one pod row, a timer started on the sent date, or a held row that nobody lists. This story is the end-to-end proof of the loop on the wave-1 services, and it is the evidence the wave 1 exit check reads.

It serves REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006, it carries CTL-15 and the reconciliation rule REC-09 (notice barcodes) into evidence, and it holds the FSD P6 measure "notices with proof of delivery, 100 percent". It exercises the loop the way the services are built: every read is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), the dispatch and delivery facts are consumed as Kafka events from the owner's topic and deduped through the inbox (DP-09), reference data such as the notice type and template version is read through the owning contract (DP-07), the ledger is rwb-source-data's and never a table (DP-18), the 16:00 run is the Airflow file window plus the P6 workflow rather than a Quartz row (DP-10), and the job and data-quality surfaces are reached through the gateway-bff composite route (DP-19). The suite provides no REST operation, publishes no event and owns no table.

### 3. Preconditions

- RWB-P6-E1055-APP is done in SIT: rwb-comms holds the notice state, dispatch_file_id, dispatch_attempts and the WIN acknowledgment handling, publishes `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` on `rwb.comms.events.v1`, and serves `GET /api/recovery/comms/v1/notices/{noticeId}`.
- RWB-P3-E1055-APP is done: rwb-case consumes `rwb.comms.NoticeDelivered.v1` through its inbox and starts the NOTICE_PERIOD timer from the delivered date, and serves `GET /api/recovery/case/v1/cases/{caseId}/timers`.
- RWB-P1-E1055-APP is done: rwb-source-data serves the pod records and the freshness stamp of the WIN proof-of-delivery data product, and holds the pod read behind the ACE batch completeness check.
- RWB-P1-E1066-APP is done: the interaction ledger is written and read on `POST /api/recovery/source-data/v1/cases/{caseId}/interactions`, and the data-quality exceptions are listed on `GET /api/recovery/source-data/v1/admin/data-quality/exceptions`.
- RWB-P3-E1028-APP is done: the NOTICE_PERIOD timer type exists in rwb-case and is visible through the timers read.
- RWB-P5-E1054-APP and RWB-P5-E1055-APP are done: rwb-document stores the WIN letter generated for the notice and returns the document ID, readable with `GET /api/recovery/document/v1/documents/{documentId}`.
- The P6 contract is published, and the seven integration dependencies above are the real services in SIT; this story builds against no contract and waits for none.
- The dispatch-eligible notice states are set to GENERATED and the attempt limit to 3 in the owning configuration; both are data in the P6 configuration and are read, never set, by this story.
- The external boundary is the stubbed WIN folder and acknowledgment at the P2 edge. The folder layout, the acknowledgment file naming and its record keys are harness configuration; they follow the WIN INT-14 and INT-15 contract and are named in the run report.
- The SIT fixture set of section 13 is loaded: case `RC-2026-000123`, notices `N-0001` and `N-0002` in state Generated with notice type DEMAND and primary account contract CT-77001, the WIN owner's sample file `WIN-POD-SAMPLE-v1` of 25 records, the 30-row pod batch of 2026-11-30 with one unknown row, and the second pod row of 2026-11-28.
- The run uses the per-service logins of the wave-1 services (DP-15); no service login is shared and the suite holds no grant on any `rwb_*` schema.
- No build dependency and no contract dependency: Day 1, against the real services as soon as the seven APP stories are live in SIT.

### 4. Flow

1. The harness resets the wave-1 SIT fixtures and loads the fixture set of section 13: the case `RC-2026-000123`, notices `N-0001` and `N-0002` in state Generated with notice type DEMAND and contract CT-77001, the WIN sample file `WIN-POD-SAMPLE-v1`, the 30-row pod batch of 2026-11-30 and the repeat pod row of 2026-11-28, all seeded through the owners' published operations only.
2. The harness opens the WIN file window at 16:00 on 2026-11-25 the way the Airflow window opens it and lets rwb-comms ask rwb-integration for the INT-14 file for that business date.
3. rwb-comms builds the file from its own notice rows for the dispatch-eligible state, sets `dispatch_file_id` and increments `dispatch_attempts`, and asks rwb-integration to deliver it.
4. rwb-integration executes the `deliverFile` activity on queue `rwb-integration`, stores the letter behind a document ID in rwb-document, and records one `outbound_item` for INT-14 and 2026-11-25.
5. The harness reads the item on `GET /api/recovery/integration/v1/admin/outbound-items` and the file on `GET /api/recovery/document/v1/documents/{documentId}`, and asserts `N-0001` and `N-0002` each appear once in the file of 2026-11-25.
6. The harness drops the acknowledgment for contract CT-77001 — sent date 26112026, barcode `RR123456789TH`, sent type NPL — at the stubbed P2 edge, the way the WIN acknowledgment arrives.
7. The harness asserts `GET /api/recovery/comms/v1/notices/N-0001` returns state Sent, sent date 2026-11-26 and barcode `RR123456789TH`, and that the ledger call to `POST /api/recovery/source-data/v1/cases/RC-2026-000123/interactions` arrives once with direction OUT, channel LETTER and the date 2026-11-26 (AC1).
8. The harness consumes `rwb.comms.events.v1` and asserts one `rwb.comms.NoticeDispatched.v1` for `N-0001` with the barcode and the sent date, keyed by the case ID, with no personal data in the payload (AC1).
9. The harness reruns `NoticeDispatchWorkflow` on 2026-11-25 from the job monitor, and asserts the second file does not hold `N-0001` and no second `outbound_item` exists for the date (AC8).
10. The harness withholds the acknowledgment on the runs of 2026-11-26, 2026-11-27 and 2026-11-28, and asserts `N-0001` stays Generated, three files are recorded for it, and after the third failure one open task carries MSG-GEN-006 naming WIN (AC4).
11. The harness sets the ACE batch for source WIN of 2026-11-30 COMPLETE, loads the sample file `WIN-POD-SAMPLE-v1` through ACE ingestion, reads it on `GET /api/recovery/source-data/v1/data-products/DP07/records`, and reads `GET /api/recovery/source-data/v1/data-products/freshness` for the feed version (AC3).
12. The harness loads the 30-row pod batch of 2026-11-30 with one row of barcode `RR000000000TH` and notice_ref `WIN-99999`, lets the pod read run, and asserts 29 notices update, 1 row is held with check References on the data-quality exceptions read, one delivery per notice, and the repeat counted (AC6, AC7).
13. The harness asserts the delivery outcome for `N-0001`: state Delivered with delivery status DELIVERED and callback date 2026-11-28, one ledger entry with the delivered date 2026-11-28 written by rwb-source-data on the proof-of-delivery read that names caseId `RC-2026-000123` (a read without caseId writes nothing), one `rwb.comms.NoticeDelivered.v1` on `rwb.comms.events.v1`, and a running NOTICE_PERIOD timer on `GET /api/recovery/case/v1/cases/RC-2026-000123/timers` started on 2026-11-28 (AC2).
14. The harness loads the second pod row of 2026-11-28 for barcode `RR123456789TH` and asserts the notice is unchanged, no second `NoticeDelivered` is consumed, and the repeat is counted under R-UNI-40 (AC10).
15. The harness sets the ACE batch of 2026-11-30 FAILED at its record count check (AC5) and then leaves the batch due on 2026-11-30 not COMPLETE on 2026-12-01 (AC11); it asserts no pod row of the date is read, no notice changes state, and the freshness answer carries MSG-P1-001 naming DP07 and 2026-11-23.
16. The harness runs REC-09 on 2026-11-28 with `N-0002` still carrying no barcode, and asserts the break is listed and visible on SCR-45 through the data-quality exceptions read (AC9).
17. The harness repeats the dispatch with rwb-integration returning `rwb.integration.FileFailed.v1` on the first attempt, waits for the retry at the interval in force, and asserts the retry succeeds, one item is ACKNOWLEDGED, one `rwb.integration.FileDelivered.v1` is consumed, and the file carries `N-0001` once (AC13).
18. The harness repeats the reads as a caller in role RW-PHONECOL, asserts status 403 with MSG-P4-002 and no state change (AC12), then runs the boundary check of section 13 and publishes the run report with the counts, the fixture versions and the contract versions.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The stubbed WIN folder does not pick the file up inside the run window | The run fails and the report names the window, the business date and the file ID; no criterion is marked passed | None | AC1 |
| X2 | The acknowledgment fixture is dropped twice for one file | The owner's inbox dedupes it; the harness asserts one Sent state and one `NoticeDispatched`, and fails the run on a second effect | None | AC7 |
| X3 | A pod row names an unknown barcode and notice_ref | The row is held on the data-quality exception list with check References and the rest of the batch is read | None | AC6 |
| X4 | The ACE batch for source WIN is not COMPLETE for the business date | No pod row of that date is read, earlier delivery data stays, and the notice data product answers with the stale marker | MSG-P1-001 | AC5, AC11 |
| X5 | rwb-source-data does not answer inside the 2 s budget | One GET retry with jitter, then the step fails and the run fails; the harness never asserts on a partial answer | None | AC3 |
| X6 | A caller in a role without the Litigation R right | The owner refuses with 403 and MSG-P4-002; nothing changes | MSG-P4-002 | AC12 |
| X7 | The same pod rows are read twice | One delivery is recorded per notice and the repeat is counted; no notice changes state a second time | None | AC7, AC10 |
| X8 | rwb-integration raises FileFailed or the acknowledgment times out | The retry runs at the interval in force; one outbound item and one letter exist at the end | MSG-GEN-006 | AC13, AC4 |
| X9 | A service answers outside `/api/recovery/<short>/v1`, or a cross-schema read appears in the run | The boundary check fails the run before the report is written | None | AC14 |
| X10 | The clock is not held for a date-dependent criterion | The run fails before the assertion and names the date and the criterion; the harness never waits on the wall clock | None | AC9, AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the real wave-1 services already in SIT; the suite builds no operation, publishes no event and owns no table. The seven integration dependencies are the services it exercises |
| Negotiable | The fixture set, the window call, the stub shape and the expected counts are harness configuration; the business values are the legacy ones and are not changed |
| Valuable | The loop that decides when a notice period starts is proved on the real services before wave 1 exits, including the freshness gate, the held row and the reconciliation break |
| Estimable | One harness, one fixture set, one boundary check and one run report; no production code and no schema |
| Small | Fits one sprint with the fixture set and the two external stubs |
| Testable | Each owned criterion has a test case in section 16, and every assertion is made on a REST answer, an event or a job artefact |

### 7. Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN, end to end

  Background:
    Given the dispatch-eligible notice states are "GENERATED"
    Given notice "N-0001" for case "RC-2026-000123" is in state "Generated" with notice type "DEMAND" and primary account contract "CT-77001"
    Given every service in the run is the real wave-1 service on its own base /api/recovery/<short>/v1
    Given the WIN folder and the WIN acknowledgment are the stubbed external boundary at the P2 edge

  Scenario: AC1 Dispatched (legacy RWB-E1-055 AC1)
    Given NoticeDispatchWorkflow runs at 16:00 on 2026-11-25
    When WIN acknowledges the file with sent date 26112026, barcode "RR123456789TH" and sent type "NPL" for contract "CT-77001"
    Then notice "N-0001" has state "Sent", sent date 2026-11-26 and barcode "RR123456789TH"
    Then the interaction ledger has an outbound "LETTER" entry for case "RC-2026-000123" on 2026-11-26
    Then the system writes noticeDispatched to the outbox with notice "N-0001", barcode "RR123456789TH" and sent date 2026-11-26
    Then the case record shows MSG-P6-004 "DEMAND was sent for registered mail on 26 November 2026."

  Scenario: AC2 A proof of delivery becomes one Delivered notice, one ledger entry and one P3 timer (new, D-RCV-60)
    Given notice "N-0001" is "Sent" with barcode "RR123456789TH" and sent date 2026-11-26
    When the proof of delivery for business date 2026-11-30 is read and holds barcode "RR123456789TH" with callback_date 2026-11-28
    Then GET /api/recovery/comms/v1/notices/N-0001 returns state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28
    Then one rwb.comms.NoticeDelivered.v1 is consumed on rwb.comms.events.v1 with delivered date 2026-11-28 and no personal data in the payload
    Then the interaction ledger of case "RC-2026-000123" holds exactly one delivery entry, written by rwb-source-data through its ledger writer on the proof-of-delivery read that names that caseId, with direction "OUT", channel "LETTER" and the date 2026-11-28
    Then GET /api/recovery/case/v1/cases/RC-2026-000123/timers returns a running "NOTICE_PERIOD" timer started on 2026-11-28 and not on 2026-11-26

  Scenario: AC3 The WIN sample file is ingested by ACE and read through rwb-source-data (new, D-RCV-60)
    Given the sample INT-15 file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner is loaded for business date 2026-11-30
    When ACE ingests it and the proof of delivery is read through GET /api/recovery/source-data/v1/data-products/DP07/records
    Then the read returns 25 of 25 rows and 0 refused
    Then GET /api/recovery/source-data/v1/data-products/freshness returns product "DP07 Legal" for 2026-11-30 with feed_version "WIN-POD-SAMPLE-v1" and status "COMPLETE"

  Scenario: AC4 A file WIN does not acknowledge is sent again for three runs and then a task is raised (new, D-RCV-60)
    Given the WIN file of 2026-11-25 holding "N-0001" is not acknowledged
    When NoticeDispatchWorkflow runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged
    Then GET /api/recovery/comms/v1/notices/N-0001 still returns state "Generated"
    Then three files are recorded for "N-0001" on GET /api/recovery/integration/v1/admin/outbound-items, one per run
    Then after the third failure one open task is raised to the litigation officer team with MSG-GEN-006 naming "WIN"

  Scenario: AC5 A failed WIN batch is not read and the notice data product shows stale (new, D-RCV-60)
    Given the ACE batch for source "WIN" of 2026-11-30 has status "FAILED" at its record count check
    When the proof of delivery for 2026-11-30 is read through rwb-source-data
    Then GET /api/recovery/source-data/v1/data-products/DP07/records returns no pod row of 2026-11-30
    Then no notice changes state and GET /api/recovery/comms/v1/notices/N-0001 still returns state "Sent"
    Then GET /api/recovery/source-data/v1/data-products/freshness shows the stale marker with status STALE and MSG-P1-001 naming "DP07" and 2026-11-23
    Then GET /api/recovery/source-data/v1/data-products/DP07/records returns 200 with the ten pod fields marked not available with reason SECTION_B_NOT_DEPLOYED while flag rwb.dataengine.pod-read is off

  Scenario: AC6 One unknown pod row is held and 29 notices update (new, D-RCV-60)
    Given the WIN batch of 2026-11-30 holds 30 rows and 1 row has barcode "RR000000000TH" and notice_ref "WIN-99999" matching no notice
    When the proof of delivery is read through rwb-source-data
    Then 29 notices update their delivery fields and reach state "Delivered"
    Then GET /api/recovery/source-data/v1/admin/data-quality/exceptions returns 1 held row with check "References"

  Scenario: AC7 The same pod rows read twice produce one delivery and the repeat is counted (new, D-RCV-60)
    Given the pod rows for business date 2026-11-30 have been read once
    When the same rows are read again on the same business date
    Then one delivery is recorded for "N-0001" and the repeat is counted under rule R-UNI-40 in data_product_load.duplicate_count of the DP07 stamp of that business date, one increment per repeat read, with no second ledger entry
    Then no notice changes state a second time and no second noticeDelivered reaches the outbox

  Scenario: AC8 A repeated NoticeDispatchWorkflow run writes no second file (new, D-RCV-60)
    Given NoticeDispatchWorkflow has written notice "N-0001" in the file of 2026-11-25
    When NoticeDispatchWorkflow is run again on 2026-11-25 from the job monitor
    Then the file of 2026-11-25 holds "N-0001" once
    Then no second outbound item exists for 2026-11-25 on GET /api/recovery/integration/v1/admin/outbound-items

  Scenario: AC9 Barcode missing after three days (legacy RWB-E1-055 AC9)
    Given notice "N-0002" was in the file of 2026-11-25 and no barcode has returned
    When the daily reconciliation REC-09 runs on 2026-11-28
    Then the system lists "N-0002" as a break for the platform administrator on SCR-45

  Scenario: AC10 A repeated pod row for an already Delivered notice changes nothing and writes no second NoticeDelivered (new, D-RCV-60)
    Given notice "N-0001" is "Delivered" with callback date 2026-11-28
    When the pod rows hold a second row with barcode "RR123456789TH" and callback_date 2026-11-28
    Then GET /api/recovery/comms/v1/notices/N-0001 is unchanged and still returns callback date 2026-11-28
    Then no second rwb.comms.NoticeDelivered.v1 is consumed on rwb.comms.events.v1
    Then the repeat is counted under rule R-UNI-40 in data_product_load.duplicate_count of the DP07 stamp of that business date, one increment per repeat read, with no second ledger entry

  Scenario: AC11 A late proof-of-delivery batch shows the stale marker (new, D-RCV-60)
    Given the WIN batch due on 2026-11-30 is not COMPLETE on 2026-12-01
    When the notice of case "RC-2026-000123" is read through the rwb-comms and rwb-source-data contracts on 2026-12-01
    Then GET /api/recovery/source-data/v1/data-products/freshness returns the stale marker for "DP07 Legal"
    Then the notice section shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23

  Scenario: AC12 A role without the Litigation right is refused (new, D-RCV-60)
    Given the caller is role "RW-PHONECOL" with no Litigation R right
    When the caller reads GET /api/recovery/comms/v1/notices/N-0001 and the proof of delivery of 2026-11-30
    Then each answer is status 403 with MSG-P4-002
    Then no notice, pod row, ledger entry or timer changes

  Scenario: AC13 A P2 FileFailed or acknowledgment timeout is retried and never sent twice (new, D-RCV-60)
    Given the WIN file of 2026-11-25 holding "N-0001" is sent and rwb-integration returns rwb.integration.FileFailed.v1 on the first attempt
    When the harness waits for the acknowledgment and the retry runs at the interval in force
    Then the retry succeeds and exactly one outbound item for "N-0001" and 2026-11-25 is "ACKNOWLEDGED"
    Then one rwb.integration.FileDelivered.v1 is consumed on rwb.integration.events.v1
    Then the file of 2026-11-25 carries "N-0001" once and no duplicate letter exists in the file or in rwb-document

  Scenario: AC14 A service answer outside the base path or a cross-schema read fails the run (new, D-RCV-60)
    Given the run is on the real wave-1 services with the boundary check active
    When a service answers outside /api/recovery/<short>/v1 or a cross-schema read appears in the run
    Then the boundary check fails the run before the report is written
```

AC1 and AC9 are the two legacy criteria this story owns and are copied word for word, except that the job in AC1 is named NoticeDispatchWorkflow and the barcode break in AC9 is numbered REC-09, because REC-05 stays the business-key orphan check of RWB-E1-011 (GAP-1169). AC2 to AC8 and AC10 to AC14 are the integration criteria of this slice and are tagged new. The remaining legacy criteria of RWB-E1-055 are owned by RWB-P6-E1055-APP and are re-exercised only inside the end-to-end run of section 13, never restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only notices in a dispatch-eligible state are written to the WIN file: Generated in Epic 1, Approved from RWB-E2-014. In the target the eligible state is configuration in rwb-comms and the suite reads it as data, never assumes it | INT-14; JOB-10; legacy RWB-E1-055 BR1; `rwb.comms.dispatch.eligible-states` |
| BR2 | A notice period starts only from the delivery date on the proof of delivery. The date travels on `rwb.comms.NoticeDelivered.v1` and rwb-case starts the NOTICE_PERIOD timer from the event, so the event date and the timer start date are the same | CTL-15; R-LIT-07; legacy RWB-E1-055 BR2; DP-09 |
| BR3 | An unacknowledged file is sent again by rwb-integration and the notice stays in its dispatch-eligible state; after the third failure a task goes to the owning team | INT-14 error handling; R-UNI-33, R-UNI-34; legacy RWB-E1-055 BR3; DP-10 |
| BR4 | A pod row is read only when the ACE batch for source WIN is COMPLETE for its business date, and the read is made by rwb-source-data, the only service with a grant on `recovery.v_ace_*`; a row with an unknown reference is held | ACE batch record; INT-15 error handling; legacy RWB-E1-055 BR4; DP-05 |
| BR5 | A notice sent with no barcode after three days is a reconciliation break, listed by rwb-source-data and shown on SCR-45 | REC-09; legacy RWB-E1-055 BR5 |
| BR6 | The same event twice, and the same pod row twice, produce one effect and the repeat is counted | R-UNI-40; legacy RWB-E1-055 BR6; DP-09 |
| BR7 | The notice data product is stale one business day after the WIN batch was due, and MSG-P1-001 names the product and the last load date | `v_ace_batch_status`; MSG-P1-001; legacy RWB-E1-055 BR7 |
| BR8 | One hop and a 2 s budget: every call in the run goes from the harness to the owner's base `/api/recovery/<short>/v1`, with one GET retry with jitter, a circuit breaker per downstream and no call chain | Architecture v5 slides 10, 11 and 12; DP-11; ADR-020 |
| BR9 | No service reads another service's tables: the notice is read on `/api/recovery/comms/v1`, the letter and its document ID on `/api/recovery/document/v1`, the outbound item on `/api/recovery/integration/v1`, the pod, the freshness, the ledger and the held rows on `/api/recovery/source-data/v1`, and the timer on `/api/recovery/case/v1`. A cross-schema read or a cross-schema join fails the boundary check of the run | DP-01; Architecture v5 slide 29; ADR-014 |

### 9. State transitions

The notice state, as the suite observes it on the owner's contract:

| From | Event | Condition | To |
|---|---|---|---|
| None | JOB-10 file written | The notice is Generated and not already in a file of the date | Generated, with `dispatch_file_id` set and `dispatch_attempts` incremented |
| Generated | WIN acknowledgment | A barcode returns for contract CT-77001 | Sent |
| Sent | `rwb.comms.NoticeDelivered.v1` content | A callback date is present on the pod row | Delivered |
| Sent | A second acknowledgment or a repeated pod row | The repeat is counted under R-UNI-40 | Sent, unchanged |
| Delivered | A repeated pod row for the same barcode and callback date | The repeat is counted under R-UNI-40 | Delivered, unchanged |

The move to Delivered is made by rwb-comms on its own row, not by this story. rwb-case starts the NOTICE_PERIOD timer when it consumes `rwb.comms.NoticeDelivered.v1` through its inbox, and the timer starts on the delivered date the event carries, 2026-11-28, never on the sent date 2026-11-26. No case status changes in this story: the case stays in the status rwb-case holds for it, and the suite asserts that status before and after the run and fails on any move. The suite sets no state by hand; a state it set itself would prove nothing, so the run report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer, wave 1 release | Owns the harness, the fixtures and the run report; takes no business decision; reads every state through the owner's contract |
| SY-DATALOAD, data load | Runs JOB-10 and the proof of delivery read in SIT through the owner's operations; the harness triggers the run the way the job does (Litigation U) |
| RW-LITOFF, litigation officer | Reads notice state, sent date, barcode and callback date (Litigation R); receives the task after the third failure |
| RW-CASEOWN, case owner | Reads notice state and the notice period timer (Litigation R) |
| RW-PLATADM, platform administrator | Runs and reruns JOB-10 on SCR-44; reads the REC-09 break on SCR-45 |
| RW-DATASTEW, data steward | Reads refused files and held rows on SCR-45 |
| rwb-comms (P6) owner identity | Owns the notice state, the dispatch workflow, the acknowledgment handling and the two events |
| rwb-integration (P2) owner identity | Owns the outbound item and executes `deliverFile` against the WIN folder |
| rwb-source-data (P1) owner identity | Owns the pod read, the freshness stamp, the interaction ledger and the data-quality exceptions |
| rwb-case (P3) owner identity | Owns the NOTICE_PERIOD timer and the task after the third failure |
| rwb-document (P5) owner identity | Owns the stored letter behind the document ID |
| No delegation level applies | The harness takes no approval decision and no authority decision; notice approval is RWB-E2-014 |

### 11. Data

| BR Field ID | Entity | Field | Owning service | Read or write |
|---|---|---|---|---|
| DF-LEG-015 | notice | id | P6 rwb-comms | Read |
| DF-LEG-016 | notice | case_id | P6 rwb-comms | Read |
| DF-LEG-017 | notice | document_id | P6 rwb-comms | Read |
| DF-LEG-018 | notice | notice_type | P6 rwb-comms | Read |
| DF-LEG-019 | notice | sent_date | P6 rwb-comms | Read |
| DF-LEG-020 | notice | barcode | P6 rwb-comms | Read |
| DF-LEG-021 | notice | callback_date | P6 rwb-comms | Read |
| DF-LEG-022 | notice | delivery_status | P6 rwb-comms | Read |
| DF-LEG-023 | notice | sent_type | P6 rwb-comms | Read |
| Standard column | notice | state | P6 rwb-comms | Read |
| DF-LEG-033 | notice | dispatch_file_id | P6 rwb-comms | Read |
| DF-LEG-034 | notice | dispatch_attempts | P6 rwb-comms | Read |
| DF-CAS-027 | case_account | is_primary | P3 rwb-case | Read, through the rwb-case contract |
| DF-ACE-006 | v_ace_account | contract_no | P1 rwb-source-data | Read, through the rwb-source-data contract |
| DF-ACE-078 | v_ace_contact | contact_value | P1 rwb-source-data | Read, into the outbound file stream only, never logged |
| DF-ACE-253 | v_ace_pod | notice_ref | P1 rwb-source-data | Read, through the rwb-source-data pod read |
| DF-ACE-254 | v_ace_pod | sent_date | P1 rwb-source-data | Read |
| DF-ACE-255 | v_ace_pod | barcode | P1 rwb-source-data | Read |
| DF-ACE-256 | v_ace_pod | callback_date | P1 rwb-source-data | Read |
| DF-ACE-257 | v_ace_pod | delivery_status | P1 rwb-source-data | Read |
| DF-ACE-258 | v_ace_pod | sent_type | P1 rwb-source-data | Read |
| DF-REF-047 | template | template_version | P6 rwb-comms | Read, through the rwb-comms contract |
| DF-INT-002 | interaction | case_id | P1 rwb-source-data | Read, through the ledger operation |
| DF-INT-004 | interaction | occurred_at | P1 rwb-source-data | Read, through the ledger operation |
| DF-INT-005 | interaction | channel | P1 rwb-source-data | Read, through the ledger operation |
| DF-INT-006 | interaction | direction | P1 rwb-source-data | Read, through the ledger operation |
| DF-INT-011 | interaction | summary | P1 rwb-source-data | Read, through the ledger operation |

Field IDs are those of the legacy story and the Logical Data Model and Data Dictionary. This story owns no table and writes no row: `notice` and `template` are P6's in schema `rwb_comms`, `outbound_item` is P2's in `rwb_integration`, `case_account` and `timer` are P3's in `rwb_case`, `document` is P5's in `rwb_document`, and the pod, freshness and interaction facts are P1's in `rwb_source_data`. The `recovery.v_ace_*` views named here are read only by rwb-source-data (DP-01, DP-05). The suite reads every field through the owner's published operation; it holds no grant on any `rwb_*` schema and no grant on the views.

### 12. Contract

#### 12.1 REST operations provided

None. This story is a test suite: it proves the dispatch and the proof-of-delivery loop and provides no REST operation. The operations of the loop belong to the P6, P3, P5 and P1 APP stories.

#### 12.2 REST operations consumed

Every call is one hop on the owner's per-service base `/api/recovery/<short>/v1`, with a 2 s timeout, one GET retry with jitter and a circuit breaker per downstream (DP-11, DP-13).

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | Notice state, sent date, barcode, callback date, delivery status and dispatch counters (AC1, AC2, AC4, AC5, AC10, AC12) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The stored letter behind the notice document ID, to prove one letter per notice (AC8, AC13) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The INT-14 items of the business date, their state and attempt count (AC4, AC8, AC13) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The pod records of DP07 for the business date, as rwb-source-data serves them (AC3, AC5, AC6) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness stamp, the feed version and the stale marker of DP07 (AC3, AC5, AC11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The ledger operation rwb-comms writes the dispatch entry through; rwb-source-data writes the delivery entry through its own ledger writer on a read that names caseId; the harness asserts exactly one entry per fact, with its direction, channel, date and summary (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/admin/data-quality/exceptions` | P1 rwb-source-data | The held pod row with check References and the REC-09 breaks (AC6, AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The running NOTICE_PERIOD timer and its start date (AC2, AC12) |

The harness writes nothing through these operations: the POST is the ledger operation rwb-comms calls for the dispatch entry only, and the harness observes that exactly one call arrives per dispatched fact and reads back what the call carried. The delivery entry is written by rwb-source-data inside its proof-of-delivery read, for the caseId named on the read, and the harness asserts exactly one such entry per delivered fact. The suite composes no call: no operation of this table is used to reach another service.

#### 12.3 Events published

None. The suite publishes no Kafka event and writes no outbox row; it consumes the owners' events and puts its result in the run report.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler in the run |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The file was delivered to WIN; asserted once per item, per business date (AC13) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The attempt failed and the retry path is open; asserted on the first attempt (AC13, AC4) |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 rwb-comms | The notice is Sent with barcode and sent date; asserted once per acknowledged notice (AC1, AC8) |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | P6 rwb-comms | The notice is Delivered with the delivered date; asserted once per newly delivered notice and never twice (AC2, AC7, AC10) |

All four are CloudEvents on the owner's topic, keyed by case ID, carrying IDs and facts only; the harness asserts the key and the absence of personal data (DP-09).

#### 12.5 Workflows and activities

Observed only. This story creates, changes and owns no workflow and no activity.

| Name | Type | Task queue | What the run observes |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow, owned by P6 | `rwb-comms` | The dispatch of the notice set for the business date: the file request, the acknowledgment handling and the two events (AC1, AC4, AC8) |
| `deliverFile` | Activity, owned by P2 | `rwb-integration` | The one file delivery for INT-14 and 2026-11-25, its retry on failure and the `FileDelivered` or `FileFailed` fact (AC13) |

The harness never starts, signals or terminates either one. It opens the 16:00 window the way the Airflow task does, drops the acknowledgment and the pod batch at the stubbed edge, and asserts the effects through the contracts and the topic.

#### 12.6 Schedules

None. JOB-10 is not a Temporal Schedule in this design: it is the bank Airflow 16:00 file window that opens the file run, plus the P6 `NoticeDispatchWorkflow` that executes it, as Architecture v5 slide 44 records ("Airflow file window + workers"). The harness creates, moves and owns no Schedule and no cron; it opens the window for the business date under test through the fixture of section 12.8 and records the call in the run report.

#### 12.7 Tables owned

None. The tables of the loop belong to their owners: `notice` and `template` to P6 in `rwb_comms`, `outbound_item` to P2 in `rwb_integration`, `document` to P5 in `rwb_document`, `case_account` and `timer` to P3 in `rwb_case`, and the pod, freshness and interaction facts to P1 in `rwb_source_data`. The suite reads them through the operations of section 12.2 only (DP-01).

#### 12.8 Contract fakes

The run uses the real wave-1 services. The only fakes are the external boundary and the fixtures, and none of them replaces a service:

| Fake or fixture | Boundary | Use in the run |
|---|---|---|
| WIN SFTP folder stub | The P2 edge, outside the bank | Receives the INT-14 file and answers the acknowledgment record (AC1, AC4, AC13) |
| WIN acknowledgment stub | The P2 edge, outside the bank | Emits the acknowledgment with sent date 26112026, barcode `RR123456789TH` and sent type NPL for CT-77001; silent for the unacknowledged runs, and a `FileFailed` answer for the retry criterion (AC1, AC4, AC13) |
| WIN dispatch file layout fake | The P2 edge, outside the bank | Stands in for the INT-14 dispatch file layout until the WIN owner agrees it; the layout is not specified in the source documents (GAP-1602) |
| Pod and freshness fixture | Behind rwb-source-data, loaded through ACE ingestion | The `WIN-POD-SAMPLE-v1` sample of 25 records, the 30-row batch of 2026-11-30 with one unknown row, the second row of 2026-11-28, and the batch states COMPLETE, FAILED and not COMPLETE (AC3, AC5, AC6, AC7, AC10, AC11) |
| Clock control | The environment clock | Holds 2026-11-25 to 2026-12-01 so the three-day REC-09 window and the one-business-day stale window are deterministic (AC9, AC11) |

No real WIN connection is opened, no production data is touched, and the fixture contents, the stub file naming and the acknowledgment record keys are harness configuration named in the run report.

Contract fakes for rwb-case, rwb-comms, rwb-document and rwb-integration (for squads building against this flow before the wave-1 services are deployed): published contract fake library version Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-22).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 8 consumed | Notice read on rwb-comms; document read on rwb-document; outbound items on rwb-integration; pod records, freshness, ledger operation and data-quality exceptions on rwb-source-data; timers on rwb-case; one hop and 2 s each |
| Kafka | 0 published, 4 consumed | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1`; `NoticeDispatched` and `NoticeDelivered` on `rwb.comms.events.v1` |
| Temporal | 1 observed | `NoticeDispatchWorkflow` on queue `rwb-comms`, with the `deliverFile` activity asserted through its effects on queue `rwb-integration` |
| File | 2 | INT-14 outbound WIN letters file, and INT-15 inbound proof-of-delivery file read back through rwb-source-data; no file content in any message or workflow payload |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg.win`, test scope only; it is not part of any deployed service and holds no production code.

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
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H rows of the table above are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The blocking work is the seven integration dependencies: RWB-P6-E1055-APP for the notice state, the dispatch workflow and the two events; RWB-P3-E1055-APP for the timer; RWB-P3-E1028-APP for the timer type; RWB-P1-E1055-APP for the pod read and the freshness stamp; RWB-P1-E1066-APP for the ledger and the held rows; RWB-P5-E1054-APP and RWB-P5-E1055-APP for the stored letter. DP-07 resolves to "the notice type and template version are read as data through the P6 contract", DP-15 to "each service migrates its own schema and the suite holds no grant", DP-18 to "the ledger is read and asserted through rwb-source-data's interaction operation" and DP-19 to "SCR-03, SCR-30, SCR-44 and SCR-45 are reached through the gateway-bff composite route".

**Components**

| Component | Type | Responsibility |
|---|---|---|
| WinDispatchRun | Test suite | The ordered end-to-end run of section 4 for one business date, with one run lock per environment |
| WindowDriver | Fixture | Opens the 16:00 WIN file window the way the Airflow task does and records the call |
| WinEdgeStub | Fake | The WIN folder and the acknowledgment record at the P2 edge, with the silent and failed variants |
| PodBatchFixture | Fixture | The `WIN-POD-SAMPLE-v1` sample, the 30-row batch, the unknown row and the repeat row, loaded through ACE ingestion and never in a view the suite reads |
| NoticeAssertions | Assertions | State, sent date, barcode, callback date, delivery status and the dispatch counters on the P6 contract |
| TimerAssertions | Assertions | The NOTICE_PERIOD timer and its start date on the P3 contract |
| LedgerAssertions | Assertions | One ledger entry per dispatched or delivered fact, with direction, channel, date and summary; one ledger call per dispatched fact only |
| ExceptionAssertions | Assertions | The held row with check References and the REC-09 break on the P1 data-quality read |
| BoundaryCheck | Check | Fails the run on any read outside `/api/recovery/<short>/v1`, any cross-schema read, any call chain and any path outside the published contract |
| RunReport | Publisher | Publishes the run report with the counts, the contract versions and the fixture versions |

**Fixtures**

- Case `RC-2026-000123` with primary account contract CT-77001, and notices `N-0001` and `N-0002` in state Generated with notice type DEMAND.
- The WIN owner's sample file `WIN-POD-SAMPLE-v1` of 25 records for 2026-11-30, and the 30-row batch of the same date with 29 matchable rows and one row of barcode `RR000000000TH` and notice_ref `WIN-99999`.
- The repeat pod row of 2026-11-28 for barcode `RR123456789TH`, and the second pod row of 2026-11-28 used by AC10.
- Batch states of source WIN: COMPLETE for 2026-11-30, FAILED at the record count check for AC5, and not COMPLETE on 2026-12-01 for AC11.
- Business dates 2026-11-25, 2026-11-26, 2026-11-27, 2026-11-28, 2026-11-30 and 2026-12-01, held by the clock control.
- Synthetic keys only: no name, address, identity number or real barcode anywhere in the fixtures.

**Real-service topology of the run**

| Node | Part in the run |
|---|---|
| rwb-comms (P6) | Owns the notice, runs `NoticeDispatchWorkflow`, handles the acknowledgment and publishes `NoticeDispatched` and `NoticeDelivered` |
| rwb-integration (P2) | Owns the outbound item and executes `deliverFile` to the stubbed WIN edge; publishes `FileDelivered` and `FileFailed` |
| rwb-source-data (P1) | Serves the pod records, the freshness stamp and the ledger operation; the only reader of `recovery.v_ace_*` |
| rwb-document (P5) | Holds the stored letter behind the document ID |
| rwb-case (P3) | Owns the NOTICE_PERIOD timer and the task after the third failure |
| rwb-access (P4) | Answers the cached permission data the owners check when a role without the Litigation R right calls; the harness calls no access operation of its own and asserts the owner's 403 |
| Kafka, Temporal and the Airflow frame | Shared platform parts; the Airflow frame opens the 16:00 window and calls the services through their APIs only |
| WIN folder and acknowledgment stub | The external party at the SFTP edge; the only stub in the run, on a synthetic fixture |

**Run order**

1. Reset the wave-1 SIT fixtures, load the fixture set of this section and hold the clock on 2026-11-25.
2. Run AC1 and AC8 on 2026-11-25: one file, `N-0001` and `N-0002` once each, the acknowledgment, Sent with barcode `RR123456789TH`, one ledger call, one `NoticeDispatched`, then the rerun with no second file and no second item.
3. Run AC4: three runs with no acknowledgment on 2026-11-26, 2026-11-27 and 2026-11-28, the notice still Generated, three files and the task with MSG-GEN-006 naming WIN.
4. Run AC3 on 2026-11-30: the 25-record sample ingested by ACE and read on the pod records and the freshness stamp, 25 of 25 and 0 refused, with the feed version.
5. Run AC2, AC6 and AC7 on 2026-11-30: 29 notices delivered, 1 row held with check References, one delivery per notice, the repeat counted, one `NoticeDelivered` and the timer started on 2026-11-28.
6. Run AC10 with the second pod row of 2026-11-28: the notice unchanged, no second `NoticeDelivered`, the repeat counted.
7. Run AC5 and AC11: the batch FAILED at the record count check and then not COMPLETE on 2026-12-01, no pod row read, no state change, and MSG-P1-001 naming DP07 and 2026-11-23.
8. Run AC9 on 2026-11-28 with `N-0002` still without a barcode, and assert the REC-09 break on the data-quality read.
9. Run AC13: the `FileFailed` answer on the first attempt, the retry at the interval in force, one ACKNOWLEDGED item, one `FileDelivered`, one letter.
10. Run AC12 as RW-PHONECOL, assert 403 with MSG-P4-002 and no change, then run the boundary check, publish the run report and restore the environment.

**Configuration.** The fixture set, the window call, the stub file naming and the expected counts sit in `itg/recovery/config`; the eligible notice state, the attempt limit and the retry intervals are data in the owning services and are read, never set, by the harness. No business value is compiled into the suite.

**Done when.** The fifteen test cases of section 16 pass in one run; the boundary check finds no read outside `/api/recovery/<short>/v1`, no cross-schema read and no call chain; the run report shows one file per business date, one delivery per pod row, one `NoticeDelivered` per newly delivered notice and the timer started on 2026-11-28 (one running timer per notice; a second NoticeDelivered for the same notice is a repeat counted under R-UNI-40); and the run is repeated once green on the same build to prove it is repeatable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the right calls the notice or the proof-of-delivery read | You cannot {action} here. Your role does not include it. |

The message text is the legacy wording of RWB-E1-055, except MSG-P1-001, which takes the FSD P1 v3 wording. The run asserts the message the owning service returns, with the values of section 7 — "DEMAND was sent for registered mail on 26 November 2026." for MSG-P6-004, "{system} is not available. Your request is queued and will be retried." with WIN named for MSG-GEN-006, "DP07 is from 2026-11-23. Today's ACE batch has not arrived." for MSG-P1-001 (the legacy fixture values 'DP07 Legal' and 2026-11-23 stay as test data) — and names the message ID in the report. The run adds no message of its own, and the report text is for the wave entry check and not part of the message standard.

### 15. Screens and states

No screen is built in this story, and the suite drives no screen. Three existing surfaces are exercised read-only through the gateway-bff composite route (DP-19):

| Surface | What the run asserts |
|---|---|
| SCR-03 Case record, notice panel (state read only; loading as in Screen Specifications v1; empty and error: Not specified in the source documents (CG-ALL-356); no access as in AC12) | Notice state, sent date, barcode, callback date and the notice period end date derived from the timer, on `RC-2026-000123` |
| SCR-30 Case documents (state read only; loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-357)) | The stored letter behind the document ID and its link to the notice, one letter per notice |
| SCR-44 Interface and job monitor (error is the failed state of the run; loading, empty and no access: Not specified in the source documents (CG-ALL-358)) | The JOB-10 run and the proof-of-delivery read in the legacy states Running; failed; complete, with the file ID and the attempt count of 2026-11-25 |
| SCR-45 Data quality (loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-359)) | The held pod row with check References in state breaks, and the REC-09 break on `N-0002` in state breaks, after the loading state of the date |

| Surface | Empty | Loading | Error | No access |
|---|---|---|---|---|
| SCR-03 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | As in Screen Specifications v1 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | 403 with MSG-P4-002 (AC12) |
| SCR-30 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | As in Screen Specifications v1 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) |
| SCR-44 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | The failed state of the run | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) |
| SCR-45 | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | The loading state of the date | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) | Not specified in the source documents (DOR-RWB-ITG-E1055-ITG-10) |

The harness reads the same facts from the owners' contracts and not from the rendered screen, because the screens are the edge's own stories; a passed run therefore means the data behind each surface is right. The composite route itself is RWB-PLT-N001-CON and the screen field lists are the edge's own stories; this suite stops at the owners' contracts.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01-ITG | AC1, BR1, BR2 | End to end | `N-0001` Generated with contract CT-77001; acknowledgment sent date 26112026, barcode `RR123456789TH`, sent type NPL, on the real P6, P2, P1 and P5 services |
| TC-E1-055-02-ITG | AC2, BR2 | Integration | Pod row of 2026-11-30 with `RR123456789TH` and callback_date 2026-11-28; the NOTICE_PERIOD timer read on the P3 contract |
| TC-E1-055-03-ITG | AC3, BR4 | Integration | `WIN-POD-SAMPLE-v1`, 25 records ingested by ACE; 25 of 25 rows and 0 refused; feed version on the freshness read |
| TC-E1-055-04-ITG | AC4, BR3 | Integration | No acknowledgment on the runs of 2026-11-26, 2026-11-27 and 2026-11-28; three files; MSG-GEN-006 naming WIN |
| TC-E1-055-05-ITG | AC5, BR4 | Integration | ACE batch for source WIN of 2026-11-30 FAILED at the record count check; no pod row read; MSG-P1-001 naming DP07 Legal and 2026-11-23 |
| TC-E1-055-06-ITG | AC6, BR4 | Integration | 30 rows of 2026-11-30, 1 with barcode `RR000000000TH` and notice_ref `WIN-99999`; 29 updated, 1 held with check References |
| TC-E1-055-07-ITG | AC7, BR6 | Integration | Pod rows of 2026-11-30 read twice; one delivery per notice; repeat counted under R-UNI-40 |
| TC-E1-055-08-ITG | AC8 | Integration | `NoticeDispatchWorkflow` rerun on 2026-11-25 from the job monitor; one file, one outbound item, `N-0001` once |
| TC-E1-055-09-ITG | AC9, BR5 | Component | `N-0002` with no barcode on 2026-11-28; REC-09 break listed and visible on SCR-45 |
| TC-E1-055-10-ITG | AC10, BR6 | Integration | Second pod row of 2026-11-28 for `RR123456789TH`; notice unchanged; no second `NoticeDelivered` |
| TC-E1-055-11-ITG | AC11, BR7 | Integration | No COMPLETE WIN batch on 2026-12-01 for the date due 2026-11-30; stale marker; MSG-P1-001 naming DP07 Legal and 2026-11-23 |
| TC-E1-055-12-ITG | AC12, BR9 | Component | Role RW-PHONECOL with no Litigation R right on the notice and proof-of-delivery read; 403 with MSG-P4-002; nothing changes |
| TC-ITG-E1055-ITG-13 | AC13, BR3, BR8 | End to end | `FileFailed` on the first attempt of the 2026-11-25 file, the retry at the interval in force, one ACKNOWLEDGED item, one `FileDelivered`, one letter |
| TC-E1-055-14-ITG | AC14, BR9 | Integration | Harness run with a service answer outside `/api/recovery/<short>/v1` and a cross-schema read; the run fails before the report is written |
| TC-E1-055-15-ITG | Section 12 operations, events and activities | Integration | Contract check of each operation, event and activity of section 12 against the owners' published contracts on the real wave-1 services |

The legacy levels map System to Integration and Access to Component; the two criteria that cross the timer and the file edge are run at end-to-end level. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the eligible notice states, the attempt limit, the retry intervals, the break days, the stale days, the fixture set and every expected count are configuration or data.
- No personal data in logs, events, fixtures, workflow inputs or the run report: the address is read from the source-data contract into the outbound file stream only and is never logged, and the report holds notice IDs, counts and hashes.
- ACE data only through rwb-source-data: the pod, the account contract number and the contact value leave through its contract, and the suite holds no grant on `recovery.v_ace_*`.
- Files only through rwb-integration: the INT-14 file is built and sent by the owner activity, no component calls WIN directly, and the WIN edge is the synthetic stub.
- No read of another service's tables and no cross-schema join: every assertion is made through `/api/recovery/<short>/v1` or on the topic, and a cross-schema read fails the boundary check.
- One hop and a 2 s budget, one GET retry with jitter and a circuit breaker per downstream; a call chain or an unbounded timeout fails the run.
- No PII in events: the four consumed events are asserted for IDs and facts only, keyed by case ID.
- Synthetic data only: no real WIN connection, no production or UAT data, and the environment is restored after the run.
- A failing criterion is fixed in the service that owns it or raised as a gap; it is never waived in the suite.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-01-ITG, TC-E1-055-02-ITG, TC-E1-055-04-ITG, TC-E1-055-08-ITG, TC-E1-055-09-ITG, TC-E1-055-10-ITG, TC-E1-055-11-ITG, TC-ITG-E1055-ITG-13 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-01-ITG, TC-E1-055-02-ITG, TC-E1-055-12-ITG |
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the owner's contract and files move only through rwb-integration | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; DP-05; DP-16 | TC-E1-055-03-ITG, TC-E1-055-05-ITG, TC-E1-055-06-ITG, TC-E1-055-07-ITG, TC-ITG-E1055-ITG-13 |

| Item | What it covers in this story |
|---|---|
| DP-01 | The notice, the letter, the outbound item, the pod and the timer are read from their owners, and no `rwb_*` table is read by the suite |
| DP-05 | The pod, the contract number and the contact value reach the run only through rwb-source-data, the sole reader of `recovery.v_ace_*` |
| DP-09 | The four events are consumed from the owners' topics with the key and the inbox dedupe asserted |
| DP-10 | JOB-10 is the Airflow 16:00 file window plus the P6 workflow, not a Quartz row and not a Schedule of this story |
| DP-13 | Every path in the run is on `/api/recovery/<short>/v1` |
| DP-18 | The interaction ledger is rwb-source-data's and is asserted through its operation |
| DP-19 | SCR-03, SCR-30, SCR-44 and SCR-45 are reached through the gateway-bff composite route |

| Assumption | What it covers | Contract element | Test cases |
|---|---|---|---|
| ASM-0491 | P6 runs JOB-10 in NoticeDispatchWorkflow at the Airflow 16:00 window; P2 executes deliverFile and returns the acknowledgment through its file contract and FileDelivered or FileFailed | NoticeDispatchWorkflow, the deliverFile activity and rwb.integration.events.v1 | TC-E1-055-01-ITG, TC-E1-055-04-ITG, TC-E1-055-08-ITG, TC-ITG-E1055-ITG-13 |
| ASM-0492 | P6 reads pod rows and freshness only through P1 and writes no WIN delivery fact | GET /data-products/{productCode}/records and GET /data-products/freshness | TC-E1-055-02-ITG, TC-E1-055-03-ITG, TC-E1-055-05-ITG, TC-E1-055-06-ITG |
| ASM-0493 | The dispatch LETTER interaction goes through P1 POST /cases/{caseId}/interactions, the delivery entry is written by rwb-source-data on the proof-of-delivery read that names caseId, and the REC-09 break is read through P1 GET /admin/data-quality/exceptions | The ledger operation and the data-quality exceptions read | TC-E1-055-01-ITG, TC-E1-055-02-ITG, TC-E1-055-09-ITG |
| ASM-0494 | P3 starts the NOTICE_PERIOD timer on rwb.comms.NoticeDelivered.v1 and the suite reads it through the P3 timers operation | rwb.comms.NoticeDelivered.v1 and GET /cases/{caseId}/timers | TC-E1-055-02-ITG, TC-E1-055-12-ITG |
| ASM-0495 | WIN stays an outside system reached only through P2's MFT/SFTP file contract; the WIN folder and acknowledgment are stubbed at the P2 boundary | The WIN folder stub and acknowledgment stub of section 12.8 | TC-E1-055-01-ITG, TC-E1-055-04-ITG, TC-ITG-E1055-ITG-13 |

TC-E1-055-12-ITG traces to the access rule behind the notice and pod reads (BR9, MSG-P4-002) and is asserted through the owner's refusal rather than a requirement row of its own.

### 19. Out of scope

- The build of the loop: RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P1-E1055-APP, and the platform CON stories the pattern table names.
- Refused, returned and undeliverable letters, the proof window and the transfer to the owner's queue (RWB-E2-021, R-LIT-08, R-LIT-09).
- The conduct check before dispatch (RWB-E2-021).
- Notice approval before dispatch (RWB-E2-014).
- Statutory sale notices for repossessed assets (FEAT-AST-04, Epic 3).
- The full SCR-44 interface and job monitor and the full SCR-45 data quality console (Epic 2 and Epic 8); this story reads their states only.
- Real WIN connectivity, the WIN owner sign-off and the production SFTP and key-store configuration (RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-ACE-001).
- Production monitoring, alerting and the job run book (RWB-E1-056).
ok (RWB-E1-056).
