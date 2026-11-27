# RWB-P2-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004, RD-P1-060, RD-P1-062, RD-P1-064, RD-P1-066; Test Cases v9 mappings.

- `AceDataReady` consumption aligned: record key per source system and business date, daily work starts only on `sourceSystem` ALS with `status` COMPLETED (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P2-E1007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E1007-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P2-E1007-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P1-E1015-CON, rwb-source-data postal-addressee read by party_id (ID Not specified in the source documents (GAP-1162)), rwb-document contract for the claim-check upload (ID Not specified in the source documents (GAP-1164)) |
| Contract version | v1 (the /v1 path prefix of the contract endpoints) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P2-E1007-APP-22); builds against fakes of the six dependency contracts until they publish, with the plan lists kept as they stand (GAP-1161) |
| Integration dependencies | None |
| External dependencies | RWB-P2-E1007-INF, RWB-P2-E1007-OPS (both not done yet; external gates of the build) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-001, FR-P2-002, FR-P2-003, FR-P2-004, FR-P2-005, FR-P2-006, FR-P2-007, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-011, FR-P2-012, FR-P2-013, FR-P2-014, FR-P2-015, FR-P2-016, FR-P2-017, FR-P2-018, FR-P2-020, FR-P2-021, FR-P2-022) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-004, RD-P1-060, RD-P1-062, RD-P1-064, RD-P1-066 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-integration, outbound files only. The legacy story's single monolith adapter, its `recovery_svc` identity, its in-process calls to the case module and its direct reads of `recovery.v_ace_*` are replaced by one service, one login, one activity contract on queue `rwb-integration`, one hop to rwb-source-data, rwb-document, rwb-case and rwb-access, and the events `FileDelivered` and `FileFailed` on `rwb.integration.events.v1`; the data lake statements of JOB-13 and JOB-15 are retired. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E1007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (40 resolved, 41 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one outbound-file capability in rwb-integration that receives a request from the owning service through the `deliverFile(manifest)` activity on queue `rwb-integration`, builds the file from its own `outbound_item` and the claim-check documents of rwb-document, reads every source fact it needs one hop away through the rwb-source-data contract, sends the file over MFT/SFTP with PGP, retries it on the intervals held in `interface_config`, moves it to the exception queue with an owner task through the rwb-case contract after the last attempt and announces `FileDelivered` or `FileFailed` on `rwb.integration.events.v1`, with the admin outbound-item and outbox-delivery surface on `/api/recovery/integration/v1` and the right check and audit write on the resend**, so that **every later outbound file follows one pattern, a failed file is found on the day it fails, and no service outside rwb-source-data ever reads an ACE view**.

The legacy story held the adapter, the tables, the scheduler and the exception queue in one module, ran as the shared legacy service login, read `recovery.v_ace_*` in process, called the case module in process and wrote two files to a data lake. Under D-RCV-60 the capability is one service with one schema, one login, one topic, one task queue and four admin operations. The outbound request arrives as a Temporal activity from the requesting service (rwb-comms for the WIN letters, rwb-payment for its posting file, rwb-debtsale for the buyer tape, rwb-reporting for the extract), never as a table write; the ACE facts arrive through the rwb-source-data contract one hop away; the file bytes live in rwb-document behind a claim-check link; the route state and the owner task belong to rwb-case; the right and the audit record belong to rwb-access and ACE Common. rwb-integration owns the pattern, the two P2 tables, the retry policy and the two events. The Workbench reads no data lake and no Power BI target: the INT-19 and INT-20 data lake extracts are removed with no target in this service; reporting projects from business events in rwb-reporting and the decision ledger is the shared decision-record topic (DP-17; Arch v5 slides 8, 44). The rwb_integration login holds no grant on the recovery schema or the recovery.v_ace_* views; every ACE fact an outbound file needs is read through the rwb-source-data contract, one hop with a 2 s budget. The debt buyer tape rows and account keys arrive in the delivery request manifest raised by rwb-debtsale; this service reads neither debt_sale_account nor v_ace_account.

The split is deliberate and it is narrow. `interface_config` and `outbound_item` are P2's tables (Ownership Map); `outbox_event`, `processed_event`, `outbox_delivery` and `idempotency_key` are platform library objects created in `rwb_integration` (DP-09); `debt_sale_account` is rwb-debtsale's and is never read here (the INT-25 tape rows arrive in the request manifest), `notice` is rwb-comms's and `document` is rwb-document's, and the thirty `recovery.v_ace_*` views are read only by rwb-source-data (Arch v5 slides 8, 9, 13, 29 and 37; ADR-010). The TSD P2 Integration v3 wording that P2 reads the views directly is superseded (GAP-0647; ASM-1071).

### 2. Business rationale

The Workbench loads no source data; ACE ingests every source and the Workbench only sends (D-RCV-35 U1). What remains of P2 is one outbound path: the WIN registered-mail notice file (INT-14), the debt-buyer data tape (INT-25), and — re-based by DP-17 — the reporting extract that now goes to rwb-reporting through the same `deliverFile` call (legacy INT-19, JOB-15) and the decision and outcome feed that is continuous Kafka ingest in rwb-decision (legacy INT-20, JOB-13). Each file is built from Workbench tables and from facts read through their owners' contracts, sent through the outbox pattern, acknowledged, retried on the intervals held in its interface row, and moved to the exception queue with a task for the owning role after the retry limit. It meets REQ-DRI-006 (no component calls a system of record directly), REQ-DRI-007 (every outbound file logged, retried and raised to a named owner) and REQ-DRI-008 (data from other systems only through ACE ingestion and the ACE views), and it holds the FSD P2 measure "outbound items in the exception queue over one day: zero".

The behaviour the business asked for is unchanged; only the seams moved. A file that cannot be built because today's ACE batch is not complete is still held, with the same date and the same stale message; a transfer that fails is still retried on the same three attempts and the same 5, 15 and 45 minute intervals; the case still moves to `RETRY_QUEUE` and then `EXCEPTION_QUEUE` and the owner still gets one task; a resend still returns the item to `PENDING` with attempt count zero. What changed is who owns each fact and which contract carries it, and that every one of those seams is now a one-hop REST call or an event with a 2 s budget, a breaker and a fake, so the app story is buildable on Day 1 (DP-11, DP-16).

Three legacy statements are retired rather than restated. No inbound adapter, no inbound folder and no sign-off is built, and no `interface_config` row has direction INBOUND (D-RCV-35 U1; BR9). No lake file is built or sent: INT-19 and INT-20 carry no lake target (DP-17). And the legacy alert names `rwb.integration.outbound.held` and `rwb.integration.outbound.failed` are not event names of the target, because the service's events are `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` (Arch v5 slides 16, 41 and 43; DP-14), so the two alerts are alert rules over the held-item series and over `FileFailed` (GAP-0647; ASM-1077).

### 3. Preconditions

- RWB-P2-E1007-CON is published: the OpenAPI 3.1 document of the four admin operations on `/api/recovery/integration/v1`, the AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`, the `deliverFile`/`receiveFile` activity contract with the manifest, the error envelope and the Idempotency-Key rule, and the fakes of rwb-source-data, rwb-document, rwb-case, rwb-comms and rwb-access.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract that carries LOV-DIRECTION, LOV-TRANSPORT, LOV-DATA-PRODUCT, LOV-ROLE and the outbound status lists with the version in force (DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with `outbox_event`, `processed_event`, `outbox_delivery` and `idempotency_key`, the retry topics, the `.dlt` topic and the one-minute relay (DP-09).
- RWB-PLT-E1071-CON is published: the workflow kit, the task queue `rwb-integration` in namespace `rwb-recovery`, the retry and heartbeat policy, the codec and the build ID rule (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-09 Exception queue (DP-19).
- RWB-P1-E1015-CON is published: the rwb-source-data contract that answers the freshness, customer and account reads, and it is the only service with a read grant on the thirty `recovery.v_ace_*` views (ADR-010; DP-05).
- The interface configuration version "IF-2026.11" is loaded for interfaces INT-14 (WIN registered mail), INT-19 (reporting extract), INT-20 (decision and outcome feed) and INT-25 (debt buyer tape), each with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes; the reference data administrator (RW-REFADM) loads the rows through the reference-data load and the load refuses a row with direction INBOUND (ASM-1079).
- The MFT/SFTP egress endpoints of RWB-P2-E1007-INF exist in each environment with their PGP keys in the key store (NFR-052), and the claim-check container of rwb-document answers `POST /api/recovery/document/v1/documents`.
- rwb-integration connects with its own login on schema `rwb_integration` and holds no grant on `recovery` and no grant on another `rwb_*` schema (DP-02; Arch v5 slide 29). The login name is Not specified in the source documents (GAP-0647; ASM-1070).
- The legacy feature flag `rwb.integration.file-adapters` exists in the platform flag library for the environment (Template and Rules §R3 default rulings).

### 4. Flow

1. Requesting service (rwb-comms for INT-14, rwb-payment for its posting file, rwb-debtsale for INT-25 per lot, rwb-reporting for INT-19): calls the rwb-integration activity `deliverFile(manifest)` on queue `rwb-integration` with the interface ID, the business date, the idempotency key, the case IDs and the claim-check manifest, in its own workflow and under its own identity.
2. rwb-integration: reads the `interface_config` row in force for the interface — target, transport, `file_pattern`, `data_product`, `max_attempts`, `retry_intervals_min`, `owner_role`, `alert_role`, `valid_from`, `valid_to` — and refuses a row whose direction is not OUTBOUND.
3. rwb-integration reads GET /api/recovery/source-data/v1/data-products/freshness?product= per required product, one hop with a 2 s timeout. X1 holds the request with MSG-P1-001 and writes no outbound_item when a required product has never been stamped. On release, a still-STALE product keeps the request held. A never-stamped response has null businessDate and staleSince and omits sourceExtractedAt and loadedAt.
4. rwb-integration: writes one `outbound_item` in status PENDING under its unique idempotency key, inside the request transaction, and writes the `outbox_event` row of the request in the same transaction (DP-09).
5. OutboundFileWorkflow builds the file from the request manifest and authorised source facts. For INT-14 the outbound-file workload identity uses GET /api/recovery/source-data/v1/customers/{personKey} (getCustomer) for the recipient firstName and lastName and the ADDRESS contact chosen by contactKey (contactValue, city, postCode, country). It uses the rwb-comms contract for notice facts. The FieldMasker fake grants clear firstName, lastName and contactValue to the notice and outbound-file workload identities only. Production masking rows are Pending (data protection officer and rwb-access owner, GAP-3283).
6. rwb-integration: stores the built file with `POST /api/recovery/document/v1/documents` on rwb-document, keeps the document ID and the manifest (fileId, batchId, sha256, record count) on the `outbound_item`, and never carries file content on a message (Arch v5 slide 11).
7. rwb-integration: sends the file to the party over the MFT/SFTP endpoint of RWB-P2-E1007-INF with PGP, sets the item SENT, and on the acknowledgment file sets it ACKNOWLEDGED; the only class that opens a session to another system is the transport component inside the service.
8. rwb-integration: on a failed attempt applies the next interval from `retry_intervals_min`, keeps the item in RETRY, and writes `outbox_delivery` rows for the events it raises.
9. rwb-integration: after the last allowed attempt sets the item EXCEPTION, writes `rwb.integration.FileFailed.v1` to its outbox in the same transaction, raises one open task for `owner_role` through `POST /api/recovery/case/v1/cases/{caseId}/actions` on rwb-case, and shows the item in the exception queue with MSG-P2-001.
10. rwb-integration: on a successful transfer and acknowledgment writes `rwb.integration.FileDelivered.v1` to its outbox so the requesting service learns the file is out, then the relay publishes both events on `rwb.integration.events.v1` with the CloudEvents envelope and the case ID as key.
11. rwb-integration: on each consumed event checks the inbox key in `processed_event` before it acts, so a redelivery is counted and ignored and no second file and no second task exist (R-UNI-40).
12. rwb-integration: on a due item locks the row with `FOR UPDATE SKIP LOCKED`, so two worker instances send the file once and the attempt count stays 1.
13. Platform administrator: opens SCR-09 through the gateway-bff composite route, lists items by status and interface with `GET /admin/outbound-items` and deliveries with `GET /admin/outbox/deliveries`, and resends an item with `POST /admin/outbound-items/{itemId}/resend`: rwb-integration checks the Platform administration U right through the rwb-access authorise contract, returns the item to PENDING with attempt count 0, answers MSG-GEN-005 and writes the resend with the user and the time to the ACE audit log (INT-22). SCR-09 states: the no-access state shows MSG-P4-002 for a role without the Platform administration right and MSG-P4-001 for a call with no Recovery role; the error state shows MSG-GEN-006 when a consumed contract is unavailable; the empty state shows the empty list when no item is in EXCEPTION; the loading state: Not specified in the source documents (DOR-RWB-P2-E1007-APP-10).
14. rwb-integration: on a resend of a delivery in EXCEPTION uses `POST /admin/outbox/deliveries/{deliveryId}/resend`, which sets the delivery PENDING with attempt count 0 and starts no second file.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch for the file's business date is not complete (the rwb-source-data freshness answer says so) | The request is held, no file is built and no `outbound_item` is written; the requesting service retries in its next window after `AceDataReady` (`sourceSystem` ALS, `status` COMPLETED); the platform administrator and the data steward are alerted | MSG-P1-001 | AC4 (owned by RWB-ITG-E1007-ITG) |
| X2 | The outbound transfer fails on an attempt | The item waits for the next attempt from `retry_intervals_min`; the cases of the file move to route state RETRY_QUEUE after the first failure | MSG-GEN-006 | AC3 |
| X3 | The retry limit of `max_attempts` is reached | The item moves to EXCEPTION, `FileFailed` is written to the outbox and published, and one task goes to `owner_role`; the cases move to EXCEPTION_QUEUE | MSG-P2-001 | AC3 |
| X4 | The same application event arrives twice with the same key | The second event is ignored, the hit count in `processed_event` rises to 2 and no action repeats (R-UNI-40) | None | AC5 |
| X5 | Two sender instances pick the same due item | Only one holds the row lock and the other skips it; the file is sent once and the attempt count is 1 | None | AC6 |
| X6 | A platform administrator resends an item from the exception queue | The item returns to PENDING with attempt count 0 and is picked up by the next sender pass | MSG-GEN-005 | AC7 |
| X7 | A role without the Platform administration right lists or resends exception items | Refused before any state change; nothing is read and nothing changes | MSG-P4-002 | AC8 (TC-E1-007-10) |
| X8 | A statement of this service reads a table of another service, an ACE view or another `rwb_*` schema | The grant refuses the statement and the architecture boundary test fails the build | None (pipeline log) | AC1, AC2 |
| X9 | rwb-source-data, rwb-document, rwb-comms, rwb-case or rwb-access does not answer inside the REST budget | One hop, 2 s timeout, one GET retry with jitter and a breaker per downstream; the attempt fails and is retried, and the file is never built from a partial answer | MSG-GEN-006 | AC2, AC3 |
| X10 | The stored file is missing behind the claim-check link when the manifest is followed | The attempt fails as a transfer failure and follows the retry path; the link is never rebuilt from a partial file | MSG-GEN-006 | AC3 |
| X11 | A resend names an item that is not in EXCEPTION, or the item version changed | The request is refused with 409 and nothing changes | MSG-GEN-004 | AC9 (TC-E1-007-09) |
| X12 | An `interface_config` load carries direction INBOUND | The load refuses the row, because rwb-integration has no inbound interface | None (load error) | AC1 |

X1 is the mechanism of legacy AC4, whose criterion is owned by RWB-ITG-E1007-ITG; this story builds the freshness call and the hold path and the integration story proves it across the real services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the published contracts and their fakes: the rwb-integration baseline, the decision-record library, the reference data, the outbox library, the workflow kit and the edge route. The rwb-source-data, rwb-document, rwb-comms, rwb-case and rwb-access answers come from their fakes |
| Negotiable | Retry counts, intervals, folders, patterns, owners and alert roles are `interface_config` rows; the transport, the staging area and the endpoints are RWB-P2-E1007-INF values; the story fixes only the behaviour |
| Valuable | Every outbound file is built from one source of truth, logged, retried and raised to a named owner from wave 1, and no service outside rwb-source-data touches an ACE view |
| Estimable | Two P2 tables, one workflow, two provided activities, four admin operations, five consumed contracts, two events and ten test cases |
| Small | One squad, one iteration with its tests |
| Testable | Each owned criterion is one automated test against the contract fakes; the access case is a component test and the resilience case is an NFR test |

### 7. Acceptance criteria

```gherkin
Feature: Integration adapters for outbound files

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has direction "OUTBOUND", max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"
    Given the business date is 2026-11-10
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 One outbound pattern (legacy RWB-E1-007 AC1)
    Given a developer adds the outbound file "INT-25" debt buyer data tape
    Given the rwb-debtsale contract mock returns the INT-25 request with the 120 synthetic account keys of the awarded lot
    Given the rwb-source-data contract mock returns the account facts for those 120 synthetic account keys
    When the build pipeline runs
    Then the system declares the file as an interface configuration row with direction "OUTBOUND" and uses OutboundFileAdapter
    Then the contract test "INT-25" builds the synthetic tape of 120 accounts from the rwb-debtsale request manifest and the rwb-source-data account facts and passes
    Then the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter
    Then no interface configuration row has direction "INBOUND"

  Scenario: AC2 Outbound file reads ACE only through the views (legacy RWB-E1-007 AC2)
    Given 85 approved notices for business date 2026-11-10, each with person_key and contact_key
    Given the rwb-comms contract mock returns the 85 approved notices of 2026-11-10 with their person_key, sent_date and document ID
    Given the rwb-source-data contract mock returns the addressee and address of each of the 85 notices by party_id and the ACE batch status "COMPLETED" for 2026-11-10
    When OutboundFileWorkflow builds the WIN file "WIN_NOTICE_20261110.txt"
    Then each addressee and address is read by party_id through one rwb-source-data postal-addressee read within a 2 s timeout, which is the only read path of the build for ACE data, and the value is kept out of rwb_comms, the event and every log
    Then no statement of the build reads a public table
    Then the outbound item records the ACE business date 2026-11-10 from the rwb-source-data batch status answer

  Scenario: AC3 Retry and exception queue (legacy RWB-E1-007 AC3)
    Given the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases
    Given the SFTP transfer fails on attempts 1, 2 and 3
    Given the rwb-case contract mock returns route state "RETRY_QUEUE" for each of the 85 cases after the first failed attempt
    Given the rwb-case contract mock returns route state "EXCEPTION_QUEUE" and one open task for role "RW-PLATADM" when the item moves to "EXCEPTION"
    When the outbox sender runs
    Then attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2
    Then each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33)
    Then after attempt 3 the item status is "EXCEPTION"
    Then each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34)
    Then the item shows in the exception queue with message MSG-P2-001

  Scenario: AC5 Duplicate application event ignored (legacy RWB-E1-007 AC5)
    Given consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1"
    Given the rwb-treatment contract mock returns event "EV-10:TRT-0001:v1" published once on rwb.treatment.events.v1
    When the same event arrives again with the same key
    Then the consumer does not act
    Then the hit count for that key becomes 2 (R-UNI-40)

  Scenario: AC6 Two senders pick the same item (legacy RWB-E1-007 AC6)
    Given outbound item "OB-0001" is due
    When two sender threads run at 10:00:00
    Then the system sends the file once
    Then the attempt count is 1

  Scenario: AC7 Resend from the exception queue (legacy RWB-E1-007 AC7)
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    Given the rwb-access contract mock returns the Platform administration U right for the platform administrator
    Given the ace-common contract mock returns the accepted resend record
    When a platform administrator resends it
    Then the item status is "PENDING" with attempt count 0
    Then the system writes the resend to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005

  Scenario: AC8 Exception queue refused without the Platform administration right (X7) (new, D-RCV-60)
    Given the rwb-access contract mock returns no Platform administration right for role "RW-CASEOWN"
    When role "RW-CASEOWN" lists or resends an exception item
    Then the request is refused before any state change
    Then nothing is read and nothing changes
    Then the response carries message MSG-P4-002

  Scenario: AC9 Resend refused when the item is not in EXCEPTION or its version changed (X11) (new, D-RCV-60)
    Given outbound item "OB-0002" has status "PENDING"
    When a platform administrator resends it
    Then the request is refused with 409
    Then nothing changes
    Then the response carries message MSG-GEN-004

  Scenario: AC10 Case, data lake and admin surface ownership (new, D-RCV-60)
    Given the rwb-case contract mock is the only owner of route state and owner tasks for outbound items
    When an outbound file is built, held, sent or resent
    Then rwb-integration writes no case row, no task row and no debt_sale_account row
    Then no data lake file, copy or delivery row exists and JOB-13 and JOB-15 are not registered
    Then the admin surface answers only on /api/recovery/integration/v1 and every POST carries the Idempotency-Key header
    Then every resend is written to the ACE audit log with the user and the time

  Scenario: AC11 Error answers of the provided operations (new, D-RCV-60)
    Given a request to a provided operation of /api/recovery/integration/v1 arrives without a valid login
    When the request is sent
    Then the answer is 401 and nothing is read or changed
    Given a request to a provided operation arrives from a role without the required right
    When the request is sent
    Then the answer is 403 and nothing is read or changed
    Given a request names an outbound item that does not exist
    When the request is sent
    Then the answer is 404 and nothing changes

  Scenario: AC12 A consumed call fails or does not answer (X9) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer the postal-addressee read within 2 s for one of the 85 notices
    When OutboundFileWorkflow builds the WIN file "WIN_NOTICE_20261110.txt"
    Then the attempt fails and is retried once with jitter, one hop and one breaker per downstream
    Then no file is built from a partial answer
    Then the response carries message MSG-GEN-006

  Scenario: AC13 A status change the model does not allow is refused (new, D-RCV-60)
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    When a status change of the item to "PENDING" is requested without a resend by a platform administrator
    Then the change is refused and the item keeps status "EXCEPTION"
    Then nothing is sent and nothing changes
```

AC1 to AC3 and AC5 to AC13 are the criteria this story owns; every legacy value is copied unchanged, and legacy table and view reads are restated as contract reads. Statements that depend on another service's data are answered by a contract fake rather than by a table of this service. AC2 is answered by the rwb-source-data fake, which serves the addressee and address by `party_id` and the ACE batch status of the business date, and by the rwb-comms fake, which serves the approved notices with their `person_key`, `sent_date` and document ID: the legacy reads of `v_ace_contact` and `v_ace_batch_status` are replaced by these contract reads, and the views are read by rwb-source-data alone (ASM-1071). AC1 is answered by the rwb-debtsale fake, which serves the INT-25 request with the 120 synthetic account keys, and by the rwb-source-data fake, which serves their account facts: the legacy `debt_sale_account` read is replaced and the rows arrive in the request manifest, because `debt_sale_account` is rwb-debtsale's table and a foreign key or a copy across schemas is forbidden (DP-01, ASM-1072). AC3 is answered by the rwb-case fake, which serves the route-state change and the owner task. AC7 is answered by the rwb-access fake for the right and by the ACE Common audit stub for the record. In AC1 the legacy package name `recovery.integration.adapter` is kept verbatim as the legacy reference of the one adapter boundary; in the target the package is `th.co.scb.ace.workbench.recovery.integration` (ASM-1070). AC4 is not owned by this story: its criterion belongs to RWB-ITG-E1007-ITG, which exercises the hold path across the real services.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound file of this service goes through the one adapter; no component calls a target system directly and no class outside the transport component opens an SFTP session | ADR-010; REQ-DRI-006; legacy RWB-E1-007 BR1 |
| BR2 | An outbound file reads ACE data only by business key, only through the rwb-source-data contract, one hop and 2 s, and never writes to ACE; no statement of this service reads a `recovery.v_ace_*` view or a `public` table | D-RCV-35 U4; ADR-010; BR-P2-001-ACE; DP-05; DP-11; ASM-1071 |
| BR3 | Use DataProductFreshness 5.1.0. A never-stamped required product holds the notice with MSG-P1-001 (product set, date empty, wording pending GAP-3284). AceDataReady ALS/COMPLETED triggers the next release window. Re-read freshness before building and keep holding while any required product is STALE. | RD-P1-062; RD-P1-066 |
| BR4 | An outbound file is sent again on the intervals in its configuration row, and after the last failure a task goes to the owning role | ifspec INT-14; `interface_config.max_attempts` and `retry_intervals_min`; legacy BR4 |
| BR5 | A system that is unavailable queues the action and retries; a consumed contract that does not answer inside 2 s fails the attempt and is retried, never partially used | R-UNI-33, R-UNI-35, R-UNI-36; DP-11 |
| BR6 | An item that fails after the retry limit moves to the exception queue with a task for the owner role and publishes `FileFailed` | R-UNI-34; REQ-DRI-007; legacy BR6 |
| BR7 | An event with a key already processed by the consumer is ignored and the hit is counted in `processed_event` | R-UNI-40; legacy BR7; DP-09 |
| BR8 | Retry counts, intervals, folders, patterns, owners and alert roles are data rows of `interface_config`, never code | Principle 1; DT02; legacy BR8 |
| BR9 | rwb-integration has no inbound adapter: no file is picked up, checked or signed off, `receiveFile` is published but called by no flow of wave 1, and `interface_config` holds outbound rows only | D-RCV-35 U1; ADR-010; legacy BR9; FSD P2 v3 A1.6 |
| BR10 | An outbound item carries case IDs, business keys and the claim-check manifest, never an address, a name or an identity number; the file itself is held in rwb-document and file content never travels on a message, a workflow input or a log | CTL-11; Guardrails; Arch v5 slide 11; DP-03 |
| BR11 | The route state and the owner task belong to rwb-case and are raised only through its contract; rwb-integration writes no case row, no task row and no `debt_sale_account` row; `debt_sale_account` belongs to S6 rwb_debtsale and `recovery_case` to P3 rwb_case, reached through their contracts or an event from P2; the event element names, the carrier of the route state to resume and the task code and due date are Not specified in the source documents (GAP-2229) and are confirmed at contract review | DP-01; Arch v5 slide 13; legacy BR2; Ownership Map v1 (GAP-3160); ASM-B2-P3-013-4 |
| BR12 | There is no data lake: INT-19 and INT-20 are removed with no target in this service (reporting projects from business events in rwb-reporting; the decision ledger is the shared decision-record topic), so no lake file, no lake copy and no lake delivery row exists and JOB-13 and JOB-15 are removed | DP-17; Arch v5 slides 37 and 44; ASM-1073 |
| BR13 | The admin surface is four operations on `/api/recovery/integration/v1`; every POST carries the Idempotency-Key header and every resend is written to the ACE audit log with the user and the time | TSD P2 v3 T-A.1 and T-A.2; Arch v5 slide 11; legacy AC7 |
| BR14 | The run state of an outbound file is answered from the dispatch fields of its notices, the workflow run and the status the P2 contract returns; no run table is written; one read and one rerun are provided on the rwb-comms service base, not as operations of this service; the right to read run state is enforced at gateway-bff for the screen path; a local guard on the operation is confirmed with the edge owner | Architecture v5 slide 20; TSD P6 T-A.1 and T6.1; GAP-1166 |
| BR15 | rwb-integration registers no Temporal Schedule; per the Ownership Map, JOB-10, JOB-13 and JOB-15 belong to P6 rwb-comms, P7 rwb-decision and P9 rwb-reporting and not to rwb-integration; JOB-13 and JOB-15 are removed with the data lake (BR12), and rwb-integration provides the delivery capability that job owners call | Ownership Map Jobs; Arch v5 slide 44; FSD P2 v3 A1.5; GAP-1536 |
| BR16 | The bank scheduler owns the window, its opening time and the re-run of a window; the attempt ladder inside the window, the exception state and the owner task belong to this service; the single owner of a retry count is left to DL11 | Arch v5 slide 32; FSD P2 v3 AC-EXC-P2-001-01; GAP-1537 |
| BR17 | Interface-level targets for outbound file size, throughput, window length and daily volume are open under DL11, with the placeholder of Template and Rules section R9; the programme targets apply to every service | BRD Program v4 sections 6.1 to 6.4; GAP-1544 |

### 9. State transitions

`outbound_item.status` (LOV-OUTBOUND-STATUS):

| From | Event | Condition | To |
|---|---|---|---|
| none | `deliverFile(manifest)` accepted | The freshness check passes and the idempotency key is new | PENDING |
| PENDING | First attempt fails | The transport or a consumed contract raises a failure | RETRY |
| RETRY | A later attempt is sent | The interval in `retry_intervals_min` has elapsed | SENT |
| RETRY | Attempt count equals `max_attempts` | The last allowed attempt fails | EXCEPTION |
| SENT | The acknowledgment file arrives | The target confirms the file | ACKNOWLEDGED |
| EXCEPTION | Platform administrator resends | The right check passes and the item version matches | PENDING |

`recovery_case.route_state` in rwb-case, moved by rwb-case when it consumes the events this story publishes:

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed attempt of an outbound file for the case | RETRY_QUEUE |
| RETRY_QUEUE | RETRY_SUCCEEDED | A later attempt is sent | RESUME_STATE |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Attempt count equals max attempts | EXCEPTION_QUEUE |
| ANY_ACTIVE | DUPLICATE_EVENT | The key is already processed | RESUME_STATE |

The case status (`recovery_case.status`) does not change and this story writes no case row: rwb-case moves the route state and raises the task when it consumes `FileFailed`, through its own contract. `outbox_delivery.status` follows PENDING, RETRYING, DELIVERED and EXCEPTION and is the library's (DP-09). A held request (X1) is not an item at all: no row exists until the freshness check passes.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-integration service identity (its own login, DP-02) | Builds, stores, sends and retries the file; writes its own `interface_config` reads, `outbound_item`, `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` rows; publishes `FileDelivered` and `FileFailed` |
| rwb-source-data service identity | Answers the freshness, customer and account reads; the only identity with a read grant on `recovery.v_ace_*` |
| rwb-document service identity | Stores the built file and returns the upload link and the document ID |
| rwb-comms service identity | Requests the WIN file and answers the notice facts the build reads |
| rwb-case service identity | Applies the route-state change and raises the owner task |
| rwb-access service identity | Answers the authorise check on the exception-queue read and on the resend |
| RW-PLATADM, platform administrator | Lists exception items and deliveries, resends an item or a delivery, reads run state (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the held-file and failed-file alerts; reads run state (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version; holds no right on the exception queue |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run state and exception items (Platform administration, R) |

The service runs as its own login on `rwb_integration` (DP-02); the login name is Not specified in the source documents (GAP-0647; ASM-1070).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-OPS-136 to DF-OPS-148 | interface_config (P2, `rwb_integration`) | id, interface_id, direction, transport, inbound_path, file_pattern, data_product, max_attempts, retry_intervals_min, owner_role, alert_role, valid_from, valid_to | Read |
| DF-OPS-168 to DF-OPS-177 | outbound_item (P2, `rwb_integration`) | all 10 fields | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event (PLT library, created in `rwb_integration`) | all 6 fields | Write |
| DF-OPS-184 to DF-OPS-188 | idempotency_key (PLT library, created in `rwb_integration`) | all 5 fields | Write |
| DF-OPS-189 to DF-OPS-197 | outbox_event (PLT library, created in `rwb_integration`) | all 9 fields | Write |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery (PLT library, created in `rwb_integration`) | all 9 fields | Write |
| DF-ACE-076 | v_ace_contact (ACE view, read only by rwb-source-data) | contact_key | Read through the rwb-source-data contract |
| DF-ACE-077 | v_ace_contact (ACE view, read only by rwb-source-data) | person_key | Read through the rwb-source-data contract |
| DF-ACE-078 | v_ace_contact (ACE view, read only by rwb-source-data) | contact_value | Read through the rwb-source-data contract |
| DF-ACE-001 | v_ace_account (ACE view, read only by rwb-source-data) | account_key | Read through the rwb-source-data contract (INT-25) |
| DF-ACE-002 | v_ace_account (ACE view, read only by rwb-source-data) | account_code | Read through the rwb-source-data contract (INT-25) |
| DF-ACE-178 | v_ace_batch_status (ACE view, read only by rwb-source-data) | source_system | Read through the rwb-source-data contract |
| DF-ACE-179 | v_ace_batch_status (ACE view, read only by rwb-source-data) | business_date | Read through the rwb-source-data contract |
| DF-ACE-182 | v_ace_batch_status (ACE view, read only by rwb-source-data) | status | Read through the rwb-source-data contract |
| DF-ACE-186 | v_ace_batch_status (ACE view, read only by rwb-source-data) | is_complete | Read through the rwb-source-data contract |
| DF-LEG-019 | notice (P6, read through the rwb-comms contract) | sent_date | Read through the rwb-comms contract (INT-14) |
| DF-LEG-030 | notice (P6, read through the rwb-comms contract) | person_key | Read through the rwb-comms contract (INT-14) |
| DF-DOC-006 | document (P5, read through the rwb-document contract) | storage_ref | Read through the rwb-document contract (INT-14) |
| DF-SAL-033 | debt_sale_account (S6, never read by this service) | account_key | Read from the `deliverFile` request manifest that rwb-debtsale sends (INT-25) |
| DF-CAS-001 | recovery_case (P3, read through the rwb-case contract) | id | Read |
| DF-CAS-007 | recovery_case (P3, read through the rwb-case contract) | route_state | Written by rwb-case only, through its contract |
| DF-WRK-018 | task (P3, read through the rwb-case contract) | case_id | Written by rwb-case only, through its contract |
| DF-WRK-019 | task (P3, read through the rwb-case contract) | task_code | Written by rwb-case only, through its contract |
| DF-WRK-022 | task (P3, read through the rwb-case contract) | status | Written by rwb-case only, through its contract |
| DF-WRK-023 | task (P3, read through the rwb-case contract) | owner_role | Written by rwb-case only, through its contract |
| DF-REF-035 | role (P4, read through the rwb-access contract) | role_code | Read through the rwb-access contract |

Field IDs are those of the legacy story, the Logical Data Model and Data Dictionary and the TSD P2 Integration v3 T3.1. The five objects of `rwb_integration` sit in the service's own schema, and `processed_event`, `idempotency_key`, `outbox_event` and `outbox_delivery` are PLT library objects created in it (DP-09). `interface_config.inbound_path` (DF-OPS-140) stays in the table, holds the outbound folder of every outbound row and is never read as an inbound path. No row of `notice`, `document`, `debt_sale_account`, `recovery_case`, `task` or `role` is copied into `rwb_integration`, no foreign key leaves the schema, and the schema holds no grant on `recovery` or on another `rwb_*` schema (DP-01, DP-02). The personal-data fields DF-ACE-077, DF-ACE-078 and DF-LEG-030 are read in memory only to build the file: they are never written to a table of `rwb_integration` and never carried on a message, a workflow input, an outbox row or a log (BR10); their classification under Data Classification v5 is Not specified in the source documents (DOR-RWB-P2-E1007-APP-11).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/outbound-items` | Lists outbound items by `status`, `interfaceId`, `from` and `to` with id, interfaceId, status, attemptCount, lastError, caseCount, ownerRole and updatedAt | Platform administration R, scope applied | Not applicable |
| POST | `/admin/outbound-items/{itemId}/resend` | Sends an item in EXCEPTION again: status PENDING, attempt count 0, written to the ACE audit log with the user and the time | Platform administration U, scope applied | `Idempotency-Key` header; 409 when the item is not in EXCEPTION or the version changed |
| GET | `/admin/outbox/deliveries` | Lists outbox deliveries by `status`, `consumer`, `eventType`, `from`, `to`, `page` and `size` | Platform administration R, scope applied | Not applicable |
| POST | `/admin/outbox/deliveries/{deliveryId}/resend` | Sends a delivery in EXCEPTION again: status PENDING, attempt count 0 | Platform administration U, scope applied | `Idempotency-Key` header; 409 when the delivery is not in EXCEPTION |

The four paths are the TSD P2 Integration v3 T-A.1 rows API-P2-001 to API-P2-004 and the Ownership Map rows with P2, re-based on the service base by DP-13; Arch v5 slide 16 names `GET /interface-runs` and `POST /interface-runs/{id}/retry` instead, and that naming is superseded (GAP-0647; ASM-1076). Errors: 401 no session (MSG-P4-001); 403 no Platform administration right (MSG-P4-002); 404 unknown item or delivery (MSG-P4-003); 409 not in EXCEPTION or a changed version (MSG-GEN-004); 503 the store or a consumed contract is unavailable (MSG-GEN-006). The delivery operations are declared here as the E1 baseline of the exception queue; a later slice narrows the consumer filter of the read and does not re-declare them. The response field names and the problem body shape are fixed by RWB-P2-E1007-CON (ASM-1082).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020).

| Method | Path | Service | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=` | rwb-source-data (P1) | Whether the ACE batch of the business date is complete, and the source date the data carries (AC2 mechanism, X1) |
| GET | `/api/recovery/source-data/v1/customers/{personKey}` | rwb-source-data (P1) | The addressee facts of the file by `person_key` and `contact_key` (AC2) |
| GET | `/api/recovery/source-data/v1/accounts/{accountKey}` | rwb-source-data (P1) | The account facts of the INT-25 tape by `account_key` (AC1) |
| GET | Not specified in the source documents (GAP-0647; ASM-1081) | rwb-comms (P6) | The notice facts behind INT-14: notice ID, `sent_date`, `person_key` and document ID |
| POST | `/api/recovery/document/v1/documents` | rwb-document (P5) | Stores the built file and returns the upload link and the document ID (AC2, AC3) |
| GET | `/api/recovery/document/v1/documents/{id}` | rwb-document (P5) | Follows the claim-check link of a stored file (X10) |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | rwb-case (P3) | The route-state change to RETRY_QUEUE and EXCEPTION_QUEUE and the one owner task (AC3) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Platform administration R and U check on the list and the resend, cached per session (X7) |
| POST (ACE Common path) | INT-22 audit and PII logging | ACE Common | The resend record with the user and the time, and the PII access event of each personal-data read |

The rwb-comms notice-fact read is named by its legacy purpose only (the build reads `notice.sent_date` and `notice.person_key`, DF-LEG-019 and DF-LEG-030, and `document.storage_ref`, DF-DOC-006); its path, query and field names are Not specified in the source documents (GAP-0647; ASM-1081) and are fixed in the rwb-comms contract and in RWB-P2-E1007-CON. The `debt_sale_account` rows of INT-25 are not read by any call: they arrive in the `deliverFile` manifest that rwb-debtsale sends (ASM-1072).

#### 12.3 Events published

| Event | Topic | Key | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | caseId | fileId, interfaceId, businessDate, documentId, sha256, recordCount, requesting service |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | caseId | fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds, ownerRole |

Both are written to `outbox_event` in the same transaction as the item state change and relayed by the outbox relay with the CloudEvents 1.0 envelope in binary mode; no personal data and no file content is carried (DP-09, Arch v5 slide 11). The local decision-record library publishes `DecisionRecorded` on `rwb.decision-record.v1` when the item moves to EXCEPTION or is resent (DP-03). The host of the two events is the requesting service, by the consumer column of Arch v5 slide 43 ("requesting service").

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Releases a held request after a failed batch and lets the next window run (X1 mechanism); record key `{sourceSystem}:{businessDate}`, `ce_subject` = sourceSystem, payload `sourceSystem`, `businessDate`, `status`, `completedAt`; this service acts on only the event with `sourceSystem` ALS and `status` COMPLETED |

The request itself is not an event: rwb-integration is called as a task (Arch v5 slide 16, "events (none: called as a task)"), so the requesting flows arrive through `deliverFile` and this service subscribes to `AceDataReady` only, with the inbox dedupe of `processed_event`. `AceDataLate` is P1's alert to the platform and to the gateway banner and is not consumed here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| `deliverFile(manifest)` | Activity, provided by P2 and called by the requesting services | `rwb-integration` | Validates the manifest, checks freshness, writes the `outbound_item` in PENDING under the idempotency key and starts `OutboundFileWorkflow`; returns the item reference and its status. The manifest carries fileId, batchId, sha256, record count, interfaceId, businessDate, caseIds, idempotencyKey, the claim-check link and the requesting service |
| `receiveFile` | Activity, provided by P2 | `rwb-integration` | The published inbound counterpart of the activity contract; wave 1 calls it from no flow, because there is no inbound adapter (BR9) |
| `OutboundFileWorkflow` | Workflow, one execution per interface and business date, workflow ID `<interfaceId>:<businessDate>` | `rwb-integration` | Builds, stores, sends, retries and reports one outbound file; owns the retry timers |
| `buildOutboundFile` | Activity | `rwb-integration` | Builds the file from the request manifest, the `outbound_item` and the notice and account facts of the consumed contracts |
| `storeOutboundFile` | Activity | `rwb-integration` | Stores the file in rwb-document and records the document ID and the sha256 on the item |
| `sendFileOverMft` | Activity | `rwb-integration` | The only step that opens the MFT/SFTP session and the PGP encryption; idempotent on the fileId |
| `parkItemInException` | Activity | `rwb-integration` | Sets EXCEPTION, writes `FileFailed` to the outbox and raises the owner task through the rwb-case contract |

The retry policy of every activity is the workflow kit's, with the 4xx answers of the consumed contracts classified as non-retryable and a 5xx or a timeout as retryable (DP-10). That `deliverFile` returns after starting the local workflow, instead of holding the caller for the whole retry ladder, is Not specified in the source documents (GAP-0647; ASM-1078).

#### 12.6 Schedules

| Window or timer | When | Owner of the trigger | Legacy reference |
|---|---|---|---|
| WIN file window | Daily 16:00 | Bank Airflow opens the window and calls the requesting service; rwb-integration receives `deliverFile` | JOB-10; Arch v5 slides 16, 31, 32 and 44 |
| Debt-buyer file window | Per lot, when the lot is awarded | Bank Airflow opens the window; rwb-debtsale requests | JOB-10; Arch v5 slide 32 (buyer files per lot) |
| Retry timers | Attempt 2 five minutes and attempt 3 fifteen minutes after the previous attempt, up to 45 minutes | `OutboundFileWorkflow` timers, from `interface_config.retry_intervals_min` | Legacy AC3; TSD P2 v3 T4 |
| Outbox relay | Every minute | The PLT relay of DP-09, in every service | JOB-11 |

No Temporal Schedule is registered by this story: the two windows belong to the bank scheduler and the relay is the platform's (ASM-1074). The exact trigger contract is Not specified in the source documents (GAP-0334; GAP-0647; GAP-0650; ASM-1074) and belongs to RWB-P2-E1007-OPS until the Airflow owner and the platform observability owner name it; JOB-13 and JOB-15 are removed with the data lake (DP-17).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `interface_config` | `rwb_integration` | P2 | The versioned outbound interface rows: target, transport, attempts, intervals, owner and alert role |
| `outbound_item` | `rwb_integration` | P2 | One outbound file waiting, sent or in the exception queue, with its manifest reference |
| `outbox_event` | `rwb_integration` | PLT library, created in `rwb_integration` | The event written in the same transaction as the item state change |
| `outbox_delivery` | `rwb_integration` | PLT library, created in `rwb_integration` | One delivery per event and consumer, with its attempts |
| `processed_event` | `rwb_integration` | PLT library, created in `rwb_integration` | The inbox: consumer, key, CloudEvents id, hit count |
| `idempotency_key` | `rwb_integration` | PLT library, created in `rwb_integration` | The stored response of the two POST operations, kept 24 hours |

`job_catalog` is P2's third table (Ownership Map) and lists the jobs of the job catalog read with owner, schedule, run book and alert threshold; whether JOB-10 and JOB-11 rows are loaded into it is Not specified in the source documents (GAP-0647; ASM-1079), and this story writes no row in it. No other table is named: `notice`, `document`, `debt_sale_account`, `recovery_case` and `task` are other owners' and are reached only through their contracts (DP-01). The legacy run and sign-off tables do not exist in the target (TSD P2 v3 T3.1). The legacy identity and table names are not fields of the Logical Data Model v9 or Data Classification v5 and are not used by any table or field of this story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | Freshness COMPLETE for 2026-11-10 and a FAILED batch at 05:20 behind it; addressee and address by `contact_key` for the 85 notices; account facts for the 120 synthetic account keys; one delayed answer beyond 2 s for X9 |
| rwb-comms WireMock | The P6 contract | The 85 approved notices of 2026-11-10 with `person_key`, `sent_date` and document ID; one 404 |
| rwb-document WireMock | The P5 contract | `POST /documents` returning a document ID and upload link; `GET /documents/{id}` returning the storage reference; one 404 for X10 |
| rwb-case WireMock | The P3 contract | The route state RETRY_QUEUE after the first failure, EXCEPTION_QUEUE after the last, and one open task for RW-PLATADM |
| rwb-access WireMock | The P4 contract | Platform administration R and U granted to RW-PLATADM; refused to RW-CASEOWN with MSG-P4-002 |
| rwb-debtsale request stub | The caller side of `deliverFile` | The INT-25 request manifest with 120 synthetic account keys for an awarded lot |
| ACE Common audit and PII stub | INT-22 | Accepts the resend record and the PII access events; refuses once for the 503 path |
| MFT/SFTP edge stub | The party at the SFTP endpoint | A receiver that accepts the file, and one that fails three times for AC3 |
| Kafka stub | `rwb.source-data.events.v1` | One `AceDataReady` for 2026-11-10 (key `ALS:2026-11-10`, `status` COMPLETED), a duplicate of it, and the event key `EV-10:TRT-0001:v1` sent twice |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 9 consumed | The four admin operations provided on `/api/recovery/integration/v1`; the freshness, customer and account reads on rwb-source-data, the notice read on rwb-comms, the store and read on rwb-document, the case action on rwb-case, the authorise on rwb-access and the ACE Common audit path consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | 2 published, 1 consumed | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` with the outbox and relay; `AceDataReady` consumed with the inbox dedupe; `DecisionRecorded` published by the library |
| Temporal | 1 workflow, 5 activities | `OutboundFileWorkflow` with four step activities, plus the provided `deliverFile(manifest)` and `receiveFile` activities on queue `rwb-integration` |
| File | 2 party interfaces, 1 reporting delivery | INT-14 WIN registered mail over MFT/SFTP with PGP; INT-25 debt buyer tape per lot over MFT/SFTP with PGP; INT-19 delivered to rwb-reporting through `deliverFile`; no data lake |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, modules `outbound`, `transport`, `idempotency` and `admin`, Java package `th.co.scb.ace.workbench.recovery.integration.outbound` and its siblings. The legacy folder `src/main/java/recovery/integration/adapter` and the legacy package `recovery.integration.adapter` are replaced by the service package under the naming rule of Architecture v5 slide 41 (DP-02, ASM-1070).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; never read another service's tables | none |
| DP-02 | Legacy shared service login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; this service owns no ACE view and holds no grant | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the lists stay rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the service topic, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Workflow kit: one workflow per interface and business date, event-started work, retry timers | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-16 | `recovery.integration.adapter` | The rwb-integration contract: the activity contract, the events and the admin operations | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed: delivery to rwb-reporting through `deliverFile` and continuous ingest in rwb-decision | none; gap if a lake file is needed |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-09 | H RWB-PLT-N001-CON |

DP-05 resolves to a prohibition as well as a rule: rwb-integration holds no grant on the `recovery` schema, so the only path to an ACE fact is the P1 contract. DP-17 resolves to "no lake target, no lake file, no lake delivery row" and is applied to the retired JOB-13 and JOB-15 statements (ASM-1073).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntegrationController | Controller | The four admin operations; validation; the mapping to the problem-details envelope |
| OutboundRequestService | Service | Receives the `deliverFile` manifest, checks freshness, writes the `outbound_item` and starts the workflow |
| OutboundFileBuilder | Service | Builds the file from the manifest, the item and the consumed facts; applies the layout and control-total checks of the interface row |
| OutboundSender | Service | The only class that opens an MFT/SFTP session and applies PGP; sends, records the attempt and the result |
| RetryPolicy | Service | Reads `max_attempts` and `retry_intervals_min` from the row and computes the next attempt, never from code |
| IdempotencyGuard | Service | Inserts into `processed_event`; on conflict increments `hit_count` and returns false, and serves the `idempotency_key` record of the POSTs |
| OutboxWriter, OutboxRelayClient | Service | Writes the event in the same transaction and hands it to the PLT relay |
| SourceFactClient | Client | The freshness, customer and account reads on the rwb-source-data contract, one hop and 2 s (DP-05, DP-11) |
| NoticeFactClient | Client | The notice facts behind INT-14 on the rwb-comms contract (ASM-1081) |
| DocumentClient | Client | Stores the file and follows the claim-check link on the rwb-document contract |
| CasePathClient | Client | The route-state change and the owner task on the rwb-case contract (DP-01) |
| AccessCheckClient | Client | The Platform administration R and U check through the rwb-access contract, cached per session by the guard library |
| AuditWriter | Client | The resend record and the PII access events through ACE Common (INT-22) |
| OutboundFileWorkflow, buildOutboundFile, storeOutboundFile, sendFileOverMft, parkItemInException | Workflow and activities | The one file run, its steps and its retry ladder on queue `rwb-integration` |
| ExceptionQueuePanel | React component | SCR-09 list, filters, resend action and the masked error and case counts |

**Database and migrations**

- The per-service Flyway sequence of `rwb_integration` starts with V0001, which creates `interface_config`, `outbound_item` and `job_catalog` with the TSD P2 v3 T3.1 columns (DP-15, RWB-PLT-E1044-CON). The outbox, inbox and idempotency objects are created by the PLT library migration in the same schema (DP-09).
- Constraints: unique `(interface_id, valid_from)` on `interface_config`; unique `(idempotency_key)` on `outbound_item`; index `(status, next_attempt_at)` on `outbound_item`; unique `(consumer, idempotency_key)` on `processed_event`; unique `(event_id, consumer)` on `outbox_delivery`.
- No table of another service, no view of the `recovery` schema and no cross-schema foreign key (DP-01, DP-02). The legacy run and sign-off tables are not created.

**Configuration and reference data**

- `interface_config` rows for INT-14, INT-19, INT-20 and INT-25 with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes, loaded by RW-REFADM through the reference-data load; a row with direction INBOUND is refused because no inbound interface exists (ASM-1079).
- Lists LOV-DIRECTION, LOV-TRANSPORT, LOV-DATA-PRODUCT, LOV-ROLE, LOV-OUTBOUND-STATUS and LOV-OUTBOX-DELIVERY come from the reference-data contract with the version in force (DP-07).
- Property `rwb.integration.sftp.endpoint` and the PGP key reference per environment come from RWB-P2-E1007-INF; no endpoint, credential or key is written in code or in a values file (NFR-052).
- Feature flag `rwb.integration.file-adapters` on the platform flag library: off means the `deliverFile` activity refuses and no item is written.

**Build steps**

1. The V0001 migration with the three tables, their constraints and their repository tests.
2. `OutboundRequestService` with the freshness check and the hold path, against the rwb-source-data fake.
3. `OutboundFileBuilder` with the manifest, the notice and account facts and the layout and control-total checks; AC1 and AC2.
4. `DocumentClient` with the store and the claim-check read; AC2.
5. `OutboundSender` and `RetryPolicy` with the row-driven intervals, the row lock, the EXCEPTION move and `FileFailed`; AC3 and AC6.
6. `CasePathClient` and `parkItemInException` with the route state and the one owner task; AC3.
7. `IdempotencyGuard` and the inbox on every listener, with the hit count; AC5.
8. The four admin operations with the access check, the Idempotency-Key rule, the 409 and the audit write; AC7 and TC-E1-007-10.
9. `OutboundFileWorkflow` and its activities registered on queue `rwb-integration`, with the retry policy and the build ID.
10. The contract tests of RWB-P2-E1007-CON and the boundary test that fails on any cross-schema statement and on any SFTP call outside the transport component.

**Feature switch.** `rwb.integration.file-adapters`.

**Done when.** The tests of section 16 pass, the boundary test runs in the pipeline, the contract tests of INT-14 and INT-25 pass in SIT against the contract fakes, and no query of this story reaches the `recovery` schema or another `rwb_*` schema.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | An outbound file is held because the ACE batch is not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | An outbound transfer fails and is queued for retry, or a consumed contract is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P2-001 | An outbound item moves to the exception queue | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-GEN-004 | A resend on an item whose version changed, or on one that is not in EXCEPTION | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Saved. |
| MSG-P4-001 | A call without a session, or a session with no Recovery role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the Platform administration right calls the list or the resend | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A resend or a list names an unknown item or delivery | This record was not found. |

No identifier is renumbered by the realignment. MSG-P1-001 and MSG-P2-001 take the wording of the Error and Message Standard v4, MSG-GEN-004, MSG-GEN-005, MSG-GEN-006, MSG-P4-002 and MSG-P4-003 keep their legacy text unchanged, and MSG-P4-001 is the access message of the Access and administration module.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-09 Exception queue | Loading | Sees the list placeholder while the gateway-bff composite route answers |
| SCR-09 Exception queue | List | Sees failed outbound items with the interface, the attempt count, the last error and the case count, filtered by status and interface |
| SCR-09 Exception queue | Empty | Sees the empty list when no item is in EXCEPTION |
| SCR-09 Exception queue | Error | Sees MSG-GEN-006 when a consumed contract is unavailable |
| SCR-09 Exception queue | No access | Sees MSG-P4-002 for a role without the Platform administration right and MSG-P4-001 with no Recovery role |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-2964) |
| SCR-09 Exception queue | Resend | Resends one item, reads MSG-GEN-005 and sees the item return to PENDING |
| SCR-09 Exception queue | Refused | A role without the right reads MSG-P4-002 and nothing changes |
| SCR-09 Exception queue | Deliveries | Sees the outbox deliveries with their status, consumer, attempt count and last error code |

The screen is reached through the gateway-bff composite route at the edge and calls the owner once per operation (DP-19); the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON. The data steward receives the held-file and failed-file alert from the alert rules over the held-item series and over `FileFailed`, with the rules and their identifiers owned by RWB-P2-E1007-OPS; the legacy event names `rwb.integration.outbound.held` and `rwb.integration.outbound.failed` are not event names of the target (GAP-0647; ASM-1077).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-01 | AC1, BR1, BR8, BR9, BR12 | End to end | Synthetic INT-25 tape, 120 accounts; interface load with an INBOUND row |
| TC-E1-007-02 | AC2, BR2, BR10 | End to end | 85 synthetic notices with person_key; rwb-source-data contract fake rows by party_id |
| TC-E1-007-03 | AC3, BR4, BR5, BR6, BR11 | End to end | Synthetic WIN file for 85 cases; SFTP stub failing three times |
| TC-E1-007-04 | AC4, BR3 (run by RWB-ITG-E1007-ITG) | End to end | ALS batch FAILED for 2026-11-10; WIN file due at 16:00 |
| TC-E1-007-07 | AC7, BR7 | End to end | Event key EV-10:TRT-0001:v1 sent twice |
| TC-E1-007-08 | AC2 | End to end | One due item, two sender threads |
| TC-E1-007-09 | AC4, AC9, BR13 | End to end | Item in EXCEPTION after 3 attempts; a PENDING item for the refused resend |
| TC-E1-007-10 | AC8, Access | Component | RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend; refused with MSG-P4-002 |
| TC-E1-007-11 | §12 operations, events and activities | Contract | Consumer-driven contract fakes of rwb-source-data, rwb-document, rwb-comms, rwb-case and rwb-access, one per operation, event and activity of §12 |
| TC-E1-007-12 | §12.7 tables (ASM-3438) | Component | Boundary rows of the six tables of §12.7 in rwb_integration |
| TC-E1-007-05 | None (retired with the inbound file load; the behaviour is ACE ingestion and EV-27 AceDataLate) | NFR | Asserts that no inbound FileLoadAdapter, FileCheckRunner, RecordLoader, inbound folder listing, DQ-057, DQ-059, missing-file run row, JOB-09 File loads or legacy run or sign-off table exists; the case "file missing at the cut-off" is ACE ingestion's and EV-27 AceDataLate; closed when RWB-ACE-001 publishes its checks |
| TC-E1-007-06 | None (retired with the inbound file load; the behaviour is ACE ingestion) | NFR | Asserts the same absence of the inbound load; the case "same file delivered twice" is ACE ingestion's; closed when RWB-ACE-001 publishes its checks |
| TC-E1-007-13 | AC10, BR11, BR12, BR13 | Component | Not specified in the source documents (NEWAC-RWB-P2-E1007-APP-AC10) |
| TC-E1-007-14 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P2-E1007-APP-AC11) |
| TC-E1-007-15 | AC12 | NFR | rwb-source-data contract fake does not answer the postal-addressee read within 2 s for one of the 85 notices |
| TC-E1-007-16 | AC13 | Component | Outbound item OB-0002 in EXCEPTION after 3 attempts; a status change to PENDING requested without a resend |
| TC-P2-E1007-APP-01 | AC2 | End to end | AC2 Outbound file reads ACE only through the views (legacy RWB-E1-007 AC2) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E1-007-04 covers AC4, whose criterion is owned and run by RWB-ITG-E1007-ITG; the row is kept here because the legacy story lists it, and the hold path it depends on is exercised by X1 as a component test. TC-E1-007-05 and TC-E1-007-06 are kept as the legacy IDs without restating the retired inbound behaviour (FSD P2 v3 A1.6), as NFR assertions of absence that close when RWB-ACE-001 publishes its checks. TC-E1-007-01 to TC-E1-007-03 and TC-E1-007-07 to TC-E1-007-16 are the ones this story runs, against its own operations and the contract fakes; the real cross-service journey of the key is proven by RWB-ITG-E1007-ITG.

### 17. Guardrails

- No business value in code: retry counts, intervals, folders, patterns, owners, alert roles and the feature switch are data rows and environment values, never literals.
- No personal data in logs, events, workflow inputs or tests: file contents are never logged, only names, counts and hashes; the events carry IDs, codes and counts.
- No read of another service's tables and no ACE view: the freshness, customer and account facts come only through the rwb-source-data contract, the notice facts only through rwb-comms, the document only through rwb-document, the route state and task only through rwb-case and the right only through rwb-access (DP-01, DP-05).
- Only the transport component opens a session to another system; the boundary test fails the build on any other SFTP, file-system or HTTP client use inside the file path.
- `rwb_integration` holds no foreign key into another schema and no copy of an ACE, case, notice or document row; the links are business keys and the claim-check manifest.
- No inbound adapter, no inbound folder, no sign-off and no `interface_config` row with direction INBOUND; `receiveFile` is published and called by no flow.
- No data lake and no lake delivery row; INT-19 and INT-20 carry no lake target (DP-17).
- One hop, no chaining: the build never calls a downstream of a downstream, and the breaker and bulkhead are per downstream.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read through the ACE views and leaves through ACE's paths and the Workbench outbound adapters | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE; BR1, BR2 | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Log every outbound file, retry on a defined schedule, exception queue with a task for a named owner | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40; BR4, BR5, BR6, BR7 | TC-E1-007-03, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09, TC-E1-007-10 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; no file load is run | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06; BR3, BR9 | TC-E1-007-01, TC-E1-007-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, claim-check for files | Decision log, D-RCV-60; ADR-020 | DP-11, DP-16 | All recovery processes | ADR-020; DP-01; DP-09 | TC-E1-007-02, TC-E1-007-03, TC-E1-007-11, TC-E1-007-12 |

TC-E1-007-10 traces to the access rule behind the resend (BR13, MSG-P4-002) and is asserted through the rwb-access contract rather than a requirement row of its own. The retirement of the lake statements of JOB-13 and JOB-15 is carried by DP-17 and by the combined gap row of GAP-0647. DL06 is an open decision: its assumptions ASM-0189, ASM-2559, ASM-2608 and ASM-2776 stand until it closes, and the rows of REQ-DRI-008 rest on them.

### 19. Out of scope

- The contract documents, the fakes, the error envelope and the versioning rule (RWB-P2-E1007-CON); this story implements against them.
- The MFT/SFTP endpoints, the PGP keys, the key store, the firewall and DNS, the staging area, the size and timeout budgets and the certificate rotation (RWB-P2-E1007-INF).
- The Helm chart, the values files, the topic and queue provisioning, the two Airflow windows, the alerts, the dashboards and the runbook (RWB-P2-E1007-OPS).
- The real cross-service journey of the path with all services live (RWB-ITG-E1007-ITG).
- The document hub itself: storage, custody, WORM and retention (P5 stories); this story only stores and follows a claim-check link.
- The ACE views and the read grant on them (RWB-P1-E1069-APP) and the freshness gate with `AceDataReady` (RWB-P1-E1015-CON and the P1 stories).
- Inbound source ingestion, its schedules, its checks and the ACE team sign-off (RWB-ACE-001).
- The WIN notice content, template and merge fields (RWB-E2-021 and the P6 stories) and the debt sale lot and award flow (S6 stories).
- The reporting extract itself in rwb-reporting and the decision ingest in rwb-decision; this story only delivers what they request.
- The full SCR-44 interface and job monitor (Epic 2 and Epic 8) and production monitoring of the exception queue (RWB-E1-056).
- GL write-off posting, read back through `v_ace_write_off`, and the SOC log through ACE logging (INT-22).
