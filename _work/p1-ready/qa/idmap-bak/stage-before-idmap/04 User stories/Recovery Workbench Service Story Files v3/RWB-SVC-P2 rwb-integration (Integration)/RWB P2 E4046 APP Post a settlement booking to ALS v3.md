# RWB-P2-E4046-APP Post a settlement booking to ALS

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

| Item | Value |
|---|---|
| Story key | RWB-P2-E4046-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P2-L |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E4046-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON (`deliverFile(manifest)`, already declared); rwb-case and rwb-access operations pending CG-ALL-3323 and CG-ALL-3324 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to no REQ IDs) |
| Readiness decisions | RD-P1-008 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-046 for rwb-integration. The legacy story sent the agreed settlement terms to ALS through the outbound interface, tracked the item in `outbound_item` and read the booked position back from the ACE views, all inside one deployable. This story builds the rwb-integration half of that journey only: the ALS booking interface row and its version, the `deliverFile(manifest)` path the settlement workflow calls as a task, the `outbound_item` lifecycle with its attempts, intervals, exception queue and resend, the two outbound events and the service's own decision record committed with the state change. The accepted treatment terms stay with rwb-treatment, the booking and posting and the legacy AC2 stay with rwb-payment, the ACE read-back of `v_ace_account` and `v_ace_payment` stays with rwb-source-data, the case state stays with rwb-case and the central ledger with rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E4046-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 25 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **Credit Administration officer**, I want **the agreed settlement terms of an accepted treatment to leave the Workbench for ALS as one outbound item on the ALS booking interface, sent by rwb-integration on the transport and retry schedule of the interface row in force, acknowledged or retried to the exception queue with a task for the owning role and a resend path, with one item for the treatment and its Idempotency-Key and the service's own decision record written with every state change**, so that **a settlement that has passed its point of no return is provably on its way to ALS, a failed sending is found and can be re-sent the same day, and no booking leaves the bank without a record behind it**.

This story is one of the three stories the legacy key opens after the split. The accepted split, stated by RWB-ITG-E4046-ITG section 19 and fixed by the Ownership Map, is: **S2 rwb-treatment** owns the accepted settlement terms and their state; **P8 rwb-payment** owns the booking, the posting and the legacy AC2 "Not recorded"; **this story** owns the ALS interface row in `interface_config`, the `deliverFile(manifest)` path on queue `rwb-integration`, the `outbound_item` lifecycle, the retry and exception behaviour, the resend and the two events; **P1 rwb-source-data** owns the read-back of `v_ace_account` and `v_ace_payment`; **P3 rwb-case** owns the case state; **P7 rwb-decision** owns the central ledger; and **RWB-ITG-E4046-ITG** proves the chain across the real services against its own four test cases.

The ALS interface id, its transport, the message or file layout, the result codes and the retry values are interface configuration data, not code: the values are Not specified in the source documents (GAP-0673; ASM-1214), and this story builds the row's reader and the lifecycle that obeys it.

### 2. Business rationale

A settlement that is signed and accepted but never booked in ALS leaves the agreement unenforceable and the payment due date unset, so the customer's money arrives against a case with nothing to receive it. The booking is also the point of no return of the settlement (Temporal and Drools Design slide 18, "Point of no return / undo: ALS/NLEADS booking"; slide 26), which means the fact that the terms left the bank, and what they were, has to be provable afterwards. That proof has two halves, and this slice owns the second: the terms leave as **one outbound item** on the ALS interface, and the service writes **its own decision record with the state change**.

The behaviour the business asked for is unchanged from the legacy key; only the seams moved. The Workbench still sends the agreed terms to ALS through the outbound interface and tracks the item (legacy story, AC1); every outbound is still logged, retried on a defined schedule and placed in an exception queue after the retry limit with a task for a named owner (REQ-DRI-007); nothing is still sent directly to a system of record (REQ-DRI-006); and a booking still sets the payment due date once the terms are booked (R-SET-13) and records the booking reference when ALS and NLEADS acknowledge (R-RES-22), while a rejection still puts the error on the officer queue and keeps the case with operations (R-RES-23). What is new is that the item, the row that configures it, the attempts, the events and the record now sit in one service with one schema and one login, and that the facts behind them are other services' and are never copied here.

**What the split changes, and why it changes here.**

- **DP-03.** The `DecisionLogWriter` of the monolith becomes the local decision-record library: each state change of the item that matters — the creation of the item, its move to EXCEPTION and its resend — is written as one record in `rwb_integration` in the same local transaction as the state change, and the library publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for the central ledger in rwb-decision. The record carries the interface id, the item id, the business date, the attempt count and the outcome; the default code of the record is the library's until the rule registry publishes one (ASM-1215). A failed record write sends nothing (AC6). The accepted-terms record of the treatment and the central ledger entry are not this service's and are not written here.
- **DP-05.** `AceSourceQuery` and every `recovery.v_ace_*` read leave this slice entirely: the booking does not read ACE at all. The booked position and the settlement payment are read after the next ACE batch by rwb-source-data through its data product, and no statement of this service touches a view, holds a grant on `recovery`, or calls rwb-source-data for this journey. The accepted terms arrive in the `deliverFile` manifest the caller sends, so this story makes no call to rwb-treatment either.
- **DP-19.** The exception queue the platform administrator works is SCR-09 and is a gateway-bff composite route over `GET /api/recovery/integration/v1/admin/outbound-items`; the browser never calls this service directly, and no screen of this slice is registered.
- **DP-16 is not re-applied.** The activity contract, the two outbound events and the two admin operations already exist on the integration base (RWB-P2-E1007-APP and its CON story). This story adds the ALS interface row, the ALS path through `deliverFile(manifest)`, the retry and exception behaviour for that row and the two activities the lifecycle needs, and adds no path to `/api/recovery/integration/v1`.

**What this slice does not decide.** The settlement amount 820000, the treatment `T-0001` and account `A-0001` are the caller's facts and the test data of the legacy key. Whether the booking is accepted is rwb-payment's. Whether the case moves to `AWAITING_PAYMENT` is rwb-case's, on R-SET-13. Whether the booking reference is recorded on the treatment is rwb-treatment's, on R-RES-22. Whether the rejection reaches the officer queue as a case state is rwb-case's, on R-RES-23; this slice raises the item to the exception queue and one task, which is the fact that step reads.

### 3. Preconditions

- RWB-P2-E1007-APP is delivered: the integration base, its `interface_config` and `outbound_item` tables in `rwb_integration`, its `deliverFile(manifest)` and `receiveFile` activity contract on queue `rwb-integration`, its `OutboundFileWorkflow`, its four admin operations on `/api/recovery/integration/v1`, its problem-response mapping and its migration sequence.
- RWB-P2-E1007-CON is published: the OpenAPI 3.1 document of the admin operations, the AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`, the activity contract with the manifest, the error envelope and the Idempotency-Key rule.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-09 Exception queue (DP-19).
- The ALS booking interface configuration row is loaded for the environment through the reference-data load, with direction OUTBOUND, the interface id, the transport, the file pattern or layout reference, `max_attempts`, `retry_intervals_min`, `owner_role`, `alert_role`, `valid_from` and `valid_to`. Every one of those values is Not specified in the source documents (GAP-0673; ASM-1214).
- The settlement workflow of the caller is able to call `deliverFile(manifest)` on queue `rwb-integration` under its own service identity, with treatment `T-0001` accepted at a settlement amount of 820000 for account `A-0001` and no call of this story back to rwb-treatment.
- rwb-document answers `GET /api/recovery/document/v1/documents/{id}` with the stored booking file and a SAS link, so `payload_ref` holds a reference and never file content.
- The ALS receiving endpoint of the environment exists and returns an acknowledgement this service can read, behind the transport stub of §12.8. Its address, its credentials and its result codes are Not specified in the source documents (GAP-0673; ASM-1214, ASM-1218).
- The legacy key names no feature switch for this behaviour; the slice runs behind the platform flag library's key for the outbound path, whose value is Not specified in the source documents (GAP-0673; ASM-1219).
- The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0673; ASM-1212).
- No build dependency, no contract dependency, no integration dependency and no external dependency: Day 1, with the fakes of §12.8 in place from the first run.

### 4. Flow

1. The settlement workflow of the caller — the settlement step of `TreatmentWorkflow` on queue `rwb-treatment` after `rwb.treatment.TreatmentApproved.v1`, or the booking step of rwb-payment where the environment runs the posting there — calls the activity `deliverFile(manifest)` on queue `rwb-integration` with the interface reference of the ALS booking, the business date, the treatment id, the case ids, the account key, the settlement amount 820000, the claim-check reference of the terms document and its Idempotency-Key. rwb-integration consumes no event for this: it is called as a task (Arch v5 slide 16, "IN: events (none: called as a task)").
2. `DeliverFileEntry`: validates the manifest (interface reference, business date, treatment id, case ids, idempotency key, claim-check reference) and refuses a manifest that misses a required value with MSG-GEN-001 and no row written.
3. `InterfaceConfigReader`: reads the `interface_config` row of the ALS booking interface in force at the business date — `transport`, `file_pattern`, `data_product`, `max_attempts`, `retry_intervals_min`, `owner_role`, `alert_role` — and refuses the call when no row is in force at that date (AC2, AC7). No value of the row is a constant in code; the row is read under the reference-data contract DP-06 and DP-07.
4. `ItemIdempotencyGuard`: looks up `outbound_item` by the interface id and the Idempotency-Key. When an item exists, the call returns that item and creates nothing; the uniqueness of the pair is what makes a repeat of the same command a no-op (AC1; ASM-1220).
5. `AlsBookingBuilder`: builds the booking file from the manifest and the documents behind the claim-check links, in the layout and with the control totals of the row, after fetching the stored file through `GET /api/recovery/document/v1/documents/{id}` and keeping the document id and the sha256 on `payload_ref`.
6. `ItemWriter`: writes one `outbound_item` in status PENDING with `attempt_count` 0, `next_attempt_at` due at once, `owner_role` from the row, `case_ids` from the manifest, and the treatment id inside the payload reference block, in one local transaction with the decision record of the creation (ASM-1215).
7. `AlsBookingSender`, the only class that opens the transport of the row: sends the file, sets the item SENT on the send and writes the attempt and its result; a failure before the send leaves the item PENDING for the next pass.
8. The acknowledgement arrives: `AcknowledgementMapper` reads the result, and on a positive acknowledgement sets the item ACKNOWLEDGED, clears `next_attempt_at`, keeps the acknowledgement reference in `payload_ref`, and writes `rwb.integration.FileDelivered.v1` to the outbox in the same transaction (AC3; ASM-1218).
9. A failed attempt: `RetryScheduleReader` takes the next interval of `retry_intervals_min` from the same row, sets the item RETRY with `next_attempt_at` and the failure code in `last_error`, and the workflow timer for that interval wakes the next pass (AC4). No interval, no count and no delay is compiled into the service.
10. The last allowed attempt fails: `ExceptionRaiser` sets the item EXCEPTION in one local transaction with `rwb.integration.FileFailed.v1` written to the outbox and the item's decision record, and then raises one open task for the row's `owner_role` through the rwb-case contract naming the item, the interface and the treatment; the item shows in the exception queue with MSG-P2-001 (AC4; ASM-1217).
11. The outbox relay publishes `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` with the CloudEvents envelope and the case id as key, carrying ids and facts only.
12. `ResendService`: a platform administrator resends an item in EXCEPTION through `POST /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend`; the right is checked through the rwb-access contract, the item returns to PENDING with `attempt_count` 0 and no second item and no second file, the resend is written to the ACE audit log with the user and the time, and the response carries MSG-GEN-005 (AC5).
13. The sender takes each due item with `FOR UPDATE SKIP LOCKED`, so two worker instances never send the same file twice and the attempt count stays correct.
14. Every state change that matters — creation, EXCEPTION, resend — commits its decision record with it or not at all; a failed record write leaves the state unchanged, sends nothing, and raises an incident with MSG-P7-003 (AC6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same treatment is delivered twice with the same Idempotency-Key | No second item, no second file, no second event; the call returns the existing item | None | AC1 |
| X2 | The same treatment is delivered with a new Idempotency-Key | A second item is created: the key is the caller's command key, not a treatment key, and the caller's own workflow id is what stops a second command | None | AC1 |
| X3 | No ALS booking interface row is in force at the business date, or the row is not OUTBOUND | The call is refused before any row is written; the item is not created and nothing is sent | MSG-GEN-001 | AC7 |
| X4 | The transport or the ALS endpoint fails on an attempt | The item waits for the next interval of the row and is retried; the interval is never computed in code | None | AC4 |
| X5 | The last allowed attempt fails | The item moves to EXCEPTION, `FileFailed` is published, one task goes to the row's owner role and the item shows in the exception queue | MSG-P2-001 | AC4 |
| X6 | The acknowledgement says the booking was rejected | The attempt counts as failed, the rejection code is kept in `last_error`, and the retry path and the exception queue apply; the case-side handling is R-RES-23 and rwb-case's | MSG-P2-001 on the last attempt | AC4 (mechanism; the case state is P3's) |
| X7 | The item's decision record cannot be written | The state change and the record roll back together; nothing is sent and no event is written; an incident is raised and the next pass starts a fresh attempt | MSG-P7-003 | AC6 |
| X8 | A platform administrator resends an item in EXCEPTION | The item returns to PENDING with attempt count 0 and the next pass sends it once | MSG-GEN-005 | AC5 |
| X9 | A resend names an item that is not in EXCEPTION, or the item changed since it was read | The request is refused with 409 and nothing changes | MSG-GEN-004 | AC5 (mechanism, owned by RWB-P2-E1007-APP) |
| X10 | A caller's role does not include Platform administration U | Refused before any read or change; nothing changes | MSG-P4-002 | AC7 |
| X11 | rwb-document does not answer inside the REST budget, or the stored file is missing behind the claim-check link | No file is built and no item is written; the workspace is never rebuilt from a partial file and the caller retries | None (the caller's own failure path) | AC2 |
| X12 | The ALS booking interface row changes between two items | The next item obeys the new version: attempts, intervals, transport and owner role are read per item, so a change is data and needs no release | None | AC2 |

X6 is the mechanism behind R-RES-23 only as far as this slice can carry it: the rejection becomes a failed attempt, an exception item and a task. The officer-queue visibility and the case staying with operations are rwb-case's and are asserted by RWB-ITG-E4046-ITG, not here. The interface row's own values are placeholders (GAP-0673; ASM-1214).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the integration base, the decision-record library and the edge route; the rwb-document, rwb-access and rwb-case answers come from their fakes |
| Negotiable | The interface id, transport, layout, attempts, intervals and owner role are rows of `interface_config`; the story fixes only the lifecycle around them |
| Valuable | A settlement that has passed its point of no return is provably on its way to ALS, and a failed sending is visible and re-sendable the same day |
| Estimable | One interface row reader, one deliver entry, one builder, one sender, one retry reader, one exception raiser, one resend path, one record writer, two events |
| Small | Fits one sprint with its tests, on top of the integration base |
| Testable | Each owned criterion is one automated test against the fakes; the access case is a component test and the forced record failure is the NFR half |

### 7. Acceptance criteria

```gherkin
Feature: Post a settlement booking to ALS

  Background:
    Given treatment "T-0001" is accepted at a settlement amount of 820000 for account "A-0001"
    And the ALS booking interface configuration row in force for business date 2027-02-26 is loaded with direction "OUTBOUND", its interface id, transport, layout, max attempts, retry intervals and owner role
    And every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 One item per treatment and Idempotency-Key (new, D-RCV-60)
    Given the rwb-document contract mock returns the stored booking file with document ID "DOC-SYN-0001" and its SAS link
    Given the settlement workflow calls "deliverFile" with treatment "T-0001", account "A-0001", the settlement amount 820000 and idempotency key "ALS-T-0001-1"
    When the settlement workflow calls "deliverFile" again with the same treatment and the same idempotency key
    Then "outbound_item" holds exactly one item for the ALS booking interface and that key
    Then the second call returns that item and creates no second item
    Then no second booking file is built and no second "FileDelivered" or "FileFailed" is written

  Scenario: AC2 The item is built from the interface configuration version in force (new, D-RCV-60)
    Given the ALS booking interface configuration row in force from 2027-02-01 carries its transport, its layout and its file pattern
    When the settlement workflow calls "deliverFile" for "T-0001"
    Then the built booking file uses the transport, the layout and the file pattern of that row
    Then the item carries the max attempts, the retry intervals and the owner role of that row and no value taken from code
    Then a new row version in force for the next item changes those values without a release

  Scenario: AC3 Sent, then acknowledged, with FileDelivered (new, D-RCV-60)
    Given the item for "T-0001" is PENDING and due
    Given the ALS receiver stub accepts the booking file and returns a positive acknowledgement
    When the sender pass runs
    Then the item status is "SENT" on the send and "ACKNOWLEDGED" on the acknowledgement
    Then "rwb.integration.FileDelivered.v1" is written to the outbox in the same transaction as "ACKNOWLEDGED" and published on "rwb.integration.events.v1"
    Then the event names the item id, the interface id, the business date, the document id and the sha256
    Then the event carries no personal data and no file content

  Scenario: AC4 Failed attempts, then the exception queue with a task (new, D-RCV-60)
    Given the item for "T-0001" is PENDING and the ALS receiver stub fails every attempt
    When the sender pass runs at each interval of the row
    Then attempt 2 starts at the second interval of the row after attempt 1 and the next attempt at the third, and no attempt starts outside the values of the row
    Then after the max attempts of the row the item status is "EXCEPTION" with attempt count equal to that maximum
    Then "rwb.integration.FileFailed.v1" is published and the item shows in the exception queue with message MSG-P2-001
    Then one open task is raised for the owner role of the row naming the item, the interface and the treatment
    Then "next_attempt_at" is empty and "last_error" carries the last failure code

  Scenario: AC5 Resend from the exception queue (new, D-RCV-60)
    Given outbound item "OB-SYN-0002" has status "EXCEPTION" after the max attempts of the row
    Given the rwb-access contract mock returns the Platform administration U right for the platform administrator
    Given the ACE audit stub accepts the resend record
    When a platform administrator resends it through "POST /api/recovery/integration/v1/admin/outbound-items/OB-SYN-0002/resend"
    Then the item status is "PENDING" with attempt count 0
    Then the resend is written to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005
    Then no second item and no second booking file are created

  Scenario: AC6 A failed decision record sends nothing (new, D-RCV-60)
    Given the item's state change is about to commit with its decision record
    Given the decision-record library stub fails
    When the sender pass runs for "T-0001"
    Then the state change and its record roll back together and nothing is sent
    Then the system raises an incident and the log carries message MSG-P7-003
    Then no "FileDelivered" and no "FileFailed" is written for that attempt

  Scenario: AC7 An absent interface row and a role without the right (new, D-RCV-60)
    Given no ALS booking interface configuration row is in force at business date 2027-02-26
    When the settlement workflow calls "deliverFile" for "T-0001"
    Then the call is refused with message MSG-GEN-001 and no "outbound_item" is written
    Given the rwb-access contract mock returns that the caller's role lacks Platform administration U
    When the caller requests the resend of "OB-SYN-0002"
    Then the response is 403 with message MSG-P4-002 and nothing changes

  Scenario: AC8 Each business rule of section 8 is proved by a criterion or a boundary test (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8 are the rules this slice must obey
    Then each rule BR1 to BR11 is proved by one criterion of this section or by the boundary test TC-E4-046-08 of section 16
    Then BR9, BR10 and BR11 are proved by the boundary test TC-E4-046-08 and no treatment row and no ACE view is read

  Scenario: AC9 Each provided operation answers 401 with no session (new, D-RCV-60)
    Given the caller holds no session
    When the caller requests "GET /admin/outbound-items" or "POST /api/recovery/integration/v1/admin/outbound-items/OB-SYN-0002/resend"
    Then the response is 401 and nothing changes

  Scenario: AC10 A consumed call that fails or does not answer leaves the item unchanged (new, D-RCV-60)
    Given the rwb-access contract mock does not answer the resend check for the platform administrator
    When a platform administrator resends "OB-SYN-0002" through "POST /api/recovery/integration/v1/admin/outbound-items/OB-SYN-0002/resend"
    Then the response status is Not specified in the source documents (NEWAC-RWB-P2-E4046-APP-AC10) and the item status stays "EXCEPTION" with no resend record written
```

The legacy story owns no acceptance criterion in this slice: AC1 of RWB-E4-046 is the criterion of RWB-ITG-E4046-ITG, which exercises the whole chain including this service's item, and AC2 "Not recorded" is owned by RWB-P8-E4046-APP. The ten criteria above are new and test only the deliverable of this slice — the outbound item, its interface row, its lifecycle, its resend, its record and its two events — so that the criteria the other two stories own stay theirs and nothing is proved twice in two places. Every cross-service value is a contract-mock Given, and every interface value the Background names is a row of the `interface_config` version in force: its interface id, transport, layout, max attempts, retry intervals and owner role are Not specified in the source documents (GAP-0673; ASM-1214), so they are cited as the placeholder rather than invented.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The Workbench writes nothing to ALS directly: the agreed terms leave through the outbound interface and the item is tracked in `outbound_item` | REQ-DRI-006; legacy RWB-E4-046 AC1 | AC1, AC3; TC-E4-046-01 |
| BR2 | Every outbound is logged, retried on a defined schedule and placed in an exception queue with a task for a named owner after the retry limit | REQ-DRI-007 | AC4; TC-E4-046-01 |
| BR3 | The retry intervals and the maximum number of attempts are read from the `interface_config` version in force for the item's business date; no interval, count or delay is written in code | TSD P2 v3 T4; FSD P2 v3 BR-P2-001; DP-01 | AC2, AC4; TC-E4-046-01 |
| BR4 | One outbound item is created per interface and Idempotency-Key; a repeat of the same command returns the existing item and creates no second one | Arch v5 slide 11 (Idempotency-Key on every POST) | AC1; TC-E4-046-01 |
| BR5 | An item that has used its retries moves to the exception queue with one task for the owner role of the row and publishes `FileFailed` | R-UNI-34; TSD P2 v3 T4; FSD P2 v3 AC-EXC-P2-001-01 | AC4; TC-E4-046-01 |
| BR6 | A resend of an item in the exception queue sets PENDING with attempt count 0, is written to the ACE audit log with the user and the time, and creates no second item | FSD P2 v3 AC-EXC-P2-001-04; TSD P2 v3 T4; API-P2-002 | AC5; TC-E4-046-05 |
| BR7 | A state change that cannot be written to the decision record does not proceed: nothing is sent and an incident is raised | R-UNI-39; CTL-06; DP-03 | AC6; TC-E4-046-02, TC-E4-046-04 |
| BR8 | Once the terms are booked in ALS the payment due date is set, and the booking reference is recorded when ALS and NLEADS acknowledge, while a rejection keeps the case with operations and puts the error on the officer queue | R-SET-13; R-RES-22; R-RES-23 | AC8; TC-E4-046-08 |
| BR9 | The accepted settlement terms are the caller's: they arrive in the request and are never read from another schema, and this service holds no treatment row | Arch v5 slide 41 (rwb-treatment owns treatments); DP-01 | AC8; TC-E4-046-08 |
| BR10 | This service reads no ACE data: the booked position and the settlement payment are read by rwb-source-data through its data product, and `rwb_integration` holds no grant on `recovery` | ADR-010; DP-05; REQ-CHO-008; REQ-S2-008 | AC8; TC-E4-046-08 |
| BR11 | The exception queue is read through the gateway-bff composite route and never called directly by the browser | DP-19 | AC8; TC-E4-046-08 |

BR1, BR2, BR5, BR6 and BR8 are the legacy and outbound rules with their sources. BR3, BR4, BR7, BR9, BR10 and BR11 are the realignment rules this slice must obey; each is forced by the ownership of a fact the legacy story held in one database.

### 9. State transitions

`outbound_item.status` (LOV-OUTBOUND-STATUS), which is the whole state this slice owns:

| From | Event | Condition | To |
|---|---|---|---|
| none | `deliverFile(manifest)` accepted | The interface row is in force at the business date and the key is new | PENDING |
| none | `deliverFile(manifest)` with a known key | An item exists for the interface and the key | PENDING, unchanged, the existing item is returned |
| PENDING | The transport fails before the send | No attempt was made | PENDING, with `last_error` |
| SENT | The send fails | The attempt counts | RETRY |
| RETRY | The next attempt is due | The interval of the row has elapsed | SENT |
| RETRY | The last allowed attempt fails | `attempt_count` equals `max_attempts` | EXCEPTION |
| SENT | A positive acknowledgement arrives | The result is positive for the row's result codes | ACKNOWLEDGED |
| SENT or RETRY | A rejection arrives | The result is negative | RETRY, then EXCEPTION on the last attempt (R-RES-23 mechanism) |
| EXCEPTION | Platform administrator resends | The right check passes and the item is still in EXCEPTION | PENDING, attempt count 0 |

The case states behind the booking are the owners' and are listed here only to show what this slice feeds: `WITH_OPS_SETTLEMENT` to `AWAITING_PAYMENT` on SETTLEMENT_BOOKED (R-SET-13), `WITH_OPS_BOOKING` to `BOOKED_IN_ALS_NLEADS` on BOOKING_CONFIRMED when ALS and NLEADS acknowledge (R-RES-22), and `WITH_OPS_BOOKING` kept with the error on the officer queue on BOOKING_REJECTED (R-RES-23). rwb-case and rwb-treatment move them; this story announces the facts and changes none of them. A held or a repeated delivery is not a state: a repeat is a no-op on the same item (AC1).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-integration service identity (its own login, DP-02) | Reads its own `interface_config` row and writes its own `outbound_item`, decision record, outbox rows and idempotency record; builds, sends, retries and resends the booking file (Outbound file, C) |
| The settlement workflow's service identity, S2 rwb-treatment or P8 rwb-payment | Calls `deliverFile(manifest)` for an accepted treatment; holds no right on the item and cannot resend it |
| RW-PLATADM, platform administrator | Lists the exception queue and resends an item (Platform administration, U), as the FSD P2 v3 T6.1 matrix and the legacy key state |
| The owner role written on the interface row | Receives the one task raised when an item enters the exception queue; the role name is a column of the row (an owner role of LOV-ROLE) and its value for the ALS booking row is Not specified in the source documents (GAP-0673; ASM-1214) |
| RW-CASEOWN, case owner | Reads the outbound item as the evidence of the booking, through the composite route (Case record, R) |
| rwb-access service identity | Answers the Platform administration U check on the resend |
| rwb-document service identity | Holds the booking file and answers the fetch by document id with a SAS link |
| The platform flag library | Owns the flag value of the outbound path per environment |

The service runs as the rwb-integration login (DP-02), carried as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-0673; ASM-1212). The ALS credentials of the endpoint are the environment's and never appear in code, a value file or a log.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-OPS-136 to DF-OPS-148 | `interface_config` (P2, `rwb_integration`) | id, interface_id, direction, transport, inbound_path, file_pattern, data_product, max_attempts, retry_intervals_min, owner_role, alert_role, valid_from, valid_to | Read; the ALS row is loaded through the reference-data load, not written by this story |
| DF-OPS-168 to DF-OPS-177 | `outbound_item` (P2, `rwb_integration`) | id, interface_id, idempotency_key, payload_ref, case_ids, attempt_count, next_attempt_at, status, last_error, owner_role | Write |
| DF-DOC-006 | `document` (P5, read through the rwb-document contract) | storage_ref and the SAS link of the stored booking file | Read through the rwb-document contract; never copied |
| DF-TRT-001 to DF-TRT-014 | `treatment` (S2, never read by this service) | id, case_id, and the accepted settlement terms | Received in the `deliverFile` manifest from the caller; no row is read or held |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (library table in `rwb_integration`) | The item's own record: interface id, item id, business date, attempt count, outcome and the reference of the state change | Write (DP-03) |
| DF-OPS-184 to DF-OPS-188 | `idempotency_key` (PLT library, created in `rwb_integration`) | id, idempotency_key, endpoint, request_hash, response | Write for the resend POST |
| DF-OPS-189 to DF-OPS-197 | `outbox_event` (PLT library, created in `rwb_integration`) | event_type, schema_version, case_id, idempotency_key, payload, occurred_at | Write, in the same transaction as the state change |
| DF-OPS-198 to DF-OPS-206 | `outbox_delivery` (PLT library, created in `rwb_integration`) | consumer, status, attempt_count, next_attempt_at, last_error_code, delivered_at | Written by the relay of DP-09 |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and the TSD P2 Integration v3 T3.1. The ten `outbound_item` fields and the thirteen `interface_config` fields are used as published and no column is added; which field ID carries each element of the ALS message or file is the layout's job and is Not specified in the source documents (GAP-0673; ASM-1216). `rwb_integration` holds no treatment row, no case row, no document row and no ACE row: the service links by business key (`case_id`, `account_key`, the treatment id and the document id) and holds no foreign key into another schema (DP-01). The only rows this story writes are the `outbound_item` row, its decision record, the resend's stored key and the outbox rows behind the two events. `payload_ref` holds the document id and the sha256 behind a SAS link, never file content. `decision_record` is a PLT library object created in `rwb_integration`, not an LDM v9 entity (section 12.7); `interface_run` and `interface_signoff` are not fields or entities of LDM v9 or Data Classification v5, and this story reads and writes neither.

### 12. Contract

The contract versions this story builds against are the `/v1` paths of sections 12.1 and 12.2; the contract version is 5.0.0 of API Specification v5 for rwb-integration and for the consumed rwb-case, rwb-access and rwb-document contracts.

#### 12.1 REST operations provided

None added. The two operations the slice uses already exist on the integration base `/api/recovery/integration/v1` and are declared by RWB-P2-E1007-APP and its CON story; this story adds the ALS interface row and the behaviour behind them and no path:

| Method | Path | Owner of the declaration | Use for the ALS booking |
|---|---|---|---|
| GET | `/admin/outbound-items` | RWB-P2-E1007-APP (API-P2-001) | Lists the ALS booking items by status and interface for the exception queue, and the item the settlement workflow sent |
| POST | `/admin/outbound-items/{itemId}/resend` | RWB-P2-E1007-APP (API-P2-002) | Takes an Idempotency-Key header; a repeat with the same key does not reset the item again. Returns an ALS item in EXCEPTION to PENDING with attempt count 0; 409 when the item is not in EXCEPTION or its version changed |

Errors on both: 401 no session; 403 no Platform administration right (MSG-P4-002); 404 unknown item; 409 not in EXCEPTION or a changed version; 503 the store or a consumed contract is unavailable. The `deliverFile(manifest)` activity is not a REST path: it is the activity contract of RWB-P2-E1007-CON, and this story adds the ALS branch of it (ASM-1213).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020).

| Method | Path | Service | Used for |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{id}` | rwb-document (P5) | The stored booking file behind the claim-check reference and its SAS link, kept on `payload_ref`; the file content never travels on a message (AC2) |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | rwb-case (P3) | The one open task for the row's owner role when the item enters the exception queue (AC4, R-UNI-34; ASM-1217) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Platform administration U check on the resend, cached per session (AC5, AC7) |
| POST | INT-22 audit and PII logging (ACE Common path) | ACE Common | The resend record with the user and the time (AC5) |

Two reads are deliberately absent. **The accepted settlement terms are not read here**: the caller passes them in the `deliverFile` manifest, so this story makes no call to rwb-treatment (BR9). **No ACE data is read here**: the booked position and the payment are rwb-source-data's read-back after the next ACE batch, and this service holds no grant on `recovery` (BR10, DP-05). The task code the owner task carries is Not specified in the source documents (GAP-0673; ASM-1217) and is agreed with the rwb-case owner before the contract test.

#### 12.3 Events published

| Event | Topic | Key | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | caseId | itemId, interfaceId, businessDate, documentId, sha256, recordCount, the treatment id, the requesting service |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | caseId | itemId, interfaceId, businessDate, attemptCount, the last failure code, caseIds, the treatment id, ownerRole |

Both are written to `outbox_event` in the same transaction as the item state change and relayed by the outbox relay with the CloudEvents 1.0 envelope in binary mode; neither carries personal data, an address, an amount or file content (Arch v5 slide 11; DP-09). The decision-record library publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for each record this story writes, with the interface id, the item id, the business date, the attempt count and the outcome (DP-03; ASM-1215). The consumer of the two outbound events is the requesting service, as the event catalogue of Arch v5 slide 43 records.

#### 12.4 Events consumed

None. rwb-integration consumes no event for the ALS booking: the settlement workflow calls the `deliverFile(manifest)` activity on queue `rwb-integration` as a task, and Arch v5 slide 16 records exactly that ("IN: events (none: called as a task)"). Nothing is subscribed to, so this slice adds no inbox consumer and no `processed_event` row; the duplicate protection of the command is the Idempotency-Key of the item (BR4, ASM-1220).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Stage child workflow of S2 rwb-treatment (Temporal Workflow and Activity Catalog v1, Workflows), not owned by this story | `rwb-treatment` or `rwb-payment` | Its settlement step, or the booking step of rwb-payment where the posting runs there, calls `deliverFile(manifest)` after the treatment is accepted; the treatment `T-0001` at 820000 for account `A-0001` is its input |
| `deliverFile(manifest)` | Activity, provided by P2 and already declared by RWB-P2-E1007-CON; this story adds its ALS branch | `rwb-integration` | Input: the interface reference, business date, treatment id, case ids, account key, settlement amount, claim-check reference, Idempotency-Key. Output: the item reference and its status |
| `buildOutboundFile` | Activity, reused from RWB-P2-E1007-APP | `rwb-integration` | Input: the manifest and the interface row. Output: the booking file in the row's layout with its control totals |
| `storeOutboundFile` | Activity, reused from RWB-P2-E1007-APP | `rwb-integration` | Stores the built file with rwb-document and keeps the document id and the sha256 on `payload_ref` |
| `sendFileOverMft` | Activity, reused, the only class that opens the transport of the row | `rwb-integration` | Sends the booking file, sets SENT, records the attempt and its result; idempotent on the document id |
| `parkItemInException` | Activity, reused | `rwb-integration` | Sets EXCEPTION, writes `FileFailed` to the outbox, raises the owner task through the rwb-case contract |
| `recordItemDecision` | Activity, added by this story | `rwb-integration` | Writes the item's decision record in the same local transaction as the state change (DP-03) |
| `resendItem` | Activity, added by this story | `rwb-integration` | Sets PENDING with attempt count 0 for an item in EXCEPTION and hands it to the next sender pass |

The retry policy inside the flow is the row's, not the kit's constant: the interval between attempts is `retry_intervals_min` of the interface version in force and the count is `max_attempts` of the same row (BR3). The kit's policy governs only the technical retry of a consumed contract, where a 4xx is non-retryable. The workflow input and its history carry business dates, business keys, ids, amounts as the caller sent them and codes only — no personal data and no file content.

#### 12.6 Schedules

None. The ALS booking has no Schedule and no cron: it is triggered by the accepted treatment through the caller's workflow and reaches this service as an activity call. The only time behaviour this story owns is the pair of durable Temporal timers of the retry path, one per interval of the interface row, and the acknowledgement wait; the intervals themselves are data of the row and are Not specified in the source documents (GAP-0673; ASM-1214). No ALS file window is named by any source: the Arch v5 job map names the WIN file at 16:00 and the buyer files per lot only (slide 44), so no window is set here.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `interface_config` | `rwb_integration` | P2 | The ALS booking interface row and its version: transport, pattern or layout, attempts, intervals, owner and alert role, validity |
| `outbound_item` | `rwb_integration` | P2 | One booking item waiting, sent, retried, acknowledged or in the exception queue |
| `decision_record` | `rwb_integration` | PLT library object, created in `rwb_integration`; not an LDM v9 entity | The item's own record, written with the state change (DP-03) |
| `idempotency_key` | `rwb_integration` | PLT library, created in `rwb_integration` | The stored response of the resend POST |
| `outbox_event`, `outbox_delivery` | `rwb_integration` | PLT library, created in `rwb_integration` | The two events and their deliveries (DP-09) |

No table is added and no column is added (ASM-1216). The treatment, the case, the task, the document, the decision log and the ACE views are other owners' and are reached only through their contracts or the request (DP-01). `job_catalog` holds no row for this journey because the booking is not a scheduled job, and no run or signoff table exists in the target.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 contract | The stored booking file with document ID "DOC-SYN-0001" and a SAS link; one 404 and one answer beyond 2 s (X11) |
| rwb-case WireMock | The P3 contract | One open task accepted for the row's owner role with the item and the treatment named; one refusal of the task call |
| rwb-access WireMock | The P4 contract | Platform administration U granted to RW-PLATADM and refused to a role that lacks it (AC7) |
| ACE Common audit stub | INT-22 | Accepts the resend record with the user and the time (AC5) |
| Decision-record library stub | RWB-PLT-E1027-CON | A committed record with its outbox row, and the unavailable store that must leave the state unchanged (AC6) |
| ALS receiver stub | The transport of the interface row | A receiver that accepts the file and returns a positive acknowledgement (AC3), one that fails every attempt (AC4), and one that returns a rejection (X6) |
| Settlement caller stub | The caller side of `deliverFile` | The manifest of treatment "T-0001", account "A-0001", settlement amount 820000, twice with the same key (AC1) and once with no interface row in force (AC7) |
| Platform flag library stub | The flag of the outbound path | The flag on for DEV, SIT and UAT |

Each fake is generated from the published OpenAPI document of its service and its version is pinned with the CON baseline. The ALS endpoint, its credentials, its layout and its result codes are fixtures of the interface row and are Not specified in the source documents (GAP-0673; ASM-1214, ASM-1218).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided by this story's own work, 2 already on the base, 3 consumed plus 1 audit path | The outbound-item list and resend of RWB-P2-E1007-APP; the document fetch on P5, the owner task on P3, the authorise check on P4 and the ACE Common audit path; one hop, 2 s timeout, breaker per downstream |
| Kafka | 2 published plus 1 by the library, 0 consumed | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` with the outbox and relay; `DecisionRecorded` by the library on `rwb.decision-record.v1`; nothing consumed, because the service is called as a task |
| Temporal | 1 activity branch provided, 2 activities added, 4 reused | `deliverFile(manifest)` for the ALS row, with `recordItemDecision` and `resendItem` added, on queue `rwb-integration` in namespace `rwb-recovery`; `buildOutboundFile`, `storeOutboundFile`, `sendFileOverMft` and `parkItemInException` reused |
| File | 1 | The ALS settlement booking file, sent over the transport of the interface row; its transport, layout and naming are Not specified in the source documents (GAP-0673; ASM-1214) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `settlement`, Java package `th.co.scb.ace.workbench.recovery.integration.settlement`. The module sits inside the service of RWB-P2-E1007-APP and owns the ALS booking slice of the outbound path only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; for this journey it means no ACE read at all and no grant on `recovery` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-09 | H RWB-PLT-N001-CON |

The two platform contracts sit in the H row of the table and are not repeated in the metadata row, which stays None for this story: the platform wave delivers them and neither blocks Day 1 (ASM-1219). DP-16 is not re-applied, because the activity contract, the events and the two admin operations are the base's and this slice consumes them.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DeliverFileEntry | Service | Validates the manifest of the ALS booking, resolves the interface reference and refuses a manifest that misses a required value with MSG-GEN-001 |
| InterfaceConfigReader | Service | Reads the row in force at the business date and hands the transport, layout, attempts, intervals, owner and alert role to the flow; refuses an absent or not-yet-valid row (AC2, AC7) |
| ItemIdempotencyGuard | Service | Finds the item by interface id and Idempotency-Key, returns it on a repeat and inserts the new item once (AC1) |
| AlsBookingBuilder | Service | Builds the file in the row's layout from the manifest and the stored terms document, and computes the control totals of the row |
| AlsBookingSender | Service | The only class that opens the transport; sends, records the attempt and its result, and maps the acknowledgement |
| AcknowledgementMapper | Service | Maps the result codes of the row to ACKNOWLEDGED or to a failed attempt; the code list is the row's data (ASM-1218) |
| RetryScheduleReader | Service | Takes the next interval and the maximum attempts from the row's version; nothing is compiled in (BR3) |
| ExceptionRaiser | Service | Sets EXCEPTION, writes `FileFailed` in the same transaction and raises one task for the row's owner role through the rwb-case contract |
| ResendService | Service | The Platform administration U check, the return to PENDING with attempt count 0, the audit record and MSG-GEN-005 |
| ItemDecisionWriter | Library client | Writes the item's decision record in the same local transaction as the state change; a failure fails the change (AC6) |
| DocumentClient, CaseTaskClient, AccessCheckClient, AuditWriter | Client | The document fetch, the owner task, the right check and the audit record, each one hop and 2 s |

**Database and migrations.** No new table and no new column: the slice uses `interface_config`, `outbound_item` and the library objects the base creates (ASM-1216). One unique index on `outbound_item (interface_id, idempotency_key)` is the only schema statement this story needs; where the base's migration does not already carry it, it is added by one migration of the rwb-integration sequence (ASM-1220). No foreign key leaves `rwb_integration` and the schema holds no grant on `recovery` or on another `rwb_*` schema.

**Configuration and reference data.**

- The ALS booking interface row: its interface id, direction OUTBOUND, transport, file pattern or layout, `max_attempts`, `retry_intervals_min`, `owner_role`, `alert_role`, `valid_from` and `valid_to`. Every value is Not specified in the source documents (GAP-0673; ASM-1214) and is loaded per environment by the reference-data administrator.
- The result codes of the acknowledgement are a list of the row's version, not an enum in code (ASM-1218).
- The flag of the outbound path is a flag of the platform library per environment; no environment value is hard-coded and no secret appears in a value file or a log.
- The ALS endpoint and its credentials are the environment's secret references, never literals.

**Build steps**

1. `InterfaceConfigReader` with the row in force, a row from another date, an absent row and a row not OUTBOUND (AC2, AC7).
2. `DeliverFileEntry` and `ItemIdempotencyGuard` with the same key twice, a new key for the same treatment and a manifest that misses a value (AC1).
3. `AlsBookingBuilder` with the fixture file of the row and its control totals, and with a document fetch that fails (X11).
4. `AlsBookingSender` and `AcknowledgementMapper` against the accepting stub and the rejecting stub (AC3, X6).
5. `RetryScheduleReader` with two row versions, so that a change of intervals and attempts changes the run without a release (AC2, AC4).
6. `ExceptionRaiser` with the failing stub, the one task for the owner role and `FileFailed` in the same transaction (AC4).
7. `ResendService` with the right granted and refused, the audit record and MSG-GEN-005 (AC5, AC7).
8. `ItemDecisionWriter` with the committed record and the unavailable store, asserting that nothing is sent (AC6).
9. The two events end to end through the outbox and the relay, with the CloudEvents envelope and the absence of personal data and file content (AC3, AC4).
10. The metrics the operations story of this legacy key deploys: items per status, attempts per item, items in the exception queue per day and resends per day.

**Done when.** The tests of section 16 pass, AC1 to AC10 are green against the fakes, one item exists per treatment and Idempotency-Key, the row's version governs every attempt, the exception queue carries the item with its task and MSG-P2-001, the resend returns the item to PENDING with attempt count 0, a failed record leaves nothing sent, `rwb_integration` holds no foreign key into another schema and no grant on `recovery`, and the contract tests of RWB-P2-E1007-CON and RWB-PLT-E1027-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the manifest or of the interface row is missing | Enter {field}. |
| MSG-GEN-004 | A resend names an item that is not in EXCEPTION, or the item changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P2-001 | An outbound item moves to the exception queue | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-GEN-005 | A resend from the exception queue is accepted | Saved. |
| MSG-P4-002 | A role without the Platform administration right requests the resend | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The item's decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the legacy texts of RWB-E4-046 unchanged. MSG-P2-001 takes its English text from the Error and Message Standard v4 (row MSG-P2-001). MSG-GEN-005 is named by the FSD P2 Integration v3 (AC-EXC-P2-001-04) without its text and keeps the text of RWB-E1-007, the story of the same outbound path; no text is invented here. The interface name and the item name inside MSG-P2-001 are the row's data. An alert, a log line and a record carry item ids, interface ids, business dates, attempt counts and codes only — never an account holder, an address, an amount that was not the caller's own, or file content.

### 15. Screens and states

No new screen. The slice renders nothing and registers no route; the two screens below are read through the gateway-bff composite route and their state belongs to their owners (DP-19):

| Screen | State | What the platform administrator or the case owner sees |
|---|---|---|
| SCR-09 Exception queue | Loading, list; empty: the empty list when no item is in EXCEPTION; no access: MSG-P4-002 and nothing changes; error: Not specified in the source documents (CG-ALL-3340) | The ALS booking item with its interface name, attempt count, last error and case count, and the resend action; the one task for the row's owner role. The data is this service's through `GET /admin/outbound-items`; the route and the masking are the edge's |
| SCR-28 Proceeds matching | Loading, matched, unmatched; empty, error and no access: Not specified in the source documents (CG-ALL-3341) | The booking and the read-back of the booked position and the payment, which rwb-payment and rwb-source-data own; this slice supplies only the fact that the terms left for ALS |

The legacy story names SCR-28 Proceeds matching for the behaviour of the key; this slice produces the outbound item behind it and no state of that screen. The route paths, the merge order and the field-level masking are Not specified in the source documents (GAP-0673; ASM-1213) and belong to RWB-PLT-N001-CON and RWB-P2-E1007-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-046-01 | AC1, AC2, AC3, AC4 of this story; the outbound-item half of legacy AC1 | End to end | Settlement `T-0001` at 820000 for account `A-0001`; the ALS booking item on the interface row in force; the accepting and the failing ALS receiver |
| TC-E4-046-02 | AC6 of this story; the "nothing is sent" half of legacy AC2, whose criterion is owned by RWB-P8-E4046-APP | End to end | Decision-record library store stopped; MSG-P7-003; no item state change and no event |
| TC-E4-046-03 | AC7 of this story; the access path | Component | A role without Platform administration U; MSG-P4-002; and no interface row in force; MSG-GEN-001 |
| TC-E4-046-04 | AC6 at the blocking half; Principle 5 | NFR | A forced decision-record write failure during a run of many items; nothing is sent for any item that has no record |
| TC-E4-046-05 | AC5 of this story; the resend path | Component | Settlement `T-0001` at 820000 for account `A-0001`; an item in EXCEPTION; the resend by a platform administrator |
| TC-E4-046-06 | Every operation, event and activity of section 12 of this story | Contract | The contract fakes of the section 12.2 operations and the section 12.5 activities |
| TC-E4-046-07 | The tables of section 12.7 at their boundary values | Component | Boundary values of each table in section 12.7; the values are Not specified in the source documents (GAP-0673) |
| TC-E4-046-08 | AC8 of this story; each business rule BR1 to BR11 of section 8 that has no criterion, with the boundary of BR9, BR10 and BR11 | Component | Not specified in the source documents (NEWAC-RWB-P2-E4046-APP-AC8) |
| TC-E4-046-09 | AC9 of this story; the 401 answer of each provided operation of section 12.1 | Component | Not specified in the source documents (NEWAC-RWB-P2-E4046-APP-AC9) |
| TC-E4-046-10 | AC10 of this story; a consumed call that fails or does not answer | Component | Not specified in the source documents (NEWAC-RWB-P2-E4046-APP-AC10) |

The four IDs are the legacy test cases of the key, kept in order with the Level column added, and the full legacy tests with their Given, When and Then are in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under those IDs. This story runs **TC-E4-046-03 at Component level** and the **outbound-item half of TC-E4-046-01 and TC-E4-046-02 at Component level** against its own flow with the contract fakes, because the item, its row, its lifecycle, its resend and its record are this slice's behaviour and are provable with the P5, P3, P4 and library answers stubbed. **TC-E4-046-01 and TC-E4-046-02 at End to end level are cited for the legacy key**: the whole-chain criterion of AC1 is RWB-ITG-E4046-ITG's and the criterion of AC2 is RWB-P8-E4046-APP's. **TC-E4-046-04 is cited at NFR level**: the blocking half is proved here in AC6 and the volume proof is the NFR story's. The `-ITG` copies of all four belong to RWB-ITG-E4046-ITG and are not restated here.

### 17. Guardrails

- No business value in code: the ALS interface id, the transport, the message or file layout, the control totals, the retry intervals and the maximum attempts are `interface_config` rows of the version in force, and the acknowledgement result codes are a list of that row. A change of any of them is data and needs no release.
- No personal data in events, logs, workflow inputs or payloads: the events name case ids, the item id, the interface id, the business date, the attempt count and the document id only; the file carries personal data only as the receiving interface allows, and the content stays in rwb-document behind a SAS link.
- Data Classification and Personal Data Inventory v5 handling for two fields this slice carries: the account key (`account_key`, Indirect identifier) travels in events, workflow inputs and payloads, including `deliverFile(manifest)`, as a reference only (the case id, or the row id of the owning service), the clear key is read by REST under the masking policy and a log holds the id of the read only; `owner_role` (Customer data) travels as a role code only, never beside a direct identifier, and a log holds a code or an id only.
- The Workbench writes nothing to ALS directly: the terms leave as one outbound item through the transport component, and no other class opens a session to the target.
- No read of another service's table: the terms arrive in the request, the file comes through the rwb-document contract, the task goes through the rwb-case contract and the right through the rwb-access contract (DP-01, DP-11).
- `rwb_integration` holds no foreign key into another schema and no grant on `recovery`; this service reads no ACE view and calls no rwb-source-data operation for this journey (ADR-010, DP-05).
- A failed local decision record sends nothing: the state change and the record commit together or not at all, and the attempt leaves MSG-P7-003 and an incident (BR7, AC6).
- One item per interface and Idempotency-Key: the key is the caller's command key, this service never rewrites it, and a repeat is a no-op.
- Every example and fixture is synthetic: no production treatment, case, party, account or payment is used, and the ALS endpoint of every test is a stub.
- No secret appears in code, a value file, a log or a prompt: the login, the transport credentials and the endpoint are secret references of the environment (NFR-052).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly; data leaves through the paths the bank already has and the Workbench outbound adapters | Business Requirements Program v5, section 5.2 | FEAT-PAY-06 | D6.4 settlement | R-SET-10 | TC-E4-046-01 |
| REQ-DRI-007 | The integration adapters log every outbound, retry on a defined schedule and place anything that fails after the retry limit in an exception queue with a task for a named owner | Business Requirements Program v5, section 5.2 | FEAT-PAY-06 | D6.4 settlement | R-SET-10, R-RES-22, R-RES-23 | TC-E4-046-01, TC-E4-046-02, TC-E4-046-04 |
| REQ-CHO-008 | Terms booked in the core system are confirmed from the next business date's ACE account data, and the Workbench holds no account or payment copy | Business Requirements Program v5, section 5.3 | FEAT-PAY-06; FEAT-CHO-08 | D6.4 settlement | R-SET-13 | TC-E4-046-01 |
| REQ-S2-008 | Booked terms and settled accounts are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-PAY-06 | D6.4 settlement | R-SET-10, R-SET-13, R-RES-22 | TC-E4-046-01 |
| R-SET-13 | Settlement: WITH_OPS_SETTLEMENT to AWAITING_PAYMENT when the agreement is signed and the terms are booked in ALS; set the payment due date | Business Rules and Routing Logic v4 | FEAT-PAY-06 | D6.4 settlement | R-SET-13 | TC-E4-046-01 |
| R-RES-22 | Restructure: WITH_OPS_BOOKING to BOOKED_IN_ALS_NLEADS when ALS and NLEADS both acknowledge; record the booking reference | Business Rules and Routing Logic v4 | FEAT-PAY-06 | D6.4 settlement | R-RES-22 | TC-E4-046-01 |
| R-RES-23 | Restructure: BOOKING_REJECTED when ALS rejects the booking; put the error on the officer queue and keep the case with operations | Business Rules and Routing Logic v4 | FEAT-PAY-06 | D6.4 settlement | R-RES-23 | TC-E4-046-01 |
| ADR-010 | Read source data from the ACE database through read-only views, by rwb-source-data alone; this slice reads no ACE data at all | Architecture Decision Records v4 | FEAT-PAY-06 | D6.4 settlement | R-SET-13 | TC-E4-046-01 |

The four requirement rows are named by RWB-ITG-E4046-ITG section 18, which is the story that carries them under this legacy key; the three rule rows and the ADR row are added because this slice is the one that has to obey them. The legacy story RWB-E4-046 carries no requirement ID of its own, so none is invented for it.

### 19. Out of scope

- The accepted settlement terms, the treatment state and the booking reference on the treatment: S2 rwb-treatment and RWB-P8-E4046-APP.
- The booking and the posting themselves, the posting file and the legacy AC2 "Not recorded": RWB-P8-E4046-APP.
- The read-back of the booked position from `v_ace_account` and the settlement payment from `v_ace_payment`: P1 rwb-source-data, and RWB-ITG-E4046-ITG asserts it.
- The case state after the booking, the officer queue of R-RES-23 and the route-state moves of RETRY_QUEUE and EXCEPTION_QUEUE: P3 rwb-case.
- The central decision ledger, its hash chain and the seal of the record: P7 rwb-decision.
- The ALS system itself: its interface id, transport, message or file layout, result codes, test endpoint and credentials, none of which a source gives.
- The activity contract, the two outbound events and the admin operations as declarations: RWB-P2-E1007-CON and RWB-P2-E1007-APP, which this story consumes and does not re-declare.
- The chart, the transport endpoint, the PGP keys, the topic subscription, the alerts, the dashboards and the runbook: RWB-P2-E1007-INF and RWB-P2-E1007-OPS.
- The cross-service proof of the whole settlement booking and the boundary check over the nineteen schemas: RWB-ITG-E4046-ITG, with the `-ITG` copies of the four test cases.
- Any direct read of an ACE view, any read of the treatment, case, task or document table, and any second item for one treatment and one Idempotency-Key.
