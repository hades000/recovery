SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P2 rwb-integration
description: Product requirements for the Integration service rwb-integration (P2) of the Recovery Workbench under D-RCV-60 - the one outbound-file capability, the freshness hold, the retry ladder and exception queue with its owner task and resend, duplicate-event handling, the outbound interface register and the EFS hand-over intake.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx
version: 1
date: 22 November 2026
decision: D-RCV-60
service: P2 rwb-integration
service_epic: RWB-SVC-P2
wave: 1
---

# Recovery Workbench PRD P2 rwb-integration

## 1. Document control and change log

### 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P2 rwb-integration |
| Document ID | P2-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | rwb-integration (P2, Integration, wave 1) |
| Service epic | RWB-SVC-P2 |
| Realignment decision | D-RCV-60 |
| Business baseline | Recovery Workbench Business Requirements Program v4 (15 November 2026), section 5.2 and section 6 |
| Business baseline, epic detail | Recovery Workbench Business Requirements Epic 1 v4 (15 November 2026), section 3.2 |
| Functional baseline | Recovery Workbench FSD P2 Integration v3 (15 November 2026) |
| Architecture baseline | Recovery Workbench Architecture v5 Text Extract v1; Temporal and Drools Design Text Extract v1; Ownership Map v1; Story Template and Rules v1 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Tool and model | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | PRD Builder, AI-SDLC playbook |

### 1.2 Trace metadata

| Item | Value |
|---|---|
| Run | D-RCV-60 microservice realignment, folder 22 |
| Work package | B-REQ-PRD-P2 |
| Upstream artifacts | BRD Program v4; BRD Epic 1 v4; FSD P2 Integration v3; Arch v5 Text Extract v1; Ownership Map v1 (ASM-2662) |
| Upstream ID sets | REQ-DRI-006, REQ-DRI-007, REQ-DRI-008, REQ-DRI-013; NFR-008, NFR-011, NFR-014, NFR-015, NFR-020, NFR-021, NFR-025, NFR-026, NFR-030, NFR-039, NFR-040, NFR-041, NFR-042, NFR-045, NFR-046, NFR-047, NFR-052, NFR-053, NFR-064, NFR-067, NFR-068; FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-10, FEAT-DRI-11, FEAT-DRI-13; RWB-E1-007 |
| Generated ID sets | CAP-P2-001 to CAP-P2-008; FR-P2-001 to FR-P2-022; NFR-P2-001 to NFR-P2-013; AC-P2-001 to AC-P2-014; Q-P2-01 to Q-P2-07 |
| Source artifact | 03 Requirements and specifications/Recovery Workbench FSD P2 Integration v3 (extract: _work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P2 Integration v3.md) |
| Status | Draft; approval gate open |

### 1.3 Change log

| Version | Date | Change | Decision | Tool |
|---|---|---|---|---|
| 1 | 22 November 2026 | First version. The service PRD is derived from BRD Program v4 section 5.2 and section 6, BRD Epic 1 v4 section 3.2 and FSD P2 Integration v3 under D-RCV-60. The module becomes the service rwb-integration with its own schema, login, REST base, topic, task queue and two events. The data lake extracts INT-19 and INT-20 leave the baseline, the inbound file adapters stay removed, the WIN file, the debt buyer tape and the reporting delivery keep one pattern, and the EFS hand-over intake is added as the wave-2 capability. | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

Change-log row: 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1.4 Requirement ID conventions

| Prefix | Meaning | Example |
|---|---|---|
| CAP-P2-nnn | Product capability of the service | CAP-P2-001 |
| FR-P2-nnn | Functional requirement; mapped to the FSD requirement IDs | FR-P2-001 |
| NFR-P2-nnn | Non-functional requirement; mapped to the BRD NFR IDs | NFR-P2-001 |
| AC-P2-nnn | Acceptance criterion in Gherkin, mapped to FR and NFR | AC-P2-001 |
| Q-P2-nn | Open question | Q-P2-01 |
| BR IDs | Business requirement IDs of the BRD, copied unchanged | REQ-DRI-007 |
| CG and ASM | Candidate gap and assumption rows of this work package, numbered later as GAP-nnnn and ASM-nnnn | GAP-1534 |

No BRD requirement is renumbered (ASM-2677). There is no predecessor PRD in this family, so this file is version 1 (ASM-2676).

## 2. Product overview and relationship to ACE

### 2.1 What the service is

rwb-integration is the outbound integration capability of the Recovery Workbench. It sends: the WIN registered-mail notice file (INT-14), the debt buyer data tape (INT-25) and the reporting delivery that legacy INT-19 described, and it provides the delivery capability that any later outbound interface of the Workbench calls. It loads nothing. Every inbound source lands in ACE through ACE ingestion and is read through the views by rwb-source-data alone (D-RCV-35 U1; ADR-010; GAP-1535; ASM-2664).

The product value is one property the business asked for and nothing else: a file that must leave the bank leaves it on the day and in the window it must, and a file that does not leave is found on the day it fails and reaches a named owner who can resend it. The FSD measure is unchanged: zero outbound items in the exception queue over one day (FSD P2 v3 A2.1.1).

### 2.2 What is new under D-RCV-60

| New | Detail |
|---|---|
| One service, one boundary | The module becomes rwb-integration with schema `rwb_integration`, its own ACE database login, REST base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, task queue `rwb-integration` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.integration` |
| Two published events | `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1`, keyed by case ID, no numbered EV ID in the sources (ASM-2667) |
| A delivery capability instead of a table write | A requesting service asks for a file through the service's delivery contract; it never writes the service's tables (Arch v5 slide 16, called as a task) |
| Ownership of three tables | `interface_config`, `outbound_item` and the job catalog read; the outbox, inbox, idempotency and local decision-record objects are platform library objects created in the service schema |
| A named owner task on failure | The route state and the owner task are raised in rwb-case through its contract; the service writes no case row and no task row |
| The EFS hand-over intake | A wave-2 orchestration step that starts only when the ACE batch for EFS is complete (ASM-2678) |

### 2.3 What is reused from ACE and from the platform

| Reused capability | Owner | Effect on this PRD |
|---|---|---|
| Sign-in, access check, audit and PII logging, and the SOC path (INT-22) | ACE common module | No product requirement; the resend is written to the ACE audit log with the user and the time |
| Notification path NSS (INT-17) and LINE OA (INT-18) | ACE common module | No P2 build and no P2 requirement (ASM-2674) |
| Read-only ACE access through thirty `recovery.v_ace_*` views | P1 rwb-source-data | Every ACE fact the service needs is one hop away through that contract (ASM-2664) |
| Document store and claim-check link | P5 rwb-document | File bytes live in the document hub; the service carries the manifest and the link, never the content |
| Case, route state, queue and task | P3 rwb-case | The retry and exception route states and the owner task are raised through that contract |
| Right check, scope and masking policy | P4 rwb-access | The platform administrator right on the exception queue read and on the resend |
| Central decision ledger | P7 rwb-decision | The shared `DecisionRecorded` event is published by the local decision-record library |
| Service template, outbox and inbox library, workflow kit, Kafka platform, gateway route, observability | Platform epics RWB-PLT | The service narrows the platform rules and redefines none of them |
| Inbound source ingestion of every source system | ACE ingestion | No inbound adapter, no inbound folder, no inbound file check, no inbound run record and no sign-off in the Workbench |

### 2.4 Confirmed constraints from Architecture v5

| Constraint | Source |
|---|---|
| Schema `rwb_integration`; own login; no grant on `recovery` and no grant on another `rwb_*` schema | Arch v5 slides 29 and 41; DP-01, DP-02, DP-05 |
| REST base `/api/recovery/integration/v1` behind gateway-bff; one hop, 2 s timeout | Arch v5 slides 8, 11 and 41; ADR-020; DP-11, DP-13 |
| Topic `rwb.integration.events.v1` with retry topics and `.dlt`; CloudEvents 1.0; outbox and inbox | Arch v5 slides 9, 11, 41 and 43; ADR-015; DP-09, DP-14 |
| Task queue `rwb-integration`; activity steps; no Temporal Schedule of this service | Arch v5 slides 16 and 44; ADR-016; DP-10 |
| No data lake and no Power BI connection | Arch v5 slides 7, 8, 13 and 37; ADR-018; DP-17 |
| Two party file interfaces only (INT-14 over MFT or SFTP; INT-25 per lot, encrypted) | Arch v5 slides 8, 16 and 32 |

### 2.5 Exclusions of this PRD

| Excluded | Reason and later home |
|---|---|
| Every inbound source load: ALS, SCBPDM, EFS, COLLINS scores, LIT, CCMS, SVAF, AMIS, RPS, WIN proof of delivery, GL postings, NLEADS, EasyApp and Entra ID | Removed by D-RCV-35 U1; later home ACE ingestion (FSD P2 v3 A1.6; ASM-2671) |
| Inbound file checks DQ-057 and DQ-059, the missing-file check of JOB-09 and the inbound run record and sign-off | Removed functions, kept as IDs only, no FR and no AC (GAP-1542; ASM-2671) |
| The data lake, the Power BI extract and the COLLINS feed through the lake | Removed by Architecture v5 (GAP-1534; ASM-2663) |
| The GL write-off posting as a Workbench file | The approved write-off is an event and the posted result is read back through the ACE view; posting files belong to rwb-payment |
| The transport of the partner portal and the document hub | Owned by S9 rwb-partner and P5 rwb-document (GAP-1547; ASM-2675) |
| The consumer-side compositions of later waves (ACE plan status, composed case list, credit pack, queue write interface, ALS settlement posting) | Requirements belong to the owning module PRDs (GAP-1541; ASM-2670; Q-P2-06) |
| Solution design: class names, table columns, endpoint signatures, deployment topology | Out of scope of a PRD; the story set and the technical specification carry it |

## 3. Personas and roles

Roles only; no person is named anywhere.

| Role | Who | What they need from this service |
|---|---|---|
| Platform administrator (RW-PLATADM) | Operations, platform team | See an item or a delivery in the exception queue, resend it, and know that the resend is audited |
| Operations engineer | DevOps and support | A run book entry and an alert for every interface, with an owner and an escalation path |
| Data steward and data product owner | Data office | Know that a held file is held because the ACE batch is not complete, with the business date and the source |
| Case owner | Recovery operations | The case does not sit in a state nobody notices: a failed file moves the route state and raises a task to the owning role |
| Requesting service owner (rwb-comms, rwb-debtsale, rwb-reporting, rwb-payment) | TechX | One way to ask for a file, one manifest, one outcome event |
| Reference data administrator (RW-REFADM) | Operations | Load an interface row and know that an inbound row is refused |
| Compliance and internal audit | Second and third line | Prove what left the bank, when, for which case, and who resent what |
| Tech lead of rwb-integration | TechX | A stable contract for the service and its two events |

## 4. User journeys

### 4.1 The WIN registered-mail notice file (INT-14), today and in the target

| Step | Today (monolith) | Target (rwb-integration) |
|---|---|---|
| 1 | The notice module builds the file in process and reads the notice table, the person and the address from the recovery schema | rwb-comms asks for the file and answers the notice facts; the addressee and the address are read one hop away through the rwb-source-data contract |
| 2 | The scheduler in the module starts the build | The bank scheduler opens the 16:00 window; the owning service starts the step; the service builds and delivers |
| 3 | A failure is written to a table and found late | A failed attempt moves the item to RETRY, then to EXCEPTION with `FileFailed` and one task to the platform administrator role |
| 4 | A resend is made by hand | The platform administrator resends the item and the event and the audit record are written |

### 4.2 The debt buyer data tape (INT-25), today and in the target

| Step | Today (monolith) | Target (rwb-integration) |
|---|---|---|
| 1 | The tape is built from the debt sale tables and the account tables in one schema | rwb-debtsale raises the delivery request with the account keys and the sale terms in the manifest |
| 2 | Account facts are read in process | The account facts are read one hop away through the rwb-source-data contract |
| 3 | The tape is sent over SFTP with no acknowledgement trail | The tape is encrypted and sent over the agreed transport, acknowledged, retried and, on failure, raised to the exception queue |

### 4.3 The reporting delivery (legacy INT-19), today and in the target

| Step | Today (FSD v3) | Target (Architecture v5) |
|---|---|---|
| 1 | The module builds a nightly extract and writes it to the data lake for Power BI | rwb-reporting builds its extract from its own projections and asks the service to deliver it; no lake file exists (ASM-2663) |
| 2 | A failure holds the publish and alerts | A failure holds the delivery, alerts the named owner and is retried in the next window |

### 4.4 A duplicate event, and a held morning

| Step | What happens |
|---|---|
| 1 | An event arrives whose key the consumer has already processed, including `AceDataReady` for a source and business date |
| 2 | The consumer does not act a second time, the hit count for the key increases, and the duplicate is visible to operations |
| 3 | If the ACE batch of the business date is not complete, no outbound item is created at all: the request is held with the stale-data message and the data steward is alerted |

### 4.5 The EFS hand-over intake (wave 2)

| Step | What happens |
|---|---|
| 1 | The ACE batch for EFS and the business date is complete, and the readiness is announced once |
| 2 | The hand-over step takes its per-account key before it asks for the case, asks rwb-case, then appends to the ledger idempotently |
| 3 | A repeat of the same morning is provable: the step does not create a second run, and a partial morning is visible as such |

## 5. Capabilities and features

Every capability is Must: each traces to a BRD requirement whose priority is Must, and the PRD does not lower a priority the BRD sets.

| CAP | Capability | BR IDs | MoSCoW | Wave | FRs | FSD feature |
|---|---|---|---|---|---|---|
| CAP-P2-001 | One outbound-file pattern: a requesting service asks, the service builds, stores, sends, acknowledges and announces | REQ-DRI-006, REQ-DRI-007 | Must | 1 | FR-P2-001, FR-P2-002, FR-P2-003, FR-P2-012, FR-P2-022 | FEAT-RDF-21, FEAT-DRI-11 |
| CAP-P2-002 | The WIN registered-mail notice file (INT-14) | REQ-DRI-006, REQ-DRI-007 | Must | 1 | FR-P2-002, FR-P2-003 | FEAT-RDF-21, FEAT-DRI-10 |
| CAP-P2-003 | The debt buyer data tape (INT-25), encrypted and per awarded lot | REQ-DRI-006, REQ-DRI-007 | Must | 1 builds, 3 first use | FR-P2-004 | FEAT-DRI-10 |
| CAP-P2-004 | The reporting delivery that replaces the data lake extract (legacy INT-19) | REQ-DRI-006, REQ-DRI-007 | Must | 1 | FR-P2-005 | FEAT-RDF-21 |
| CAP-P2-005 | The item lifecycle: freshness hold, retry ladder, exception queue, owner task, resend, audit record | REQ-DRI-007 | Must | 1 | FR-P2-006, FR-P2-007, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-017, FR-P2-020 | FEAT-RDF-23, FEAT-RDF-24 |
| CAP-P2-006 | Duplicate-event detection and ignore, including the ACE readiness event | REQ-DRI-007, REQ-DRI-008 | Must | 1 | FR-P2-013, FR-P2-014 | FEAT-DRI-13 |
| CAP-P2-007 | The outbound interface register as data, and the administrator reads of items, deliveries, jobs and the interface register | REQ-DRI-007 | Must | 1 | FR-P2-011, FR-P2-015, FR-P2-016, FR-P2-021 | FEAT-RDF-21, FEAT-DRI-10 |
| CAP-P2-008 | The EFS hand-over intake: one run per business date, started by the ACE readiness, idempotent on repeat | REQ-DRI-013 | Must | 2 | FR-P2-019 | FSD P2 v3 Requirements served |

### 5.1 Capabilities carried out of scope, with their source

| Removed or non-capability | Source and disposition |
|---|---|
| FEAT-DRI-09 file adapters for CCMS, SVAF, AMIS, RPS, WIN and GL | Removed by D-RCV-35; later home ACE ingestion; no CAP and no FR (ASM-2671) |
| Inbound half of FEAT-RDF-21 and of FEAT-DRI-10, FileLoadAdapter and the inbound folders | Removed by D-RCV-35; later home ACE ingestion |
| The data lake extract and the COLLINS feed through the lake (INT-19, INT-20) | Removed by Architecture v5; INT-19 is delivered to rwb-reporting and INT-20 is continuous ingest in rwb-decision (ASM-2663) |
| The interaction ledger and the case content of the service | Owned by P1, P3 and P7; this service orchestrates and delivers |

## 6. Functional requirements

Every requirement is specific and testable. The FSD column names the requirement ID of the functional specification it serves; the BR column names the business requirement it traces to.

| ID | Requirement | CAP | BR (BRD) | FSD source | Priority |
|---|---|---|---|---|---|
| FR-P2-001 | The service SHALL deliver an outbound file only on a delivery request raised by the owning service, carrying the interface, the business date, the case IDs, the record count, the file hash, the idempotency key and the claim-check link; it SHALL return the item reference and the item status and SHALL announce the outcome as `FileDelivered` or `FileFailed`. | CAP-P2-001 | REQ-DRI-006 | FSD P2 v3 A2.1, A2.6 | Must |
| FR-P2-002 | The service SHALL build the WIN registered-mail notice file (INT-14) from the notice facts of rwb-comms and the addressee and address read one hop away through the rwb-source-data contract by person key and contact key; it SHALL NOT read a notice table, an ACE view or an ACE table itself. | CAP-P2-001, CAP-P2-002 | REQ-DRI-006 | FSD P2 v3 A1.5, A2.1, AC-ALT-P2-001-03 | Must |
| FR-P2-003 | The service SHALL send the WIN file in the 16:00 daily window opened by the bank scheduler, on the request of the owning service and under that service's job (JOB-10, owner rwb-comms); the service SHALL register no schedule of its own (GAP-1536; ASM-2665). | CAP-P2-002 | REQ-DRI-007 | FSD P2 v3 A1.5; Arch v5 slide 44 | Must |
| FR-P2-004 | The service SHALL build the debt buyer data tape (INT-25) from the account keys and sale terms of the request manifest raised by rwb-debtsale, read the account facts through the rwb-source-data contract, encrypt the file and send it over the agreed transport, and acknowledge or raise it to the exception queue (GAP-1539; ASM-2668). | CAP-P2-003 | REQ-DRI-006 | FSD P2 v3 A1.5, A2.5 | Must |
| FR-P2-005 | The service SHALL deliver the reporting extract of rwb-reporting as a delivery request on the same pattern and SHALL produce no data lake file, no Power BI feed and no lake delivery row. | CAP-P2-004 | REQ-DRI-007 | FSD P2 v3 A1.5 (INT-19); Arch v5 slides 37, 44; DP-17 | Must |
| FR-P2-006 | The service SHALL record every outbound item with its interface, business date, case IDs, attempt count, next attempt time, last error, owner role and status, and SHALL expose the status list PENDING, SENT, RETRY, EXCEPTION and ACKNOWLEDGED, and for a delivery PENDING, RETRYING, DELIVERED and EXCEPTION. | CAP-P2-005 | REQ-DRI-007 | FSD P2 v3 A2.1.2, A1.5 | Must |
| FR-P2-007 | The service SHALL hold a delivery request and create no outbound item when the ACE batch for the business date of the file is not complete, SHALL show the stale-data message MSG-P1-001 with the product and the date, and SHALL make the hold visible to the data steward and the owner role. | CAP-P2-005 | REQ-DRI-008 | FSD P2 v3 VR-P2-001-1, A1.4, A2.1.3.1 | Must |
| FR-P2-008 | The service SHALL retry a failed attempt on the intervals held in the interface configuration row of the interface, up to the maximum number of attempts in that row, and SHALL hold neither attempt count nor interval in code (GAP-1540; ASM-2669). | CAP-P2-005 | REQ-DRI-007 | FSD P2 v3 A2.2, AC-EXC-P2-001-01 | Must |
| FR-P2-009 | After the last allowed attempt the service SHALL move the item to EXCEPTION, publish `FileFailed`, show the item in the exception queue with MSG-P2-001, and raise exactly one task to the owning role through the rwb-case contract; it SHALL write no case row and no task row (GAP-1537; ASM-2666). | CAP-P2-005 | REQ-DRI-007 | FSD P2 v3 A2.3, AC-EXC-P2-001-01, R-UNI-34 | Must |
| FR-P2-010 | A platform administrator SHALL be able to resend an item or a delivery that is in EXCEPTION; the status returns to PENDING with attempt count zero, the resend is written to the ACE audit log with the user and the time, and the response carries MSG-GEN-005. A resend of a record that is not in EXCEPTION SHALL be refused and SHALL change nothing. | CAP-P2-005 | REQ-DRI-007 | FSD P2 v3 AC-EXC-P2-001-04 | Must |
| FR-P2-011 | A platform administrator SHALL be able to list outbound items and deliveries by interface, status, consumer and date range, read only, and SHALL see one record per item with its status and its attempt history. | CAP-P2-007 | REQ-DRI-007 | FSD P2 v3 A1.5; Ownership Map API rows owned by P2 | Must |
| FR-P2-012 | The service SHALL publish `rwb.integration.FileDelivered.v1` on acknowledgement and `rwb.integration.FileFailed.v1` on exception, keyed by case ID, with identifiers, codes, counts and hashes only and with no personal data and no file content (GAP-1538; ASM-2667). | CAP-P2-001, CAP-P2-005 | REQ-DRI-007 | Arch v5 slide 43; FSD P2 v3 A2.1.2 | Must |
| FR-P2-013 | The service SHALL recognise a consumed event whose key it has already processed, SHALL not act a second time, SHALL count the repeat against that key, and SHALL keep the repeat visible to operations. | CAP-P2-006 | REQ-DRI-007 | FSD P2 v3 A2.7, AC-EXC-P2-001-03, R-UNI-40 | Must |
| FR-P2-014 | The service SHALL consume the ACE readiness event of rwb-source-data once per source and business date and SHALL not start a second run for the same source and business date when the event repeats. | CAP-P2-006 | REQ-DRI-008 | FSD P2 v3 A2.7, AC-EXC-P2-007-07, EV-26 | Must |
| FR-P2-015 | The service SHALL hold every outbound interface as a versioned configuration row carrying direction, transport, file pattern, data product, maximum attempts, retry intervals, owner role, alert role and validity dates, and SHALL refuse a row whose direction is inbound. | CAP-P2-007 | REQ-DRI-007 | FSD P2 v3 A1.5, BR-P2-001; D-RCV-35 U1 | Must |
| FR-P2-016 | The service SHALL provide no inbound adapter: no file is picked up, checked, run-recorded or signed off, and no interface configuration row has an inbound direction; the published inbound counterpart exists for completeness and is called by no wave-1 flow. | CAP-P2-007 | REQ-DRI-008 | FSD P2 v3 A1.6, A2.4; D-RCV-35 U1 | Must |
| FR-P2-017 | The service SHALL move the route state of a case only through the rwb-case contract, to the retry state after the first failed attempt and to the exception state with the owner task after the last, and SHALL hold no case state of its own. | CAP-P2-005 | REQ-DRI-006 | FSD P2 v3 AC-EXC-P2-001-01, R-UNI-33, R-UNI-34 | Must |
| FR-P2-018 | The service SHALL read every ACE fact it needs through the rwb-source-data contract, one hop with a 2 second budget and a breaker, and SHALL hold no grant on the recovery schema and no grant on another service schema. | CAP-P2-001 | REQ-DRI-006 | Arch v5 slides 8, 9, 29; ADR-010; DP-05, DP-11 | Must |
| FR-P2-019 | The service SHALL run the EFS hand-over intake once per business date, only when the ACE batch for EFS and that date is complete, SHALL take its per-account key before it asks rwb-case for the case, SHALL append to the ledger idempotently, and SHALL make a partial or repeated morning provable. | CAP-P2-008 | REQ-DRI-013 | FSD P2 v3 Requirements served; BRD Program v4 REQ-DRI-013 | Must |
| FR-P2-020 | The service SHALL write a local decision record for every exception, resend and held request, on the shared decision-record topic, carrying the action, the item or delivery reference and the freshness of the data used. | CAP-P2-005 | REQ-DRI-007 | FSD P2 v3 A2.1.2; Arch v5 slide 42 EV-08; DP-03 | Must |
| FR-P2-021 | The service SHALL expose the run status of every interface and the count of held and failed items to operations, SHALL raise an alert to the named owner when an interface fails or is held, and SHALL carry a run book entry for every interface it serves. | CAP-P2-007 | REQ-DRI-007 | FSD P2 v3 A1.5; BRD Program v4 NFR-067, NFR-068 | Must |
| FR-P2-022 | The service SHALL treat a GL write-off posting as an event of the write-off module and a read-back through the ACE view, and SHALL build no Workbench file for it. | CAP-P2-001 | REQ-DRI-006, REQ-DRI-008 | FSD P2 v3 A1.1; Arch v5 slide 44 | Must |

### 6.1 Business rules that qualify the requirements

| BR ID | Rule | Source |
|---|---|---|
| BR-P2-001 | No value a business person may change is written in code; it is read from a versioned data row | FSD P2 v3 BR-P2-001; principle 1 |
| BR-P2-001-ACE | An outbound file reads ACE only through the owner's contract and never writes to ACE | FSD P2 v3 BR-P2-001-ACE, re-based by DP-05 |
| BR-P2-002 | Retry counts, intervals, patterns, owners and alert roles are interface configuration rows, never code | FSD P2 v3 BR-P2-002; story rule BR8 |
| BR-P2-003 | No personal data and no file content in an event, a request manifest or a log | Arch v5 slide 11; CTL-11; DP-09 |
| BR-P2-004 | The service owns the pattern, the item lifecycle, its own tables and the job catalog read; it owns no case, no document, no ledger and no ACE object | DP-01; Arch v5 slide 41; Ownership Map |

## 7. Non-functional requirements

Each requirement traces to a BRD non-functional requirement; a target the source does not state is held open and never invented (ASM-2672).

| ID | Requirement | Traces to | Target | Status |
|---|---|---|---|---|
| NFR-P2-001 | An interface failure after the retry limit moves the item to the exception queue with a task for a named owner, and an alert reaches that owner | NFR-026, NFR-068 | Three attempts per item, then the exception queue; alert within 15 minutes | Proposed, DL11 |
| NFR-P2-002 | An unavailable target queues the outbound action and retries it on a schedule, and the action is not lost | NFR-025 | Queue and retry; no loss | Proposed |
| NFR-P2-003 | The service is available when dispatch runs, outside business hours as well as inside them | NFR-020, NFR-021 | 99.9 percent in business hours; 99.5 percent outside, excluding the change window | Proposed, DL11 |
| NFR-P2-004 | A delivery request answers inside the caller's wait, and a consumed contract that does not answer inside its budget fails the attempt and is retried | NFR-008, NFR-011 | One hop, 2 second budget, breaker per downstream; screen under 2 seconds | Proposed |
| NFR-P2-005 | Logs, traces and metrics are produced for every delivery, retry, exception and resend, and every interface has a run book, monitoring and an alert | NFR-064, NFR-067 | Every interface and every job | Proposed |
| NFR-P2-006 | Personal data is minimised per interface and masked by role, and every read of personal data is logged | NFR-039, NFR-040, NFR-042 | Masked in use; every read | Proposed |
| NFR-P2-007 | The debt buyer tape carries only the fields the approved sale terms and the approved mask list allow | NFR-041 | Masked tape; field list open under DL26 (GAP-1545; ASM-2673) | Open, DL26 |
| NFR-P2-008 | Data is encrypted at rest and in transit, and secrets are held in the key store and never in code, configuration or prompts | NFR-052, NFR-053 | Encrypted; no secret in code | Proposed |
| NFR-P2-009 | Interface data stays in the bank's tenancy in the agreed region and every interface row carries a classification | NFR-046, NFR-047 | SCB Azure, Southeast Asia; classification per row | Proposed, DL26 |
| NFR-P2-010 | A missing, failed or late ACE batch is visible on the held item and alerts the data steward, and no Workbench load starts in its place | NFR-013, NFR-014, NFR-015 | Start of day, on the ACE business date | Proposed, DL43 |
| NFR-P2-011 | The record of a send, an exception and a resend is retained for the period set for it, is answerable to audit and is written before the action proceeds | NFR-030, NFR-036 | Not specified in the source documents (GAP-1548; ASM-2679) | Open, DL26 |
| NFR-P2-012 | A restart or a replay does not send a file twice, and a release rolls back by redeploying the previous tag | NFR-027 | Idempotent on the item key; rollback by previous tag | Proposed |
| NFR-P2-013 | No production data is used in development, and every environment fixture is synthetic | NFR-045 | Synthetic in development | Proposed |

## 8. Data requirements

The service holds the pattern and the evidence of a send. It holds no case, no document, no ledger and no ACE copy.

| Entity | Key fields | Classification | Source | Retention |
|---|---|---|---|---|
| Outbound interface row (`interface_config`) | interface ID, direction, transport, file pattern, data product, maximum attempts, retry intervals, owner role, alert role, valid from and to, version | [CONFIDENTIAL] | Reference data load by the reference data administrator | Versioned; superseded rows kept with their validity dates |
| Outbound item (`outbound_item`) | item ID, interface ID, business date, case IDs, attempt count, next attempt at, status, last error, manifest reference, idempotency key, owner role | [CONFIDENTIAL] | Created by the service on an accepted delivery request | Not specified in the source documents (GAP-1548; ASM-2679) |
| Delivery record (library) | event ID, consumer, status, attempt count, next attempt at, last error code, delivered at, task ID | [CONFIDENTIAL] | Platform outbox and inbox library | Not specified in the source documents (GAP-1548; ASM-2679) |
| Published event record (library) | event type and version, case ID, sequence, idempotency key, payload, occurred at | [CONFIDENTIAL] | Library, written in the same transaction as the state change | Per the platform event retention |
| Processed event record (library) | consumer, key, event ID, hit count, last seen at | [CONFIDENTIAL] | Library, on every consumed event | Per the platform event retention |
| Idempotency record (library) | key, operation, request hash, stored response | [CONFIDENTIAL] | Library | 24 hours for the stored response |
| Local decision record (library) | decision code, action (deliver, exception, resend, hold), item or delivery reference, freshness, versions | [CONFIDENTIAL] | Library on the shared decision-record topic | Per the decision log retention, DL26 |
| WIN notice file content | addressee name, address, notice reference, case reference | [PII] | Built at run time; held in rwb-document behind the claim-check link | Per the document retention class, DL26 |
| Debt buyer tape content | account keys, balances, arrears, sale terms, permitted personal data | [PII] and [SENSITIVE_FINANCIAL] | Built from the request manifest; held in rwb-document behind the claim-check link | Per the document retention class, DL26 |
| Reporting delivery content | case, queue, task, timer, decision and outcome facts of the business date | [SENSITIVE_FINANCIAL] | Built by rwb-reporting; delivered by this service | Held by rwb-reporting, not by this service |
| ACE facts read at run time | person key, contact key, account key, balance and batch completeness | [PII] and [SENSITIVE_FINANCIAL] | Read through the rwb-source-data contract | Not stored by this service |
| Status and role lists | outbound status list, delivery status list, transport list, direction list | [PUBLIC] | Reference data | Versioned |

Rules that apply to the data:

- The service holds no copy of an ACE row, no staging table and no load table (ADR-010; DP-01; DP-05).
- File content never travels in an event, a request manifest, a workflow input or a log; the manifest carries the file identity, the hash, the count, the claim-check link and the keys (BR-P2-003).
- A request that is held writes no item: there is no evidence of a file that was never built (FR-P2-007).
- The physical names, lengths and required flags of the held entities are the technical specification's; this PRD fixes the product content only.

## 9. Integration points

| System or service | Direction | Protocol | Owner | Notes and unknowns |
|---|---|---|---|---|
| WIN, registered mail (INT-14) | Out | File over MFT or SFTP, 16:00 daily window | rwb-integration, file built at the request of rwb-comms | Acknowledged, retried, then the exception queue. Window contract: Q-P2-02 |
| Debt buyers (INT-25) | Out | Encrypted file over MFT or SFTP, per awarded lot | rwb-integration, file requested by rwb-debtsale | First real use in wave 3 with the debt sale epic |
| rwb-reporting (legacy INT-19) | Out | Delivery request and file | rwb-integration delivers, rwb-reporting builds | No data lake and no Power BI (ASM-2663) |
| rwb-decision (legacy INT-20) | Ingest, not P2 | Event | rwb-decision | The decision and outcome feed is continuous ingest of the shared decision-record topic; P2 carries no feed |
| rwb-source-data | Out and in | REST, one hop, 2 second budget | rwb-source-data | Freshness, customer and account facts; the only reader of the ACE views |
| rwb-document | Out and in | REST | rwb-document | Stores the built file and returns the claim-check link |
| rwb-case | Out | REST | rwb-case | Route state and owner task; no P2 write to a case or a task |
| rwb-access | Out | REST | rwb-access | The platform administrator right on the read and on the resend |
| rwb-comms | In | Request and read | rwb-comms | Notice facts behind INT-14; the notice-fact contract is the owner's |
| rwb-debtsale | In | Request | rwb-debtsale | The tape request with its keys and sale terms |
| ACE common module (INT-22, INT-17, INT-18, INT-34) | Out | ACE paths | ACE team | Audit, PII and SOC logging, NSS and LINE OA, sign-in; no P2 build (GAP-1546; ASM-2674) |
| ACE ingestion | In, not P2 | ACE batch | ACE team | Every inbound source; readiness is announced by rwb-source-data (EV-26) |
| Bank scheduler (Airflow) | In | Window and business-date readiness | Platform | Opens the windows and signals readiness; P2 registers no schedule |
| Key store | Out | Managed identity | Platform | Interface credentials and PGP keys; never in code |

Unknowns carried as questions: the exact trigger contract of the two file windows (Q-P2-02), the interface-level volume and size targets (Q-P2-03), the mask list of the tape (Q-P2-04), the retention of the transmission records (Q-P2-05), the boundary with the consumer-side compositions (Q-P2-06) and the same-day interface list (Q-P2-01).

## 10. Release slicing proposal

Waves follow Architecture v5 slide 38 and the wave map of the Story Template and Rules section R5.6. Dates are copied unchanged from BRD Program v4 section 8 and are tentative.

| Slice | Wave | Release (tentative) | Capabilities | Rationale |
|---|---|---|---|---|
| Platform enablers | 0 | The sources give no date for wave 0 (Arch v5 slide 38 names it the enabler wave) | None of this PRD; the platform epics supply the service template, the outbox and inbox library, the workflow kit, the schema and login, the Kafka topic and ACLs, the gateway route and observability | Nothing of this service is buildable before its platform enablers exist |
| MVP | 1 (Epic 1, EP01) | 30 November 2026 (tentative) | CAP-P2-001, CAP-P2-002, CAP-P2-003 (built; activated in wave 3), CAP-P2-004, CAP-P2-005, CAP-P2-006, CAP-P2-007 | The outbound pattern, the WIN file and the reporting delivery, with the freshness hold, the retry ladder, the exception queue, the owner task, the resend and duplicate handling, are the whole of the Epic 1 promise for this service: a file leaves, or its failure is visible and owned |
| Wave 2 increment | 2 (Epic 2, EP02 and EP03) | 31 December 2026 (tentative) | CAP-P2-008 | The hand-over intake depends on the EFS batch and on the case creation step; it adds orchestration only and needs no new interface |
| Wave 3 activation and reuse | 3 (Epic 4 and Epic 5, EP04 and EP05) | 28 February 2027 (tentative) and 31 March 2027 (tentative) | CAP-P2-003 activated; no new capability for the other uses | The debt buyer tape can only be exercised when the debt sale lot is awarded, so the capability built in wave 1 delivers its business value here; the ALS settlement posting (legacy key RWB-E4-046, release 28 February 2027 (tentative)) is a new interface row on the same pattern and not a new capability |
| Wave 4 reuse | 4 (Epic 6 to Epic 8, EP06 to EP08) | 30 April 2027 (tentative), 31 May 2027 (tentative) and 30 June 2027 (tentative) | No new capability | Further outbound interfaces reuse the pattern as interface rows and delivery requests; the capability set of this PRD is closed at wave 3 |

Slicing rules:

- A capability ships whole: a slice never ships a retry without an exception queue or an exception queue without a resend.
- CAP-P2-003 ships built in wave 1 and activated in wave 3; a build without its business trigger is a defect of the slice, not a stretch.
- No slice of this PRD starts before the platform enablers of wave 0 exist.
- A capability that cannot meet its slice is cut from the slice and reported, never shipped partly.

## 11. Acceptance criteria and validation evidence

```gherkin
Feature: P2 rwb-integration product behaviour

  Background:
    Given the interface configuration version in force holds interface "INT-14" with direction OUTBOUND, max attempts 3 and its retry intervals
    Given the business date is 2026-11-10
    Given every consumed contract is the published contract of its owner

  Scenario: AC-P2-001 The WIN file leaves with the addressee read through the owner of the facts
    Given 85 approved notices for business date 2026-11-10, each with a person key and a contact key
    When the WIN file is built in the 16:00 window at the request of the owning service
    Then the item records the ACE business date 2026-11-10 and a complete batch for that date
    And each addressee and address is read through the rwb-source-data contract by contact key
    And no statement of the build reads an ACE table or an ACE view
    And the file is announced as FileDelivered when the target acknowledges it

  Scenario: AC-P2-002 The debt buyer tape leaves from the request manifest only
    Given an awarded lot whose request carries 120 account keys and the sale terms
    When the tape is built and sent
    Then the tape carries the 120 keys of the request and only the personal data the approved terms and mask list allow
    And the account facts are read through the rwb-source-data contract
    And the file is encrypted and sent over the agreed transport
    And no table of another service and no ACE view is read

  Scenario: AC-P2-003 The reporting delivery replaces the lake extract
    Given a business date with case, queue, task, timer, decision and outcome changes
    When rwb-reporting asks for the delivery of its extract
    Then the extract is delivered on the one pattern and acknowledged
    And no data lake file, Power BI feed or lake delivery row exists
    And a failure holds the delivery, alerts the named owner and is retried in the next window

  Scenario: AC-P2-004 A file is held when the ACE batch is not complete
    Given the ACE batch for ALS and business date 2026-11-10 is not complete
    When a delivery is requested for that business date
    Then the request is held with the message that the product is from 2026-11-10 and today's data is not yet complete
    And no outbound item exists for the request
    And the hold is visible to the data steward and to the owner role

  Scenario: AC-P2-005 A failed transfer is retried, then owned
    Given the WIN file of business date 2026-11-10 and a transport that fails on attempts 1, 2 and 3
    When the attempts run
    Then attempt 2 follows attempt 1 by 5 minutes and attempt 3 follows attempt 2 by 15 minutes
    And the item is in the retry state after attempt 1 and in the exception state after attempt 3
    And FileFailed is published
    And each case of the file is in the exception route state with exactly one task for the platform administrator role
    And the item appears in the exception queue with the message that the file was not sent after 3 attempts

  Scenario: AC-P2-006 A resend is possible, audited and refused when it is not allowed
    Given an item in the exception state after 3 attempts
    When a platform administrator resends it
    Then the item is PENDING with an attempt count of zero
    And the resend is written to the ACE audit log with the user and the time
    And the response confirms that the change was saved
    When another user resends the same item again before it is in the exception state
    Then the resend is refused and nothing changes

  Scenario: AC-P2-007 An acknowledgement closes the item once
    Given an item in the sent state
    When the target acknowledges the file
    Then the item is in the acknowledged state
    And FileDelivered is published once
    And a repeated acknowledgement changes neither the item nor the event count

  Scenario: AC-P2-008 A duplicate event is ignored and counted
    Given a consumer that has processed the event key of a booking confirmation
    When the same event arrives again with the same key
    Then the consumer does not act
    And the hit count for that key is 2
    Given the ACE readiness event for ALS and business date 2026-11-10 has been processed
    When it arrives again with the same key
    Then no second hand-over run starts for that source and business date

  Scenario: AC-P2-009 Only outbound interfaces exist
    Given the interface configuration of the service
    When the rows are reviewed
    Then every row has direction OUTBOUND
    And a row with an inbound direction is refused by the load
    And no inbound folder, inbound file check, inbound run record or sign-off exists
    And the published inbound counterpart is called by no wave-1 flow

  Scenario: AC-P2-010 The service crosses no boundary
    Given the code and the migrations of the service
    When the boundary check runs
    Then no statement reads an ACE view, a public table or another service's table
    And no foreign key leaves the service schema
    And no case row and no task row is written by this service
    And no file system or transfer call sits outside the one transport component

  Scenario: AC-P2-011 The hand-over runs once per morning and is provable
    Given the ACE batch for EFS and business date 2026-11-10 is complete and the readiness event has arrived once
    When the hand-over runs
    Then the per-account key is taken before the case is asked for
    And the ledger append is idempotent on its own key
    And a repeat of the same morning starts no second run
    And a partial morning is visible as partial

  Scenario: AC-P2-012 Nothing personal leaves in a message
    Given every published event, request manifest and activity input of the service
    When the schema and the fixtures are reviewed
    Then no element can carry a name, an address, an identity number or file content
    And the file is referenced only by its claim-check link and its hash
    And every read of personal data is logged

  Scenario: AC-P2-013 An owner hears about a failure in time
    Given an interface that fails or is held
    When the alert rule evaluates
    Then an alert reaches the named owner role within 15 minutes
    And the interface has a run book entry with purpose, schedule, owner and restart steps

  Scenario: AC-P2-014 A restart does not send a file twice
    Given an item in the sent state and a service restart before the acknowledgement
    When the delivery resumes
    Then the file is sent once and the attempt count is 1
    And the acknowledgement still closes the same item
```

### 11.1 Criterion to requirement mapping

| AC | FR and NFR | Origin in the source |
|---|---|---|
| AC-P2-001 | FR-P2-002, FR-P2-003, FR-P2-012, FR-P2-018; NFR-P2-004 | FSD P2 v3 AC-ALT-P2-001-03, AC-P2-001-01 |
| AC-P2-002 | FR-P2-004, FR-P2-018; NFR-P2-007, NFR-P2-008 | FSD P2 v3 A1.5 INT-25, AC-P2-001-01 |
| AC-P2-003 | FR-P2-005, FR-P2-021 | FSD P2 v3 A1.5 INT-19; Arch v5 slides 37 and 44 |
| AC-P2-004 | FR-P2-007, FR-P2-020; NFR-P2-010 | FSD P2 v3 VR-P2-001-1, A1.4 |
| AC-P2-005 | FR-P2-008, FR-P2-009, FR-P2-017; NFR-P2-001 | FSD P2 v3 AC-EXC-P2-001-01 |
| AC-P2-006 | FR-P2-010, FR-P2-020; NFR-P2-011 | FSD P2 v3 AC-EXC-P2-001-04 |
| AC-P2-007 | FR-P2-012; NFR-P2-012 | Arch v5 slide 43; FSD P2 v3 A2.1.2 |
| AC-P2-008 | FR-P2-013, FR-P2-014 | FSD P2 v3 AC-EXC-P2-001-03, AC-EXC-P2-007-07 |
| AC-P2-009 | FR-P2-015, FR-P2-016 | FSD P2 v3 A1.6, A2.4; D-RCV-35 U1 |
| AC-P2-010 | FR-P2-017, FR-P2-018; NFR-P2-006 | Arch v5 slides 8, 9, 29; DP-01, DP-05 |
| AC-P2-011 | FR-P2-019 | FSD P2 v3 Requirements served, REQ-DRI-013 |
| AC-P2-012 | FR-P2-001, FR-P2-012; NFR-P2-006, NFR-P2-009 | Arch v5 slide 11; BRD NFR-039, NFR-040, NFR-042 |
| AC-P2-013 | FR-P2-021; NFR-P2-001, NFR-P2-005 | BRD NFR-067, NFR-068 |
| AC-P2-014 | FR-P2-001, FR-P2-012; NFR-P2-012 | BRD NFR-027; DP-09 |

### 11.2 Validation evidence required before a capability is called done

| Evidence | What it shows |
|---|---|
| Contract test of the delivery request and of the two events | The manifest, the outcomes and the no-personal-data rule hold |
| Contract test of the consumed contracts against their fakes | The service builds without another service being finished |
| Boundary test | No ACE view, no cross-schema statement, no foreign key out of the schema, no transfer call outside the one component |
| Freshness test | A held request writes no item and shows the stale-data message |
| Failure test | The retry ladder, the exception state, the single owner task and the alert |
| Resend test | Status, attempt count, audit record and the refusal of a resend that is not allowed |
| Replay test | One send, attempt count 1, one acknowledgement |
| Operations evidence | A run book entry, a dashboard and an alert per interface |
| Audit evidence | The send, the exception and the resend answerable for a named case population |

## 12. Open questions

Questions carried forward from the BRD, plus product-level questions this PRD raises. No answer is invented.

| ID | Question | Owner | Needed by | Impact if unanswered |
|---|---|---|---|---|
| Q-P2-01 | Which interfaces need same-day data, and which take the daily batch? The BRD leaves DL06 open and ACE has no real time feed today; the named same-day triggers are a case transferred from EFS, a payment received and a legal event | Solution architect with the ACE team lead | Before the wave-1 release | A same-day interface cannot be promised and a file waits for the next batch |
| Q-P2-02 | Who owns a retry, the bank scheduler that owns the window and the transfer, or the service that owns the attempt ladder and the exception queue? DL11 has no answer, and both statements are in the source set (GAP-1537) | Solution architect with the IT lead | Before the wave-1 release | A duplicate retry sends a file twice, or a failed file is never retried |
| Q-P2-03 | What is the largest file, the records per file, the daily tape volume, the window length and the extract size? No source states an interface target (GAP-1544) | Solution architect with Risk | Before the wave-1 release | The interface NFRs cannot be tested and stay open |
| Q-P2-04 | Which fields of the debt buyer tape are masked, and which personal data do the sale terms allow? DL26 is open (GAP-1545) | Compliance with Legal | Before the wave-3 activation | An unmasked field in the tape is a reportable breach |
| Q-P2-05 | How long are an outbound item, a delivery record, a manifest and an acknowledgement kept? DL26 is open (GAP-1548) | Compliance | Before the wave-1 release | A purge before the case closes destroys the evidence of a send |
| Q-P2-06 | Are the consumer-side compositions assigned to rwb-integration in the later wave story slices (ACE plan status, composed case list, credit pack, queue write interface, ALS settlement posting) in this PRD or in the PRD of the owning module? (GAP-1541) | Product Owner with the solution architect | Before the wave-2 release | Duplicated or missing product requirements for the same screen |
| Q-P2-07 | Does the ACE team accept the scope and dates of the ACE additions (14 tables, 12 columns, 80 source fields) that the views behind these interfaces depend on? DL43 is open | ACE team lead | 21 November 2026, per the BRD | A file that needs a Tier 2 field stays behind its flag |

## 13. Approval

| Role | Name | Decision | Date | Signature |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

Approval is open. The BRD carries no approval record and no status field (GAP-1543; ASM-2661), so this PRD is issued as Draft and the requirements approval gate is not evidenced.

## Appendix A. Traceability summary

The master matrix `requirement/Traceability_Matrix.md` in the AI-SDLC workspace is assembler-owned; the rows this PRD contributes are below.

| BR ID | CAP | FR and NFR | AC |
|---|---|---|---|
| REQ-DRI-006 | CAP-P2-001, CAP-P2-002, CAP-P2-003, CAP-P2-004 | FR-P2-001, FR-P2-002, FR-P2-004, FR-P2-017, FR-P2-018, FR-P2-022 | AC-P2-001, AC-P2-002, AC-P2-003, AC-P2-010 |
| REQ-DRI-007 | CAP-P2-001, CAP-P2-002, CAP-P2-003, CAP-P2-004, CAP-P2-005, CAP-P2-006, CAP-P2-007 | FR-P2-003, FR-P2-005, FR-P2-006, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-011, FR-P2-012, FR-P2-013, FR-P2-015, FR-P2-020, FR-P2-021 | AC-P2-003, AC-P2-005, AC-P2-006, AC-P2-007, AC-P2-008, AC-P2-009, AC-P2-013 |
| REQ-DRI-008 | CAP-P2-005, CAP-P2-006, CAP-P2-007 | FR-P2-007, FR-P2-014, FR-P2-016, FR-P2-022 | AC-P2-004, AC-P2-008, AC-P2-009 |
| REQ-DRI-013 | CAP-P2-008 | FR-P2-019 | AC-P2-011 |
| NFR-008, NFR-011 | All | NFR-P2-004 | AC-P2-001 |
| NFR-013, NFR-014, NFR-015 | CAP-P2-005 | NFR-P2-010 | AC-P2-004 |
| NFR-020, NFR-021 | All | NFR-P2-003 | AC-P2-013 |
| NFR-025, NFR-026, NFR-068 | CAP-P2-005, CAP-P2-007 | NFR-P2-001, NFR-P2-002 | AC-P2-005, AC-P2-013 |
| NFR-027 | All | NFR-P2-012 | AC-P2-007, AC-P2-014 |
| NFR-030, NFR-036 | CAP-P2-005 | NFR-P2-011 | AC-P2-006 |
| NFR-039, NFR-040, NFR-041, NFR-042 | CAP-P2-002, CAP-P2-003 | NFR-P2-006, NFR-P2-007 | AC-P2-002, AC-P2-012 |
| NFR-045, NFR-046, NFR-047 | All | NFR-P2-009, NFR-P2-013 | AC-P2-012 |
| NFR-052, NFR-053 | CAP-P2-001, CAP-P2-003 | NFR-P2-008 | AC-P2-002, AC-P2-012 |
| NFR-064, NFR-067 | CAP-P2-007 | NFR-P2-005 | AC-P2-013 |

### A.1 Business requirement coverage

| BR ID | FR count | Status |
|---|---|---|
| REQ-DRI-006 | 6 | Covered |
| REQ-DRI-007 | 12 | Covered |
| REQ-DRI-008 | 4 | Covered |
| REQ-DRI-013 | 1 | Covered |

No P2 business requirement of the BRD is without a functional requirement. One obligation is carried without a requirement of its own: REQ-DRI-006 and REQ-DRI-008 are also discharged by rwb-source-data, which is the only reader of the ACE views, so the P2 requirement is the negative one (FR-P2-016, FR-P2-018, FR-P2-022).
