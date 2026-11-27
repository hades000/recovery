# RWB-P6-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P6-E1007-APP-16) |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP08, DP09, DP10, DP11, DP16, DP17, DP19 |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-040, RD-P1-041, RD-P1-060, RD-P1-062 |
| Parallel lane | L-P6-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON (version Not specified in the source documents (DOR-RWB-P6-E1007-APP-23)); contract of this story (key Not specified in the source documents (DOR-RWB-P6-E1007-APP-21)); RWB-P1-E1015-CON, rwb-source-data.yaml 5.1.0 (API Specification v7), for the freshness read and the problem body; the addressee read is `getCustomer` (`GET /customers/{personKey}`) of rwb-source-data.yaml 5.1.0 (RD-P1-060; builder RWB-P1-E1069-APP; masking rule rows pending, NEW-GAP-D1); rwb-document contract (name and version Not specified in the source documents (GAP-1164)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-023) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The held-run rule reads `DataProductFreshness` of DP02 from `GET /data-products/freshness`: LOADED or STALE, with the never-stamped answer added as AC12 (RD-P1-005, RD-P1-041; findings #2, #3).
- The addressee read is the published `GET /customers/{personKey}` of rwb-source-data.yaml 5.1.0; the masking rule rows for the rwb-comms notice identity stay open (finding #1; RD-P1-060; NEW-GAP-D1).
- The rerun POST takes the platform idempotency answers (AC13) and every error body is the shared Problem (RD-P1-001, RD-P1-004; findings #4, #5).
- This story consumes neither AceDataReady nor AceDataLate and appends no ledger or delivery entry (RD-P1-003, RD-P1-007, RD-P1-040; findings #6, #7).
- Finishing pass: the addressee read is `getCustomer` with its masking rows pending (RD-P1-060; NEW-GAP-D1); the never-stamped wording gap and retry window follow RD-P1-062; test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for the rwb-comms producer side of the INT-14 outbound notice file. The legacy single adapter module, its `recovery_svc` identity, its in-process reads of the `recovery.v_ace_*` views, its Quartz jobs JOB-10, JOB-11, JOB-13 and JOB-15 and its two data-lake deliveries are replaced by one service with its own login, one build-and-hand-off capability against the published contract `RWB-P2-E1007-CON`, and the removal of the lake interfaces INT-19 and INT-20. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E1007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (34 resolved, 44 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the notices rwb-comms holds for a business date written into the INT-14 WIN letter file from the service's own `notice` and `template` rows, the file offered as a claim-check object and handed to rwb-integration through the published contract `RWB-P2-E1007-CON`, with the run state readable on SCR-44 and the addressee never entering `rwb_comms`**, so that **every notice leaves for WIN on one path, the transport, the retry schedule and the exception queue belong to the service that owns them, and no statement of rwb-comms reads another service's table or an ACE view**.

This document is the rwb-comms slice of legacy key RWB-E1-007. The same legacy key has the primary slice in rwb-integration (`RWB-P2-E1007-APP`, which owns `interface_config`, `outbound_item`, the SFTP transport, the retry ladder, the exception queue and the `FileDelivered` and `FileFailed` events), an infrastructure and a deployment slice of that service, and the integration story `RWB-ITG-E1007-ITG` which proves the whole journey on the real wave-1 services. This story owns only the producer side: the record set, the file, the hand-off and the run state.

The legacy story held the adapter, the five tables, the scheduler and the exception queue in one module, ran as the shared legacy service identity, read `recovery.v_ace_contact`, `recovery.v_ace_account` and `recovery.v_ace_batch_status` in process and wrote two lake files. Under D-RCV-60 the producer side is one service, one schema `rwb_comms`, one login, one task queue `rwb-comms` and no table of another owner. rwb-comms builds the record set from its own rows, writes the file behind a claim-check reference, calls the rwb-integration hand-off, publishes the existing notice event, and reads the outcome the owner announces. The lake interfaces INT-19 and INT-20 are removed and are not rebuilt here.

It serves REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008, and it serves the FSD P6 measure "notices with proof of delivery, 100 percent" by making the outbound file of the business date a single, repeatable run.

### 2. Business rationale

The Workbench loads no source data; ACE ingests every source and the Workbench only sends (D-RCV-35 U1). What remains of the legacy key on this side is the producer of one file: the WIN registered-mail notice file of the business date (INT-14, JOB-10). The legacy rationale, the four outbound interfaces and the one adapter pattern are unchanged in intent; the owner of each fact is what moved. The notice rows and the template version are rwb-comms's own; the interface row, the item, the transport, the retry intervals, the exception queue and the delivery events are rwb-integration's; the addressee and contact token is read by rwb-source-data and never stored here; the list values and the eligible notice state are reference data of rwb-case; the letter behind `notice.document_id` and the claim-check object are rwb-document's.

Three legacy statements are retired rather than restated, because no source gives them a target. The inbound file load, its checks, its run record and its sign-off are ACE ingestion (RWB-ACE-001), and P2 has no inbound adapter. The INT-19 reporting extract and the INT-20 decision-log copy are lake interfaces; DP-17 removes the lake, reporting is fed by events into rwb-reporting, and the decision ledger is fed by the shared decision-record topic. And the legacy Quartz rows are gone: JOB-10 is a file window of the bank scheduler plus the dispatch Schedule of the service, and JOB-11 is the platform outbox relay of DP-09. The removals are recorded as GAP-1163 with ASM-2110 and GAP-1165 with ASM-2112.

What the business asked for is unchanged. A notice of the business date still leaves in one file; a repeated run still adds nothing; a file that cannot be handed over is still reported with the same message; and a caller without the right is still refused with the same text. What changed is that every one of those seams is now a one-hop contract call with a 2 s budget, a breaker and a fake, so the story is buildable on Day 1 against `RWB-P2-E1007-CON` alone.

### 3. Preconditions

- RWB-P2-E1007-CON is published: the `deliverFile(manifest)` activity contract on queue `rwb-integration` with the manifest and its return element, the `rwb.integration.events.v1` AsyncAPI document with `FileDelivered` and `FileFailed`, the read that returns the INT-14 interface row in force, the error envelope and the fakes.
- The INT-14 interface configuration row is loaded by the reference data administrator (RW-REFADM) at version "IF-2026.11" with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes; it is a row of rwb-integration and is read through the contract only, never as a table (DP-01).
- The notices of the business date exist in `rwb_comms`: RWB-P6-E1052-APP generates them and RWB-P6-E1046-APP holds the template and merge-field catalog; the dispatch columns `dispatch_file_id` and `dispatch_attempts` are in `notice` (DF-LEG-033, DF-LEG-034).
- The reference-data contract of rwb-case carries the eligible state set plus LOV-NOTICE, LOV-SENT-TYPE and LOV-DELIVERY with the version in force, so no list value is written in code; that contract (RWB-P3-E1043-CON) is not in this story's contract list (GAP-1161; ASM-2108).
- The platform libraries that DP-03, DP-09, DP-10 and DP-19 add are live: the local decision-record library (RWB-PLT-E1027-CON), the outbox, inbox and idempotency library with CloudEvents (RWB-PLT-TE006-CON), the workflow kit with task queue `rwb-comms` in namespace `rwb-recovery` (RWB-PLT-E1071-CON) and the gateway-bff composite route (RWB-PLT-N001-CON). None of the four is in this story's build list, which is empty, so the story builds against their fakes until they publish (GAP-1161; ASM-2108).
- The secondary P5 slice has no legacy AC: its six criteria are new under D-RCV-60. Manifest and claim-check field names come from RWB-P2-E1007-CON; the document-hub values, including the claim-check duration and the document case key, are Not specified in the source documents (GAP-1027); the outbound document type row is loaded by the type-table load (GAP-1027).
- The recipient name and postal address of a notice are read through `GET /api/recovery/source-data/v1/customers/{personKey}` (`getCustomer`, rwb-source-data.yaml 5.1.0), by the ACE `person_key` of the party named by `notice.party_id`, under the rwb-comms notice workload identity: `firstName`, `lastName`, and the `ADDRESS` row's `contactValue`, `city`, `postCode` and `country`, chosen by `contactKey` (RD-P1-060 rules 1 and 3). "Addressee token" in this story means those values, held in memory inside the file build only. The values are clear only where `isUnmasked` is true for that identity. Pending: the masking rule rows that unmask them for the rwb-comms notice identity, owner data protection officer with the rwb-access owner, tracked as NEW-GAP-D1; interim, the `FieldMasker` fake unmasks `firstName`, `lastName` and `contactValue` for this identity only, and tests assert both the unmasked and the masked branch. The DP02 records read keeps answering contact rows without a value, name or address (RD-P1-060 rule 4).
- The freshness of the contact data is read from `GET /api/recovery/source-data/v1/data-products/freshness` (rwb-source-data.yaml 5.1.0) as the element with `productCode` "DP02", the data product that holds the contact points; the access of the rwb-comms workload identity to this operation follows NEW-GAP-S3-6.
- The claim-check object store that holds the built file, and the operation that accepts it and returns its reference, are not named in the source documents (GAP-1164; ASM-2111); the payload reference is the `payload_ref` element of the rwb-integration manifest (DF-OPS-171).
- The WIN edge in SIT is the stub of 12.8: an SFTP folder and an acknowledgment record reached by rwb-integration, with no real WIN connection and no production data.
- The service runs as its own login on schema `rwb_comms` (DP-02); it holds no grant on `recovery`, no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. The dispatch Schedule of rwb-comms starts the dispatch run for the business date at 16:00 Asia/Bangkok on task queue `rwb-comms` in namespace `rwb-recovery` (JOB-10); the bank Airflow file window opens the cross-system edge in the same window.
2. `NoticeDispatchWorkflow` starts with workflow ID `INT-14:<businessDate>` and asks the rwb-integration contract for the INT-14 interface row in force: the file pattern, the record layout and the record count rule (12.2).
3. `selectFileRecords` reads the eligible set from `rwb_comms` only: notices of the business date in the eligible state, with a resolved template version, that carry no file reference for that date; the eligible state and the lists come from the rwb-case reference-data contract with their version.
4. `renderNoticeFile` builds the INT-14 record set and its trailer from those rows and from the template version in force; where a rule decides the eligible set, the outcome is written through the local decision-record library before the record set is fixed (DP-03).
5. Before the first addressee request the run reads `GET /data-products/freshness` and takes the element of `productCode` "DP02"; when its `status` is `STALE`, or the call does not answer, no addressee is requested and the run is held (X5, X1). Otherwise the addressee and address of each record are requested through `GET /customers/{personKey}` of rwb-source-data, for the party named by `notice.party_id`, inside the build only (RD-P1-060); no name, address or contact value is stored in `rwb_comms`, put on the manifest or logged.
6. `storeNoticeFile` stores the built file behind a claim-check reference in the object store and returns that reference; the file content never travels on a message, a workflow input or a log.
7. `handoffFile` calls `deliverFile(manifest)` on queue `rwb-integration` with the interface ID `INT-14`, the business date, the idempotency key `INT-14:<businessDate>`, the claim-check payload reference, the record count, the notice IDs, the case IDs and the requesting service; one hop, 2 s timeout, one retry with jitter and a breaker.
8. The run records the item reference and its status in the answer, sets `dispatch_file_id` to that reference and increments `dispatch_attempts` on each notice it wrote, and writes `rwb.comms.NoticeDispatched.v1` to its outbox in the same transaction (DP-09).
9. rwb-integration owns everything after the hand-off: the `outbound_item` row, the SFTP transfer with PGP, the attempt ladder inside the file window, the exception queue, the owner task and the two events; the bank Airflow owns the file window and its re-run. This service never opens a session to WIN and never writes an item.
10. When rwb-integration announces `rwb.integration.FileDelivered.v1` or `rwb.integration.FileFailed.v1`, the inbox of `rwb_comms` dedupes it on the event ID and the run records the delivered or failed state with the attempt count and the last error code; no notice state changes on either event, because the acknowledgment that sets a notice Sent belongs to RWB-P6-E1055-APP.
11. A repeated run on the same business date rebuilds nothing for a notice that already carries the file reference and hands the same file over under the same idempotency key, so no second item and no second file exist.
12. The platform administrator reads the run state on SCR-44 through the gateway-bff composite route with `GET /file-runs/{businessDate}`; a data-quality break of the run is shown on SCR-45.

Screen states (DOR-RWB-P6-E1007-APP-10). SCR-44: a refused read shows MSG-P4-002 (AC8); empty, loading, error and no-access states = Not specified in the source documents (CG-ALL-6314). SCR-45: the data-quality break is shown with its count (AC5); loading shows the placeholder while the gateway-bff composite route answers; empty, error and no-access states = Not specified in the source documents (CG-ALL-6315).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | rwb-integration does not answer the hand-off inside 2 s, or its breaker is open | The run records the hand-off as not accepted, no notice changes state, nothing is retried by this service and the next run of the business date hands the same file over under the same key | MSG-GEN-006 | AC4 |
| X2 | rwb-integration reports the file in its exception queue after the last attempt | The run shows the failed state with the attempt count and the error code, and names the owner's message; the resend belongs to the owner and is not built here | MSG-P2-001 | AC4, AC8 |
| X3 | The run is repeated on the same business date | No notice is written into a second file; the file reference and the attempt count move once; the owner answers with the first item | None | AC3 |
| X4 | A notice carries a template code that resolves to no template row, or a notice type outside LOV-NOTICE | The notice is left out of the record set and counted on the run; the rest of the file is written and handed over | None | AC5 |
| X5 | `GET /data-products/freshness` answers `status` `STALE` for product DP02, with a `businessDate` or with `businessDate` null for a never-stamped product | The record set is not built from a partial answer: no addressee is requested, no file is stored, nothing is handed over, no notice changes state and the run is held; it names the product and, where the answer holds one, its `businessDate` | MSG-P1-001 | AC9, AC12, TC-E1-007-11 |
| X6 | The same `FileDelivered` or `FileFailed` event arrives twice | The inbox ignores the repeat, counts the hit and no run state moves a second time (BR13) | None | AC3 |
| X7 | A caller without the right reads or reruns a run | Refused at the edge before any read or write; nothing changes | MSG-P4-002 | AC8, TC-E1-007-10 |
| X8 | A run, a component or a statement reaches an ACE view, another `rwb_*` schema, an SFTP client or the file system | The grant refuses the statement and the architecture boundary test fails the build; nothing is released | None (pipeline log) | AC2, AC6 |
| X9 | A read names a business date with no run | The answer is 404 and no record is read | MSG-P4-003 | AC8 |
| X10 | The decision record cannot be written where a rule decided the eligible set | Nothing is written into the file and the run stops with an incident | MSG-P7-003 | AC10, BR10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-P2-E1007-CON` and its fakes; the reference data, the source-data token, the outbox library, the workflow kit and the edge route are fakes until their stories publish (GAP-1161; ASM-2108) |
| Negotiable | The file pattern, the layout, the attempts and the intervals are the owner's interface row; the object store and its operation are open; the story fixes only the producer behaviour |
| Valuable | The notice file of the business date leaves on one path, a repeated run adds nothing, and the addressee never enters this service |
| Estimable | One workflow, four activities, two read operations, three consumed contracts, one event and ten test cases |
| Small | Fits two weeks with its tests, as the secondary slice of the legacy key |
| Testable | Each criterion runs against the contract fakes with synthetic notices; the access row is a component test and the retired inbound checks are NFR rows |

### 7. Acceptance criteria

```gherkin
Feature: Integration adapters for outbound files, producer side in rwb-comms

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has direction "OUTBOUND", max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given the business date is 2026-11-30
    Given every consumed contract is the published contract of its owner and is answered by its fake
    Given the rwb-source-data contract mock answers "GET /data-products/freshness" with the element productCode "DP02" and status "LOADED", unless a scenario says otherwise

  Scenario: AC1 The record set is built from the service's own rows (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns the eligible state set "GENERATED" and the lists LOV-NOTICE, LOV-SENT-TYPE and LOV-DELIVERY at their version in force
    Given 85 notices of business date 2026-11-30 are in state "Generated" with notice type "DEMAND", template code "DEMAND-SSME" version 1 and contract "CT-77001"
    Given the rwb-integration contract mock returns the "INT-14" interface row in force and accepts the hand-off
    When the file run for interface "INT-14" and business date 2026-11-30 builds the record set
    Then the record set holds 85 notice records, one per notice of the business date in the eligible state
    Then the run writes the "INT-14" file once and offers it as a claim-check payload reference
    Then no statement of the run reads an ACE view, another schema or the interface row as a table

  Scenario: AC2 The item is created by rwb-integration and never by rwb-comms (new, D-RCV-60)
    Given the rwb-integration contract mock returns item reference "OB-0001" in status "PENDING" for interface "INT-14" and business date 2026-11-30
    Given the run has written the "INT-14" file for 2026-11-30
    When the hand-off completes
    Then the notices the run wrote carry file reference "OB-0001" and attempt count 1
    Then the boundary test finds no outbound_item table and no interface_config table in rwb_comms, and no write to rwb_integration
    Then the service holds no transport, no SFTP client and no file-system client

  Scenario: AC3 A repeated run adds no second row and no second file (new, D-RCV-60)
    Given the file run of 2026-11-30 has written 85 notices and holds item reference "OB-0001" in status "PENDING"
    Given every notice it wrote carries file reference "OB-0001"
    When the run is repeated on 2026-11-30
    Then no notice that already carries the reference is written again and the hand-off carries the same idempotency key "INT-14:2026-11-30"
    Then the owner answers with the first item "OB-0001" and no second file is written
    Then every notice still carries one file reference and the attempt count moved once

  Scenario: AC4 rwb-integration unavailable: the hand-off is queued by its owner and reported here (new, D-RCV-60)
    Given the rwb-integration contract mock does not answer inside 2 s for business date 2026-11-30 and returns no item reference
    Given 85 notices of 2026-11-30 are in state "Generated"
    When the file run hands the file over
    Then the run records the hand-off as not accepted and no notice changes state
    Then the run shows MSG-GEN-006 naming "rwb-integration" on SCR-44
    Then the next run of 2026-11-30 hands the same file over again under the same idempotency key "INT-14:2026-11-30"

  Scenario: AC5 A notice with an unknown reference is left out and counted (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns template code "DEMAND-SSME" version 1 as the version in force and no template for code "DEMAND-OLD"
    Given notice "N-0002" of 2026-11-30 carries template code "DEMAND-OLD" and resolves to no template row
    Given the other 84 notices of 2026-11-30 are in state "Generated" with a resolved template version
    When the file run builds the record set for 2026-11-30
    Then notice "N-0002" is not written into the file and is counted as not buildable
    Then the other 84 notices are written and the run completes
    Then the count is shown on SCR-44 and on SCR-45 as a data-quality break

  Scenario: AC6 The INT-19 and INT-20 path does not exist (new, D-RCV-60)
    Given the legacy key RWB-E1-007 carried the reporting extract "INT-19" and the copy "INT-20" as lake files
    When the build pipeline runs the boundary test and the interface check
    Then the service holds no lake client, no lake target and no lake delivery row
    Then no component, endpoint or job of this service writes "INT-19" or "INT-20"
    Then the reporting projection is fed by rwb.comms.NoticeDispatched.v1 on rwb.comms.events.v1, consumed by rwb-reporting

  Scenario: AC7 No addressee or contact value in the file metadata or the event (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the addressee token of party "P-0001" for notice "N-0001" and case "RC-2026-000123"
    Given the file run of 2026-11-30 writes notice "N-0001" and publishes rwb.comms.NoticeDispatched.v1
    When the file metadata, the outbox row and the log of the run are inspected
    Then the file metadata and the event carry no name, no address and no contact value
    Then rwb_comms holds no column for an addressee and no copy of a contact point
    Then the token is used inside the file build only and is not logged

  Scenario: AC8 The read of the run state (new, D-RCV-60)
    Given the file run of 2026-11-30 holds item reference "OB-0001" and the rwb-integration contract mock returns item status "ACKNOWLEDGED"
    Given a platform administrator holds the right the edge checks for the run read
    When the platform administrator reads "/file-runs/2026-11-30" through the gateway-bff composite route on SCR-44
    Then the answer holds the business date, interface "INT-14", record count 85, item reference "OB-0001", item status and attempt count
    Then a business date with no run answers 404 with MSG-P4-003
    Then a caller without the right is refused with MSG-P4-002 and nothing is read

  Scenario: AC9 A stale source answer holds the run and builds no partial record set (new, D-RCV-60)
    Given the rwb-source-data contract mock answers "GET /data-products/freshness" with the element productCode "DP02", status "STALE", businessDate "2026-11-26" and staleSince "2026-11-27"
    Given 85 notices of business date 2026-11-30 are in state "Generated"
    When the file run for interface "INT-14" and business date 2026-11-30 builds the record set
    Then the record set is not built and the run is held: no addressee is requested, no file is stored, deliverFile is not called, no notice changes state and no NoticeDispatched event is written
    Then MSG-P1-001 names the product "DP02" and the date 2026-11-26 on SCR-44

  Scenario: AC10 A decision record that cannot be written stops the run before any file is written (new, D-RCV-60)
    Given the eligible set of business date 2026-11-30 is decided by a rule
    Given the local decision-record library cannot write the decision record
    When the file run for interface "INT-14" and business date 2026-11-30 builds the record set
    Then nothing is written into the "INT-14" file and no notice changes state
    Then the run stops with an incident and shows MSG-P7-003

  Scenario: AC11 A caller without a credential or without the right is answered 401 or 403 (new, D-RCV-60)
    Given a caller without a valid credential calls the provided operations of the service
    Given a caller with a valid credential and without the right calls the same operations
    When each caller reads "/file-runs/2026-11-30" through the gateway-bff composite route
    Then the caller without a valid credential is answered 401 and no run state is read
    Then the caller without the right is answered 403 with MSG-P4-002 and no run state is read

  Scenario: AC12 A never-stamped contact data product holds the run (new, RD-P1-041)
    Given the rwb-source-data contract mock answers "GET /data-products/freshness" with the element productCode "DP02", status "STALE" and businessDate null
    Given 85 notices of business date 2026-11-30 are in state "Generated"
    When the file run for interface "INT-14" and business date 2026-11-30 builds the record set
    Then no addressee is requested, no file is stored, deliverFile is not called and no notice changes state
    Then the run is held and shows MSG-P1-001 for product "DP02" on SCR-44 with no date value invented

  Scenario: AC13 The rerun answers the platform idempotency rules (new, RD-P1-001, RD-P1-004)
    Given a platform administrator holds the right the edge checks for the rerun
    Given the file run of 2026-11-30 is recorded as not accepted
    When "POST /file-runs/2026-11-30/retry" is sent without the header "Idempotency-Key"
    Then the answer is 400 "application/problem+json" with messageCode "MSG-PLT-N009-03" and a traceId, and no run starts
    When the call is sent twice with Idempotency-Key "7f1c2a4e-9b3d-4c21-8a5e-0d6f4b2e9a11"
    Then the second call answers the stored status and body of the first and one rerun only has started
    When the same key is sent on "POST /file-runs/2026-11-29/retry"
    Then the answer is 409 with messageCode "MSG-PLT-N009-05" and nothing starts
    When the idempotency store cannot be read and the rerun is sent with a new key
    Then the answer is 503 with messageCode "MSG-PLT-N009-06" and nothing is written
```

The thirteen criteria are new work under D-RCV-60 and the RD-P1 rulings and test only the producer deliverable of this story. They assert nothing that belongs to the rwb-integration slice: the item table, the transport, the retry intervals, the exception queue, the resend and the owner task are owned by `RWB-P2-E1007-APP` and its contract. The legacy criteria AC1 to AC7 of RWB-E1-007 are owned by the P2 slice (AC1, AC2, AC3, AC5, AC6, AC7) and by `RWB-ITG-E1007-ITG` (AC4), and no legacy line is restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The INT-14 record set is built from this service's own `notice` and `template` rows for the business date; the eligible state, the list values, the file pattern and the layout are data with a version, never code | legacy BR1, BR8; INT-14; JOB-10; DP-07 |
| BR2 | The only path to WIN is the rwb-integration contract; no SFTP client, no file-system client and no direct WIN call exist in rwb-comms | legacy BR1; DP-16; REQ-DRI-006; ADR-010 |
| BR3 | `interface_config` and `outbound_item` belong to rwb-integration, and this service creates, reads and writes neither; the item reference is all the run holds | Ownership Map; legacy BR10; DP-01 |
| BR4 | The addressee and the contact value are read by rwb-source-data and never enter `rwb_comms`; they are used inside the file build as the token the owner's contract returns, are never logged and are not put on an event | legacy BR10; CTL-11; DP-05 |
| BR5 | A repeated run on one business date adds no second item and no second file, because the hand-off carries one idempotency key per interface and business date | legacy section 12, JOB-10 ("a second run adds nothing"); BR13 |
| BR6 | A downstream that fails is retried by its owner, and this service never advances a notice on a call that failed; the run reports only the state it learned | legacy BR5; R-UNI-33; DP-11 |
| BR7 | There is no data lake: the reporting extract INT-19 and the decision-log copy INT-20 are not built, and reporting is fed by events into rwb-reporting | DP-17; Architecture v5 slides 2, 37 and 44 |
| BR8 | JOB-10 is the dispatch Schedule of this service and JOB-11 is the platform outbox relay; no Quartz row and no job table entry is written | Architecture v5 slide 44; DP-10 |
| BR9 | A notice with a template code that resolves to no template row, or a notice type outside LOV-NOTICE, is left out of the file and counted; a partial record set is never handed over as complete | legacy section 5, X8; FSD P6 A2.2 AC-EXC-P6-002-02 (the held notice is not in the WIN file) |
| BR10 | The decision is never recorded after the effect: where a rule decides the eligible set, the record is written first through the local decision-record library, and a failed write stops the run | DP-03; MSG-P7-003; FSD P6 A2.2 AC-EXC-P6-002-03 |
| BR11 | A downstream system that fails is retried, and the state of the record is not advanced until the retry succeeds | legacy BR5; INT-14 error handling |
| BR12 | A retried call that passes its limit leaves the record in the exception queue with the reason, and the queue is reviewed by the owning team | legacy BR6; INT-14 error handling |
| BR13 | The same event or the same source row twice produces one effect, and the repeat is counted | legacy BR7; R-UNI-40 |

**Coverage.** BR1 AC1; BR2 and BR3 AC2; BR4 AC7; BR5 AC3; BR6 AC4; BR7 AC6; BR8 TC-E1-007-13; BR9 AC5; BR10 AC10; BR11 AC4; BR12 AC4; BR13 AC3.

### 9. State transitions

This story moves the dispatch fields of the notice and the state of its own file run. It moves no notice lifecycle state: the move to Sent is the acknowledgment of RWB-P6-E1055-APP and the move to Delivered is its proof of delivery.

| From | Event | Condition | To |
|---|---|---|---|
| Notice in the eligible state with no file reference for the date | The run writes the notice into the record set | The template version resolves and the eligible state is current | The notice keeps its state, `dispatch_file_id` is set and `dispatch_attempts` is incremented |
| Notice with a file reference for an earlier date | A later run writes it again | The notice is still in the eligible state | `dispatch_file_id` moves to the new file and `dispatch_attempts` is incremented |
| Notice with a file reference for the same date | The run is repeated on that date | The same business date | Unchanged: no second reference and no second file |
| Notice left out of the record set | The run finds no resolvable template version | The reference is unknown | Unchanged, and counted on the run as not buildable |
| Run without an item reference | `deliverFile` answers with an item reference | The hand-off is accepted | The run holds the reference and its status, and the notices carry it |
| Run without an item reference | `deliverFile` does not answer inside 2 s | The breaker is open or the call times out | The run records the hand-off as not accepted; the next run retries the same key |
| Run with an item reference | `rwb.integration.FileDelivered.v1` is consumed | The envelope names interface INT-14 and the business date | The run records the delivered state and the attempt count; no notice state changes |
| Run with an item reference | `rwb.integration.FileFailed.v1` is consumed | The envelope names interface INT-14 and the business date | The run records the failed state, the attempt count and the error code; no notice state changes |

The item status the run reports is the owner's list (`PENDING`, `SENT`, `RETRY`, `EXCEPTION`, `ACKNOWLEDGED`, LOV-OUTBOUND-STATUS of the rwb-integration interface row) and is never re-derived here. This service writes no run table (GAP-1166; ASM-2113): the run is read from the dispatch fields of its own notices, the workflow run and the status the owner returns.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity | Builds the record set, stores the file, calls the hand-off, writes the dispatch fields and the outbox row, and reads the run state; it holds no grant on another schema and no `v_ace_*` grant |
| RW-PLATADM, platform administrator | Documents R and Litigation absent (TSD P6 T6.1): reads the run state on SCR-44 and reruns the producer run of a business date |
| RW-DATASTEW, data steward | Documents R: reads the run state and receives the held-file and failed-file alerts |
| RW-LITOFF, litigation officer | Litigation CRUA: reads the notice and its file reference on the case; no right on the run operations |
| RW-AUDIT, RW-COMPLY, RW-COE | Documents R: read the run state |
| rwb-integration service identity | Answers the interface row, creates and owns the item, transports and retries the file, and announces the two events |
| rwb-case, rwb-source-data and rwb-document service identities | Serve the reference data, the addressee token and the claim-check store; they take no decision in this story |

The right on the two run operations is enforced at the edge for the screen path (DP-19); a local guard on the operation itself is not named in the source documents (GAP-1166; ASM-2113), so both operations call the rwb-access authorise check of DP-08 before any read or write; the check's operation name is Not specified in the source documents (DOR-RWB-P6-E1007-APP-6). A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6, `rwb_comms`) | id | Read |
| DF-LEG-016 | notice (P6, `rwb_comms`) | case_id | Read |
| DF-LEG-018 | notice (P6, `rwb_comms`) | notice_type | Read, against LOV-NOTICE |
| DF-LEG-019 | notice (P6, `rwb_comms`) | sent_date | Read |
| DF-LEG-020 | notice (P6, `rwb_comms`) | barcode | Read |
| DF-LEG-023 | notice (P6, `rwb_comms`) | sent_type | Read, against LOV-SENT-TYPE |
| DF-LEG-030 | notice (P6, `rwb_comms`) | party_id | Read, as the reference the addressee token is requested by |
| DF-LEG-031 | notice (P6, `rwb_comms`) | template_id | Read |
| DF-LEG-033 | notice (P6, `rwb_comms`) | dispatch_file_id | Write |
| DF-LEG-034 | notice (P6, `rwb_comms`) | dispatch_attempts | Write |
| Standard column | notice (P6, `rwb_comms`) | state | Read |
| DF-REF-045 | template (P6, `rwb_comms`) | id | Read |
| DF-REF-046 | template (P6, `rwb_comms`) | template_code | Read |
| DF-REF-047 | template (P6, `rwb_comms`) | template_version | Read |
| DF-REF-050 | template (P6, `rwb_comms`) | body_ref | Read |
| DF-REF-051 | template (P6, `rwb_comms`) | approved_by_legal | Read, as the condition of an eligible template version |
| DF-REF-065 | template (P6, `rwb_comms`) | valid_from | Read |
| DF-REF-067 | template (P6, `rwb_comms`) | notice_type | Read |
| DF-OPS-137 | interface_config (P2) | interface_id | Read through the rwb-integration contract |
| DF-OPS-141 | interface_config (P2) | file_pattern | Read through the rwb-integration contract |
| DF-OPS-143 | interface_config (P2) | max_attempts | Read through the rwb-integration contract |
| DF-OPS-144 | interface_config (P2) | retry_intervals_min | Read through the rwb-integration contract |
| DF-OPS-168 | outbound_item (P2) | id | Read through the rwb-integration contract, as the item reference |
| DF-OPS-171 | outbound_item (P2) | payload_ref | Sent in the manifest and read through the contract; never stored here |
| DF-OPS-173 | outbound_item (P2) | attempt_count | Read through the rwb-integration contract |
| DF-OPS-175 | outbound_item (P2) | status | Read through the rwb-integration contract |
| DF-OPS-176 | outbound_item (P2) | last_error | Read through the rwb-integration contract |
| DF-ACE-076, DF-ACE-077, DF-ACE-078 | v_ace_contact (read only by rwb-source-data) | contact_key, person_key, contact_value | Read through `GET /customers/{personKey}`, inside the build only and never stored (RD-P1-060) |
| DF-ACE-178, DF-ACE-179, DF-ACE-186 | v_ace_batch_status (read only by rwb-source-data) | source_system, business_date, is_complete | Not read by this service: rwb-source-data turns them into the freshness stamp, and this story reads `productCode`, `businessDate`, `status` and `staleSince` of DP02 from `GET /data-products/freshness` (X5) |

Field IDs are those of the legacy story, the Logical Data Model and Data Dictionary, the TSD P6 Communications v2 T3.1 and the TSD P2 Integration v3 T3.1. The names `recovery_svc`, `interface_run` and `interface_signoff` are legacy names of the retired path; they are not LDM v9 or Data Classification v5 entities and appear only in the change log and the retired-path checks. No new table and no new column is created: the dispatch columns `dispatch_file_id` (DF-LEG-033) and `dispatch_attempts` (DF-LEG-034) arrive with the `notice` table of RWB-P6-E1052-APP and this story writes them only. `outbox_event`, `processed_event` and `idempotency_key` are platform library objects created in `rwb_comms` (DP-09). No row of `interface_config`, `outbound_item`, `document`, `party_ext` or `contact_point_ext` is copied into `rwb_comms`, no foreign key leaves the schema, and `notice.dispatch_file_id` is an identifier and not a foreign key across schemas (DP-01).

**Personal data.** The rows this story reads carry identifiers, dates, a code and a counter; the contact fields DF-ACE-076, DF-ACE-077 and DF-ACE-078 are personal data, read through the rwb-source-data contract and never stored here. The addressee, the address and the contact value are read by rwb-source-data and used inside the file build as a token; they are never stored in `rwb_comms`, never logged, never put on the manifest beyond the claim-check reference and never put on an event. The file content is never logged, only its name, its record count and its hash.

**Open decision DL06.** DL06 is still open; this story builds on its assumptions ASM-0189, ASM-2559, ASM-2608 and ASM-2776, which the directive confirms.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/file-runs/{businessDate}` | Read the run state of the business date: interface `INT-14`, the record count, the notice count, the item reference, the item status the owner reports, the attempt count, the last error code and the delivered or failed state | Documents R, enforced at the edge (DP-19) | Not applicable |
| POST | `/file-runs/{businessDate}/retry` | Rerun the producer run of the business date: rebuild the record set and hand the same file over under the same idempotency key; it resends no item and changes no item state, because the resend of an exception item is the owner's operation | Documents U, enforced at the edge (DP-19) | `Idempotency-Key` header required (UUID, 36 characters): missing 400 MSG-PLT-N009-03; a replay answers the stored status and body for 24 hours; the key reused on another request, or while the first call is in flight, 409 MSG-PLT-N009-05; key store unavailable 503 MSG-PLT-N009-06. A new key is a new request and follows the operation's own rule: 409 with MSG-GEN-004 when the run is already accepted and the version changed; 404 with MSG-P4-003 for a business date with no run |

The two paths are this story's design on the service base, because no source names them: the TSD P6 Communications v2 appendix T-A carries no run operation and the interface monitor is SCR-44 of the operations surface (GAP-1166; ASM-2113). Errors: 401 no session (Not specified in the source documents (CG-ALL-6295)); 403 no right (MSG-P4-002); 404 unknown business date (MSG-P4-003); 409 a changed version (MSG-GEN-004); 503 a store or a consumed contract unavailable (MSG-GEN-006). Every 4xx and 5xx is `application/problem+json` with the shared `Problem` body (`type`, `title`, `status`, `messageCode` and `traceId` required; the message code named here is the `messageCode`). The response field names are fixed in the P2 contract story only for the item it returns, and the run answer is this service's own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| Temporal activity | `deliverFile(manifest)` on queue `rwb-integration` | P2 rwb-integration (RWB-P2-E1007-CON) | The only path to WIN: the manifest carries the interface ID, the business date, the idempotency key, the claim-check payload reference, the record count, the notice IDs, the case IDs and the requesting service, and the answer returns the item reference and its status |
| GET | Not specified in the source documents (GAP-1164; ASM-2111) | P2 rwb-integration | The `INT-14` interface row in force: the file pattern, the record layout and the record count rule, read through the contract and never as a table |
| GET | `/api/recovery/source-data/v1/customers/{personKey}` (`getCustomer`) | P1 rwb-source-data (rwb-source-data.yaml 5.1.0; RD-P1-060; builder RWB-P1-E1069-APP) | The recipient name and postal address of each record, for the party of `notice.party_id`, inside the file build only; 404 MSG-P4-003 for a key with no row; no `Idempotency-Key` on this GET |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1015-CON, rwb-source-data.yaml 5.1.0) | `DataProductFreshness` of `productCode` DP02: `status` `LOADED` or `STALE`, `businessDate` (null only for a never-stamped product) and `staleSince`, read before the addressee requests (X5) |
| The LOV read of the rwb-case reference-data contract | P3 rwb-case (contract not in this story's list, GAP-1161; ASM-2108) | The eligible state set, LOV-NOTICE, LOV-SENT-TYPE and LOV-DELIVERY by version, so no list value is in code |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). No row is composed into another: this service never calls a service that calls a third one, and the hand-off is the only call that leaves the service with a file.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | caseId | Fields as fixed by Kafka Catalog v1 row EV-14: barcode, noticeid, sentdate. No addressee, no address, no contact value |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | caseId | decision record reference, rule code, rule version, final call, decided at; written through the local decision-record library where a rule decides the eligible set |

No new event name is added: the file-run fact travels on the existing `NoticeDispatched` event of the service, whose envelope and field names are fixed by the service's event contract and never re-declared here. Both rows are written to the outbox in the same transaction as the dispatch-field change and relayed with the CloudEvents envelope (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler use |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The run records the delivered state, the item reference and the attempt count; no notice state changes |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The run records the failed state, the attempt count and the error code and shows MSG-P2-001; no notice state changes and no task is raised here |

Both events name the requesting service as their consumer (Architecture v5 slide 43), so this service consumes them and nothing else. Each is deduped through the inbox of schema `rwb_comms` on its event ID; a repeat produces no second effect and is counted (R-UNI-40). The hand-off request itself is an activity, not an event (Architecture v5 slide 16, "events (none: called as a task)").

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow from the kit template, one execution per interface and business date, workflow ID `INT-14:<businessDate>` | `rwb-comms` in namespace `rwb-recovery` | Owns the run: the interface row, the eligible set, the file, the hand-off, the outcome and the events |
| `selectFileRecords` | Activity | `rwb-comms` | Reads the eligible notices of the business date from `rwb_comms` and resolves their template version |
| `renderNoticeFile` | Activity | `rwb-comms` | Builds the INT-14 record set and its trailer in the layout of the interface row, with the addressee token |
| `storeNoticeFile` | Activity, calls the claim-check object store | `rwb-comms` | Stores the built file and returns its claim-check reference (GAP-1164; ASM-2111) |
| `handoffFile` | Activity calling `deliverFile` on `rwb-integration` | `rwb-integration` | One hop, 2 s timeout; returns the item reference and status, or no answer |
| `recordFileRun` | Activity | `rwb-comms` | Writes the dispatch fields of the notices, the outbox rows and the state the run reports |

The workflow is idempotent by interface and business date: a retried run writes no notice into a second file, does not rebuild a record that already carries the reference, and does not re-send an accepted file.

#### 12.6 Schedules

One Schedule starts the work of this story; it is registered by the dispatch story of the service, because the run it starts is the dispatch run.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The dispatch Schedule of rwb-comms, registered by RWB-P6-E1055-APP (RWB-PLT-E1071-CON) | 16:00 Asia/Bangkok, daily | SKIP | Catch-up window of the workflow kit | The dispatch run whose file build and hand-off are this story |

The cross-system edge of JOB-10 is the bank Airflow file window, owned by the platform and by rwb-integration (Architecture v5 slide 44, "Airflow file window + workers"). This story registers no Schedule of its own, no Quartz row, no job table entry and no Control-M job, and JOB-11 is the platform outbox relay of DP-09 (BR8).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice rows of the record set and their dispatch fields `dispatch_file_id` and `dispatch_attempts` |
| template | P6 (rwb_comms) | The template version in force behind each record, read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox, inbox and idempotency objects of the published event, the two consumed events and the retry operation (DP-09) |

Not owned and never read as a table: `interface_config` and `outbound_item` (P2), `document` (P5), `party_ext` and `contact_point_ext` (P1), `recovery_case` and `task` (P3), `decision_log_entry` (P7). No `v_ace_*` view is read here and no ACE table is read here: every ACE fact arrives through the rwb-source-data contract (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-integration contract fake (RWB-P2-E1007-CON) | The `INT-14` interface row in force with direction OUTBOUND, max attempts 3 and intervals 5, 15 and 45 minutes; `deliverFile` returning item reference `OB-0001` in status `PENDING` for 2026-11-30; `ACKNOWLEDGED` after the transfer; `EXCEPTION` with an error code after three attempts; no answer beyond 2 s; the acknowledgment record carrying sent date 30112026, barcode `RR123456789TH` and sent type `NPL` for contract `CT-77001` | AC1, AC2, AC3, AC4, AC8 |
| rwb-case reference-data fake | The eligible state set `GENERATED`; LOV-NOTICE (`DEMAND`, `RECALL`, `STATUTORY_SALE_NOTICE`, `GUARANTOR_NOTICE`), LOV-SENT-TYPE (`BEFORE_NPL`, `NPL`) and LOV-DELIVERY (`DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING`) at their version; no template for code `DEMAND-OLD` | AC1, AC5 |
| rwb-source-data addressee fake | `getCustomer` answer of party `P-0001` for notice `N-0001` on case `RC-2026-000123` (rwb-source-data.yaml 5.1.0 `Customer`), unmasked for the rwb-comms notice identity and masked for any other identity | AC7, TC-E1-007-04 |
| rwb-source-data contract fake (rwb-source-data.yaml 5.1.0) | `GET /data-products/freshness` with DP02 `LOADED`; DP02 `STALE` with `businessDate` 2026-11-26 and `staleSince` 2026-11-27; DP02 `STALE` with `businessDate` null | AC9, AC12 |
| Claim-check store stub | Accepts the built file and returns a reference; refuses once for the 503 path | AC1, AC4 |
| Kafka stub | `rwb.integration.events.v1` with one `FileDelivered`, one `FileFailed` and a duplicate of one of them | AC3, AC8 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the baseline is a build failure in the P2 contract.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The run read and the rerun on `/api/recovery/comms/v1`; the interface row on rwb-integration, the addressee token and the freshness read on rwb-source-data and the LOV read on rwb-case; one hop and 2 s each |
| Kafka | 2 published, 2 consumed | `NoticeDispatched` and `DecisionRecorded` on `rwb.comms.events.v1` and `rwb.decision-record.v1`; `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` |
| Temporal | 1 workflow, 5 activities | `NoticeFileRunWorkflow` on `rwb-comms` with the four build steps, and the hand-off activity that calls `deliverFile` on `rwb-integration` |
| File | 1 | The INT-14 outbound WIN letters file, built and stored here and delivered by rwb-integration; no lake file and no inbound file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `outboundfile`, Java package `th.co.scb.ace.workbench.recovery.comms.outboundfile`. The legacy folder `src/main/java/recovery/integration/adapter` and the legacy package `recovery.integration.adapter` are not carried over: the transport and the adapter boundary are rwb-integration's, and this service holds the producer only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | Legacy shared service login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service reads no ACE view and holds no `v_ace_*` grant, so the addressee, the address and the batch completeness arrive through the rwb-source-data contract. DP-16 applies as "the only path to WIN is `deliverFile`", and DP-17 as "no lake file, no lake copy and no lake delivery row".

**Dependencies the table adds and the plan lists do not hold.** The patterns above add six H rows and one C row: `RWB-PLT-E1027-CON` (DP-03), `RWB-PLT-E1043-CON` with `RWB-P3-E1043-CON` (DP-07), `RWB-PLT-TE006-CON` (DP-09), `RWB-PLT-E1071-CON` (DP-10) and `RWB-PLT-N001-CON` (DP-19). This story's plan lists hold `Depends on (build)` None and `Contract dependencies` `RWB-P2-E1007-CON` only, so none of them is in the metadata table. The story keeps the plan's lists as they are, builds against the contract fakes until those stories publish, and records the absence as GAP-1161 with ASM-2108.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FileRunController | Controller | The run read and the rerun on `/api/recovery/comms/v1`, with the problem mapping for 401, 403, 404, 409 and 503 |
| NoticeFileRunWorkflow | Workflow | The run of section 4: the interface row, the eligible set, the file, the hand-off, the outcome and the events |
| EligibleSetSelector | Service | The eligible notices of the business date from `rwb_comms` only, with the eligible state and the lists read as reference data |
| NoticeFileWriter | Service | The INT-14 record set and its trailer in the layout of the interface row, with the addressee token read at build time |
| ClaimCheckWriter | Client | Stores the built file behind a claim-check reference; holds no file-system path and no SFTP setting |
| IntegrationHandoffClient | Client | The `deliverFile` call on queue `rwb-integration`, one hop and 2 s, with the breaker and the retry boundary |
| FileOutcomeListener | Listener | The inbox-deduped handlers of `FileDelivered` and `FileFailed`, and the run state they record |
| NoticeDispatchedPublisher | Service | Writes the outbox row of `NoticeDispatched` in the same transaction as the dispatch-field change |
| FileRunReader | Service | The run answer from the dispatch fields, the workflow run and the status the owner reports |
| BoundaryRuleTest | Test | No SFTP client, no file-system client, no lake client and no statement outside `rwb_comms` |

**Database and migrations.** No new table and no new column. `notice`, `template`, `merge_field` and the library objects live in `rwb_comms`; the dispatch columns and their indexes arrive with the `notice` table of RWB-P6-E1052-APP, and this story adds no Flyway file of its own. `interface_config` and `outbound_item` are not created here.

**Configuration and reference data.** `rwb.comms.filerun.eligible-states` = `GENERATED`; `rwb.comms.filerun.interface-id` = `INT-14`; `rwb.comms.filerun.idempotency-prefix` = `INT-14:`. All three are reference data read with their version through the rwb-case reference-data contract and owned by the platform administrator, and none is compiled into the service. The file pattern, the layout, the attempts and the intervals are the owner's interface row and are never copied into a value file.

**Build steps**

1. Build `EligibleSetSelector` over `rwb_comms` with the reference-data read and the resolved template version; test AC1 and AC5.
2. Build `NoticeFileWriter` with the layout of the interface row, the trailer and the addressee token; test AC1 and AC7.
3. Build `ClaimCheckWriter` against the store stub and record the returned reference; test AC1.
4. Build `IntegrationHandoffClient` with the manifest, the 2 s budget, the breaker and the no-answer path; test AC2 and AC4.
5. Build `NoticeFileRunWorkflow` with workflow ID `INT-14:<businessDate>`, the idempotency rule and the repeated-run path; test AC3.
6. Build `FileOutcomeListener` with the inbox dedupe and the two run states; test AC3 and AC8.
7. Build `NoticeDispatchedPublisher` in the same transaction as the dispatch-field change, and the decision record where a rule decides; test AC3 and AC6.
8. Build `FileRunController`, the right check at the edge and the 409 and 404 paths; test AC8 and TC-E1-007-10.
9. Add the boundary test for the lake, the SFTP client, the file system and the foreign schema; test AC2 and AC6.

**Feature flag.** `rwb.comms.win-file-v1`, read as a flag of the platform library; off means no record set is built and no file is handed over.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-P2-E1007-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one file per business date, no notice in a second file of the same date, one item per file created by rwb-integration, no addressee value stored here and no lake interface of this key.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The record set is held because `GET /data-products/freshness` answers `STALE` for DP02 | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The hand-off does not answer inside 2 s, or the breaker is open, or the claim-check store is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P2-001 | rwb-integration reports the file in its exception queue after the last attempt | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-GEN-004 | A rerun names a run whose record changed | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A rerun is accepted | Saved. |
| MSG-P4-002 | A role without the right reads or reruns a run | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A read or a rerun names a business date with no run | This record was not found. |
| MSG-P7-003 | The decision record cannot be written where a rule decided the eligible set; the run stops with an incident | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-PLT-N009-03 | The rerun arrives with no `Idempotency-Key` header or with a blank value (400) | Text owned by the platform library (RWB-PLT-N009) |
| MSG-PLT-N009-05 | The same key arrives with a different request (409) | Text owned by the platform library (RWB-PLT-N009) |
| MSG-PLT-N009-06 | The `idempotency_key` store cannot be read (503) | Text owned by the platform library (RWB-PLT-N009) |

MSG-GEN-004, MSG-GEN-006, MSG-P4-002 and MSG-P4-003 are copied unchanged from the legacy story RWB-E1-007 section 14; MSG-P1-001, MSG-P2-001 and MSG-P7-003 are copied from the English text of the Error and Message Standard v4 (CG-ALL-6306, CG-ALL-6307 and DOR-RWB-P6-E1007-APP-9); no identifier is renumbered. For a never-stamped product the `businessDate` is null; the run is held, and it is run again in the next file window after AceDataReady (RD-P1-062 rule 4; the RWB-P2-E1007-APP X1 mechanism). Pending: the wording of MSG-P1-001 when `{date}` is empty, owner Error and Message Standard owner (UX content lead), tracked as NEW-GAP-D2; interim: `messageCode` MSG-P1-001 with `{product}` filled and `{date}` left empty, and tests assert the code and the product only (RD-P1-062; NEW-GAP-F13-2 closed). `MSG-P2-001` is authored by rwb-integration and is displayed on the run state here, never raised by this service, because the exception queue is the owner's.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-44 Interface and job monitor | Loading | Sees the placeholder while the gateway-bff composite route answers |
| SCR-44 Interface and job monitor | List | Sees the run of the business date with interface `INT-14`, the record count, the item reference, the item status and the attempt count |
| SCR-44 Interface and job monitor | Held | Sees the run held with MSG-P1-001 naming the product and its date |
| SCR-44 Interface and job monitor | Not accepted | Sees that rwb-integration did not accept the hand-off, with MSG-GEN-006 |
| SCR-44 Interface and job monitor | Failed | Sees the failed state with the attempt count, the last error code and MSG-P2-001 |
| SCR-44 Interface and job monitor | Rerun | Reruns the producer run, reads MSG-GEN-005 and sees no second file |
| SCR-44 Interface and job monitor | Refused | A role without the right reads MSG-P4-002 and nothing changes |
| SCR-44 Interface and job monitor | Empty | Not specified in the source documents (CG-ALL-6314) |
| SCR-44 Interface and job monitor | Error | Not specified in the source documents (CG-ALL-6314) |
| SCR-44 Interface and job monitor | No access | Not specified in the source documents (CG-ALL-6314) |
| SCR-45 Data quality | Breaks | Sees the notices left out of the record set and counted, and the held run of the business date |
| SCR-45 Data quality | Loading | Sees the placeholder while the gateway-bff composite route answers |
| SCR-45 Data quality | Empty | Not specified in the source documents (CG-ALL-6315) |
| SCR-45 Data quality | Error | Not specified in the source documents (CG-ALL-6315) |
| SCR-45 Data quality | No access | Not specified in the source documents (CG-ALL-6315) |

Both screens are reached through the gateway-bff composite route at the edge and read this service once per operation (DP-19); the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON, and the full interface and job monitor of the programme belongs to the platform and operations stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-10 | AC8 | Component | RW-CASEOWN calls `POST /file-runs/2026-11-30/retry`; refused with MSG-P4-002 |
| TC-E1-007-01 | AC1, AC6 | End to end | 85 notices of 2026-11-30; one `INT-14` interface row with direction OUTBOUND; the boundary test for the lake, the inbound path and the SFTP client |
| TC-E1-007-02 | AC2 | End to end | 85 notices with party `P-0001`; the source-data addressee token; the file metadata and the outbox row |
| TC-E1-007-03 | AC3, AC4 | End to end | The file of 2026-11-30 handed over once with item `OB-0001` and once with no answer inside 2 s |
| TC-E1-007-04 | AC4 | End to end | The hand-off of 2026-11-30 with no item reference; the stale marker of the business date; the next run under the same idempotency key |
| TC-E1-007-11 | AC9 | End to end | DP02 `STALE` with `businessDate` 2026-11-26 on the freshness answer; the run is held, no partial record set is built and MSG-P1-001 names DP02 and the date. TC: changed row to be restated in Test Cases v9 (W2-tests) |
| TC-P6-E1007-APP-01 | AC12 | End to end | DP02 `STALE` with `businessDate` null; the run is held and nothing is handed over |
| TC-P6-E1007-APP-02 | AC13 | Component | The rerun with no key, a replayed key, a reused key and the key store unavailable |
| TC-E1-007-12 | AC10 | Component | The decision record cannot be written; nothing is written into the file and the run stops with an incident |
| TC-E1-007-13 | BR8 | NFR | No Quartz row and no job table entry is written by this service; JOB-10 and JOB-11 are the only jobs named |
| TC-E1-007-07 | AC7 | End to end | The file of 2026-11-30 handed over twice with one idempotency key |
| TC-E1-007-08 | AC2, AC3 | End to end | One business date, two hand-off attempts, one item reference |
| TC-E1-007-09 | AC4, AC8 | End to end | Item `OB-0001` reported in status `EXCEPTION` by the contract; the run read of 2026-11-30 |
| TC-E1-007-05 | None (retired with the inbound file load; the behaviour is ACE ingestion and EV-27 AceDataLate, raised by rwb-source-data once per source system and business date at 05:30 and not consumed here) | NFR | The legacy inbound case "file missing at the cut-off"; asserts that no inbound adapter, folder listing, DQ-057 or DQ-059 check or interface_run row exists here; closed when the ACE ingestion story publishes its own checks |
| TC-E1-007-06 | None (retired with the inbound file load; the behaviour is ACE ingestion and EV-27 AceDataLate, raised by rwb-source-data once per source system and business date at 05:30 and not consumed here) | NFR | The legacy inbound case "same file delivered twice"; asserts that no inbound adapter, folder listing, DQ-057 or DQ-059 check or interface_run row exists here; closed when the ACE ingestion story publishes its own checks |
| TC-E1-007-16 | AC5 | Component | The AC5 criterion of section 7 with its Given, When and Then in Recovery Workbench Test Cases v9.xlsx, tab Story test cases |
| TC-E1-007-17 | Section 12 operations, events and activities | Component | Contract test of each operation, event and activity of section 12 against its published contract; the consumed rows of section 12.2 are checked against the owner's contract |
| TC-E1-007-18 | Section 12.7 tables | Component | Boundary test of the tables owned in section 12.7 |
| TC-E1-007-14 | AC5 | Component | One notice of 2026-11-30 whose template code resolves to no template row; the other notices with a resolved template version; the count on SCR-44 and SCR-45 |
| TC-E1-007-15 | AC11 | Component | A caller without a credential and a caller without the right call `/file-runs/2026-11-30`; 401 and 403 are answered and MSG-P4-002 is shown on 403; no run state is read |

The ten legacy identifiers are kept in the order of the source list. Legacy levels map System to End to end, Access to Component and Resilience to NFR. `TC-E1-007-05` and `TC-E1-007-06` are the retired inbound-load cases: their behaviour is ACE ingestion, the ACE batch record and the EV-27 `AceDataLate` alert, so they run as NFR checks on the retired path and assert only that no inbound adapter, no inbound folder, no file check of DQ-057 or DQ-059 and no `interface_run` row exists here (GAP-1165; ASM-2112). The real cross-service journey of the file is proven by `RWB-ITG-E1007-ITG`, and the item, transport, retry and resend cases are run by `RWB-P2-E1007-APP`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the eligible state, the interface ID, the file pattern, the layout, the attempts, the intervals and the list values are data with a version; no role, list value, state name or count appears in Java.
- No personal data in events, logs, workflow inputs or tests: the addressee, the address and the contact value never enter `rwb_comms` and are never logged; file content is never logged, only its name, its record count and its hash.
- ACE data only through the owner's contract: the addressee and the batch completeness arrive through rwb-source-data, and this service holds no `v_ace_*` grant and no grant on the `recovery` schema (DP-05).
- No read of another service's tables and no cross-schema join: `interface_config`, `outbound_item`, `document`, `party_ext` and `contact_point_ext` are reached only through their owners' contracts (DP-01).
- Files move only through rwb-integration: no component opens an SFTP session, reads a folder or calls WIN, and the boundary test fails the build on any such call (DP-16, REQ-DRI-006).
- No data lake and no lake delivery row: INT-19 and INT-20 have no target, and no adapter of this key writes them (DP-17).
- One hop and a 2 s budget per consumed call, with one GET retry with jitter and a breaker per downstream; no call chain.
- Every published event is written to the outbox in the same transaction as the dispatch-field change and carries IDs and facts only; every consumed event is deduped through the inbox (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read through ACE's paths and files leave only through rwb-integration | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE; BR2, BR4 | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Log every outbound file, retry on a defined schedule, exception queue with a task for a named owner | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-40; BR5, BR6 | TC-E1-007-01, TC-E1-007-03, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; no file load is run | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06; BR4, BR9 | TC-E1-007-01, TC-E1-007-04 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-007 | The producer side of the outbound file only; the item, the transport, the retry and the exception queue are `RWB-P2-E1007-APP`'s, and the journey is `RWB-ITG-E1007-ITG`'s |
| Primary slice RWB-P2-E1007-APP | `interface_config`, `outbound_item`, the SFTP transport with PGP, the retry intervals, the exception queue, the owner task and the two events |
| RWB-P2-E1007-CON | The hand-off activity and its manifest, the two events, the interface-row read and the fakes this story builds against |
| RWB-ACE-001 and the retired inbound load | The inbound adapters, the folder listing, the checks DQ-057 and DQ-059, the missing-file run row, JOB-09, `interface_run` and `interface_signoff` |
| RWB-P1-E1055-APP and RWB-P1-E1015-CON | The freshness of the data products read here (RWB-P1-E1015-CON). The proof-of-delivery read (RWB-P1-E1055-APP) writes nothing and is not used by this story: delivery entries are appended to the interaction ledger over REST by rwb-comms in `RWB-P6-E1055-APP` (RD-P1-007) |
| RWB-E1-056 and the job monitor | The run books, the alerts and the full SCR-44 interface and job monitor of the programme |
| Schedules and shared tables | JOB-10 as the file window and the service's dispatch Schedule, JOB-11 as the platform relay, and no shared Quartz table (DP-10) |
| DP-17 removal | INT-19 and INT-20 are removed with the lake; reporting is fed by events into rwb-reporting and the ledger by the decision-record topic |
| DP-01, DP-02, DP-05, DP-16 | `rwb_comms` and its login, no other schema and no ACE view, and rwb-integration as the only path to WIN |
| DP-03, DP-07, DP-09, DP-10, DP-11, DP-19 | The decision record, the reference data, the outbox and inbox, the workflow kit, the one-hop budget and the edge route |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-018, ADR-020 | 19 services, schema and login per service, Kafka with outbox and CloudEvents, the reusable Temporal layer, no data lake, and contract-first REST with one hop |

### 19. Out of scope

- The item, the transport, the retry schedule, the exception queue, the owner task, the resend and the two events: `RWB-P2-E1007-APP` and `RWB-P2-E1007-CON`; the MFT/SFTP endpoints, the PGP keys, the firewall and the staging area: `RWB-P2-E1007-INF`.
- The real cross-service journey of the file with all services live: `RWB-ITG-E1007-ITG`.
- The inbound source ingestion, its schedules, its checks and the ACE team sign-off, which replace the retired inbound load of this legacy key: RWB-ACE-001.
- The record-level checks, the reconciliation and the stale marker of the data products: RWB-P1-E1011-APP and RWB-P1-E1015-CON.
- The dispatch run itself, the WIN acknowledgment, the sent fields and the proof of delivery: `RWB-P6-E1055-APP` and its contract; notice generation and the template catalog: RWB-P6-E1052-APP and RWB-P6-E1046-APP.
- The run books, the alerts and the full SCR-44 interface and job monitor: RWB-E1-056 and the platform and operations stories.
- The Scheduled jobs and the shared tables they used: JOB-10 is the file window and the service's dispatch Schedule, JOB-11 is the platform relay, and no Quartz row or job table entry is written.
- The data lake: the reporting extract INT-19 and the decision-log copy INT-20 are removed and are not rebuilt; reporting comes from events into rwb-reporting and the decision ledger from the shared decision-record topic.
- The stored letter, the claim-check store's own retention and custody: rwb-document (P5) and its stories; this story follows the contract reference only.

### 20. Remaining delivery steps

- Add the masking rule rows that unmask the recipient name and postal address for the rwb-comms notice identity (NEW-GAP-D1; data protection officer with the rwb-access owner), and build `getCustomer` and its fake (RWB-P1-E1069-APP).
- Publish the rwb-source-data 5.1.0 provider fake and the rwb-comms workload identity grant on the freshness read (NEW-GAP-S3-6; rwb-source-data service owner and solution architect).
- Give the MSG-P1-001 wording for a never-stamped product (NEW-GAP-D2; Error and Message Standard owner).
- Add the changed and new test cases in Test Cases v9 (test lead).
- Publish the consumed contracts and fakes with fixed versions (owning service owners).
- Set the size and sign off the epic design (squad and architect).
- Load the synthetic test data in DEV (squad).
