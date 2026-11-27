# RWB-ITG-E1007-ITG Integration adapters for outbound files — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Freshness path is `/data-products/freshness`; the answer carries `status` `LOADED` or `STALE`, not an ACE batch status (RD-P1-005, RD-P1-041).
- The held file is released by `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED (RD-P1-003, RD-P1-040).
- Batch literal `COMPLETE` reads `COMPLETED`.
- Customer and account reads follow the published `getCustomer` and `getAccount` operations; the addressee name and postal address are clear only for the outbound-file identity, with the unmasking rules pending as NEW-GAP-D1 (RD-P1-060).
- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1007-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1007-ITG-16); sized by the squad at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P4-E1007-APP |
| Contract dependencies | Provider contracts of section 12.2 (rwb-document, rwb-source-data, rwb-case, rwb-access; CG-ALL-144 to CG-ALL-149); contract version Not specified in the source documents (DOR-RWB-ITG-E1007-ITG-23); contracts of RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON (GAP-1161) |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P1-E1015-APP, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P6-E1007-APP, RWB-P5-E1007-APP, RWB-P4-E1007-APP |
| External dependencies | None |
| Fakes until publish | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON (DP-03, DP-07, DP-09, DP-10, DP-19) are built against fakes until they publish; swap each for the real contract in the same iteration |
| Interface volume and window targets | Not specified in the source documents (GAP-1544); open under DL11, placeholder of Template and Rules section R9 |
| Egress values | Not specified in the source documents (GAP-0649); held in the key store behind the rwb-integration workload identity |
| Event and task element names | Not specified in the source documents (GAP-2229); confirm in RWB-P2-E1007-CON at contract review |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-027, FR-PLT-028, FR-PLT-029, FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041, RD-P1-004, RD-P1-060 |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-007 is split (rework) and this integration story proves the one outbound-file path end to end across the real wave-1 services — rwb-comms requests, rwb-integration executes `deliverFile`, rwb-source-data answers every source-data read, rwb-document stores the file, rwb-case takes the route-state change and the owner task and rwb-access authorises. It builds and executes the integration tests and publishes no operation of its own. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1007-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (38 resolved, 39 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the one outbound-file path proved end to end against the real wave-1 services, from the requesting notice in rwb-comms through the `deliverFile` activity on queue `rwb-integration`, the source-data reads that leave one hop to rwb-source-data, the claim-check store in rwb-document, the delivery to WIN and to a debt buyer, and the retry, exception-queue and owner-task path into rwb-case, with the right check in rwb-access on the resend**, so that **every outbound file of every later wave is proved once, on the real services, before it is copied**.

### 2. Business rationale

The legacy story fixed one adapter pattern for every outbound file, built from `recovery.v_ace_*`, retried on intervals held as data and raised to an exception queue with a named owner. In the target that pattern is no longer one process reading an ACE table: rwb-comms requests the WIN letters file, rwb-payment the posting file and rwb-debtsale the buyer tape, rwb-integration executes one activity `deliverFile(manifest)` on queue `rwb-integration`, rwb-source-data is the only service that reads the thirty `recovery.v_ace_*` views, rwb-document holds the bytes behind a claim-check link and rwb-case carries the route state and the task (DP-01, DP-05, DP-09, DP-16, DP-17). Every one of those edges fails in a way no single-service suite can see: a second file built for one request, a read that reaches an ACE view from the wrong service, a retry that duplicates a file, a task raised for nobody because the event and the action disagreed.

This story is the end-to-end proof of that path on the wave-1 services, and it is the reference the later ITG stories copy. It exercises REQ-DRI-006 (no direct call to a system of record), REQ-DRI-007 (every outbound file logged, retried and raised to an owner) and REQ-DRI-008 (data from other systems only through ACE ingestion and the ACE views, read by rwb-source-data alone), and it holds the FSD P2 measure "outbound items in the exception queue over one day: zero". It also proves DP-17 for this legacy key: no inbound adapter, no data lake, INT-19 and INT-20 carry no lake target, the reporting extract goes to rwb-reporting through `deliverFile` and the decision and outcome feed is continuous Kafka ingest in rwb-decision.

### 3. Preconditions

- RWB-P2-E1007-APP is done in SIT: `deliverFile(manifest)` and `receiveFile` are published in the activity contract on queue `rwb-integration`, and the exception-queue read, the resend and the outbox-delivery read exist on base `/api/recovery/integration/v1`.
- RWB-P2-E1007-CON is published: the activity contract jar, the AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`, the error envelope, the Idempotency-Key rule and the contract fakes. This story runs against the real services, so the fakes are not used here.
- RWB-P6-E1007-APP is done: rwb-comms requests the WIN letters file for a business date and publishes `rwb.comms.NoticeGenerated.v1`.
- RWB-P1-E1001-APP, RWB-P1-E1069-APP and RWB-P1-E1015-APP are done: rwb-source-data answers `GET /api/recovery/source-data/v1/customers/{personKey}`, `/accounts/{accountKey}` and `/data-products/freshness` behind its own views, and it is the only service with a read grant on `recovery.v_ace_*`.
- RWB-P5-E1007-APP is done: rwb-document accepts a stored file on `POST /api/recovery/document/v1/documents` and returns the upload link and the document ID.
- RWB-P3-E1007-APP is done: rwb-case consumes `rwb.integration.FileFailed.v1`, moves the route state and raises the owner task through the case contract.
- RWB-P4-E1007-APP is done: rwb-access answers the authorise check on `POST /api/recovery/access/v1/authorise` for the right on the exception-queue screen.
- The interface configuration version "IF-2026.11" is loaded for interfaces INT-14 (WIN registered mail, daily outbound file), INT-19 (reporting extract), INT-20 (decision and outcome feed) and INT-25 (debt buyer tape), each with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes. The reference-data administrator (RW-REFADM) loads the rows.
- The bank Airflow frame opens the WIN file window at 16:00 and the debt-buyer window per lot, and calls the services through their APIs only. The exact trigger contract of the two windows is Not specified in the source documents (GAP-0334; ASM-0428), so the harness opens the window by calling the requesting service the way the Airflow task does and records the call in the run log.
- The `deliverFile(manifest)` payload and the claim-check handoff between rwb-integration and rwb-document are Not specified in the source documents (GAP-0334; ASM-0428); the manifest of section 12.5 is used until the P2 contract review fixes it.
- SIT holds the run fixtures of section 13: 85 approved notices for business date 2026-11-10, the synthetic INT-25 tape of 120 accounts, one ALS batch at status FAILED at 05:20 for 2026-11-10, and the event key EV-10:TRT-0001:v1.
- The run uses the per-service logins of the wave-1 services (DP-02); no service login is shared.
- No build dependency and no contract dependency: the eight integration dependencies are on the real services. Day 1.

### 4. Flow

1. Bank Airflow: at 16:00 opens the WIN file window and calls rwb-comms for the business date's approved notices, the way the Airflow task does; the harness records the call in the run log.
2. rwb-comms: publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` for the 85 approved notices of 2026-11-10, then calls the rwb-integration activity `deliverFile(manifest)` on queue `rwb-integration` with the interface ID "INT-14", the business date, the idempotency key and the case IDs.
3. rwb-integration: reads the interface configuration row in force for "INT-14" — target, transport, attempts, retry intervals, owner role and alert role — from `interface_config` in its own schema `rwb_integration`.
4. rwb-integration: asks rwb-source-data `GET /api/recovery/source-data/v1/data-products/freshness` for the business date; the answer gives each data product `status` `LOADED` or `STALE` and its `businessDate`, which says whether the ACE batch of 2026-11-10 is complete and which source date the data carries (AC4, AC13). One hop, 2 s timeout.
5. rwb-integration: builds the file from its own `outbound_item` and from the notice references it was given, and reads the addressee and account facts it needs with `GET /api/recovery/source-data/v1/customers/{personKey}` and `GET /api/recovery/source-data/v1/accounts/{accountKey}`, one hop each, 2 s timeout. No statement of the build reads `recovery.v_ace_*`.
6. rwb-integration: writes one `outbound_item` for "INT-14" and 2026-11-10 under the unique idempotency key, in status PENDING, then calls rwb-document `POST /api/recovery/document/v1/documents` and stores the built file `WIN_NOTICE_20261110.txt`; `outbound_item` holds the document ID and the claim-check manifest (fileId, batchId, sha256, record count 85). No file content travels on a message.
7. rwb-integration: sends the file to WIN over MFT/SFTP with PGP, sets the item SENT, and writes the `outbox_delivery` rows of the events it raises; on the acknowledgment file the item moves to ACKNOWLEDGED.
8. rwb-integration: publishes `rwb.integration.FileDelivered.v1` on `rwb.integration.events.v1` with key the case ID and the requesting service in the payload; the requesting service acknowledges it once through its inbox. Nothing else in the run builds, sends or stores a file for that business date.
9. rwb-integration: on a failed transfer raises the next attempt from the retry intervals in the row — attempt 2 five minutes after attempt 1 and attempt 3 fifteen minutes after attempt 2 — and keeps the item in RETRY while an attempt is outstanding.
10. rwb-integration: after the last allowed attempt sets the item EXCEPTION, writes `rwb.integration.FileFailed.v1` to its outbox in the same transaction, and shows the item in the exception queue with MSG-P2-001.
11. rwb-case: consumes `rwb.integration.FileFailed.v1` through its inbox once, moves the route state of each case on the file to EXCEPTION_QUEUE — RETRY_QUEUE after a first failure — and raises one open task for role RW-PLATADM for the case set, through the rwb-case contract.
12. rwb-access: answers the authorise check when the platform administrator opens the exception queue and when the resend is called; a role without the right is refused with MSG-P4-002 and nothing changes.
13. rwb-integration: on the resend returns the item to PENDING with attempt count 0, answers MSG-GEN-005, and writes the resend to the access audit trail with the role and the time.
14. rwb-reporting: when its extract falls due for the business date, calls `deliverFile(manifest)` for "INT-19" with its own base and receives `rwb.integration.FileDelivered.v1` back; no file goes to a data lake and no lake copy is written.
15. rwb-decision: ingests the decision and outcome feed continuously from `rwb.decision-record.v1`; no "INT-20" file is produced and no lake delivery row exists (DP-17).
16. The harness: compares the run against the expected counts — one outbound_item per interface and business date, 85 cases on the WIN file, 120 accounts on the INT-25 tape, one FileDelivered or FileFailed per item, one task per case set, zero duplicate files — and publishes the run report with the boundary result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch for the file's business date is not complete | rwb-source-data answers the freshness check with the source date; no file is built and no outbound_item is written; the request waits for the next window after AceDataReady with `sourceSystem` ALS and `status` COMPLETED | MSG-P1-001 | AC4 |
| X2 | The outbound transfer fails on an attempt | The item waits for the next attempt from the retry intervals in the row; the cases of the file move to route state RETRY_QUEUE after the first failure | MSG-GEN-006 | AC16 |
| X3 | The retry limit of 3 attempts is reached | The item moves to EXCEPTION, `rwb.integration.FileFailed.v1` is published, each case moves to EXCEPTION_QUEUE and one task goes to role RW-PLATADM | MSG-P2-001 | AC14 |
| X4 | The same requesting event arrives twice with the same key | The inbox of rwb-integration drops the second one, the hit is counted and no second file is built (R-UNI-40) | None | AC17 |
| X5 | Two worker instances pick the same due item | Only one holds the row lock; the other skips it, so the file is sent once and the attempt count is 1 | None | AC18 |
| X6 | A platform administrator resends an item from the exception queue | The item returns to PENDING with attempt count 0, the sender picks it up in its next pass and no duplicate file exists | MSG-GEN-005 | AC14 |
| X7 | A role without the right lists or resends exception items | Refused by rwb-access; nothing changes | MSG-P4-002 | AC19 |
| X8 | A service other than rwb-source-data attempts a read of `recovery.v_ace_*` | The statement fails at the database grant and the boundary check of the run fails | None (run log) | AC13 |
| X9 | The stored file is missing in rwb-document when the manifest is followed | The attempt fails as a transfer failure; the claim-check link is never rebuilt from a partial file; the item follows the retry path | MSG-GEN-006 | AC12, AC14 |
| X10 | rwb-source-data does not answer inside the REST budget | One hop, 2 s timeout, no retry other than one GET retry with jitter; the attempt fails and is retried, never built from a partial answer | None | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the real wave-1 services already in SIT; it builds no operation and waits for no contract. The eight integration dependencies are the services it exercises |
| Negotiable | The fixtures, the window call and the expected counts are harness configuration; the business values are the legacy ones and are not changed |
| Valuable | The one outbound path of every later wave is proved on the real services once, including the retry, the exception queue and the owner task |
| Estimable | One harness, one fixture set, one boundary check, one run report; no production code |
| Small | Fits one sprint with the fixture set |
| Testable | Every owned criterion has a test case in section 16; the last four are the new end-to-end ones |

### 7. Acceptance criteria

```gherkin
Feature: Integration adapters for outbound files, end to end

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has direction "OUTBOUND", max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"
    Given the business date is 2026-11-10
    Given every service in the run is the real wave-1 service on its own base /api/recovery/<short>/v1

  Scenario: AC4 Outbound file held while the ACE batch is not complete (legacy RWB-E1-007 AC4)
    Given the rwb-source-data freshness answer for 2026-11-10 reports DP01 with `status` `STALE`, the ALS batch having read "FAILED" at 05:20
    Given the WIN notice file for 2026-11-10 is due at 16:00
    When JOB-10 reaches its build step
    Then no file is built and no outbound_item is written
    Then the request is held with the reason "DP01 Account and arrears is from 2026-11-07"
    Then the platform administrator receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-07. Today's load has not arrived."
    Then the file is built by the next JOB-10 run after EV-26 with `sourceSystem` ALS and `status` COMPLETED for 2026-11-10

  Scenario: AC12 A WIN request produces one outbound item and one stored file (new, D-RCV-60)
    Given 85 approved notices for business date 2026-11-10 are in rwb-comms and it publishes rwb.comms.NoticeGenerated.v1
    When rwb-comms calls the rwb-integration deliverFile(manifest) activity on queue "rwb-integration" for "INT-14"
    Then exactly one outbound_item exists for "INT-14" and 2026-11-10, in status "PENDING"
    Then the built file "WIN_NOTICE_20261110.txt" is stored in rwb-document and the outbound_item holds its document ID
    Then the claim-check manifest carries fileId, batchId, sha256 and record count 85, and no file content travels on a message
    Then rwb.integration.FileDelivered.v1 is published on rwb.integration.events.v1 with key the case ID and the requesting service in the payload
    Then the requesting service acknowledges it once, and the outbound_item moves to "SENT" and then "ACKNOWLEDGED" when the acknowledgment file arrives

  Scenario: AC13 Source data for the build is one hop to rwb-source-data (new, D-RCV-60)
    Given the file build needs the addressee and the account facts of the business date
    When deliverFile builds the file
    Then each source-data read is one REST call to rwb-source-data: GET /api/recovery/source-data/v1/customers/{personKey}, GET /api/recovery/source-data/v1/accounts/{accountKey} and GET /api/recovery/source-data/v1/data-products/freshness
    Then every call has a 2 s timeout, one GET retry with jitter and no call chain
    Then no service outside rwb-source-data reads recovery.v_ace_* and the boundary check of the run finds no such read
    Then the ACE business date on the outbound_item is the one rwb-source-data reports, 2026-11-10

  Scenario: AC14 The retry limit, the exception queue and the owner task (new, D-RCV-60)
    Given outbound_item "OB-0002" for the 85 cases of the file is due
    Given the transfer fails on attempts 1, 2 and 3
    When the third attempt fails
    Then the item status is "EXCEPTION" and the item shows in SCR-09 with message MSG-P2-001
    Then rwb.integration.FileFailed.v1 is published on rwb.integration.events.v1 for the requesting service
    Then the rwb-case contract raises one open task with owner role "RW-PLATADM" for the case set of the file, and each case is in route state "EXCEPTION_QUEUE"
    Then the outbox holds one FileFailed row and the inbox of rwb-case processes it once, so a redelivery writes no second file and no second task
    Then a platform administrator resends the item, the response carries MSG-GEN-005, the item returns to "PENDING" with attempt count 0, and no duplicate file exists

  Scenario: AC15 No inbound adapter and no data lake (new, D-RCV-60)
    Given every interface configuration row of version "IF-2026.11", including "INT-14", "INT-19", "INT-20" and "INT-25"
    When the interface configuration rows of version "IF-2026.11" are loaded
    Then every row has direction "OUTBOUND" and the load refuses a row with direction "INBOUND"
    Then no inbound folder is read and the receiveFile activity is called by no flow in the run
    Then "INT-19" and "INT-20" name no data lake target: the reporting extract is delivered through deliverFile(manifest) to rwb-reporting and the decision and outcome feed is continuous Kafka ingest in rwb-decision
    Then no file is sent to a data lake, no lake copy is written, and no JOB-13 file exists
    Then the debt buyer tape "INT-25" is delivered through the same deliverFile path, per lot, encrypted

  Scenario: AC16 An outbound transfer failure waits for the next attempt and holds the cases in RETRY_QUEUE (new, D-RCV-60)
    Given outbound_item "OB-0001" for the 85 cases of the file is due
    When the transfer fails on attempt 1
    Then the item waits for attempt 2 on the retry interval of its configuration row
    Then each case of the file is in route state "RETRY_QUEUE" and the response carries MSG-GEN-006

  Scenario: AC17 A requesting event with a key already processed is ignored (new, D-RCV-60)
    Given the requesting event with key "EV-10:TRT-0001:v1" has been processed by the inbox of rwb-integration
    When the same requesting event arrives a second time
    Then the inbox of rwb-integration drops the second event and the hit is counted
    Then no second file is built and no second outbound_item is written

  Scenario: AC18 Two workers do not send the same due item twice (new, D-RCV-60)
    Given outbound_item "OB-0001" is due
    When two worker instances pick the same due item
    Then only one holds the row lock and the other skips the item
    Then the file is sent once and the attempt count is 1

  Scenario: AC19 A role without the right cannot list or resend exception items (new, D-RCV-60)
    Given a role without the right to list or resend exception items
    When that role lists or resends an exception item
    Then rwb-access refuses the request with MSG-P4-002
    Then nothing changes

  Scenario: AC20 The adapter writes only its own tables and keeps no run table (new, D-RCV-60)
    Given outbound_item "OB-0001" has notices with dispatch fields and a workflow run
    When the run state of the outbound file is requested
    Then the state is answered from the dispatch fields of its notices, the workflow run and the status the P2 contract returns
    Then no run table is kept and the adapter writes only interface_config, outbound_item, outbox_event, outbox_delivery and processed_event
    Then debt_sale_account and recovery_case change only through a contract call or an event from P2

  Scenario: AC21 A status change the model does not allow is refused (new, D-RCV-60)
    Given outbound_item "OB-0001" is in status "ACKNOWLEDGED"
    When a status change of "OB-0001" to "PENDING" is requested
    Then the change is refused and the item stays in status "ACKNOWLEDGED"
```

The legacy criteria this story does not own (AC1, AC2, AC3, AC5, AC6, AC7) are owned by RWB-P2-E1007-APP and are re-exercised only inside the end-to-end run of section 13, never restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound file goes through the one adapter; no component calls a target system directly | ADR-010; REQ-DRI-006; legacy RWB-E1-007 BR1 |
| BR2 | An outbound file reads ACE data only by business key, through the owner's contract, and never writes to ACE | D-RCV-35 U4; ADR-010; BR-P2-001-ACE; legacy RWB-E1-007 BR2 |
| BR3 | An outbound file is built only when the ACE batch for its business date is complete | VR-P2-001-1; legacy RWB-E1-007 BR3 |
| BR4 | An outbound file is sent again on the intervals in its configuration row inside the window that the bank scheduler opens; the service owns the attempt ladder and the exception state, and after the last failure a task goes to the owning role; the single owner of the retry count is left to DL11 | ifspec INT-14; interface_config.max_attempts; Architecture v5 slide 32; FSD P2 v3 A2.2; legacy RWB-E1-007 BR4 |
| BR5 | A system that is unavailable queues the action and retries | R-UNI-33, R-UNI-35, R-UNI-36; legacy RWB-E1-007 BR5 |
| BR6 | An item that fails after the retry limit moves to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007; legacy RWB-E1-007 BR6 |
| BR7 | An event with a key already processed by the consumer is ignored and the hit is counted | R-UNI-40; events.txt Rules sheet, Duplicates; legacy RWB-E1-007 BR7 |
| BR8 | Retry counts, intervals, folders, patterns and owners are data rows, never code | Principle 1; DT02; legacy RWB-E1-007 BR8 |
| BR9 | rwb-integration has no inbound adapter: no file is picked up, checked or signed off in the Workbench, and `interface_config` holds outbound rows only | D-RCV-35 U1; ADR-010; legacy RWB-E1-007 BR9 |
| BR10 | An outbound item carries case IDs and business keys, never an address, a name or an identity number; the file itself is held in rwb-document behind the claim-check link | CTL-11; Guardrails; legacy RWB-E1-007 BR10 |
| BR13 | The adapter writes only interface_config, outbound_item, outbox_event, outbox_delivery and processed_event; debt_sale_account (S6 rwb_debtsale) and recovery_case (P3 rwb_case) change through a contract call or an event from P2 | Ownership Map v1; Build Notes v6 RWB-E1-007 View note |
| BR14 | The run state of an outbound file is answered from the dispatch fields of its notices, the workflow run and the status the P2 contract returns; no run table is kept and the interface monitor is SCR-44 at the platform edge | TSD P6 Communications v2 T-A.1; Architecture v5 slide 20 |
| BR15 | JOB-10, JOB-13 and JOB-15 run in the owning services named by the Ownership Map (rwb-comms, rwb-decision, rwb-reporting); rwb-integration registers no Temporal Schedule and provides the delivery capability the owner calls | Ownership Map Jobs; Architecture v5 slide 44; FSD P2 v3 A1.5 |
| BR16 | INT-19, INT-20, JOB-13 and JOB-15 are removed from this service with no target: no data lake file, copy or delivery row is created; the reporting projection is rwb-reporting's and the decision ledger goes to the shared decision-record topic | DP-17; Architecture v5 slides 2, 8, 37 and 44 |
| BR17 | The INT-14 record layout and file pattern are read through the rwb-integration interface row and never copied into a value file; the built file is stored in rwb-document behind a claim-check reference and only that reference travels in the manifest | Architecture v5 slides 11 and 16; TSD P2 Integration v3 T3.1 DF-OPS-141 and DF-OPS-171 |
| BR11 | Between services the file path is contract-only: rwb-integration reads source data only through the rwb-source-data REST contract, one hop and 2 s, and no service outside rwb-source-data reads `recovery.v_ace_*`; no service reads another service's tables and no file content travels on a Kafka message | DP-01; DP-05; DP-11; DP-16; ADR-010; Architecture v5 slides 9, 10 and 11 |
| BR12 | There is no data lake: the reporting extract is delivered to rwb-reporting through `deliverFile` (legacy JOB-15) and the decision and outcome feed is continuous Kafka ingest in rwb-decision (legacy JOB-13); INT-19 and INT-20 carry no lake target | DP-17; Architecture v5 slides 37 and 44 |

### 9. State transitions

`outbound_item.status` as exercised end to end:

| From | Event | Condition | To |
|---|---|---|---|
| None | `deliverFile(manifest)` accepted | The freshness check passes and the idempotency key is new | PENDING |
| PENDING | First transfer fails | The transport raises a failure | RETRY |
| RETRY | A later attempt is sent | The retry interval in the row has elapsed | SENT |
| RETRY | Attempt count equals `max_attempts` (3) | The third attempt fails | EXCEPTION |
| SENT | The acknowledgment file arrives | The target confirms the file | ACKNOWLEDGED |
| EXCEPTION | Platform administrator resends | The right check passes and the item version matches | PENDING |

`recovery_case.route_state` in rwb-case, as exercised by the events this story publishes:

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed attempt of an outbound file for the case | RETRY_QUEUE |
| RETRY_QUEUE | RETRY_SUCCEEDED | A later attempt is sent | RESUME_STATE |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Attempt count equals max attempts | EXCEPTION_QUEUE |

The case status (`recovery_case.status`) does not change and this story writes no case row: rwb-case moves the route state when it consumes `rwb.integration.FileFailed.v1`. This story writes no row through any owner either; every assertion is made on the owner's contract answer and on the events on the topic. The run also exercises `outbox_delivery.status` in rwb-integration and the inbox row in `processed_event` of every consumer, through those services' own logs and admin reads.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-integration service identity (its own login, DP-02) | Builds, stores, sends and retries the file; writes its own `outbound_item`, `outbox_event` and `outbox_delivery` rows; publishes `FileDelivered` and `FileFailed` |
| rwb-source-data service identity | Answers the freshness, customer and account reads; the only identity with a read grant on `recovery.v_ace_*` |
| rwb-document service identity | Stores the built file and returns the upload link and the document ID |
| rwb-case service identity | Consumes `FileFailed`, moves the route state and raises the owner task |
| rwb-access service identity | Answers the authorise check for the exception-queue read and the resend |
| rwb-reporting service identity | Requests the reporting extract through `deliverFile` and receives `FileDelivered` |
| rwb-decision service identity | Ingests the decision and outcome feed continuously |
| RW-PLATADM, platform administrator | Lists exception items, resends one, reads the run state (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the held-file and failed-file alert; reads run state (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version; holds no right on the exception queue |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run state and exception items (Platform administration, R) |
| The integration lead and the QA role | Own the harness, the fixtures and the run report; take no business decision |

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-OPS-137 to DF-OPS-148 | interface_config (P2, `rwb_integration`) | interface_id, direction, transport, file_pattern, data_product, max_attempts, retry_intervals_min, owner_role, alert_role, valid_from, valid_to | Read |
| DF-OPS-168 to DF-OPS-177 | outbound_item (P2, `rwb_integration`) | all 10 fields | Read |
| DF-OPS-178 to DF-OPS-183 | processed_event (PLT library, created in `rwb_integration`) | all 6 fields | Read |
| DF-OPS-189 to DF-OPS-197 | outbox_event (PLT library, created in `rwb_integration`) | all 9 fields | Read |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery (PLT library, created in `rwb_integration`) | all 9 fields | Read |
| DF-LEG-019 | notice (P6, read through the rwb-comms contract) | sent_date (INT-14) | Read |
| DF-LEG-030 | notice (P6, read through the rwb-comms contract) | person_key (INT-14) | Read |
| DF-DOC-006 | document (P5, read through the rwb-document contract) | storage_ref (INT-14) | Read |
| DF-SAL-033 | debt_sale_account (S6, read through the rwb-debtsale contract) | account_key (INT-25) | Read |
| DF-CAS-001 | recovery_case (P3, read through the rwb-case contract) | id | Read |
| DF-CAS-007 | recovery_case (P3, read through the rwb-case contract) | route_state | Read; written by rwb-case only |
| DF-WRK-018, DF-WRK-019, DF-WRK-022, DF-WRK-023 | task (P3, read through the rwb-case contract) | case_id, task_code, status, owner_role | Read; written by rwb-case only |
| DF-REF-035 | role (P4, read through the rwb-access contract) | role_code | Read |
| DF-ACE-001, DF-ACE-002, DF-ACE-076, DF-ACE-077, DF-ACE-179, DF-ACE-186 | ACE source data (read through the rwb-source-data contract) | contact_key, person_key, account_key, account_code, business_date, is_complete | Read |

Field IDs are those of the legacy story and the Logical Data Model and Data Dictionary. The five integration tables sit in schema `rwb_integration`; `processed_event`, `outbox_event` and `outbox_delivery` are PLT library objects created in that schema (DP-09). This story owns no table and writes none: it reads them through the rwb-integration admin operations and asserts on the contract answers. The source-data fields the build needs — `contact_key`, `person_key`, `account_key`, `account_code`, `business_date`, `is_complete` (DF-ACE-001, DF-ACE-002, DF-ACE-076, DF-ACE-077, DF-ACE-179, DF-ACE-186) — are read only through the rwb-source-data contract, never from a view by this story or by rwb-integration. Fields classed as personal data (person_key, contact_key) are read for the build only and are carried on no outbound_item, event payload or claim-check manifest.

### 12. Contract

#### 12.1 REST operations provided

None. This story builds and executes integration tests and publishes no operation; the operations of the path belong to RWB-P2-E1007-CON and RWB-P2-E1007-APP.

#### 12.2 REST operations consumed

Every call is one hop on the owner's per-service base, with a 2 s timeout and a circuit breaker per downstream (DP-11, DP-13).

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | List items by status and interface for the exception-queue assertions of AC14 |
| POST | `/api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` | P2 rwb-integration | Resend an item in EXCEPTION (AC14, MSG-GEN-005) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | Outbox delivery state of `FileDelivered` and `FileFailed` |
| POST | `/api/recovery/document/v1/documents` | P5 rwb-document | Store the built file and take the upload link and document ID (AC12) |
| GET | `/api/recovery/document/v1/documents/{id}` | P5 rwb-document | Follow the claim-check link to the stored file (AC12) |
| GET | `/api/recovery/source-data/v1/customers/{personKey}` | P1 rwb-source-data | `getCustomer` (RD-P1-060): the addressee name and postal address of the file build, clear only for the rwb-integration outbound-file workload identity; unmasking rules Pending (NEW-GAP-D1), FieldMasker fake until then (AC13) |
| GET | `/api/recovery/source-data/v1/accounts/{accountKey}` | P1 rwb-source-data | `getAccount` (RD-P1-060): account facts of the file build (AC13) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | ACE batch completeness for the business date (AC4, AC13) |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | P3 rwb-case | Route-state change and owner task on the case set of the file (AC14) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Right check on the exception-queue read and the resend (X7) |

A service never calls another service's base inside a business step: the file steps run as Temporal activities on the owner's queue (DP-10, DP-16), and the requests of section 12.4 are events. The connection matrix of Architecture v5 slide 13 shows no cell for the rwb-integration read of rwb-source-data or for the `FileFailed` listen edge of rwb-case; the matrix cell is Not specified in the source documents (GAP-0338; ASM-0432) and is treated as incomplete, so the reads follow slides 12 and 15 and DP-11.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 | caseId | fileId, interfaceId, businessDate, documentId, sha256, recordCount, requesting service |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 | caseId | fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds, ownerRole |

Both are written to the outbox in the same transaction as the item state change and relayed with the CloudEvents envelope; no personal data and no file content is carried (DP-09). This story asserts on the topic and on the outbox rows; it publishes nothing itself.

#### 12.4 Events consumed

These are the requesting flows the run exercises, and the events the path reacts to.

| Event | Topic | Owner of the type | Handler in the run |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 | rwb-comms then requests `deliverFile` for INT-14; the run starts here (AC12) |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Releases a held request and starts the next window after a failed batch, only with `sourceSystem` ALS and `status` COMPLETED; one event per source system and business date, record key `{sourceSystem}:{businessDate}`, payload `sourceSystem`, `businessDate`, `status`, `completedAt` (AC4) |
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 | rwb-payment requests `deliverFile` for its posting file, the second requesting flow of the same path (X2) |
| `rwb.debtsale.LotAwarded.v1` | `rwb.debtsale.events.v1` | S6 | rwb-debtsale requests `deliverFile` for the INT-25 buyer tape, per lot (AC15) |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| `deliverFile(manifest)` | Activity, provided by P2 and called by the requesting services | `rwb-integration` | Builds, stores, sends and retries one outbound file; one item per interface and business date. The manifest carries fileId, batchId, sha256 and record count, and the claim-check link; its exact payload is Not specified in the source documents (GAP-0334; ASM-0428) |
| `receiveFile` | Activity, provided by P2 | `rwb-integration` | The published inbound activity of the P2 contract; wave 1 exercises no inbound call and the run asserts that no flow calls it (BR9, AC15) |

The claim-check handoff is a manifest plus a SAS link valid 15 minutes for one file (Architecture v5 slide 11); the exact handoff is Not specified in the source documents (GAP-0334; ASM-0428), and the assumption holds until the P2 contract review.

#### 12.6 Schedules

| Window or timer | When | Owner of the trigger | Legacy reference |
|---|---|---|---|
| WIN file window | Daily 16:00 | Bank Airflow opens the window; rwb-comms requests and rwb-integration executes | JOB-10; Architecture v5 slides 16 and 44 |
| Debt-buyer file window | Per lot, when the lot is awarded | Bank Airflow opens the window; rwb-debtsale requests | JOB-10; Architecture v5 slide 16 (buyer files per lot) |
| Retry timers | Attempt 2 five minutes and attempt 3 fifteen minutes after the previous attempt, up to 45 minutes | The `deliverFile` retry timer, from `interface_config.retry_intervals_min` | ifspec INT-14; legacy AC3 |

The exact trigger contract of the two windows is Not specified in the source documents (GAP-0334; ASM-0428); the harness opens them the way the Airflow task does and records the call. No service-side cron opens a file window.

#### 12.7 Tables owned

None. The path's tables — `interface_config`, `outbound_item`, `processed_event`, `outbox_event` and `outbox_delivery` in `rwb_integration` — are owned by P2 rwb-integration with the PLT library for the outbox, inbox and idempotency objects (DP-01, DP-09). This story owns no schema and reads those rows only through the owner's admin operations.

#### 12.8 Contract fakes

None. The run uses the real wave-1 services and their published contracts; the contract fakes of RWB-P2-E1007-CON are replaced by the services themselves at this level.

Named fakes for rwb-access, rwb-case, rwb-document, rwb-integration and rwb-source-data: none. Contract fake library version: Not specified in the source documents (DOR-RWB-ITG-E1007-ITG-22). Source-data test data is set only through the rwb-source-data contract answers (freshness, customers, accounts), never through `recovery.v_ace_*`.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 10 consumed | Admin reads and resend on rwb-integration; store and read on rwb-document; freshness, customer and account reads on rwb-source-data; case action on rwb-case; authorise on rwb-access; one hop, 2 s |
| Kafka | 2 published by the path, 4 consumed by the run | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` asserted; `NoticeGenerated`, `AceDataReady`, `ProceedsMatched` and `LotAwarded` drive the requesting flows |
| Temporal | 2 activities | `deliverFile(manifest)` and `receiveFile` on queue `rwb-integration` |
| File | 2 interfaces | INT-14 WIN registered mail daily outbound file and INT-25 debt buyer tape per lot; claim-check to Blob through rwb-document and MFT/SFTP with PGP to the party; no data lake |

### 13. Solution plan

**Package.** Folder `test/integration/recovery` in the ACE repository, package `<ACE base package>.recovery.itg.files`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP dependencies stay with the service implementation stories; this story carries only the eight integration dependencies on the real services and no H, C or X dependency. DP-03 resolves to "the decision and outcome feed is read from `rwb.decision-record.v1`", DP-19 to "SCR-09 is reached through the gateway-bff composite route at the edge", and DP-17 to "no lake row, no lake target, no lake delivery".

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FilePathRun | Test suite | The ordered end-to-end run of section 4; one run lock per environment |
| RequestingFlowDriver | Fixture | Drives rwb-comms, rwb-payment and rwb-debtsale to request the file, the way their own flows do |
| WindowDriver | Fixture | Opens the WIN window at 16:00 and the debt-buyer window per lot the way the Airflow task does, and records the call |
| AceBatchFixture | Fixture | Sets the ACE batch of the business date to COMPLETED or FAILED at 05:20 behind rwb-source-data, never in a view read by another service |
| ItemAssertions | Assertions | One item per interface and business date, the state chain, the attempt count, the retry intervals, the exception queue |
| DocumentAssertions | Assertions | The stored file, the document ID and the manifest (fileId, batchId, sha256, record count) |
| CasePathAssertions | Assertions | Route state RETRY_QUEUE and EXCEPTION_QUEUE, one open task with owner role RW-PLATADM per case set |
| BoundaryCheck | Check | Fails the run on any `recovery.v_ace_*` read outside rwb-source-data, any cross-schema read, any call chain and any inbound folder read |
| RunReport | Publisher | Publishes the run report with the counts, the boundary result and the fixture versions |

**Fixtures**

- 85 approved notices for business date 2026-11-10 with `person_key` and `contact_key`, and the WIN file expected as `WIN_NOTICE_20261110.txt`.
- The synthetic INT-25 tape of 120 accounts from `debt_sale_account` and the account facts answered by rwb-source-data.
- The ALS batch for 2026-11-10 at status FAILED at 05:20 for AC4, and the same batch COMPLETED for the other criteria.
- Outbound items OB-0001 (due, two workers) and OB-0002 (in EXCEPTION after 3 attempts).
- The event key EV-10:TRT-0001:v1 sent twice.
- Interface configuration version "IF-2026.11" for INT-14, INT-19, INT-20 and INT-25, plus one INBOUND row used only to prove that the load refuses it.
- Synthetic keys only; no name, address or identity number anywhere in the fixtures.

**Real-service topology of the run**

| Node | Part in the run |
|---|---|
| gateway-bff | The staff entry to SCR-09 and to the resend, one hop per call |
| rwb-comms (P6) | Publishes `NoticeGenerated` and requests `deliverFile` for INT-14 |
| rwb-integration (P2) | Executes `deliverFile` and `receiveFile` on queue `rwb-integration`; owns `interface_config`, `outbound_item` and the outbox |
| rwb-source-data (P1) | Answers freshness, customer and account reads; the only reader of `recovery.v_ace_*` |
| rwb-document (P5) | Stores the file and returns the claim-check link |
| rwb-case (P3) | Consumes `FileFailed`, moves the route state and raises the owner task |
| rwb-access (P4) | Answers the authorise check |
| rwb-reporting (P9) | Requests the reporting extract and receives `FileDelivered` |
| rwb-decision (P7) | Ingests the decision and outcome feed continuously |
| Kafka, Temporal, Airflow frame, Blob, MFT/SFTP with PGP | Shared platform parts; the party at the SFTP edge is a stub, the only stub in the run |

**Run order**

1. Reset the wave-1 schemas in the environment and load interface configuration version "IF-2026.11", including the refused INBOUND row.
2. Start the wave-1 services and the shared platform parts; wait for every health check.
3. Load the fixtures of this section, then set the ACE batch for 2026-11-10 to FAILED at 05:20 and run the held-file criterion (AC4).
4. Set the ALS batch to COMPLETED and raise `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED; open the WIN window and run AC12: one item, one stored file, one `FileDelivered`, item SENT then ACKNOWLEDGED.
5. Run AC13: capture every source-data call of the build, assert one hop, 2 s timeout, no chain and the reported business date.
6. Run the retry and exception criteria: three failed attempts, EXCEPTION, `FileFailed`, the route states, the owner task, the single inbox action, then the resend (AC14).
7. Run the duplicate-event and two-worker criteria on the same path (TC-E1-007-05-ITG, TC-E1-007-06-ITG) and the access refusal (TC-E1-007-10-ITG).
8. Open the debt-buyer window per lot, run the INT-25 tape and the reporting extract, and run AC15: no inbound adapter, no inbound folder, no lake target, continuous ingest in rwb-decision.
9. Run the boundary check, publish the run report and restore the environment.

**Configuration.** The fixtures, the window call and the expected counts sit in `test/integration/recovery/config`; the interface rows, the attempts and the retry intervals are data in `interface_config`, never in the harness.

**Done when.** The fourteen test cases of section 16 pass in one run, the boundary check finds no `recovery.v_ace_*` read outside rwb-source-data and no call chain, the run report shows one item per interface and business date with zero unexplained exception items, and the run is repeated once green on the same build to prove it is repeatable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | An outbound file is held because the ACE batch is not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | An outbound transfer fails and is queued for retry | {system} is not available. Try again in a few minutes. |
| MSG-P2-001 | An outbound file or an outbox delivery moves to the exception queue after the retry limit | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-GEN-004 | A resend on an item whose version changed | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Saved. |
| MSG-P4-001 | A call without a session | Your session has ended. Sign in again. |
| MSG-P4-002 | A role without the right calls the screen or the resend | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A resend names an unknown item | This record was not found. |

Every message is the legacy wording of RWB-E1-007, except MSG-P1-001 and MSG-P2-001, whose English text is copied from Error and Message Standard v4 (CG-ALL-153, CG-ALL-154), and is asserted unchanged in the run; the run adds no message of its own and its report text is for the release team only.

Error and Message Standard v4 §4 uses MSG-P4-001 for 'Sign-in with no Workbench role' and MSG-P4-003 for 'A record outside the role's scope'. This story uses them for a call without a session and a resend that names an unknown item. The standard's message IDs for these two uses are Not specified in the source documents (CG-ALL-155; CG-ALL-156); the rows above keep the legacy wording until the standard allocates them.

### 15. Screens and states

SCR-09 Exception queue (E1) is exercised end to end through the gateway-bff composite route: Loading and list, where the platform administrator sees the failed outbound items with the interface, the attempt count, the last error and the case count; empty, when no item is in EXCEPTION; filtered, on interface INT-14 and on the business date; the resend action, which answers MSG-GEN-005 and returns the item to PENDING; and the refusal for a role without the right, which answers MSG-P4-002 and changes nothing. States of SCR-09: loading (list) and empty (no item in EXCEPTION) as above; the error and no access screen states are Not specified in the source documents (CG-ALL-162). The run asserts the list content from the rwb-integration admin read and not from the screen, because the screen is the edge's own story; the screen fields and the composite route specification are Not specified in the source documents (GAP-0334; ASM-0428). The full SCR-44 interface and job monitor is out of scope (section 19). States of SCR-44: loading, empty, error and no access are Not specified in the source documents (CG-ALL-163).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-10-ITG | Access, X7 | Component | Role RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend in the real service; refused with MSG-P4-002 |
| TC-E1-007-01-ITG | Run by RWB-P2-E1007-APP for AC1, BR1, BR8, BR9 | Integration | Synthetic INT-25 tape of 120 accounts through the real path; an INBOUND interface row refused by the load |
| TC-E1-007-02-ITG | Run by RWB-P2-E1007-APP for AC2, BR2, BR10 | Integration | 85 notices with person_key and contact_key; every source-data read on the rwb-source-data base |
| TC-E1-007-03-ITG | Run by RWB-P2-E1007-APP for AC3, BR4, BR5, BR6 | Integration | WIN file for 85 cases; the MFT/SFTP edge failing on attempts 1, 2 and 3; route state and owner task asserted through rwb-case |
| TC-E1-007-04-ITG | AC4, BR3 | Integration | ALS batch FAILED at 05:20 for 2026-11-10; WIN file due at 16:00; AceDataReady releases it |
| TC-E1-007-07-ITG | Run by RWB-P2-E1007-APP for AC5, BR7 | Integration | Event key EV-10:TRT-0001:v1 sent twice to the real inbox; hit count 2 |
| TC-E1-007-08-ITG | Run by RWB-P2-E1007-APP for AC6 | Integration | One due item OB-0001, two worker instances; one send, attempt count 1 |
| TC-E1-007-09-ITG | Run by RWB-P2-E1007-APP for AC7 | Integration | Item OB-0002 in EXCEPTION after 3 attempts; resend accepted with MSG-GEN-005 |
| TC-E1-007-05-ITG | Retired inbound case: file missing at the cut-off; ACE ingestion (RWB-ACE-001) | NFR | Asserts no FileLoadAdapter, no inbound folder listing, no DQ-057 or DQ-059 check and no missing-file run row; the behaviour is ACE ingestion and the EV-27 AceDataLate alert; closes when RWB-ACE-001 publishes its checks |
| TC-E1-007-06-ITG | Retired inbound case: same file delivered twice; ACE ingestion (RWB-ACE-001) | NFR | Asserts no FileLoadAdapter, no inbound folder listing, no DQ-057 or DQ-059 check and no missing-file run row; the behaviour is ACE ingestion and the EV-27 AceDataLate alert; closes when RWB-ACE-001 publishes its checks |
| TC-ITG-E1007-01 | AC12 | Integration | 85 approved notices for 2026-11-10; one outbound_item, the file in rwb-document, one FileDelivered, SENT then ACKNOWLEDGED |
| TC-ITG-E1007-02 | AC13, BR11 | Integration | The build's source-data calls captured; one hop, 2 s, no chain, no `recovery.v_ace_*` read outside rwb-source-data |
| TC-ITG-E1007-03 | AC14 | Integration | Three failed attempts, EXCEPTION, FileFailed, route state EXCEPTION_QUEUE, one owner task per case set, one inbox action, no duplicate file on resend |
| TC-ITG-E1007-04 | AC15, BR12 | Integration | Every interface row OUTBOUND and the INBOUND row refused; no inbound folder read; no lake target; the extract to rwb-reporting; continuous ingest in rwb-decision |
| TC-ITG-E1007-05 | §12 operations, events and activities | Contract | Each operation, event and activity of section 12 answered by its provider: deliverFile(manifest), rwb.integration.FileDelivered.v1, rwb.integration.FileFailed.v1, and the rwb-document, rwb-source-data, rwb-case and rwb-access contracts of section 12.2 |
| TC-ITG-E1007-06 | AC16 | Integration | Transfer fails on attempt 1 for OB-0001; item waits for attempt 2; route state RETRY_QUEUE per case |
| TC-ITG-E1007-07 | AC17 | Integration | Requesting event key EV-10:TRT-0001:v1 sent twice; inbox drops the second, hit counted, no second file |
| TC-ITG-E1007-08 | AC18 | Integration | One due item OB-0001, two worker instances; one send, attempt count 1 |
| TC-ITG-E1007-09 | AC19 | Integration | Role without the right lists and resends an exception item; refused with MSG-P4-002; nothing changes |
| TC-ITG-E1007-10 | AC20, BR13, BR14 | Integration | Run state of an outbound file answered from dispatch fields, workflow run and P2 status; no run table; only the five adapter tables written |
| TC-ITG-E1007-11 | AC21 | Integration | outbound_item OB-0001 in status ACKNOWLEDGED; change to PENDING requested; refused and status unchanged |

The legacy criteria not owned by this story (AC1, AC2, AC3, AC5, AC6, AC7) are owned by RWB-P2-E1007-APP and are re-exercised only inside the end-to-end run; the retired inbound test cases TC-E1-007-05 and TC-E1-007-06 are NFR rows that assert the absence of the inbound path (GAP-1165), closed when ACE ingestion under RWB-ACE-001 publishes its own checks. Legacy levels map System to Integration and Access to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the interface rows, the attempts, the retry intervals, the owner role and every fixture count are data or configuration.
- No personal data in logs, events, workflow inputs, fixtures or the run report: synthetic keys only, and file contents are never logged — names, counts and hashes only.
- ACE data only through the rwb-source-data contract; a `recovery.v_ace_*` read outside rwb-source-data is a defect and fails the boundary check of the run.
- No read of another service's tables and no cross-schema join: every assertion is made through the owner's published operation or on the topic.
- One hop, 2 s timeout, no call chain; the run fails when a call chain or an unbounded timeout is observed.
- No file content on a Kafka message or in a workflow payload: the claim-check link and the manifest only.
- No inbound adapter, no inbound folder, no sign-off and no interface row with direction INBOUND; no data lake and no lake delivery row.
- The run never touches UAT or production data, and the environment is restored after the run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the views and leaves through ACE's paths | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE | TC-E1-007-01-ITG, TC-E1-007-02-ITG, TC-ITG-E1007-02 |
| REQ-DRI-007 | Log every outbound file, retry, exception queue with an owner task | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40 | TC-E1-007-03-ITG, TC-E1-007-07-ITG, TC-E1-007-08-ITG, TC-E1-007-09-ITG, TC-ITG-E1007-03 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06; DP-17 | TC-E1-007-04-ITG, TC-E1-007-05-ITG, TC-E1-007-06-ITG, TC-ITG-E1007-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, claim-check for files | Decision log, D-RCV-60; ADR-020 | DP-11, DP-16 | All recovery processes | ADR-020; DP-01; DP-09 | TC-ITG-E1007-01, TC-ITG-E1007-02, TC-ITG-E1007-05 |

TC-E1-007-10-ITG traces to the access rule behind the resend (BR6, MSG-P4-002) and is asserted through the rwb-access contract rather than a requirement row of its own.

Open decision DL06 remains open. Its assumptions ASM-0189, ASM-2559, ASM-2608 and ASM-2776 are confirmed by the programme directive and apply to this story.

### 19. Out of scope

- The build of the outbound path in rwb-integration (RWB-P2-E1007-APP) and its contract (RWB-P2-E1007-CON).
- The document hub itself: storage, custody, retention and the WORM policy (P5, RWB-P5-E1007-APP and the P5 document stories).
- The ACE views and the read grants on them (RWB-P1-E1069-APP) and the freshness gate with `AceDataReady` (RWB-P1-E1015-APP).
- Inbound source ingestion, its schedules, its checks and the ACE team sign-off (RWB-ACE-001).
- The full SCR-44 interface and job monitor (Epic 2 and Epic 8).
- The WIN notice content, template and merge fields (RWB-E2-021 and the P6 stories).
- The reporting extract build in rwb-reporting and the dashboard (P9 stories); this story only proves the delivery through `deliverFile`.
- The deployment of the path: Helm values, the SFTP and key-store configuration, the dashboards and the runbook (RWB-P2-E1007-OPS, RWB-P2-E1007-INF).
- Production monitoring of the exception queue (RWB-E1-056).
