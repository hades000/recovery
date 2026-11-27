# RWB-P4-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P4-L |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DRI-006, REQ-DRI-007, REQ-DRI-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-access, as the secondary slice of the legacy key. The legacy story held the adapter, the SFTP transport, the retry ladder, the exception queue and the scheduled jobs of one module in one process under one `recovery_svc` identity. This slice takes the one part of that key that belongs to the access service — the six-monthly access-review file of JOB-18 — and makes it a **requester** of the rwb-integration outbound-file capability instead of a transport of its own: two activities on queue `rwb-access`, one manifest, one store call to rwb-document, one `deliverFile(manifest)` call on queue `rwb-integration`, the two delivery outcomes consumed with inbox dedupe, and one decision-record entry per request and per outcome. No SFTP class, no second file copy, no ACE view, no data lake, no table and no Schedule of its own. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM) and a compliance and PDPA officer (RW-COMPLY)**, I want **the six-monthly access-review file of rwb-access built from the service's own `role`, `permission`, `masking_rule` and `delegation_limit` rows and the access records it already holds, stored once in rwb-document behind a claim-check manifest of file name, sha256, record count and business date, handed to rwb-integration through the `deliverFile(manifest)` activity on task queue `rwb-integration`, with the `FileDelivered` and `FileFailed` outcomes consumed once each and one decision-record entry written for the request and for the outcome**, so that **the review pack leaves the Workbench through the one governed outbound path of the platform, the access service never becomes a second transport adapter, and every request for the pack and every delivery outcome is on the append-only record**.

Inside `rwb-access` this is the requester side of the legacy story RWB-E1-007:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the activity pair `buildAccessReviewFile` and `requestFileDelivery` on queue `rwb-access`; and the two consumption handlers of `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1` with inbox dedupe, the item-status read through the rwb-integration admin operation, and one local decision-record entry per request and per outcome through the DP-03 library.
- The JOB-18 `Schedule` and the workflow that calls the two activities are **not** this story's: they belong to RWB-P4-AD008-APP (Architecture v5 slide 44). This story registers no workflow and no Schedule, and it runs correctly when that workflow calls it.
- The transport, the MFT/SFTP session, the PGP key, the retry ladder on `retry_intervals_min`, the exception queue, the resend and the owner task are **not** this story's either: they are the rwb-integration capability of RWB-P2-E1007-APP, RWB-P2-E1007-INF and RWB-P2-E1007-OPS, the exception-queue surface of RWB-P2-E1007-CON, and the end-to-end proof of RWB-ITG-E1007-ITG. This story makes the request, stores the bytes once and reads the outcome.
- `outbound_item`, `interface_config` and `outbox_delivery` are P2's tables and are read only through the rwb-integration admin operation, never from `rwb_integration`; `rwb_access` holds no grant outside its own schema (DP-01, DP-02).

Two source silences are load-bearing and are carried as one combined gap row and three assumptions rather than as invented values. The interface ID, the file name pattern, the extract layout and the recipient of the access-review file are named nowhere: Architecture v5 slide 44 gives the job only as "JOB-18 | Access review list | six-monthly | rwb-access | Schedule", and neither the FSD P4 nor the TSD P4 nor the legacy story contains the extract, so every such value reads "Not specified in the source documents (GAP-0981; ASM-1717)". The two activity names, their inputs and the manifest element list are fixed by this story because no source names them: "Not specified in the source documents (GAP-0981; ASM-1716)". And the delivery events are keyed by case ID, while an access-review file has no case: "Not specified in the source documents (GAP-0981; ASM-1718)".

### 2. Business rationale

Architecture v5 gives rwb-access a six-monthly access-review list as its only `Schedule` (slide 44, JOB-18) and gives rwb-integration the single outbound-file path of the platform: `deliverFile(manifest)` and `receiveFile` on queue `rwb-integration`, the two events `FileDelivered` and `FileFailed` on `rwb.integration.events.v1`, and the admin outbound-item surface (slide 16). DP-16 makes the rwb-integration contract the only way any service puts a file into the outside world, and DP-17 removes the data lake, so a service that keeps its own SFTP class and its own lake copy would be a defect rather than a shortcut.

Read together, those rulings fix where the access-review pack is built and how it leaves. The **content** is rwb-access's own: Recovery roles as data, the permission matrix, the masking policy and the delegation table are its four tables (Architecture v5 slide 41), and the access records are its local decision-record entries (DP-03). The **movement** is rwb-integration's: the manifest, the claim-check link to the stored bytes, the MFT/SFTP transport, the retry ladder, the exception queue and the owner task. This story is the seam between them, and it is deliberately small: build, store, request, consume, record. It meets REQ-DRI-006 (no component calls a system of record directly), REQ-DRI-007 (every outbound file is logged, retried on a defined schedule and raised to a named owner) and REQ-DRI-008 (data from other systems arrives only through ACE ingestion and the ACE views) for the one outbound artefact this service owns, and it does so without a second copy of the outbound pattern.

The behaviour the business relies on is unchanged from the legacy key: one file per review cycle, a record of every request and every outcome, and a failed delivery that is found and alerted rather than lost. What changes is who owns each step, and the change is a reduction of this service's surface — no transport, no retry ladder, no lake, no new table, no job of its own.

### 3. Preconditions

- RWB-P2-E1007-CON is published: the `deliverFile(manifest)` and `receiveFile` activity contract on task queue `rwb-integration` with the manifest of fileId, batchId, sha256, record count, interfaceId, businessDate, caseIds, idempotencyKey, the claim-check link and the requesting service; the AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`; the four admin operations on `/api/recovery/integration/v1`; the one error envelope; and the contract fakes (DP-16).
- RWB-P5-E1007-APP is published: rwb-document accepts `POST /api/recovery/document/v1/documents` and returns the document ID and the upload link for the stored bytes.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1`, with the append-only, hash-chained entry (DP-03).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with `processed_event`, the CloudEvents 1.0 envelope, the retry topics and the `.dlt` topic (DP-09). This story consumes events; it publishes none of its own.
- RWB-PLT-E1071-CON is published: the workflow kit, the task queue `rwb-access` in namespace `rwb-recovery`, the typed activity interfaces, the retry and heartbeat policy and the codec (DP-10). This story registers two activities on the queue and no workflow.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract that carries LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE with the version in force (DP-07).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the administration screens (DP-19). This story builds no screen.
- RWB-P4-E1037-APP and RWB-P4-E1037-CON delivered the `rwb_access` baseline: the tables `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit`, their dictionary rows, and the operations on `/api/recovery/access/v1`. This story adds no table, no column and no path.
- RWB-P4-AD008-APP owns the JOB-18 `Schedule` and the workflow that calls `buildAccessReviewFile` and `requestFileDelivery`; without it the two activities are built and tested here against the workflow stub, and the run date arrives as an activity input.
- The access-review interface row exists in `interface_config` of `rwb_integration` at the version in force, with direction OUTBOUND, its `file_pattern`, its `data_product`, its `owner_role` and its `alert_role`, loaded by the reference data administrator (RW-REFADM). Its interface ID and its file pattern are Not specified in the source documents (GAP-0981; ASM-1717), so no ID and no pattern appears in this story and no value is written in code.
- The tables the extract reads hold rows at the versions in force: `role` and `permission` at the matrix version in force, `masking_rule` at the masking version in force, `delegation_limit` at the limit version in force, loaded by their own P4 load stories.
- The service runs as the rwb-access login (DP-02) on schema `rwb_access`, and holds no grant on `recovery`, on `public` or on another `rwb_*` schema. The login name is Not specified in the source documents (GAP-0981; ASM-1716).
- The feature switch `rwb.access.access-review-file` exists in the platform flag library and is read as a parameter (Template and Rules §R3 default rulings).

### 4. Flow

1. RWB-P4-AD008-APP: the JOB-18 `Schedule` starts the access-review workflow on queue `rwb-access` for the review date, with the workflow ID derived from the date so a second start for the same date is a no-op.
2. The workflow calls `buildAccessReviewFile(reviewDate)` on queue `rwb-access` (BR1).
3. `buildAccessReviewFile`: resolves the identity that started the run and asks the service's own authorise path for capability area `REFERENCE_DATA`, right R, at the matrix version in force, reading `role` and `permission` in `rwb_access`; a starter without the right is refused before any read of the extract and before any file exists (BR2, AC6).
4. `buildAccessReviewFile`: reads the four tables of this service at the versions in force — `role`, `permission`, `masking_rule`, `delegation_limit` — and the access records of the review period from the local decision-record store; it reads no ACE view, no `public` table and no other schema (BR3, DP-01, DP-05).
5. `buildAccessReviewFile`: writes the extract to the service's staging area as one file, computes the sha256 of the bytes and the record count, and takes the file name from the `file_pattern` of the interface row in force; no file name, pattern or layout is written in code (BR4, BR5).
6. `buildAccessReviewFile`: stores the bytes once with `POST /api/recovery/document/v1/documents` on rwb-document and keeps the document ID; the bytes are never copied a second time and never travel on a message (BR6, DP-11).
7. `buildAccessReviewFile`: assembles the manifest — file name, sha256, record count, business date, the interface ID, the requesting service `rwb-access` and the idempotency key `<interfaceId>:<businessDate>` — and returns it with the document ID; the manifest carries no row of the four tables and no personal data (BR7).
8. The workflow calls `requestFileDelivery(manifest)` on queue `rwb-access`.
9. `requestFileDelivery`: reads the `idempotency_key` object of the library created in `rwb_access`; when the key is already present, it answers the stored item reference and makes no second request and writes no second entry (BR8, AC1).
10. `requestFileDelivery`: calls the rwb-integration activity `deliverFile(manifest)` on task queue `rwb-integration` once, with the manifest of RWB-P2-E1007-CON, and keeps the item reference and the item status it returns (BR9, DP-16, AC3).
11. `requestFileDelivery`: writes one decision-record entry with the action `request`, the interface, the business date, the file name, the sha256, the record count, the document ID and the item reference, in the same transaction as the stored idempotency key (BR10, DP-03).
12. The workflow waits. rwb-integration builds, sends, retries on the intervals of its own interface row and, after its last attempt, parks the item in its exception queue with the owner task through rwb-case — none of which is a step of this service (BR11).
13. The outcome listener: on `rwb.integration.FileDelivered.v1` or `rwb.integration.FileFailed.v1` for an interface and business date this service requested, checks the inbox in `processed_event` by consumer and CloudEvents id, and on a first sight writes one decision-record entry — action `delivered` with the document ID, the sha256 and the record count, or action `failed` with the attempt count and the last error code (BR12, BR13, AC4, AC5).
14. On `FileFailed` the listener raises an alert naming the interface, the business date and the last error code to the alert role of the interface row; it raises no task, no case route state and no retry of its own (BR14, AC5).
15. A redelivery of either event writes nothing new: the inbox hit count rises and the request state stays as it was (BR15, AC8).
16. On demand, `requestFileDelivery` answers the item status through `GET /api/recovery/integration/v1/admin/outbound-items` on `/api/recovery/integration/v1` — a read, one hop, 2 s, never a row read of `rwb_integration` (BR16, DP-11).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same review date is requested twice | The `idempotency_key` of the library holds `<interfaceId>:<businessDate>`, so the second run makes no second document, no second `deliverFile` call and no second request entry | None | AC1, AC8 |
| X2 | The identity that started the run holds no R letter in capability area `REFERENCE_DATA` | 403 before any read of the extract; no file, no document, no `deliverFile` call, no request entry | MSG-P4-002 | AC6 |
| X3 | rwb-document does not answer, or answers with an error | The activity fails with a typed failure and is retried by the workflow kit; no manifest is returned and no `deliverFile` call is made, so no request entry exists | MSG-GEN-006 | AC2, AC3 |
| X4 | The `deliverFile` activity fails with a typed failure | The request activity returns the failure to the workflow; no delivery is recorded, no second call is made in that run and the state stays `REQUESTED` | MSG-GEN-006 | AC3 |
| X5 | rwb-integration reports the file as failed after its last attempt | One decision-record entry with action `failed`, one alert to the alert role of the interface row; no task, no case route state and no retry ladder here | MSG-P2-001 (produced by rwb-integration) | AC5 |
| X6 | The same `FileDelivered` or `FileFailed` arrives twice with the same CloudEvents id | The second is ignored, the hit count in `processed_event` rises to 2 and no second entry and no second alert exist (R-UNI-40) | None | AC8 |
| X7 | The decision record cannot be written | The activity fails with 503 and no manifest and no request entry is produced, so nothing is delivered that cannot be recorded | MSG-P7-003 | AC4, AC7 |
| X8 | A class of the package names a `v_ace_*` view, a `public` table or a data lake path | The build fails with boundary rule BND-6 and the class is named; nothing merges | Build log | AC7 |
| X9 | A class of the package opens an SFTP session or writes a second copy of the file bytes | The boundary test fails the build and the class is named | Build log | AC7 |
| X10 | The delivery events arrive for an interface and business date this service never requested | The event is recorded as an unmatched outcome and written to the `.dlt` with an alert, because it cannot be tied to a request of this service | None | AC4, AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P2-E1007-CON and its fakes, the rwb-document fake and the decision-record stub; it waits for no other service's implementation and for no in-lane story |
| Negotiable | The interface row, the file pattern, the data product, the owner and alert roles, the review date and the feature switch are rows and parameters; the story fixes only the behaviour and the record |
| Valuable | The one outbound artefact of the access service leaves through the platform's one governed file path, and every request and outcome is on the append-only record |
| Estimable | Two activities, two listeners, one manifest, two consumed contracts, one store call, one admin read and one decision-record writer |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key; no table, no migration, no workflow and no Schedule |
| Testable | Every criterion in section 7 is one automated test against the contract fakes; the boundary criteria are build rules |

### 7. Acceptance criteria

```gherkin
Feature: The access-review file requested from the rwb-integration outbound-file capability

  Background:
    Given the base is /api/recovery/access/v1, the schema is rwb_access, the topic is rwb.access.events.v1 and the task queue is rwb-access
    Given the rwb-integration activity contract of RWB-P2-E1007-CON is published on task queue rwb-integration and is answered by its fake
    Given the review date is 2026-11-30 and the interface row in force for the access-review interface has direction "OUTBOUND"
    Given every access row fixture is synthetic and no production row, file or address is used

  Scenario: AC1 One request per business date under the idempotency key (new, D-RCV-60)
    Given the access-review workflow of RWB-P4-AD008-APP runs for review date "2026-11-30"
    When buildAccessReviewFile and requestFileDelivery run on queue "rwb-access" for that date
    Then exactly one deliverFile call is made with the idempotency key "<interfaceId>:2026-11-30"
    When the same two activities run again for the same date
    Then the idempotency_key record of the library answers the first item reference and no second deliverFile call is made
    Then no second document is stored and no second decision-record request entry is written
    Then the workflow ID of the run keeps a second start for the same date a no-op

  Scenario: AC2 The manifest and the stored file (new, D-RCV-60)
    Given role, permission, masking_rule and delegation_limit hold their fixture rows at the versions in force for "2026-11-30"
    When buildAccessReviewFile builds the extract
    Then the bytes are stored once through POST /api/recovery/document/v1/documents on rwb-document and the document ID is kept
    Then the manifest carries the file name taken from the file_pattern of the interface row, the sha256 of the stored bytes, the record count and the business date "2026-11-30"
    Then the record count equals the number of rows written to the file and the sha256 is recomputed from the stored bytes
    Then the manifest carries no row of the four tables, no name, no address and no identity number
    Then no file name, layout or pattern is written in code, and the file name, layout and recipient are Not specified in the source documents (GAP-0981; ASM-1717)

  Scenario: AC3 The deliverFile call and its one-hop activity contract (new, D-RCV-60)
    Given the manifest of the extract for "2026-11-30"
    When requestFileDelivery runs on queue "rwb-access"
    Then it calls the rwb-integration activity deliverFile(manifest) on task queue "rwb-integration" once, with the manifest elements of RWB-P2-E1007-CON
    Then the answer is the outbound item reference and its status, and the outcome arrives as rwb.integration.FileDelivered.v1 or rwb.integration.FileFailed.v1
    Then no statement of the activity names interface_config, outbound_item, outbox_delivery or any other relation of rwb_integration
    Then the call is one hop with no chain, and no second copy of the file is built, staged or sent
    Then a typed failure of deliverFile returns the failure to the workflow with no delivery recorded and no second call in that run

  Scenario: AC4 FileDelivered consumed once and recorded (new, D-RCV-60)
    Given rwb.integration.FileDelivered.v1 for the access-review interface and "2026-11-30" arrives on rwb.integration.events.v1
    When the outcome listener handles it
    Then one processed_event row is written for the consumer and the CloudEvents id
    Then one decision-record entry is written through the DP-03 library with the action "delivered", the item reference, the document ID, the sha256 and the record count
    Then the entry carries no name, no address, no identity number and no file content
    Then the request state is "DELIVERED"

  Scenario: AC5 FileFailed recorded and alerted with no task raised here (new, D-RCV-60)
    Given rwb.integration.FileFailed.v1 for the access-review interface and "2026-11-30" arrives with an attempt count and a last error code
    When the outcome listener handles it
    Then one decision-record entry is written with the action "failed", the item reference, the attempt count and the last error code
    Then one alert is raised to the alert role of the interface row, naming the interface, the business date and the last error code
    Then no task row, no case route state and no exception-queue row is written or changed by this story
    Then no retry is scheduled by this story and the request state is "FAILED"
    Then the delivery event is matched to the request by interface and business date, and the case-ID key of the event is Not specified in the source documents for a file with no case (GAP-0981; ASM-1718)

  Scenario: AC6 A role without the Reference data R right is refused (new, D-RCV-60)
    Given the fixture permission row of role "RW-CASEOWN" carries no R letter in capability area "REFERENCE_DATA"
    When a review run started by that role calls buildAccessReviewFile for "2026-11-30"
    Then the call is refused with status 403 and message MSG-P4-002
    Then no table of the extract is read, no file is built, no document is stored, no deliverFile call is made and no decision-record entry is written
    When a review run is started by a role whose permission row carries R in "REFERENCE_DATA"
    Then the request proceeds and one request entry is written
    Then the letters are read from permission at the matrix version in force, and no role code and no letter is written in code

  Scenario: AC7 No SFTP and no ACE view read in the package (new, D-RCV-60)
    Given a class "th.co.scb.ace.workbench.recovery.access.review.CustomerReader" with a query on "recovery.v_ace_customer"
    When the pipeline runs the boundary rule of the rwb-access build
    Then the build fails with boundary rule BND-6, the class and the object
    When the same class names "public.customer" instead
    Then the build fails with boundary rule BND-6, the class and the object
    When a class of the package opens an SFTP session, writes a second copy of the file bytes or names a data lake path
    Then the build fails and the class is named
    Then the rwb-access login holds no SELECT on any of the 30 recovery.v_ace_* views and no privilege in public
    Then the only file writing class of the package writes the one staging file and the only storage call is POST /api/recovery/document/v1/documents

  Scenario: AC8 A repeated outcome writes nothing new (new, D-RCV-60)
    Given the request for "2026-11-30" is in state "DELIVERED" and its outcome entry exists
    When a redelivery of the same rwb.integration.FileDelivered.v1 arrives with the same CloudEvents id
    Then the hit count of the inbox row becomes 2 and no second entry is written
    Then the request state stays "DELIVERED" and no second alert is raised
    When a redelivery of the same rwb.integration.FileFailed.v1 arrives after a delivered outcome with the same CloudEvents id
    Then no second failed entry is written and no second alert is raised
    Then a re-run of the review for the same date makes no second document, no second deliverFile call and no second request entry
```

The eight criteria above are new and test only this deliverable: the requester side of the outbound path and its record. The legacy criteria of RWB-E1-007 are owned elsewhere — AC1, AC2, AC3, AC5, AC6 and AC7 by RWB-P2-E1007-APP, AC4 by RWB-ITG-E1007-ITG, and the end-to-end journey of the key by RWB-ITG-E1007-ITG — and no legacy criterion text is copied into this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The access-review pack is built by two activities on queue `rwb-access` and by nothing else: `buildAccessReviewFile` and `requestFileDelivery`. The workflow and the six-monthly `Schedule` are RWB-P4-AD008-APP's | Architecture v5 slide 44 (JOB-18); DP-10; GAP-0981; ASM-1716 |
| BR2 | The run is authorised before the extract is read: the starter must hold the R letter in capability area `REFERENCE_DATA` at the matrix version in force, and the letters are rows of `permission` | FSD P4 A2.4; VR-P4-004-1; MSG-P4-002 |
| BR3 | The extract is built only from this service's own `role`, `permission`, `masking_rule`, `delegation_limit` and its local access records; no ACE view, no `public` table and no other schema is read | Architecture v5 slides 8, 9, 14 and 41; DP-01; DP-05; ADR-010 |
| BR4 | The file name comes from the `file_pattern` of the interface row in force and the layout from the interface's own definition; no name, pattern, layout or recipient is written in code | Principle 1; DP-16; GAP-0981; ASM-1717 |
| BR5 | One file per review cycle per business date, with the sha256 of the stored bytes and the record count on the manifest; the count is the count of rows actually written | Arch v5 slide 11 (claim-check: fileId, batchId, sha256, record count); DP-16 |
| BR6 | The bytes are stored once, through `POST /api/recovery/document/v1/documents` on rwb-document, and are never copied a second time and never carried on a message, a workflow input or a log | Arch v5 slide 11; DP-11; CTL-11 |
| BR7 | The manifest carries the file name, the sha256, the record count, the business date, the interface, the requesting service and the idempotency key, and carries no row of the four tables and no personal data | Arch v5 slide 11; DP-16; ASM-1716 |
| BR8 | One request per business date: the key `<interfaceId>:<businessDate>` is recorded in the `idempotency_key` object of the library created in `rwb_access`, and a repeat answers the first item reference and changes nothing | Arch v5 slide 11; DP-09; legacy RWB-E1-007 section 12 (key per interface and business date) |
| BR9 | The delivery request is the rwb-integration activity `deliverFile(manifest)` on task queue `rwb-integration`, one hop, never a REST substitute and never a write to an `rwb_integration` table | DP-16; DP-11; RWB-P2-E1007-CON |
| BR10 | One decision-record entry per request, written through the DP-03 library in the same transaction as the stored idempotency key; a request that cannot be recorded is not made | DP-03; R-UNI-39; FSD P4 A2.7 |
| BR11 | The transport, the PGP key, the retry ladder on `retry_intervals_min`, the exception queue, the resend and the owner task are rwb-integration's and rwb-case's; this story builds none of them and reads none of their tables | Architecture v5 slides 13, 16 and 44; DP-16; RWB-P2-E1007-APP |
| BR12 | The outcomes are consumed from `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1` with the inbox dedupe of `processed_event`, and one entry is written per first sight | DP-09; R-UNI-40; Arch v5 slide 43 |
| BR13 | The delivered entry carries the document ID, the sha256 and the record count; the failed entry carries the attempt count and the last error code; neither carries file content, a name, an address or an identity number | CTL-11; DP-09; Guardrails |
| BR14 | A failed delivery raises one alert to the alert role of the interface row and nothing else: no task, no case route state, no retry and no exception-queue row of this service | R-UNI-34 (owner task is rwb-integration's and rwb-case's); RWB-P2-E1007-OPS |
| BR15 | A redelivered outcome is ignored and counted in `processed_event`; a rule that acts twice on one outcome is a defect | R-UNI-40; DP-09 |
| BR16 | The item status is read through the rwb-integration admin operation `GET /api/recovery/integration/v1/admin/outbound-items`, one hop with a 2 s budget, and never from a table of `rwb_integration` | DP-11; DP-16; RWB-P2-E1007-CON |
| BR17 | There is no data lake and no lake copy: no lake path, no lake file and no lake delivery row is built by this story | DP-17; Arch v5 slides 37 and 44 |
| BR18 | There is no SFTP class, no file-system transport and no second file copy in this package: the only transport of the bytes is rwb-document and the only transport to the party is rwb-integration's | DP-16; DP-17; Arch v5 slide 42 |

### 9. State transitions

The request state of one review cycle, held on the decision record and not in a table of its own:

| From | Event | Condition | To |
|---|---|---|---|
| none | `buildAccessReviewFile` and `requestFileDelivery` complete | The R letter is held, the file is stored and `deliverFile` accepted the manifest | REQUESTED |
| none | The starter holds no R letter in `REFERENCE_DATA` | The authorise answer refuses | Refused; no state is recorded and no file exists |
| REQUESTED | `rwb.integration.FileDelivered.v1` first sight | The item is the one this request named | DELIVERED |
| REQUESTED | `rwb.integration.FileFailed.v1` first sight | The item is the one this request named | FAILED |
| DELIVERED | The same event redelivered | The CloudEvents id is already in `processed_event` | DELIVERED, hit count raised |
| FAILED | The same event redelivered | The CloudEvents id is already in `processed_event` | FAILED, hit count raised |
| FAILED | A later review cycle for a later business date | A new request under a new key | REQUESTED, for the new date |

The outbound item states this service observes and never writes are rwb-integration's: PENDING, SENT, RETRY, EXCEPTION and ACKNOWLEDGED (LOV-OUTBOUND-STATUS; TSD P2 v3 T3.2), and `outbox_delivery` follows PENDING, RETRYING, DELIVERED and EXCEPTION. No case status, no case route state and no task state is read or written by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Builds the extract from its own four tables, stores the bytes once, calls `deliverFile`, consumes the two outcomes, writes the decision-record entries and reads the item status |
| rwb-integration service identity | Receives the manifest, executes the outbound-file workflow, applies the retry ladder, parks the item in its exception queue, raises the owner task and publishes `FileDelivered` and `FileFailed` |
| rwb-document service identity | Stores the bytes once and returns the document ID and the upload link behind the claim-check link |
| RW-SECADM, security administrator | Starts a review cycle and holds CRUDA in Platform administration; reads the delivery outcome |
| RW-REFADM, reference data administrator | Loads the interface row of the review file and the four tables' versions; holds no right on the delivery |
| RW-COMPLY, compliance and PDPA officer | Reads the review file, the masking rows it carries and the delivery outcome |
| RW-AUDIT, internal audit | Reads the request entries, the outcome entries and the delivery status |
| RW-CASEOWN and every other business role | Nothing in this story: the review file is not theirs to request and no letter of theirs names `REFERENCE_DATA` R |
| No approval level from the delegation of authority applies | The story takes no business decision and reads the DoA table only as extract content |

The rwb-access login name is Not specified in the source documents (GAP-0981; ASM-1716); the story names it "the rwb-access login (DP-02)" until the platform DB story fixes it. No role grants itself a row, and no role code, area or letter is fixed in code.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` (P4, `rwb_access`) | id, role_code, role_name, role_class, default_scope, entra_group | Read; the extract carries the role rows in force |
| DF-REF-040 to DF-REF-044 | `permission` (P4, `rwb_access`) | id, role_id, capability_area, letters, matrix_version | Read; the extract carries the matrix rows in force |
| DF-REF-198 to DF-REF-204 | `masking_rule` (P4, `rwb_access`) | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read; the extract carries the masking rows in force |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | `delegation_limit` (P4, `rwb_access`) | id, decision_code, approval_level, product_group, the limits, the holder and substitute, limit_version, valid_from, valid_to | Read; the extract carries the limit rows in force |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | access entry (local decision record) | decision code, actor reference, action, item reference, decided at, hash chain, idempotency key | Write; the request entry and the outcome entry of each cycle |
| DF-DEC-014 | access entry (local decision record) | actions (interface, business date, file name, sha256, record count, document ID, attempt count, last error code) | Write |
| DF-OPS-137 to DF-OPS-148 | `interface_config` (P2, `rwb_integration`) | interface_id, direction, file_pattern, data_product, owner_role, alert_role, valid_from, valid_to | Read through the rwb-integration contract only; no row read from `rwb_integration` |
| DF-OPS-168 to DF-OPS-177 | `outbound_item` (P2, `rwb_integration`) | id, status, attempt count, last error, manifest reference | Read through `GET /api/recovery/integration/v1/admin/outbound-items` only |
| DF-OPS-178 to DF-OPS-183 (library numbering, created in `rwb_access`) | `processed_event` (PLT library) | consumer, idempotency key, CloudEvents id, hit count, last seen at | Write |
| DF-OPS-184 to DF-OPS-188 (library numbering, created in `rwb_access`) | `idempotency_key` (PLT library) | key, operation, request hash, stored answer | Write; the `<interfaceId>:<businessDate>` key of the request |
| DF-DOC-006 | `document` (P5, `rwb_document`) | storage_ref behind the claim-check link | Read through the rwb-document contract answer only |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` (ACE view, read only by rwb-source-data) | the personal fields the masking rows key on | Not read and not written; the masking rows name a field ID only |

The four tables of `rwb_access` are read and never written by this story; the access entries are written through the decision-record library into the service's own schema, and the two library objects are created there by DP-09. `outbound_item`, `interface_config` and `outbox_delivery` are P2's and are reached only through the rwb-integration admin operation, never from another schema. No foreign key leaves `rwb_access`, no row of another service is copied into it, and the extract carries values from its own tables only. Field IDs are those of the Logical Data Model and Data Dictionary v9 and the TSD P4 Access and administration v3 T3.1.

### 12. Contract

#### 12.1 REST operations provided

None new. The service base is `/api/recovery/access/v1` and its operations are RWB-P4-E1037-CON's: `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `GET /masking-policies`. This slice adds no path, no query parameter and no response field, and the request of a review cycle is a Temporal activity call from the JOB-18 workflow, not a REST operation. The six-monthly trigger is RWB-P4-AD008-APP's `Schedule` and is declared there, not here.

#### 12.2 REST operations consumed

Two operations, each one hop with a 2 s client budget, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The `deliverFile` call of AC3 is a Temporal activity and is declared in 12.5, not here.

| Method | Path | Owner | Used for |
|---|---|---|---|
| POST | `/api/recovery/document/v1/documents` | P5 rwb-document | Stores the built extract once and returns the document ID and the upload link (AC2) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | Reads the status of the request's outbound item by interface and business date (AC3, BR16) |

No third call is made at run time: the access rows come from the service's own schema, the reference lists come through the client library of DP-07, and the right check is answered inside the service. The access-review extract has no reader in this story — the recipient of the file, the layout and the interface ID are Not specified in the source documents (GAP-0981; ASM-1717) and are fixed in the interface row at run time, not here.

#### 12.3 Events published

None of its own. This service publishes no file event and opens no second topic for the review: the request entry and the outcome entry are decision records written through the DP-03 library, which publishes `rwb.decision-record.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1` under its own schema (RWB-PLT-E1027-CON). A review file event of this service would duplicate `FileDelivered` and is therefore not declared.

#### 12.4 Events consumed

| Event type | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | First sight: one `processed_event` row and one decision-record entry with the action `delivered`; the request state becomes DELIVERED (AC4) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | First sight: one `processed_event` row, one decision-record entry with the action `failed` and one alert to the alert role of the interface row; no task and no retry here (AC5) |

Both arrive with the CloudEvents 1.0 envelope in binary mode and are deduped by consumer and CloudEvents id in `processed_event`; a message without the envelope or of any other type is refused by the consumer's schema check and routed to `.dlt` with an alert (DP-09). The payload elements are those of RWB-P2-E1007-CON: fileId, interfaceId, businessDate, documentId, sha256, recordCount and requesting service for the delivered event, and fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds and ownerRole for the failed event. The events are keyed by case ID and an access-review file carries no case, so this service matches an outcome to its request by interface and business date and uses no case key: Not specified in the source documents (GAP-0981; ASM-1718).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `buildAccessReviewFile(reviewDate)` | Activity, provided by this service | `rwb-access` | Input: the review date, the starter identity and the feature switch. Output: the manifest of BR7 and the document ID. Typed failures: `RightRefused`, `ExtractNotBuilt`, `StoreUnavailable`, `RecordUnwritable` |
| `requestFileDelivery(manifest)` | Activity, provided by this service | `rwb-access` | Input: the manifest of BR7 and the document ID. Output: the outbound item reference, the item status and the idempotency key. Typed failures: `DeliveryRefused`, `DeliveryUnavailable`, `RecordUnwritable` |
| `deliverFile(manifest)` | Activity, provided by P2, called from `requestFileDelivery` | `rwb-integration` | The one-hop call of BR9: input and output as published by RWB-P2-E1007-CON, one call per business date |
| The JOB-18 workflow | Workflow, owned by RWB-P4-AD008-APP | `rwb-access` | Calls the two activities for the review date and carries the six-monthly trigger; this story registers no workflow |

The activity names, their inputs and outputs and the manifest element list are fixed by this story: Not specified in the source documents (GAP-0981; ASM-1716). The retry policy of both activities is the workflow kit's — initial interval 1 s, back-off 2, with a refused right and an unwritable record classified as non-retryable and a 5xx or a timeout as retryable (DP-10). The file-level retry ladder is not an activity retry: it is the `max_attempts` and `retry_intervals_min` of the interface row, applied inside rwb-integration, and this story holds no timer of its own.

#### 12.6 Schedules

None. The six-monthly access-review list is JOB-18 and its `Schedule` sits in this service but is the deliverable of RWB-P4-AD008-APP (Architecture v5 slide 44). This story registers no `Schedule`, no cron and no timer, and it is called by that workflow.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `role` | P4 (`rwb_access`) | Recovery roles as data; read here, no row written |
| `permission` | P4 (`rwb_access`) | The matrix as data; read here, no row written |
| `masking_rule` | P4 (`rwb_access`) | Which role sees which personal field unmasked, by version; read here, no row written |
| `delegation_limit` | P4 (`rwb_access`) | The DoA table; read here as extract content, no row written |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | The request entry and the outcome entry of each cycle (DP-03) |
| `processed_event` | PLT library, created in `rwb_access` | The inbox of the two delivery events (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_access` | The `<interfaceId>:<businessDate>` key of the request (DP-09) |

No table is created, altered or added by this story and no migration of its own is written: the four tables and the library objects arrive with the `rwb_access` baseline and DP-09. `interface_config`, `outbound_item` and `outbox_delivery` are P2's and appear in no statement of this package; `document` is P5's and is reached through its contract only; no `v_ace_*` view is named (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P2-E1007-CON activity fake | `deliverFile(manifest)` on queue `rwb-integration` | Acceptance with an item reference and PENDING; one `DeliveryRefused` typed failure; one `DeliveryUnavailable` |
| rwb-integration admin WireMock | `GET /api/recovery/integration/v1/admin/outbound-items` | One item in PENDING, one in ACKNOWLEDGED and one in EXCEPTION; one 404 |
| rwb-document WireMock | `POST /api/recovery/document/v1/documents` | 201 with a document ID and an upload link; one 503 for X3 |
| Kafka stubs | `rwb.integration.events.v1` | One `FileDelivered`, one `FileFailed`, a duplicate of each with the same CloudEvents id, one event for an unknown interface, one malformed envelope |
| decision-record library stub | DP-03 | A healthy chain and a stopped chain for the 503 path |
| reference-data fake | DP-07 | LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE at the version in force |
| interface row fixture | The interface row of the review file | Direction OUTBOUND, a file pattern and an alert role; the interface ID and the pattern are synthetic placeholders of GAP-0981 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided, 2 consumed | `POST /api/recovery/document/v1/documents` on rwb-document and `GET /api/recovery/integration/v1/admin/outbound-items` on rwb-integration; one hop, 2 s timeout |
| Kafka | 0 published by this story, 2 consumed | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` with the inbox dedupe; the decision-record library publishes `DecisionRecorded` on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 2 activities provided, 1 activity consumed | `buildAccessReviewFile` and `requestFileDelivery` on queue `rwb-access`; `deliverFile` on queue `rwb-integration`; the JOB-18 workflow is RWB-P4-AD008-APP's |
| File | 1 delivered file per review cycle | One staging file and one stored document behind the claim-check manifest handed to rwb-integration; no SFTP class, no second copy and no data lake in this package |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.review`, module `review`, in the service root `th.co.scb.ace.workbench.recovery.access`. The outcome listener sits beside it in `...access.review.event`, and the boundary rule is added to the test source tree of the service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_access`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts only through rwb-source-data's contract; this service reads no view | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case and the client library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the owner's topic, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal activity contract on the service queue through the workflow kit; the Schedule is AD008's | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST and activity contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-16 | `recovery.integration.adapter` | The rwb-integration contract: the `deliverFile` activity, the two events and the admin read | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); no lake target, no lake file and no lake delivery row | none; gap if the story needed lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**This is a secondary slice: the metadata H row is None and this story adds no build dependency of its own.** The platform contracts behind DP-03, DP-07, DP-09, DP-10 and DP-19 arrive with the `rwb_access` baseline and RWB-P4-E1037-CON, and the one contract dependency, `RWB-P2-E1007-CON` of DP-16, never blocks a build (§R5.4): the activity fake, the admin read fake and the Kafka stubs of 12.8 stand in for rwb-integration on Day 1. DP-05 resolves to a prohibition (no `v_ace_*` view is read here and the boundary rule enforces it), DP-01 to "the four tables and the records are this service's and no other schema is named", DP-17 to "no lake element anywhere in the package", and DP-11 to the inbound budget of the two consumed operations and the one hop of the `deliverFile` call. DP-19 is the route that renders the delivery outcome on the administration screens, which this story does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessReviewRequestAuthoriser` | Service | Resolves the starter identity and the R letter in `REFERENCE_DATA` from `role` and `permission` at the matrix version in force before any extract is read |
| `AccessReviewExtractReader` | Repository | Reads `role`, `permission`, `masking_rule`, `delegation_limit` and the local access entries at the versions in force; reads no other schema |
| `AccessReviewFileBuilder` | Service | Writes the one staging file, computes the sha256 and the record count, takes the file name from the interface row |
| `AccessReviewManifest` | Value | The manifest of BR7: file name, sha256, record count, business date, interface, requesting service and idempotency key |
| `DocumentStoreClient` | Client | `POST /api/recovery/document/v1/documents` on rwb-document, one hop, 2 s; returns the document ID |
| `DeliveryRequestClient` | Client | The one `deliverFile(manifest)` call on task queue `rwb-integration`, typed failures mapped |
| `RequestKeyStore` | Service | Reads and writes the `idempotency_key` object created in `rwb_access`, so one request exists per business date |
| `DeliveryOutcomeListener` | Listener | Consumes `FileDelivered` and `FileFailed`, dedupes in `processed_event`, writes the outcome entry, raises the failure alert |
| `ItemStatusReader` | Client | `GET /api/recovery/integration/v1/admin/outbound-items`, one hop, 2 s |
| `ReviewRecordWriter` | Service | Writes the request and outcome entries through the DP-03 library, first in the transaction; a failed write fails the activity |
| `buildAccessReviewFile`, `requestFileDelivery` | Activities | The two typed activities on queue `rwb-access` |
| `ReviewBoundaryRule` | ArchUnit rule in the test source | BND-6 over the module map: no `v_ace_*` view, no `public` table, no data lake path, no SFTP class and no second file copy |

**Database and migrations.** None. This story creates no table, adds no column and writes no migration: the four tables, `role_conflict` and the library objects are the `rwb_access` baseline and DP-09, and the verdicts of `masking_rule` are another P4 story's rows. The request and outcome entries are rows of the decision-record library in `rwb_access`, and the two library objects (`processed_event`, `idempotency_key`) are created there by the platform library migration.

**Configuration and reference data**

- The interface row of the access-review file: direction OUTBOUND, its `file_pattern`, `data_product`, `owner_role` and `alert_role`, loaded by RW-REFADM at the version in force. Its interface ID and its pattern are Not specified in the source documents (GAP-0981; ASM-1717).
- The extract layout and the recipient of the file: Not specified in the source documents (GAP-0981; ASM-1717). The layout is declared with the interface row and never in code, and this story fixes only the manifest.
- Lists LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE come from the reference-data contract at the version in force (DP-07); the capability area of the right check, `REFERENCE_DATA`, is one of their values.
- The feature switch is `rwb.access.access-review-file`, read as a parameter: off means `buildAccessReviewFile` refuses and no file, no document and no request exist.
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0981; ASM-1716).

**Build steps**

1. `AccessReviewRequestAuthoriser` with the R-letter check in `REFERENCE_DATA` ordered before every read; tests for AC6.
2. `AccessReviewExtractReader` over the four tables and the access records, with a fixture set that names no ACE view and no other schema; tests for AC2 and the reading half of AC7.
3. `AccessReviewFileBuilder` and `AccessReviewManifest` with the sha256, the record count and the file name from the interface row; tests for AC2.
4. `DocumentStoreClient` with the one store call and the 503 path; tests for AC2 and X3.
5. `RequestKeyStore` and the one-request-per-date path, including the second run of the same date; tests for AC1.
6. `DeliveryRequestClient` and the two activities with the typed failures and the one-hop call on queue `rwb-integration`; tests for AC3.
7. `DeliveryOutcomeListener` with the inbox dedupe, the two entry shapes and the failure alert; tests for AC4, AC5 and AC8.
8. `ItemStatusReader` against the admin-read fake; the read half of AC3.
9. `ReviewBoundaryRule` and the module map with a fixture class on `recovery.v_ace_customer`, the same class on `public.customer`, a class naming a lake path and a class opening an SFTP session; tests for AC7.
10. A contract-fake run of the whole path, so the story builds before RWB-P4-AD008-APP and rwb-integration are live.

**Feature switch.** `rwb.access.access-review-file`, read as a parameter; off refuses the build of the extract and leaves the boundary rules and the right check in force.

**Done when.** The tests of section 16 pass, one request exists per review date under the key, one document is stored and one `deliverFile` call is made per cycle, each outcome writes one entry and a redelivery writes none, the build is green and red on the four boundary fixtures, and a session as the rwb-access login holds no privilege on any of the 30 views and none in `public`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The token holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The starter's roles carry no R letter in capability area `REFERENCE_DATA` | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written, so the request is not made | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | rwb-document or the `deliverFile` activity is unavailable and the step is retried | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-001 | Produced by rwb-integration when its item moves to the exception queue; read here, never produced | The {interface} file {file} was not sent after {count} attempts. It is in the exception queue. |
| Build log | A class names a `v_ace_*` view, a `public` table, a lake path or an SFTP session | Boundary rule BND-6 broken: {class} names {object}. A recovery class names no ACE view, no public table, no lake and no SFTP endpoint. |
| Alert | A `FileFailed` outcome is consumed for a request of this cycle | The {interface} access-review file for {businessDate} was not delivered: {lastError}. |

For MSG-P4-002 in this story, {action} names the action the role tried, for example "request the access-review file", and never a row of the extract. The alert text and its identifier are Not specified in the source documents (GAP-0981; ASM-1717) and are owned by RWB-P2-E1007-OPS through the alert role of the interface row; the delivery itself is never re-sent from here. No new `MSG-` identifier is introduced by this story.

### 15. Screens and states

No screen is built by this story. The delivery outcome is read on the administration screens served by the gateway-bff composite route (DP-19) — SCR-43 Roles and access for the review rows and the versions they were built from, and the interface and job monitor for the file state — and those screens, their fields and their states belong to their own stories. This story supplies the request entry, the outcome entry and the item status the screens read, and it renders nothing: the review file is a file, not a screen, and its layout and recipient are Not specified in the source documents (GAP-0981; ASM-1717).

| State | What the reader sees through the owner's contract |
|---|---|
| Requested | One request entry for the business date and the item in PENDING on the rwb-integration admin read |
| Delivered | One outcome entry with action `delivered`, the document ID, the sha256 and the record count |
| Failed | One outcome entry with action `failed`, the attempt count and the last error code, and the item in the rwb-integration exception queue with its owner task |
| Repeated | The same view as the first outcome, with the inbox hit count raised and no second entry |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-10 | AC6, BR2 | Component | A review run started by role RW-CASEOWN with no R letter in `REFERENCE_DATA`; refused with MSG-P4-002 and no file, no document and no request entry |
| TC-E1-007-01 | AC3 (requester side only); the one-pattern behaviour itself is RWB-P2-E1007-APP's | Contract | One manifest against the `deliverFile` activity fake; the declared manifest elements; an undeclared field refused |
| TC-E1-007-02 | AC7, BR3 | Component | Fixture classes on `recovery.v_ace_customer` and `public.customer`; the passing class on the rwb-document contract; a session as the rwb-access login against the 30 view names |
| TC-E1-007-03 | None here (the retry ladder, the exception queue and the owner task are RWB-P2-E1007-APP's and RWB-ITG-E1007-ITG's); AC5 records the outcome only | Integration | The `FileFailed` fixture with an attempt count and a last error code; the entry and the alert asserted, no task and no route state |
| TC-E1-007-04 | None here (the held request is the freshness gate of RWB-P2-E1007-APP and the criterion of RWB-ITG-E1007-ITG); this story builds nothing while a request is held | Integration | The held-request fixture of the P2 activity fake; no document, no request entry and no second call |
| TC-E1-007-07 | AC4, AC8, BR12, BR15 | Component | One `FileDelivered` and one `FileFailed`, each sent twice with the same CloudEvents id; hit count 2 and no second entry |
| TC-E1-007-08 | AC1, BR8 | Component | Two runs for the same review date; one document, one `deliverFile` call and one request entry |
| TC-E1-007-09 | None here (the resend and the exception-queue surface are RWB-P2-E1007-APP's and RWB-P2-E1007-CON's) | Integration | The resend fixture of the rwb-integration admin fake; this story only re-reads the item status, and the resend changes nothing here |
| TC-E1-007-05 | None (retired with the inbound file load; the behaviour is ACE ingestion and EV-27 AceDataLate) | End to end | The legacy inbound case "file missing at the cut-off"; carried as a reference row only and not run by this story |
| TC-E1-007-06 | None (retired with the inbound file load; the behaviour is ACE ingestion) | End to end | The legacy inbound case "same file delivered twice"; carried as a reference row only and not run by this story |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. Every legacy test case of this key is listed above with the slice of the behaviour this story answers: TC-E1-007-10 answers the access refusal on the request that this service now owns; TC-E1-007-01 answers the one-pattern rule at the requester boundary, the pattern itself being RWB-P2-E1007-APP's; TC-E1-007-02 answers the ACE boundary as a prohibition, because this service reads no view at all; TC-E1-007-03, TC-E1-007-04 and TC-E1-007-09 answer the retry ladder, the held request and the resend, which are rwb-integration's and are run by RWB-P2-E1007-APP and RWB-ITG-E1007-ITG; TC-E1-007-07 and TC-E1-007-08 answer the duplicate outcome and the single request, which this slice does own; and TC-E1-007-05 and TC-E1-007-06 stay as retired legacy IDs. The `-ITG` copies of these cases are not here — they belong to RWB-ITG-E1007-ITG, which proves the file path across the real services.

### 17. Guardrails

- No business value in code: the interface ID, the file pattern, the layout, the data product, the owner and alert roles, the review date, the matrix, masking and limit versions and the feature switch are rows and parameters read at run time.
- No personal data in events, logs, workflow inputs, manifests, tests or prompts: the manifest carries a file name, a sha256, a count and a date, and the entries carry identifiers, codes and counts; file content is never logged.
- ACE data only through the owner's contract or `v_ace_*` views — and this service reads neither: a class that names a view fails the build, and the masking rows name a field ID only.
- No cross-schema read and no cross-schema key: `rwb_access` holds no foreign key into another schema and no copy of an item, a document or a case row; `outbound_item`, `interface_config` and `outbox_delivery` are reached only through the rwb-integration admin operation (DP-01).
- No SFTP class, no file-system transport and no second copy of the bytes in this package: the only transport of the bytes is rwb-document and the only transport to the party is rwb-integration's transport component (DP-16).
- No data lake: no lake path, no lake file, no lake delivery row and no lake element in any document of this story (DP-17).
- One request per business date under one key; a second request for the same date is a defect even when it is harmless.
- The record comes first: a request that cannot be recorded is not made, and an outcome that cannot be recorded fails the listener rather than being dropped (R-UNI-39).
- One hop, no chaining: the two activities never call a downstream of a downstream, and the breaker and bulkhead are per downstream.
- No new table, no migration and no `Schedule`: a story that adds one of them has left this slice.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the views and leaves through ACE's paths and the Workbench outbound adapters | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE; BR3, BR9, BR18 | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Every outbound file is logged, retried on a defined schedule and raised to a named owner in an exception queue | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40; BR10, BR11, BR12, BR14, BR15 | TC-E1-007-03, TC-E1-007-04, TC-E1-007-07, TC-E1-007-09, TC-E1-007-10 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; the Workbench runs no file load | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06; BR3, BR17 | TC-E1-007-01, TC-E1-007-02, TC-E1-007-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, claim-check for files | Decision log, D-RCV-60; ADR-020 | DP-11, DP-16 | All recovery processes | ADR-020; DP-01; DP-09 | TC-E1-007-01, TC-E1-007-02 |

The supporting features of this slice are FEAT-ACA-04 (role to permission matrix as data), FEAT-ACA-05 (mask PDPA fields by role) and FEAT-ACA-06 (the DoA table as reference data), which the FSD P4 module pairs with the access stories; this slice answers them only as the content of the review file and changes neither the matrix, the masking design nor the DoA design. The `-ITG` copies of the test cases and the end-to-end journey of the key are carried by RWB-ITG-E1007-ITG.

### 19. Out of scope

- The six-monthly `Schedule`, the JOB-18 workflow and the review-cycle date convention: RWB-P4-AD008-APP. This story is called by it.
- The outbound-file capability itself — the `deliverFile` and `receiveFile` activities, the builder, the MFT/SFTP transport with PGP, the retry ladder, the exception queue, the resend, the owner task and the two events: RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF and RWB-P2-E1007-OPS.
- The real cross-service journey of the outbound path with all services live: RWB-ITG-E1007-ITG.
- The document hub itself — storage, custody, WORM and retention and the claim-check read: RWB-P5-E1007-APP and the P5 document stories.
- The role, permission, masking and DoA rows as content — their load, approval, rollback and versions: RWB-P4-E1037-APP, RWB-P4-E1038-APP, RWB-P4-AD002-APP and RWB-P4-AD004-APP. This story reads them and writes no row of them.
- The access-log search and export and the break-glass grant: RWB-P4-AD007-APP and RWB-P4-AD006-APP.
- The administration screens that show the outcome and their composite route: the edge and the screen stories, RWB-PLT-N001-CON and RWB-P4-AD008-APP.
- The ACE views, the per-service logins and the grants on them: RWB-P1-E1069-DB and RWB-ITG-E1069-ITG.
- The alert rules, their thresholds and their identifiers: RWB-P2-E1007-OPS, over the alert role of the interface row.
- Inbound source ingestion, its schedules and its checks: RWB-ACE-001. There is no inbound file in this story and none is built.
- The data lake and every lake statement of the legacy key: removed by DP-17.
